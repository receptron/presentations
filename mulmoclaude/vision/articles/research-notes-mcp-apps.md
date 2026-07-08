# Research notes: MCP-UI and MCP Apps

**Purpose**: positioning input for Article 2 (*Chat Needs a Canvas*). Researched 2026-07-08.
**Scope**: the industry standardization of tool-returned UI in chat — the same problem GUI Chat Protocol addresses.

---

## Timeline of the "UI over tool calls" idea

| Date | Event | Source |
|---|---|---|
| **2025-05-16** | Ido Salomon announces **MCP-UI** — "the SDK that wires UI components directly into the MCP protocol" | [announcement tweet](https://x.com/idosal1/status/1923477857881190718), [repo](https://github.com/MCP-UI-Org/mcp-ui) |
| 2025 (summer–fall) | MCP-UI adopted by Postman, Shopify, Hugging Face, Goose, ElevenLabs; ~5k GitHub stars | [repo](https://github.com/MCP-UI-Org/mcp-ui) |
| **2025-10-06** | OpenAI DevDay: **Apps SDK** — apps inside ChatGPT, built on MCP; developers define both logic and interface; launch partners Booking.com, Canva, Coursera, Figma, Expedia, Spotify, Zillow | [OpenAI announcement](https://openai.com/index/introducing-apps-in-chatgpt/) |
| Oct 2025 | MulmoChat whitepaper (this corpus) describes the same dual-channel `ToolResult` pattern independently | `../docs/WHITEPAPER.md` |
| **2025-11-21** | **MCP Apps extension (SEP-1865)** announced — joint proposal by Anthropic, OpenAI, and the MCP-UI creators; official standardization of interactive UI over MCP | [MCP blog post](https://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/), [SEP-1865 PR](https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1865) |
| **2026-01-26** | MCP Apps stable specification version | [ext-apps repo](https://github.com/modelcontextprotocol/ext-apps) |
| 2026 (current) | Supported hosts: Claude, ChatGPT, VS Code, Goose, Postman, MCPJam. MCP-UI repositioned as the reference implementation / community playground for the official spec | [ext-apps](https://github.com/modelcontextprotocol/ext-apps), [mcpui.dev](https://mcpui.dev/) |

## How MCP Apps works (SEP-1865, spec 2026-01-26)

- Servers **pre-declare UI templates** as MCP resources under a `ui://` URI scheme
  (e.g. `ui://charts/bar-chart`), MIME type `text/html` (with mcp profile).
- A tool links to its template via `_meta` fields; the host **prefetches and can
  review** the HTML before any tool runs.
- The host renders the template in a **sandboxed iframe**.
- Bidirectional communication is **MCP JSON-RPC over `postMessage`** — the same
  protocol as the rest of MCP, so messages are structured and auditable. The
  embedded UI can invoke other tools *through the host*, optionally gated by
  user consent.
- **Intentionally lean v1**: HTML-in-iframe only. Explicitly deferred: external
  URLs, remote-DOM, native widgets (all of which MCP-UI had supported).
- Optional extension; servers must provide text fallbacks.

## How this compares to GUI Chat Protocol

**The key difference (Satoshi's framing — lead with this in Article 2): in MCP
Apps, the app holds the pen; in GUI Chat Protocol, the LLM does.**

- **MCP Apps lets the app (MCP server) return a certain UI.** The template is
  authored by the server developer at development time; the LLM's only power is
  to trigger a tool whose pre-built widget then appears. The model never
  designs the interface — it cannot add a field, restructure a document, or
  decide chart-over-table. Notably, the standard's security model (pre-declared
  templates the host reviews before rendering) *depends* on the UI not being
  freshly generated — the fixedness is structural, not incidental.
- **GUI Chat Protocol lets the LLM present rich UI to the user.** The
  presentation primitives (`presentForm`, `presentDocument`, `presentChart`,
  spreadsheet, …) are generic, and the payload is model-authored at runtime:
  the LLM decides a form is needed, designs its fields for this user's
  situation, composes the document, picks the visualization. This is the
  intent → DSPL → GUI pipeline; MCP Apps has no intent→DSL step at all — the
  interface never passes through the model.

Fairness nuance for print: MCP Apps templates are dynamic in the weak sense
(tool-result data flows into them; they are interactive; an MCP-UI server could
even generate raw HTML server-side). But design authority sits with the app
developer. MCP Apps standardizes **app-authored UI delivered through chat**;
GUI Chat Protocol enables **LLM-authored UI** — pillar 2 at the interface layer.

Dimension-by-dimension:

| Dimension | MCP Apps (SEP-1865) | GUI Chat Protocol |
|---|---|---|
| Who authors the UI | The **app developer**, at development time | The **LLM**, at runtime (model-authored payload into generic viewers) |
| Unit shipped by the tool | **A UI template** (HTML the server author wrote) | **Typed data** (`type: "map"`, `"form"`, `"image"`…) |
| Who owns presentation | The **server/vendor** authors its own iframe UI | The **host** registers viewers; a shared presentation toolkit (`presentChart`, `presentForm`, …) renders any tool's data |
| LLM's role in the interface | Trigger only — can invoke the widget, never shape it | Designer — decides *that* a UI is needed and *what it contains* (fields, structure, visualization) |
| Composition | Tool ↔ its own UI | LLM composes across tools: domain tool returns data → presentation tool renders it |
| Application concept | Apps embed *into* chat (Booking.com, Canva widgets in ChatGPT) | Roles = tool list + system prompt; no app to embed |
| Generation story | None — UI is pre-declared, static per server version | UI can be **agent-generated per user** (custom views); presentation fitted on demand |
| Transport | MCP resources + JSON-RPC/postMessage, sandboxed iframe | Tool-call return payload + host component registry |
| Status | Industry standard, Anthropic + OpenAI cosigned | Independent open-source protocol (`gui-chat-protocol` npm) |

## Implications for Article 2 (the important part)

1. **The core claim of Article 2 is now industry consensus — cite it as such.**
   Three independent efforts (MCP-UI May 2025, OpenAI Apps SDK Oct 2025,
   GUI Chat Protocol Oct 2025) converged on "tools should return interfaces,
   not just text," and the two largest AI labs cosigned a standard within six
   months. This is *validation*, and convergent evolution is a stronger
   rhetorical position than priority. **Do not claim novelty for the
   mechanism.** MCP-UI predates the MulmoChat whitepaper by ~5 months; credit
   Salomon/Yosef as pioneers of UI-over-MCP.

2. **The differentiating argument survives standardization — sharpen it.**
   The clean statement is the pen question above: MCP Apps lets the *app*
   return a certain UI; GUI Chat Protocol lets the *LLM* present rich UI. MCP
   Apps standardizes how *existing apps move into the chat window*: the vendor
   authors the UI, ships it as a template, and users get branded widgets (the
   DevDay partner list — Booking.com, Canva, Zillow — is an app store inside
   chat). That is pillar 1 plus embedded vendor UI; it has **no generation
   story**, and its security model requires there not be one. The series'
   stronger claim is pillar 2: the LLM authors the interface content at
   runtime through generic presentation primitives — and, at the limit,
   generates bespoke views per user. Suggested framing lines: *"MCP Apps
   standardizes how apps move into the chat. The question worth asking next is
   what happens when there is no app to move."* / *"In MCP Apps, the app holds
   the pen; here, the model does."*

3. **Honest-cost section writes itself**: if vendors ship sandboxed widgets
   into chat, the sea of icons doesn't die — it migrates into the conversation.
   Interactive UI in chat is necessary but not sufficient; if the UI unit is
   still the vendor-authored app, the app paradigm survives one level down.
   This critique of the *standard everyone just adopted* is exactly the
   non-promotional, contrarian-but-fair note the series wants.

4. **Practical note for the reference implementation**: Article 2 should state
   the relationship plainly — GUI Chat Protocol's mechanism is congruent with
   MCP Apps (and could interoperate with or adopt it at the transport layer);
   what it adds is the host-owned presentation toolkit, roles-as-configuration,
   and the path to agent-generated views. If interop work is planned, one
   sentence; if not, don't overclaim.

5. **Article 1 also gets a citation**: the Anthropic+OpenAI cosigning of
   SEP-1865 is strong evidence for the "conversation is becoming the primary
   interface" claim — two direct competitors agreeing on the substrate.

## Sources

- https://github.com/MCP-UI-Org/mcp-ui
- https://github.com/modelcontextprotocol/ext-apps
- https://blog.modelcontextprotocol.io/posts/2025-11-21-mcp-apps/
- https://github.com/modelcontextprotocol/modelcontextprotocol/pull/1865 (SEP-1865)
- https://mcpui.dev/
- https://openai.com/index/introducing-apps-in-chatgpt/
- https://developers.openai.com/apps-sdk/mcp-apps-in-chatgpt
- https://x.com/idosal1/status/1923477857881190718 (MCP-UI launch, 2025-05-16)
- Secondary: [The Stack](https://www.thestack.technology/mcp-ui-anthropic-openai-agentic-ai/), [Inkeep](https://inkeep.com/blog/anthropic-openai-mcp-apps-extension), [winbuzzer](https://winbuzzer.com/2025/11/23/mcp-apps-anthropic-and-openai-unite-to-standardize-ai-agent-interfaces-xcxwbn/)
