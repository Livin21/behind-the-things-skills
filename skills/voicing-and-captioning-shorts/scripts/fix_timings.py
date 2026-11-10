"""Repair Whisper word timings against the audio's real pauses.

Whisper tends to start the first word after a pause late (by up to ~0.5 s) and to stretch
the last word before a pause into the silence. Captions and cuts timed from those values
appear late and hang over pauses. This snaps them to measured silences.

Usage:
  python3 -I fix_timings.py <narration.wav|mp3> <transcript.json> [--noise -35] [--min 0.18]

- Keeps the untouched transcript as <transcript>.raw.json (only the first time).
- Prints every change; fails if the result is not monotonic.
Transcript format: [{"text": str, "start": float, "end": float, ...}, ...] (npx hyperframes transcribe).
"""
import json, os, re, subprocess, sys


def silences(audio, noise, min_d):
    out = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", audio, "-af", f"silencedetect=noise={noise}dB:d={min_d}", "-f", "null", "-"],
        capture_output=True, text=True,
    ).stderr
    starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", out)]
    ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", out)]
    return list(zip(starts, ends))


def main():
    args = sys.argv[1:]
    if len(args) < 2:
        sys.exit(__doc__)
    audio, path = args[0], args[1]
    noise = float(args[args.index("--noise") + 1]) if "--noise" in args else -35
    min_d = float(args[args.index("--min") + 1]) if "--min" in args else 0.18
    raw = path.replace(".json", ".raw.json")
    if not os.path.exists(raw):
        with open(path) as f, open(raw, "w") as g:
            g.write(f.read())
    words = json.load(open(raw))
    for s, e in silences(audio, noise, min_d):
        # the first word whose onset falls between the silence midpoint and 0.6 s after it ends
        cand = [i for i, w in enumerate(words) if (s + e) / 2 - 0.05 <= w["start"] <= e + 0.6]
        if cand:
            i = cand[0]
            if abs(words[i]["start"] - e) > 0.03:
                print(f"onset  {words[i]['text']!r:>16}: {words[i]['start']:.2f} -> {e:.2f}")
                words[i]["start"] = round(e, 3)
        # any word ending inside this silence ends where the silence starts
        for w in words:
            if w["start"] < s < w["end"] <= e + 0.05 and w["end"] - s > 0.01:
                print(f"end    {w['text']!r:>16}: {w['end']:.2f} -> {s:.2f}")
                w["end"] = round(s, 3)
    bad = [(a["text"], b["text"]) for a, b in zip(words, words[1:]) if b["start"] < a["start"] or a["end"] < a["start"]]
    if bad:
        sys.exit(f"Non-monotonic timings after repair, fix by hand: {bad[:5]}")
    json.dump(words, open(path, "w"), indent=1)
    print(f"wrote {path} ({len(words)} words); original kept at {raw}")


if __name__ == "__main__":
    main()
