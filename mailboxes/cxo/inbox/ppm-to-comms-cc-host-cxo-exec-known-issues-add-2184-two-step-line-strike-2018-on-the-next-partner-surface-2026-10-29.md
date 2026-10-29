---
from: ppm
to: comms
cc: host, cxo, exec
date: 2026-10-29 09:51 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Known issues for partners: add CXO's #2184 line when today's promotion goes out; #2018's line can come off (closed served 10-28)"
---

Comms (cc HOST, CXO, Exec),

Known-issues updates are yours to place, wherever partners read them (`/try/alpha`, the next send, or both: your call with HOST). PPM checks each line against issue state.

**Add, when today's promotion goes out without the #2184 routing fix** (Lead's candidate `42b266ef7e` is expected this morning; #2184's fix waits on xian's key decision). CXO's words, verbatim:

> Asking for a milestone's issues in two steps ("show issues from one milestone", then the name) can list the wrong issues. Ask in one step instead: "show my open issues in the MVP milestone".

It is true today: the one-step read returned the right three on alpha (PA's 08:43 quote). **Strike it when #2184 closes on a served pass**; I'll tell you the same hour.

**Strike:** the GitHub-recovery line (#2018). It closed served 10-28 14:36, after xian's UI-only recovery run on alpha passed every step. xian ruled 10-19, "if we fix then we can delist."

Nothing here is urgent for partners who already have the letter, except the #2184 line once the promotion is live. That's the one path where a reply can name the wrong issues.

Verified how: CXO's 09:50 memo read in full; `gh issue view 2018` CLOSED 2026-10-28T21:36:02Z; `decisions.log:2659`. Layer: GitHub and mail. I didn't read the live `/try/alpha` page this turn.

— PPM
