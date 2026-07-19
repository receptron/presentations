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
| demos/collections-showcase | D3 | ✅ | —（モックのみ） | ✅ | —（同左） | ✅ |
| demos/what-is-mulmoclaude | D1 | ✅ | —（モックのみ） | ✅ | —（同左） | ✅ |
| demos/daily-workflow | D2 | 📝 未 commit（旧ネイビー） | — | 未着手 | — | — |
| tutorials/getting-started | T2 | 📝 未 commit | — | 未着手 | — | — |
| tutorials/building-a-collection | （旧 T1 下書き） | 📝 未 commit。kitchen-trio が T1 を実装、下書きの扱いは要判断 | — | — | — | — |
| tutorials/pantry-list-tutorial | 番号外（育てる編・kitchen 続編） | 📝 設計済み（content-plan 参照）・ja ライブ収録中 | 収録中 | 未着手 | 未着手 | — |

ja の mp4/PDF は旧キャプチャ前提のため、ja キャプチャ撮り直し後に finalize し直す。

## モック差し替えバックログ

「※ 実際の画面キャプチャに差し替え予定」注記の残数（1 言語あたり）。

| デッキ | 枚数 | 中身 | 方針 |
|---|---|---|---|
| demos/collections-showcase | 3 | レシピ帳 / 買い物リスト / 家計簿 | 台所三点セットの作り方デッキ（tutorials/ の T1）を先に収録 → golden から差し替え |
| demos/what-is-mulmoclaude | 1 | 来週の予定 | todo に一時データ → 撮影 → git restore（固定資産を汚さない） |
| demos/weather-showcase | 6 | 天気×予定カード / やることリスト×2 / 持ち物リスト / メール下書き / 旅のしおり | 通知・演出系が多い。台所セット完了後に 1 枚ずつ実キャプチャ化可否を判断 |

## 構成整理の TODO

Why/What/How の分類（vision = Why / demos = What / tutorials = How）に対する整理。

1. ✅ **collection-creation-demo を tutorials/ へ移動**（対応済み）— content-plan がコアセットの How と呼んでいるとおり中身は How のため。connected-collections / record-buttons は「新機能の告知」なので What として demos/ に残す
2. **台所三点セットの作り方デッキは最初から tutorials/ に、T1（Building a Collection フラッグシップ）として作る** — 「多段階でコレクションを作っていく過程」という content-plan の重要テーマに充当。既存の T1 下書き `tutorials/building-a-collection.json`（未 commit）はテーマが重なるため、置き換えるか別テーマで残すか要判断
3. ✅ **制作状態の単一ソースをこの PROGRESS.md に一本化**（対応済み）— ファイルを `mulmoclaude/PROGRESS.md` に移動し、企画 md 側は状態をここへの参照に切り替え、デッキ表に企画# 列を追加

## 次のアクション

1. ✅ 台所三点セットの作り方デッキ `tutorials/kitchen-trio-tutorial_ja`（ja ライブ収録・finalize 済み。実収録の学び: 買い物リストの自動チェックと予算ビュー生成が起きたためビート構成に反映。家計簿 slug は ja=kakeibo）
2. kitchen-trio の ja golden データを翻訳して en workspace（データの正）に反映・commit
3. en workspace で英語ライブ再演・収録 → `kitchen-trio-tutorial.json`（en）作成・finalize
4. collections-showcase の 3 枚を golden からの実キャプチャに差し替え（ja/en）
5. what-is の 1 枚を一時データ方式で差し替え
6. weather の 6 枚の扱いを個別判断
7. （別トラック）ja 3 デッキのキャプチャ撮り直し
8. **次の動画（着手中）**: 常備品リストで育てるデッキ `tutorials/pantry-list-tutorial_ja` — kitchen-trio の「使いながら育てる」を引き継ぎ、「家にあれば不要」の推測をデータに基づく判断へ。設計は content-plan.md 参照
9. 新デッキ企画: 買い物リストの「お買い物モード」（モバイルビュー）を会話で作るデッキ — 素材は ja workspace のチャットセッション a0627168（ビュー作成の実録）。kitchen-trio のビート 8 が予告済み
