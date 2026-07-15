# デモスクリプト制作ガイド

`mulmoclaude/demos/` 配下のデモ（What/How コンテンツ）を作るためのパターン集。特に同一内容で多言語する際に利用する。 `collection-creation-demo.json` をベースに作成した。新しいデモを書くときは、このガイドと実例の両方を参照する。

デモを増やすにあたって改善は適宜行う。

## ビート構成の型

| 順 | ビート | 役割 |
|---|---|---|
| 1 | 課題提示 + 結果先出し | 「〜していませんか？」という落ち着いた問いかけで共感を作り、完成形のスクショを最初に見せる（前半離脱の防止） |
| 2 | タイトル（slide layout） | テーマの宣言。params は既存スクリプトを流用 |
| 3 | 起動方法 | ターミナル演出 1 枚。コマンドはスライドに表示し、ナレーションでは読み上げない |
| 4〜 | STEP 解説 | 1 操作 = 1 ビート。STEP バッジは通し番号（同じ番号を 2 枚に振らない） |
| 途中 | 画面の見方 | 「左で会話すると、右に結果が出る」を最初のフォーム/結果が出る直前に 1 枚入れる |
| 途中 | AI の逆提案 | AI が次のステップを提案してくる画面をハイライトし、「はい、お願いします」で進む流れを見せる |
| 後半 | 後から拡張 | 完成後の追加リクエストで育っていく様子（レビューで強調を求められた必須要素） |
| n-1 | まとめ | Step 一覧を行形式で。番号はビートの STEP バッジと一致させる（文言は行に収まる短い言い換えで良い） |
| n | クロージング | 応用例カード + 🌱「作った後も、育てられる」+ CTA「ぜひ、試してみてください！」 |

## デザインルール

- **配色は warm sunrise テーマ**（明るい暖色。palette はリポジトリの CLAUDE.md、実例は `mulmoclaude/vision/the-assistant-you-nurture_ja.json`）。`collection-creation-demo.json` は旧ダークネイビーのままなので、構成は実例として参照しつつ配色は本ガイドのスニペットを正とする
- **キャプチャ領域（差し替え対象の画像・モック）は静止**を維持する。キャプチャビートでも対話テキスト側だけなら「長いビート対策」（下記）の A 方式でアニメ化してよい
- 上部バーは 2 段: 1 段目 = バッジ（`text-lg`）+ タイトル（`text-4xl`）、2 段目 = サブタイトル（`text-2xl`、色は textMuted `#7C5E3C`）
- 画像は `max-height: 560px`（2 段バーとの組で 720px に収まる）
- 本文文字サイズの下限目安: 本文 `text-xl`、補足 `text-lg`。まとめ・クロージングは タイトル `text-5xl` / 行 `text-3xl`+`text-2xl` まで上げる
- 全ビートの右下にページ番号 `N / 総数`（タイトルスライドは theme レイアウトのため番号なしで可）
- テーマの `fonts` は `'Hiragino Sans', 'Helvetica Neue', Helvetica, sans-serif` を指定する（Georgia のままだと日本語タイトルが明朝にフォールバックする）
- 引用プロンプトは上部バーに押し込まず、画像上の吹き出しに置く

## 長いビート対策（ナレーション同期とスピルオーバー）

1 ビートのナレーションが長い（20 秒前後）のに絵が 1 枚だと、「一枚の絵に複数のメッセージ」「変化のない絵をじっと見る時間」が生まれる（2026-07 のレビュー指摘）。対策は 2 通り。

### A. 1 音声のまま、ナレーションに同期して要素を出す（html_tailwind + data-animation）

- 同じレイアウト内で要素を段階表示できるならこちらが第一候補。TTS を分割しないので音声キャッシュと韻律の連続性が保たれる
- 仕組みは `collection-creation-demo.json` と同じ: `image.animation: true` + 要素に `data-animation='animate'` `data-opacity='0,1'` `data-start`/`data-end`（秒）`data-easing='easeOut'`
- animated ビートはナレーション尺の mp4 としてレンダリングされるため、`data-start` の秒がそのまま「そのビートの音声開始からの秒」になる
- 実測〜`data-start` 書き込みは Claude Code の `/mulmo-finalize` skill で自動化できる（要素に `data-sync='<文番号>:<文内位置>'` を書いておくと retime スクリプトが `data-start`/`data-end` を計算・書き込みする）。以下は skill を使わない場合の手動手順
- タイミングは推測ではなく実測する:
  1. 一度 movie を回すとビート別 mp3 が `output/<name>/audio/` にキャッシュされる
  2. `ffmpeg -i <beat の mp3> -af silencedetect=noise=-35dB:d=0.25 -f null -` で無音区間（文間のポーズ）を検出
  3. 文字数比例で推定した文境界を、最寄りの無音区間の中点に吸着（±1 秒以内）させると各文頭の実時間が得られる
  4. 各要素の `data-start` を「その内容を読み上げる文頭」に合わせる（表示は 0.4〜0.6 秒で完了させる）
- 注意点:
  - 最初のビートだけ `audioParams.introPadding`（既定 1 秒）ぶん映像が音声に先行するので、要素タイミングに +introPadding する。完成 mp4 冒頭の無音を silencedetect で実測すれば確認できる
  - 「。」で文分割する際、ナレーション引用内の「。」（『〜考えて。』等）でも分割される点に注意
  - キャプチャビートでは対話テキストだけをアニメ化し、キャプチャ領域は静止のまま維持する（差し替え作業を単純に保つ）
- 実例: `collections-showcase.json`（タイトルで「レシピ、買い物リスト、家計簿」の単語ごとにカードが 1 枚ずつ出る）

### B. スピルオーバー（1 音声に複数スライド）

- メッセージごとに絵を丸ごと切り替えたいとき（画像生成ビートなど段階表示できない場合）はこちら
- テキストを持つビートに `duration`（そのスライドを見せる秒数）を指定し、続くビートを `"text": ""` にすると、音声が流れたまま次のスライドへ切り替わる
- グループ最後のビートは `duration` を省略すると音声の残り時間ぶん表示される
- 実例: `mulmoclaude/vision/the-assistant-you-nurture_ja.json` の beat 1〜3・4〜6（1 音声 × 3 スライド）

### 使い分け

- 同一レイアウトへの積み上げ（説明・図解） → A
- 絵そのものを差し替えたい（画像生成・場面転換） → B
- 併用も可: 長い音声を B で 2〜3 面に割り、各面の中を A で同期させる

## 共通パーツ（コピペ用スニペット）

ルート div には `relative` を付け（ページ番号の絶対配置に必要）、背景に warm グラデーションを敷く: `style='background: linear-gradient(160deg, #FFFBF2, #FFF3DC 55%, #FCE8C8)'`。

テーマ色の Tailwind 対応: primary `#EA580C` = `orange-600` / accent `#F59E0B` = `amber-500` / info `#0284C7` = `sky-600` / danger `#DC2626` = `red-600`。本文 `#431407`・textMuted `#7C5E3C`・textDim `#A08B6E` は Tailwind に無いので inline style で指定する。

```html
<!-- 2 段上部バー -->
<div class='px-8 pt-5 pb-3 space-y-1'>
  <div class='flex items-center gap-4'>
    <span class='bg-orange-600 text-white text-lg font-bold px-5 py-1.5 rounded-full'>STEP 1</span>
    <h2 class='text-4xl font-bold' style='color: #431407'>タイトル</h2>
  </div>
  <p class='text-2xl' style='color: #7C5E3C'>サブタイトル</p>
</div>

<!-- 赤枠ハイライト（画像を relative ラッパーで包み、画像に対する % で指定） -->
<div class='relative'>
  <img src='...' class='rounded-xl shadow-2xl' style='max-height: 560px; object-fit: contain' />
  <div class='absolute border-2 border-red-600 rounded-lg' style='top: 9%; left: 74.4%; width: 11.4%; height: 7%'></div>
</div>

<!-- プロンプト吹き出し（入力した言葉を画像に重ねる。静止） -->
<div class='absolute rounded-2xl px-6 py-3 shadow-xl whitespace-nowrap' style='top: 58%; left: 50%; transform: translateX(-50%); background: #FFF3DC; border: 1px solid rgba(234, 88, 12, .45)'>
  <span class='text-2xl' style='color: #431407'>💬 「はい、お願いします！」</span>
</div>

<!-- 拡大コールアウト（拡大部分を上、全体像を下、対応を矢印で示す） -->
<div class='relative mb-12'>
  <img src='(拡大クロップ)' class='rounded-xl shadow-2xl' style='width: 1000px' />
  <div class='absolute border-4 border-red-600 rounded-lg' style='top: 4%; left: 57.5%; width: 5.6%; height: 88%'></div>
  <div class='absolute text-red-600 text-2xl font-bold whitespace-nowrap' style='top: 118%; left: 50%'>↑ このボタンをクリック</div>
</div>
<div class='relative mt-10'>
  <img src='(全体スクショ)' class='rounded-xl shadow-2xl' style='max-height: 320px; object-fit: contain' />
  <div class='absolute border-2 border-sky-600 rounded-lg' style='top: 0%; left: 0%; width: 60.5%; height: 7.4%'></div>
  <div class='absolute text-sky-600 text-xl font-semibold whitespace-nowrap' style='top: -13%; left: 18%'>⬆ この部分を拡大しています</div>
</div>

<!-- ①② の領域説明（画面の見方ビート用） -->
<div class='absolute border-4 border-sky-600 rounded-lg' style='top: 14.5%; left: 0.4%; width: 24.6%; height: 84%'></div>
<div class='absolute bg-sky-600 text-white text-xl font-bold px-4 py-1 rounded-full whitespace-nowrap shadow-lg' style='top: 10.5%; left: 1.5%'>① 左で会話</div>

<!-- ページ番号 -->
<div class='absolute bottom-3 right-6 text-lg' style='color: rgba(160, 139, 110, .6)'>4 / 16</div>
```

画像は `collection-demo-assets/xxx.png` のような **JSON からの相対パス**で参照する（mulmocast が file:// に解決する）。

## キャプチャ規約

### ブラウザ操作（Playwright MCP）

- Playwright MCP は内蔵 Chromium を使う（システムの Chrome を指定しない）。`.mcp.json` はシンプルに:

  ```json
  {
    "mcpServers": {
      "playwright": {
        "type": "stdio",
        "command": "npx",
        "args": ["@playwright/mcp@latest"]
      }
    }
  }
  ```

- 最初に `browser_resize` で **1280×720** に設定し、全キャプチャを通じて維持する（スライド間で縮尺がズレるのを防ぐ）
- ページ遷移・モーダル表示の後は、アニメーション完了とローディングスピナー・トーストの消滅を待ってから `browser_take_screenshot` する
- スナップショットで拾えない UI は `browser_evaluate` でクリックやスクロールを行う（例: サイドバーを少しスクロールして内部プロンプトの写り込みを画面外に出す）

### 撮り方のルール

- **ブラウザウィンドウは 1280×720**（キャンバスと同サイズ）で撮る。全画面スクショがスライドにほぼ原寸で載り、左右の余白も出ない
- モーダル・フォーム・詳細パネルは全画面のまま使わず、**該当パネルだけにクロップ**して文字が読めるサイズにする。ただし「選択モーダル」のような文脈が要る画面は、背景（薄暗いオーバーレイ越しの元画面）ごと見せる
- クロップは ffmpeg を使う: `ffmpeg -i in.png -vf "crop=W:H:X:Y" out.png`（macOS の `sips --cropOffset` は中央基準になり意図通りに切れない）
- 赤枠・吹き出しの座標は、クロップ後の画像を開いて実測し、画像サイズに対する % に換算する
- **写り込み NG 集**: ホバーツールチップ / 内部プロンプト（システム指示文がサイドバーに見える状態）/ 雑多なタブ名 / ローディングスピナー・トースト / API キー・個人情報
- ファイル名は `demo-{連番2桁}-{英語kebab-case}.png`。連番はストーリー上の登場順
- スクリプトが参照しなくなった画像はコミットに含めない（追跡済みなら `git rm`。履歴から復元できる）

## ナレーション規則

- 非エンジニア向け。技術用語（スキーマ、API、レコード、フィールド、モーダル等）を使わない。「モーダル」→「画面」
- コマンド文字列・URL・地名の列挙は読み上げず、スライド表示に任せる
- **実例・機能をナレーションで数え上げない**（3 個以上の列挙は赤信号）。幅広さは「カードの物量」「振れ幅の大きい例（複式簿記の会計・W杯観戦管理のような意外な例）」「開いた締め（『…と、あなたの趣味』等）」で見せ、語りは 1 ビートにつき 1〜2 例に絞る。スライドに表示して読み上げない使い分けは OK（2026-07 の What デッキレビュー指摘: 列挙型は「たくさんあった気がするが何も思い出せない」になる）
- 読み上げ総量の目安はデッキ（10 ビート・約 3 分）あたり 1,050 字前後、1 ビート 100〜120 字
- 内部動作の説明（仕様目線）ではなくユーザー便益で語る。例: 「済むと次回分が自動で生まれる」→「毎月の用事も、忘れない」
- 固有名詞の TTS 安定化: 「MulmoClaude」はナレーションでは「マルモクロード」と表記する
- TTS が読み間違える語はナレーション側だけ言い換える(スライド表記は変えない)。例: 「表」は「おもて」と読まれるため「一覧表」(いちらんひょう)にする
- 音声トーンも vision デッキと統一する: `speechParams` の speaker に、`the-assistant-you-nurture_ja.json` の Gemini Kore warm instruction（`speechOptions.instruction`、明るく温かいトーン指定）をそのまま流用する。instruction を変更すると全ビートの音声が再生成される点に注意
- vision デッキ「AIアシスタント育成ツール」の語彙に合わせる: 変更・更新ではなく**「育てる」**。「作って終わりではなく、会話しながら育てていける」
- 「インストール不要」とは言わない（vision の「ぜひインストールし」と食い違う）。「面倒な設定は不要」等に言い換える
- 見出しの口語は落ち着いたトーンに（「〜じゃない？」→「〜していませんか？」）

## 検証と出力

```sh
npm test                                     # 全スクリプトの schema validate
npm run preview -- mulmoclaude/demos/<name>.json   # ライブプレビュー（保存で自動リロード）
npm run movie -- mulmoclaude/demos/<name>.json     # mp4（未変更ビートはキャッシュ再利用）
mulmo pdf -g mulmoclaude/demos/<name>.json                     # スライド PDF
mulmo pdf -g --pdf_mode handout mulmoclaude/demos/<name>.json  # ハンドアウト PDF（スライド + ナレーション）
```

レビューには mp4 と PDF 2 種（slide / handout）を添付する。

## キャプチャ台本（collection-creation-demo の再現手順）

別言語版や撮り直しのための台本。前提: MulmoClaude がローカル起動済み（`npx mulmoclaude@latest`）、ブラウザ操作ツール（Playwright MCP 等）でウィンドウを **1280×720** にリサイズ済み。

### シナリオ

天気予報コレクションをゼロから作る。会話で入力するプロンプト（英語版の例を括弧内に）:

1. ガイド付きセットアップのフォームに記入 — コレクション名「天気予報」(Weather Forecast)、内容「場所ごと・時間帯ごとの天気を管理したい。出張で移動するので、土浦・東京・盛岡など複数の場所の天気を一覧で確認したい。」(I travel for work, so I want to see the weather for multiple locations — Tsuchiura, Tokyo, Morioka — at a glance, by time of day.)
2. AI が項目を自動生成し、初期レコード作成を逆提案してくる → 「はい、お願いします！」(Yes, please!)
3. 「3時間ごとの天気も出せる？」(Can you add 3-hourly forecasts?)
4. 「出張の移動に合わせて、時間ごとの天気を並べて見たい」(Show the weather as a timeline that follows my travel schedule.)

### アセット別の撮り方（現行 11 枚）

| アセット | 画面状態 | 全画面 / クロップ |
|---|---|---|
| collections-1280 | コレクション一覧（ツールバーのコレクションボタンで開く） | 全画面 |
| toolbar-zoom | 同上 | 上端のツールバー帯だけをクロップ（拡大コールアウト用） |
| guided-modal-bg | 一覧で「＋ コレクション」をクリックした直後のモーダル | 全画面（背景のオーバーレイごと見せる） |
| chat-form-1280 | チャットでガイド付きセットアップを選び、空のフォームが右に出た状態。サイドバー最上部に内部プロンプトが写らない位置までスクロール | 全画面（画面の見方ビート用） |
| form-panel | フォームに記入済みの状態 | フォームパネルだけをクロップ |
| created-fields | 作成完了メッセージの後半（フィールド構成の表 + 末尾の逆提案文が入る範囲） | パネル後半をクロップ |
| weather-table-1280 | 3 地点のレコードが入ったテーブルビュー | 全画面（吹き出しを下の余白に重ねる） |
| detail-modal | 1 地点をクリックした詳細モーダル（週間予報の表まで） | モーダルだけをクロップ |
| hourly-modal | 3時間ごと予報の追加後、同じ詳細モーダル | モーダルだけをクロップ |
| timeline-1280 | カスタムビュー切替で「出張タイムライン」を表示 | 全画面（吹き出しを横の余白に重ねる） |
| timeline-hero | 同上 | タイムラインパネルだけをクロップ（導入ビートのヒーロー用） |

- 撮影順は表の上から進めると操作の手戻りがない
- クロップの px 座標は言語・データで変わるため、この表の「対象」を目安に毎回実測する
- 撮り終えたら「写り込み NG 集」（上記キャプチャ規約）を全アセットに対して最終チェックする

## 多言語展開の要点

- キャプチャは言語ごとに撮り直す（UI 言語を切り替え、上記キャプチャ台本と同じ流れで同じ構図を再現）。アセットは `collection-demo-assets-en/` のように言語別ディレクトリに分ける
- スクリプトはコピーして `lang`・`voiceId`・ナレーション・スライド内テキストを差し替え、赤枠・吹き出し座標を対象言語 UI に合わせて微調整する
- 英語 TTS なら「マルモクロード」表記は不要（MulmoClaude のままで読める）
