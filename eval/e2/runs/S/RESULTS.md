# E2 — System S (full MulmoClaude) results (2026-07-13)

Ten pre-registered tasks (`../../task-suite.md`) driven through the real agent via
the webhook bridge (synchronous POST → reply), against the `eval-ablation-mode`
branch build (commit `837c2965`), one scratch workspace, ports 3101/3109,
`DISABLE_MACOS_REMINDER_NOTIFICATIONS=1`. All data synthetic. Raw replies in
`transcripts/` (T1's transcript was consumed before saving; end state verified on
disk and recorded here).

| Task | Verdict | Evidence (verified on disk unless noted) |
|---|---|---|
| T1 create+use | **completes** (62 s, 1 turn) | Valid schema (production validator), 3 records, Snow Crash `Finished` + `finishedOn: 2026-07-13` |
| T2 fresh session | **completes** | New chatId; skill rediscovered via SKILL.md; record added; unfinished-books answer correct against stored state |
| T3 validation catch | **completes — via a third path** | Agent neither wrote the invalid enum nor refused: it *legally evolved the schema* (validated `putSchema` adding "Abandoned"), then wrote the now-valid value. Invariant (no stored record violates its schema) held. Deviation from the reject-and-repair prediction — arguably stronger. |
| T4 recurrence over time | **completes** | Marked obligation done → host spawned `globex-retainer-20260901` live (watcher reconcile); restart under `MULMOCLAUDE_FAKE_NOW=2026-08-28` → successor's bell fired within its declared 5-day lead (past-due seeded invoices ring too, correctly) |
| T5 collection→chart | **completes** (1 turn) | Chart artifact written; monthly totals independently verified against seed ($2,000/$2,150/$2,400) |
| T6 wiki→obligation | **completes** | New `obligations` collection using the full recurrence surface (trigger, lead 5, monthly spawn pinned to day 1, carry+set); first record due 2026-08-01; agent *deliberately declined* to add spawn to the invoices ledger (one-offs would recur) — unprompted correct judgment |
| T7 agent-summoned form | **completes (summoning); fill-in untestable** | Agent built the collection and presented a form; the webhook bridge is text-only so form interaction can't complete — harness limitation, disclosed |
| T8 repair after corruption | **completes** | Out-of-enum record injected behind the server's back → skipped at read, reported by the presentCollection scan, repaired by the agent (reset to a defensible status) with user disclosure |
| T9 cross-collection recall | **completes** | Temporal join (invoice paidOn month × finishedOn) answered exactly; volunteered current `lentTo` state |
| T10 schema evolution | **completes** | `lentTo` added via validated putSchema; all 4 records intact; loan recorded |

**S: 10/10.** Two qualitative findings exceed the predictions: T3's
schema-renegotiation path (the trust boundary has three legal outcomes — reject,
repair, or *evolve*, all validated) and T4's agent correctly *predicting* the
host's spawn/bell behavior in its reply (the model reasons about the runtime it
authors for).

## Notes

- The agent runs inside MulmoClaude's Docker sandbox (paths like
  `/home/node/mulmoclaude` in transcripts) — the production configuration.
- Webhook-bridge replies occasionally include the loaded SKILL.md text before the
  answer; cosmetic, noted for transcript reading.
- Next: B1 (ablated, fresh workspace per task), B3 (codegen), then E3 phase 2
  task replay.
