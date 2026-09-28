"""Build two sampler decks (16:9 and 9:16) that turn the Opus 5.5 X patterns into MulmoScript beats.

Each beat is silent (text "") with a fixed duration, so `mulmo movie` renders the animation
without any TTS cost. Swap in narration later and the timings keep working (seconds-based).
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent

BG = (
    "background:radial-gradient(1200px 700px at 12% -10%,rgba(253,224,71,.30),transparent 60%),"
    "radial-gradient(1000px 600px at 100% 0%,rgba(251,146,60,.22),transparent 55%),"
    "linear-gradient(160deg,#FFFBF2,#FFF3DC 55%,#FCE8C8);color:#431407"
)
FONT = "<style>.t{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif}.g{font-family:Georgia,serif}.m{font-family:Menlo,monospace}</style>"


def frame(w, h, inner, extra_style=""):
    return f"{FONT}<div class='t relative overflow-hidden' style='width:{w}px;height:{h}px;{BG};{extra_style}'>{inner}</div>"


def beat(html, script, duration, label):
    return {
        "id": label,
        "text": "",
        "duration": duration,
        "image": {"type": "html_tailwind", "html": html, "script": script, "animation": {"fps": 30}},
    }


# ---------------------------------------------------------------- 16:9 beats
W, H = 1280, 720

# 1. Kinetic typography sting (intro / outro)
sting = beat(
    frame(W, H, """
<div class='absolute inset-0 flex flex-col items-center justify-center gap-2'>
  <div class='flex gap-6 g text-7xl font-bold'>
    <span id='w0' style='opacity:0'>Record.</span><span id='w1' style='opacity:0'>Organize.</span><span id='w2' style='opacity:0;color:#EA580C'>Present.</span>
  </div>
  <div id='logo' class='text-5xl font-extrabold tracking-tight mt-10' style='opacity:0'>MulmoClaude</div>
  <div class='h-2 mt-2 rounded-full' style='background:#EA580C;width:420px;transform-origin:left'><div id='bar' style='width:0;height:100%;background:#F59E0B'></div></div>
</div>"""),
    """var animation = new MulmoAnimation();
animation
  .stagger('#w{i}', 3, { opacity: [0, 1], scale: [1.8, 1], translateY: [-30, 0] }, { start: 0.3, stagger: 0.45, duration: 0.35, easing: 'easeOut' })
  .animate('#w0', { opacity: [1, 0.35] }, { start: 2.2, end: 2.6 })
  .animate('#w1', { opacity: [1, 0.35] }, { start: 2.2, end: 2.6 })
  .animate('#logo', { opacity: [0, 1], translateY: [24, 0] }, { start: 2.4, end: 3.0, easing: 'easeOut' })
  .animate('#bar', { width: [0, 100, '%'] }, { start: 2.8, end: 3.8, easing: 'easeInOut' });""",
    5,
    "p1-kinetic-sting",
)

# 2. UI parts lifted out of a recreated screen (feature intro)
chips = "".join(
    f"<span id='c{i}' class='px-3 py-1 rounded-full text-sm font-semibold' style='background:{bg};color:{fg}'>{t}</span>"
    for i, (t, bg, fg) in enumerate([("main", "#FCE8C8", "#431407"), ("ctx 62%", "#FCE8C8", "#431407"), ("+12 −3", "#FCE8C8", "#431407"), ("PR #125", "#EA580C", "#fff")])
)
lift = beat(
    frame(W, H, f"""
<div id='dim' class='absolute inset-0' style='background:#431407;opacity:0'></div>
<div id='screen' class='absolute rounded-2xl shadow-2xl' style='left:140px;top:90px;width:1000px;height:560px;background:#1f1a17'>
  <div id='header' class='flex items-center gap-3 px-5 py-3 rounded-t-2xl' style='background:#FFF3DC'>
    <span class='w-3 h-3 rounded-full' style='background:#EA580C'></span><span class='font-bold'>mulmo-presentations</span>
    <div class='flex gap-2 ml-auto'>{chips}</div>
  </div>
  <div id='term' class='m text-sm leading-6 px-5 py-4' style='color:#FCE8C8'>
    <div>&gt; claude</div><div style='color:#F59E0B'>● Reading mulmoclaude/PROGRESS.md</div><div>● Editing demos/record-buttons-demo.json</div><div style='opacity:.6'>…</div>
  </div>
  <div id='tdim' class='absolute left-0 right-0 bottom-0 rounded-b-2xl' style='top:52px;background:#000;opacity:0'></div>
</div>
<div id='callout' class='absolute text-center g text-4xl font-bold' style='left:0;right:0;top:620px;opacity:0;color:#fff'>The header tells you where the work stands</div>"""),
    """var animation = new MulmoAnimation();
animation
  .animate('#screen', { opacity: [0, 1], translateY: [40, 0] }, { start: 0, end: 0.8, easing: 'easeOut' })
  .animate('#dim', { opacity: [0, 0.45] }, { start: 1.6, end: 2.2 })
  .animate('#tdim', { opacity: [0, 0.6] }, { start: 1.6, end: 2.2 })
  .animate('#c0', { translateX: [0, -420], translateY: [0, 200], scale: [1, 2] }, { start: 1.8, end: 2.4, easing: 'easeOut' })
  .animate('#c1', { translateX: [0, -250], translateY: [0, 200], scale: [1, 2] }, { start: 1.98, end: 2.58, easing: 'easeOut' })
  .animate('#c2', { translateX: [0, -60], translateY: [0, 200], scale: [1, 2] }, { start: 2.16, end: 2.76, easing: 'easeOut' })
  .animate('#c3', { translateX: [0, 120], translateY: [0, 200], scale: [1, 2] }, { start: 2.34, end: 2.94, easing: 'easeOut' })
  .animate('#callout', { opacity: [0, 1], translateY: [20, 0] }, { start: 3.0, end: 3.6, easing: 'easeOut' });
// chips sit above the terminal dim (same stacking context: #screen)
document.querySelectorAll('#header [id^=c]').forEach(function (el) { el.style.position = 'relative'; el.style.zIndex = 20; });""",
    6,
    "p2-ui-lift",
)

# 3. Zoom dive: grid -> one cell -> one chip (explain where something lives)
cells = "".join(
    f"<div class='rounded-xl overflow-hidden' style='background:#1f1a17'><div class='px-3 py-1 text-xs font-bold flex gap-2' style='background:{'#EA580C' if i == 4 else '#FFF3DC'};color:{'#fff' if i == 4 else '#431407'}'>project-{i}"
    + ("<span id='target' class='ml-auto px-2 rounded-full' style='background:#fff;color:#EA580C'>PR #125</span>" if i == 4 else "")
    + "</div><div class='m text-[9px] p-2' style='color:#FCE8C8'>● working…</div></div>"
    for i in range(6)
)
zoom = beat(
    frame(W, H, f"""
<div id='world' class='absolute grid grid-cols-3 gap-4' style='left:140px;top:110px;width:1000px;height:500px;transform-origin:0 0'>{cells}</div>
<div id='cap0' class='absolute left-0 right-0 top-6 text-center g text-3xl font-bold'>Six sessions at once</div>
<div id='cap1' class='absolute left-0 right-0 bottom-8 text-center' style='opacity:0'><span class='g text-3xl font-bold px-6 py-2 rounded-full' style='background:#FFF3DC'>…each one says which PR it is on</span></div>"""),
    """var animation = new MulmoAnimation();
animation
  .animate('#cap0', { opacity: [1, 0] }, { start: 1.0, end: 1.4 })
  .animate('#cap1', { opacity: [0, 1] }, { start: 4.6, end: 5.2 });
// Camera keyframes: [time, focusX, focusY, zoom] in page px. Two animate() calls on one element
// fight (the later entry wins every frame), so the camera is interpolated here instead.
var world = document.getElementById('world');
var KEYS = [[0, 640, 360, 1], [1.2, 640, 360, 1], [3.0, 640, 452, 2.4], [3.4, 640, 452, 2.4], [4.8, 0, 0, 5.5]];
function focusOf(sel) {                       // centre of an element in un-zoomed page coordinates
  world.style.transform = 'none';
  var r = document.querySelector(sel).getBoundingClientRect();
  return [r.left + r.width / 2, r.top + r.height / 2];
}
var chip = focusOf('#target');
KEYS[4][1] = chip[0]; KEYS[4][2] = chip[1];
var cell = document.querySelector('#target').parentElement.parentElement.getBoundingClientRect();
KEYS[2][1] = KEYS[3][1] = cell.left + cell.width / 2; KEYS[2][2] = KEYS[3][2] = cell.top + cell.height / 2;
function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
function render(frame, totalFrames, fps) {
  animation.update(frame, fps);
  var t = frame / fps, k = 0;
  while (k < KEYS.length - 2 && t > KEYS[k + 1][0]) k++;
  var a = KEYS[k], b = KEYS[k + 1];
  var p = ease(Math.max(0, Math.min(1, (t - a[0]) / (b[0] - a[0]))));
  var fx = a[1] + (b[1] - a[1]) * p, fy = a[2] + (b[2] - a[2]) * p, z = a[3] + (b[3] - a[3]) * p;
  var ox = world.offsetLeft, oy = world.offsetTop;   // transform-origin 0 0 is the world's own corner
  world.style.transform = 'translate(' + (640 - (fx - ox) * z - ox) + 'px,' + (360 - (fy - oy) * z - oy) + 'px) scale(' + z + ')';
}""",
    6.5,
    "p3-zoom-dive",
)

# 4. Line-draw reveal of a flow diagram (explain a mechanism)
nodes = [("Chat", 170), ("Collection", 520), ("View", 870)]
svg_nodes = "".join(
    f"<g id='n{i}' opacity='0'><rect x='{x}' y='300' width='240' height='120' rx='22' fill='#FFF3DC' stroke='#EA580C' stroke-width='4'/>"
    f"<text x='{x + 120}' y='372' text-anchor='middle' font-family='Georgia' font-size='34' font-weight='bold' fill='#431407'>{t}</text></g>"
    for i, (t, x) in enumerate(nodes)
)
draw = beat(
    frame(W, H, f"""
<svg class='absolute inset-0' width='{W}' height='{H}'>
  <path id='p0' d='M410 360 L520 360' stroke='#431407' stroke-width='5' fill='none' stroke-dasharray='110' stroke-dashoffset='110'/>
  <path id='p1' d='M760 360 L870 360' stroke='#431407' stroke-width='5' fill='none' stroke-dasharray='110' stroke-dashoffset='110'/>
  <path id='p2' d='M990 420 C990 560 290 560 290 420' stroke='#F59E0B' stroke-width='5' fill='none' stroke-dasharray='1100' stroke-dashoffset='1100'/>
  {svg_nodes}
  <text id='loop' x='640' y='600' text-anchor='middle' font-family='Georgia' font-size='28' fill='#EA580C' opacity='0'>what you see becomes the next thing you ask</text>
</svg>
<div class='absolute left-0 right-0 top-12 text-center g text-4xl font-bold'>How a record travels</div>"""),
    """var animation = new MulmoAnimation();
animation
  .stagger('#n{i}', 3, { opacity: [0, 1], translateY: [20, 0] }, { start: 0.4, stagger: 1.0, duration: 0.5, easing: 'easeOut' })
  .animate('#p0', { 'stroke-dashoffset': [110, 0] }, { start: 0.9, end: 1.4 })
  .animate('#p1', { 'stroke-dashoffset': [110, 0] }, { start: 1.9, end: 2.4 })
  .animate('#p2', { 'stroke-dashoffset': [1100, 0] }, { start: 3.0, end: 4.4, easing: 'easeInOut' })
  .animate('#loop', { opacity: [0, 1] }, { start: 4.2, end: 4.8 });""",
    6,
    "p4-line-draw",
)

# 5. Accumulating data story (vision / retrospective): a year of days fills in
days = "".join(f"<div class='d' style='width:14px;height:14px;border-radius:3px;background:#FCE8C8'></div>" for _ in range(364))
accum = beat(
    frame(W, H, f"""
<div class='absolute left-0 right-0 top-10 text-center g text-4xl font-bold'>One year of small records</div>
<div id='cal' class='absolute grid' style='left:130px;top:170px;grid-template-rows:repeat(7,14px);grid-auto-flow:column;gap:4px'>{days}</div>
<div class='absolute text-center' style='left:0;right:0;top:360px'>
  <div id='num' class='text-8xl font-extrabold' style='color:#EA580C'>0</div>
  <div class='text-2xl mt-1'>entries kept for you</div>
</div>
<div id='month' class='absolute m text-xl' style='left:130px;top:140px'>Jan</div>"""),
    """var animation = new MulmoAnimation();
animation.counter('#num', [0, 1284], { start: 0.3, end: 5.0, easing: 'easeOut' });
var cells = document.querySelectorAll('#cal .d');
var months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
function shade(i) { var r = Math.sin(i * 12.9898) * 43758.5453; r = r - Math.floor(r); return r; }
function render(frame, totalFrames, fps) {
  animation.update(frame, fps);
  var t = Math.min(1, Math.max(0, (frame / fps - 0.3) / 4.7));
  var p = 1 - (1 - t) * (1 - t);
  var shown = Math.floor(p * cells.length);
  for (var i = 0; i < cells.length; i++) {
    var s = shade(i);
    cells[i].style.background = i < shown ? (s > 0.8 ? '#EA580C' : s > 0.45 ? '#F59E0B' : '#FCD34D') : '#FCE8C8';
  }
  document.getElementById('month').textContent = months[Math.min(11, Math.floor(shown / 30.4))];
}""",
    6,
    "p5-accumulate",
)

# 6. Split before/after with a sweeping divider (comparison)
split = beat(
    frame(W, H, """
<div class='absolute inset-0 flex'>
  <div class='w-1/2 h-full flex flex-col justify-center px-16 gap-4' style='background:#EDE7DD;color:#6b5a4e'>
    <div class='text-xl font-bold tracking-widest'>BEFORE</div>
    <div class='g text-4xl'>Copy the notes.<br>Paste into a sheet.<br>Make the chart.</div>
  </div>
  <div class='w-1/2 h-full flex flex-col justify-center px-16 gap-4'>
    <div class='text-xl font-bold tracking-widest' style='color:#EA580C'>AFTER</div>
    <div class='g text-4xl font-bold'>“Show me this month.”</div>
  </div>
</div>
<div id='cover' class='absolute top-0 right-0 h-full' style='width:640px;background:#EDE7DD'></div>
<div id='divider' class='absolute top-0 h-full' style='left:1274px;width:12px;background:#EA580C'></div>"""),
    """var animation = new MulmoAnimation();
animation
  .animate('#divider', { translateX: [0, -640] }, { start: 1.6, end: 2.6, easing: 'easeInOut' })
  .animate('#cover', { width: [640, 0, 'px'] }, { start: 1.6, end: 2.6, easing: 'easeInOut' });""",
    5,
    "p6-split-compare",
)

# 7. Hand-drawn paper strokes on canvas (warm style layer, deterministic)
brush = beat(
    frame(W, H, """
<canvas id='cv' width='1280' height='720' class='absolute inset-0'></canvas>
<div id='t' class='absolute left-0 right-0 text-center g text-6xl font-bold' style='top:300px;opacity:0'>Kept by hand, drawn by code</div>"""),
    """var animation = new MulmoAnimation();
animation.animate('#t', { opacity: [0, 1] }, { start: 2.6, end: 3.4 });
var ctx = document.getElementById('cv').getContext('2d');
function rnd(seed) { var x = Math.sin(seed) * 10000; return x - Math.floor(x); }
var strokes = [];
for (var s = 0; s < 46; s++) {
  strokes.push({ y: 120 + rnd(s) * 480, x0: -40 + rnd(s + 1) * 200, len: 700 + rnd(s + 2) * 500, w: 18 + rnd(s + 3) * 36,
    c: ['rgba(234,88,12,', 'rgba(245,158,11,', 'rgba(252,211,77,'][s % 3], a: 0.08 + rnd(s + 4) * 0.12, t0: s * 0.05 });
}
function render(frame, totalFrames, fps) {
  animation.update(frame, fps);
  var sec = frame / fps;
  ctx.clearRect(0, 0, 1280, 720);
  strokes.forEach(function (st, k) {
    var p = Math.max(0, Math.min(1, (sec - st.t0) / 1.2));
    if (p <= 0) return;
    for (var j = 0; j < 6; j++) {            // layered, slightly jittered passes = watercolour edge
      ctx.strokeStyle = st.c + st.a + ')';
      ctx.lineWidth = st.w * (0.6 + rnd(k * 7 + j) * 0.6);
      ctx.lineCap = 'round';
      ctx.beginPath();
      var n = 24;
      for (var q = 0; q <= n * p; q++) {
        var x = st.x0 + (q / n) * st.len;
        var y = st.y + Math.sin(q * 0.5 + k) * 6 + (rnd(k * 31 + j * 5 + q) - 0.5) * 4;
        if (q === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
      }
      ctx.stroke();
    }
  });
}""",
    5,
    "p7-brush-paper",
)

# 8. Three.js: sessions as panels floating in space, camera dollies in (3D — the biggest gap)
three = beat(
    frame(W, H, """
<script src='https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js'></script>
<canvas id='gl' width='1280' height='720' class='absolute inset-0'></canvas>
<div id='cap' class='absolute left-0 right-0 bottom-10 text-center g text-4xl font-bold' style='opacity:0'>Every session, one space</div>"""),
    """var animation = new MulmoAnimation();
animation.animate('#cap', { opacity: [0, 1], translateY: [16, 0] }, { start: 3.2, end: 3.8, easing: 'easeOut' });
var renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('gl'), antialias: true, alpha: true, preserveDrawingBuffer: true });
renderer.setPixelRatio(1);
renderer.setSize(1280, 720, false);
var scene = new THREE.Scene();
scene.fog = new THREE.Fog(0xfff3dc, 9, 22);
var camera = new THREE.PerspectiveCamera(40, 1280 / 720, 0.1, 100);
scene.add(new THREE.AmbientLight(0xffffff, 0.9));
var sun = new THREE.DirectionalLight(0xffe0b0, 1.4); sun.position.set(4, 8, 6); scene.add(sun);
function label(text, hot) {
  var c = document.createElement('canvas'); c.width = 512; c.height = 320;
  var x = c.getContext('2d');
  x.fillStyle = '#1f1a17'; x.fillRect(0, 0, 512, 320);
  x.fillStyle = hot ? '#EA580C' : '#FFF3DC'; x.fillRect(0, 0, 512, 56);
  x.fillStyle = hot ? '#fff' : '#431407'; x.font = 'bold 30px Helvetica'; x.fillText(text, 20, 38);
  x.fillStyle = '#FCE8C8'; x.font = '22px Menlo';
  ['> claude', '● reading files', '● editing', '● tests pass'].forEach(function (l, i) { x.fillText(l, 20, 100 + i * 44); });
  return new THREE.CanvasTexture(c);
}
var panels = [];
for (var i = 0; i < 7; i++) {
  var a = (i - 3) * 0.42;
  var m = new THREE.Mesh(new THREE.BoxGeometry(2.4, 1.5, 0.08),
    [0, 0, 0, 0, 0, 0].map(function (_, f) { return f === 4 ? new THREE.MeshStandardMaterial({ map: label('project-' + i, i === 3) }) : new THREE.MeshStandardMaterial({ color: 0xfce8c8 }); }));
  m.position.set(Math.sin(a) * 7, (i % 2) * 0.5 - 0.25, -Math.cos(a) * 7 + 7);
  m.rotation.y = -a;
  scene.add(m); panels.push(m);
}
var ground = new THREE.Mesh(new THREE.CircleGeometry(12, 64), new THREE.MeshStandardMaterial({ color: 0xfce8c8 }));
ground.rotation.x = -Math.PI / 2; ground.position.y = -1.4; scene.add(ground);
function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
function render(frame, totalFrames, fps) {
  animation.update(frame, fps);
  var t = frame / fps;
  var p = ease(Math.min(1, t / 4.5));
  var orbit = -0.5 + p * 0.5;                   // swing round to face the centre panel
  var dist = 13 - p * 6.2;                      // dolly in
  camera.position.set(Math.sin(orbit) * dist, 2.6 - p * 1.9, Math.cos(orbit) * dist);
  camera.lookAt(0, 0, 0);
  panels.forEach(function (m, k) { m.position.y = ((k % 2) * 0.5 - 0.25) + Math.sin(t * 1.6 + k) * 0.08; });
  renderer.render(scene, camera);
}""",
    6,
    "p8-threejs-space",
)

# ---------------------------------------------------------------- 9:16 beats
VW, VH = 720, 1280

telop_lines = ["Cells run side by side", "Each header shows its PR", "Tap a chip, open the diff", "Done? It chimes."]
telop = beat(
    frame(VW, VH, "<div class='absolute left-0 right-0 top-24 text-center g text-5xl font-bold'>MulmoTerminal</div>"
          "<div class='absolute overflow-hidden' style='left:60px;right:60px;top:420px;height:360px'>"
          "<div id='roll' class='flex flex-col gap-10'>"
          + "".join(f"<div class='text-4xl font-bold px-6 py-5 rounded-2xl' style='background:#FFF3DC;border-left:10px solid #EA580C'>{t}</div>" for t in telop_lines)
          + "</div></div>"),
    """// hold each line, then roll up by one row. Step height is measured, not hard-coded.
var roll = document.getElementById('roll');
var step = roll.children[1].offsetTop - roll.children[0].offsetTop;
function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }
function render(frame, totalFrames, fps) {
  var t = frame / fps, y = 0;
  for (var k = 0; k < 3; k++) y += ease(Math.max(0, Math.min(1, (t - (1.4 + k * 1.4)) / 0.4)));
  roll.style.transform = 'translateY(' + (-step * y) + 'px)';
  for (var i = 0; i < roll.children.length; i++) roll.children[i].style.opacity = Math.abs(i - y) < 0.5 ? 1 : 0.35;
}""",
    6,
    "v1-scroll-telop",
)

vcount = beat(
    frame(VW, VH, """
<div class='absolute left-0 right-0 top-40 text-center g text-5xl font-bold leading-tight'>Two years<br>in one number</div>
<div id='n' class='absolute left-0 right-0 text-center font-extrabold' style='top:520px;font-size:150px;color:#EA580C'>0</div>
<div class='absolute left-0 right-0 text-center text-3xl' style='top:720px'>records kept</div>
<div class='absolute' style='left:80px;right:80px;top:880px;height:22px;border-radius:11px;background:#FCE8C8'><div id='b' style='width:0;height:100%;border-radius:11px;background:#EA580C'></div></div>"""),
    """var animation = new MulmoAnimation();
animation
  .animate('#b', { width: [0, 100, '%'] }, { start: 0.4, end: 4.0, easing: 'easeOut' });
function render(frame, totalFrames, fps) {
  animation.update(frame, fps);
  var p = Math.max(0, Math.min(1, (frame / fps - 0.4) / 3.6));
  document.getElementById('n').textContent = Math.round(30113 * (1 - (1 - p) * (1 - p))).toLocaleString('en-US');
}""",
    5,
    "v2-count-up",
)


def deck(title, w, h, beats):
    return {
        "$mulmocast": {"version": "1.1"},
        "canvasSize": {"width": w, "height": h},
        "title": title,
        "description": "Sampler of motion patterns seen in Claude Opus 5.5 posts on X (2026-09), rebuilt as html_tailwind animation beats. Silent: each beat has a fixed duration.",
        "lang": "en",
        "speechParams": {"speakers": {"Presenter": {"displayName": {"en": "Presenter"}, "voiceId": "Kore", "isDefault": True, "provider": "gemini", "model": "gemini-2.5-pro-preview-tts"}}},
        "beats": beats,
    }


(HERE / "opus55-motion-sampler.json").write_text(json.dumps(deck("Opus 5.5 motion sampler (16:9)", W, H, [sting, lift, zoom, draw, accum, split, brush, three]), ensure_ascii=False, indent=2) + "\n")
(HERE / "opus55-motion-sampler-vertical.json").write_text(json.dumps(deck("Opus 5.5 motion sampler (9:16)", VW, VH, [telop, vcount]), ensure_ascii=False, indent=2) + "\n")
print("ok")
