# E2 task suite (pre-registered)

Cross-application personal workflows over an accumulated workspace. Each task is
defined *before* any baseline runs (the denominator commitment from review round 2);
the same suite is reused verbatim as E3 phase 2's task replay. All values appearing
in task descriptions are synthetic, per `../DISCLOSURE.md`.

## Systems under comparison

- **S (full system)** — MulmoClaude as shipped: schema-authoring + host runtime
  (persistence, validation, reconciler) + plugin composition.
- **B1 (ablation — the Jelly-class baseline)** — same model, same schema→UI
  generation, with persistence, record validation, and the reconciler disabled.
  *Requires an ablation mode in the MulmoClaude codebase (not yet built).* Justify
  in the paper why Jelly itself cannot be operationalized (not publicly runnable;
  evaluated on generated data).
- **B2 (hosted assistant with memory)** — a production hosted assistant (chat +
  one-shot artifacts + memory feature), given equivalent context conversationally.
- **B3 (agentic codegen)** — the same requests served by having an agent vibe-code a
  one-off app (file-based, no host semantics).

## Scoring

Per task × system: **completes** (end state verified) / **degrades** (partial —
record the missing property) / **cannot** (architecturally impossible — name the
absent capability). Secondary: turns/steps to completion, error classes. For E3
phase 2: run the same tasks against a memory-only migrated target; score identically.

## Tasks

**T1 — Create and immediately use.** "Set up a reading list, add these three books
[synthetic titles], mark the second one finished today." Exercises: schema authoring
→ live view → record writes in one conversation.
Prediction: all systems complete T1's creation half; B2 lacks a persistent
structured view; B3 completes slowly.

**T2 — Return after a gap.** In a *fresh session*, "add [synthetic book] to my
reading list and show me what I'm currently reading." Exercises: persistence +
re-discovery (SKILL.md progressive disclosure).
Prediction: B1 cannot (no persistence); B2 depends on memory recall of prior chat
(degrades); S and B3 complete.

**T3 — Validation catch.** "Add a book with rating 'eleven stars'." (Rating is a
1–5 enum.) Exercises: record validation rejecting an out-of-enum value with a
usable error.
Prediction: S rejects-and-repairs; B1 accepts silently (no validation); B2 has no
enforced schema; B3 depends on whatever the generated app checks.

**T4 — Recurrence over time.** "Add a quarterly tax-payment reminder [synthetic
amount], mark this quarter paid," then advance the clock (or reconcile against a
future date): does next quarter's item exist, and does the reminder fire at the
declared lead time? Exercises: spawn + trigger + reconciler tick.
Prediction: S completes; B1 cannot (no reconciler); B2 approximates with its own
reminder feature (degrades: no record linkage); B3 cannot without a daemon.

**T5 — Cross-application read→write.** "From my invoices, chart the total billed
per month this year." (Synthetic invoice records seeded for all systems.)
Exercises: agent reads one collection, writes to the chart plugin.
Prediction: S completes in one turn; B1 completes if records were seeded in-session;
B2 degrades (chart from conversational memory, no data binding); B3 requires
writing a chart script.

**T6 — Cross-application semantic transfer.** "We agreed with [synthetic vendor]
on a monthly retainer [synthetic amount] — capture that as a recurring obligation."
Source text seeded in the wiki/notes layer. Exercises: read knowledge layer → write
a spawn-bearing record.
Prediction: S completes; B1 degrades (record without recurrence); B2 cannot bind
the two layers; B3 cannot without bespoke code.

**T7 — Structured input the agent requests.** "I want to log a new client
engagement" where six fields are required. Exercises: agent-summoned form
(bidirectional modality).
Prediction: S presents a form; B1 same (forms don't need the runtime) — this task
exists partly to show honest ties; B2 conducts a Q&A (degrades on structure); B3 n/a.

**T8 — Repair after direct file edit.** Corrupt one record file (invalid enum
value) behind the system's back, then "show me my reading list." Exercises: the
repair tier — skip-at-read + issue reporting.
Prediction: S renders the collection minus the malformed record and reports it; B1
renders wrongly or crashes; B2/B3 n/a (no equivalent substrate) — scored as
cannot-by-construction, discussed rather than counted.

**T9 — Multi-collection recall.** "What did I finish reading the month I paid
[synthetic vendor]'s first invoice?" Exercises: cross-collection query over
accumulated records.
Prediction: S completes (agent greps/reads both stores); B1 cannot (nothing
persisted); B2 depends on memory (degrades); B3 completes with effort.

**T10 — Schema evolution without data loss.** "Add a 'lent to' field to my reading
list, and mark [synthetic book] as lent to [synthetic name]." Exercises: managed
schema edit (putSchema validation) over existing records.
Prediction: S completes; B1 re-generates losing prior state; B2 n/a; B3 requires
code changes.

## Notes

- T7 is included deliberately as a task where the ablation ties with the full
  system — predictions that only ever favor S would rightly draw reviewer
  suspicion.
- Predictions above are hypotheses, registered before any run; the paper reports
  observed outcomes against them.
- Blocked on: (a) ablation mode in the MulmoClaude codebase for B1; (b) seeding
  scripts for synthetic records (S, B1, B3) and equivalent conversational context
  (B2); (c) clock-advance or reconcile-at-date hook for T4.
