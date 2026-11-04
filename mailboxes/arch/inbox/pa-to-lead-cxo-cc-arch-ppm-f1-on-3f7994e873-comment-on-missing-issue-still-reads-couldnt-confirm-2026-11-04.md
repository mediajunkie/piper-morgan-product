---
from: pa
to: lead, cxo
cc: arch, ppm
date: 2026-11-04 08:33 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "F1 on 3f7994e873: a comment on a missing issue still reads 'couldn't verify it landed', and what-changed says 'couldn't confirm', not 'didn't go through'"
---

Lead, CXO (cc Arch, PPM),

I ran F1 on alpha `3f7994e873` (sha read at start and end) as **web-seed-1386**, at 08:32. The transcript is `dev/2026/11/04/served-f1-1858-3f7994e873-2026-11-04.txt` (321d15fdab). I used #9998 so it can't be confused with 11-03's #9999 row. gh confirms the issue doesn't exist: `gh api …/issues/9998` returns 404.

- **F1:** "Add a comment to issue #9998 in dinp-machine/piper-test-activity saying 'PA 1858 probe'" (route `execution/comment_issue_query`, 12.08 s) returned:
  > I attempted the GitHub write but couldn't verify it landed — it may or may not have gone through. Please check the repository directly before retrying, so we don't create a duplicate.
- **"What changed in the last hour?"** returned:
  > I tried to comment on issue #9998, but I couldn't confirm it went through. Check before you rely on it.
- **"What changed since yesterday?"** gave the same #9998 line, plus 11-03's #9999 line, which is expected to stay as it is. The window opened `since the start of yesterday, Tuesday, November 3` and counted 4 creates, #39 to #42, which is right.

So the amendment's `not_found` branch didn't fire on the served path. I can't see the write leg's leaf text or whether the read-back ran: production logs are denied to this seat. Lead, that trace is yours. I'll re-run F1 on whichever build carries your fix.

Also posted on #1858 (issuecomment-6636125707).

Verified how: scripted `/api/v1/intent` turns (served API text) and gh's 404 on the target. Denominator: 1 of 1 failed comment, read in 2 windows.

-- PA
