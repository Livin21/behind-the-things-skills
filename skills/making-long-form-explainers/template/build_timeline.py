"""Write the long-form root (index.html) and one preview file per chapter (previews/<id>.html) from chapters.json.
Render one chapter fast with:  npx hyperframes@0.9.28 render -c previews/ch03.html --quality draft -o renders/ch03.mp4

Usage:  python3 -I build_timeline.py [chapters.json]

chapters.json:
{
  "id": "l01-slug", "thing": "BLUE LOCATION DOT",          # brand tag reads "BEHIND THE <thing>"
  "fps": 30,
  "scripts": ["lib/drawings.js"],                           # extra shared scripts (optional)
  "fonts": [{"family": "Archivo", "src": "assets/fonts/Archivo-VF.woff2", "weight": "100 900"}],  # local woff2 (StaticGuard needs @font-face)
  "music": {"src": "assets/music/bed.mp3", "volume": 0.28},  # optional
  "tail": 0,                                                 # seconds after the last chapter (keep 0; the last chapter fades itself)
  "chrome_off": {"chapter": "ch07", "after_vo": 0.2},        # fade brand tag + indicator after that chapter's last word
  "chapters": [
    {"id": "ch01", "title": "Cold open", "indicator": true,
     "duration": 44.5,                                       # chapter length (s); starts are cumulative
     "vo": "assets/vo/ch01_norm.wav", "vo_at": 0.25, "vo_duration": 43.6}
  ]
}
- Chapter n is compositions/<id>.html, a <template> with data-composition-id="<id>" and data-duration = duration.
- The root holds only background, chapter mounts, chrome (brand tag + chapter indicator) and audio.
- Every start is snapped to 1/fps. Re-run after changing any duration; it overwrites index.html, previews/*.html and timestamps.txt (paste into the YouTube description).
"""
import json, sys

HEAD = """<!doctype html>
<html lang="en"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" /><title>{title}</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
{fontfaces}</style>
<link rel="stylesheet" href="lib/btt.css" />
<script src="lib/btt.js"></script>
{scripts}</head><body>
"""


def snap(x, fps):
    return round(round(x * fps) / fps, 4)


def build(cfg, only=None):
    fps = cfg.get("fps", 30)
    chs = cfg["chapters"]
    t = 0.0
    for c in chs:
        c["start"] = snap(t, fps)
        c["duration"] = snap(c["duration"], fps)
        t = c["start"] + c["duration"]
    total = snap(t + cfg.get("tail", 0), fps)
    if only:
        sel = [c for c in chs if c["id"] == only]
        base = sel[0]["start"]
        total_out = snap(sel[0]["duration"] + (cfg.get("tail", 0) if sel[0] is chs[-1] else 0), fps)
    else:
        sel, base, total_out = chs, 0.0, total
    numbered = [c for c in chs if c.get("indicator", True)]
    n = len(numbered)
    fonts = cfg.get("fonts") or [{"family": "Archivo", "src": "assets/fonts/Archivo-VF.woff2", "weight": "100 900"},
                                 {"family": "IBM Plex Mono", "src": "assets/fonts/IBMPlexMono-500.woff2", "weight": "500"}]
    ff = "".join(f'@font-face {{ font-family: "{f["family"]}"; src: url("{f["src"]}") format("woff2"); font-weight: {f.get("weight", "400")}; }}\n' for f in fonts)
    out = [HEAD.format(fontfaces=ff, title=cfg["id"] + (" · " + only if only else ""), scripts="".join(f'<script src="{x}"></script>\n' for x in cfg.get("scripts", [])))]
    out.append(f'<div id="root" data-composition-id="main" data-start="0" data-duration="{total_out}" data-width="1920" data-height="1080">\n')
    out.append(f'<div id="bg" class="clip" data-start="0" data-duration="{total_out}" data-track-index="0"><div id="bg-grid"></div><div id="bg-grain" style="background-image:url(&quot;assets/grain.png&quot;)"></div></div>\n')
    for c in sel:
        s = snap(c["start"] - base, fps)
        out.append(f'<div id="m-{c["id"]}" class="clip" data-composition-id="{c["id"]}" data-composition-src="compositions/{c["id"]}.html" data-start="{s}" data-duration="{c["duration"]}" data-track-index="1" data-width="1920" data-height="1080"></div>\n')
    out.append(f'<div id="chrome" class="clip" data-start="0" data-duration="{total_out}" data-track-index="7" style="z-index:70"><div id="brandtag">BEHIND THE {cfg["thing"].upper()}</div><div id="chapterind"></div></div>\n')
    for i, c in enumerate(sel):
        if c.get("vo"):
            s = snap(c["start"] - base + c.get("vo_at", 0), fps)
            out.append(f'<audio id="vo-{c["id"]}" data-start="{s}" data-duration="{c["vo_duration"]}" data-track-index="{10 + i % 2}" src="{c["vo"]}" data-volume="1"></audio>\n')
    m = cfg.get("music")
    if m:
        ms = 0 if not only else base
        out.append(f'<audio id="music" data-start="0" data-media-start="{ms}" data-duration="{total_out}" data-track-index="12" src="{m["src"]}" data-volume="{m.get("volume", 0.28)}" data-fade-in="0.3" data-fade-out="{1.2 if not only else 0}"></audio>\n')
    out.append("</div>\n<script>\nwindow.__timelines = window.__timelines || {};\nvar tl = gsap.timeline({ paused: true });\n")
    out.append(f'tl.to("#bg-grid",{{x:-40,y:-40,duration:{total_out},ease:"none"}},0);\ntl.to("#bg-grain",{{x:30,y:-30,duration:{total_out},ease:"none"}},0);\n')
    ind = document_ind = "#chapterind"
    for c in sel:
        s = snap(c["start"] - base, fps)
        if c.get("indicator", True):
            k = chs.index(c) + 1   # numbered among ALL chapters (a hidden cold open still counts as 01)
            label = f'{k:02d} / {len(chs):02d} · {c["title"].upper()}'
        else:
            label = ""
        out.append(f'tl.set("{ind}",{{textContent:{json.dumps(label)}}},{s});\n')
    co = cfg.get("chrome_off")
    if co and not only or (co and only == co["chapter"]):
        c = next((x for x in chs if x["id"] == co["chapter"]), None)
        if c is None:
            raise SystemExit(f'chrome_off names chapter {co["chapter"]!r}, which is not in chapters.json')
        t_off = snap(c["start"] - base + c.get("vo_at", 0) + c["vo_duration"] + co.get("after_vo", 0.2), fps)
        out.append(f'tl.to(["#brandtag","#chapterind"],{{opacity:0,duration:0.4,ease:"power2.in"}},{t_off});\n')
    out.append('window.__timelines["main"] = tl;\n</script></body></html>\n')
    return "".join(out), total


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "chapters.json"
    cfg = json.load(open(path))
    html, total = build(json.loads(json.dumps(cfg)))
    open("index.html", "w").write(html)
    print(f"index.html: {len(cfg['chapters'])} chapters, {total:.2f} s ({int(total // 60)}:{total % 60:05.2f})")
    import os, re
    os.makedirs("previews", exist_ok=True)
    for c in cfg["chapters"]:
        h, _ = build(json.loads(json.dumps(cfg)), only=c["id"])
        # previews live one folder down so check/render see a single root (index.html)
        # assets and lib resolve from the preview file; data-composition-src resolves from the project root
        h = re.sub(r'(src|href)="(assets|lib)/', r'\1="../\2/', h)
        h = h.replace('url("assets/', 'url("../assets/').replace('url(&quot;assets/', 'url(&quot;../assets/')
        open(f"previews/{c['id']}.html", "w").write(h)
    # YouTube description timestamps (M:SS, rounded; first is always 0:00)
    lines, t = [], 0.0
    for c in cfg["chapters"]:
        r = int(round(t)); lines.append(f"{r // 60}:{r % 60:02d} {c['title']}"); t += c["duration"]
    open("timestamps.txt", "w").write("\n".join(lines) + "\n")
    t = 0.0
    for c in cfg["chapters"]:
        print(f"  {c['id']}  starts {int(t // 60)}:{t % 60:05.2f}  {c['duration']:6.2f} s  {c['title']}")
        t += c["duration"]


if __name__ == "__main__":
    main()
