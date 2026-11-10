"""List words where the transcript disagrees with the script, with timestamps.

An agent can't listen. Two transcriptions (small.en, then medium.en in a scratch folder)
plus this diff give a short list of moments a human should listen to before release.

Usage: python3 -I diff_words.py <script_narration.txt> <transcript.json> [<transcript2.json>]
"""
import difflib, json, re, sys

NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six",
       "7": "seven", "8": "eight", "9": "nine", "10": "ten"}


def norm(w):
    w = re.sub(r"[^\w'-]", "", w.lower()).strip("'-")
    return NUM.get(w, w)


def main():
    script = [norm(w) for w in open(sys.argv[1]).read().split()]
    script = [w for w in script if w]
    for path in sys.argv[2:]:
        tr = json.load(open(path))
        heard = [norm(t["text"]) for t in tr]
        sm = difflib.SequenceMatcher(a=script, b=heard, autojunk=False)
        issues = [(op, script[i1:i2], tr[j1:j2]) for op, i1, i2, j1, j2 in sm.get_opcodes() if op != "equal"]
        print(f"== {path}: {len(issues)} difference(s)")
        for op, said, got in issues:
            t = f"{got[0]['start']:.2f}s" if got else "?"
            print(f"  {t:>8}  script: {' '.join(said) or '-':<28} heard: {' '.join(g['text'] for g in got) or '-'}")
    print("Numbers/years often differ only in form (1974 vs nineteen seventy-four): ignore those. Listen to the rest.")


if __name__ == "__main__":
    main()
