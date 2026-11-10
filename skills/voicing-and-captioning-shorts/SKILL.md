---
name: voicing-and-captioning-shorts
description: Use when generating narration for a short video with text-to-speech, setting its loudness, getting word-level timings, building speech-synced captions, or adding a music bed under a voice - including when renders come out too loud, Whisper timings drift or hang over pauses, numbers transcribe as one token, a word may be mispronounced, or captions don't match the script.
---

# Voicing and captioning shorts

## Overview
The voice is the clock: scene cuts and captions are timed from its word timestamps. Get the loudness right for the **render**, make the timings match the real pauses, and flag anything a human should hear. The script's wording always wins over the transcriber's.

All scripts live in this skill's `scripts/` folder. Call them by absolute path from the episode's `video/` folder. Use the project's pinned HyperFrames version (see its `CHANNEL.md`) wherever this skill says `npx hyperframes`.

## Process
1. **Narration.** Send the script's narration text to the channel's single voice. Write it to `narration.txt` first, so the exact text sent is on disk.
   - Higgsfield example: `generate_audio` with `{"model":"text2speech_v2","variant":"elevenlabs","voice_type":"preset","voice_id":"<id>","prompt":"<text>"}`. The job is async: wait with `jobs_wait`, then download `result_url` to `assets/narration.mp3`.
   - TTS takes text only. A pronunciation fix means respelling the word in the prompt; keep the correct spelling in the captions.
   - Each blank line between paragraphs becomes a 0.5–0.8 s pause. Keep to about 7 paragraphs or fewer.
   - **Regenerate at most once,** and only for a clear mispronunciation, an overlong take or a factual fix.
2. **Loudness.** Run `bash normalize_voice.sh assets/narration.mp3 assets/narration_norm.wav`.
   - It brings the mono file to −16.5 LUFS. A mono voice plays on both channels of the stereo render (about +3 LU), so the render lands at about −13.7.
   - Leave the voice at `data-volume="1"`. Measure the render later.
3. **Word timings.** Run `npx hyperframes transcribe assets/narration.mp3 --model small.en --language en`.
   - It writes `assets/transcript.json` next to the audio, **overwriting** any existing one: `[{"text","start","end",…}]`, one entry per token.
   - Do any extra transcriptions in a scratch folder.
4. **Repair the timings.** Run `python3 -I fix_timings.py assets/narration.mp3 assets/transcript.json`.
   - It fixes only the words around measured pauses: late onsets, sentence-final words pushed into a pause, and ends spanning a pause. It keeps `transcript.raw.json` and refreshes that copy if the audio changes. Re-runs are idempotent. It fails on out-of-order or overlapping words.
   - **Read its printout.** A breath right after a pause can pull an onset too early. If a changed onset isn't followed by speech (spot-check with a 0.5 s `volumedetect` window), put the raw value back by hand. Do hand repairs after the last run.
   - It can't fix drift in the middle of a long sentence. If a cut or emphasised caption lands mid-sentence and looks late, transcribe that sentence alone in a scratch folder (cut it with ffmpeg at its pauses), add the cut's start time, and copy those onsets in.
5. **Flag pronunciation.** Transcribe again with `--model medium.en` in a scratch folder, then run
   `python3 -I diff_words.py narration.txt assets/transcript.json <scratch>/transcript.json`.
   Number-form differences ("55" vs "fifty-five") are fine. Put every other difference in your report as "listen at mm:ss". **A human listens to the hook and the flagged moments before release.**
6. **Caption spec.** Write `captions.spec.json` as `[token_count, "display text", emphasis_index]` groups.
   - **Token counts follow the transcript, not the script.** "1974", "man-made" and "cut-offs" are one token each.
   - **The emphasis index counts words of the display text,** split on spaces. Use `-1` for none.
7. **Inject the captions** (in the animation stage, once `index.html` has the `/*CAPTIONS:BEGIN*/…/*CAPTIONS:END*/` markers): `python3 -I build_captions.py assets/transcript.json captions.spec.json index.html`. It fails on count mismatches, out-of-order timings and bad indices.

## Caption grouping
- **The project's `DESIGN.md` sets the group size.** The default is 2–7 words at phrase boundaries, two lines at most, with one emphasis word per group: the key noun or number.
- Display text uses the script's wording ("city-centre", "nearer"). Show figures and years as digits ("1974", "13.5 million").
- Speech-synced captions always trigger `line_unread` warnings. Don't stretch the timing to silence them.

## Music bed
- Copy the channel's bed into `assets/`. It must be at least as long as the video; if it's shorter, generate a longer one rather than cutting the fade.
- Set a volume lane at **0.28** under the voice (about −28 LUFS), rising to **0.5** about 0.2 s after the last word, and `data-fade-out="1.2"`.
- **Check:** compare a 0.5 s window inside a pause in the render with the bed alone at 0.28. They should match within 0.5 dB.
  `ffmpeg -ss <t> -t 0.5 -i render.mp4 -af volumedetect -f null -` versus `… -i music.mp3 -af "volume=0.28,volumedetect" …`

## After the render
Measure the integrated loudness of the render. If it's outside −13 to −14.5 LUFS, change **only** the voice `data-volume`, to `10^((−13.7 − measured)/20)` (for −11.8 that's 0.80), and render again. Don't re-normalise the file. If it's off by more than 3 LU, first check that `narration_norm.wav` really came from `normalize_voice.sh`.

## Common mistakes
| Mistake | Fix |
|---|---|
| Normalising the narration to −14 | That gives about −11 in the render; use −16.5 for a mono voice |
| Trusting raw Whisper onsets | Run `fix_timings.py`; read its changes |
| Re-transcribing in `assets/` | It overwrites `transcript.json`; use a scratch folder |
| Counting script words for the spec | Count transcript tokens |
| "Sounds fine" with nobody listening | Report the `diff_words.py` moments; a human checks them |
