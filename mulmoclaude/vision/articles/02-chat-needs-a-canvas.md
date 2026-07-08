# Chat Needs a Canvas

*Part 2 of the series "Beyond the Sea of App Icons."*

Elena is sixty-eight, and her left knee has been bad since March. When she checks in at the clinic, she is greeted not by a clipboard but by a conversation. *What brings you in today?* The knee again, she says — worse on stairs — and could she see Dr. Okafor if possible?

A form appears in the chat. Five fields, not forty. Which knee — already filled in: left. Pain on stairs and pain at rest, scored separately, because she mentioned stairs. One line asking her to confirm the dose of her blood thinner, because her record shows one and the dose matters more than the rest of her medication list. A checkbox: any imaging done elsewhere since her last visit? Nothing about childhood illnesses or emergency contacts — her record already knows.

She fills it in and taps submit. Her answers flow back into the conversation as structured data, and the assistant asks the one follow-up worth asking: the record says the dose changed in January — is 5mg still current? Ninety seconds, start to finish.

The interesting thing about this form is that it did not exist until Elena said "knee." Nobody at the clinic designed it, and there is no forms library it was pulled from. A language model, instructed to act as a clinic receptionist, decided mid-conversation that structured input would beat twenty questions asked one at a time, chose the five fields this patient on this visit actually needed, and called a tool named `presentForm` with them. The form is the model's sentence, written in interface instead of prose.

This essay is about the mechanism behind that moment — why conversation needs it, how the industry spent two years converging on it from four directions at once, and where the real disagreement now sits: not whether tools should return interfaces, but who gets to write them.

## A scroll is not a workshop

Part 1 of this series argued that chat proved the first pillar — **the computer that understands** — and simultaneously proved that understanding alone is not an interface for work. It is worth being precise about why.

Chat is a scroll. It is linear, like a text adventure: each turn appends to the transcript, and the transcript only grows downward. That shape is superb for questions and terrible for creation. A designer needs a canvas she can point at; an analyst needs a table she can sort and re-sort; a patient needs five labeled fields, not five questions rationed out one message at a time. A transcript can *describe* a spreadsheet in loving detail, and you still cannot drag a cell. Amelia Wattenberger made the design-side case in "Why Chatbots Are Not the Future": good tools signal what they can and cannot do, and an empty text box signals neither — it has, in her terms, no affordances.

The obvious retreat is back to applications — bolt the language model onto the existing GUI, as Microsoft did with Copilot in Excel. That recovers the canvas by giving up most of the conversation: the model becomes a feature inside one bundle, and the sea of icons Part 1 described returns intact, now with a chat box in each icon. The interesting fix runs the other way: keep the conversation as the spine of the interaction, and let the tools it calls return interfaces, not just text.

## Two payloads

The mechanism is small enough to state in a paragraph, and that smallness is the point.

Every major language model already supports function calling: the model decides a tool is needed, emits a JSON call, and receives a text result it weaves into the conversation. The enhancement is that the tool returns *two* payloads instead of one. The first is words for the model — "Form created with five fields" — which is all the model ever sees, so nothing changes from its side. The second is a typed payload for the human: a structured object tagged `"form"`, `"map"`, `"image"`, `"spreadsheet"`, which the chat application routes to a matching viewer it has registered — a real component, rendered live beside the transcript. No new architecture, no special model capability; any model that can call a function can drive a canvas.

The channel runs both ways, and the return trip is where Elena's story closes. When she submits the form, the host serializes her answers to JSON and hands them to the model as if she had typed them. Conversation produces an interface; the interface produces structured data; the data rejoins the conversation. One loop, and the GUI never stops being part of the dialogue.

The same loop covers creation, not just intake. Say to such a system: *"Show me the present value of $1,000 a month for a year, and make it easy to change the discount rate."* The model generates spreadsheet data — columns, formulas, a highlighted cell for the rate — a viewer renders it live, and dragging the rate recomputes the table while the conversation continues alongside. The spreadsheet emerged *from* the dialogue and stays *inside* it; edits and comments feed back into the model's context like anything else said. Claude's Artifacts and ChatGPT's Canvas are single-purpose versions of the same instinct — a live surface opening beside the transcript — which suggests how general the instinct is.

## Everyone arrived at once

I want to be careful about credit here, because the record is unambiguous and it does not begin with me.

The earliest named productization I can find is Vercel's AI SDK 3.0, on March 1, 2024, which called the pattern "generative UI": tool calls mapped to streamed React components, with the motivation stated plainly — chatbots "have been challenging to write and are still lacking in richness and interactivity." (That specific API has since been deprecated; cite it as the origin of the pattern, not current practice.) The pioneer of the idea over an open protocol came on May 16, 2025, when Ido Salomon and Liad Yosef released MCP-UI — UI components wired directly into the Model Context Protocol. Within months it had been adopted by Shopify, Postman, and Hugging Face.

October 2025 brought two more arrivals in the same month. OpenAI announced its Apps SDK at DevDay: full applications running inside ChatGPT, built on MCP, with Booking.com, Canva, Figma, and Zillow as launch partners. And I published a whitepaper describing the mechanism above — the dual-channel tool result — believing, at the time, that the idea was reasonably fresh. It was not; MCP-UI had beaten it into the world by five months. My design was arrived at independently, which is worth exactly what independent arrival is worth: it is evidence about the idea, not about me. When four groups reach the same shape from different starting points, the shape is probably load-bearing.

The convergence closed in November 2025, when Anthropic and OpenAI — direct competitors — cosigned MCP Apps (SEP-1865), a joint proposal with the MCP-UI creators to standardize interactive UI over MCP; the stable specification landed in January 2026, and it is supported today in Claude, ChatGPT, VS Code, and a growing list of hosts. When rivals co-author the substrate, the substrate has stopped being anyone's thesis. "Tools should return interfaces, not just text" is now consensus, and consensus is the strongest position an idea can occupy.

Which means the interesting question has moved.

## Who holds the pen

MCP Apps deserves to be described at its best, because its design is more considered than a quick summary suggests. A server pre-declares its UI templates as resources under a `ui://` scheme; a tool links to its template through metadata; the host prefetches the HTML and can review it *before any tool runs*, then renders it in a sandboxed iframe. The embedded UI talks back over the same JSON-RPC as the rest of MCP, so every message is structured and auditable, and the UI can invoke other tools only through the host, gated by user consent. Note what makes the security story work: the host can audit the interface precisely because the interface is fixed at development time. The templates' fixedness is not an oversight or a v1 shortcut — it is the load-bearing wall of the trust model. And the templates are dynamic in the weak sense: live data flows into them, they respond to interaction. What they are not is *authored at runtime*.

Now run Elena through it. Under MCP Apps, the clinic's developer designs the intake form — a good, general-purpose intake form — ships it as a template, and the model's entire power is to summon it. It can trigger the widget; it can never shape it. It cannot add the blood-thinner confirmation for this patient, cannot split the pain score because she mentioned stairs, cannot drop the fields her record already answers. The interface never passes through the model at all.

That is the disagreement, and it is smaller and sharper than "competing protocols." Both camps agree tools should return interfaces. They differ on authorship. **In MCP Apps, the app holds the pen; here, the model does.**

In the mechanism this essay describes — I named it the GUI Chat Protocol — the presentation primitives are generic, and the payload is model-authored at runtime. The model decides *that* a form is needed, designs its fields for this user's situation, composes the document, chooses the chart over the table. Intent becomes a small declarative description of an interface, and a viewer turns that description into a live GUI: two translations, with the model performing the first. This is also the first appearance in this series of the second pillar — **the computer that builds** — showing up at the interface layer before it touches schemas or logic. MCP Apps standardizes how apps move into the chat. The question worth asking next is what happens when there is no app to move.

## The ratchet gets its mechanism

Part 1 watched one capability — graphing — get re-implemented in the spreadsheet, the project tracker, the CRM, the notes app, each bundle growing more complex and more expensive for it, and argued the AI-native answer is to give the capability to the conversational layer once. The shared presentation toolkit is where that argument stops being an argument and becomes a mechanism. `presentForm`, `presentChart`, `presentMarkdown`, `presentSpreadsheet` — host-owned viewers, written once — and the model composes them across every domain: the ledger tool returns numbers and `presentChart` draws them; the clinic tool checks the record and `presentForm` collects what is missing. No Mac application ships its own scroll bar; no domain tool here ships its own chart engine. Each application shrinks toward its own irreducible core, and Part 4 follows that shrinking the rest of the way down.

## An application in a paragraph

Once presentation is shared, look at what is left of the receptionist that greeted Elena: a list of tool names — `presentForm`, `presentDocument`, `takePhoto`, a records lookup — and a system prompt describing how a receptionist behaves. That is the entire application. No custom code, no custom screens. Swap the list and the prompt and the same chat shell becomes a recipe guide (`presentForm` to collect skill level and time, `presentDocument` for the recipe, `generateImage` for the steps) or a trip planner (add `map`). The role *is* the application, and the role is configuration — a paragraph of text and a list of names.

Anything that is configuration is data, and anything that is data is something a model can write. That sentence is a trapdoor, and Part 4 goes through it: if the interface can be model-authored, why not the schema underneath, and the logic underneath that?

## What this costs

Four objections deserve full strength, and the first is aimed at the standard everyone just adopted — my own side of the pen question included, since we share the substrate.

If the unit of interface shipped into chat is the vendor-authored widget, the sea of icons does not die; it migrates into the conversation. The DevDay partner list — Booking.com, Canva, Zillow — is, read plainly, an app store inside a chat window: branded surfaces competing for placement in the transcript instead of on the home screen. Interactive UI in chat is necessary for everything this series argues, and sufficient for none of it. If the app remains the unit, the app paradigm survives one level down, with better ergonomics.

Second, a single point of interpretation. When Elena's clinic ran on fixed forms, a bad form was at least *consistently* bad, and someone was accountable for it. Here, the model that misreads intent picks the wrong tool, or designs a form that omits the allergy question for the one patient who needed it. Apps bounded their failures inside bundle walls; a conversational layer that authors interfaces concentrates interpretation — and therefore misinterpretation — in one place.

Third, latency. A pre-built screen is instant; a model-authored one costs seconds of generation, every time, and interfaces are things people wait on differently than they wait on prose.

Fourth, Per Axbom's critique of generated UI, which I think is the most serious. Interfaces composed per user are interfaces no two people share: documentation, phone support, accessibility audits, and the simple act of a granddaughter showing Elena where to tap all assume a common surface that no longer exists. And an interface authored at runtime, per user, by a system that has goals, can be authored to *persuade* — the dark pattern generated bespoke, fitted to exactly the user it works on. Part of the answer is constraining what the model may author, which is Part 3's whole subject. Part of it has no answer yet, and I would rather say so than paper over it.

## Where I am testing this

The receptionist scene at the top of this essay is not hypothetical; it runs in MulmoClaude, the open-source reference implementation I built to find out whether any of this survives contact with use. The form round-trip works the way the mechanism section describes, and roles really are text files — the receptionist, the recipe guide, and a trip planner differ only in tool list and prompt, which is how I became confident the "application in a paragraph" claim is literal rather than rhetorical. The mechanism is congruent with MCP Apps, and could adopt the standard outright at the transport layer; what it tests beyond the standard is the model-authored payload, the shared presentation toolkit, and roles. The failures were as instructive as the successes: the model occasionally reached for the wrong presentation tool — a document where a form was wanted — and early forms asked questions the record could already answer, which is a reminder that giving the model the pen includes giving it the chance to write badly. Both failures are legibility problems, not dead ends, and both point at the same need for constraint.

That need is where this series goes next. Part 3 takes up the question this essay leaves hanging — if the model authors interfaces, and eventually schemas and logic, what makes its output trustworthy to someone who cannot read it? — and argues that the answer is a deliberately limited language: a harness that gives up power on purpose.

---

## Appendix: the dual-channel ToolResult

The mechanism in "Two payloads," as a type. A tool returns one object with two audiences:

```typescript
interface ToolResult {
  // Channel 1 — for the model (all it ever sees)
  message: string;        // e.g. "Found location: Kyoto Station"
  jsonData?: any;         // structured data for follow-up reasoning
  instructions?: string;  // optional guidance, e.g. "Wait for the user to submit the form"

  // Channel 2 — for the human (never enters the model's context)
  data?: {
    type: string;         // "map" | "form" | "image" | "spreadsheet" | ...
    [key: string]: any;   // payload for the viewer registered to this type
  };
  updating?: boolean;     // update the existing view in place vs. create a new one
}
```

The host maintains a registry mapping each `type` to a view component (and a compact preview for the transcript). The `type` tag is the entire coupling between tools and rendering.

A worked example — a map tool:

```javascript
const location = await geocode(address);

return {
  message: `Found location: ${location.name} at (${location.lat}, ${location.lng})`,
  jsonData: location,

  data: {
    type: "map",
    center: { lat: location.lat, lng: location.lng },
    zoom: 15,
    markers: [{ position: location, label: location.name }]
  }
};
```

The model receives one line of text and can keep reasoning about the location; the human gets a live, scrollable map beside the conversation. A later call with `updating: true` — "zoom in on that" — modifies the same map instead of stacking a new one, which keeps the canvas continuous with the dialogue.
