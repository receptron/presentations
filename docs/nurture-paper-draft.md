# Nurtured at Home: A Local-First Schema-as-Application Architecture for User-Owned Personal AI

*Working draft — title, abstract, and section outline. Companion document:
[nurture-paper-literature-scan.md](nurture-paper-literature-scan.md) (novelty map and
must-cite list, 2026-07-13). Target shape: systems paper (UIST / CHI systems track).
Revised 2026-07-13 after external review (Codex): narrowed to a single artifact-centered
contribution, empirical claims reframed as position/hypothesis, evaluation protocol
added, longitudinal study explicitly future work.*

## Scope decision (post-review)

One paper, one contribution: **MulmoClaude as a local-first schema-as-application
system for user-owned personal AI accumulation.** The economics argument is the
*motivation* (a position, not an empirical claim); the nurturing study is *future
work*; "premium features dissolve" and the GUI-protocol material are discussion
asides, not contributions.

## Abstract

Personal AI assistants are increasingly defined by what accumulates around the model —
memories, data, and applications — rather than by the model alone: every major vendor
now ships memory features that invite users to build up context on the vendor's
premises. We take a position on this arrangement: if accumulation is what makes an
assistant valuable, it is also what makes leaving costly, and remedies based on memory
portability carry only one layer of what a user accrues. A personal assistant, we
argue, should be nurtured at home — grown in an environment the user owns.

We present MulmoClaude, an open-source system that instantiates this position through
a schema-as-application architecture: the user describes what they need in natural
language; the model authors a small declarative schema; and a host runtime — not the
model — renders the interface, validates every record, and runs reconciliation and
recurrence over a plain-file workspace on the user's own machine. The model authors
the application; the host runs it; the records endure. We evaluate the architecture
three ways: (i) reliability — schema-generation validity and host-side rejection rates
across a corpus of app-creation tasks; (ii) capability — cross-application workflows
over accumulated personal data that neither memory export nor one-shot UI generation
supports; and (iii) a migration experiment quantifying what a memory export carries
versus what the workspace contains. We report the costs of local-first ownership
alongside its benefits, and outline the longitudinal questions the system opens.
The result is a working architectural blueprint — and an evidence base — for
personal AI whose accumulation remains with the person it describes.

## Section outline

### 1. Introduction

- Open with the observable fact (vendors racing to ship memory features; users already
  cultivating context on hosted platforms — CSCW '25 Digital Companionship: users
  believe they nurture their chatbot, back up chat logs, refuse to delete).
- State the position as a position: *if* accumulation is the value, it is also the
  switching cost, and it compounds. Frame as design stance motivating the system —
  explicitly not an empirical claim of this paper. (Per the lit scan: personalization
  payoff is itself contested, 2606.06614 — which strengthens the urgency of asking
  who owns the accumulation before the value question settles.)
- Contributions list (narrowed):
  1. The schema-as-application architecture: model-authored declarative schemas
     executed by a validating host runtime over a user-owned plain-file workspace.
  2. MulmoClaude, an installable open-source artifact implementing it end to end.
  3. An evaluation: schema-generation reliability, cross-application workflow
     capability against two baselines, and a migration experiment that measures the
     memory-export gap.
  4. A tradeoff analysis of local-first personal AI (what ownership buys, what it costs).

### 2. Related work

Positioning strategy per the literature scan — cite early, differentiate explicitly:

- **NL-to-declarative UI (primary axis).** Jelly (CHI 2025) — closest system; same
  anti-codegen motivation. Differentiation must be *demonstrated, not asserted*
  (→ Evaluation ii): persistence, record validation, reconciler/recurrence, real data
  over a personal store — all deferred in Jelly. Also Varv (CHI 2022), Potluck,
  GenerativeGUI, Generative UI (2604.09577), Software as Content (2603.21334).
- **Portability as remedy (second axis).** Portable Agent Memory (2605.11032), SAMEP
  (2507.10562). Shared problem statement; our rebuttal is the migration experiment
  (→ Evaluation iii): what fraction of the workspace's operative state rides a memory
  export.
- **Memory as substrate.** Mem0, MemGPT, MemoryBank, hosted memory features —
  accumulation-as-mechanism, no ownership discussion.
- **Nurturing agents.** Nurture-First (2603.10808) claims the metaphor for
  domain-expert agents; we ask *where* the nurturing happens. One paragraph, not a pillar.
- **Malleable software and local-first.** Ink & Switch essays; Robin Sloan. Apps-for-one
  is theirs; our delta: agent-composed, economics-motivated, evaluated.
- **Accumulation economics (motivation only).** Arrow (1962), Hayek (1945); Nadella's
  Reverse Information Paradox (X, Jul 2026) as *secondary practitioner corroboration*,
  not scholarly support — cite once for the leakage/captivity distinction, keep the
  weight on Arrow/Hayek and the switching-cost literature (Klemperer, Shapiro & Varian).
- **Agent-GUI protocols.** MCP Apps, AG-UI, A2UI, Apps SDK — one paragraph situating
  gui-chat-protocol as the artifact's implementation choice, no novelty claim.
- **Agent substrates.** The Log is the Agent (2605.21997) — complementary runtime layer.

### 3. Motivation: accumulation, lock-in, home (position, ~1.5 pages)

- The economics as design rationale, hedged: Arrow's Information Paradox and its
  AI-age inversion; Hayek's knowledge of particular circumstance; classic
  switching-cost economics applied to accumulated assistant state.
- Leakage vs. captivity as two distinct failure modes of hosted accumulation; map
  existing remedies (tenant boundaries → leakage; portability protocols → part of
  captivity) and state the ownership hypothesis: local-first addresses both — *at a
  cost*, analyzed in §7.
- Define "nurtured at home" operationally: plain files, open source, local execution,
  relay-only remote access — each property tied to the specific failure mode it
  removes (shutdown, repricing, acquisition, export lock), stated as design goals
  the evaluation then exercises where measurable.

### 4. Design commitments (condensed from the manifesto, ~1 page)

1. The agent is a universal controller — joins, not replaces, the UI.
2. Chat summons GUIs — bidirectional modality choice, including agent-requested forms.
3. The protocol is open and extends MCP.
4. The accumulation belongs to the user — the commitment the other three serve.

### 5. Architecture: schema as application

- The collection mechanism: NL → small declarative schema; host renders (table /
  kanban / calendar), validates every record, runs the reconciler (reminders,
  recurrence). Corrected slogan: **the records are data, the schema is the
  application, the model is the author, the host is the runtime.**
- Implementation depth (required by systems reviewers — this is not a thin schema
  wrapper over files, and the paper must show it):
  - *Schema language*: the full declarative surface — field types, relations,
    done-marker, reminder and recurrence declarations — with the grammar/JSON-Schema
    definition and a complete example schema as a figure.
  - *Validation semantics*: what is checked, when (authoring time vs. record write),
    how errors surface to the agent and to the user, and the guarantee: an invalid
    application never executes.
  - *Beyond static validity — semantic mismatch and runtime faults*: static
    validation cannot catch a schema that is grammatically valid but contradicts the
    user's intent; the architecture's answer is the cheap re-authoring loop (the user
    says the sentence again; the schema is disposable, the records endure) plus
    runtime error surfacing — data contradictions detected by the reconciler are
    raised through defined channels to both the agent (for self-correction) and the
    user (for judgment), never silently absorbed.
  - *Reconciler and recurrence model*: the tick model, recurrence-advancement rules,
    reminder firing — specified precisely enough to be checked against the E1 oracle.
  - *Plugin boundary*: the MCP tool surface and the gui-chat-protocol runtime
    interface (pub/sub channels, scoped dispatch, error isolation) — what a plugin
    consumes vs. what the host implements.
  - Architecture figure: model-author / host-runtime split with the trust boundary
    drawn explicitly.
- Trust boundary: everything the model authors is validated before it runs; views,
  reconciler, and recurrence are engine code that never guesses. Invalid applications
  never execute.
- Honest persistence description: plain-file workspace; append-only islands (chat
  transcripts, accounting journal with compensating entries, wiki snapshot history)
  vs. mutable subsystems — why correctness-critical subsystems independently
  converged on logs.
- Worked examples (now feeding the evaluation, not replacing it): accounting
  (API + UI + agent; receipt photo → same API), a collection built in one
  conversation, cross-plugin composition.
- Sharing: schema registry — apps-for-one compose into a commons.

### 6. Evaluation (new — the section the paper stands on)

Three questions, matching the three claims a skeptical reviewer will test:

**E1 — Is model-authored + host-validated reliable enough to trust?**
- Corpus of N app-creation requests (drawn from real collection categories: trackers,
  lists, drills, recurring obligations; varied phrasing, two languages).
- Measure: valid-schema rate on first attempt; retry convergence; host-side rejection
  rate (invalid schemas caught before execution — the trust-boundary claim,
  quantified); record-validation catch rate on deliberately malformed records;
  reconciler/recurrence correctness against a hand-built oracle (due dates,
  recurrence advancement, reminder firing).

**E2 — Does the combination change what users/agents can do?** (the Jelly
differentiation, demonstrated — with a non-strawman baseline strategy)
- Task suite of cross-application personal workflows over an accumulated workspace
  (e.g., receipts → ledger → quarterly chart; wiki agreement → recurring obligation;
  feed items → collection records).
- Baseline strategy (three tiers, each answering a different "why not X?"):
  - (a) **Ablation baseline — the Jelly-class comparison.** Jelly itself is not
    publicly runnable and was evaluated on generated data, so it cannot be fairly
    operationalized directly; state this explicitly, then reproduce its architectural
    point as an ablation of our own system: same model, same schema→UI generation,
    with persistence, record validation, and the reconciler *disabled*. This isolates
    exactly the components we claim matter, under otherwise identical conditions —
    fairer to Jelly than a reimplementation, and immune to the strawman objection.
  - (b) **Hosted-assistant baseline.** A production assistant with memory but no host
    runtime (chat + one-shot artifacts) — the status-quo competitor.
  - (c) **Codegen baseline.** The same tasks via vibe-coded one-off apps (agentic
    codegen) — the "generate code instead of schema" alternative the anti-codegen
    argument must beat on iteration and durability.
- Measure: task completion, steps/turns, error classes; for each baseline, which
  tasks are *impossible* and which architectural absence causes it (no persistence;
  no validation; no recurrence; no cross-app state).

**E3 — Migration experiment: what does a memory export carry?** (the captivity claim,
made empirical — with an auditable metric, not a constructed one)
- Take a workspace nurtured over weeks (dogfooding data, disclosed as such).
  Export what portability protocols cover (conversational memory). Attempt to
  reconstitute the assistant's behavior elsewhere.
- No single "X%": a weighted scalar over heterogeneous artifacts invites the
  constructed-result objection. Two complementary measures instead:
  - **Transfer matrix (descriptive).** Enumerate workspace state as a typed
    inventory — records, schemas, recurrence/reminder state, wiki pages, memory
    topics, automations, plugin data, generated app behaviors — from the workspace
    directory structure itself (the coding scheme is the file layout, independently
    auditable). Report per-type: carried / degraded / lost. No cross-type weighting.
  - **Task replay (functional).** Re-run the E2 task suite against the migrated
    target; report per-task completion delta. This sidesteps artifact weighting
    entirely — the denominator is tasks, defined before the experiment.
- Result format: a transfer matrix plus "N of M workflow tasks still complete after
  memory-only migration" — the accumulation-is-more-than-memory rebuttal as data.

**E4 — Formative usability signal** (added per review: can non-authors do this?)
- Small task-based formative study, 6–10 participants who are not authors: create a
  collection of their own choosing by conversation, then perform two prescribed
  workflows over it.
- Recruiting criteria (stated explicitly — this is what makes the no-code claim
  testable): general knowledge workers with no programming experience and no
  AI-coding-tool experience (Cursor, Copilot, Claude Code, etc.); prior LLM exposure
  limited to chat use. Report the screening instrument.
- Measure: unassisted success, time, points of confusion, and what participants ask
  for that the schema language cannot express; standard short usability instrument
  plus think-aloud.
- Framed strictly as formative (does the interaction work at all for non-authors?),
  not summative — the longitudinal study remains future work.

Scope honesty: E1–E3 are artifact evaluations and E4 is formative; no claims about
long-term user behavior or adoption are made.

### 7. The costs of home (expanded tradeoff analysis — was a bullet, now a section)

- What ownership costs, treated symmetrically with what it buys: install and setup
  burden; backup responsibility (no vendor durability); single-machine availability
  and sync limits of relay-only access; security surface of a local server; model/API
  dependence (local-first ≠ model-independent — the engine is still rented; mitigation:
  orchestration decoupled from any single model, workspace unchanged across engine
  swaps); the nontechnical-adoption gap.
- For each cost: current mitigation in the artifact, or honest statement that it is
  unmitigated. This section exists so the paper argues a *tradeoff*, not a free lunch.

### 8. Discussion

- Premium-features-dissolve as an observed consequence of composition (one paragraph,
  discussion aside — not a contribution; cite unbundling literature as context).
- What the artifact cannot yet show: longitudinal nurturing. Design sketch for the
  study (what people build, whether accumulation measurably changes capability, where
  the metaphor breaks) — explicitly future work, citing the n=1 Nurture-First case
  study as the current state of evidence.
- Generalization: which parts are MulmoClaude-specific vs. portable design patterns
  for any local-first agent host.

### 9. Conclusion

- Return to the opening, now hedged honestly: the question of who owns the upbringing
  is being decided by defaults; this paper contributes a working alternative default
  and evidence about what it can and cannot do.

## Notes

- Review feedback incorporated (2026-07-13, Codex, round 1): abstract reframed from
  assertion to position; contributions narrowed to artifact + evaluation; evaluation
  protocol added (E1–E3); local-first tradeoffs promoted to a full section; slogan
  fixed ("model is the author, host is the runtime"); Nadella demoted to secondary
  corroboration; premium-dissolve demoted to discussion.
- Review feedback incorporated (2026-07-13, Codex, round 2 — verdict upgraded to
  plausible weak/borderline accept): E2 baseline strategy made non-strawman (ablation
  as the Jelly-class comparison, with explicit justification for why Jelly cannot be
  operationalized directly; hosted-assistant and codegen tiers); E3 metric made
  auditable (typed transfer matrix with the file layout as coding scheme + task-replay
  functional measure, replacing the weighted "X%"); implementation-depth requirements
  spelled out in §5 (schema language, validation semantics, reconciler model, plugin
  boundary, architecture figure); E4 formative usability study added.
- Review feedback incorporated (2026-07-13, Gemini — verdict: execute as planned,
  strong-accept potential): abstract closing impact sentence added (measured version,
  not Gemini's "user-sovereign computing" phrasing, to stay consistent with the
  hedged position framing); semantic-mismatch and runtime-fault handling added to §5
  implementation depth (re-authoring loop + reconciler error surfacing); E4
  recruiting criteria specified (no programming, no AI-coding tools, chat-only LLM
  exposure).
- Re-run the literature scan immediately before submission.
- Author-voice pieces to reuse: MANIFEST.md, the assistant-you-nurture essay/deck.
- Venue candidates: UIST (systems) primary; CHI systems alternate. The economics
  position could be flagged separately in a short Interactions / CACM essay or
  workshop paper; the longitudinal study targets CHI/CSCW as paper two.
