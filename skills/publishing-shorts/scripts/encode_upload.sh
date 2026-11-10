#!/usr/bin/env bash
# Make a browser-upload copy (< 10 MB for a ~55 s 1080x1920 short) from a master render.
# Usage: bash encode_upload.sh <master.mp4> <out.mp4> [video_kbps]
set -euo pipefail
in="$1"; out="$2"; kbps="${3:-1180}"
dir="$(mktemp -d)"
ffmpeg -hide_banner -loglevel error -y -i "$in" -c:v libx264 -preset slow -b:v "${kbps}k" -pass 1 -passlogfile "$dir/pass" -an -f null /dev/null
ffmpeg -hide_banner -loglevel error -y -i "$in" -c:v libx264 -preset slow -b:v "${kbps}k" -pass 2 -passlogfile "$dir/pass" \
  -pix_fmt yuv420p -c:a aac -b:a 160k -movflags +faststart "$out"
rm -rf "$dir"
size=$(wc -c < "$out")
echo "$out: $((size / 1024)) KB"
if [ "$size" -gt 10000000 ]; then echo "WARNING: over 10 MB - rerun with a lower kbps (e.g. 1000)"; fi
