# デモ・チュートリアル制作の進捗管理

`mulmoclaude/` 配下（demos = What / tutorials = How）の ja/en 展開の状態を追う表。
**制作状態（叩き台・スクリプト・キャプチャ・mp4）の単一ソースはこのファイル**。`content-roadmap.md`（コンテンツマトリクス・コアセット戦略）と `what-materials.md`（素材集・執筆ルール）は企画（何を・どの順で・どういう構成で）を持ち、状態はここを参照する。
作業のルールと撮り方は `demos/DEMO-GUIDE.md` を参照。
更新タイミング: デッキの追加・キャプチャ撮影・finalize・モック差し替えを行ったとき。

**このファイルは現在の状態だけを持つ**。残作業・バックログの完了項目は ✅ を付けずに行ごと削除する（経緯の正本は commit / PR。デッキ表・タイトル表は現在の状態として保持）。決定・方針は content-roadmap.md へ。日付付きのスナップショット節は作らない。

## デッキ別ステータス

🔁 = 要撮り直し / 📝 = 下書き / — = 対象なし。完成し公開まで済んだ列は「済」。
企画# は content-roadmap.md のコンテンツマトリクスの番号(番号外 = マトリクス外の追加分)。

| デッキ | 企画# | ja スクリプト | ja キャプチャ | en スクリプト | en キャプチャ | en mp4/PDF |
|---|---|---|---|---|---|---|
| tutorials/collection-creation-demo | 番号外（コアセットの How） | 済（旧ネイビー配色） | 済・据え置き（英語名コレクション混在だが公開済みのため撮り直さない） | 済 | 済 11 枚 | 済 |
| tutorials/kitchen-trio-tutorial | tutorials #1（フラッグシップ） | 済 14 ビート | 済 10 枚 | 未着手 | 未着手（en ライブ再演） | — |
| tutorials/pantry-list-tutorial | 番号外（育てる編・kitchen 続編） | 済 9 ビート | 済 7 枚 | 未着手 | 未着手 | — |
| tutorials/csv-collection-tutorial | 番号外（新機能 How・CSV） | 済 13 ビート | 済 10 枚（素材 CSV は assets の source/） | 未着手 | 未着手 | — |
| demos/what-is-mulmoclaude | demos #1 | 済 | —（モック確定） | 済 | —（同左） | 済 |
| demos/collections-showcase | demos #3 | 済 | 済 3 枚 | 済 | 済 3 枚 | 済 |
| demos/weather-showcase | 番号外（showcase 追加分） | 済 | —（流用アセット 2 点のみ） | 済 | —（同左） | 済 |
| demos/connected-collections-demo | 番号外（新機能告知） | 済 | 済・beat 3 の一覧 1 枚のみ英語名混在（en 再演時に ja も撮り直す） | 済 | 済 6 枚 | 済 |
| demos/record-buttons-demo | 番号外（新機能告知） | 済 | 済 | 済 | 済 6 枚 | 済 |
| demos/calendar-showcase | demos #2 | 未着手（企画は content-roadmap.md「demos #2 Calendar Showcase の構成」） | — | 未着手 | — | — |
| tutorials/getting-started | tutorials #2 | 📝 未 commit | — | 未着手 | — | — |
| tutorials/building-a-collection | （旧 tutorials #1 下書き） | 📝 未 commit。kitchen-trio が tutorials #1 を実装、扱いは要判断 | — | — | — | — |


## タイトル・参照名の管理

動画内の相互参照（「〜という動画で」）と YouTube 等の公開タイトルのズレを防ぐための正はこの表。
**参照名は、そのデッキのタイトルページに実際に映っている文字から取る**（スクリプト title のメタデータではなく）。他デッキから言及するときは必ずこの表の参照名をそのまま使う。YouTube タイトルは公開時に決めて記入する。
YouTube 公開時の手順（メタデータ記入・playlist の作成/追加・説明文リンク）は `youtube/README.md` を参照。

| デッキ | スクリプト title（ja） | タイトルページの表記 | 参照名 | YouTube タイトル |
|---|---|---|---|---|
| tutorials/collection-creation-demo | コレクション作成デモ — 天気予報コレクション | eyebrow「コレクション作成デモ」+ 題「天気予報コレクション」 | コレクション作成デモ | ja: [天気予報コレクションを会話で作る — MulmoClaude コレクション作成デモ](https://youtu.be/VJMlTwRz6z4)（メタデータ: youtube/collection-creation-demo_ja.md）<br>en: [Build a Weather Collection by Talking — MulmoClaude Collection Creation Demo](https://youtu.be/D-937j0jkyo)（メタデータ: youtube/collection-creation-demo.md） |
| tutorials/kitchen-trio-tutorial | 台所の三点セットを、会話で作る | 同左 | 台所の三点セットを、会話で作る | ja: [台所の三点セットを、会話で作る — MulmoClaude チュートリアル](https://youtu.be/s7wbM32vLL4)（メタデータ: youtube/kitchen-trio-tutorial_ja.md） |
| tutorials/pantry-list-tutorial | コレクションは、使いながら育てる — 常備品リスト編 | 題「使いながら、育てる」 | 常備品リスト編（使いながら、育てる） | ja: [コレクションは、使いながら育てる — MulmoClaude 常備品リスト編](https://youtu.be/b_SlGYyWToU)（メタデータ: youtube/pantry-list-tutorial_ja.md） |
| tutorials/csv-collection-tutorial | CSVは、置くだけでいい | 同左 | CSVは、置くだけでいい | ja: [CSVは、置くだけでいい — MulmoClaude CSVコレクション](https://youtu.be/c6CkrgYWC2M)（メタデータ: youtube/csv-collection-tutorial_ja.md） |
| demos/collections-showcase | コレクション実例集 — 暮らしのアプリが、ひとつの会話でつながる | 「コレクション実例集」+ 見出し「暮らしのアプリが、ひとつの会話でつながる。」 | コレクション実例集 | ja: [暮らしのアプリが、ひとつの会話でつながる — MulmoClaude コレクション実例集](https://youtu.be/Q5HKzDUhs1g)（メタデータ: youtube/collections-showcase_ja.md）<br>en: [Your Everyday Apps, Connected by One Conversation — MulmoClaude Collections](https://youtu.be/2D-R7MpCB_I)（メタデータ: youtube/collections-showcase.md） |
| demos/what-is-mulmoclaude | MulmoClaude で何ができる？ | 見出し「できることは、暮らしの数だけ。」 | — | ja: [できることは、暮らしの数だけ — MulmoClaude 3分ツアー](https://youtu.be/TDzy0KcHuag)（メタデータ: youtube/what-is-mulmoclaude_ja.md）<br>en: [As Many Uses as There Are Lives — A 3-Minute Tour of MulmoClaude](https://youtu.be/yogapAc9nds)（メタデータ: youtube/what-is-mulmoclaude.md） |
| demos/weather-showcase | 明日の天気は、もう予定に入っている | 同左 | — | 未定 |
| demos/connected-collections-demo | バラバラのデータが、つながる | — | — | ja: [バラバラのデータが、つながる — MulmoClaude 新機能 バックリンク＆ロールアップ](https://youtu.be/6XJywDCJ7V0)（メタデータ: youtube/connected-collections-demo_ja.md）<br>en: [Scattered Data, Connected — Backlinks & Rollups in MulmoClaude](https://youtu.be/FmQ9HVirrf8)（メタデータ: youtube/connected-collections-demo.md） |
| demos/record-buttons-demo | 押すだけの仕事は、ボタンにする | — | — | ja: [押すだけの仕事は、ボタンにする — MulmoClaude 新機能 レコードボタン](https://youtu.be/VaZur8HDjI4)（メタデータ: youtube/record-buttons-demo_ja.md）<br>en: [Turn Routine Work into Buttons — Record Buttons in MulmoClaude](https://youtu.be/81oYVOYDbik)（メタデータ: youtube/record-buttons-demo.md） |

### 見た目スタイルの使い分け

- **What（demos: showcase / what-is / weather）** = 方眼罫線入りの誌面（実例集）スタイル
- **How（tutorials: kitchen / pantry / collection-creation）** = 罫線なしの暖色グラデ・チュートリアルスタイル

この使い分けは意図的なもの。新デッキも所属（What/How）に合わせる。モックの差し替え方針は「collections-showcase のみ実キャプチャ、what-is / weather はモックのまま確定」。

## 残作業

1. **X の URL 記帳** — 状態の正本は各メタデータの「投稿枠」「投稿後」行。一覧は書き写さず `mulmo-x-status` スキルで導出する（`node ~/.claude/skills/mulmo-x-status/scripts/x-status.mjs`）
2. **weather-showcase** — Slack で確認依頼中（2026-07-25〜）。承認後: 公開一式の提示 → 公開 → 「できること」playlist を手動ソートへ切替 + マスター並び順の更新（`youtube/README.md` が正本）→ メタデータ作成・タイトル表記帳 → X 予約（8/1 枠）
3. **講座 3 本の en**（kitchen-trio → pantry → csv）— kitchen の ja golden データは en workspace へ英訳投入済み。次は en workspace での英語ライブ再演・収録 → en スクリプト作成・finalize
4. **calendar-showcase（demos #2）の制作着手** — 企画は content-roadmap.md
5. **未 commit 下書き 3 本の扱い判断** — `tutorials/getting-started` / `tutorials/building-a-collection` / `demos/daily-workflow`（demos #2 吸収により役割終了）。破棄か別テーマか
6. **未決**: en X（@mulmocast）の動画告知 5 本の文面と開始日
7. **週次リリースノート動画の試作 1 本** — content-roadmap の 3 レーン構成参照。フォーマット（1 機能 1 ビート・2 分前後・ss web 記事の派生まで）をここで詰める
8. 任意: 生成済み .srt の YouTube 字幕アップ / 新デッキ企画「お買い物モードを会話で作る」（素材: ja workspace セッション a0627168。kitchen-trio ビート 8 が予告済み）/ csv 分析ビートに「発注先」列を足す改良（en 版収録か続編で）

## 既知のズレ（据え置き）

- **ja 台所系の献立日付**: `collections-showcase_ja` / `kitchen-trio-tutorial_ja` は買い物リストのメモが「月〜木」なのに日付が 7/21〜24（火〜金）で、「木曜は洋風」が画面と 1 日ずれている。公開済みのため差し替えない。en は公開前に 7/27〜30（月〜木）へ修正済み。ja の台所データを撮り直す機会に合わせる
- **en 翻訳レビューの保留 2 件**: `collection-creation-demo` beat 8 の en キャプチャがファイルパスを写していて ja より技術寄り / `collections-showcase` 締めバッジが ja「育」・en 🌱（破綻はしていない）
