"""Rebuild word timings by transcribing the narration piece by piece, cut at its real pauses.

Whisper drifts over a whole take: onsets late mid-sentence, sentence-final words pushed into the
next pause. Transcribing each stretch between pauses on its own, then pinning each piece's first
word to the moment speech resumes, fixes both. Run it instead of (or after) fix_timings.py.

Usage (from the episode's video/ folder):
  python3 -I retime_by_pauses.py assets/narration_norm.wav assets/transcript.json [--pin 0.9.28]
      [--noise -32] [--min 0.18] [--model small.en]

- Keeps the previous file as transcript.wholefile.json (once), then overwrites transcript.json.
- Pieces are transcribed in a temporary folder with `npx hyperframes@<pin> transcribe`.
- Prints each piece and fails if the result is out of order or overlaps.
- Token text comes from the piece transcriptions, so write captions.spec.json AFTER running this.
"""
import argparse, json, os, re, shutil, subprocess, sys, tempfile


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    if r.returncode:
        sys.exit(f"failed: {' '.join(cmd[:4])}…\n{r.stderr[-800:]}")
    return r


def silences(audio, noise, min_d):
    err = run(["ffmpeg", "-hide_banner", "-i", audio, "-af", f"silencedetect=noise={noise}dB:d={min_d}", "-f", "null", "-"]).stderr
    s = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", err)]
    e = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", err)]
    return list(zip(s, e))


def duration(audio):
    return float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", audio]).stdout)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("audio"); ap.add_argument("transcript")
    ap.add_argument("--pin", default="0.9.28"); ap.add_argument("--noise", type=float, default=-32)
    ap.add_argument("--min", type=float, default=0.18); ap.add_argument("--model", default="small.en")
    a = ap.parse_args()

    total = duration(a.audio)
    gaps = [(s, e) for s, e in silences(a.audio, a.noise, a.min) if s > 0.05 and e < total - 0.05]
    # A piece runs from where speech resumes (a gap's end) to where the next gap starts.
    starts = [0.0] + [e for _, e in gaps]
    ends = [s for s, _ in gaps] + [total]
    pieces = [(max(0.0, st - 0.04), en + 0.04, st) for st, en in zip(starts, ends) if en - st > 0.15]

    tmp = tempfile.mkdtemp(prefix="retime_")
    words = []
    try:
        for k, (cut0, cut1, speech0) in enumerate(pieces):
            d = os.path.join(tmp, f"p{k:02d}"); os.makedirs(d)
            wav = os.path.join(d, "piece.wav")
            run(["ffmpeg", "-v", "error", "-y", "-ss", f"{cut0:.3f}", "-to", f"{cut1:.3f}", "-i", a.audio, "-ac", "1", "-ar", "16000", wav])
            run(["npx", "--yes", f"hyperframes@{a.pin}", "transcribe", wav, "--model", a.model, "--language", "en"], cwd=d)
            got = json.load(open(os.path.join(d, "transcript.json")))
            got = [w for w in got if w.get("text", "").strip()]
            if not got:
                continue
            for j, w in enumerate(got):
                st, en = cut0 + float(w["start"]), cut0 + float(w["end"])
                if j == 0:
                    st = max(st, speech0) if st > speech0 + 0.25 else speech0   # pin the first word to speech onset
                en = min(max(en, st + 0.05), cut1 - 0.04)
                words.append({**w, "start": round(st, 3), "end": round(en, 3)})
            print(f"piece {k:2d} {speech0:6.2f}-{cut1 - 0.04:6.2f}  {len(got):3d} words  {' '.join(x['text'] for x in got)[:70]}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    for i in range(1, len(words)):
        if words[i]["start"] < words[i - 1]["end"] - 1e-3:
            words[i - 1]["end"] = words[i]["start"]
        if words[i]["start"] < words[i - 1]["start"] or words[i - 1]["end"] < words[i - 1]["start"]:
            sys.exit(f"out of order near {words[i]['text']!r} at {words[i]['start']}")
    backup = a.transcript.replace(".json", ".wholefile.json")
    if not os.path.exists(backup) and os.path.exists(a.transcript):
        shutil.copy(a.transcript, backup)
    json.dump(words, open(a.transcript, "w"), indent=1)
    print(f"wrote {a.transcript}: {len(words)} words from {len(pieces)} pieces (previous kept as {os.path.basename(backup)})")


if __name__ == "__main__":
    main()
