"""Kick times + per-frame loudness from an audio file (no numpy): ffmpeg -> s16le -> energy envelope."""
import json, struct, subprocess, sys, math
src, out = sys.argv[1], sys.argv[2]
SR, HOP, FPS = 11025, 110, 30          # ~10 ms hop
def pcm(af):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-ac", "1", "-ar", str(SR), "-af", af, "-f", "s16le", "-"], capture_output=True, check=True).stdout
    return struct.unpack("<%dh" % (len(raw) // 2), raw)
def env(x, hop):
    return [math.sqrt(sum(v * v for v in x[i:i + hop]) / hop) / 32768 for i in range(0, len(x) - hop, hop)]
low = env(pcm("lowpass=f=120,lowpass=f=120"), HOP)
full = env(pcm("anull"), SR // FPS)
diff = [max(0, low[i] - low[i - 1]) for i in range(1, len(low))]
thr = sorted(diff)[int(len(diff) * 0.97)]
kicks, last = [], -1
for i in range(1, len(diff) - 1):
    t = (i + 1) * HOP / SR
    if diff[i] >= thr and diff[i] >= diff[i - 1] and diff[i] >= diff[i + 1] and t - last > 0.3:
        kicks.append(round(t, 3)); last = t
iv = sorted(b - a for a, b in zip(kicks, kicks[1:]))
med = iv[len(iv) // 2] if iv else None
peak = max(full) or 1
json.dump({"kicks": kicks, "median_interval": med, "bpm_est": round(60 / med, 1) if med else None,
           "loud": [round(v / peak, 3) for v in full]}, open(out, "w"))
print(len(kicks), "kicks; median interval", med, "-> bpm", round(60 / med, 1) if med else None, "; first", kicks[:6], "; last", kicks[-3:])
