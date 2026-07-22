# コンテンツロードマップ

制作状態の単一ソースは `PROGRESS.md`。本ファイルは「何を・どの順で作るか」のマスターリスト。

## コンテンツの階層と制作パイプライン（2026-07-22 決定）

コンテンツは 3 層構造。上の層が約束し、下の層が回収する。

1. **what-is（総論）** — 「何ができるか」の全体像。`demos/what-is-mulmoclaude` の 1 本のみ（総論を複数作らない。入口が割れるため）。コレクション（記録）中心だが、計画セッション・自動化・記憶の育ちまで触れている。
2. **showcase（各論・テーマ別深掘り）** — what-is の一面をテーマとして深掘る。台所 = `collections-showcase`（コレクションの深掘り）/ 天気 = `weather-showcase`（自動化・通知・先回りの深掘り。what-is beat 6 の水やり例を深掘る）。テーマはコレクションに限らない。良いテーマを思いついたら適宜追加してよい（ロードマップ外の追加を認める。前例: weather-showcase）。what-is が触れていない柱（調査・プレゼン動画化等）の showcase を作るときは、what-is へのビート追加も検討する。
3. **How（実演）** — showcase が見せた世界を、実キャプチャで実際に作ってみせる。

制作ルール:

- **what-is / showcase はモック HTML のまま公開まで行く**（What はイメージと割り切る）。実画面はキャプチャ必須の How の担当。モックに「※差し替え予定」等の注記は入れない。
- **How は対応する What（showcase）をベースに作る**。画像は実キャプチャ。
- **CTA は階層に沿って張る**: what-is → showcase → How と誘導し、How の末尾から showcase（実例）へ戻す。How が未制作の showcase は CTA がそのまま How のバックログになる（How 公開後に YouTube の説明文へリンクを追記する）。

## コンテンツマトリクス（What + How 12 本）

優先度: P0 = 7 月着手 / P1 = 8 月 / P2 = 9 月以降。

### Tutorials（How）

| # | テーマ | 尺 | capture | 優先度 |
|---|---|---|---|---|
| T1 | Building a Collection with AI（多段階でコレクションを育てる） | 5-6 分 | 必須 | **P0** |
| T2 | Getting Started（セットアップ〜最初の会話） | 4 分 | 必須 | P0 |
| T3 | Feeds & Automations（定期タスク・情報収集を任せる） | 4 分 | 必須 | P1 |
| T4 | Skills（自分の手順を教えて自動化） | 4 分 | 必須 | P1 |
| T5 | Custom Views 深掘り（コレクションにリッチ UI を付ける） | 5 分 | 必須 | P2 |
| T6 | Remote Access & Bridges（スマホ・LINE から使う） | 4 分 | 必須 | P2 |

### Demos（What）

| # | テーマ | 尺 | capture | 優先度 |
|---|---|---|---|---|
| D1 | What is MulmoClaude?（3 分ツアー） | 3 分 | 必須 | **P0** |
| D2 | A Day with MulmoClaude（1 日の使い方） | 3-4 分 | 必須 | P1 |
| D3 | Collections Showcase（実例コレクション集） | 3 分 | 必須 | P1 |
| D4 | チャットからプレゼン動画を作る（MulmoCast 連携） | 3 分 | 必須 | P2 |
| D5 | Remote Access デモ（外出先から自宅の workspace） | 2-3 分 | 必須 | P2 |
| D6 | 実ユーザーの応用例紹介（ショーケース） | 3-4 分 | 必須 | P1 |

### Vision（Why）

既存試作 3 本（Software for an Audience of One / GUI Chat Protocol / DSLs as Harnesses）の仕上げ。

## コアセットと見せる順

- ローンチ（X / YouTube / Product Hunt）は**コアセット 3〜4 本**で行う。
- コアセット: **What 1 本**（D1）/ **Why 1 本**（the-assistant-you-nurture）/ **How 1 本**（collection-creation-demo）/ 必要に応じて +T2（Getting Started）。
- 見せる順は **What → Why → How**（具体 → 思想 → 行動）。カテゴリ自体が未知のプロダクトなので初見には具体が先。
- 例外: 登壇・ウェビナーなど聞く姿勢のある場では Why 先行で良い。
- 順番よりも**各動画末尾の相互 CTA** を必ず張る（What 末尾 →「なぜこの形かは Why 編へ」、Why 末尾 →「始め方は How 編へ」、How 末尾 →「実例は What 編へ」）。
- 残りの D/T は公開後の**週次コンテンツ**として反応を見て着手する。
