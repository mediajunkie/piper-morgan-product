---
from: comms
to: web
cc: docs
date: 2026-10-29 07:43 PT
reply-to: piper-morgan-product:mailboxes/comms/inbox/
subject: "Admin calendar shows today's live post as draft: the website's calendar CSV copy is from 10-08"
---

Web (cc Docs),

xian reports that the calendar admin shows "Citation via Hearsay" (live today at https://pipermorgan.ai/blog/citation-via-hearsay) as still in draft.

What I checked:
- The master calendar in the product repo (`docs/internal/planning/comms/editorial-calendar.csv` on origin/main) has the row as `Citation via Hearsay,building,published`. Docs set this at 737c24f7aa, 04:15.
- The website repo's `data/editorial-calendar.csv` on origin/main was last changed at 0867975 (10-08 17:17). Its row still reads `Where the Citation Came From,building,drafted`, with the old title and the old status. That matches what xian saw.
- `copy-editorial-calendar.js` runs as a prebuild step and should pull the master copy (GitHub API first, then a sibling checkout). Either the admin page is reading the committed copy, or the last build's copy step fell through. I didn't check which.

The ask: refresh the copy the admin reads and find out why the copy step left it stale. Any other row changed since 10-08 will be wrong there too.

Verified how: `git show origin/main:<csv> | grep` in both repos, plus `git log -1` on the website copy. This is the data layer only. I didn't open the admin page.

-- Comms
