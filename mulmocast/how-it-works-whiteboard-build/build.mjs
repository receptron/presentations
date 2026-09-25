// Builds mulmocast/how-it-works-whiteboard_ja.json in place from the narration already in that file.
// usage (from the repo root): node mulmocast/how-it-works-whiteboard-build/build.mjs mulmocast/how-it-works-whiteboard_ja.json
import fs from "node:fs";
import { buildBoardBeats, stroke, text, circlePath, INK, RED, BLUE } from "./board.mjs";

const OUT = process.argv[2];
const base = JSON.parse(fs.readFileSync(OUT, "utf8"));

// ---------- the board (all beats' elements; each beat reveals its own) ----------
const node = (x, y) => circlePath(x, y, 15);

const SVG = [
  // title
  text("title", 640, 92, 60, "MulmoCast のしくみ"),
  stroke("titleLine", "M420 116 Q640 104 860 118", RED, 5),
  // script sheet
  stroke("sheet", "M70 190 L200 190 L230 220 L230 400 L70 400 Z M200 190 L200 220 L230 220"),
  text("sBeats", 88, 250, 26, "beats: [", BLUE, "start"),
  text("sWords", 108, 292, 26, "ことば", BLUE, "start"),
  text("sPics", 108, 334, 26, "絵の説明", BLUE, "start"),
  text("sEnd", 88, 376, 26, "]", BLUE, "start"),
  text("sLabel", 150, 446, 34, "台本"),
  // GraphAI
  stroke("arrow1", "M245 300 L365 300 M365 300 L347 288 M365 300 L347 312"),
  stroke("gNodes", [node(420, 250), node(520, 250), node(470, 305), node(420, 360), node(520, 360)].join(" ")),
  stroke("gEdges", "M431 261 L459 294 M509 261 L481 294 M459 316 L431 349 M481 316 L509 349 M435 250 L505 250", INK, 4),
  text("gLabel", 470, 430, 34, "GraphAI"),
  // agents: voice + pictures
  stroke("arrow2", "M555 285 Q610 225 672 212 M672 212 L652 204 M672 212 L656 226"),
  stroke("mic", "M725 165 Q725 145 745 145 Q765 145 765 165 L765 205 Q765 225 745 225 Q725 225 725 205 Z M710 195 Q710 245 745 245 Q780 245 780 195 M745 245 L745 262 M725 264 L765 264"),
  text("micLabel", 745, 300, 28, "音声合成"),
  stroke("arrow3", "M555 320 Q610 380 672 392 M672 392 L652 384 M672 392 L656 406"),
  stroke("pic", "M695 350 L800 350 L800 430 L695 430 Z M700 425 L730 390 L752 412 L768 396 L796 425"),
  stroke("sun", circlePath(778, 370, 9), RED, 4),
  text("picLabel", 748, 470, 28, "画像生成"),
  // assemble
  stroke("arrow4", "M815 210 Q870 230 885 262 M885 262 L867 252 M885 262 L889 242"),
  stroke("arrow5", "M815 392 Q870 372 885 340 M885 340 L867 350 M885 340 L889 360"),
  stroke("arrow6", "M1016 300 L1052 300 M1052 300 L1036 290 M1052 300 L1036 310"),
  stroke("screen", "M1062 245 L1212 245 L1212 355 L1062 355 Z"),
  stroke("play", "M1122 275 L1122 325 L1162 300 Z", RED, 5),
  text("movieLabel", 1137, 398, 34, "動画！", RED),
  // outputs
  stroke("arrow7", "M1100 420 L1080 470 M1080 470 L1076 450 M1080 470 L1094 458 M1175 420 L1195 470 M1195 470 L1181 458 M1195 470 L1199 450"),
  stroke("pdf", "M1045 485 L1090 485 L1108 503 L1108 570 L1045 570 Z M1060 520 L1095 520 M1060 540 L1095 540"),
  text("pdfLabel", 1076, 606, 24, "PDF", RED),
  stroke("pod", "M1175 495 Q1175 482 1190 482 Q1205 482 1205 495 L1205 525 Q1205 538 1190 538 Q1175 538 1175 525 Z M1165 518 Q1165 555 1190 555 Q1215 555 1215 518 M1190 555 L1190 568", BLUE, 4),
  text("podLabel", 1190, 606, 24, "ポッドキャスト", BLUE),
  stroke("scriptCircle", "M58 200 Q48 120 150 128 Q250 130 246 250 Q244 470 150 468 Q52 468 56 300 Q55 250 64 215", RED, 5),
  text("punch", 470, 600, 46, "台本を書くだけ！", RED),
].join("\n");

// ---------- timings (local seconds per beat, aligned to measured narration pauses) ----------
const BEATS = [
  { id: "title", items: [["title", 0.3, 1.6], ["titleLine", 1.7, 2.2]] },
  { id: "script", items: [["sheet", 0.9, 1.6], ["sBeats", 1.7, 2.2], ["sWords", 3.15, 3.7], ["sPics", 4.4, 5.1], ["sEnd", 5.2, 5.3], ["sLabel", 5.5, 6.1]] },
  { id: "graphai", items: [["arrow1", 0.1, 0.35], ["gNodes", 0.35, 1.0], ["gLabel", 1.0, 1.5], ["gEdges", 2.3, 3.0]] },
  { id: "agents", items: [["arrow2", 0.1, 0.3], ["mic", 0.3, 0.9], ["micLabel", 1.0, 1.6], ["arrow3", 2.4, 2.6], ["pic", 2.6, 3.1], ["sun", 3.1, 3.3], ["picLabel", 3.3, 3.9]] },
  { id: "assemble", items: [["arrow4", 1.55, 1.8], ["arrow5", 1.8, 2.05], ["ffLogo", 2.05, 2.9], ["arrow6", 3.0, 3.2], ["screen", 3.2, 3.7], ["play", 3.7, 3.9], ["movieLabel", 3.9, 4.4]] },
  { id: "outputs", items: [["scriptCircle", 0.45, 1.05], ["arrow7", 1.3, 1.6], ["pdf", 1.65, 2.1], ["pdfLabel", 2.1, 2.3], ["pod", 2.5, 2.95], ["podLabel", 2.95, 3.3], ["punch", 3.35, 3.85]] },
];

// The FFmpeg project logo (public domain, Wikimedia Commons "FFmpeg_Logo_new.svg"), revealed like handwriting.
const LOGO_W = 150, LOGO_H = Math.round((LOGO_W * 60.19) / 224.44);
const OVERLAY = `<img id="ffLogo" class="abs" src="image:ffmpeg_logo" style="left:${935 - LOGO_W / 2}px;top:${300 - LOGO_H / 2}px;width:${LOGO_W}px;height:${LOGO_H}px;opacity:0">`;
const images = buildBoardBeats(BEATS, SVG, "image:marker_hand", OVERLAY);
const out = {
  ...base,
  imageParams: {
    images: {
      marker_hand: { type: "image", source: { kind: "path", path: "how-it-works-whiteboard-assets/marker_hand.png" } },
      ffmpeg_logo: { type: "image", source: { kind: "path", path: "how-it-works-whiteboard-assets/ffmpeg_logo.svg" } },
    },
  },
  // BGM made with ElevenLabs Music, sections matched to the scene boundaries.
  audioParams: { ...(base.audioParams ?? {}), bgm: { kind: "path", path: "../resources/bgms/mulmocast-how-it-works.mp3" }, bgmVolume: 0.3 },
  beats: base.beats.map((b, i) => ({ ...b, image: images[i] })),
};
fs.writeFileSync(OUT, JSON.stringify(out, null, 2) + "\n");
console.log("wrote", OUT);
