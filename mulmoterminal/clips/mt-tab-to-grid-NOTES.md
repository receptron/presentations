# mt-tab-to-grid — NOTES

## BH-030 vA4 (briefVersion: bh030-a4-audio-amber-expand-2026-09-30)

- Session: 92e62dbc-f22a-4762-9600-ef23f184a89b (Claude Code), model claude-opus-5-5.
- This session wrote both scripts (`mt-tab-to-grid.json`, `mt-tab-to-grid_ja.json`) and ran both
  `mulmo movie -g -f -o /workspace/full-feature-media/tab-to-grid …` commands itself (JA exit 0, EN exit 0).
  No other agent or shell ran mulmo.
- Start 2026-09-30T18:23:09+0800 / end 2026-09-30T18:26:03+0800 (Asia/Singapore).
- Structure: 4 full-frame `html_tailwind` movie beats playing the existing captures in order —
  before-term.mp4 (4.0s, tab hopping) → grid-live.mp4 (4.5s, 2x3 grid) → expand-live.mp4 (6.0s, Expand on the
  amber waiting-on-you cell **acme-api**, AskUserQuestion rate-limit Fixed window / Token bucket) → end-grid.mp4
  (2.5s, silent residual). No loupe, no overlays, captions off.
- Audio: Gemini TTS Presenter / Kore / gemini-2.5-pro-preview-tts, suppressSpeech=false, BGM morning001.mp3 at 0.10.
  JA line 2 spells the product name まるもたーみなる.
- Assets were not regenerated. Posters: mulmo produced no poster, so assets/poster.png was copied to the three
  delivery poster names.
- Deliverables: bh030-tab-to-grid_ja-vA4.mp4 (18.97s, video+audio), bh030-tab-to-grid_en-vA4.mp4 (19.75s, video+audio).

## BH-030 vA5 (briefVersion: bh030-a5-return-to-grid-2026-09-30)

- Session: 92e62dbc-f22a-4762-9600-ef23f184a89b (Claude Code), model claude-opus-5-5.
- This session wrote both scripts and ran the `mulmo movie -g -f -o /workspace/full-feature-media/tab-to-grid …`
  commands itself. No other agent or shell ran mulmo.
- Start 2026-09-30T18:35:30+0800 / end 2026-09-30T18:40:30+0800 (Asia/Singapore).
- Why remade: vA4 ended still expanded. vA5 ends with a **return-to-grid** beat: beat 4 plays
  `end-grid.mp4`, the real full 2×3 mosaic that replaced the vA4 asset. Frames were checked: the asset's last
  frame and both deliverables at duration−1.2s show all six cells.
- Beats: before-term.mp4 4.0 → grid-live.mp4 4.0 → expand-live.mp4 5.5 (Expand on the amber waiting-on-you cell
  **acme-api**, AskUserQuestion rate-limit Fixed window / Token bucket) → end-grid.mp4 3.5 ("Back to the whole grid." /
  「格子全体に戻ります。」). Full-frame html_tailwind movie beats, no loupe, no overlays, captions off.
- Audio: Gemini TTS Kore / gemini-2.5-pro-preview-tts, suppressSpeech=false, BGM morning001.mp3 at 0.10.
- Run history: the first pass of both renders (outroPadding 0.8) exited 0 for JA and EN. JA came out at 20.04s, so its
  outroPadding was cut to 0.5 and JA was re-rendered (exit 0, 19.09s). The EN re-render with the same trim exited 1:
  the Gemini API returned 429 because gemini-2.5-pro-tts is capped at 50 requests per day. EN was therefore left at
  outroPadding 0.8, and its delivery file is the first-pass EN render (exit 0, 19.23s), which matches the committed
  EN script exactly. Result: the two scripts differ only in outroPadding (EN 0.8, JA 0.5).
- Posters: mulmo produced none, so assets/poster.png was copied to the three vA5 poster names.

## BH-030 vA5 (briefVersion: bh030-a5-grid-wording-amber-return-2026-09-30) — CORRECTED

- Session: this Claude Code session (Opus 4.5), model claude-opus-4-5.
- This session updated both scripts (`mt-tab-to-grid.json`, `mt-tab-to-grid_ja.json`) and ran both
  `mulmo movie -g -f -o /workspace/full-feature-media/tab-to-grid …` commands itself (JA exit 0, EN exit 0).
  No other agent or shell ran mulmo.
- Start 2026-09-30T19:13:00+0800 / end 2026-09-30T19:17:54+0800 (Asia/Singapore).
- Why remade: the prior vA5 session still used 格子 in JA wording and pro TTS model. This render fixes both:
  - **グリッド wording**: JA title changed from 「タブ渡りから格子一枚へ」→「タブ渡りからグリッド一枚へ」;
    beat 2 「チームが格子一枚に集まります」→「チームがグリッド一枚に集まります」;
    beat 4 「格子全体に戻ります」→「グリッド全体に戻ります」. No 格子 remains.
  - **TTS model**: changed from gemini-2.5-pro-preview-tts to gemini-2.5-flash-preview-tts (pro daily quota exhausted / 429).
- Beats: before-term.mp4 4.0s → grid-live.mp4 4.0s → expand-live.mp4 5.5s (Expand on the amber waiting-on-you cell
  **acme-api**, AskUserQuestion rate-limit Fixed window / Token bucket) → end-grid.mp4 3.5s ("Back to the whole grid." /
  「グリッド全体に戻ります。」). Full-frame html_tailwind movie beats, no loupe, no overlays, captions off.
- Return-to-grid: beat 4 plays end-grid.mp4 — the full 2×3 mosaic. Video ends on the grid, not expanded.
- Amber: the amber waiting-on-you color (#f5a623 / var(--amber)) is visible in grid-live.mp4 and expand-live.mp4 assets.
- Audio: Gemini TTS Kore / **gemini-2.5-flash-preview-tts**, suppressSpeech=false, BGM morning001.mp3 at 0.10.
  Both JA and EN TTS rendered and are audible.
- Deliverables: bh030-tab-to-grid_ja-vA5.mp4 (18.56s, video+audio), bh030-tab-to-grid_en-vA5.mp4 (18.99s, video+audio).
- Posters: mulmo produced none, so assets/poster.png was copied to the three vA5 poster names.

### 2026-09-30T19:23 re-bake
- expand-live.mp4 re-trimmed for continuous amber (#f5a623) throughout expand beat; remux only, scripts unchanged.
- グリッド wording unchanged (confirmed: 0 matches for 格子 in JA script).
- mulmo movie -g -f exit codes: JA 0, EN 0.
- Durations: JA 18.56s, EN 18.86s.

## BH-030 vA6 (briefVersion: bh030-a6-amber-fill-not-thin-stroke-2026-09-30)

- Session: this Claude Code session (Opus 5.5), model claude-opus-4-5.
- This session updated both scripts (`mt-tab-to-grid.json`, `mt-tab-to-grid_ja.json`) and ran both
  `mulmo movie -g -f -o /workspace/full-feature-media/tab-to-grid …` commands itself (JA exit 0, EN exit 0).
  Grok Shell did NOT run mulmo — this session ran it directly.
- Start 2026-09-30T19:50+0800 / end 2026-09-30T19:52+0800 (Asia/Singapore).
- Why remade: Marketing withdrew vA5 PASS — amber was thin gold stroke + teal header, not product amber FILL.
  vA6 assets now have waiting-cell HEADER filled with product amber #f5a623 (glance-readable in grid and Expand).
- Amber HEADER FILL: #f5a623 on waiting cell header (not thin stroke).
- Return-to-grid: beat 4 plays end-grid.mp4 — the full 2×3 mosaic. Video ends on the grid, not expanded.
- グリッド wording: JA uses グリッド only (0×格子 confirmed via grep).
- Beats: before-term.mp4 4.0s → grid-live.mp4 4.0s → expand-live.mp4 5.5s (Expand on the amber waiting-on-you cell
  **acme-api**, AskUserQuestion rate-limit Fixed window / Token bucket) → end-grid.mp4 3.5s ("Back to the whole grid." /
  「グリッド全体に戻ります。」). Full-frame html_tailwind movie beats, no loupe, no overlays, captions off.
- Audio: Gemini TTS Kore / **gemini-2.5-flash-preview-tts** (NOT pro), suppressSpeech=false, BGM morning001.mp3 at 0.10.
  Both JA and EN TTS rendered and are audible.
- mulmo exit codes: JA 0, EN 0.
- Deliverables:
  - /workspace/full-feature-media/tab-to-grid/bh030-tab-to-grid_ja-vA6.mp4 (18.69s, video+audio)
  - /workspace/full-feature-media/tab-to-grid/bh030-tab-to-grid_en-vA6.mp4 (18.84s, video+audio)
- Posters: mulmo produced none, so assets/poster.png was copied to:
  - bh030-tab-to-grid_ja-vA6-poster.png
  - bh030-tab-to-grid_en-vA6-poster.png
  - bh030-tab-to-grid-poster-vA6.png
- Creation path: This session wrote scripts and ran mulmo; Grok did not run mulmo.
