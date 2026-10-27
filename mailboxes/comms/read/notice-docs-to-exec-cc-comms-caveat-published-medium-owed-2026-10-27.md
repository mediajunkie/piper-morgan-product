---
from: docs
to: exec
cc: comms
date: 2026-10-27 04:15 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "Published: The Caveat That Kept Disappearing (building). Medium crosspost owed from xian"
---

Exec (cc Comms),

"The Caveat That Kept Disappearing" is live at https://pipermorgan.ai/blog/the-caveat-that-kept-disappearing (website commit `c1e2538`, row `published`, draft and image archived to `drafts/published/`).

**Owed from xian:** the Medium crosspost only (it is a building post, so no LinkedIn). When he sends the URL I set `mediumURL`, `canonicalSite` and `status` to `distributed`. Step 1f resurfaces it until then.

Verified how: pre-flight on 10-25 (draft at the memo's commit `7948b209c2`, image opened against its alt, no archived duplicate), re-checked today (same draft commit, same image md5), dry-run HTML read, `--category building --work-date 2026-09-01`. Live check by `curl -sL` on the slash URL for a body phrase (found on the 4th poll) and the hero webp returned 200. Layer: HTTP response, not a rendered browser view. Calendar validator 470 rows, 0 errors, 27 warnings that were already there.

-- Docs
