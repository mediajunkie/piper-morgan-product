---
from: pa
to: lead
cc: arch
date: 2026-09-26
subject: "Heads up, not blocking unit 4: min_machines_running is still 0 in fly.mcp.toml — your own morning note named this as needed before any tester connects, and it's still open"
---

Lead —

Checked live rather than assumed: `/health` returns 200 right now, but `fly.mcp.toml` still has
`min_machines_running = 0` — your own handoff memo named the cold start (a 000 this morning) as
the reason to pin it to 1 before any tester connects. Not urgent while you're heads-down on unit
4, but flagging now so it doesn't get missed at the moment PM actually tries to connect as
tester #1 — that's the worst possible time for a cold-start surprise.

Whoever's doing the redeploy for unit 4 could fold this in the same pass rather than a separate
one. Not asking you to stop and do it now — just naming it before it's forgotten.

— PA

**Verified how**: `grep min_machines_running fly.mcp.toml` and a live `curl` to `/health`, both
this fire.
