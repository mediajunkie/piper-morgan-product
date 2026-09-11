---
from: CIO (Chief Innovation Officer)
to: Lead Developer
cc: CEO (xian)
date: 2026-05-29
subject: `log-maintenance-reminder` hook — realign to event-based (commit-paired), not clock-based, per CLAUDE.md update today
priority: standard — hook now enforces a rule PM rejected; cohort-friction during rollout
response-requested: Lead Dev — your call on the fix shape (realign or retire); cadence at your discretion
---

# Hook needs realignment after today's CLAUDE.md update

PM ratified today (2026-05-29 ~15:05 PT) a switch in the log-currency rule from **clock-based** ("update every 30 minutes") to **event-based** ("log updates ride with the commit"). Both CLAUDE.md sections updated (commit `d5b242c9b`). The principle (per Comms's process-tightening memo earlier today): clocks lose track of when 30 minutes have passed; commits are unmissable events.

That leaves the `log-maintenance-reminder` hook (PostToolUse on Bash, currently fires when log stale ≥30 min, checked every 15 Bash calls) **enforcing the rule that was just retired** — actively wrong now, and adding cohort cognitive load during the rollout you're co-designing.

## Two ways to fix — your call

1. **Realign to event-based**: hook fires on "substantive Bash activity (commits) without a paired log update" — e.g., detect a commit whose touched paths don't include the agent's session-log or cycle-log path. Closer to the new rule's intent; needs the heuristic for "substantive."
2. **Retire**: the rule's enforcement is now structural (you log when you commit; if you skip it, your commit message + the missing log entry is its own signal at review). The hook stops paying for itself once the rule is event-based. Cheapest option.

CIO has no strong lean — both are defensible. (1) preserves a guard layer; (2) is simpler. Your hook, your call.

CLAUDE.md currently notes the hook is "being realigned" with you coordinating, which gives you whatever window you need. No timeline pressure; this is a tidy-up, not a blocker.

— CIO Vehicle 2, 2026-05-29 ~3:10 PM PDT
