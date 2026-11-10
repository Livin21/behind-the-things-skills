---
name: running-an-explainer-channel
description: Use when starting, planning or running a faceless educational short-video channel (YouTube Shorts, Instagram Reels, TikTok) end to end - choosing a niche and a look, producing a batch of episodes, delegating episodes to subagents, reviewing their output, or getting a channel's accounts and releases set up.
---

# Running an explainer channel

## Overview
A channel is a production line: one fact-checked script, one consistent voice, one code-drawn animation, one QA pass, then a release at the same minute on every platform. Each stage has its own skill. This skill covers the order, what "done" means, and the decisions made once and written down.

## Stages
| # | Stage | Skill | Done when |
|---|---|---|---|
| 1 | Hook and script | scripting-explainer-shorts | The hook is verified; words ≤ 54 × voice pace; every claim and on-screen number has a source row |
| 2 | Voice and timings | voicing-and-captioning-shorts | Narration normalised; timings repaired; differences flagged for a human; caption spec written |
| 3 | Animation and render | animating-shorts-in-hyperframes | Check has 0 errors; two snapshot looks (step 7); render at 1080×1920/30 fps and −13 to −14.5 LUFS; frame 0 shows the object; cover and review sheet exported |
| 3½ | Review | this skill (Producing a batch) | You have read the narration against `sources.md`, opened frame 0 and the review sheet; a human has heard the hook and every "listen at" moment before the release time |
| 4 | Release | publishing-shorts | Scheduled on every platform the channel uses (publishing-shorts covers YouTube Shorts and Instagram Reels) and on the site, all for one release time; logged |
| 5 | Measure | this skill (below) | 48 h and 7-day numbers logged for the episode |

## Decide once and write down
Keep two files in the project. Agents read them before anything else.
- **`DESIGN.md`:** the look, in numbers: palette with roles, two fonts, caption group size, safe zones, motion timings, what not to do. Start from `animating-shorts-in-hyperframes/template/DESIGN.example.md`.
- **`CHANNEL.md`:** the assets: voice and TTS parameters, measured voice pace, music bed path, fonts, pinned tool versions, brand tag, sign-off line, follow line, folder naming, release slot, log and metrics paths. Template: `CHANNEL.example.md` in this folder.

Also decide:
1. **Format name** ("Behind the ___"): the series and episode name, used on the site, the script heading, the on-screen brand tag and the sign-off. Platform titles are different: the question a viewer would search for (see publishing-shorts).
2. **Niche:** real, everyday things. Avoid saturated speculative formats ("What if…").
3. **Pilot gate:** get the owner's explicit approval of the voice, captions and first 2 seconds before making more. When the approved pilot and `DESIGN.md` disagree, update `DESIGN.md` to match the pilot.
4. **Numbering:** episodes are numbered in release order. Update the plan when the order changes.

## Producing a batch
- Give each episode one subagent, which owns stages 1–3 in `episodes/NNN-slug/`.
- The brief is the topic, the release date, the paths to these skills, and the instruction to read `CHANNEL.md`, `DESIGN.md` and one finished episode. If an agent needs more, put the missing fact in `CHANNEL.md` or the skill, not the brief.
- **Report:** render path, duration, **render** loudness, hook (draft → final), partly verified claims, and the "listen at" moments.
- **Folder at the end of stage 3:** `script.md`, `sources.md`, `narration.txt`, `video/{index.html, captions.spec.json, package.json, hyperframes.json, meta.json, assets/(narration.mp3, narration_norm.wav, transcript.json, transcript.raw.json, music.mp3, fonts/, grain.png), renders/(epNNN-slug.mp4, frame0.png, cover.jpg, review-sheet.jpg)}`.
- **Review every render yourself.** Read the narration against the sources (spot-check numbers against physics), look at the review sheet and frame 0, and send the owner the hook and the "listen at" moments (mm:ss) to hear. "Check passed" is not a review.
- **Scheduling before the listen is allowed**, as long as the listen happens before the release time. If it finds a problem, fix it (one regeneration, see Spend), re-render, and replace the scheduled upload; if there isn't time, unschedule the episode everywhere, including the site's release time.
- **Spend:** narration plus at most one regeneration per episode, and only for a clear mispronunciation, an overlong take or a factual fix.

## Measure
- Keep `METRICS.md` at the path in `CHANNEL.md`'s Metrics row (template: `METRICS.example.md` in this folder). Log each episode at 48 h and at 7 days after release. If a reading is late, log the numbers you see and write the real age ("72 h") in Note.
- The first number to read is YouTube's **viewed vs swiped away** for Shorts: it measures the hook. Then **average percentage viewed**: it measures the middle. Shares, saves and follows come later and are noisy at small numbers.
- Don't change the format until episode 010 has its 7-day reading; episodes due before then keep the current format. Then review the batch, keep what the top episodes share, and change **one** variable for the next batch, naming it in the "Variable tested" column. A variable is a pattern applied to every episode in the batch (hook style such as "question" vs "surprising number", title style, length, cover style), never one episode's wording.

## Accounts
- **Never create accounts or type passwords**, even when asked. Give the owner the exact values (name, handle, bio) and let them sign up or sign in. Then do the profile, uploads and scheduling.
- Check a handle on every platform before committing to it. See publishing-shorts.

## Common mistakes
| Mistake | Fix |
|---|---|
| Making more episodes before the pilot is approved | Stop at one; get sign-off |
| Facts living in briefs | Put them in `CHANNEL.md` once |
| Trusting a subagent's summary | Open the review sheet and frame 0; read the numbers |
| `DESIGN.md` drifting from what shipped | Update it whenever an approved episode differs |
| Releasing platform by platform | One release time; schedule everything |
