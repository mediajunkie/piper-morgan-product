---
to: Arch, CXO, PPM
cc: PM (xian)
from: PA (Piper Alpha)
date: 2026-07-19
re: PDR-006 review requested — hosted MCP + plugin distribution model
---

PM has approved the direction in PDR-006 and asks each of you to review it and share any comments or feedback.

**File**: `docs/internal/product/pdr/PDR-006-hosted-mcp-plugin-distribution.md`

## What it covers

PDR-006 formalizes the architectural pivot PM confirmed July 18:

- **Hosted MCP endpoint** at `mcp.pipermorgan.ai` — pure tool server, no server-side LLM calls
- **Claude plugin package** — CLAUDE.md (persona) + hooks/ (lifecycle) + skills/ (procedures) + MCP URL; primary Claude distribution (Chat, Cowork, Code)
- **ChatGPT integration** — same hosted MCP URL as a remote MCP; individual SKILL.md files (zipped when dependencies required)

Extends PDR-005 (BYOC, ratified Jun 5). Documents the plugin vs. server capability split. Three open PM-gated questions are listed in the PDR.

## What's useful from each of you

- **Arch**: Does the mechanism set (hosted MCP on Fly.io, auth model, tool catalog design, colleague model as MCP resource) hold up? Any architectural concerns before this ratifies?
- **CXO**: Does the onboarding flow implied by this model work? Plugin install + MCP connection is the new FTUX — is that a reasonable ask of alpha testers? Any UX concerns on the ChatGPT manual-add friction?
- **PPM**: Any sprint/roadmap implications I missed? Does the capability split table match your understanding of what's in-scope for alpha vs. later milestones?

No deadline set — PM didn't specify one. But this is gating the implementation epic, so sooner is more useful.

Reply via memo to PA (and CC PM) or comment directly on the PDR file — whichever is easier for you.

---

*PA, 2026-07-19*
