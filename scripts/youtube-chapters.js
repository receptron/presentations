// YouTube chapter timeline for a rendered MulmoScript deck.
//
// Prints one line per beat: index, start time (m:ss), and the narration text,
// so a human can pick which beats become chapters and write their labels.
// Beat start times are derived from the per-beat audio files under
// output/<deck>/audio/ (the same content-hash naming mulmocast uses), so the
// numbers reflect what was actually rendered.
//
//   node scripts/youtube-chapters.js mulmoclaude/tutorials/collection-creation-demo_ja.json
//   node scripts/youtube-chapters.js <script.json> [--lang ja] [--output-dir output/<deck>]

const fs = require("fs");
const path = require("path");
const crypto = require("crypto");
const { execFileSync } = require("child_process");

const DEFAULT_LANG = "ja";
const DEFAULT_INTRO_PADDING_SEC = 1.0;
const DEFAULT_PADDING_SEC = 0.3;
const TEXT_PREVIEW_CHARS = 42;

const text2hash = (input) => crypto.createHash("sha256").update(input, "utf8").digest("hex");

const parseArgs = (argv) => {
  const args = { scriptPath: null, lang: DEFAULT_LANG, outputDir: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === "--lang") args.lang = argv[++i];
    else if (argv[i] === "--output-dir") args.outputDir = argv[++i];
    else if (!args.scriptPath) args.scriptPath = argv[i];
  }
  return args;
};

// Mirrors mulmocast getBeatAudioPathOrUrl: the audio filename is
// `${studioFilename}_${sha256(hashString)}` with a `_${lang}.mp3` suffix.
const resolveAudioParam = (script, beat) => {
  const speakers = script.speechParams?.speakers ?? {};
  const speakerId = beat.speaker ?? Object.keys(speakers).find((id) => speakers[id]?.isDefault) ?? Object.keys(speakers)[0];
  const speaker = speakers[speakerId] ?? {};
  const speechOptions = { ...(speaker.speechOptions ?? {}), ...(beat.speechOptions ?? {}) };
  return { voiceId: speaker.voiceId ?? "", provider: speaker.provider ?? "", model: speaker.model, speechOptions };
};

const audioHashString = ({ voiceId, provider, model, speechOptions }, text) =>
  [
    text,
    voiceId,
    speechOptions.instruction ?? "",
    speechOptions.speed ?? 1.0,
    provider,
    model ?? "",
    speechOptions.decoration ?? "",
    speechOptions.stability ?? "",
    speechOptions.similarity_boost ?? "",
  ].join(":");

const audioDurationSec = (filePath) => {
  const out = execFileSync(
    "ffprobe",
    ["-v", "quiet", "-show_entries", "format=duration", "-of", "csv=p=0", filePath],
    { encoding: "utf8" },
  );
  const seconds = parseFloat(out.trim());
  if (!Number.isFinite(seconds)) throw new Error(`ffprobe returned no duration for ${filePath}`);
  return seconds;
};

const formatTime = (seconds) => {
  const total = Math.floor(seconds);
  return `${Math.floor(total / 60)}:${String(total % 60).padStart(2, "0")}`;
};

const beatDurationSec = (script, beat, studioFilename, audioDir, lang) => {
  const text = beat.text ?? "";
  if (text.trim() === "") return { seconds: beat.duration ?? 0, hasNarration: false };
  const hash = text2hash(audioHashString(resolveAudioParam(script, beat), text));
  const audioFile = path.join(audioDir, `${studioFilename}_${hash}_${lang}.mp3`);
  if (!fs.existsSync(audioFile)) {
    // No fallback: a missing audio file means the timeline cannot be trusted.
    throw new Error(`Audio file not found for beat text (regenerate audio first):\n  ${audioFile}\n  text: ${text.slice(0, 60)}...`);
  }
  return { seconds: audioDurationSec(audioFile), hasNarration: true };
};

const main = () => {
  const { scriptPath, lang, outputDir } = parseArgs(process.argv.slice(2));
  if (!scriptPath) {
    console.error("Usage: node scripts/youtube-chapters.js <script.json> [--lang ja] [--output-dir output/<deck>]");
    process.exit(1);
  }
  const script = JSON.parse(fs.readFileSync(scriptPath, "utf8"));
  const studioFilename = path.basename(scriptPath, ".json");
  const deckOutputDir = outputDir ?? path.join("output", studioFilename);
  const audioDir = path.join(deckOutputDir, "audio");
  if (!fs.existsSync(audioDir)) {
    console.error(`Audio directory not found: ${audioDir}\nRender the deck first (npm run movie -- ${scriptPath}).`);
    process.exit(1);
  }

  const introPadding = script.audioParams?.introPadding ?? DEFAULT_INTRO_PADDING_SEC;
  const padding = script.audioParams?.padding ?? DEFAULT_PADDING_SEC;

  console.log(`# Chapters for ${studioFilename} (${lang})\n# beat  start  narration`);
  let elapsed = introPadding;
  script.beats.forEach((beat, index) => {
    const { seconds, hasNarration } = beatDurationSec(script, beat, studioFilename, audioDir, lang);
    // YouTube requires the first chapter to be 0:00.
    const start = index === 0 ? 0 : elapsed;
    const preview = hasNarration ? (beat.text ?? "").slice(0, TEXT_PREVIEW_CHARS) : "(no narration)";
    console.log(`${String(index + 1).padStart(3)}  ${formatTime(start).padStart(5)}  ${preview}`);
    elapsed += seconds + padding;
  });
  console.log(`\n# total ~${formatTime(elapsed)} (excludes closing/outro padding)`);
};

main();
