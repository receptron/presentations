# MulmoCast 30 秒プロモーション（マーケティング用）— 申し送り

## 動画生成 AI の扱い

- 生成の場面（タイル 3 枚）の 3 枚目は「動画生成」で、ナレーションは「ナレーションも、画像も、動画生成AIの映像も。」。MulmoCast は beat の `moviePrompt` で動画生成 AI を呼べる（対応は Replicate の既定 `bytedance/seedance-1-lite` と Google の既定 `veo-2.0-generate-001`。根拠は mulmocast-cli の `src/types/provider2agent.ts` の `provider2MovieAgent`、2.12.0 時点）。
- 以前の「動画も、AIが生成」は、音声と画像をつないで最後に書き出す動画と紛れたので、動画生成 AI だと分かる言い方に変えた。

## 作り直すときの注意

- 台本の JSON は `promo-30s-build/build.mjs` から書き出す（直接編集しない）: `node mulmocast/promo-30s-build/build.mjs mulmocast/promo-30s_ja.json`。人物の SVG は `promo-30s-build/man.mjs`（Codex gpt-6-astra が描いたものに、肩と腕を手で直したもの）。
- 声は `gemini-3.1-flash-tts-preview`（Aoede、落ち着いたトーンの指示付き）。ナレーションを変えたら、各 beat の無音区間を測ってアニメーションの時刻（`build.mjs` の各 beat の秒数）を合わせ直す。
- Gemini 3.1 Flash TTS の上限は、1 分あたり 10 リクエストと 1 日あたり 100 リクエスト（どちらもプロジェクト・モデルごと）。2 本続けて作ると 1 分の上限に当たるので、1 分空ける。
- BGM は ElevenLabs Music で作った `resources/bgms/mulmocast-promo-30s.mp3`。場面の切れ目に合わせて作ったので、尺が変わったら作り直す（`promo-30s-build/bgm-plan.json` の各区間の長さを変えて Music API に渡す）。
- Gemini TTS に話し方の指示を付けると、台本やセリフの話をしている文が安全フィルタ（`PROHIBITED_CONTENT`）で止まることがある（ホワイトボード版で「台本には、場面ごとのセリフと絵の指示を書きます。」が止まった）。音声が返らないときは、言い回しを変える。
- 参照画像付きの画像生成（`references` / `canvasSize`）を使っているので、この repo の mulmocast（2.7.2）では検証が通らない。2.12.0 以降で書き出す: `npx mulmocast@2.12.1 movie -g -o "$MAIN/output" mulmocast/promo-30s_ja.json`（`$MAIN` は CLAUDE.md の worktree の節のとおり）。
