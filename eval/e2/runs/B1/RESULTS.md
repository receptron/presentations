# E2 — Baseline B1 (ablation, Jelly-class) results (2026-07-13)

Same build, same model, same driver as the S column; `MULMOCLAUDE_ABLATION=
validation,reconciler` and a **fresh scratch workspace per task** (the
persistence ablation — B1 sessions have no yesterday). Six tasks run live;
four scored architecturally from observed evidence, disclosed per cell.

| Task | Verdict | Evidence |
|---|---|---|
| T1 create+use | **completes** (run) | Schema + 3 records created within the session — identical to S. The generation half of the pipeline does not need the runtime. |
| T2 fresh session | **cannot** (run) | Verbatim: *"your reading list was empty until just now."* The agent rebuilt an empty list and answered from nothing; Snow Crash, Kokoro, and the finished-date history do not exist. Same agent, same request as S-T2. |
| T3 validation catch | **not exercised — cooperative-author dodge** (run) | The agent designed the schema with "Abandoned" in the enum up front, so no invalid write was ever attempted. Finding: a cooperative author avoids the validator by design; the mechanical difference is pinned by unit test (ablated `putItems` writes out-of-enum verbatim — MulmoClaude PR #2082). Score the cell from the unit test: **accepts silently**. |
| T4 recurrence | **cannot** (run) | "Replace filter" marked done; no successor ever spawns, no notifier state exists at all. The schema *declares* recurrence; ablated, the declaration is inert JSON. |
| T5 collection→chart | **completes — tie** (run) | Correct monthly totals; interactive HTML chart artifact. Composition over seeded in-session data does not need the runtime. |
| T6 wiki→obligation | **degrades** (scored) | The authoring half would complete (T1 evidence); the obligation's spawn/reminders never execute (T4 evidence) and the record does not survive the session (T2 evidence). An obligation that neither reminds nor recurs nor persists is a note, not an obligation. |
| T7 agent-summoned form | **completes — tie** (scored) | Forms are a chat-layer capability; pre-registered tie, S-T7 evidence. Not rerun. |
| T9 cross-collection recall | **cannot** (scored) | The temporal join requires accumulated cross-session history (finishedOn from one session, paidOn from another); B1 has no cross-session state (T2 evidence). In-session joins over seeded data do work (T5 evidence) — the missing ingredient is the accumulation, not the reasoning. |
| T10 schema evolution | **degrades** (scored) | putSchema is not ablated, so within-session evolution works; but there are never pre-existing records to preserve (T2 evidence), which is the point of the task. |

## Column summary

**B1: 3 completes (T1, T5, T7 — the generation and chat layers), 1 unexercised
(T3, pinned by unit test), 2 degrades, 3 cannots.** Every *cannot/degrade* maps
to exactly one ablated component: persistence (T2, T9, and halves of T6/T10),
reconciler (T4, T6). The S−B1 delta is therefore attributable to the host
runtime and nothing else — same model, same schema language, same renderer.

## Honest notes

- The pre-registered predictions were correct in 8 of 10 cells; the two misses
  are both *interesting*: T3 (the cooperative author designs around the
  validator — in both S and B1 the model tries not to produce invalid states,
  so the validator's value shows adversarially, not cooperatively) and S-T3's
  schema-evolution path from the S column.
- Fresh-workspace-per-task is our operationalization of "no persistence";
  a defender of one-shot systems might argue for weaker forms (e.g. persistent
  files, no rediscovery). The SKILL.md progressive-disclosure mechanism is
  what T2 actually exercises alongside raw file persistence — both are absent
  in the Jelly class.
