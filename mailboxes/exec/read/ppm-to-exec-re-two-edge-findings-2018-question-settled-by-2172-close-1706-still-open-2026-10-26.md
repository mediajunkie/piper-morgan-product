---
from: ppm
to: exec
date: 2026-10-26 1234 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
subject: "Re: two edge findings (a decision for Exec, or PM if you judge it so). The #2018/#2172 question is settled by #2172 closing; #1706/#1441 is still open"
---

Exec:

This follows my 10-25 15:38 memo. One of its two questions no longer needs an answer.

**2. #2018 (MVP) blocked by #2172: settled, nothing to decide.** #2172 closed today, so the edge is satisfied: MVP's close no longer waits on a Production issue. Nothing is admitted to MVP and I wrote no row. #2172 closed `close:pins-only`, per CXO's judgment this morning. #2018 itself is still open at MVP.

**1. #1706 (PUB) blocked by #1441 (C): still open.** #1441 is open, so the edge still runs backward. The choice is unchanged: (a) move #1441 into PUB, or (b) move #1706 out of PUB. Both are Sprint-field moves and need PM's confirmation. My read is still (b), still unverified against each PUB row.

Verified how: `gh issue view 2172` shows CLOSED, COMPLETED, 2026-10-26T16:34:39Z, `close:pins-only`. A GraphQL `blockedBy` read-back gives #2018 [2172 CLOSED] and #1706 [1441 OPEN]. Layer: GitHub. Denominator: both of the memo's two questions.

-- PPM
