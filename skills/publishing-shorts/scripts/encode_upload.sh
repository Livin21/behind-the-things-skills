#!/usr/bin/env bash
# Make a browser-upload copy (< 10 MB for a ~55 s 1080x1920 short) from a master render.
# Usage: bash encode_upload.sh <master.mp4> <out.mp4> [video_kbps] [cover.jpg]
# With a cover, frame 0 is replaced by the cover (1/30 s, imperceptible on playback), so any player
# or share preview that grabs the first frame (YouTube's auto thumbnails, X, Slack, Discord) shows it.
# Frame count, duration and audio are unchanged.
set -euo pipefail
in="$1"; out="$2"; kbps="${3:-1180}"; cover="${4:-}"
dir="$(mktemp -d)"
if [ -n "$cover" ]; then
  inputs=(-i "$in" -i "$cover")
  vf=(-filter_complex "[1:v][0:v]scale2ref[c][v];[v][c]overlay=0:0:enable='eq(n\,0)'[o]" -map "[o]")
  amap=(-map "0:a?")
else
  inputs=(-i "$in"); vf=(); amap=()
fi
ffmpeg -hide_banner -loglevel error -y "${inputs[@]}" "${vf[@]}" -c:v libx264 -preset slow -b:v "${kbps}k" -pass 1 -passlogfile "$dir/pass" -an -f null /dev/null
ffmpeg -hide_banner -loglevel error -y "${inputs[@]}" "${vf[@]}" "${amap[@]}" -c:v libx264 -preset slow -b:v "${kbps}k" -pass 2 -passlogfile "$dir/pass" \
  -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$out"
rm -rf "$dir"
size=$(wc -c < "$out")
echo "$out: $((size / 1024)) KB"
if [ "$size" -gt 10000000 ]; then echo "WARNING: over 10 MB - rerun with a lower kbps (e.g. 1000)"; fi
