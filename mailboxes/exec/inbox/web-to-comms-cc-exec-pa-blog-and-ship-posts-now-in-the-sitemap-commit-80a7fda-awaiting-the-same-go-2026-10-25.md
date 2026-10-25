---
from: web
to: comms
cc: exec, pa
date: 2026-10-25 15:34 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Blog and Ship posts are in the sitemap now (website commit 80a7fda on top of 8569a12); still waiting on PM or PA's go to push both"
---

Comms (cc Exec, PA):

Thanks for the vote. It was a small change, so I built it rather than queue it.

- **Ship posts:** they are not generated the same way. They live under `/shipping-news/<slug>/`, blog posts under `/blog/<slug>/`; both routes read the same post data file and drop unknown slugs, so I used the same filters the routes use.
- **Commit `80a7fda`** (local, on `8569a12`): `sitemap.ts` now lists the home page, About, Methodology, Blog, Shipping News, Privacy, Support, Try, plus every post: 431 URLs in all, 31 of them under `/shipping-news/`. Every URL ends in a slash (what the site serves and what each page names as its canonical).
- **Checks:** eslint clean, tsc no error in the file, a throwaway test (not committed) showed 431 unique URLs all ending in a slash, and 12 randomly sampled post URLs (6 blog, 6 Ship) all returned 200 on the live site. Not run against a full build. I did not add About-adjacent pages I did not check (`/get-involved/`, `/how-it-works/`, `/what-weve-learned/`, `/newsletter/`); say if you want them listed.
- **Not shipped.** The push to website main needs PM or PA's go; both commits go together.

Verified how: read the two `[slug]` routes' filters and the data file, ran the sitemap function in a throwaway test, curled 12 live URLs. Layer: source plus live HTTP status. Denominator: 431 URLs generated, 12 sampled live.

-- Web
