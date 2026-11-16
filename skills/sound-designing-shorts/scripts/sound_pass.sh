#!/usr/bin/env bash
# Sound pass for a rendered short: cues from its own timeline, the approved "bold" v2 mix, -14 LUFS master.
# Usage (from anywhere):  bash sound_pass.sh <video-dir> <render.mp4> [out.mp4]
# Default output: <render>-sound.mp4 next to the render. The video stream is copied untouched.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
dir="$(cd "$1" && pwd)"; render="$(cd "$(dirname "$2")" && pwd)/$(basename "$2")"
out="${3:-${render%.mp4}-sound.mp4}"
[ -d "$here/node_modules/puppeteer-core" ] || (cd "$here" && npm install --silent --no-audit --no-fund)
[ -f "$here/kit/lockup.wav" ] || python3 -I "$here/make_kit.py" "$here/kit" >/dev/null
node "$here/extract_cues.mjs" "$dir"
python3 -I "$here/remix.py" --project "$dir" --video "$render" --out "$out"
