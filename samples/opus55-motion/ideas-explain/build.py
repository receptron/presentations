"""Idea gallery — explainers. Three silent beats, everything driven in render(frame).

1. math-derivative      Manim-like: axes, curve, secant -> tangent as h -> 0, KaTeX steps
2. ocean-dive           surface to 4000 m on a log depth scale, zones, marine snow, bioluminescence
3. art-history-speedrun 40,000 years of art: the same 2,400 particles re-arrange era by era
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
W, H = 1280, 720

HELPERS = r"""
function clamp01(x) { return Math.max(0, Math.min(1, x)); }
function P(t, a, b) { return clamp01((t - a) / (b - a)); }
function eio(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function eout(x) { return 1 - Math.pow(1 - x, 3); }
function eback(x) { var c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }
function rnd(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
function lerp(a, b, p) { return a + (b - a) * p; }
function $(id) { return document.getElementById(id); }
"""


def beat(label, html, script, duration, bg):
    page = f"<div class='relative overflow-hidden' style='width:{W}px;height:{H}px;background:{bg}'>{html}</div>"
    return {"id": label, "text": "", "duration": duration,
            "image": {"type": "html_tailwind", "html": page, "script": HELPERS + script, "animation": {"fps": 30}}}


# ------------------------------------------------------------------ 1. math-derivative
TEX = {
    "title": r"f(x) = \tfrac{x^3}{3} - x",
    "f0": r"m = \frac{f(x+h) - f(x)}{h}",
    "f1": r"= \frac{\frac{(x+h)^3}{3} - (x+h) - \frac{x^3}{3} + x}{h}",
    "f2": r"= x^2 + {\color{#FC6255} xh} + {\color{#FC6255} \tfrac{h^2}{3}} - 1",
    "f3": r"\xrightarrow{\;h \to 0\;} \; x^2 - 1",
    "f4": r"f'(x) = x^2 - 1",
}
math_html = """
<link rel='stylesheet' href='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css'>
<script src='https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js'></script>
<style>.tx{position:absolute;color:#ECECEC;white-space:nowrap}.katex{font-size:1em}</style>
<svg id='plot' class='absolute' style='left:0;top:0' width='780' height='720'>
  <defs><clipPath id='clip'><rect x='30' y='40' width='720' height='660'/></clipPath></defs>
  <g id='grid' opacity='0'></g>
  <line id='ax' x1='40' y1='380' x2='740' y2='380' stroke='#BBBBBB' stroke-width='2.5' stroke-dasharray='700' stroke-dashoffset='700'/>
  <line id='ay' x1='380' y1='690' x2='380' y2='50' stroke='#BBBBBB' stroke-width='2.5' stroke-dasharray='640' stroke-dashoffset='640'/>
  <g clip-path='url(#clip)'>
    <path id='deriv' d='' stroke='#83C167' stroke-width='3' fill='none' stroke-dasharray='10 8' opacity='0.9'/>
    <path id='curve' d='' stroke='#58C4DD' stroke-width='5' fill='none' stroke-linecap='round'/>
    <line id='sec' x1='0' y1='0' x2='0' y2='0' stroke='#F9D65C' stroke-width='3.5' opacity='0'/>
  </g>
  <line id='hbar' x1='0' y1='396' x2='0' y2='396' stroke='#FC6255' stroke-width='4' opacity='0'/>
  <text id='hlab' x='0' y='428' fill='#FC6255' font-family='KaTeX_Math, serif' font-size='26' font-style='italic' opacity='0'>h</text>
  <line id='pdrop' x1='0' y1='380' x2='0' y2='380' stroke='#777' stroke-width='1.5' stroke-dasharray='4 4' opacity='0'/>
  <line id='qdrop' x1='0' y1='380' x2='0' y2='380' stroke='#777' stroke-width='1.5' stroke-dasharray='4 4' opacity='0'/>
  <circle id='pp' r='9' fill='#F9D65C' opacity='0'/>
  <circle id='qq' r='9' fill='#FC6255' opacity='0'/>
</svg>
<div id='title' class='tx' style='left:60px;top:40px;font-size:34px;opacity:0'></div>
<div id='hval' class='tx' style='left:60px;top:96px;font-size:28px;font-family:Menlo,monospace;color:#FC6255;opacity:0'></div>
<div id='f0' class='tx' style='left:800px;top:140px;font-size:34px;opacity:0'></div>
<div id='f1' class='tx' style='left:800px;top:250px;font-size:26px;opacity:0'></div>
<div id='f2' class='tx' style='left:800px;top:350px;font-size:34px;opacity:0'></div>
<div id='f3' class='tx' style='left:800px;top:440px;font-size:34px;opacity:0'></div>
<div id='fin' class='absolute' style='left:830px;top:540px;opacity:0'>
  <svg class='absolute' style='left:-24px;top:-18px' width='420' height='110'><rect id='box' x='3' y='3' width='414' height='104' rx='10' fill='none' stroke='#F9D65C' stroke-width='4' stroke-dasharray='1040' stroke-dashoffset='1040'/></svg>
  <div id='f4' class='tx' style='left:0;top:0;font-size:44px;position:relative'></div>
</div>
"""
math_js = "var TEX = " + json.dumps(TEX) + ";\n" + r"""
Object.keys(TEX).forEach(function (k) { katex.render(TEX[k], $(k === 'title' ? 'title' : k), { displayMode: false }); });
// grid lines
var grid = $('grid'), NS = 'http://www.w3.org/2000/svg';
for (var gx = -2; gx <= 2; gx++) { var l = document.createElementNS(NS, 'line'); l.setAttribute('x1', X(gx)); l.setAttribute('x2', X(gx)); l.setAttribute('y1', 50); l.setAttribute('y2', 690); l.setAttribute('stroke', '#2E3A44'); grid.appendChild(l); }
for (var gy = -3; gy <= 3; gy++) { var l2 = document.createElementNS(NS, 'line'); l2.setAttribute('y1', Y(gy)); l2.setAttribute('y2', Y(gy)); l2.setAttribute('x1', 40); l2.setAttribute('x2', 740); l2.setAttribute('stroke', '#2E3A44'); grid.appendChild(l2); }
function X(x) { return 380 + x * 130; }
function Y(y) { return 380 - y * 105; }
function f(x) { return x * x * x / 3 - x; }
function g(x) { return x * x - 1; }
function pathOf(fn, x0, x1) {
  var d = '', n = 160;
  for (var i = 0; i <= n; i++) { var x = x0 + (x1 - x0) * i / n; d += (i ? 'L' : 'M') + X(x).toFixed(1) + ' ' + Y(fn(x)).toFixed(1); }
  return d;
}
var redTerms = Array.prototype.slice.call($('f2').querySelectorAll('[style*="color"]'));
var X0 = 1.5;
function render(frame, total, fps) {
  var t = frame / fps;
  // axes + grid
  $('ax').setAttribute('stroke-dashoffset', 700 * (1 - eio(P(t, 0.1, 1.0))));
  $('ay').setAttribute('stroke-dashoffset', 640 * (1 - eio(P(t, 0.3, 1.2))));
  grid.setAttribute('opacity', 0.9 * P(t, 0.6, 1.4));
  $('title').style.opacity = P(t, 0.8, 1.4);
  // curve plots left to right
  var c = eio(P(t, 1.1, 3.0));
  $('curve').setAttribute('d', c > 0 ? pathOf(f, -2.55, -2.55 + 5.1 * c) : '');
  // secant: h shrinks 1.0 -> 0
  var hs = P(t, 4.2, 7.6), h = 1.0 * Math.pow(1 - eio(hs), 1.6) + 0.0001;
  var show = P(t, 3.1, 3.6);
  var xp = X0, xq = X0 + h, m = (f(xq) - f(xp)) / h;
  var fade = 1 - P(t, 10.4, 11.0) * 0.6;
  $('sec').setAttribute('x1', X(-3)); $('sec').setAttribute('y1', Y(f(xp) + m * (-3 - xp)));
  $('sec').setAttribute('x2', X(3)); $('sec').setAttribute('y2', Y(f(xp) + m * (3 - xp)));
  $('sec').setAttribute('opacity', show * fade);
  $('sec').setAttribute('stroke', hs >= 1 ? '#83C167' : '#F9D65C');
  $('pp').setAttribute('cx', X(xp)); $('pp').setAttribute('cy', Y(f(xp))); $('pp').setAttribute('opacity', show);
  $('qq').setAttribute('cx', X(xq)); $('qq').setAttribute('cy', Y(f(xq))); $('qq').setAttribute('opacity', show * (1 - P(t, 7.4, 7.7)));
  ['pdrop', 'qdrop'].forEach(function (id, k) {
    var xx = k ? xq : xp; var e = $(id);
    e.setAttribute('x1', X(xx)); e.setAttribute('x2', X(xx)); e.setAttribute('y2', Y(f(xx))); e.setAttribute('opacity', show * 0.9 * (1 - P(t, 7.4, 7.7)));
  });
  $('hbar').setAttribute('x1', X(xp)); $('hbar').setAttribute('x2', X(xq)); $('hbar').setAttribute('opacity', show * (1 - P(t, 7.4, 7.7)));
  $('hlab').setAttribute('x', (X(xp) + X(xq)) / 2 - 7); $('hlab').setAttribute('opacity', show * (1 - P(t, 7.0, 7.4)));
  $('hval').textContent = 'h = ' + h.toFixed(3) + '   slope = ' + m.toFixed(3);
  $('hval').style.opacity = P(t, 3.4, 3.9) * (1 - P(t, 10.4, 10.9));
  // formulas
  function up(id, a) { var p = eout(P(t, a, a + 0.5)); $(id).style.opacity = p; $(id).style.transform = 'translateY(' + (1 - p) * 18 + 'px)'; }
  up('f0', 3.3);
  $('f0').style.textShadow = hs > 0 && hs < 1 ? '0 0 18px rgba(249,214,92,.55)' : 'none';
  up('f1', 7.7); up('f2', 8.5); up('f3', 9.6);
  var kill = P(t, 9.1, 9.6);
  redTerms.forEach(function (el) { el.style.opacity = 1 - kill * 0.85; el.style.textDecoration = kill > 0.3 ? 'line-through' : 'none'; });
  // final box + derivative curve
  $('fin').style.opacity = P(t, 10.1, 10.5);
  $('box').setAttribute('stroke-dashoffset', 1040 * (1 - eio(P(t, 10.2, 11.0))));
  var dc = eio(P(t, 10.3, 11.7));
  $('deriv').setAttribute('d', dc > 0 ? pathOf(g, -2.1, -2.1 + 4.2 * dc) : '');
}
"""
math_beat = beat("math-derivative", math_html, math_js, 12, "radial-gradient(circle at 30% 40%, #1f252b, #111417 80%)")

# ------------------------------------------------------------------ 2. ocean-dive
ocean_html = """
<canvas id='cv' width='1280' height='720' class='absolute inset-0'></canvas>
<div id='zone' class='absolute' style='left:56px;top:48px;font-family:Georgia,serif;color:#E6F7FF;font-size:52px;letter-spacing:.02em;text-shadow:0 2px 12px rgba(0,30,60,.8)'></div>
<div id='zsub' class='absolute' style='left:60px;top:116px;font-family:Helvetica,Arial;color:#CDEBF7;font-size:22px;letter-spacing:.18em;text-shadow:0 2px 10px rgba(0,30,60,.9)'></div>
<div id='depth' class='absolute text-right' style='right:150px;top:318px;font-family:Menlo,monospace;color:#E6F7FF;font-size:46px;text-shadow:0 2px 12px rgba(0,30,60,.9)'></div>
"""
ocean_js = r"""
var ctx = $('cv').getContext('2d');
var ZONES = [[0, 'Sunlight zone', 'EPIPELAGIC · 0–200 m'], [200, 'Twilight zone', 'MESOPELAGIC · 200–1,000 m'],
             [1000, 'Midnight zone', 'BATHYPELAGIC · 1,000–4,000 m'], [4000, 'Abyssal zone', 'ABYSSOPELAGIC · 4,000 m +']];
var K = 520;                                   // px per unit of ln(depth + 40)
function L(d) { return Math.log(d + 40); }
function depthAt(t) { var p = eio(P(t, 0.6, 9.3)); return Math.exp(lerp(L(0), L(4000), p)) - 40; }
function yOf(dc, d) { return 360 + (L(dc) - L(d)) * K; }
function mix(a, b, p) { return [lerp(a[0], b[0], p), lerp(a[1], b[1], p), lerp(a[2], b[2], p)]; }
var STOPS = [[0, [64, 196, 240]], [60, [18, 132, 196]], [200, [8, 72, 128]], [700, [4, 34, 70]], [1500, [2, 14, 34]], [4000, [1, 4, 12]]];
function waterAt(d) {
  if (d <= 0) return STOPS[0][1];
  for (var i = 0; i < STOPS.length - 1; i++) if (d <= STOPS[i + 1][0]) return mix(STOPS[i][1], STOPS[i + 1][1], (d - STOPS[i][0]) / (STOPS[i + 1][0] - STOPS[i][0]));
  return STOPS[STOPS.length - 1][1];
}
function rgb(c, a) { return 'rgba(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ',' + (a === undefined ? 1 : a) + ')'; }
// creatures placed at fixed depths (log space)
var FISH = []; for (var i = 0; i < 26; i++) FISH.push({ d: 15 + rnd(i) * 140, x: rnd(i + 50) * 1280, sp: 30 + rnd(i + 90) * 50, s: 0.6 + rnd(i + 7) * 0.6 });
var GLOW = [];
for (var j = 0; j < 22; j++) GLOW.push({ d: 700 + rnd(j + 300) * 3300, x: 90 + rnd(j + 400) * 950, kind: j % 3, ph: rnd(j + 500) * 6, s: 0.7 + rnd(j + 600) * 0.9 });
var SNOW = []; for (var k = 0; k < 260; k++) SNOW.push({ x: rnd(k + 1000) * 1280, u: rnd(k + 2000), r: 0.8 + rnd(k + 3000) * 2 });
function jelly(x, y, s, pulse, a) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.shadowColor = 'rgba(120,255,240,' + a + ')'; ctx.shadowBlur = 30 * pulse;
  ctx.strokeStyle = 'rgba(140,255,240,' + (0.55 * a) + ')'; ctx.fillStyle = 'rgba(90,230,255,' + (0.18 * a * pulse) + ')'; ctx.lineWidth = 2;
  var bw = 34 + pulse * 6;
  ctx.beginPath(); ctx.moveTo(-bw, 0); ctx.quadraticCurveTo(0, -50 - pulse * 8, bw, 0); ctx.quadraticCurveTo(0, 12, -bw, 0); ctx.fill(); ctx.stroke();
  for (var q = -3; q <= 3; q++) { ctx.beginPath(); ctx.moveTo(q * 9, 4); for (var z = 0; z < 8; z++) ctx.lineTo(q * 9 + Math.sin(z * 0.9 + pulse * 3 + q) * 6, 4 + z * 11); ctx.stroke(); }
  ctx.restore();
}
function angler(x, y, s, pulse, a) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  ctx.fillStyle = 'rgba(30,40,60,' + (0.8 * a) + ')';
  ctx.beginPath(); ctx.ellipse(0, 0, 48, 30, 0, 0, Math.PI * 2); ctx.fill();
  ctx.beginPath(); ctx.moveTo(44, 0); ctx.lineTo(78, -22); ctx.lineTo(78, 22); ctx.fill();
  ctx.strokeStyle = 'rgba(80,100,130,' + a + ')'; ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(-30, -24); ctx.quadraticCurveTo(-40, -70, -70, -58); ctx.stroke();
  ctx.shadowColor = 'rgba(255,240,150,1)'; ctx.shadowBlur = 40 * pulse; ctx.fillStyle = 'rgba(255,245,170,' + a + ')';
  ctx.beginPath(); ctx.arc(-70, -58, 5 + pulse * 3, 0, Math.PI * 2); ctx.fill();
  ctx.restore();
}
function chain(x, y, s, tt, a) {
  ctx.save(); ctx.translate(x, y); ctx.scale(s, s);
  for (var q = 0; q < 14; q++) {
    var px = q * 16, py = Math.sin(q * 0.6 + tt * 1.5) * 14, on = 0.5 + 0.5 * Math.sin(tt * 4 - q * 0.7);
    ctx.shadowColor = 'rgba(140,120,255,1)'; ctx.shadowBlur = 18 * on; ctx.fillStyle = 'rgba(170,150,255,' + (a * (0.25 + 0.75 * on)) + ')';
    ctx.beginPath(); ctx.arc(px, py, 3.5, 0, Math.PI * 2); ctx.fill();
  }
  ctx.restore();
}
function render(frame, total, fps) {
  var t = frame / fps, d = depthAt(t);
  // water column: every screen row gets the colour of the depth it shows
  var gtop = Math.exp(L(d) - 360 / K) - 40, gbot = Math.exp(L(d) + 360 / K) - 40;
  var gr = ctx.createLinearGradient(0, 0, 0, 720);
  for (var s = 0; s <= 8; s++) { var yy = s / 8 * 720, dd = Math.exp(L(d) + (yy - 360) / K) - 40; gr.addColorStop(s / 8, rgb(waterAt(Math.max(0, dd)))); }
  ctx.fillStyle = gr; ctx.fillRect(0, 0, 1280, 720);
  // sky + surface when near the top
  var sy = yOf(0, d);
  if (sy > -40) {
    var sk = ctx.createLinearGradient(0, 0, 0, Math.max(1, sy)); sk.addColorStop(0, '#FFE8B8'); sk.addColorStop(1, '#BFE9FF');
    ctx.fillStyle = sk; ctx.beginPath(); ctx.moveTo(0, 0); ctx.lineTo(1280, 0);
    for (var wx = 1280; wx >= 0; wx -= 20) ctx.lineTo(wx, sy + Math.sin(wx * 0.02 + t * 3) * 7 + Math.sin(wx * 0.047 - t * 2) * 4);
    ctx.closePath(); ctx.fill();
  }
  // god rays, fading with depth
  var ray = clamp01(1 - d / 260);
  if (ray > 0) {
    ctx.save(); ctx.globalCompositeOperation = 'lighter';
    for (var r = 0; r < 7; r++) {
      var x0 = 120 + r * 170 + Math.sin(t * 0.7 + r) * 40, w = 50 + rnd(r) * 70;
      var rg = ctx.createLinearGradient(0, Math.max(0, sy), 0, 720); rg.addColorStop(0, 'rgba(255,255,230,' + 0.22 * ray + ')'); rg.addColorStop(1, 'rgba(255,255,230,0)');
      ctx.fillStyle = rg; ctx.beginPath(); ctx.moveTo(x0, Math.max(0, sy)); ctx.lineTo(x0 + w, Math.max(0, sy)); ctx.lineTo(x0 + w * 3 + 160, 720); ctx.lineTo(x0 + 120, 720); ctx.fill();
    }
    ctx.restore();
  }
  // zone boundary lines
  ctx.font = '18px Helvetica'; ctx.textAlign = 'left';
  [200, 1000, 4000].forEach(function (b) {
    var by = yOf(b, d); if (by < -10 || by > 730) return;
    ctx.strokeStyle = 'rgba(200,240,255,.35)'; ctx.setLineDash([10, 10]); ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(0, by); ctx.lineTo(1100, by); ctx.stroke(); ctx.setLineDash([]);
    ctx.fillStyle = 'rgba(200,240,255,.7)'; ctx.fillText(b.toLocaleString('en-US') + ' m', 20, by - 8);
  });
  // schools of fish near the surface
  FISH.forEach(function (fi, i) {
    var fy = yOf(fi.d, d); if (fy < -30 || fy > 750) return;
    var fx = ((fi.x + t * fi.sp) % 1400) - 60;
    ctx.fillStyle = 'rgba(10,40,70,.55)'; ctx.save(); ctx.translate(fx, fy + Math.sin(t * 2 + i) * 4); ctx.scale(fi.s, fi.s);
    ctx.beginPath(); ctx.ellipse(0, 0, 18, 6, 0, 0, Math.PI * 2); ctx.fill(); ctx.beginPath(); ctx.moveTo(-16, 0); ctx.lineTo(-28, -7); ctx.lineTo(-28, 7); ctx.fill(); ctx.restore();
  });
  // bioluminescence in the dark
  var dark = clamp01((d - 500) / 900);
  GLOW.forEach(function (gl, i) {
    var gy = yOf(gl.d, d); if (gy < -120 || gy > 840 || dark <= 0) return;
    var pulse = 0.5 + 0.5 * Math.sin(t * 2.4 + gl.ph);
    var gx = gl.x + Math.sin(t * 0.5 + i) * 30;
    if (gl.kind === 0) jelly(gx, gy, gl.s, pulse, dark); else if (gl.kind === 1) angler(gx, gy, gl.s, pulse, dark); else chain(gx - 100, gy, gl.s, t + gl.ph, dark);
  });
  // marine snow: fixed in depth, so it streams upward as we sink
  var snowA = clamp01((d - 80) / 300);
  ctx.fillStyle = 'rgba(230,245,255,' + (0.55 * snowA) + ')';
  SNOW.forEach(function (sn) {
    var y = ((sn.u * 720 - L(d) * K * 1.3) % 720 + 720) % 720;
    ctx.beginPath(); ctx.arc(sn.x + Math.sin(t + sn.u * 9) * 6, y, sn.r, 0, Math.PI * 2); ctx.fill();
  });
  // depth gauge on the right: ticks every 10/100/1000 m on the same log scale
  ctx.fillStyle = 'rgba(0,0,0,.25)'; ctx.fillRect(1150, 0, 130, 720);
  ctx.strokeStyle = 'rgba(220,245,255,.8)'; ctx.fillStyle = 'rgba(220,245,255,.85)'; ctx.font = '15px Menlo'; ctx.lineWidth = 1.5;
  var marks = []; for (var m = 0; m <= 100; m += 10) marks.push(m); for (m = 200; m <= 1000; m += 100) marks.push(m); for (m = 2000; m <= 5000; m += 1000) marks.push(m);
  marks.forEach(function (mk) {
    var my = yOf(mk, d); if (my < 0 || my > 720) return;
    var big = mk === 0 || mk === 100 || mk === 1000 || mk % 1000 === 0 || mk === 200 || mk === 500;
    ctx.beginPath(); ctx.moveTo(1160, my); ctx.lineTo(1160 + (big ? 28 : 14), my); ctx.stroke();
    if (big) ctx.fillText(mk.toLocaleString('en-US'), 1196, my + 5);
  });
  ctx.strokeStyle = '#FFD166'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(1140, 360); ctx.lineTo(1275, 360); ctx.stroke();
  // labels
  var z = ZONES[0]; ZONES.forEach(function (zz) { if (d >= zz[0] - 0.5) z = zz; });
  $('zone').textContent = z[1]; $('zsub').textContent = z[2];
  $('depth').textContent = Math.round(d).toLocaleString('en-US') + ' m';
}
"""
ocean_beat = beat("ocean-dive", ocean_html, ocean_js, 10, "#000")

# ------------------------------------------------------------------ 3. art-history-speedrun
art_html = """
<canvas id='cv' width='1280' height='720' class='absolute inset-0'></canvas>
<div id='year' class='absolute text-right' style='right:40px;top:30px;padding:4px 22px;border-radius:14px;background:rgba(15,12,10,.72);font-family:Georgia,serif;font-size:60px;font-weight:bold;color:#fff'></div>
<div id='plate' class='absolute' style='left:44px;bottom:44px;background:#FBF8F1;padding:14px 22px;box-shadow:0 6px 24px rgba(0,0,0,.35);min-width:340px'>
  <div id='pt' style='font-family:Georgia,serif;font-size:26px;font-weight:bold;color:#1d1d1d'></div>
  <div id='ps' style='font-family:Helvetica,Arial;font-size:15px;letter-spacing:.12em;color:#6b6b6b;margin-top:4px'></div>
</div>
<div class='absolute' style='left:430px;right:48px;bottom:58px;height:4px;background:rgba(255,255,255,.35)'></div>
<div id='mark' class='absolute' style='bottom:50px;width:20px;height:20px;border-radius:50%;background:#fff;box-shadow:0 0 12px rgba(255,255,255,.9)'></div>
"""
art_js = r"""
var ctx = $('cv').getContext('2d');
var N = 2400, GX = 60, GY = 40, CW = 1280 / GX, CH = 720 / GY;
var ERAS = [
  { y: -40000, t: 'Hand stencils', s: 'CAVE PAINTING · EL CASTILLO', bg: [58, 42, 30] },
  { y: 540, t: 'Byzantine mosaic', s: 'TESSERAE · RAVENNA', bg: [24, 18, 14] },
  { y: 1886, t: 'Pointillism', s: 'DOTS OF PURE COLOUR · SEURAT', bg: [244, 239, 226] },
  { y: 1921, t: 'De Stijl', s: 'PRIMARY COLOURS · MONDRIAN', bg: [245, 241, 230] },
  { y: 1963, t: 'Pop art', s: 'BEN-DAY DOTS · LICHTENSTEIN', bg: [255, 255, 255] },
  { y: 2026, t: 'Generative art', s: 'A FLOW FIELD · WRITTEN IN CODE', bg: [10, 10, 20] }
];
var SEG = 2.3, TR = 0.85;
function hex(h) { return [parseInt(h.substr(1, 2), 16), parseInt(h.substr(3, 2), 16), parseInt(h.substr(5, 2), 16)]; }
// ---- era states: x, y, colour, w, h, round
var ST = ERAS.map(function () { return []; });
// 0: hand stencils — spray dots around three hands, the hands stay as negative space
var HANDS = [[300, 330, 1.0, -0.25], [640, 300, 1.15, 0.05], [960, 360, 0.95, 0.3]];
function segDist(px, py, ax, ay, bx, by) { var dx = bx - ax, dy = by - ay, u = clamp01(((px - ax) * dx + (py - ay) * dy) / (dx * dx + dy * dy)); var qx = ax + u * dx - px, qy = ay + u * dy - py; return Math.sqrt(qx * qx + qy * qy); }
function inHand(px, py, hd) {
  var cx = hd[0], cy = hd[1], s = hd[2], r = hd[3];
  var lx = (px - cx) * Math.cos(-r) - (py - cy) * Math.sin(-r), ly = (px - cx) * Math.sin(-r) + (py - cy) * Math.cos(-r);
  lx /= s; ly /= s;
  if ((lx * lx) / (46 * 46) + ((ly - 20) * (ly - 20)) / (56 * 56) < 1) return true;
  var F = [[-30, -20, -52, -105], [-10, -30, -16, -128], [10, -30, 16, -124], [28, -22, 46, -98], [-40, 20, -92, -12]];
  for (var i = 0; i < F.length; i++) if (segDist(lx, ly, F[i][0], F[i][1], F[i][2], F[i][3]) < 12) return true;
  return lx > -38 && lx < 38 && ly > 50 && ly < 110;   // wrist
}
var n = 0, seed = 1;
while (n < N) {
  var hd = HANDS[n % 3], a = rnd(seed) * Math.PI * 2, rr = Math.sqrt(rnd(seed + 7)) * 190 * hd[2];
  var px = hd[0] + Math.cos(a) * rr, py = hd[1] + Math.sin(a) * rr * 0.95; seed += 13;
  if (inHand(px, py, hd)) continue;
  if (rnd(seed + 3) > 1.25 - rr / (190 * hd[2])) continue;           // denser near the hand edge
  var sh = 0.75 + rnd(seed + 5) * 0.35;
  ST[0].push({ x: px, y: py, c: [168 * sh, 62 * sh, 36 * sh], w: 3 + rnd(seed + 9) * 4, h: 0, r: 1 }); n++;
}
// 1: mosaic — tesserae on the grid, a halo and a blue disc with a star
for (var i = 0; i < N; i++) {
  var gx = i % GX, gy = Math.floor(i / GX), cx = (gx + 0.5) * CW, cy = (gy + 0.5) * CH;
  var dx = cx - 640, dy = (cy - 360) * 1.25, dd = Math.sqrt(dx * dx + dy * dy), ang = Math.atan2(dy, dx);
  var col;
  if (gx < 2 || gx > GX - 3 || gy < 2 || gy > GY - 3) col = [120, 26, 30];
  else if (dd < 110 + 40 * Math.pow(Math.abs(Math.cos(ang * 4)), 6)) col = dd < 40 ? [250, 245, 230] : [240, 230, 200];
  else if (dd < 230) col = [31, 78, 140];
  else if (dd < 250) col = [230, 190, 60];
  else col = [201, 162, 39];
  var j = 0.85 + rnd(i + 77) * 0.25;
  ST[1].push({ x: cx, y: cy, c: [col[0] * j, col[1] * j, col[2] * j], w: CW * 0.82, h: CH * 0.8, r: 0 });
}
// 2: pointillism — dots whose colour comes from a landscape
function land(x, y) {
  var sun = Math.hypot(x - 930, y - 190);
  if (sun < 70) return [255, 200, 90];
  if (y < 300) { var p = y / 300; return [lerp(150, 250, p), lerp(190, 200, p), lerp(240, 190, p)]; }
  if (y < 450) { var ref = Math.abs(x - 930) < 60 + (y - 300) * 0.3 && rnd(Math.floor(x / 9) + Math.floor(y / 9) * 131) > 0.4; return ref ? [255, 210, 120] : [lerp(90, 40, (y - 300) / 150), 140, 200]; }
  var tree = Math.hypot(x - 260, y - 470) < 110 || Math.hypot(x - 380, y - 440) < 90;
  if (tree) return [30, 90, 50];
  return [lerp(120, 60, (y - 450) / 270), lerp(170, 120, (y - 450) / 270), 70];
}
for (i = 0; i < N; i++) {
  var x = rnd(i + 5000) * 1280, y = rnd(i + 9000) * 720, cc = land(x, y), k = rnd(i + 12000);
  if (k > 0.82) cc = [cc[2], cc[0], cc[1]];             // a few complementary dots, as Seurat did
  ST[2].push({ x: x, y: y, c: [cc[0] * (0.9 + k * 0.2), cc[1] * (0.9 + k * 0.2), cc[2] * (0.9 + k * 0.2)], w: 9 + rnd(i + 15000) * 5, h: 0, r: 1 });
}
// 3: Mondrian — grid squares that tile flat colour; black bars drawn on top
var MV = [0, 300, 820, 1100, 1280], MH = [0, 220, 520, 720];
function mcol(x, y) {
  if (x < 300 && y < 220) return hex('#D62E2E');
  if (x > 820 && y > 520) return hex('#1F4FA3');
  if (x > 1100 && y < 220) return hex('#F2C230');
  if (x < 300 && y > 520) return hex('#F2C230');
  return hex('#F4F0E6');
}
for (i = 0; i < N; i++) { var mx = (i % GX + 0.5) * CW, my = (Math.floor(i / GX) + 0.5) * CH; ST[3].push({ x: mx, y: my, c: mcol(mx, my), w: CW + 0.6, h: CH + 0.6, r: 0 }); }
// 4: pop art — Ben-Day dots sampled from an off-screen comic burst
var off = document.createElement('canvas'); off.width = 1280; off.height = 720; var ox = off.getContext('2d');
ox.fillStyle = '#7CCBEA'; ox.fillRect(0, 0, 1280, 720);
ox.beginPath(); for (var q = 0; q < 28; q++) { var aa = q / 28 * Math.PI * 2, rad = q % 2 ? 190 : 330; ox.lineTo(640 + Math.cos(aa) * rad * 1.4, 360 + Math.sin(aa) * rad); } ox.closePath();
ox.fillStyle = '#FFD60A'; ox.fill(); ox.lineWidth = 26; ox.strokeStyle = '#111'; ox.stroke();
ox.font = '900 190px Impact, Helvetica'; ox.textAlign = 'center'; ox.textBaseline = 'middle'; ox.fillStyle = '#E63946'; ox.fillText('WOW!', 640, 370);
ox.lineWidth = 10; ox.strokeText('WOW!', 640, 370);
var img = ox.getImageData(0, 0, 1280, 720).data;
for (i = 0; i < N; i++) {
  var row = Math.floor(i / GX), px2 = (i % GX + 0.5 + (row % 2) * 0.5) * CW, py2 = (row + 0.5) * CH;
  var o = (Math.min(719, py2 | 0) * 1280 + Math.min(1279, px2 | 0)) * 4, c2 = [img[o], img[o + 1], img[o + 2]];
  var dark = c2[0] + c2[1] + c2[2] < 120, bgd = c2[2] > 200 && c2[0] < 150;
  ST[4].push({ x: px2, y: py2, c: c2, w: dark ? CW * 1.05 : bgd ? CW * (0.45 + 0.25 * (py2 / 720)) : CW * 0.92, h: 0, r: 1 });
}
// 5: generative — each particle starts where it was and flows along a field
for (i = 0; i < N; i++) ST[5].push({ x: ST[4][i].x, y: ST[4][i].y, c: [0, 0, 0], w: 3, h: 0, r: 1 });
function field(x, y, tt) { return Math.sin(x * 0.0045 + tt * 0.25) * 2.2 + Math.cos(y * 0.006 - tt * 0.2) * 2.2 + Math.sin((x + y) * 0.002) ; }
function hue(i, y) { var h = (y / 720) * 140 + 180 + (i % 7) * 6; return 'hsl(' + h + ',85%,' + (55 + (i % 5) * 4) + '%)'; }
// rock texture for the cave
var rock = document.createElement('canvas'); rock.width = 1280; rock.height = 720; var rc = rock.getContext('2d');
rc.fillStyle = 'rgb(150,112,78)'; rc.fillRect(0, 0, 1280, 720);
for (i = 0; i < 1400; i++) { var rx = rnd(i + 20000) * 1280, ry = rnd(i + 21000) * 720, rs = 10 + rnd(i + 22000) * 90, sh2 = rnd(i + 23000); rc.fillStyle = 'rgba(' + (sh2 > 0.5 ? '190,150,110' : '90,64,44') + ',' + (0.05 + rnd(i + 24000) * 0.08) + ')'; rc.beginPath(); rc.ellipse(rx, ry, rs, rs * 0.6, rnd(i + 25000) * 3, 0, Math.PI * 2); rc.fill(); }
for (var hh = 0; hh < 3; hh++) {
  var H0 = HANDS[hh], placed = 0, sd = 90000 + hh * 50000;
  while (placed < 14000) {
    var ma = rnd(sd) * Math.PI * 2, mr = Math.pow(rnd(sd + 1), 0.7) * 175 * H0[2], mx2 = H0[0] + Math.cos(ma) * mr, my2 = H0[1] + Math.sin(ma) * mr; sd += 3;
    if (inHand(mx2, my2, H0)) continue;
    rc.fillStyle = 'rgba(' + (140 + rnd(sd + 2) * 40 | 0) + ',42,26,' + (0.10 + (1 - mr / (175 * H0[2])) * 0.35) + ')';
    rc.beginPath(); rc.arc(mx2, my2, 0.8 + rnd(sd + 5) * 2.2, 0, Math.PI * 2); rc.fill(); placed++;
  }
}
// a dense pointillist under-layer so the landscape reads; the 2,400 moving dots sit on top
var pb = document.createElement('canvas'); pb.width = 1280; pb.height = 720; var pc = pb.getContext('2d');
pc.fillStyle = '#F4EFE2'; pc.fillRect(0, 0, 1280, 720);
for (i = 0; i < 26000; i++) { var qx = rnd(i + 40000) * 1280, qy = rnd(i + 70000) * 720, qc = land(qx, qy), qk = rnd(i + 99000); if (qk > 0.85) qc = [qc[2], qc[0], qc[1]]; pc.fillStyle = 'rgb(' + (qc[0] | 0) + ',' + (qc[1] | 0) + ',' + (qc[2] | 0) + ')'; pc.beginPath(); pc.arc(qx, qy, 3 + rnd(i + 120000) * 2.5, 0, Math.PI * 2); pc.fill(); }
function fmtYear(y) { y = Math.round(y); return y < 0 ? Math.abs(y).toLocaleString('en-US') + ' BCE' : y < 1000 ? y + ' CE' : String(y); }
function yearPos(y) { return y < 0 ? lerp(0, 0.25, (y + 40000) / 40000) : y < 1800 ? lerp(0.25, 0.45, y / 1800) : lerp(0.45, 1, (y - 1800) / 226); }
function render(frame, total, fps) {
  var t = frame / fps;
  var k = Math.min(ERAS.length - 1, Math.floor(t / SEG)), local = t - k * SEG;
  var p = k === 0 ? 1 : eio(clamp01(local / TR));
  var A = ST[Math.max(0, k - 1)], B = ST[k];
  var bg = ERAS[k].bg, bgp = ERAS[Math.max(0, k - 1)].bg;
  ctx.fillStyle = 'rgb(' + (lerp(bgp[0], bg[0], p) | 0) + ',' + (lerp(bgp[1], bg[1], p) | 0) + ',' + (lerp(bgp[2], bg[2], p) | 0) + ')';
  ctx.fillRect(0, 0, 1280, 720);
  var rockA = k === 0 ? 1 : k === 1 ? 1 - p : 0;
  if (rockA > 0) { ctx.globalAlpha = rockA; ctx.drawImage(rock, 0, 0); ctx.globalAlpha = 1; }
  var pbA = k === 2 ? p : k === 3 ? 1 - p : 0;
  if (pbA > 0) { ctx.globalAlpha = pbA; ctx.drawImage(pb, 0, 0); ctx.globalAlpha = 1; }
  if (k === 5) {
    // flow field: integrate each particle's path from the era start, draw the tail
    var steps = Math.min(90, Math.floor(local * 34)), tail = 26;
    ctx.lineCap = 'round'; ctx.lineWidth = 2;
    for (var i = 0; i < N; i++) {
      var x = ST[4][i].x, y = ST[4][i].y, pts = [[x, y]];
      for (var s = 0; s < steps; s++) { var a = field(x, y, s / 30); x += Math.cos(a) * 3.2; y += Math.sin(a) * 3.2; pts.push([x, y]); }
      var from = Math.max(0, pts.length - tail);
      ctx.strokeStyle = hue(i, ST[4][i].y); ctx.globalAlpha = 0.85;
      ctx.beginPath(); ctx.moveTo(pts[from][0], pts[from][1]); for (var q = from + 1; q < pts.length; q++) ctx.lineTo(pts[q][0], pts[q][1]);
      if (pts.length === 1) ctx.lineTo(x + 0.1, y);
      ctx.stroke();
    }
    ctx.globalAlpha = 1;
  } else {
    for (var i2 = 0; i2 < N; i2++) {
      var a0 = A[i2], b0 = B[i2], d = rnd(i2 + 777) * 0.35, pp = k === 0 ? 1 : eio(clamp01((local - d * TR) / (TR * (1 - 0.35) + 0.001)));
      var sw = Math.sin(pp * Math.PI) * 60 * (rnd(i2 + 55) - 0.5);
      var x2 = lerp(a0.x, b0.x, pp) + sw, y2 = lerp(a0.y, b0.y, pp) - sw * 0.6;
      var c = [lerp(a0.c[0], b0.c[0], pp), lerp(a0.c[1], b0.c[1], pp), lerp(a0.c[2], b0.c[2], pp)];
      var w = lerp(a0.w, b0.w, pp), h = lerp(a0.h || a0.w, b0.h || b0.w, pp), r = lerp(a0.r, b0.r, pp);
      // a little life during the hold
      if (k === 0) { ctx.globalAlpha = 0.55 + 0.35 * rnd(i2 + 31); }
      ctx.fillStyle = 'rgb(' + (c[0] | 0) + ',' + (c[1] | 0) + ',' + (c[2] | 0) + ')';
      if (r > 0.5) { ctx.beginPath(); ctx.arc(x2, y2, Math.max(0.5, w / 2), 0, Math.PI * 2); ctx.fill(); }
      else ctx.fillRect(x2 - w / 2, y2 - h / 2, w, h);
      ctx.globalAlpha = 1;
    }
  }
  if (k === 3) {                                           // Mondrian's black bars grow in
    var g = eio(P(local, TR * 0.7, TR + 0.5));
    ctx.fillStyle = '#111';
    [300, 820, 1100].forEach(function (vx, i) { ctx.fillRect(vx - 8, 0, 16, 720 * clamp01(g * 1.3 - i * 0.15)); });
    [220, 520].forEach(function (hy, i) { ctx.fillRect(0, hy - 8, 1280 * clamp01(g * 1.3 - i * 0.2), 16); });
  }
  // year counter and plate
  var yA = ERAS[Math.max(0, k - 1)].y, yB = ERAS[k].y, yr = k === 0 ? yB : lerp(yA, yB, eio(clamp01(local / TR)));
  $('year').textContent = fmtYear(yr);
  var plateIn = eout(P(local, TR * 0.6, TR + 0.2));
  $('pt').textContent = ERAS[k].t; $('ps').textContent = ERAS[k].s;
  $('plate').style.opacity = k === 0 ? P(t, 0.2, 0.7) : plateIn;
  $('plate').style.transform = 'translateY(' + (1 - (k === 0 ? 1 : plateIn)) * 16 + 'px)';
  $('mark').style.left = (430 + (1280 - 48 - 430) * yearPos(yr) - 10) + 'px';
}
"""
art_beat = beat("art-history-speedrun", art_html, art_js, 14, "#000")

deck = {
    "$mulmocast": {"version": "1.1"},
    "canvasSize": {"width": W, "height": H},
    "title": "Idea gallery — explainers",
    "description": "Silent idea beats for mulmocast users: a Manim-like derivative, a log-scale ocean dive, and 40,000 years of art re-drawn by the same particles.",
    "lang": "en",
    "speechParams": {"speakers": {"Presenter": {"displayName": {"en": "Presenter"}, "voiceId": "Kore", "isDefault": True, "provider": "gemini", "model": "gemini-2.5-pro-preview-tts"}}},
    "beats": [math_beat, ocean_beat, art_beat],
}
(HERE / "ideas-explain.json").write_text(json.dumps(deck, ensure_ascii=False, indent=2) + "\n")
print("ok")
