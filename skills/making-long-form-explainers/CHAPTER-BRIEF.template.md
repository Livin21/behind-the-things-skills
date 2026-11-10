# Chapter build brief: <episode> (1920×1080 long-form)

Copy this into the episode folder, fill in the angle-bracket parts, and give each chapter agent its path plus its chapter-specific notes.

You build ONE chapter of a <N>-chapter, code-animated explainer. Other agents build the other chapters at the same time in the same project, so stay inside your own file.

## What you own
- Write only `video/compositions/chNN.html` (NN = your chapter), plus your own outputs under `video/renders/` (`chNN-draft.mp4`, `chNN-sheet/`). Do not edit `lib/`, `index.html`, `chapters.json`, `previews/`, audio, or another chapter.
- If you need a drawing that `lib/drawings.js` doesn't have, define it as a local function inside your chapter's script. If you think a lib file has a bug, say so in your report; don't fix it.

## Read first
1. `script.md`, your chapter's section: narration, beat table, and every on-screen string. **Copy each on-screen string exactly**, including punctuation and the `·` separator.
2. `video/compositions/ch01.html`: the approved pilot scene. Match its look, motion and code patterns (put(), wrappers, K helpers, scene switching with visibility sets, wipes).
3. `video/lib/btt.css`, `video/lib/btt.js`, `video/lib/drawings.js`: the shared classes, helpers (`BTT.kit(tl)`) and drawings (`BTT.draw.*`).
4. the project's `DESIGN.md`: the "Layout (long-form, 1920×1080)" and "Camera and motion" sections, plus "What NOT to Do".
5. `<path to the skills repo>/skills/animating-shorts-in-hyperframes/traps.md`: known HyperFrames/GSAP traps.

## Timing
- Your chapter's duration and `vo_at` (voice start, chapter-local) are in `video/chapters.json`. Set `data-duration` to that duration exactly.
- Word timings: `video/assets/vo/chNN.transcript.json` (`[{text,start,end}]`, in voice time). **Chapter time = vo_at + word start.** Cue every beat to its words. Land cuts in pauses, and land label entrances on the first syllable of the word they name.
- Chapter card (chapters 2–7): `K.card("#chNN-l3", 0.4, 4)` using the `.lower3` markup from `_chapter.example.html`. `CHAPTER 0N` over the chapter title, exactly as in `chapters.json`.

## Rules that the pilot learned the hard way
- **Never tween x/y/scale on a `<g>` that has a `transform` attribute.** GSAP replaces the translate and the drawing jumps to the top-left. Wrap: `<g id="chNN-xw"><g transform="translate(..) scale(..)">drawing</g></g>` and tween `#chNN-xw` (see `put()` in ch01).
- The stroke-draw helper `K.draw` makes dashed `.flowline` paths solid. Fade dashed lines in instead (opacity), or use `K.flow` for travelling dashes.
- All ids start with `chNN-`. Deterministic only: no Math.random, no Date. Build the timeline synchronously.
- Scene switches inside a chapter: hide the outgoing layer and show the incoming one with `tl.set(..., {visibility})` at the cut. Set the **initial** hidden state with an immediate `gsap.set(sel, {visibility: "hidden"})` as well as `tl.set(sel, {visibility: "hidden"}, 0)`; a set at 0 alone does not apply on the chapter's first frame, which breaks match cuts. Use `K.wipe(sel, T)` for a paper-wipe cut inside the chapter.
- A `fromTo` that reveals a hidden element must put `opacity: 1` in the destination too, or multi-worker renders can leave it invisible (`check` error `gsap_cold_seek_hidden_fromto_missing_reveal`).
- Check that the mono font has every glyph you type (`≈`, `−`, `→`, `✓`); if not, draw it in SVG or accept a system fallback after looking at the frame.
- Text-safe area is x 96–1824, y 64–940. The brand tag (top-left) and chapter indicator (top-right, y about 56–90) are drawn by the root, so keep your content clear of y < 120 at the corners.
- No burned-in captions. On-screen text is only what the beat table lists.
- **One accent (`--accent`) element per frame** at most. The chapter card's small accent square is chrome and exempt. `--flow` is for signals, data and paths.
- Sizes: tags `.tag` (32px), readouts `.readout`, hero numbers `.hero-num`, statements `.statement` (68px), sentences `.sentence`. Nothing below 28px except drawing texture labels, which carry `data-layout-ignore`.
- Push-in: `K.push(stage, start, dur)` (0.4%/s, cap 5%) on held scenes.
- Every element visible at a moment must have entered with motion (no element appears fully formed, except the hero object at a cut or match cut).

## Chapter boundaries (transitions)
- **Match cuts (optional):** if chapter N ends on an object that chapter N+1 opens on, give both agents the exact drawing call, position and scale, and leave the wipe out at that boundary. <Write the exact call here.>
- **Other chapters start:** under a paper wipe that leaves at t = 0. Add `<div class="wipe" id="chNN-wipein"></div>` as the last element in the chapter markup, then `gsap.set("#chNN-wipein", {yPercent: 0}); tl.to("#chNN-wipein", {yPercent: -102, duration: 0.3, ease: "power3.out"}, 0);`. Your scene is already in place underneath at t = 0.
- **Every chapter except the last ends:** a paper wipe covers the last 0.25 s. Add `<div class="wipe" id="chNN-wipeout"></div>`, then `gsap.set("#chNN-wipeout", {yPercent: 102}); tl.to("#chNN-wipeout", {yPercent: 0, duration: 0.25, ease: "power3.in"}, DUR - 0.25);`. Everything must still be on screen until the wipe covers it. No exit animations before the wipe.

## Check your work (required, iterate until clean)
1. Render your chapter alone: `cd video && npx --yes hyperframes@0.9.28 render -c previews/chNN.html --quality draft --workers 2 -o renders/chNN-draft.mp4`. Don't run `check` on the whole project; the lead does that at integration.
2. Make a contact sheet with one frame per beat, plus 0.1 s, the middle of each scene and DUR − 0.4: `ffmpeg -ss <t> -i renders/chNN-draft.mp4 -frames:v 1 -vf scale=480:-1 renders/chNN-sheet/<i>.png` for each time, then `ffmpeg -pattern_type glob -i 'renders/chNN-sheet/*.png' -filter_complex tile=5x3:padding=6:color=white renders/chNN-sheet.png`. **Open it with the Read tool and look.** Then extract 2–3 full-size frames of the busiest moments and look at those too.
3. Fix overlaps, cut-off drawings, text outside the safe area, things that appear without motion, more than one orange element, wrong strings, and beats that land before or after their words. Re-render and re-check. At least two rounds.

## Report (concise)
- What each beat shows, and its start time.
- Any deviation from the beat table, and why.
- Anything you couldn't make work.
- The path to your final contact sheet.

## The last chapter only
- It has no outgoing wipe. Everything fades to plain paper over the last 0.5 s (DUR − 0.55 → DUR); it is the only chapter allowed an exit fade.
- After the sign-off line, an end card: the channel's lockup (adapt the shorts sign-off: small mono line, very large display word on the accent marker bar, episode line in ink-2), plus the cadence line from `CHANNEL.md`, centred in 1920×1080. The root fades the brand tag and indicator after the last word (`chrome_off` in chapters.json).
