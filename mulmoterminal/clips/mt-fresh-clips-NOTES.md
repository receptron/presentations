# fresh + stock クリップ (09-01) — 制作メモ

fresh クリップの初回一括（2026-08-31 決定・marketing repo `feature-clips-plan.md` が発注書）。
1 機能 = 1 クリップ・1 ビート、機能名は焼き込み（フェードインさせない）。素材は
`mt-demo-home/footage/2026-08-31/`（fresh-a〜e）、切り出しの正本は同 `cut-mt-fresh.sh`、
rig は `mulmoterminal-video` skill 同梱 `record-fresh.mjs`。撮影対象は npx 経由の **4.14.0**
（Settings の version チップが mt-quit の画面内に写っている）。

| デッキ | 出た版 | 素材 | 備考 |
|---|---|---|---|
| mt-restart | 4.14.0 | fresh-c/take-restart | 2 ビート: ①元の会話 → restart クリック（**ボタンに琥珀リング焼き込み** — 2 段目・Skill の右）→ 再起動 ②**opt-in の設定スニペット**（buttons / keymap の両方）。設定の話が無い初版は「ボタンが出てない」と差し戻された |
| mt-launch-form | 4.11.0 | fresh-b/take-launchform | 拡大中に + → フォームが横 → 隣で 2 本目が起動 |
| mt-right-click | 4.13.0 | fresh-b/take-rightclick | `read ` の打ちかけに Insert relative path で README.md が入る |
| mt-shortcut-list | 4.13.0 | fresh-a/40-shortcuts.png | **静止画から camera-move**（下の「Settings は撮らない」） |
| mt-quit | 4.11.0 | fresh-e/take-quit + final.png | 動画（確認 → Stopping…）+ 静止画（has stopped）の継ぎ |

### stock 5 本（09-01 夜間・再撮影なし）

台帳「素材あり」の 5 機能を 08-30 の footage から新しい型で組んだ。切り出しは footage 08-31 の `cut-mt-stock.sh`。

| デッキ | 台帳 # | 素材 |
|---|---|---|
| mt-status-colors | #2 | 08-30 cockpit-a/take-grid |
| mt-cockpit-roster | #3 | 08-30 cockpit-a/take-cockpit-b（ロスター行クリックにポインタ + 直前パルス） |
| mt-tmux-persist | #11 | 08-30 pty-persist/take-persist |
| mt-plain-shell | #41 | 08-30 pty-launch/take-shell-launch（Shell チップにポインタ） |
| mt-launch-commands | #42 | 08-30 pty-grid2/take-mixed-grid |

投稿しないと決めた 08-30 の 3 デッキ（mt-cockpit / mt-any-command / mt-nothing-lost）の素材は、これで全部この形に消化された。

### backlog 3 本 + 共通エンドカード（09-01 深夜〜）

- 追加 3 本: `mt-rate-gauge`（ツールチップは**ネイティブ title で screencast に写らない** — 常時表示 + カメラ寄りに変更）／ `mt-run-menu`（acme-web3 に `script.json` + 通るテスト 3 本を仕込み、demo-baseline `ee470cf`〜）／ `mt-split-editor`（追従判定は body 全体でなく**エディタ自身のテキスト**で。中間 20 秒は 6 倍速圧縮）
- **Path Links / Copy Code Block は rig 環境（symlink cwd）では機能が発火せず撮影不可** — 前者はリンクが形成されない（カーソル掃引でも pointer 化せず）、後者は transcript 参照が外れて「No completed turn yet」。**上流報告の候補**
- **全クリップ共通のエンドカード**: 黒地 `npx mulmoterminal@latest`（v8 と同じ意匠・TTS なし・duration 1.0）。`outroPadding` 2.0 がフェード窓になり BGM がその上で消えていく
- `mt-restart` beat 2 は**実操作の映像**（Settings → Keyboard shortcuts → Set up shortcuts… → 「Let an agent set this up?」ダイアログで締め）。静止スクショ案は差し戻された
- 完了待ちは done 状態のポーリングでなく「working を経て working でなくなった」で判定（短い返答の done は一瞬で idle に戻る）

### restart は「同じ会話」を映像で反証した（2026-09-01・上流報告候補 3 件目）

再開後に「What did you say src/index.js exports?」を打ったら、**「I haven't looked at that file
before in this conversation」と返ってきた**（restart-proof2 テイク）。この環境では restart は会話を
引き継いでいない — #1918/#1920 と ChangeLog の「same conversation」の主張と食い違う。クリップからは
会話の主張を落とし、「同じセル・同じディレクトリ・ランチャー往復が不要」の範囲にした。
**解決（2026-09-01 深夜）**: 実体パス起動（config 差し替え無しの素の `npx` + rig の `MT_DEMO_ROOT`
オーバーライド）で restart は設計どおり動いた — **会話がまるごと再描画され、続き質問に記憶で答える**。
最終テイクは「CLAUDE.md に署名ルールを追記 → restart → 同じ会話のまま、次の返事から署名が付く」で、
**同じ会話 + 設定反映**を 1 画面で証明している（restart-claudemd2）。settings.json の model 変更は
`--resume` がセッションのモデルを引き継ぐため乗り物として不適（restart-model で実測）。

**根本原因は確定した（2026-09-01 検証）**: サーバの `projectSessionsDir()` は `path.resolve(cwd)` のみで
realpath しないため、symlink cwd（`/tmp/mt-demo/…`）では `-tmp-mt-demo-*` slug を探すが、claude 自身は
realpath slug（`-Users-…-mt-demo-home-…`）にしか書かない（`-tmp-*` slug は 1 つも存在しないことを確認）。
よって `sessionExistsOnDisk` が常に false → mintId → 新規会話。**同じ根が copyblock の
「No completed turn yet」も説明する**（transcript 参照系が同じ slug を見る）。証拠: 続き質問が
新規ファイル・新規 id（`623c62fd…`）の先頭プロンプトになっている。pathlink（リンク不形成）だけは
別経路の可能性が残り未確定。修正の本筋は実装側の realpath 化＋ docs（header.md の "on the same
conversation"）の但し書き。非 symlink 環境では正常系のはず。

## 撮影で確定したこと（rig に反映済み）

- **Settings モーダルは録画しない** — `fixed inset-0` で screencast が凍る既知条件そのもの
  （take-shortcuts が実際に凍った）。静止画 2 枚 + camera-move で作るのが正解
- **Quit は 2 段** — セクションの「Quit MulmoTerminal」は確認パネルを開くだけで、本番は中の赤い
  「Quit」。ナビ項目も同名なので、可視の一致の**最後**を押す
- **クリック注釈は「動くポインタ + 0.25s 枠パルス」**（v8 round 6 と同じ。リング初版は差し戻された）。
  実装は `cut-mt-fresh.sh`（pointer.png も footage 側に保存）。**パルスはクリックの「直前」に置く** —
  メニュー項目や確認を開くボタンはクリックの瞬間に消える／ずれるので、クリック時刻に合わせると
  枠が空中に浮く（right-click のメニュー・quit のセクションボタンで実際に踏んだ）
- **1 セル拡大時は横にランチャーが既定で居座る** — ファイルペインの絵を撮るときは Show files 後に
  「ツリーの実表示 + dir 入力の不在」を検証してから回す
- **restart 後の会話は画面に再描画されない**（60 秒観察）。transcript からの再開は製品ドキュメントの
  主張どおりだが、絵では見えない — ナレーションはドキュメントの主張（same cell, same conversation）の
  範囲に留めた。**次のウィンドウの宿題**: 再開後に続きの指示を打って「文脈が生きている」を見せるテイク
- restart 後の tmux セッションは**新しい id** で立つ — capture-pane で検証するときは grid_v2 から
  id を毎回取り直す（rig は反映済み。それでも今回は検証が通らず、目視で合格にした）

### 09-02 補修（ユーザー差し戻し 3 件）

カットの正本は footage `2026-09-02/cut-recuts.sh`（右クリック・launch-form）。

- **mt-right-click**: 出荷版はメニューを開いたまま終わり「パスが挿入されない」— rc-half2 の
  screencast がメニュー表示中に凍っていた（挿入は撮影後の final.png にのみ残存）。ライブ
  （クリックまで）+ final.png（メニュー閉・`read README.md` 完成）の継ぎに再カット。メニューは
  実物もクリックで瞬時に閉じるので、この継ぎは実挙動どおり
- **mt-launch-form**: パルス（1.73–1.98）とフォーム出現（1.7）が同時で「上部をクリックしていない」
  ように見えた。先頭 1.0s ホールドを足して + クリック完了 2.55 → フォーム 2.70 に。フォーム内は
  ディレクトリ欄ホバー → 起動 ▶ パルス（4.50–4.78、フォームは 4.82 に閉じる実測）
- **mt-quit**: ナビ項目を画面外のまま DOM クリックしていたため「突然 Quit に変わる」。rig
  （record-fresh.mjs）にナビの実スクロール（1.6s smoothstep）を実装して撮り直し。素の npx は実
  config を共有しモーダル縁に実ワークスペースが写るため、demo config（capture-server.sh）必須

### 09-02 補修 第2ラウンド（ユーザーレビュー 4 件）

- **全 13 デッキ**: ナレーションがエンドカードに 0.8〜1.2s はみ出していた — mulmo は beat の絵を
  「音声長 − introPadding」で切るため。**全ナレーションビートに明示 duration（= 音声長 + 0.9）**を
  入れて解消（実測: 発話終了 → 1s 以上の間 → エンドカード）。**新デッキを作るときも同じ式で
  duration を入れること**（audio 長は 1 パス目レンダー後の studio.json から取る）
- **mt-launch-form**: ディレクトリ欄のプログラム書き換え（steer）は「利用者と同じ操作」でないと
  差し戻し → rig をチップ実クリック経路（cell-chip-main → cell-dir-go、page.mouse.click）に変更して
  撮り直し（footage `2026-09-02/lf-chip4`）。チップは title 属性（フルパス）の後方一致で当てる。
  **チップ実クリックにはプリセットチップに載っている repo が要る**（acme-api2 は非掲載で失敗）
- **mt-quit**: 「stop コマンドがあるなら画面に出す」→ `mulmoterminal stop` チップをビート HTML に
  置き、**mulmocast の宣言的アニメーション（`data-animation='animate'` + `data-opacity='0,1'` +
  `data-start`）**でナレーションと同期してフェードイン（en 8.2s / ja 7.4s — タイミングはデッキ側なので
  クリップは 1 本のまま）。⚠️ **animation:true はフレームを仮想時刻で描画するため、ネイティブ CSS の
  keyframes（Tailwind 組み込み animate-* 含む）は時計が進まない**（mulmocast 2.7.2 で最小ケース確認）。
  動きは MulmoAnimation の data-attribute で書く — 対応プロパティ一覧は cli の
  `assets/html/js/data_attribute_registration.js` 冒頭、実例は `scripts/test/test_data_animation.json`。
  ja ナレーションは直訳調を書き直し（「たいてい見ていないウィンドウです」→ 自然文）
  この ffmpeg は drawtext 非搭載 — テキストは PIL で PNG にして overlay。ja ナレーションは直訳調を
  書き直し（「たいてい見ていないウィンドウです」→ 自然文）
- **mt-shortcut-list**: 「設定方法が無い」→ beat1「Set up with an agent」を追加（restart の
  clip2 = Settings 実操作 → 「Let an agent set this up?」を流用、narration は独自）

### 09-02 補修 第3ラウンド（mt-shortcut-list）

- 「ズーム後 5 秒静止」の差し戻し → 静止画 + camera-move をやめ、**一覧ペインの実スクロールを録画**
  （footage `2026-09-02/sl-scroll`。rig の take-shortcuts にスクロール実装、素材はトリムのみで
  ポインタ注釈なし）
- 「一つも設定されていないので半分くらい入れて」→ demo-config に **keymap 5 本**（ガイドの
  iTerm2 風レディメイド: zoom-toggle / zoom-next / zoom-prev / next-attention /
  terminal-new-adjacent）を追加して撮影。以後の Settings 系テイクにもこの 5 本が写る。
  ⚠️ サーバーは config を起動時に読む — demo-config.json を変えたら capture-server の再起動が要る
- **mt-status-colors**: 「HN 版のように枠を出せないか」→ ナレーションの列挙（青→緑→琥珀）に同期して、
  該当セルを囲む 4px の枠（`data-animation` の宣言・ビート HTML 側）を積み上げる形に。クリップは
  1 本のまま en/ja でタイミング差し替え。琥珀セルの遷移時刻（5.5-6.0s）はピクセルサンプリングで確認
  してから枠時刻（6.5s）を決めた
- **mt-tmux-persist beat1（サーバー再起動でもセルが戻る）を追加**（2026-09-03）。最初はランチャーの
  再開リストで撮ろうとして 2 回失敗 — ①Settings の Sessions that survived a restart は実パスの
  実セッションが混ざり撮影不可 ②ランチャーの per-directory 再開リストは symlink cwd と realpath
  transcript の slug 不一致（Path Links / Copy Code Block と同根・3 例目）で行が出ない。
  **正解は作者指摘の「localStorage に grid が残っていれば、開き直すだけでセルが生存セッションに
  再接続する」**: 仕込みと撮影を**同じ Chrome プロファイル**で行う必要があり、rig の launchBrowser に
  `userDataDir` オプションを追加した（既定は毎回使い捨てプロファイル）。手順: 仕込み（3 体起動・
  グリッド残置）→ capture-server を Ctrl+C → 再起動 → 同プロファイルで開き直しを録画。
  セルがある状態の reload は beforeunload ガードで止まる — `page.on("dialog", accept)` が要る

## 4.15.0 fresh（09-03）— mt-mulmo-menu

台帳 F6（marketing `feature-videos.md`）。素材は `mt-demo-home/footage/2026-09-03/mulmo-b/take-menu.webm`（rig `record-mulmo.mjs`、仕込みは acme-docs demo-baseline `8f7f540` の `decks/launch.json` + `.mulmoterminal.json` の `decks`）。切り出しの正本は footage `2026-09-03/cut-mt-mulmo-menu.sh`。

- 1 ビート + エンドカード。絵: Claude が返答を流している最中に `Mulmo ˅` → `Launch talk` → セルが拡大して Canvas → Edit タブでスライド。ポインタ 3 本（Mulmo / Launch talk / Edit）+ 直前 0.25s の枠パルス
- **Media タブ（既定）はリポジトリ内デッキだとビートごとに赤い `File not found` を出す**（receptron/mulmoterminal#1970: plugin View 4.5.2 が named root の `root` を送らない）。その区間（素材 4.35〜5.05s）を 2.5 倍速で 0.28s に詰め、Edit タブのスライド描画で締める。クリップ 10.07s
- duration は 1 パス目の実測 + 0.9: en 9.5（音声 8.64）/ ja 7.9（音声 7.03）。en は余裕 0.57s で `check-beat-fit` の 0.5 ぎりぎり — TTS を作り直したら測り直す
- **F7 Deck in the Repo は保留**: 素材 `mulmo-e/take-deckrepo.webm` の 0〜8s（右クリック → Open in the Canvas → Edit タブ）は使えるが、③「編集がリポジトリのファイルに入る」は 4.15.0 では保存されない（#1970）。9.7s 以降の title 編集 → `git diff`（空）は使わない
- Canvas はプラグイン View が shadow root の中に居るので、rig の DOM 判定は shadow root を降りて探す（`document.querySelectorAll` では見えない）。Shell セルは `cell-dir` の title を持たない（ヘッダー 1 段目にパス）。ツリー行は名前だけの葉要素で引く（行の textContent にはアイコンのリガチャが混ざる）— いずれも `record-mulmo.mjs` に反映済み

## 4.15.0 fresh（09-03）— mt-chat-agent-picker

台帳 F8。素材は `mt-demo-home/footage/2026-09-03/picker-b/`（`take-picker.webm` + `64-header-picker.png`、rig `record-mulmo.mjs --only picker`）。切り出しの正本は footage `2026-09-03/cut-mt-chat-agent-picker.sh`。仕込みは demo-workspace-en のコレクション 3 つ（shopping-list / recipes / todo）を `mt-demo/data/` と `mt-demo/data/skills/` にコピー（個人情報なしを grep で確認）。

- 絵: workspace ルート（`/tmp/mt-demo`）の Claude セルで Collections ペインをターミナルの上まで広げ、Shopping List → Chat → モーダルのフッター `LAUNCH WITH: Claude` → Codex に → 閉じるとペインのヘッダにもピッカー。画角はペイン + モーダル（crop 1800×1200 @ (600,66)。ペイン左端 732 で切るとビューポート中央のモーダルが左欠け）
- **チャットのモーダルは `fixed inset-0` で、閉じる瞬間に screencast が凍る**（既知条件）。ライブは Codex に変えたところまで（素材 7.2s）、閉じた後の「ヘッダにピッカー」は `64-header-picker.png` の静止画（4.8s、リング 0.25〜3.2s）。一覧を読む待ち（素材 2.5〜4.2s）は 4 倍速 — en のナレーション 6.8s の内側に③を乗せるため
- duration は実測 + 0.9: en 7.7（音声 6.84）/ ja 9.7（音声 8.76）。クリップ 10.43s
- **Collections ペインの言語は `navigator.language`**（host binding の `localeTag` = `browserLocale()`）。macOS の Chrome は `--lang` を無視するので日本語 OS ではペインだけ日本語になる（picker-a）— rig は `evaluateOnNewDocument` で `navigator.language` を en-US に固定
- コレクションはセルのディレクトリ基準で解決される（project セルは `<dir>/.claude/skills`、managed workspace = 起動ディレクトリは `data/`）。ルートのセルを起動するとランチャーの MRU に `/tmp/mt-demo` が入り、**同じウィンドウの次の rig 起動は preflight（preset は全部 `/tmp/mt-demo/` 配下）で落ちる** — demo-config.json の `cwdPresets` を `POST /api/config` で入れ直してから回す（picker-b の手順）
- インデックスのカードは `[data-testid="collections-index-card-<slug>"]`、チャット起動は「Chat」ボタン、モーダルのピッカーは `[data-testid="chat-modal-agent-picker"] select`、ヘッダのピッカーは `[data-testid="launch-agent-picker"]`（いずれも PluginFrame の shadow root 内）
