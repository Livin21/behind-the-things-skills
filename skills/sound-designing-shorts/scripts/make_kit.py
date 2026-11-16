"""Behind The Things sound-effects kit: every sound synthesised in code (no samples, no licences).

Usage:  python3 -I make_kit.py <out_dir>
Writes 48 kHz mono float WAVs, each peaking at -3 dBFS. Mix levels are set by remix.py, not here.
Design notes: short, bright, paper-and-plastic. Most sounds are under 120 ms, centred 2.5-5 kHz, like the
measured reference (SKILL.md). Tonal sounds sit in D major to agree with the music bed.
"""
import os, sys
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt

SR = 48000
RNG = np.random.default_rng(7)  # deterministic kit


def t_(dur):
    return np.arange(int(SR * dur)) / SR


def env_exp(dur, tau, attack=0.0005):
    t = t_(dur)
    a = np.clip(t / attack, 0, 1) if attack > 0 else 1.0
    return a * np.exp(-t / tau)


def bp(x, lo, hi, order=4):
    return sosfilt(butter(order, [lo, hi], btype="band", fs=SR, output="sos"), x)


def hp(x, f, order=2):
    return sosfilt(butter(order, f, btype="high", fs=SR, output="sos"), x)


def lp(x, f, order=2):
    return sosfilt(butter(order, f, btype="low", fs=SR, output="sos"), x)


def noise(dur):
    return RNG.standard_normal(int(SR * dur))


def sine(freq, dur, phase=0.0):
    t = t_(dur)
    if callable(freq):
        ph = 2 * np.pi * np.cumsum(freq(t)) / SR
    else:
        ph = 2 * np.pi * freq * t
    return np.sin(ph + phase)


def swept_bp(x, f0, f1, width=0.6, blocks=48):
    """Band-pass whose centre glides from f0 to f1 (block-wise, crossfaded)."""
    n = len(x); out = np.zeros(n); step = n // blocks
    for i in range(blocks):
        a, b = i * step, n if i == blocks - 1 else (i + 1) * step + step // 2
        fc = f0 * (f1 / f0) ** (i / max(1, blocks - 1))
        seg = bp(x[max(0, a - step // 2):b], fc * (1 - width / 2), min(fc * (1 + width / 2), SR / 2 - 100), 2)
        seg = seg[(a - max(0, a - step // 2)):][: (b - a)]
        w = np.ones(len(seg)); fade = min(step // 2, len(seg))
        w[:fade] = np.linspace(0, 1, fade) if i else 1; w[-fade:] = np.minimum(w[-fade:], np.linspace(1, 0, fade)) if i < blocks - 1 else w[-fade:]
        out[a:a + len(seg)] += seg * w
    return out


def place(dst, src, at):
    i = int(at * SR); dst[i:i + len(src)] += src[: max(0, len(dst) - i)]
    return dst


def norm(x, peak_db=-3.0):
    x = x - np.mean(x)
    fade = int(0.002 * SR); x[-fade:] *= np.linspace(1, 0, fade)
    return (x / (np.max(np.abs(x)) + 1e-9) * 10 ** (peak_db / 20)).astype(np.float32)


# ---------- the kit ----------
def tick(pitch=3200):
    d = 0.035
    click = bp(noise(d), 2500, 9000) * env_exp(d, 0.004)
    tone = sine(pitch, d) * env_exp(d, 0.006) * 0.6
    return click + tone


def digit(pitch=2200):
    d = 0.02
    return bp(noise(d), 3000, 7500) * env_exp(d, 0.0025) * 0.8 + sine(pitch, d) * env_exp(d, 0.003) * 0.5


def dot():
    d = 0.07
    return sine(lambda t: 1600 - 2500 * t, d) * env_exp(d, 0.016, attack=0.002)


def blip(semitone=0):
    d = 0.08; f = 880 * 2 ** (semitone / 12)
    return (sine(f, d) + 0.2 * sine(3 * f, d)) * env_exp(d, 0.022, attack=0.002)


def switch():
    d = 0.14; x = np.zeros(int(SR * d))
    place(x, tick(3600), 0.0)
    clunk = bp(noise(0.08), 300, 1500) * env_exp(0.08, 0.012) + sine(180, 0.08) * env_exp(0.08, 0.02) * 0.7
    place(x, clunk * 0.9, 0.045)
    return x


def lift():
    d = 0.36; t = t_(d)
    shape = np.minimum(t / 0.2, 1) * np.clip((d - t) / 0.16, 0, 1)
    return swept_bp(noise(d), 800, 3600, 0.7) * shape


def wipe():
    d = 0.32; t = t_(d)
    shape = np.minimum(t / 0.12, 1) ** 1.5 * np.clip((d - t) / 0.2, 0, 1)
    grain = 0.75 + 0.25 * lp(RNG.standard_normal(len(t)), 60, 1) / 0.1
    x = swept_bp(hp(noise(d), 400), 2000, 6000, 0.9) * shape * np.clip(grain, 0.3, 1.3)
    return x


def marker():
    d = 0.3; t = t_(d)
    shape = np.minimum(t / 0.04, 1) * np.clip((d - t) / 0.1, 0, 1)
    rough = np.clip(0.7 + 0.3 * lp(RNG.standard_normal(len(t)), 120, 1) / 0.08, 0.2, 1.4)
    return bp(noise(d), 3000, 9500) * shape * rough * 0.8


def stamp():
    d = 0.2; x = np.zeros(int(SR * d))
    thunk = sine(lambda t: 95 - 120 * t, d) * env_exp(d, 0.04, attack=0.001) + bp(noise(d), 200, 1200) * env_exp(d, 0.015) * 0.6
    place(x, thunk, 0.0); place(x, tick(2800) * 0.5, 0.008)
    return x


def bell(f, d, tau):
    parts = [(1, 1.0), (2.76, 0.35), (5.4, 0.12)]
    return sum(a * sine(f * r, d) * env_exp(d, tau / r ** 0.5, attack=0.003) for r, a in parts)


def reveal():
    d = 1.0; x = np.zeros(int(SR * d))
    place(x, sine(lambda t: 72 - 20 * t, 0.5) * env_exp(0.5, 0.12, attack=0.002) * 0.9, 0.0)
    place(x, bell(1174.66, 0.8, 0.35) * 0.35, 0.02)    # D6
    place(x, bell(1760.0, 0.8, 0.35) * 0.3, 0.14)      # A6
    return x


def lockup():
    d = 0.7
    return sum(bell(f, d, 0.32) for f in (587.33, 739.99, 880.0)) / 3


KIT = {
    "tick": lambda: tick(), "tick-hi": lambda: tick(3800), "tick-lo": lambda: tick(2700),
    "digit": lambda: digit(), "digit-hi": lambda: digit(2600), "digit-lo": lambda: digit(1900),
    "dot": dot, "switch": switch, "lift": lift, "wipe": wipe, "marker": marker, "stamp": stamp,
    "reveal": reveal, "lockup": lockup,
    **{f"blip{s:+d}": (lambda s=s: blip(s)) for s in (0, 2, 4, 7, 9, 12)},
}


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "kit"
    os.makedirs(out, exist_ok=True)
    for name, fn in KIT.items():
        x = norm(np.asarray(fn(), dtype=np.float64))
        wavfile.write(os.path.join(out, f"{name}.wav"), SR, x)
        print(f"{name:10} {len(x) / SR * 1000:6.0f} ms")


if __name__ == "__main__":
    main()
