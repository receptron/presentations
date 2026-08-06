# mulmoterminal-90s-v2.json — ターミナル軸ドラフト（positioning.md 2026-08-04 準拠）

90s/60s（旧軸）はそのまま温存し、**複製**として作った新軸ドラフト。74秒。
コピーは全文ドラフト（positioning.md「用途別の一言」を種に作文。確定レビュー前）。

## 構成と素材

| ビート | 内容 | 素材 |
|---|---|---|
| 1 | "tmux was built for terminals that don't ask questions." | 同一見た目5ペインのモック（90s から流用） |
| 2 | 混成グリッド（dev server / top / Claude が同居） | **実写 axis-grid6.mp4**（6セル通し撮りから切り出し） |
| 3 | amber の質問を拡大 | **実写 axis-amber-zoom.mp4** |
| 4 | 2×2 でカメラ上回答 →「Got it — structured JSON body it is」 | **実写 axis-answer4.mp4**（4セル通し撮り） |
| 5 | worktree（dev サーバを隣で回せる文脈に差し替え） | 実写流用 |
| 6 | マルチベンダー（タブ＋リング） | 静止画流用 |
| 7 | 永続（再接続リプレイ） | 実写流用 |
| 8-9 | npx / URL カード | 完成 |

## ナレーション対訳（英語＝ドラフト原稿 / 日本語＝意味確認用・画面には出さない）

capture-guide §6-2 と同じ形式。英文は positioning.md「用途別の一言」を種にした**ドラフト**（確定レビュー前）。

| # | 英語 | 日本語 |
|---|---|---|
| 1 | tmux was built for terminals that don't ask questions. | tmux は、質問してこないターミナルのために作られた |
| 2 | This is a terminal with agents in it. A dev server, a system monitor, and Claude — every cell is a real pty. | これはエージェントが入っているターミナル。dev サーバも、システムモニタも、Claude も — セルは全部本物の pty |
| 3 | The agents are the ones that ask questions. Amber means one needs you — and only amber chimes. | 質問してくるのはエージェント。琥珀色は「あなたを待っている」の印 — 鳴るのは琥珀だけ |
| 4 | Answer it, and everything keeps moving. Even one to three agents is where this pays off. | 答えれば、全部が動き続ける。並列が1〜3体でも元が取れる |
| 5 | Each agent works in its own worktree — and the dev server runs right beside it. | エージェントはそれぞれ自分の worktree で作業する — dev サーバはそのすぐ隣で回せる |
| 6 | Claude, Codex, Antigravity — one grid, same rules. | Claude も Codex も Antigravity も — 同じグリッド、同じルール |
| 7 | Restart the server — every session survives and reattaches. | サーバを再起動しても — 全セッションが生き残って繋ぎ直される |
| 8 | Local. Open source. No Electron. | ローカル。オープンソース。Electron 不使用 |

## ビートの見せ方の原則（2026-08-07 レビューより）

**grid ビートは俯瞰、読ませるビートは拡大**でサイズ要件が違う。全画面 1440px を動画に縮めると
セル内文字は実質 8〜9px で構造的に読めない — 読めなくてよいのは俯瞰ビート（色と状態が主役）だけ。
読ませるもの（質問・diff）は、生テイクが retina（2880px）なのを利用してクロップズームするか、
静止クローズアップに差し替える（capture-guide §6-2 の「この動画でだけ自動ズーム」と同趣旨）。
実施済み: amber 質問 = クロップズーム動画（crop 1720x970@700,270）、worktree diff = ヘッダー+
差分+ボタン行を縦積みした静止クローズアップ（スピルオーバーで音声継続）。

## 撮影メモ（axis 通し撮り、2026-08-06）

- **staging と録画は同一ブラウザで一気通貫にすること** — ターン未消化の claude セルと
  shell 系セルは、開いたクライアントの切断で tmux ごと消える（seed 手渡し方式は全滅した）
- shell セルは**組み込み Shell でなく OR-LAUNCH の Shell チップ**（`env ZDOTDIR=/tmp/mt-demo-home zsh`）
  で起動する — 組み込みは操作者の実プロンプト（user@host）が写る
- チップの一致は `endsWith("Shell")`（textContent に material icon のリガチャが混入する）
- スクリプト: scratchpad `stage-terminal-axis.mjs`（staging→6セル録画→2セル閉→4セル録画）。
  原素材とスクリプトの写しは `mt-demo-home/footage/2026-08-06/` に保存

## 次テイクで直すこと（今回はドラフト許容）

- curl 先が実在しないパスで **404 の連発**になっている → `/` を叩いて 200 に
- web のタスク文が capture 用リポの関数名（applyCoupon）を指し、**質問化して amber が2つに**
  → mt-demo の実ファイル（greet / formatDate）を指す文にすれば working（青）が立つ
- log tail セルと devserver セルの**内容重複** → 6セル目は別の絵に（要検討）
- top のプロセス欄に実アプリ名（NordVPN 等）— 一般アプリ名なので許容中、最終版で判断
