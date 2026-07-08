# Article Series Plan — "Beyond the Sea of App Icons"

**Status**: Planning. Created 2026-07-08.
**Deliverables**: 6 Markdown articles (this folder) + 6 companion MulmoScript presentations (`mulmoclaude/vision/*.json`).

**Context** (self-contained — this plan should work in a fresh session):
Satoshi Nakajima is publishing a public series articulating his AI-native
computing vision, distilled from nine draft documents in `../docs/`. Hard
requirements from him: (1) **not promotional** — MulmoClaude/MulmoChat is only
a reference implementation, never the subject; (2) readable by non-technical
readers yet compelling for tech-savvy ones; (3) the **two-pillar theme**
(below) emphasized throughout — his own addition, reflecting how his thinking
evolved from NLUI (2025 docs) to on-demand generation (2026 essays).

**File map**:
- `../docs/*.md` — the nine source drafts (do not publish as-is)
- `PLAN.md` — this file, the working spec
- `research-notes.md` — verified citations for the "death of software /
  headless apps" discourse + per-article citation map
- `research-notes-mcp-apps.md` — MCP-UI / MCP Apps (SEP-1865) positioning for
  Article 2
- `mulmoclaude/vision/*.json` — MulmoScript drafts (first drafts; replace —
  see "Existing MulmoScript drafts" below)
- Repo `CLAUDE.md` — how to validate (`npm run validate`), preview
  (`npm run preview`), and render (`npm run movie`) MulmoScripts

**Open decisions (Satoshi's to make — don't assume)**:
1. Publish Article 5 first as a standalone teaser, or run 1→6 in order?
2. Will `gui-chat-protocol` (npm) claim interop/alignment with MCP Apps in
   print? Article 2 needs one plain sentence either way.
3. Venue and cadence (not discussed yet).
4. Final series title ("Beyond the Sea of App Icons" is the working name).

---

## What the series argues

The AI-native future of computing rests on **two pillars**, and the thesis is their fusion:

1. **The computer that understands** (NLUI) — natural language becomes the primary
   interface; users express intent instead of navigating apps.
2. **The computer that builds** (on-demand code generation) — the AI generates the
   GUI, the database schema, and even the business logic, fitted to a specific
   user, in the same conversation that expressed the need.

Each pillar alone has a known ceiling. Understanding without generation is a
concierge over fixed apps (Siri's limit). Generation without understanding is a
tool for programmers only (Copilot's limit). Together, **software materializes
from intent** — and the app, as a unit of software, dies twice: users no longer
choose apps, and apps no longer need to pre-exist.

Use the two pillar names **consistently in every article** so the series reads as
engineered, not accreted.

## Editorial rules (apply to every article)

- **Naming (Satoshi's directive, 2026-07-08): never write "MulmoChat" —
  always "MulmoClaude."** This applies to all published articles and scripts,
  including references to the 2025 prototype work (say "an open-source
  prototype" / "the reference implementation, MulmoClaude"). Do not link the
  MulmoChat GitHub repo in published pieces.
- **The feature-ratchet argument (Satoshi's addition, 2026-07-08) is a series
  theme.** Software historically grows by accreting features to justify higher
  prices (example: graphing, re-implemented in the spreadsheet, project
  tracker, CRM, notes app — each more complex and expensive for it). The
  AI-native answer: give the capability to the LLM layer once (a shared
  `presentChart`), not to each app — so one capability is reused across every
  scenario and each application stays slim: **database schema + business
  logic + basic UI + custom LLM-generated UI**. Introduced in Article 1 ("The
  feature ratchet" section); Article 2 develops it as the presentation
  toolkit; Article 4 makes it the "domain plugins stay narrow" structural
  argument. Analogy: no Mac app ships its own scroll bar.

- **Non-promotional.** MulmoClaude/MulmoChat appears only as "the reference
  implementation I built to test this," in first person, in the last third of
  each piece, with a repo link. Never in titles. Every claim gets at least one
  non-Mulmo example (spreadsheets, Claude Code, ChatGPT, Karpathy's LLM OS,
  generative-UI products). No "Benefits for X" sections — show benefits in
  stories.
- **Dual audience, layered depth.** Open with a concrete scene, not a thesis.
  One idea per article. One quotable sentence per article (candidates listed
  below). Mechanism in the last third; specs/JSON/TypeScript only in appendices
  or the repo. A non-technical reader who stops before the appendix loses nothing.
- **Honest costs.** Every article has one section arguing against itself
  (correctness, sprawl, trust). This is the strongest anti-promotional signal.
- **Personal arc.** Where natural, narrate the author's own trajectory: "I
  thought the revolution was understanding (2025); building the prototype taught
  me the second half is generation (2026)."
- **Length**: ~1,500–2,500 words each. Exception, learned from the Article 1
  judge panel (2026-07-08): Article 1 may run to ~2,800 — none of three
  independent drafts fit scene + discourse map + differentiation in 2,500.
- **Companion video is the entry point, not a summary.** ~10–12 beats, ends with
  "read the full essay." Reuse the shared slide theme from
  `mulmoclaude/vision/gui-chat-protocol.json`.

## Voice and taste (the register, made explicit)

The rules above say *what* to include; this section is *how it should sound*.
When in doubt, the 2026 essays (`software-for-one.md`,
`workspace-is-the-agent.md`) already have the right voice; the 2025 docs
(`LLM_OS.md`, `WHITEPAPER.md`) often have the wrong one. The difference:

**1. A researcher reporting, not a founder pitching.** First person singular.
Built things appear in past tense, as experiments with findings — including
findings that surprised or disappointed.

> ✗ "MulmoChat enables both information generation and collection through one
> unified conversational interface — the essence of an AI-native user
> experience."
> ✓ "I built a prototype to find out whether a form could emerge from a
> conversation instead of being designed in advance. It could. The interesting
> part was what broke."

The product appears in a subordinate clause; the *finding* carries the
sentence. Enthusiasm is allowed for ideas, never for artifacts.

**2. Concreteness beats category words.** Name the actual artifact.

> ✗ "The agent can generate bespoke visualization interfaces on demand."
> ✓ "My restaurant list is drawn as a Tokyo subway map. Nobody would ever
> build that product. It took one sentence."

If a paragraph has no named, specific thing in it (a file, a person, a date,
a quote), rewrite it or cut it.

**3. Steelman before differentiating.** When engaging competing work, state
its strongest form first, credit precisely (names, dates), then locate the
actual disagreement — which is usually smaller and sharper than it first
appears. Model: the MCP Apps treatment in `research-notes-mcp-apps.md` — we
credit MCP-UI as the pioneer (it predates the whitepaper by 5 months), note
that MCP Apps' fixed templates are a deliberate security decision rather than
a limitation, and only then draw the pen question. Convergent evolution is
claimed as *validation*, never priority. The reader should feel the author
would pass an ideological Turing test for the other side.

**4. Epistemic hygiene is part of the style.** Quote transcripts, not
headlines (Nadella said "probably... all collapse"; he did not say "SaaS is
dead" — preserve his hedge). Scope empirical results honestly (SaaS-Bench's
<4% is GUI-driving agents, end-to-end only). Never cite the two refuted claims
in `research-notes.md`. Tech-savvy readers grant trust on exactly this.

**5. The honest-cost section is an argument, not a disclaimer.** Its job is to
be the best available statement of the objection — ideally one that advances
the thesis when answered. Model: Bain's defense of SaaS (harden logic into the
data model) is not waved away; it is read as a *specification* of what the
AI-native version must own, relocated from vendor to user. A paragraph that
merely concedes "challenges remain" is cut.

**6. Quotable lines are earned, not asserted.** One per article, placed
*after* the story that makes it true — never as the opening claim. "The code
is disposable; intent and data are the asset" works because six named views
precede it.

**7. Banned register.** Superlatives ("revolutionary", "game-changer",
"seamless", "the essence of"), exclamation marks, "unlock/empower/leverage",
rhetorical questions as section openers, and any sentence whose subject is a
product name doing something admirable. The 2025 docs' "Benefits for X"
structure is the format-level version of this — already banned above.

## Existing MulmoScript drafts — replace, don't keep

Three first-draft scripts exist in `mulmoclaude/vision/` (`gui-chat-protocol.json`,
`dsls-as-harnesses.json`, `software-for-an-audience-of-one.json`). Satoshi has
okayed deleting/replacing them. They are essay-shaped, not video-shaped; when
each article is drafted, author its script fresh (reuse only the params/theme
blocks) and fix these specific faults:

- **One idea per beat, glanceable slides.** No 6-row tables or dense two-column
  comparisons — a slide must be absorbable in ~3 seconds while the viewer
  listens. Split dense sections across beats or cut.
- **Scene before abstraction.** Open with the story (subway map, Maria, the
  receptionist), not the thesis quote. Big quotable lines land mid-deck, after
  the story earns them.
- **Write narration as spoken language.** Short sentences. No "∴", no nested
  clauses, no essay diction read aloud. Read it out loud before validating.
- **Series identity in every script**: the two pillars named, "part N of the
  series" positioning, closing beat that points to the full essay.
- **Vary the visuals**: mix in generated images (`imageParams` is already
  wired) between slide layouts to give the deck air.

## Positioning research (done)

- `research-notes.md` — the "death of software / headless applications"
  discourse, adversarially verified (Nadella BG2, Karpathy Software 3.0,
  Vercel generative UI, Ink & Switch malleable software, Appleton/Sloan
  personal software, Bain 2025, SaaS-Bench, refuted claims to avoid). Includes
  a per-article citation map and the headline finding: **the
  application-becomes-data thesis has no verified owner in the discourse** —
  the fusion quadrant (agent authors GUI + schema + logic) is unclaimed.
- `research-notes-mcp-apps.md` — MCP-UI / MCP Apps (SEP-1865) timeline and
  comparison for Article 2.

Key positioning line to defend: the common "headless app" thesis keeps the
schema and business logic fixed and lets AI supply the interface. This series
claims more — AI generates **all three layers** per user. Not just AI-*operated*
software; AI-*authored* software. Cite the existing discourse; do not duplicate it.

---

## Article 1 — Beyond the Sea of App Icons

**Status: DRAFTED** (2026-07-08) — `01-beyond-the-sea-of-app-icons.md`,
awaiting Satoshi's review. Produced via a 3-draft judge panel (drafts and
comparison memo preserved in `drafts/`); base = scene-first draft + grafts
(the "unclaimed square" map paragraph, the two-sided Karpathy steelman,
"Understanding was the door; generation was the room") + the feature-ratchet
section + MulmoClaude-only naming.

**File**: `01-beyond-the-sea-of-app-icons.md`
**The one idea**: Apps solved capability, never intent. When the computer both
understands and builds, the app dissolves as the unit of computing.
**Pillar emphasis**: introduces **both pillars** and the "app dies twice" frame.
**Quotable line (settled — all three panel drafts converged on it)**: "The app
dies twice: you stop choosing apps, and apps stop needing to pre-exist."
(Retired: "The ultimate interface is understanding itself" — do not reach for
it in later articles either.)

**What to write** (this is the only article requiring real writing — a merge of
four overlapping drafts):
- Opening scene: the glittering sea of icons; Maria the soap maker (from
  `LLM_OS.md` abstract) spending 20 minutes managing apps instead of her business.
- The history compressed: CUI → GUI → chat, and why chat alone is not the answer
  (linear, no canvas) — from `VISION.md` §3.
- The ChatGPT moment: interaction unit changed from query to conversation — from
  `VISION.md` §2, heavily condensed.
- **State the two pillars explicitly** (new material; see thesis above). This is
  where "death of software" discourse gets cited and differentiated
  (research-notes.md).
- One orchestration walkthrough — pick ONE example (the Q4 board presentation
  from `VISION.md` §7 or the Kyoto trip from §5), not four.
- Honest-cost section: discovery ("how do you know what to ask for?"), trust,
  and the reliability question — deferred to articles 3 and 5 with forward links.
- Close: series roadmap in two sentences; first mention of the reference
  implementation, one paragraph, with link.

**Source docs** (merge; do not port wholesale):
- `../docs/VISION.md` — narrative voice, CUI→GUI→chat history, examples (§2–§7)
- `../docs/LLM_OS.md` — Maria scene, capability-vs-app table, evolution phases
- `../docs/WHITEPAPER.md` — taxi-driver metaphor (§1.2), Man-Machine-AI framing;
  leave the architecture for article 2
- `../docs/AI_NATIVE_OS.md` — the tightest existing prose; steal its register
- `research-notes.md` — citations for the discourse positioning

**Cut from sources**: the four-way repetition of the icon-sea metaphor; all
"Benefits" tables; the plugin interface code (moves to article 2's appendix).

**Companion MulmoScript**: `mulmoclaude/vision/beyond-the-sea-of-app-icons.json`
— the icon-sea visual, the two-pillars slide, one orchestration story, roadmap.

---

## Article 2 — Chat Needs a Canvas

**File**: `02-chat-needs-a-canvas.md`
**The one idea**: Conversation is the wrong shape for creation — the fix is not
going back to apps, but letting tools return interfaces, not just text.
**Pillar emphasis**: pillar 1's mechanics, plus the first seed of pillar 2
(the UI itself is generated into the conversation).
**Quotable candidate**: "Chat taught computers to listen. GUI taught them to
show. The future must let them do both — at once."

**What to write**:
- Opening scene: the hospital receptionist or recipe-guide flow (forms generated
  mid-conversation) from `GUI_CHAT_PROTOCOL.md` / `AI_NATIVE_OS.md`.
- Why linear chat fails creation: designers need canvases, analysts dashboards —
  from `VISION.md` §3.
- The core mechanism in prose: a tool call returns two payloads — words for the
  model, a typed interface for the human. No new architecture; an enhancement of
  function calling every LLM already supports.
- **The convergence section** (see `research-notes-mcp-apps.md`): three
  independent efforts arrived at this — MCP-UI (May 2025, Salomon/Yosef),
  OpenAI's Apps SDK (Oct 2025), GUI Chat Protocol (Oct 2025) — and Anthropic +
  OpenAI cosigned the MCP Apps standard (SEP-1865, Nov 2025). Cite as
  validation; **do not claim novelty for the mechanism** (MCP-UI predates the
  whitepaper by ~5 months; credit it as the pioneer).
- **The differentiation — the pen question**: MCP Apps lets the *app* return a
  certain UI (developer-authored template; the LLM can only trigger it, never
  shape it — and the security model depends on that fixedness). GUI Chat
  Protocol lets the *LLM* present rich UI: the model authors the payload at
  runtime — designs the form's fields, composes the document, picks the
  visualization — through generic presentation primitives (intent → DSPL →
  GUI). Framing lines: "MCP Apps standardizes how apps move into the chat. The
  question worth asking next is what happens when there is no app to move." /
  "In MCP Apps, the app holds the pen; here, the model does."
- Bidirectionality: GUIs that collect input, not just display output (the form →
  JSON round-trip).
- Roles: an application defined as tool-list + system prompt, no code — the
  bridge toward article 4's "applications become data."
- Honest-cost section: if vendors ship widgets into chat, the sea of icons
  migrates into the conversation rather than dying — interactive UI in chat is
  necessary but not sufficient. Plus: single point of interpretation, latency,
  wrong-tool selection.
- Reference implementation paragraph: state the MCP Apps relationship plainly
  (congruent mechanism; adds the presentation toolkit, roles, generated views).
  Appendix: the `ToolResult` shape and one worked example (from `WHITEPAPER.md`
  appendices, trimmed).

**Source docs**:
- `../docs/GUI_CHAT_PROTOCOL.md` — primary source (concept, examples, roles)
- `../docs/WHITEPAPER.md` — LLM-MVC framing, dual-channel `ToolResult`, appendices
- `../docs/AI_NATIVE_OS.md` — DSPL framing, spreadsheet-by-conversation example
- `research-notes-mcp-apps.md` — MCP-UI / MCP Apps timeline, comparison table,
  positioning (done, in this folder)
- Non-Mulmo anchors: MCP Apps (SEP-1865), OpenAI Apps SDK, Claude Artifacts,
  ChatGPT Canvas, Vercel generative UI (verify against `research-notes.md`)

**Companion MulmoScript**: `mulmoclaude/vision/gui-chat-protocol.json` — a
first draft exists; replace it per "Existing MulmoScript drafts" above (add the
two-pillar frame, the pen question, and the convergence story).

---

## Article 3 — DSLs as Harnesses

**File**: `03-dsls-as-harnesses.md`
**The one idea**: A deliberately limited language is what makes AI-generated
software trustworthy for someone who cannot read code.
**Pillar emphasis**: pillar 2's **safety problem** — generation is only useful if
its output can be constrained, validated, and sandboxed.
**Quotable candidate**: "A DSL is a powerful harness precisely because it gives
up power." / "Take the harness away and you have an untrained user holding a
loaded code generator."

**What to write** (lightest edit — the source essay is nearly publication-ready):
- Keep the essay's structure: the claim, the four harness properties
  (schema-as-record, free validator, grammar-as-forcing-function,
  unit-of-context), the escape-hatch hazard, "why this matters more as models
  improve."
- Keep **vibe crafting** as the centerpiece section — it is the user-facing name
  for pillar 2 made safe.
- Add: explicit connection to the two-pillar frame (generation needs a harness
  the way understanding needs a canvas).
- Add one non-Mulmo example alongside MulmoScript/Collections: SQL, Terraform,
  or spreadsheet formulas as familiar DSL-harnesses; the SWE-agent linter story
  is already there — keep it.
- Soften: "MulmoClaude's collections feature" → "the collections system in my
  reference implementation"; trim internal cross-references to companion essays
  into forward/back links within the series.
- Appendix: keep §A (MulmoScript) and §C (collection schema); consider dropping
  §B (recurring payments) or compressing it — three appendices is a lot.

**Source docs**:
- `../docs/dsl-as-harness.md` — primary source, near-verbatim
- `../docs/collections-architecture.md` — "harness" vocabulary consistency check

**Companion MulmoScript**: replaces the existing
`mulmoclaude/vision/dsls-as-harnesses.json`. The appendix of the source essay
contains a draft MulmoScript about itself; the meta-move (a DSL-authored video
about DSLs) is worth keeping as an explicit beat.

---

## Article 4 — Applications Become Data

**File**: `04-applications-become-data.md`
**The one idea**: schema + records + an LLM runtime = a complete application.
The AI generates all three layers — GUI, schema, business logic — not just the
interface.
**Pillar emphasis**: pillar 2 in full. This is the article that engages the
"headless application" discourse head-on.
**Quotable candidate**: "The records are data. The schema is the application.
Claude is the runtime." (genericize: "the model is the runtime")

**What to write** (merge of two sources):
- Opening scene: an invoice tracker or restaurant guide coming into existence
  from a sentence — no database server, no deployment.
- The core equation: `schema.json + records + model = application`; the
  four-systems collapse (database, ORM, UI framework, workflow engine) — from
  `collections-architecture.md`.
- **The headless-app engagement** (new material, from `research-notes.md`): the
  discourse says AI replaces the interface over fixed logic; this architecture
  goes further — the schema and business logic are themselves generated,
  per user. "Business logic becomes language."
- The inversion topology from `AI_NATIVE_BUSINESS_APP_ARCHITECTURE.md`: the API
  as product, GUI and LLM as peer clients — include the two-clients diagram as a
  real visual; the accounting example works because invariants are the value.
- Where the pattern earns its keep (invariants: accounting, scheduling,
  contracts) vs. where the plugin layer disappears entirely (notes, bookmarks).
- Honest-cost section: who validates a generated schema? The host/model
  responsibility split table; "extend the declarative layer only when it
  outperforms the agent."
- Reference implementation paragraph; appendix: one full schema example
  (invoices, from `dsl-as-harness.md` §C, if not already used in article 3 —
  coordinate to avoid duplication).

**Source docs**:
- `../docs/collections-architecture.md` — primary source
- `../docs/AI_NATIVE_BUSINESS_APP_ARCHITECTURE.md` — the inversion, the shell,
  the accounting reference implementation
- `../docs/dsl-as-harness.md` §C — concrete schema artifact
- `research-notes.md` — headless-app citations (primary engagement point)

**Companion MulmoScript**: `mulmoclaude/vision/applications-become-data.json` —
the inversion diagram, the four-systems collapse, the equation slide.

---

## Article 5 — Software for an Audience of One

**File**: `05-software-for-an-audience-of-one.md`
**The one idea**: The marginal cost of bespoke software collapsed to near zero,
inverting the economics that forced fifty years of mass software. Code becomes
disposable; intent and data are the assets.
**Pillar emphasis**: pillar 2's **economics**.
**Quotable candidate**: "The code is disposable; intent and data are the asset."

**What to write** (lightest edit — strongest essay in the corpus; also the best
candidate to publish FIRST as a standalone teaser, since it needs zero technical
background):
- Keep everything: the six-views table (Tokyo subway map opener), the cost
  arithmetic, code-as-intermediate-representation, the honest spreadsheet/no-code
  precedent (§4 — the "double removal" is the two-pillar argument in economic
  form; make that link explicit), and §5's correctness-relocation section.
- Soften workspace references: "one MulmoClaude workspace" → "the workspace of
  my reference implementation"; keep the table of views — it is the evidence.
- Adjust companion-essay links to series-internal links (this becomes
  back-reference to 3 and 4, forward to 6).
- Add citations from `research-notes.md`: Robin Sloan's home-cooked app, Maggie
  Appleton's barefoot developers — this article's thread has named precedents in
  the discourse; cite them.

**Source docs**:
- `../docs/software-for-one.md` — primary source, near-verbatim
- `research-notes.md` — personal-software / end-user-programming citations

**Companion MulmoScript**: replaces the existing
`mulmoclaude/vision/software-for-an-audience-of-one.json` — the subway-map
story, the cost-arithmetic slides, the intent/code/data triptych, the
correctness-relocation warning.

---

## Article 6 — The Workspace Is the Agent (capstone)

**File**: `06-the-workspace-is-the-agent.md`
**The one idea**: When the agent authors applications into its own substrate,
the app/agent boundary dissolves — the workspace IS the agent, and building
software is how the agent grows.
**Pillar emphasis**: the **fusion**. The agent understands (pillar 1), builds
(pillar 2), and *keeps what it builds as itself* — the step neither pillar
implies alone.
**Quotable candidate**: "The workspace is the agent, and building software is
how the agent grows."

**What to write** (moderate edit):
- Keep: the code-vs-data workspace table (§1), Karpathy lineage (§1.1), the
  collection-skill-is-an-application argument (§2), dissolving boundaries (§3),
  the recognize → crystallize → tune → retire loop (§4), the reliability dial
  (§5), self-pruning (§6), forking/portability (§7).
- §8 (Nadella, owning the learning loop) — verify the quote/URL against
  `research-notes.md` and keep; it is the bridge from personal vision to
  enterprise stakes and the strongest close for the series.
- Add: explicit two-pillar closing — the series' final restatement.
- Soften: heavy MulmoClaude specifics (`config/roles/`, `mc-*` migration) into
  "in my reference implementation" framing; the trajectory argument (§3.4) stays
  because it is evidence, but one paragraph, not a section.
- Trim the arXiv self-reference (§1.1 note) or keep as a footnote.
- End the series where the paper ends: two ways software comes to exist, old
  phase / new phase.

**New argument (Satoshi, 2026-07-08) — the self-hosted 24/7 assistant.** The
workspace-is-the-agent architecture uniquely enables an always-on personal AI
assistant that lives on hardware you own, with phones/laptops as thin remote
windows into it. Google/Meta-style assistants are structurally cloud-resident
(the memory, learning loop, and personality live server-side — you *rent* your
assistant; hosting its self is their business model), so this topology is a
durable differentiator, not a feature race. It compounds §8: model-agnostic
AND location-sovereign. Lineage: local-first software (Ink & Switch) extended
from documents to agents — unclaimed in the verified discourse. Honest costs
to state: self-hosting ops burden (Appleton's barefoot gap), home PC ≠
datacenter (uptime/backup), and remote access to an agent that can act on your
whole life is a serious security surface. Lands as a short section after §7
(portability) / feeding §8's outward turn.

**Source docs**:
- `../docs/workspace-is-the-agent.md` — primary source
- `../docs/remote-host.md` — the solved remote-access mechanism (Firestore
  relay: outbound-only host, per-user auth scope, durable offline queue,
  sandboxed mobile views). §8's security cost is answered by this architecture;
  the honest residue kept in the article: commands/results transit a
  third-party cloud relay even though the assistant's self stays home.
- `../docs/collections-architecture.md`, `../docs/software-for-one.md` — for
  consistent back-references
- `research-notes.md` — Nadella verification

**Companion MulmoScript**: `mulmoclaude/vision/workspace-is-the-agent.json` —
the workspace table, the self-improvement loop diagram, the reliability dial,
the fork-is-cp-r slide, the closing restatement.

---

## Status (2026-07-08)

**All six articles AND all six companion MulmoScripts are DRAFTED**, validated
(6/6 via `npm test`), and cross-verified (naming, quotable uniqueness, pillar
consistency, "Part N of 6" identity, cross-references). Article 6 includes the
self-hosted-24/7 section with the remote-host relay answer. The old first-draft
scripts are gone: `dsls-as-harnesses.json` and
`software-for-an-audience-of-one.json` were replaced in place;
`gui-chat-protocol.json` was deleted (superseded by `chat-needs-a-canvas.json`;
CLAUDE.md's reference-example pointer updated to
`beyond-the-sea-of-app-icons.json`). Remaining: Satoshi's review pass of all
twelve artifacts, video rendering (`npm run movie`) per script after review,
and the four open decisions in the header.

## Order of work

1. `research-notes.md` — land the deep-research report here (in progress).
2. Article 1 — the only heavy writing task; sets the series register. Draft
   with its MulmoScript as a template pair.
3. Articles 5 and 3 — lightest edits, publication-ready fastest.
4. Article 4 — the merge + discourse engagement (needs research-notes).
5. Article 2 — revise existing `gui-chat-protocol.json` alongside.
6. Article 6 — last; capstone must reference final versions of all others.

Validate every MulmoScript with `npm run validate`; preview with
`npm run preview` before rendering video.

## Consistency checklist (run before publishing each piece)

- [ ] Two pillars named with the same words as the other articles
- [ ] Opens with a scene, not a thesis
- [ ] Exactly one idea; quotable line present
- [ ] MulmoClaude only as first-person reference implementation, last third
- [ ] At least one non-Mulmo example per major claim
- [ ] One honest-cost section
- [ ] No "Benefits" tables; no feature lists
- [ ] Code/JSON only in appendix; article readable without it
- [ ] Series-internal links (back/forward) instead of repo-internal doc links
- [ ] Companion MulmoScript validated and consistent with shared slide theme
