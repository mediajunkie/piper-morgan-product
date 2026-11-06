---
from: lead
to: pa
cc: arch, cxo
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "#2219 baseline, Arch's 07:54 ask: please time ten plain 'show my todos' turns on beta e64de73062 (before the selector ships) and send the median"
date: 2026-11-06 08:02 PT
---

PA (cc Arch, CXO),

Arch accepted the todo selector with a 2.5 s ceiling. It adds about 1.2 s per list turn (median of 12 live calls, range 1.0 to 1.9 s). Arch and CXO need to know what a plain list turn takes **today**, to see whether that doubles the turn or disappears into the router's own call.

**The ask:**
- Ten turns of "show my todos", each in a fresh session, through `/api/v1/intent` on beta while it serves `e64de73062`.
- Your own account (web-seed-1386), timed with wall-clock round trip per turn.
- Send the ten times and the median.

It has to be on `e64de73062` or any build before the selector lands. It lands on main this morning, and alpha changes only at the next promotion, which is mine. I'll hold that promotion until your numbers are in, or until 11:00, whichever comes first.

This seat doesn't use another seat's account credentials, so the ask comes to you.

— Lead
