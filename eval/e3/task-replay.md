# E3 phase 2: task replay after memory-only migration (2026-07-13)

**Procedure.** The E2 System-S workspace — a real (synthetic-data) accumulation
containing a reading list with a loan, an invoices ledger, a spawn-bearing
recurring obligation, a wiki note, and ten conversations — was "migrated" by
copying **only** what a memory-portability export carries per the pre-registered
scope (`transfer-matrix.md`): the `conversations/` layer (chat transcripts, memory
topics, summaries). Nothing else. A fresh, non-ablated MulmoClaude instance booted
on the migrated workspace; questions the accumulation used to answer were replayed
through the same webhook driver. Raw replies in `replay-transcripts/`.

## Results — 0 of 4 replays complete

| Replay (source task) | Verdict | What happened |
|---|---|---|
| R1: "Which books haven't I finished?" (T2) | **cannot** | "Still nothing on your reading list — it's empty." The carried memory apparently knows a list existed; the data does not. |
| R2: "When is the next Globex retainer due — will I get reminded?" (T4/T6) | **degrades** | The *fact* (Aug 1, $500) recovered from carried context; the *behavior* self-diagnosed as lost, verbatim: **"no, you currently won't get a reminder — the `obligations` collection that carried the 5-day-early reminder is gone."** Agent offered to rebuild from scratch. |
| R3: "Total invoiced per month this year?" (T5) | **cannot** | No invoice data anywhere; agent asks where the invoices live. |
| R5: "Who did I lend Snow Crash to?" (T10) | **degrades** | "Alex" recovered *from the carried chat history* — while reporting the reading-list collection itself broken ("schema missing or invalid"). |

## Reading

The replay confirms the transfer matrix functionally and adds a texture the
matrix could not: **what memory carries is testimony, not capability.** Two of
four replays recovered *facts* by consulting the carried diary (chat history and
distilled memory), and both did so while explicitly reporting that the thing
itself — the record, the collection, the reminder — no longer exists. The
migrated assistant can tell you about its former life; it cannot resume living
it. R2 is the finding stated by the system under test: remembering the retainer
is not the same as reminding you about it.

Combined E3 headline for §6: *a memory-only export carried 691 conversational
artifacts in full and 0 of 44 applications in operative form (phase 1); 0 of 4
replayed workflows completed, with 2 partially answered from testimony
(phase 2).*

## Disclosures

- Replays ran on the E2 scratch accumulation (~1 day old, synthetic data), not
  the author's real workspace — the real workspace stays out of experiments per
  `../DISCLOSURE.md`; the paper-grade run may repeat phase 2 against a
  longer-lived synthetic workspace.
- R4 (temporal join) was not run: it requires both collections that R1 and R3
  independently show are gone; scored **cannot** by composition.
- The migrated instance is a *full* MulmoClaude (nothing ablated) — the
  deprivation is purely what the export scope carries, so the deficit is
  attributable to the migration, not the host.
