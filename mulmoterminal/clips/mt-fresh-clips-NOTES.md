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
