---
name: scripting-explainer-shorts
description: Use when writing or fact-checking the narration for a short (under 60 seconds) educational video about how something works, when choosing or verifying a hook, when a source won't open or contradicts itself, or when writing on-screen labels, descriptions or web copy that state facts about an episode.
---

# Scripting explainer shorts

## Overview
An explainer is only as good as its weakest claim. **Every factual sentence and every on-screen number needs a source you actually opened.** A hook that sounds great is usually the least true line in the draft, so verify it first and rewrite it if it fails.

## Process
1. **Verify the hook first.** Find a primary source (a standards body, manufacturer, government agency, university or published source code) that states it. Then:
   - **It fails:** rewrite it to what the source says. "The stripes aren't the number" became "the barcode doesn't know the price"; "a speck of radioactive metal" became "something radioactive" (it's an oxide, too small to see).
   - **It holds with a nuance:** keep it, adjust words to match the source, and carry the nuance in a beat ("doesn't cook from the inside out" → the waves do heat about an inch in).
   - **It's provable only for some cases:** keep it general, attribute every specific number to its source ("Android's default…", "Windows…"), and record the gap as partly verified.
2. **Research the beats.** Open each source rather than trusting a search snippet, and quote the supporting line. Pick the strongest source that states the claim:

   | Rank | Source | Example |
   |---|---|---|
   | 1 | Standards bodies, specifications, published source code | EMVCo, ISO/IEC catalogue page, NFC Forum, GS1, AOSP |
   | 2 | Government agencies, regulators, central banks | NRC, EPA, FDA, USDA, Federal Reserve, ECB |
   | 3 | The maker's own documentation | Visa, Mastercard, NXP datasheets, Microsoft Learn |
   | 4 | Universities, textbooks, peer-reviewed papers | university course notes, conference papers |
   | 5 | Reputable explainers and press | only when 1–4 don't state it |

   Never cite a mirror or re-host (IPFS or other Wikipedia copies, PDF re-uploads), a content farm, an SEO blog or vendor marketing. If only a mirror opens, find the original page or an archived copy of it. Wikipedia (or a copy of it) can lead you to a source: follow the article's reference, open it, and cite that.
   - **A page won't open:** try another fetcher, then an archived copy. If you use an archive, label it. If nothing loads, hedge the line or cut it.
   - **The source contradicts itself or physics:** speak the correct figure plainly ("about five inches") and show the working in `sources.md`. Note the source's own figure under "Simplified on purpose". Example: c ÷ 2450 MHz = 12.2 cm ≈ 5 in, not the USDA's rounded "4 in".
   - **An inference** (true by reasoning, but no source says it in one line): mark it as an inference in `sources.md`.
3. **Write the narration** (shape below).
4. **Fit the budget.** The cap is `54 × (the voice's words per second)`, taken from the project's `CHANNEL.md`; it's about 140 words for a 2.6 words-per-second voice. The spoken sign-off is included. Count with `wc -w`; a hyphenated word counts as one.
5. **Scene table and packaging** (see the template in `templates.md`).
6. **Write `sources.md`** with the template: one row per claim, including every number shown on screen in tags or readouts, then "Simplified on purpose" and "Partly verified".

## Narration shape
1. **Hook (0–3 s):** a surprising true fact, said over the object, which is fully drawn in frame one.
2. **The reveal:** open the object and show what's inside. If the "thing" is abstract (an icon, a signal), reveal the device that produces it, such as the phone's radio for Wi-Fi bars. Pick the drawn view so the reveal exposes the insides, and make the verb match the motion ("lift the cover").
3. **Three beats:** what's inside → how it works → what nobody expects.
4. **Twist line:** the fact people repeat to a friend.
5. **Sign-off:** the channel's fixed line.

Write for the ear: short sentences, and spell numbers as spoken. Add voice notes for risky words, which become respellings in the TTS prompt.

## Every other text
On-screen tags, YouTube descriptions, captions and site pages may only state claims that are already in `sources.md`. Adding a "small" fact while writing copy is how errors ship.

## Common mistakes
| Mistake | Fix |
|---|---|
| Keeping a catchy hook that's "basically true" | Rewrite it to what the source says |
| Repeating a source's rounding error | Check against physics or a second source; show the working |
| Tags with unsourced numbers | Add a source row for every on-screen figure |
| 148 words for a slow voice | Use the voice's measured pace; cap at 54 × pace |
| Silently dropping an unopenable source | Hedge or cut the line; record it as partly verified |
| Citing a vendor blog or a Wikipedia mirror | Go up the table: the spec, the regulator, the maker |
