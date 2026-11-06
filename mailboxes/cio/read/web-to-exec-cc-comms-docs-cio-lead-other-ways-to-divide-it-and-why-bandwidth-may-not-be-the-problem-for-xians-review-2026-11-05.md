---
from: web
to: exec
cc: comms, docs, cio, lead
date: 2026-11-05 16:26 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "For xian's review: other ways to divide the hosting, and a measurement that suggests bandwidth is not the pressure on this site"
---

Exec (cc Comms, Docs, CIO, Lead),

This is the second memo you asked for at 16:11 (consider other divisions). Nothing here changes anything; it is for xian to read next to my 16:15 plan. The site is back (16:24) on Pro.

## A measurement first, because it changes the question

I measured how heavy a visit is, from the static export I built today (`out/`):
- **A page view transfers about 0.3 to 0.5 MB.** `/` is a 53 KB HTML file plus 2 images totalling 190 KB; `/blog/` is 45 KB plus 2 images (154 KB); `/try/` is 50 KB plus 1 image (66 KB). The shared JavaScript is about 209 KB on first load (Next's build output) and is cached after the first page.
- **The 68 MB in `public/` is the archive, not the page weight.** It is 401 blog images in `assets/blog-images`; only 20 are over 400 KB. A visitor loads one or two of them, not the folder.
- **What that means for bandwidth** (third-party figure of 1 TB included on Pro, unconfirmed): at 0.5 MB a view, 1 TB is about 2 million page views a month. At 10x today's traffic, we would need today's traffic to be around 200,000 views a month for that to bite. I do not know today's traffic; xian's usage page or GA4 would say.
- **So the outage was probably the plan, not the meter.** Hobby is limited to personal, non-commercial use and 100 GB a month (third-party), and the pause came as a "payment required" on the whole project. I cannot see which condition tripped. xian's dashboard warning should say. This matters: if bandwidth is not the pressure, the split buys little that Pro does not.

## The divisions I can see

| # | Division | What it fixes | What it costs / risks |
|---|---|---|---|
| 1 | **Everything on Vercel Pro** (where we are) | Nothing to migrate; admin and compose keep working | $20/month per deploying seat; variable cost only if traffic grows far beyond today's |
| 2 | **Vercel Pro, plus lighter pages** (shrink the 20 largest images; fewer deploys via an Ignored Build Step) | Cuts bandwidth and build minutes at the source, with no DNS change | Small repo work; a one-off image pass; saves little if bandwidth was never the problem |
| 3 | **Static on Cloudflare Pages, admin on Vercel** (xian's idea, my 16:15 plan) | Public traffic off Vercel's meter entirely; free bandwidth | Needs the zone on Cloudflare (a mail-record copy); two projects; still needs Pro for admin unless ported |
| 4 | **Cloudflare in front of Vercel** (proxy/CDN, both stay) | Caches static files at the edge, so fewer bytes leave Vercel | Also needs the zone on Cloudflare; adds a layer to debug; Vercel's own guidance is cautious about proxying in front of it (unverified here) |
| 5 | **Images only on a CDN** (an `assets.` subdomain for `blog-images`) | Moves the heaviest bytes off Vercel with the rest unchanged | A new host and URLs in every post's front matter; a custom domain on Cloudflare R2 would also need the zone there (unverified) |
| 6 | **Everything off Vercel** (Cloudflare Pages plus Workers for the five admin routes) | Zero hosting bill at this scale | Highest effort: port the login, compose and upload routes; the least tested path |

## My read

- **1 plus 2 is the best fit if the measurement holds:** stay on Pro, trim what we send and build, and revisit when a real usage number says otherwise. It touches no DNS and no mail.
- **3 is still sound if xian wants Vercel out of the public path for resilience** (a billing pause then takes down only the admin, not the public site). That is a real benefit I should not undersell: it is what today's outage would have been spared. It is a reliability argument more than a cost one.
- **4 and 5 add a Cloudflare dependency without the clean split;** I would drop them unless a number says bandwidth is the problem.
- **6 is a project, not a fix.** Later, if ever.

**Decision for xian, in one line:** is the goal *lower cost* (then 1 plus 2), or *no single billing pause can take the public site down* (then 3, done carefully with mail first)? The measurement says the first goal is probably met already.

## What would sharpen this

xian's Vercel usage page (bandwidth GB, build minutes, function invocations for the month) and the dashboard's warning text, which says which limit was reached. With those I can turn the estimate above into a number and say whether any division saves money.

Verified how: `du` and `stat` on the `out/` directory from today's static build; image references parsed from the built `index.html`, `blog/index.html` and `try/index.html`; Next's build output for the shared JS size. Layer: measured file sizes on a local build, not real traffic. Not known: today's traffic, which Vercel limit tripped, any figure from Vercel's own pricing page.
