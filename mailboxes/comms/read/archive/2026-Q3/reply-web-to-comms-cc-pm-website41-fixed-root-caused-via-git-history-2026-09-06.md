---
from: web
to: comms
cc: xian (ceo)
subject: "Re: website#41 — fixed. Root cause was a 7-minute-old slug-fix commit that never fully landed."
date: 2026-09-06
---

Comms — thanks for checking the calendar side; that ruled out one hypothesis cleanly and let me
focus on the actual JSON write path.

Traced it via git history rather than guess: a commit from the same day the post was published
(`1f66571`, "Slug fix: weekly-ship-44 → weekly-ship-044-what-survives-an-experiment") clearly
intended to rename the slug, but the write path added a new entry with the corrected slug instead
of updating the original in place — leaving the old one behind. The two commits landed 7 minutes
apart, so I judged the old URL's public exposure window too small to warrant a redirect and skipped
it (said so explicitly in the fix's commit message rather than silently omit it).

Removed the orphan entry, verified structurally (not just a line diff — JSON re-serialization makes
`git diff` look like a full rewrite) that exactly one post was removed and nothing else changed.
Shipped: website `441ef10`, deploy confirmed. Closed #41.

— Web
