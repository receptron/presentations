"""mulmocast idea gallery — 3D / game.

Three silent beats (fixed duration, no paid APIs). Everything is drawn by Three.js inside
html_tailwind animation beats; render(frame) is a pure function of the frame number, so frames
can be rendered in any order.
"""

import json
import pathlib

HERE = pathlib.Path(__file__).parent
W, H = 1280, 720

THREE = ("<script src='https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js'></script>"
         "<script src='https://cdn.jsdelivr.net/npm/three@0.147.0/examples/js/loaders/GLTFLoader.js'></script>")
FONT = "<style>.t{font-family:'Helvetica Neue',Helvetica,Arial,sans-serif}.m{font-family:Menlo,monospace}</style>"

HELPERS = """
function clamp01(x) { return Math.max(0, Math.min(1, x)); }
function P(t, a, b) { return clamp01((t - a) / (b - a)); }
function eio(x) { return x < 0.5 ? 4 * x * x * x : 1 - Math.pow(-2 * x + 2, 3) / 2; }
function eout(x) { return 1 - Math.pow(1 - x, 3); }
function lerp(a, b, x) { return a + (b - a) * x; }
function rnd(n) { var x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); }
function $(id) { return document.getElementById(id); }
"""


def beat(label, html, script, duration):
    page = f"{FONT}{THREE}<div class='t relative overflow-hidden' style='width:{W}px;height:{H}px;background:#000'>{html}</div>"
    return {"id": label, "text": "", "duration": duration,
            "image": {"type": "html_tailwind", "html": page, "script": HELPERS + script, "animation": {"fps": 30}}}


# ------------------------------------------------------------------ 1. game chase
game = beat("3D-1-game-chase", """
<canvas id='gl' width='1280' height='720' class='absolute inset-0'></canvas>
<div class='absolute left-6 top-5 m text-white' style='text-shadow:0 2px 0 #000'>
  <div class='text-sm tracking-widest opacity-80'>SCORE</div><div id='score' class='text-5xl font-bold'>000000</div>
</div>
<div class='absolute left-6 bottom-6'>
  <div class='m text-xs text-white tracking-widest mb-1' style='text-shadow:0 1px 0 #000'>STAMINA</div>
  <div style='width:300px;height:16px;border:2px solid #fff;border-radius:4px;background:rgba(0,0,0,.4)'><div id='sta' style='height:100%;background:linear-gradient(90deg,#22d3ee,#a3e635)'></div></div>
</div>
<div class='absolute right-6 top-5' style='width:130px;height:180px;border:2px solid rgba(255,255,255,.8);border-radius:10px;background:rgba(10,20,40,.55);overflow:hidden'>
  <div style='position:absolute;left:61px;top:0;bottom:0;width:8px;background:rgba(255,255,255,.25)'></div>
  <div id='cpm' style='position:absolute;left:45px;width:40px;height:4px;background:#facc15'></div>
  <div id='dot' style='position:absolute;left:58px;width:14px;height:14px;border-radius:50%;background:#f43f5e;box-shadow:0 0 10px #f43f5e'></div>
</div>
<div id='slow' class='absolute left-0 right-0 top-24 text-center m text-2xl font-bold tracking-[0.5em]' style='color:#22d3ee;opacity:0;text-shadow:0 0 12px #22d3ee'>SLOW-MO</div>
<div id='cp' class='absolute left-0 right-0 text-center font-black italic' style='top:280px;font-size:110px;color:#facc15;opacity:0;-webkit-text-stroke:5px #111;paint-order:stroke fill;letter-spacing:-2px'>CHECKPOINT!</div>
<div id='vig' class='absolute inset-0 pointer-events-none' style='background:radial-gradient(ellipse at center,transparent 55%,rgba(0,0,0,.55))'></div>
""", """
var R3 = new THREE.WebGLRenderer({ canvas: $('gl'), antialias: true, preserveDrawingBuffer: true });
R3.setPixelRatio(1); R3.setSize(1280, 720, false);
var scene = new THREE.Scene();
scene.background = new THREE.Color(0x7dd3fc); scene.fog = new THREE.Fog(0x7dd3fc, 25, 90);
var cam = new THREE.PerspectiveCamera(55, 16 / 9, 0.1, 300);
scene.add(new THREE.HemisphereLight(0xffffff, 0x4d7c0f, 1.6));
var sun = new THREE.DirectionalLight(0xfff1c1, 2.2); sun.position.set(-20, 30, 10); scene.add(sun);
var flat = function (c) { return new THREE.MeshStandardMaterial({ color: c, flatShading: true, roughness: 0.9 }); };
var SPEED = 7, LEN = 160;
// ground: grass + road + stripes
var grass = new THREE.Mesh(new THREE.PlaneGeometry(200, 400), flat(0x65a30d)); grass.rotation.x = -Math.PI / 2; grass.position.z = 150; scene.add(grass);
var road = new THREE.Mesh(new THREE.PlaneGeometry(6, 400), flat(0x334155)); road.rotation.x = -Math.PI / 2; road.position.set(0, 0.01, 150); scene.add(road);
for (var s = 0; s < 80; s++) { var st = new THREE.Mesh(new THREE.PlaneGeometry(0.25, 2), flat(0xf8fafc)); st.rotation.x = -Math.PI / 2; st.position.set(0, 0.02, s * 5); scene.add(st); }
// low-poly trees and rocks at deterministic positions
for (var i = 0; i < 90; i++) {
  var side = i % 2 ? 1 : -1, z = i * 3.2 + rnd(i) * 2, x = side * (5 + rnd(i + 7) * 14);
  if (rnd(i + 3) > 0.25) {
    var tr = new THREE.Group();
    var trunk = new THREE.Mesh(new THREE.CylinderGeometry(0.25, 0.35, 1.4, 5), flat(0x78350f)); trunk.position.y = 0.7; tr.add(trunk);
    var h = 2.5 + rnd(i + 9) * 2.5;
    var crown = new THREE.Mesh(new THREE.ConeGeometry(1.2 + rnd(i + 2) * 0.6, h, 6), flat([0x15803d, 0x16a34a, 0x166534][i % 3])); crown.position.y = 1.4 + h / 2; tr.add(crown);
    tr.position.set(x, 0, z); scene.add(tr);
  } else {
    var rock = new THREE.Mesh(new THREE.DodecahedronGeometry(0.8 + rnd(i) * 1.2, 0), flat(0x94a3b8)); rock.position.set(x, 0.5, z); scene.add(rock);
  }
}
// coins over the road and an obstacle to jump
var coins = [];
for (var c = 0; c < 26; c++) {
  var coin = new THREE.Mesh(new THREE.TorusGeometry(0.35, 0.12, 8, 16), new THREE.MeshStandardMaterial({ color: 0xfacc15, emissive: 0xca8a04, emissiveIntensity: 0.5, metalness: 0.6, roughness: 0.3 }));
  var cz = 8 + c * 2.4, cx = Math.sin(c * 0.5) * 1.6;
  coin.position.set(cx, 1.1, cz); coin.userData.z = cz; scene.add(coin); coins.push(coin);
}
var JUMPZ = 44;   // obstacle position; the slow-mo jump happens here
var crate = new THREE.Mesh(new THREE.BoxGeometry(2.5, 1.1, 1), flat(0xea580c)); crate.position.set(0, 0.55, JUMPZ); scene.add(crate);
// checkpoint arch
var CPZ = 52, arch = new THREE.Group();
[-3.5, 3.5].forEach(function (x) { var p = new THREE.Mesh(new THREE.BoxGeometry(0.6, 5, 0.6), flat(0xf8fafc)); p.position.set(x, 2.5, 0); arch.add(p); });
var bar = new THREE.Mesh(new THREE.BoxGeometry(7.6, 1, 0.6), flat(0xfacc15)); bar.position.y = 5; arch.add(bar);
arch.position.z = CPZ; scene.add(arch);
// game time: normal, then slow-mo SA..SB at SK speed, then normal again
var SA = 5.3, SB = 7.3, SK = 0.25;          // slow-mo window (real seconds) and its speed
function gameTime(t) {
  if (t < SA) return t;
  if (t < SB) return SA + (t - SA) * SK;
  return SA + (SB - SA) * SK + (t - SB);
}
function realTime(g) {                          // inverse of gameTime
  var gb = SA + (SB - SA) * SK;
  if (g < SA) return g;
  if (g < gb) return SA + (g - SA) / SK;
  return SB + (g - gb);
}
var robot = null, mixer = null, run = null, jump = null;
var ready = new Promise(function (res, rej) {
  new THREE.GLTFLoader().load('https://cdn.jsdelivr.net/gh/mrdoob/three.js@r160/examples/models/gltf/RobotExpressive/RobotExpressive.glb', function (g) {
    robot = g.scene; robot.scale.setScalar(0.55); scene.add(robot);
    mixer = new THREE.AnimationMixer(robot);
    var get = function (n) { return g.animations.filter(function (a) { return a.name === n; })[0]; };
    run = mixer.clipAction(get('Running')); jump = mixer.clipAction(get('Jump'));
    run.play(); jump.play(); res();
  }, undefined, rej);
});
function render(frame, total, fps) {
  return ready.then(function () {
    var t = frame / fps, tg = gameTime(t);
    var z = tg * SPEED + 4, x = Math.sin(tg * 0.6) * 0.8;
    // jump arc over the crate (in game time)
    var jt0 = (JUMPZ - 4 - 3.2) / SPEED, jp = P(tg, jt0, jt0 + 0.9);
    var y = Math.sin(jp * Math.PI) * 2.0;
    robot.position.set(x, y, z);
    robot.rotation.y = 0;
    run.time = (tg * 1.1) % run.getClip().duration;
    jump.time = jp * jump.getClip().duration * 0.95;
    var jw = jp > 0 && jp < 1 ? 1 : 0;
    run.setEffectiveWeight(1 - jw); jump.setEffectiveWeight(jw);
    mixer.update(0);
    coins.forEach(function (c, i) { c.rotation.y = tg * 4 + i; c.visible = c.userData.z > z + 0.3; });   // passed = collected, so the score never goes down
    // camera: chase -> low angle -> whip round to the front for the slow-mo jump -> back to chase
    var chase = [x * 0.5, 3.2, z - 7.5], low = [x + 3.0, 0.35, z - 6.0];
    var ang = eio(P(t, 4.3, 5.4)) * Math.PI * 0.72 - eio(P(t, SB, SB + 0.8)) * Math.PI * 0.72;
    var rad = lerp(7.5, 7.0, P(t, 4.3, 5.4));
    var orbit = [x + Math.sin(ang) * rad, lerp(3.2, 2.6, P(t, 4.3, 5.4)) + P(t, SB, SB + 0.8) * 0.6, z - Math.cos(ang) * rad];
    var toLow = eio(P(t, 1.6, 2.2)) * (1 - eio(P(t, 3.6, 4.3)));
    var cx = lerp(orbit[0], low[0], toLow), cy = lerp(orbit[1], low[1], toLow), cz = lerp(orbit[2], low[2], toLow);
    if (t < 1.6) { cx = chase[0]; cy = chase[1]; cz = chase[2]; }
    var shake = t > SB && t < SB + 0.3 ? 0.12 * Math.sin(frame * 2.3) : 0;
    cam.position.set(cx + shake, cy, cz);
    cam.fov = lerp(55, 48, P(t, 5.0, 5.4)) + (lerp(0, 13, P(t, SB, SB + 0.5)));
    cam.updateProjectionMatrix();
    cam.lookAt(x, 1.2 + y * 0.6, z + 2);
    R3.render(scene, cam);
    // HUD
    var got = 0; coins.forEach(function (c) { if (!c.visible) got++; });
    $('score').textContent = String(Math.floor(tg * 130) + got * 250).padStart(6, '0');
    $('sta').style.width = (100 - tg * 7 + (t > 8 ? 30 : 0)) + '%';
    $('dot').style.top = (166 - Math.min(1, z / 80) * 160) + 'px';
    $('cpm').style.top = (166 - CPZ / 80 * 160 + 5) + 'px';
    var slow = t > SA && t < SB;
    $('slow').style.opacity = slow ? 0.6 + 0.4 * Math.sin(t * 12) : 0;
    R3.domElement.style.filter = slow ? 'saturate(1.3) contrast(1.1)' : 'none';
    var cpT = realTime((CPZ - 4) / SPEED);      // real time the arch is passed
    var cpp = P(t, cpT, cpT + 1.3);
    $('cp').style.opacity = cpp > 0 && cpp < 1 ? 1 - Math.pow(cpp, 4) : 0;
    $('cp').style.transform = 'scale(' + (0.4 + eout(clamp01(cpp * 4)) * 0.6) + ') rotate(-4deg)';
  });
}
""", 10)

# ------------------------------------------------------------------ 2. stop-motion clay
clay = beat("3D-2-stop-motion-clay", """
<canvas id='gl' width='1280' height='720' class='absolute inset-0'></canvas>
<div class='absolute left-0 right-0 bottom-6 text-center' style='font-family:Georgia,serif;font-size:34px;color:#fff7ed;text-shadow:0 2px 6px rgba(0,0,0,.4)'>no clay was used — only code, animated on twos</div>
""", """
var R3 = new THREE.WebGLRenderer({ canvas: $('gl'), antialias: true, preserveDrawingBuffer: true });
R3.setPixelRatio(1); R3.setSize(1280, 720, false);
R3.shadowMap.enabled = true; R3.shadowMap.type = THREE.PCFSoftShadowMap;
var scene = new THREE.Scene(); scene.background = new THREE.Color(0xf5d0a9);
var cam = new THREE.PerspectiveCamera(35, 16 / 9, 0.1, 100);
scene.add(new THREE.HemisphereLight(0xfff7ed, 0x9a3412, 1.2));
var key = new THREE.DirectionalLight(0xffffff, 2.4); key.position.set(4, 8, 5); key.castShadow = true;
key.shadow.mapSize.set(2048, 2048); key.shadow.camera.left = -8; key.shadow.camera.right = 8; key.shadow.camera.top = 8; key.shadow.camera.bottom = -8; scene.add(key);
// fingerprint-ish bump texture: concentric wobbly ellipse arcs at deterministic spots
function thumbTex(seed) {
  var c = document.createElement('canvas'); c.width = c.height = 512; var x = c.getContext('2d');
  x.fillStyle = '#808080'; x.fillRect(0, 0, 512, 512);
  for (var k = 0; k < 14; k++) {
    var cx = rnd(seed + k) * 512, cy = rnd(seed + k + 50) * 512, rot = rnd(seed + k + 99) * Math.PI;
    for (var r = 4; r < 70; r += 5) {
      x.strokeStyle = 'rgba(' + (r % 10 ? 60 : 200) + ',' + (r % 10 ? 60 : 200) + ',' + (r % 10 ? 60 : 200) + ',.35)'; x.lineWidth = 2;
      x.beginPath(); x.ellipse(cx, cy, r, r * 0.7, rot, rnd(k + r) * 2, rnd(k + r) * 2 + 4.5); x.stroke();
    }
  }
  var tex = new THREE.CanvasTexture(c); tex.wrapS = tex.wrapT = THREE.RepeatWrapping; tex.repeat.set(2, 2); return tex;
}
var bump = thumbTex(3);
function clayMat(col) { return new THREE.MeshStandardMaterial({ color: col, roughness: 0.75, metalness: 0, bumpMap: bump, bumpScale: 0.6 }); }
var wobbly = [];
function add(mesh, amt) { mesh.castShadow = mesh.receiveShadow = true; scene.add(mesh); if (amt) { mesh.userData.base = mesh.geometry.attributes.position.array.slice(); mesh.userData.amt = amt; wobbly.push(mesh); } return mesh; }
var ground = add(new THREE.Mesh(new THREE.CylinderGeometry(7, 7.3, 0.6, 40, 1), clayMat(0x84cc16)), 0.05); ground.position.y = -0.3;
var path = add(new THREE.Mesh(new THREE.BoxGeometry(12, 0.08, 1.6, 24, 1, 4), clayMat(0xfde68a)), 0.04); path.position.set(0, 0.05, 1.2);
var houses = [[-3.6, -1.6, 0xf87171, 0x7c2d12], [-0.6, -2.4, 0x60a5fa, 0x1e3a8a], [2.6, -1.8, 0xfbbf24, 0x9a3412]];
houses.forEach(function (h, i) {
  var b = add(new THREE.Mesh(new THREE.BoxGeometry(1.8, 1.6, 1.6, 6, 6, 6), clayMat(h[2])), 0.06); b.position.set(h[0], 0.8, h[1]);
  var r = add(new THREE.Mesh(new THREE.ConeGeometry(1.5, 1.2, 4, 3), clayMat(h[3])), 0.07); r.position.set(h[0], 2.2, h[1]); r.rotation.y = Math.PI / 4;
  var d = add(new THREE.Mesh(new THREE.BoxGeometry(0.4, 0.7, 0.1), clayMat(0x451a03)), 0); d.position.set(h[0], 0.35, h[1] + 0.82);
});
[[-5, 1.5], [4.8, 0.4], [5.3, -2.8], [-5.4, -2.2]].forEach(function (p, i) {
  var tr = add(new THREE.Mesh(new THREE.IcosahedronGeometry(0.9, 2), clayMat(0x15803d)), 0.12); tr.position.set(p[0], 1.6, p[1]);
  var tk = add(new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.25, 1, 8), clayMat(0x78350f)), 0.03); tk.position.set(p[0], 0.5, p[1]);
});
// the blob creature
var blob = new THREE.Group(); scene.add(blob);
var body = add(new THREE.Mesh(new THREE.SphereGeometry(0.7, 32, 24), clayMat(0xa855f7)), 0.05); scene.remove(body); blob.add(body); body.position.y = 0.7;
function eye(x) {
  var w = new THREE.Mesh(new THREE.SphereGeometry(0.17, 16, 12), clayMat(0xffffff)); w.position.set(x, 0.95, 0.58); blob.add(w);
  var p = new THREE.Mesh(new THREE.SphereGeometry(0.08, 12, 10), clayMat(0x111111)); p.position.set(x, 0.95, 0.72); blob.add(p);
}
eye(-0.22); eye(0.22);
var arm = new THREE.Mesh(new THREE.CapsuleGeometry(0.1, 0.45, 4, 8), clayMat(0xa855f7)); arm.castShadow = true; blob.add(arm);
function wobble(step) {
  wobbly.forEach(function (m, mi) {
    var a = m.geometry.attributes.position, b = m.userData.base, amt = m.userData.amt;
    for (var i = 0; i < a.count; i++) {
      var bx = b[i * 3], by = b[i * 3 + 1], bz = b[i * 3 + 2];
      var n = Math.sin(bx * 3.1 + step * 1.7 + mi) * Math.cos(bz * 2.7 - step * 1.3) + Math.sin(by * 4.3 + step * 2.1);
      a.setXYZ(i, bx + n * amt * 0.5, by + n * amt * 0.4, bz + n * amt * 0.5);
    }
    a.needsUpdate = true; m.geometry.computeVertexNormals();
  });
}
function render(frame, total, fps) {
  var f2 = Math.floor(frame / 2) * 2, t = f2 / fps;   // on twos: 12 fps motion
  wobble(Math.floor(frame / 2) % 3);                  // boil: three wobble states, like re-sculpted clay
  // blob hops along the path left -> right, then stops and waves
  var hopT = P(t, 0.3, 5.0), hops = 5;
  var hx = lerp(-4.5, 1.2, hopT), ph = (hopT * hops) % 1;
  var hy = hopT > 0 && hopT < 1 ? Math.sin(ph * Math.PI) * 0.9 : 0;
  var squash = hopT > 0 && hopT < 1 ? (ph < 0.12 || ph > 0.88 ? 0.75 : 1.08) : 1;
  blob.position.set(hx, hy, 1.2);
  body.scale.set(1 / Math.sqrt(squash), squash, 1 / Math.sqrt(squash));
  blob.rotation.y = hopT < 1 ? Math.PI / 2 * 0.6 : lerp(Math.PI / 2 * 0.6, 0, P(t, 5.0, 5.6));
  var wave = t > 5.6 ? Math.sin((t - 5.6) * 9) * 0.6 : 0;
  arm.position.set(0.72, 1.0 + (t > 5.6 ? 0.25 : 0), 0); arm.rotation.z = t > 5.6 ? -2.2 + wave : -0.3;
  // slightly nudged camera, also on twos
  cam.position.set(Math.sin(t * 0.25) * 1.5 + (rnd(f2) - 0.5) * 0.04, 5.2 - t * 0.12, 10.5 - t * 0.35);
  cam.lookAt(0, 0.8, 0);
  R3.render(scene, cam);
}
""", 8)

# ------------------------------------------------------------------ 3. same scene, two ways
twoways = beat("3D-3-same-scene-two-ways", """
<canvas id='gl' width='1280' height='720' class='absolute inset-0'></canvas>
<div id='div' class='absolute top-0 bottom-0' style='width:4px;background:#fff;box-shadow:0 0 16px rgba(255,255,255,.9)'></div>
<div id='lA' class='absolute top-6 m text-sm tracking-[0.4em] font-bold' style='color:#93c5fd'>BLUEPRINT</div>
<div id='lB' class='absolute top-6 m text-sm tracking-[0.4em] font-bold' style='color:#431407'>RENDER</div>
<div class='absolute left-0 right-0 bottom-6 text-center text-2xl font-bold' style='color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.6)'>One scene. Two renderers. One script.</div>
""", """
var R3 = new THREE.WebGLRenderer({ canvas: $('gl'), antialias: true, preserveDrawingBuffer: true });
R3.setPixelRatio(1); R3.setSize(1280, 720, false);
R3.shadowMap.enabled = true; R3.shadowMap.type = THREE.PCFSoftShadowMap;
R3.autoClear = false;
var scene = new THREE.Scene();
var cam = new THREE.PerspectiveCamera(38, 16 / 9, 0.1, 200);
var hemi = new THREE.HemisphereLight(0xfff7ed, 0x78716c, 0.9); scene.add(hemi);
var sun = new THREE.DirectionalLight(0xffe4c4, 2.6); sun.position.set(-12, 18, 10); sun.castShadow = true;
sun.shadow.mapSize.set(2048, 2048); ['left', 'bottom'].forEach(function (k) { sun.shadow.camera[k] = -20; }); ['right', 'top'].forEach(function (k) { sun.shadow.camera[k] = 20; }); scene.add(sun);
function M(c, r) { return new THREE.MeshStandardMaterial({ color: c, roughness: r === undefined ? 0.8 : r }); }
function add(g, m, x, y, z) { var o = new THREE.Mesh(g, m); o.position.set(x, y, z); o.castShadow = o.receiveShadow = true; scene.add(o); return o; }
// a small castle keep: stone base, stacked tiers with flared roofs, walls and a gate
add(new THREE.BoxGeometry(40, 0.2, 40), M(0x84a98c), 0, -0.1, 0);
add(new THREE.BoxGeometry(12, 3, 12), M(0x9ca3af, 0.95), 0, 1.5, 0);           // stone base
var tiers = [[9, 2.4], [7.2, 2.0], [5.6, 1.8], [4.2, 1.6], [3, 1.4]], y = 3;
tiers.forEach(function (tr, i) {
  add(new THREE.BoxGeometry(tr[0], tr[1], tr[0]), M(0xf5f5f4, 0.7), 0, y + tr[1] / 2, 0);
  var roof = add(new THREE.CylinderGeometry(tr[0] * 0.45, tr[0] * 0.85, 0.9, 4, 1), M(0x3f6f63, 0.5), 0, y + tr[1] + 0.35, 0);
  roof.rotation.y = Math.PI / 4;
  for (var w = -1; w <= 1; w++) add(new THREE.BoxGeometry(0.5, tr[1] * 0.4, 0.1), M(0x1c1917), w * tr[0] * 0.28, y + tr[1] * 0.5, tr[0] / 2 + 0.05);
  y += tr[1] + 0.8;
});
add(new THREE.ConeGeometry(0.4, 1.4, 8), M(0xd4a017, 0.3), 0, y + 0.4, 0);
[[-14, 0], [14, 0], [0, -14], [0, 14]].forEach(function (p, i) {
  var wall = add(new THREE.BoxGeometry(i < 2 ? 1 : 28, 2.2, i < 2 ? 28 : 1), M(0xd6d3d1), p[0], 1.1, p[1]);
});
add(new THREE.BoxGeometry(4, 3, 1.4), M(0x78350f), 0, 1.5, 14);
for (var k = 0; k < 16; k++) { var a = k / 16 * Math.PI * 2; add(new THREE.ConeGeometry(0.9, 3, 7), M(0x3f7d4a), Math.cos(a) * 18, 1.5, Math.sin(a) * 18); }
var grid = new THREE.GridHelper(40, 40, 0x93c5fd, 0x3b82f6); grid.visible = false; scene.add(grid);
var wire = new THREE.MeshBasicMaterial({ color: 0xdbeafe, wireframe: true, transparent: true, opacity: 0.85 });
var BLUE = new THREE.Color(0x0b2a5b), SKY = new THREE.Color(0xfde6c8);
function render(frame, total, fps) {
  var t = frame / fps;
  var a = 0.5 + t * 0.22, rad = 34 - t * 1.2;
  cam.position.set(Math.cos(a) * rad, 14 - t * 0.6, Math.sin(a) * rad); cam.lookAt(0, 6, 0);
  // divider: sweeps across and settles in the middle
  var dx = t < 2 ? lerp(1180, 200, eio(P(t, 0.3, 2))) : lerp(200, 640, eio(P(t, 2.4, 4.2)));
  dx = Math.round(dx);
  R3.setScissorTest(true);
  R3.setViewport(0, 0, 1280, 720);
  // left: blueprint
  R3.setScissor(0, 0, dx, 720);
  scene.background = BLUE; scene.overrideMaterial = wire; grid.visible = true; sun.castShadow = false;
  R3.clear(); R3.render(scene, cam);
  // right: lit render with shadows
  R3.setScissor(dx, 0, 1280 - dx, 720);
  scene.background = SKY; scene.overrideMaterial = null; grid.visible = false; sun.castShadow = true;
  R3.clear(); R3.render(scene, cam);
  R3.setScissorTest(false);
  $('div').style.left = (dx - 2) + 'px';
  $('lA').style.left = Math.max(16, dx - 190) + 'px'; $('lA').style.opacity = dx > 220 ? 1 : 0;
  $('lB').style.left = (dx + 22) + 'px'; $('lB').style.opacity = dx < 1100 ? 1 : 0;
}
""", 8)


def deck():
    return {
        "$mulmocast": {"version": "1.1"},
        "canvasSize": {"width": W, "height": H},
        "title": "mulmocast idea gallery — 3D / game",
        "description": "Silent idea beats: a GLB character game chase with HUD and slow-mo, stop-motion clay on twos, and one scene rendered as blueprint and as a lit render.",
        "lang": "en",
        "speechParams": {"speakers": {"Presenter": {"displayName": {"en": "Presenter"}, "voiceId": "Kore", "isDefault": True, "provider": "gemini"}}},
        "beats": [game, clay, twoways],
    }


(HERE / "ideas-3d.json").write_text(json.dumps(deck(), ensure_ascii=False, indent=2) + "\n")
print("ok")
