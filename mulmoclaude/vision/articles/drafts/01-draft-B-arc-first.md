# Beyond the Sea of App Icons

In October 2025 I published a whitepaper with a taxi in it. The metaphor was the part I was proudest of: when you ride in a taxi, you do not drive — you tell the driver where you want to go, and the driver operates the machine. I argued that AI was becoming that driver, the intermediary between human intent and machine execution, and that this would end the era of the app icon. I wrote several papers that year making versions of the same argument. I believed I had seen the whole revolution: the computer was finally going to understand us.

I was half right. This year, building the prototype that was supposed to test that thesis, I watched it do something my papers had no vocabulary for. This essay is about the belief, the moment it broke, and the larger claim that sits on the other side.

## The half I saw first

Start with the problem the 2025 papers were aimed at. A small-business owner — call her Maria, a soap maker — wants to announce a new product. Today that means a notes app for the text, a photo editor for the image, a memory of which filter she used last time, then Instagram, Facebook, and X, each with its own paste-and-upload ritual. Twenty minutes of managing applications, in service of one sentence of intent: *tell people about the lavender soap.*

Nothing in that twenty minutes is a capability problem. Every function Maria needs has existed for a decade. The problem is that the functions are packaged as **apps** — islands, each with its own customs, gestures, and logic — and Maria has to be the ferry. Her home screen, like yours and mine, is a glittering sea of icons, and every task begins not with intention but with a choice: *which app do I open?* Apps solved capability. They never solved intent.

The history of interfaces is a history of moving that translation burden. The command line demanded we learn the computer's grammar. The GUI let us point at pictures instead — a genuine liberation in 1984, which hardened over forty years into the icon sea. Then, in late 2022, ChatGPT quietly changed the unit of interaction from the query to the conversation. People stopped typing "best italian restaurant near me" and started asking "where should I take my wife for dinner?" — and the machine answered in kind. For the first time, the computer spoke our language rather than the reverse.

But a chat window is not an interface for work. Conversation is linear; it scrolls like a text adventure — fine for questions, awkward for creation. Designers need canvases, analysts need dashboards. Amelia Wattenberger made the design-side version of this point sharply in "Why Chatbots Are Not the Future": good tools show you what they can and cannot do, and a blank text box shows you nothing.

So the 2025 thesis, mine and others', was a synthesis: keep natural language as the primary channel, put an LLM in the orchestrator's seat, expose every capability as a tool the model can call, and let graphical interfaces appear on demand — a chart when you discuss numbers, a map when you mention a place — then fade when they have served their purpose. Maria says one sentence; the driver handles the rest. I built a prototype, MulmoChat, to find out whether this actually worked as an experience and not just as an architecture diagram. Mostly, it did.

Call this pillar what it is: **the computer that understands.** Natural language becomes the interface; you express intent instead of navigating applications. Through the end of 2025, I believed this was the entire story.

## The turn

The moment the thesis broke was small enough that I almost missed it.

By early 2026 I was building a second prototype, this time on top of a coding agent, and I had been keeping a list of restaurants in it — plain structured records, names and neighborhoods and notes. One day, more out of playfulness than need, I asked for my restaurants drawn as a Tokyo subway map: stations for restaurants, lines for neighborhoods, my own taste as the geography. A minute later it existed — a self-contained HTML file, interactive, correct, mine. I never saw the code. I have still never seen the code.

Understand why this stopped me. In the taxi metaphor, the driver operates a vehicle that already exists. Every 2025 paper I wrote assumed the tools were *there* — built by developers, registered in a catalog, waiting for the orchestrator to pick the right one. A restaurant-list-as-subway-map is not in any catalog. No company has built it and no company ever will; there is no market for my restaurants rendered to my taste. The agent did not select that software. It *authored* it — the interface, and beneath the interface the data schema, and around the schema the little bits of logic that made it behave — fitted to one user, in the same conversation that expressed the wish.

The driver had built the vehicle. My papers had a name for computers that understand; they had no name for this.

So here is the second pillar, the one that took me a prototype to see: **the computer that builds.** The AI generates the GUI, the database schema, even the business logic — not from a template gallery, but fresh, for a specific person's specific need. (What this does to the economics of software is a large enough subject that I am saving it for Part 5 of this series. Here I only need the fact of it.)

## Two pillars, one fusion

Each pillar alone has a ceiling, and we have already watched both ceilings get hit.

Understanding without building is a concierge over fixed apps. That is Siri's limit, and Alexa's: however well the assistant parses your sentence, it can only route you to software somebody already wrote, so the long tail of human intent — which is most of human intent — goes unserved. Building without understanding is a tool for programmers only. That is Copilot's limit, and the limit of every code generator that assumes its user can read the output: the authoring power is real, but the audience is the small fraction of humanity that already speaks code.

The interesting thing — the thing I now believe the next decade of computing is actually about — is the fusion. When the same system both understands the intent and builds the artifact, software materializes from conversation. And at that point the app, as the unit of computing, dies twice. First death: you stop choosing apps, because the orchestrator chooses capabilities for you — that much my 2025 papers had. Second death: apps stop needing to *pre-exist*, because whatever doesn't exist can be generated at the moment of need. The first death empties the home screen. The second empties the app store.

The app dies twice: you stop choosing them, and they stop needing to pre-exist.

## The neighbors

I am not the only person circling this territory, and it is worth mapping the neighbors precisely, because each one stops somewhere specific.

Satya Nadella, on the BG2 podcast in December 2024, said of business applications: "The notion that business applications exist, that's probably where they'll all collapse... in the agent era," describing SaaS apps as "essentially CRUD databases with a bunch of business logic" whose logic migrates to the agent tier. Note the "probably" — he hedged, and the "SaaS is dead" headlines that followed were the media's words, not his. Nadella is describing the demand side of the collapse, from the buyer's chair; he does not say what architecture it lands on.

Andrej Karpathy, in his June 2025 "Software Is Changing (Again)" talk, gave pillar two its cleanest slogan — "your prompts are now programs" — and gave the field the LLM-as-OS analogy that my own 2025 work explicitly built on. But cite him carefully, because he is emphatically not a collapse proponent: in the same talk he argues *for* dedicated apps with human-controlled autonomy sliders and GUIs that make verification fast — "less Iron Man robots and more Iron Man suits" — and he has repeatedly cooled agent timelines ("this is the decade of agents," not the year). I read his verification argument as support rather than objection, and I will return to it below, because he is pointing at exactly the part of this vision that is hardest.

The empirical record backs him on the hard part. SaaS-Bench, a May 2026 benchmark of 106 long-horizon tasks on 23 real SaaS systems, found that even the strongest GUI-driving agents completed fewer than 4% of tasks end-to-end. The scope matters — this measures agents clicking through human interfaces, strictly end-to-end, and partial-progress scores run much higher — but the direction is clear: making the AI operate our apps, pixel by pixel, is the wrong layer. The fix is architectural, not a bigger model.

And the industry has started converging on the substrate. In November 2025, Anthropic and OpenAI — direct competitors — cosigned the MCP Apps extension (SEP-1865), a shared standard for delivering interactive interfaces inside a conversation. When the two largest AI labs agree on plumbing, the plumbing is telling you something: conversation is becoming the primary surface of computing, and everyone is preparing for it.

Here is the map, then. Nadella predicts the logic migrates but names no architecture. Karpathy supplies the OS frame but defends a distinct app layer. Generative-UI efforts, MCP Apps included, let AI deliver or select the interface — over schemas and business logic that a vendor still authors and fixes in advance. To my knowledge, nobody in this discourse yet claims the full fusion: the AI authoring all three layers — interface, schema, logic — per user, per need. That unclaimed square is where this series lives.

## One conversation, start to finish

To make the fusion concrete, walk through a single task as the two pillars together would handle it — a scenario I have run in pieces, and which existing products (Claude's Artifacts, ChatGPT's Canvas, any coding agent) already run in fragments.

You say: "I need to explain our Q4 results to the board." A table appears with placeholder columns — Revenue, Expenses, Profit. You say the numbers; the table fills, and a chart materializes beside it. "Compare that to Q3" — the chart becomes a trend. "Now draft the summary document" — an outline appears, its sections already pulling figures from the table. "Add context about why expenses rose" — you explain out loud, and your explanation lands as prose in the right section. "Actually, make this a short video for the members who can't attend" — the document becomes a script, images and narration are generated, and a few minutes later you are watching it.

Count what never happened. You never opened Excel, PowerPoint, Word, or a video editor. You never exported, imported, or reformatted. But also — this is the second pillar earning its keep — the table's columns, the chart's form, the document's structure, and the video's script were not features of any pre-built product. Each was authored, in the moment, for this board and this quarter. Understanding routed the conversation; building materialized the artifacts.

## What this costs

An idea this convenient deserves its strongest objection stated plainly, and the strongest objection is not reliability — it is *discovery*.

The sea of app icons is exasperating, but it is also a map. A menu is a catalog of the possible: every item is a promise, every grayed-out button a boundary. Wattenberger's affordance argument cuts deepest exactly here — when the interface is a blank conversation, nothing signals what the system can do, and so users systematically under-ask. I have watched this in my own testing: people request what they already know software does, which means the one capability that is genuinely new — *ask for something that doesn't exist* — is precisely the one no blank text box will ever suggest. Killing the icon sea kills the catalog, and the catalog was doing real work. Any honest AI-native design has to rebuild that signaling — proactive suggestion, visible capability, interfaces that teach — rather than assume intent arrives fully formed.

The second cost is trust, and it compounds the first. When the interface itself is generated, the old warrant of correctness — "millions of users have hammered on this same screen" — is gone; my subway map has an audience of one, so its bugs have an audience of one. Karpathy's Iron Man suit is the right instinct here: the answer is not blind autonomy but generated interfaces whose job includes making verification fast for the human wearing them. How to make one-shot generated software trustworthy for someone who cannot read code is the subject of Part 3 of this series; what the audience-of-one economics does to correctness, and where the burden of proof relocates, is Part 5. I flag both now because the two-pillar claim is not credible without them.

## Where this series goes

The prototypes behind this essay are the reference implementations I built to test the thesis against reality: [MulmoChat](https://github.com/receptron/MulmoChat), the 2025 experiment in conversation-with-canvas that validated the first pillar, and MulmoClaude, the 2026 workspace experiment that surprised me into the second — the one that drew the subway map. They appear in this series only as instruments; the findings, including the ones that broke my own papers, are the point.

The remaining five parts take one load-bearing piece each: why chat needs a canvas and how tools can return interfaces instead of text (Part 2); why a deliberately limited language is what makes generated software trustworthy (Part 3); how schema plus records plus a model amounts to a complete application (Part 4); what near-zero-cost bespoke software does to the economics of the field (Part 5); and what happens when the agent keeps what it builds as part of itself (Part 6). I spent 2025 arguing that the computer would finally understand us; this series is my attempt to report, carefully, what I learned in 2026 — that it can also build for us, and that the two together end the app as we have known it.
