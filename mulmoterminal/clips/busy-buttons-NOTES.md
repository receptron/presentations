# busy-buttons — MulmoTerminal 4.7.3 の機能紹介クリップ

15 秒・3 ビート。MulmoTerminal のリリースごとに短尺クリップを出すための 1 本目で、
`mulmoclaude/demos/clips/collection-map_ja.json`（10 秒・1 ビート）の続き。

| | |
|---|---|
| 題材 | 4.7.3 — `+ New worktree` が押した回数だけ worktree を作っていた問題（#1549）と、削除中のセルの表示（#1551） |
| 尺 | 英語 15.0 秒 / 日本語 14.6 秒 |
| 出典 | mulmoterminal `docs/guide/{en,ja}/v4.7.3.md`、`docs/ChangeLog.md` の 4.7.3 |

## リポジトリ規約からの意図的な逸脱

**スライドは英語だけ。日本語版もスライドは英語のまま、ナレーションと字幕だけが日本語。**
規約（リポジトリ CLAUDE.md）は「`_ja` 先行 → 英語版へ翻訳、スライドも撮影素材も両方作る」だが、
MulmoTerminal のクリップはこの方針を取らない。したがって:

- 素材ディレクトリは `busy-buttons-assets/` **1 つだけ**（`-assets-ja` は作らない）。
  日本語版のスライドが存在しないので、日本語用の素材も存在しない
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

## 素材

`busy-buttons-assets/` の中身と作り方（元は mulmoterminal の `docs/guide/images/`）:

| ファイル | 元 | 加工 |
|---|---|---|
| `worktree-creating.png` | `v4.7.3-worktree-creating.png` | 上端の切れた行を落とす `crop=580:97:0:12` |
| `cell-removing.png` | `v4.7.3-cell-removing.png` | 無加工。下 2 つの切り出し元として置いてある（デッキからは参照していない） |
| `removing-header.png` | 同上 | `crop=988:78:0:8` |
| `removing-spinner.png` | 同上 | `crop=530:82:230:285` |

**ビート 3 でセル全体を出すのはやめた。** 988×649 のセルを 1280×720 のキャンバスに収めると
`Removing acme-web (fix-login)…` が実質 9px になって読めない（skill の「俯瞰と読ませの使い分け」）。
`camera-move.mjs` のプッシュインも試したが、このセルは削除中で中身が空なので、寄り切った先が
ただの暗い矩形になり文脈が消える。採用したのは 90s-v2 NOTES にある**縦積みの静止クローズアップ** —
減光したヘッダー帯（等倍）と、スピナー帯（1.6 倍、ズームであることを示す枠付き）を重ねる。

## 引っかかったところ

- **Gemini TTS が 1 ビートで 116 秒の音声を返した。** 日本語ビート 1 の
  「押すたびに、ワークツリーができていました。同じものが、三つ。」で発生。体言止めの短い断片が
  引き金と見て、1 文にまとめ直したら 5.3 秒に収まった。音声は内容ハッシュでキャッシュされるので、
  暴走した音声は**本文を変えるか `-f`** で取り直す（同じ本文の再実行では戻ってこない）
- **TTS は単発で落ちることがある。** 日本語の初回レンダーが `ttsGeminiAgent` のエラーで止まり、
  同じコマンドの再実行で通った
- **`scripts/validate-all.js` は `mulmoclaude/` しか走査していない。** `mulmoterminal/` 配下は
  `npm test` の対象外なので、このクリップも launch デッキ 3 本も CI では検証されない。
  検証は個別に `npm run validate -- <file>` を回す必要がある（走査対象の修正は別 PR）
