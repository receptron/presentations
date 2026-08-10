# busy-buttons — MulmoTerminal 4.7.3 の機能紹介クリップ

22 秒・4 場面。MulmoTerminal のリリースごとに短尺クリップを出すための 1 本目で、
`mulmoclaude/demos/clips/collection-map_ja.json`（10 秒・1 ビート）の続き。

制作フォーマットの正本は `mulmoclaude/content-roadmap.md` の
「制作フォーマット（本編と 10 秒クリップ）」と「10 秒クリップの作り方」。
ここには**そこから外れた点だけ**を書く。

| | |
|---|---|
| 題材 | 4.7.3 — worktree のコントロールが処理中に進行を出すようになった（#1549）ことと、削除中のセルの表示（#1551） |
| 尺 | 英語 22.2 秒 / 日本語 21.0 秒 |
| 出典 | mulmoterminal `docs/guide/{en,ja}/v4.7.3.md`、`docs/ChangeLog.md` の 4.7.3 |
| 構成 | 4 場面すべて実写。①フォーム→worktree 行へズームイン→`Creating…` ②セルと閉じるボタン ③確認ダイアログ ④減光→削除中→セルが消える |
| 原素材 | `mt-demo-home/footage/2026-08-10/acme-web-{create,close}-v3.mp4` |

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

撮影は `shoot-v3.mjs`（`footage/2026-08-10/` に同梱）。capture-server.sh の :34599 に対して、
preset チップ → 打鍵 → `+ New worktree` → 起動、そのセルを閉じて worktree ごと削除、までを
1 ブラウザで通す。`page.screencast` は **2880×1800（retina 2x）**なので、クロップで寄っても
解像度が足りる。

切り出し（原素材は `footage/2026-08-10/acme-web-{create,close}-v3.mp4`）:

```sh
# 01 フォーム → worktree 行へズームイン（カットで切り替えない）。Creating… で着地する
ffmpeg -i acme-web-create-v3.mp4 -ss 0.80 -t 3.60 -an s1src.mp4
ffmpeg -i s1src.mp4 -vf "crop=1700:680:600:380,fps=60" -an s1crop.mp4
node ~/.claude/skills/mulmoterminal-video/camera-move.mjs s1crop.mp4 01-press-once.mp4 \
  --target 260,171,1160,464 --hold 1.5 --push 1.3 --tail 6.0 --canvas 1120x448

# 02 生きているセル。× に静的なリングを重ねる
ffmpeg -i acme-web-create-v3.mp4 -ss 8.00 -t 2.00 -an s2src.mp4
ffmpeg -i s2src.mp4 -vf "crop=2840:1136:20:110,tpad=stop_mode=clone:stop_duration=6.6,fps=60" -an 02-close-button.mp4

# 03 確認ダイアログ。Remove worktree に静的なリング
ffmpeg -i acme-web-close-v3.mp4 -ss 0.55 -t 2.00 -an s3src.mp4
ffmpeg -i s3src.mp4 -vf "crop=1600:640:641:626,setpts=1.20*PTS,tpad=stop_mode=clone:stop_duration=6.2,fps=60" -an 03-it-asks.mp4

# 04 減光 → 削除中 → セルが消える。実時間 1.6 秒しかないので 3.5 倍に伸ばす
ffmpeg -i acme-web-close-v3.mp4 -ss 2.55 -t 1.60 -an s4src.mp4
ffmpeg -i s4src.mp4 -vf "crop=1600:640:641:626,setpts=3.50*PTS,tpad=stop_mode=clone:stop_duration=3.0,fps=60" -an 04-removing.mp4
```

**スライドは全場面で同じ絶対座標**（見出し `top:84px`、クリップ `top:180px` の 1060px 幅）。
flex の中央寄せだと中身の高さで見出しとクリップが場面ごとに動き、切り替わるたびに画面が
揺れて見える。クリップ側も全部 2.5:1 に揃えて、変わるのは画角の中身だけにする。

**クリップは音声より長く作る（各 8.5 秒）。** 尺はナレーションが決めるので、クリップが短いと
末尾が凍る。長いぶんはビート終端で切られるだけで害がない。

| ファイル | 中身 |
|---|---|
| `01-press-once.mp4` | 1120×448 — フォーム → worktree 行へのズームイン |
| `02-close-button.mp4` | 2840×1136 — 生きているセル。× にリング |
| `03-it-asks.mp4` | 1600×640 — 確認ダイアログ。Remove worktree にリング |
| `04-removing.mp4` | 1600×640 — 減光 → 削除中 → セルが消える |

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
- **リングは `data-animation` で出さない。** クリップの再生時刻とアニメーションの時刻がずれて、
  1〜3 秒遅れて出る。確認ダイアログを指すリングが、ダイアログが消えたあとに現れて空中に浮いた。
  場面いっぱい出しっぱなしの静的なリングにする（そのぶん、リングが指すものが画面から消える
  場面では切って別の場面にする）。
- **状態が消える前で切る。** `Creating…` のクリップを「フォームが消えたあと」まで伸ばしていて、
  末尾のフリーズが空の矩形になり、2 秒ほど何も映らなかった。トリムの終わりは必ず
  「見せたい状態がまだ出ている」フレームにする。
- **同じ UI の寄り引きはカットではなくズームでつなぐ。** 起動フォームから worktree の行への
  切り替えをカットにしていたら、同じ画面が突然大きさだけ変わって見えた。`camera-move.mjs` の
  プッシュインにすると、どこを見ればいいかが動きで伝わる。
- **一瞬で終わる状態は伸ばす。** 削除の減光〜消滅は実時間 1.6 秒しかなく、そのまま置くと
  ビートの大半が「消えたあとの空のフォーム」になる。`setpts=3.5*PTS` で伸ばす。
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
