# Nurtured at Home: Why Personal AI Must Grow on an Accumulation You Own

*Working draft — title, abstract, and section outline. Companion document:
[nurture-paper-literature-scan.md](nurture-paper-literature-scan.md) (novelty map and
must-cite list, 2026-07-13). Target shape: systems paper (UIST / CHI systems track),
with the longitudinal nurturing study as a companion or follow-up paper.*

## Abstract

Every major AI vendor has converged on the same insight: the value of a personal
assistant is determined not by the intelligence of its model but by what accumulates
around it — memories, data, and the applications that grow up around a user's life.
An assistant, in other words, cannot be bought; it can only be nurtured. But the
nurturing has already begun, and it is happening in someone else's house: hosted
assistants now invite users to cultivate memory and context on the vendor's premises,
where every conversation deepens an accumulation the user can never take with them.
If accumulation is the value, accumulation is also the lock-in — switching costs
compound with every interaction, and the personalization race is structurally a race
to make leaving impossible. Proposed remedies focus on memory portability, but the
accumulation is more than the memory: it includes schemas, applications, and host
semantics that no memory export carries. An assistant must be nurtured at home, in
an environment the user owns.

We present MulmoClaude, an open-source platform embodying this position. Its central
mechanism is a schema-as-application architecture: the user describes what they need
in natural language; the model emits a small declarative schema; and a host runtime —
not the model — renders the interface, validates every record, and runs reconciliation
and recurrence over a persistent, plain-file workspace on the user's own machine. The
same architecture yields a universal-controller property: one agent composes across
capabilities that would otherwise be separate applications, and the cross-application
work that constitutes the premium tier of conventional software becomes the default
mode of operation. We describe the architecture, the design commitments behind it,
and the questions it opens about how people nurture an assistant that is theirs alone.

## Section outline

### 1. Introduction

- Open with the argument chain, in three steps: (a) accumulation, not model
  intelligence, is the value of a personal assistant — the vendors' own memory
  features concede this; (b) therefore accumulation is also the lock-in, and it
  compounds: every interaction deepens the switching cost; (c) therefore the remedy
  is not portability of one layer but ownership of the environment — the assistant
  must be nurtured at home.
- Users are already nurturing, on hosted platforms — cite the CSCW '25 Digital
  Companionship findings (users believe they cultivate their chatbot; back up chat
  logs; refuse to delete). The behavior exists; the question is who owns the upbringing.
- Contributions list: (1) the compounding-lock-in argument for local-first personal
  AI; (2) the schema-as-application architecture with a host runtime over a persistent
  personal workspace; (3) MulmoClaude, an installable open-source artifact embodying
  both; (4) design lessons and open questions for longitudinal study.

### 2. Related work

Positioning strategy per the literature scan — cite early, differentiate explicitly:

- **Nurturing agents.** Nurture-First (arXiv 2603.10808) claims the metaphor for
  domain-expert agents. Our one-sentence response: it argues agents must be nurtured;
  we ask *where* — and show the answer determines who owns the assistant.
- **Memory as substrate.** Mem0, MemGPT, MemoryBank, hosted memory features. They
  establish accumulation-as-mechanism; none discusses ownership or switching costs.
  Hedge the value premise with Re-Centering Humans (2606.06614): personalization
  payoff is contested, which strengthens (not weakens) the lock-in reading — vendors
  race to accumulate even before value is proven.
- **Portability as remedy.** Portable Agent Memory (2605.11032), SAMEP (2507.10562).
  State their problem statement as shared ground; argue the accumulation-is-more-
  than-memory rebuttal: schemas, apps, and host semantics don't ride a memory export.
- **NL-to-declarative UI.** Jelly (CHI 2025) — closest system; same anti-codegen
  motivation. Differentiate on persistence, validation, reconciler/recurrence, and
  real data over a personal store (all deferred in Jelly). Also Varv (CHI 2022),
  Potluck, GenerativeGUI, Generative UI (2604.09577), Software as Content (2603.21334).
- **Malleable software and local-first.** Ink & Switch essays; Robin Sloan's
  home-cooked app. Apps-for-one framing is theirs; our delta is agent-composed (not
  human-composed) and economics-motivated (not agency-motivated) local-first.
- **Agent-GUI protocols.** MCP Apps, AG-UI, A2UI, OpenAI Apps SDK. Present
  gui-chat-protocol as one entrant; claim only the MVC universal-controller
  articulation and the composition-over-owned-accumulation combination.
- **Agent substrates.** The Log is the Agent (2605.21997) — event-sourced runtime
  layer; complementary, cited for auditability/forkability directions.
- **Accumulation economics.** Nadella's "Reverse Information Paradox" (X, Jul 2026) —
  the enterprise counterpart and strongest mainstream validation: the buyer of
  intelligence pays twice (money + the proprietary knowledge revealed to use it);
  one-directional learning converges value to the owners of learning infrastructure.
  Differentiate on scale (enterprise → personal), mechanism (his *leakage* of exhaust
  vs. our *captivity* of the accumulation), and remedy (his tenant boundary inside a
  vendor cloud answers leakage but not captivity; ownership answers both).

### 3. The argument: accumulation, lock-in, home

- Anchor the economics canonically: Arrow's Information Paradox (1962) — the seller
  risks giving knowledge away to sell it — and its AI-age inversion (Nadella 2026):
  the buyer gives knowledge away to use what they bought. Hayek (1945) grounds what
  accumulates: the knowledge of time, place, and circumstance that only the user holds.
- Two failure modes of hosted accumulation, treated separately: *leakage* (interaction
  exhaust trains the provider; asymmetric learning) and *captivity* (the accumulation
  is held on the premises; switching costs compound). Portability protocols address
  neither fully; tenant boundaries address leakage only; ownership addresses both.
- Formalize the compounding: switching cost as a function of accumulated interactions,
  apps, and schemas; contrast with classic data-gravity/switching-cost literature.
- Why portability protocols under-remedy: enumerate what a memory export carries vs.
  what constitutes the assistant (records + schemas + host semantics + generated apps).
- Define "nurtured at home": plain files, open source, local execution, relay-only
  remote access. Each property tied to a failure mode it prevents (shutdown,
  repricing, acquisition, export lock).

### 4. Design commitments (from the manifesto, condensed)

1. The agent is a universal controller — joins, not replaces, the UI; composes across
   a plugin registry.
2. Chat summons GUIs — bidirectional modality choice, including agent-requested
   structured input (forms).
3. The protocol is open and extends MCP (gui-chat-protocol).
4. The accumulation belongs to the user — the commitment the other three serve.

### 5. Architecture: schema as application

- The collection mechanism: NL → small declarative schema; host renders (table /
  kanban / calendar), validates every record, runs the reconciler (reminders,
  recurrence). "The records are data, the schema is the application, the model is
  the runtime."
- Trust boundary: everything the model authors is validated before it runs; views
  and recurrence are engine code that never guesses. Invalid applications never execute.
- Honest persistence description: plain-file workspace, per-entity storage; append-only
  islands (chat transcripts, accounting journal with compensating entries, wiki snapshot
  history) vs. mutable subsystems — and why correctness-critical subsystems
  independently converged on logs.
- Worked examples: accounting (API + UI + agent; receipt photo → same API), a
  collection built in one conversation, cross-plugin composition (accounting → chart;
  wiki → recurring obligation).
- Sharing: a collection schema published to a registry — apps-for-one compose into
  a commons.

### 6. Discussion

- Premium features dissolve: the integration tier was the integration cost; connect
  to the practitioner unbundling literature (Bain, Deloitte, Gartner) as context,
  claim the mechanism articulation.
- Limitations: no longitudinal evidence yet (design the study; cite the n=1
  Nurture-First case study as the current state of evidence); personalization payoff
  contested; single-machine availability; model dependence.
- Open questions for the longitudinal study: what do people build, does accumulation
  measurably change capability, where does the nurturing metaphor break.

### 7. Conclusion

- Return to the opening: the assistant you cannot buy — and cannot board out. The
  architecture exists, the install is one command, and the question of who owns the
  upbringing is being decided now, by defaults.

## Notes

- Re-run the literature scan immediately before submission (preempting sources are
  fresh preprints; space moves monthly).
- Author-voice pieces to reuse: MANIFEST.md (design commitments, patterns), the
  assistant-you-nurture essay/deck (framing, metaphors).
- Venue candidates: UIST (systems), CHI (systems/argument hybrid), CSCW (if study
  lands in time); short-form flag option: Interactions / CACM essay or a workshop
  paper on the economics framing.
