"""Sound design v2 mix for a short: processed voice + music bed + code-made effects, mastered to -14 LUFS.

Usage:
  python3 -I remix.py --project <video-dir> --video renders/epNNN.mp4 --out renders/epNNN-sound.mp4
      (reads the voice and music elements, start times and the music automation from <video-dir>/index.html;
       cues from <video-dir>/sfx-cues.json; kit next to this script)
  python3 -I remix.py --video renders/epNNN.mp4 --voice assets/narration_norm.wav --music assets/music.mp3 \
      --cues sfx-cues.json --kit <tools/sfx/kit> --out renders/epNNN-sound-v2.mp4 \
      [--music-points "0:0.28,53.1:0.28,53.7:0.5"] [--sfx-db -16] [--voice-at 0]

- Voice chain ("bold", approved 16 Nov): high-pass 80 Hz, presence +4.5 dB at 4.5 kHz, air +2.5 dB above 9 kHz, de-ess, 2.5:1 compression.
- Effects: each cue {t, s, g} drops the kit sound at t, scaled by g and by --sfx-db (default -12 dB).
  Tiny deterministic level jitter (±1 dB) avoids a machine-gun feel. No cue lands in the first 0.15 s.
- Music: the bed with its volume automation (linear between points), 0.3 s fade-in, 1.2 s fade-out.
- Master: gain to -14 LUFS integrated, limiter at -1 dBTP. The video stream is copied untouched.
"""
import argparse, json, os, subprocess, sys, tempfile
import numpy as np
from scipy.io import wavfile

SR = 48000


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-1500:])
    return r


def load(path, dur=None):
    """Decode any audio to 48 kHz mono float via ffmpeg."""
    tmp = tempfile.mktemp(suffix=".wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", path, "-ac", "1", "-ar", str(SR), "-c:a", "pcm_f32le", tmp])
    sr, x = wavfile.read(tmp); os.remove(tmp)
    x = x.astype(np.float32)
    if dur is not None:
        n = int(dur * SR); x = np.pad(x, (0, max(0, n - len(x))))[:n]
    return x


def ffilter(x, chain):
    a, b = tempfile.mktemp(suffix=".wav"), tempfile.mktemp(suffix=".wav")
    wavfile.write(a, SR, x.astype(np.float32))
    run(["ffmpeg", "-v", "error", "-y", "-i", a, "-af", chain, "-c:a", "pcm_f32le", b])
    _, y = wavfile.read(b); os.remove(a); os.remove(b)
    return y.astype(np.float32)[: len(x)] if len(y) >= len(x) else np.pad(y.astype(np.float32), (0, len(x) - len(y)))


def lufs(path):
    e = run(["ffmpeg", "-hide_banner", "-i", path, "-af", "loudnorm=print_format=summary", "-f", "null", "-"]).stderr
    return float([l for l in e.splitlines() if "Input Integrated" in l][0].split()[2])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project"); ap.add_argument("--video", required=True); ap.add_argument("--voice"); ap.add_argument("--music")
    ap.add_argument("--cues"); ap.add_argument("--kit", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "kit")); ap.add_argument("--out", required=True)
    ap.add_argument("--music-points", default="0:0.28"); ap.add_argument("--sfx-db", type=float, default=-12.0)
    ap.add_argument("--voice-at", type=float, default=0.0); ap.add_argument("--voice-gain", type=float, default=1.0)
    a = ap.parse_args()
    if a.project:
        import html as _h, re as _re
        page = open(os.path.join(a.project, "index.html")).read()
        def audio(id_):
            m = _re.search(r'<audio[^>]*id="%s"[^>]*>' % id_, page, _re.S)
            if not m:
                sys.exit(f"no <audio id={id_}> in index.html")
            tag = m.group(0); g = lambda k: (_re.search(k + r'="([^"]*)"', tag) or [None, None])[1]
            return g("src"), float(g("data-start") or 0), g("data-automation"), float(g("data-volume") or 1)
        vsrc, vat, _, vvol = audio("vo"); msrc, _, mauto, mvol = audio("music")
        a.voice = a.voice or os.path.join(a.project, vsrc); a.voice_at = vat; a.voice_gain = vvol
        a.music = a.music or os.path.join(a.project, msrc)
        a.cues = a.cues or os.path.join(a.project, "sfx-cues.json")
        if mauto and a.music_points == "0:0.28":
            pts = json.loads(_h.unescape(mauto))["lanes"][0]["points"]
            a.music_points = ",".join(f"{p['t']}:{p['v'] * mvol}" for p in pts)
        elif a.music_points == "0:0.28":
            a.music_points = f"0:{mvol}"
    if not (a.voice and a.music and a.cues):
        sys.exit("give --project, or --voice, --music and --cues")
    dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", a.video]).stdout)
    n = int(dur * SR)

    voice = np.zeros(n, np.float32)
    v = load(a.voice) * a.voice_gain; i = int(a.voice_at * SR); voice[i:i + len(v)] = v[: n - i]
    voice = ffilter(voice, "highpass=f=80,equalizer=f=4500:t=q:w=1.0:g=4.5,highshelf=f=9000:g=2.5,deesser=i=0.4,"
                           "acompressor=threshold=-22dB:ratio=2.5:attack=5:release=90:makeup=1.5")

    music = load(a.music, dur)
    pts = sorted((float(p.split(":")[0]), float(p.split(":")[1])) for p in a.music_points.split(","))
    tt = np.arange(n) / SR
    music *= np.interp(tt, [p[0] for p in pts] + [dur], [p[1] for p in pts] + [pts[-1][1]]).astype(np.float32)
    fi, fo = int(0.3 * SR), int(1.2 * SR)
    music[:fi] *= np.linspace(0, 1, fi); music[-fo:] *= np.linspace(1, 0, fo)

    sfx = np.zeros(n, np.float32); cues = json.load(open(a.cues)); cues = cues["cues"] if isinstance(cues, dict) else cues
    base = 10 ** (a.sfx_db / 20); cache = {}
    for k, c in enumerate(cues):
        if c["t"] < 0.15:
            continue
        if c["s"] not in cache:
            if not os.path.exists(os.path.join(a.kit, c["s"] + ".wav")):
                sys.exit(f"unknown sound '{c['s']}' at {c['t']} s; kit sounds: " + ", ".join(sorted(f[:-4] for f in os.listdir(a.kit))))
            sr, s = wavfile.read(os.path.join(a.kit, c["s"] + ".wav")); cache[c["s"]] = s.astype(np.float32)
        s = cache[c["s"]] * base * c.get("g", 1.0) * 10 ** ((((k * 7919) % 21) - 10) / 10 / 20)
        j = int(c["t"] * SR); sfx[j:j + len(s)] += s[: max(0, n - j)]

    mix = voice + music + sfx
    tmp = tempfile.mktemp(suffix=".wav"); wavfile.write(tmp, SR, mix.astype(np.float32))
    gain = -14.0 - lufs(tmp)
    master = tempfile.mktemp(suffix=".wav")
    run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"volume={gain:.2f}dB,alimiter=limit=0.89:level=false:attack=3:release=60",
         "-ac", "2", "-c:a", "pcm_s16le", master])
    run(["ffmpeg", "-v", "error", "-y", "-i", a.video, "-i", master, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", a.out])
    os.remove(tmp); os.remove(master)
    ticks = sum(1 for c in cues if c["s"].startswith("digit"))
    print(f"{a.out}: {len(cues)} cues, {(len(cues) - ticks) / dur:.2f}/s without counter ticks; master {lufs(a.out):.1f} LUFS (gain {gain:+.1f} dB)")


if __name__ == "__main__":
    main()
