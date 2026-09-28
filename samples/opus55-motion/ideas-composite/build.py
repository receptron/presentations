"""Idea gallery — compositing & formats.

Five silent beats (text "", fixed duration) that show mulmocast users what an html_tailwind
beat can host besides slides: real footage under code-drawn annotations, a reference clip
next to its code recreation, keynote-style icon choreography, a hand-written Lottie, and an
8-bit scene on a pixel canvas. Every motion is a pure function of the frame number.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
# relative src attributes are resolved against this script's folder by mulmocast (html_tailwind)
FOOTAGE = "../../../mulmoterminal/clips/first-run-assets/07-grid.mp4"
W, H = 1280, 720

HELPERS = """
function clamp01(x) { return Math.max(0, Math.min(1, x)); }
function P(t, a, b) { return clamp01((t - a) / (b - a)); }
function eio(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function eout(x) { return 1 - Math.pow(1 - x, 3); }
function eback(x) { var c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }
function rnd(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
function $(id) { return document.getElementById(id); }
// Seek a <video> and resolve once that exact frame is decoded.
function seekTo(v, t) {
  return new Promise(function (res) {
    function go() {
      if (Math.abs(v.currentTime - t) < 0.0005) return res();
      v.addEventListener('seeked', function h() { v.removeEventListener('seeked', h); res(); });
      v.currentTime = t;
    }
    if (v.readyState >= 2) go(); else v.addEventListener('loadeddata', go, { once: true });
  });
}
"""

FONT = "<style>.t{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif}.m{font-family:Menlo,monospace}</style>"


def beat(label, html, script, duration, bg="#000"):
    return {
        "id": label,
        "text": "",
        "duration": duration,
        "image": {
            "type": "html_tailwind",
            "html": f"{FONT}<div class='t relative overflow-hidden' style='width:{W}px;height:{H}px;background:{bg}'>{html}</div>",
            "script": HELPERS + script,
            "animation": {"fps": 30},
        },
    }


# ------------------------------------------------------------------ 1. footage overlay
# Footage layout (1280x720 source): cell 1 = top-left, cell 2 = top-right, launcher = bottom-left
# until ~3.5 s of video time, when a third agent cell replaces it. Video plays at 0.76x.
overlay = beat("C1-footage-overlay", f"""
<div id='wrap' class='absolute inset-0' style='transform-origin:50% 50%'>
  <video id='v' src='{FOOTAGE}' muted playsinline preload='auto' class='absolute inset-0' style='width:1280px;height:720px'></video>
</div>
<div class='absolute inset-0' style='background:radial-gradient(ellipse at center,rgba(0,0,0,0) 55%,rgba(0,0,0,.55) 100%)'></div>
<div id='dim' class='absolute inset-0' style='background:#000;opacity:0'></div>
<svg class='absolute inset-0' width='1280' height='720' style='overflow:visible'>
  <defs><filter id='gl'><feGaussianBlur stdDeviation='3' result='b'/><feMerge><feMergeNode in='b'/><feMergeNode in='SourceGraphic'/></feMerge></filter>
    <marker id='ah' markerWidth='12' markerHeight='12' refX='6' refY='6' orient='auto'><path d='M0,0 L12,6 L0,12 z' fill='#FACC15'/></marker></defs>
  <rect id='b1' x='10' y='10' width='620' height='360' rx='10' fill='none' stroke='#22D3EE' stroke-width='4' filter='url(#gl)' pathLength='100' stroke-dasharray='100' stroke-dashoffset='100'/>
  <rect id='b2' x='650' y='10' width='620' height='360' rx='10' fill='none' stroke='#A78BFA' stroke-width='4' filter='url(#gl)' pathLength='100' stroke-dasharray='100' stroke-dashoffset='100'/>
  <rect id='b3' x='10' y='382' width='620' height='326' rx='10' fill='none' stroke='#FACC15' stroke-width='5' filter='url(#gl)' pathLength='100' stroke-dasharray='100' stroke-dashoffset='100'/>
  <rect id='src' x='690' y='276' width='220' height='30' rx='4' fill='none' stroke='#F472B6' stroke-width='2' stroke-dasharray='6 5' opacity='0'/>
  <line id='lead' x1='800' y1='306' x2='960' y2='440' stroke='#F472B6' stroke-width='2' opacity='0'/>
  <path id='arr' d='M 960 610 C 860 640, 720 600, 650 560' fill='none' stroke='#FACC15' stroke-width='5' stroke-linecap='round' marker-end='url(#ah)' pathLength='100' stroke-dasharray='100' stroke-dashoffset='100'/>
  <circle id='pulse' cx='320' cy='545' r='0' fill='none' stroke='#FACC15' stroke-width='6' opacity='0'/>
</svg>
<div id='loupe' class='absolute overflow-hidden rounded-full' style='left:830px;top:440px;width:260px;height:260px;border:5px solid #F472B6;box-shadow:0 0 30px rgba(244,114,182,.6),0 20px 40px rgba(0,0,0,.6);opacity:0;background:#000'>
  <canvas id='lc' width='260' height='260' class='absolute inset-0'></canvas>
</div>
<div id='l1' class='absolute px-4 py-1 rounded-md font-bold text-lg' style='left:22px;top:334px;background:#22D3EE;color:#062028;opacity:0'>SESSION 1 · acme-web</div>
<div id='l2' class='absolute px-4 py-1 rounded-md font-bold text-lg' style='left:662px;top:334px;background:#A78BFA;color:#1a1033;opacity:0'>SESSION 2 · orders-page</div>
<div id='l4' class='absolute px-4 py-1 rounded-md font-bold text-lg' style='left:1100px;top:560px;background:#F472B6;color:#330a1f;opacity:0'>×2.6</div>
<div id='l3' class='absolute px-5 py-2 rounded-md font-extrabold text-2xl' style='left:975px;top:585px;background:#FACC15;color:#1f1a00;opacity:0'>AGENT 3 JOINS</div>
<div class='absolute m text-lg font-bold flex items-center gap-2' style='right:26px;top:18px;color:#fff;text-shadow:0 1px 4px #000'><span id='rec' style='color:#EF4444'>●</span><span id='tc'>00:00:00:00</span></div>
<div id='cnt' class='absolute m font-bold px-4 py-2 rounded-md' style='right:26px;bottom:22px;background:rgba(0,0,0,.7);color:#fff;font-size:22px'>AGENTS <span id='cn' style='color:#FACC15'>2</span></div>
<div class='absolute' style='left:18px;top:18px;width:40px;height:40px;border-left:3px solid #fff;border-top:3px solid #fff;opacity:.8'></div>
<div class='absolute' style='right:18px;bottom:70px;width:40px;height:40px;border-right:3px solid #fff;border-bottom:3px solid #fff;opacity:.8'></div>
""", """
var v = $('v'), lc = $('lc').getContext('2d');
var RATE = 0.76, EVT = 3.5 / 0.76;                 // third cell appears at 3.5 s of footage
var Z = 2.6, RX = 800, RY = 291, LR = 130;          // loupe zoom and the source point it magnifies
function draw(id, a, b) { $(id).setAttribute('stroke-dashoffset', 100 * (1 - eio(P(t, a, b)))); }
function chip(id, a) { var p = eout(P(t, a, a + 0.35)); $(id).style.opacity = p; $(id).style.transform = 'translateX(' + (1 - p) * -30 + 'px)'; }
var t = 0;
function render(frame, total, fps) {
  t = frame / fps;
  var vt = Math.min(7.6, t * RATE);
  var out = P(t, 8.8, 9.6);                        // everything clears at the end
  $('wrap').style.transform = 'scale(' + (1 + 0.05 * eio(P(t, 0, 10))) + ')';
  draw('b1', 0.5, 1.2); chip('l1', 1.0);
  draw('b2', 1.6, 2.3); chip('l2', 2.1);
  // loupe: pops in, follows nothing (the footage is static there), leaves before the event
  var lp = eback(P(t, 2.6, 3.0)) * (1 - P(t, 4.1, 4.4));
  $('loupe').style.opacity = clamp01(lp); $('loupe').style.transform = 'scale(' + Math.max(0, lp) + ')';
  $('src').setAttribute('opacity', clamp01(lp)); $('lead').setAttribute('opacity', clamp01(lp));
  $('l4').style.opacity = clamp01(lp);
  // event: pulse ring, box, arrow, label, counter
  var pr = P(t, EVT, EVT + 0.8);
  $('pulse').setAttribute('r', eout(pr) * 260); $('pulse').setAttribute('opacity', pr > 0 && pr < 1 ? 1 - pr : 0);
  draw('b3', EVT + 0.2, EVT + 0.9);
  $('arr').setAttribute('stroke-dashoffset', 100 * (1 - eio(P(t, EVT + 0.7, EVT + 1.3))));
  var l3 = eback(P(t, EVT + 1.1, EVT + 1.5)); $('l3').style.opacity = clamp01(l3); $('l3').style.transform = 'scale(' + Math.max(0, l3) + ')';
  $('cn').textContent = t >= EVT + 0.2 ? '3' : '2';
  $('cnt').style.transform = 'scale(' + (1 + 0.3 * Math.exp(-Math.max(0, t - EVT - 0.2) * 6) * (t >= EVT + 0.2 ? 1 : 0)) + ')';
  // dim the rest of the frame while the new cell is being pointed at
  $('dim').style.opacity = 0.35 * P(t, EVT + 0.2, EVT + 0.8) * (1 - out);
  ['b1', 'b2', 'b3'].forEach(function (id) { $(id).setAttribute('opacity', 1 - out); });
  $('arr').setAttribute('opacity', t >= EVT + 0.7 ? 1 - out : 0);   // hide the arrowhead marker until the stroke starts
  ['l1', 'l2', 'l3'].forEach(function (id) { $(id).style.opacity = parseFloat($(id).style.opacity) * (1 - out); });
  // timecode + blinking record dot
  var f = frame % 30, s = Math.floor(t);
  $('tc').textContent = '00:00:' + (s < 10 ? '0' : '') + s + ':' + (f < 10 ? '0' : '') + f;
  $('rec').style.opacity = Math.floor(t * 2) % 2 ? 0.25 : 1;
  // loupe: copy the magnified region out of the same decoded frame (a second <video> never painted)
  return seekTo(v, vt).then(function () {
    var src = LR / Z;
    lc.drawImage(v, RX - src, RY - src, src * 2, src * 2, 0, 0, 260, 260);
  });
}
""", 10)

# ------------------------------------------------------------------ 2. reference vs recreation
BOX_W, BOX_H = 587, 330            # 16:9 panel, 0.4586 of the 1280x720 footage
BX = (W - BOX_W) // 2
lines = "".join(f"<div class='ln' style='height:5px;border-radius:2px;margin:5px 0;background:{c};width:0'></div>" for c in ["#9CA3AF", "#FDE68A", "#9CA3AF", "#86EFAC", "#9CA3AF", "#9CA3AF", "#FCA5A5", "#9CA3AF", "#9CA3AF", "#86EFAC"])


def cell(cid, x, y, w, h, title):
    return (f"<div id='{cid}' class='absolute rounded overflow-hidden' style='left:{x}px;top:{y}px;width:{w}px;height:{h}px;background:#0f1320;border:1px solid #2a3350'>"
            f"<div class='px-2 text-[9px] font-bold flex items-center gap-1' style='height:14px;background:#14532d;color:#bbf7d0'><span style='width:6px;height:6px;border-radius:3px;background:#4ade80'></span>{title}</div>"
            f"<div class='px-2 pt-1'><div class='flex gap-1 items-center mb-1'><div style='width:18px;height:14px;background:#f472b6;border-radius:2px'></div><div style='height:6px;width:90px;background:#e5e7eb;border-radius:2px'></div></div>{lines}</div></div>")


recre = beat("C2-reference-vs-recreation", f"""
<div class='absolute inset-x-0 top-0' style='height:360px;background:#0b0d12'></div>
<div class='absolute inset-x-0 bottom-0' style='height:360px;background:#11151f'></div>
<div class='absolute left-8 top-6 font-extrabold tracking-[0.25em] text-sm' style='color:#94a3b8'>REFERENCE<br><span class='m font-normal tracking-normal text-xs'>screen recording · 07-grid.mp4</span></div>
<div class='absolute left-8 font-extrabold tracking-[0.25em] text-sm' style='top:386px;color:#FACC15'>RECREATED IN CODE<br><span class='m font-normal tracking-normal text-xs' style='color:#a3a3a3'>div + render(frame) · no pixels copied</span></div>
<div class='absolute rounded-lg overflow-hidden' style='left:{BX}px;top:15px;width:{BOX_W}px;height:{BOX_H}px;box-shadow:0 10px 30px rgba(0,0,0,.6)'>
  <video id='v' src='{FOOTAGE}' muted playsinline preload='auto' style='width:{BOX_W}px;height:{BOX_H}px'></video>
</div>
<div id='rc' class='absolute rounded-lg overflow-hidden' style='left:{BX}px;top:375px;width:{BOX_W}px;height:{BOX_H}px;background:#0a0d18;box-shadow:0 10px 30px rgba(0,0,0,.6)'>
  {cell('c1', 2, 2, 290, 168, 'acme-web')}
  {cell('c2', 295, 2, 290, 168, 'orders-page')}
  <div id='lau' class='absolute rounded' style='left:28px;top:180px;width:262px;height:136px;background:#141a2e;border:1px solid #2a3350'>
    <div class='flex gap-1 justify-center pt-2'>{''.join(f"<span class='px-1 text-[8px] rounded' style='background:{'#334155' if i == 0 else 'transparent'};color:#cbd5e1'>{n}</span>" for i, n in enumerate(['Claude', 'Codex', 'Antigravity', 'Grok', 'Muse', 'Shell']))}</div>
    <div class='mx-3 mt-3 text-[8px]' style='color:#94a3b8'>WORKING DIRECTORY</div>
    <div class='mx-3 mt-1 rounded' style='height:14px;border:1px solid #475569'></div>
    <div id='bars' class='mx-3 mt-2'>{''.join("<div class='lb' style='height:4px;margin:4px 0;background:#334155;border-radius:2px;width:0'></div>" for _ in range(4))}</div>
    <div class='mx-auto mt-2 rounded-full text-[8px] text-center' style='width:40px;background:#14532d;color:#bbf7d0'>Shell</div>
  </div>
  {cell('c3', 2, 173, 290, 155, 'pricing')}
</div>
<div class='absolute m text-xs' style='right:34px;top:26px;color:#94a3b8'>video <span id='vt'>0.00</span>s</div>
<div class='absolute m text-xs' style='right:34px;top:386px;color:#FACC15'>frame <span id='fr'>0</span></div>
<div id='sync' class='absolute m text-xs px-3 py-1 rounded-full' style='right:34px;top:345px;background:#1f2937;color:#86efac'>● in sync</div>
""", """
var v = $('v');
var V0 = 1.6, RATE = 0.75, EVT = 3.5;              // video time of the third cell's arrival
var L1 = document.querySelectorAll('#c1 .ln'), L2 = document.querySelectorAll('#c2 .ln'), L3 = document.querySelectorAll('#c3 .ln'), LB = document.querySelectorAll('#lau .lb');
function grow(list, start, speed) {                  // terminal output: one line every 1/speed s
  list.forEach(function (el, i) { var p = eout(P(vt, start + i / speed, start + i / speed + 0.25)); el.style.width = (40 + (i * 37) % 55) * p + '%'; });
}
var vt = 0;
function render(frame, total, fps) {
  var t = frame / fps; vt = V0 + t * RATE;
  grow(L1, 0, 1.6); grow(L2, 0.4, 1.4);
  LB.forEach(function (el, i) { el.style.width = (i === 0 ? 70 : 45 + i * 12) * eout(P(vt, 1.9 + i * 0.12, 2.3 + i * 0.12)) + '%'; });
  var sw = P(vt, EVT - 0.05, EVT + 0.25);
  $('lau').style.opacity = 1 - sw; $('lau').style.transform = 'scale(' + (1 - 0.08 * sw) + ')';
  var pop = eback(P(vt, EVT - 0.05, EVT + 0.3));
  $('c3').style.opacity = clamp01(pop * 1.5); $('c3').style.transform = 'scale(' + (0.85 + 0.15 * pop) + ')';
  grow(L3, EVT + 0.2, 1.8);
  $('vt').textContent = vt.toFixed(2); $('fr').textContent = frame;
  return seekTo(v, vt);
}
""", 8)

# ------------------------------------------------------------------ 3. icon choreography
ICONS = [
    # name, gradient, inner svg (stroked, 100x100 viewBox)
    ("pencil", "#FF9F0A,#FF375F", "<path d='M28 72 L66 34 L74 42 L36 80 L26 82 Z' fill='none' stroke='#fff' stroke-width='6' stroke-linejoin='round'/><path d='M60 40 L68 48' stroke='#fff' stroke-width='6'/>"),
    ("ruler", "#30D158,#0A84FF", "<rect x='20' y='40' width='60' height='22' rx='3' fill='none' stroke='#fff' stroke-width='6' transform='rotate(-35 50 50)'/><path d='M36 58 l4 -6 M46 51 l4 -6 M56 44 l4 -6' stroke='#fff' stroke-width='4' transform='rotate(0)'/>"),
    ("brush", "#BF5AF2,#5E5CE6", "<path d='M70 22 C60 34 50 46 44 56' stroke='#fff' stroke-width='7' stroke-linecap='round' fill='none'/><path d='M44 56 C34 56 28 64 30 76 C40 76 50 70 50 60 Z' fill='#fff'/>"),
    ("magnifier", "#64D2FF,#0A84FF", "<circle cx='44' cy='44' r='18' fill='none' stroke='#fff' stroke-width='7'/><path d='M57 57 L76 76' stroke='#fff' stroke-width='8' stroke-linecap='round'/>"),
    ("scissors", "#FF453A,#FF9F0A", "<circle cx='34' cy='68' r='9' fill='none' stroke='#fff' stroke-width='6'/><circle cx='66' cy='68' r='9' fill='none' stroke='#fff' stroke-width='6'/><path d='M40 60 L70 24 M60 60 L30 24' stroke='#fff' stroke-width='6' stroke-linecap='round'/>"),
    ("compass", "#FFD60A,#FF9F0A", "<circle cx='50' cy='50' r='26' fill='none' stroke='#fff' stroke-width='6'/><path d='M50 30 L58 50 L50 70 L42 50 Z' fill='#fff'/>"),
]
tiles = "".join(
    f"<div class='tile absolute' data-i='{i}' style='left:0;top:0;width:140px;height:140px;border-radius:34px;background:linear-gradient(145deg,{g});"
    f"box-shadow:0 18px 40px rgba(0,0,0,.18),0 4px 10px rgba(0,0,0,.08);display:flex;align-items:center;justify-content:center'>"
    f"<svg class='ic' width='96' height='96' viewBox='0 0 100 100'>{svg}</svg></div>"
    for i, (n, g, svg) in enumerate(ICONS)
)
# Morph source/target silhouettes (filled), sampled to equal point counts at load.
PENCIL_SIL = "M24 78 L30 60 L64 26 Q70 20 76 26 Q82 32 76 38 L42 72 Z"
BRUSH_SIL = "M72 18 Q80 22 76 30 L56 54 Q60 68 48 78 Q36 86 22 82 Q28 74 28 64 Q30 52 44 50 L66 22 Q68 18 72 18 Z"
icons = beat("C3-icon-choreography", f"""
<div class='absolute inset-0' style='background:radial-gradient(ellipse at 50% 40%,#ffffff,#f2f2f7 70%)'></div>
<div id='stage' class='absolute inset-0'>{tiles}</div>
<svg width='0' height='0' style='position:absolute'><path id='ps' d='{PENCIL_SIL}'/><path id='pb' d='{BRUSH_SIL}'/></svg>
<div id='mt' class='absolute' style='left:0;top:0;width:140px;height:140px;border-radius:34px;opacity:0;box-shadow:0 18px 40px rgba(0,0,0,.18);display:flex;align-items:center;justify-content:center'>
  <svg width='96' height='96' viewBox='0 0 100 100'><polygon id='mp' fill='#fff'/></svg></div>
<div id='ttl' class='absolute inset-x-0 text-center font-semibold' style='top:600px;font-size:44px;letter-spacing:-1px;color:#1d1d1f;opacity:0'>Tools, <span style='background:linear-gradient(90deg,#FF375F,#BF5AF2,#0A84FF);-webkit-background-clip:text;color:transparent'>reimagined.</span></div>
""", """
var T = Array.prototype.slice.call(document.querySelectorAll('.tile'));
var N = T.length, CX = 640, CY = 330;
function lerp(a, b, p) { return a + (b - a) * p; }
// entry arcs: each starts off-screen and swings in along a quadratic curve
var START = [[-300, -200], [1580, -150], [-250, 900], [1550, 850], [640, -350], [640, 1000]];
var CTRL = [[200, 650], [1100, 650], [300, 0], [1000, 20], [100, 300], [1200, 330]];
function grid(i) { var c = i % 3, r = Math.floor(i / 3); return [CX + (c - 1) * 190, CY - 95 + r * 190]; }
function arc(i, p) { var s = START[i], c = CTRL[i], e = [CX + (i - 2.5) * 16, CY + (i - 2.5) * -6], q = 1 - p;
  return [q * q * s[0] + 2 * q * p * c[0] + p * p * e[0], q * q * s[1] + 2 * q * p * c[1] + p * p * e[1]]; }
function sampleSil(id, n) { var el = $(id), L = el.getTotalLength(), out = [];
  for (var k = 0; k < n; k++) { var pt = el.getPointAtLength(L * k / n); out.push([pt.x, pt.y]); } return out; }
var SP = sampleSil('ps', 90), SB = sampleSil('pb', 90);
function render(frame, total, fps) {
  var t = frame / fps;
  T.forEach(function (el, i) {
    var x, y, rot = 0, sc = 1, z = 10;
    var a = P(t, 0.2 + i * 0.22, 1.3 + i * 0.22);                  // fly in
    var ap = arc(i, eio(a)); x = ap[0]; y = ap[1]; rot = (1 - eio(a)) * (i % 2 ? 180 : -180) + (i - 2.5) * 4;
    var o = eio(P(t, 3.2, 3.9));                                     // spread into an orbit
    var ang = (i / N) * Math.PI * 2 + Math.max(0, t - 3.2) * 1.1;
    var ox = CX + Math.cos(ang) * 250, oy = CY + Math.sin(ang) * 110;
    x = lerp(x, ox, o); y = lerp(y, oy, o); rot = lerp(rot, 0, o);
    var depth = Math.sin(ang); sc = lerp(1, 0.78 + 0.28 * (depth + 1) / 2, o); z = Math.round(lerp(10 + i, 50 + depth * 40, o));
    var g = eback(P(t, 5.8 + i * 0.07, 6.5 + i * 0.07));              // snap into a grid
    var gp = grid(i); x = lerp(x, gp[0], g); y = lerp(y, gp[1], g); sc = lerp(sc, 1, clamp01(g)); rot = lerp(rot, 0, clamp01(g));
    if (g > 0.5) z = 10 + i;
    el.style.transform = 'translate(' + (x - 70) + 'px,' + (y - 70) + 'px) rotate(' + rot + 'deg) scale(' + sc + ')';
    el.style.zIndex = z;
    el.style.opacity = a > 0 ? 1 : 0;
  });
  // morph: the pencil tile becomes a brush — silhouette points interpolate, gradient crossfades
  var m = eio(P(t, 7.2, 8.4)), mt = $('mt'), g0 = grid(0);
  var on = t >= 7.1;
  mt.style.opacity = on ? 1 : 0; T[0].style.opacity = on ? 0 : T[0].style.opacity;
  mt.style.transform = 'translate(' + (g0[0] - 70) + 'px,' + (g0[1] - 70 - Math.sin(m * Math.PI) * 30) + 'px) rotate(' + Math.sin(m * Math.PI) * 12 + 'deg) scale(' + (1 + Math.sin(m * Math.PI) * 0.15) + ')';
  mt.style.background = 'linear-gradient(145deg,' + (m < 0.5 ? '#FF9F0A,#FF375F' : '#BF5AF2,#5E5CE6') + ')';
  mt.style.filter = 'hue-rotate(' + (m < 0.5 ? m * 2 * -60 : (1 - m) * 2 * 60) + 'deg)';
  $('mp').setAttribute('points', SP.map(function (p, k) { var q = SB[k]; return lerp(p[0], q[0], m).toFixed(2) + ',' + lerp(p[1], q[1], m).toFixed(2); }).join(' '));
  var tt = eout(P(t, 8.6, 9.3));
  $('ttl').style.opacity = tt; $('ttl').style.transform = 'translateY(' + (1 - tt) * 20 + 'px)';
}
""", 10, bg="#f2f2f7")

# ------------------------------------------------------------------ 4. hand-written Lottie
def kf(t, s, ease=(0.33, 0.67)):
    return {"t": t, "s": s, "i": {"x": [ease[1]], "y": [1]}, "o": {"x": [ease[0]], "y": [0]}}


def prop(v):
    return {"a": 0, "k": v}


def anim(*keys):
    return {"a": 1, "k": list(keys)}


def tr(p=(0, 0), s=(100, 100), r=0, o=100):
    return {"ty": "tr", "p": prop(list(p)), "a": prop([0, 0]), "s": prop(list(s)), "r": prop(r), "o": prop(o)}


def layer(ind, name, shapes, ks, ip=0, op=180):
    return {"ddd": 0, "ind": ind, "ty": 4, "nm": name, "sr": 1, "ip": ip, "op": op, "st": 0, "bm": 0, "ks": ks, "shapes": shapes}


def ks(p, s=prop([100, 100, 100]), r=prop(0), o=prop(100)):
    return {"o": o, "r": r, "p": p, "a": prop([0, 0, 0]), "s": s}


def color(hexs):
    h = hexs.lstrip("#")
    return [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)] + [1]


CXL, CYL = 640, 330
L_layers = []
# 1 ring drawn by a trim path, then slowly rotating
L_layers.append(layer(1, "ring", [{"ty": "gr", "it": [
    {"ty": "el", "p": prop([0, 0]), "s": prop([300, 300])},
    {"ty": "tm", "s": prop(0), "e": anim(kf(0, [0]), kf(40, [100])), "o": prop(0), "m": 1},
    {"ty": "st", "c": prop(color("#6366F1")), "o": prop(100), "w": prop(18), "lc": 2, "lj": 2},
    tr()]}], ks(prop([CXL, CYL, 0]), r=anim(kf(0, [-90]), kf(179, [270], (0.2, 0.8))))))
# 2 filled disc popping with overshoot
L_layers.append(layer(2, "disc", [{"ty": "gr", "it": [
    {"ty": "el", "p": prop([0, 0]), "s": prop([240, 240])},
    {"ty": "fl", "c": prop(color("#22C55E")), "o": prop(100)}, tr()]}],
    ks(prop([CXL, CYL, 0]), s=anim(kf(30, [0, 0, 100]), kf(44, [115, 115, 100]), kf(52, [95, 95, 100]), kf(58, [100, 100, 100])))))
# 3 check mark drawn by trim path
L_layers.append(layer(3, "check", [{"ty": "gr", "it": [
    {"ty": "sh", "ks": prop({"i": [[0, 0], [0, 0], [0, 0]], "o": [[0, 0], [0, 0], [0, 0]], "v": [[-60, 0], [-15, 45], [65, -45]], "c": False})},
    {"ty": "tm", "s": prop(0), "e": anim(kf(50, [0]), kf(70, [100])), "o": prop(0), "m": 1},
    {"ty": "st", "c": prop(color("#FFFFFF")), "o": prop(100), "w": prop(22), "lc": 2, "lj": 2}, tr()]}],
    ks(prop([CXL, CYL, 0]))))
# 4 three bars bouncing below (position keyframes with easing)
for k in range(3):
    x = CXL - 70 + k * 70
    L_layers.append(layer(4 + k, f"bar{k}", [{"ty": "gr", "it": [
        {"ty": "rc", "p": prop([0, 0]), "s": prop([40, 40]), "r": prop(12)},
        {"ty": "fl", "c": prop(color(["#F59E0B", "#EC4899", "#06B6D4"][k])), "o": prop(100)}, tr()]}],
        ks(anim(*[kf(f, [x, CYL + 250 - (60 if (i % 2) else 0), 0], (0.4, 0.6)) for i, f in enumerate(range(70 + k * 6, 180, 14))]),
           s=anim(kf(66 + k * 6, [0, 0, 100]), kf(76 + k * 6, [100, 100, 100])))))
# 7-14 confetti shards flying out of the disc
for k in range(8):
    import math
    a = k / 8 * math.tau + 0.3
    dx, dy = math.cos(a) * 330, math.sin(a) * 230
    L_layers.append(layer(7 + k, f"confetti{k}", [{"ty": "gr", "it": [
        {"ty": "rc", "p": prop([0, 0]), "s": prop([22, 10]), "r": prop(3)},
        {"ty": "fl", "c": prop(color(["#6366F1", "#22C55E", "#F59E0B", "#EC4899"][k % 4])), "o": prop(100)}, tr()]}],
        ks(anim(kf(44, [CXL, CYL, 0], (0.1, 0.4)), kf(90, [CXL + dx, CYL + dy, 0])),
           r=anim(kf(44, [0]), kf(90, [360 * (1 if k % 2 else -1)])),
           o=anim(kf(44, [100]), kf(80, [100]), kf(96, [0])),
           s=anim(kf(40, [0, 0, 100]), kf(46, [100, 100, 100]))), ip=40))
LOTTIE = {"v": "5.7.4", "fr": 30, "ip": 0, "op": 180, "w": W, "h": H, "nm": "mulmo-lottie", "ddd": 0, "assets": [], "layers": list(reversed(L_layers))}
lottie_json = json.dumps(LOTTIE, separators=(",", ":"))
snippet = json.dumps({"ty": "tm", "e": {"a": 1, "k": [{"t": 0, "s": [0]}, {"t": 40, "s": [100]}]}}, separators=(",", ":"))
lottie = beat("C4-lottie-layers", f"""
<script src='https://cdn.jsdelivr.net/npm/lottie-web@5.12.2/build/player/lottie.min.js'></script>
<div class='absolute inset-0' style='background:#0f172a'></div>
<div id='lt' class='absolute inset-0'></div>
<div class='absolute left-8 top-7 font-bold text-white text-2xl'>Lottie inside a beat</div>
<div class='absolute left-8 top-16 m text-sm' style='color:#94a3b8'>{len(L_layers)} shape layers · trim paths · eased keyframes · editable vector</div>
<div class='absolute m text-xs rounded-lg px-4 py-3' style='right:28px;top:26px;width:360px;background:#1e293b;color:#a5b4fc;line-height:1.5'>
  <div style='color:#64748b'>// ring layer, trim path end</div><div style='word-break:break-all'>{snippet}</div></div>
<div class='absolute m text-sm px-3 py-1 rounded-full' style='right:28px;bottom:24px;background:#1e293b;color:#e2e8f0'>frame <span id='fn'>000</span> / 180 · goToAndStop</div>
<div id='tl' class='absolute' style='left:28px;right:28px;bottom:10px;height:4px;background:#1e293b;border-radius:2px'><div id='th' style='height:4px;width:0;background:#6366F1;border-radius:2px'></div></div>
""", """
var anim = lottie.loadAnimation({ container: $('lt'), renderer: 'svg', loop: false, autoplay: false, animationData: """ + lottie_json + """ });
function render(frame, total, fps) {
  anim.goToAndStop(Math.min(179, frame), true);
  $('fn').textContent = ('00' + Math.min(180, frame)).slice(-3);
  $('th').style.width = Math.min(100, frame / 179 * 100) + '%';
}
""", 6)

# ------------------------------------------------------------------ 5. retro 8-bit
retro = beat("C5-retro-8bit", """
<div class='absolute inset-0' style='background:#000'></div>
<canvas id='cv' width='256' height='240' class='absolute' style='left:256px;top:0;width:768px;height:720px;image-rendering:pixelated'></canvas>
<div class='absolute' style='left:256px;top:0;width:768px;height:720px;background:repeating-linear-gradient(0deg,rgba(0,0,0,.18) 0 1px,transparent 1px 3px);pointer-events:none'></div>
<div class='absolute' style='left:256px;top:0;width:768px;height:720px;box-shadow:inset 0 0 120px rgba(0,0,0,.55)'></div>
""", r"""
var cx = $('cv').getContext('2d');
cx.imageSmoothingEnabled = false;
// 12-colour night palette
var PAL = { k: '#000000', w: '#FCFCFC', n1: '#0C1030', n2: '#1C2468', n3: '#3050A0', m: '#FCE8A8', h: '#243058', H: '#34447C',
            wa: '#08204C', wl: '#3C78C8', y: '#FCBC3C', o: '#E45C10', g: '#A4A4B8', G: '#5C5C74', c: '#7C4C1C', C: '#B47C3C', t: '#38A898' };
var F = {
 A:['01110','10001','10001','11111','10001','10001','10001'], B:['11110','10001','10001','11110','10001','10001','11110'], C:['01110','10001','10000','10000','10000','10001','01110'],
 D:['11110','10001','10001','10001','10001','10001','11110'], E:['11111','10000','10000','11110','10000','10000','11111'],
 F:['11111','10000','10000','11110','10000','10000','10000'], G:['01110','10001','10000','10111','10001','10001','01111'],
 H:['10001','10001','10001','11111','10001','10001','10001'], I:['01110','00100','00100','00100','00100','00100','01110'],
 L:['10000','10000','10000','10000','10000','10000','11111'], M:['10001','11011','10101','10101','10001','10001','10001'],
 N:['10001','11001','10101','10011','10001','10001','10001'], O:['01110','10001','10001','10001','10001','10001','01110'],
 R:['11110','10001','10001','11110','10100','10010','10001'], S:['01111','10000','10000','01110','00001','00001','11110'],
 T:['11111','00100','00100','00100','00100','00100','00100'], U:['10001','10001','10001','10001','10001','10001','01110'],
 W:['10001','10001','10001','10101','10101','11011','10001'],
 '0':['01110','10011','10101','10101','11001','10001','01110'], '1':['00100','01100','00100','00100','00100','00100','01110'],
 '2':['01110','10001','00001','00110','01000','10000','11111'], '5':['11111','10000','11110','00001','00001','10001','01110'],
 '!':['00100','00100','00100','00100','00100','00000','00100'], '.':['00000','00000','00000','00000','00000','01100','01100'],
 '+':['00000','00100','00100','11111','00100','00100','00000'], ' ':['00000','00000','00000','00000','00000','00000','00000'],
 'v':['00000','11111','11111','01110','01110','00100','00000']
};
function text(str, x, y, col) {
  cx.fillStyle = col;
  for (var i = 0; i < str.length; i++) { var g = F[str[i]] || F[' '];
    for (var r = 0; r < 7; r++) for (var c = 0; c < 5; c++) if (g[r][c] === '1') cx.fillRect(x + i * 6 + c, y + r, 1, 1); }
}
function sprite(rows, map, x, y) {
  for (var r = 0; r < rows.length; r++) for (var c = 0; c < rows[r].length; c++) { var ch = rows[r][c];
    if (ch !== '.') { cx.fillStyle = PAL[map[ch]]; cx.fillRect(x + c, y + r, 1, 1); } }
}
// original hero: small hooded traveller carrying a lantern (a = hood, b = cloak, f = face, e = eye, l = lantern)
var HMAP = { a: 't', b: 'g', f: 'm', e: 'k', l: 'y', d: 'G', s: 'C' };
var HERO = [
 ['....aaaa......','...aaaaaa.....','..aaffffaa....','..afefefaa....','..aaffffaa....','...aaaaaa.....','..bbbbbbbb....','.bbbbbbbbbd...','.bbbbbbbbbd.l.','.bbbbbbbbd..l.','..bbbbbbb..lll','..bbbbbbb..lll','...ss..ss.....','...ss...ss....'],
 ['....aaaa......','...aaaaaa.....','..aaffffaa....','..afefefaa....','..aaffffaa....','...aaaaaa.....','..bbbbbbbb....','.bbbbbbbbbd...','.bbbbbbbbbd.l.','.bbbbbbbbd..l.','..bbbbbbb..lll','..bbbbbbb..lll','....ss.ss.....','...ss..ss.....']
];
var STARS = []; for (var i = 0; i < 40; i++) STARS.push([Math.floor(rnd(i) * 256), Math.floor(rnd(i + 50) * 110), rnd(i + 99)]);
function wrap(x, span) { return ((x % span) + span) % span; }
function house(x, y, w, h, lit, t) {
  cx.fillStyle = PAL.h; cx.fillRect(x, y, w, h);
  cx.fillStyle = PAL.H; for (var i = 0; i < w / 2 + 1; i++) cx.fillRect(x - 1 + i, y - i, w + 2 - 2 * i, 1);
  if (lit) { cx.fillStyle = (Math.floor(t * 2 + x) % 5) ? PAL.y : PAL.o; cx.fillRect(x + 3, y + 5, 3, 3); cx.fillRect(x + w - 6, y + 5, 3, 3); }
}
function lighthouse(x, t) {
  cx.fillStyle = PAL.g; cx.fillRect(x, 96, 12, 76);
  cx.fillStyle = PAL.o; cx.fillRect(x, 110, 12, 6); cx.fillRect(x, 134, 12, 6); cx.fillRect(x, 158, 12, 6);
  cx.fillStyle = PAL.G; cx.fillRect(x - 2, 88, 16, 8); cx.fillStyle = PAL.y; cx.fillRect(x + 3, 90, 6, 5);
  // sweeping beam: a wedge of pale pixels
  var a = t * 1.4, len = 150;
  cx.fillStyle = 'rgba(252,232,168,0.18)';
  for (var r = 6; r < len; r += 2) { var spread = r * 0.18, bx = x + 6 + Math.cos(a) * r, by = 92 + Math.sin(a) * r * 0.25;
    cx.fillRect(Math.floor(bx - spread / 2), Math.floor(by - spread / 4), Math.ceil(spread), Math.max(1, Math.ceil(spread / 2))); }
}
function chest(x, y, open) {
  cx.fillStyle = PAL.c; cx.fillRect(x, y + 5, 16, 9); cx.fillStyle = PAL.C; cx.fillRect(x + 1, y + 6, 14, 1);
  cx.fillStyle = PAL.y; cx.fillRect(x + 7, y + 8, 2, 3);
  if (open) { cx.fillStyle = PAL.c; cx.fillRect(x, y - 3, 16, 3); cx.fillStyle = PAL.y; cx.fillRect(x + 2, y + 2, 12, 3); }
  else { cx.fillStyle = PAL.C; cx.fillRect(x, y + 1, 16, 4); }
}
var MSG1 = 'HELLO FROM MULMOCAST!', MSG2 = 'THIS SCENE IS ALL CODE.';
var STOP = 4.6, OPEN = 2.6;
function render(frame, total, fps) {
  var t = frame / fps;
  var walkT = Math.min(t, OPEN - 0.3) + Math.max(0, Math.min(t, STOP) - (OPEN + 0.5));
  var scroll = Math.floor(walkT * 55);
  // night sky, stars twinkle, moon
  cx.fillStyle = PAL.n1; cx.fillRect(0, 0, 256, 240);
  cx.fillStyle = PAL.n2; cx.fillRect(0, 70, 256, 60);
  STARS.forEach(function (s) { if ((Math.floor(t * 3 + s[2] * 10) % 4) !== 0) { cx.fillStyle = PAL.w; cx.fillRect(wrap(s[0] - Math.floor(scroll * 0.05), 256), s[1], 1, 1); } });
  cx.fillStyle = PAL.m; for (var yy = -7; yy <= 7; yy++) for (var xx = -7; xx <= 7; xx++) { if (xx * xx + yy * yy <= 49 && (xx - 4) * (xx - 4) + (yy + 2) * (yy + 2) > 36) cx.fillRect(207 + xx, 40 + yy, 1, 1); }
  // far: lighthouse on a cliff (slow parallax)
  var lx = 60 - Math.floor(scroll * 0.15);
  cx.fillStyle = PAL.n3; cx.fillRect(lx - 30, 172, 90, 20);
  lighthouse(lx + 10, t);
  // mid: town silhouettes
  for (var k = 0; k < 7; k++) { var hx = wrap(k * 52 - Math.floor(scroll * 0.45), 364) - 60; house(hx, 158 - (k % 3) * 6, 20 + (k % 2) * 8, 26 + (k % 3) * 6, k % 2 === 0, t); }
  // sea with moving highlights
  cx.fillStyle = PAL.wa; cx.fillRect(0, 186, 256, 20);
  cx.fillStyle = PAL.wl; for (var i = 0; i < 18; i++) cx.fillRect(wrap(i * 29 + Math.floor(t * 8) - Math.floor(scroll * 0.6), 256), 190 + (i % 3) * 5, 5, 1);
  // near: wooden pier planks + posts
  cx.fillStyle = PAL.c; cx.fillRect(0, 206, 256, 8);
  cx.fillStyle = PAL.C; for (var x = -(scroll % 12); x < 256; x += 12) cx.fillRect(x, 206, 11, 1);
  cx.fillStyle = PAL.k; for (var x = -(scroll % 12); x < 256; x += 12) cx.fillRect(x + 11, 206, 1, 8);
  cx.fillStyle = PAL.c; for (var x = -(scroll % 48); x < 256; x += 48) cx.fillRect(x + 4, 214, 4, 26);
  cx.fillStyle = PAL.wa; cx.fillRect(0, 214, 256, 26); cx.fillStyle = PAL.c; for (var x = -(scroll % 48); x < 256; x += 48) cx.fillRect(x + 4, 214, 4, 26);
  // chest on the pier; the traveller stops, opens it
  var chX = 232 - Math.floor((Math.min(t, OPEN - 0.3)) * 55) - Math.floor(Math.max(0, Math.min(t, STOP) - (OPEN + 0.5)) * 55);
  var opened = t >= OPEN;
  chest(chX, 192, opened);
  if (opened && t < OPEN + 1.2) {
    var sp = P(t, OPEN, OPEN + 1.2), sy = 184 - Math.floor(eout(sp) * 28);
    cx.fillStyle = PAL.m; var r = Math.floor(2 + sp * 6);
    cx.fillRect(chX + 8, sy - r, 1, r * 2 + 1); cx.fillRect(chX + 8 - r, sy, r * 2 + 1, 1);
    cx.fillStyle = PAL.w; cx.fillRect(chX + 7, sy - 1, 3, 3);
    text('+1 ITEM', chX - 12, sy - 14, PAL.y);
  }
  // hero walk cycle (frame-stepped), lantern flickers, glow halo
  var walking = t < STOP && !(t > OPEN - 0.3 && t < OPEN + 0.5);
  var fr = walking ? Math.floor(frame / 7) % 2 : 0, hx = 90, hy = 192;
  cx.fillStyle = 'rgba(252,188,60,0.12)'; var gr = 14 + (Math.floor(t * 8) % 2);
  cx.fillRect(hx + 12 - gr, hy + 10 - gr / 2, gr * 2, gr);
  sprite(HERO[fr], HMAP, hx, hy - (walking && fr ? 1 : 0));
  // HUD
  text('STAGE 01', 12, 10, PAL.w);
  text('HARBOUR', 12, 19, PAL.m);
  text('SCORE', 190, 10, PAL.w); text(('0000' + (opened ? 50 : 0) + '0').slice(-5), 190, 19, PAL.w);
  text('ITEM', 110, 10, PAL.w); text(opened ? '1' : '0', 122, 19, PAL.y);
  // dialogue box with typewriter
  if (t >= STOP + 0.2) {
    cx.fillStyle = PAL.k; cx.fillRect(16, 128, 224, 44); cx.fillStyle = PAL.w; cx.fillRect(18, 130, 220, 1); cx.fillRect(18, 169, 220, 1); cx.fillRect(18, 130, 1, 40); cx.fillRect(237, 130, 1, 40);
    var n = Math.floor((t - STOP - 0.3) * 18);
    text(MSG1.slice(0, Math.max(0, n)), 26, 138, PAL.w);
    text(MSG2.slice(0, Math.max(0, n - MSG1.length)), 26, 152, PAL.w);
    if (n > MSG1.length + MSG2.length && Math.floor(t * 3) % 2) text('v', 226, 160, PAL.w);
  }
}
""", 8)

deck = {
    "$mulmocast": {"version": "1.1"},
    "canvasSize": {"width": W, "height": H},
    "title": "mulmocast idea gallery — compositing & formats",
    "description": "Silent idea beats: code annotations over real footage, reference vs code recreation, icon choreography, a hand-written Lottie, an 8-bit pixel scene.",
    "lang": "en",
    "speechParams": {"speakers": {"Presenter": {"voiceId": "Kore", "isDefault": True, "provider": "gemini"}}},
    "beats": [overlay, recre, icons, lottie, retro],
}
(HERE / "ideas-composite.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1) + "\n")
print("ok", len(lottie_json), "bytes of lottie")
