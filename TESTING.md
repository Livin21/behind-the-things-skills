# How these skills were tested

The skills follow test-driven development for documentation: first record what goes wrong without the skill (RED), then write the skill so it addresses those failures, then check that agents using the skill avoid them (GREEN), and fix any new gaps (REFACTOR).

## RED: failures observed without the skills

These came from producing the first four episodes of [Behind The Things](https://behindthethings.com) (Card Tap, Barcode, QR Code, Traffic Light), with agents working from ad-hoc briefs.

| # | Stage | What went wrong | Caught by | Skill that now prevents it |
|---|---|---|---|---|
| 1 | Script | Draft hook "the stripes aren't the number" was false: the stripes are the number | Fact-check pass | scripting-explainer-shorts |
| 2 | Script | "Rip off a third and it still scans" overstated QR error correction (30% of codewords at level H, not 30% of area) | Fact-check pass | scripting-explainer-shorts |
| 3 | Site copy | A summary added a claim the sources didn't support ("agree before the beep"; the terminal beeps when the card read finishes, before approval) | Self-review | scripting-explainer-shorts |
| 4 | Captions | Whisper collapsed "one, one, three, one, one" into one token placed 1.7 s late; onsets drifted 0.1–0.35 s | Agent review | voicing-and-captioning-shorts |
| 5 | Animation | Scene-wipe panel stuck covering the frame: CSS `translateY` plus GSAP `yPercent` added together | `check` (text occluded) | animating-shorts-in-hyperframes |
| 6 | Animation | Fonts used without `@font-face`, failing the StaticGuard contract | `check` | animating-shorts-in-hyperframes |
| 7 | Animation | Slow push-in grew objects into the caption zone on long scenes | Contact-sheet review | animating-shorts-in-hyperframes |
| 8 | Animation | SVG rings scaled from the top-left corner (GSAP's default origin for SVG) | Contact-sheet review | animating-shorts-in-hyperframes |
| 9 | Animation | Off-screen items started too close to the edge and peeked into frame early | Contact-sheet review | animating-shorts-in-hyperframes |
| 10 | Animation | Fixed-width labels wrapped onto two lines; a moving packet covered labels | `check` plus review | animating-shorts-in-hyperframes |
| 11 | Animation | The first frame was empty paper, so the platforms' default cover was blank | Publishing | animating-shorts-in-hyperframes, publishing-shorts |
| 12 | Publish | YouTube banner text cut off: designed for 1546×423, but the all-devices safe area is 1235×338 | Banner crop tool | publishing-shorts |
| 13 | Publish | The chosen handle was free as typed, but YouTube treats `.`/`_` variants as the same handle | Channel creation | publishing-shorts |
| 14 | Publish | The agent tried to create an account itself; it must not, and YouTube also requires phone verification | Policy, then platform | running-an-explainer-channel |
| 15 | Publish | Browser file uploads were capped at about 10 MB, but the master render was 28 MB | Upload tool | publishing-shorts |
| 16 | Publish | The Instagram web composer can't schedule | Exploration | publishing-shorts |
| 17 | Publish | Meta Business Suite's "Add video" opens a native file picker that automation can't reach | Exploration | publishing-shorts |
| 18 | Publish | Hashtag autocomplete merged two tags into "#learnsometh#learnsomethingnew2024" | Visual check | publishing-shorts |
| 19 | Site | Next.js 16 with Cache Components rejected `dynamicParams`; unknown slugs returned a soft 200 instead of a 404 | Build, then curl | publishing-shorts (site-release.md) |

## GREEN: episodes 005–007 produced with the skills

Each episode is produced by a fresh agent. Its brief contains only the topic, the paths to these skills and the project's DESIGN.md. Every agent writes `SKILL-FEEDBACK.md`, listing each gap, ambiguity or error it found in the skills.

| Episode | Agent result (with skills v0) | Main gaps reported | Fixed in v1 |
|---|---|---|---|
| 005 Microwave | Rendered first time; `check` had 0 errors. The hook held (FDA and USDA). Review found a sourced-but-imprecise number (USDA "4 in" vs 12.2 cm) | Loudness recipe missed its target (4 renders to fix); word budget assumed 2.75 words/s but the voice read 2.46; blank frame 0 in the template; the reveal wasn't covered | `normalize_voice.sh`; budget = 54 × measured pace; hook fully drawn at t = 0; reveal guidance; "source contradicts physics" rule |
| 006 Wi-Fi Bars | Rendered; `check` had 0 errors. The hook held (Android source, Windows docs) | Loudness; skill vs DESIGN.md conflicts with no precedence rule; timing repair assumed a visible waveform; no pronunciation check | Precedence rule; `fix_timings.py`; `diff_words.py`; render-loudness formula |
| 007 Smoke Detector | Rendered; `check` had 0 errors. Hook **corrected**: "radioactive metal / speck" → "something radioactive" (it's an oxide, about 0.3 µg) | Loudness; 148 words ran over 58 s; no timing tool (the agent wrote its own); captions followed a stale DESIGN.md rule | Per-voice budget; `fix_timings.py` (generalised from the agent's script); "update DESIGN.md to match the approved pilot" |

All three agents avoided every RED-table animation trap that the v0 skill listed (wipe, fonts, push-in, SVG origin, off-canvas starts, overlaps). New failures they found are now traps 7, 9, 11, 13 and 14 in `traps.md`.

**v1 verification:** a fresh agent answered 15 application questions using only the v1 skills. Covered: loudness maths, the frame-0 rule, token counts, cut placement, unopenable and contradictory sources, precedence, word cap, Instagram scheduling, handles, expected warnings, state changes, folder contents, account creation. All 15 were answered correctly, with file citations. It also reported 8 minor ambiguities (whether to re-normalise or only change `data-volume`, the cut position inside a pause, wording a corrected figure, hyphens in handles, the folder list, "two looks", the version pin, the cover timestamp); all 8 were fixed in v1.1. Episode 005's fix was redone with the v1 tools (`fix_timings.py`, `normalize_voice.sh`).

## REFACTOR: testing the timing tool against hand-verified data

The 005 agent re-ran its episode with `fix_timings.py` v1 and found 7 faults: a sentence-final word placed after its pause, words wholly inside a pause, crushed 0.02 s words, overlaps passing the check, words spanning a pause, a stale raw copy that could undo a re-voice, and no clamp to the audio length.

Each candidate fix was scored against the agents' hand-verified transcripts for 005–007, counting words more than 0.15 s from the hand value:

| Version | 005 onsets / ends | 006 onsets / ends | 007 onsets / ends | Notes |
|---|---|---|---|---|
| Raw Whisper | 16 / 35 | 3 / 19 | 11 / 17 | Baseline |
| v1 (snap onsets, clamp ends) | 16 / 23 | 6 / 4 | 5 / 12 | Had the 7 faults above |
| Segment-fit rewrite | 65 / – | 60 / – | 97 / – | **Rejected:** stretching whole segments distorted correct words |
| Chunked re-transcription | 44 / – | 34 / – | 75 / – | **Not shipped:** the hand data is biased toward raw Whisper, so its benefit can't be shown |
| **v3 (shipped)** | **16 / 22** | **5 / 8** | **4 / 7** | Targeted fixes for all 7 faults; idempotent; detects a changed audio file |

Known limit (documented in the skill): a breath right after a pause can pull an onset early (006 "Lift"), and mid-sentence drift (005) still needs a one-sentence re-transcription.

## v1.2: publishing failures from the 005–007 release, then two retrieval tests

Failures seen while scheduling 005–007 for real:
- **Merged hashtags:** typing `#tag` straight into Meta Business Suite merged tags twice ("#learnsometh#MicrowaveOven", "#ph#scienceexperiment").
- **Thumbnail:** no suggested thumbnail showed the hook caption.
- **Stale clicks:** a window resize moved YouTube's Next and Schedule buttons, so clicks at the old coordinates missed.
- **Slow listing:** a newly scheduled reel took about 30 s to appear.

Ideas taken from an outside review of the channel: question-style platform titles, a ranking of sources by authority (episode 001 relied on a Wikipedia mirror on IPFS), and a measurement stage.

Each fix was written into the skills, then a fresh agent answered 8 scenarios using only the skills.

**First test:** it found 11 gaps. The most serious:
- No stage required the review and the human listen before release.
- "Behind the ___ as the title pattern" contradicted the new question-title rule.
- Nothing said what to do when a reel is missing from Scheduled.
- The repair for merged hashtags was underspecified.
- "Cadence line" and "the publishing folder" were never defined.

All 11 were fixed.

**Second test:** a fresh agent answered 6 scenarios on the fixed text. It found 5 remaining issues:
- The new review stage could be marked done by sending the owner timestamps, with nobody having listened.
- "Missing reel" had no action for each outcome.
- The hashtag repair needed the original tag list.
- "Matching titles" in the publishing overview.
- Two wording mismatches.

All 5 were fixed. The review stage now requires the listen before release time; scheduling earlier is allowed, but a problem found then means replacing the upload or unscheduling everywhere.
