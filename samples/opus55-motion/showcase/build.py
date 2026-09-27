"""Showcase decks, levels 2-3 plus a high-tempo Shorts reel.

Level 1 (safe) lives in build.py. Here every beat drives its own timeline in render(frame):
MulmoAnimation is only a helper for simple tweens, and staged motion on one element
fights inside it (the later entry wins every frame), so nothing here depends on it.

Silent beats with fixed durations: rendering costs no TTS.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent

FONT = "<style>.t{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif}.g{font-family:Georgia,serif}.m{font-family:Menlo,monospace}</style>"
CREAM = "linear-gradient(160deg,#FFFBF2,#FFF3DC 55%,#FCE8C8)"

# Shared JS helpers, prepended to every script.
HELPERS = """
function clamp01(x) { return Math.max(0, Math.min(1, x)); }
function P(t, a, b) { return clamp01((t - a) / (b - a)); }
function eio(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function eout(x) { return 1 - Math.pow(1 - x, 3); }
function eback(x) { var c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }
function rnd(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
function $(id) { return document.getElementById(id); }
"""


def beat(w, h, html, script, duration, label, bg=CREAM):
    page = f"{FONT}<div class='t relative overflow-hidden' style='width:{w}px;height:{h}px;background:{bg};color:#431407'>{html}</div>"
    return {
        "id": label,
        "text": "",
        "duration": duration,
        "image": {"type": "html_tailwind", "html": page, "script": HELPERS + script, "animation": {"fps": 30}},
    }


W, H = 1280, 720


def letters(word, cls, style=""):
    return "".join(f"<span class='{cls}' style='display:inline-block;{style}'>{c if c != ' ' else '&nbsp;'}</span>" for c in word)


# ============================================================ LEVEL 2

# L2-1 Kinetic typography: masked letter rises, colour-block wipes, a bounce, then everything shrinks to a logo.
kinetic = beat(W, H, f"""
<div id='blk' class='absolute inset-y-0 left-0' style='width:0;background:#EA580C'></div>
<div id='blk2' class='absolute inset-y-0 right-0' style='width:0;background:#431407'></div>
<div id='grp' class='absolute inset-0' style='transform-origin:50% 50%'>
  <div id='s1' class='absolute inset-0 flex items-center justify-center'><div style='overflow:hidden;height:190px'><div class='g font-bold' style='font-size:170px;line-height:190px'>{letters('Talk.', 'a')}</div></div></div>
  <div id='s2' class='absolute inset-0 flex items-center justify-center' style='opacity:0'><div style='overflow:hidden;height:190px'><div class='g font-bold' style='font-size:170px;line-height:190px;color:#fff'>{letters('It keeps', 'b')}</div></div></div>
  <div id='s3' class='absolute inset-0 flex flex-col items-center justify-center' style='opacity:0'>
    <div class='g font-bold' style='font-size:170px;line-height:190px;color:#FDE68A'>{letters('everything.', 'c')}</div>
    <svg width='900' height='60'><path id='ul' d='M20 40 C 250 10, 600 60, 880 20' stroke='#EA580C' stroke-width='14' fill='none' stroke-linecap='round' stroke-dasharray='900' stroke-dashoffset='900'/></svg>
  </div>
</div>
<div id='logo' class='absolute inset-0 flex items-center justify-center' style='opacity:0'><div class='font-extrabold tracking-tight' style='font-size:96px;color:#431407'>Mulmo<span style='color:#EA580C'>Claude</span></div></div>
""", """
var A = document.querySelectorAll('.a'), B = document.querySelectorAll('.b'), C = document.querySelectorAll('.c');
function render(frame, total, fps) {
  var t = frame / fps;
  A.forEach(function (el, i) { var p = eout(P(t, 0.15 + i * 0.06, 0.55 + i * 0.06)); el.style.transform = 'translateY(' + (1 - p) * 190 + 'px)'; });
  $('blk').style.width = eio(P(t, 1.1, 1.55)) * 100 + '%';
  $('s1').style.opacity = t < 1.4 ? 1 : 0;
  $('s2').style.opacity = t >= 1.4 && t < 2.75 ? 1 : 0;
  B.forEach(function (el, i) { var p = eout(P(t, 1.45 + i * 0.05, 1.85 + i * 0.05)); el.style.transform = 'translateY(' + (1 - p) * 190 + 'px)'; });
  $('blk2').style.width = eio(P(t, 2.45, 2.9)) * 100 + '%';
  $('s3').style.opacity = t >= 2.75 ? 1 : 0;
  C.forEach(function (el, i) { var p = eback(P(t, 2.85 + i * 0.045, 3.25 + i * 0.045)); el.style.transform = 'scale(' + p + ') rotate(' + (1 - clamp01(p)) * -30 + 'deg)'; });
  $('ul').setAttribute('stroke-dashoffset', 900 * (1 - eio(P(t, 3.5, 4.0))));
  var s = P(t, 4.4, 4.9);
  $('grp').style.transform = 'scale(' + (1 - eio(s) * 0.85) + ') rotate(' + eio(s) * -8 + 'deg)';
  $('grp').style.opacity = 1 - P(t, 4.7, 4.9);
  $('blk2').style.opacity = 1 - P(t, 4.6, 5.0);
  $('blk').style.opacity = 1 - P(t, 4.6, 5.0);
  var l = P(t, 4.8, 5.3);
  $('logo').style.opacity = l;
  $('logo').style.transform = 'scale(' + (0.6 + eback(l) * 0.4) + ')';
}
""", 6.2, "L2-1-kinetic-type")

# L2-2 CSS 3D parallax dolly: layers at real depths, camera flies through, depth-of-field blur by distance.
cells = "".join(
    f"<div class='rounded-xl' style='background:#1f1a17;border-top:14px solid {'#EA580C' if i == 4 else '#FCE8C8'}'></div>" for i in range(9)
)
bokeh = "".join(
    f"<div class='bk absolute rounded-full' data-z='{350 + (i % 3) * 60}' data-x='{(i * 173) % 1300 - 650}' data-y='{(i * 97) % 640 - 320}' "
    f"style='width:{60 + (i * 37) % 90}px;height:{60 + (i * 37) % 90}px;background:rgba(245,158,11,.35)'></div>"
    for i in range(9)
)
chips = "".join(
    f"<div class='ly absolute px-6 py-3 rounded-full text-3xl font-bold shadow-xl' data-z='{z}' data-x='{x}' data-y='{y}' style='background:{bg};color:{fg}'>{t}</div>"
    for t, z, x, y, bg, fg in [("main", 180, -420, -210, "#FFF3DC", "#431407"), ("ctx 62%", 260, 380, -240, "#FFF3DC", "#431407"),
                               ("+12 −3", 220, -470, 200, "#FFF3DC", "#431407"), ("PR #125", 300, 420, 190, "#EA580C", "#fff")]
)
parallax = beat(W, H, f"""
<div class='absolute inset-0' style='perspective:1100px;perspective-origin:50% 50%'>
  <div id='cam' class='absolute inset-0' style='transform-style:preserve-3d'>
    <div class='ly absolute rounded-full' data-z='-1600' data-x='0' data-y='-60' style='width:1500px;height:1500px;background:radial-gradient(circle,#FDE68A,#FDBA74 45%,rgba(253,186,116,0) 70%)'></div>
    <div class='ly absolute grid grid-cols-3 gap-6' data-z='-700' data-x='0' data-y='0' style='width:1500px;height:840px'>{cells}</div>
    <div class='ly absolute rounded-2xl shadow-2xl' data-z='0' data-x='0' data-y='0' style='width:760px;height:430px;background:#1f1a17'>
      <div class='px-5 py-3 rounded-t-2xl font-bold' style='background:#FFF3DC'>mulmo-presentations</div>
      <div class='m text-lg leading-8 px-5 py-4' style='color:#FCE8C8'>&gt; claude<br><span style='color:#F59E0B'>● Reading PROGRESS.md</span><br>● Editing demos/*.json<br>● Tests pass</div>
    </div>
    {chips}
    {bokeh}
  </div>
</div>
<div id='cap' class='absolute left-0 right-0 bottom-10 text-center' style='opacity:0'><span class='g text-4xl font-bold px-8 py-3 rounded-full shadow-xl' style='background:#FFF3DC'>Depth, not slides</span></div>
""", """
var layers = Array.prototype.slice.call(document.querySelectorAll('.ly, .bk'));
layers.forEach(function (el) {
  el.style.left = '640px'; el.style.top = '360px';
});
function render(frame, total, fps) {
  var t = frame / fps, p = eio(P(t, 0, 6));
  var dz = -500 + p * 820, ry = -22 + p * 30, rx = 10 - p * 12;
  $('cam').style.transform = 'translateZ(' + dz + 'px) rotateX(' + rx + 'deg) rotateY(' + ry + 'deg)';
  layers.forEach(function (el, i) {
    var z = +el.dataset.z, x = +el.dataset.x, y = +el.dataset.y;
    var bob = el.classList.contains('bk') ? Math.sin(t * 1.3 + i) * 14 : Math.sin(t * 1.1 + i) * 6;
    el.style.transform = 'translate(-50%,-50%) translate3d(' + x + 'px,' + (y + bob) + 'px,' + z + 'px)';
    var dist = Math.abs(z + dz - 60);                 // focal plane just in front of the window
    el.style.filter = 'blur(' + Math.min(14, dist / 90) + 'px)';
  });
  $('cap').style.opacity = P(t, 4.2, 4.8);
}
""", 6.5, "L2-2-parallax-3d")

# L2-3 Liquid wipe: a wobbling blob grows out of a chip and becomes the next scene, twice.
liquid = beat(W, H, """
<div id='A' class='absolute inset-0 flex items-center justify-center' style='background:#1f1a17'>
  <div class='m text-4xl' style='color:#FCE8C8'>● tests pass <span id='chip' class='ml-4 px-4 py-1 rounded-full text-2xl' style='background:#EA580C;color:#fff'>PR #125</span></div>
</div>
<div id='B' class='absolute inset-0 flex items-center justify-center' style='background:#EA580C;clip-path:circle(0)'>
  <div class='g font-bold text-white' style='font-size:150px'>Merged.</div>
</div>
<div id='C' class='absolute inset-0 flex items-center justify-center' style='background:#FFF3DC;clip-path:circle(0)'>
  <div class='g font-bold' style='font-size:110px'>Next task <span style='color:#EA580C'>→</span></div>
</div>
""", """
function blob(cx, cy, R, t, seed) {
  var pts = [];
  for (var k = 0; k < 72; k++) {
    var a = k / 72 * Math.PI * 2;
    var r = R * (1 + 0.13 * Math.sin(3 * a + t * 6 + seed) + 0.08 * Math.sin(5 * a - t * 4) + 0.05 * Math.sin(9 * a + t * 9));
    pts.push((cx + Math.cos(a) * r).toFixed(1) + 'px ' + (cy + Math.sin(a) * r).toFixed(1) + 'px');
  }
  return 'polygon(' + pts.join(',') + ')';
}
var cr = $('chip').getBoundingClientRect(), cx = cr.left + cr.width / 2, cy = cr.top + cr.height / 2;
function render(frame, total, fps) {
  var t = frame / fps;
  var b = eio(P(t, 1.2, 2.3));
  $('B').style.clipPath = b <= 0 ? 'circle(0)' : blob(cx + (640 - cx) * b, cy + (360 - cy) * b, 20 + b * 1000, t, 0);
  $('chip').style.transform = 'scale(' + (1 + Math.sin(P(t, 0.4, 1.2) * Math.PI) * 0.25) + ')';
  var c = eio(P(t, 3.1, 4.2));
  $('C').style.clipPath = c <= 0 ? 'circle(0)' : blob(640, 470, 10 + c * 1000, t, 2);
}
""", 5.2, "L2-3-liquid-wipe")

# L2-4 After-Effects style hit: light leak, motion-blurred slam, impact shake + RGB split, trim-path burst, rings, glow, flare.
rays = "".join(
    f"<line class='ray' x1='640' y1='360' x2='{640 + 520 * __import__('math').cos(i / 14 * 6.2832):.0f}' y2='{360 + 520 * __import__('math').sin(i / 14 * 6.2832):.0f}' "
    f"stroke='{'#EA580C' if i % 2 else '#FDE68A'}' stroke-width='{6 if i % 2 else 3}' stroke-linecap='round' pathLength='100' stroke-dasharray='0 100'/>"
    for i in range(14)
)
aefx = beat(W, H, f"""
<div id='leak1' class='absolute rounded-full' style='width:900px;height:900px;left:-300px;top:-400px;background:radial-gradient(circle,rgba(253,186,116,.9),rgba(253,186,116,0) 65%);mix-blend-mode:screen'></div>
<div id='leak2' class='absolute rounded-full' style='width:800px;height:800px;right:-300px;bottom:-400px;background:radial-gradient(circle,rgba(234,88,12,.7),rgba(234,88,12,0) 65%);mix-blend-mode:screen'></div>
<svg class='absolute inset-0' width='1280' height='720'>{rays}
  <circle id='r1' cx='640' cy='360' r='0' fill='none' stroke='#FDE68A' stroke-width='10'/>
  <circle id='r2' cx='640' cy='360' r='0' fill='none' stroke='#EA580C' stroke-width='6'/>
</svg>
<div id='shake' class='absolute inset-0'>
  <div id='ghosts'></div>
  <div id='hero' class='absolute inset-0 flex items-center justify-center'>
    <div id='cr' class='absolute font-extrabold' style='font-size:180px;color:#ff2d55;opacity:0'>4.18</div>
    <div id='cc' class='absolute font-extrabold' style='font-size:180px;color:#22d3ee;opacity:0'>4.18</div>
    <div id='main' class='absolute font-extrabold' style='font-size:180px;color:#fff'>4.18</div>
  </div>
  <div id='sub' class='absolute left-0 right-0 text-center font-bold tracking-[0.4em]' style='top:500px;font-size:30px;color:#FDE68A;opacity:0'>MULMOTERMINAL RELEASE</div>
</div>
<div id='flare' class='absolute' style='left:0;top:352px;width:1280px;height:16px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.95),transparent);filter:blur(3px);opacity:0'></div>
<div id='flash' class='absolute inset-0' style='background:#fff;opacity:0'></div>
""", """
var rays = document.querySelectorAll('.ray');
var ghosts = $('ghosts');
for (var g = 0; g < 6; g++) {
  var d = document.createElement('div');
  d.className = 'absolute inset-0 flex items-center justify-center font-extrabold';
  d.style.fontSize = '180px'; d.style.color = '#FDE68A';
  d.textContent = '4.18'; ghosts.appendChild(d);
}
var HIT = 1.0;
function render(frame, total, fps) {
  var t = frame / fps;
  // background: dark warm, light leaks drift and breathe
  $('leak1').style.transform = 'translate(' + (t * 60) + 'px,' + (t * 30) + 'px) scale(' + (1 + Math.sin(t * 2) * 0.1) + ')';
  $('leak1').style.opacity = 0.35 + 0.5 * P(t, 0, 0.9) - 0.3 * P(t, 3.5, 5);
  $('leak2').style.transform = 'translate(' + (-t * 50) + 'px,' + (-t * 20) + 'px)';
  $('leak2').style.opacity = 0.3 + 0.6 * Math.exp(-Math.pow((t - HIT) * 3, 2));
  // slam in from the left with motion-blur ghosts
  var s = P(t, 0.55, HIT), x = (1 - eout(s)) * -1400;
  $('main').style.transform = 'translateX(' + x + 'px) skewX(' + (1 - s) * -25 + 'deg)';
  var gs = ghosts.children;
  for (var k = 0; k < gs.length; k++) {
    var gp = P(t, 0.55 - (k + 1) * 0.02, HIT - (k + 1) * 0.02);
    gs[k].style.transform = 'translateX(' + (1 - eout(gp)) * -1400 + 'px)';
    gs[k].style.opacity = t < HIT + 0.05 ? 0.25 - k * 0.035 : 0;
    gs[k].style.filter = 'blur(' + (4 + k * 2) + 'px)';
  }
  // impact: flash, shake, RGB split
  var imp = Math.exp(-Math.max(0, t - HIT) * 9) * (t >= HIT ? 1 : 0);
  $('flash').style.opacity = imp * 0.7;
  $('shake').style.transform = 'translate(' + (rnd(frame) - 0.5) * 40 * imp + 'px,' + (rnd(frame + 9) - 0.5) * 40 * imp + 'px)';
  $('cr').style.opacity = $('cc').style.opacity = imp > 0.02 ? 0.8 : 0;
  $('cr').style.transform = 'translateX(' + (-18 * imp) + 'px)';
  $('cc').style.transform = 'translateX(' + (18 * imp) + 'px)';
  // trim-path burst: each ray's visible segment travels outward
  rays.forEach(function (r, i) {
    var p = P(t, HIT + i * 0.01, HIT + 0.55 + i * 0.01);
    var head = eout(p) * 100, tail = eio(P(t, HIT + 0.15, HIT + 0.75)) * 100;
    r.setAttribute('stroke-dasharray', '0 ' + tail + ' ' + Math.max(0, head - tail) + ' 200');
  });
  var r1 = P(t, HIT, HIT + 0.7), r2 = P(t, HIT + 0.12, HIT + 0.9);
  $('r1').setAttribute('r', eout(r1) * 380); $('r1').setAttribute('stroke-width', (1 - r1) * 18); $('r1').style.opacity = r1 < 1 ? 1 : 0;
  $('r2').setAttribute('r', eout(r2) * 520); $('r2').setAttribute('stroke-width', (1 - r2) * 10); $('r2').style.opacity = r2 < 1 ? 1 : 0;
  // glow pulse
  var glow = 20 + 30 * Math.exp(-Math.max(0, t - HIT) * 3) + 8 * Math.sin(t * 5);
  $('main').style.textShadow = '0 0 ' + glow + 'px rgba(253,186,116,.95), 0 0 ' + glow * 2 + 'px rgba(234,88,12,.7)';
  // flare sweep and subtitle tracking in
  var f = P(t, 1.3, 2.1);
  $('flare').style.opacity = Math.sin(f * Math.PI);
  $('flare').style.transform = 'scaleX(' + (0.2 + f) + ') translateX(' + (f - 0.5) * 600 + 'px)';
  var sb = eout(P(t, 1.6, 2.4));
  $('sub').style.opacity = sb;
  $('sub').style.letterSpacing = (1.2 - sb * 0.8) + 'em';
  // exit: everything punches out
  var ex = eio(P(t, 4.3, 4.9));
  $('shake').style.opacity = 1 - ex;
  $('hero').style.transform = 'scale(' + (1 + ex * 2.5) + ')';
  $('hero').style.filter = 'blur(' + ex * 20 + 'px)';
}
""", 5.2, "L2-4-after-effects-hit", bg="radial-gradient(circle at 50% 50%, #3b1a0c, #140906 75%)")

# ============================================================ LEVEL 3

# L3-1 Particles assemble a logo, explode, and re-form as a second word. Motion streaks are drawn analytically.
particles = beat(W, H, """
<canvas id='cv' width='1280' height='720' class='absolute inset-0'></canvas>
""", """
var ctx = $('cv').getContext('2d');
function sample(text, size) {
  var c = document.createElement('canvas'); c.width = 1280; c.height = 720;
  var x = c.getContext('2d'); x.fillStyle = '#000'; x.font = '900 ' + size + 'px Helvetica Neue, Helvetica, Arial';
  x.textAlign = 'center'; x.textBaseline = 'middle'; x.fillText(text, 640, 360);
  var d = x.getImageData(0, 0, 1280, 720).data, out = [];
  for (var yy = 0; yy < 720; yy += 5) for (var xx = 0; xx < 1280; xx += 5) if (d[(yy * 1280 + xx) * 4 + 3] > 128) out.push([xx, yy]);
  return out;
}
var TA = sample('MulmoClaude', 170), TB = sample('MulmoTerminal', 150);
var N = Math.max(TA.length, TB.length);
var PAL = ['#EA580C', '#F59E0B', '#FDBA74', '#431407', '#FDE68A'];
var parts = [];
for (var i = 0; i < N; i++) {
  var a = rnd(i) * Math.PI * 2, r = 500 + rnd(i + 1) * 500;
  parts.push({ sx: 640 + Math.cos(a) * r, sy: 360 + Math.sin(a) * r * 0.7, a: TA[i % TA.length], b: TB[i % TB.length],
    d: rnd(i + 2) * 0.7, sw: (rnd(i + 3) - 0.5) * 2, c: PAL[i % 5], ex: rnd(i + 4) * Math.PI * 2, es: 150 + rnd(i + 5) * 350 });
}
function pos(p, t) {
  if (t < 3.3) {                                  // swirl in to word A
    var q = eio(P(t, 0.3 + p.d, 1.9 + p.d)), sw = Math.sin(q * Math.PI) * 180 * p.sw;
    var x = p.sx + (p.a[0] - p.sx) * q, y = p.sy + (p.a[1] - p.sy) * q;
    return [x - sw * 0.6, y + sw];
  }
  var e = P(t, 3.3, 3.8), g = eio(P(t, 3.7 + p.d * 0.5, 4.9 + p.d * 0.5));
  var ox = p.a[0] + Math.cos(p.ex) * p.es * eout(e), oy = p.a[1] + Math.sin(p.ex) * p.es * eout(e);
  return [ox + (p.b[0] - ox) * g, oy + (p.b[1] - oy) * g];
}
function render(frame, total, fps) {
  var t = frame / fps;
  var bg = ctx.createLinearGradient(0, 0, 1280, 720); bg.addColorStop(0, '#FFFBF2'); bg.addColorStop(1, '#FCE8C8');
  ctx.fillStyle = bg; ctx.fillRect(0, 0, 1280, 720);
  ctx.lineCap = 'round';
  for (var i = 0; i < parts.length; i++) {
    var p = parts[i], a = pos(p, t - 0.045), b = pos(p, t);
    ctx.strokeStyle = p.c; ctx.lineWidth = 3.2;
    ctx.beginPath(); ctx.moveTo(a[0], a[1]); ctx.lineTo(b[0] + 0.01, b[1]); ctx.stroke();
  }
}
""", 6.0, "L3-1-particles-logo")

# L3-2 Raw WebGL2 fragment shader: ray-marched spheres, printed as two-ink halftone with misregistration.
shader = beat(W, H, """
<canvas id='gl' width='1280' height='720' class='absolute inset-0'></canvas>
<div id='cap' class='absolute left-12 bottom-10 g text-5xl font-bold' style='color:#431407;opacity:0'>One HTML file. No images.</div>
""", """
var gl = $('gl').getContext('webgl2', { preserveDrawingBuffer: true });
var VS = '#version 300 es\\nin vec2 p;void main(){gl_Position=vec4(p,0.,1.);}';
var FS = [
'#version 300 es',
'precision highp float;uniform float T;uniform vec2 R;out vec4 o;',
'float map(vec3 q){float d=q.y+1.;',
' for(int i=0;i<5;i++){float fi=float(i);vec3 c=vec3(sin(T*.7+fi*1.26)*2.2,sin(T*1.3+fi)*.35+.1,cos(T*.7+fi*1.26)*2.2+6.);',
'  d=min(d,length(q-c)-(.55+.12*fi));}',
' return min(d,length(q-vec3(0.,.2+sin(T)*.2,6.))-1.1);}',
'vec3 nrm(vec3 p){vec2 e=vec2(.002,0.);return normalize(vec3(map(p+e.xyy)-map(p-e.xyy),map(p+e.yxy)-map(p-e.yxy),map(p+e.yyx)-map(p-e.yyx)));}',
'float shade(vec2 uv){vec3 ro=vec3(0.,1.4-T*.05,-1.5+T*.35),rd=normalize(vec3(uv,1.4)-vec3(0.,.25,0.));float t=0.;',
' for(int i=0;i<90;i++){float d=map(ro+rd*t);if(d<.001||t>30.)break;t+=d;}',
' if(t>30.)return 1.;vec3 p=ro+rd*t,n=nrm(p),l=normalize(vec3(.6,.9,-.4));',
' float s=1.;float k=.05;for(int i=0;i<24;i++){float h=map(p+l*k);s=min(s,10.*h/k);k+=clamp(h,.02,.3);}',
' float dif=clamp(dot(n,l),0.,1.)*clamp(s,0.,1.);float ao=clamp(map(p+n*.3)/.3,0.,1.);',
' return clamp(.12+.85*dif*(.5+.5*ao)+.25*pow(1.-max(dot(n,-rd),0.),3.),0.,1.);}',
'float dots(vec2 f,float ang,float cell,float v){mat2 m=mat2(cos(ang),-sin(ang),sin(ang),cos(ang));vec2 g=m*f/cell;vec2 c=fract(g)-.5;',
' float r=sqrt(clamp(1.-v,0.,1.))*.62;return smoothstep(r+.06,r-.06,length(c));}',
'void main(){vec2 f=gl_FragCoord.xy;vec2 uv=(f-.5*R)/R.y;',
' float cell=mix(22.,7.,smoothstep(.2,3.5,T));',
' vec2 mis=vec2(sin(T*2.)*3.,cos(T*1.7)*2.);',
' float v1=shade(uv),v2=shade((f+mis-.5*R)/R.y);',
' float inkA=dots(f,.26,cell,v1),inkB=dots(f+mis,.79,cell*1.1,v2);',
' vec3 paper=vec3(1.,.97,.9),a=vec3(.92,.35,.05),b=vec3(.26,.08,.03);',
' vec3 col=paper;col=mix(col,col*a*1.05,inkA*.95);col=mix(col,col*b*1.6,inkB*.55);',
' float grain=fract(sin(dot(f,vec2(12.9898,78.233)))*43758.5453);col-=grain*.04;',
' o=vec4(col,1.);}'].join('\\n');
function sh(type, src) { var s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) console.error(gl.getShaderInfoLog(s)); return s; }
var pr = gl.createProgram(); gl.attachShader(pr, sh(gl.VERTEX_SHADER, VS)); gl.attachShader(pr, sh(gl.FRAGMENT_SHADER, FS)); gl.linkProgram(pr); gl.useProgram(pr);
var buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
var loc = gl.getAttribLocation(pr, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
var uT = gl.getUniformLocation(pr, 'T'), uR = gl.getUniformLocation(pr, 'R');
function render(frame, total, fps) {
  var t = frame / fps;
  gl.viewport(0, 0, 1280, 720); gl.uniform1f(uT, t); gl.uniform2f(uR, 1280, 720);
  gl.drawArrays(gl.TRIANGLES, 0, 3);
  $('cap').style.opacity = P(t, 3.6, 4.3);
}
""", 6.0, "L3-2-shader-halftone")

# L3-3 Three.js: records rise as a city, wireframe first then solid, camera orbits, one tower gets a tracked label.
city = beat(W, H, """
<script src='https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js'></script>
<canvas id='gl' width='1280' height='720' class='absolute inset-0'></canvas>
<div id='tag' class='absolute px-4 py-2 rounded-xl text-xl font-bold shadow-xl' style='background:#EA580C;color:#fff;opacity:0;transform:translate(-50%,-130%)'>Sep 27 · 14 entries</div>
<div id='cap' class='absolute left-0 right-0 top-8 text-center g text-5xl font-bold' style='opacity:0'>A year of records, as a city</div>
""", """
var R3 = new THREE.WebGLRenderer({ canvas: $('gl'), antialias: true, preserveDrawingBuffer: true });
R3.setPixelRatio(1); R3.setSize(1280, 720, false); R3.setClearColor(0xfff3dc);
var scene = new THREE.Scene(); scene.fog = new THREE.Fog(0xfff3dc, 28, 70);
var cam = new THREE.PerspectiveCamera(38, 1280 / 720, 0.1, 200);
scene.add(new THREE.HemisphereLight(0xfff7e8, 0xd9a066, 1.1));
var sun = new THREE.DirectionalLight(0xffffff, 1.2); sun.position.set(10, 20, 8); scene.add(sun);
var fillMat = new THREE.MeshStandardMaterial({ color: 0xfce8c8, transparent: true, opacity: 0, roughness: 0.8 });
var lineMat = new THREE.LineBasicMaterial({ color: 0x9a3412, transparent: true, opacity: 0.9 });
var hotMat = new THREE.MeshStandardMaterial({ color: 0xea580c, emissive: 0xea580c, emissiveIntensity: 0.2 });
var box = new THREE.BoxGeometry(0.8, 1, 0.8); box.translate(0, 0.5, 0);
var edges = new THREE.EdgesGeometry(box);
var towers = [], G = 22, hot = null;
for (var i = 0; i < G; i++) for (var j = 0; j < G; j++) {
  var x = i - G / 2 + 0.5, z = j - G / 2 + 0.5, n = i * G + j;
  var h = 0.3 + Math.pow(rnd(n), 2.2) * 5 + (Math.sin(i * 0.5) + Math.cos(j * 0.4)) * 0.6;
  var isHot = (i === 13 && j === 9);
  var g = new THREE.Group(); g.position.set(x, 0, z);
  var m = new THREE.Mesh(box, isHot ? hotMat : fillMat); var l = new THREE.LineSegments(edges, lineMat);
  g.add(m); g.add(l); scene.add(g);
  var tw = { g: g, h: isHot ? 5.5 : Math.max(0.2, h), s: 0.2 + Math.hypot(x, z) * 0.1 };
  towers.push(tw); if (isHot) hot = tw;
}
var ground = new THREE.Mesh(new THREE.PlaneGeometry(80, 80), new THREE.MeshStandardMaterial({ color: 0xfbe3c0 }));
ground.rotation.x = -Math.PI / 2; ground.position.y = -0.01; scene.add(ground);
function render(frame, total, fps) {
  var t = frame / fps;
  towers.forEach(function (tw) { var p = eback(P(t, tw.s, tw.s + 0.9)); tw.g.scale.set(1, Math.max(0.001, p * tw.h), 1); });
  fillMat.opacity = eio(P(t, 2.4, 3.6));
  lineMat.opacity = 0.9 - 0.5 * P(t, 2.8, 3.8);
  hotMat.emissiveIntensity = 0.2 + 0.6 * (0.5 + 0.5 * Math.sin(t * 6)) * P(t, 4, 4.5);
  var a = 0.9 + t * 0.16, rad = 26 - eio(P(t, 0, 7)) * 8, hgt = 20 - eio(P(t, 0, 7)) * 10;
  cam.position.set(Math.cos(a) * rad, hgt, Math.sin(a) * rad); cam.lookAt(0, 3.2, 0);
  R3.render(scene, cam);
  var v = new THREE.Vector3(hot.g.position.x, hot.g.scale.y + 0.2, hot.g.position.z).project(cam);   // box is 1 unit tall, scaled
  $('tag').style.left = ((v.x + 1) / 2 * 1280) + 'px'; $('tag').style.top = ((1 - v.y) / 2 * 720) + 'px';
  $('tag').style.opacity = P(t, 4.2, 4.7);
  $('cap').style.opacity = P(t, 0.6, 1.3) * (1 - P(t, 3.8, 4.2));
}
""", 7.0, "L3-3-three-city")

# L3-4 Infinite zoom (powers of ten): year -> day -> record -> sentence -> word, one continuous camera.
S = 10
levels = [
    # each level is a 1280x720 page; its centre 128x72 box is exactly where the next level lives
    ("Your year", "<div class='absolute' style='left:174px;top:299px;display:grid;grid-template-columns:repeat(52,14px);gap:4px'>"
     + "".join(f"<div style='width:14px;height:14px;border-radius:3px;background:{['#FCE8C8', '#FDE68A', '#F59E0B', '#EA580C'][int((i * 7919) % 97 / 25)]}'></div>" for i in range(52 * 7))
     + "</div>"),
    ("Sep 27", "".join(f"<div class='absolute left-[240px] right-[240px] rounded-xl px-6 flex items-center text-2xl' style='top:{130 + k * 96}px;height:72px;background:#FFF3DC'>{e}</div>"
                       for k, e in enumerate(["08:10  Morning run 5 km", "10:30  Standup notes", "", "18:40  Groceries", "21:00  Read 30 pages"]))),
    ("One record", "<div class='absolute left-[260px] right-[260px] top-[120px] bottom-[120px] rounded-3xl p-10' style='background:#FFF3DC'>"
     "<div class='text-2xl font-bold mb-6'>Lunch · 12:40</div><div class='text-xl leading-10' style='color:#7c4a2d'>Place: the soba shop by the station<br>With: A.<br>Mood: calm<br></div></div>"),
    ("One sentence", "<div class='absolute inset-x-0 flex justify-center' style='top:230px'><div class='g text-5xl'>“I want to cook</div></div>"
     "<div class='absolute inset-x-0 flex justify-center' style='top:430px'><div class='g text-5xl'>more at home.”</div></div>"),
    ("", "<div class='absolute inset-0 flex items-center justify-center'><div class='g font-bold' style='font-size:210px;color:#EA580C'>cook</div></div>"),
]
PORTALS = [
    "<div class='absolute rounded' style='left:576px;top:324px;width:128px;height:72px;border:3px solid #EA580C'></div>",
    "<div class='absolute rounded-xl' style='left:576px;top:324px;width:128px;height:72px;background:#EA580C'></div>",
    "<div class='absolute rounded' style='left:576px;top:324px;width:128px;height:72px;background:#FCE8C8'></div>",
    "<div class='absolute rounded' style='left:576px;top:324px;width:128px;height:72px;border-bottom:4px solid #EA580C'></div>",
    "",
]
lv_html = "".join(
    f"<div class='lv absolute' style='left:0;top:0;width:1280px;height:720px;transform-origin:640px 360px'>{body}{PORTALS[i]}"
    + (f"<div class='absolute left-0 right-0 top-8 text-center g text-4xl font-bold'>{title}</div>" if title else "")
    + "</div>"
    for i, (title, body) in enumerate(levels)
)
zoom = beat(W, H, lv_html + "<div id='cap' class='absolute left-0 right-0 bottom-10 text-center g text-4xl font-bold' style='opacity:0'>Every scale is still yours.</div>", """
var LV = document.querySelectorAll('.lv'), S = 10;
function u(t) {                                    // hold, zoom one decade, hold, ...
  var seg = 1.45, k = Math.floor(t / seg), f = (t - k * seg) / seg;
  if (k >= LV.length - 1) return LV.length - 1;
  return k + eio(clamp01((f - 0.25) / 0.75));
}
function render(frame, total, fps) {
  var t = frame / fps, U = u(t);
  LV.forEach(function (el, i) {
    var sc = Math.pow(S, U - i);                    // apparent scale of level i
    el.style.transform = 'scale(' + sc + ')';
    var vis = sc < 0.08 ? 0 : sc < 0.35 ? (sc - 0.08) / 0.27 : sc > 4 ? Math.max(0, 1 - (sc - 4) / 4) : 1;
    el.style.opacity = vis;
    el.style.display = vis <= 0 ? 'none' : 'block';
  });
  $('cap').style.opacity = P(t, 6.2, 6.8);
}
""", 7.4, "L3-4-infinite-zoom")

# ============================================================ TEMPO: high-tempo Shorts reel (9:16)
VW, VH = 720, 1280
CAP = "font-extrabold text-center leading-none"
STROKE = "-webkit-text-stroke:6px #1f1a17;paint-order:stroke fill;color:#fff"
scenes = [
    # id, start, end, background, content
    ("k0", 0.0, 0.5, "#EA580C", f"<div class='{CAP}' style='font-size:190px;{STROKE}'>STOP</div>"),
    ("k1", 0.5, 0.9, "#FFF3DC", f"<div class='{CAP}' style='font-size:110px;color:#431407'>scrolling.</div>"),
    ("k2", 0.9, 1.7, "#1f1a17", "<div class='grid grid-cols-2 gap-4' style='width:620px'>" + "".join(
        f"<div class='rounded-xl' style='height:250px;background:#2a221e;border-top:18px solid {'#EA580C' if i in (1, 4) else '#FCE8C8'}'></div>" for i in range(6)) + "</div>"),
    ("k3", 1.7, 2.3, "#431407", f"<div class='{CAP}' style='font-size:260px;color:#FDE68A'><span id='n6'>6</span></div><div class='{CAP} mt-4' style='font-size:80px;{STROKE}'>agents</div>"),
    ("k4", 2.3, 2.8, "#FFF3DC", f"<div class='{CAP}' style='font-size:130px;color:#EA580C'>1 screen.</div>"),
    ("k5", 2.8, 3.4, "#1f1a17", "<div class='px-10 py-6 rounded-full font-bold' style='font-size:84px;background:#EA580C;color:#fff'>PR #125</div>"),
    ("k6", 3.4, 3.8, "#EA580C", "<div class='px-10 py-6 rounded-full font-bold' style='font-size:84px;background:#FFF3DC;color:#431407'>ctx 62%</div>"),
    ("k7", 3.8, 4.2, "#FFF3DC", "<div class='px-10 py-6 rounded-full font-bold' style='font-size:84px;background:#431407;color:#FDE68A'>+12 −3</div>"),
    ("k8", 4.2, 4.6, "#431407", "<div class='px-10 py-6 rounded-full font-bold' style='font-size:84px;background:#22c55e;color:#fff'>tests ✓</div>"),
    ("k9", 4.6, 5.8, "#431407", "<div id='bell' style='font-size:180px'>🔔</div><div class='flex flex-wrap justify-center gap-x-6 mt-6' style='width:640px'>"
     + "".join(f"<span class='w {CAP}' style='font-size:92px;{STROKE};opacity:0'>{w}</span>" for w in ["It", "chimes", "when", "done."]) + "</div>"),
    ("k10", 5.8, 7.0, "#EA580C", "<div id='lg' class='font-extrabold' style='font-size:78px;color:#fff;letter-spacing:-2px'>MulmoTerminal</div><div id='sweep' class='absolute' style='top:0;bottom:0;width:120px;background:linear-gradient(90deg,transparent,rgba(255,255,255,.7),transparent);transform:skewX(-20deg)'></div>"),
    ("k11", 7.0, 8.4, "#1f1a17", "<div class='m px-8 py-6 rounded-2xl' style='font-size:44px;background:#2a221e;color:#FDE68A'>$ <span id='cmd'></span><span id='cur'>▋</span></div>"),
    ("k12", 8.4, 10.6, "#FFF3DC", f"<div id='cta' class='{CAP}' style='font-size:120px;color:#EA580C'>Try it →</div>"),
]
shorts_html = "".join(
    f"<div id='{sid}' class='sc absolute inset-0 flex flex-col items-center justify-center' data-a='{a}' data-b='{b}' style='background:{bg};display:none'>{body}</div>"
    for sid, a, b, bg, body in scenes
) + "<div id='flash' class='absolute inset-0' style='background:#fff;opacity:0'></div><div id='prog' class='absolute left-0 top-0' style='height:10px;background:#EA580C'></div>"
shorts = {
    "id": "SHORTS-high-tempo",
    "text": "",
    "duration": 10,
    "image": {
        "type": "html_tailwind",
        "html": f"{FONT}<div id='root' class='t relative overflow-hidden' style='width:{VW}px;height:{VH}px;background:#000'>{shorts_html}</div>",
        "script": HELPERS + """
var SC = Array.prototype.slice.call(document.querySelectorAll('.sc'));
var WORDS = document.querySelectorAll('.w'), CMD = 'npx mulmoterminal';
// transition INTO each scene: whip-h, whip-v, flash, glitch, pop, zoom-through
var IN = { k1: 'whip-h', k2: 'whip-h', k3: 'flash', k4: 'whip-v', k5: 'glitch', k6: 'pop', k7: 'pop', k8: 'pop', k9: 'whip-v', k10: 'zoom', k11: 'glitch', k12: 'whip-h' };
function render(frame, total, fps) {
  var t = frame / fps;
  $('prog').style.width = (t / 10 * 100) + '%';
  var flash = 0;
  SC.forEach(function (el) {
    var a = +el.dataset.a, b = +el.dataset.b;
    if (t < a || t >= b) { el.style.display = 'none'; return; }
    el.style.display = 'flex';
    var k = t - a, local = (t - a) / (b - a), kind = IN[el.id];
    var tr = '', fl = '';
    var punch = 1 + local * 0.12;                               // every shot slowly pushes in
    if (kind === 'whip-h' && k < 0.12) { var w = 1 - eout(k / 0.12); tr += 'translateX(' + w * 720 + 'px) skewX(' + w * -20 + 'deg)'; fl = 'blur(' + w * 30 + 'px)'; }
    if (kind === 'whip-v' && k < 0.12) { var v = 1 - eout(k / 0.12); tr += 'translateY(' + v * 1280 + 'px)'; fl = 'blur(' + v * 30 + 'px)'; }
    if (kind === 'flash' && k < 0.1) flash = 1 - k / 0.1;
    if (kind === 'pop') punch *= 0.6 + eback(clamp01(k / 0.18)) * 0.4;
    if (kind === 'glitch' && k < 0.2) { var gx = (rnd(frame) - 0.5) * 40; tr += 'translateX(' + gx + 'px)'; fl = 'drop-shadow(10px 0 0 rgba(255,0,60,.9)) drop-shadow(-10px 0 0 rgba(0,230,255,.9))'; }
    if (kind === 'zoom' && k < 0.25) { var z = 1 - eout(k / 0.25); punch *= 1 + z * 3; fl = 'blur(' + z * 25 + 'px)'; }
    if (el.id === 'k0') tr += 'translate(' + (rnd(frame) - 0.5) * 24 + 'px,' + (rnd(frame + 3) - 0.5) * 24 + 'px)';
    el.style.transform = tr + ' scale(' + punch + ')';
    el.style.filter = fl;
  });
  $('flash').style.opacity = flash;
  $('n6').textContent = Math.min(6, 1 + Math.floor(P(t, 1.7, 2.0) * 6));
  WORDS.forEach(function (w, i) { var p = P(t, 4.75 + i * 0.2, 4.9 + i * 0.2); w.style.opacity = p > 0 ? 1 : 0; w.style.transform = 'scale(' + (0.5 + eback(p) * 0.5) + ')'; });
  $('bell').style.transform = 'rotate(' + Math.sin(t * 40) * 18 * Math.exp(-P(t, 4.6, 5.6) * 3) + 'deg)';
  $('sweep').style.left = (-200 + P(t, 6.1, 6.7) * 1100) + 'px';
  $('cmd').textContent = CMD.substring(0, Math.floor(P(t, 7.15, 8.0) * CMD.length));
  $('cur').style.opacity = Math.floor(t * 3) % 2 ? 1 : 0;
  $('cta').style.transform = 'scale(' + (1 + Math.sin(t * 8) * 0.05) + ')';
}
""",
        "animation": {"fps": 30},
    },
}


def deck(title, w, h, beats):
    return {
        "$mulmocast": {"version": "1.1"},
        "canvasSize": {"width": w, "height": h},
        "title": title,
        "description": "Showcase of higher-expression motion patterns seen in Claude Opus 5.5 posts on X (2026-09). Silent, fixed-duration beats.",
        "lang": "en",
        "speechParams": {"speakers": {"Presenter": {"displayName": {"en": "Presenter"}, "voiceId": "Kore", "isDefault": True, "provider": "gemini", "model": "gemini-2.5-pro-preview-tts"}}},
        "beats": beats,
    }


(HERE / "opus55-motion-showcase.json").write_text(json.dumps(deck("Opus 5.5 motion showcase — levels 2-3", W, H, [kinetic, parallax, liquid, aefx, particles, shader, city, zoom]), ensure_ascii=False, indent=2) + "\n")
(HERE / "opus55-motion-shorts.json").write_text(json.dumps(deck("Opus 5.5 motion showcase — high-tempo Shorts", VW, VH, [shorts]), ensure_ascii=False, indent=2) + "\n")
print("ok")
