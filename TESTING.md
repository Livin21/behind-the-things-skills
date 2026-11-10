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
