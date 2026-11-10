"""Build the long-form music bed: level each track, crossfade sections at chapter boundaries, bake in drops/lifts.

Usage:  python3 -I build_bed.py bed.json chapters.json

bed.json:
{
  "target_lufs": -16.9,                       # each source track is levelled to this first (gain only)
  "xfade": 3.0,                               # crossfade length, centred on each boundary
  "sections": [                               # in order; "until" = chapter id whose START ends the section
    {"src": "assets/music/m1.mp3", "until": "ch03"},
    {"src": "assets/music/m2.mp3", "until": "ch05"},
    {"src": "assets/music/m3.mp3", "until": "ch07"},
    {"src": "assets/music/m1.mp3", "align": "end", "end_trim": 1.45}   # last section: end on the track's own (audible) ending
  ],
  "drops": [{"chapter": "ch05", "from": 46.03, "to": 48.24}],   # chapter-relative VOICE times (vo_at is added)
  "lift":  {"chapter": "ch07", "after_vo": 0.4, "gain_db": 5.0}  # raise the bed after the last word (end card)
}
Writes assets/music/bed.mp3 at the full video length (chapters + tail). Prints section ranges.
"""
import json, subprocess, sys


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        sys.exit(r.stderr[-2000:])
    return r


def lufs(p):
    err = run(["ffmpeg", "-hide_banner", "-i", p, "-af", "loudnorm=print_format=summary", "-f", "null", "-"]).stderr
    return float([l for l in err.splitlines() if "Input Integrated" in l][0].split()[2])


def dur(p):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p]).stdout)


def main():
    bed, cfg = json.load(open(sys.argv[1])), json.load(open(sys.argv[2]))
    starts, t = {}, 0.0
    for c in cfg["chapters"]:
        starts[c["id"]] = (t, c); t += c["duration"]
    T = t + cfg.get("tail", 0)
    X = bed.get("xfade", 3.0)
    secs, inputs, filt = bed["sections"], [], []
    bounds = [starts[s["until"]][0] for s in secs[:-1]]
    edges = [0.0] + bounds + [T]
    for k, s in enumerate(secs):
        a, b = edges[k], edges[k + 1]
        length = (b - a) + (X / 2 if k > 0 else 0) + (X / 2 if k < len(secs) - 1 else 0)
        src_len = dur(s["src"])
        if length > src_len + 0.01:
            sys.exit(f"section {k} needs {length:.2f}s but {s['src']} is {src_len:.2f}s")
        # "align": "end" lines the section up with the track's last *audible* moment ("end_trim" s of tail silence skipped)
        off = src_len - length - s.get("end_trim", 0.0) if s.get("align") == "end" else 0.0
        gain = bed.get("target_lufs", -16.9) - lufs(s["src"])
        inputs += ["-i", s["src"]]
        filt.append(f"[{k}:a]atrim=start={off:.3f}:duration={length:.3f},asetpts=PTS-STARTPTS,volume={gain:.2f}dB,aformat=sample_rates=48000:channel_layouts=stereo[s{k}]")
        print(f"section {k}: {s['src']} [{off:.2f}..{off + length:.2f}] -> video {max(0, a - (X / 2 if k else 0)):.2f}..{b + (X / 2 if k < len(secs) - 1 else 0):.2f}  gain {gain:+.2f} dB")
    cur = "s0"
    for k in range(1, len(secs)):
        filt.append(f"[{cur}][s{k}]acrossfade=d={X}:c1=tri:c2=tri[x{k}]"); cur = f"x{k}"
    # drops and the end lift as one piecewise-linear gain expression
    terms = []
    for d in bed.get("drops", []):
        st, c = starts[d["chapter"]]; a = st + c.get("vo_at", 0) + d["from"]; b = st + c.get("vo_at", 0) + d["to"]
        terms.append(f"max(0,min(1,max(({a + 0.35:.3f}-t)/0.35,(t-{b - 0.35:.3f})/0.35)))")
        print(f"drop: {a:.2f}..{b:.2f}")
    expr = "*".join(terms) if terms else "1"
    lf = bed.get("lift")
    if lf:
        st, c = starts[lf["chapter"]]; a = st + c.get("vo_at", 0) + c["vo_duration"] + lf.get("after_vo", 0.4)
        g = 10 ** (lf.get("gain_db", 5.0) / 20)
        expr = f"({expr})*(1+({g - 1:.4f})*max(0,min(1,(t-{a:.3f})/1.2)))"
        print(f"lift: +{lf.get('gain_db', 5.0)} dB from {a:.2f}")
    filt.append(f"[{cur}]volume='{expr}':eval=frame,atrim=duration={T:.3f},afade=t=out:st={T - 0.4:.3f}:d=0.4[out]")
    out = "assets/music/bed.mp3"
    run(["ffmpeg", "-hide_banner", "-y", *inputs, "-filter_complex", ";".join(filt), "-map", "[out]", "-c:a", "libmp3lame", "-b:a", "192k", out])
    print(f"wrote {out}: {dur(out):.2f}s (video {T:.2f}s)")


if __name__ == "__main__":
    main()
