// Builds mulmocast/promo-30s_ja.json in place (keeps narration/speech settings from the existing file).
// usage (from the repo root): node mulmocast/promo-30s-build/build.mjs mulmocast/promo-30s_ja.json
import fs from "node:fs";
import { manSVG, MAN_JS } from "./man.mjs";

const OUT = process.argv[2];
const base = JSON.parse(fs.readFileSync(OUT, "utf8"));

const HEAD = `<link href="https://fonts.googleapis.com/css2?family=Yomogi&family=Zen+Maru+Gothic:wght@700;900&display=block" rel="stylesheet">
<style>
.stage{position:relative;width:1280px;height:720px;overflow:hidden;font-family:'Zen Maru Gothic',sans-serif;color:#222;}
.abs{position:absolute;}
.hand{font-family:'Yomogi',cursive;color:#333;}
.ln{fill:none;stroke:#222;stroke-width:3;stroke-linecap:round;stroke-linejoin:round;}
.fw{fill:#fff;stroke:#222;stroke-width:3;stroke-linejoin:round;}
.olabel{position:absolute;background:#ea8c6c;color:#fff;font-weight:900;padding:6px 22px;white-space:nowrap;clip-path:polygon(0 0,100% 0,97% 50%,100% 100%,0 100%,3% 50%);}
.ntag{position:absolute;background:#233a8b;color:#fff;font-weight:900;padding:6px 20px;white-space:nowrap;}
.card{background:#fff;border:4px solid #222;border-radius:10px;box-shadow:8px 8px 0 #233a8b;}
.mult{mix-blend-mode:multiply;}
</style>`;

// ---------- shared runtime helpers ----------
const COMMON_JS = `
const el = (id) => document.getElementById(id);
const clamp01 = (t) => Math.max(0, Math.min(1, t));
const seg = (t, a, b) => clamp01((t - a) / (b - a));
const ease = (t) => { t = clamp01(t); return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; };
const back = (t) => { t = clamp01(t); const c1 = 1.70158, c3 = c1 + 1; return 1 + c3 * Math.pow(t - 1, 3) + c1 * Math.pow(t - 1, 2); };
const pop = (id, t, start, dur = 0.35) => { const k = back(seg(t, start, start + dur)); const e = el(id); e.style.transform = 'scale(' + k + ')'; e.style.opacity = seg(t, start, start + 0.08); };
let fontsReady = false;
const waitFonts = async () => { if (!fontsReady) { await document.fonts.ready; fontsReady = true; } };
`;

// Rigged character (drawn by Codex gpt-6-astra): manSVG(id) markup + MAN_JS rig runtime.

// Dark thought cloud (bumps around an ellipse).
const cloudSVG = (w, h) => {
  const cx = w / 2, cy = h / 2, rx = w / 2 - h * 0.18, ry = h / 2 - h * 0.18, r = h * 0.2;
  const bumps = Array.from({ length: 12 }, (_, i) => {
    const a = (i / 12) * Math.PI * 2;
    return `<circle cx="${(cx + Math.cos(a) * rx).toFixed(1)}" cy="${(cy + Math.sin(a) * ry).toFixed(1)}" r="${r.toFixed(1)}"/>`;
  }).join("");
  return `<svg class="abs" style="left:0;top:0" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}"><g fill="#2b2b2b">${bumps}<ellipse cx="${cx}" cy="${cy}" rx="${rx}" ry="${ry}"/></g></svg>`;
};
const cloud = (id, left, top, w, h, text, size, origin) =>
  `<div id="${id}" class="abs" style="left:${left}px;top:${top}px;width:${w}px;height:${h}px;transform-origin:${origin};opacity:0">${cloudSVG(w, h)}<div class="abs" style="inset:0;display:flex;align-items:center;justify-content:center;text-align:center;color:#fff;font-weight:900;font-size:${size}px;line-height:1.2">${text}</div></div>`;

const star = (id, left, top, size, color = "#f5c542") =>
  `<svg id="${id}" class="abs" style="left:${left}px;top:${top}px" width="${size}" height="${size}" viewBox="0 0 100 100"><path d="M50 0 Q56 44 100 50 Q56 56 50 100 Q44 56 0 50 Q44 44 50 0 Z" fill="${color}" stroke="#222" stroke-width="3"/></svg>`;

const desk = (left, top, width) =>
  `<div class="abs" style="left:${left}px;top:${top}px;width:${width}px;height:22px;background:#fff;border:3px solid #222"></div><div class="abs" style="left:${left + 20}px;top:${top + 25}px;width:${width - 40}px;height:${720 - top - 25}px;background:#3a3a3a"></div>`;

const stack = (id, left, top) => {
  const lines = Array.from({ length: 15 }, (_, i) => `<path class="ln" stroke-width="2.5" d="M4 ${158 - i * 10} Q75 ${152 - i * 10} 146 ${158 - i * 10}"/>`).join("");
  return `<svg id="${id}" class="abs" style="left:${left}px;top:${top}px;transform-origin:50% 100%" width="150" height="162" viewBox="0 0 150 162"><rect x="2" y="8" width="146" height="152" fill="#fff"/>${lines}</svg>`;
};

const beatImage = (html, script) => ({
  type: "html_tailwind",
  html: HEAD + html,
  script: COMMON_JS + MAN_JS + script,
  animation: true,
});

// ---------- beat 1: pain ----------
const pain = beatImage(
  `<div class="stage" style="background:#e3ecf1">
<svg class="abs" style="left:60px;top:150px" width="230" height="170"><rect class="fw" x="3" y="3" width="220" height="150"/><rect x="24" y="24" width="50" height="44" fill="#fff" stroke="#222" stroke-width="2"/><rect x="92" y="30" width="50" height="44" fill="#fff" stroke="#222" stroke-width="2"/><rect x="40" y="88" width="50" height="44" fill="#fff" stroke="#222" stroke-width="2"/><path class="ln" d="M20 165 L210 165"/></svg>
<svg class="abs" style="left:1110px;top:150px" width="120" height="120" viewBox="0 0 120 120"><circle class="fw" cx="60" cy="60" r="54" stroke-width="5"/><path class="ln" d="M60 12 L60 20 M60 100 L60 108 M12 60 L20 60 M100 60 L108 60"/><line id="hh" x1="60" y1="60" x2="60" y2="34" class="ln" stroke-width="6"/><line id="mh" x1="60" y1="60" x2="60" y2="18" class="ln" stroke-width="4"/><circle cx="60" cy="60" r="5" fill="#222"/></svg>
<div class="abs" style="left:440px;top:215px;width:400px;height:420px">${manSVG("m")}</div>
${stack("stackL", 320, 395)}${stack("stackR", 810, 395)}
${desk(250, 555, 780)}
<div class="abs" style="left:360px;top:523px;background:#fff;border:3px solid #222;font-weight:900;font-size:22px;padding:0 14px">IN</div>
<div class="abs" style="left:850px;top:523px;background:#fff;border:3px solid #222;font-weight:900;font-size:22px;padding:0 14px">IN</div>
<svg class="abs" style="left:560px;top:500px" width="64" height="58"><path class="fw" d="M8 4 L46 4 L44 54 L10 54 Z" style="fill:#333"/><path class="ln" d="M46 16 Q62 20 45 38"/></svg>
${cloud("b1", 130, 170, 240, 140, "編集", 44, "100% 100%")}
${cloud("b2", 900, 290, 220, 130, "録音", 44, "0% 50%")}
${cloud("b3", 120, 330, 250, 150, "スライド<br>づくり", 36, "100% 30%")}
<div id="note" class="abs hand" style="left:890px;top:450px;font-size:44px;transform:rotate(-5deg)"></div>
<div id="ribbon" class="abs" style="left:240px;top:24px;width:800px;height:90px">
<svg class="abs" style="left:0;top:0" width="800" height="90" viewBox="0 0 800 90"><path class="fw" d="M0 30 L90 30 L90 84 L0 84 L28 57 Z"/><path class="fw" d="M800 30 L710 30 L710 84 L800 84 L772 57 Z"/><path class="fw" d="M60 10 L740 10 L740 70 L60 70 Z" stroke-width="4"/></svg>
<div class="abs" style="left:60px;top:10px;width:680px;height:60px;display:flex;align-items:center;justify-content:center;color:#233a8b;font-weight:900;font-size:36px">動画づくり、手間がかかりすぎ？</div>
</div>
</div>`,
  `
const animation = new MulmoAnimation();
animation.typewriter('#note', '手間ばかり…', { start: 5.0, end: 5.7 });
async function render(frame, totalFrames, fps) {
  await waitFonts();
  const t = frame / fps;
  animation.update(frame, fps);
  el('ribbon').style.transform = 'translateY(' + (1 - back(seg(t, 0.1, 0.6))) * -130 + 'px)';
  el('mh').setAttribute('transform', 'rotate(' + t * 540 + ' 60 60)');
  el('hh').setAttribute('transform', 'rotate(' + t * 45 + ' 60 60)');
  const up = ease(seg(t, 2.4, 2.9));
  const hr = t < 2.9 ? Math.sin(t * 2) * 2 : Math.sin((t - 2.9) * 9) * 5 * Math.min(1, (t - 2.9) / 0.3);
  headRot('m', hr);
  face('m', t < 2.5 ? 'neutral' : 'worried');
  const pl = lerpPose(P.down, P.head, up), pr = mirPose(pl);
  const follow = (p) => ({ E: rotP(p.E, NECK, hr * up * 0.5), H: rotP(p.H, NECK, hr * up) });
  setArm('m', 'L', SL, follow(pl), up > 0.5 ? 'palm' : 'relaxed');
  setArm('m', 'R', SR, follow(pr), up > 0.5 ? 'palm' : 'relaxed');
  blinkEyes('m', t);
  pop('b1', t, 3.3); pop('b2', t, 4.0); pop('b3', t, 4.5);
  const g = 0.3 + 0.7 * ease(seg(t, 3.3, 5.0));
  el('stackL').style.transform = 'scaleY(' + g + ')';
  el('stackR').style.transform = 'scaleY(' + g + ')';
}`,
);

// ---------- beat 2: intro ----------
const codeLines = ["{", '  "title": "新商品のご紹介",', '  "beats": [', '    { "text": "こんにちは！" },', '    { "text": "今日は…" }', "  ]", "}"];
const intro = beatImage(
  `<div class="stage" style="background:#f6f4df">
<div id="logo" class="abs" style="left:0;top:40px;width:1280px;text-align:center;opacity:0"><span style="font-size:124px;font-weight:900;color:#233a8b;letter-spacing:2px">Mulmo<span style="color:#ea8c6c">Cast</span></span></div>
${star("sp1", 300, 60, 56)}${star("sp2", 930, 40, 44)}${star("sp3", 960, 150, 30)}${star("sp4", 270, 170, 28)}
<div id="card" class="abs card" style="left:150px;top:250px;width:590px;height:300px;opacity:0">
<div style="height:42px;border-bottom:3px solid #222;display:flex;align-items:center;gap:8px;padding-left:14px"><span style="width:12px;height:12px;border-radius:50%;background:#ea8c6c"></span><span style="width:12px;height:12px;border-radius:50%;background:#f5c542"></span><span style="width:12px;height:12px;border-radius:50%;background:#7bc47f"></span><span style="margin-left:10px;font:700 18px Menlo,monospace;color:#666">promo.json</span></div>
<pre id="code" style="margin:0;padding:12px 24px;font:700 23px/1.45 Menlo,monospace;color:#233a8b;white-space:pre"></pre>
</div>
<div class="abs" style="left:810px;top:190px;width:400px;height:420px">${manSVG("m")}</div>
${desk(760, 560, 540)}
<svg class="abs" style="left:1150px;top:500px" width="60" height="60"><path class="fw" d="M14 30 L46 30 L42 58 L18 58 Z"/><path class="ln" d="M30 30 Q24 12 12 8 M30 30 Q36 10 50 6 M30 30 L30 4"/></svg>
<div id="lab" class="olabel" style="left:190px;top:590px;font-size:48px">台本を書くだけ</div>
</div>`,
  `
const animation = new MulmoAnimation();
animation.codeReveal('#code', ${JSON.stringify(codeLines)}, { start: 2.6, end: 4.3 });
async function render(frame, totalFrames, fps) {
  await waitFonts();
  const t = frame / fps;
  animation.update(frame, fps);
  const lk = back(seg(t, 1.15, 1.65));
  el('logo').style.transform = 'scale(' + lk + ')';
  el('logo').style.opacity = seg(t, 1.15, 1.25);
  ['sp1', 'sp2', 'sp3', 'sp4'].forEach((id, i) => {
    const k = back(seg(t, 1.55 + i * 0.1, 1.85 + i * 0.1)) * (1 + Math.sin(t * 6 + i) * 0.15);
    el(id).style.transform = 'scale(' + k + ') rotate(' + t * 40 * (i % 2 ? -1 : 1) + 'deg)';
  });
  el('card').style.opacity = seg(t, 2.2, 2.45);
  el('card').style.transform = 'translateY(' + (1 - ease(seg(t, 2.2, 2.6))) * 60 + 'px)';
  el('lab').style.transform = 'translateX(' + (1 - back(seg(t, 2.65, 3.05))) * -800 + 'px)';
  face('m', 'happy');
  const pt = ease(seg(t, 2.3, 2.7));
  let pl = lerpPose(P.down, P.point, pt);
  if (t > 2.7) pl = { E: pl.E, H: rotP(pl.H, pl.E, Math.sin((t - 2.7) * 8) * 6) };
  setArm('m', 'L', SL, pl, pt > 0.4 ? 'point' : 'relaxed');
  setArm('m', 'R', SR, mirPose(P.down), 'relaxed');
  headRot('m', -4 * pt + Math.sin(t * 3) * 2);
  blinkEyes('m', t, 0.7);
}`,
);

// ---------- beat 3: generate ----------
const tileBox = (id, top, inner) =>
  `<div id="${id}" class="abs card" style="left:800px;top:${top}px;width:150px;height:150px;opacity:0;overflow:hidden">${inner}</div>`;
const bars = (prefix, n, x0, gap, w, color) =>
  Array.from({ length: n }, (_, i) => `<rect id="${prefix}${i}" x="${x0 + i * gap}" y="60" width="${w}" height="30" rx="${w / 2}" fill="${color}"/>`).join("");
const generate = beatImage(
  `<div class="stage" style="background:#f6f4df">
<div id="tag" class="ntag" style="left:60px;top:40px;font-size:42px;opacity:0">AIがまとめて生成</div>
<svg class="abs" style="left:0;top:0" width="1280" height="720"><path id="a1" class="ln" d="M660 380 Q730 230 796 185" stroke-width="5" stroke-dasharray="400" stroke-dashoffset="400"/><path id="a2" class="ln" d="M670 380 L796 375" stroke-width="5" stroke-dasharray="400" stroke-dashoffset="400"/><path id="a3" class="ln" d="M660 390 Q730 530 796 565" stroke-width="5" stroke-dasharray="400" stroke-dashoffset="400"/></svg>
<div class="abs" style="left:0;top:300px;width:340px;height:357px">${manSVG("m")}</div>
${desk(-20, 600, 480)}
<svg class="abs" style="left:95px;top:505px" width="180" height="96"><path class="fw" d="M10 3 L170 3 L160 93 L20 93 Z" style="fill:#dfe3e6"/><circle cx="90" cy="50" r="9" fill="#bbb"/><path d="M104 20 L140 17 L140 29 L104 32 Z" fill="#233a8b"/></svg>
${[1, 2, 3].map((i) => `<svg id="f${i}" class="abs" style="left:0;top:0;opacity:0" width="44" height="54"><path class="fw" d="M3 3 L30 3 L41 14 L41 51 L3 51 Z"/><path class="ln" d="M10 20 L33 20 M10 29 L33 29 M10 38 L26 38" stroke-width="2.5"/></svg>`).join("")}
<div id="ai" class="abs" style="left:490px;top:300px;width:170px;height:170px"><svg width="170" height="170" viewBox="0 0 170 170"><circle id="ring" cx="85" cy="85" r="78" fill="none" stroke="#ea8c6c" stroke-width="6" stroke-dasharray="22 12"/><circle cx="85" cy="85" r="64" fill="#233a8b" stroke="#222" stroke-width="4"/><text x="85" y="104" text-anchor="middle" font-size="56" font-weight="900" fill="#fff" font-family="Zen Maru Gothic">AI</text></svg></div>
${tileBox("t1", 110, `<svg width="150" height="150" viewBox="0 0 150 150"><g transform="translate(0 0)">${bars("w", 9, 17, 14, 8, "#233a8b")}</g></svg>`)}
${tileBox("t2", 300, `<svg width="150" height="150" viewBox="0 0 150 150"><rect x="0" y="0" width="150" height="150" fill="#dff0f7"/><circle id="sun" cx="104" cy="120" r="18" fill="#f5c542" stroke="#222" stroke-width="3"/><path class="fw" d="M-4 150 L40 70 L70 112 L96 84 L154 150 Z" style="fill:#9fd39a"/></svg>`)}
${tileBox("t3", 490, `<svg width="150" height="150" viewBox="0 0 150 150"><rect x="14" y="22" width="122" height="84" rx="8" fill="#333"/><path d="M64 46 L64 82 L94 64 Z" fill="#fff"/><rect x="14" y="118" width="122" height="10" rx="5" fill="#ddd"/><rect id="pb" x="14" y="118" width="0" height="10" rx="5" fill="#ea8c6c"/></svg>`)}
<div id="l1" class="olabel" style="left:975px;top:160px;font-size:34px">ナレーション</div>
<div id="l2" class="olabel" style="left:975px;top:350px;font-size:34px">画像</div>
<div id="l3" class="olabel" style="left:975px;top:540px;font-size:34px">動画生成</div>
</div>`,
  `
async function render(frame, totalFrames, fps) {
  await waitFonts();
  const t = frame / fps;
  // typing man
  face('m', t < 4.0 ? 'neutral' : 'happy');
  const tp = (ph) => ({ E: [P.down.E[0], P.down.E[1] + Math.sin(t * 22 + ph) * 5], H: P.down.H });
  setArm('m', 'L', SL, tp(0), 'relaxed');
  setArm('m', 'R', SR, mirPose(tp(Math.PI)), 'relaxed');
  headRot('m', Math.sin(t * 4) * 2);
  blinkEyes('m', t, 0.3);
  // sheets fly from laptop to AI
  [1, 2, 3].forEach((i) => {
    const ph = ((t - 0.1) / 1.2 + i / 3) % 1;
    const on = t > 0.1 ? 1 : 0;
    const x = 185 + (545 - 185) * ph, y = 500 - Math.sin(ph * Math.PI) * 170 - ph * 110;
    const e = el('f' + i);
    e.style.transform = 'translate(' + x + 'px,' + y + 'px) rotate(' + ph * 200 + 'deg) scale(' + (1 - ph * 0.4) + ')';
    e.style.opacity = on * Math.min(1, Math.sin(ph * Math.PI) * 3);
  });
  // AI core
  el('ring').setAttribute('transform', 'rotate(' + t * 90 + ' 85 85)');
  const pulse = 1 + 0.15 * Math.sin(seg(t, 4.0, 4.5) * Math.PI);
  el('ai').style.transform = 'scale(' + pulse + ')';
  // outputs
  [[1, 0.55], [2, 1.95], [3, 3.05]].forEach(([i, s]) => {
    el('a' + i).setAttribute('stroke-dashoffset', 400 * (1 - ease(seg(t, s - 0.3, s))));
    pop('t' + i, t, s);
    el('l' + i).style.transform = 'translateX(' + (1 - back(seg(t, s + 0.1, s + 0.45))) * 400 + 'px)';
  });
  for (let i = 0; i < 9; i++) {
    const h = t > 0.55 ? 16 + Math.abs(Math.sin(t * 9 + i * 1.3)) * 60 : 16;
    const b = el('w' + i); b.setAttribute('height', h); b.setAttribute('y', 75 - h / 2);
  }
  el('sun').setAttribute('cy', 120 - 70 * ease(seg(t, 2.0, 3.0)));
  el('pb').setAttribute('width', 122 * seg(t, 3.1, 5.7));
  const tg = back(seg(t, 4.05, 4.45));
  el('tag').style.opacity = seg(t, 4.05, 4.15);
  el('tag').style.transform = 'scale(' + tg + ')';
}`,
);

// ---------- beat 4: formats ----------
const outBox = (id, cx, inner) => `<div id="${id}" class="abs card" style="left:${cx - 140}px;top:300px;width:280px;height:220px;opacity:0;overflow:hidden">${inner}</div>`;
const formats = beatImage(
  `<div class="stage" style="background:#f6f4df">
<svg class="abs" style="left:0;top:0" width="1280" height="720"><path id="c1" class="ln" d="M600 215 Q360 230 250 300" stroke-width="4" stroke-dasharray="10 10" style="opacity:0"/><path id="c2" class="ln" d="M640 215 L640 300" stroke-width="4" stroke-dasharray="10 10" style="opacity:0"/><path id="c3" class="ln" d="M680 215 Q920 230 1030 300" stroke-width="4" stroke-dasharray="10 10" style="opacity:0"/></svg>
<div id="card" class="abs card" style="left:540px;top:60px;width:200px;height:150px;display:flex;flex-direction:column;align-items:center;justify-content:center"><div style="font-size:46px;font-weight:900;color:#233a8b">台本</div><div style="font:700 18px Menlo,monospace;color:#888">promo.json</div></div>
<div id="note" class="abs hand" style="left:800px;top:70px;font-size:40px;transform:rotate(-4deg)"></div>
${outBox("o1", 240, `<svg width="280" height="220" viewBox="0 0 280 220"><rect x="96" y="30" width="110" height="150" fill="#fff" stroke="#222" stroke-width="3"/><rect x="86" y="38" width="110" height="150" fill="#fff" stroke="#222" stroke-width="3"/><path class="ln" d="M100 70 L180 70 M100 90 L180 90 M100 110 L160 110" stroke-width="2.5"/><g id="flip"><rect x="86" y="38" width="110" height="150" fill="#fff" stroke="#222" stroke-width="3"/><path class="ln" d="M100 70 L180 70 M100 90 L180 90 M100 110 L160 110" stroke-width="2.5"/></g><rect x="150" y="140" width="70" height="36" rx="6" fill="#e0413a" stroke="#222" stroke-width="3"/><text x="185" y="166" text-anchor="middle" font-size="22" font-weight="900" fill="#fff">PDF</text></svg>`)}
${outBox("o2", 640, `<svg width="280" height="220" viewBox="0 0 280 220"><rect x="116" y="30" width="48" height="84" rx="24" fill="#233a8b" stroke="#222" stroke-width="3"/><path class="ln" d="M98 90 Q98 140 140 140 Q182 140 182 90 M140 140 L140 170 M112 172 L168 172" stroke-width="4"/>${bars("pw", 4, 30, 16, 8, "#ea8c6c")}${bars("px", 4, 202, 16, 8, "#ea8c6c")}<text id="ptime" x="140" y="205" text-anchor="middle" font-size="20" font-weight="700" fill="#444">▶ 0:00</text></svg>`)}
${outBox("o3", 1040, `<svg width="280" height="220" viewBox="0 0 280 220"><circle cx="90" cy="120" r="62" fill="#dff0f7" stroke="#222" stroke-width="3"/><ellipse id="mer" cx="90" cy="120" rx="30" ry="62" fill="none" stroke="#222" stroke-width="2.5"/><path class="ln" d="M28 120 L152 120 M38 88 L142 88 M38 152 L142 152" stroke-width="2.5"/><path class="fw" d="M150 30 L266 30 Q274 30 274 38 L274 86 Q274 94 266 94 L178 94 L162 112 L166 94 L150 94 Q142 94 142 86 L142 38 Q142 30 150 30 Z"/></svg><div id="lang" class="abs" style="left:142px;top:30px;width:132px;height:64px;display:flex;align-items:center;justify-content:center;font-weight:900;font-size:24px;color:#233a8b"></div>`)}
<div class="abs" style="left:100px;top:545px;width:280px;display:flex;justify-content:center"><div id="l1" class="olabel" style="position:relative;font-size:32px">PDF</div></div>
<div class="abs" style="left:500px;top:545px;width:280px;display:flex;justify-content:center"><div id="l2" class="olabel" style="position:relative;font-size:32px">ポッドキャスト</div></div>
<div class="abs" style="left:900px;top:545px;width:280px;display:flex;justify-content:center"><div id="l3" class="olabel" style="position:relative;font-size:32px">多言語</div></div>
</div>`,
  `
const animation = new MulmoAnimation();
animation.typewriter('#note', 'ぜんぶ同じ台本から！', { start: 0.05, end: 0.75 });
const langs = ['こんにちは', 'Hello', '你好', 'Bonjour', 'Hola', '안녕하세요'];
async function render(frame, totalFrames, fps) {
  await waitFonts();
  const t = frame / fps;
  animation.update(frame, fps);
  el('card').style.transform = 'scale(' + (1 + 0.04 * Math.sin(t * 5)) + ')';
  [[1, 240, 0.75], [2, 640, 2.1], [3, 1040, 3.5]].forEach(([i, cx, s]) => {
    const k = back(seg(t, s, s + 0.45));
    const e = el('o' + i);
    e.style.opacity = seg(t, s, s + 0.08);
    e.style.transform = 'translate(' + (640 - cx) * (1 - k) + 'px,' + (-270) * (1 - k) + 'px) scale(' + (0.2 + 0.8 * k) + ')';
    el('c' + i).style.opacity = seg(t, s, s + 0.2);
    const lk = back(seg(t, s + 0.2, s + 0.5));
    el('l' + i).style.transform = 'scale(' + lk + ')';
  });
  const ph = (t % 0.9) / 0.9;
  const sx = Math.cos(ph * Math.PI);
  el('flip').setAttribute('transform', 'translate(86 0) scale(' + sx + ' 1) translate(-86 0)');
  for (let i = 0; i < 4; i++) {
    ['pw', 'px'].forEach((p, j) => {
      const h = 14 + Math.abs(Math.sin(t * 8 + i * 1.1 + j)) * 50;
      const b = el(p + i); b.setAttribute('height', h); b.setAttribute('y', 72 - h / 2);
    });
  }
  const sec = Math.floor(Math.max(0, t - 2.1) * 4);
  el('ptime').textContent = '▶ 0:' + String(sec).padStart(2, '0');
  el('mer').setAttribute('rx', Math.abs(Math.cos(t * 2.4)) * 60);
  el('lang').textContent = langs[Math.floor(Math.max(0, t - 3.5) / 0.4) % langs.length];
}`,
);

// ---------- beat 5: happy (split screen) ----------
const happy = beatImage(
  `<div class="stage" style="background:#e3ecf1">
<div class="abs card" style="left:50px;top:50px;width:540px;height:170px;padding:18px 24px;font:700 26px/1.9 Menlo,monospace;color:#233a8b">
<div>"text": "<span style="position:relative">こんにちは！<span id="strike" class="abs" style="left:0;top:48%;height:5px;width:0;background:#e0413a"></span></span>"</div>
<div>"text": "<span id="new" style="color:#e0413a"></span>"</div>
</div>
<svg id="pencil" class="abs" style="left:0;top:0" width="70" height="70" viewBox="0 0 70 70"><path d="M8 62 L16 42 L52 6 L64 18 L28 54 Z" fill="#f5c542" stroke="#222" stroke-width="3" stroke-linejoin="round"/><path d="M8 62 L16 42 L28 54 Z" fill="#fff" stroke="#222" stroke-width="3" stroke-linejoin="round"/></svg>
<div class="abs" style="left:120px;top:250px;width:400px;height:420px">${manSVG("m")}</div>
${desk(0, 600, 660)}
<div id="rp" class="abs" style="left:640px;top:0;width:640px;height:720px;background:#f6f4df;border-left:5px solid #222">
<img id="cheer" class="abs mult" src="image:cheer_man_v2" style="left:90px;top:110px;width:470px;height:470px;object-fit:contain">
<svg id="regen" class="abs" style="left:40px;top:40px" width="120" height="120" viewBox="0 0 120 120"><path d="M60 16 A44 44 0 1 1 18 72" fill="none" stroke="#ea8c6c" stroke-width="12" stroke-linecap="round"/><path d="M60 0 L82 18 L58 34 Z" fill="#ea8c6c"/></svg>
<div id="ver" class="abs" style="left:470px;top:50px;background:#233a8b;color:#fff;font-weight:900;font-size:40px;padding:4px 22px;border-radius:30px">v1</div>
${star("s1", 110, 420, 50)}${star("s2", 500, 180, 40)}${star("s3", 540, 470, 34)}
</div>
<div id="band" class="abs" style="left:0;top:612px;width:1060px;height:84px;background:#233a8b;color:#fff;font-size:46px;font-weight:900;display:flex;align-items:center;padding-left:70px;clip-path:polygon(0 0,94% 0,100% 50%,94% 100%,0 100%)">何度でも、作り直せる</div>
</div>`,
  `
const animation = new MulmoAnimation();
animation.typewriter('#new', 'はじめまして！', { start: 1.35, end: 2.0 });
animation.counter('#ver', [1, 5], { start: 2.7, end: 4.7, prefix: 'v', decimals: 0 });
async function render(frame, totalFrames, fps) {
  await waitFonts();
  const t = frame / fps;
  animation.update(frame, fps);
  el('strike').style.width = 100 * ease(seg(t, 0.9, 1.3)) + '%';
  const px = t < 1.3 ? 170 + 180 * seg(t, 0.9, 1.3) : 170 + 200 * seg(t, 1.35, 2.0);
  const py = t < 1.3 ? 60 : 110;
  el('pencil').style.transform = 'translate(' + (px + Math.sin(t * 30) * 3) + 'px,' + (py + Math.cos(t * 30) * 3) + 'px)';
  el('pencil').style.opacity = 1 - seg(t, 2.05, 2.2);
  // left man: types, then cheers
  const ch = ease(seg(t, 2.4, 2.8));
  const tp = (ph) => ({ E: [P.down.E[0], P.down.E[1] + Math.sin(t * 22 + ph) * 5 * (1 - ch)], H: P.down.H });
  const bounce = ch * Math.abs(Math.sin((t - 2.4) * 7)) * 10;
  const cl = lerpPose(tp(0), { E: [P.cheer.E[0], P.cheer.E[1] - bounce], H: [P.cheer.H[0], P.cheer.H[1] - bounce] }, ch);
  setArm('m', 'L', SL, cl, ch > 0.5 ? 'fist' : 'relaxed');
  setArm('m', 'R', SR, mirPose(lerpPose(tp(Math.PI), { E: [P.cheer.E[0], P.cheer.E[1] - bounce], H: [P.cheer.H[0], P.cheer.H[1] - bounce] }, ch)), ch > 0.5 ? 'fist' : 'relaxed');
  face('m', t < 2.4 ? 'neutral' : 'happy');
  headRot('m', ch * Math.sin(t * 7) * 4);
  blinkEyes('m', t, 1.1);
  // right panel slides in
  el('rp').style.transform = 'translateX(' + (1 - ease(seg(t, 2.2, 2.6))) * 660 + 'px)';
  el('cheer').style.transform = 'translateY(' + -Math.abs(Math.sin(t * 6)) * 14 + 'px) rotate(' + Math.sin(t * 6) * 2 + 'deg)';
  el('regen').style.transform = 'rotate(' + t * 300 + 'deg)';
  ['s1', 's2', 's3'].forEach((id, i) => {
    el(id).style.transform = 'scale(' + (0.6 + 0.4 * Math.abs(Math.sin(t * 4 + i))) + ') rotate(' + t * 60 + 'deg)';
  });
  el('band').style.transform = 'translateX(' + (1 - ease(seg(t, 2.6, 3.0))) * -1100 + 'px)';
}`,
);

// ---------- beat 6: cta ----------
const cta = beatImage(
  `<div class="stage" style="background:#f6f4df">
<img id="wa" class="abs mult" src="image:woman_a_v2" style="left:20px;top:120px;width:580px;height:580px;object-fit:contain">
<img id="wb" class="abs mult" src="image:woman_b_v2" style="left:20px;top:120px;width:580px;height:580px;object-fit:contain;opacity:0">
<div id="badge" class="abs" style="left:660px;top:50px;width:440px;height:440px;border-radius:50%;background:#fff;border:6px solid #222;display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0">
<div style="font-size:40px;font-weight:900;color:#222">オープンソース</div>
<div style="font-size:104px;font-weight:900;color:#233a8b;line-height:1.02;text-align:center">Mulmo<br><span style="color:#ea8c6c">Cast</span></div>
</div>
${star("s1", 640, 60, 70)}${star("s2", 1070, 120, 50)}${star("s3", 1080, 400, 64, "#f2a58e")}${star("s4", 650, 400, 40)}
<div id="term" class="abs" style="left:620px;top:530px;width:580px;height:72px;background:#222;border-radius:14px;color:#fff;font:700 30px Menlo,monospace;display:flex;align-items:center;padding-left:26px;opacity:0"><span style="color:#7ee787">$&nbsp;</span><span id="cmd"></span><span id="cur">▋</span></div>
<div id="url" class="abs" style="left:620px;top:625px;width:580px;text-align:center;font-size:26px;font-weight:700;color:#233a8b;opacity:0">github.com/receptron/mulmocast-cli</div>
</div>`,
  `
const animation = new MulmoAnimation();
animation.typewriter('#cmd', 'npm install -g mulmocast', { start: 2.1, end: 3.2 });
animation.blink('#cur', { interval: 0.3 });
async function render(frame, totalFrames, fps) {
  await waitFonts();
  const t = frame / fps;
  animation.update(frame, fps);
  pop('badge', t, 0.2, 0.5);
  ['s1', 's2', 's3', 's4'].forEach((id, i) => {
    const k = back(seg(t, 0.5 + i * 0.12, 0.8 + i * 0.12)) * (0.8 + 0.25 * Math.sin(t * 5 + i * 2));
    el(id).style.transform = 'scale(' + k + ') rotate(' + t * 50 * (i % 2 ? -1 : 1) + 'deg)';
  });
  const sw = ease(seg(t, 2.5, 2.7));
  const bob = 'translateY(' + Math.sin(t * 3) * 6 + 'px)';
  el('wa').style.opacity = 1 - sw; el('wa').style.transform = bob;
  el('wb').style.opacity = sw; el('wb').style.transform = bob;
  el('term').style.opacity = seg(t, 1.9, 2.05);
  el('term').style.transform = 'translateY(' + (1 - ease(seg(t, 1.9, 2.2))) * 40 + 'px)';
  el('url').style.opacity = seg(t, 3.0, 3.4);
}`,
);

const STYLE =
  "Clean black-and-white line art in exactly the same drawing style as the reference image: smooth ink outlines, flat white fills, no gray shading, no hatching, no gradients, navy blue (#233a8b) used only on the necktie or bow. Pure white background. No text, no letters, no frame, no border, no ground shadow.";
const MAN_REF = { source: { kind: "path", path: "promo-30s-assets/man_ref.png" } };

const out = {
  ...base,
  imageParams: {
    provider: "google",
    model: "gemini-3-pro-image-preview",
    images: {
      cheer_man_v2: {
        type: "imagePrompt",
        canvasSize: { width: 1024, height: 1024 },
        references: [{ ...MAN_REF, label: "the character to draw (same face, hair, glasses, shirt, navy tie and line style)" }],
        prompt: `${STYLE} The same young office worker as the reference, now sitting behind a desk with an open laptop, both fists raised high in celebration, big happy open-mouth smile. Upper body visible, centered.`,
      },
      woman_a_v2: {
        type: "imagePrompt",
        canvasSize: { width: 1024, height: 1024 },
        references: [{ ...MAN_REF, label: "drawing-style reference only (a different person)" }],
        prompt: `${STYLE} A different character drawn in the same style as the reference: a young Japanese woman with a sleek black bob haircut and round glasses, white blouse with a small navy bow, sitting at a desk behind an open laptop, smiling confidently toward the viewer, hands resting on the desk. Upper body visible, centered.`,
      },
      woman_b_v2: {
        type: "imagePrompt",
        canvasSize: { width: 1024, height: 1024 },
        referenceImageName: "woman_a_v2",
        prompt: `${STYLE} The same woman as in the reference image, same outfit, same desk and laptop, same drawing style and same framing, now giving a thumbs-up with her right hand next to her face and winking cheerfully.`,
      },
    },
  },
  // BGM made with ElevenLabs Music, sections matched to the scene boundaries.
  audioParams: { ...(base.audioParams ?? {}), bgm: { kind: "path", path: "../resources/bgms/mulmocast-promo-30s.mp3" }, bgmVolume: 0.3 },
  movieParams: { transition: { type: "fade", duration: 0.3 } },
  beats: base.beats.map((b) => ({ ...b, image: { pain, intro, generate, formats, happy, cta }[b.id] })),
};

fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + "\n");
