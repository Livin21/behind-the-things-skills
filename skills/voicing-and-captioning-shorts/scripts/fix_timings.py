"""Repair Whisper word timings around the audio's real pauses (targeted, not global).

Whisper is accurate for most words; it drifts at pauses:
  (a) the first word after a pause starts late,
  (b) a sentence's last word is pushed into - or entirely inside - the following silence,
  (c) a word ends inside, or spans, a pause.
This fixes only those words, using silences measured with ffmpeg silencedetect.

Usage:
  python3 -I fix_timings.py <narration.wav|mp3> <transcript.json> [--noise -35] [--min 0.18]

- First run saves the untouched transcript as <transcript>.raw.json plus the audio's hash.
  Re-runs start from that raw copy (idempotent). If the audio changed (re-voice), the raw copy
  is refreshed from the current transcript automatically.
- Do hand repairs AFTER the last run; a re-run discards them.
- Prints each change of 0.02 s or more; fails on out-of-order or overlapping words.
Transcript format: [{"text": str, "start": float, "end": float, ...}] (npx hyperframes transcribe).
"""
import hashlib, json, os, re, subprocess, sys

ENDS_SENTENCE = re.compile(r"[.?!]['\")]*$")
MIN_WORD = 0.12


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


def silences(audio, noise, min_d):
    err = run(["ffmpeg", "-hide_banner", "-i", audio, "-af", f"silencedetect=noise={noise}dB:d={min_d}", "-f", "null", "-"]).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(s, e))


def load_raw(audio, path):
    raw, tag = path.replace(".json", ".raw.json"), path.replace(".json", ".raw.sha1")
    digest = hashlib.sha1(open(audio, "rb").read()).hexdigest()
    if not (os.path.exists(raw) and os.path.exists(tag) and open(tag).read().strip() == digest):
        if os.path.exists(raw):
            print("audio changed since the raw copy was made: refreshing raw from the current transcript")
        with open(path) as f, open(raw, "w") as g:
            g.write(f.read())
        open(tag, "w").write(digest)
    return json.load(open(raw)), raw


def main():
    a = sys.argv[1:]
    if len(a) < 2:
        sys.exit(__doc__)
    audio, path = a[0], a[1]
    noise = float(a[a.index("--noise") + 1]) if "--noise" in a else -35
    min_d = float(a[a.index("--min") + 1]) if "--min" in a else 0.18
    words, raw = load_raw(audio, path)
    total = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]).stdout.strip())
    orig = [dict(w) for w in words]
    moved = set()

    def say(i, what, old, new):
        if abs(old - new) >= 0.02:
            print(f"{what:<6} {words[i]['text']!r:>16}: {old:.2f} -> {new:.2f}")

    for s, e in silences(audio, noise, min_d):
        cands = [i for i, w in enumerate(words) if i not in moved and (s + e) / 2 - 0.05 <= w["start"] <= e + 0.6]
        # (b) sentence-final word sitting in/just after the pause, with the next word after the pause: it belongs before
        while cands and ENDS_SENTENCE.search(words[cands[0]]["text"]) and cands[0] + 1 < len(words) \
                and words[cands[0] + 1]["start"] >= e - 0.1:
            i = cands.pop(0)
            prev_end = words[i - 1]["end"] if i else 0.0
            if prev_end > s - MIN_WORD:   # no room before the pause: leave this word where it is
                moved.add(i); continue
            dur = min(max(orig[i]["end"] - orig[i]["start"], 0.2), 0.6)
            ns = max(prev_end, s - dur)
            say(i, "move", words[i]["start"], ns)
            words[i]["start"], words[i]["end"] = round(ns, 3), round(s, 3)
            moved.add(i)
        # (a) first word after the pause starts when the pause ends
        if cands:
            i = cands[0]
            if abs(words[i]["start"] - e) > 0.03:
                say(i, "onset", words[i]["start"], e)
                words[i]["start"] = round(e, 3)
            moved.add(i)
        # (c) words ending inside, or spanning, this pause end where it starts
        for i, w in enumerate(words):
            if w["start"] < s < w["end"] and (w["end"] <= e + 0.05 or w["end"] > e):
                if s - w["start"] >= MIN_WORD:
                    say(i, "end", w["end"], s)
                    w["end"] = round(s, 3)

    # tidy: minimum length, no overlaps, nothing past the audio
    for i, w in enumerate(words):
        if w["end"] > total:
            say(i, "clamp", w["end"], total); w["end"] = round(total, 3)
        if w["end"] - w["start"] < MIN_WORD:
            prev_end = words[i - 1]["end"] if i else 0.0
            w["start"] = round(max(prev_end, w["end"] - MIN_WORD), 3)
        if i + 1 < len(words) and w["end"] > words[i + 1]["start"]:
            w["end"] = round(max(words[i + 1]["start"], w["start"] + 0.04), 3)
    short = [w["text"] for w in words if w["end"] - w["start"] < 0.08 and len(re.sub(r"\W", "", w["text"])) >= 4]
    if short:
        print(f"WARN   very short words, check by hand: {short}")
    inverted = [w["text"] for w in words if w["end"] <= w["start"]]
    if inverted:
        sys.exit(f"Words that end before they start, fix by hand: {inverted[:5]}")
    bad = [(x["text"], y["text"]) for x, y in zip(words, words[1:]) if y["start"] < x["start"] or x["end"] > y["start"] + 0.001]
    if bad:
        sys.exit(f"Out-of-order or overlapping words, fix by hand: {bad[:5]}")
    json.dump(words, open(path, "w"), indent=1)
    print(f"wrote {path} ({len(words)} words); raw copy: {raw}")


if __name__ == "__main__":
    main()
