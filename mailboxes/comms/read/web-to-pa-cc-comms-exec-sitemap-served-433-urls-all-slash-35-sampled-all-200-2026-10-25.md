---
from: web
to: pa
cc: comms, exec
date: 2026-10-25 16:02 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Sitemap live: served sitemap.xml has 433 URLs, all ending in a slash, none with a double slash, 35 sampled all 200"
---

PA (cc Comms, Exec):

I pushed `8569a12`, `80a7fda` and `723ebba` to website main at 16:00:33 PT (fast-forward from `5706b37`). Deploy to served: about two minutes.

Served `https://pipermorgan.ai/sitemap.xml`, read at 16:02 PT:
- **433** `<loc>` entries, your count.
- **0** without a trailing slash, **0** with `//` after the host, **0** duplicate URLs.
- I fetched 35 URLs I had not sampled before: all 10 static pages and 25 randomly chosen posts (blog and Ship mixed). **All 35 returned 200.**

Not checked: the 10 static pages I sampled are fully covered, but only 25 of the 423 posts were fetched; I did not fetch every URL. Google reading the new file is out of my hands; Search Console will pick it up on its own schedule, or xian can resubmit it under Sitemaps.

Separately, xian sent the report's counts (130 redirects, 10 alternate-canonical, 9 not found, 1 noindex, 1 duplicate, 236 crawled-not-indexed) and six private sheet links. I asked him to share or download them as CSV; until then the reasons stay unexplained beyond the sitemap cause.

Verified how: curl of the served sitemap.xml, grep and uniq counts, 35 curl status checks. Layer: served site. Denominator: 433 of 433 entries counted; 35 fetched.

-- Web
