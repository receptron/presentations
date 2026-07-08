# DSLs as Harnesses

*Part 3 of the series "Beyond the Sea of App Icons."*

## The claim

When the team behind SWE-agent studied what made their coding agent succeed, the single highest-leverage component was not the model. It was a linter that ran on every edit and rejected syntactically broken changes at the moment of introduction, before the error could propagate through a dozen later steps. The model supplied the intelligence; a guardrail supplied the reliability.

That finding generalizes into the prevailing lesson of applied AI engineering in 2025–2026: the *harness* — the designed environment an agent operates inside — matters more than the model. A harness is the set of tools an agent can call, the format of the information it receives, the feedback that catches its mistakes, and the scaffolding that lets it hand work to its future self. The same model, given a better harness, produces dramatically better work. The interface is not a convenience layer wrapped around the intelligence; for a language model, the interface *is* the cognitive architecture.

This essay argues a narrower and, I think, more useful point: **a domain-specific language is one of the most powerful harnesses you can give an agent.** A DSL trades the unlimited expressiveness of general-purpose code for a small, legible, checkable surface — and that trade is exactly what an autonomous agent needs to be reliable over the long run.

Part 1 of this series argued that AI-native computing rests on two pillars — **the computer that understands** and **the computer that builds** — and left the second holding a debt: generation is only trustworthy when its output can be constrained, validated, and sandboxed. Who guarantees that a generated table computes what it claims? I promised there that constrained languages and validation were the answer; this article pays that debt. Generation needs a harness the way understanding needs a canvas — the canvas was Part 2's subject; the harness is this one's.

Ink & Switch, an AI-optimistic research lab, concluded in their June 2025 essay "Malleable Software" that "AI code generation alone does not address all the barriers to malleability" — that dropping a code-generating model into today's closed, monolithic app ecosystem is "like bringing a talented sous chef to a food court." This essay is about the kitchen.

## Why the trade pays off

A general-purpose programming language is Turing-complete. That is its glory and, for an agent, its hazard. There are infinitely many ways to write any given behavior, no two codebases agree on conventions, and nothing about the language itself tells the agent whether a given program is *correct for this domain*. The agent is free, and freedom under uncertainty is where agents thrash: they explore broadly, drift toward locally-plausible patterns, and accumulate subtle mistakes that only surface much later.

A DSL inverts every one of those properties. It is deliberately *not* a general language. It can express a bounded set of things, in a bounded number of ways, and it usually ships with a parser and validator that can say "this is well-formed" or "this is not" before anything executes. When you hand an agent a DSL, you are not just giving it a tool — you are reshaping the space it has to search. That reshaping is what makes the four classic harness patterns fall out of a single design decision.

### 1. The schema is the system of record

Harness engineering insists that anything the agent cannot read in context effectively does not exist; intent must live in a machine-readable artifact, not in a Slack thread or a person's head. A DSL satisfies this by construction. Its schema *is* the specification. When an agent writes a DSL document, the user's intent is captured as a structured, inspectable object rather than dissolved into the incidental details of imperative code. You can diff it, version it, validate it, and reason about it — all without running it.

### 2. The validator is a free feedback loop

The linter from the opening is the pattern: reject a malformed change the instant it is introduced, with a localized, actionable message, before the error can compound. A DSL gives you that loop for nothing. Every DSL has a parser; most have a type or schema checker; a malformed structure is rejected the instant it is emitted. You did not have to build the feedback loop — it came bundled with the language.

### 3. The grammar is a forcing function

SWE-agent's search tool capped results and told the agent to narrow its query when it was too vague. That cap was not a limitation; it was a *forcing function* that pushed the agent from flailing toward deliberate, specific action. A DSL's grammar is a forcing function over the entire output. Because the vocabulary is finite, the room to hallucinate is structurally smaller. The agent cannot invent an option that does not exist in the grammar; it can only compose the primitives the language actually provides. Constraint, here, is a feature.

### 4. The unit of the language is the unit of context

Progressive disclosure — start small, reveal more only when needed — is the antidote to dumping an entire project into a context window and diluting the agent's attention. A well-designed DSL has a natural decomposition: a beat, a service, a rule, a step. That granularity becomes the agent's editing unit. It can work on one piece without holding the whole document in mind, and the language's structure, not an ad-hoc heuristic, defines the seams.

None of this is exotic. A spreadsheet formula is a DSL, and hundreds of millions of people who would never call themselves programmers write them — the grammar is small, a broken formula fails loudly in one cell instead of silently corrupting the workbook, and the cell is the unit of context. SQL has run the world's databases for fifty years on the same trade: declare *what* you want, and let a planner you never see decide *how*. These properties have been quietly load-bearing in ordinary software for decades; the new move is handing the trade to an agent.

**A DSL is a powerful harness precisely because it gives up power.**

## Three examples

### MulmoScript: generation and execution, cleanly separated

MulmoScript is a JSON-based DSL for describing multimodal presentations and videos — a sequence of *beats*, each carrying text, imagery, audio, and timing. What makes it instructive as a harness is the architecture it enables: **the agent does not produce the video; it produces the script.** A deterministic renderer turns that script into the finished artifact.

This split is the essay's thesis made concrete. The probabilistic, creative work (deciding what the video should say and show) is done by the agent in the DSL. The deterministic, repeatable work (rendering pixels and audio) is done by code that never guesses. The output is inspectable before a single frame is rendered, the same script always yields the same video, and a bad result can be diffed, edited, and re-rendered rather than regenerated from scratch. The harness slogan "the model decides *what* to think about; the harness decides *how* it is executed" is, in MulmoScript, an actual boundary in the pipeline.

### Collections: a DSL that enforces its own invariants — authored by the user

The collections system in my reference implementation, MulmoClaude, is a DSL-as-harness whose authoring pen is handed to the end user. A collection is defined by a schema — a small DSL describing the shape of the data: its fields and types, the relationships between them, which value marks a record "done," when to raise a notification, how a record recurs, and — for a feed — where to fetch its records from. That schema drives the skills the agent uses to read, write, and reason over the records. The schema is the spec; the generated skill files and the host's reconciler are the execution layer.

Like any good harness, the schema enforces its own invariants. Whoever declares a collection — agent or user — has wide latitude in *what* to model, but cannot emit a structurally incoherent schema, because the loader rejects one before it is ever used: a money field with neither a literal currency nor a per-record currency field, a `ref` pointing at a collection that does not exist, a `spawn` whose successor would be born already matching its own predicate (an unbounded respawn), a `triggerField` that does not name a real date field. Each failure is a precise, actionable message — feedback the author can act on without a human in the loop. And the part that must not drift belongs to the host and runs identically every time: the reconciler that fires and clears bells, the civil-date math that advances each recurrence, the create-if-absent write that makes spawning idempotent. Recurring obligations, once a dedicated subsystem in the host, are now just a handful of schema keys executed by that same reconciler. The collection stays correct across every later edit not because a reviewer caught each one, but because the schema would not let an incorrect one through.

The novel move is *who writes the DSL*. In the SWE-agent case, an engineer designs the harness and the agent operates inside it. Collections push the authoring of the harness toward the end user: by declaring a schema, a non-engineer is, in effect, designing the environment the agent will work in. This is the literal democratization of harness engineering. The principle that "engineers design environments rather than write code" becomes "*anyone* can design an environment, declaratively, and let the agent execute within it." Part 4 of this series follows that thought to its conclusion — the schema as the application, the model as the runtime.

### Vibe crafting

There is a good name for what this feels like from the user's chair: **vibe crafting**. Where "vibe coding" lets a *developer* conjure software by describing intent and letting a capable model fill in the code, vibe crafting lets an *end user* conjure a working data app — a collection and, when the built-in views run short, a custom view to see it through — the same way. "Add a priority field." "Track this as a kanban." "Make the rent recur monthly." "Give me a year-at-a-glance view." The user never sees a schema or a line of HTML; they describe what they want and the thing appears, live.

It is tempting to credit this entirely to the model: code-capable LLMs are what make it *possible*. But possible is not the same as *safe to hand to someone who cannot read the output*. A developer vibe-coding still reviews the diff, runs the tests, owns the failure when it breaks. An end user has none of that — they cannot audit a schema they didn't know existed, and they shouldn't have to. Dan Cripe, writing about AI code generation in "The Mythical LLM," put the commercial version plainly: "you can't ship '90% correct' to enterprise customers." An enterprise at least employs reviewers to hunt the missing ten percent; the person tracking their rent in a generated app has no one. What closes that gap is not a better model; it is the **harness**. The collection DSL constrains what can be expressed to what the host can safely render; the schema validator rejects an incoherent app *before* it ever loads, with a message the agent can act on unattended — "90% correct" never ships, because anything less than valid never loads; the custom view runs as sandboxed, capability-scoped HTML that can touch nothing but this one collection's data. Each guardrail is the reason a non-developer can be handed the LLM's coding power without also being handed its failure modes. Vibe crafting is what you get when strong model capability is run through a well-designed harness — the model supplies the expressiveness, and the DSL plus its validators and sandbox supply the safety the user can no longer supply for themselves. Take the harness away and you don't have vibe crafting; you have an untrained user holding a loaded code generator.

This is the same boundary the whole essay is about, drawn at the point of maximum leverage: the more capable the model, the *more* the value comes from the harness that makes its output safe to delegate — here, to delegate all the way out to the person who just wanted a place to track their recipes. (The economics of that delegation are Part 5's subject.)

## The one hazard: design the escape hatch

The same rigidity that makes a DSL a good harness is also its failure mode. When the language cannot express what the user actually needs, an agent will do one of two bad things: give up, or contort the DSL into something it was never meant to hold. A DSL that is too hard becomes a cage.

The well-designed DSLs all answer this the same way — with a deliberate exit to a more expressive layer. A collection drops out of its declarative schema into a seeded chat — an agent with full tools — the moment a record needs the human judgment the form cannot capture; its action buttons start exactly such a chat. A collection's *presentation* has the same exit: when host-rendered field types cannot show the data well — a portfolio as a chart, restaurants as a map — the schema escapes to a **custom HTML view**, arbitrary code the agent writes and the host serves sandboxed, rather than contorting the field-type vocabulary into a layout it was never meant to express. MulmoScript can incorporate arbitrary external assets and media rather than insisting everything be expressed in its own primitives. The art of DSL-as-harness is not maximizing constraint; it is choosing *where* the constraint binds and providing a clean, legible path out where it does not. A harness with no escape hatch eventually forces the agent to either fail or lie, and both are worse than a slightly leakier abstraction.

## Why this matters more as models improve

There is a tempting intuition that DSLs are a crutch for weak models — that as models get smarter, we can hand them general-purpose code and dispense with the guardrails. I think the opposite is true. The case for a DSL is strongest precisely where we want to delegate *autonomously and over long horizons*: where no human will review each step, where the output must be verifiable, where execution must be deterministic and reversible. Those are the conditions of serious agentic work, and they get *more* important as we trust agents with more.

Andrej Karpathy made the human-facing half of this argument in his June 2025 talk "Software Is Changing (Again)." He is no autonomy maximalist — "when I see things like 2025 is the year of agents, I get very concerned... this is the decade of agents" — and his prescription is partial autonomy: an "autonomy slider," and interfaces that let a human verify the AI's work at a glance. "Less Iron Man robots and more Iron Man suits." A DSL is what the suit is made of on the generation side: the artifact is a small document a human can read, the validator checks what a glance cannot, and the deterministic layer guarantees that what you verified is what will run. In Part 1 I read his caution as a design requirement rather than a rebuttal. This is that requirement, met in the language itself.

A smarter model inside a DSL harness is not wasted capability; it is capability aimed at the part of the problem that genuinely requires judgment — what to say, what to build, what to express — while the language guarantees the rest. The model is the reasoning engine. The DSL is a particularly sharp way of deciding what it gets to reason about. Getting that boundary right is the whole game, and a well-chosen DSL draws it with unusual precision. What happens when the agent keeps what it builds is where this series ends, in Part 6.

---

## Appendix: two of the DSLs, concretely

The body argued the case in the abstract. This appendix grounds two of the examples in an actual artifact — the **document an agent emits**, and the **schema or declaration that constrains it** — with a note on which harness property (§1 schema-as-record, §2 free validator, §3 grammar-as-forcing-function, §4 unit-of-context, plus the escape hatch) each one makes concrete.

### A. MulmoScript — a presentation as inspectable data

A MulmoScript is a JSON document: a header, some shared parameters, and an array of **beats**, each a slide with a speaker, narration, and one visual. The agent authors *this*, never the pixels. A meta-example — a short narrated explainer about this very essay:

```json
{
  "$mulmocast": { "version": "1.1" },
  "title": "Why DSLs Make Good Harnesses",
  "lang": "en",
  "speechParams": {
    "speakers": {
      "Presenter": { "provider": "google", "voiceId": "Kore" }
    }
  },
  "beats": [
    {
      "speaker": "Presenter",
      "text": "A harness is the environment an agent works inside: the tools it can call, the format of what it sees, and the feedback that catches its mistakes.",
      "image": {
        "type": "textSlide",
        "slide": { "title": "Harness > Model", "bullets": ["Tools it can call", "Format of information", "Feedback on mistakes"] }
      }
    },
    {
      "speaker": "Presenter",
      "text": "A domain-specific language is a powerful harness precisely because it gives up power.",
      "image": {
        "type": "markdown",
        "markdown": "## The trade\n- Bounded vocabulary\n- A validator for free\n- Inspectable before it runs"
      }
    },
    {
      "speaker": "Presenter",
      "text": "The agent writes the script; a deterministic renderer turns it into the video. Generation and execution stay cleanly separated.",
      "image": {
        "type": "mermaid",
        "title": "Generation vs. execution",
        "code": { "kind": "text", "text": "graph LR\n  A[Agent writes MulmoScript] --> B[Validator]\n  B --> C[Deterministic renderer]\n  C --> D[Video]" }
      }
    }
  ]
}
```

**The schema** is a published JSON schema shipped with the mulmocast engine (the `$mulmocast` version pins it). My reference implementation validates a draft against it on every save and edit, before anything renders — that is harness property §2, the free feedback loop: a malformed beat is rejected with a localized message, no frames wasted. The closed set of beat `image` types (a subset: `markdown`, `slide`, `textSlide`, `image`, `chart`, `mermaid`, `html_tailwind`) is §3, the grammar as forcing function: the agent can only compose visuals the renderer actually understands. And each **beat is the unit of context** (§4) — the agent can revise one slide without re-reasoning about the whole deck. The escape hatch is the `image`/`html_tailwind` types that embed arbitrary assets or raw HTML when the structured layouts run out.

### B. The Collection DSL — a user-authored schema

A collection in my reference implementation is a `schema.json` (the DSL the host renders) plus a `SKILL.md` (the script the agent reads to CRUD records). The novel move, per the body, is that the *user* authors this harness. An invoices collection, exercising relations, a computed total, and an action:

`schema.json`:

```json
{
  "title": "Invoices",
  "icon": "receipt_long",
  "dataPath": "data/invoices/items",
  "primaryKey": "id",
  "completionField": "status",
  "completionDoneValues": ["paid", "void"],
  "fields": {
    "id": { "type": "string", "label": "Invoice #", "primary": true, "required": true },
    "issuer": { "type": "embed", "label": "From", "to": "mc-profile", "id": "me" },
    "clientId": { "type": "ref", "label": "Client", "to": "mc-clients", "required": true },
    "issueDate": { "type": "date", "label": "Issued", "required": true },
    "currency": { "type": "enum", "label": "Currency", "values": ["USD", "JPY", "EUR"], "required": true },
    "lineItems": {
      "type": "table",
      "label": "Line Items",
      "of": {
        "description": { "type": "string", "label": "Description", "required": true },
        "quantity": { "type": "number", "label": "Qty", "required": true },
        "rate": { "type": "money", "label": "Rate", "currencyField": "currency", "required": true }
      }
    },
    "taxRate": { "type": "number", "label": "Tax Rate" },
    "total": { "type": "derived", "label": "Total", "display": "money", "currencyField": "currency", "formula": "sum(lineItems[].quantity * lineItems[].rate) * (1 + taxRate)" },
    "status": { "type": "enum", "label": "Status", "values": ["draft", "sent", "paid", "void"], "required": true }
  },
  "actions": [
    { "id": "pdf", "label": "Generate PDF", "icon": "picture_as_pdf", "kind": "chat", "role": "office", "template": "templates/invoice-pdf.md" }
  ]
}
```

`SKILL.md`:

```markdown
---
name: invoices
description: Issue and track invoices — line items, total, status, and a PDF action. Use when the user wants to draft an invoice, add line items, or mark one sent / paid / void ("create an invoice for X", "mark INV-2026-0007 paid"). Records live at `data/invoices/items/<id>.json`; viewed at `/collections/invoices`.
---

# Invoices (schema-driven collection)

## Record shape
- `id` — invoice number, primary key / filename (e.g. `INV-2026-0007`).
- `issuer` — display-only `embed` of `mc-profile/me`; nothing is stored here.
- `clientId` — a `ref`: store an existing `mc-clients` primary-key slug.
- `currency` — the code every money field formats against.
- `lineItems` — table rows of `description`, `quantity`, `rate`.
- `taxRate` — a fraction (e.g. `0.1` for 10%).
- `total` — **host-computed `derived`. NEVER write it** — the host recomputes it from the line items + tax rate on every render.
- `status` — `draft` / `sent` / `paid` / `void`.

## What to do
- **Create.** Resolve the `clientId` ref, set `currency`, add `lineItems`, set `status: draft`, then Write `data/invoices/items/<id>.json` WITHOUT `total`.
- **List.** Call `presentCollection` with `collectionSlug: invoices`.

## Conventions
- Only link `clientId` to a real `mc-clients` record; create it first otherwise.
- Money values are plain decimals; `currency` is presentation only.
```

The `schema.json` is §1 made literal — the spec a user can diff and version — and a Zod validator (`CollectionSchemaZ`) gives §2 for free: a malformed schema is rejected at load with a localized reason, never crashing the host. The finite field-type vocabulary is §3, and each record / field is the §4 editing unit. Part 1 asked who guarantees that a generated table computes what it claims; the `derived` field is the literal answer — the agent is forbidden to write `total`, and the host recomputes it from the line items on every render. The escape hatch is the **`actions` mechanism**: "Generate PDF" can't be expressed declaratively — laying out a document and writing a file is real work — so the schema doesn't try. The button hands off to an `office`-role chat seeded from `templates/invoice-pdf.md`, dropping to the most expressive layer there is (an agent with tools) exactly where the DSL runs out. Business logic as prose, behind a declarative door.

> The Collections idea — applications as data, the schema as a user-authored harness, the model as the runtime — is developed at length in Part 4 of this series.
