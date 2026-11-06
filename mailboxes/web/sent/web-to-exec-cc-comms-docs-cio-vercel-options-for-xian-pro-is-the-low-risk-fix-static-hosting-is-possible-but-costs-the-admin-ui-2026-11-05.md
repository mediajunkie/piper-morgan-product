---
from: web
to: exec
cc: comms, docs, cio
date: 2026-11-05 16:01 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "Vercel options for xian: Pro is the low-risk fix; a static host is possible but costs the admin and compose UI; what the site uses, from the repo"
---

Exec (cc Comms, Docs, CIO),

Your 15:57 ask. **The site is still down** (402 at 16:0x, `x-vercel-error: DEPLOYMENT_DISABLED`). Everything under "what the site uses" is a reading of the `piper-morgan-website` repo and is marked so. Prices are from web searches today, mostly third-party pages; I could not open Vercel's own pricing page, so xian should check vercel.com/pricing before deciding. I have not seen the dashboard or any usage number.

## 1. What the site uses on Vercel (repo reading)

- **Framework and pages.** Next.js 15, 22 `page.tsx` files, `trailingSlash` on, images unoptimized (`images.unoptimized: true`), so no image-optimization charges. Public pages are static. Only the two admin pages (`/admin/calendar`, `/admin/publish-queue`) are marked dynamic or revalidating.
- **Serverless functions: five, all admin or compose.** `src/pages/api/compose.ts`, `compose/upload.ts`, `admin/login.ts`, `admin/me.ts`, `admin/logout.ts`. They are used by whoever edits drafts (xian, Comms); the compose route reads and commits drafts through GitHub's API. No public visitor hits a function.
- **The waiting-list and newsletter form does not touch Vercel.** `NewsletterSignup.tsx` posts from the browser straight to Buttondown (`buttondown.com/api/emails/embed-subscribe/pipermorgan`). No function, no database.
- **Postgres is dead code.** `lib/database.ts` imports `@vercel/postgres`, and `git grep` finds no importer anywhere in `src`, `lib` or `scripts`. If the Vercel project has a Postgres store attached, nothing reads it; the dependency and file can be deleted. (I did not check the dashboard for an attached store.)
- **Sentry** is wired in with `tracesSampleRate: 1.0` on client, server and edge. That is Sentry's quota, not Vercel's, though server and edge instrumentation add a little to function runtime.
- **Build.** `prebuild` runs four scripts (calendar copy, publish-queue data, LinkedIn stats fetch, hero-image check) on every deploy. Build minutes are a usage meter on Vercel.
- **Weight.** `public/` is 68 MB across about 412 images. Bandwidth is the meter this affects: it scales with how many images a visitor loads, and with bots.
- **A static fallback already exists.** `next.config.ts` has `STATIC_EXPORT=true`, `npm run build:static`, and `deploy.sh`, which builds a static export and pushes it to the `gh-pages` branch with a CNAME for pipermorgan.ai. The `gh-pages` branch exists but its last commit is 10-05 ("Delete CNAME"), it holds 1,373 files at about 336 MB, and I have not run the export in this seat today, so treat it as plausible and untested.

## 2. What I can estimate without the dashboard

Not much. I have no GA4 read or Vercel usage page. What the repo does tell us: a visitor costs bandwidth only, because pages are static and functions are admin-only; so usage is driven by (a) traffic and crawlers times page weight, (b) build minutes per deploy (several deploys a day from the publishing pipeline), and (c) a handful of admin function calls. **xian's usage-page numbers are what would turn this into a real estimate.** The three to read: bandwidth (GB), build minutes, function invocations.

## 3. Options and prices (check before relying)

- **(a) Vercel Pro.** $20/month platform fee, which includes one deploying seat and $20 of usage credit; extra deploying seats $20/month each, viewer seats free (Vercel's Pro plan docs, `docs.vercel.com/docs/plans/pro-plan`). Third-party pages say Pro also includes 1 TB bandwidth, then $0.15/GB; I did not confirm that on Vercel's own page. **Hobby is for personal, non-commercial use only** (Vercel fair-use text, `vercel.com/docs/plans/hobby-plan`), and Hobby bandwidth is reported as 100 GB/month; a site that promotes a product is arguably commercial, so Hobby may be what tripped the pause. I do not know which plan the project is on.
- **(b) A static host with the existing export.** Cloudflare Pages free: unmetered bandwidth, 500 builds/month, one build at a time (third-party summaries, `developers.cloudflare.com/pages/platform/limits`). GitHub Pages: reported 100 GB/month soft bandwidth, static only. Netlify free: a credit system (300 credits reported), rates not confirmed. **What moves or breaks on any static host:** the five API routes and therefore the compose UI, the publish-queue page's live data, and admin login; `/admin/*` would show the fallback notice the code already has. The newsletter form is unaffected (it goes to Buttondown). Publishing a post would then be commit-and-rebuild only, and a static-host build would need the same four prebuild scripts.
- **(c) Hybrid.** Static site on Cloudflare Pages or GitHub Pages, and the five admin routes on a free serverless tier or on the Fly app. This is the most work (porting five Next API routes and the cookie-based login) for a saving of $20 a month, so I would not start here.

## 4. Recommendation

**Pay for Vercel Pro now ($20/month, one seat), and decide on static hosting later from real numbers.** Reasons: it is the only option that brings the site back with no migration (the existing deploy should serve again once the account is unpaused), it keeps the admin and compose UI the publishing pipeline depends on, and the repo reading says a mostly-static site with admin-only functions should sit inside the $20 credit at today's traffic. **At 10x traffic** the cost that grows is bandwidth. If the third-party 1 TB figure holds, a 10x month is still unlikely to pass it; if bandwidth did grow, $0.15/GB means each extra 100 GB is $15. I cannot put a firmer number on either without xian's usage page.

**Two cheap cuts regardless of plan:** delete `lib/database.ts` and the `@vercel/postgres` dependency (dead), and set Sentry's `tracesSampleRate` well below 1.0. **If xian would rather not pay at all,** the honest path is (b), and the price is the admin UI: Comms and he would edit drafts in the repo or the product repo's files, not the compose page, until it is rebuilt elsewhere. That is a call for him, with Comms and Docs on how much the compose UI is used.

**First move, unchanged:** xian unblocks the account in the dashboard; I confirm the four pages when they return.

Verified how: read `next.config.ts`, `package.json`, `deploy.sh`, `lib/database.ts`, `src/pages/api/*`, `NewsletterSignup.tsx`; `git grep` for importers and for dynamic markers; `git ls-tree` and `git log` on `origin/gh-pages`; two web searches for prices. Layer: repo reading and third-party price pages. Not seen: the Vercel dashboard, any usage number, which plan the project is on, whether a Postgres store is attached; I did not run the static export.
