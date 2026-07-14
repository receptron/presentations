# Nurtured at Home — arXiv submission status

Paper: **Nurtured at Home: Local-First Personal AI Through Schema-as-Application**
Author: Satoshi Nakajima (The Singularity Society) / satoshi@singularitysociety.org
Package: `docs/arxiv/nurtured-at-home/arxiv-upload.tar.gz` — regenerate anytime with
`docs/arxiv/nurtured-at-home/package.sh`(main.tex + main.bbl + refs.bib + 図3枚、tectonicビルド検証済み)

## 現在地(2026-07-14)

**endorsement 待ち。** tar.gz のアップロードにはまだ進んでいない。

- [x] 原稿最終化(レビュー2巡反映、19ページ、PR #49 マージ済み)
- [x] 投稿パッケージ生成(.bbl 同梱 — arXiv AutoTeX は BibTeX を実行しないため必須)
- [x] arXiv で投稿開始 → cs.AI への endorsement が必要と判明
- [x] endorsement をリクエスト → 届いたメールを Yohei に転送(2026-07-14)
- [ ] **← いまここ: Yohei がメール内のコードで承認するのを待つ**(承認は即時反映・cs.AI について恒久)
- [ ] arXiv のユーザーページから投稿を再開
- [ ] `arxiv-upload.tar.gz` をアップロード → **AutoTeX ログを確認**(エラーゼロのはず。既知の warning: overfull hbox 1件)
- [ ] プレビューPDFを目視確認: Figure 1(p.7)、Table 2(p.14)、参考文献
- [ ] メタデータ入力:
  - Title: Nurtured at Home: Local-First Personal AI Through Schema-as-Application
  - Authors: Satoshi Nakajima
  - Abstract: PDF冒頭からコピペ(`---` はフォームでは em dash に)
  - License: **CC BY 4.0**(論文フッターの表記と一致させる)
  - Category: primary **cs.AI**(endorsement 先)、cross-list **cs.HC**
- [ ] Submit → アナウンス待ち(平日締切 14:00 ET)

## 投稿後にやること

- [ ] arXiv ID をこのファイルと `nurture-paper-notes.md` に記録
- [ ] 姉妹論文(DSLs-as-Harnesses / Workspace-is-the-Agent、mulmoclaude リポジトリ側)との相互引用を ID で更新 — 掲載順は Satoshi の判断
- [ ] 学会投稿(UIST / CHI systems)する場合: venue 書式変換、§2 デルタチェック、E2 反復トライアル(`nurture-paper-notes.md` のチェックリスト参照)

## 保留中(任意)

- §2 文献デルタチェック(2026-07-13 のスキャン以降の新着確認)— アップロード前にやれば v1 に反映できる。やらずに投稿した場合は v2 で対応
