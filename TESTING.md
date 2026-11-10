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

| Episode | Agent result | Gaps reported | Fixed in |
|---|---|---|---|
| 005 Microwave | _pending_ | | |
| 006 Wi-Fi Bars | _pending_ | | |
| 007 Smoke Detector | _pending_ | | |
