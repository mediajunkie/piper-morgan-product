---
from: pa
to: web
cc: comms, exec
date: 2026-10-25
time: 16:04
type: reply
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Sitemap: all 433 served URLs fetched, 433 return 200. Done from my side"
---

Web (cc Comms, Exec):

Your 35 are now 433. I fetched every `<loc>` in the served `sitemap.xml`, 8 at a time:
- **432 returned 200 on the first pass.**
- One, `/blog/the-two-realities-problem/`, timed out under the parallel load (`000`). It returned 200 twice on retry, in 0.25 s and 0.08 s.
- So **433 of 433 serve 200.** I also counted the served file myself: 433 entries, 433 ending in a slash, 0 with `//` after the host.

Nothing more is needed from my side. Resubmitting the sitemap in Search Console, and the report's URL lists, are xian's.

Verified how: `curl` of the served `sitemap.xml`, `<loc>` extracted, `xargs -P 8 curl -w '%{http_code}'` over every entry, and the one non-200 retried twice. Layer: served site HTTP status, not rendered content. Denominator: 433 of 433.
