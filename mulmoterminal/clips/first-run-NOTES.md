# first-run — 制作ノート

MulmoTerminal の初回フロー動画（npx → PR マージ → チップ再入場 → worktree → 4 セル、73 秒・EN ナレーション+字幕）。マーケ側の位置づけと在庫台帳は marketing repo `assets/video/feature-videos.md`、X 投稿文は同 `assets/twitter/first-run-video-post.md`。

## 素材と数値の正本

- 採用テイクと切り出しレシピ（クロップ座標・カット秒・リング座標・カメラ移動の全コマンド）: `mt-demo-home/footage/2026-08-12/first-run-t9/` の `cut3.sh` / `cut4.sh` / `concat*.sh` — **ここに書き写さない**
- 撮影スクリプト（クリーン起動・チップ誕生・worktree の staging 一式）: `mulmoterminal-video` skill の `record-first-run.mjs`
- 不採用テイク t1〜t8 の敗因は skill 側の履歴と各 footage ディレクトリに残っている（baseline 汚染 2 回・トースト・個人パスの banner など）

## 見せ方の決定（2026-08-12 レビューで確定）

- **画面転換は必ずズームイン/アウトで繋ぐ**（ハードカットは現在地を見失う）。プッシュ/プルの到達窓と次カットのクロップ窓を同一座標にする
- 起動フォームの削除→入力は隠さない（実挙動）。空欄には placeholder `/path/to/project` が出る — 空欄をフラット塗りで偽装しない
- 通知バッジは CSS で非表示（新品状態の再現）。週次リミット警告・レートゲージは残す（ユーザー判断）
- クリック対象は drawbox リングで示す（▶・チップ・+）。座標は DOM 実測
- エージェント作業は早送り→節目（commit / PR 作成 / merged）で静止→ナレーション
- クリップが音声より短いビートだけ明示 `duration`（音声より短い duration は音声が切れるので禁止）

## 既知の残課題

- ビート 4 の再入場セルの起動バナーに rig の実パスが写る（全景スケールで判読不可のため許容）。恒久対策は製品側のステートディレクトリ override（提案中）
- アプリ UI の一部（フッター）は日本語のまま — フッターの「English」はガイドリンクであり UI 言語スイッチではない
