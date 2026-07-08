# The Workspace Is the Self-Improving Agent

> Why putting code — not just data — into the agent's workspace turns an
> assistant into a self-improving builder of its own applications.

**Status**: Paper. Written 2026-06-13. Author: Satoshi Nakajima.

**Companion essays**: [`dsl-as-harness.md`](./dsl-as-harness.md) argues *why* a
deliberately limited language is a powerful harness;
[`collections-architecture.md`](./collections-architecture.md) develops the
collection mechanism in detail. This paper is the synthesis: it asks what it
means when the *whole agent* — its identity, behavior, capabilities, and memory —
is nothing but files in a workspace, most of them written in DSLs.

---

## Abstract

MulmoClaude's founding philosophy is *the workspace is the database; files are
the source of truth; Claude is the intelligent interface.* Its long-term memory
follows Andrej Karpathy's *LLM Knowledge Bases* idea — rather than a flat
`memory.md`, the agent builds and maintains its own interconnected wiki, an
artifact it authors and curates itself. This paper argues that the philosophy,
and that lineage, understate their own reach. The workspace does not hold only
*data*. It holds *code* — roles, collection schemas, skills, automations, tool
wiring — almost all of it written in domain-specific languages that Claude
interprets. Once the artifact the agent maintains includes its own *behavior*,
the right statement is stronger: **the workspace is the agent**, and an agent
that authors its own workspace is **self-improving**.

The consequence is that the boundary between "the agent" and "the applications
the agent builds for its user" dissolves. A collection skill — a todo list, a
personal restaurant guide, an invoice tracker — *acts like a traditional
application*: it has a data model, workflows, a UI, and reliable operations. But
it is authored by the agent on demand, into the agent's own substrate, with no
deployment boundary. An app the agent builds becomes part of the agent.
Improving such an app is therefore self-improvement. We claim that
**"self-improving agent" is a more accurate description of this architecture
than "no-code platform,"** because the latter still casts a human as the builder
and the app as a separate product. We develop the self-improvement loop
(recognize → crystallize → tune → retire), the "reliability dial" between what is
pinned in a DSL and what is left to Claude's judgment, the resulting
personalization-through-accreted-apps, and the honest tensions — chiefly sprawl
and the need for self-pruning.

---

## 1. From "the workspace is the database" to "the workspace is the agent"

MulmoClaude's stated philosophy is deliberately humble: *the workspace is the
database.* It positions the file system as storage and Claude as the interface
that reads and writes it. That framing is correct but incomplete, because it
describes only half of what actually lives in `~/mulmoclaude/`.

Look at what is actually there:

| Location | What it is | Which sense |
|---|---|---|
| `config/roles/` | persona / system-prompt definitions | **code** (behavior DSL) |
| `config/mcp.json` | tool-and-server wiring | **code** (capability DSL) |
| `config/helps/` | help surfaces | code + data |
| `data/collections/*/schema.json` | data model + UI + computation + workflow | **code** (application DSL) |
| `data/collections/*/views/*.html` | bespoke, agent-authored UI for a collection | **code** (presentation) |
| collection `SKILL.md` | procedural instructions the agent reads to operate a collection | **code** (procedural DSL) |
| `feeds/*/schema.json` | external-source ingestion + data model | **code** (acquisition DSL) |
| `data/scheduler/` | recurring automations | **code** (trigger DSL) |
| `data/wiki/` | densely cross-linked knowledge | data + graph DSL |
| `conversations/memory.md` | accreted facts | **data** |
| `artifacts/` | generated outputs | **data** |

Only the bottom rows are "the database." Everything above is *program*: it
specifies what the agent is, what it can do, how it behaves, and when it acts.
Claude is not merely an interface onto stored data; it is the **runtime that
interprets a multi-DSL program persisted as files.** The agent's identity is
`config/roles/`; its capability set is `config/mcp.json` plus its skills; its
applications are its collections; its proactive behavior is its automations; its
long-term knowledge is its wiki and memory. Strip the running process away and
the agent does not disappear — it sits, complete and inspectable, on disk.

That is why the sharper claim is **the workspace is the agent.** The workspace is
not where the agent keeps its data. The workspace *is* the agent, of which data
is one part.

### 1.1 Lineage: from self-maintained memory to self-improvement

The direct ancestor of this design is Andrej Karpathy's *LLM Knowledge Bases*
idea: rather than cramming everything into the context window or a flat
`memory.md`, let the LLM build and maintain its own **wiki** — a growing,
interconnected set of files that serves as genuine long-term memory. MulmoClaude
ships exactly that: a wiki the agent writes, links, and lints itself. The
principle Karpathy named is the one this paper builds on — *the agent maintains
its own artifact.* The files are the agent's own, authored and curated by it, not
handed to it from outside.

This paper takes that principle one step past memory. Karpathy's wiki is
self-maintained **data** (unstructured knowledge); collections already extend it
to self-maintained **structured** data. The observation here is that the same
workspace also holds self-maintained **code** — schemas, skills, roles,
automations (§1). So the agent does not merely curate its own *knowledge*; it
builds and refines its own *applications*. The instant the artifact the agent
maintains includes its own behavior, "self-maintaining" becomes
**self-improving** — and that turn is the whole subject of this paper.

It is worth saying why that turn matters so much. An agent that only accumulates
facts gets *better-informed*; an agent that can author and refine the
applications it runs gets *more capable* — and capable in a direction shaped by
one particular user (§4). This kind of self-improvement **compounds**: each app
the agent crystallizes makes the next interaction faster and more reliable, and
the workspace grows into a personal capability surface that no general model
update can reproduce. That is a more consequential property than any single
feature, which is why the rest of the paper is about the loop that produces it
(§4), the boundary that keeps it reliable (§5), and the discipline it demands
(§6).

> A note on what this design gives up. Other work names a different primary
> artifact — Nakajima's *The Log is the Agent* (arXiv:2605.21997) makes the
> event log primary to get deterministic execution replay. The workspace view
> deliberately forgoes byte-for-byte run replay (the LLM step is
> nondeterministic) in exchange for an agent you can read, fork, and evolve as
> plain files. The two optimize for different things; this paper pursues the
> second.

---

## 2. A collection skill is a traditional application

The most important consequence of "code lives in the workspace" is this: **a
collection skill is an application in the full, traditional sense — not merely
structured memory.**

A traditional application bundles a handful of concerns. A collection skill
bundles the same ones, and the host supplies the runtime for all of them
generically:

| Concern | Traditional stack | Collection skill |
|---|---|---|
| Data model | database + ORM | `schema.json` fields |
| Relationships | foreign keys, joins | `ref` / `embed` fields |
| User interface | frontend framework | host-rendered field types — **free** |
| Custom UI | bespoke frontend code | `views/*.html` the agent authors — sandboxed, capability-scoped |
| Computation | service code | `derived` fields (spreadsheet-like, cross-collection) |
| Workflow | workflow engine | `actions` + `SKILL.md` procedures |
| Data acquisition | ETL / cron jobs | `ingest` block (RSS / Atom / JSON, scheduled) |
| Persistence | DB server | `records/*.json` on disk |

A personal restaurant guide built this way *is* an app: it has persistent
structured records, a list/detail UI, derived fields (distance, average rating),
relationships (a restaurant `ref`s a neighborhood), and workflows ("mark visited,"
"draft a reservation message"). The same is true of a todo list, an invoice
tracker, a portfolio, a CRM, a reading list. The host platform contains *zero*
domain knowledge about any of them; it understands only fields, relationships,
derived values, and actions. Everything domain-specific is the collection.

### 2.1 Why it is an *application*, not a memory note

It is tempting to say "but you could just ask Claude to track restaurants in
`memory.md`." The difference is exactly the difference between an application and
a note, and it is threefold:

1. **Structure.** A schema pins the shape: every restaurant has the same fields,
   typed and validated. A note is free-form and re-parsed, lossily, every time.
2. **Durability of behavior.** A collection behaves the *same way tomorrow*. The
   skill is a stable contract; a prompt-of-the-moment is not. CRUD on a
   collection is a real, repeatable file operation, not a re-derived guess.
3. **A UI for free.** The host renders the collection as a navigable surface with
   pickers, links, and computed columns — and where field types are not enough,
   the agent authors a bespoke view (`views/*.html`: a chart, a map, a flashcard
   deck) that the host serves sandboxed. A note renders as text.

There is a natural ladder of memory maturity, and a collection skill is the top
rung:

```text
conversation        ephemeral
   ↓
memory.md           persistent, unstructured
   ↓
collection          persistent, structured, queryable
   ↓
collection skill    + workflows + UI + a stable contract  =  application
```

Part of the agent's job is to recognize when a recurring need has stabilized
enough to deserve promotion up this ladder — to *crystallize* a loose, repeated
intent into a durable application. That recognition is where self-improvement
begins (§4).

---

## 3. The boundaries that dissolve

A traditional application is **built by developers**, shipped across a
**deployment boundary**, and **run by users**. The DSL-in-workspace model erases
all three.

### 3.1 The builder is the agent, not a developer — and not a human composer

This is the line that separates the architecture from no-code platforms. In
Airtable, Notion, Retool, or PowerApps, the environment is still designed by a
human: the platform hands you primitives and *you* compose the app. The human is
the builder; the tool is the saw.

Here the **agent** is the builder. The user expresses a need in natural language
— often implicitly, through repeated similar requests — and the agent translates
it into the DSLs: it writes the `schema.json`, authors the `SKILL.md`, wires the
actions. The human is the product owner, not the carpenter. This is the jump from
*no-code* (a human composes blocks) to *intent-driven* (an agent composes the
DSL program from intent). The companion essays call the user-authored case "the
democratization of harness engineering"; the agent-authored case goes one step
further — the harness writes itself on request.

### 3.2 There is no deployment boundary

A traditional app is built in one place and deployed to another. A collection
skill is authored **directly into the agent's own substrate.** Building it and
running it happen in the same workspace, in the same breath. There is no build
step, no CI, no release, no migration. The user says "also track whether I've
been to each restaurant and my rating," and the agent edits the schema and skill
in place; the app has evolved, live, with no redeploy.

### 3.3 The app/agent boundary disappears — so improving an app is self-improvement

Because the workspace *is* the agent (§1), and the app is authored into the
workspace (§3.2), **the app becomes part of the agent.** There is no longer a
clean line between "the agent" and "the applications the agent built." The
restaurant guide is not a product the agent ships and walks away from; it is now
one of the agent's own capabilities, indistinguishable in kind from its roles and
skills.

This is why the framing matters. When the agent refines a collection it built, it
is not maintaining a separate product — **it is modifying its own code.** That is
the precise sense in which this is a *self-improving agent*, and it is why
"self-improving agent" is a better description than "no-code platform":

- "No-code platform" foregrounds a human builder and a separate artifact. Both
  are wrong here.
- "Self-improving agent" foregrounds the loop that actually defines the system:
  the agent extends its own capabilities by writing DSL code into itself.

### 3.4 The trajectory already proves it

This is not aspirational; the codebase is mid-migration along exactly this path.
Features such as worklog / client / invoice began as **hardcoded host plugins** —
developer-built apps behind a deployment boundary, requiring host code, a route,
a build, a release. They are being **superseded by `mc-*` collection skills** —
agent-buildable apps with no deployment boundary. Recurring obligations, once a
dedicated scheduling subsystem, are now a handful of keys on a collection schema
(`triggerField`, `spawn`) that the agent can author without touching the host
(see `dsl-as-harness.md` §B). The locus of application creation is visibly moving
**from the development team to the agent.** A restaurant guide never needs a
developer to ship a "restaurant plugin." That migration *is* this paper's thesis,
demonstrated in the git history.

---

## 4. The self-improvement loop

"Self-improving" is loose unless we say what improves and how. It is not that the
model gets generally smarter — the weights are fixed. It is that the agent
**accretes and refines a personal suite of applications in its workspace.** The
loop has four steps, and the fourth is the one most easily forgotten.

```text
   ┌─────────────┐     ┌──────────────┐     ┌────────────┐     ┌──────────┐
   │  RECOGNIZE  │ ──▶ │ CRYSTALLIZE  │ ──▶ │   TUNE     │ ──▶ │  RETIRE  │
   │ a recurring │     │ into a DSL   │     │  the dial  │     │  when    │
   │   need      │     │   app        │     │  (§5)      │     │ superseded│
   └─────────────┘     └──────────────┘     └────────────┘     └──────────┘
          ▲                                                          │
          └──────────────────────────────────────────────────────────┘
```

1. **Recognize.** Notice that a need recurs — the user keeps asking for the same
   shape of thing in free-form chat. This is the signal to promote it up the
   maturity ladder (§2.1).
2. **Crystallize.** Author the application: write the schema, the skill, the
   actions. The loose intent becomes a durable, structured, reliable app.
3. **Tune.** As the need evolves, adjust *where the reliability dial sits* (§5) —
   move more structure into the schema where it must be deterministic, leave more
   to Claude where it needs judgment. Edit fields, add derived columns, refine the
   skill's instructions.
4. **Retire.** When an app is superseded or abandoned, remove it. This step keeps
   the agent's "self" coherent rather than sprawling (§6).

The output of running this loop over months is not a smarter model. It is an
agent whose workspace has grown into a **personalized application suite shaped to
one user.** Two MulmoClaude instances that start identical will diverge into very
different agents, because they will have crystallized different apps from
different lives. Self-improvement here is **personalization through accreted
applications** — the agent becomes more useful to *its* owner specifically, not
more capable in the abstract.

---

## 5. The reliability dial

The reason a self-built, LLM-operated application is not just "flaky chat with
extra steps" is the central design principle of the whole architecture: **the DSL
is a contract that pins down what must be reliable, while Claude supplies the
flexibility, judgment, and language understanding.** You get the *reliability of
a traditional application* and the *authoring flexibility of an LLM*
simultaneously, because they live on opposite sides of a deliberate line.

Concretely, the host guarantees the deterministic half — schema validity, path
safety, derived-value computation, recurrence math, record storage — and these
run identically every time. Claude owns the judgment half — what to model, what a
record means, how a workflow should go, when to hand off to a human. A schema
*validator* makes the boundary self-enforcing: a structurally incoherent
application is rejected at load, with an actionable message, before it can run
(see `dsl-as-harness.md` §2).

The craft is **where you set the dial:**

```text
        more pinned in the DSL  ◀──────────────●──────────────▶  more left to Claude
        (rigid, deterministic,                                    (flexible, judgment,
         verifiable)                                               adaptable)

        over-pinned  →  a cage; the old no-code rigidity, can't express real needs
        under-pinned →  flaky; a bare prompt with no stable contract
```

Push everything into the DSL and you rebuild the brittle, can't-express-this cage
that made no-code platforms frustrating. Push everything to Claude and you lose
the durable contract that made it an application at all. A good collection schema
draws the line precisely: structure that must not drift goes in the schema;
genuine judgment goes to Claude; and an **escape hatch** (a schema-declared
`action` that opens a seeded chat with full tools) exists for exactly the moments
the declarative layer runs out — "business logic as prose, behind a declarative
door."

The "Tune" step of the self-improvement loop (§4) is, precisely, the agent
**learning where to set this dial, per app, per user, over time.** Early on a
collection may lean on Claude for most decisions; as patterns stabilize, more
gets promoted into the schema where it becomes cheap and certain. The guiding
rule from `collections-architecture.md` holds: *extend the declarative layer only
when it outperforms the agent.*

---

## 6. The honest tension: self-improvement requires self-pruning

If every recognized need spawns an artifact, and every artifact becomes part of
the agent's "self," then **self-improvement without self-pruning produces a junk
drawer.** Half-built collections, abandoned skills, stale automations, and dead
roles accumulate. Traditional applications have maintainers and sunset processes;
an agent's self-built apps need the same discipline, and nothing provides it
automatically.

This is not hypothetical. The very migration that proves the thesis (§3.4) — old
worklog / client / invoice plugins superseded by `mc-*` collection skills —
*is* the pruning problem surfacing: superseded apps that must now be retired
cleanly, with their references cleaned up, or they rot in place and confuse both
the user and the agent.

So the loop in §4 must be stated as a full cycle, with the retire step
first-class:

> recognize a recurring need → crystallize it into a DSL app → tune the dial as
> it evolves → **retire it when superseded.**

The retire step is the one that keeps the agent's self **coherent** rather than
merely **larger.** An agent that only ever adds capabilities does not improve
indefinitely; past some point it degrades, because more surface means more ways
to be wrong, more stale instructions, more conflicting skills competing for the
same intent. A genuinely self-improving agent must be as willing to delete its own
code as to write it.

A related, milder tension is the determinism gap already noted in §1.1: because
execution is not replayable, a self-modification's *effect* cannot be A/B-replayed
against the old behavior on identical inputs. The mitigation is the cheap one — a
git-backed workspace makes every self-edit auditable and revertable at the
configuration level, which is the level that matters here. This is the one place
where importing a sliver of "the log is the source of truth" genuinely pays:
not to replay runs, but to make the agent's edits to itself reviewable.

---

## 7. Forking, portability, and what the workspace buys for free

Because the agent *is* its workspace, several properties that normally require
engineering fall out of the file system:

- **Forking an agent is `cp -r`.** Copying the workspace copies the agent whole —
  its apps, its memory, its personality, its automations — as a single coherent
  unit. There is no separate "export behavior" and "export data" step, because
  they are the same files.
- **Versioning an agent is `git`.** A git-backed workspace gives configuration
  replay (`checkout`), branching (`branch`), and self-edit lineage (`blame`) —
  audit and rollback for the agent's edits to itself, with no bespoke runtime.
- **Portability is trivial.** The agent is just files. No runtime state is locked
  inside a process; nothing is stranded in a database server. Move the directory,
  move the agent.
- **Inspectability is total.** Every part of the agent — what it is, what it can
  do, what it knows — is a readable, greppable, diffable file. There is no opaque
  learned blob that constitutes "the agent" apart from its workspace.

These are not the headline result, but they are why the headline result is
practical. An agent you can fork, version, inspect, and carry is an agent you can
safely let modify itself, because every modification is a visible, reversible
change to files you can read.

---

## 8. Owning the learning loop: from one user to the firm

The sharpest external statement of *why this matters* arrived, while this essay was
being written, from Satya Nadella:
["a frontier without an ecosystem is not stable."](https://x.com/satyanadella/status/2066182223213293753)
His argument is that the strategic question for any organization in an AI economy is
not which model is best, but whether it can **own the learning loop** that encodes
its institutional knowledge — and that the *test* of that ownership is whether it can
swap out a generalist model without losing the "company-veteran" expertise built on
top of it.

The workspace-is-the-agent architecture passes that test by construction. The
expertise lives in `config/roles/`, the collection schemas, the `SKILL.md` files,
and the wiki — files the model interprets, not weights it carries. Replace the model
and the accumulated knowledge is untouched, because it was never inside the model.
The "company veteran" *is* the workspace.

This is a stronger form of ownership than the one usually reached for. The reflexive
answer to "own your learning loop" is *fine-tune a model on your private traces* —
but a model you tuned is a model you are now coupled to: the IP is baked into weights
you cannot fully inspect, diff, or carry to the next frontier model without
retraining. A declarative workspace keeps the IP **inspectable, diffable, forkable,
and model-agnostic.** The honest qualification is one of coverage, not direction:
declarative files capture *explicit* knowledge — workflows, judgment-as-prose, linked
notes — better than the *tacit* pattern recognition that learning on private traces
can absorb. The two are complementary. The workspace is the portable substrate that
survives a model swap; private tuning, if any, is an accelerator layered on top — not
the thing you own.

And the concept is not intrinsically personal. MulmoClaude, throughout this essay, is
a **single-user** agent, and that is the scope of the evidence. But the same
primitives scale to an organization: a team's learning loop becomes a **shared,
versioned workspace** — roles, collection schemas, skills, and a cross-linked wiki —
forked with `cp -r`, branched and audited with `git`, and owned independently of any
model vendor. At that scale the workspace is precisely the firm's compounding
capital: institutional memory made queryable, recurring workflows crystallized into
applications (§4), and the whole of it portable across model generations. The
multi-user case has real open problems — concurrency, access control, and the merge
discipline that keeps a shared "self" coherent — which this essay does not solve. But
the single-user result already points at the conclusion that matters: **the durable
unit of ownership, whether the owner is a person or a firm, can be a workspace of
files rather than a tuned model.**

---

## 9. The broader shift

Two sentences capture the change in how software comes to exist.

Traditional software assumes:

```text
Engineers write programs.  Users operate them.
```

This architecture assumes:

```text
Users express intent.  Agents write the programs — into themselves.  Everyone operates them.
```

The collection schema is the program. The DSLs in the workspace are the source
code. Claude is the runtime. The workspace is the agent. And because the programs
live inside the agent, writing them is the agent improving itself — which is why,
of all the names available, **self-improving agent** is the one that fits.

The companion essays end on "applications become data; harnesses become
software." This paper's addition is the reflexive turn: when the harnesses live in
the agent's own workspace and the agent authors them, **the software is the
agent, and building software is how the agent grows.**

---

## See also

- [`dsl-as-harness.md`](./dsl-as-harness.md) — why a limited language is a
  reliable harness; concrete walkthroughs of MulmoScript and the Collection DSL.
- [`collections-architecture.md`](./collections-architecture.md) — Collections
  as applications-as-data; host/Claude responsibility split; relationships,
  derived fields, actions.
- [`extension-mechanisms.md`](../extension-mechanisms.md) — the seven extension
  paths the host exposes to Claude, and how to choose among them.
- Karpathy, [*LLM Knowledge Bases*](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
  — the self-maintained-wiki idea this paper extends from memory to applications
  (§1.1).
- Nakajima, *The Log is the Agent*, arXiv:2605.21997 — names a different primary
  artifact (the event log); briefly contrasted in §1.1.
