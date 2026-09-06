# Agent Picker / Any Backend（09-04）— 制作メモ

marketing repo の台帳 #54 / #55（`feature-videos.md` 第 5 節「Agents & backends」— `features.md` の表に無く、ガイドの `agents.md` / `providers.md` から採録した 2 行）。positioning がベンダー製品に対して残した 4 点の①「いま課金している CLI とアカウントのまま」の絵がここまで 1 本も無かった（v8 も hero も 9 セル全部 Claude）。素材は `mt-demo-home/footage/2026-09-04/`（agents-a〜c）、切り出しの正本は同 `cut-mt-agents.sh`、rig は `mulmoterminal-video` skill 同梱 `record-agents.mjs`。撮影対象は npx 経由の **4.16.0**。

| デッキ | 台帳 # | 素材 | ビート |
|---|---|---|---|
| mt-agent-picker | #54 | agents-f/take-pick-codex・take-pick-agy、agents-g/take-agents-grid | ①ランチャー → エージェント行の Codex → ▶ → Codex が立つ ②New terminal → Antigravity → ▶ → 立つ ③3 セル並走（俯瞰のまま 10.5 秒保持。寄らない）|
| mt-any-backend | #55 | agents-e/take-model-launch・agents-c/30-model-help.png | ①ランチャーの Model ピッカーで OpenRouter のプリセット（Kimi K2.7 Code · 3/3）→ ▶ ②設定ビート = Model ピッカー横の help（アプリ自身が `providers` の JSON を表示する）に寄る静止画 ③起動 → バナーの `moonshotai/kimi-k2.7-code`（アンダーライン）に寄る → 質問を打鍵 → 思考（12 倍速）→ 回答が返って緑になるまで |

## 決めたこと・分かったこと

- **撮影機に居るのは Claude / Codex / Antigravity の 3 つ**（Grok / Muse は無い）。エージェント行には 6 択が写るので、ナレーションは「five agents, three shown here」と断り、無いものを使えるとは言わない
- **「うちだけ」は言わない** — OSS の並列ランナーはほぼ全部これを持つ（positioning 08-16）。①はベンダー製品に対しての差
- **Any Backend は Claude セッション専用**（guide `agents.md`: providers / customAgents は Claude-only）。ナレーションは「Same Claude Code, same cell」で、他のエージェントに掛かる言い方をしない
- **Antigravity のバナーはアカウントのメールを出す**（設定で消せない）。作者判断（09-04）で**メールアドレスの文字列だけ `boxblur`** で伏せる（塗りつぶしではなく、明らかに伏せ字と分かる形）。座標はソース系 1500,325 412x36
- **Codex の trust プロンプトは実パス `/Users/…` を出す**ので、`~/.codex/config.toml` の `projects` にデモ repo 15 本を事前 trust した。Antigravity は `~/.gemini/antigravity-cli/settings.json` の `trustedWorkspaces`。Codex の TUI は directory を `~/mulmoclaude/github/…/acme-api` と表示する — Claude のバナーと同じ扱い（これまでのクリップと同じ）
- **OpenRouter のセルには Claude Code 自身の「claude.ai connectors are disabled …」の 1 行が必ず出る**（providers 機構が `ANTHROPIC_BASE_URL` / `AUTH_TOKEN` を立てるため）。製品の正しい状態なので隠さない。操作者のグローバル CLAUDE.md が 40k 字を超えていたときは実パス入りの警告がもう 1 行出た（agents-b）— 09-04 に 28k 字へ整理されて消えた
- **セルのヘッダにはモデルのバッジは出なかった**（`web · main ↑2 ↓5 · 見出し` / `/tmp/mt-demo/acme-web · Skill…` の 2 段）。モデル名は Claude Code のバナーの 2 行目に出るので、③はそこに寄る。Codex / Antigravity のヘッダには `gpt-5.5 · ctx 7%` / `Gemini 3.8 Flash` が出る
- **Model ピッカーは native `<select>`** で、開いたドロップダウンは screencast に写らない。表示値が「This directory's default」→「Kimi K2.7 Code · 3/3 · 14s · 262k」に変わるところを、直前 0.25s の枠パルスで示す
- **help モーダル（ModelSetupHelp）は `fixed inset-0`** — screencast が確実に凍る条件なので録画せず、PNG から camera-move で作る
- **hero-tmux の sender はセル名 → session id をキャッシュする** — closeAllCells の後に同じディレクトリで立て直したセルへ古い id で送って「can't find pane」になった（agents-b）。段ごとに sender を作り直す
- 3 セルのグリッドは 1200×800 で 2 列になり右下が空く。そのまま出す（製品の実状態）

## カットの当たり（記録）

- pick-codex: trim 0.3〜9.5。寄り（hold 0.4 + push 0.8）を Codex クリック（t' 1.52）より先に終える。初版は 1.0 始まりで寄りの途中にクリックが乗った
- pick-agy: trim 2.0〜11.5。メールのぼかしは t' 5.5 から（それ以前は暗い背景で見えない）
- pick-model: pull-back を cell_up より後ろに置き、バナーが描かれてから画角が戻るようにする（空のセルを引きで受けない）
- cell: ramp-and-arc。バナー 2 倍速 → 打鍵 1.5 倍 → 思考 6 倍 → 回答 等速。寄りはバナーだけ
- **grid にもメールが写っていた**（出荷判定の sub-agent が 14〜16 秒で発見。自分のコンタクトシート確認では見落とした — 技術作業の目と判定の目は別、の実例）。Antigravity の CLI は起動から約 5.7 秒後に自分で再描画してメール行を落とすので、それまでの 5.75 秒だけ同じ座標帯（1500,262 410x34）をぼかす。それ以後の同じ行には `Gemini 3.8 Flash` が上がってくるので、ぼかしを常時にはしない
- **「Signing in…」は 3.5 秒続く**（t' 5.5〜9.0）。初版の「バナー ≈ 8.5 秒」は vfr の webm に対する入力側シークで読んだ時刻で、1 秒以上ずれていた。時刻は CFR に正規化した中間ファイルで出力側シークして測る
- **ランチャーの「OR RESUME A AGY CONVERSATION HERE」にリハーサルが写る**（出荷判定 2 回目で指摘）。前のテイクで打った依頼文が「8h ago」の再開候補として並び、5 秒後に同じ文を打つので演出がバレる。Antigravity は会話を自分の store に持つので rig の reset では消えない。pick-agy の寄りの画角を y 90〜870 に狭めて（zoom 2.05）、その行（y 882〜932）を画角外にした。引きの画角ではフォームはもうセルに置き換わっている。**次に撮るときは、撮影前に Antigravity の会話 store を空にするか、前回と別のディレクトリを使う**
- pick-agy / pick-model はどちらも ramp-and-arc で rig の settle を早回しにし、ビート（5.8〜6.4 秒）の終わりが「立ち上がったセル」になるようにした。初版は等速で、片方は「Signing in…」、もう片方は黒いセルの途中でビートが切れていた

## 尺（09-05 レンダー・studio 実測 + 0.9 を duration に。数値は studio.json が正）

| デッキ | beat 1 | beat 2 | beat 3 | beat 4 | クリップ |
|---|---|---|---|---|---|
| mt-agent-picker | en 7.3 / ja 7.3 | en 6.4 / ja 5.8 | en 8.7 / ja 7.3 | — | pick-codex 9.5 / pick-agy 11.0 / grid 10.5 |
| mt-any-backend | en 7.6 / ja 7.8 | en 7.9 / ja 8.0 | en 7.6 / ja 7.9 | — | pick-model 9.5 / help 10.0 / cell 10.1 |

初回レンダーで grid（8.0s）と help（7.4s）が `check-beat-fit` の OVERRUN、09-05 のナレーション差し替えで pick-model（7.9s）も OVERRUN。いずれも素材側を伸ばした（ナレーションは削らない）。

## 09-05 作者レビュー（ナレーション 2 件・絵は変えない）

- **Agent Picker beat 1 で Codex と言う** — 絵は Codex を選んで起動する場面なのに、初版は「five agents, three shown here」で名前を出していなかった。「Each cell picks its own CLI — this one starts Codex, one of five agents.」に。「5 つのうち 3 つ」の断りは beat 3（「three of the five agents, one grid」）へ移した
- **Any Backend beat 1 は「プランの上限」ではない** — 要点は「OpenRouter でいろいろなモデルを使える」。初版の「なぜ」（Hit your plan's limit?）は発生源に無い創作で、台帳の規則（「なぜ」は創作せず発生源から取る）に反していた。「Same Claude Code, many models — pick one per session through OpenRouter.」（何ができるか）に。beat 4 の「backend you chose」も「model you chose」に
- 絵に写るモデルは Kimi 1 つだけ（ピッカーは native select で一覧が録画に写らない）なので、他のモデル名は読み上げない。「many models」の裏は画面の実測ラベル（`3/3 · 14s · 262k`）と help の文面
- **grid ビートは寄らない**（作者判断 09-05）。初版は「3 つの CLI が違う」証拠としてヘッダの `gpt-5.5` を読ませるため Codex セルに 1.8 倍で寄って戻していたが、主張は「3 セルが 1 つのグリッドに並んでいる」で、寄りは主張と噛み合わない（skill の「grid ビートは俯瞰」のとおり）。CLI の違いは引きでもセルの色・エージェントのマーク・中身で分かり、名前はナレーションと字幕が言う
- **Model ピッカーの一覧は録画に写らない**（native `<select>` の一覧は OS のポップアップで、screencast にも `page.screenshot` にも入らない）。一覧を出したいなら OS の `screencapture` で開いた状態を静止画に撮る手がある（未実施・作者判断待ち）
- **アンダーラインは beat 3 のバナー**（作者指示 09-05）。Claude Code のバナー 2 行目 `moonshotai/kimi-k2.7-code` の下に琥珀の線（4px）を、寄りの窓（バナーのセグメント）の間だけ焼く。beat 1 の Model 行に入れた版は「冒頭の方はいらない」で外した
- **クリックには全部ポインタ**（作者指摘 09-05）。初版は Codex / Antigravity ボタンと ▶ だけで、ディレクトリ欄（rig は値を直接セットするので画面には「パスが現れる」だけ）と、2 セル目を開く `+`（ツールバーの New terminal）に矢印が無かった。ディレクトリ欄は「欄に寄る → 枠パルス → パスが入る」、`+` は trim を 0.7 秒始まりに戻して「矢印 → パルス → ランチャーが開く」を入れた

## 09-05 撮り直し（agents-e / agents-f）— ディレクトリはチップのクリックで入れる

- 作者指摘: rig が欄に値を直接セットしていたので、3〜4 秒（Codex）と 11 秒（Antigravity）でパスが 1 フレームで置き換わっていた。矢印を足しても「何をしたらそうなったか」が見えない。**上のチップ行の該当ディレクトリをクリックして入れる**形に rig を直して撮り直した（`launchWith` — チップが無いときだけ従来の直接セット）。欄が既にそのパス（ランチャーの既定 = 最後に使った場所）のときは何もしない — Any Backend の 3 秒で変わらない欄に矢印と枠を付けていた件（作者指摘）もこれで消えた
- チップは起動のたびに最近使った順で並び替わるので、**位置はテイクごとに測る**（agents-f: acme-api チップ 1108,150 172x48 / 右セルの acme-mobile チップ 1410,96 240x46）。寄りの画角はチップ行を含める（単独セル y 120〜、右セル y 60〜860）
- agents-d は Codex が起動時に自己更新（0.153.0 → 0.153.4）して exit し、その `disconnected` ピルが次のテイクの待ちを止めた。rig の接続ピルの検査を「いま立てたセルだけ」に絞った
- agents-e は Antigravity のサインインが長引き（1.1.26 → 1.1.27 に更新も）、バナーが録画の外に出た。rig を「バナー（`Antigravity CLI x.y.z`）が pane に出るまで最大 20 秒待つ」にして agents-f で撮り直し（バナーは take の 9.8 秒ごろ）
- Any Backend は agents-e の model テイクを使う（ディレクトリは既定のまま、Model ピッカーと ▶ だけ注釈）

## 09-05 作者判断: Any Backend の beat 4（回答の寄り）を外す

- 要点は「モデルを選ぶと、同じ Claude Code がそのモデルで動く」で、返事の中身ではない。beat 4 はナレーション（7.6〜7.9 秒）より素材（13.4 秒）が長く、返事の場面がビートの外に落ちたのを埋めるために足していたもの
- 代わりに beat 3 の早回しを詰めた（打鍵 3 倍・思考 12 倍）。返事が返って緑になるところまでがナレーションの中に入り、クリップは 27 秒前後に
- `answer.mp4` は `git rm`

## 09-05 grid の撮り直し（agents-g）

- 出荷判定で、grid ビートの Claude セルの入力欄に薄い文字で「Have index.js import formatDate from utils.js」が写っていると指摘された。Claude Code が作業を終えたあとに自分で出す「次にやること」の候補（ゴーストテキスト）で、こちらが打った文ではないが、打ちかけの指示に見える。Claude への依頼を長くして（関数ごとの説明 + 改善案とトレードオフ）、13 秒の間ずっと作業中の絵にした。撮り直し後の最終フレームの入力欄は空
- この take は 3 セルに依頼を投げてから始まるので、Antigravity のバナー（メール入り）は開始時点で既にスクロールアウトしている。grid のぼかしは不要になった（agents-b 版では 5.75 秒までぼかしていた）
- 出荷判定（最終）で ja の beat 3 の末尾 2 フレームが「右上セルの再描画の瞬間（空）」に乗っていると指摘された。素材 7.73 秒に端末の再描画で 2 フレームだけ空になる瞬間があり、trim 0.5 始まりだと ja のビート末尾（7.3 秒）がそこに一致していた。trim を 1.2 始まりにずらしてビートの途中に置いた（0.9 では ja の末尾まで 0.1 秒しか余裕が無く、再描画は 0.3 秒間隔で 2 回ある。1.2 で余裕 0.4 秒。en は元から中間）
