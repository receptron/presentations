# Scene brief — cinematic shots drawn in code

These are **sample shots for anyone making a video with mulmocast** — an opening, a chapter card, a product reveal,
an app showcase. They must be good enough that someone watching the reel wants to drop one into their own video,
and generic: no event, brand or story of ours. Every piece of text, colour and wording a user would change comes
from `P` (see below).

Each beat of `../cinematic.json` is one html page that mulmocast renders frame by frame (`html_tailwind` with
`animation`). A scene is two files here:

- `scenes/<id>.html` — the markup inside the 1280×720 stage
- `scenes/<id>.js` — the script; it must define `async function render(frame, totalFrames, fps)`

`../build.py` wraps them (read `scene()`): it prepends the fonts, the CSS, the three.js r147 CDN scripts (three.min,
EffectComposer, RenderPass, ShaderPass, UnrealBloomPass, CopyShader, LuminosityHighPassShader), the kit
(`../kit/common.js`, `../kit/three-kit.js` — read both, use them), and these constants:

- `D` — the beat's length in seconds
- `P` — the beat's parameters, from `SHOTS` in build.py (text, colours…). Read every user-facing string from `P`.
- `TOTAL_FRAMES` — frames in the whole reel

and appends a black `#bf` layer that `beatFade(t, D, fadeIn, fadeOut)` drives. Put
`// requires: objects/Water, objects/Sky` (comma separated, paths under `three@0.147.0/examples/js/`, no `.js`) on the
**first line** of the .js to load extra modules for that beat only. Available and checked: objects/Water, objects/Sky,
objects/Reflector, environments/RoomEnvironment, math/SimplexNoise, geometries/RoundedBoxGeometry,
geometries/TextGeometry, loaders/FontLoader, postprocessing/BokehPass + shaders/BokehShader, postprocessing/FilmPass +
shaders/FilmShader, shaders/FXAAShader, shaders/VignetteShader, postprocessing/AfterimagePass + shaders/AfterimageShader.
Other libraries may be loaded from cdn.jsdelivr.net with a `<script src>` in the .html (e.g. opentype.js to turn a
font into outlines for real 3D text of any string).

## Assets

Local files live in `../assets/` (`waternormals.jpg`: three.js water normals, MIT). mulmocast rewrites **only
`src="..."` attributes in the html** to absolute `file://` paths (relative to the script folder); a relative path
inside JavaScript does not resolve. Put the file in the .html as a hidden
`<img id='tex_x' src='assets/…' style='display:none' alt=''>` (or `<video>` for footage) and load it in JS from that
element: `await new THREE.TextureLoader().loadAsync(el('tex_x').src)`, inside setup, before the first frame.

## Rules the renderer imposes (each measured while building the remake this kit comes from)

1. Everything is a pure function of `t = frame / fps`. No `Date.now()`, no `Math.random()` (use `rnd(n)`), no
   requestAnimationFrame, no physics that integrates over frames.
2. `render()` may be async; mulmocast awaits it, then screenshots. Build heavy things once (`if (!S) S = setup()`).
3. Use `makeRenderer()` from the kit. It gives an opaque canvas (`alpha: false` — with alpha, half-transparent pixels
   let the layer underneath show through), `preserveDrawingBuffer`, and a composer whose targets have **4x MSAA**
   (the renderer's own `antialias` does not reach the composer; without MSAA thin lines stair-step).
4. **One display transform, and only where the light is linear.** Scenes lit with plain hex colours (the
   renderer's default, `NoToneMapping`) already come out as display values: a finishing pass with `pow(c, 1/2.2)` on
   them applies gamma twice and lifts every black to grey — every scene of the first remake round looked like pale
   clay because of exactly this. Scenes built on physically based light (objects/Sky, objects/Water) output linear
   light and need exactly one transform at the end: exposure → ACES → sRGB, as in `golden_ocean`. Judge by the
   rendered frame, not by the rule of thumb. Avoid objects/Sky's high turbidity for golden light: its solar halo
   spreads over half the frame; a bounded sky gradient (as in `golden_ocean`) keeps the colour.
5. **Reflections.** The kit swaps `THREE.RoomEnvironment` for a dark studio (warm softbox, cool strip, hot key) and,
   on the first render, keeps env reflections on bright metals only. RoomEnvironment itself is a light grey room:
   gold reflected grey (olive bronze) and dark props read as grey clay.
6. Text in a canvas texture shown in 3D: keep it below the bloom threshold or bloom smears it. HTML overlays on top of
   the WebGL canvas give the sharpest type.
7. Projecting HTML onto a 3D plane with CSS `matrix3d`: an all-zero z row makes the matrix non-invertible and the
   browser silently draws nothing. Put a 1 on the z diagonal.
8. `ShapeGeometry` frames with a hole: the hole's chamfer must be the outer chamfer inset along the 45° edge
   (`ringOf` in the kit); a bigger one pokes through the outline and the hole fills in.
9. `<video>`: mulmocast re-seeks every `<video>` to the beat's own time after `render()`. Keep it hidden, seek it
   yourself and draw it into a canvas (`paint()` in the kit).
10. Budget: a frame should render in ~1.5 s with software GL (SwiftShader): ~1–2 M triangles, particles in the tens
    of thousands, no huge shadow maps.
11. Fonts loaded: 'Inter Tight' (400/600/800/900), 'JetBrains Mono' (400/600), 'Instrument Serif' (italic).
    `await waitFonts()` before measuring or drawing text in a canvas.
12. End render with `beatFade(t, D, 0.3, 0.3)`.

## Look

Photographic and cinematic, each shot lit for what it is (a sunrise, golden hour, a studio, a dark room with a
screen). What made the first attempts weak, so avoid it: pale grey haze over everything, flat matte materials, small
subjects floating in empty space, flat colour gradients standing in for sky or land, and static cameras. What makes a
shot read as crafted: a light source with direction and colour, contrast (real shadows), atmospheric perspective,
materials that respond to light (metal, glass, water, rock), a camera that moves with intent (dolly, crane, orbit,
slow push), depth of field or haze separating planes, and composition with the subject filling the frame. Typography
is large, clean and legible, and sits in the shot rather than on top of it.

## Check your frames

Chrome cannot start inside a Codex sandbox, so you may not be able to render. If you can't, check what you can
(`python3 ../build.py`, `node --check scenes/<id>.js`) and reason carefully about framing and exposure; the lead
renders your shots and sends the frames back for a revision round.

## Shots

| id | what it is for | what it must look like |
|---|---|---|
| sunrise_peaks | an opening or chapter card: "the start of something" | A mountain range at sunrise seen from above a sea of clouds. Several layers of ridges (real terrain: fBm noise with enough resolution, ridged peaks, rock and snow by slope and height), a cloud sea filling the valleys between them, the sun breaking the horizon with warm light raking across the peaks, atmospheric perspective turning far ridges blue, light shafts through gaps, a slow crane/dolly move. `P.eyebrow` and `P.title` appear as a chapter card. This replaces a weak earlier attempt (flat brown hills, no clouds, no light) — the bar is a photograph. |
| golden_ocean | an ending, travel, a brand mood | Open ocean at golden hour: objects/Water with the normals, objects/Sky with a low sun, a strong glitter path, a few layers of soft clouds lit from below, a low camera gliding over the swell. `P.line` as an elegant caption. |
| metal_title | a title card for any text | `P.lines` as real extruded 3D letters (any string: outline a real font, e.g. Inter Tight via opentype.js, not hard-coded glyphs) in polished metal (`P.metal`: gold / silver / copper), bevelled, lit by the studio env and a moving light that sweeps a highlight across them; subtle dust, dark backdrop, a slow push; `P.sub` small underneath. |
| product_hero | a product reveal | A sleek generic device (rounded slab with a glass front and metal edge, or similar — not a real brand) on a turntable pedestal under studio softboxes, rotating to reveal its edge, with reflections on a glossy floor; `P.name` and `P.tagline` appear. |
| ui_screen | an app or website showcase | A large floating glass screen in a dim space showing a rich, real-looking HTML interface (cards, a chart, a list — styled, with `P.app` and `P.headline`), projected onto the 3D plane with matrix3d (rule 7), with the camera orbiting and the UI animating (numbers counting, a chart drawing). |
| particle_logo | an intro or transition | Tens of thousands of glowing particles drift as a nebula, gather into `P.word` in 3D, then flow into a logo shape (`P.logo`: "star" or an SVG path string), with bloom and depth. |
| split_flap | an announcement, a number, a destination | A real 3D split-flap board: hinged flaps that flip (top half falls over the bottom), metal casing, spot light, showing `P.rows` (label, value pairs) settling one after another. |
| footage_notes | annotating a screen recording or footage | The footage in `P.footage` (via hidden `<video>` + `paint()`) plays, slows and freezes; a loupe magnifies a region, a hand-drawn red circle draws around it and `P.note` appears; at the end the picture switches off like an old CRT. |
