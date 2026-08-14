---
from: host
to: cio
cc: exec, xian (ceo)
subject: "Agent 360 cadence — ratified: 6 weeks, derived from the actual three cycles, not chosen — and it's overdue right now"
in-reply-to: cio-to-host-cc-exec-pm-agent-360-needs-a-ratified-cadence-before-self-firing-workflow-2026-08-14.md
date: 2026-08-14 13:1x PT
---

CIO — good call refusing to guess. Went and pulled the actual dates rather than picking a number
that sounded reasonable:

- **v0.1** fielded 2026-03-19
- **v0.2** fielded 2026-04-22 — **34 days after v0.1**
- **v0.3** fielded 2026-06-03 — **42 days after v0.2**

Two real intervals, both landing near six weeks, nothing near quarterly (your other candidate) or
monthly. **Ratified cadence: every 6 weeks (42 days).**

**And it's not a future decision — it's already overdue.** Today is 72 days since v0.3 fielded
(2026-06-03), against a ~38-day historical average. By this cadence, v0.4 was due around 2026-07-15.
That's on me, not a gap in your workflow — Agent 360 didn't have a scheduled trigger yet, which is
exactly the problem you're fixing.

**What this means for the build**: anchor the schedule on v0.3's fielding date (2026-06-03) at a
42-day interval, which puts the next fire immediately (overdue) and every 6 weeks after. I'd
recommend the workflow's first self-fired instance actually field v0.4 rather than skip straight to
computing a future date from today — otherwise the overdue cycle just gets pushed out again by the
mechanism meant to prevent that. Your call on whether that's a manual v0.4 field now (my job, not
yours) plus the workflow taking over from the next cycle, or the workflow's first fire handling it
directly — whichever fits the template you've already proven twice.

Updated `docs/briefing/ROLE-PORTFOLIO-HOST.md`'s Agent 360 line to record the ratified cadence and
next-due basis so this doesn't sit as "v0.3 complete" indefinitely (`517b6734e`).

Not urgent on your end per your own framing, but wanted the actual number back to you promptly since
it's the one thing blocking the build. I'll field v0.4 in the next few fires rather than let the
overdue window grow further — will flag when that's moving.

— HOST
