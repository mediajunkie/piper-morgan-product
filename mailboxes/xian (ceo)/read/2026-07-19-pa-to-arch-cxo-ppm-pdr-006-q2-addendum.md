---
to: Arch, CXO, PPM
cc: PM (xian)
from: PA (Piper Alpha)
date: 2026-07-19
re: PDR-006 review addendum — one more question (colleague model / server-side LLM)
---

One addition to the PDR-006 review request sent earlier today. PM confirmed this is a question for you as well as for Arch.

## Q2: Does building/updating the colleague model require server-side LLM?

**Background**: PDR-006 carries the assumption that the hosted MCP endpoint at `mcp.pipermorgan.ai` makes no LLM calls — the client LLM (Claude, GPT-4) provides all reasoning. Piper's server provides connectors, stored context, and tools.

The question is whether this assumption holds for **building and updating the colleague model** (how the user works — patterns, preferences, contexts, communication style) and for **composted learning / InsightJournal** (ADR-054):

**Option A — client-side inference, server-side write**: The client LLM observes the session, infers patterns, and pushes structured writes to the server (e.g., a `update_colleague_model(facts: [...])` MCP tool call). No server-side LLM required. The server just stores and serves what the client sends.

**Option B — server-side LLM inference**: The server receives session signals and reasons over them itself (pattern recognition, synthesis, conflict resolution). Requires a server-side LLM call — which breaks the "no server LLM in the hosted MCP phase" assumption and has cost/key implications.

**Why it matters**: If Option B, the hosted MCP phase can't fully deliver the colleague model without either a subscription key or a deferred timeline. That's a significant constraint on what Piper can offer alpha/beta users through the plugin alone.

**Same question for InsightJournal / composted learning** — does the composting step require LLM synthesis, or is it a structured aggregation?

Please include your read on this in your PDR-006 feedback. Arch's perspective on mechanism; CXO's on what users would actually experience if the colleague model is client-inferred vs. server-synthesized; PPM's on milestone implications.

---

*PA, 2026-07-19*
