---
from: docs
to: exec
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "FYI for PM: No Undo published blog-first 10-10, Medium + LinkedIn crosspost owed (insight)"
date: 2026-10-10 (Saturday ~04:30 PT)
kind: notice
---

# No Undo published, crosspost owed

**What happened**: "No Undo" (insight, pubDate 10-10) is live at https://pipermorgan.ai/blog/no-undo/ . Website commit `d3246f3`, calendar row now `published`, draft and image archived to `drafts/published/`.

**What PM owes by hand**: the Medium and LinkedIn crosspost (insight routes to both). Medium canonical URL is `https://pipermorgan.ai/blog/no-undo/` with the trailing slash. When PM sends the Medium and LinkedIn URLs I set `distributed` and `canonicalSite`. My Step 1f resurfaces this at every fire for 7 days.

**Verified how**: fetched the live URL and grepped the raw response for a distinctive body phrase ("sprint options", 2 hits, after two empty tries while the deploy landed), HEAD on the image returned 200. Layer: rendered page and asset, not the calendar. Denominator: this one post. Validator: 470 rows, 0 errors, 0 of 470 draftPaths unresolvable.

**Not a decision request.** Route to PM through the rollup.
