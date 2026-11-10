# CHANNEL.md (example)

Read this first, then `DESIGN.md`, then one finished episode (`episodes/<latest>/`).

| Asset | Value |
|---|---|
| Narrator | `<tts tool + exact params>`, e.g. Higgsfield `text2speech_v2`, `variant: elevenlabs`, `voice_type: preset`, `voice_id: <id>`. The job is async; download `result_url`. |
| Voice pace | `<measured words/second on the pilot>`, so the cap is `54 × pace` words |
| Music bed | `<path>` (`<length>` s, `<LUFS>`). Copy it into each episode's `video/assets/`; it must be ≥ the video length |
| Fonts | `<paths to woff2>`; missing glyphs: `<e.g. no → in the mono font>` |
| Tool versions | `hyperframes@<x.y.z>` |
| Brand tag | `<pattern>` at `<position>` |
| Sign-off line | "<fixed spoken line>"; card: `<lockup text>` |
| Folders | `episodes/NNN-slug/` → `script.md`, `sources.md`, `narration.txt`, `video/` |
| Release slot | `<days> at <time tz>` |
| Publishing log | `<path>` |
| Template token mapping | `--accent` = `<brand accent>`; `--flow` = `<flow colour>`; `--display` / `--mono` = `<fonts>` |
