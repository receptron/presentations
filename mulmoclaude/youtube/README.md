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

### playlist の並び順（YouTube 上の並びの正本）

動画を追加・公開したらここを更新し、YouTube 側の並びをこの順に合わせる。
手動並べ替えを使うのは**マスターのみ**。他はソート設定で自動的にこの順になる（各 playlist に記載）。

<details><summary>MulmoClaude（日本語） — ソート: YouTube 内で手動</summary>

1. 自分で育てるAIアシスタント（中島聡氏・Life is Beautiful）
2. できることは、暮らしの数だけ — MulmoClaude 3分ツアー
3. 暮らしのアプリが、ひとつの会話でつながる — MulmoClaude コレクション実例集
4. 天気予報コレクションを会話で作る — MulmoClaude コレクション作成デモ
5. 台所の三点セットを、会話で作る — MulmoClaude チュートリアル
6. コレクションは、使いながら育てる — MulmoClaude 常備品リスト編
7. CSVは、置くだけでいい — MulmoClaude CSVコレクション
8. バラバラのデータが、つながる — MulmoClaude 新機能 バックリンク＆ロールアップ
9. 押すだけの仕事は、ボタンにする — MulmoClaude 新機能 レコードボタン

（weather-showcase 公開後は 3 の次に挿入）

</details>

<details><summary>MulmoClaude でできること — ソート: 公開日（新しい順）</summary>

1. できることは、暮らしの数だけ — MulmoClaude 3分ツアー
2. 暮らしのアプリが、ひとつの会話でつながる — MulmoClaude コレクション実例集

（weather-showcase を公開すると「新しい順」では先頭に来てしまうため、公開時に「YouTube 内で手動」へ切り替えて上記順に直す）

</details>

<details><summary>MulmoClaude コレクションの作り方 — ソート: 公開日（古い順）</summary>

1. 天気予報コレクションを会話で作る — MulmoClaude コレクション作成デモ（基礎・入口）
2. 台所の三点セットを、会話で作る — MulmoClaude チュートリアル
3. コレクションは、使いながら育てる — MulmoClaude 常備品リスト編
4. CSVは、置くだけでいい — MulmoClaude CSVコレクション

</details>

<details><summary>MulmoClaude 機能紹介 — ソート: 公開日（古い順）</summary>

1. バラバラのデータが、つながる — MulmoClaude 新機能 バックリンク＆ロールアップ
2. 押すだけの仕事は、ボタンにする — MulmoClaude 新機能 レコードボタン

</details>

説明文の共通ブロック（製品紹介）は全動画・全 playlist で次の文に統一する（中島聡氏の表現に準拠）:

> MulmoClaudeは「AIアシスタント育成ツール」で、オープンソースで公開されています。AIエンジンには Claude Code を使っています。ぜひ、自分だけのAIアシスタントをあなたのパソコンの上で育ててください。

ハッシュタグには `#ClaudeCode` を必ず含める（Claude Code は検索起点として MulmoClaude より圧倒的に強いため）。

コンテンツの階層（総論 → showcase → How）と制作パイプラインは `../content-roadmap.md` を正とする。

### 英語版の playlist（2026-07-27 作成済み）

en の playlist も 4 本。所属ルールは ja と同じ「**全動画 → マスター ＋ トピック playlist のどれか 1 つ**」。ja には混ぜない。

- **MulmoClaude (English)**（マスター） — 全動画を入れる。公開済みの vision 動画 [An AI Assistant Is Something You Nurture, Not Something You Buy](https://www.youtube.com/watch?v=Wonr3eOPww4) を先頭に置く入口。並び順は導線として管理する: vision → what-is → showcase → 作り方 → 機能紹介。
  - https://www.youtube.com/playlist?list=PLK5YLxSUugRA
- **What MulmoClaude Can Do** — 総論（`what-is-mulmoclaude`）とテーマ別 showcase（`collections-showcase`, `weather-showcase`, …）。初見の人に見せる棚。
  - https://www.youtube.com/playlist?list=PLbWRoQApuX14
- **Building Collections with MulmoClaude** — How 連続講座。基礎 `collection-creation-demo` → `kitchen-trio` → `pantry` → `csv-collection`。「▶ 順番に見る」リンクはこれを張る。
  - https://www.youtube.com/playlist?list=PLVyZ79Q40gCY
- **MulmoClaude Feature Demos** — 機能単位の解説と新機能告知（`connected-collections-demo`, `record-buttons-demo`、今後: フィード、wiki、Skills 等）。すでに使っている人向けの棚。
  - https://www.youtube.com/playlist?list=PLRMyMyvS-8tA

#### 英語版 playlist の並び順（YouTube 上の並びの正本）

ja と同じ運用。動画を追加・公開したらここを更新し、YouTube 側の並びをこの順に合わせる。
手動並べ替えを使うのは**マスターのみ**。他はアップロード順＝この順になるようにして、ソート設定「公開日（古い順）」で維持する。

<details><summary>MulmoClaude (English) — ソート: YouTube 内で手動</summary>

1. An AI Assistant Is Something You Nurture, Not Something You Buy（公開済み・vision）
2. As Many Uses as There Are Lives — A 3-Minute Tour of MulmoClaude
3. Your Everyday Apps, Connected by One Conversation — MulmoClaude Collections
4. Build a Weather Collection by Talking — MulmoClaude Collection Creation Demo
5. Scattered Data, Connected — Backlinks & Rollups in MulmoClaude
6. Turn Routine Work into Buttons — Record Buttons in MulmoClaude

（weather-showcase の en を公開したら 3 の次に挿入）

</details>

<details><summary>What MulmoClaude Can Do — ソート: 公開日（古い順）</summary>

1. As Many Uses as There Are Lives — A 3-Minute Tour of MulmoClaude
2. Your Everyday Apps, Connected by One Conversation — MulmoClaude Collections

（この順にアップロードすれば「古い順」で維持できる。崩れたら「YouTube 内で手動」へ切り替える）

</details>

<details><summary>Building Collections with MulmoClaude — ソート: 公開日（古い順）</summary>

1. Build a Weather Collection by Talking — MulmoClaude Collection Creation Demo

（kitchen-trio → pantry → csv-collection の en が揃うたびに末尾へ追加される）

</details>

<details><summary>MulmoClaude Feature Demos — ソート: 公開日（古い順）</summary>

1. Scattered Data, Connected — Backlinks & Rollups in MulmoClaude
2. Turn Routine Work into Buttons — Record Buttons in MulmoClaude

</details>

説明文の共通ブロック（英語）は全動画・全 playlist で次の文に統一する。ja の「AIアシスタント育成ツール」に対応し、デッキで統一した nurture を使う:

> MulmoClaude is an "AI assistant nurturing tool", released as open source. It uses Claude Code as its AI engine. Nurture an AI assistant of your own, on your own computer.

ハッシュタグには ja と同じく `#ClaudeCode` を必ず含める。

playlist 作成時に貼る説明文（各末尾に上の共通ブロックと `https://github.com/receptron/mulmoclaude` を付ける）:

```
MulmoClaude (English)
Everything about MulmoClaude, in English. Start here: what it can do, how to build your first collection, and what each feature looks like in use.
```

```
What MulmoClaude Can Do
Real examples of what people build with MulmoClaude — personal apps for records, plans and the weather, all born from ordinary conversation. Watch these first if you are new here.
```

```
Building Collections with MulmoClaude
A short course on building collections by talking. Start with the weather collection, then follow the kitchen, pantry and CSV episodes as they are published.
```

```
MulmoClaude Feature Demos
One feature at a time: backlinks and rollups, record buttons, and more as they ship. For people already using MulmoClaude.
```

**タイトルの制約**: en のスライドは他の動画をタイトルで名指ししている。参照が外れないよう、YouTube タイトルは次を満たすこと。

- `collection-creation-demo` のタイトルに **Collection Creation Demo** を含める（what-is / collections-showcase / weather-showcase の締めが参照）
- vision の en は公開済みだが、**公開タイトルがデッキの `title` と違う**（デッキ: `An AI Assistant Nurturing Tool` / 公開: `An AI Assistant Is Something You Nurture, Not Something You Buy`）。what-is の締めの参照を公開タイトルに合わせて修正済み（2026-07-27）。以後もデッキ側を公開タイトルに合わせる

## 公開時チェックリスト

動画を公開したら、Claude は次を行う／ユーザーに伝える:

1. **メタデータファイル記入** — `mulmoclaude/youtube/<deck>_<lang>.md` を作成し、Title / Description（末尾にハッシュタグ）/ Playlist / Thumbnail / URL を埋める。タグは説明文のハッシュタグに集約し、独立した Tags 欄は作らない。
2. **PROGRESS.md 記入** — タイトル管理表の該当行「YouTube タイトル」列に、タイトル＋動画 URL をリンク形式で記入。
3. **playlist をユーザーに依頼（YouTube 側の操作は Claude にはできない）**:
   - この動画を所属 playlist（A / B）に**追加**するよう伝える。
   - 該当する playlist がまだ無ければ、**新規作成**するよう伝える。
4. **新規 playlist を作った場合** — その playlist に入るべき**過去の動画**（例: `collection-creation-demo`）も追加するよう、あわせてユーザーに伝える。新規 playlist は最新1本だけでは順序が成立しないため。
5. **説明文リンク** — playlist ができたら、ユーザーから `&list=<ID>` を受け取り、説明文に `▶ 順番に見る（<playlist 名>）: https://www.youtube.com/watch?v=<動画ID>&list=<ID>` を追記し、メタデータファイルの Playlist 欄にも反映する。
6. **生成物の片付け** — YouTube 公開と X 投稿（mp4 添付・予約含む）まで済んだデッキは、`output/<deck>/` を `output/done/<deck>/` へ移す。メタデータファイル内の `output/<deck>/…` という記載は書き換えず、公開済みは `output/done/` 配下と読み替える（再 finalize するときは元の位置に戻すと生成キャッシュが効く）。

## メタデータファイルの形式

セクションは Title / Description / Playlist / Thumbnail / URL / X 投稿（日本語・任意）。

- **Description** — 冒頭で何の動画かのフック → 製品一行紹介 → チャプター → 起動 1 行（`始めるのは、ターミナルにこの1行だけ：npx mulmoclaude@latest`）→ GitHub リンク（https://github.com/receptron/mulmoclaude）→ 末尾にハッシュタグ。X 投稿も同じ起動 1 行を GitHub リンクの直前に入れる（リンクを増やさず行動導線を作る）。
  - 所属 playlist があれば、冒頭フックの直後に `▶ 順番に見る（<playlist 名>）: https://www.youtube.com/playlist?list=<ID>` を置く。playlist が無い間は省略し、**作成後に説明文へ追記**する（公開済み動画は YouTube Studio で説明文を編集）。
- **Playlist** — 所属予定/所属済みの playlist 名と `&list=` URL（未作成なら「未作成」と書く）。

## X 告知の運用

- X 原案（日本語）は各動画のメタデータファイルの `## X 投稿（日本語）` 節が**正本**。投稿後は同節の「投稿後」行に X ポスト URL を記入する
- 動画は YouTube リンクではなく **mp4 をネイティブ添付**する（video_view・滞在時間が X の予測対象のため。日本語アカウントは課金済みで長尺可）。本文には YouTube 動画リンクを入れず、所属 playlist のリンクと GitHub リンクで導線を作る
- 文面ルール: 初見でも分かる製品の一文紹介 / ユーザー価値から文章化（機能名先行・箇条書き羅列は NG）/ 末尾に返信を促す CTA / 煽り語を避けた誠実なトーン / タグは `#MulmoClaude #AI #VibeCrafting`
- **提示・投稿前に Codex クロスチェック必須**（`codex exec --sandbox read-only` に文面ルールを埋め込んでレビューさせ、MUST FIX ゼロにする。mulmoclaude ワークスペースの `mulmo-beta-announcements` スキルの運用に準拠）
- ペース: 動画告知は **1 日 1 本・20:30 JST**（同一話題の同日連投は減衰するため 1 日 1 本を守る。20:30 は毎日の定常便（テキスト告知）と同じ夜枠 — 定常便と同日になる場合は動画側を昼 12:15 にずらす。週次リリースノート動画は対象外 — 土曜 20:30 固定、正本は roadmap）。朝 10:00 は 10 秒クリップ枠で、話題が別なら同日でも可。**レーン構成・クリップの上限や対象はここに写さない** — `../content-roadmap.md` の「リリース告知の 3 レーン構成」が正本
