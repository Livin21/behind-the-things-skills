"""Build one YouTube SRT for a long-form episode from per-chapter narration text + word timings.

Usage:  python3 -I build_srt.py chapters.json out.srt

For each chapter in chapters.json that has "vo", it reads:
  - the spoken script: "script" key (path, default ../narration/<id>.txt)  -> wording and punctuation (the script wins)
  - word timings:      "transcript" key (default assets/vo/<id>.transcript.json, [{"text","start","end"}])
Top-level "caption_display": [["spoken phrase", "display form"], ...] turns spelled numbers into digits.
Script words are aligned to transcript tokens (difflib on normalised words); unmatched script words get
interpolated times. Cue rules: <= 2 lines x 42 chars, <= 6 s, break at sentence ends and at pauses > 0.45 s.
Times are absolute: chapter start + vo_at + word time. Prints a summary and any alignment warnings.
"""
import difflib, json, re, sys

MAXC, MAXD, PAUSE = 84, 6.0, 0.45


def fits(text):
    if len(text) <= 42:
        return True
    w = text.split(" ")
    return any(len(" ".join(w[:i])) <= 42 and len(" ".join(w[i:])) <= 42 for i in range(1, len(w)))


def apply_display(words, times, pairs):
    """Merge spoken phrases into display forms, e.g. "twenty thousand two hundred" -> "20,200"."""
    out_w, out_t, i = [], [], 0
    keys = [([norm(x) for x in a.split()], b) for a, b in pairs]
    keys.sort(key=lambda k: -len(k[0]))
    while i < len(words):
        for k, b in keys:
            n = len(k)
            if [norm(x) for x in words[i:i + n]] == k:
                tail = re.sub(r"^.*?([^A-Za-z0-9]*)$", r"\1", words[i + n - 1])  # keep trailing punctuation
                out_w.append(b + tail); out_t.append((times[i][0], times[i + n - 1][1])); i += n; break
        else:
            out_w.append(words[i]); out_t.append(times[i]); i += 1
    return out_w, out_t


def norm(w):
    return re.sub(r"[^a-z0-9]", "", w.lower())


def ts(t):
    ms = max(0, round(t * 1000)); h, ms = divmod(ms, 3600000); m, ms = divmod(ms, 60000); s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def wrap(text):
    if len(text) <= 42:
        return text
    words, best = text.split(" "), None
    for i in range(1, len(words)):
        a, b = " ".join(words[:i]), " ".join(words[i:])
        score = abs(len(a) - len(b)) - (18 if a[-1] in ",;:" else 0) + (12 if b.split(" ")[0].lower() in ("a", "an", "the", "of", "to", "in", "at") and False else 0)
        if a.split(" ")[-1].lower() in ("a", "an", "the", "of", "to", "in", "at", "by", "and"):
            score += 25  # never end a line on a small word
        if len(a) <= 42 and len(b) <= 42 and (best is None or score < best[0]):
            best = (score, a + "\n" + b)
    return best[1] if best else text


def align(script_words, toks):
    a = [norm(w) for w in script_words]
    b = [norm(t["text"]) for t in toks]
    times = [None] * len(a)
    for blk in difflib.SequenceMatcher(None, a, b, autojunk=False).get_matching_blocks():
        for k in range(blk.size):
            t = toks[blk.b + k]; times[blk.a + k] = (t["start"], t["end"])
    known = [i for i, x in enumerate(times) if x]
    if not known:
        raise SystemExit("no words aligned")
    miss = len(a) - len(known)
    for i in range(len(a)):
        if times[i]:
            continue
        prev = max([k for k in known if k < i], default=None); nxt = min([k for k in known if k > i], default=None)
        if prev is None:
            s = times[nxt][0]; times[i] = (s, s)
        elif nxt is None:
            e = times[prev][1]; times[i] = (e, e)
        else:
            s0, e1 = times[prev][1], times[nxt][0]; f = (i - prev) / (nxt - prev)
            times[i] = (s0 + (e1 - s0) * f, s0 + (e1 - s0) * f)
    return times, miss


def main():
    cfg = json.load(open(sys.argv[1])); out = sys.argv[2]
    t, cues, report = 0.0, [], []
    for c in cfg["chapters"]:
        start = t; t += c["duration"]
        if not c.get("vo"):
            continue
        words = open(c.get("script", f"../narration/{c['id']}.txt")).read().split()
        toks = json.load(open(c.get("transcript", f"assets/vo/{c['id']}.transcript.json")))
        times, miss = align(words, toks)
        words, times = apply_display(words, times, cfg.get("caption_display", []))
        report.append(f"{c['id']}: {len(words)} words, {miss} interpolated")
        off = start + c.get("vo_at", 0)
        cur = None
        for w, (s, e) in zip(words, times):
            s += off; e += off
            if cur and (not fits(cur["text"] + " " + w) or e - cur["start"] > MAXD or s - cur["end"] > PAUSE or re.search(r"[.?!][\"')]*$", cur["text"])):
                cues.append(cur); cur = None
            if cur:
                cur["text"] += " " + w; cur["end"] = e
            else:
                cur = {"text": w, "start": s, "end": e}
        cues.append(cur)
    for a, b in zip(cues, cues[1:]):
        a["end"] = min(max(a["end"] + 0.25, a["start"] + 1.0), b["start"] - 0.04)
    cues[-1]["end"] += 0.8
    open(out, "w").write("".join(f"{n}\n{ts(c['start'])} --> {ts(c['end'])}\n{wrap(c['text'])}\n\n" for n, c in enumerate(cues, 1)))
    print("\n".join(report)); print(f"{len(cues)} cues -> {out}")


if __name__ == "__main__":
    main()
