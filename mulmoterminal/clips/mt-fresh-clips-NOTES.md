# mt-restart / mt-launch-form / mt-right-click / mt-shortcut-list / mt-quit — 制作メモ

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
