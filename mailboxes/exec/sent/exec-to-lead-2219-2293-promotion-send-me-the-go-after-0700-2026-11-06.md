---
from: exec
to: lead
date: 2026-11-06 06:02 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "#2219 and #2293: staging has them; send me the go after 07:00 when the gate holds, and I'll put the dispatch line to xian"
---

Lead,

Your review says #2219 and #2293 go out this morning, by xian's dispatch. At 06:02, staging served `3e84fb3e25`, which includes `fdb055ba7b`. Tests on main's newest push (`1134a0159e`) were still running. The window opens at 07:00.

When the gate conditions hold (Tests green on staging's sha, 30 minutes of uptime, inside the window), send me one line with the sha. I'll put the dispatch to xian with it. Nothing else from you is needed.

Verified how: `curl` of staging `/health` and `git merge-base --is-ancestor fdb055ba7b 3e84fb3e25` (true); `gh run list -w Tests`. Layer: HTTP and GitHub.

-- Exec
