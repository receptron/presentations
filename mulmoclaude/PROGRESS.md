# デモ・チュートリアル制作の進捗管理

`mulmoclaude/` 配下（demos = What / tutorials = How）の ja/en 展開の状態を追う表。
**制作状態（叩き台・スクリプト・キャプチャ・mp4）の単一ソースはこのファイル**。`content-roadmap.md`（コンテンツマトリクス・コアセット戦略）と `what-materials.md`（素材集・執筆ルール）は企画（何を・どの順で・どういう構成で）を持ち、状態はここを参照する。
作業のルールと撮り方は `demos/DEMO-GUIDE.md` を参照。
更新タイミング: デッキの追加・キャプチャ撮影・finalize・モック差し替えを行ったとき。

## デッキ別ステータス

✅ = 完了 / 🔁 = 要撮り直し / 📝 = 下書き / — = 対象なし
企画# は content-roadmap.md のコンテンツマトリクスの番号(番号外 = マトリクス外の追加分)。

| デッキ | 企画# | ja スクリプト | ja キャプチャ | en スクリプト | en キャプチャ | en mp4/PDF |
|---|---|---|---|---|---|---|
| tutorials/kitchen-trio-tutorial | T1（フラッグシップ） | ✅ 14 ビート（答え合わせビートは削除 — スマホチェックと矛盾のため。demo-08 は未使用アセットとして保持） | ✅ 10 枚（ja workspace ライブ + 実機スマホ 1 枚） | 未着手 | 未着手（en ライブ再演） | —（ja mp4/PDF は ✅） |
| tutorials/collection-creation-demo | コアセットの How | ✅（旧ネイビー配色） | ✅ 据え置き（2026-07-27 判断）— 旧混合 workspace 産でコレクション名が英語のまま（`demo-28-collections-1280.png` 等）だが、ja は公開済みのため撮り直さない | ✅ | ✅ 11 枚 | ✅ |
| demos/connected-collections-demo | 番号外（新機能告知） | ✅ | ✅ 公開可（2026-07-22 全 6 枚確認。実害は beat 3 のコレクション一覧 1 枚のみ＝英語名コレクション混在。en 再演時に ja も撮り直す） | ✅ | ✅ 6 枚（ライブ再演） | ✅ |
| demos/record-buttons-demo | 番号外（新機能告知） | ✅ | ✅ 公開可（2026-07-22 全 6 枚確認。撮り直し不要） | ✅ | ✅ 6 枚（ライブ再演） | ✅ |
| demos/weather-showcase | 番号外（showcase 追加分） | ✅ | —（流用アセット 2 点のみ） | ✅ | —（同左） | ✅ |
| demos/collections-showcase | D3 | ✅ | ✅ 3 枚（kitchen golden のクロップ） | ✅ | ✅ 3 枚（en workspace の実キャプチャ。2026-07-26 差し替え） | ✅ |
| demos/what-is-mulmoclaude | D1 | ✅ | —（モックのみ） | ✅ | —（同左） | ✅ |
| demos/calendar-showcase | D2 | 未着手（企画のみ — 4 段構成は content-roadmap.md の「D2 Calendar Showcase の構成」参照。旧 D2「A Day with MulmoClaude」を吸収して改題） | — | 未着手 | — | — |
| tutorials/getting-started | T2 | 📝 未 commit | — | 未着手 | — | — |
| tutorials/building-a-collection | （旧 T1 下書き） | 📝 未 commit。kitchen-trio が T1 を実装、下書きの扱いは要判断 | — | — | — | — |
| tutorials/pantry-list-tutorial | 番号外（育てる編・kitchen 続編） | ✅ 9 ビート（在庫管理否定の設計ビートは削除し、STEP1 のナレーション一言に縮約） | ✅ 7 枚（ja workspace ライブ） | 未着手 | 未着手 | —（ja mp4/PDF は ✅） |
| tutorials/csv-collection-tutorial | 番号外（新機能 How・CSVデータコレクション） | ✅ 13 ビート（在庫分布を現実的に直した v2 データで再収録・差し替えはチャット経由・スマホビート追加） | ✅ 10 枚（ja workspace ライブ再収録 9 枚＋スマホ実機 1 枚。モバイルビュー「商品一覧」は会話で作成）。素材 CSV は assets の source/ に保存 | 未着手 | 未着手 | —（ja mp4/PDF は ✅） |

ja の mp4/PDF は旧キャプチャ前提のため、ja キャプチャ撮り直し後に finalize し直す。

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

相互参照の現状（2026-07-19 検証）: kitchen beat 3・15 →「コレクション作成デモ」✅／kitchen beat 15 →「コレクション実例集」（旧「コレクションでつながる暮らし」から修正済み）／pantry beat 10 →「台所の三点セットを、会話で作る」✅＋お買い物モード（未制作の予告）。

### 見た目スタイルの使い分け（2026-07-19 確認）

- **What（demos: showcase / what-is / weather）** = 方眼罫線入りの誌面（実例集）スタイル
- **How（tutorials: kitchen / pantry / collection-creation）** = 罫線なしの暖色グラデ・チュートリアルスタイル

この使い分けは意図的なもの。新デッキも所属（What/How）に合わせる。

## モック差し替えバックログ

方針決定（2026-07-19）: **collections-showcase のみ実キャプチャに差し替え。what-is / weather はモックのまま（What はイメージと割り切る）**。

| デッキ | 枚数 | 中身 | 状態 |
|---|---|---|---|
| demos/collections-showcase | 3 | レシピ帳 / 買い物リスト / 家計簿 | ja ✅ kitchen golden のクロップで差し替え済み。en ✅ en workspace の実キャプチャに差し替え済み（2026-07-26） |
| demos/what-is-mulmoclaude | 1 | 来週の予定 | モックのまま確定。スライド上の「※差し替え予定」注記は撤去済み（2026-07-22、ja/en・weather・collections-showcase(en) 含む全デッキ） |
| demos/weather-showcase | 6 | 天気×予定カード / やることリスト×2 / 持ち物リスト / メール下書き / 旅のしおり | モックのまま確定。同上 |

## 構成整理の TODO

Why/What/How の分類（vision = Why / demos = What / tutorials = How）に対する整理。

1. ✅ **collection-creation-demo を tutorials/ へ移動**（対応済み）— content-plan がコアセットの How と呼んでいるとおり中身は How のため。connected-collections / record-buttons は「新機能の告知」なので What として demos/ に残す
2. **台所三点セットの作り方デッキは最初から tutorials/ に、T1（Building a Collection フラッグシップ）として作る** — 「多段階でコレクションを作っていく過程」という content-plan の重要テーマに充当。既存の T1 下書き `tutorials/building-a-collection.json`（未 commit）はテーマが重なるため、置き換えるか別テーマで残すか要判断
3. ✅ **制作状態の単一ソースをこの PROGRESS.md に一本化**（対応済み）— ファイルを `mulmoclaude/PROGRESS.md` に移動し、企画 md 側は状態をここへの参照に切り替え、デッキ表に企画# 列を追加
4. **旧 D2 下書き `demos/daily-workflow.json`（未 commit・旧ネイビー配色）の扱い** — D2 は calendar-showcase へ改題・吸収したため役割終了。破棄するか別テーマで残すか要判断（`tutorials/building-a-collection.json` と同じ扱い）

## YouTube / X 公開の残作業（2026-07-25 時点）

ja 8 本の YouTube 公開・playlist 整備・Discord 告知・X 予約 7 本（7/24〜30 の 20:30）までは完了。残り:

1. ✅ **X 予約の追加 2 本**（対応済み）— what-is（7/29 20:30）と csv（7/30 20:30）を予約済み。文面は `youtube/<deck>_ja.md` の「X 投稿（日本語）」節どおり
2. **X 公開ごとの URL 記帳** — 状態の正本は各メタデータファイル `youtube/<deck>_ja.md` の「投稿枠」「投稿後」行。**このファイルに一覧を書き写さない**（更新漏れで陳腐化するため）。現況は `mulmo-x-status` スキルで導出する（`node ~/.claude/skills/mulmo-x-status/scripts/x-status.mjs`）。公開時刻を過ぎたのに未記帳のものと、文面が無いデッキだけを出す
3. ✅ **基礎編 `collection-creation-demo` の X 予約が抜けていた**（2026-07-27 発覚・同日対応）— 公開済み ja 8 本のうちこの 1 本だけ X 投稿の文面が未作成だった（メタデータに `## X 投稿` 節そのものが無かった）。文面を作成（Codex チェック済み）し、mp4 と .srt を添えて 7/31 20:30 枠に予約済み。「コレクションの作り方」playlist の入口動画なので、他の作り方動画から張った導線の先が X で紹介されていない状態になっていた
4. **weather-showcase** — Slack で確認依頼中（2026-07-25）。承認後: 公開一式の提示 → 公開 → 「できること」playlist を手動ソートへ切替 + マスター並び順の更新（`youtube/README.md` の並び順節が正本）→ メタデータ作成・本ファイルのタイトル表記帳 → X 予約（基礎編が 7/31 に入るため 8/1 枠）
5. 任意: mulmoclaude ワークスペースの `mulmo-beta-announcements` スキルへ「動画シェアの型」を追記する提案 / 生成済み .srt の YouTube 字幕アップ

## 英語版の公開準備（2026-07-26 時点）

**mp4 の鮮度**: en の mp4 は 6 本すべて 7/19 レンダのままで、その後のスクリプト変更（`ac99759` の「※差し替え予定」注記削除・アニメ retiming）が反映されていなかった。2026-07-26 に what-is / weather / connected-collections / record-buttons / collections-showcase を finalize し直して解消（collection-creation-demo は元から mp4 がスクリプトより新しく、対象外）。旧生成物は各 `output/<deck>/old/` へ退避。

**キャプチャ**: 7/19 のライブ再演分（connected-collections 6 枚・record-buttons 6 枚・collection-demo 11 枚）は撮り直し不要と判断。アプリは 7/19 以降 560 コミット進んでいるが、実差分はコレクション一覧の `Map` タブ追加とレコードボタンのアイコン字形のみで、内容が誤りになるものではない。ボタン定義（`data/skills/invoice/schema.json` の `actions`）も en workspace に残っている。

**公開前に残っているもの**:

1. ✅ **en のメタデータファイル**（対応済み・2026-07-27）— 5 本ぶんを `youtube/<deck>.md`（無印 = 英語版）に作成。チャプターはレンダリング済み音声から算出
2. ✅ **en の playlist**（対応済み・2026-07-27）— 4 本作成。ID と並び順・ソート方法は `youtube/README.md` の「英語版の playlist」節が正本
3. **講座の続きが en 未着手** — kitchen-trio / pantry / csv の en。「コレクションの作り方」は現状 collection-creation-demo の 1 本のみ
4. weather-showcase は ja が Slack 承認待ちのため、en を先行公開しない
5. ✅ **en 5 本の公開**（2026-07-27 完了）— what-is / collections-showcase / collection-creation-demo / connected-collections / record-buttons。URL は各メタデータとタイトル管理表に記帳済み。playlist への追加とマスターの手動並べ替え、collections-showcase の説明文への基礎編 URL 追記（公開時点では基礎編が未公開だったため後追い）まで完了。en 側の残作業なし
6. **vision の en 動画は据え置き**（2026-07-27 判断）— [An AI Assistant Is Something You Nurture, Not Something You Buy](https://youtu.be/Wonr3eOPww4) は playlist を作る前に公開したため、説明文に `▶ Watch in order` が無く、`youtube/` にメタデータファイルも無い（チャプターも無し）。マスターの先頭に置く動画なので、余力があるときにメタデータ作成と説明文の差し替えを行う

**翻訳レビュー（2026-07-26）**: en 6 本を Codex に通した（ja/en 対照＋レンダリング済みスライドの添付＋`demos/DEMO-GUIDE.md` の翻訳ルールを前提として渡す）。意味の破綻・数値の食い違い・レイアウト崩れの指摘はゼロ。英語として壊れていた 6 件とトーンが強すぎた 4 件を修正済み。積み残し 2 件: (a) `collection-creation-demo` beat 8 の en キャプチャがファイルパス（`data/skills/weather/schema.json` 等）を写しており ja のフィールド表より技術寄り — ja のキャプチャ据え置きを決めたため、単独で撮り直すほどではないと判断して保留 (b) `collections-showcase` 締めのバッジが ja「育」/ en 🌱（他デッキでは ja も 🌱 なので破綻はしていない）。

**ja に残っている既知のズレ（公開済みのため据え置き）**: `collections-showcase_ja` / `kitchen-trio-tutorial_ja` の献立は、買い物リストのメモが「月・火・水・木」で書かれているのに日付が 2026-07-21〜24（火〜金）になっており、ナレーションの「木曜は洋風」が画面の日付と 1 日ずれている。曜日名は画面に出ないため実害は小さいと判断し、公開済み動画は差し替えない。en は未公開だったので 7/27〜30（月〜木）に直した（`demo-workspace-en` の `a96749a`）。ja の台所データを撮り直す機会があればそのとき合わせる。

**en workspace の台所データ**: `demo-workspace-en` に recipes / shopping-list / ledger を英訳して投入済み（同リポジトリ commit `da090f1`）。家計簿の slug は en=`ledger`（デッキ本文が "the ledger collection" と呼ぶため）。お買い物モードのビューは、タップした品が一覧から消えて買い物の途中経過が見えなくなっていたため修正した（カテゴリ内の「購入済 / Bought」区切りの下に残す・件数を「済 / 全体」表示に戻す）。en `8212a9b` / ja `c0c2311` で両ワークスペースに適用済み。

## 次のアクション

1. ✅ 台所三点セットの作り方デッキ `tutorials/kitchen-trio-tutorial_ja`（ja ライブ収録・finalize 済み。実収録の学び: 買い物リストの自動チェックと予算ビュー生成が起きたためビート構成に反映。家計簿 slug は ja=kakeibo）
2. kitchen-trio の ja golden データを翻訳して en workspace（データの正）に反映・commit
3. en workspace で英語ライブ再演・収録 → `kitchen-trio-tutorial.json`（en）作成・finalize
4. ✅(ja) collections-showcase の 3 枚を golden からの実キャプチャに差し替え — en は en workspace 再演後
5. ～6. ✅ what-is / weather のモックは差し替えず確定（イメージと割り切り）。スライド上の注記は撤去済み（2026-07-22）
7. （別トラック）ja 3 デッキのキャプチャ撮り直し
8. ✅ 常備品リストで育てるデッキ `tutorials/pantry-list-tutorial_ja`（ja ライブ収録・finalize 済み）— kitchen-trio の「使いながら育てる」を引き継ぎ、「家にあれば不要」の推測をデータに基づく判断へ。設計は content-roadmap.md 参照
9. 新デッキ企画: 買い物リストの「お買い物モード」（モバイルビュー）を会話で作るデッキ — 素材は ja workspace のチャットセッション a0627168（ビュー作成の実録）。kitchen-trio のビート 8 が予告済み
10. ✅ 買い物リストに「買い物日」フィールド追加（ja workspace セッション 757db354・2026-07-19）— 購入済 16 品に 7/19、未購入 3 品は空欄=次回扱い。お買い物モードは次回分のみ表示に改修（タップで当日日付+購入済を自動記録）。pantry デッキ beat 8 を新ビューで撮り直し済み。kitchen のキャプチャはフィールド追加前の歴史的記録としてそのまま。セッションは「誤って常備品側に適用→指摘で自己修復」の実録で、デッキ素材候補
11. アイディア（csv-collection-tutorial の分析ビート改良）: 商品カタログ CSV に「発注先」列を足し、STEP3 の集計を「在庫切れは何件」→「在庫切れを発注先別に」へ — カテゴリ別より行動に直結（そのまま発注の連絡リストになる）してインパクトが出る。en 版収録か続編で反映候補。CSV は assets の source/gen_catalog_csv.py に列追加すれば seed 固定で再現可能
