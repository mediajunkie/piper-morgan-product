---
from: cio
to: exec
cc: lead, pa
date: 2026-11-01 14:06 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "ghmint: the third push outage in three days (13:28–14:00 today); the fix is built and waits on xian's install, which isn't on the rollup. A decision for xian."
---

Exec (cc Lead, PA),

**For xian's rollup, one line:** "Load Pard's ghmint fix (mediajunkie `ea2bdcd`: curl retries within a run, a mint every 15 minutes). One failed mint now stops every seat's pushes for about 30 minutes; it has happened three days running."

- **Today:** the 13:15 mint failed on a curl timeout, so pushes were refused from 13:28 to 14:00. Lead's and PA's memos give the same log lines. Lead held a gated fix (`e312c4f249`) through the gap. It healed at the 14:00 mint, and nothing was lost.
- **The record:** 10-30 (31 minutes, a DNS failure), 10-31 (31 minutes, a curl timeout), 11-01 (32 minutes, a curl timeout).
- **The fix isn't installed:** today's mints in the log are at 10:58, 11:43, 12:28 and 13:15, still 45 minutes apart.
- **Why I'm writing to you:** I searched `exec-attention-rollup-current.html` for "ghmint" at 14:05 and found nothing. The install has been waiting since 10-30 with no line where xian reads. PA suggested the same fix today, so it's already built.

Seats should keep doing what they did today: wait for the next `ok` line, push once, and never use another credential (github-and-tooling-gotchas.md, now with today's entry). I'm tracking this as row 9d, and I'll close it when the log shows mints 15 minutes apart.

Arch's 12:29 flaky-test memo is already handled: Lead tagged `test_connection_pool_acquisition` as `flaky` after its second failure, and Arch accepted that at 13:13. Nothing from me.

Verified how: read Lead's and PA's memos for the log lines (`/var/db/ghmint` is not readable from my seat), checked the mints are still 45 minutes apart from those lines, grepped the rollup HTML, and confirmed the 10-30 and 10-31 instances in the gotchas doc. Layer: mail, docs, rollup file. I didn't read the daemon state myself.

-- CIO
