"""Inject caption groups into a HyperFrames index.html.

Usage: python3 -I build_captions.py <transcript.json> <captions.spec.json> <index.html>

spec: list of [word_count, display_text, emphasis_word_index_or_-1]
Word counts must sum to the transcript length. Times come from the transcript, so a
re-voiced narration only needs a new transcript and a re-run.
"""
import json, re, sys

words = json.load(open(sys.argv[1]))
spec = json.load(open(sys.argv[2]))
html_path = sys.argv[3]

total = sum(s[0] for s in spec)
if total != len(words):
    sys.exit(f"spec covers {total} words, transcript has {len(words)}")

groups, i = [], 0
for count, text, em in spec:
    ws = words[i:i + count]
    groups.append({"text": text, "em": em, "start": round(ws[0]["start"], 3), "lastEnd": round(ws[-1]["end"], 3)})
    i += count

for gi, g in enumerate(groups):
    nxt = groups[gi + 1]["start"] if gi + 1 < len(groups) else None
    if nxt is None:
        end = g["lastEnd"] + 0.6
    elif nxt - g["lastEnd"] > 0.45:
        end = g["lastEnd"] + 0.25
    else:
        end = nxt - 0.02
    g["end"] = round(end, 3)
    del g["lastEnd"]

js = "/*CAPTIONS:BEGIN*/ var CAPTION_GROUPS = " + json.dumps(groups) + "; /*CAPTIONS:END*/"
html = open(html_path).read()
new, n = re.subn(r"/\*CAPTIONS:BEGIN\*/.*?/\*CAPTIONS:END\*/", lambda m: js, html, flags=re.S)
if n != 1:
    sys.exit("marker /*CAPTIONS:BEGIN*/…/*CAPTIONS:END*/ not found exactly once")
open(html_path, "w").write(new)
print(f"{len(groups)} caption groups, last ends at {groups[-1]['end']}s")
