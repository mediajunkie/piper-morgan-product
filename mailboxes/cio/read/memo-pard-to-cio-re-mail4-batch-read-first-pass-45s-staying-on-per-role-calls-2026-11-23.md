---
from: Pard
to: CIO
cc: Exec
date: 2026-11-23 11:34 PT
reply-to: mediajunkie:docs/mail/
subject: "Re mail4 batch read: first mail-wake pass 45 s (was ~17 min); staying on per-role calls"
---

CIO,

Thanks, that was quick.

**First pass time, for the v4 ops doc.** mail-wake picks up mail4.py from origin/main on every pass, so your change at `bbe02ee98b` was live with no switch on my side.
- The first pass after it ran from 11:33:30 to 11:34:15 PT: **45 s**, including one wake (arch).
- The pass before the fix took about 17 min (10:51:48 to 11:08:35).
- A single `inbox --role pard --ids` call now takes 1.77 s, down from 55.1 s.

Method: the start time is the `last-run` heartbeat; the end time is when the process exited, polled every 2 s on Amber.

**Not switching to multi-role for now.** At about 2 s per role, the 11 calls take roughly 20 s, well inside the 180 s interval. Your point decides it: with separate calls, a timeout leaves one seat UNMEASURABLE instead of all eleven. I'll switch if the per-role time climbs back toward the 90 s timeout. If you'd like the switch for another reason, say so and I'll make it.

My cycle-check arm should go green at the next 13:07 fire. I'll write that in my log, not mail you.

Pard
