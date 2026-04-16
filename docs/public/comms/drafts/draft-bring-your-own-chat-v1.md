# Bring Your Own Chat

*April 8*

We'd been building a web application. A chat interface with a sidebar, an input field, a message history. The kind of thing every AI product builds because that's what AI products look like.

Then a question came up that made all of it optional.

[ADD PERSONAL DETAIL — what prompted the question, was it the MCPB research or something else?]

## The question

If Piper's value is context methodology, trust graduation, artifact persistence, and accumulated understanding — the things we'd been calling the differentiator stack — then where does that value live?

Not in the chat interface. The interface is a container. The value lives in the layers underneath: the five-layer context model that assembles relevant information, the object model grammar that structures how Piper thinks about projects and entities, the trust graduation system that calibrates how much initiative Piper takes, the artifact persistence that accumulates understanding across sessions.

Those layers don't need a specific interface. They need a protocol.

## MCP changes the math

The Model Context Protocol is a Linux Foundation standard for connecting AI tools to LLM clients. It defines how a server exposes capabilities — tools, resources, prompts — and how a client discovers and uses them. Claude Desktop, Cursor, Windsurf, and a growing number of other clients speak MCP natively.

[CONSIDER — how much MCP explanation is needed for the audience, whether to keep it minimal]

We'd already decided that tool integrations — Slack, GitHub, Calendar, Notion — belonged in MCP plugins rather than bespoke handlers. "Don't reinvent indoor plumbing." But the PA's feasibility research surfaced a deeper possibility: what if Piper itself was an MCP server?

Build the differentiator stack as an MCP server. The context assembler becomes an MCP Resource. The trust graduation becomes a tool that calibrates responses. Artifact persistence becomes storage that any client can access. Package it for Claude's ecosystem first — that's where our users are — but the server itself is cross-platform.

The user picks their chat client. Piper shows up as capabilities within that client. No separate app to install. No new interface to learn. The agent meets you where you already work.

## What it changes

This isn't just a distribution strategy. It changes what the MVP needs to include.

We'd been assuming we needed a web interface. A chat UI. Session management. Authentication. Hosting. All the infrastructure of a standalone application. With a "Bring Your Own Chat" model, the client handles all of that. We build the intelligence layer and let existing clients provide the container.

[ADD PERSONAL DETAIL — the relief of dropping scope, or the concern about losing control of the experience]

It also reframes discovery — the problem that spawned the floor inversion investigation in the first place. In a standalone app, users ask "what can you do?" and you need onboarding flows, capability menus, contextual hints. In an MCP-powered conversation, the agent offers capabilities contextually. The user says "I need to prepare for my stakeholder meeting" and the relevant tools are right there. No navigation. No menus. The protocol handles discovery through context.

## The insight nobody planned

Here's what I find interesting about how this emerged. Nobody sat down and said "let's rethink our distribution strategy." The insight came from a collision of three things happening in the same week:

The PA researched MCP packaging feasibility for a different reason — exploring how to make Piper available alongside a sibling project. The PM had been thinking about cross-platform reach after setting up a second project on a different platform. And the strategic conversation about "methodology over code" had just clarified what Piper's actual value was.

[ADD PERSONAL DETAIL — the conversation itself, how it felt to watch the pieces click together in real-time]

Three independent threads converging into a distribution philosophy that reframes the entire product. Not through planning. Through accumulated context creating the conditions for the connection to happen.

We'd been calling this "Bring Your Own Key" — the user provides their own LLM API key, we provide the intelligence layer. "Bring Your Own Chat" extends the same principle to the interface. You bring the chat client you already use. We bring the context, the methodology, the accumulated understanding.

The plumbing is commodity. The bathing experience is the product.

---

*Next on Building Piper Morgan: [PLACEHOLDER].*

*What would change about your product if the interface was someone else's problem?*
