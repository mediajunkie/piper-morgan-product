---
from: Piper Alpha (PA), on behalf of PM
to: Chief Architect
date: 2026-04-08
subject: Vision V2.1 + Roadmap restructure + MCPB feasibility — Architect review requested
priority: normal
---

# Vision V2.1 + Roadmap Restructure + MCPB — Architect Review

PM and PA have been working through a product strategy conversation that touches the tech stack. We'd like your architectural review.

**Documents to review**:
1. `docs/internal/planning/current/vision-v2-draft.md` (Vision V2.1)
2. `dev/active/roadmap-restructure-proposal-2026-04-08.md` (Roadmap v15.0 proposal)
3. `dev/active/mcpb-feasibility-2026-04-08.md` (MCPB distribution research)

**The architectural questions**:

1. **MCPB as primary distribution**: Research confirms MCPB can handle persistent SQLite storage, external API calls, and MCP Apps (interactive HTML in chat). The gap: MCP servers cannot inject into the system prompt. Proposed solution: hybrid approach — MCPB for tools/storage/UI, Claude Project for persona/instructions. Does this architecture hold? What are the risks?

2. **Action gate simplification**: We're questioning whether the 19-category intent classifier is over-specified. If most categories route to the floor anyway, could a simpler binary ("does this need a side effect?") suffice? What would we lose by simplifying?

3. **Bespoke web UI vs MCP Apps**: If MCPB + MCP Apps can render artifact browsers and project dashboards inside Claude Desktop, what's the case for maintaining the standalone web UI? Is the web UI still the right development/testing surface even if it's not the distribution product?

4. **Context assembler as MCP Resource provider**: Could the existing context assembler be adapted to serve project state as an MCP Resource? This would let the floor pull rich context without handler infrastructure.

5. **The WIRE-* issues**: With floor-first routing, how many of the wiring issues (#690-695) are still architecturally necessary? Which handlers genuinely need wired MUX integration vs which just need good context assembly?

6. **Prototype request**: Could we build a minimal MCPB that exposes 2-3 Piper tools (save artifact, retrieve artifact, get project status) to test the UX in Claude Desktop? How much effort?

**Supporting analysis**:
- `dev/active/mux-analysis-what-survives-floor-first-2026-04-07.md` — what survives
- `dev/active/backlog-deep-review-2026-04-07.md` — superseded issues analysis

No timeline pressure, but the MCPB question is architecturally significant and could reshape our MVP scope.
