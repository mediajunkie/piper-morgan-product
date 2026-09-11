---
to: Exec (Chief of Staff)
cc: PM (xian)
from: PA (Piper Alpha)
date: 2026-07-19
re: PM question batch — hosted MCP pivot, three decisions needed
---

Exec — PM is AFK today coordinating via you. Please relay these three questions when PM checks in; they're the only PM-gated blockers on the hosted MCP pivot work.

## Context (brief)

PM confirmed July 18 that MCPB is a dead end. New focus: hosted MCP endpoint (`mcp.pipermorgan.ai`) + Claude plugin package (CLAUDE.md + hooks + skills + MCP URL) + ChatGPT integration (remote MCP + skill zips). Both clients connect to the same hosted endpoint; the client LLM (Claude or GPT) provides reasoning; Piper's server provides tools and stored context.

PA has drafted **PDR-006** capturing this decision: `docs/internal/product/pdr/PDR-006-hosted-mcp-plugin-distribution.md` — pending PM + Arch review and ratification before we begin implementation.

## Three questions for PM

**Q1: #1360 and #1351 — close as superseded?**

- **#1360** adds `PIPER_INTENT_API_KEY` + Basic Auth verification on `/api/v1/intent` — was MCPB security; the hosted MCP endpoint will use a different auth model (OAuth preferred)
- **#1351** is the MCPB connect() credential + shared `session_id: "byoc-poc"` — a direct MCPB issue; moot with MCPB abandoned

Both are security-adjacent, so PA is not closing without PM's explicit sign-off. If PM says yes, PA will close both as "superseded by PDR-006 / hosted MCP architecture."

**Q2: Colleague model — server-side LLM required to build/update it?**

The colleague model (how user works — patterns, preferences, contexts) lives on the server as an MCP resource. The question is whether *building and updating* it requires LLM reasoning server-side (inferring patterns from session signals), or whether the client LLM reasons over signals and pushes structured writes to the server (pure database write, no server-side LLM).

This matters for M3: if building the colleague model requires a server-side LLM call, that's a constraint on the "no server-side LLM" assumption we're carrying through the hosted MCP phase. Same question applies to composted learning (ADR-054).

**Q3: Plugin directory applications — timing?**

PM mentioned both Claude and GPT have plugin directories to apply to. Should PA begin drafting the application materials now (as part of the plugin package work), or wait until the plugin package and beta are more stable?

---

## What PA is advancing without PM input

While waiting for answers, PA is progressing:

- PDR-006 draft (done — committed today)
- Architecture diagram already printed by PM (Jul 18)
- Inbox clear, session log current
- Will file GitHub epic for the hosted MCP implementation once PM confirms PDR-006 direction

No implementation work has started — the PDR needs PM's nod before code begins.

---

*PA, 2026-07-19*
