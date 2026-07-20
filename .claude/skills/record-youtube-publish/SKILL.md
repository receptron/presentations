---
name: record-youtube-publish
description: MulmoScript デッキを YouTube 公開する際の、タイトル/説明文/チャプター/サムネの下書きと、公開後のリポジトリ記録（メタデータファイル・PROGRESS.md・playlist リマインド）を一括で行う。「YouTube に公開」「YouTube 用の title/description」「公開情報を記録」等で起動。
allowed-tools: Read, Edit, Write, Bash, Glob, Grep
user-invocable: true
---

# /record-youtube-publish — MulmoCast デッキの YouTube 公開支援

MulmoScript デッキ（`mulmoclaude/**/<deck>.json`）を YouTube 公開するときの下書き作成と、公開後のリポジトリ記録をまとめる。
運用の正本は `mulmoclaude/youtube/README.md`。このスキルはその手順を実行する。

## 引数

```
/record-youtube-publish <deck パス> [公開後の URL]
```

- URL 未指定 = 公開前（title/description/チャプター/サムネの下書きまで）
- URL 指定 = 公開後（メタデータファイル・PROGRESS.md 記入・playlist リマインドまで）

## 手順

### 1. デッキの把握（コンテキスト節約）

MulmoScript JSON はフル Read せず、ナレーションだけ抽出する（`~/.claude/rules/mulmoscript.md`）:

```bash
node -e "const s=require('./<deck>.json'); console.log(s.title, s.description); s.beats.forEach((b,i)=>b.text&&console.log(i+1, b.text))"
```

### 2. チャプター算出

レンダリング済みなら `output/<deck>/audio/` から算出:

```bash
npm run chapters -- <deck パス>
```

- beat ごとの開始時刻が出る。**どの beat をチャプターにするか・ラベルは編集判断**（16 beat 全部ではなく意味のある区切りに絞る）
- 音声ファイルが無ければエラーで停止する（フォールバックしない）。先に `npm run movie -- <deck>` でレンダリングする

### 3. title / description の下書き

**手本を必ず参照してから書く**（`~/.claude/CLAUDE.md` の Deliverable Style Feedback）:

- 形式の手本: mulmocast-app の `docs/release_notes/*/youtube_*_ja.md`（場所は `MULMOCLAUDE_CODE_REPO`）と、`mulmoclaude/youtube/collection-creation-demo_ja.md`
- **手本に無いセクション/欄は足さない**（例: 独立した Tags 欄は作らない。タグは説明文末尾のハッシュタグに集約）
- 参照名・相互リンクの正は `mulmoclaude/PROGRESS.md` のタイトル管理表
- Title: 先頭15文字にフック。タイトルページの参照名を含める
- Description: フック → 製品一行紹介 → チャプター → GitHub リンク（https://github.com/receptron/mulmoclaude）→ ハッシュタグ。所属 playlist があれば冒頭フック直後に `▶ 順番に見る: …&list=<ID>`
- サムネ候補は `output/<deck>/images/*.png` を Read して提案（多くは beat1 = `0p.png` のフック画面）

### 4. 公開後の記録（URL があるとき）

`mulmoclaude/youtube/README.md` の公開時チェックリストを実行:

1. `mulmoclaude/youtube/<deck>_<lang>.md` を作成（Title / Description / Playlist / Thumbnail / URL）
2. `PROGRESS.md` タイトル管理表の該当行「YouTube タイトル」に タイトル＋URL をリンク形式で記入
3. **ユーザーに伝える**（YouTube 側操作は Claude にはできない）: この動画を所属 playlist に追加 / 無ければ新規作成
4. **新規 playlist を作った場合**: 過去動画（例 `collection-creation-demo`）もその playlist に追加するよう伝える
5. playlist ができたら `&list=<ID>` をもらい、説明文リンクとメタデータの Playlist 欄に反映（公開済み動画は Studio で説明文編集）

### 5. commit

グローバル git ルールに従う（明示パス add・英語メッセージ・`feat:`/`docs:` prefix・別 commit で修正）。ブランチが main なら先にフィーチャーブランチを切る。

## 注意

- アップロード自体はこのスキルでは行わない（ユーザーが YouTube 側で実施）。グローバルの `/youtube-upload` は news-shorts 系向けで、本リポジトリのプレゼン動画は README の運用に従う
