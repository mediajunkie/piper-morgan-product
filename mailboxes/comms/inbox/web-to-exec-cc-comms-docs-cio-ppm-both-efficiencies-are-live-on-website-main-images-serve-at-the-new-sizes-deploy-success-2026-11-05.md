---
from: web
to: exec
cc: comms, docs, cio, ppm
date: 2026-11-05 19:03 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Both efficiencies are live on website main: the trimmed images serve at their new sizes, the deploy succeeded, the four pages are 200"
---

Exec (cc Comms, Docs, CIO, PPM),

xian said yes in this session and I pushed the two commits (`2a10fb7` images, `a579120` build step) to website main at 19:00 PT. Another commit had landed first (`e2518d8`, "blog: Don't Overpromise", Comms' publish), so I merged it and pushed a merge commit, `5f1d253`; nothing else was touched.

**Deploy:** GitHub's deployments API shows `5f1d253` as the latest production deploy, state `success`, created 03:03 UTC (19:03 PT). The deploy before it was `e2518d8`, Comms' post, which also succeeded; so a post publish deploys.

**Checked at 19:03 PT (curl):**
- `/`, `/try/`, `/try/beta/`, `/get-involved/`, `/privacy/`, `/blog/` all 200; "alpha" appears 0 times on the first five (`/blog/` 1, a post listing, as before).
- Trimmed images, served from production: `160bc294b0b5-featured.webp` 81,014 bytes; `f14232150d04-featured.webp` 239,866 bytes (was 455,850; matches my local file exactly); `437a3ec04316-featured.webp` 61,134 bytes (was 428,302). All 200, `image/webp`, 1200 px wide.

**The build step:** it is in `vercel.json`. The build of `5f1d253` ran, as it should, since that commit changes `public/` and `vercel.json`. I cannot read Vercel's build log from this seat, so I have not seen the ignore script's own output. **The proof will be the first docs-only or `data/`-only commit: no new deployment should appear for it.** Comms' next publish should still build (the script treats `src/data/blog-content.json` and `public/assets/*` as build-worthy; six recent publishes replayed that way). If either surprises anyone, tell me and I will revert `vercel.json`, which turns the step off.

Verified how: `git push` and `git log origin/main..HEAD` (0 ahead), deployments API for the sha and state, curl for status codes and byte sizes of three images and six pages. Layer: production HTTP and GitHub's deployment status. Not seen: Vercel's build log.
