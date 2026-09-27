// A single whiteboard drawn across several beats. Each beat shows everything drawn by earlier beats,
// draws its own items (strokes grow along the path, text is revealed left to right), and the marker
// hand follows the tip. The hand carries over between beats: it starts where the previous beat ended.

export const INK = "#1f1f1f", RED = "#d9443b", BLUE = "#2451b8";
const HAND_W = 520;
// Marker tip inside the 1024x1024 hand image, scaled to the display width.
const TIP = [(166 / 1024) * HAND_W, (277 / 1024) * HAND_W];
const EXIT = [1400, 900];

export const stroke = (id, d, color = INK, width = 5) =>
  `<path id="${id}" d="${d}" fill="none" stroke="${color}" stroke-width="${width}" stroke-linecap="round" stroke-linejoin="round" style="opacity:0"/>`;
export const text = (id, x, y, size, str, color = INK, anchor = "middle") =>
  `<text id="${id}" x="${x}" y="${y}" text-anchor="${anchor}" font-family="Yomogi" font-size="${size}" fill="${color}" stroke="${color}" stroke-width="${size / 30}" stroke-linejoin="round" paint-order="stroke" style="opacity:0">${str}</text>`;
// Circle as a single path (starts at the left, clockwise), so it can be drawn like any stroke.
export const circlePath = (cx, cy, r) => `M${cx - r} ${cy} A${r} ${r} 0 1 1 ${cx + r} ${cy} A${r} ${r} 0 1 1 ${cx - r} ${cy}`;

const HEAD = `<link href="https://fonts.googleapis.com/css2?family=Yomogi&display=block" rel="stylesheet">
<style>.stage{position:relative;width:1280px;height:720px;overflow:hidden}.abs{position:absolute}</style>`;

const BOARD_BG = `<div class="abs" style="left:14px;top:14px;width:1252px;height:676px;background:#fdfdfb;border:10px solid #c9cdd2;border-radius:6px;box-sizing:border-box;box-shadow:inset 0 0 40px rgba(0,0,0,.06)"></div>
<div class="abs" style="left:120px;top:690px;width:1040px;height:16px;background:#b9bec4;border-radius:4px"></div>
<svg class="abs" style="left:0;top:0" width="1280" height="720"><g fill="none" stroke="#eceeec" stroke-linecap="round" opacity=".8"><path d="M160 650 Q420 622 640 656" stroke-width="34"/><path d="M880 110 Q1010 86 1150 122" stroke-width="26"/><path d="M60 300 Q80 380 66 460" stroke-width="18"/></g></svg>`;

const RUNTIME = `
const el = (id) => document.getElementById(id);
const clamp01 = (t) => Math.max(0, Math.min(1, t));
const seg = (t, a, b) => clamp01((t - a) / (b - a));
const ease = (t) => { t = clamp01(t); return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
let geo = null;
const initGeo = () => {
  geo = {};
  [...PAST, ...ITEMS].forEach(([id]) => {
    const e = el(id);
    if (e.tagName === 'text') { geo[id] = { text: true, b: e.getBBox() }; }
    else if (e.tagName === 'IMG') { geo[id] = { text: true, b: { x: e.offsetLeft, y: e.offsetTop, width: e.offsetWidth, height: e.offsetHeight } }; }
    else { const L = e.getTotalLength(); e.style.strokeDasharray = L + ' ' + L; geo[id] = { L }; }
  });
};
const pointOf = (id, p) => {
  const g = geo[id];
  if (g.text) return [g.b.x + g.b.width * p, g.b.y + g.b.height * 0.8];
  const q = el(id).getPointAtLength(g.L * p);
  return [q.x, q.y];
};
const reveal = (id, p) => {
  const e = el(id), g = geo[id];
  e.style.opacity = p > 0 ? 1 : 0;
  if (g.text) e.style.clipPath = 'inset(0 ' + (100 * (1 - p)) + '% 0 0)';
  else e.style.strokeDashoffset = g.L * (1 - p);
};
const lerpArc = (a, b, k) => [a[0] + (b[0] - a[0]) * k, a[1] + (b[1] - a[1]) * k - Math.sin(k * Math.PI) * 25];
const idleHand = (t) => {
  const next = ITEMS.findIndex(([, s]) => s > t);
  if (next === 0) {
    const from = PAST.length ? pointOf(PAST[PAST.length - 1][0], 1) : START;
    return lerpArc(from, pointOf(ITEMS[0][0], 0), ease(seg(t, 0, ITEMS[0][1])));
  }
  const last = ITEMS[(next === -1 ? ITEMS.length : next) - 1];
  const from = pointOf(last[0], 1);
  if (next !== -1) return lerpArc(from, pointOf(ITEMS[next][0], 0), ease(seg(t, last[2], ITEMS[next][1])));
  if (!IS_LAST) return from;
  const k = ease(seg(t, last[2], last[2] + 0.4));
  return [from[0] + (EXIT[0] - from[0]) * k, from[1] + (EXIT[1] - from[1]) * k];
};
async function render(frame, totalFrames, fps) {
  if (!geo) { await document.fonts.ready; initGeo(); }
  const t = frame / fps;
  PAST.forEach(([id]) => reveal(id, 1));
  let hand = null;
  ITEMS.forEach(([id, s, e]) => {
    const p = seg(t, s, e);
    reveal(id, p);
    if (t >= s && t <= e) hand = pointOf(id, p);
  });
  if (!hand) hand = idleHand(t);
  const wobble = Math.sin(t * 23) * 1.5;
  el('hand').style.transform = 'translate(' + (hand[0] - TIP[0] + wobble) + 'px,' + (hand[1] - TIP[1] + wobble) + 'px)';
}`;

// beats: [{ id, items: [[elementId, startSec, endSec], ...] }]; svg: the full board markup (all beats' elements).
export const buildBoardBeats = (beats, svg, handSrc, overlayHtml = "") =>
  beats.map((beat, index) => {
    const past = beats.slice(0, index).flatMap((b) => b.items);
    const isLast = index === beats.length - 1;
    return {
      type: "html_tailwind",
      html: `${HEAD}<div class="stage" style="background:#e9ebe8">${BOARD_BG}
<svg id="board" class="abs" style="left:0;top:0" width="1280" height="720" viewBox="0 0 1280 720">${svg}</svg>
${overlayHtml}
<img id="hand" class="abs" src="${handSrc}" style="left:0;top:0;width:${HAND_W}px;height:${HAND_W}px"></div>`,
      script: `const ITEMS = ${JSON.stringify(beat.items)};
const PAST = ${JSON.stringify(past)};
const IS_LAST = ${isLast};
const TIP = ${JSON.stringify(TIP)};
const START = ${JSON.stringify(EXIT)};
const EXIT = ${JSON.stringify(EXIT)};
${RUNTIME}`,
      animation: true,
    };
  });
