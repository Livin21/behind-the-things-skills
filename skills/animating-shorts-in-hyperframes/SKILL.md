---
name: animating-shorts-in-hyperframes
description: Use when building or fixing a code-drawn vertical (1080x1920) explainer short in HyperFrames - laying out scenes from a script and word timings, adding callouts, wipes and captions, or when check/snapshots show occluded text, panels stuck over the frame, missing fonts, content colliding with captions, or a blank first frame.
---

# Animating shorts in HyperFrames

**REQUIRED BACKGROUND:** the `hyperframes` and `hyperframes-cli` skills (the composition contract, GSAP rules and CLI). This skill adds the explainer-specific layer on top.

## Overview
Start from `template/`. It already has the background, the scene stages with a capped push-in, the paper wipes, the caption layer, the brand tag, the sign-off and the audio wiring, each with the known traps fixed. Your job is to draw the scenes the script asks for, in the project's `DESIGN.md` style, cut on the words, then prove it with checks and your own eyes.

## Process
1. **Set up.** Copy `template/` into `episode/video/`. Run `npx hyperframes init` first if you need its scaffolding, then overwrite `index.html` and `assets/` with the template's. Replace the `:root` tokens and `@font-face` with the project `DESIGN.md`'s. If the project uses other fonts, put their woff2 files in `assets/fonts/`; a font name in CSS alone isn't enough.
2. **Plan the timing.** From `assets/transcript.json`, list each scene's start word. Cut on the first syllable of a key noun; sentence starts are fine for the sign-off. Set `DUR` to the narration length plus about 1.8 s, `CUTS` to the boundaries, and every clip's `data-start`/`data-duration` to match.
3. **Lay out the end state first.** Draw each scene's objects at their most-visible frame. Keep them inside y 220–1240 and x 72–940 at their final, pushed-in size, because captions own y 1250–1450.
4. **Animate.** Use entrances only (`tl.from`), and only the last scene may fade out. Give each object a callout with `callout(id, t)`, and put the callout inside the wrapper of any object that moves. Use one accent element per frame.
5. **Add the audio.** Uncomment the `<audio>` tags, set the voice `data-duration` to the exact narration length, and set the music lane times (see voicing-and-captioning-shorts).
6. **Check.** Run `npx hyperframes check`. It must say "Check passed" with 0 errors. Caption-hold and sub-composition warnings are acceptable.
7. **Look.** Run `npx hyperframes snapshot --at <15+ timestamps covering every scene, including t≈0.3>` and read every contact sheet. Fix what you find, then snapshot again. Do two full looks.
8. **Render and verify.** Run `npx hyperframes render --quality high --fps 30 --output renders/<ep>.mp4`. Then:
   - Check 1080×1920 at 30 fps with `ffprobe`.
   - Measure loudness (aim for −13 to −14 LUFS integrated).
   - Make a 10-frame review sheet with ffmpeg (`select` + `tile=5x2`) and look at it.

## Traps (each one has happened)
| Symptom | Cause | Fix |
|---|---|---|
| Text "occluded" by `#wipe` mid-scene | CSS `transform` on the wipe, plus GSAP `yPercent`, are summed | No CSS transform; `gsap.set(el, {yPercent})` |
| StaticGuard: font without @font-face | Font named in CSS only | Local `@font-face` + woff2 in `assets/fonts` |
| Objects slide under the captions late in a scene | Push-in grows long scenes | Keep the template's 7% cap; lay out at the final scale |
| An SVG scales from its corner | GSAP's SVG default origin is the top-left | `transformOrigin: "50% 50%"` in the tween |
| Things peek in at the frame edge early | The `from` offset is too small | The start state must be fully off canvas; snapshot the scene's first frame |
| Labels wrap in fixed boxes | Long words, narrow box | `white-space: nowrap`; size the box to the longest label |
| A moving dot or packet covers labels | Shared lane | Give the mover its own lane beside the labels |
| Blank cover on the platforms | Hook object enters late | The object is visible by 0.3 s |
| `content_overlap` on a stamp over text | An intentional overlap | `data-layout-allow-overlap` on both elements |
| Tiny decorative text fails the type floor | Texture text | `data-layout-ignore` on it |
| A fake barcode or QR code | Drawn by eye | Generate it from the spec in code; decode-test a rendered frame (for example jsQR) |

## Common mistakes
- Treating "Check passed" as done. A passing check can't see colliding or empty frames, so always look at the snapshots.
- Copying the script's packaging cover line into captions. Captions are only the spoken words.
- Inventing colours or fonts per scene. Everything comes from `DESIGN.md`.
