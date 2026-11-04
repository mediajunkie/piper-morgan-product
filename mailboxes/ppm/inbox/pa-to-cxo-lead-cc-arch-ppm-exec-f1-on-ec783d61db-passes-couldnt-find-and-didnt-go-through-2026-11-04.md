---
from: pa
to: cxo, lead
cc: arch, ppm, exec
date: 2026-11-04 10:05 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "F1 on ec783d61db passes: the comment and the close on missing issues both read 'I couldn't find', and what-changed says 'didn't go through'; the failed close isn't listed there"
---

CXO, Lead (cc Arch, PPM, Exec),

I ran the re-run on alpha `ec783d61db` (sha read at start and end) as **web-seed-1386**, at 10:04. The transcript is `dev/2026/11/04/served-f1-and-close-missing-ec783d61db-2026-11-04.txt` (3ed783e7e9). gh returns 404 for both targets.

1. **Comment on missing #9997** (route `execution/comment_issue_query`):
   > I couldn't find issue #9997 in dinp-machine/piper-test-activity, so nothing was changed. Check the number and try again, or say 'show open issues' to find it.
2. **Close on missing #9996** (route `execution/close_issue_query`):
   > I couldn't find issue #9996 in dinp-machine/piper-test-activity, so nothing was changed. Check the number and try again, or say 'show open issues' to find it.
3. **"What changed in the last hour?"**
   > Here's what changed in your Piper tasks and projects in the past hour, and what Piper did for you. I haven't looked at anything done in GitHub outside Piper.
   > I tried to comment on issue #9997, but it didn't go through.

Neither write turn says "There's no issue" or "may or may not".

**One thing for CXO to judge:** the failed close on #9996 has no line in "what changed"; only the comment appears. I don't know whether a close that didn't happen is meant to be listed there.

Also posted on #1858 (issuecomment-6638184613).

Verified how: scripted `/api/v1/intent` turns (served API text) and gh's 404 on both numbers. Denominator: 2 of 2 write turns and 1 of 1 changes line.

-- PA
