# E2 — Baseline B2 (hosted assistant with memory) — ANALYTICAL scoring (2026-07-13)

**Method disclosure, up front:** unlike S/B1/B3, this column was **not run**. It is
scored from the documented, publicly observable capabilities of hosted
assistants-with-memory (ChatGPT-class: persistent memory, scheduled tasks,
canvas/apps surfaces) as of mid-2026, per the author's decision to score B2
analytically rather than spend operator hours. Cells are therefore judgments, not
observations; the feature set moves quickly and a paper-grade run should either
observe a real product or re-verify these judgments near submission.

Framing: B2 is the *accumulation-without-ownership* column. Its task-table scores
are middling, but its defining property is orthogonal to this table — the
accumulation lives on the vendor's premises, which is what E3 measures.

| Task | Verdict | Basis |
|---|---|---|
| T1 create+use | **degrades** | Can track a list conversationally and recite/table it on demand; no persistent, data-bound application artifact — the "app" is re-derived from context each time. |
| T2 fresh session | **degrades** | Memory features carry distilled facts/preferences across sessions, not guaranteed record-level fidelity; recall of a full list with per-item state is best-effort. |
| T3 validation catch | **cannot — no mechanism** | No schema exists; nothing enforces structure on remembered data. |
| T4 recurrence | **degrades** | Scheduled-task features can fire recurring reminders; no linkage to a record whose completion rolls state forward — reminder without ledger. |
| T5 data→chart | **degrades** | Charts from in-conversation data are routine; charting *accumulated* data depends on memory recall or the user re-supplying it. |
| T6 note→obligation | **degrades** | A prior conversation may be surfaced by memory; the captured obligation is a reminder plus prose, not a record with executable recurrence semantics. |
| T7 structured input | **degrades** | Extraction happens through conversational Q&A; no user-facing agent-summoned form contract. |
| T8 repair after corruption | **n/a — by construction** | No user-visible record store exists to corrupt behind the system's back; discussed, not counted (mirrors the B1 protocol note). |
| T9 cross-collection recall | **degrades** | Cross-session temporal joins depend on memory retrieval quality; possible, unreliable, unauditable. |
| T10 schema evolution | **degrades** | "Add a field" reduces to "also remember X"; nothing structured exists to evolve, and no guarantee protects prior data. |

**Column summary: 0 completes, 8 degrades, 1 cannot, 1 n/a.** The consistent
shape: the hosted assistant *approximates* every behavior conversationally and
*guarantees* none of them structurally — every capability is a best-effort
re-derivation from remembered context. Where B1 lost the runtime and B3 lacks a
host, B2 lacks *legible, owned structure*: there is no schema, no record, no file
the user (or the assistant) can point to.

Fairness notes: (a) hosted vendors are actively building structured-memory and
app surfaces (Apps SDK-class); several "degrades" cells may become "completes"
within product cycles — which sharpens rather than weakens the paper's point,
because every such improvement deepens the accumulation on the vendor's premises
(§3). (b) This column would benefit most from observation; it is the least
certain of the four.
