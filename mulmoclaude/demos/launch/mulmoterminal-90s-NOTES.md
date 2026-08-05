# mulmoterminal-90s.json — ドラフトの状態と差し替え手順

MulmoTerminal ローンチ用 90 秒デモのドラフト。カット割り・英語コピーの正本は
mulmoterminal-marketing の `assets/capture-guide.md` §6-2（英文は 2026-07-25 確定のものをそのまま使用）。
パイプラインは「キャプチャ → 動画撮影 → mp4 を埋め込んだ MulmoScript → mp4 書き出し」。

## 素材の状態（2026-08-05 時点）

| ビート | 時間 | 予定ファイル（`mulmoterminal-90s-assets/`） | 素材 | 状態 |
|---|---|---|---|---|
| 1–2 | 0:00–0:14 | `broll-tabs.mp4` | B-roll: 通常ターミナルのタブ往復 | 未撮影（§6-3 の 1。10 秒でよい） |
| 3 | 0:14–0:22 | `grid-open.mp4` | グリッドがバッと開く決め画 | **撮影済み・埋め込み済み（2026-08-05 ドラフト画質）** — セルの状態リングが薄い（撮影時に青タスクが完了済みだった）。最終版は staging 直後に撮り直し推奨 |
| 4 | 0:22–0:35 | `grid-states.mp4` | 4 セル並走 → 色変化にズーム | **撮影済み・埋め込み済み（2026-08-05）** — 青5・アンバー2・done2 のタイル → mobile へズーム → 見えるタイピング。検品4点合格 |
| 5 | 0:35–0:45 | `amber-answer.mp4` | アンバーを開いて答える → 青へ | 未撮影（同上） |
| 6 | 0:45–0:58 | `phone-notify.mp4` | ロック画面に通知（実写） | **未撮影・カメラ必要（A-2 待ち）** |
| 7 | 0:58–1:08 | `phone-tap.mp4` | スマホから yes → Mac が動く | **未撮影・カメラ必要（A-2 待ち）** |
| 8 | 1:08–1:18 | `worktree-pr.mp4` | worktree → diff → PR ボタン | 未撮影（§6-3 の 2） |
| 9 | 1:18–1:26 | `cost-chips.mp4` | コスト・context% チップに寄る | 未撮影（同上） |
| 10 | 1:26–1:32 | —（HTML カードで完成） | `npx mulmoterminal@latest` | **完成** |
| 11 | 1:32–1:35 | —（HTML カードで完成） | GitHub URL | **完成** |

PLACEHOLDER ビートはレンダリングするとアンバー（A-2 待ちの 2 枚は赤）の点線バッジ付きの
説明フレームになる。仮レンダリングでもどこが埋まっていないか一目で分かる。

## 差し替え手順（1 ビートずつ）

前例 `demos/clips/collection-map_ja.json` の video 埋め込みパターンに置き換える:

```json
"image": {
  "type": "html_tailwind",
  "animation": { "movie": true },
  "html": ["<video src='./mulmoterminal-90s-assets/<clip>.mp4' autoplay muted playsinline style='max-height:640px'></video>"]
}
```

- `duration` はクリップ実尺に合わせて更新する（現値はカット割りの秒数）
- クリップはナレーション長より少し長めに切る（movie ビートはナレーション尺でレンダリング
  されるため、短いと最終フレームで止まる）
- 字幕焼き込みは不要（ナレーションが同じ文を読む。ミュート視聴対策で字幕も欲しくなったら
  captionParams を検討）

## ドラフトで確定させた事項・保留事項

- **TTS ナレーション + BGM**（presentations の流儀: gemini / Kore、`morning001.mp3`、bgmVolume 0.12）。
  §6-2 の英語字幕列をそのまま読み上げ原稿にした。読点・記号だけ TTS 向けに調整した箇所:
  - beat 4: `Blue = working. Amber = needs you.` → 「Blue means working. Amber means it needs you.」
  - beat 7: `Yes / no / continue.` → 「Yes. No. Continue.」
  - beat 8: `PR` → 「pull request」
  - beat 10: コマンド行は読まず表示のみ（DEMO-GUIDE の規約）。beat 11 は無音
- ⚠️ **capture-guide §6-1 は「ナレーション無し・字幕のみ」のまま**。この TTS 版はそこからの
  逸脱なので、この方針で行くなら §6-1 を更新する（正本を直すのが先。書き写さない）
- ⚠️ **60 秒か 90 秒かの正本間矛盾は未解決**（`launch-show-hn.md` §4 = 60 秒・HN 不要 /
  `capture-guide.md` §6 = 90 秒・Show HN 用）。このドラフトは 90 秒側
- canvasSize はリポジトリ前例に合わせ 1280×720。§6-4 の「1080p 書き出し」との整合は
  レンダリング時に判断（全既存デッキが 720p のため）
- 英語 canonical（ローンチは英語圏向け。リポジトリ規約「_ja 先行」からの意図的な逸脱）
- BGM・voiceId はドラフト仮置き。ローンチのトーンに合わせて要再選定

## 検証

```
npm run validate -- mulmoclaude/demos/launch/mulmoterminal-90s.json
```
