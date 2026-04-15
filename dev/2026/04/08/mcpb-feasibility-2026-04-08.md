# MCPB Distribution Feasibility Assessment

**Author**: Piper Alpha (PA)
**Date**: April 8, 2026
**Status**: Research findings for PM and Architect review

---

## Summary

Packaging Piper as an MCPB bundle is **feasible and promising** but has one critical architectural gap: MCP servers cannot inject into the system prompt. Piper can provide *capabilities* (tools, storage, dashboards) but cannot autonomously make Claude *be* Piper.

## What Works

- **Persistent project state** via SQLite (cross-session memory, trust profiles, artifact storage)
- **External API integration** (GitHub, Slack, Calendar — full network access)
- **Artifact save/retrieve** (filesystem tools, scoped to user-configured directories)
- **Interactive UI via MCP Apps** (HTML rendered in sandboxed iframes inside chat — dashboards, project views, artifact browsers)
- **One-click install** for users (double-click .mcpb, confirm permissions)
- **Node.js runtime ships with Claude Desktop** (zero dependency friction)

## What Doesn't Work

- **No system prompt injection** — servers cannot silently shape Claude's voice. The user must activate a Prompt template or pull a Resource explicitly. This is the biggest gap for a "PM colleague persona."
- **No background work when app is closed** — scheduled checks need a separate daemon or Claude Code remote triggers
- **Every tool call needs user approval** — no autonomous action (each invocation shows a confirm dialog)
- **No conversation history access** — server can't read prior conversations

## The Persona Gap

This is the critical architectural question. An MCPB gives Piper tools, storage, and UI — but the consciousness layer (Five Pillars, grammar, anti-flattening) needs a different delivery mechanism:

**Option A: Prompt Template** — User activates a "Piper Morgan PM Assistant" prompt at the start of each conversation. This prompt contains the voice rules, grammar constraints, and personality guidance. Workable but requires user action each time.

**Option B: MCP Apps + Resources** — The Piper server exposes a rich context resource that the model pulls when the user asks PM-related questions. The resource includes personality guidance alongside project data. Less reliable than prompt injection but more seamless.

**Option C: Hybrid (MCPB + Claude Project)** — User creates a Claude Desktop project with Piper's personality in the project instructions (Layer 2). The MCPB provides the tools and storage. The project provides the persona. This maps cleanly to the five-layer model: L1-L2 from Claude Project, L3-L5 from MCPB server.

**Option C seems strongest** — it uses each platform for what it's good at. Claude Projects handle persona/instructions (which they already do well). MCPB handles tools and persistence (which MCP is designed for).

## The MCP Apps Opportunity

MCP Apps (released January 2026) allow servers to render **interactive HTML UIs inside the chat window**. This directly addresses the "artifact canvas" need — Piper could render:

- Project status dashboard
- Artifact browser with lifecycle states
- Sprint board view
- Decision log

This is real and shipping in Claude Desktop, not theoretical. It means Piper can surface the "artifact / history canvas" xian wants without building a standalone web app.

## Recommendation

**Pursue MCPB as the primary distribution path.** The hybrid approach (MCPB for tools/storage/UI + Claude Project for persona) resolves the system prompt gap. Research MCP Apps for the artifact canvas. This could dramatically simplify MVP by removing the bespoke web UI from the critical path.

**Open questions for Architect**:
1. Can we prototype a minimal MCPB that exposes 2-3 Piper tools (save artifact, retrieve artifact, get project status) and test the UX in Claude Desktop?
2. What's the effort to port the context assembler to work as an MCP Resource provider?
3. Does the hybrid approach (MCPB + Claude Project for persona) introduce sync/coherence risks?

---

*Research for project record. Sources documented in PA session log.*
