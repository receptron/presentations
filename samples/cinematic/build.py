#!/usr/bin/env python3
"""Build cinematic.json — cinematic establishing shots and hero beats, drawn in code (three.js r147).

Silent beats (no narration, fixed durations), so a render costs nothing but time. Each beat is a scene file pair
scenes/<id>.html + scenes/<id>.js wrapped with the kit (kit/common.js, kit/three-kit.js). Every beat reads its
text, colours and other knobs from `P` (set per beat in SHOTS below) — change them there to reuse a shot.
Run from anywhere: python3 build.py. Contract for writing a scene: scenes/BRIEF.md.
"""
import json
import math
import os

HERE = os.path.dirname(os.path.abspath(__file__))
FPS = 30

# (id, seconds, P) — P is handed to the scene as `const P = {...}`
SHOTS = [
    ("sunrise_peaks", 9.0, {"eyebrow": "CHAPTER ONE", "title": "First Light"}),
    ("golden_ocean", 8.0, {"line": "Where the day begins"}),
    ("metal_title", 6.0, {"lines": ["NORTHERN", "LIGHTS"], "sub": "A FILM BY YOUR NAME", "metal": "gold"}),
    ("product_hero", 7.0, {"name": "Aurora One", "tagline": "Light, reshaped."}),
    ("ui_screen", 7.0, {"app": "Dashboard", "headline": "Everything, at a glance."}),
    ("particle_logo", 7.0, {"word": "Create", "logo": "star"}),
    ("split_flap", 6.0, {"rows": [["NOW BOARDING", "GATE 12"], ["NEXT STOP", "TOKYO"]]}),
    ("footage_notes", 8.0, {"note": "Meet Claude", "footage": "../../mulmoterminal/clips/first-run-assets/07-grid.mp4",
                            "focus": [678, 100], "radius": 46, "zoom": 1.6}),  # focus: footage pixels (Claude Code's mascot)
]
TOTAL_FRAMES = sum(math.floor(d * FPS) for _, d, _ in SHOTS)

FONTS = '<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@400;600;800;900&family=JetBrains+Mono:wght@400;600&family=Instrument+Serif:ital@0;1&display=block" rel="stylesheet">'
CSS = """<style>
html,body{background:#000;margin:0;}
.stage{position:relative;width:1280px;height:720px;overflow:hidden;background:#05070b;color:#f4f1ea;font-family:'Inter Tight',sans-serif;}
.abs{position:absolute;} .full{position:absolute;left:0;top:0;width:1280px;height:720px;}
.mono{font-family:'JetBrains Mono',monospace;} .serif{font-family:'Instrument Serif',serif;}
</style><div class='abs' style='font-family:Inter Tight;font-weight:800;opacity:0'>A<span style='font-family:Instrument Serif;font-style:italic'>A</span><span class='mono'>A</span></div>"""
THREE_CDN = "".join(
    f"<script src='https://cdn.jsdelivr.net/npm/three@0.147.0/{p}.js'></script>"
    for p in ["build/three.min", "examples/js/shaders/CopyShader", "examples/js/shaders/LuminosityHighPassShader",
              "examples/js/postprocessing/EffectComposer", "examples/js/postprocessing/RenderPass",
              "examples/js/postprocessing/ShaderPass", "examples/js/postprocessing/UnrealBloomPass"]
)
KIT = open(os.path.join(HERE, "kit", "common.js")).read() + "\n" + open(os.path.join(HERE, "kit", "three-kit.js")).read()


def scene(bid, dur, params):
    html = open(os.path.join(HERE, "scenes", bid + ".html")).read()
    js = open(os.path.join(HERE, "scenes", bid + ".js")).read()
    # first line `// requires: objects/Water, objects/Sky` loads extra three.js r147 examples/js modules for this beat only
    first = js.split("\n", 1)[0]
    extra = [m.strip() for m in first.split("requires:", 1)[1].split(",")] if first.startswith("// requires:") else []
    cdn = "".join(f"<script src='https://cdn.jsdelivr.net/npm/three@0.147.0/examples/js/{m}.js'></script>" for m in extra if m)
    return {
        "id": bid,
        "text": "",
        "duration": dur,
        "image": {
            "type": "html_tailwind",
            "animation": {"fps": FPS},
            "html": FONTS + CSS + THREE_CDN + cdn + "<div class='stage'>" + html + "<div id='bf' class='full' style='background:#000;opacity:0'></div></div>",
            "script": KIT + f"\nconst D = {dur}; const P = {json.dumps(params, ensure_ascii=False)}; const TOTAL_FRAMES = {TOTAL_FRAMES};\n" + js,
        },
    }


ONLY = [x for x in os.environ.get("ONLY", "").split(",") if x]
beats = [scene(*s) for s in SHOTS if (not ONLY or s[0] in ONLY) and os.path.exists(os.path.join(HERE, "scenes", s[0] + ".js"))]
deck = {
    "$mulmocast": {"version": "1.1"},
    "title": "Cinematic shots drawn in code",
    "description": "Silent sample beats: a mountain sunrise, a golden-hour ocean, a metal title, a product hero shot, a floating UI screen, particles into a logo, a split-flap board and annotated footage — all three.js, all parameterised.",
    "lang": "en",
    "canvasSize": {"width": 1280, "height": 720},
    "speechParams": {"speakers": {"Presenter": {"voiceId": "Kore", "isDefault": True, "provider": "gemini"}}},
    "beats": beats,
}
with open(os.path.join(HERE, "cinematic.json"), "w") as f:
    json.dump(deck, f, ensure_ascii=False, indent=1)
    f.write("\n")
print("ok", len(beats), "beats")
