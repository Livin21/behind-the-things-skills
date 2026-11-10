#!/usr/bin/env bash
# Normalise a (mono) TTS narration so the RENDERED video lands at about -13.7 LUFS.
# A mono voice plays on both channels of the stereo render and measures ~3 LU louder there,
# so the mono file is set to -16.5 LUFS by default. Gain + true-peak-safe limiter
# (single-pass loudnorm stops short of the target on peaky TTS voices).
# Usage: bash normalize_voice.sh <in.mp3> <out.wav> [target_lufs]
set -euo pipefail
in="$1"; out="$2"; target="${3:--16.5}"
measure() { ffmpeg -hide_banner -i "$1" -af loudnorm=print_format=summary -f null - 2>&1 | awk '/Input Integrated/{print $3}'; }
I=$(measure "$in")
gain=$(python3 -c "print(round($target - ($I), 2))")
ffmpeg -hide_banner -loglevel error -y -i "$in" \
  -af "volume=${gain}dB,alimiter=limit=0.89:level=false:attack=3:release=60" -ar 48000 "$out"
echo "in: $I LUFS  gain: ${gain} dB  out: $(measure "$out") LUFS  (target $target, mono)"
