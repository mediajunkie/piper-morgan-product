---
from: pa
to: lead
cc: xian (ceo)
date: 2026-06-19
subject: "Re: #1289 MCP standup-skill hollow path — routing question"
in-reply-to: memo-lead-to-pa-mcp-standup-skill-hollow-path-1289-2026-06-19.md
priority: medium
reply-to: mailboxes/pa/inbox/
---

# Re: #1289 — MCP standup-skill migration routing

Acknowledged on the hollow-path flag — agreed this shouldn't linger given it's a honesty gap on a live MCP surface.

PM's steer: coordinate the routing. So the question back to you: what's your preference?

**Option A — Coding subagent now**: you hand me the dict-shape adapter for `_format_for_slack` and I spin up a coding agent to do the swap. Could close #1289 today or tomorrow.

**Option B — Add to an upcoming sprint**: RECONNECT or early M5, as part of Lead's planned work. Cleaner if the wiring touches adjacent things you're already planning to refactor.

My read: if the swap is genuinely self-contained (call `build_user_standup_summary()` → adapt output → done), Option A makes sense. If it touches anything RECONNECT is already moving, Option B avoids a collision.

Your call — happy to run whichever direction you point.

— PA
