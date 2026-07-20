# YouTube 公開の運用

このフォルダは各動画の YouTube 公開情報（メタデータ）の正本を置く場所。
デッキ1本＝ファイル1つ（`<deck>_<lang>.md`、例: `collection-creation-demo_ja.md`）。
形式の手本は mulmocast-app の `docs/release_notes/*/youtube_*_ja.md`。

## playlist の方針

- **少数・固定**。公開のたびに新しく作るのではなく、既存 playlist に**足すだけ**にする（毎回の手間を最小化するため）。
- **番号(N/M)は振らない**。「1/3」等の絶対位置はタイトルにも説明文にも入れない — 間に1本足しただけで全動画の書き直しになるため。順序は playlist 自身が持つ。
- **1本の動画は複数 playlist に所属してよい**。マスターとシリーズの両方に入れられる。

playlist は目的で2種類に分ける:

- **A. コアセット導線（What→Why→How）** — 初見が順番に見る王道。Why(=vision)は代表1本だけ入れる（vision エッセイ群を全部は入れない）。
  - What: `demos/what-is-mulmoclaude` ／ Why: `vision/the-assistant-you-nurture` ／ How: `tutorials/collection-creation-demo`
- **B. トピック/How シリーズ** — 「作り方」をまとめて見る受け皿。vision は入れない。
  - 基礎（汎用の作り方）: `tutorials/collection-creation-demo` → 応用（テーマ別実演）: `kitchen-trio` → `pantry` → `csv-collection`
  - `collection-creation-demo` は「コレクションの作り方」の汎用基礎なので、テーマ(天気)に関わらず**先頭の入口**として入れる。テーマごとに作り方動画を作り直さない。

見せる順・相互 CTA の方針は `content-plan.md`（コアセット定義・What→Why→How）を正とする。

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

セクションは Title / Description / Playlist / Thumbnail / URL。

- **Description** — 冒頭で何の動画かのフック → 製品一行紹介 → チャプター → GitHub リンク（https://github.com/receptron/mulmoclaude）→ 末尾にハッシュタグ。
- **Playlist** — 所属予定/所属済みの playlist 名と `&list=` URL（未作成なら「未作成」と書く）。
