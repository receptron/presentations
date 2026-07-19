# デモ制作の進捗管理

demos/ 配下の ja/en 展開の状態を追う表。
作業のルールと撮り方は `DEMO-GUIDE.md` を参照。
更新タイミング: デッキの追加・キャプチャ撮影・finalize・モック差し替えを行ったとき。

## デッキ別ステータス

✅ = 完了 / 🔁 = 要撮り直し / 📝 = 下書き / — = 対象なし

| デッキ | ja スクリプト | ja キャプチャ | en スクリプト | en キャプチャ | en mp4/PDF |
|---|---|---|---|---|---|
| collection-creation-demo | ✅（旧ネイビー配色） | 🔁 旧混合 workspace 産。ja workspace で撮り直し | ✅ | ✅ 11 枚 | ✅ |
| connected-collections-demo | ✅ | 🔁 同上 | ✅ | ✅ 6 枚（ライブ再演） | ✅ |
| record-buttons-demo | ✅ | 🔁 同上 | ✅ | ✅ 6 枚（ライブ再演） | ✅ |
| weather-showcase | ✅ | —（流用アセット 2 点のみ） | ✅ | —（同左） | ✅ |
| collections-showcase | ✅ | —（モックのみ） | ✅ | —（同左） | ✅ |
| what-is-mulmoclaude | ✅ | —（モックのみ） | ✅ | —（同左） | ✅ |
| daily-workflow | 📝 未 commit（旧ネイビー） | — | 未着手 | — | — |
| tutorials/getting-started | 📝 未 commit | — | 未着手 | — | — |
| tutorials/building-a-collection | 📝 未 commit | — | 未着手 | — | — |

ja の mp4/PDF は旧キャプチャ前提のため、ja キャプチャ撮り直し後に finalize し直す。

## モック差し替えバックログ

「※ 実際の画面キャプチャに差し替え予定」注記の残数（1 言語あたり）。

| デッキ | 枚数 | 中身 | 方針 |
|---|---|---|---|
| collections-showcase | 3 | レシピ帳 / 買い物リスト / 家計簿 | 台所三点セットの作り方デッキを先に収録 → golden から差し替え |
| what-is-mulmoclaude | 1 | 来週の予定 | todo に一時データ → 撮影 → git restore（固定資産を汚さない） |
| weather-showcase | 6 | 天気×予定カード / やることリスト×2 / 持ち物リスト / メール下書き / 旅のしおり | 通知・演出系が多い。台所セット完了後に 1 枚ずつ実キャプチャ化可否を判断 |

## 構成整理の TODO（PR #56 マージ後、別の小 PR で）

Why/What/How の分類（vision = Why / demos = What / tutorials = How）に対する整理。

1. **collection-creation-demo を tutorials/ へ移動** — content-plan がコアセットの How と呼んでいるとおり中身は How なのに demos/ に居る。ja/en 両スクリプト + アセットディレクトリを `git mv` し、参照（DEMO-GUIDE / CLAUDE.md / 企画 md / output キャッシュ）を追随させる。connected-collections / record-buttons は「新機能の告知」なので What として demos/ に残す
2. **台所三点セットの作り方デッキは最初から tutorials/ に、T1（Building a Collection フラッグシップ）として作る** — 「多段階でコレクションを作っていく過程」という content-plan の重要テーマに充当。既存の T1 下書き `tutorials/building-a-collection.json`（未 commit）はテーマが重なるため、置き換えるか別テーマで残すか要判断
3. **制作状態の単一ソースをこの PROGRESS.md に一本化** — content-plan / what-materials に散っている状態記述（「叩き台あり」等）を PROGRESS 参照に置き換え、PROGRESS のデッキ表に D/T 番号列を追加して相互参照できるようにする

## 次のアクション

1. 台所三点セットの作り方デッキ（新規、`_ja` 先行で設計。置き場所は上記 TODO 2 のとおり tutorials/）
2. en workspace で英語ライブ作成・収録 → en golden commit → 翻訳データを ja に反映
3. ja workspace で日本語ライブ再演・収録
4. 両言語 finalize → collections-showcase の 3 枚を差し替え
5. what-is の 1 枚を一時データ方式で差し替え
6. weather の 6 枚の扱いを個別判断
7. （別トラック）ja 3 デッキのキャプチャ撮り直し
