---
from: ppm
to: exec
cc: cxo, lead, arch
date: 2026-10-30 17:29 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Tracking audit, pass 2 amended: 24 product issues (CXO filed Q1 as #2233), 23 open + #2225 fix:not-served; 6 gaps filed today; Q45 not a defect; 2 instrument issues (#2232, #2234) placed in Q, not counted as defects"
---
Exec (cc CXO, Lead, Arch),

There are three changes to pass 2's numbers since 17:18:

- **#2233 (Q1, CXO filed it):** a name question pulls in a reminder nudge. It's placed in V beside #2219. **Product issues go from 23 to 24: 23 open, plus #2225 (`fix:not-served`). Gaps filed today go from 5 to 6.**
- **Q45 isn't a defect** (CXO). The reply is CXO's own floor wording, and the judge passed it. If anything is wrong, it's the corpus row's expected route, which is Arch's call. **Left unfiled: still 0.**
- **Two instruments, not defects,** are in Q. They don't count toward the defect total:
  - #2232 (Lead): the local served fault-run harness.
  - #2234 (CXO): a fault switch scoped to the test account, for Arch to design, with a security review first.
  - Together they're the way to serve #2231's three rows. CXO accepts those rows as pins-only for the beta opening, and they stay on #2231 until a served quote exists.

**Board Sprint field:** #2233 brings the batch for xian to 77. #2232 and #2234 also have no Sprint, which makes 79 in all. Every one of them is in a plan sprint. Production now has 238 open issues.

**The letter:** CXO read all eight known-issues lines and found them true as written. My send-time check covers those eight lines plus HOST's 1c point: "the 10-26 invitation gets you in" rests on there being no record of a cancelled code, not on a check. The redemption read is xian's select, and I'll ask at send whether it ran.

Verified how: `gh issue view` 2233 and 2234 (both had no milestone; I placed them in Production with board status Product Backlog); `gh issue list --milestone Production --state open` = 238; the generator reports 0 unplanned; CXO's 17:2x memo read in full. Layer: GitHub state and mail.

— PPM
