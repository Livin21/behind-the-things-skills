---
name: animating-shorts-in-hyperframes
description: Use when building or fixing a code-drawn vertical (1080x1920) explainer short in HyperFrames - laying out scenes from a script and word timings, adding callouts, reveals, wipes and captions, rendering and verifying - or when check/snapshots show occluded text, a panel stuck over the frame, missing fonts, content colliding with captions, or a blank first frame.
---

# Animating shorts in HyperFrames

**REQUIRED BACKGROUND:** the `hyperframes` skill (composition contract, GSAP rules). For diagram explainers this skill overrides its flex-layout advice: scenes here are absolutely positioned illustrations.

## Overview
Start from `template/`. It has the project files, background, capped push-in, paper wipes, captions, brand tag, sign-off, audio wiring and helpers (`push`, `callout`, `flow`, `swap`, `counter`), each with the known traps fixed.

**Precedence:** the project's `DESIGN.md` and `CHANNEL.md` decide the look and the assets. This skill decides the mechanics and safe zones. If they disagree on a mechanic, follow this skill and report it.

## Process
1. **Set up.**
   - Copy `template/` to `episodes/NNN-slug/video/`, then delete `DESIGN.example.md` and `captions.spec.example.json`. The template already has `package.json` with the pinned CLI, `hyperframes.json` and `meta.json`; set the id in `meta.json`. Don't run `init`.
   - Map `DESIGN.md` onto the `:root` tokens. Colours appear only there; SVGs use the `.f-*`/`.s-*` classes.
   - Swap the `@font-face` rules and `assets/fonts/` for the project's fonts.
   - Copy the music bed into `assets/`.
2. **Plan the timing** from the repaired `assets/transcript.json`.
   - **Cuts (wipes) sit in pauses:** a cut time `T` is when the wipe fully covers, 0.25 s after it starts. Put `T` in the pause just before the sentence that starts the new picture.
   - **Nouns get in-scene reveals:** callouts, the reveal, accent hand-overs.
   - Merge scenes when the picture is continuous (for example the hook and the reveal); holds of up to about 20 s are fine with the push-in cap.
   - Set `DUR` to the last word's end plus 1.8 s; if that passes 58 s, cut the tail to no less than 1.2 s. Each scene's `data-duration` must end exactly where the next `data-start` begins; all scenes go on track 1.
3. **Lay out the end state.** Before the push-in, keep objects inside **x 104–912, y 258–1211**; at the full 7% push that becomes x 72–940, y 220–1240. Captions own y 1250–1450.
4. **Animate.**
   - **Hook object:** fully drawn at t = 0. Settle it with scale or y only, never opacity.
   - **Entrances:** every other element enters (`tl.from`).
   - **State changes:** fine at any time (`tl.to`): the reveal, readouts via `swap`, colour hand-overs.
   - **Exits:** only in the final scene.
   - **Reveal:** move the casing (a `tl.to`) far enough to clear what it covers; parking it small at the top-left works. A shrunken copy must not carry a second accent.
   - **Accent:** one accent element at a time. It may hand over to a new subject mid-scene; the caption marker is exempt.
   - **Callouts:** put each one inside the wrapper of any object that moves.
5. **Audio and captions.** Uncomment the `<audio>` tags (voice `data-duration` = narration length) and set the music lane times. Then inject the captions (see voicing-and-captioning-shorts).
6. **Check.** Run `npm run check`; it must say "Check passed" with 0 errors. If it says "Nothing changed", add `--no-cache`. Expected and acceptable: `line_unread` (captions and short tags), `composition_file_too_large`, `timeline_track_too_dense`, `nested_structure_needs_subcomposition`, and `connector_orphan` (info, on flow lines). Investigate anything else.
7. **Look twice.** Snapshot with `npx hyperframes@<pin> snapshot --at <times> --no-end` and read **every** contact sheet it writes.
   - **First look:** a moment in each scene once everything has entered, plus each caption change you're unsure of.
   - **Second look:** different times: each scene's first frame, mid-wipe, the final fade.
   - Tags shrink in contact sheets, so proofread them in the HTML.
8. **Render and verify.**
   ```bash
   npm run render -- --output renders/epNNN-slug.mp4
   ffprobe -v error -show_entries format=duration:stream=width,height,r_frame_rate -of compact renders/epNNN-slug.mp4
   ffmpeg -i renders/epNNN-slug.mp4 -af loudnorm=print_format=summary -f null - 2>&1 | grep "Input Integrated"   # aim for −13 to −14.5
   ffmpeg -y -i renders/epNNN-slug.mp4 -frames:v 1 renders/frame0.png                                          # must show the object
   ffmpeg -y -ss 2.6 -i renders/epNNN-slug.mp4 -frames:v 1 -q:v 2 renders/cover.jpg                            # chosen cover
   N=$(ffprobe -v error -count_packets -select_streams v:0 -show_entries stream=nb_read_packets -of csv=p=0 renders/epNNN-slug.mp4)
   ffmpeg -y -i renders/epNNN-slug.mp4 -vf "select='not(mod(n\,$((N/10))))',scale=270:-1,tile=5x2" -frames:v 1 -vsync 0 renders/review-sheet.jpg
   ```
   Look at `frame0.png`, `cover.jpg` and `review-sheet.jpg`. If the loudness is off, see voicing-and-captioning-shorts → After the render.

## Traps
See `traps.md`: 16 symptoms that have happened, with their cause and fix. Scan it before the first look.

## Common mistakes
- Treating "Check passed" as done. A passing check can't see colliding or empty frames.
- Copying the script's packaging cover line into captions. Captions are only the spoken words.
- Inventing colours or fonts per scene. Everything comes from `DESIGN.md`.
