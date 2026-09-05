# Agent Picker / Any Backend（09-04）— 制作メモ

marketing repo の台帳 #54 / #55（`feature-videos.md` 第 5 節「Agents & backends」— `features.md` の表に無く、ガイドの `agents.md` / `providers.md` から採録した 2 行）。positioning がベンダー製品に対して残した 4 点の①「いま課金している CLI とアカウントのまま」の絵がここまで 1 本も無かった（v8 も hero も 9 セル全部 Claude）。素材は `mt-demo-home/footage/2026-09-04/`（agents-a〜c）、切り出しの正本は同 `cut-mt-agents.sh`、rig は `mulmoterminal-video` skill 同梱 `record-agents.mjs`。撮影対象は npx 経由の **4.16.0**。

| デッキ | 台帳 # | 素材 | ビート |
|---|---|---|---|
| mt-agent-picker | #54 | agents-c/take-pick-codex・take-pick-agy、agents-b/take-agents-grid | ①ランチャー → エージェント行の Codex → ▶ → Codex が立つ ②New terminal → Antigravity → ▶ → 立つ ③3 セル並走（俯瞰のまま 10.5 秒保持。寄らない）|
| mt-any-backend | #55 | agents-c/take-model-launch・30-model-help.png・take-model-launch-final.png | ①ランチャーの Model ピッカーで OpenRouter のプリセット（Kimi K2.7 Code · 3/3）→ ▶ ②設定ビート = Model ピッカー横の help（アプリ自身が `providers` の JSON を表示する）に寄る静止画 ③起動 → バナーの `moonshotai/kimi-k2.7-code … API Usage Billing` に寄る → 質問を打鍵 → 思考（6 倍速）→ 回答 ④回答の寄り（静止画）|

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
| mt-agent-picker | en 7.3 / ja 7.3 | en 6.4 / ja 5.8 | en 8.7 / ja 7.3 | — | pick-codex 9.2 / pick-agy 7.5 / grid 10.5 |
| mt-any-backend | en 7.6 / ja 7.8 | en 7.9 / ja 8.0 | en 7.6 / ja 7.9 | en 5.1 / ja 4.5 | pick-model 9.4 / help 10.0 / cell 13.4 / answer 6.6 |

初回レンダーで grid（8.0s）と help（7.4s）が `check-beat-fit` の OVERRUN、09-05 のナレーション差し替えで pick-model（7.9s）も OVERRUN。いずれも素材側を伸ばした（ナレーションは削らない）。

## 09-05 作者レビュー（ナレーション 2 件・絵は変えない）

- **Agent Picker beat 1 で Codex と言う** — 絵は Codex を選んで起動する場面なのに、初版は「five agents, three shown here」で名前を出していなかった。「Each cell picks its own CLI — this one starts Codex, one of five agents.」に。「5 つのうち 3 つ」の断りは beat 3（「three of the five agents, one grid」）へ移した
- **Any Backend beat 1 は「プランの上限」ではない** — 要点は「OpenRouter でいろいろなモデルを使える」。初版の「なぜ」（Hit your plan's limit?）は発生源に無い創作で、台帳の規則（「なぜ」は創作せず発生源から取る）に反していた。「Same Claude Code, many models — pick one per session through OpenRouter.」（何ができるか）に。beat 4 の「backend you chose」も「model you chose」に
- 絵に写るモデルは Kimi 1 つだけ（ピッカーは native select で一覧が録画に写らない）なので、他のモデル名は読み上げない。「many models」の裏は画面の実測ラベル（`3/3 · 14s · 262k`）と help の文面
- **grid ビートは寄らない**（作者判断 09-05）。初版は「3 つの CLI が違う」証拠としてヘッダの `gpt-5.5` を読ませるため Codex セルに 1.8 倍で寄って戻していたが、主張は「3 セルが 1 つのグリッドに並んでいる」で、寄りは主張と噛み合わない（skill の「grid ビートは俯瞰」のとおり）。CLI の違いは引きでもセルの色・エージェントのマーク・中身で分かり、名前はナレーションと字幕が言う
