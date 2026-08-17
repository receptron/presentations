# mulmoterminal-launch-v8.json — 「あなたがボトルネックになった日」v8（1 メッセージ版）

v7（中島さんの 2 分台本を機能カット込みで組んだ版）から、作者の判断（2026-08-17 Slack: remote は落とす／細かい機能紹介より「多数を同時に動かしているとき状態が一瞬で分かる」に特化／expand して状態が変わってどんどん指示するシーンが欲しい／動画で active な terminal をカメラで拡大するのは負け／色にメリハリ）に合わせて組み直した。**英語版が canonical**、`_ja` はナレーションだけ日本語（見出しは英語のまま）。

## 構成（9 beat）

| # | 台本の意図 | 素材 | 種別 |
|---|---|---|---|
| 0 | 黒画面＋点滅カーソル | html（`blink`） | mock |
| 1 | 同じ見た目のタブ 5 枚を手で切り替える | `tab-web/mobile/docs/auth/api.mp4` — **take-pain**（Shell セルで `claude --model sonnet` を 5 本）から各セルの端末部分をクロップ | 実写＋タブ枠 |
| 2 | 止まっている 1 枚と、その経過時間 | `tab-api.mp4`（question tool で止まっている）＋ `waiting 0:00→4:12` のバッジ | 実写＋html |
| 3 | 全部を 1 画面に。青→amber | `grid.mp4` = take-grid 4〜22 s（**amber 点灯は clip 11.4 s**） | 実写 |
| 4 | ⤢ で拡大して答える | `light.mp4` = take-cockpit 0〜13 s（expand 2.2 s / 回答 9.8 s） | 実写 |
| 5 | roster：頼んだこと・返ってきたこと。緑の行へ移って次の指示 | `roster.mp4` = take-cockpit 13〜34 s | 実写 |
| 6 | 次が roster で光る → クリック → 答える | `loop.mp4` = take-cockpit 56〜76 s（**amber2 点灯 clip 5.9 s**、クリック 7.6 s、回答 15.5 s） | 実写 |
| 7 | 締め（triage） | `close.mp4` = take-cockpit 186〜207 s（amber3 点灯 3.6 s、回答 12.6 s、グリッドへ 15.8 s） | 実写 |
| 8 | `npx` | html | — |

落としたもの（作者判断）: スマホ（1:28）、worktree→diff→PR（1:14）、kill→再起動→htop（1:44）、「1〜3 体でも効く」の一文。中島さんには「remote を落とした」を伝える必要がある（未）。

## 素材の正本

`mt-demo-home/footage/2026-08-17/cockpit-n/`（`record-cockpit.mjs`、9 checkout・1x 描画・1200×800）。カット点は各 `-marks.json`。クリップは全部 ffmpeg 1 行（trim → crop で上部ツールバー 60px を落とす → 1200×740）。タブ用は各セル本体 370×270 を 2 倍（740×540）に拡大しているので**甘い** — 痛みの絵だけ 2x で撮り直す価値あり（`launchBrowser(..., {scale: 2})`、Shell 5 セルなら軽いのでクラッシュしない見込み）。

## 使うときの注意

- **take-cockpit 85〜111 s は使わない**（api2 に追加指示を打つ区間に Claude Code の hook タイムアウトの赤字が拡大ペインに出る。機械が重かった影響）→ v8 の clip はこの区間を避けている
- **take-pain の auth セル**は 8〜14 s だけ使う（それ以外の時刻に `find` の出力で個人パスが写る）→ `tab-auth.mp4` はその窓
- `verify-takes.sh` は grid / cockpit を FROZEN と判定したが、**端末が流れ続ける画では「最終フレーム ≒ 終了後の静止画」が成り立たず誤判定**する。時系列でフレームを抜いて中身が進んでいることを目視で確認した（skill 側の課題として記録）
- 「Green is done」（beat 3）: take-grid の中では緑が出ない（全部 blue → 1 つ amber）。緑は beat 5〜6 の roster で見える。ナレーションは中島さんの文のまま

## v7 レビューで直したこと（v8 に反映）

見出しは `top:56px`・映像は `top:108px / 幅 960`（下端 700 で字幕に掛からない）／タブ枠に映像が収まる（760 幅の枠に 740 の映像）／4:12 は MulmoTerminal ではなく痛みの絵に／⤢ とクリックで拡大（カメラのズーム無し）／旧 footage の使い回し無し（全部 cockpit-n）／スマホ・機能カット無し

## 2026-08-17 レビュー 1 回目の対応

- **TTS が話者の `instruction` を読み上げていた**（ja: 「琥珀は、あなたを待っています」が beat 1・2 に混入、en: beat 3 が 3 秒長い）。指示文の中の引用フレーズが原因。mt-first-run と同じ文言に戻して全音声を再生成。**指示文に台詞を引用しない**こと（文字数 ÷ 秒 の外れ値で検出できる: en 1.6〜3.0 語/秒、ja 3.5〜7 字/秒）
- 4:12 のバッジは「早送りのカウントアップ」だと経過時間に見えなかった → **`waiting for 4:12` から実時間で秒が進む時計**に変更、見出しは beat の最初から出す
- 締め（beat 7）は cockpit の戻りグリッドに hook タイムアウトの赤字が写ったので、take-grid の amber 部分（冒頭の callback）に差し替え
- ja の尺は ja の音声から算出（`max(en の duration, ja voice + 0.8)`）
- **解像度**: グリッドと痛みの絵は 1x 撮影のため甘い → `MT_SCALE=2 … --only grid,pain` で 2x 撮り直し（未実施・撮影窓が要る）

### まだ怪しいところ（未対応）

- 拡大ペインと roster 行に staging 用プロンプト（"Ask me exactly one multiple-choice question … using your question tool"）がそのまま写る。自然な文で question tool が安定して出るか未検証
- beat 3 のグリッドに緑（done）が出ないままナレーションが "Green is done" と言う（緑は beat 5〜6 の roster で見える）
- beat 4 の冒頭 1〜2 秒、拡大直後のペインが空（描画待ち）
