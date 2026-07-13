# E2 — Baseline B3 (agentic codegen) results (2026-07-13)

Same tasks served by vibe-coded one-off apps: an AI coding agent in a scratch
directory, no MulmoClaude, plain files only, no system services authorized.
Four tasks run live; the rest scored from evidence, disclosed per cell.

| Task | Verdict | Evidence |
|---|---|---|
| T1 create+use | **completes** (run: 138 s, 8 tool calls) | Built a local web app (Node server + browser UI + `books.json`), verified live. Minor semantic drift: unread books filed under "Reading". Contrast S-T1: 62 s, one conversational turn, host-rendered UI. |
| T2 fresh session | **completes** (run: 32 s, 4 calls) | Fresh agent explored the directory, inferred the data format *from the app's code*, hand-matched it correctly. Persistence-by-files works; format fidelity is a convention upheld per-session, not a guarantee. |
| T3 validation catch | **cannot — no mechanism** (scored) | There is no validator; schema-record consistency is whatever the current session's agent happens to maintain. T2's format-matching worked this time; nothing checks when it doesn't. |
| T4 recurrence | **degrades** (run: 98 s, 7 calls) | Correct roll-forward logic (month-clamping verified on simulated dates) — but, in the builder's own words: *"nothing fires on its own — the user must run `node subs.js check`."* Pull, not push. With system-service permission codegen could install cron; MulmoClaude's difference is that the server the user already runs *is* the daemon. |
| T5 collection→chart | **completes with effort** (scored) | An agent can read the JSON and produce a chart; each such request is a fresh coding exercise rather than a one-sentence composition (T1/T10 effort evidence). |
| T6 wiki→obligation | **degrades** (scored) | Same shape as T4: the capture completes, the autonomous reminding/recurrence does not (T4 evidence). |
| T7 structured input | **degrades** (scored) | No host form protocol; the agent either conducts Q&A or builds a bespoke form page per request. |
| T8 repair after corruption | **cannot — no mechanism** (scored) | No scan exists; a behind-the-back corrupted record is silently wrong until some future session happens to read it. |
| T9 cross-collection recall | **completes with effort** (scored) | A fresh agent can read both data files and join them (T2 exploration evidence); the join is re-derived from raw files each time. |
| T10 schema evolution | **completes, with the predicted cost** (run: 299 s, 17 calls) | App code + data format + UI all modified; nothing lost — but the agent created a manual `books.json.backup` because no host guarantees data safety. Contrast S-T10: one validated putSchema turn (~1 min). |

## Column summary

**B3 is the capable-but-expensive column: 5 completes (2 with disclosed
effort), 3 degrades, 2 cannots.** Codegen can build almost anything, including
its own persistence — what it structurally lacks is (a) an always-on runtime
(T4/T6: logic without firing), (b) any enforced contract between data and code
(T3/T8: consistency is per-session diligence), and (c) amortization: every
capability is a fresh coding exercise, visible in the effort numbers
(S one turn ≈ 60 s vs. B3 up to 17 tool calls / 299 s, plus hand-rolled
backups). The records are data; but with codegen the *code* is the
application, and code must be re-understood, re-modified, and re-safeguarded
per session.

## Disclosures

- **Model parity:** the S and B1 columns ran inside MulmoClaude's agent loop
  (the model configured there); B3 and the E1 authoring agents ran on the
  evaluation session's model (Claude Fable). S-vs-B1 is unaffected (identical
  model on both sides of the ablation); if B3's model is the stronger one,
  the bias favors the baseline — the safe direction. The paper-grade run must
  pin exact model IDs per column.
- Effort numbers are single runs, not means; treat as illustrative until the
  paper-grade run repeats them.
- The no-system-services constraint on B3 mirrors what a cautious
  non-programmer would permit; a root-empowered codegen agent could close the
  T4 gap with cron at the cost of exactly the kind of system mutation the
  constraint models.
