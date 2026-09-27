"""Idea deck: characters and stories.

- cafe-*: two characters talk; each mouth is driven by the loudness of its own TTS line.
  Two passes: `mulmo audio` makes the lines, mouth.py measures them into mouth.json, this script bakes
  the numbers in, then `mulmo movie` renders.
- battle-map: an ink-wash map (Nano Banana Pro) with units, brush arrows and a calligraphy cut-in.
- latte-battle: fighting-game VS screen and HUD with the same two characters.
- paper-collage: three paper-cut layers (Nano Banana Pro) composited with parallax, on-twos jitter.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
mouth = json.load(open(HERE / "mouth.json")) if (HERE / "mouth.json").exists() else {}

HELPERS = """
function clamp01(x) { return Math.max(0, Math.min(1, x)); }
function P(t, a, b) { return clamp01((t - a) / (b - a)); }
function eio(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function eout(x) { return 1 - Math.pow(1 - x, 3); }
function eback(x) { var c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(x - 1, 3) + c1 * Math.pow(x - 1, 2); }
function rnd(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
function $(id) { return document.getElementById(id); }
"""
FONT = "<style>.t{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif}.g{font-family:Georgia,serif}.min{font-family:'Hiragino Mincho ProN','Yu Mincho',serif}</style>"


def page(inner, bg):
    return f"{FONT}<div class='t relative overflow-hidden' style='width:1280px;height:720px;background:{bg}'>{inner}</div>"


# ---------------------------------------------------------------- characters (SVG, shared by cafe + battle)
def person(pid, hair, skin, shirt, flip=False):
    s = -1 if flip else 1
    return f"""
<g id='{pid}'>
  <g id='{pid}-body'><path d='M-110 260 Q-100 120 0 110 Q100 120 110 260 Z' fill='{shirt}'/><rect x='-22' y='82' width='44' height='40' rx='14' fill='{skin}'/></g>
  <g id='{pid}-head'>
    <ellipse cx='0' cy='0' rx='88' ry='98' fill='{skin}'/>
    <path d='M-92 -8 Q-96 -110 0 -112 Q96 -110 92 -8 Q{70 * s} -70 {-10 * s} -64 Q{-60 * s} -60 -92 -8 Z' fill='{hair}'/>
    <g id='{pid}-eyes'><ellipse cx='-32' cy='8' rx='9' ry='12' fill='#2a1d17'/><ellipse cx='32' cy='8' rx='9' ry='12' fill='#2a1d17'/></g>
    <path id='{pid}-brow' d='M-46 -18 Q-32 -26 -18 -18 M18 -18 Q32 -26 46 -18' stroke='#2a1d17' stroke-width='5' fill='none' stroke-linecap='round'/>
    <ellipse cx='-54' cy='36' rx='14' ry='8' fill='#f28b82' opacity='.45'/><ellipse cx='54' cy='36' rx='14' ry='8' fill='#f28b82' opacity='.45'/>
    <ellipse id='{pid}-mouth' cx='0' cy='50' rx='16' ry='3' fill='#6b2b2b'/>
  </g>
</g>"""


LINES = [
    ("Mika", "Morning, Ren! The usual? A flat white, extra hot?"),
    ("Ren", "You remembered again. How do you keep track of everyone?"),
    ("Mika", "I don't. I just write it down, and the notes remember for me."),
    ("Ren", "Then I'll have the usual. And a story for your notes."),
]

CAFE_BG = (
    "<svg class='absolute inset-0' width='1280' height='720'>"
    "<rect width='1280' height='720' fill='#f4e3c9'/>"
    "<rect x='80' y='60' width='420' height='260' rx='12' fill='#bfe0f2'/><rect x='80' y='60' width='420' height='260' rx='12' fill='none' stroke='#8a5a3b' stroke-width='14'/>"
    "<line x1='290' y1='60' x2='290' y2='320' stroke='#8a5a3b' stroke-width='10'/>"
    + "".join(f"<rect x='{760 + i * 90}' y='{110 + (i % 2) * 8}' width='60' height='{80 - (i % 3) * 10}' rx='8' fill='{c}'/>" for i, c in enumerate(['#c0392b', '#2e86ab', '#f4a261', '#6a994e', '#8e7dbe']))
    + "<rect x='720' y='200' width='480' height='14' fill='#8a5a3b'/><rect x='720' y='90' width='480' height='14' fill='#8a5a3b'/>"
    "<rect x='0' y='520' width='1280' height='200' fill='#8a5a3b'/><rect x='0' y='510' width='1280' height='22' fill='#a8734f'/>"
    "</svg>"
)


def cafe_beat(i, speaker, line):
    env = mouth.get(f"cafe-{i}", [])
    shot = ["wide", "ren", "mika", "wide"][i]
    return {
        "id": f"cafe-{i}", "speaker": speaker, "text": line,
        "image": {"type": "html_tailwind", "animation": {"fps": 30},
                  "html": page(f"""
<div id='cam' class='absolute inset-0' style='transform-origin:640px 360px'>
  {CAFE_BG}
  <svg class='absolute inset-0' width='1280' height='720'>
    <g transform='translate(330 330)'>{person('mika', '#3b2a20', '#f6d2b8', '#e76f51')}</g>
    <g transform='translate(950 330)'>{person('ren', '#1d2b3a', '#e9bf9b', '#2a9d8f', flip=True)}</g>
    <rect x='0' y='560' width='1280' height='160' fill='#6f4a33'/><rect x='560' y='520' width='70' height='46' rx='8' fill='#fff'/><path d='M630 530 q22 6 0 26' stroke='#fff' stroke-width='8' fill='none'/>
  </svg>
</div>
<div class='absolute left-0 right-0 flex justify-center' style='bottom:34px'>
  <div class='px-7 py-3 rounded-2xl text-3xl' style='background:rgba(20,14,10,.78);color:#fff;max-width:1100px'><b style='color:{"#ffb4a2" if speaker == "Mika" else "#8fe3d8"}'>{speaker}</b>&nbsp;&nbsp;<span id='sub'></span></div>
</div>""", "#f4e3c9"),
                  "script": HELPERS + f"""
var ENV = {json.dumps(env)}, LINE = {json.dumps(line)}, SPK = {json.dumps(speaker.lower())}, SHOT = {json.dumps(shot)};
function env(t) {{ var k = Math.floor(t * 30); return k < ENV.length ? ENV[k] : 0; }}
function face(pid, t, talking) {{
  var a = talking ? env(t) : 0;
  var m = $(pid + '-mouth'); m.setAttribute('ry', 3 + a * 20); m.setAttribute('rx', 16 + a * 6 - (a > 0.6 ? 4 : 0));
  var blink = (Math.floor(t * 30) + (pid === 'mika' ? 0 : 40)) % 110 < 4;
  $(pid + '-eyes').setAttribute('transform', blink ? 'translate(0 8) scale(1 0.12) translate(0 -8)' : '');
  var bob = talking ? a * 6 : Math.max(0, Math.sin(t * 2.4 + (pid === 'mika' ? 0 : 1))) * 4;   // listener nods
  $(pid + '-head').setAttribute('transform', 'translate(0 ' + (-bob) + ') rotate(' + (talking ? Math.sin(t * 3) * 2 : (pid === 'mika' ? 3 : -3)) + ')');
  $(pid + '-brow').setAttribute('transform', 'translate(0 ' + (-a * 6) + ')');
}}
function render(frame, total, fps) {{
  var t = frame / fps, dur = total / fps;
  face('mika', t, SPK === 'mika'); face('ren', t, SPK === 'ren');
  $('sub').textContent = LINE.substring(0, Math.ceil(P(t, 0, Math.max(0.5, dur - 1.0)) * LINE.length));
  // camera: wide two-shot, or a slow push toward whoever the shot is on
  var z = 1, x = 0, p = eio(P(t, 0, dur));
  if (SHOT === 'mika') {{ z = 1.35 + p * 0.1; x = 310; }}
  if (SHOT === 'ren') {{ z = 1.35 + p * 0.1; x = -310; }}
  if (SHOT === 'wide') {{ z = 1 + p * 0.04; }}
  $('cam').style.transform = 'translateX(' + (x * (z - 1) / 0.35) + 'px) scale(' + z + ')';
}}"""}}


# ---------------------------------------------------------------- battle map
UNITS = ([("w", i, "#1d3557") for i in range(5)] + [("e", i, "#b3261e") for i in range(5)])
battle = {
    "id": "battle-map", "text": "", "duration": 9,
    "image": {"type": "html_tailwind", "animation": {"fps": 30},
              "html": page(f"""
<div id='map' class='absolute' style='left:0;top:0;width:1280px;height:720px;transform-origin:0 0'>
  <img src='assets/map.png' style='position:absolute;inset:0;width:1280px;height:720px;object-fit:cover'>
  <svg class='absolute inset-0' width='1280' height='720'>
    <path id='arW' d='M250 520 C 380 470, 520 420, 620 385' stroke='#1d3557' stroke-width='16' fill='none' stroke-linecap='round' stroke-dasharray='520' stroke-dashoffset='520' opacity='.85'/>
    <path id='arE' d='M1040 300 C 900 330, 760 360, 680 380' stroke='#b3261e' stroke-width='16' fill='none' stroke-linecap='round' stroke-dasharray='420' stroke-dashoffset='420' opacity='.85'/>
    {''.join(f"<g id='u{s}{i}'><rect x='-16' y='-10' width='32' height='20' fill='{c}' stroke='#f5efe0' stroke-width='3'/><line x1='-16' y1='-10' x2='-16' y2='-40' stroke='#2b2b2b' stroke-width='3'/><path d='M-16 -40 L8 -34 L-16 -28 Z' fill='{c}'/></g>" for s, i, c in UNITS)}
  </svg>
</div>
<div id='band' class='absolute left-0 right-0' style='top:250px;height:220px;background:#111;transform:scaleY(0)'></div>
<div id='ink' class='absolute inset-0'></div>
<div id='cut' class='absolute left-0 right-0 flex items-center justify-center min font-black' style='top:250px;height:220px;font-size:190px;color:#f5efe0;letter-spacing:.2em;clip-path:inset(0 100% 0 0)'>決戦</div>
<div id='cap' class='absolute left-0 right-0 text-center min text-4xl' style='bottom:40px;color:#111;opacity:0'>西軍、橋を渡る</div>
<div class='absolute min text-2xl' style='left:40px;top:30px;color:#1d3557'>西軍</div><div class='absolute min text-2xl' style='right:40px;top:30px;color:#b3261e'>東軍</div>""", "#e9e1cf"),
              "script": HELPERS + """
function along(path, u) { var el = $(path), L = el.getTotalLength(), p = el.getPointAtLength(L * clamp01(u)); return [p.x, p.y]; }
var inkDots = []; for (var i = 0; i < 26; i++) inkDots.push([640 + (rnd(i) - .5) * 900, 360 + (rnd(i + 5) - .5) * 300, 4 + rnd(i + 9) * 26]);
function render(frame, total, fps) {
  var t = frame / fps;
  // camera: wide establishing, then a push onto the bridge
  var p = eio(P(t, 0.5, 4.5)), z = 1 + p * 0.9, fx = 640 + (620 - 640) * p, fy = 360 + (385 - 360) * p;
  $('map').style.transform = 'translate(' + (640 - fx * z) + 'px,' + (360 - fy * z) + 'px) scale(' + z + ')';
  $('arW').setAttribute('stroke-dashoffset', 520 * (1 - eout(P(t, 1.0, 3.2))));
  $('arE').setAttribute('stroke-dashoffset', 420 * (1 - eout(P(t, 1.6, 3.6))));
  for (var i = 0; i < 5; i++) {
    var a = along('arW', P(t, 1.0 + i * 0.12, 3.6 + i * 0.12) * (0.88 - i * 0.06)), b = along('arE', P(t, 1.6 + i * 0.12, 4.0 + i * 0.12) * (0.88 - i * 0.06));
    var jit = Math.floor(t * 12) % 2 ? 1.5 : -1.5;
    $('uw' + i).setAttribute('transform', 'translate(' + (a[0] - 30 - i * 10) + ' ' + (a[1] + 30 + (i % 2) * 18 + jit) + ')');
    $('ue' + i).setAttribute('transform', 'translate(' + (b[0] + 30 + i * 10) + ' ' + (b[1] - 30 - (i % 2) * 18 - jit) + ')');
  }
  // calligraphy cut-in: band slams, brush reveal left to right, ink splatter
  var bnd = P(t, 4.8, 5.0) * (1 - P(t, 7.2, 7.5));
  $('band').style.transform = 'scaleY(' + eout(bnd) + ')';
  var rv = eout(P(t, 5.0, 5.9)) * (1 - P(t, 7.2, 7.4));
  $('cut').style.clipPath = 'inset(0 ' + (100 - rv * 100) + '% 0 0)';
  $('cut').style.transform = 'scale(' + (1.15 - 0.15 * eout(P(t, 5.0, 5.6))) + ')';
  var ink = $('ink'); ink.innerHTML = '';
  if (t > 5.0 && t < 7.3) inkDots.forEach(function (d, i) { var g = eout(P(t, 5.0 + i * 0.01, 5.3 + i * 0.01)); var e = document.createElement('div'); e.style.cssText = 'position:absolute;border-radius:50%;background:#111;left:' + d[0] + 'px;top:' + d[1] + 'px;width:' + d[2] * g + 'px;height:' + d[2] * g + 'px'; ink.appendChild(e); });
  $('cap').style.opacity = P(t, 7.5, 8.0);
}"""}}

# ---------------------------------------------------------------- latte battle (fighting-game HUD)
latte = {
    "id": "latte-battle", "text": "", "duration": 9,
    "image": {"type": "html_tailwind", "animation": {"fps": 30},
              "html": page(f"""
<div id='vs' class='absolute inset-0'>
  <div id='L' class='absolute inset-0' style='background:linear-gradient(135deg,#e76f51,#9d2f1a);clip-path:polygon(0 0,58% 0,42% 100%,0 100%)'></div>
  <div id='R' class='absolute inset-0' style='background:linear-gradient(135deg,#2a9d8f,#15525b);clip-path:polygon(58% 0,100% 0,100% 100%,42% 100%)'></div>
  <svg id='figs' class='absolute inset-0' width='1280' height='720'>
    <g id='fl' transform='translate(300 380) scale(1.25)'>{person('fm', '#3b2a20', '#f6d2b8', '#e76f51')}</g>
    <g id='fr' transform='translate(980 380) scale(1.25)'>{person('fn', '#1d2b3a', '#e9bf9b', '#2a9d8f', flip=True)}</g>
  </svg>
  <div id='nl' class='absolute font-black italic' style='left:60px;bottom:60px;font-size:96px;color:#fff;-webkit-text-stroke:4px #111'>MIKA</div>
  <div id='nr' class='absolute font-black italic' style='right:60px;top:60px;font-size:96px;color:#fff;-webkit-text-stroke:4px #111'>REN</div>
  <div id='vsT' class='absolute inset-0 flex items-center justify-center font-black italic' style='font-size:230px;color:#ffd166;-webkit-text-stroke:8px #111;text-shadow:0 0 40px #ffd166'>VS</div>
</div>
<div id='hud' class='absolute inset-0' style='opacity:0'>
  <div class='absolute' style='left:40px;top:30px;width:500px;height:34px;background:#222;border:4px solid #fff;transform:skewX(-15deg)'><div id='chipL' class='absolute inset-y-0 right-0' style='left:0;background:#ff4d4d'></div><div id='hpL' class='absolute inset-y-0 right-0' style='left:0;background:#ffd166'></div></div>
  <div class='absolute' style='right:40px;top:30px;width:500px;height:34px;background:#222;border:4px solid #fff;transform:skewX(15deg)'><div id='chipR' class='absolute inset-y-0 left-0' style='right:0;background:#ff4d4d'></div><div id='hpR' class='absolute inset-y-0 left-0' style='right:0;background:#ffd166'></div></div>
  <div id='timer' class='absolute left-0 right-0 text-center font-black' style='top:14px;font-size:64px;color:#fff;-webkit-text-stroke:3px #111'>99</div>
  <div class='absolute font-black italic text-3xl' style='left:48px;top:74px;color:#fff'>MIKA</div><div class='absolute font-black italic text-3xl' style='right:48px;top:74px;color:#fff'>REN</div>
  <div id='combo' class='absolute font-black italic' style='left:70px;top:200px;font-size:84px;color:#ffd166;-webkit-text-stroke:4px #111;opacity:0'><span id='hits'>0</span> HITS</div>
  <div id='move' class='absolute font-black italic' style='left:70px;top:300px;font-size:40px;color:#fff;-webkit-text-stroke:2px #111;opacity:0'>LATTE ART COMBO!</div>
</div>
<div id='ko' class='absolute inset-0 flex items-center justify-center font-black italic' style='font-size:260px;color:#ff4d4d;-webkit-text-stroke:10px #111;opacity:0'>K.O.</div>
<div id='flash' class='absolute inset-0' style='background:#fff;opacity:0'></div>""", "#111"),
              "script": HELPERS + """
var HITS = []; for (var i = 0; i < 14; i++) HITS.push(3.3 + i * 0.18);
function render(frame, total, fps) {
  var t = frame / fps;
  // VS intro
  var sl = eout(P(t, 0, 0.35)); $('L').style.transform = 'translateX(' + (-(1 - sl) * 800) + 'px)'; $('R').style.transform = 'translateX(' + ((1 - sl) * 800) + 'px)';
  $('fl').setAttribute('transform', 'translate(' + (300 - (1 - eout(P(t, 0.2, 0.6))) * 500) + ' 380) scale(1.25)');
  $('fr').setAttribute('transform', 'translate(' + (980 + (1 - eout(P(t, 0.2, 0.6))) * 500) + ' 380) scale(1.25)');
  $('nl').style.transform = 'translateX(' + (-(1 - eout(P(t, 0.5, 0.8))) * 700) + 'px)'; $('nr').style.transform = 'translateX(' + ((1 - eout(P(t, 0.5, 0.8))) * 700) + 'px)';
  var v = P(t, 0.9, 1.15); $('vsT').style.opacity = v; $('vsT').style.transform = 'scale(' + (3 - 2 * eback(v)) + ') rotate(-8deg)';
  var vsOut = P(t, 2.3, 2.6); $('vs').style.opacity = 1 - vsOut * 0.75;
  // fight
  $('hud').style.opacity = P(t, 2.4, 2.7);
  $('timer').textContent = Math.max(0, 99 - Math.floor(P(t, 2.7, 8.5) * 12));
  var n = 0, last = -1; HITS.forEach(function (h) { if (t >= h) { n++; last = h; } });
  var imp = last > 0 ? Math.exp(-(t - last) * 14) : 0;
  $('hits').textContent = n; $('combo').style.opacity = n > 1 ? 1 : 0; $('combo').style.transform = 'scale(' + (1 + imp * 0.35) + ')';
  $('move').style.opacity = n >= 6 ? 1 : 0;
  var hpR = 1 - n / 14, chip = 1 - Math.max(0, n - 2) / 14;
  $('hpR').style.left = ((1 - hpR) * 100) + '%'; $('chipR').style.left = ((1 - Math.min(1, chip + 0.0)) * 100 * P(t, 3.3, 6.2)) + '%';
  $('hpL').style.right = (6 * P(t, 2.9, 3.1)) + '%';
  $('flash').style.opacity = imp * 0.35 + (t > 5.9 && t < 6.0 ? 0.9 : 0);
  var shake = imp * 14 + (t > 5.9 && t < 6.6 ? (1 - P(t, 5.9, 6.6)) * 30 : 0);
  document.body.firstElementChild && (document.getElementById('vs').parentElement.style.transform = 'translate(' + (rnd(frame) - .5) * shake + 'px,' + (rnd(frame + 3) - .5) * shake + 'px)');
  var k = P(t, 6.0, 6.25); $('ko').style.opacity = k > 0 ? 1 : 0; $('ko').style.transform = 'scale(' + (2.5 - 1.5 * eback(k)) + ')';
}"""}}

# ---------------------------------------------------------------- paper collage
collage = {
    "id": "paper-collage", "text": "", "duration": 9,
    "image": {"type": "html_tailwind", "animation": {"fps": 30},
              "html": page(f"""
<div id='sky' class='absolute' style='left:-60px;top:-10px;width:1400px;height:788px;mix-blend-mode:multiply'><img src='assets/sky.png' style='filter:brightness(1.1) contrast(1.15);width:100%;height:100%;object-fit:cover;object-position:50% 20%'></div>
<svg id='stars' class='absolute inset-0' width='1280' height='720' style='mix-blend-mode:multiply'></svg>
<div id='city' class='absolute' style='left:-80px;top:190px;width:1440px;height:810px;mix-blend-mode:multiply'><img src='assets/city.png' style='filter:brightness(1.1) contrast(1.15);width:100%;height:100%;object-fit:cover'></div>
<div id='cat' class='absolute' style='left:760px;top:300px;width:520px;height:520px;mix-blend-mode:multiply'><img src='assets/cat.png' style='filter:brightness(1.1) contrast(1.15);width:100%;height:100%;object-fit:cover'></div>
<div id='grain' class='absolute inset-0' style='background-image:repeating-linear-gradient(0deg,rgba(0,0,0,.025) 0 1px,transparent 1px 3px),repeating-linear-gradient(90deg,rgba(0,0,0,.02) 0 1px,transparent 1px 4px)'></div>
<div id='title' class='absolute left-0 right-0 text-center g italic' style='top:40px;font-size:54px;color:#1d2b53;opacity:0'>made of paper, moved by code</div>""", "#f3ecdf"),
              "script": HELPERS + """
var st = $('stars'), N = 18;
for (var i = 0; i < N; i++) {
  var x = 80 + rnd(i) * 1120, y = 30 + rnd(i + 7) * 260, r = 8 + rnd(i + 3) * 10, pts = [];
  for (var k = 0; k < 10; k++) { var a = k / 10 * Math.PI * 2 - Math.PI / 2, rr = (k % 2 ? r * 0.45 : r) * (0.9 + rnd(i * 13 + k) * 0.2); pts.push((Math.cos(a) * rr).toFixed(1) + ',' + (Math.sin(a) * rr).toFixed(1)); }
  st.insertAdjacentHTML('beforeend', "<polygon id='s" + i + "' points='" + pts.join(' ') + "' fill='#f2c14e' transform='translate(" + x + " " + y + ") scale(0)'/>");
}
function render(frame, total, fps) {
  var t = frame / fps, p = eio(P(t, 0, 9));
  var j = (Math.floor(frame / 2) % 3) - 1;                      // on twos: paper shivers every other frame
  $('sky').style.transform = 'translate(' + (-p * 30 + j * 0.6) + 'px,' + (p * 10) + 'px) scale(' + (1 + p * 0.04) + ')';
  $('city').style.transform = 'translate(' + (-p * 70 - j * 0.8) + 'px,' + (40 - eout(P(t, 0.2, 1.6)) * 40) + 'px)';
  var cy = 60 - eback(P(t, 1.4, 2.2)) * 60;
  $('cat').style.transform = 'translate(' + (-p * 120 + j) + 'px,' + (cy + Math.sin(t * 2) * 2) + 'px) rotate(' + (Math.sin(Math.floor(t * 6)) * 1.2) + 'deg)';
  for (var i = 0; i < N; i++) { var g = eback(P(t, 2.2 + i * 0.12, 2.6 + i * 0.12)); var tw = 1 + 0.12 * Math.sin(t * 5 + i); var el = $('s' + i); var tr = el.getAttribute('transform').replace(/scale\\([^)]*\\)/, 'scale(' + Math.max(0, g * tw) + ')'); el.setAttribute('transform', tr); }
  $('title').style.opacity = P(t, 5.0, 5.8);
}"""}}

deck = {
    "$mulmocast": {"version": "1.1"},
    "canvasSize": {"width": 1280, "height": 720},
    "title": "Idea: characters and stories",
    "description": "Lip-synced two-character dialogue (Gemini 3.1 Flash TTS), an ink-wash battle map, a fighting-game HUD and a paper-cut collage (Nano Banana Pro).",
    "lang": "en",
    "speechParams": {"speakers": {
        "Mika": {"voiceId": "Aoede", "isDefault": True, "provider": "gemini", "model": "gemini-3.1-flash-tts-preview",
                 "speechOptions": {"instruction": "Warm, cheerful cafe barista greeting a regular. Natural and friendly."}},
        "Ren": {"voiceId": "Puck", "provider": "gemini", "model": "gemini-3.1-flash-tts-preview",
                "speechOptions": {"instruction": "Relaxed, amused regular customer. Natural and friendly."}}}},
    "audioParams": {"padding": 0.35, "introPadding": 0.4, "closingPadding": 0.6, "outroPadding": 0.8},
    "beats": [cafe_beat(i, s, l) for i, (s, l) in enumerate(LINES)] + [battle, latte, collage],
}
(HERE / "ideas-story.json").write_text(json.dumps(deck, indent=1))
print("ok; mouth envelopes baked:", {k: len(v) for k, v in mouth.items()})
