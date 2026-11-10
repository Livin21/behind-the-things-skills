---
name: publishing-shorts
description: Use when uploading, scheduling or setting up accounts for short vertical videos on YouTube Shorts and Instagram Reels through browser automation, preparing upload files and covers, releasing episode pages on a website at the same time, or when uploads exceed size limits, covers come out blank, or Instagram won't schedule.
---

# Publishing shorts

## Overview
A release is one moment: YouTube, Instagram and the website all go public at the same scheduled time, with matching covers, copy and links (titles follow step 3; Instagram has no title field). Prepare the files once, schedule everything, and log every ID.

## Before the first release (owner does the accounts)
- **Never create accounts or type passwords.** Give the owner the exact name and handle, and let them sign up or sign in. Then you do the profile, uploads and scheduling.
- **Handles:** check every platform first. YouTube treats `behind.the.things`, `behind_the_things` and `behindthethings` as the same handle, so add **letters only** (for example `behindthethingshq`): no dots, underscores, hyphens or random suffixes. Use the same handle everywhere.
- Profile details are in `youtube.md` (banner safe area, avatar) and `instagram.md` (Creator account, bio link).

## Per episode
1. **Upload copy.** Browser file uploads can be capped at about 10 MB per call. Make a copy from the master render: `bash scripts/encode_upload.sh <master.mp4> <out.mp4>` (2-pass, about 1.2 Mbps; a 55 s short comes to about 9 MB). Keep the master for anything else.
2. **Cover.** Use the episode's `renders/cover.jpg`: a frame at about 2–3 s where the hook object and its caption are both visible. If it's missing: `ffmpeg -ss <t> -i master.mp4 -frames:v 1 -q:v 2 cover.jpg`. Never use the platform's default frame.
3. **Copy.** Write the title, YouTube description and Instagram caption from the script's packaging and its sourced claims only:
   - title: the question a viewer would type into search, which the video answers ("Do Wi-Fi Bars Measure Your Internet Speed?"), not a statement of the twist
   - first line: the hook, from the script's Packaging
   - then 2–3 sentences
   - then "Sources and the full explainer: <site>/episodes/<slug>"
   - then the cadence line from `CHANNEL.md`, and 5–6 hashtags (on YouTube, `#shorts` is one of them)
4. **Schedule YouTube**: see `youtube.md`.
5. **Schedule Instagram**: see `instagram.md`. The web app can't schedule, so use Meta Business Suite.
6. **Website**: give the episode page the same release time. See `site-release.md`.
7. **Log it**: episode, title, YouTube ID, Instagram status, site slug and release time, in the project's publishing log.

## Quick reference
| Thing | Value |
|---|---|
| YouTube banner | 2560×1440; text inside the centred **1235×338** |
| Avatar | 800×800, a simple mark readable at 40 px |
| Shorts detection | Vertical, ≤ 3 min, automatic |
| Made for kids | No (for adult explainers) |
| YouTube "AI use" question | Answer against its listed cases (real person, real-event footage, realistic scene, AI music as the main focus). A synthetic narrator over a drawn animation matches none of them. |
| Instagram "AI label" | For realistic AI photos and video; not for drawn animation |
| Time zone | Use the channel owner's local time on every platform |

## Common mistakes
| Mistake | Fix |
|---|---|
| Uploading the 28 MB master through the browser | Use the upload copy |
| Using the platform's default cover | Upload or choose the hook frame |
| Hashtags merged by autocomplete | Type the tags as plain words, then add each "#" in place (`instagram.md` step 4); zoom in before scheduling |
| A site page that appears before the video (or after it) | Use the same release time; the site checks the time itself |
| Typing "1930" into a segmented time field | Type the hour and the minutes separately, then verify |
| Clicking stale coordinates after a resize | Use `find` refs, or re-measure from a fresh screenshot |
