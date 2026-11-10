---
name: voicing-and-captioning-shorts
description: Use when generating narration for a short video with text-to-speech, normalising its loudness, getting word-level timings, building speech-synced captions, or adding a music bed under a voice - including when Whisper timings drift, numbers transcribe as one token, or captions don't match the script.
---

# Voicing and captioning shorts

## Overview
The voice is the clock: scene cuts and captions are timed from its word timestamps. Get clean audio and trustworthy timings, and everything downstream lines up. The script wording always wins over the transcriber's spelling.

## Process
1. **Generate the narration** with the channel's single fixed voice. Speak the script's narration exactly. Example: Higgsfield `text2speech_v2`, `variant: "elevenlabs"`, a preset `voice_id` (about 2.4 credits for 150 words). Save it to `assets/narration.mp3`.
2. **Normalise the loudness:**
   `ffmpeg -i assets/narration.mp3 -af loudnorm=I=-14:TP=-1.0:LRA=11 -ar 48000 assets/narration_norm.wav`
   Measure it with `-af loudnorm=print_format=summary -f null -`.
3. **Get the word timings:**
   `npx hyperframes transcribe assets/narration.mp3 --model small.en --language en` (writes `assets/transcript.json`).
4. **Check the transcript against the script.**
   - The word count should match the script's (numbers may differ: "1974" is one token).
   - Look for collapsed runs ("one, one, three, one, one" → one late token) and onsets drifting late at sentence starts.
   - If either happens, re-transcribe sentence by sentence (cut with ffmpeg at the silences) and merge. Hand-set any onset you can see in the waveform.
5. **Build the captions.** Write `captions.spec.json` as `[word_count, "display text", emphasis_index]` groups, then run
   `python3 -I scripts/build_captions.py assets/transcript.json captions.spec.json index.html`.
   It injects `CAPTION_GROUPS` between the `/*CAPTIONS:BEGIN*/` and `/*CAPTIONS:END*/` markers.
6. **Add the music bed** (if the channel uses one): see below.

## Caption grouping
- Make groups of 2–7 words at phrase boundaries; allow two lines (about 88 px heavy sans for 1080 wide).
- Use one emphasis word per group: the key noun or number, highlighted with the accent colour. Use -1 for none.
- Write display text in the script's wording, not the transcriber's ("city-centre", "nearer").
- The builder ends a group at the next group's start, or 0.25 s after its last word when the gap is longer than 0.45 s.
- "line_unread" or caption-hold warnings are expected with speech-synced captions. Don't stretch the timing to silence them.

## Music bed
- Use one instrumental, reused in every episode. Generated music is fine if the licence is commercial (for example ElevenLabs Music: `force_instrumental: true`, duration = video length).
- Leave the source at about −17 LUFS. Under the voice, set a volume automation lane at **0.28** (about −28 LUFS), lift it to **0.5** about 0.2 s after the last word, and fade out over 1.2 s.
- Verify by measuring a gap between sentences: the mix there should equal the bed alone.

## Common mistakes
| Mistake | Fix |
|---|---|
| Captions copied from Whisper | Use the script's words and spelling |
| Trusting sentence-start timings blindly | Spot-check 3 onsets against the waveform |
| A new voice per episode | One voice is part of the brand |
| Music at speech level | 0.28 gain under the voice; measure the gap |
| Regenerating the voice to fix a caption | Captions are text; fix the spec |
