# YouTube 公開の運用

このフォルダは各動画の YouTube 公開情報（メタデータ）の正本を置く場所。
デッキ1本＝ファイル1つ（`<deck>_<lang>.md`、例: `collection-creation-demo_ja.md`）。
形式の手本は mulmocast-app の `docs/release_notes/*/youtube_*_ja.md`。

## playlist の方針

- **少数・固定**。公開のたびに新しく作るのではなく、既存 playlist に**足すだけ**にする（毎回の手間を最小化するため）。
- **番号(N/M)は振らない**。「1/3」等の絶対位置はタイトルにも説明文にも入れない — 間に1本足しただけで全動画の書き直しになるため。順序は playlist 自身が持つ。
- **1本の動画は複数 playlist に所属してよい**。マスターとトピックの両方に入れられる。
- **ja / en は playlist を分ける**。en 動画の公開が始まったら「MulmoClaude (English)」等を別途作る（ja に混ぜない）。

ja の playlist は 4 本（2026-07-22 作成済み）。所属ルールは「**全動画 → マスター ＋ トピック playlist のどれか 1 つ**」で機械的に決める:

- **MulmoClaude（日本語）**（マスター） — 全動画を入れる。中島聡氏の vision 動画「自分で育てるAIアシスタント」を含む、メルマガ読者の入口。並び順は導線として管理する: vision → what-is → showcase → 作り方 → 機能紹介。
  - https://www.youtube.com/playlist?list=PLPS3_Hl0r6Ic
- **MulmoClaude でできること** — 総論（`what-is-mulmoclaude`）とテーマ別 showcase（`collections-showcase`, `weather-showcase`, …）。初見の人に見せる棚。
  - https://www.youtube.com/playlist?list=PLPFzwVwcieOI
- **MulmoClaude コレクションの作り方** — How 連続講座。基礎 `collection-creation-demo` → `kitchen-trio` → `pantry` → `csv-collection`。「▶ 順番に見る」リンクはこれを張る。`collection-creation-demo` は汎用基礎なのでテーマ(天気)に関わらず先頭の入口。テーマごとに作り方動画を作り直さない。
  - https://www.youtube.com/playlist?list=PLYPiiR7YGHJI
- **MulmoClaude 機能紹介** — 機能単位の解説と新機能告知（`connected-collections-demo`, `record-buttons-demo`、今後: フィード、wiki、Skills 等）。すでに使っている人向けの棚。
  - https://www.youtube.com/playlist?list=PLEN0vGL7IeUQ

説明文の共通ブロック（製品紹介）は全動画・全 playlist で次の文に統一する（中島聡氏の表現に準拠）:

> MulmoClaudeは「AIアシスタント育成ツール」で、オープンソースで公開されています。AIエンジンには Claude Code を使っています。ぜひ、自分だけのAIアシスタントをあなたのパソコンの上で育ててください。

ハッシュタグには `#ClaudeCode` を必ず含める（Claude Code は検索起点として MulmoClaude より圧倒的に強いため）。

コンテンツの階層（総論 → showcase → How）と制作パイプラインは `../content-roadmap.md` を正とする。

## 公開時チェックリスト

動画を公開したら、Claude は次を行う／ユーザーに伝える:

1. **メタデータファイル記入** — `mulmoclaude/youtube/<deck>_<lang>.md` を作成し、Title / Description（末尾にハッシュタグ）/ Playlist / Thumbnail / URL を埋める。タグは説明文のハッシュタグに集約し、独立した Tags 欄は作らない。
2. **PROGRESS.md 記入** — タイトル管理表の該当行「YouTube タイトル」列に、タイトル＋動画 URL をリンク形式で記入。
3. **playlist をユーザーに依頼（YouTube 側の操作は Claude にはできない）**:
   - この動画を所属 playlist（A / B）に**追加**するよう伝える。
   - 該当する playlist がまだ無ければ、**新規作成**するよう伝える。
4. **新規 playlist を作った場合** — その playlist に入るべき**過去の動画**（例: `collection-creation-demo`）も追加するよう、あわせてユーザーに伝える。新規 playlist は最新1本だけでは順序が成立しないため。
5. **説明文リンク** — playlist ができたら、ユーザーから `&list=<ID>` を受け取り、説明文に `▶ 順番に見る（<playlist 名>）: https://www.youtube.com/watch?v=<動画ID>&list=<ID>` を追記し、メタデータファイルの Playlist 欄にも反映する。

## メタデータファイルの形式

セクションは Title / Description / Playlist / Thumbnail / URL / X 投稿（日本語・任意）。

- **Description** — 冒頭で何の動画かのフック → 製品一行紹介 → チャプター → GitHub リンク（https://github.com/receptron/mulmoclaude）→ 末尾にハッシュタグ。
  - 所属 playlist があれば、冒頭フックの直後に `▶ 順番に見る（<playlist 名>）: https://www.youtube.com/playlist?list=<ID>` を置く。playlist が無い間は省略し、**作成後に説明文へ追記**する（公開済み動画は YouTube Studio で説明文を編集）。
- **Playlist** — 所属予定/所属済みの playlist 名と `&list=` URL（未作成なら「未作成」と書く）。

## X 告知の運用

- X 原案（日本語）は各動画のメタデータファイルの `## X 投稿（日本語）` 節が**正本**。投稿後は同節の「投稿後」行に X ポスト URL を記入する
- 動画は YouTube リンクではなく **mp4 をネイティブ添付**する（video_view・滞在時間が X の予測対象のため。日本語アカウントは課金済みで長尺可）。本文には YouTube 動画リンクを入れず、所属 playlist のリンクと GitHub リンクで導線を作る
- 文面ルール: 初見でも分かる製品の一文紹介 / ユーザー価値から文章化（機能名先行・箇条書き羅列は NG）/ 末尾に返信を促す CTA / 煽り語を避けた誠実なトーン / タグは `#MulmoClaude #AI #VibeCrafting`
- **提示・投稿前に Codex クロスチェック必須**（`codex exec --sandbox read-only` に文面ルールを埋め込んでレビューさせ、MUST FIX ゼロにする。mulmoclaude ワークスペースの `mulmo-beta-announcements` スキルの運用に準拠）
- ペース: 1 日 1 本・夜枠・週末スキップ（同一話題の連投は減衰するため）
