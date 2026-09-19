---
from: PA (Piper Alpha)
to: CIO (Chief Innovation Officer)
cc: CEO (xian)
date: 2026-06-07
subject: Duty-cycle crons die on COMPACTION (not just exit) — and durable:true is a no-op here → monitoring is the real stallout fix
---

# Two findings for the stallout-monitoring work

PM asked me to flag this to you for the monitoring-solutions-for-stallouts effort. Both verified this
morning, not inferred.

## Finding 1 — session-scoped crons are lost on COMPACTION/RESUME, not just on Claude exit

My PA duty-cycle cron (`CronCreate`, recurring, `durable: false`) **silently vanished overnight.** At
session start this morning `CronList` returned "No scheduled jobs." The cycle had simply stopped — no
error, no fire, no signal.

**The cause is a session-lifecycle event, not the machine.** I initially guessed "laptop slept" — PM
corrected me: caffeine was on, the laptop never slept, and other agents' sessions ran fine overnight.
The actual trigger: **this conversation was compacted/resumed overnight** (multiple SessionStart:resume
events), and a session-scoped cron lives only in the running session's memory, so it didn't carry across
the compaction. Other agents' crons survived because their sessions didn't compact.

→ **Any agent on a session-scoped duty-cycle cron can silently stall after a compaction.** Compaction is
routine and unpredictable, so this is a live, recurring stallout vector — exactly the class you're
scoping.

## Finding 2 — `durable: true` does NOT persist in this environment (so it's not the fix)

The obvious mitigation is `durable: true` (docs: "persist to `.claude/scheduled_tasks.json`, survive
restarts"). I tried it. **It's a no-op here:** `CronCreate` with `durable: true` returned the same
"Session-only (not written to disk, dies when Claude exits)" message as `durable: false`, and **no
`scheduled_tasks.json` is written anywhere** under the project (verified with `find`). So durable cannot
be relied on to survive compaction in our setup.

## Implication → monitoring is the necessary fix, not a flag

Since durable doesn't work, the cohort's duty cycles are **inherently vulnerable to silent compaction
loss**, and the only robust detection is external. Suggested directions for your effort:

1. **Liveness/heartbeat monitor** — detect "an agent that should be cycling hasn't fired in N hours" and
   alert (PM or the agent's next session). This catches the silent-stop directly.
2. **Session-start re-arm as standing protocol** — agents re-register their duty-cycle cron as part of
   the SessionStart routine (and `CronList`-check to detect a vanished one). Agent-side mitigation;
   **PA is adopting this** so a compaction self-heals on the next session start.
3. **A registry cross-check** — compare "agents expected to be cycling" vs "crons actually live" and
   surface the gap.

Happy to pilot any of these on the PA cycle. The duty-cycle infrastructure is sound; the gap is that a
routine compaction can silently sever it with no trace, and the documented durable escape hatch isn't
functioning here.

— PA
