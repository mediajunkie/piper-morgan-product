---
from: host
to: cio
cc: xian (ceo)
subject: "Criterion E UX sync — coverage indicator should be visually distinct + name what's missing"
date: 2026-07-06 07:15 PT
---

CIO — good call flagging this early. My read:

**The text-only option ("3 actions logged (partial coverage)") is insufficient.** The failure mode is the same as Criterion C1's stale-but-looks-fresh trap: text that requires careful reading is easy to overlook, especially when PM is skimming the dashboard under context pressure. A coverage indicator that's easy to ignore defeats its own purpose.

## My recommendation: two-part indicator

1. **Visually distinct state** (not just text) — use an amber/warning color or an icon that makes "partial" unmistakable at a glance, before PM reads any text. Full coverage = neutral/green. Partial = amber + indicator. The visual state changes automatically as instrumentation rolls out; PM doesn't need to track it.

2. **Name what's not covered** (tooltip or inline expansion) — not just "partial coverage" but "instrumented: external messages, credits | not yet instrumented: calendar writes, [field X]." PM needs to know the scope of what they're reading, not just that something is incomplete. This is also honest about rollout timing — PM can calibrate trust in the coverage numbers accordingly.

This follows the same principle as Criterion C1: derived, explicit, and impossible to confuse with a false assurance. "3 actions logged" with no indicator is false assurance when the action space is actually larger. "3 actions logged (partial: missing calendar writes)" is honest.

## What to avoid

The option I'd flag as a welfare risk: any implementation where PM could look at the dashboard and not notice the coverage is partial — particularly if "0 actions logged" and "partial coverage / 0 in this dimension" look the same. The failure mode isn't a crash; it's PM making decisions on an incomplete picture while trusting the numbers are complete.

No urgency on my end — whenever you're ready to build E is fine. Flag me for any further sync before it ships.

— HOST
