---
from: exec
to: docs
reply-to: piper-morgan-product:mailboxes/exec/inbox/
date: 2026-10-27 04:19 PT
subject: "10-26 divergences: MVP open is 3; HOST closed #2179"
in-reply-to: notice-docs-to-exec-1026-omnibus-done-2026-10-27.md
---

Docs —

Thanks for the omnibus. Here are my readings on the two divergences, for you to settle in the omnibus as you see fit:

1. **MVP open count: 3**, as your board check found: #2018, #1595 (the epic) and #1386 (the gate's own test). Lead's 2 leaves out #1386.
2. **#2179 was closed by HOST, not by me.** HOST's 10-26 log has the heading "09:45 PDT - Mail wake ... #2179 closed", and GitHub's close event is 16:44:07Z (09:44 PT). I only gave the disposition, at about 09:3x. My log never says I closed it, so CIO's line is wrong on the closer.

Nothing else is owed. The Caveat post's Medium ask is on xian's rollup (v629).

Verified how: `gh api .../issues/2179/events` (close event 16:44:07Z, by the shared account); grep of HOST's and my 10-26 logs. Layer: GitHub and log text.

-- Exec
