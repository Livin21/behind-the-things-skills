---
name: sound-designing-shorts
description: Use when a rendered HyperFrames short needs sound effects, a final mix or mastering before upload - including when the sound feels flat or empty next to other explainer channels, nothing audible marks on-screen changes, renders are louder or quieter than the platforms' −14 LUFS, or a moment (the twist, a readout swap) needs its own sound.
---

# Sound-designing shorts

## Overview
Every on-screen change gets a short sound, and every sound is made in code, like the pictures. The cues come from the composition's own GSAP timeline, so nobody places sounds by hand, and the voice, bed and effects are mixed and mastered to −14 LUFS. The owner approved this "bold" mix on 16 Nov 2026 after an A/B/C listen. It was modelled on measured reference Reels (about 1.5 effects per second, mostly bright clicks under 80 ms, mastered to −14 LUFS).

## When
After the render (animating-shorts-in-hyperframes) and before the upload copy (publishing-shorts). It works only for shorts, which have one `main` timeline; long-form sub-compositions aren't supported yet.

## Run it
From the episode's `video/` folder:
```
bash <skills>/sound-designing-shorts/scripts/sound_pass.sh . renders/epNNN-slug.mp4
```
- **Outputs:** `sfx-cues.json` (the cue list) and `renders/epNNN-slug-sound.mp4` (the video copied untouched, plus the new mix). The `-sound.mp4` file is the master from now on, for the upload copy and the site.
- **Writes nothing else into the episode.** On first run it installs `puppeteer-core` into `scripts/node_modules/` and synthesises the kit into `scripts/kit/` (deterministic), both inside this skill's folder.
- **Browser:** it uses the Chrome that HyperFrames already downloaded, at the project's pinned version.
- **Files:**
  - `sound_pass.sh` runs everything.
  - `extract_cues.mjs` is the headless runner.
  - `extract_cues.js` is the rule set it evaluates in the page.
  - `make_kit.py` makes the sounds.
  - `remix.py` mixes and masters.

## Check
- **Density:** 1.0–2.0 cues per second **without counter ticks**, which the printout reports separately. Episodes 002–007 measured 1.07–1.86.
- **Loudness:** −13.8 to −14.5 LUFS integrated, measured on the output, and true peak at −1 dBTP or lower: `ffmpeg -i <out> -af ebur128=peak=true -f null -`. This measurement is the authority; the printout's figure can differ by 0.1. ebur128 logs every frame, so grep its "Summary" block.
- **Bursts above 6 per second** are fine for counters (10 ticks a second) and staggers (at most 10 a second, 6 per tween).
- **Too sparse (under 1.0):** the extractor can't hear SVG attribute tweens (a circle's `r`, stroke width), colour changes, position moves without a fade, or `repeat` pulses. Add hand `sfx()` cues on those visible changes, typically `tick`, `tick-lo` or a stepping blip. A repeating pulse goes under `data-sfx="off"` with its beats placed by hand.
- **Too dense, or a burst under narration that isn't a counter or a stagger:** find the stretch in `sfx-cues.json`. Silence its element with `data-sfx="off"` (or a plain-object tween with `data: "nosfx"`) and run the pass again. Don't lower `--sfx-db`.
- **Listen:** a human hears the whole `-sound.mp4` on headphones; effects should sit under the voice and never cover a word. An agent can't listen, so it reports "sound listen pending" with the three busiest moments (mm:ss) for the owner's next review.

## What makes a sound
Rules are checked in this order, first match wins. An id "word" means the id split on hyphens, with a trailing digit allowed (`s2-case`, `s6-check1`).

| On screen | Sound | Gain |
|---|---|---|
| Paper wipe (`#wipe` to `yPercent: 0`) | `wipe` | 1 |
| Callout dot (`.dot` scales) | `dot` | 0.8 |
| Tag or minitag fades in | `tick` | 1 |
| Flow line starts (`strokeDashoffset`, longer than 0.4 s; 0.6 s apart at least) | `blip`, stepping +0, +2, +4, +7, +9, +12 | 0.7 |
| Counter: the template's `counter()` (tagged `data: "counter"`) | `digit` ×10/s, then `tick` at the end | 0.8, end 0.9 |
| Any other plain-object `onUpdate` tween longer than 0.4 s (a sweep, a progress bar) | one stepping `blip` | 0.7 |
| Id word `shell`, `cover`, `lid`, `casing`, `case`, `door` or `flap` rotates | `lift` | 1 |
| Class `stamp`, or id word `stamp`, `check`, `cross`, `ok`, `no` or `nomatch`, enters, scales or draws | `stamp` | 0.8 |
| End card: id word `lock`, `lockup`, `so-big` or `things` enters (first one only) | `lockup` | 0.9 |
| Id starting `mark` or `so-mark` sweeps (`scaleX` or `backgroundSize`) | `marker` | 0.7 |
| Anything rotates 90° or more | `lift` | 0.6 |
| Other entrances, in order: clip-path; scaleY; scale; x slide over 1 s; short fade-and-move | `marker`; stepping `blip`; `tick-hi`; `lift`; `tick-lo` | 0.45; 0.55; 0.65; 0.45; 0.55 |

- **Staggers:** each target sounds at its own start, at most 10 cues a second and 6 per tween.
- **Never sonified:** captions (`.cg`), anything inside `[data-sfx="off"]`, and tweens with `data: "nosfx"`.
- **Spacing:** no cue in the first 0.15 s, and none within 70 ms of another.

## Hand-placed cues
The extractor can't know which moment is the twist. In `index.html`, next to `tl`:
```js
window.__sfx = [];
function sfx(t, s, g) { window.__sfx.push({ t: t, s: s, g: g == null ? 1 : g }); }
sfx(47.19, "reveal", 0.8);       // the twist: once per episode
sfx(31.2, "switch", 0.9);        // a readout swap (STEADY → DROPPED)
```
- **Where the reveal goes:** on the first word of the **answer** (not the question), where the picture lands its payoff. Take the time from `assets/transcript.json`.
- **Its length:** `reveal` lasts 1.0 s (a 0.5 s low thump plus a two-note chime), so it rings under the next words; use gain 0.8.
- **Precedence:** a hand cue replaces any automatic cue within 70 ms. The kit:
- `tick`, `tick-hi`, `tick-lo`
- `digit`, `digit-hi`, `digit-lo`
- `dot`, `switch`, `lift`, `wipe`, `marker`, `stamp`, `reveal`, `lockup`
- `blip+0`, `blip+2`, `blip+4`, `blip+7`, `blip+9`, `blip+12`

## Mix (fixed; change it only with the owner)
- **Voice:** high-pass at 80 Hz, +4.5 dB at 4.5 kHz, +2.5 dB shelf above 9 kHz, de-esser, 2.5:1 compression. Its `data-volume` is applied.
- **Effects:** −12 dB (`--sfx-db`), with a ±1 dB deterministic jitter.
- **Music:** the `<audio id="music">` lane as written.
- **Master:** −14 LUFS integrated, limiter at −1 dBTP.

To change the character, edit `make_kit.py` or `remix.py` for every episode at once, and get the owner to hear a before-and-after. Never tweak the mix for one episode.

## Common mistakes
| Mistake | Fix |
|---|---|
| Running it on a render older than `index.html` | Cues come from the current HTML, so re-render first or they drift |
| Fixing loudness in the render or the HyperFrames lanes | The pass rebuilds the mix from `narration_norm.wav` and the music file, then masters it; the render's own audio is ignored |
| Uploading the raw render | Make the upload copy from `-sound.mp4` |
| `waitForFunction` timing out in headless Chrome | Headless-shell doesn't run rAF-based waits reliably; the runner (`extract_cues.mjs`) polls by hand, so keep it that way |
| A hand-written counter that doesn't use `counter()` | Add `data: "counter"` to its tween, or it gets one blip instead of digit ticks |
| A per-episode `--sfx-db` | One level for the channel; a bad moment needs a hand cue or a lower gain on that cue |
