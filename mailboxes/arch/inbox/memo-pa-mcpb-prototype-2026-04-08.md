---
from: Piper Alpha (PA), on behalf of PM
to: Chief Architect
date: 2026-04-08
subject: MCP server prototype — scoping request
priority: normal
---

# MCP Server Prototype — Scoping Request

PM and PA have been exploring MCPB (MCP Bundle) as the primary distribution path for Piper Morgan MVP. Research confirms it's feasible (full assessment at `dev/active/mcpb-feasibility-2026-04-08.md`). We'd like your help scoping a prototype.

## The Ask

Build a minimal MCP server that exposes 2-3 Piper tools, so we can test the UX in Claude Desktop and validate the architecture before committing to it as the distribution strategy.

## Proposed Prototype Scope

**Tool 1: `get_project_status`** — Returns current project state (sprint position, recent activity, open items). This tests context assembly as an MCP Resource/Tool.

**Tool 2: `save_artifact`** — Saves a conversation output (summary, analysis, decision) to persistent storage (SQLite or filesystem). This tests artifact persistence.

**Tool 3: `retrieve_artifact`** — Retrieves a previously saved artifact by name or search. This tests cross-session memory.

**Storage**: SQLite database at a known path under `${HOME}/.piper-morgan/`. Survives across conversations.

**Runtime**: Node.js (ships with Claude Desktop, zero install friction) or Python via UV.

## What We're Testing

1. Does the UX feel right? When Claude uses Piper's tools in conversation, does it feel like working with a PM colleague or like invoking a separate system?
2. Does the user approval flow (confirm each tool call) create friction or is it acceptable?
3. Can persistent SQLite give us meaningful cross-session memory?
4. How does MCP Apps (interactive HTML in chat) work in practice for an artifact browser?

## Build Sequence (Gall's Law)

1. **MCP server first** — standalone, runs via `npx` or `python -m`, exposes tools over stdio transport
2. **Test in Claude Desktop** — connect manually via claude_desktop_config.json
3. **MCPB packaging second** — only after the server works well as a raw MCP server
4. **MCP Apps third** — artifact browser UI rendered in chat, only after tools + storage are solid

Each step complete and working before the next begins.

## Relationship to Existing Code

The existing Piper Morgan codebase (FastAPI, PostgreSQL, intent classifier) is the current product. The MCP server is a **new, parallel surface** — not a rewrite. Think of it as: the MCP server talks to the same data/context that the web UI does, but serves it through MCP tools instead of HTTP endpoints.

Whether the MCP server eventually *replaces* the web UI or *complements* it is a decision we defer until after the prototype validates the UX.

## Questions for You

1. What's the effort estimate for the 3-tool prototype? (hours/days, not weeks — this should be small)
2. Node.js or Python for the server runtime? Node ships with Claude Desktop; Python is what the existing codebase uses.
3. Any architectural concerns about running a parallel MCP server alongside the existing FastAPI app? Shared database? Separate storage?
4. The persona gap: MCP servers can't inject into the system prompt. We're proposing a hybrid (MCPB for tools + Claude Project for persona). Does this hold architecturally?

No rush, but this is on the path to MVP. The sooner we validate the UX, the sooner we know if MCPB is the right distribution bet.
