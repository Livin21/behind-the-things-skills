"""Insert silence into a chapter's voice file and shift its word timings to match.

Usage:  python3 -I splice_pause.py <chNN_norm.wav> <chNN.transcript.json> <at_seconds> <add_seconds>

- <at_seconds>: voice-time point to split at; choose the middle of the existing pause
  (find it with: ffmpeg -i chNN_norm.wav -af silencedetect=noise=-40dB:d=0.3 -f null -).
- Writes the wav in place (keeps <name>.orig.wav the first time) and shifts every word that starts at or after
  <at_seconds> by <add_seconds>. Run fix_timings.py BEFORE this, never after (it would refresh its raw copy).
- Then: update the chapter's vo_duration and duration in chapters.json, add a "drops" entry to bed.json spanning
  the new pause (previous word's end -> next word's start), and re-run build_timeline.py, build_bed.py, build_srt.py.
"""
import json, os, shutil, subprocess, sys


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    wav, tr, at, add = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4])
    orig = wav.replace(".wav", ".orig.wav")
    if not os.path.exists(orig):
        shutil.copy(wav, orig)
    info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=channels,sample_rate", "-of", "csv=p=0", orig],
                          capture_output=True, text=True).stdout.strip().split(",")
    sr, ch = info[0], "mono" if info[1] == "1" else "stereo"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", orig, "-filter_complex",
                    f"[0]atrim=0:{at},asetpts=PTS-STARTPTS[a];aevalsrc=0:c={ch}:s={sr}:d={add}[s];"
                    f"[0]atrim=start={at},asetpts=PTS-STARTPTS[b];[a][s][b]concat=n=3:v=0:a=1", "-ar", sr, wav], check=True)
    words = json.load(open(tr))
    n = 0
    for w in words:
        if w["start"] >= at:
            w["start"] = round(w["start"] + add, 3); w["end"] = round(w["end"] + add, 3); n += 1
    json.dump(words, open(tr, "w"), indent=1)
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", wav],
                             capture_output=True, text=True).stdout)
    print(f"inserted {add}s at {at}s; shifted {n} words; new length {d:.3f}s (update vo_duration and duration)")


if __name__ == "__main__":
    main()
