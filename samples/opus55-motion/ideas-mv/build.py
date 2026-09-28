"""Idea: a hand-painted music video that hits on the kicks of an ElevenLabs track.

The audio is analysed first (analyze.py -> mv-beats.json: kick times + per-frame loudness) and the
numbers are baked into the beat's script, so every splash lands on a detected kick.
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
beats = json.load(open(HERE / "mv-beats.json"))
DUR = 24.0

HELPERS = """
function clamp01(x) { return Math.max(0, Math.min(1, x)); }
function P(t, a, b) { return clamp01((t - a) / (b - a)); }
function eout(x) { return 1 - Math.pow(1 - x, 3); }
function rnd(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
"""

script = HELPERS + "var KICKS = " + json.dumps(beats["kicks"]) + ";\nvar LOUD = " + json.dumps(beats["loud"]) + ";\n" + """
var cv = document.getElementById('cv'), ctx = cv.getContext('2d');
var W = 1280, H = 720;
// paper: fixed grain + fibres, drawn once
var paper = document.createElement('canvas'); paper.width = W; paper.height = H;
(function () {
  var p = paper.getContext('2d'); p.fillStyle = '#f6efe2'; p.fillRect(0, 0, W, H);
  for (var i = 0; i < 26000; i++) { p.fillStyle = 'rgba(90,70,40,' + (rnd(i) * 0.05) + ')'; p.fillRect(rnd(i + 1) * W, rnd(i + 2) * H, 1.5, 1.5); }
  p.strokeStyle = 'rgba(120,95,60,.05)';
  for (var j = 0; j < 400; j++) { p.beginPath(); var x = rnd(j + 7) * W, y = rnd(j + 9) * H; p.moveTo(x, y); p.lineTo(x + (rnd(j + 3) - .5) * 40, y + (rnd(j + 4) - .5) * 40); p.stroke(); }
})();
function loud(t) { return LOUD[Math.min(LOUD.length - 1, Math.max(0, Math.round(t * 30)))] || 0; }
// smooth watercolour shape: radius wobbles with a sum of sines (no jagged per-vertex noise)
function wash(pathFn, col, alpha, seed) {
  for (var layer = 0; layer < 6; layer++) {
    ctx.save(); ctx.translate((rnd(seed + layer) - .5) * 6, (rnd(seed + layer + 9) - .5) * 6);
    ctx.beginPath(); pathFn(layer); ctx.closePath();
    ctx.globalAlpha = alpha * 0.16; ctx.fillStyle = col; ctx.fill();
    ctx.globalAlpha = alpha * 0.10; ctx.lineWidth = 3; ctx.strokeStyle = col; ctx.stroke();   // pigment pools at the edge
    ctx.restore();
  }
  ctx.globalAlpha = 1;
}
function blob(x, y, r, seed, col, alpha) {
  if (r <= 0) return;
  wash(function (layer) {
    for (var k = 0; k <= 72; k++) {
      var a = k / 72 * Math.PI * 2;
      var rr = r * (1 + 0.07 * Math.sin(2 * a + seed + layer * .3) + 0.05 * Math.sin(3 * a + seed * 2) + 0.03 * Math.sin(7 * a + seed * 3 + layer));
      var px = x + Math.cos(a) * rr, py = y + Math.sin(a) * rr;
      if (k === 0) ctx.moveTo(px, py); else ctx.lineTo(px, py);
    }
  }, col, alpha, seed);
}
// a ridge line revealed left to right, filled down to `base`
function ridge(peaks, base, col, alpha, seed, reveal) {
  if (reveal <= 0) return;
  ctx.save(); ctx.beginPath(); ctx.rect(0, 0, W * reveal, H); ctx.clip();
  wash(function (layer) {
    ctx.moveTo(-20, base);
    for (var x = -20; x <= W + 20; x += 8) {
      var y = base;
      peaks.forEach(function (pk) { y = Math.min(y, pk[1] + Math.abs(x - pk[0]) * pk[2] + Math.sin(x * 0.05 + seed + layer) * 4); });
      ctx.lineTo(x, y);
    }
    ctx.lineTo(W + 20, base);
  }, col, alpha, seed);
  ctx.restore();
}
// dry brush along a polyline; progress 0..1 draws it from its start
function brush(pts, width, col, progress, seed, alpha) {
  if (progress <= 0) return;
  var n = Math.max(2, Math.floor(pts.length * progress));
  for (var b = 0; b < 16; b++) {
    var off = (b - 8) / 8 * width / 2;
    ctx.globalAlpha = (alpha || 1) * (0.10 + rnd(seed * 7 + b) * 0.25); ctx.strokeStyle = col; ctx.lineWidth = 1.5 + rnd(b + seed) * 3; ctx.lineCap = 'round';
    ctx.beginPath();
    for (var s = 0; s < n; s++) {
      var q = pts[s], x = q[0], y = q[1] + off;
      if (rnd(seed * 97 + b * 41 + s) < 0.05) { ctx.stroke(); ctx.beginPath(); ctx.moveTo(x, y); continue; }   // dry gaps
      if (s === 0) ctx.moveTo(x, y); else ctx.lineTo(x, y);
    }
    ctx.stroke();
  }
  ctx.globalAlpha = 1;
}
function line(x0, y0, x1, y1, n, wob, seed) { var o = []; for (var i = 0; i <= n; i++) { var u = i / n; o.push([x0 + (x1 - x0) * u + Math.sin(u * 9 + seed) * wob, y0 + (y1 - y0) * u + Math.cos(u * 7 + seed) * wob]); } return o; }
function grow(k, d) { return eout(P(TNOW, k, k + (d || 0.4))); }
var TNOW = 0;
var K = KICKS;
var TREES = []; for (var i = 12; i < 24 && i < K.length; i++) TREES.push({ k: K[i], x: 90 + ((i * 173) % 1100), h: 90 + rnd(i) * 90, seed: i });
function render(frame, total, fps) {
  var t = frame / fps; TNOW = t;
  var punch = 0;
  K.forEach(function (k) { if (t >= k) punch = Math.max(punch, Math.exp(-(t - k) * 10)); });
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.drawImage(paper, 0, 0);
  var z = 1 + punch * 0.03;
  ctx.setTransform(z, 0, 0, z, W / 2 * (1 - z), H / 2 * (1 - z));
  // intro (no kicks yet): the sky breathes in with the synth, the sun blooms
  var sky = eout(P(t, 0.2, 7.5)) * (0.85 + loud(t) * 0.3);
  blob(300, 180, 360 * sky, 1, '#9cc3ff', 0.9);
  blob(980, 160, 330 * sky, 2, '#ffc8a2', 0.9);
  blob(900, 230, 70 * eout(P(t, 4.5, 7.8)), 3, '#f3a712', 1.3);
  // kicks 0-3: far ridge; 4-7: near ridge
  ridge([[180, 330, 0.6], [520, 300, 0.7], [860, 340, 0.55], [1150, 310, 0.65]], 480, '#7d8fb3', 1.2, 11, grow(K[0], 4 * 0.5));
  ridge([[80, 400, 0.8], [420, 370, 0.9], [760, 410, 0.7], [1080, 380, 0.85]], 540, '#3d4f7a', 1.3, 12, grow(K[4], 4 * 0.5));
  // kicks 8-11: lake, one dry horizontal stroke each
  for (var i = 8; i < 12; i++) brush(line(-40, 560 + (i - 8) * 32, 1320, 560 + (i - 8) * 32 + 6, 80, 3, i), 26, ['#5b8def', '#ffc8a2', '#7aa6ff', '#f3a712'][i % 4], grow(K[i], 0.35), i, 1.1);
  // kicks 12-23: a tree lands on every kick
  TREES.forEach(function (tr) {
    var g = grow(tr.k, 0.3), base = 540 + (tr.seed % 3) * 8;
    brush(line(tr.x, base, tr.x + 4, base - tr.h, 20, 1.5, tr.seed), 8, '#3b2a1a', g, tr.seed, 1.4);
    blob(tr.x, base - tr.h - 20, 42 * eout(P(t, tr.k + 0.12, tr.k + 0.45)), tr.seed + 50, tr.seed % 2 ? '#2f6b3a' : '#4f8a3c', 1.3);
  });
  // lift section (from 14 s): birds flick in on the kicks
  K.forEach(function (k, i) {
    if (k < 14 || k >= 21.4 || i % 2 || t < k) return;
    var bx = 250 + ((i * 211) % 800), by = 90 + ((i * 53) % 120), g = grow(k, 0.25);
    brush([[bx - 18, by], [bx - 8, by - 8], [bx, by], [bx + 8, by - 8], [bx + 18, by]].slice(0, Math.max(2, Math.ceil(5 * g))), 4, '#29335c', 1, i + 200, 1.6);
  });
  // last kick: the seal
  ctx.setTransform(1, 0, 0, 1, 0, 0);
  var last = K[K.length - 1], st = P(t, last, last + 0.12);
  if (st > 0) {
    var sz = 84 * (1.6 - 0.6 * eout(st));
    ctx.save(); ctx.translate(1140, 620); ctx.rotate(-0.05);
    ctx.globalAlpha = 0.88; ctx.fillStyle = '#c0392b'; ctx.fillRect(-sz / 2, -sz / 2, sz, sz);
    ctx.globalAlpha = 1; ctx.fillStyle = '#f6efe2'; ctx.font = 'bold ' + sz * 0.42 + 'px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
    ctx.fillText('拍', 0, -sz * 0.18); ctx.font = 'bold ' + sz * 0.26 + 'px serif'; ctx.fillText('120', 0, sz * 0.24);
    ctx.restore();
  }
  document.getElementById('title').style.opacity = P(t, last + 0.5, last + 1.1);
}
"""

html = ("<div style='position:relative;width:1280px;height:720px;overflow:hidden'>"
        "<canvas id='cv' width='1280' height='720' style='position:absolute;inset:0'></canvas>"
        "<div id='title' style='position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0;"
        "font-family:Georgia,serif;font-style:italic;font-size:54px;color:#29335c;letter-spacing:.02em;align-items:flex-start;padding-top:36px'>one stroke per kick</div></div>")

deck = {
    "$mulmocast": {"version": "1.1"},
    "canvasSize": {"width": 1280, "height": 720},
    "title": "Idea: a hand-painted MV on the kicks",
    "description": "ElevenLabs track -> kick detection -> every splash lands on a kick. No video model.",
    "lang": "en",
    "speechParams": {"speakers": {"Presenter": {"voiceId": "Kore", "isDefault": True, "provider": "gemini"}}},
    "audioParams": {"bgm": {"kind": "path", "path": "assets/mv.mp3"}, "bgmVolume": 1.0, "audioVolume": 1.0,
                    "padding": 0, "introPadding": 0, "closingPadding": 0, "outroPadding": 0},
    "beats": [{"id": "mv-painted-kicks", "text": "", "duration": DUR,
               "image": {"type": "html_tailwind", "html": html, "script": script, "animation": {"fps": 30}}}],
}
(HERE / "ideas-mv.json").write_text(json.dumps(deck, indent=1))
print("ok", len(beats["kicks"]), "kicks baked in")
