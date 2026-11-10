# Behind The Things: skills for code-animated explainer shorts

These are the agent skills behind **[Behind The Things](https://behindthethings.com)**, a channel of 50-second explainers about how everyday things work. Every frame is drawn in code, and every claim has a source.

Watch the output: [YouTube @behindthethingshq](https://www.youtube.com/@behindthethingshq) · [Instagram @behindthethingshq](https://www.instagram.com/behindthethingshq/)

Each skill is a folder with a `SKILL.md`, in the [Agent Skills](https://agentskills.io) format used by Claude Code and other agents. Together they cover the whole line, from a fact-checked hook to a release scheduled on every platform.

| Skill | Use it when |
|---|---|
| [`running-an-explainer-channel`](skills/running-an-explainer-channel/SKILL.md) | Starting or running the channel: niche, look, batches, subagents, review, accounts, measuring what works |
| [`scripting-explainer-shorts`](skills/scripting-explainer-shorts/SKILL.md) | Writing or fact-checking a 45–60 s script, its hook and its sources |
| [`voicing-and-captioning-shorts`](skills/voicing-and-captioning-shorts/SKILL.md) | TTS narration, loudness, word timings, speech-synced captions, a music bed |
| [`animating-shorts-in-hyperframes`](skills/animating-shorts-in-hyperframes/SKILL.md) | Building the 1080×1920 animation in [HyperFrames](https://hyperframes.heygen.com) from a tested template |
| [`publishing-shorts`](skills/publishing-shorts/SKILL.md) | Scheduling on YouTube Shorts, Instagram Reels and your site at one release time |
| [`making-long-form-explainers`](skills/making-long-form-explainers/SKILL.md) | A 6–8 minute 16:9 explainer from the same pipeline: deciding, chapters, parallel chapter agents, music sections, SRT, release |

## Install
```bash
git clone https://github.com/Livin21/behind-the-things-skills
cp -R behind-the-things-skills/skills/* ~/.claude/skills/      # all projects
# or: cp -R behind-the-things-skills/skills/* <project>/.claude/skills/
```
Start a new agent session so the skills load. Then ask for something like *"Make an episode about how a zipper works"*.

**You'll need:**
- Node 22+ and ffmpeg
- The HyperFrames CLI (`npx hyperframes`) and its `hyperframes` skills
- A text-to-speech voice (the examples use Higgsfield's ElevenLabs voices)
- A browser-automation tool, for publishing

## Make it yours
Your project keeps two files that every episode reads:
- **`DESIGN.md`:** the look, in numbers. Start from [`DESIGN.example.md`](skills/animating-shorts-in-hyperframes/template/DESIGN.example.md).
- **`CHANNEL.md`:** voice, music, fonts, tool versions, sign-off line and release slot. Start from [`CHANNEL.example.md`](skills/running-an-explainer-channel/CHANNEL.example.md).

The example style ("Graph Paper") is intentionally different from Behind The Things' own look.

## How the skills were tested
See [TESTING.md](TESTING.md). It records each failure observed while making the first episodes without these skills, and the results of producing new episodes with them.

## License
MIT. If you make something with these, tag **@behindthethingshq**; we'd love to see it.
