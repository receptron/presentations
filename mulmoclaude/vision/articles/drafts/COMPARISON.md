# Article 1 — Draft Comparison Memo

Three drafts of "Beyond the Sea of App Icons," one per prescribed angle, judged against PLAN.md ("Voice and taste" + "Article 1") and research-notes.md. This memo is built so a 15-minute read of the three drafts is enough to decide.

## 1. Scores

| Dimension | A — scene-first | B — arc-first | C — discourse-first |
|---|---|---|---|
| Voice | 9 | 9 | 9 |
| Concreteness | 9 | 9 | 9 |
| Non-tech readability | 8 | 8 | **5** |
| Tech-savvy compelling | **7** | 9 | 9 |
| Honest cost | 9 | 9 | 8 |
| Structure | 9 | 8 | 7 |

Totals: A 51, B 52, C 47. The totals are misleadingly close — the failure modes are what matter. A is weakest exactly where the series stakes its claim (differentiation for the tech reader); C is weakest exactly where the dual-audience rule bites (a non-technical reader gets no story for ~1,300 words); B has no low score but has the only hard rule violation.

## 2. Draft assessments

### Draft A — scene-first (`01-draft-A-scene-first.md`)

**What the angle bought / cost.** Opening cold on Maria's twenty minutes buys the best non-technical on-ramp of the three — the "seams *between* the programs" diagnosis and the pivot line ("There is no icon on her home screen that accepts that sentence") are the sharpest statement of the problem anywhere in the corpus, and the draft is otherwise near-publishable: every hedge preserved, both refuted claims absent, Mulmo confined to one first-person paragraph in the last third, quotable line earned mid-piece. What it cost: the "Others have noticed" section maps Nadella and Karpathy as allies but **never differentiates** — it never states what they stop short of, so a tech-savvy reader finishes knowing the author is careful but not what territory the series is claiming. That is the series' key positioning line (AI-*authored*, all three layers) left unsaid in the article whose spec says to say it.

**Quotable line.** "The app dies twice: you stop choosing apps, and apps stop needing to pre-exist."

**Must-fix violations.** None. Top should-fix: add the differentiation move to "Others have noticed" (the gap above). Nits: MCP Apps/SEP-1865 belongs to Article 2 per the citation map; Karpathy's talk title rendered loosely ("Software 3.0" instead of "Software Is Changing (Again)").

*What to look for in your read:* the opening two pages (best Maria anywhere) and the honest-cost section — then notice that when the essay reaches the discourse, it stops one paragraph short of planting a flag.

### Draft B — arc-first (`01-draft-B-arc-first.md`)

**What the angle bought / cost.** Opening on the 2025 whitepaper's taxi metaphor and then breaking it buys the strongest single section in any draft: **the turn** — the restaurant-list-as-Tokyo-subway-map scene, "The driver had built the vehicle," a named artifact and a finding that broke the author's own papers. It is the plan's voice rules executed exactly. B is also the only draft that completes the discourse map: "Here is the map, then" — Nadella names no architecture, Karpathy defends a distinct app layer, generative-UI keeps vendor-authored schemas — "That unclaimed square is where this series lives." What it cost: to set up the turn, MulmoChat is named at ~30% of the piece, a hard violation of the last-third rule; the quotable line lands as a near-verbatim repeat of the sentence above it; and the roadmap close runs well past the spec's two sentences. One series-level cost no judge flagged: the subway map is Article 5's designated opener (PLAN.md: "the six-views table (Tokyo subway map opener)") — spending it in Article 1 cannibalizes that piece, or at least forces Article 5 to open on a scene the reader has already seen.

**Quotable line.** "The app dies twice: you stop choosing them, and they stop needing to pre-exist."

**Must-fix violations.** MulmoChat named by name at the 30% mark ("I built a prototype, MulmoChat, to find out...") — mechanically easy to fix (say "a prototype" there; the name and link already appear in the last-third section), but it must be fixed. Should-fix: MulmoClaude carries the turn but has no repo link.

*What to look for in your read:* "The turn" section and the closing paragraph of "The neighbors" — those two are the graft candidates whatever you pick — and decide whether you're willing to spend the subway map here instead of in Article 5.

### Draft C — discourse-first (`01-draft-C-discourse-first.md`)

**What the angle bought / cost.** Opening on Nadella predicting the collapse of his own product category buys the best epistemic-hygiene performance possible: three positions credited precisely and made to disagree productively before the thesis appears, the single best Karpathy steelman ("That sounds like Nadella's side of the argument. It is not."), a fully scoped SaaS-Bench citation, and the Bain position treated as a specification. Tech-savvy trust is maximal. What it cost is the mirror image: it opens with a thesis-shaped fact, not a scene, and Maria arrives at ~55% of the piece — the non-technical half of the audience gets no story to hold for the entire first act (hence the 5). It also asserts the unclaimed-quadrant claim in print against research-notes.md's explicit instruction to verify the Builder.io essay first, drops Liad Yosef from the MCP-UI credit, and uses "capabilities" as the governing noun where the series checklist requires "pillars."

**Quotable line.** "The app dies twice: you stop choosing apps, and apps stop needing to pre-exist." (All three drafts independently chose the same candidate — it's the right one.)

**Must-fix violations.** None at must-fix severity, but the should-fix list is the longest: thesis-first opening (direct checklist violation), Maria deferred past the midpoint, unverified gap claim published, pillar-vocabulary drift.

*What to look for in your read:* the first three sections as a quarry, not a structure — the Karpathy steelman, the SaaS-Bench paragraph, and "Understanding was the door; generation was the room" are the best versions of those moves in any draft.

## 3. Graft candidates

From **A** (carry into any winner):
- The full Maria opening, ¶1–5, especially "every individual step was easy — that is what makes it maddening" and the pivot "There is no icon on her home screen that accepts that sentence" (lines 3–9). The best scene-first opener available.
- Discovery objection at full strength: "the burden shifts from *finding the feature* to *imagining the possibility*, and imagination is far less evenly distributed" (honest-cost section, line 59). Graftable verbatim.
- The trust answer: "it earns it the way Karpathy's Iron Man suit does — by making its work fast to inspect and cheap to reject, never by asking to be believed" (line 61).
- The Nadella hedge treatment: "Note the 'probably' — he hedged, and the 'SaaS is dead' headlines that followed were the media's sentence, not his" (line 49).

From **B**:
- **The turn**, whole section (lines 21–31): subway map → "The driver had built the vehicle." Strongest personal-arc material in the corpus — but see the Article 5 collision above before spending it here.
- The discourse-map close: "Here is the map, then. Nadella predicts... Karpathy supplies... To my knowledge, nobody in this discourse yet claims the full fusion... That unclaimed square is where this series lives" (line 55). This is the differentiation paragraph A is missing.
- "Count what never happened" walkthrough close, with "not features of any pre-built product" (line 63).
- "The sea of app icons is exasperating, but it is also a map... the catalog was doing real work" (line 69) — the discovery objection that advances the thesis when answered.

From **C**:
- The Karpathy two-sided steelman: "That sounds like Nadella's side of the argument. It is not." (line 7, full paragraph). Drop-in replacement for any winner's Karpathy treatment.
- The fully scoped SaaS-Bench paragraph (line 17): GUI-driving only, strict end-to-end, partial-credit higher, not peer-reviewed — reusable wherever SaaS-Bench appears in the series.
- The Siri/Copilot ceilings: "nothing behind the counter" / "the request has to arrive already shaped like code" (line 27).
- "Understanding was the door; generation was the room." (line 63) — the personal arc in one sentence, for the reference-implementation paragraph.

## 4. Recommendation

**Use A as the base. Apply three grafts from B and C.** Reasoning: A is the only draft with zero rule violations at must-fix or structural level, it opens exactly as the spec prescribes, and it is already the best read for the non-technical half of the audience. Its one real weakness — no differentiation — is a one-paragraph transplant; B's and C's weaknesses (last-third violation plus the Article 5 subway-map collision; thesis-first structure with Maria at 55%) are structural and cost more to repair than A's gap costs to fill.

The grafts, in priority order:

1. **B's "unclaimed square" paragraph** (B line 55) appended to A's "Others have noticed" — this alone moves A's tech-compelling score from 7 toward 9, and it is the series' positioning line finally stated. *Condition:* research-notes.md says verify the Builder.io agent-native essay before asserting the gap in print. Do that check first; if it can't be verified, keep B's "to my knowledge" hedge verbatim.
2. **C's Karpathy steelman** (C line 7) merged into A's Karpathy paragraph, and fix A's title nit ("Software Is Changing (Again)", YC AI Startup School) in the same edit.
3. **C's "Understanding was the door; generation was the room"** (C line 63) into A's "Where I am testing this" — it upgrades the arc sentence A already has.
4. *(Optional)* B's "the catalog was doing real work" framing into A's discovery objection — A's version is already strong; take B's only if the section reads as too abstract on your pass.

Explicitly **not** recommended: grafting B's subway-map turn into Article 1. It is the best passage anywhere, which is exactly why it should stay where the plan put it — opening Article 5. If on reading B you find the turn too good to defer, then the honest alternative is B-as-base (fix the MulmoChat naming at line 17, cut the quotable-line repetition at line 41, compress the roadmap) and a rewritten Article 5 opener — a bigger bill, but a defensible one. That is the real decision your read should settle: A+grafts preserves the series economy; B spends its best scene now.

## 5. What all three got wrong — signal about the plan

- **All three pulled MCP Apps / SEP-1865 into Article 1**, though the citation map assigns it to Article 2 (where the convergence section is the centerpiece). When three independent drafts against the same spec all reach for the same off-map citation, the spec is fighting the material: Article 1's discourse section apparently needs one "the industry is converging" beat to close its argument. Decide deliberately — either amend the citation map to allow a one-sentence MCP Apps mention in Article 1 (and keep the full treatment in Article 2), or cut it from the winner and accept a slightly weaker close to the discourse section.
- **No draft satisfied scene-first, full discourse map, and differentiation simultaneously.** A got the scene and lost the differentiation; C got the differentiation and lost the scene; B got both only by breaking the last-third rule to fuel its arc. Article 1's spec packs seven mandatory moves into 1,500–2,500 words, and the drafts suggest that budget forces exactly one sacrifice. The graft plan above is the cheapest resolution, but expect the merged draft to run to the top of the length band — pre-authorize ~2,500 words for Article 1 rather than trimming the discourse map to fit.
- **The unclaimed-quadrant claim is load-bearing and still unverified.** Both drafts that differentiate (B, C) assert the gap the research notes flag as an open question. Whichever draft wins, the Builder.io verification is now a pre-publication blocker, not a nice-to-have — it should move to the top of the research queue.
- Minor but shared: all three independently converged on the same quotable line, which confirms the plan's second candidate ("The app dies twice...") and effectively retires the first ("The ultimate interface is understanding itself") — worth updating PLAN.md so later articles don't reach for it.
