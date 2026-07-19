# デモ・チュートリアル制作の進捗管理

`mulmoclaude/` 配下（demos = What / tutorials = How）の ja/en 展開の状態を追う表。
**制作状態（叩き台・スクリプト・キャプチャ・mp4）の単一ソースはこのファイル**。content-plan.md / what-materials.md は企画（何を・どの順で・どういう構成で）を持ち、状態はここを参照する。
作業のルールと撮り方は `demos/DEMO-GUIDE.md` を参照。
更新タイミング: デッキの追加・キャプチャ撮影・finalize・モック差し替えを行ったとき。

## デッキ別ステータス

✅ = 完了 / 🔁 = 要撮り直し / 📝 = 下書き / — = 対象なし
企画# は content-plan.md のコンテンツマトリクスの番号(番号外 = マトリクス外の追加分)。

| デッキ | 企画# | ja スクリプト | ja キャプチャ | en スクリプト | en キャプチャ | en mp4/PDF |
|---|---|---|---|---|---|---|
| tutorials/kitchen-trio-tutorial | T1（フラッグシップ） | ✅ 15 ビート | ✅ 10 枚（ja workspace ライブ + 実機スマホ 1 枚） | 未着手 | 未着手（en ライブ再演） | —（ja mp4/PDF は ✅） |
| tutorials/collection-creation-demo | コアセットの How | ✅（旧ネイビー配色） | 🔁 旧混合 workspace 産。ja workspace で撮り直し | ✅ | ✅ 11 枚 | ✅ |
| demos/connected-collections-demo | 番号外（新機能告知） | ✅ | 🔁 同上 | ✅ | ✅ 6 枚（ライブ再演） | ✅ |
| demos/record-buttons-demo | 番号外（新機能告知） | ✅ | 🔁 同上 | ✅ | ✅ 6 枚（ライブ再演） | ✅ |
| demos/weather-showcase | 番号外（showcase 追加分） | ✅ | —（流用アセット 2 点のみ） | ✅ | —（同左） | ✅ |
| demos/collections-showcase | D3 | ✅ | ✅ 3 枚（kitchen golden のクロップ） | ✅ | —（モックのまま。en 差し替えは en 再演後） | ✅ |
| demos/what-is-mulmoclaude | D1 | ✅ | —（モックのみ） | ✅ | —（同左） | ✅ |
| demos/daily-workflow | D2 | 📝 未 commit（旧ネイビー） | — | 未着手 | — | — |
| tutorials/getting-started | T2 | 📝 未 commit | — | 未着手 | — | — |
| tutorials/building-a-collection | （旧 T1 下書き） | 📝 未 commit。kitchen-trio が T1 を実装、下書きの扱いは要判断 | — | — | — | — |
| tutorials/pantry-list-tutorial | 番号外（育てる編・kitchen 続編） | ✅ 10 ビート | ✅ 7 枚（ja workspace ライブ） | 未着手 | 未着手 | —（ja mp4/PDF は ✅） |

ja の mp4/PDF は旧キャプチャ前提のため、ja キャプチャ撮り直し後に finalize し直す。

## タイトル・参照名の管理

動画内の相互参照（「〜という動画で」）と YouTube 等の公開タイトルのズレを防ぐための正はこの表。
**参照名は、そのデッキのタイトルページに実際に映っている文字から取る**（スクリプト title のメタデータではなく）。他デッキから言及するときは必ずこの表の参照名をそのまま使う。YouTube タイトルは公開時に決めて記入する。

| デッキ | スクリプト title（ja） | タイトルページの表記 | 参照名 | YouTube タイトル |
|---|---|---|---|---|
| tutorials/collection-creation-demo | コレクション作成デモ — 天気予報コレクション | eyebrow「コレクション作成デモ」+ 題「天気予報コレクション」 | コレクション作成デモ | 未定 |
| tutorials/kitchen-trio-tutorial | 台所の三点セットを、会話で作る | 同左 | 台所の三点セットを、会話で作る | 未定 |
| tutorials/pantry-list-tutorial | コレクションは、使いながら育てる — 常備品リスト編 | 題「使いながら、育てる」 | 常備品リスト編（使いながら、育てる） | 未定 |
| demos/collections-showcase | コレクション実例集 — 暮らしのアプリが、ひとつの会話でつながる | 「コレクション実例集」+ 見出し「暮らしのアプリが、ひとつの会話でつながる。」 | コレクション実例集 | 未定 |
| demos/what-is-mulmoclaude | MulmoClaude で何ができる？ | 見出し「できることは、暮らしの数だけ。」 | — | 未定 |
| demos/weather-showcase | 明日の天気は、もう予定に入っている | 同左 | — | 未定 |
| demos/connected-collections-demo | バラバラのデータが、つながる | — | — | 未定 |
| demos/record-buttons-demo | 押すだけの仕事は、ボタンにする | — | — | 未定 |

相互参照の現状（2026-07-19 検証）: kitchen beat 3・15 →「コレクション作成デモ」✅／kitchen beat 15 →「コレクション実例集」（旧「コレクションでつながる暮らし」から修正済み）／pantry beat 10 →「台所の三点セットを、会話で作る」✅＋お買い物モード（未制作の予告）。

### 見た目スタイルの使い分け（2026-07-19 確認）

- **What（demos: showcase / what-is / weather）** = 方眼罫線入りの誌面（実例集）スタイル
- **How（tutorials: kitchen / pantry / collection-creation）** = 罫線なしの暖色グラデ・チュートリアルスタイル

この使い分けは意図的なもの。新デッキも所属（What/How）に合わせる。

## モック差し替えバックログ

方針決定（2026-07-19）: **collections-showcase のみ実キャプチャに差し替え。what-is / weather はモックのまま（What はイメージと割り切る）**。

| デッキ | 枚数 | 中身 | 状態 |
|---|---|---|---|
| demos/collections-showcase | 3 | レシピ帳 / 買い物リスト / 家計簿 | ja ✅ kitchen golden のクロップで差し替え済み。en は en workspace 再演後に同様に差し替え |
| demos/what-is-mulmoclaude | 1 | 来週の予定 | モックのまま確定。スライド上の「※差し替え予定」注記の撤去は提案中 |
| demos/weather-showcase | 6 | 天気×予定カード / やることリスト×2 / 持ち物リスト / メール下書き / 旅のしおり | モックのまま確定。同上 |

## 構成整理の TODO

Why/What/How の分類（vision = Why / demos = What / tutorials = How）に対する整理。

1. ✅ **collection-creation-demo を tutorials/ へ移動**（対応済み）— content-plan がコアセットの How と呼んでいるとおり中身は How のため。connected-collections / record-buttons は「新機能の告知」なので What として demos/ に残す
2. **台所三点セットの作り方デッキは最初から tutorials/ に、T1（Building a Collection フラッグシップ）として作る** — 「多段階でコレクションを作っていく過程」という content-plan の重要テーマに充当。既存の T1 下書き `tutorials/building-a-collection.json`（未 commit）はテーマが重なるため、置き換えるか別テーマで残すか要判断
3. ✅ **制作状態の単一ソースをこの PROGRESS.md に一本化**（対応済み）— ファイルを `mulmoclaude/PROGRESS.md` に移動し、企画 md 側は状態をここへの参照に切り替え、デッキ表に企画# 列を追加

## 次のアクション

1. ✅ 台所三点セットの作り方デッキ `tutorials/kitchen-trio-tutorial_ja`（ja ライブ収録・finalize 済み。実収録の学び: 買い物リストの自動チェックと予算ビュー生成が起きたためビート構成に反映。家計簿 slug は ja=kakeibo）
2. kitchen-trio の ja golden データを翻訳して en workspace（データの正）に反映・commit
3. en workspace で英語ライブ再演・収録 → `kitchen-trio-tutorial.json`（en）作成・finalize
4. ✅(ja) collections-showcase の 3 枚を golden からの実キャプチャに差し替え — en は en workspace 再演後
5. ～6. what-is / weather のモックは差し替えず確定（イメージと割り切り）。スライド上の注記撤去のみ提案中
7. （別トラック）ja 3 デッキのキャプチャ撮り直し
8. ✅ 常備品リストで育てるデッキ `tutorials/pantry-list-tutorial_ja`（ja ライブ収録・finalize 済み）— kitchen-trio の「使いながら育てる」を引き継ぎ、「家にあれば不要」の推測をデータに基づく判断へ。設計は content-plan.md 参照
9. 新デッキ企画: 買い物リストの「お買い物モード」（モバイルビュー）を会話で作るデッキ — 素材は ja workspace のチャットセッション a0627168（ビュー作成の実録）。kitchen-trio のビート 8 が予告済み
10. ✅ 買い物リストに「買い物日」フィールド追加（ja workspace セッション 757db354・2026-07-19）— 購入済 16 品に 7/19、未購入 3 品は空欄=次回扱い。お買い物モードは次回分のみ表示に改修（タップで当日日付+購入済を自動記録）。pantry デッキ beat 8 を新ビューで撮り直し済み。kitchen のキャプチャはフィールド追加前の歴史的記録としてそのまま。セッションは「誤って常備品側に適用→指摘で自己修復」の実録で、デッキ素材候補
