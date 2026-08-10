# busy-buttons — MulmoTerminal 4.7.3 の機能紹介クリップ

23 秒・5 場面。MulmoTerminal のリリースごとに短尺クリップを出すための 1 本目で、
`mulmoclaude/demos/clips/collection-map_ja.json`（10 秒・1 ビート）の続き。

制作フォーマットの正本は `mulmoclaude/content-roadmap.md` の
「制作フォーマット（本編と 10 秒クリップ）」と「10 秒クリップの作り方」。
ここには**そこから外れた点だけ**を書く。

| | |
|---|---|
| 題材 | 4.7.3 — worktree のコントロールが処理中に進行を出すようになった（#1549）ことと、削除中のセルの表示（#1551） |
| 尺 | 英語 23.1 秒 / 日本語 22.9 秒 |
| 出典 | mulmoterminal `docs/guide/{en,ja}/v4.7.3.md`、`docs/ChangeLog.md` の 4.7.3 |
| 構成 | 5 場面すべて実写。俯瞰（起動フォーム）→ 寄り（ボタン）→ 俯瞰（セルと閉じるボタン）→ 寄り（確認ダイアログ）→ 寄り（削除中） |
| 原素材 | `mt-demo-home/footage/2026-08-10/acme-web-{create,close}-v2.mp4` |

**直した不具合の説明はしない。** できるようになったことだけを見せる。初稿は
「6 秒かかるのに無反応だったので押し増され、worktree が 3 本できた」を 1 ビート目に置いたが、
その 6 秒が何の 6 秒かはクリップ内のどこにも無く（日本語版に至ってはナレーションが
その数字に一度も触れないまま、スライドにだけ英語で出ていた）、伝わらなかった。

**ビート数ではなく場面数で設計する。** 正本の「標準形は 1 ビート」は課金とミュート自動再生が
理由で、尺の上限ではない。静止画 1 枚で 10 秒持たせるのは無理があり、伝わらなければ意味がない
ので、場面転換の数を先に決めてから尺を決める。

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

撮影は `reshoot-worktree.mjs`（take A: 作成）と `reshoot-close.mjs`（take B: 閉じる）。
どちらも `footage/2026-08-10/` に同梱。capture-server.sh の :34599 に対して、preset チップ →
打鍵 → `+ New worktree` → 起動、いったんブラウザを閉じて worktree 行から復帰 → 閉じる →
削除、を撮る。`page.screencast` は **2880×1800（retina 2x）**で録れるので、クロップで寄っても
解像度が足りる。

切り出し（原素材は `footage/2026-08-10/acme-web-{create,close}-v2.mp4`）。
**2 テイクから 5 場面を作っている** — 2x なので、クロップの取り方だけで俯瞰と寄りを作り分けられる:

```sh
# 01 俯瞰: 起動フォーム全体（読ませない。worktree の行がここにあると分かればよい）
ffmpeg -i acme-web-create-v2.mp4 -ss 0.80 -t 1.50 -an c1.mp4
ffmpeg -i c1.mp4 -vf "crop=1700:1000:600:200,setpts=1.30*PTS,tpad=stop_mode=clone:stop_duration=6.6,fps=60" -an 01-name-the-task.mp4

# 02 寄り: 打鍵 → New worktree → Creating… の行だけ
ffmpeg -i acme-web-create-v2.mp4 -ss 1.90 -t 2.70 -an c2.mp4
ffmpeg -i c2.mp4 -vf "crop=1160:210:860:678,setpts=1.15*PTS,tpad=stop_mode=clone:stop_duration=5.4,fps=60" -an 02-creating.mp4

# 03 俯瞰: 生きているセル。× にリングを重ねるので、ヘッダーの上に余白を残して切る
ffmpeg -i acme-web-close-v2.mp4 -ss 0.20 -t 2.20 -an c3.mp4
ffmpeg -i c3.mp4 -vf "crop=2840:1650:20:80,tpad=stop_mode=clone:stop_duration=6.3,fps=60" -an 03-the-close-button.mp4

# 04 寄り: 確認ダイアログ（ダイアログが消える前で切って、そのフレームで止める）
ffmpeg -i acme-web-close-v2.mp4 -ss 2.70 -t 1.30 -an c4.mp4
ffmpeg -i c4.mp4 -vf "crop=1600:740:641:576,setpts=1.30*PTS,tpad=stop_mode=clone:stop_duration=6.8,fps=60" -an 04-close-confirm.mp4

# 05 寄り: 削除中
ffmpeg -i acme-web-close-v2.mp4 -ss 4.30 -t 1.30 -an c5.mp4
ffmpeg -i c5.mp4 -vf "crop=1700:790:578:522,setpts=1.30*PTS,tpad=stop_mode=clone:stop_duration=6.8,fps=60" -an 05-removing.mp4
```

**クリップは音声より長く作る（各 8.5 秒）。** 尺はナレーションが決めるので、クリップが短いと
末尾が凍る。長いぶんはビート終端で切られるだけで害がない。

| ファイル | 中身 |
|---|---|
| `01-name-the-task.mp4` | 1700×1000 — 起動フォーム（俯瞰） |
| `02-creating.mp4` | 1160×210 — worktree の行（寄り） |
| `03-the-close-button.mp4` | 2840×1650 — 生きているセル（俯瞰）。× にリングを重ねる |
| `04-close-confirm.mp4` | 1600×740 — 閉じる確認ダイアログ（寄り） |
| `05-removing.mp4` | 1700×790 — 削除中のセル（寄り） |

**「どのボタンから削除に行くのか」は場面 3 のリングだけが答えている。** 入口はセル自身の
閉じるボタン（ヘッダー右端の ×）で、worktree のセルだと押した先が確認ダイアログになる。
クリップは押す瞬間を映せない（スクリーンキャストにポインタが写らず、そもそも JS click している）ので、
`<video>` を `relative` なラッパーに入れて % 座標のリングを `data-animation` で重ねる。

**寄りの画角はクリップ側で決める。** 一度 1120×640 のクリップをスライドで 665px 幅に縮めて
置いたことがあり、`camera-move.mjs` で稼いだ拡大がその縮小でそのまま相殺された。
クリップの縦を詰めて（1120×520）スライドでは原寸で置くのが正しい。

**ガイド用のスクリーンショット（mulmoterminal の `docs/guide/images/v4.7.3-*.png`）は使っていない。**
初稿はこれで組んだが、988×649 のセル画像を 1280×720 のキャンバスに収めると
`Removing acme-web (fix-login)…` が実質 9px になって読めず、そのセルは削除中で中身が空なので
プッシュインしても寄り切った先が暗い矩形になった。実写だと減光した端末の中身が背景に薄く残るので
「セル全体が減光している」ことがそのまま伝わる。

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
- **一度目のテイクは起動に失敗したセルを撮っていた。** worktree は作られたのにエージェントが
  上がらず、ヘッダーに赤い `disconnected`、端末には
  `[this worktree already has a session — resume it from its row instead of starting a second one]`
  だけ。過去に同じ名前で作った worktree のセッション登録が残っていたのが原因で、**未使用の
  タスク名を使う**と再現しない。ヘッダーを画角に入れられず（＝ × を指せず）、減光の背景も
  空だったので撮り直した。撮影スクリプトは着手前に「その名前の worktree 行が既にあるか」を
  検査して落ちる。
- **xterm はキャンバス描画なので、端末の中身は DOM に出ない。** `.xterm-rows` の innerText を
  待つ検査は、正常に起動しているセルに対してタイムアウトする。DOM で判るのは
  「起動フォームが消えた」ことと「接続状態のピルが無い」ことまで。
- **話者の `instruction` が尺を動かす。** 日本語版に「文と文のあいだの間を十分に取ってください」と
  書いていたら、1 文のビートが 10.8 秒まで伸びた。「テンポよく」に替えて 5.8 秒。
  英語版の同じ趣旨の一文（`Let the pauses between sentences breathe.`）はローンチデッキ由来で、
  英語ではここまで効かない。
- **Gemini TTS が 1 ビートで 116 秒の音声を返した。** 日本語ビート 1 の体言止め
  （「…同じものが、三つ。」）で発生。1 文にまとめ直したら 5.3 秒に収まった。音声は内容ハッシュで
  キャッシュされるので、暴走したら**本文を変えるか `-f`** で取り直す。TTS はほかにも単発で
  落ちて、同じコマンドの再実行で通った。
- **`scripts/validate-all.js` は `mulmoclaude/` しか走査していない。** `mulmoterminal/` 配下は
  `npm test` の対象外なので、このクリップも launch デッキ 3 本も CI では検証されない。
  検証は個別に `npm run validate -- <file>` を回す必要がある（走査対象の修正は別 PR）。
