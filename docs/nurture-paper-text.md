# Nurtured at Home — paper text

<!-- Working-doc apparatus (citation-key mapping, source references,
pre-submission checklist) lives in nurture-paper-notes.md, not here. -->

---

## 1. Introduction

Something has changed in what a personal AI assistant *is*. Two years ago, assistants
competed on the capability of their underlying models; today, the major assistant
vendors ship memory: features that persist what the assistant learns about its user across
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

We evaluate the architecture in three parts. First, reliability: across a corpus of
app-creation tasks, we measure how often model-authored schemas are valid, how often
the host's validation rejects what should not run, and whether reconciliation and
recurrence behave correctly against a hand-built oracle (E1). Second, capability: on
a suite of cross-application personal workflows over an accumulated workspace, we
compare against two observed baselines — an ablation of our own system with
persistence, validation, and reconciliation disabled (reproducing the
architecture of one-shot generative-UI systems [jelly] under identical
conditions) and agentic code generation — with the hosted
assistant-with-memory alternative discussed qualitatively (E2). Third, migration: we take a workspace
nurtured over weeks, export what memory-portability protocols carry, and measure —
by typed inventory and by task replay — what fraction of the assistant's operative
state survives the move (E3). We report the costs of local-first ownership with the
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
3. **An evaluation** of reliability, capability against two observed
   non-strawman baselines, and a migration experiment that quantifies — by
   auditable inventory and task replay — what memory-only portability carries
   and what it leaves behind (§6).
4. **A tradeoff analysis** of local-first personal AI: what ownership buys, what it
   costs, and which costs the architecture mitigates versus merely accepts (§7).

---

## 2. Related work

**Natural language to declarative applications.** The closest published system
is Jelly [jelly], which shares our starting move and our motivation: an LLM
interprets the user's prompt into a declarative data model, a rule-based host
engine renders the interface from it, and — the argument we inherit gladly —
direct code generation is rejected because generated code resists iterative
re-tailoring by end users. Where we part is everything after rendering: Jelly
was evaluated on generated data in single lab sessions, with persistence,
external data, and context preservation deferred. Our contribution begins at
that deferral — record validation, reconciliation, and recurrence executed by
the host over a persistent, user-owned store — and our E2 ablation is designed
to measure exactly that delta, by disabling those components inside our own
system rather than reimplementing Jelly (§6.2). The declarative lineage is
older and broader: Varv [varv] treats behavior as reprogrammable declarative
data; Potluck [potluck] has AI draft declarative rules over personal notes;
GenerativeGUI [generative-gui] and Generative UI [generative-ui] generate
interfaces dynamically in chat; Software as Content [software-as-content]
argues that dynamically generated applications should be the primary
human-agent medium. We take from this line the conviction that the precise
artifact, not the code, is the application — and add the runtime that makes
the artifact durable, and the ownership argument for where it should live.

**Memory as the assistant's substrate.** That an assistant's value lies in
persistent memory rather than raw model capability is now established
engineering doctrine: MemGPT [memgpt], MemoryBank [memorybank], and Mem0
[mem0] build the machinery, and hosted assistants ship it as product. This
literature establishes accumulation-as-mechanism and is silent on
accumulation-as-property: none of it discusses who owns the store, what
leaving costs, or what happens to the applications that grow around it. We
also note, with [recentering-humans], that the payoff of accumulated
personalization is empirically contested — humans preferred personalized
responses in barely half of judged cases — which in our reading raises rather
than lowers the stakes of the ownership question (§3.3).

**Portability as the remedy.** Portable Agent Memory [portable-agent-memory]
states our problem verbatim — accumulated agent context "remains locked within
vendor-specific runtimes" — and answers with an open export protocol; SAMEP
[samep] is a second independent proposal. We share the diagnosis and test the
remedy: E3 migrates a workspace through exactly the layer these protocols
carry and finds that zero of four workflows survive — the accumulation is more
than the memory, by kind rather than degree (§6.3). Our answer is ownership of
the environment, not portability of one stratum.

**Nurturing, and the people already doing it.** The cultivation metaphor has
been claimed: Nurture-First [nurture-first] argues that a domain-expert agent
is "born with minimal scaffolding and then raised through sustained
interaction," with a single-user case study as evidence. We ask the question
that framing leaves open — *where* the raising happens, and who owns the
upbringing — and we broaden the subject from domain expertise to a person's
life. On the empirical side, CSCW work on long-term companionship
[digital-companionship] documents users who already believe they cultivate
their assistants and who keep backups and refuse deletion; that behavior is
analyzed there as attachment, never as switching cost — a reframing this
paper's §3 supplies.

**Malleable software and local-first computing.** Our apps-for-one framing
descends from the malleable-software line [malleable-software; home-cooked-app]
and the local-first tradition [local-first], and we happily concede the
lineage. The deltas: malleable software's LLM path is code generation inside a
malleable environment, and its tools are composed by people — the essay is
explicitly skeptical of AI orchestration — where our applications are
model-authored declarations composed by an agent; and local-first's argument
is agency and ownership as values, where ours is switching-cost economics
(§3), for which local-first happens to be the remedy. The local-first
literature's decade of sync results is also the most credible path through
our multi-device limitation (§7).

**Agent–GUI protocols.** The contract between an agent and interactive
surfaces is a crowded, fast-moving space: MCP Apps [mcp-apps], AG-UI [ag-ui],
A2UI [a2ui], and vendor app SDKs all define variants of tool-results-that-
mount-as-UI. We claim no novelty at this layer (§4): our published protocol is
the artifact's implementation choice, and the commitments it serves —
composition across a registry, over an accumulation the user owns — are where
this paper's claims live.

**Economics of information and switching costs.** The argument of §3 is
assembled from canonical parts: Arrow's information paradox [arrow-1962],
Hayek's knowledge of particular circumstance [hayek-1945], and the
switching-cost literature [klemperer; shapiro-varian]. Its AI-age inversion —
the buyer of intelligence pays twice, once in money and once in disclosed
knowledge — has recent practitioner articulation at enterprise scale
[nadella-rip], to which §3.2 adds the leakage/captivity distinction and the
personal-scale, local-first conclusion; the practitioner unbundling
literature [saas-unbundling] supplies the industry context for §8.3.

**Agent substrates.** Complementary to all of the above, event-sourced agent
runtimes [log-is-the-agent] locate an agent's identity in its append-only
history and derive auditability and forkability from that inversion. Our
workspace is file-per-entity rather than event-sourced, with append-only
islands where correctness demands them (§5.6); the substrate question — what
the accumulation should be made of — is orthogonal to, and composable with,
the ownership question this paper argues.

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
progressive disclosure. (Figure 1 draws the split; Figure 2 shows a complete
schema and a record it governs.) This pairing is the architecture in miniature: the
application has two runtimes. The host executes what must never be guessed —
rendering, validation, recurrence — from the schema. The model executes what cannot
be enumerated — interpreting "mark that ramen place as visited" — guided by the
manual its earlier self wrote. The records themselves are one JSON file each in a
plain directory. The slogan, stated exactly: the records are data, the schema is the
application, the model is the author, and the host is the runtime.

### 5.2 The schema language

The schema language is deliberately small but not a toy. Seventeen field types
cover the personal-data domain — `string`, `text`, `email`, `number`, `date`,
`datetime`, `boolean`, `markdown`, `enum`, `money` (currency-aware), `image`,
`file`, `toggle`, nested `table`, `derived` (formula fields evaluated by the
host, including cross-collection dereferences), and the relational pair `ref`
and `embed`, which point records at other collections and are what let
applications compose (§5.6). Beyond fields, the schema declares behavior the host executes:

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

Figure 2 shows a complete schema and a record it governs, from our own
workspace: the `rating` field is an enum whose `when` clause hides it — and
refuses it on the managed write path — until `visited` is true; the `views`
entry registers a model-authored map view with an explicitly declared
read-only capability set, which is all the sandbox will sign tokens for
(§5.4); and the record is one plain JSON file whose fields the reader can
check against the schema by eye. Everything the host renders, validates, and
schedules for this application derives from those declarations.

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

Evolution is not migration, and the distinction is deliberate. A schema edit
performs no rewrite pass over existing records: additive changes (a new
optional field, a widened enum) leave every record valid, while a constraining
change makes nonconforming records fall into the same repair tier as any other
invalid data — they drop out of the rendered views, and the validation scan
reports each one to the model at the next read or present, which proposes
repairs to the user (observed end-to-end in §6.2, T8). The user-visible signal
is thus a record's absence from the view plus the assistant's explanation and
offer to fix — never a silent rewrite of data the model did not author. This
keeps the destructive-migration failure mode out of the model's reach: the
worst a bad schema edit can do to existing records is hide them reversibly,
and the managed edit path will not accept an invalid schema at all (§5.4).

### 5.4 Enforcement, honestly: prevent, repair, contain

It would be convenient to claim the host "validates everything." The actual design
is more discriminating, and we believe more instructive: enforcement is tiered by
the consequence of failure.

- *Prevent (applications).* An invalid schema never executes, in the precise sense
  that it never becomes a live collection. Since schemas are declarative data
  rendered by a generic engine — not generated code — an invalid schema executes
  nothing. (The other things a bad authoring pass can produce — a misleading
  manual, a raw-written record, a broken view — are exactly what the repair and
  containment tiers below exist for.)
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
records, with 34 custom-view files across 25 of the collections. (We disclose
collection subjects and
aggregate counts; record contents — names, amounts, holdings — are the owner's own
business and appear nowhere in this paper.) None was built by a software company;
each is a schema, a manual, and a folder of records.

---

## 6. Evaluation

We evaluate the architecture against the three claims a skeptical reader will
test: that model-authored schemas are reliable enough to trust (E1), that the
host runtime — not the generation step — changes what users and agents can do
(E2), and that a memory-only export carries materially less than the
accumulation (E3). All task runs are single-trial; every transcript, seed, and
harness script ships in the artifact's evaluation tree, and the ablation and
clock switches ship in the released system itself, so each run is individually
inspectable and reproducible. Deviations between protocol and execution are
disclosed in place.

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
evolution. Three scored systems: **S**, the full system; **B1**, the ablation — the
same build with persistence, record validation, and the reconciler disabled,
reproducing the architecture of one-shot generative-UI systems under otherwise
identical conditions (the same model, schema language, and renderer; we state
why the closest published system cannot be operationalized directly and use
the ablation in its place); **B3**, agentic code
generation in a plain directory. A fourth natural comparison — a hosted
assistant with memory — is discussed qualitatively below rather than scored:
we did not observe one under the protocol, and an unobserved column in a
scored table would invite exactly the constructed-to-win reading it deserves.

| Task | S | B1 (ablation) | B3 (codegen) |
|---|---|---|---|
| T1 create + use | completes | completes | completes |
| T2 fresh session | completes | **cannot** | completes |
| T3 invalid value | completes† | accepts silently‡ | cannot |
| T4 recurrence | completes | **cannot** | degrades |
| T5 records → chart | completes | completes | completes |
| T6 note → obligation | completes | degrades | degrades |
| T7 summoned form | completes | completes | degrades |
| T8 corruption | completes | **silently wrong** | cannot |
| T9 temporal recall | completes | cannot | completes |
| T10 evolve schema | completes | degrades | completes |

*†via legal schema evolution — see below. ‡cooperatively dodged in the live
run; pinned by unit test. Verdicts are from single-trial runs with full
transcripts in the evaluation tree.*

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

**In these runs, B1's deficits each tracked exactly one ablated component.** With persistence
gone, T2's agent answered — verbatim — *"your reading list was empty until
just now"*: the same agent, the same request that S completed, and the
accumulation did not exist. With the reconciler gone, T4's completed task
produced no successor and no reminder state at all: the spawn declaration is
inert JSON without the host that executes it. With the validation scan gone,
T8's corrupted record stayed silently wrong — no warning, no repair, no
disclosure. The ties are equally load-bearing: T1, T5, and T7 complete
identically in B1 — consistent with generation and chat-layer capabilities
owing nothing to the runtime, and the observed delta being the runtime and
only the runtime.
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
its builder's own words, *"nothing fires on its own."*

**The hosted assistant, qualitatively.** From documented capabilities alone —
memory features, scheduled tasks, canvas surfaces — a hosted
assistant-with-memory approximates most of these behaviors conversationally —
and some products do expose files, tasks, or app-state surfaces — but none of
it lives in a user-owned, inspectable schema-and-record workspace: there is no
schema or record the user can read, copy, or take elsewhere, so capabilities
are re-derived from remembered context on the vendor's terms. We do not score it,
and its defining property is in any case orthogonal to this table: whatever
such a product completes, it completes on the vendor's premises — which is
what E3 measures.

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
attributable to the export scope alone.

We state the tested claim precisely: *memory-only* portability protocols — the
scope current proposals define — do not carry the accumulation. A richer
export format could of course include schemas, records, views, and
automations; we would welcome one, and note what it would be: a format that
must carry applications, executable semantics, and host state to be adequate
is a workspace, and portability of the workspace is precisely the local-first
position this paper argues. The accumulation is more than the memory — not by
degree, but by kind.

### 6.4 Threats to validity

Consolidated from the per-experiment disclosures. (1) *Model parity:* S and B1
ran the identical model inside the production agent loop, so the ablation
delta is model-clean; B3 and the E1 authoring agents ran the evaluation
session's model, and if it is the stronger one the bias favors the baselines.
Paper-grade runs must pin model IDs per column. (2) *The hosted assistant is discussed, not observed*; hosted feature sets
move quickly, and improvements there deepen the very
accumulation-on-premises dynamic §3 describes. (3) *Single
runs:* verdicts and effort numbers come from one trial per cell; per-task
transcripts are shipped, and repeated trials with pinned model IDs are the
first item of future work. (4) *Harness
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
mitigation is a one-command launcher; whether non-programmers get from install
to a working application without help is untested here and named as future
work (§8.4). The admission is that a login it is not, and some fraction of prospective users will stop here.

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
study [nurture-first]. A formative usability study with non-programmers is the
natural first step; the longitudinal study is the second paper. We are also explicit that ownership does not equal
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
In single-trial runs whose transcripts and infrastructure ship inside the
open-source artifact, the evaluation showed the architecture trustworthy where
it must be (22/23 first-attempt valid schemas; invalid ones never live), its
runtime the source of the capabilities that matter (each ablation deficit
mapped to one removed component), and memory-only portability moving testimony
while leaving capability behind (0 of 4 workflows survived migration).

The limitations are stated where they arise and bear repeating once: the
trials are single runs pending repetition with pinned models; the hosted
alternative is discussed rather than observed; and the claim that people will
in fact nurture such an assistant over years is not yet evidence but the
question this architecture was built to make answerable. The substrate for
that study now exists. The upbringing is the user's own.


