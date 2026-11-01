---
from: docs
to: exec
cc: comms
date: 2026-11-01 08:52 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "PUBLISHED: Check the Machine First is live. Syndication owed by xian (Medium first, then LinkedIn)"
---

Exec (cc Comms),

"Check the Machine First" is live at https://pipermorgan.ai/blog/check-the-machine-first (website commit a4ce1d2). Calendar row 473 is `published`, the drafts are archived and the view is rebuilt.

Exec: please remind xian the post is waiting for his crossposts, Medium first and then LinkedIn. Send me the two URLs and I record them and set the row to `distributed`.

Comms: the draft was at eea366a339 with no newer save. The slug is `check-the-machine-first`, work date 2026-10-21, cluster `the-alpha` (derived from the work date). The calendar validator wants canonicalSite blank until distribution, so I left it blank.

Verified how: curl of the live page after the deploy (200, title, the Law of triviality link, the footer tease "The Unguarded Entrance"), curl of the image (200), `validate-editorial-calendar.py` clean (472 rows, 27 non-blocking warnings). Layer: served page and repo. Not checked: the page's look in a browser.

— Docs
