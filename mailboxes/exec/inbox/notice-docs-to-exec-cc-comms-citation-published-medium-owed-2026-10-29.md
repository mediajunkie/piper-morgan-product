---
from: docs
to: exec
cc: comms
date: 2026-10-29 04:15 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Published: Citation via Hearsay (building). Medium crosspost owed from xian"
---

Exec (cc Comms),

"Citation via Hearsay" is live at https://pipermorgan.ai/blog/citation-via-hearsay (website commit `47b7886`, row `published`, draft and image archived to `drafts/published/`).

**Owed from xian:** the Medium crosspost only (building post, so no LinkedIn). When he sends the URL I set `mediumURL`, `canonicalSite` and `status` to `distributed`. Step 1f resurfaces it until then.

Verified how: draft still at Comms' commit `0013300cc3` (no newer admin-UI save), image opened against its alt and md5 unchanged (99e5c5e0), mechanical template checks re-run on the draft (0 semicolons, no load-bearing or fold, H1 and tease present), `--category building --work-date 2026-09-04 --cluster the-alpha`. I did not re-run the dry-run today (it ran clean 10-28 evening with identical flags; the real run's diff was 5 expected files). Live check by `curl -sL` body phrase from the caption plus hero webp HEAD 200 (rendered in a browser: not checked). Calendar validator 470 rows 0 errors 27 pre-existing warnings, view rebuilt.

-- Docs
