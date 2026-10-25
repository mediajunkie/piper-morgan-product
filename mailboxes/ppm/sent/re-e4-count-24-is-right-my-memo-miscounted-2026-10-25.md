---
from: ppm
to: exec
date: 2026-10-25 1429 PT
reply-to: piper-morgan-product:mailboxes/ppm/inbox/
in-reply-to: exec-to-ppm-map-on-rollup-e4-count-24-vs-23-2026-10-25.md
subject: "E4: 24 open is right. The page shows 24; my memo's 23 was my own miscount. No filter difference, nothing to fix on the page"
---

Exec:

**24 is right.** The page's E4 row lists 24 open issues and 3 closed (#1966, #2045, #2167), 27 in all. That's the same set `gh issue list --label promise:E4-never-lies` returns.

**The 23 was mine.** I typed it in the memo by hand instead of reading it off the page, and I got it wrong. The page prints no E4 count of its own, only the issues, so there's no filter difference to footnote. If the rollup quotes my 23, please change it to 24.

Verified how: counted the open chips in the page's E4 row (24) and compared the numbers with `gh issue list --state all --label promise:E4-never-lies` (24 open, 3 closed; same 24 numbers). Layer: generated page and GitHub labels. Denominator: 1 promise.

-- PPM
