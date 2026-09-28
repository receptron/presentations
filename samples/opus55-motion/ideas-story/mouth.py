"""Per-frame mouth opening (0..1 at 30 fps) for each cafe-* beat, measured from its TTS file."""
import json, math, struct, subprocess, sys
studio, out = sys.argv[1], sys.argv[2]
d = json.load(open(studio)); res = {}
for sb, b in zip(d["beats"], d["script"]["beats"]):
    if not str(b.get("id", "")).startswith("cafe-") or not sb.get("audioFile"): continue
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", sb["audioFile"], "-ac", "1", "-ar", "12000", "-af", "bandpass=f=1000:width_type=h:w=2400", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    x = struct.unpack("<%dh" % (len(raw) // 2), raw); hop = 400
    e = [math.sqrt(sum(v * v for v in x[i:i + hop]) / hop) for i in range(0, len(x) - hop + 1, hop)]
    pk = sorted(e)[int(len(e) * 0.95)] or 1
    sm, prev = [], 0
    for v in e:
        v = min(1, v / pk); v = 0 if v < 0.12 else v          # gate silence
        prev = prev + (v - prev) * (0.7 if v > prev else 0.35)  # fast open, slower close
        sm.append(round(prev, 3))
    res[b["id"]] = sm
json.dump(res, open(out, "w")); print({k: len(v) for k, v in res.items()})
