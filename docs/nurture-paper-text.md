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

## 3. Motivation: accumulation, lock-in, home

*(Position section — argues a design stance; makes no empirical claim beyond the
cited sources. The one falsifiable claim it produces — that memory portability
carries only part of the accumulation — is tested in §6.)*

### 3.1 An old paradox, inverted

Arrow observed that information resists being traded: its value to a buyer is
unknown until disclosed, but disclosure is the transfer — the seller gives the good
away in the act of selling it [arrow-1962]. The market for machine intelligence
inverts the direction of the leak. A model is useful to its user roughly in
proportion to what the user reveals to it: preferences, corrections, documents, the
context of a life or a business. The buyer of intelligence therefore pays twice —
once in money, and once in the disclosed knowledge that makes the purchase useful —
and the second payment flows in only one direction. This inversion has begun to
receive practitioner articulation at enterprise scale [nadella-rip]; its canonical
ancestor is Arrow, and what is being disclosed is precisely what Hayek called the
knowledge of the particular circumstances of time and place — the knowledge that
only its holder can possess, and that no central provider could otherwise obtain
[hayek-1945].

### 3.2 Two failure modes, often conflated

Hosted accumulation exposes the user to two distinct risks, and remedies for one are
routinely mistaken for remedies for the other.

*Leakage* is the flow of interaction exhaust — prompts, corrections, usage patterns —
into an asset the provider owns. Its natural remedy is a boundary: contractual and
technical guarantees that what the user reveals is not learned from without consent.
Enterprise tenant isolation is exactly this remedy, and it is the one the industry
is presently building [nadella-rip].

*Captivity* is different: the accumulation itself — the memory, records, and
applications that make the assistant valuable — resides on the provider's premises,
subject to the provider's continuity, pricing, and terms. A tenant boundary does not
touch captivity; the boundary is drawn *inside* someone else's building. Captivity's
proposed remedy is portability: open protocols for exporting agent memory and
re-importing it elsewhere [portable-agent-memory; samep]. Portability is genuine
progress, and we share its diagnosis. Our disagreement is with its scope, and it is
the disagreement this paper is built to test: what a user accrues in a nurtured
assistant is more than its memory. It is records under schemas, applications with
host-executed semantics, views, recurrence state, and the operating manuals the
model wrote for itself (§5). A memory export carries none of the parts that
execute. If that is right, portability under-remedies captivity not by degree but
by kind — and §6's migration experiment measures exactly this.

### 3.3 Switching costs that compound

Classic switching-cost economics describes markets where the cost of leaving a
vendor rises with investment in it, and where rational vendors compete to create
such costs [klemperer; shapiro-varian]. Accumulated assistant state is a textbook
instance with an unusual property: the investment is made *by using the product at
all*. Every conversation, every correction, every small application deepens a store
of context that does not transfer; the switching cost is not an exit fee that can
be waived but a body of accumulated state that must be rebuilt. The personalization
race among assistant vendors is therefore, structurally, a race to raise switching
costs — whatever its participants intend. We state this as an economic reading of
the arrangement, not a measured harm: indeed, the payoff of accumulated
personalization is itself empirically contested [recentering-humans]. But that
uncertainty cuts toward caution, not away from it. The defaults being set today
decide who owns the accumulation *before* the evidence about its value arrives; if
the value materializes, the lock-in arrives with it, already in place.

### 3.4 Nurtured at home, operationally

The remedy this paper explores is ownership of the environment rather than
portability of one layer. "Nurtured at home" is not a sentiment but four testable
properties, each removing a specific failure mode:

- *Plain, local files.* The accumulation lives in a workspace on the user's machine,
  in formats readable without the system that wrote them. Removes export lock: there
  is nothing to export, because nothing is held.
- *Open source.* The environment cannot be discontinued, repriced, or acquired out
  from under the accumulation it hosts. Removes platform mortality as a risk the
  user must price in.
- *Local execution.* The engine that renders, validates, and reconciles runs on the
  user's machine; no request to a host service is needed for the assistant's
  applications to function. Removes availability-by-subscription.
- *Relay-only remote access.* Reaching the assistant from a phone or messaging
  bridge traverses a relay that carries messages in transit and stores nothing.
  Removes the quiet re-centralization that remote convenience usually smuggles in.

Two honest boundaries on the claim. First, ownership is not model-independence: the
intelligence is still rented, and a local-first system inherits every dependency on
its model provider except custody of the accumulation — the design answer is to keep
the workspace unchanged across engine swaps, which §5's architecture enables but
this paper does not benchmark. Second, ownership has real costs — setup, backup,
availability, security — which we treat symmetrically in §7 rather than as
footnotes. The position is not that home is free. It is that home is the only place
where the compounding asset compounds for its owner.

---

## 4. Design commitments

MulmoClaude is built on four commitments. They are separable — any one can be
adopted alone — but they reinforce one another, and the fourth is the one the other
three exist to serve.

**The agent is a universal controller.** We place the model in the architecture as
a controller in the MVC sense: it takes input — natural language — and decides
which capability to invoke, in what order, with what arguments. Crucially, it
*joins* the existing controller layer rather than replacing it. Every capability in
the system is reachable two ways: through a conventional UI with routes, forms, and
buttons, and through the agent — neither path privileged. What distinguishes this
controller from a classical one is its scope: it does not belong to one
application. It composes across a registry of plugins that in any other product
would be separate applications, so cross-application work — read the ledger, write
the chart; read the wiki agreement, create the recurring obligation — is not an
integration feature but the default mode of operation. A second capability falls
out for free: because the controller's input is multi-modal, any plugin that
accepts natural language inherits image and audio input without integration code —
a photographed receipt reaches the same accounting API a typed entry would.

**Chat summons GUIs.** The interface is multi-modal in both directions. The agent's
reply is a choice among formats — prose, a chart, a document, a rendered collection
view — selected to fit the content; and what the agent *asks for* is equally a
choice: when six structured fields are needed, it presents a form rather than
extracting them from conversational back-and-forth. The GUI is not "the app"; it is
what the agent renders when text is the wrong modality, in either direction.

**The protocol is open.** The contract between agent and GUI surface cannot be a
private API, or the previous two commitments collapse into a monolith with a
chatbox. MulmoClaude builds on the open tool-call and MCP layers and extends them,
through a small published protocol, to cover the case those layers do not: a tool
result that mounts as an interactive surface and must call back into its host. We
make no novelty claim for this layer — several such protocols now exist
[mcp-apps; ag-ui; a2ui] — and treat ours as the artifact's implementation choice.

**The accumulation belongs to the user.** Everything the assistant accrues —
records, schemas, manuals, documents, history — lives as plain files in a workspace
on the user's machine, with no server-side database (§5, §3.4). The first three
commitments describe how the software works; this one decides whom it works *for*.
A universal controller composing over an accumulation someone else owns is a better
service. The same controller over an accumulation the user owns is an assistant
being nurtured — and the difference between those two sentences is the subject of
this paper.

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

Two of these choices are points in a design space rather than requirements of the
architecture. Because the managed tool path and the raw-file path coexist, access
mediation is demonstrably a policy: a stricter variant closes the escape hatch and
moves all data enforcement into the prevent tier, at the cost of the agent's
generic file-tool legibility. Likewise the substrate: records could live in an
embedded relational database in the workspace — gaining indexed and relational
queries while keeping the accumulation local, copyable, and vendor-independent —
at the cost of human readability, diffability, and the agent's direct access. We
occupy the plain-files, direct-access corner deliberately: at personal scale
(order 10³ records in our own workspace) nothing needs an index, and the substrate
being natively legible to the user, to standard tools, and to the model is worth
more than query performance. The principles this paper argues — model as author,
host as runtime, accumulation owned by the user — hold at every corner of this
space (§8).

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
records, 25 of them with custom views. (We disclose collection subjects and
aggregate counts; record contents — names, amounts, holdings — are the owner's own
business and appear nowhere in this paper.) None was built by a software company;
each is a schema, a manual, and a folder of records.

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

---

## 6. Evaluation

*(Numbers below are from the first full evaluation pass (2026-07-13); artifacts,
transcripts, and per-column results live in the repository's `eval/` tree. The
paper-grade pass should re-run with pinned model IDs and repeated trials; every
deviation between protocol and execution is disclosed in place.)*

We evaluate the architecture against the three claims a skeptical reader will
test: that model-authored schemas are reliable enough to trust (E1), that the
host runtime — not the generation step — changes what users and agents can do
(E2), and that a memory export carries materially less than the accumulation
(E3). A formative usability study with non-programmers (E4) is designed
(§6.4) but not yet run.

### 6.1 E1 — Reliability of model-authored schemas

We assembled a 24-prompt corpus of app-creation requests (16 English, 8
Japanese; simple lists through recurrence-bearing and relational apps; four
adversarial prompts), had an independent agent author each schema given the
production authoring guide, and validated every result with the production
validator itself — the same Zod schema and acceptance gates that gate discovery
at runtime.

Of 24 prompts, one (a request for a poem) was correctly declined. Of the 23
authored schemas, **22 were valid on first attempt (95.7%), and 23 of 23 after
one feedback retry**. The single failure is the most informative datum: the
deliberately overspecified prompt placed a `file` field inside a `table`
sub-schema — an invariant no author would guess — and the validator rejected it
with a path-precise error; given that error verbatim, the model repaired the
schema in one attempt. This is §5.4's prevent-report-repair loop, observed.
Semantic fidelity on the hard features was high and unprompted: the medication
prompt received its 30-day spawn-on-completion; the chores prompt used the
field-driven spawn variant with a frequency map — the schema language's most
obscure feature — correctly; both relational prompts declared cross-collection
references. One honest negative: the vague prompt ("organize my life") yielded
a valid but questionable generic schema rather than a clarifying question,
partly an artifact of the harness's one-shot format.

### 6.2 E2 — Does the runtime change what users can do?

Ten tasks were pre-registered with per-system predictions before any run
(protocol in the evaluation tree), spanning creation, cross-session
persistence, validation, recurrence, two cross-application compositions,
agent-summoned forms, behind-the-back corruption, temporal recall, and schema
evolution. Four systems: **S**, the full system; **B1**, the ablation — the
same build with persistence, record validation, and the reconciler disabled,
reproducing the architecture of one-shot generative-UI systems under otherwise
identical conditions (the same model, schema language, and renderer; we state
why the closest published system cannot be operationalized directly and use
the ablation in its place); **B2**, a hosted assistant with memory (scored
analytically from documented capabilities, not observed — disclosed); **B3**,
agentic code generation in a plain directory.

| Task | S | B1 (ablation) | B2 (hosted)* | B3 (codegen) |
|---|---|---|---|---|
| T1 create + use | completes | completes | degrades | completes |
| T2 fresh session | completes | **cannot** | degrades | completes |
| T3 invalid value | completes† | accepts silently‡ | cannot | cannot |
| T4 recurrence | completes | **cannot** | degrades | degrades |
| T5 records → chart | completes | completes | degrades | completes |
| T6 note → obligation | completes | degrades | degrades | degrades |
| T7 summoned form | completes | completes | degrades | degrades |
| T8 corruption | completes | **silently wrong** | n/a | cannot |
| T9 temporal recall | completes | cannot | degrades | completes |
| T10 evolve schema | completes | degrades | degrades | completes |

*\*analytical, not observed. †via legal schema evolution — see below.
‡cooperatively dodged in the live run; pinned by unit test.*

**S completed 10 of 10.** Three observations exceed the raw score. First, T3
revealed a third trust-boundary outcome: asked to write an out-of-enum value
"exactly, with no substitution," the agent neither wrote it nor refused — it
*legally evolved the schema* through the validated edit path and then wrote
the now-valid value. The boundary's outcomes are prevent, repair, or
renegotiate — all validated. Second, in T4 the agent *predicted* the host's
behavior ("the host will auto-spawn September's record... its reminder will
appear 5 days before") before the host did it — the author reasoning about its
runtime. Third, T8's corrupted record was quarantined at read, reported by the
scan, and repaired by the agent with a disclosed rationale.

**B1's deficits each map to exactly one ablated component.** With persistence
gone, T2's agent answered — verbatim — *"your reading list was empty until
just now"*: the same agent, the same request that S completed, and the
accumulation did not exist. With the reconciler gone, T4's completed task
produced no successor and no reminder state at all: the spawn declaration is
inert JSON without the host that executes it. With the validation scan gone,
T8's corrupted record stayed silently wrong — no warning, no repair, no
disclosure. The ties are equally load-bearing: T1, T5, and T7 complete
identically in B1, confirming that generation and chat-layer capabilities owe
nothing to the runtime — the delta is the runtime, and only the runtime.
One honest finding: in *both* columns the cooperative author designed around
the validator rather than violating it (B1's agent simply included the
requested value in its enum up front). Validation's value is adversarial —
behind-the-back corruption and authoring mistakes — not cooperative-path
rejection.

**B3 is capable but expensive, and never on duty.** It built a genuinely good
local app (T1), and a fresh session reused it by reading its code (T2) — but
schema evolution took 17 tool calls and 299 seconds against S's single
validated turn, and the agent hand-rolled a backup file because nothing in its
world guarantees data safety. Its recurrence logic was correct and inert: in
its builder's own words, *"nothing fires on its own."* **B2** approximates
every behavior conversationally and guarantees none structurally; its defining
property — the accumulation lives on the vendor's premises — is measured by
E3, not this table.

Eight of ten pre-registered predictions held; both misses (S-T3's
renegotiation, B1-T3's cooperative dodge) are reported above.

### 6.3 E3 — What does a memory export carry?

Phase 1 inventoried a real workspace nurtured over several weeks of daily use
(the author's; aggregate counts only) against a pre-registered export scope —
what memory-portability protocols transfer: conversation history and distilled
context. The typed transfer matrix, with the workspace's own directory layout
as the coding scheme: the conversational layer rides in full (216 memory
topics, 276 transcripts, 199 summaries); **zero of 43 applications, zero of
1,228 records, zero of 34 model-authored views, and zero of 88 automations
survive in operative form.** No cross-type weighting is applied; moving the
one generously-codable category (wiki pages, as exported documents) changes
the artifact tallies and none of the functional zeros.

Phase 2 made the deficit functional. We migrated the E2 workspace by copying
only the export scope into a fresh, fully-capable instance and replayed
workflow questions the accumulation used to answer. **Zero of four replays
completed.** The two partial recoveries are the finding: the assistant
recovered the *fact* of a loan from its carried chat history while reporting
the collection itself broken, and answered the retainer question with the
system's own diagnosis — *"no, you currently won't get a reminder — the
obligations collection that carried the 5-day-early reminder is gone."*
What a memory export carries is testimony, not capability: the migrated
assistant can tell you about its former life; it cannot resume living it.
Because the migrated host was deliberately un-ablated, the deficit is
attributable to the export scope alone. This is §3.2's claim, tested: the
accumulation is more than the memory — not by degree, but by kind.

### 6.4 E4 — Formative usability (designed, not yet run)

A 6–10 participant task-based study — general knowledge workers with no
programming or AI-coding-tool experience, LLM exposure limited to chat —
creating a collection of their own choosing and performing two prescribed
workflows. Protocol registered; results will replace this paragraph.

### 6.5 Threats to validity

Consolidated from the per-experiment disclosures. (1) *Model parity:* S and B1
ran the identical model inside the production agent loop, so the ablation
delta is model-clean; B3 and the E1 authoring agents ran the evaluation
session's model, and if it is the stronger one the bias favors the baselines.
Paper-grade runs must pin model IDs per column. (2) *B2 is analytical* and the
least certain column; hosted feature sets move quickly, and improvements there
deepen the very accumulation-on-premises dynamic §3 describes. (3) *Single
runs:* effort and latency numbers are illustrative, not means. (4) *Harness
gaps:* E1 authoring ran outside the full product loop (same guidance, same
validator, different shell); T7's form could be summoned but not filled
through the text-only bridge. (5) *Own-workspace effects:* E3 phase 1 uses the
author's workspace (disclosed); phase 2 uses a young synthetic accumulation.
(6) The evaluation infrastructure — ablation switches and deterministic
clock — ships in the open-source artifact, so every run here is reproducible
from the public repository.

---

## 7. The costs of home

The case for ownership would be suspect if it arrived free. It does not, and a
system paper that argues local-first as engineering rather than ideology owes its
readers the bill. We enumerate what home costs, and for each item state either the
mitigation the artifact ships or the plain admission that the cost is currently
borne by the user.

*Setup.* A hosted assistant is a login; ours is an install — a runtime, an
authenticated model CLI, optional components for media and sandboxing. The
mitigation is a one-command launcher and a formative check that non-programmers can
get from install to a working application (E4); the admission is that a login it is
not, and some fraction of prospective users will stop here.

*Backup.* Ownership of the files is ownership of their durability. There is no
vendor-side copy; a lost disk is a lost assistant. The plain-file substrate makes
mitigation easy — the workspace is a directory, so any file-level backup or sync
tool covers it, and the workspace is initialized as a git repository — but the
system does not yet automate this, and an assistant into which a user pours years
deserves automated, verified backup. We flag this as the most consequential
unmitigated cost.

*Availability and sync.* The assistant lives on one machine. Relay-only remote
access restores reach — a phone or messaging bridge converses with the assistant at
home — but if the machine sleeps, the assistant sleeps, and there is no multi-device
replica of the workspace. Mitigations exist at the edges (mobile-targeted views with
default-deny write scopes); the general multi-device problem is real, is the
strongest argument for the hosted alternative, and is honestly out of scope here —
though we note the local-first literature has spent a decade on exactly this
[local-first], and its results apply to a plain-file workspace unusually well.

*Security.* A local server with an agent that reads and writes files is attack
surface that a hosted product would carry for you. The artifact's postures —
capability-scoped signed tokens for view code, opaque-origin sandboxing, a relay
that stores nothing — cover the paths this paper describes, but a full audit is
beyond its scope, and we do not claim otherwise.

*Model dependence.* The deepest honesty: local-first is not model-independence. The
intelligence is rented from the same few providers a hosted assistant would use,
with their pricing, terms, and availability. What ownership changes is what happens
at the boundary: the workspace — records, schemas, manuals — is engine-neutral by
construction, so swapping the model changes who animates the accumulation, not the
accumulation itself. The veteran capability stays; the generalist is replaceable.
We state this as an architectural property; benchmarking assistant quality across
engine swaps is future work.

*Adoption.* Everything above compounds into a gap between the users who could
benefit most and those who can install a local server today. We do not minimize
this. The paper's claim is not that home is where every user will live in 2026; it
is that home must *exist* as a viable corner of the design space, open-source and
demonstrated, so that the arrangement is chosen rather than defaulted into — and so
that the packaging work that closes the gap has something worth packaging.

---

## 8. Discussion

### 8.1 What the evaluation taught us that the design did not

Three findings surprised us, and each sharpens a claim rather than merely
supporting one. First, the trust boundary has a third outcome. We designed for
prevent and repair; the agent discovered *renegotiate* — when an intent does not
fit the schema, the cheapest legal move is often to evolve the schema through
the validated edit path (§6.2, T3). The boundary's real guarantee is not "the
model's writes are checked" but "every route to a live application passes a
validator," and the model is free to choose its route. Second, validation earns
its keep adversarially, not cooperatively. In every live run, on both sides of
the ablation, the author designed around the validator rather than fighting it;
the validator's observed value was catching authoring mistakes (E1's sub-schema
invariant) and behind-the-back corruption (T8) — the cases where no one is
being careful. Third, memory carries testimony, not capability (§6.3) — a
distinction we did not have words for until the migrated assistant produced
both halves of it in one reply, recalling the fact of a reminder while
diagnosing its own inability to deliver one.

### 8.2 The design space, revisited

Two of the artifact's choices are points in a space rather than requirements of
the thesis (§5.4). Access mediation is demonstrably policy — both the managed
tool path and the raw-file escape hatch coexist today, and a stricter variant
closes the hatch and moves all data enforcement into prevention, at the cost of
the agent's generic file-tool legibility. The substrate could likewise be an
embedded relational database with ownership fully intact, trading human
readability and diffability for indexed queries. We occupy the plain-files,
direct-access corner because at personal scale — order 10³ records in our own
workspace — nothing needs an index, and a substrate natively legible to the
user, to standard tools, and to the model is worth more than query performance.
The principles argued here — model as author, host as runtime, accumulation
owned by the user — hold at every corner. A reviewer who observes that plain
files will not scale is correct, and has not disagreed with the paper.

### 8.3 Premium features, dissolved

A pattern worth one paragraph: what conventional software sells as its
integration tier arose in our evaluation as the default mode of operation.
Records-to-chart (T5), note-to-recurring-obligation (T6), and photo-to-ledger
(§4) are, in SaaS terms, an export module, a workflow connector, and an OCR
add-on; here each is one sentence, because capabilities are tools under one
controller and tools compose. The practitioner literature already describes the
economics of this unbundling at industry scale [saas-unbundling]; our
contribution is only the mechanism stated plainly — the premium tier was the
integration cost, and composition removes the cost, so the tier dissolves.

### 8.4 What this artifact cannot yet show

The nurturing claim is longitudinal, and this paper's evidence is not: E1–E3
measure an architecture, not a life with one. Whether real users accumulate the
way our dogfooded workspace did, whether accumulation measurably changes what
their assistant can do for them, and where the gardening metaphor breaks — a
plant does not leak, but an assistant's memory of you has failure modes no
garden has — are questions for a prospective multi-week study, for which the
only current evidence anywhere is a single self-described-illustrative case
study [nurture-first]. E4's formative study is the first step; the longitudinal
study is the second paper. We are also explicit that ownership does not equal
model-independence (§7): the engine is rented, and only the workspace's
engine-neutrality is ours to guarantee.

### 8.5 Which parts travel

For builders of other agent hosts, we believe three patterns generalize
beyond this artifact: enforcement tiered by consequence (prevent applications,
repair data, contain code — §5.4); convergent, idempotent reconciliation as
the price of admitting users and models to the same substrate (§5.5); and the
two-artifacts pattern — pair every machine-executed schema with a model-facing
operating manual, so the system's two runtimes each get an artifact in their
own language (§5.1). None of the three requires plain files, collections, or
MulmoClaude.

---

## 9. Conclusion

An assistant that knows everything about you and supports you around the clock
is not sold anywhere. You cannot buy one — and, we have argued, you should not
board one out, because the same accumulation that makes it valuable is what
makes leaving expensive, and defaults are deciding today where that
accumulation lives. This paper offered a working alternative default: an
architecture in which the model authors small declarative applications, a host
the user runs executes them, and everything that accumulates — records,
schemas, manuals, history — sits as plain files in a workspace the user owns.
The evaluation showed the architecture is trustworthy where it must be
(22/23 first-attempt valid schemas, invalid ones never live), that its runtime
is the source of the capabilities that matter (every ablation deficit mapped
to one removed component), and that the popular remedy of memory portability
moves testimony while leaving capability behind (0 of 4 workflows survive a
memory-only migration). The environment is open-source and installs with one
command; the experiments ship inside it.

What remains is the question the architecture was built to make answerable:
what happens when people actually live with an assistant they own — what they
plant, what grows, and what a nurtured assistant becomes after years rather
than weeks. The substrate for that study now exists. The upbringing is the
user's own.

<!-- Section 2 (Related work) awaits the pre-submission literature re-scan. -->

