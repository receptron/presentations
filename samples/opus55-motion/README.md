# Opus 5.5 の映像表現 — X 調査と、mulmocast で作った見本（2026-09-27）

X で「Claude Opus 5.5 で作った」とされる映像表現を集め、mulmocast の `html_tailwind` のアニメーションで作り直した見本集。本番のデッキではなく、演出を探すときに参照するためのもの。

## 目次（どの演出がどこにあるか）

| フォルダ | 台本 | 中身 | 生成 AI |
|---|---|---|---|
| `sampler/` | `opus55-motion-sampler.json`（16:9、8 演出）、`opus55-motion-sampler-vertical.json`（9:16、2 演出） | L1（手堅い）: タイポ、UI 部品の持ち上げ、潜るズーム、線画、蓄積する暦、左右比較、筆致、Three.js の空間、巻物テロップ、数字の増加 | なし |
| `showcase/` | `opus55-motion-showcase.json`（16:9、8 演出）、`opus55-motion-shorts.json`（9:16、10 秒） | L2（映像的）・L3（作品的）・Shorts のハイテンポ | なし |
| `ideas-mv/` | `ideas-mv.json` | 曲のキックごとに筆が入り、風景画が描き上がる MV | ElevenLabs（BGM） |
| `ideas-explain/` | `ideas-explain.json` | 微分の解説（KaTeX）、深海への降下、美術史の早回し | なし（ナレーションの案は `NOTES.md`） |
| `ideas-news/` | `ideas-news.json` | 公開データから自動で組むニュース番組（GitHub の新しいリポジトリ、28 都市の気温の地球儀） | Gemini 3.1 Flash TTS、ElevenLabs |
| `ideas-story/` | `ideas-story.json`、画像の生成用に `assets.json` | 音声に合わせて口が動く掛け合い、墨絵の合戦の地図、対戦ゲーム風の HUD、切り絵のコラージュ | Gemini 3.1 Flash TTS、Nano Banana Pro |
| `ideas-3d/` | `ideas-3d.json` | GLB のロボットが走るゲーム映像、2 コマ打ちの粘土、設計図と描画で見せる城 | なし |
| `ideas-composite/` | `ideas-composite.json` | 撮影映像の上の注釈とルーペ、参照と再現の比較、アイコンの振り付け、Lottie、8bit | なし |
| `research/` | `x-posts.json` | X から集めた 79 件（URL・投稿者・日付・反応数・動画の縦横と尺・技法タグ・要約）。投稿の本文は含めていない | — |

どの台本も、隣の `build.py` が書き出したもの。台本を直すときは `build.py` を直して、そのフォルダで `python3 build.py` を実行する。台本の JSON は直接編集しない。

## 作り直し方

- 書き出しは repo のルートから `npm run movie -- -o "$MAIN/output" samples/opus55-motion/<フォルダ>/<台本>.json`（`$MAIN` は CLAUDE.md の worktree の節のとおり）。ナレーションの無い台本は TTS の費用がかからない
- 素材は台本からの相対パスで参照している。`html_tailwind` の `src` 属性に書いた相対パスは、mulmocast が台本のフォルダを基準に解決する（`image:` / `movie:` の参照の後に解決される）。BGM の `audioParams.bgm.path` も相対パス
- `ideas-mv`: 曲を作り直したら `python3 analyze.py assets/mv.mp3 mv-beats.json` でキックの時刻を測り直してから `build.py`。曲の指示は `plan-mv.json`（ElevenLabs Music の `composition_plan`。1 区間は 3 秒以上）
- `ideas-news`: `python3 data/fetch.py` でデータを取り直し、`data/gh.json` を見て、番組に使う 3 本を `build.py` の `PICK` で選び直す。センシティブな題材（災害、政治、企業の内紛、プライバシーに関わるもの）は選ばない
- `ideas-story`: 台詞を変えたら 2 段階で書き出す。`mulmo audio -g -o <出力先> ideas-story.json` → `python3 mouth.py <出力先>/ideas-story/ideas-story_studio.json mouth.json` → `python3 build.py` → `mulmo movie`。画像は `mulmo images -g -o <出力先> assets.json` で作り、できた png を `assets/` に置く
- `ideas-composite`: 撮影映像は repo の `mulmoterminal/clips/first-run-assets/07-grid.mp4` を相対パスで参照している

## 1. 何を調べたか

- 期間は 2026-08-01〜2026-09-27 の X の投稿。Opus 5.5 は 9/22 に公開され、集まった 79 件はすべて 9 月の投稿だった
- 収集は Cursor Agent の Grok 4.7 に任せた。X 公式の MCP（`api.x.com/mcp`）の `search_posts_all` を使い、9 本のクエリを日本語と英語で投げた
- 返ってきた投稿は 484 件で、関連する 79 件を残した。内訳は英語 40・日本語 30・中国語 7・その他 2。費用は X API のクレジット $1.79（$17.75 → $15.96）
- 実在の確認として、79 件すべてを X の oEmbed に投げ、投稿者と本文の冒頭を照合した。78 件が一致した。残る 1 件は自分の返信投稿で、先頭の `@宛先` が埋め込み表示で省かれるために文字列が合わなかっただけ
- 生データは `research/x-posts.json`（投稿ごとの URL・反応数・動画の縦横と尺・技法タグ、何を見せているか・何が上がったと言っているかの要約）。この repo は公開なので、他人の投稿の本文は除いた

## 2. X で言われている「Opus 5.5 の何が上がったか」

- **動画生成ではなく、全フレームを描くプログラムを書く**。Chrome で 1 コマずつ撮り、ffmpeg でつなぐ。文字が鋭い、同じ物体が破綻せずに繰り返せる、カットが溶けない。これらは描き方の副作用として説明されている（[Vladic_ETH](https://x.com/Vladic_ETH/status/2104198303919305127)、[xiaohu](https://x.com/xiaohu/status/2102979455308439555)、[arlooooooo](https://x.com/arlooooooo/status/2103282282790633715)）
- **構成力**。同じ資料から作った研修動画を比べると、GPT-6 Astra は支離滅裂で、Opus 5.5 は話の組み立てとモーションが内容を補っている（[excel_niisan](https://x.com/excel_niisan/status/2102719776984559798)）。同じ「15 秒ショーリール」の指示でも、構成と見せ方が変わる（[ai_300](https://x.com/ai_300/status/2104028254348964135)、[ConnorPRose](https://x.com/ConnorPRose/status/2103494412047147443)）
- **ナレーションと画面のタイミングが、雑な指示でも合う**（[se_yakiimosan](https://x.com/se_yakiimosan/status/2103424382249099343)）
- **自分のフレームを見て直す**。書き出したコマを見てバグを 3 つ見つけ、直して書き出し直した（[AzamIntikhab](https://x.com/AzamIntikhab/status/2102508449955524707)）
- **分業**。絵コンテを書き、曲を 9 章に分け、章ごとにサブエージェントへ渡す（[xiaohu](https://x.com/xiaohu/status/2102979455308439555)、[Qestir](https://x.com/Qestir/status/2103555083573383296)）
- 注意書きとして、「ワンプロンプト」は宣伝文句で、実際の指示は約 9,500 字だったという指摘がある（[Vladic_ETH](https://x.com/Vladic_ETH/status/2104198303919305127)）

## 3. 社内デッキとの差分（まだ表現できていない側）

基準にしたのは次の 2 つの PR。

- receptron/presentations の PR #126: 腕のリグ付き SVG の人物、手で描いていくホワイトボード、無音区間に合わせたタイミング、ElevenLabs の BGM
- ystknsh/media の PR #3: `render(frame)` で描く心電図の曲線、画面も音も止める落差

X で目立っていて、社内のデッキにまだ無いのは次の 5 つ。

| 領域 | X の代表例 | 社内デッキ |
|---|---|---|
| 3D（Three.js / WebGL / Blender） | 反応数の上位 5 件のうち 3 件（[xikhar](https://x.com/xikhar/status/2104001664793600012) ♥4749、[onofumi_AI](https://x.com/onofumi_AI/status/2102568200122884553)）、[mdaman010](https://x.com/mdaman010/status/2103788160031592572) | 無し → **見本 p8 で 2.7.2 でも書き出せることを確認** |
| カメラの言語（潜るズーム、パララックス） | [mdaman010](https://x.com/mdaman010/status/2103788160031592572)（データセンター → 原子）、[higgsfield_ai](https://x.com/higgsfield_ai/status/2103964599737536831) | 無し（`coverZoom` / `coverPan` は画像にだけ効く）→ 見本 p3 |
| 実 UI を部品に分けて動かす | [pranavclickks](https://x.com/pranavclickks/status/2103598924632396258)（フロントのコードから画面収録風の映像を組む） | スクショの差し替えが中心 → 見本 p2 |
| データの蓄積・経年 | [guriham_lab](https://x.com/guriham_lab/status/2104154927362945532)（2 年・30,113 枚の縦動画）、[brsabel](https://x.com/brsabel/status/2103132094243521015) | 無し → 見本 p5・v2 |
| 質感（手描きの紙・筆致、網点） | [ring_hyacinth](https://x.com/ring_hyacinth/status/2102986085328716066) ♥674、[akiy_8](https://x.com/akiy_8/status/2103434383218872503)（WebGL2 のレイトレースと網点） | ホワイトボードの線まで → 見本 p7 |

## 4. 演出カタログ（用途 × 縦横）

「見本」列は `opus55-motion-sampler.json`（16:9）と `opus55-motion-sampler-vertical.json`（9:16）の beat id。実装の列は次のとおり。

- MA: MulmoAnimation だけで書ける
- 直書き: `render(frame)` に直接書く
- 3D: Three.js を CDN から読む

| 演出 | 用途 | 向く縦横 | MulmoClaude / MulmoTerminal での使いどころ | 元の投稿 | 見本 | 実装 |
|---|---|---|---|---|---|---|
| キネティック・タイポの締め | 紹介（冒頭・締め）、告知 | 横・縦・正方形 | リリース告知の最初の 2 秒、ロゴ前の三語 | [shun_cmdouga](https://x.com/shun_cmdouga/status/2102719159524307233)、[higgsfield_ai](https://x.com/higgsfield_ai/status/2103963588012744859)、[1littlecoder](https://x.com/1littlecoder/status/2103587706999914649) | p1 | MA |
| UI 部品の持ち上げ | 紹介（新機能） | 横（縦は画面を 1 セルに絞れば可） | MulmoTerminal のヘッダチップ、ロスターの行、ボタンを画面から抜き出して拡大 | [pranavclickks](https://x.com/pranavclickks/status/2103598924632396258) | p2 | MA |
| 潜るズーム | 説明（どこにあるか） | 横 | グリッド → 1 セル → チップ。MulmoClaude ならワークスペース → コレクション → 1 レコード | [mdaman010](https://x.com/mdaman010/status/2103788160031592572) | p3 | 直書き |
| 線から立ち上がる図 | 説明（仕組み） | 横 | Chat → Collection → View の循環、エージェントとセッションの関係 | [onofumi_AI](https://x.com/onofumi_AI/status/2102548517596381463)、PR #126 のホワイトボード | p4 | MA |
| 蓄積していく暦と数字 | ビジョン、振り返り | 横・縦 | 「一年分の小さな記録」。MulmoClaude の Why に直結する | [guriham_lab](https://x.com/guriham_lab/status/2104154927362945532)、[brsabel](https://x.com/brsabel/status/2103132094243521015) | p5・v2 | 直書き |
| 仕切りが滑る前後比較 | 比較（旧 → 新、手作業 → 一言） | 横（縦は上下に分けて可） | 「メモを表にしてグラフ」→「今月を見せて」 | [excel_niisan](https://x.com/excel_niisan/status/2102719776984559798)、[martinleblanc](https://x.com/martinleblanc/status/2103565583128346678) | p6 | MA |
| 手描きの紙・筆致 | 雰囲気、ビジョン | 横・縦 | 暖色の水彩テーマとそろう。区切りや章の扉に | [ring_hyacinth](https://x.com/ring_hyacinth/status/2102986085328716066)、[NFT_Chen](https://x.com/NFT_Chen/status/2103380404791333144) | p7 | 直書き（canvas） |
| 3D の空間にセルを並べる | 紹介（全体像）、ローンチ | 横 | 「全部のセッションが 1 つの空間に」。ローンチ動画の見せ場 | [xikhar](https://x.com/xikhar/status/2104001664793600012)、[onofumi_AI](https://x.com/onofumi_AI/status/2102568200122884553) | p8 | 3D |
| 巻物テロップ | 説明（要点を順に） | 縦 | Shorts / Reels の機能列挙 | [cryptoninjanime](https://x.com/cryptoninjanime/status/2102580899040972982)（画像 15 枚 8.2MB → コード 11KB） | v1 | 直書き |
| 伸びるグラフで始まる資料 | 説明（報告） | 横 | 月次のまとめを見せる MulmoClaude のデモ | [koharu_ai_diary](https://x.com/koharu_ai_diary/status/2103794245186506804) | （p5 の数字と同型） | MA |

縦の投稿は 79 件中 13 件で、振り返り・列挙・再現比較に偏っていた（[guriham_lab](https://x.com/guriham_lab/status/2104154927362945532)、[chatcutapp](https://x.com/chatcutapp/status/2102819759247208653)、[cryptoninjanime](https://x.com/cryptoninjanime/status/2102580899040972982)、[pirrer](https://x.com/pirrer/status/2103737429954056454)）。4:5 は説明動画で使われていた（[itsluizneto](https://x.com/itsluizneto/status/2102540146055008689)、[brsabel](https://x.com/brsabel/status/2103132094243521015)）。この repo の 99 本はすべて 1280×720。

## 5. 採らなかったもの

- ブラウザゲーム、キャラクターの 3D モデルとアニメーション（xikhar の Spider-Man 系）: 製品の説明に対して重い。3D は p8 の「空間に並べる」程度で足りる
- グリーンバックのダンスや口パクのキャラクター（[sankakuten91256](https://x.com/sankakuten91256/status/2103483923783373039)、[QinElke](https://x.com/QinElke/status/2104176976261271655)）: 人物の扱いは PR #126 で判断済み
- ゲーム HUD の VS / K.O.（[szounft](https://x.com/szounft/status/2103947802426699853)）: 製品の空気と合わない

この文書に載せた投稿の URL は、すべて x-posts.json（oEmbed で実在を照合済みの 79 件）にある。

## 6. 作ってみて分かった MulmoAnimation の落とし穴（mulmocast 2.7.2）

見本を書き出してコンタクトシートで確かめたところ、次の 4 つで壊れた。どれもエラーにはならず、見た目が違うだけなので気づきにくい。

1. **同じ要素に `animate()` を 2 回かけると、毎フレーム両方が適用され、後に登録した方が勝つ**。開始前の区間でも後の登録の初期値が書き込まれるため、「0〜2 秒で拡大 → 3〜4 秒でさらに拡大」は最初から拡大済みになる。段階のある動き（カメラ、テロップ送り）は `render()` に直接書く（p3・v1）
2. **`scaleX` / `scaleY` は対応外**。対応する変形は `translateX` / `translateY` / `scale` / `rotate*` だけ。棒の伸び縮みは `width: [0, 100, '%']` で書く（p1・p6・v2）
3. **SVG の `opacity` は属性として書き込まれる**。初期値を style の `opacity:0` で書くと style が勝ち、ずっと見えない。SVG の要素は属性 `opacity='0'` で書く（p4）
4. **`transform` を持つ親は重なり順を閉じ込める**。暗幕の上に子要素だけを出したいときは、暗幕を同じ親の中に置く（p2）

逆に、次のことは確かめられた。

- `<script src>` で CDN の Three.js を読み、`render()` の中で `renderer.render()` を呼べば、WebGL の 3D もフレーム単位で書き出せる（p8。`preserveDrawingBuffer: true` を付けた）
- ナレーションを空にして `duration` を付けた beat は、TTS も画像生成も走らずに書き出せる。横 45.5 秒が 31 秒、縦 11 秒が 22 秒で書き出せたので、演出だけを試すときに安い

## 7. 作り方の知見（X の投稿から）

- 絵コンテ → 章分け → 章ごとにサブエージェント（[xiaohu](https://x.com/xiaohu/status/2102979455308439555)）。この repo なら「beat ごとに担当を分ける」に当たる
- 書き出したフレームを自分で見て直す（[AzamIntikhab](https://x.com/AzamIntikhab/status/2102508449955524707)）。今回の検品（beat ごとに 3 コマ抜いてコンタクトシート）と同じ手順で、実際に 4 件が見つかった
- 指示は長い（約 9,500 字、[Vladic_ETH](https://x.com/Vladic_ETH/status/2104198303919305127)）。「ワンプロンプト」を真に受けない

## 8. レベル別の見本集（「こんな表現がある」を見せる）

実際に使うかどうかは置いておき、演出の幅を見るための見本。レベルは「作るのに何が要るか」で分けた。

- L1（手堅い）: MulmoAnimation の範囲、DOM と SVG。4 節の 10 演出。`opus55-motion-sampler.json`、`opus55-motion-sampler-vertical.json`
- L2（映像的）: 奥行き・マスク・形の変化・合成を `render(frame)` に直接書く。`opus55-motion-showcase.json` の前半 4 本
- L3（作品的）: 描画エンジンを書く水準で、canvas・WebGL2・Three.js を使う。`opus55-motion-showcase.json` の後半 4 本
- テンポ軸（縦 9:16）: Shorts 型のハイテンポな切り替え。`opus55-motion-shorts.json`

| レベル | beat id | 演出 | 使った技 | 手本にした投稿 |
|---|---|---|---|---|
| L2 | L2-1-kinetic-type | キネティック・タイポグラフィ。マスクから文字がせり上がり、色ブロックのワイプで場面が変わり、文字がバウンスし、手書きの下線が引かれ、全体が縮んでロゴになる | 文字単位の時間差、`overflow:hidden` のマスク、easeOutBack | [higgsfield_ai](https://x.com/higgsfield_ai/status/2103963588012744859)、[shun_cmdouga](https://x.com/shun_cmdouga/status/2102719159524307233) |
| L2 | L2-2-parallax-3d | 2.5D のパララックス。背景の太陽、セルのグリッド、窓、チップ、ぼけ玉を実際の奥行きに置き、カメラが通り抜ける。距離に応じて被写界深度のぼかしをかける | CSS `perspective` + `translate3d`、奥行きから計算した `blur` | [higgsfield_ai](https://x.com/higgsfield_ai/status/2103964599737536831) |
| L2 | L2-3-liquid-wipe | 液状のワイプ。チップから揺れる塊が広がって次の場面になり、それを 2 回繰り返す | 毎フレーム作る `clip-path: polygon()`（正弦波の和で縁を揺らす） | [chatcutapp](https://x.com/chatcutapp/status/2102819759247208653) |
| L2 | L2-4-after-effects-hit | After Effects 風の衝撃。光漏れ、残像付きの突入、衝撃時のフラッシュ・揺れ・RGB のずれ、トリムパスの放射線、広がる輪、グロー、レンズフレア、字間が詰まる副題、最後はぼけながら抜ける | `mix-blend-mode:screen`、ゴースト 6 枚、`stroke-dasharray` による trim、`text-shadow` | [ConnorPRose](https://x.com/ConnorPRose/status/2103494412047147443)、[szounft](https://x.com/szounft/status/2103947802426699853) |
| L3 | L3-1-particles-logo | 粒子がロゴを組む。散った粒子が渦を巻いて「MulmoClaude」になり、爆散して「MulmoTerminal」に組み直す | 文字をオフスクリーンに描いて画素を拾う。軌跡は時刻の関数から描くので、残像も決定的 | [AzamIntikhab](https://x.com/AzamIntikhab/status/2102508449955524707) |
| L3 | L3-2-shader-halftone | 素の WebGL2 のフラグメントシェーダー。レイマーチした球の群れを、2 色の網点の印刷として描く。版ずれと紙の粒子も入れた | SDF、ソフトシャドウ、AO、回転した網点スクリーン | [akiy_8](https://x.com/akiy_8/status/2103434383218872503) |
| L3 | L3-3-three-city | 1 年の記録が 3D の街として立ち上がる。最初は線だけで、あとから面が付き、カメラが回り込む。1 本の塔にラベルが追従する | Three.js、`EdgesGeometry`、3D 座標を画面に射影してラベルを置く | [onofumi_AI](https://x.com/onofumi_AI/status/2102548517596381463)、[brsabel](https://x.com/brsabel/status/2103132094243521015) |
| L3 | L3-4-infinite-zoom | 無限ズーム（Powers of Ten）。年 → 日 → 記録 → 文 → 単語を、1 本の連続したカメラで潜る | 階層ごとに 10 倍の縮尺で入れ子にし、`10^(u-i)` で拡大する | [mdaman010](https://x.com/mdaman010/status/2103788160031592572) |
| テンポ | SHORTS-high-tempo | 10 秒・13 カット。0.4〜0.6 秒ごとに、ホイップ（横・縦）、白フラッシュ、グリッチ、ポップ、ズームを通り抜ける遷移で切り替える。どのカットもゆっくり押し込み、字幕は単語ごとに出す。上端に進捗バー | カットの表と遷移の種類を 1 つの `render()` で配る | [cryptoninjanime](https://x.com/cryptoninjanime/status/2102580899040972982)、[guriham_lab](https://x.com/guriham_lab/status/2104154927362945532) |

検品で分かったこと（L2・L3）:

- WebGL2 の生シェーダーも Three.js も、mulmocast 2.7.2 のフレーム書き出しでそのまま描けた（`preserveDrawingBuffer: true`）
- 残像やトレイルを「前のフレームに重ね塗り」で作ると、フレームを飛ばして描いたときに結果が変わる。見本では、時刻 `t` と `t - 0.045` の 2 点を結ぶ線として毎フレーム描き直した
- 書き出しの時間は、横 8 本（約 50 秒）で約 1 分、Shorts 10 秒で約 20 秒だった

## 9. mulmocast ユーザー向けのアイディア集（「これもできるの？」）

8 節までは「MulmoClaude / MulmoTerminal の説明に使えるか」で選んでいた。この節は基準を変え、X で見つけた表現のうち製品の説明にならないとして落としていたものを、mulmocast で作れる見本として拾い直した。動画生成 AI は使っていない。使った生成 AI は次のとおり。

- BGM: ElevenLabs Music
- ナレーション: Gemini 3.1 Flash TTS（`gemini-3.1-flash-tts-preview`）。mulmocast のモデル一覧には無いが、2.7.2 でもそのまま API に渡って動いた
- 画像: Nano Banana Pro（`gemini-3-pro-image-preview`）

| 系統 | デッキ（beat） | 何を見せるか | 使った仕組み | 手本にした投稿 |
|---|---|---|---|---|
| 音楽 | ideas-mv（mv-painted-kicks、24 秒） | 曲のキックのたびに筆が 1 本入り、曲が終わると 1 枚の風景画が描き上がる | ElevenLabs で 120 BPM の曲を作る → 低音の立ち上がりからキック 28 回を検出 → 時刻を台本に埋める。書き出した mp4 の音声で再検出し、ずれが 0 秒であることを確認した | [xiaohu](https://x.com/xiaohu/status/2102979455308439555)、[arlooooooo](https://x.com/arlooooooo/status/2103282282790633715)、[ring_hyacinth](https://x.com/ring_hyacinth/status/2102986085328716066) |
| 解説 | ideas-explain（math-derivative） | 割線の h が 0 に縮んで接線になり、式が項ごとに変形して f′(x) に至る。黒板風 | KaTeX（CDN）、canvas | [LinearUncle](https://x.com/LinearUncle/status/2103128559174971663)、[Hesamation](https://x.com/Hesamation/status/2103822595993018838) |
| 解説 | ideas-explain（ocean-dive） | 水面から深海 4,000 m へ潜る。光の筋が消え、発光生物が灯る | canvas、対数の深度計 | [lolkain](https://x.com/lolkain/status/2103191497424376286)、[mdaman010](https://x.com/mdaman010/status/2103788160031592572) |
| 解説 | ideas-explain（art-history-speedrun） | 同じ 2,400 粒の粒子が、洞窟の手形 → モザイク → 点描 → モンドリアン → ポップアート → ジェネラティブと組み変わる | canvas、粒子の目標座標の切り替え | [moonshot104](https://x.com/moonshot104/status/2103473343596785764) |
| データ | ideas-news（全 6 beat、約 64 秒） | 実行した時点の公開データから、台本・ナレーション・画面を自動で組む番組。GitHub で今週伸びた新しいリポジトリ 3 本と、世界 28 都市の今の気温を 3D の地球儀で見せる | GitHub search API と Open-Meteo を取得 → Python で台本を生成 → Gemini 3.1 の TTS。BGM は ElevenLabs | [gigabit_million](https://x.com/gigabit_million/status/2104068536041959719)、[brsabel](https://x.com/brsabel/status/2103132094243521015) |
| キャラクター | ideas-story（cafe-0〜3） | バリスタと常連の掛け合い。話している側の口が音声に合わせて開閉し、聞いている側は相づちを打つ。カメラが話し手に寄る | 2 段階: `mulmo audio` で先に音声を作る → 1/30 秒ごとの音量を測る → 口の開きとして台本に埋める → `mulmo movie` | [QinElke](https://x.com/QinElke/status/2104176976261271655)、[doerstokyo342](https://x.com/doerstokyo342/status/2103781798132211788)、[shoei05](https://x.com/shoei05/status/2103188019440394621) |
| キャラクター | ideas-story（battle-map） | 墨絵の地図の上を、架空の東軍と西軍が進む。筆の矢印が伸び、「決戦」のカットインが入る | Nano Banana Pro の地図、SVG の経路に沿って部隊を動かす | [den_neko__](https://x.com/den_neko__/status/2103801444596109428) |
| キャラクター | ideas-story（latte-battle） | 対戦ゲーム風。VS 画面、体力ゲージ（遅れて減る赤い部分つき）、コンボのカウンター、K.O. | DOM、揺れとフラッシュ | [szounft](https://x.com/szounft/status/2103947802426699853) |
| キャラクター | ideas-story（paper-collage） | 月・街・猫の切り絵を 3 層に重ねて視差で動かし、2 コマごとに紙が揺れ、紙の星が灯る | Nano Banana Pro で白背景の切り絵を 3 枚作り、乗算で重ねる | [NFT_Chen](https://x.com/NFT_Chen/status/2103380404791333144) |
| 3D | ideas-3d（game-chase） | GLB のロボットが手続き生成の道を走り、コインを取り、障害物を越える。スローモーション、HUD、ミニマップ付き | Three.js、GLTFLoader、`AnimationMixer` を毎フレームその時刻に合わせる | [xikhar](https://x.com/xikhar/status/2104001664793600012)、[pirrer](https://x.com/pirrer/status/2103737429954056454) |
| 3D | ideas-3d（stop-motion-clay） | 粘土の街とスライム。2 コマ打ち（12fps）で、形が毎コマわずかに揺れる | Three.js、canvas の指紋風テクスチャ | [pirrer](https://x.com/pirrer/status/2103737429954056454) |
| 3D | ideas-3d（same-scene-two-ways） | 同じ城を、左は設計図、右は影付きの描画で見せる。仕切りが走る | Three.js の scissor（描画範囲の切り抜き） | [onofumi_AI](https://x.com/onofumi_AI/status/2102568200122884553) |
| 合成 | ideas-composite（footage-overlay） | 本物の撮影映像の上に、自分で描かれる囲み、ルーペ、矢印、タイムコードを重ねる | `<video>` をフレームごとに seek し、ルーペは canvas に拡大コピー | [sankakuten91256](https://x.com/sankakuten91256/status/2103483923783373039)、[AiNamanari33743](https://x.com/AiNamanari33743/status/2104154745988587531) |
| 合成 | ideas-composite（reference-vs-recreation） | 上に撮影映像、下に同じ動きをコードで作り直したものを並べる | 同じ時刻で同期 | [chatcutapp](https://x.com/chatcutapp/status/2102819759247208653) |
| 合成 | ideas-composite（icon-choreography） | 基調講演風。道具のアイコンが弧を描いて飛び、回り、整列し、1 つが別の形に変形する | SVG、`getPointAtLength` による形の補間 | [DavidKPiano](https://x.com/DavidKPiano/status/2103555549929566323) |
| 形式 | ideas-composite（lottie-layers） | 手書きの Lottie（14 層）を beat の中で再生する | lottie-web の `goToAndStop` | [motion_mau](https://x.com/motion_mau/status/2102702060198346772)、[kelly_thepotato](https://x.com/kelly_thepotato/status/2103776947310637367) |
| 形式 | ideas-composite（retro-8bit） | ファミコン風。256×240 の canvas を拡大し、視差、歩行のコマ、文字送りのウィンドウを付ける | canvas、`image-rendering:pixelated`、独自のドットフォント | [ai_na_nitijou](https://x.com/ai_na_nitijou/status/2103333636942753870) |

作って分かったこと（mulmocast 2.7.2）:

- **CDN のライブラリはそのまま使える**: KaTeX、lottie-web、Three.js と GLTFLoader（three@0.147 の `examples/js` を 0.160 の本体と組み合わせた）が動いた。`render()` が Promise を返せば、読み込みや seek を待ってからそのコマが撮られる
- **ローカルの素材は `file://` で読める**: 画像も mp4 も読めた
- **音に合わせる方法**: mulmocast の中で合わせるのではなく、先に音を作って測り、数字を台本に焼き込む。2 段階にすれば、曲のキックにも口パクにも使える
- **乗算による切り抜きの合成**: 背景が白の生成画像は、乗算で重ねれば切り抜かなくても合成できる。ただし乗算は `transform` を持つ要素の中に閉じ込められるので、その要素自身に指定する。生成画像の背景はわずかに灰色なので、明るさとコントラストの補正が要る
- **BGM の既定値**: `audioParams.bgm` を書かないと、既定の BGM が入る（ideas-story で確認）
- **書き出しのタイムアウト**: 動画を seek する beat が複数あるデッキ（ideas-composite）は、初回の書き出しで puppeteer がタイムアウトした（`Runtime.callFunctionOn timed out`）。もう一度書き出すと通ったが、済んだ beat が再利用されたからではない（次項）
- **アニメーションの beat はキャッシュされない**: 2.7.2 では、`animation` 付きの `html_tailwind` の beat は、中身を変えていなくても書き出すたびに `*_animated.mp4` と静止画が作り直される（2026-09-27、変更していない試験用デッキを書き出し直して、4 beat すべての更新時刻が新しくなることで確認した）。beat が多いデッキは、1 か所を直しただけでも全体の書き出し時間がかかる
- **データの題材**: 実データで自動生成するときは、題材を選ぶ段階でセンシティブなもの（災害、政治、企業の内紛、プライバシー）を外す。最初の版では Hacker News の見出しと地震のデータを使っていたが、差し替えた
- **Opus 5.5 の MV のソース**: X で話題になった Opus 5.5 の MV（「I'm Upping My P(doom)」）のソースコードが、GitHub の `JohnHeibel/PDoomVideo` で公開されていた（2026-09-27 の検索で今週の新しいリポジトリ 6 位、★1,150）
