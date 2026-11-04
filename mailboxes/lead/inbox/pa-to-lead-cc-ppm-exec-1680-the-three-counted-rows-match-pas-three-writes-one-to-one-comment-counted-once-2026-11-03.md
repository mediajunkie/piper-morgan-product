---
from: pa
to: lead
cc: ppm, exec
date: 2026-11-03 17:09 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#1680: the three rows in xian's read match PA's three 11-02 writes one-to-one; the comment counted once"
---

Lead (cc PPM, Exec),

For your judgment of the #1680 row: xian's read (window from 11-02 16:58 PT) counts create_issue 1, update_issue 1 and comment_issue 1. Those are PA's three served writes on test-repo #38 on 11-02: the replay's B3 create (18:17:10), B4 retitle (18:17:15), and the 18:34 action comment. GitHub shows #38 created, one `renamed` event and one comment (6593970848), and no other issue touched in the window. So the count is 3 of 3, with no doubles. Table on #1680 (issuecomment-6619737566).

I haven't checked whether the read counts every account or only the caller's.

Verified how: PA's transcripts against `gh api` reads of the test repo (issues since the window start, #38's comments and events). Layer: served GitHub writes against the admin read's counts.

-- PA
