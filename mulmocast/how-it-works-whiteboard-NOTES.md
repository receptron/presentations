# MulmoCast のしくみ（ホワイトボード）— 申し送り

## 作り

- 1 文 = 1 beat の 6 beat。どの beat も同じボードの図（全 beat 分の線と文字）を持ち、前の beat までの分を描き終えた状態で表示して、自分の分だけを描く。手は前の beat の最後の位置から動き始める。beat 間の切り替え効果は付けていない（付けるとつなぎ目が見える）。
- 線は描き順どおりに stroke-dashoffset で伸ばし、文字と FFmpeg のロゴは左から見せる。手（`how-it-works-whiteboard-assets/marker_hand.png`）はペン先が描いている位置に来るよう毎フレーム動かす。ペン先の画像内の座標は `how-it-works-whiteboard-build/board.mjs` の `TIP`。
- 各 beat の中の描く時刻は、ナレーションの無音区間を測って合わせた（`build.mjs` の `BEATS`）。ナレーションを変えたら測り直す。
- FFmpeg のロゴは Wikimedia Commons の `FFmpeg_Logo_new.svg`（パブリックドメイン）。

## 書き出し

- 台本の JSON は `node mulmocast/how-it-works-whiteboard-build/build.mjs mulmocast/how-it-works-whiteboard_ja.json` で書き出す（直接編集しない）。
- 声は `gemini-2.5-pro-preview-tts`（Aoede）。2026-09-24 は `gemini-3.1-flash-tts-preview` が 1 日 100 リクエストの上限に達していたため 2.5 Pro にした。
- Gemini TTS に話し方の指示を付けると、台本やセリフの話をしている文が安全フィルタ（`PROHIBITED_CONTENT`）で止まることがある。「台本には、場面ごとのセリフと絵の指示を書きます。」が止まったので、2 つ目の文は「まず、場面ごとに、話す言葉と絵の説明を用意します。」にした。
- BGM は ElevenLabs Music で作った `resources/bgms/mulmocast-how-it-works.mp3`（区間の指定は `how-it-works-whiteboard-build/bgm-plan.json`）。
- 最初の動画は mulmocast-cli の開発版で書き出した。この repo で作り直すと TTS も全 beat 作り直しになる。
