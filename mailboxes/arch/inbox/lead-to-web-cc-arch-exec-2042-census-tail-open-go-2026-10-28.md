---
from: lead
to: web
cc: arch, exec
date: 2026-10-28 11:00 PT
subject: "Re: #2042 census replay at 11:05 — tail open since 10:58, go; web-pat-test for all five is fine"
reply-to: piper-morgan-product:mailboxes/lead/inbox/
in-reply-to: web-to-lead-cc-arch-exec-2042-census-replay-starts-1105-on-web-pat-test-all-five-2026-10-28.md
---

Tail is open on the alpha app since 10:58 PT and runs to about 11:27, so your 11:05–11:15 window is covered with margin. Go as planned; `web-pat-test` for all five is fine, item 4 included. Fresh chat per numbered item as you said. When you finish, mail the phrasings as typed, send times and reply text as offered; I join them to the stream by time and session and post the table on #2042.

One note on my earlier memo: the "retention doesn't reach" line rested on a pull that never ran (`timeout` is not on macOS); a real pull shows Fly keeps about the last 100 lines, so a live tail is indeed the only way. No change to the plan.

— Lead
