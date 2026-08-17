# mulmoterminal-120s-v7.json — 2 分ローンチ動画（2026-08-16 台本準拠）の初稿

v6（60 秒・冒頭 2 拍）とは別の系統。中島さんの 2026-08-16 台本（"The day you became the bottleneck"、10 カット・120 秒・WHY 先行）をそのまま beat に落とした。台本の正本は台本 PDF（`mulmoterminal-launch-video-script-2026-08-16.pdf`）で、ここには写さない。ナレーションは台本の英文をそのまま使い、beat 8 だけ 2 文に割った（下記）。

**英語版が canonical**（ローンチ動画の規約どおり）。TTS は v6 と同じ Presenter / Kore、`instruction` に台本の Delivery notes（"Read it flat" / 「Amber is waiting on you.」だけ少し落とす）を反映した。

## v6 からの前提の変更

| | v6 | v7 |
|---|---|---|
| 尺 | 60 秒 | 120 秒 |
| 冒頭 | `launch-show-hn.md` §4（10 秒で 2 拍・ナレーション無し） | WHY 先行（黒画面→5 タブ→amber スロー）。§4 の 2 拍は 0:18〜0:58 に移動 |
| 落ちたもの | — | 「Claude, Codex — one grid, same rules」／「Even one to three agents is where this pays off」（台本に無い。要相談 → marketing 側 TASKS 参照） |

## beat と素材

| # | 台本の時刻 | 素材 | 種別 |
|---|---|---|---|
| 0 | 0:00 | 黒画面 + カーソル | **mock**（html） |
| 1 | 0:08 | agent-1〜5 のタブを手で切り替える | **mock**（90s v1 の beat 1 を英語化・リタイム） |
| 2 | 0:18 | `amber-slow.mp4` = `open-amber-answer.mp4` 1.6〜3.3 s を 3 倍スロー → 末尾フレームで 15 s までホールド。チャイムは `chime-amber-slow.mp3`（4.27 s、amber と同期） | 既存 footage の派生 |
| 3 | 0:32 | `grid6-colors.mp4` = `grid6-amber.mp4` + ホールド（13.5 s） | 既存 footage の派生 |
| 4 | 0:48 | `enlarge-answer.mp4` = `open-amber-answer.mp4` 3.4 s〜末尾（寄り→質問→打鍵で回答） | 既存 footage の派生 |
| 5 | 0:58 | `roster-hold.mp4` = `expand-diff.mp4` 0〜5.8 s（拡大→roster）+ ホールド（16.5 s）。roster 列に HTML リング（6.5 s〜） | 既存 footage の派生 |
| 6 | 1:14 | `worktree-diff-pr.mp4` = `worktree-create.mp4`（5 s）+ `worktree-diff.mp4` 0〜3.4 s + ホールド（計 15 s）。`Open PR` ボタンに HTML リング（10.5 s〜） | 既存 footage の派生 |
| 7 | 1:28 | スマホのロック画面通知（Yes / No / Continue のチップ、タップ後に "Sent."） | **mock**（html） |
| 8a | 1:44 | サーバを ^C → `npx mulmoterminal@latest` → "reattached 6 tmux sessions" | **mock**（html） |
| 8b | 1:44 | `mixed-grid-hold.mp4` = `axis-grid6.mp4`（system monitor・dev サーバ・Claude の混成グリッド、2026-08-06 撮影）+ ホールド（12 s） | 既存 footage の派生（**UI が 1 世代前**） |
| 9 | 1:54 | `npx mulmoterminal@latest` + MIT · URL | html |

派生素材の作り方は全部 ffmpeg 1 行（trim / setpts / tpad / concat）で、元は `mulmoterminal-60s-v4-assets/` と `mulmoterminal-90s-assets/`。scratchpad の中間物は残していない。

台本の "On-screen text" 列は、各 beat の左下に同じスタイルの字幕（`font-mono` の帯）で焼いた: `the slowest thing is you` / `4:12 — time this agent spent doing nothing` / `working / done / needs you` / `remembering → 0 seconds` / `worktree → diff → PR` / `walk away.` / `restart is not loss`。絵文字は使っていない（台本の指定）。

## mock を実写に差し替えるときの撮り物（= 未撮影のもの）

1. **0:08 タブ往復** — 素のターミナル（何でもよい。iTerm 限定ではない）に 5 タブ、1 つは許可待ちが裏に隠れている。手で 2 往復。5〜10 秒
2. **0:18 amber スロー** — いまは v6 の take を 3 倍スロー＋静止で代用。台本は「他のセルは動き続ける」なので、**長回しの実写に置き換える**。字幕の `4:12` は**実測にする** — amber になった時刻と答えた時刻の差を rig のタイムスタンプから取り、字幕とナレーションの "four minutes" をその値に揃える（現状はプレースホルダ）
3. **1:28 スマホ実写** — 屋外・物理カメラ（marketing `assets/capture-guide.md` §5 の手順）。台本の 3 本柱（0:08 / 0:32 / 1:28）の 1 つなので落とせない
4. **1:44 kill → 再起動 → htop が生きている** — 台本は「実際に kill しろ」。現状は kill を mock、混成グリッドを 08-06 の take で代用。撮り直しは 4.8.x の UI で、htop・dev サーバ・エージェントを 1 グリッドに
5. **0:32 の "Green is done"** — 製品 README は「done, unreviewed（blue）」と「finished は green」が混在（roster は green）。**現行ビルドのグリッド枠で「完了」が何色かをカメラで確認してから**この 1 文を確定する

## 撮影 rig の制約で台本と違うところ

- **マウスポインタは映らない**（CDP screencast はポインタを撮らず、操作は JS click / 打鍵）。0:48 の「クリック」は打鍵（回答は typed）で、対象は amber の発光と HTML リングで示す。台本 0:32 の "The mouse does not move" は自動的に満たす
- ジャンプ・拡大をキーでやるなら、撮影用 HOME の `.mulmoterminal/config.json` に `keymap`（`next-attention` / `zoom-toggle`）を入れる。既定では未割り当て

## 検証

- `npm run validate` は通過。レンダー後に `check-beat-fit.py`（skill 同梱）で各 beat のクリップ尺 ≥ 音声尺 + 0.5 s を確認する（下の「実測」に追記）
- 動画の秒数はドキュメントにもコピーにも書かない（skill の規約）。台本の時刻は目安

## 実測（2026-08-17 初回レンダー）

- `check-beat-fit.py` 全 beat ok（クリップ尺 ≥ 音声尺 + 0.5 s）。明示 `duration` は beat 4（打鍵の回答を最後まで見せるため 6.9 s）・beat 8a（mock の演出 6.5 s）・beat 10（5.5 s）だけで、残りは音声が尺を決める
- TTS の語速は 1.8〜2.7 語/秒でばらつく（beat 1 が 2.7、beat 6 が 1.8）。beat 5 と 6 の余裕（+3.6 / +1.9 s）はこのばらつき用に取ってある
- 台本の時刻（0:18 / 0:32 …）より全体が短めに出る。秒数はここに書かない（規約）

## レンダーで踏んだこと（次の版で同じ穴に落ちないために）

- **beat に `audio` を置くと、その beat の TTS は生成されない**（mulmocast `actions/audio.js` の `needsTTS = !beat.audio`）。初稿はチャイムを beat 2 の `audio` に置いたので、台本の "One of them is always stopped…" が**丸ごと喋られていなかった**。チャイムは外した。復活させるなら `chime-amber-slow.mp3` を `amber-slow.mp4` の音声トラックに mux して `image.type: "movie"` の beat にする（TTS と movie 音声は mix される。ただしリポジトリ内に前例なし・字幕は ffmpeg で焼く必要あり）— follow-up
- **Gemini TTS が特定の文で壊れる。** beat 5（"The other kind of slow is: what did I even ask this one? …"）は 2 回とも喋り 12 秒のあとに **17 秒／111 秒の無音**が付いて返った（同一入力で決定的）。文面は台本どおり残したいので、生成された mp3（`output/…/audio/…de3e9e65…_en.mp3`）を **12.6 秒でトリムしてキャッシュに戻した**。`output/` を消して再生成すると同じ無音が戻る — そのときはこの手順を繰り返すか、文を微修正する。beat 9（"…tmux — so htop, …"）は 500 INTERNAL が 2 回続いたので `—` をカンマに変えたら通った（意味は同じ）
- **on-screen text は左上に置く。** 左下に置くとナレーションの字幕（`captionParams`、画面下中央）と重なって隠れる（初回レンダーで `4:12 —…` が読めなかった）
- **クリップを差し替えたら `output/<deck>/images/` を退避してから再レンダー**（skill の規約どおり。今回 2 回やった。退避先は `images.stale1` / `images.stale2`、`output/` は gitignore）
