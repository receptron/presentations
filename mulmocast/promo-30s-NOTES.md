# MulmoCast 30 秒プロモーション（マーケティング用）— 申し送り

## 残作業

### 1. 「動画生成もできる」を加える

- MulmoCast は beat の `moviePrompt` で動画生成 AI を呼べる。対応は Replicate（既定 `bytedance/seedance-1-lite`）と Google（既定 `veo-2.0-generate-001`）。根拠は mulmocast-cli の `src/types/provider2agent.ts` の `provider2MovieAgent`（2.12.0 時点）。
- いまの台本の「ナレーションも、画像も、動画も、AIが生成。」の「動画」は、音声と画像をつないで最後に書き出す動画のことで、動画生成 AI の話ではない。加えるときは、両者を取り違えない言い方にする（例: 「動画生成AIで、動く映像も作れます。」）。
- 入れる場所の候補は、生成の場面（タイル 3 枚の場面）にタイルを 1 枚足すか、形式の場面（PDF・ポッドキャスト・多言語）に並べるか。ナレーションが延びる分、ほかの文を削って 30 秒前後に収める。

### 2. TTS の上限が解けたら作り直す

- この台本の声は `gemini-3.1-flash-tts-preview`（Aoede）。1 日あたり 100 リクエスト／プロジェクト／モデルの上限（`GenerateRequestsPerDayPerProjectPerModel`）に 2026-09-24 に達した。そのときの 429 の `retryDelay` は 81351 秒（約 22.6 時間）だった。
- 上の 1 で文を変えたら、変えた beat だけが作り直される（音声のキャッシュは本文ごと）。音声を作り直したら、各 beat の無音区間を測ってアニメーションの時刻を合わせ直す（今回もそうした）。

## 作り直すときの注意

- 台本の JSON は `promo-30s-build/build.mjs` から書き出す（直接編集しない）: `node mulmocast/promo-30s-build/build.mjs mulmocast/promo-30s_ja.json`。人物の SVG は `promo-30s-build/man.mjs`（Codex gpt-6-astra が描いたものに、肩と腕を手で直したもの）。
- BGM は ElevenLabs Music で作った `resources/bgms/mulmocast-promo-30s.mp3`。場面の切れ目に合わせて作ったので、尺が変わったら作り直す（`promo-30s-build/bgm-plan.json` の各区間の長さを変えて Music API に渡す）。
- Gemini TTS に話し方の指示を付けると、台本やセリフの話をしている文が安全フィルタ（`PROHIBITED_CONTENT`）で止まることがある（ホワイトボード版で「台本には、場面ごとのセリフと絵の指示を書きます。」が止まった）。音声が返らないときは、言い回しを変える。
- 参照画像付きの画像生成（`references` / `canvasSize`）を使っているので、この repo の mulmocast（2.7.2）では検証が通らない。2.12.0 以降で書き出す: `npx mulmocast@2.12.0 movie -g -o "$MAIN/output" mulmocast/promo-30s_ja.json`（`$MAIN` は CLAUDE.md の worktree の節のとおり）。
- 最初の動画は mulmocast-cli の開発版で書き出したもので、音声・画像のキャッシュはこの repo の `output/` には無い。作り直すと TTS も全 beat 作り直しになる（上の上限に注意）。
