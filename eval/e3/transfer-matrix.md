# E3 phase 1: the transfer matrix (2026-07-13)

**Question.** If the owner of this workspace left via a memory-portability protocol,
what would they carry and what would they leave behind?

**Subject.** The author's production MulmoClaude workspace, nurtured over several
weeks of daily use (disclosed dogfooding data). Counts from `inventory.sh` — the
coding scheme is the workspace's own directory layout; aggregate counts only, no
record contents. Disclosure policy: see `eval/DISCLOSURE.md`.

**Export scope definition (pre-registered).** "Memory export" = what Portable Agent
Memory-class protocols (arXiv 2605.11032; SAMEP 2507.10562) transfer: conversational
memory and distilled agent context — i.e., conversation history and consolidated
facts/preferences. It does not include application definitions, executable
semantics, or host state; where content *could* be serialized into memory text but
would cease to function, we code **degraded**, not carried.

**Coding.** carried = arrives in operative form · degraded = content survives as
text, function/semantics lost · lost = does not ride the export at all.

## The matrix

| Artifact type | Count | Verdict | Rationale |
|---|---:|---|---|
| Memory topic files | 216 | **carried** | This is precisely what memory protocols move. |
| Chat session transcripts | 276 | **carried** | Conversation history is in scope; session metadata (bookmarks, read state) is not — minor degradation noted. |
| Conversation summaries | 199 | **carried** | Distilled context; in scope. |
| Wiki pages | 153 | **degraded** | Markdown content could ride as documents; the `[[link]]` graph resolution, host rendering, lint tooling, and page-addressed CRUD do not. |
| Wiki snapshot history | 247 snapshots / 79 pages | **lost** | Attributed version history is host state; no memory protocol carries it. |
| Collection records | 1,228 | **degraded** | Field values could be serialized into memory text, but they cease to be records: no schema binding, no validation, no views, no reconciler. Recoverable as prose, inoperative as data. |
| Collection schemas (the applications) | 43 | **lost** | Application definitions are not memory. The 17-type field system, completion/trigger/spawn declarations, view selections — none is expressible in a memory export. |
| SKILL.md operating manuals | 43 | **degraded** | Prose could ride as text; the function — progressive-disclosure invocation binding future agent sessions to the collection — requires the skills mechanism. |
| Custom views (model-authored code) | 34 files | **lost** | Sandboxed application code; out of scope for any memory protocol. |
| Scheduler / automation entries | 88 | **lost** | Host-executed behavior. |
| Reminder / recurrence runtime state | 2 bell files + per-record trigger state | **lost** | The reconciler's due/spawn state is meaningful only to the host that executes it. |
| Feed definitions + ingest state | ~8 + 4 | **lost** | Declarative retrievers executed by the host. |
| Attachments | 51 | **lost** | Files referenced by records; memory protocols do not carry binary stores. |
| Generated artifacts (charts, docs, images) | 1,536 | **lost** | Outputs living in the workspace, addressed by conversations that assume their paths. |

## Reading the matrix

**By artifact count** (a deliberately crude view — no cross-type weighting):
carried 691 / degraded 1,458 / lost ~1,990. But the honest headline is functional,
not proportional:

- **0 of 43 applications** survive in executable form.
- **0 of 1,228 records** remain operative data (all 1,228 recoverable as text at
  best).
- **0 of 88 automations** and none of the recurrence/reminder behavior survive.
- What survives fully — 691 conversational artifacts — is exactly the layer the
  assistant's *conversations* live in, and none of the layers its *applications*
  live in.

This is the paper's §3.2 claim, now as data: a memory export moves the diary and
leaves the workshop. The accumulation is more than the memory — in this workspace,
the majority of operative state (by any coding) sits in layers no memory protocol
addresses.

**Fairness notes.** (1) The coding is generous to portability where possible:
transcripts and summaries are coded fully carried even though session metadata is
lost. (2) A portability advocate could respond that schemas and views are "just
files" that could be copied alongside the export — which is precisely the paper's
point: once the export must include applications, executable semantics, and host
state to be adequate, it has become workspace portability, i.e., local-first
ownership of the whole environment. (3) Wiki pages arguably deserve "carried" under
a generous document-export reading; moving them to carried changes the artifact
tallies but none of the functional zeros.

## Phase 2 (pending)

Task replay: re-run the E2 task suite against a memory-only migrated target and
report per-task completion — the functional denominator, defined before the
experiment. Blocked on the E2 task suite.
