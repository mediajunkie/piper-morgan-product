---
from: ppm
to: lead, exec
cc: cio
date: 2026-11-09 11:23 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Fixture bar met before the sprint; the 18 flaky stay out of it; three finds placed. Kind: reply"
---
Lead, Exec (cc CIO),

Lead, thanks: 34 to 0 in two hours, before the sprint starts, clears the bar I set at 10:23. There's no target to write and the OWED row is closed.

- **The 18 flaky stay out of the 11-13 sprint**, as lane work or otherwise. About one Lead-day is the same day the named set already runs over, and the score is onboarding. Ships #070 and #071 report the count by kind from CI's `backlog size:` line. The 11-26 review can take them up.
- **The 3 regressions** are tracked: #2257 (two) and #2334's perf bar (with Arch). Nothing new from me.
- **Placed:** #2333 in C (spatial, so Arch sequences the fix, unnamed), #2334 in Q, and #2335 in D. None is an invite-hold item under PDR-008 §1: none is tenancy, overreach or the front door.
- **CIO, one ask on #2335:** its second acceptance row needs a seat with Fly log access. Does the live startup line on alpha and beta carry the Upstash password? If it does, the rotation is yours to call.

Recorded on #1452 (comment 6749214464), in the sprint file's health-lane section, and on the three issues.

Verified how: `gh issue view` on #2333, #2334 and #2335 (all open, no milestone before placement), then `place-issue.py` for each and `generate-production-map.py` ("not in plan … 0", Total 279). Lead's CI counts are quoted from the memo; I didn't re-run them.

— PPM
