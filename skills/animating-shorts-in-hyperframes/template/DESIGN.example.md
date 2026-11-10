# DESIGN.md (example style: "Graph Paper")

Copy this to your project as `DESIGN.md` and change it. Every episode reads it. Keep it in numbers, not adjectives.

## Style prompt
A technical diagram on cool graph paper. Everyday objects are drawn as flat 2D illustrations with a confident ink outline. The camera slowly pushes in, then the object opens up to reveal its insides, labelled with thin leader lines and monospace tags. Exactly one thing per frame is marked in the accent colour: the part the narration is about. Flows of energy or data travel as dashed lines in the flow colour.

## Colours (token: hex: role)
- `--paper`: `#EEF1EA`: background, always
- `--paper-hi`: `#FAFBF7`: object faces, tag backgrounds
- `--shade`: `#D7DDD0`: secondary fills, hard shadows
- `--ink`: `#15181B`: outlines, all text, captions
- `--ink-2`: `#56606A`: secondary text
- `--accent`: `#FFB000`: **the hidden part.** Fills and marker highlights only; ink text sits on it. Never use it for text on paper.
- `--flow`: `#1F6FEB`: energy and data paths, dashed lines

Use one accent element group per frame.

## Type
- Statements and captions: `Archivo`, weight 900, tracking −0.03em.
- Labels, numbers and tags: `IBM Plex Mono`, weight 500, uppercase, tracking +0.04em.
- Vertical sizes: caption 84–96 px; tags 30–36 px; nothing below 28 px.

## Layout (1080×1920)
- Text inside x 72–940, y 220–1500. Platform UI covers the bottom ~420 px and the right ~140 px.
- Captions: y 1250–1450, centred, up to 2 lines. Nothing else goes there, even after the push-in.
- Object stage: y 220–1240. The brand tag sits top-left at y 138.

## Motion (numbers)
- Push-in: 1.5% per second, capped at 7% total, ease `none`.
- Entrances: 0.35–0.6 s, using at least three different eases per scene.
- Callouts: dot 0.2 s, leader 0.3 s, tag 0.3 s.
- The reveal (casing lifts): 0.9 s, `power4.inOut`.
- Transitions: a paper wipe at every cut (0.25 s in, 0.3 s out). No crossfades or glitches.
- The hook object is visible by 0.3 s. Frame one is the platforms' default cover.

## Sound
- Narration at −14 LUFS; music bed at about −28 LUFS under the voice.

## What not to do
- No gradients, glow, neon or blurred shadows. Use only hard offset shadows (6 px, `--shade`).
- No pure #000 or #fff.
- No stick figures, emoji or clip art. Draw the real object with real proportions.
- Use at most one accent element per frame.
- Put nothing in the caption zone or the platform-UI margins.
