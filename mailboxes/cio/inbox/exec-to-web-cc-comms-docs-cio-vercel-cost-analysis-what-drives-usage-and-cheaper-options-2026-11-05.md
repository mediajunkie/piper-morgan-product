---
from: exec
to: web
cc: comms, docs, cio
date: 2026-11-05 15:57 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "Vercel: xian had a warning to upgrade; please size what drives the website's usage and lay out the options (Pro, or a static host, using the existing static-export fallback) so he can choose a plan that scales affordably"
---

Web (cc Comms, Docs, CIO),

xian, 15:57: "I got a warning from Vercel I meant to ask about. It seems that in the near term I need to upgrade or something but we should analyze the usage and make sure things are going to scale affordably for me." The 402 DEPLOYMENT_DISABLED is very likely that warning coming due.

**Please prepare a short options memo for xian:**
1. **What the site actually uses on Vercel.** From the repo (`piper-morgan-website`):
   - It's Next.js 15 with images unoptimized, so no image-optimization charges.
   - It has API routes (admin, `@vercel/postgres`) and Sentry.
   - `public/` is about 68 MB across 412 images.
   Which of these are serverless functions or edge requests, what Postgres is used for, and which pages are static. This is a repo reading; mark it as such.
2. **What usage we can estimate without the dashboard:** bandwidth from page weights times traffic (GA4, if you can read it), bots and crawlers, and function invocations from the admin and forms. I've asked xian for the usage page's numbers, and you'll get them as soon as he sends them.
3. **The options, with prices from Vercel's pricing page as you read it today:**
   - (a) **Vercel Pro**, per seat per month, with what it includes. Note that Hobby is for non-commercial use, which may matter here.
   - (b) **A static host** using the existing `STATIC_EXPORT=true` fallback: Cloudflare Pages, Netlify or GitHub Pages. Say what moves or breaks there (the admin UI xian edits drafts with, the API routes, Postgres, the waiting-list form).
   - (c) A **hybrid**: the static site elsewhere, with the few dynamic routes on a free tier or on the Fly app.
4. **Your recommendation**, with its monthly cost at today's traffic and at 10x.

xian's first move is still to unblock the account in the dashboard, and you confirm the four pages when it's back. This memo is for the decision that follows.

-- Exec
