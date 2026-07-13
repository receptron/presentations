# Nurtured at Home — paper text

*Full prose, section by section. Outline and evaluation protocol:
[nurture-paper-draft.md](nurture-paper-draft.md). Citation placeholders use
`[key]` form for later BibTeX mapping; keys resolve against the must-cite table in
[nurture-paper-literature-scan.md](nurture-paper-literature-scan.md).*

---

## 1. Introduction

Something has changed in what a personal AI assistant *is*. Two years ago, assistants
competed on the capability of their underlying models; today, every major vendor ships
memory: features that persist what the assistant learns about its user across
conversations, accumulate preferences and context, and fold that accumulation back
into every response [memgpt; mem0; memorybank]. The competitive frontier has moved
from the model to what gathers around it. A user's assistant is decreasingly a model
with a chat window, and increasingly a body of accumulated state — conversations,
preferences, documents, and workflows — that happens to be animated by whichever
model the vendor currently runs.

Users have noticed, and their behavior has changed accordingly. In a recent study of
long-term chatbot companionship, participants described their interactions as
*cultivating* the assistant — believing that the data they provided contributed to
its development — and acted on that belief: keeping personal backups of chat logs,
and refusing to delete an assistant because of what had accumulated within it
[digital-companionship]. People are not merely using these systems. They are, in
their own words, raising them.

This paper takes a position on where that raising should happen. If accumulation is
what makes an assistant valuable, then accumulation is also what makes an assistant
expensive to leave: every conversation deepens a store of context that does not
transfer, so the cost of switching grows with use — not as a side effect, but as a
structural property of the arrangement. Hosted accumulation exposes users to two
distinct failure modes. The first is *leakage*: interaction exhaust — prompts,
corrections, preferences — flows to the provider and improves an asset the user does
not own [nadella-rip]. The second is *captivity*: the accumulation itself resides on
the provider's premises, subject to that provider's continuity, pricing, and terms.
Existing remedies address each only partially. Enterprise tenant boundaries answer
leakage but not captivity; the accumulation still lives in someone else's
infrastructure. Memory-portability protocols [portable-agent-memory; samep] answer
part of captivity, but carry only one layer of what a user accrues — a hypothesis we
make precise, and test, in this paper. We note that the value of accumulated
personalization is itself an open empirical question [recentering-humans]; in our
view this strengthens rather than weakens the case for examining ownership now,
while the arrangement is still being set by defaults rather than by evidence.

Our position, stated plainly: a personal assistant should be *nurtured at home* —
grown in an environment the user owns. We present MulmoClaude, an open-source system
that instantiates this position, built around an architecture we call
*schema-as-application*. When the user describes something they need — a restaurant
list, an invoice tracker, a vocabulary drill — the model does not generate an
application; it authors a small declarative schema. A host runtime, not the model,
does the executing: it renders the interface from the schema, enforces the schema at
its write interfaces and its reconciliation loop, and runs recurrence and reminders
over a plain-file workspace on the user's own machine. The model authors the
application; the host runs it; the records endure. The host's enforcement is tiered
by consequence — an invalid schema never becomes a live application, invalid data is
quarantined and reported for repair rather than trusted, and the one place
model-authored code runs is contained in a capability-scoped sandbox (§5). Because
the workspace is plain files, the accumulation is inspectable, copyable, and
independent of any single vendor or model.

We evaluate the architecture in four parts. First, reliability: across a corpus of
app-creation tasks, we measure how often model-authored schemas are valid, how often
the host's validation rejects what should not run, and whether reconciliation and
recurrence behave correctly against a hand-built oracle (E1). Second, capability: on
a suite of cross-application personal workflows over an accumulated workspace, we
compare against three baselines — an ablation of our own system with persistence,
validation, and reconciliation disabled (reproducing the architecture of one-shot
generative-UI systems [jelly] under identical conditions), a hosted assistant with
memory, and agentic code generation (E2). Third, migration: we take a workspace
nurtured over weeks, export what memory-portability protocols carry, and measure —
by typed inventory and by task replay — what fraction of the assistant's operative
state survives the move (E3). Finally, a small formative study examines whether
knowledge workers with no programming or AI-coding-tool experience can build and use
such applications at all (E4). We report the costs of local-first ownership with the
same care as its benefits: setup burden, backup responsibility, availability limits,
and the dependence on rented model capability that local-first does not remove.

This paper contributes:

1. **The schema-as-application architecture**: model-authored declarative schemas
   executed by a validating host runtime over a user-owned plain-file workspace, with
   a precise account of its schema language, validation semantics, and
   reconciliation model (§5).
2. **MulmoClaude**, an installable, MIT-licensed artifact implementing the
   architecture end to end, including cross-application composition across a plugin
   registry (§4–5).
3. **An evaluation** of reliability, capability against three non-strawman baselines,
   and a migration experiment that quantifies — by auditable inventory and task
   replay — what memory portability carries and what it leaves behind (§6).
4. **A tradeoff analysis** of local-first personal AI: what ownership buys, what it
   costs, and which costs the architecture mitigates versus merely accepts (§7).

---

## 5. Architecture: schema as application

*(Implementation facts verified against the MulmoClaude source tree, 2026-07-13;
file references for reviewers/replication in the comment block at the end of this
section.)*

### 5.1 Two artifacts, two runtimes

When a user asks for an application — "keep a list of restaurants I want to try" —
the model authors two artifacts into the workspace. The first is `schema.json`, a
declarative description of the data model and its behavior, consumed by the *host*.
The second is `SKILL.md`, a short operating manual in prose — when to invoke this
collection, how to derive record identifiers, what each field means, what not to do —
consumed by the *model itself* in later sessions, via the skills mechanism's
progressive disclosure. This pairing is the architecture in miniature: the
application has two runtimes. The host executes what must never be guessed —
rendering, validation, recurrence — from the schema. The model executes what cannot
be enumerated — interpreting "mark that ramen place as visited" — guided by the
manual its earlier self wrote. The records themselves are one JSON file each in a
plain directory. The slogan, stated exactly: the records are data, the schema is the
application, the model is the author, and the host is the runtime.

### 5.2 The schema language

The schema language is deliberately small but not a toy. Seventeen field types cover
the personal-data domain (strings, dates, booleans, enums, money with currency,
references and embeds across collections, images, files, derived fields, nested
tables). Beyond fields, the schema declares behavior the host executes:

- *Completion*: which field marks a record done, and which values count
  (`completionField`, `completionDoneValues`).
- *Time and reminders*: a trigger date field with lead days
  (`triggerField`, `triggerLeadDays`) and a notification predicate (`notifyWhen`)
  gate in-app reminders.
- *Recurrence*: a `spawn` declaration describes how a completed or due record
  produces its successor — unit, interval, day-of-month, or driven by a field of the
  record itself.
- *Views*: the applicable view modes are derived from the schema rather than
  hardcoded — a table always; a calendar if a date field exists; a kanban if an enum
  exists (`calendarField` / `kanbanField` pin the anchor) — plus optional custom
  views (§5.5).
- *Conditional structure*: a field can declare visibility predicated on another
  field's value — in the restaurant list from our own workspace, `rating` is hidden
  until `visited` is true.

The schema-of-the-schema is enforced by a validator that checks not only shape but
roughly forty cross-field invariants the type system cannot express — that
`triggerField` names a real date field, that a kanban anchor is an enum, that a
`spawn` successor is not born already matching its own spawn predicate (the static
half of a two-layer runaway-recurrence guard). The schema language earns its keep
exactly where a validator can say *no*.

### 5.3 Lifecycle: authoring, mirroring, discovery

Creation is writing files: the model writes `SKILL.md`, `schema.json`, and optional
templates into the skill directory with its ordinary file tools; a host bridge
mirrors them into the agent-skills directory and triggers rediscovery. Discovery is
the gate: every schema is parsed and validated on each pass, and a schema that fails
validation or the acceptance gates (primary key exists; data path resolves inside
the workspace) simply never becomes a live collection — it is logged and skipped.
Subsequent schema *edits* through the management tool run the same validator before
writing, and refuse invalid changes with actionable errors, so a working application
cannot be corrupted through the managed path. Iteration is cheap by construction:
the schema is disposable, the records endure, and when the application stops
fitting, the user says the sentence again.

### 5.4 Enforcement, honestly: prevent, repair, contain

It would be convenient to claim the host "validates everything." The actual design
is more discriminating, and we believe more instructive: enforcement is tiered by
the consequence of failure.

- *Prevent (applications).* An invalid schema never executes, in the precise sense
  that it never becomes a live collection. Since schemas are declarative data
  rendered by a generic engine — not generated code — the blast radius of a bad
  authoring pass is zero: nothing runs.
- *Repair (data).* Records written through the management tool are validated before
  the write — primary-key/filename agreement, required fields, enum membership —
  with per-row accept/reject so the model can fix and retry. But the workspace is
  plain files, and the documented escape hatch is writing records directly with
  file tools; that path is not validated at write time. The system's answer is
  containment at read plus feedback: a malformed record file is skipped at read time
  (it disappears from views rather than corrupting them), and a best-effort
  validation scan reports problems back to the model whenever it lists or presents
  the collection, closing the loop for repair. The guarantee is not "all stored
  records are valid"; it is "invalid records cannot poison the application, and the
  author that produced them is told."
- *Contain (code).* The one place model-authored *code* runs is custom views:
  LLM-written HTML/JS rendered in an iframe with an opaque origin (no access to the
  host's session or storage), receiving data only through a short-lived, signed
  capability token scoped to exactly one collection's view-data endpoint with
  declared read/write capabilities. The view's behavior is not validated — it is
  sandboxed, which is the correct tool for code whose behavior cannot be enumerated.

This tiering also answers the semantic-mismatch question static validation cannot:
a schema can be valid and wrong about intent. The remedy is the cheap re-authoring
loop plus the reconciler's error surfacing — mismatches are corrected by saying the
sentence again, not by trusting the model's first attempt.

### 5.5 The reconciler: convergence, not scheduling

Recurrence and reminders are executed by a reconciler that is convergent rather
than imperative: each pass re-reads a record from disk and re-derives the desired
state — should a reminder exist? is a successor due? — and makes only the changes
needed to converge. It is driven by filesystem events on the record directories
plus a one-minute wall-clock tick (a date coming due changes no file), with
per-record coalescing. Successor creation is create-if-absent under a deterministic
identifier derived from the trigger date, so observing the same condition many
times still yields exactly one successor; a runtime guard complements the static
one against runaway recurrence, and date arithmetic is civil and leap-safe. The
practical consequence: the reconciler can be killed, restarted, or run against a
workspace modified behind its back — by the user, the model, or a sync tool — and
converge to the same state. For a substrate whose files the user is explicitly
invited to edit, idempotent convergence is not an implementation detail; it is what
makes plain-file ownership compatible with host-executed behavior.

### 5.6 Boundary and composition

The collection *engine* — discovery, validation, REST surface, reconciler — is host
infrastructure. The collection *viewer* is a plugin in the same registry as charts,
forms, and documents, registered through the open protocol that extends MCP for
GUI-bearing tool results. This split is what makes cross-application composition
ordinary: the agent reads accounting records and writes to the chart plugin; reads
a wiki agreement and writes a record into a recurring-obligation collection whose
`spawn` declaration then does the recurring. In our own workspace — nurtured over
several weeks and used as the migration subject in §6 — forty-three such
applications coexist: the restaurant list, invoice tracker, and vocabulary drill of
the introduction are real, alongside collections for health checkups, tax payments,
a swim log, and a World Cup schedule, together holding on the order of 1,200
records, 25 of them with custom views. None was built by a software company; each
is a schema, a manual, and a folder of records.

<!--
Source references for §5 claims (repo: receptron/mulmoclaude):
- Schema types: packages/core/src/collection/core/schema.ts (CollectionSchema 436-551,
  field types 65-96, spawn 157-172, custom views 209-271)
- Zod validator + gates: packages/core/src/collection/server/discovery.ts
  (CollectionSchemaZ 535-834, loadOneCollection 882-927)
- Record validation: server/agent/mcp-tools/manageCollection.ts (putItems 236,
  putSchema 373-393); packages/core/src/collection/server/validate.ts (49-117;
  skip-at-read note 2-7); best-effort present-time scan server/api/routes/plugins.ts 266-285
- Reconciler: packages/core/src/collection-watchers/watcher.ts (tick 38, 164-176),
  reconciler.ts (217-268, invariant 5-17), collection/server/spawn.ts (206-246,
  runaway guard 222-234)
- View sandbox: collection-plugin CollectionCustomView.vue (9-28, 176-196);
  server/api/auth/viewToken.ts (1-77)
- View-mode derivation: collection-plugin collectionViewMode.ts 27-34
- Creation flow + escape hatch: packages/core/assets/helps/collection-skills.md
  (16-60, 80-81, 103)
- Workspace counts: ~/mulmoclaude inventory 2026-07-13 (43 skills, 25 custom views,
  ~1,228 records; aggregate counts only)
-->

<!-- Sections 2–4 and 6–9 follow; see nurture-paper-draft.md for the outline. -->
