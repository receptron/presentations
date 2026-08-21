# mulmoterminal-launch-v8.json — 「あなたがボトルネックになった日」v8（1 メッセージ版）

v7（台本作者の 2 分台本を機能カット込みで組んだ版）から、作者の判断（2026-08-17 Slack: remote は落とす／細かい機能紹介より「多数を同時に動かしているとき状態が一瞬で分かる」に特化／expand して状態が変わってどんどん指示するシーンが欲しい／動画で active な terminal をカメラで拡大するのは負け／色にメリハリ）に合わせて組み直した。**英語版が canonical**、`_ja` はナレーションだけ日本語（見出しは英語のまま）。

## 構成（9 beat）

| # | 台本の意図 | 素材 | 種別 |
|---|---|---|---|
| 0 | 黒画面＋点滅カーソル | html（`blink`） | mock |
| 1 | 同じ見た目のタブ 5 枚を手で切り替える | `tab-web/mobile/docs/auth/api.mp4` — **take-pain**（Shell セルで `claude --model sonnet` を 5 本）から各セルの端末部分をクロップ | 実写＋タブ枠 |
| 2 | 止まっている 1 枚と、その経過時間 | `tab-api.mp4`（question tool で止まっている）＋ `waiting 0:00→4:12` のバッジ | 実写＋html |
| 3 | 全部を 1 画面に。青→amber | `grid.mp4` = take-grid 4〜22 s（**amber 点灯は clip 11.4 s**） | 実写 |
| 4 | ⤢ で拡大して答える | `light.mp4` = take-cockpit 0〜13 s（expand 2.2 s / 回答 9.8 s） | 実写 |
| 5 | roster：頼んだこと・返ってきたこと。緑の行へ移って次の指示 | `roster.mp4` = take-cockpit 13〜34 s | 実写 |
| 6 | 次が roster で光る → クリック → 答える | `loop.mp4` = take-cockpit 56〜76 s（**amber2 点灯 clip 5.9 s**、クリック 7.6 s、回答 15.5 s） | 実写 |
| 7 | 締め（triage） | `close.mp4` = take-cockpit 186〜207 s（amber3 点灯 3.6 s、回答 12.6 s、グリッドへ 15.8 s） | 実写 |
| 8 | `npx` | html | — |

落としたもの（作者判断）: スマホ（1:28）、worktree→diff→PR（1:14）、kill→再起動→htop（1:44）、「1〜3 体でも効く」の一文。remote を落とした判断は 2026-08-20 のレビュー共有時に明記済み。

## 素材の正本

`mt-demo-home/footage/2026-08-17/cockpit-n/`（`record-cockpit.mjs`、9 checkout・1x 描画・1200×800）。カット点は各 `-marks.json`。クリップは全部 ffmpeg 1 行（trim → crop で上部ツールバー 60px を落とす → 1200×740）。タブ用は各セル本体 370×270 を 2 倍（740×540）に拡大しているので**甘い** — 痛みの絵だけ 2x で撮り直す価値あり（`launchBrowser(..., {scale: 2})`、Shell 5 セルなら軽いのでクラッシュしない見込み）。

## 使うときの注意

- **take-cockpit 85〜111 s は使わない**（api2 に追加指示を打つ区間に Claude Code の hook タイムアウトの赤字が拡大ペインに出る。機械が重かった影響）→ v8 の clip はこの区間を避けている
- **take-pain の auth セル**は 8〜14 s だけ使う（それ以外の時刻に `find` の出力で個人パスが写る）→ `tab-auth.mp4` はその窓
- `verify-takes.sh` は grid / cockpit を FROZEN と判定したが、**端末が流れ続ける画では「最終フレーム ≒ 終了後の静止画」が成り立たず誤判定**する。時系列でフレームを抜いて中身が進んでいることを目視で確認した（skill 側の課題として記録）
- 「Green is done」（beat 3）: take-grid の中では緑が出ない（全部 blue → 1 つ amber）。緑は beat 5〜6 の roster で見える。ナレーションは台本の文のまま

## v7 レビューで直したこと（v8 に反映）

見出しは `top:56px`・映像は `top:108px / 幅 960`（下端 700 で字幕に掛からない）／タブ枠に映像が収まる（760 幅の枠に 740 の映像）／4:12 は MulmoTerminal ではなく痛みの絵に／⤢ とクリックで拡大（カメラのズーム無し）／旧 footage の使い回し無し（全部 cockpit-n）／スマホ・機能カット無し

## 2026-08-17 レビュー 1 回目の対応

- **TTS が話者の `instruction` を読み上げていた**（ja: 「琥珀は、あなたを待っています」が beat 1・2 に混入、en: beat 3 が 3 秒長い）。指示文の中の引用フレーズが原因。mt-first-run と同じ文言に戻して全音声を再生成。**指示文に台詞を引用しない**こと（文字数 ÷ 秒 の外れ値で検出できる: en 1.6〜3.0 語/秒、ja 3.5〜7 字/秒）
- 4:12 のバッジは「早送りのカウントアップ」だと経過時間に見えなかった → **`waiting for 4:12` から実時間で秒が進む時計**に変更、見出しは beat の最初から出す
- 締め（beat 7）は cockpit の戻りグリッドに hook タイムアウトの赤字が写ったので、take-grid の amber 部分（冒頭の callback）に差し替え
- ja の尺は ja の音声から算出（`max(en の duration, ja voice + 0.8)`）
- **解像度**: グリッドと痛みの絵は 1x 撮影のため甘い → `MT_SCALE=2 … --only grid,pain` で 2x 撮り直し（未実施・撮影窓が要る）

### まだ怪しいところ（未対応）

- 拡大ペインと roster 行に staging 用プロンプト（"Ask me exactly one multiple-choice question … using your question tool"）がそのまま写る。自然な文で question tool が安定して出るか未検証
- beat 3 のグリッドに緑（done）が出ないままナレーションが "Green is done" と言う（緑は beat 5〜6 の roster で見える）
- beat 4 の冒頭 1〜2 秒、拡大直後のペインが空（描画待ち）

## 2026-08-18 レビュー 2 回目の対応

指摘（en 版の秒数）と対応:

| 指摘 | 対応 |
|---|---|
| 1–8 s: 何の絵か分からない、カーソル点滅だけ | **1 体のエージェントが生成している端末**に差し替え（`solo.mp4` = 2x の take-pain、web セル 0〜9 s の本体。汎用のタイトルバーを付けた 1 枚窓） |
| 9 s〜: タブ窓が縦長で字幕に被る | 窓を **900×450 の横長**に（上 100px → 下 586px、字幕帯に掛からない）。中身は 2x の take-pain の 4 セル（web / mobile / docs、auth は**個人パスが写るので不使用**） |
| 4:12（バッジと見出し）は意味が伝わらない・数字がズレる | **両方とも削除**。ナレーションの "four minutes later" だけ残す。beat 2 は止まっているタブ（api の質問ダイアログ）に着地して静止 |
| 25 s: 9 分割の文字が甘い | **2x 撮り直し**（`footage/2026-08-18/cockpit-2x/`、`MT_SCALE=2 --only grid,pain`）。grid / close / solo / tab-* を 2x から切り直した。cockpit（light / roster / loop）は 1x のまま |
| 青＝作業中・緑＝完了 に枠と説明を | グリッドに **状態リング＋ラベル**（`working` は中央セルに 3.4 s、`needs you` は amber セルに 7.8 s、HTML オーバーレイ）。**緑は take-grid に出ないので付けていない**（ナレーションの "Green is done" は残る。次の撮り直しで「すぐ終わるタスク」を 1 本先に入れる） |
| キャプションと音声がずれる（32 s に音声なし） | 原因は**明示 `duration` が音声より長い beat**（`estimate` 分割はビート尺で按分するので、待ち時間があるぶん後半のキャプションが遅れる）。→ 全 beat の `duration` を外し（末尾の npx だけ残す）、**待ちは早送りで詰めた** |
| 喋り終わってから次まで長い | 同上。クリップ側で「対象の状態が来るまでの待ち」を 1.5〜2 倍速に（`light` = 拡大直後の空ペイン 2.45〜6.0 s をカット、`roster` = 行を見て回る区間を 2 倍速、`loop` = amber2 点灯までと回答後を 1.5〜2 倍速） |
| 40 s: 拡大ボタン／ショートカットを使ったと分かるように | **⤢ ボタンにリングを焼き込み**（`light.mp4` 0.4〜2.4 s、drawbox 白）。カメラは動かさない |
| 42 s: 拡大直後の読み込み中が写る・上が切れる・9 分割だけ切り抜かなくてよい | 読み込み中（2.45〜6.0 s）をカット。**全 beat をアプリの全画面（ツールバー込み・1200×800）**に戻し、幅 860 で配置（上 92 → 下 665） |
| 1:04 "roster" | 一般語（名簿・当番表）で英語ネイティブには通じ、製品 README も "cockpit roster" を使うので**そのまま** |
| どこをクリックしたか分かるように | **roster 行のクリックにリングを焼き込み**（`roster.mp4` 5.1〜6.3 s の api3 行、`loop.mp4` 3.3〜4.5 s の api 行。座標は take-cockpit の 19.5 s / 63.0 s のフレームから実測） |

素材の追加: `footage/2026-08-18/cockpit-2x/`（take-grid 2400×1600・16.7 s・amber 9.62 s／take-pain 2400×1600・24 s）。`verify-takes.sh` はここでも FROZEN 判定だが、フレーム差分（2 → 6 → 10 → 14 s で平均差 1.4〜2.5）と目視で LIVE を確認。

### 2026-08-18 レビュー 3 回目の対応（cockpit の 2x 撮り直し）

3 点とも撮り直しで解消した。素材は `footage/2026-08-18/cockpit-2x-f/`（5 回目で完走。a〜e は rig の穴で失敗、下記）。

| 残件 | 対応 |
|---|---|
| staging 用プロンプトが写る | amber の 3 本と pain の api を**人が書いた文**に（例: "Before you write anything: should API errors go back to clients as structured JSON or plain text? Ask me, two options, wait for my answer, then implement it."）。question tool の指示は **demo リポの CLAUDE.md** に移した（"ask with your question tool (AskUserQuestion) and wait"、`demo-baseline` に commit）。tmux で 1 本試して picker が出ることを確認してから撮った |
| "Green is done" のときグリッドに緑が無い | quick done（web3）を**最初に**送り、`waitState(done, is-done)` をロール前のゲートにした。グリッドの beat に **緑のリング＋`done` ラベル**（右上セル）を追加 |
| cockpit が 1x | **2x で分割録画**: a（拡大→回答）／ b（roster→done 行→追加指示→そのまま amber2 の点灯待ち→クリック→回答、約 67 s）／ d-N（amber3、30 s ごとにローテーション）。長回しを避けたので落ちなかった。クリップは 2400×1600 → 1800×1200 |

roster が 9 行入るように demo-config に `cockpitLines: {summary:1, prompt:1, response:1}`（撮影中は `POST /api/config` で反映）。役割も **押す行・光る行が roster の 1〜5 行目**に来るよう並べ替え（amber1=web、done=web3、amber2=api、amber3=api2）。

撮り直しで踏んだ穴（全部 rig に反映・commit 済み）:

- **idle_prompt の Notification** — 待たせて 60 s 経つと Claude Code が Notification を送り、こちらが行を見た（flag clear）**後**に届くと amber になる。cue 前に「見て clear → 送る」を入れた（`cueWhenFree` の is-blocked 分岐）
- **点灯の瞬間が chunk の切れ目に落ちた**（b を止めて c を始める 2 秒の隙間）→ b を止めずに待ちへ入り、30 s ごとのローテーションだけにした
- **`cellState` が dot の色トークンで読めない**ケースがあった → roster 行の状態語（waiting / done / running / idle）を fallback に
- **ssh のパスフレーズ入力が端末に出た**（`Enter passphrase for key '/Users/…/.ssh/id_ed25519'` が question dialog に重なる）→ 全プロンプトに "Work offline: no git fetch, pull, or push"、demo リポに `core.sshCommand = ssh -o BatchMode=yes`
- 質問プロンプトの後に "then implement it" を足した（回答後に青へ戻る。放置すると idle_prompt でまた amber になる）

### 公開前に潰すもの — セルの中に個人パスが写る（→ レビュー 8〜9 回目の撮り直しで解消済み）

Claude Code が Bash ツールで `cd /Users/<name>/…/mt-demo/acme-api2 && …` と**実パスを表示する**ことがあり（`/tmp/mt-demo` は symlink で、realpath はホーム配下）、グリッドのセルにその行が出る（take-grid 2x-f の 36 s 付近 api2 セル、d-1 末尾の mobile2 セル）。860 px 幅の表示ではほぼ読めないが、**公開版では対策が必要**: demo ツリーを symlink でなく `/tmp/mt-demo` の実体にする（capture-guide §3 の元の設計に戻す）か、CLAUDE.md の「絶対パスを出すな」を Bash の cwd 指定にも効くよう強める。今回の v8 は内部レビュー用としてそのまま。

### まだ残っているもの

- （解消済み）上の個人パスは 2026-08-19 の撮り直しテイクで再確認して消えた
- 端末内の文字は 860 px 幅ではまだ小さい（2x で輪郭は締まった）。読ませる場面は拡大ペインに任せる方針のまま

## 2026-08-18 レビュー 4 回目の対応 — 冒頭 3 カットの文字が大きすぎる・見切れる

原因は 2x ではなく切り出し: 5 分割 pain テイクの **375 CSS px 幅のセル**を 900 px に引き伸ばしていた（2.4 倍）。9 分割は全画面を 0.72 倍にしているだけなので正しく、そのまま。

対応: 痛みの絵を **横長で撮り直し**（`footage/2026-08-18/pain-wide3/`）。`MT_WINDOW=1300x560`（roster 約 350 px ＋ペイン約 940 px）で、**nord テーマの予備リポ 5 本（docs / billing / worker / infra / cli）** に Shell → `claude --model sonnet` を立て、**1 ペインずつ拡大して 11〜14 s 録画**（`take-pain-<repo>`）。冒頭用に docs だけプロンプト直後（生成中）にも 1 本（`take-pain-acme-docs-working`）。ペイン本体を `crop=1800:880:736:236 → scale=900:440` で切ると**文字は 1x の実寸・行は丸ごと・輪郭は 2x**。タブ窓とソロ窓は 900×440。

- 最初に `MT_WINDOW=940x560` で撮ったら、拡大ペインの横に roster（固定幅）が付いてペインが 600 px 幅になり 2:1 にならなかった → 1300 幅にして解決（`pain-wide/` は不採用）
- 止まっている 1 枚は cli（question tool）。worker も CLAUDE.md の nudge で質問して止まったので、タブには使っていない
- rig: `--only pain` で 9 セルの起動と take-grid を飛ばすようにした（`WANT_NINE`）

## 2026-08-18 レビュー 5 回目の対応

| 指摘 | 対応 |
|---|---|
| タブの端末が全部 "9s" で止まって見える | 痛みの絵を撮り直し（`pain-wide4/`）: 5 本に**重さの違うタスク**を出し、**4 分後に**各ペインを録画。時計が "1m 13s" / "2m 12s" / "45s" / 生成中 "(16s · thinking)" / 質問ダイアログ とばらけた（`MT_PAIN_WAIT_MS`、既定 220 s） |
| 39 s: 拡大直後の空ペインのフレーム | 拡大の 2.35〜3.9 s を切って詰めた（`light.mp4`）。行クリック後の 0.3 s の描画中は残している |
| 9 分割も撮り直し | `cockpit-2x-g/` で grid＋cockpit を撮り直し。グリッドは amber 1・緑 4・青 4、個人パスの写り込みなし。beat 3〜5・7 は g、**beat 6（loop）だけ f のまま** — g の cockpit-b 後半で web2 行の AI 要約が日本語（「ログインモジュール実装」）になったため。roster の要約はサーバ側の生成でデモ CLAUDE.md の英語指定が効かないことがある（要注意・再発したら要約を消す設定を探す） |

## 2026-08-19 レビュー 6 回目の対応

- beat 1 の見出し "the slowest thing is you" が 4.0 s から出るのにナレーションが 5.4 s で終わり、一瞬しか見えなかった → **beat の頭から表示**（他の beat と同じ）
- クリック注釈を**枠から「動くポインタ」に変更**: アプリ自身の状態枠（amber / 緑 / 青の選択）と白い枠が競合して「状態」か「操作」か分かりにくかった。ポインタ形の矢印 PNG（白＋黒縁、`scratchpad` で生成）を ffmpeg の `overlay` で拡大ペイン側から目的の行／⤢ ボタンへ 0.6〜0.7 s かけて動かし、止まったところで **0.25 s の枠パルス** → 消す。実機のポインタは screencast に写らないので、その代替。座標は 2400×1600 のソース系で `scale` の前に焼く（`light.mp4` = ⤢、`roster.mp4` = web3 行、`loop.mp4` = api 行）

## 2026-08-19 レビュー 7 回目の対応 — 「53 s で止まる」「貼り付けに見える」「TTS と画面が合っていない」

原因は beat 5（roster）の作りにあった: ナレーションは「roster に頼んだこと・返ってきたことが並ぶ」なのに、映像は **done 行をクリックしたあと追加指示を 2 倍速で打っている**（貼り付けに見え、途中で beat が終わって「止まって」見えた）。言葉と絵がずれていた。

対応: **beat を 2 つに割った**。
- beat 5（roster、"remembering → 0 seconds"）: api 行を見る → 行を読む → ポインタで done 行（web3）をクリック → その完了結果を読む、まで。打鍵なし
- **beat 6（新規）**: *"When it is done, the next order goes in right there — no window to find, no tab to raise."*（ja: 「終わったら、次の指示はその場で打つ。探すウィンドウも、開くタブもありません。」）— 追加指示を**等速で**打ち、Enter、Claude が動き出すまで（`next.mp4` = take-cockpit-b 12.4〜22 s、1x）。レビューで求められた「expand して状態が変わってどんどん指示する」シーンがここに入る
- 以降は 1 つずつ後ろへ（loop = beat 7、締め = beat 8、npx = beat 9）

## 2026-08-19 レビュー 8〜9 回目の対応

- **スピナーが止まる／打鍵がコマ落ちする**: 原因は mulmocast の `animation: {movie:true}`（実時間 screencast 取り込み。素材 27 fps → beat 動画 9 fps）。全ビートを **`animation: true`（フレーム単位）** に切り替え、素材のコマがそのまま残るようになった。skill にも記録
- **「結果を読む」ストーリーをやめた**: beat 5 は拡大表示のまま **roster の行を上から順に薄くハイライト**（web → web2 → api → mobile）。セッションは切り替えない
- **PR / issue の動きを入れた**: 打つ追加指示を *"Open a pull request for this — pick the branch name yourself."*（done 行）と *"Good. File a GitHub issue for the follow-up work you would suggest."*（待ち時間の完了セル）に。GitHub の remote があるのは acme-web だけなので **done 役を acme-web に**、amber1 を acme-web2 に移した（remote は変更しない方針）。撮影中に本当に PR が立った（mt-demos/acme-web #17）。ただし issue の方は api2 の remote がローカルパスなので失敗し、その旨の返答が d-1 末尾のグリッドに写る → 締めは take-grid のコールバックを使用
- 素材: `footage/2026-08-19/cockpit-2x-h/`（grid / cockpit、2x）と `footage/2026-08-19/pain-wide5/`（痛みの絵。重い仕事を出して 1.5 分後に録画 → 大半がスピナーで動いていて、時計は分単位。1 本は生成中、1 本は質問で停止）
- クリック注釈は全部「動くポインタ＋クリック時の枠パルス」。beat 4 の ⤢（top-middle セル）、beat 6 の done 行（web = 1 行目）、beat 7 の api 行
- 撮り直しのたびに変わる座標（⤢ ボタン・roster 行）は、そのテイクのフレームから測り直している（この NOTES に数値は書かない。切り出しコマンドはこの版のものが正本）
- フレーム単位レンダリングの落とし穴（2026-08-19）: `imageParams.concurrency` 既定 4 だと 4 ビートが同時に puppeteer でコマ撮りして `Page.captureScreenshot timed out` で落ちる → **`concurrency: 1`**。それでも beat 5（ほぼ静止・17 s の ja）だけ落ち続けたので、その beat は `animation: {fps: 15}`（コマ数半分）にした。クリップは beat の尺より **数秒長く**しておく（末尾ぎりぎりまでシークすると止まることがある）


## 2026-08-19 レビュー 10 回目の対応 — beat 7 の筋を「光っているものから選ぶ」に

- 指摘: 「Answer it, and the next one lights up」は嘘 — 画面は「api が**もう**光っている → クリック → 答える」で、答えた後に光るものは無い。素材（take b）で api が光る瞬間は b 23〜25 s（api2 に issue 起票の指示を打っている最中）にあり、loop クリップ（b 27 s〜）はそれより後から始まる
- 直し: **筋を「次は光っているものから選ぶ」に**。ナレーション en「Then you pick the next one from whatever is lit. Click, answer, move on. You never go looking — the roster tells you.」/ ja「次は、光っているものから選ぶだけ。クリックして、答えて、次へ。…」、見出し `pick from what is lit`。クリップ冒頭で web2 と api の 2 行が光っていて、そこから api を選ぶ絵になっているので、この筋のほうが映像に合う
- ついでに確認した 2 点（変更なし）
  - 52 s の roster で `prompt` 1 行だけの行があるのは MulmoTerminal の仕様 — `summary`（AI 題名）と `reply` は**ターンが 1 回終わった時点**で付く（server/session/registry.ts）。web3 / api2 / api3 / mobile2 は撮影直前に最初の仕事を渡したばかりで、まだ何も返ってきていない
  - 締めの「No Electron」は 60 秒版（v6）にはあったが、v7 を台本どおりに組んだとき（台本の最終カードは「That is the whole install.」+ npx + MIT · URL のみ）に外れ、v8 もそれを引き継いでいる。明示的な「外す」判断ではない。現状維持
- 1:06 の場面飛び（beat 6 → 7）: take b の 17〜27 s（api2 行をクリック → "Good. File a GitHub issue for the follow-up work you would suggest." を打つ）を丸ごと切っていたのが原因。**速度の規則を変更**: ポインタ操作は等速、**打鍵は 4 倍速**、待ちは 2 倍速（それまでは「打鍵は等速」で、入らない打鍵は切っていた）。loop.mp4 を組み直し: b 17.3〜19.7 等速（ポインタ → api2 行 → クリック）→ 19.7〜27.3 を 4 倍速（issue 指示の打鍵。その間に api 行が amber に変わる）→ 27.3〜30.5 を 2 倍速（ポインタ → 光った api 行）→ 30.5〜31.5 等速（クリック）→ 31.5〜39.2 を 2 倍速（質問に答える）→ 4 s ホールド = 14.8 s。issue 起票の動きも画面に残る
- beat 6 の PR 指示の打鍵（4.5 s・等速のまま）は未変更 — 同じ規則を当てるなら 4 倍速にする


## 2026-08-20 レビュー 11 回目の対応 — beat 2 の「4 分」を落とす

- 指摘: beat 2 のナレーションが長くてテンポが悪い。「4 分」の数字を入れず「気づくまで動いていない」趣旨に
- 直し: en「One of them is always stopped. A permission prompt. A question. Until you notice, it does nothing at all.」/ ja「どれか 1 体は、必ず止まっています。許可待ち。質問待ち。あなたが気づくまで、何もしていません。」（14.5 s → 約 9 s）
- 副次効果: いまの絵のタイマーは「1m 21s」「1m 34s」で、「four minutes」は映像と食い違っていた。数字を落としてズレも解消
- 4 倍速バッジ（▶▶ 4×）は**入れない**で確定（レビュー 10 回目の打鍵 4x 区間。バッジまで付けると画面がうるさい）
- 成果物の置き場整理: 旧キャプション版 mp4（`_en__en` / `_ja_ja__ja`）と assets の迷子 3 本は各ディレクトリの `old/` へ mv。台本レビュー用に `mulmo pdf --pdf_mode handout --pdf_size a4` で en / ja の handout PDF を生成（メイン checkout の output/ に cp）
