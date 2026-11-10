---
name: scripting-explainer-shorts
description: Use when writing or fact-checking the narration for a 45-60 second educational short (YouTube Shorts, Reels, TikTok) about how something works, when choosing or verifying a hook, or when writing captions, descriptions or web copy that state facts about an episode.
---

# Scripting explainer shorts

## Overview
An explainer is only as good as its weakest claim. **Every factual sentence needs a source you actually opened.** A hook that sounds great is usually the least true line in the draft, so verify it first and rewrite it if it fails.

## Process
1. **Verify the hook before writing anything else.** Find a primary source (a standards body, manufacturer, government agency or university) that states it. If the source says something narrower, the hook becomes the narrower, true version. Examples of draft hooks that failed:
   - "The stripes aren't the number" → the stripes *are* the number. The true surprise: the price isn't in the barcode.
   - "Rip off a third and it still scans" → only about 30% of *codewords* at the top level, and most codes are set nearer 15%.
2. **Research the beats.** Open each source rather than trusting a search snippet. Note the exact supporting line.
3. **Write the narration** (shape below).
4. **Count the words.** The budget is 125–148 words, which at a typical TTS pace of about 2.75 words per second runs 46–54 s, plus a 2 s sign-off.
5. **Write the scene table and packaging** (template below).
6. **Write `sources.md`**: one row per claim, plus a "Simplified on purpose" note for each deliberate simplification.

## Narration shape
1. **Hook (0–3 s):** a surprising true fact, said over the object. The object is on screen in frame one.
2. **The reveal:** open the object up and show what's inside.
3. **Three beats:** what's inside → how it works → what nobody expects.
4. **Twist line:** the fact people repeat to a friend.
5. **Sign-off:** one fixed line, the same every episode (for example "Now you know what's behind the ___.").

Write for the ear: short sentences, spell numbers as spoken ("thirteen and a half million"), and avoid tongue-twisters. Add voice notes for words a TTS voice may mispronounce.

## script.md template
```markdown
# NNN — <Title>
Format: Short, 1080×1920, ≤ 58 s. Word count: N (≈ N/2.75 s).

## Narration (spoken exactly)
<one paragraph per beat>

Voice notes: <pronunciations>

## Scenes
| # | Words | Picture | Accent element |
|---|---|---|---|
| 1 Hook | "first words… last words" | <drawable description, named tags like `PRICE: NOT IN HERE`> | <the one highlighted thing> |

## Packaging
- Title: <curiosity + the object; the video pays it off>
- Instagram first line: <hook, rephrased>
- Cover: <a frame that exists in the video: object + its caption at about 2–3 s>
```

## Rules for every other text
Descriptions, captions and site pages may only restate claims that are already in `sources.md`. Adding a "small" fact when writing copy is how errors ship.

## Common mistakes
| Mistake | Fix |
|---|---|
| Keeping a catchy hook that's "basically true" | Rewrite it to what the source says |
| Citing a search snippet | Open the page; quote the line |
| 170-word scripts | Cut to 148 or fewer; the voice won't speed up |
| A cover line that never appears on screen | Captions are the spoken words; plan the cover from a real frame |
| Unflagged simplifications | List them under "Simplified on purpose" |
