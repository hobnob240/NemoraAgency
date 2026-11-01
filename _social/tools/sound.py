"""NEMORA background sound: an original, quiet music bed synthesised from scratch (sine and filtered-noise synthesis,
no samples, no copyrighted music, no AI), timed to a reel's scene changes.

    python3 _social/tools/sound.py out.wav --seconds 22.5 --cuts 3.1,8.8,13.5 --seed 3

Layers: a warm chord pad, a soft plucked arpeggio, a low pulse on the beat, and a short airy swell into each scene
change. --seed picks the key, chord progression and tempo, so each video sounds a little different.
"""
import argparse, wave
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve

SR = 44100
ap = argparse.ArgumentParser()
ap.add_argument('out'); ap.add_argument('--seconds', type=float, required=True)
ap.add_argument('--cuts', default=''); ap.add_argument('--seed', type=int, default=1)
a = ap.parse_args()
rng = np.random.default_rng(a.seed)
N = int(a.seconds * SR); t = np.arange(N) / SR
cuts = [float(x) for x in a.cuts.split(',') if x.strip()]

# key, tempo and progression (scale degrees as semitone offsets of 4-note voicings) chosen by seed
roots = [53, 55, 57, 50, 52, 48]                     # F, G, A, D, E, C (MIDI, low octave)
progs = [[[0, 4, 7, 11], [-3, 0, 4, 7], [-7, -3, 0, 4], [-5, -1, 2, 5]],      # I maj7 - vi7 - IV - V
         [[0, 4, 7, 14], [5, 9, 12, 16], [-3, 0, 4, 7], [-5, -1, 2, 7]],      # I add9 - IV - vi - V
         [[-3, 0, 4, 7], [-7, -3, 0, 4], [0, 4, 7, 11], [-5, -1, 2, 5]]]      # vi - IV - I - V
root = roots[a.seed % len(roots)]; prog = progs[a.seed % len(progs)]
bpm = [88, 92, 96, 84][a.seed % 4]; beat = 60 / bpm; bar = beat * 4
hz = lambda m: 440 * 2 ** ((m - 69) / 12)

def lp(x, f, order=2): return sosfilt(butter(order, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, order=2): return sosfilt(butter(order, f, 'high', fs=SR, output='sos'), x)
def env_adsr(n, a_, r_):
    e = np.ones(n); ai = min(int(a_ * SR), n // 2); ri = min(int(r_ * SR), n - ai)
    if ai: e[:ai] = np.linspace(0, 1, ai)
    if ri: e[-ri:] *= np.linspace(1, 0, ri)
    return e

L = np.zeros(N); R = np.zeros(N)
# 1. pad: two bars per chord, detuned sines with a little 2nd/3rd harmonic, slow attack and release, crossfaded
chord_len = bar * 2
for ci, start in enumerate(np.arange(0, a.seconds, chord_len)):
    ch = prog[ci % len(prog)]; s0 = int(start * SR); n = min(N - s0, int((chord_len + 1.2) * SR))
    if n <= 0: break
    tt = np.arange(n) / SR; e = env_adsr(n, 1.0, 1.4)
    for k, iv in enumerate(ch):
        f = hz(root + 12 + iv)
        for det, pan in ((-0.12, 0.3), (0.12, 0.7)):
            ph = 2 * np.pi * (f + det) * tt + rng.uniform(0, 6.28)
            v = (np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)) * e * 0.05
            L[s0:s0 + n] += v * (1 - pan); R[s0:s0 + n] += v * pan
    bass = np.sin(2 * np.pi * hz(root + ch[0] - 12) * tt) * e * 0.07
    L[s0:s0 + n] += bass; R[s0:s0 + n] += bass

# 2. plucked arpeggio on eighth notes (soft, panned left/right), starts after the first bar
pattern = [0, 2, 1, 3, 2, 1, 3, 1]
for j, st in enumerate(np.arange(bar * 0.5, a.seconds - 1.0, beat / 2)):
    ch = prog[int(st // chord_len) % len(prog)]; m = root + 24 + ch[pattern[j % 8]]
    s0 = int(st * SR); n = min(N - s0, int(0.9 * SR)); tt = np.arange(n) / SR
    v = (np.sin(2 * np.pi * hz(m) * tt) + 0.25 * np.sin(4 * np.pi * hz(m) * tt)) * np.exp(-tt * 6) * 0.035 * (0.85 + 0.3 * rng.random())
    v *= np.minimum(1, tt / 0.004)
    pan = 0.35 if j % 2 else 0.65
    L[s0:s0 + n] += v * (1 - pan); R[s0:s0 + n] += v * pan

# 3. a low, soft pulse on beats 1 and 3 from bar 2 (felt more than heard)
for st in np.arange(bar, a.seconds - 1.5, beat * 2):
    s0 = int(st * SR); n = min(N - s0, int(0.35 * SR)); tt = np.arange(n) / SR
    f = 55 * np.exp(-tt * 9) + 42
    v = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 10) * 0.12
    L[s0:s0 + n] += v; R[s0:s0 + n] += v

# 4. an airy swell into each scene change (filtered noise rising for 0.45 s, gone by the cut)
for c in cuts:
    n = int(0.6 * SR); s0 = int((c - 0.45) * SR)
    if s0 < 0 or s0 + n > N: continue
    noise = hp(lp(rng.standard_normal(n), 5000), 600)
    e = np.concatenate([np.linspace(0, 1, int(0.45 * SR)) ** 2, np.linspace(1, 0, n - int(0.45 * SR)) ** 0.5]) * 0.03
    L[s0:s0 + n] += noise * e; R[s0:s0 + n] += noise[::-1] * e

# room: a short synthetic reverb (exponentially decaying noise), then gentle tone shaping
ir = rng.standard_normal(int(1.6 * SR)) * np.exp(-np.arange(int(1.6 * SR)) / SR * 3.2); ir = lp(ir, 4000) * 0.05
L = L + fftconvolve(L, ir)[:N] * 0.5; R = R + fftconvolve(R, ir[::-1])[:N] * 0.5
L, R = lp(hp(L, 35), 9000), lp(hp(R, 35), 9000)
fade = np.ones(N); fi, fo = int(0.6 * SR), int(1.8 * SR); fade[:fi] = np.linspace(0, 1, fi); fade[-fo:] *= np.linspace(1, 0, fo) ** 1.5
st = np.stack([L * fade, R * fade], 1); st /= max(1e-9, np.abs(st).max()) / 0.8
with wave.open(a.out, 'wb') as w:
    w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((st * 32767).astype('<i2').tobytes())
print(a.out, f'{a.seconds:.1f}s', f'root {root} bpm {bpm}')
