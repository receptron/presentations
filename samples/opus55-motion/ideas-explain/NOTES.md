# Idea gallery — explainers (silent)

Build: `python3 build.py` → `ideas-explain.json`. Render from the repo: `npx mulmo movie -g -o <this dir>/out <abs path>/ideas-explain.json`.
All beats are silent (`text: ""`, fixed `duration`), everything is drawn in `render(frame)`.

## math-derivative (12 s) — planned narration (English, timed to the animation)

| time | narration |
|---|---|
| 0.0–3.0 | Here is a curve: f of x equals x cubed over three, minus x. |
| 3.0–7.6 | Pick two points and join them. As the gap h shrinks, the secant turns into the tangent. |
| 7.6–10.0 | Expand the slope, and every term that still has an h in it disappears. |
| 10.0–12.0 | What is left is the derivative: x squared minus one. |

Once narration exists, measure each sentence's start and move the cue times in `math_js` (secant 3.1, h shrink 4.2–7.6, formulas 7.7/8.5/9.6, box 10.1).

## ocean-dive (10 s)
Log depth scale (`ln(depth+40)`), so every zone gets screen time. Zone lines at 200 / 1,000 / 4,000 m, marine snow fixed in depth, jellyfish / anglerfish / siphonophore chains drawn with canvas `shadowBlur`.

## art-history-speedrun (14 s)
The same 2,400 particles re-arrange: hand stencils (sprayed ochre mist on a rock texture) → Byzantine mosaic → pointillism (dense under-layer + moving dots) → Mondrian (bars grow in) → pop-art Ben-Day dots sampled from an off-screen "WOW!" burst → flow field (each particle's path is re-integrated from the era start every frame, so it is deterministic).
