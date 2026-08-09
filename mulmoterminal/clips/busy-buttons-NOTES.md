# busy-buttons — MulmoTerminal 4.7.3 の機能紹介クリップ

15 秒・3 ビート。MulmoTerminal のリリースごとに短尺クリップを出すための 1 本目で、
`mulmoclaude/demos/clips/collection-map_ja.json`（10 秒・1 ビート）の続き。

| | |
|---|---|
| 題材 | 4.7.3 — `+ New worktree` が押した回数だけ worktree を作っていた問題（#1549）と、削除中のセルの表示（#1551） |
| 尺 | 英語 14.8 秒 / 日本語 14.2 秒 |
| 出典 | mulmoterminal `docs/guide/{en,ja}/v4.7.3.md`、`docs/ChangeLog.md` の 4.7.3 |
| ビート 1 | HTML のみ（問題の説明） |
| ビート 2・3 | 実写クリップ。原素材は `mt-demo-home/footage/2026-08-10/` |

## リポジトリ規約からの意図的な逸脱

**スライドは英語だけ。日本語版もスライドは英語のまま、ナレーションと字幕だけが日本語。**
規約（リポジトリ CLAUDE.md）は「`_ja` 先行 → 英語版へ翻訳、スライドも撮影素材も両方作る」だが、
MulmoTerminal のクリップはこの方針を取らない。したがって:

- 素材ディレクトリは `busy-buttons-assets/` **1 つだけ**（`-assets-ja` は作らない）
- 2 ファイルの `beats[].image` は**完全に一致させる**。差し替えるのは `text` と `lang`、
  `captionParams.lang` / `textSplit`、話者の `instruction`、`title` / `description` だけ

一致の確認:

```sh
python3 -c "
import json
en=json.load(open('mulmoterminal/clips/busy-buttons.json'))
ja=json.load(open('mulmoterminal/clips/busy-buttons_ja.json'))
print(all(a['image']==b['image'] for a,b in zip(en['beats'],ja['beats'])))
"
```

ビートが増えたらこの二重管理は破綻する。そのときは「英語版を正本にして `_ja` を生成する」形へ移す。

## レンダリング

```sh
npm run movie -- mulmoterminal/clips/busy-buttons.json -c en
npm run movie -- mulmoterminal/clips/busy-buttons_ja.json -c ja
```

出力は `output/busy-buttons/busy-buttons_en__en.mp4` と
`output/busy-buttons_ja/busy-buttons_ja_ja__ja.mp4`（`<lang>__<caption>` が付く）。

`-l ja` による 1 ファイル多言語は**採らなかった**。翻訳は LLM の自動生成で、結果は
`output/<name>/<name>_lang.json`（gitignore 配下）に入るため、手直しした日本語ナレーションが
バージョン管理の外に出る。ナレーションは英日で尺が違うので、そもそも直訳では詰められない。

## 字幕

X はミュート自動再生なので焼き込み前提。`captionParams` に `bottomOffset: 4` を入れている
（既定の 0 だと日本語の字幕が下端に張り付く。ローンチデッキ `mulmoterminal-90s-v2.json` は
まだ 0 のまま）。`textSplit` の区切りは英語 `". "` / 日本語 `"。"`。

## 素材の作り方

撮影は `probe-busy-window.mjs`（`footage/2026-08-10/` に同梱）。capture-server.sh の :34599 に
対して、preset チップ → `fix-login` を打鍵 → `+ New worktree` → 起動、そのセルを閉じて
worktree ごと削除、までを 1 ブラウザで通す。`page.screencast` は **2880×1800（retina 2x）**で
録れるので、クロップで寄っても解像度が足りる。

切り出し（原素材はいずれも `footage/2026-08-10/acme-web-{create,remove}.mp4`）:

```sh
# worktree-creating.mp4 — 打鍵 → Creating… の worktree 行だけを切り、0.75 倍速、末尾をフリーズ
ffmpeg -i acme-web-create.mp4 -ss 1.40 -t 2.60 -an create-trim.mp4
ffmpeg -i create-trim.mp4 -vf "crop=1160:210:860:678,setpts=1.33*PTS,tpad=stop_mode=clone:stop_duration=4.6,fps=60" -an worktree-creating.mp4

# cell-removing.mp4 — 確認ダイアログ → 減光したセル、そこからスピナーへプッシュイン
ffmpeg -i acme-web-remove.mp4 -ss 1.15 -t 0.72 -an remove-trim.mp4
ffmpeg -i remove-trim.mp4 -vf "crop=2840:1319:20:345,fps=60" -an remove-crop2.mp4
node ~/.claude/skills/mulmoterminal-video/camera-move.mjs remove-crop2.mp4 cell-removing.mp4 \
  --target 820,276,1200,558 --hold 1.1 --push 1.2 --tail 2.5 --canvas 1120x520
```

## 引っかかったところ

- **「小さいリポジトリでは busy 状態が一瞬で終わる」は誤りだった。** これを未検証の前提にして、
  `git worktree add` が 5-8 秒かかる 97,340 ファイルのフィクスチャリポジトリ（419MB）を rig に
  作りかけた。実測すると 7 ファイルの acme-web で **`Creating…` が 122 フレーム・2,017ms**
  出ていた（ボタンが握られている窓は git の所要時間ではなく、サーバー往復・MCP 登録・セッション
  起動まで含むため）。フィクスチャは破棄した。
  **`Removing…` は 6 フレーム・83ms しかないが、それでも足りる** — 尺は編集で作るもので、
  `camera-move.mjs --hold`（`tpad=stop_mode=clone`）が一瞬をそのまま伸ばす。
  ビートの長さぶん状態が続いている必要はない。
- **ビートに `duration` を書かない。** TTS の長さは再生成のたびに変わる（英語ビート 1 で
  5.30 → 4.80 秒、日本語ビート 0 で 5.59 → 6.07 秒）。固定値を入れたら英語ビート 3 が
  音声 3.67 秒に対し 3.30 秒で切られた。**クリップ側の末尾フリーズを音声より長く取り、
  尺は音声に決めさせる**（クリップが余ればビート終端で切られるだけ）。
- **`camera-move.mjs` はアスペクト不一致を拒否する**（`--canvas` を勝手に合わせない）。
  縦を詰めたいときはソースを先にクロップしてからキャンバスを合わせる。
- **Gemini TTS が 1 ビートで 116 秒の音声を返した。** 日本語ビート 1 の体言止め
  （「…同じものが、三つ。」）で発生。1 文にまとめ直したら 5.3 秒に収まった。音声は内容ハッシュで
  キャッシュされるので、暴走したら**本文を変えるか `-f`** で取り直す。TTS はほかにも単発で
  落ちて、同じコマンドの再実行で通った。
- **`scripts/validate-all.js` は `mulmoclaude/` しか走査していない。** `mulmoterminal/` 配下は
  `npm test` の対象外なので、このクリップも launch デッキ 3 本も CI では検証されない。
  検証は個別に `npm run validate -- <file>` を回す必要がある（走査対象の修正は別 PR）。
