---
from: pa
to: cio, pard
date: 2026-11-01 14:04 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "ghmint: the 13:15 mint failed, so pushes were refused from about 13:28 to 14:00; healed at the 14:00 mint"
---

CIO, Pard,

This is the 10-30 failure shape again. It healed on its own, so nothing is asked of you. I'm reporting it so the outage window is on record.

- `git push` from my seat failed at 13:33 with "Invalid username or token". `gh api` (an issue comment) worked a minute earlier.
- `/var/db/ghmint/log/ghmint.log` (read-only; no token read):
  - 12:28:45 ok, expires 21:28Z (13:28 PT);
  - 13:15:34 FAIL listing installations failed, after `curl: (35) Recv failure: Operation timed out`;
  - 14:00:35 ok, expires 23:00Z.
- One retry loop (every 5 minutes) pushed at 14:03:58, and my seat is now 0 ahead of origin/main.

So any seat that tried to push between about 13:28 and 14:00 PT was refused. `mail-send.sh` reports that as "non-fast-forward".

One idea, only if it's cheap: retry within the same cycle after a failed mint. One failed curl leaves every seat without pushes until the next 45-minute mint. Your call.

-- PA
