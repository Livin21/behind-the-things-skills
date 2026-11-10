---
name: making-long-form-explainers
description: Use when making a 5–10 minute horizontal (16:9, 1920×1080) explainer from a shorts pipeline - choosing the topic and length, splitting it into chapters, per-chapter narration and a multi-section music bed, building chapters in parallel with subagents in HyperFrames, SRT captions, rendering and checking a long composition, or releasing it on YouTube and a website.
---

# Making long-form explainers

## Overview
A long video is **one question, answered in 6–8 chapters, in 6–8 minutes**. Each chapter is its own HyperFrames sub-composition, built in parallel by one subagent from a locked shared library, then rendered once as a whole. The shorts skills still apply: scripting-explainer-shorts for facts, voicing-and-captioning-shorts for voice, animating-shorts-in-hyperframes for traps. This skill covers what changes at 16:9 and 7 minutes.

## Stages
| # | Stage | Done when |
|---|---|---|
| 0 | Set up | `episodes/L0N-slug/video/` holds this skill's `template/` plus `package.json`, `hyperframes.json`, `meta.json`, `assets/fonts/`, `assets/grain.png` from the shorts template; `lib/btt.css` tokens set from `DESIGN.md`; `DESIGN.md` has a long-form layout section (see `reference/`) |
| 1 | Decide | Three research reports (topic demand and competition, format and retention, production feasibility), then one decision document: topic, length, title and alternates, thumbnail, first 10 s, the chapter table with every on-screen string, release, metrics. The owner approves it, or has said a subagent may decide |
| 2 | Script | scripting-explainer-shorts' sourcing rules (its 54 × pace cap and five-part shape are replaced by the chapter table); per chapter in `script.md`: title, narration, a beat table with every on-screen string; budgets = (chapter seconds − pauses) × pace; `narration/chNN.txt` holds exactly what is spoken |
| 3 | Voice | One TTS request per chapter (batch), normalised, transcribed, `fix_timings.py`, `diff_words.py`; deliberate pauses spliced in (below) |
| 4 | Timeline | `chapters.json` → `build_timeline.py` (root + `previews/`), `build_bed.py` (music), `build_srt.py` (captions) |
| 5 | Pilot chapter | The lead builds chapter 1 and the shared drawings, reviews a contact sheet, and locks `lib/` |
| 6 | Fan out | One subagent per remaining chapter, briefed with `CHAPTER-BRIEF.template.md`; each renders its preview and reviews contact sheets |
| 7 | Integrate | `check` passes with 0 errors; full render; a boundary sheet (±0.3 s at every chapter edge); audio checks; high-quality master |
| 8 | Release | Upload (files over 10 MB need the owner), SRT, description timestamps from `chapters.json`, thumbnail, website page |

## Numbers that worked (L01, 6:55)
- 6–8 minutes for a cold audience; about 1,050 words at 2.6 words per second.
- Chapter 1 is a cold open: no chapter card, hidden indicator, voice at 0.25 s. Other chapters: card at 0.4 s, voice at 1.2 s, 1.4 s tail. The last chapter carries a 5 s end card and fades itself (`tail: 0`).
- Indicator text counts every chapter, including the hidden cold open: `02 / 07 · TITLE`.
- Render: 6:55 at 1080p in about 6.5 min (M4, standard); about 100 MB at standard, more at high. Loudness lands at −13.8 LUFS with voices at −16.5 mono.
- Spend: 7 narration requests (about 21 credits) and 3 × 150 s music tracks (about 65).

## Voice, step by step
Run in `video/`; raw takes are `assets/vo/chNN.mp3`.
1. One TTS request per chapter, submitted together (Higgsfield `generate_audio_batch`); download each result to `assets/vo/chNN.mp3`.
2. `bash <skills>/voicing-and-captioning-shorts/scripts/normalize_voice.sh assets/vo/chNN.mp3 assets/vo/chNN_norm.wav`
3. Transcribe **one chapter at a time**; `transcribe` overwrites `transcript.json` in the audio's folder:
   `npx hyperframes@<pin> transcribe assets/vo/chNN.mp3 --model small.en --language en && mv assets/vo/transcript.json assets/vo/chNN.transcript.json`
4. `python3 -I <skills>/voicing-and-captioning-shorts/scripts/fix_timings.py assets/vo/chNN.mp3 assets/vo/chNN.transcript.json`, then `diff_words.py` against a `medium.en` transcript made in a scratch folder (voicing skill step 5). Skip that skill's caption steps 6–7.
5. Deliberate pauses: `python3 -I template/splice_pause.py` (below).
6. `chapters.json`, with `vo_duration` = `ffprobe -v error -show_entries format=duration -of csv=p=0 assets/vo/chNN_norm.wav`:
   - chapter 1 (cold open): `vo_at` 0.25, `duration` = 0.25 + vo_duration + 1.4
   - middle chapters: `vo_at` 1.2, `duration` = 1.2 + vo_duration + 1.4
   - last chapter: `vo_at` 1.0, `duration` = 1.0 + vo_duration + 5.0 (end card); top-level `"tail": 0`
7. After **any** duration change, re-run `build_timeline.py`, `build_bed.py` and `build_srt.py`. Finish all of this before briefing chapter agents; they cue to these timings.

## Voice and pauses
- Pace varies by chapter (2.5–2.9 words per second); flag the fastest chapter for the human listen.
- **Keep a reveal pause short, with the music under it.** On L01 a 2.2 s pause with the bed dropped out read as an awkward dead gap to the owner; 0.8 s with the music continuing worked. Give drama with the picture (a held frame, a slow push), not with silence.
- **A deliberate pause** (a reveal): `python3 -I splice_pause.py assets/vo/chNN_norm.wav assets/vo/chNN.transcript.json <mid-pause s> <seconds to add>`. It splices silence into the wav and shifts the later words. Then update that chapter's `vo_duration` and `duration`, and if you really want the music out too, add a `drops` entry to `bed.json` (voice times, previous word's end to next word's start), but test it with a human first.

## Music bed
- Three tracks in the same palette (prompt them as opening, mechanism, closing), each levelled to the bed target, crossfaded 3 s on chapter boundaries.
- A 150 s track can't cover 7 minutes in three sections; reuse the opening track's unused tail under the recap. Use `end_trim` to align on the track's **audible** ending; generated tracks end with 1–2 s of silence.

## Captions
No burned-in captions at 16:9. `python3 -I build_srt.py chapters.json ../<id>.en.srt` aligns each `narration/chNN.txt` with its word timings (the script's wording wins). `caption_display` in `chapters.json` maps spoken phrases to display forms: numbers to digits (list "three hundred thousand" before "three hundred"), and any TTS respelling back to the real spelling. Lines are 42 characters at most, two per cue, and avoid ending on a small word.

## Fan-out rules
- Lock `lib/` (tokens, helpers, drawings) and one approved chapter **before** briefing agents. Agents write only `compositions/chNN.html`.
- Give each agent: duration, vo_at, its beat table, and how its first and last frames meet the neighbours (wipe, or an exact match-cut drawing call).
- Agents render with `--workers 2` (six render at once) and don't run the project-wide `check`; the lead does.
- Expect 15–20 minutes per chapter agent, with two or more render-and-review rounds.

## Integration review (stage 7)
1. `npx hyperframes@<pin> check`: 0 errors. Warnings to read: `gsap_*` ones are real; `line_unread` means hold the tag longer; `dead_stretch` is often false (confirm with frames).
2. Full render: `npx hyperframes@<pin> render --quality standard -o renders/<id>.mp4` for review; the upload master uses `--quality high`.
3. A boundary sheet: frames at ±0.3 s around every chapter start, plus frame 0 and the last frame (ffmpeg `tile`). Match cuts must line up and indicators must read right.
4. Audio: integrated loudness −13 to −14.5 LUFS (`ebur128`); `silencedetect=noise=-38dB:d=0.9` over the whole file should find only the deliberate pauses. Silence at the end means the last music section ends on its silent tail (set `end_trim`, measured with `silencedetect` on the track).
5. The lead watches the whole render once at normal speed, and a human hears the hook, every chapter boundary and every flagged word before release.

## Traps (all hit on L01)
| Trap | Fix |
|---|---|
| GSAP `x`/`y`/`scale` on an SVG `<g>` that has `transform="translate(...)"` replaces the translate, so the drawing jumps to the top-left | Animate an outer wrapper with no transform; the inner group holds the placement |
| Preview files next to `index.html` fail `check` ("multiple root compositions") | `previews/` subfolder: assets and lib paths get `../`, but `data-composition-src` stays root-relative |
| Hidden layers set with `tl.set(..., 0)` show on a chapter's first frame | Also `gsap.set(...)` immediately (this is where a match cut breaks) |
| A `fromTo` that reveals a hidden element but leaves opacity out of the destination is invisible in multi-worker renders (`check` error) | Put `opacity: 1` in the destination too |
| `K.draw` (stroke-dashoffset) turns dashed lines solid | Fade dashed lines in, or use `K.flow` |
| The mono font lacks `≈`, `−` or `→` | It falls back to a system glyph; check the frames, or use ASCII |
| `check` "dead_stretch" warnings on long sub-compositions | Usually false; confirm against frames from the full render |
| `fix_timings.py` (before v4) could make a word end before it starts | Fixed: v4 skips the move and fails on inverted words |

## Release notes
- Don't make a sub-10 MB upload copy (`encode_upload.sh` is for shorts). Browser upload tools may cap files at 10 MB, so the owner drags the high-quality master into YouTube Studio as Private; then the agent fills in title, description (with `timestamps.txt`), thumbnail (1280×720), SRT captions and the schedule.
- Chapters, A/B tests and pinned comments need YouTube **advanced features** (ID or video verification, about 24 h). Ask the owner on day one; ship with timestamps in the description anyway.
- Shorts cut from the long video link to it as their Related Video (needs phone verification only).
- On the website, a long-form entry embeds YouTube (click-to-load, privacy-enhanced) instead of hosting the file.
- `reference/` has L01's drawings library and its approved cold-open chapter, as worked examples of the patterns (`put()` wrappers, scene switching, the pull-up camera move).
