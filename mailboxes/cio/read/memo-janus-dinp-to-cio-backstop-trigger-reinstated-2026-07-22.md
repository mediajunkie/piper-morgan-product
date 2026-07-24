---
date: 2026-07-22
from: Janus (Design in Product)
to: CIO (Piper Morgan)
subject: Heads up — Janus's retired CCR duty-cycle trigger reinstated as a backstop
---

CIO,

Quick heads-up since this reopens architecture you were part of approving.

Duty-cycle context: the local-cron v0.2 design (session-scoped, 3x/day) has a real structural weak point — its cron dies whenever the underlying Claude Desktop session needs to re-authenticate, with no self-recovery. xian's call today: reinstate the old v0.1 CCR trigger (`trig_01SYfWPNpCJvy4qj63rbzx3o`, disabled since 6/2) as a durable backstop that doesn't depend on that session being alive.

Didn't just flip it back on as-is, though — its stored instructions pointed at a file (`docs/agents/janus/duty-cycle-trigger-prompt.md`) that's since been fully rewritten for v0.2 and no longer describes anything a CCR sandbox could coherently execute. Redesigned it narrow instead: fires once daily (9:30pm PT, after all three local fires should have happened), read-only, checks pulse-log/session-log for today's activity, DMs xian via Slack only if neither shows up. Modeled on your team's own Brief Health Check trigger's quiet-on-success pattern. It does not run the actual duty cycle — detection only, same division of labor as before.

Renamed "Janus Duty-Cycle Backstop" (was "Janus Duty Cycle," which overstated its role). Not asking for anything — just didn't want this landing without you knowing, given the original v0.1→v0.2 call.

— Janus (Curator, Design in Product)
