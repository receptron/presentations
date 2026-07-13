# Literature scan: the nurtured-assistant paper

*Novelty assessment for a prospective position/systems paper based on the MulmoClaude
manifesto ("How AI-Native Applications Should Be Built") and the assistant-you-nurture
vision. Compiled 2026-07-13 from a multi-agent deep-research pass (106 agents, 24 sources
fetched, 25 top claims adversarially verified 3-vote) plus a targeted follow-up on
agent-GUI protocols and SaaS-unbundling economics.*

**Shelf-life warning:** the key preempting sources are non-peer-reviewed preprints from
the last few months in a fast-moving space. Re-scan immediately before submission.

---

## Verdict by claim

### Claim 1 — "The assistant is the accumulation, not the model" / nurture metaphor

**Status: preempted — needs differentiation, cannot be presented as new.**

- [*Nurture-First Agent Development*](https://arxiv.org/html/2603.10808v1) (Linghao Zhang,
  arXiv 2603.10808, Mar 2026) claims the metaphor almost verbatim: the agent "is not built
  and then deployed — it is born with minimal scaffolding and then raised through sustained
  interaction with its user," with value located in progressively accumulated, consolidated
  knowledge assets rather than raw model capability. Single-author, non-peer-reviewed,
  scoped to domain-expert agents (equity research).
- **Differentiable:** personal-assistant scope; the accumulation being *data + apps + schemas*,
  not just consolidated knowledge; peer-reviewable rigor.
- The mechanism (persistent memory as the differentiator) is established engineering
  literature: [Mem0](https://arxiv.org/pdf/2504.19413), MemGPT (Packer et al. 2023),
  MemoryBank (Zhong et al., AAAI 2024), ChatGPT/Claude memory features.
- **Hedge required:** [*Re-Centering Humans in LLM Personalization*](https://arxiv.org/pdf/2606.06614)
  found humans judged personalized responses no better than generic ones in 54.6% of 1,101
  judgments. "Accumulation = value" must be argued or measured, not asserted.

### Claim 2 — "The schema is the application, the model is the runtime"

**Status: mechanism crowded, full architecture unclaimed. Centerable with careful positioning.**

- [Jelly](https://dl.acm.org/doi/full/10.1145/3706598.3713285) (CHI 2025, Xia lab UCSD;
  [arXiv 2503.04084](https://arxiv.org/abs/2503.04084)) already: LLM interprets prompts into
  a declarative task-driven data model; rule-based host engine maps schema annotations to UI
  widgets; explicitly argues **against** direct code generation because generated code resists
  iterative end-user re-tailoring — the same motivation as MulmoClaude's.
- Jelly's limits (= the open territory): no reconciler/recurrence semantics, no record
  validation over a **persistent personal data store**, generated (not real) data, evaluation
  is a single 80-minute lab session (n=8), external data integration deferred to future work.
- Apps-for-one framing is owned by Ink & Switch's
  [malleable software essay](https://www.inkandswitch.com/essay/malleable-software/)
  (Litt, Horowitz, van Hardenberg, Matthews, June 2025) — but its LLM path is code generation
  inside a malleable environment, not schema-emission with a host runtime, and humans (not an
  agent) compose the tools.
- Adjacent ingredients requiring differentiation: **Potluck** (AI-drafted declarative rules),
  **Varv** (CHI 2022, behavior as declarative data).
- **The unclaimed statement:** small declarative schema + host runtime performing validation,
  reconciliation, and recurrence over a persistent personal accumulation — "the records are
  data, the schema is the application, the model is the runtime."

### Claim 3 — Lock-in compounds with accumulation → local-first

**Status: problem statement is prior art; the economic framing is open. The strongest claim to center.**

- [*Portable Agent Memory*](https://arxiv.org/abs/2605.11032) (arXiv 2605.11032, Microsoft
  author, May 2026) states the problem verbatim — accumulated agent context "remains locked
  within vendor-specific runtimes" — and ships an open portability protocol (Merkle-DAG
  provenance, cross-model transfer). [SAMEP](https://arxiv.org/abs/2507.10562) is a second
  independent portability proposal. So accumulation-lock-in cannot be presented as a new
  observation.
- Empirical grounding exists but only under an attachment framing:
  [*Digital Companionship*](https://dl.acm.org/doi/10.1145/3715070.3749245) (CSCW '25;
  [arXiv 2510.15905](https://arxiv.org/abs/2510.15905)) documents users backing up chat logs
  and refusing to delete assistants ("it would feel like killing it"); 12 of 30 high-engagement
  interviewees believed their interactions cultivated the chatbot. The paper never uses
  lock-in / switching-cost / data-gravity language.
- Ink & Switch's local-first argument is agency/ownership; zero occurrences of lock-in or
  switching-cost economics.
- **The unclaimed framing:** lock-in-compounds-with-accumulation as an *economic* (data-gravity,
  switching-cost) argument for local-first personal AI.
- **Required rebuttal:** why local-first beats portability protocols. Strongest form:
  *the accumulation is more than the memory* — portable memory does not transfer the schema'd
  apps, host-engine semantics, and workspace that constitute the assistant.

### Claim 4 — LLM as universal controller / chat summons GUIs / gui-chat-protocol

**Status: crowded and moving fast. Do not center; position as one entrant with a distinct articulation.**

The initial workflow found nothing here; a targeted follow-up showed that was a coverage
artifact. The space filled up in 2025–26:

- [MCP Apps](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/) — official MCP
  extension for UI-bearing tool results, championed by OpenAI and Anthropic (Jan 2026).
- [AG-UI](https://docs.ag-ui.com/introduction) (CopilotKit) — event-based agent ↔ frontend
  protocol; see the [protocol comparison](https://www.copilotkit.ai/blog/the-state-of-agentic-ui-comparing-ag-ui-mcp-ui-and-a2ui-protocols).
- [A2UI](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/)
  (Google) — generative UI spec for agent-delivered widgets.
- OpenAI Apps SDK — apps-in-ChatGPT with structured UI, incl. agent-requested forms.
- [*Generative UI: LLMs are Effective UI Generators*](https://arxiv.org/html/2604.09577v1)
  (Google Research) — model chooses presentation (chart/form/map/etc.); human-preference evaluation.
- [GenerativeGUI](https://dl.acm.org/doi/10.1145/3706599.3719743) (CHI EA) — dynamic GUI
  generation on chat interfaces, with user study.
- [*Software as Content*](https://arxiv.org/pdf/2603.21334) (arXiv 2603.21334) — argues
  dynamically generated agentic applications should be the *primary medium* of human-agent
  interaction; closest to "chat summons GUIs" as a paradigm claim.

**Possibly still unclaimed:** the MVC "universal controller" articulation (agent as a second
controller *joining* a real UI, neither privileged), and composition across a plugin registry
combined with user-owned accumulation. The substance, however, is contested space.

### Claim 5 — "Premium features dissolve"

**Status: widely circulating in practitioner/analyst form; a framing contribution, not a novelty claim.**

- The agents-unbundle-SaaS thesis is mainstream:
  [Bain](https://www.bain.com/insights/will-agentic-ai-disrupt-saas-technology-report-2025/),
  [Deloitte 2026 predictions](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/saas-ai-agents.html),
  Gartner (35% of point-product SaaS replaced/absorbed by 2030), the
  ["SaaSpocalypse" / Great SaaS Unbundling](https://www.uncoveralpha.com/p/the-great-saas-unbundling-why-ai)
  discourse, [the unbundling thesis explained](https://aiagentslist.com/blog/will-ai-agents-replace-saas-the-unbundling-thesis-explained).
- No academic formalization of the specific mechanism was found — *the premium tier was the
  integration cost; remove the integration cost and the premium tier dissolves* — which is a
  sharper articulation than anything scanned, but the surrounding idea is not new.

### Longitudinal nurturing study

**Status: confirmed open — the largest unclaimed territory in the scan.**

- Only existing evidence: Nurture-First's 12-week, n=1 case study (equity analyst, "useful
  analyses" 38%→74%), self-described as "illustrative rather than definitive."
- Closest CHI/CSCW work is retrospective (Digital Companionship: survey N≈200 + 30 interviews),
  one-week, or prompt-customization-only
  ([*Not Just Novelty*](https://arxiv.org/abs/2402.09894)).
- **No prospective multi-week study of real users nurturing a memory-accumulating personal
  assistant exists.** MulmoClaude is an instrument that can generate this data.

---

## Bottom line

Center the paper on the three verified-open contributions:

1. **The lock-in-economics argument for local-first**, sharpened to "the accumulation is more
   than the memory" (vs. portability protocols).
2. **The complete schema-as-application architecture** — schema + host runtime with
   validation/reconciler/recurrence over a persistent personal store (vs. Jelly/Potluck/Varv).
3. **The longitudinal nurturing study** — no competition at all, if willing to run it.

Present the nurture metaphor, universal-controller, and premium-dissolution claims as the
integrating narrative, with prior work cited. The claim no single prior work can match is the
integration: all four commitments running together in one installable, MIT-licensed artifact.

## Must-cite list

| Work | Venue / status | Role |
| --- | --- | --- |
| Nurture-First Agent Development ([2603.10808](https://arxiv.org/html/2603.10808v1)) | arXiv preprint, Mar 2026 | Nurture metaphor prior art |
| Jelly ([10.1145/3706598.3713285](https://dl.acm.org/doi/full/10.1145/3706598.3713285)) | CHI 2025 | NL → declarative model → rule-based UI |
| Digital Companionship ([10.1145/3715070.3749245](https://dl.acm.org/doi/10.1145/3715070.3749245)) | CSCW '25 | Empirical nurturing perceptions, accumulation attachment |
| Malleable Software ([Ink & Switch](https://www.inkandswitch.com/essay/malleable-software/)) | Essay, 2025 | Apps-for-one framing |
| Local-first software (Ink & Switch, 2019) | Essay/Onward! | Local-first foundations |
| Varv (CHI 2022) | CHI | Behavior as declarative data |
| Potluck (Ink & Switch) | Essay/lab | AI-drafted declarative rules |
| Portable Agent Memory ([2605.11032](https://arxiv.org/abs/2605.11032)) | arXiv preprint, May 2026 | Lock-in problem statement + portability mitigation |
| SAMEP ([2507.10562](https://arxiv.org/abs/2507.10562)) | arXiv preprint | Second portability proposal |
| Mem0 ([2504.19413](https://arxiv.org/pdf/2504.19413)) | arXiv, company-authored | Memory substrate; benchmark scores disputed — cite framing only |
| MemGPT (Packer et al. 2023) | arXiv | Memory-architecture foundations |
| MemoryBank (Zhong et al.) | AAAI 2024 | Persistent user-profile memory |
| Ethical Personal AI with LTM ([2409.11192](https://arxiv.org/html/2409.11192v1)) | arXiv preprint | LTM personalization, privacy-only risk framing |
| Re-Centering Humans in LLM Personalization ([2606.06614](https://arxiv.org/pdf/2606.06614)) | arXiv preprint | 54.6% null result — hedge for accumulation-value |
| Not Just Novelty ([2402.09894](https://arxiv.org/abs/2402.09894)) | arXiv | Longitudinal-adjacent customization study |
| Generative UI ([2604.09577](https://arxiv.org/html/2604.09577v1)) | Google Research, arXiv | Model-chosen output modality |
| Software as Content ([2603.21334](https://arxiv.org/pdf/2603.21334)) | arXiv preprint | Generated apps as primary interaction medium |
| GenerativeGUI ([10.1145/3706599.3719743](https://dl.acm.org/doi/10.1145/3706599.3719743)) | CHI EA | Dynamic GUI generation in chat |
| MCP Apps ([announcement](https://blog.modelcontextprotocol.io/posts/2026-01-26-mcp-apps/)) / [AG-UI](https://docs.ag-ui.com/introduction) / [A2UI](https://developers.googleblog.com/introducing-a2ui-an-open-project-for-agent-driven-interfaces/) / OpenAI Apps SDK | Industry protocols, 2025–26 | Agent-GUI protocol landscape |
| Bain ([2025](https://www.bain.com/insights/will-agentic-ai-disrupt-saas-technology-report-2025/)) / Deloitte ([2026](https://www.deloitte.com/us/en/insights/industry/technology/technology-media-and-telecom-predictions/2026/saas-ai-agents.html)) / Gartner | Analyst reports | SaaS-unbundling economics context |
| The Log is the Agent ([2605.21997](https://arxiv.org/abs/2605.21997), Yohei Nakajima) | arXiv preprint, 2026 | Event-sourced agent substrate; auditability/forkability related work |
