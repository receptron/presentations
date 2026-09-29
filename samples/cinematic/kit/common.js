// Shared helpers for animated html_tailwind beats: timing curves, deterministic noise, fonts, text sampling,
// and miniFilm() (tiny code-drawn films for screens). Pasted in front of every scene script by build.py.
const el = (id) => document.getElementById(id);
const clamp01 = (t) => Math.max(0, Math.min(1, t));
const seg = (t, a, b) => clamp01((t - a) / (b - a));
const lerp = (a, b, k) => a + (b - a) * k;
const ease = (t) => { t = clamp01(t); return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
const easeOut = (t) => 1 - Math.pow(1 - clamp01(t), 3);
const easeIn = (t) => Math.pow(clamp01(t), 3);
const back = (t) => { t = clamp01(t); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
const fadeInOut = (t, a, b, f = 0.25) => Math.min(seg(t, a, a + f), 1 - seg(t, b - f, b));
const flashAfter = (t, start, dur = 0.12) => (t >= start ? 1 - seg(t, start, start + dur) : 0);
let fontsReady = false;
const waitFonts = async () => { if (!fontsReady) { await document.fonts.ready; fontsReady = true; } };
const rnd = (n) => { const x = Math.sin(n * 127.1 + 311.7) * 43758.5453; return x - Math.floor(x); };
const pad = (n, w) => String(n).padStart(w, '0');
// fade the whole beat in and out so cuts between beats breathe
const beatFade = (t, D, i = 0.25, o = 0.25) => { el('bf').style.opacity = 1 - Math.min(seg(t, 0, i), 1 - seg(t, D - o, D)); };
// points covering text drawn in a font — targets for particle type
const textTargets = (txt, font, w, h, step, dx = 0, dy = 0) => {
  const c = document.createElement('canvas'); c.width = w; c.height = h; const g = c.getContext('2d');
  g.fillStyle = '#fff'; g.font = font; g.textAlign = 'center'; g.textBaseline = 'middle'; g.fillText(txt, w / 2, h / 2);
  const d = g.getImageData(0, 0, w, h).data, pts = [];
  for (let y = 0; y < h; y += step) for (let x = 0; x < w; x += step) if (d[(y * w + x) * 4 + 3] > 128) pts.push([x + dx, y + dy]);
  return pts;
};
// tiny code-drawn films, shared by several beats
const miniFilm = (g, k, x, y, w, h, t) => {
  g.save(); g.beginPath(); g.rect(x, y, w, h); g.clip();
  if (k === 0) {
    const sky = g.createLinearGradient(0, y, 0, y + h); sky.addColorStop(0, '#2b1a4d'); sky.addColorStop(0.55, '#ff8a5c'); sky.addColorStop(0.56, '#1b3a5c'); sky.addColorStop(1, '#0a1a2c');
    g.fillStyle = sky; g.fillRect(x, y, w, h);
    g.fillStyle = '#ffd59a'; g.beginPath(); g.arc(x + w * 0.5, y + h * 0.55, h * 0.18, Math.PI, 0); g.fill();
    g.strokeStyle = 'rgba(255,200,150,.6)'; g.lineWidth = Math.max(1, h / 70);
    for (let r = 0; r < 5; r++) { g.beginPath(); for (let i = 0; i <= w; i += 6) { const yy = y + h * (0.62 + r * 0.08) + Math.sin(i * 0.05 + t * 2 + r) * h * 0.02; i ? g.lineTo(x + i, yy) : g.moveTo(x + i, yy); } g.stroke(); }
  } else if (k === 1) {
    g.fillStyle = '#081426'; g.fillRect(x, y, w, h);
    for (let b = 0; b < 12; b++) {
      const bw = w / 12, bh = h * (0.35 + 0.5 * rnd(b * 9.1)), bx = x + b * bw;
      g.fillStyle = '#10243c'; g.fillRect(bx + 1, y + h - bh, bw - 2, bh);
      const s = Math.max(3, h / 30);
      for (let wy = y + h - bh + s * 1.5; wy < y + h - s; wy += s * 2.2) for (let wx = bx + s; wx < bx + bw - s; wx += s * 1.8)
        if (rnd(Math.floor(wx) * 3.3 + Math.floor(wy) * 7.7 + Math.floor(t * 3 + rnd(wx) * 5)) > 0.55) { g.fillStyle = 'rgba(255,214,140,.9)'; g.fillRect(wx, wy, s * 0.7, s); }
    }
  } else if (k === 2) {
    g.fillStyle = '#05060f'; g.fillRect(x, y, w, h);
    for (let i = 0; i < 300; i++) {
      const a = rnd(i) * 6.283 + t * 0.6 + (i % 2) * Math.PI, rr = Math.pow(rnd(i * 5.1), 0.7) * h * 0.55, sw = a + rr / h * 2.5;
      g.fillStyle = `rgba(${180 + 75 * rnd(i * 2)},${170 + 60 * rnd(i * 3)},255,${0.4 + 0.6 * rnd(i * 4)})`;
      g.fillRect(x + w / 2 + Math.cos(sw) * rr * 1.5, y + h / 2 + Math.sin(sw) * rr * 0.6, Math.max(1.5, h / 90), Math.max(1.5, h / 90));
    }
  } else if (k === 3) {
    g.fillStyle = '#071a1f'; g.fillRect(x, y, w, h);
    for (let i = 0; i < 38; i++) {
      const v = 0.2 + 0.8 * Math.abs(Math.sin(i * 0.7 + t * 5) * Math.sin(i * 0.23 + t * 1.3));
      g.fillStyle = `hsl(${170 + i * 2},80%,60%)`; g.fillRect(x + w * 0.04 + i * (w * 0.92) / 38, y + h / 2 - v * h * 0.38, (w * 0.92) / 38 - 2, v * h * 0.76);
    }
  } else {
    const bg = g.createLinearGradient(x, y, x + w, y + h); bg.addColorStop(0, '#1d1236'); bg.addColorStop(1, '#0a1630'); g.fillStyle = bg; g.fillRect(x, y, w, h);
    const cx = x + w * 0.5 + Math.sin(t * 0.8) * w * 0.02;
    g.fillStyle = '#05070c'; g.beginPath(); g.arc(cx, y + h * 0.42, h * 0.2, 0, 6.283); g.fill();
    g.beginPath(); g.ellipse(cx, y + h * 1.02, w * 0.3, h * 0.38, 0, Math.PI, 0); g.fill();
    g.strokeStyle = 'rgba(255,170,120,.9)'; g.lineWidth = Math.max(2, h / 45); g.beginPath(); g.arc(cx, y + h * 0.42, h * 0.2, -1.2, 0.6); g.stroke();
  }
  g.fillStyle = 'rgba(0,0,0,.16)'; for (let yy = y; yy < y + h; yy += 4) g.fillRect(x, yy, w, 1);
  g.restore();
};
// Footage: mulmocast re-seeks every <video> to the beat's own time after render() returns (html_render.ts,
// syncVideosToFrame), so a visible <video> never shows the time you asked for. Keep the <video> hidden, seek it
// yourself, and paint the decoded frame into a canvas; the canvas keeps it when mulmocast re-seeks.
const seekTo = (v, t) => new Promise((res) => {
  const go = () => {
    if (Math.abs(v.currentTime - t) < 0.0005) return res();
    v.addEventListener('seeked', function h() { v.removeEventListener('seeked', h); res(); });
    v.currentTime = t;
  };
  if (v.readyState >= 2) go(); else v.addEventListener('loadeddata', go, { once: true });
});
const paint = async (vid, cid, t, sx = 0, sy = 0, sw = null, sh = null) => {
  const v = el(vid); await seekTo(v, t);
  const c = el(cid); c.getContext('2d').drawImage(v, sx, sy, sw ?? v.videoWidth, sh ?? v.videoHeight, 0, 0, c.width, c.height);
};
