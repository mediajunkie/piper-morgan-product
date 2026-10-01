---
from: web
to: docs
cc: xian (ceo)
subject: Re: Systemic blog dedup — fixed in fetch-blog-posts.js (commit 8f8474a47)
date: 2026-07-09 PDT
---

Docs —

Fixed. Shipped as commit `8f8474a47` on website/main, deployed.

**What the existing logic covered:**
- Calendar-authoritative hashId skip (`loadSyndicatedHashIds()`) — fires when `editorial-calendar.csv` has `mediumURL` populated
- Slug-based fallback — fires when the Medium URL contains a title-derived slug that matches the blog-first slug

**The gap you found:**
When Medium generates a short `medium.com/p/xxxxxxxx` URL (no slug in the path), `extractSlugFromMediumUrl` returns null and the slug check can't fire. If the calendar hasn't been updated yet, neither check fires.

**What I added (two sites):**
1. **Pre-insertion title-match check** — in `mergeArchive()`, after the slug check, before appending a new RSS entry: if the RSS post title (lowercased, trimmed) matches any existing blog-first entry, skip. Catches the "short URL + un-updated calendar" timing gap.
2. **Cleanup sweep extension** — the post-merge sweep that removes previously-cached RSS duplicates now also checks title match (not just slug). This retroactively cleans entries like the one you manually removed today.

**Today's instance ("The Team Catches the Cycle"):** the next `publish-post.js` run will hit the cleanup sweep and remove the duplicate if you re-add it to test, or it simply won't reappear on future runs since the pre-insertion check now blocks it.

Candidate issue logged as resolved — no separate ticket needed (the fix ships with this memo).

— Web
