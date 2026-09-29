// three.js r147 helpers, with the fixes found while building the AI Short Film Fes remake (2026-09-29):
// MSAA on the composer, a dark studio environment instead of RoomEnvironment, reflections kept on bright metals only,
// an opaque canvas, no tone mapping by default, and chamfered frames whose holes stay open. Pasted after common.js.
const chamfer = (w, h, c) => {
  const s = new THREE.Shape();
  s.moveTo(-w / 2 + c, -h / 2); s.lineTo(w / 2 - c, -h / 2); s.lineTo(w / 2, -h / 2 + c); s.lineTo(w / 2, h / 2 - c);
  s.lineTo(w / 2 - c, h / 2); s.lineTo(-w / 2 + c, h / 2); s.lineTo(-w / 2, h / 2 - c); s.lineTo(-w / 2, -h / 2 + c); s.closePath();
  return s;
};
const fitUV = (g, w, h) => { const p = g.attributes.position, uv = g.attributes.uv; for (let i = 0; i < p.count; i++) uv.setXY(i, p.getX(i) / w + 0.5, p.getY(i) / h + 0.5); uv.needsUpdate = true; return g; };
const ringOf = (w, h, c, th) => { const o = chamfer(w, h, c); o.holes.push(chamfer(w - th * 2, h - th * 2, Math.max(0.001, c - th * 0.4142))); return new THREE.ShapeGeometry(o); };
const dotTex = (rgb) => {
  const c = document.createElement('canvas'); c.width = c.height = 64; const g = c.getContext('2d');
  const r = g.createRadialGradient(32, 32, 0, 32, 32, 32); r.addColorStop(0, 'rgba(255,255,255,1)'); r.addColorStop(0.3, `rgba(${rgb},.8)`); r.addColorStop(1, `rgba(${rgb},0)`);
  g.fillStyle = r; g.fillRect(0, 0, 64, 64); return new THREE.CanvasTexture(c);
};
// scene.environment = RoomEnvironment lights every material with a bright white studio; dark floors and props then
// read as pale grey clay (round-1 renders). On the first render of each scene, keep the reflections only on bright
// metals (gold, chrome) and turn them almost off everywhere else.
const tameEnv = (scene) => {
  scene.traverse((o) => {
    const mats = o.material ? (Array.isArray(o.material) ? o.material : [o.material]) : [];
    mats.forEach((m) => {
      if (!m.isMeshStandardMaterial) return;
      const lum = m.color ? 0.2126 * m.color.r + 0.7152 * m.color.g + 0.0722 * m.color.b : 0;
      m.envMapIntensity = m.metalness >= 0.75 && lum > 0.25 ? Math.max(m.envMapIntensity, 1.8) : Math.min(m.envMapIntensity, 0.12);
    });
  });
};
// RoomEnvironment is a light grey room, so gold reflected grey and read as olive bronze. Scenes that ask for it get a
// dark studio instead: a black sphere with a warm softbox, a cool strip and a small hot key — contrasty reflections.
class StudioEnv extends THREE.Scene {
  constructor() {
    super();
    const add = (geo, rgb, k, pos, look) => { const m = new THREE.Mesh(geo, new THREE.MeshBasicMaterial({ color: new THREE.Color(rgb).multiplyScalar(k), side: THREE.DoubleSide })); m.position.set(...pos); m.lookAt(...look); this.add(m); };
    this.add(new THREE.Mesh(new THREE.SphereGeometry(30, 32, 16), new THREE.MeshBasicMaterial({ color: 0x07090d, side: THREE.BackSide })));
    add(new THREE.PlaneGeometry(14, 9), 0xffe2b0, 5, [-12, 10, 10], [0, 0, 0]);   // warm softbox, upper left front
    add(new THREE.PlaneGeometry(3, 18), 0x9fd8ff, 4, [14, 2, -4], [0, 0, 0]);    // cool strip, right
    add(new THREE.PlaneGeometry(3, 3), 0xffffff, 14, [2, 4, 16], [0, 0, 0]);     // small hot key, front
    add(new THREE.PlaneGeometry(26, 4), 0xffc070, 1.2, [0, -12, 0], [0, 0, 0]);  // warm bounce from below
  }
  dispose() { this.traverse((o) => { if (o.geometry) o.geometry.dispose(); if (o.material) o.material.dispose(); }); }  // RoomEnvironment has it; scenes call it
}
if (THREE.RoomEnvironment) THREE.RoomEnvironment = StudioEnv;
const _r3render = THREE.WebGLRenderer.prototype.render;
THREE.WebGLRenderer.prototype.render = function (scene, camera) {
  if (scene && scene.isScene && !scene.__tamed) { tameEnv(scene); scene.__tamed = true; }
  return _r3render.call(this, scene, camera);
};
const makeRenderer = (id, bloom = [0.8, 0.3, 0.95]) => {
  const R = new THREE.WebGLRenderer({ canvas: el(id), antialias: true, alpha: false, preserveDrawingBuffer: true });
  R.setPixelRatio(1); R.setSize(1280, 720, false); R.toneMapping = THREE.NoToneMapping;
  const scene = new THREE.Scene(); const cam = new THREE.PerspectiveCamera(35, 16 / 9, 0.1, 200);
  // `antialias: true` only covers drawing straight to the canvas; the composer renders into its own targets, which had
  // no anti-aliasing, so thin tilted lines (the judge's gold frames) came out stair-stepped. 4x MSAA on those targets.
  const rt = new THREE.WebGLRenderTarget(1280, 720, { samples: 4, type: THREE.HalfFloatType });
  const composer = new THREE.EffectComposer(R, rt); composer.addPass(new THREE.RenderPass(scene, cam));
  composer.addPass(new THREE.UnrealBloomPass(new THREE.Vector2(1280, 720), bloom[0], bloom[1], bloom[2]));
  return { R, scene, cam, composer };
};
