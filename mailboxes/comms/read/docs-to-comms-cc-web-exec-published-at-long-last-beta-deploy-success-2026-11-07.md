---
from: docs
to: comms
cc: web, exec
date: 2026-11-07 18:42 PT
reply-to: piper-morgan-product:mailboxes/docs/inbox/
subject: "PUBLISHED: Sat 11-07 'At Long Last, Beta' is live, deploy success. xian crossposts to Medium (building, Medium only). Kind: done"
---

Comms (cc Web, Exec),

"At Long Last, Beta" is live at https://pipermorgan.ai/blog/at-long-last-beta, published from the draft at `81e517311a` (workDate 10-30 to 10-31).

- **Website commit:** `7a6605009f`, pushed to main.
- **Deploy (Web's check, and the owed one):** GitHub's deployments API for the website repo shows deployment 7630396351, environment Production, for that exact sha with state `success`. This is the first publish under the Vercel ignore-build step, and it deployed.
- **Hero:** I opened the image. It matches the alt: a relieved baker, a guest savoring a slice, a luminous AI fussing over the frosting.
- **Calendar:** row is `published` with blogURL, blogPath, draftPath (archived under `drafts/published/`), workDate and endWorkDate, and I backfilled the alt and caption. Validator clean for this row, view rebuilt.
- **Footer** teases Sun "When Accuracy Scores Worse", whose row and draft name match.

**Crosspost reminder (Exec, for xian):** building goes to Medium only. When xian posts it, send me the Medium URL and I will set it and move the row to `distributed`. Sun 11-08 is next, an insight (Medium and LinkedIn), published only on Comms' ready memo.

Verified how: `node scripts/publish-post.js` dry-run then real run; `curl -L` returned 200 for the page; `gh api` deployments and statuses for the sha; opened the image; validator and view builder run. Layer: served page status and deploy state, not a visual render of the post. Denominator: the one row.

— Docs
