# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

A collection of MulmoCast presentation scripts (JSON) about MulmoClaude/MulmoTerminal — an AI assistant vision for recording, organizing, and presenting people's work and life. There is no application code here; the "source" is MulmoScript JSON files, and the build product is narrated presentation videos.

Scripts live under `mulmoclaude/`, organized by intent: `vision/` (Why), plus planned `demos/` (What) and `tutorials/` (How).

For demo scripts with app screenshots (`mulmoclaude/demos/`), follow `mulmoclaude/demos/DEMO-GUIDE.md` — beat structure, HTML slide snippets, capture conventions, and narration rules distilled from the reviewed `collection-creation-demo.json`.

## Commands

Videos are generated with the `mulmocast` CLI (installed globally, v2.7.x — not a package.json dependency). `mulmo` and `mulmocast` are aliases for the same binary; `mulmo-mcp` is its MCP server:

```sh
npm run movie -- mulmoclaude/vision/<name>.json   # = mulmo movie -g <file>
```

- `-g/--grouped` puts all generated files under `output/<basename>/` (images, per-beat audio, mp3, mp4, studio.json).
- `-f/--force` regenerates everything; without it, unchanged beats are reused via content-hash-cached audio/image files.
- `--estimate` prints API cost estimates without generating.
- `-l <lang>` / `-c <lang>` select narration / caption language.

`npm run viewer -- <file>` generates a single-file HTML slideshow (no audio/video — fast and cheap). `npm run preview -- <file>` (`scripts/preview.js`) serves that viewer at http://localhost:8787 with live reload: on each save it re-runs `mulmo viewer` (cached beats are reused) and auto-refreshes the browser; invalid scripts show an error banner instead. The server exits on its own a few seconds after the last preview tab is closed (`--no-open` suppresses opening a browser tab).

`output/` is gitignored. Generation requires API keys in `.env` (OpenAI for images, Gemini for TTS, Replicate for movie/sound effects, etc.).

## MulmoScript structure

Each script is a single JSON file with this shape (see `mulmoclaude/vision/beyond-the-sea-of-app-icons.json` as the reference example):

- `$mulmocast.version`, `canvasSize` (1280×720), `title`, `description`, `lang`
- `speechParams.speakers` — one "Presenter" speaker, Gemini voice `Kore`
- `imageParams` (provider: openai), `movieParams` / `soundEffectParams` (provider: replicate)
- `slideParams.theme` — the shared visual identity: dark navy palette (`bg: 0A0F24`, primary `38BDF8`, accent `818CF8`), Georgia/Helvetica/Menlo fonts, glass card style, radial/linear gradient backgrounds. Keep new scripts consistent with this theme.
- `audioParams` — padding and volume settings
- `beats[]` — the presentation itself. Each beat has `text` (spoken narration) and `image.slide` with a `layout` such as `title`, `columns`, `grid`, `split`, `comparison`, `manifesto`, `timeline`, `table`, `bigQuote`. Scripts run ~10–12 beats.

When writing a new script, copy the params blocks from an existing script and write new `title`, `description`, and `beats`.

## MulmoScript type definition and validation

`mulmocast` is installed as a devDependency (version matched to the global CLI). The authoritative MulmoScript definition is local:

- Types: `node_modules/mulmocast/lib/types/type.d.ts` (compiled from the CLI repo's `src/types/type.ts`)
- Zod schemas: `node_modules/mulmocast/lib/types/schema.d.ts` — exports `mulmoScriptSchema`, `mulmoBeatSchema`, etc.

Consult these files (not memory or the web) for available beat fields, slide layouts, and provider options. After writing or editing a script, validate it before rendering:

```sh
npm run validate -- mulmoclaude/vision/<name>.json   # = mulmo tool complete -o /dev/null <file>
```

`npm test` validates every script under `mulmoclaude/` at once (`scripts/validate-all.js`, using the local devDependency's `mulmoScriptSchema` — reports all invalid files with full Zod issue paths).

The CLI has no dedicated `validate` command; `tool complete` parses the script against the full schema first, prints `Validation errors:` with field paths and exits 1 on failure, exits 0 on success. The `-o /dev/null` discards the completed-script output (otherwise it writes `<name>_completed.json` next to the file).

Its messages can be shallow for deeply nested union fields (e.g. a bad slide layout surfaces only as `beats.0.image: Invalid input`). To pinpoint such errors, fall back to the full Zod issue list:

```sh
node -e "const m=require('mulmocast'); const r=m.mulmoScriptSchema.safeParse(require('./mulmoclaude/vision/<name>.json')); console.log(r.success ? 'valid' : r.error.issues)"
```
