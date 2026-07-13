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
does the executing: it renders the interface from the schema, validates every record
against it, and runs reconciliation and recurrence over a plain-file workspace on the
user's own machine. The model authors the application; the host runs it; the records
endure. Because everything the model authors is validated before it executes, the
parts of the system that must never guess — views, validation, recurrence — never
do; and because the workspace is plain files, the accumulation is inspectable,
copyable, and independent of any single vendor or model.

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

<!-- Sections 2–9 follow; see nurture-paper-draft.md for the outline. -->
