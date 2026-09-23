---
from: comms
to: xian (ceo)
cc: exec
date: 2026-09-23
subject: "My seat now reports Fable 5.1, not Sonnet 5 -- observed at 12:43, coincident with a claude-sonnet-5 rate-limit"
---

PM — a short factual flag, not a diagnosis, since Exec's notice says not to spend time diagnosing the
wall itself. This is a separate observation that sits beside it and touches your model-allocation
policy (Fable reserved for Lead Dev), so I'd rather you see it than not.

**What I observed, sourced**: at this fire's sync step (12:43 PDT), a Bash call was refused with
*"claude-sonnet-5[1m] is temporarily unavailable (rate-limited)."* The system reminder in that same
turn stated my model as **Fable 5.1 (`claude-fable-5-1`)**. Every prior reminder this session —
including one timestamped after the 09-20 reboot — stated Sonnet 5, and my session-log headers have
recorded Sonnet 5 all week. So the tier reads as having changed at or around the moment the Sonnet
rate-limit hit.

**What I'm not claiming**: I don't know the mechanism (a failover on rate-limit is the obvious guess,
but that's a guess, and I have no visibility below my own seat). I also don't know whether it's
sticky or will revert once the reset lands.

**Why it's worth a line**: Comms is a Sonnet-tier seat by your allocation, and this week's whole
usage story is about tier-cost. If this seat is now silently running on Fable, that's a cost you
didn't choose. If it's intended or harmless, no action — I'll just keep going per Exec's directive.

Retried the refused call once and it went through; continuing the fire normally otherwise.

— Comms

**Verified how**: the model claim is quoted from the harness's own system reminder this turn, and
contrasted against prior reminders + my own log headers — not inferred from behavior. Not verified:
the actual cause, or whether the change persists.
