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
differentiation, demonstrated)
- Task suite of cross-application personal workflows over an accumulated workspace
  (e.g., receipts → ledger → quarterly chart; wiki agreement → recurring obligation;
  feed items → collection records).
- Baselines: (a) a hosted assistant with memory but no host runtime (one-shot
  generated UI / chat-only), (b) memory-portability-style export + generic tools.
- Measure: task completion, steps/turns, error classes; qualitatively, which tasks are
  *impossible* per baseline and why (no persistence; no validation; no recurrence; no
  cross-app state).

**E3 — Migration experiment: what does a memory export carry?** (the captivity claim,
made empirical)
- Take a workspace nurtured over weeks (dogfooding data, disclosed as such).
  Export what portability protocols cover (conversational memory). Attempt to
  reconstitute the assistant's behavior elsewhere.
- Measure: fraction of operative state carried (records, schemas, recurrence state,
  app behavior, cross-plugin workflows) vs. lost; enumerate failure cases. Result
  format: "a memory export carries X% of the artifacts and 0 of the running
  applications" — the accumulation-is-more-than-memory rebuttal as data.

Scope honesty: E1–E3 are artifact evaluations, not user studies; no claims about
long-term user behavior are made.

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

- Review feedback incorporated (2026-07-13, Codex): abstract reframed from assertion
  to position; contributions narrowed to artifact + evaluation; evaluation protocol
  added (E1–E3); local-first tradeoffs promoted to a full section; slogan fixed
  ("model is the author, host is the runtime"); Nadella demoted to secondary
  corroboration; premium-dissolve demoted to discussion.
- Re-run the literature scan immediately before submission.
- Author-voice pieces to reuse: MANIFEST.md, the assistant-you-nurture essay/deck.
- Venue candidates: UIST (systems) primary; CHI systems alternate. The economics
  position could be flagged separately in a short Interactions / CACM essay or
  workshop paper; the longitudinal study targets CHI/CSCW as paper two.
