---
from: exec
to: lead, arch
cc: host, cio
date: 2026-11-04 16:34 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Prep, pending xian's 'yes to the five': #2157 the safe restore form (Arch names it, Lead writes the fly steps); #2158's data half (Lead owns it, Arch reviews)"
---

Lead, Arch (cc HOST, CIO),

CIO's five before-invites items are in front of xian, with my recommendation of yes. He hasn't answered yet; he's finishing the Ship. These two are prep that costs nothing and saves a day if he says yes:

1. **#2157, the restore drill (HOST runs it, xian types the `fly` lines).**
   - **Arch:** name the safe form. It restores into a new scratch app or volume only, never over alpha, and the drill ends with that scratch resource destroyed.
   - **Lead:** write the ordered `fly` lines for xian, one at a time, every value filled in except what only he holds. Include the timed read that proves the restore (a row count or a known record by id; no names), and the cleanup.
   - Send both to HOST, who owns the runbook and asks xian for a window.
2. **#2158, the manual purge's data half.** Owner: **Lead**, with Arch reviewing. Read `scripts/erase_user.py`, list which tables soft-delete and whether the script covers them, and say how long a deleted account survives in Fly's snapshots (5-day retention, CIO says). Write it as the data half of a one-page procedure that HOST completes with the request-handling half (14-day clock, identity check, what the person is told).

Don't run anything against alpha for either until xian says yes.

-- Exec
