# Applications Become Data

*Part 4 of the series "Beyond the Sea of App Icons."*

Maria — the soap maker from Part 1 — has a new problem, and it is the good kind: wholesale accounts. A dozen shops now stock her soap, and the invoices have outgrown the folder of PDFs she was keeping. So she says to her computer: *"Track the invoices I send my wholesale accounts — who has paid, who is late, and what each order was."*

A moment later there is an invoice tracker. A list, one row per invoice: client, amount, due date, status. Overdue rows are flagged; a running total of what she is owed sits at the top, and it is correct. Each record opens into a proper detail form — line items, a computed total she cannot accidentally overwrite. A week later she adds, mid-conversation, "I need the shop's purchase-order number on these," and the application changes shape while she watches.

Now inventory what did *not* happen. She did not evaluate vendors, create an account, or start a subscription. Nothing was installed, no database server was provisioned, no code was deployed anywhere. There is no company whose roadmap decides what her tracker becomes next. The application did not exist, and then it did, inside one sentence.

Part 1 argued that AI-native computing rests on two pillars — **the computer that understands** and **the computer that builds** — and promised to follow the second pillar all the way down. This article is the bottom: what an application actually *is*, once a machine can build one.

## What is left when the software is gone

Look at what came into existence on Maria's disk: a schema — a few dozen lines of JSON declaring the fields, their types, which status values mean an invoice is settled, and a formula for the total — and records, one small file per invoice. The third ingredient is not on disk at all: the model that reads both.

Set that against the traditional application stack, which is four separate systems: a **database** to hold the records, an **ORM** to translate between storage and program objects, a **UI framework** to put the records on screen, and a **workflow engine** to make things happen on schedule. Walk through where each went.

The database became plain files: records live in the user's workspace as JSON, the files are the source of truth, and whoever owns the workspace owns the data — no vendor between Maria and her invoices. The ORM simply vanished: a language model reads the schema and the records directly, so there is nothing to translate. The UI framework became the host's rendering of the schema itself: from the field types alone, every collection gets a list, a detail form, and, where declared, calendar and kanban layouts. When field types cannot present the data well — a portfolio wants to be an allocation chart, a restaurant list wants to be a map — the agent writes a custom HTML view the host serves sandboxed: the presentation layer is itself a file inside the collection. And the workflow engine split in two: what must never guess — recurrence, notifications, feed ingestion, computed fields — runs deterministically in the host, driven by schema declarations; what requires judgment is written as prose the model executes.

None of this is exotic. A spreadsheet emailed between colleagues is already an application shipped as data — columns and formulas as schema, rows as records, the recalculation engine as runtime. Collections remove that bargain's ceilings: formulas that follow references into other files, views that are not grids, and a runtime that reasons instead of merely recalculating.

So the four systems collapse into one artifact plus one capability:

```text
schema.json + records + model = application
```

**The records are data. The schema is the application. The model is the runtime.**

## Business logic becomes language

The schema carries more than shape. A derived field is a spreadsheet formula that can cross file boundaries: declare a holding's value as `shares * ticker.price`, with the price in a different collection, and the portfolio revalues itself whenever the quote changes — no synchronization code, no update job, and the model is handed records with the values already computed.

The more interesting design decision is where the schema deliberately *stops*. Low-code platforms — Airtable, Retool, PowerApps — grow ever more elaborate formula languages and workflow builders, trying to make the declarative layer express everything. Collections stop earlier. A schema can declare that an invoice carries a button, "Record payment": when it appears, which role handles it, which instruction template it opens. The accounting logic behind the button is written in natural language. Bookkeeping conventions, compliance rules, how to chase a late payer politely — these are easier to state in prose than in any workflow language yet devised, and now there is a runtime that executes prose. Business logic becomes language.

This is Part 3's harness wearing work clothes: deterministically validated structure around judgment, with the authoring pen in the end user's hand.

## The inversion

Some applications are more than record-keeping. In a ledger, every entry must balance; in a scheduler, a room cannot be double-booked; a contract moves through states in one legal order. Here the rules are not decoration on the data — the rules *are* the application, and they should be enforced by code that never guesses. Even then, the AI-native shape differs from anything SaaS-shaped, because of where the interface sits.

A traditional business application is UI-centric:

```text
   ┌──────────────────────────────────────┐
   │                UI                    │   ← the product
   ├──────────────────────────────────────┤
   │         Business logic               │   ← behind the UI
   ├──────────────────────────────────────┤
   │             Database                 │
   └──────────────────────────────────────┘
```

The interface is the product; the API, if one exists, is a side door for integration partners. The AI-native topology inverts this:

```text
          [ LLM ]                 [  UI / View  ]
              \                       /
               \                     /
                ─────── API ────────
                         │
                 Business logic
                         │
                     Database
                  (file system)
```

The API is the product. Two clients call it as peers: a thin, fixed-schema interface for what a human wants to look at — a balance sheet that looks like a balance sheet — and a language model that reads the same API, calls the same operations, reasons about the same state. Because there is exactly one contract, a manual click and a model's tool call flow through the same handlers; there is no drift between what the interface can do and what the AI can do, because they are the same thing.

The pattern earns its keep exactly where the invariants are the value: accounting, scheduling, inventory, contracts. The other end of the spectrum deserves equal honesty: for notes and bookmarks, there are no invariants worth enforcing — the model edits the files directly and the plugin layer disappears entirely. Between the two sit collections: real structure, declaratively enforced, no code. Three tiers; take on machinery only as the invariants demand.

## The ratchet, followed all the way down

In Part 1 I described the feature ratchet — graphing re-implemented in the spreadsheet, the project tracker, the CRM, the notes app — and promised that Part 4 would follow the shrinking application all the way down. Here is the floor.

The accounting application in the inverted diagram above contains **no chart code**. Not a charting library, not a rendering routine, nothing. Graphing exists once, at the LLM layer, as a shared presenter — `presentChart`, from the same Part 2 toolkit as `presentForm` and `presentSpreadsheet`. Ask to see quarterly revenue, and the model reads a time series from the accounting API and hands the numbers to the presenter. The workflow "graph my Q3 revenue" exists nowhere as code. It exists only as the model's runtime decision to read from one plugin and write into another.

A Mac application does not implement its own buttons; the operating system supplies the widget, and every application draws on the same vocabulary. An AI-native application, likewise, does not ship a chart engine: the shell supplies the presentation vocabulary; the model supplies the dataflow glue. Two structural consequences follow. Domain plugins stay narrow: there is no incentive to absorb presentation features, because the model will pick a better presenter than any plugin author could inline. And presenters improve for everyone at once: a better `presentChart` upgrades the ledger, the portfolio, and the fitness log in the same release, without touching any of them.

So the slim application settles into four parts: **a database schema, the business logic, a basic UI, and whatever custom interfaces the model generates on request.** The ratchet's engine — features accreted to justify pricing tiers — has nothing left to grip: the capabilities it used to accrete now live in a layer no application owns.

## The discourse, and where this sits in it

Satya Nadella described the demand side. In Part 1 I quoted his December 2024 remark on the BG2 podcast: business applications will "probably... all collapse" in the agent era — "they are essentially CRUD databases with a bunch of business logic," and "the business logic is all going to these agents." He hedged, and the hedge should stand. But read from the architect's chair, that is very nearly the collections equation stated from the outside: a CRUD database is records plus a schema, and logic migrating to the agent tier is the model becoming the runtime. He named what collapses. He did not say what it collapses *into*.

The closest published answer is Vishwas Gopinath's "Agent-Native Architecture" essay at Builder.io (May 2026), the nearest cousin this architecture has. His prescription: build software so humans and AI agents operate the same product through shared actions, data, permissions, and context — define each action once, let the UI call it and the agent see it as a tool. That is the peer-clients inversion in the diagram above, published before this series; I take it as convergent validation of the topology. But notice what stays fixed: in agent-native architecture, the schema, the business logic, and the interface all remain developer-authored. The agent is granted equal *access*, not authorship. It can operate any action the developers defined; it cannot define one. That is where this article begins: Maria's tracker had no developer — its schema, its logic-as-prose, and its views were authored by the model, for her.

Bain & Company supplied the strongest counterargument. Their Technology Report 2025 essay on agentic AI and SaaS argues the moat was never the interface: "your data is your moat," and vendors survive by hardening logic into the data model — "build unique constraints — approval flows, state transitions, and compliance rules — right into your data model. Any external agent should have to validate through your system of record." As engineering this is exactly right — and it is what the inverted architecture already does: invariants in the domain module, every client validating through it. So I read Bain's defense of SaaS as something more useful than a rebuttal — a *specification* of what the AI-native version must own. The disagreement is not whether constraints belong in the system of record; it is who owns the system of record. Bain assumes the schema and its constraints stay with the vendor; here they live in the user's workspace, as files she can read, version, and take with her. The moat is real. It has moved.

Finally, the empirical result. SaaS-Bench, a May 2026 preprint, ran agents against 106 long-horizon tasks on 23 real SaaS systems; even the strongest models finished fewer than 4% end-to-end. The scope matters — it measured *GUI-driving* agents clicking through interfaces built for human hands, under a strict all-or-nothing standard, and it is not yet peer-reviewed — but read carefully it is evidence against an architecture, not against agents. Making a model impersonate a human in front of a vendor's interface is the wrong plan, which argues for exactly the inversion above: the agent never sees a GUI at all. It reads schemas and calls typed APIs, the interface it is actually good at.

Part 1 mapped this discourse and pointed at an unclaimed square: nobody claiming the AI authors all three layers — interface, schema, logic — per user. This article is that square, filled in: schema, logic, and interface authored by the model, owned by the user — the move Maria's sentence performed.

## The case against this

The obvious objection: a generated application comes from a system that is sometimes confidently wrong, for a user who cannot read a schema. Who checks the work?

The structural half of the answer was Part 3's whole subject, so I will state it rather than re-argue it: the host's validator. A schema is checked deterministically before it ever loads — a reference to a collection that does not exist, a recurrence that would respawn unboundedly — and rejected with a message the model can act on unattended. An invalid application never runs. Derived fields answer the arithmetic half: the model is forbidden to write a computed total, and the host recomputes it on every render.

The validator is one instance of a split that runs through the whole architecture:

| The host guarantees | The model provides |
| --- | --- |
| Schema validity | Workflow decisions |
| Record storage, path safety | Business reasoning |
| Deterministic computation | Semantic correctness |
| Rendering, sandboxing | Domain expertise |

The boundary is not fixed — as patterns prove out, a responsibility can migrate from prose into schema, right column to left. But the migration has a guiding rule worth writing on the wall: **extend the declarative layer only when it outperforms the agent.** Every key added to the schema language is complexity every future application carries; the workflow-engine graveyard is full of platforms that declared too much.

And a residue no validator reaches: a schema can be perfectly valid and quietly wrong — a tax formula that parses, computes deterministically, and applies the wrong jurisdiction's rate. Structural correctness is checkable; semantic correctness, for software with an audience of one, has no reviewer and no other users to hit the bug first. What "correct" means under those conditions is Part 5's question.

## Where I am testing this

The accounting example above is not hypothetical; it is the `manageAccounting` plugin in my reference implementation, MulmoClaude. I built it because accounting is where this architecture should fail first: the invariants are unforgiving. The domain module is a double-entry ledger — every entry must balance, the journal is append-only, corrections are reversing pairs, never edits — over a directory of plain files per book. One endpoint with an action discriminator serves both clients: a thin GUI on the canvas — journal, balance sheet, profit and loss — and Claude, over MCP, invoking the identical operations. In use I switch between clicking and asking without thinking about it, and there is no state drift — both modes are the same ledger through the same contract.

Two findings from building it. The composition genuinely happens at runtime: asking for a revenue graph produces a `getTimeSeries` call followed by a `presentChart` call — a pipeline that appears in no source file, in a plugin with no chart code. And the fixed GUI came out far smaller than I would have budgeted, because every request outside the canonical views — comparisons, projections, odd slices of the books — flows through the model instead of becoming a screen. Give the API a second client that can improvise, and most of the interface you were going to build turns out to be requests you can simply make.

Part 5 turns to the economics: when the marginal cost of software built for one person approaches zero, code becomes disposable and the correctness question above must be answered without reviewers. Part 6 ends where the logic ends: when the agent authors applications into its own workspace and keeps them, the boundary between agent and software dissolves.

---

## Appendix: the files are the database

The body claims the workspace is the data layer; here is what that looks like on disk for one accounting book in the reference implementation. This is the entire persistent state of the application — no database server, no proprietary format, every file inspectable with a text editor:

```text
data/accounting/books/<bookId>/
├── accounts.json          # the chart of accounts: id, name, type, opening balance
├── journal/
│   ├── 2026-01.jsonl      # append-only journal, one balanced entry per line
│   ├── 2026-02.jsonl
│   └── ...
└── snapshots/
    ├── 2026-01.json       # cached month-end balances, derived from the journal
    └── ...
```

The journal files are the authoritative record: append-only JSON Lines, one balanced double-entry transaction per line, corrections appended as reversing pairs. The snapshots are a pure cache — deletable and rebuildable from the journal at any time. Backing up the application is copying the directory; migrating away from it is reading the files; auditing it is opening them. The same property holds for every collection in the workspace: `schema.json` beside a folder of records. Applications become data, and data is just files the user owns.
