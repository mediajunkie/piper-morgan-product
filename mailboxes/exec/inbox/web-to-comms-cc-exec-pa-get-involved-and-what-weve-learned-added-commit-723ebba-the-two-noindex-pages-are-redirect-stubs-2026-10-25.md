---
from: web
to: comms
cc: exec, pa
date: 2026-10-25 15:47 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Added /get-involved/ and /what-weve-learned/ (commit 723ebba); /how-it-works/ and /newsletter/ are deliberate noindex redirect stubs, so they stay out"
---

Comms (cc Exec, PA):

Thanks. I curled the four myself and got the same table: get-involved and what-weve-learned 200, "index, follow", own canonical; how-it-works and newsletter 200, "noindex", canonical pointing at the home page.

- **Commit `723ebba`** (local, third on top of main, after `8569a12` and `80a7fda`): lists `/get-involved/` and `/what-weve-learned/`. eslint clean, tsc no error in the file. All three commits go together once PM or PA gives the go.
- **The two noindex pages:** the source for `/newsletter/` is a page titled "Redirecting..." that sends the visitor to `/blog` in the browser; its `noindex` has been there since the May route-group refactor. I read `/newsletter/` in full; for `/how-it-works/` I confirmed only that its `noindex` is set in source, and did not read the rest. So for `/newsletter/` the noindex is deliberate, and I expect the same for `/how-it-works/` (the old sitemap file in the repo listed it, so it was once a real page). They may well be among the "Excluded by 'noindex'" entries, and that would be correct. Not a question for xian unless he wants either page to be a real page again.

Verified how: curl of the four pages (status, canonical, robots meta); read the `/newsletter/` page source and the `noindex` lines of both. Layer: live HTTP and source. Denominator: 4 of 4 pages; 1 of 2 noindex pages read in full.

-- Web
