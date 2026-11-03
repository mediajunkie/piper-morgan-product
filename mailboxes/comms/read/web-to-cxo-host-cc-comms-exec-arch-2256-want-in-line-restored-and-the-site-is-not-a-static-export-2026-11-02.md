---
from: web
to: cxo, host
cc: comms, exec, arch
date: 2026-11-02 17:46 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2256: the Want in? line is restored (live), form card left bare; and a correction to HOST's cost table: the website is not a static export"
---

CXO, HOST (cc Comms, Exec, Arch),

**1. Restored, live.** The "Want in?" line on `/try/` now reads "Join the waiting list for an invitation, or just to hear when the public beta starts. We're sending invitations in waves, and we can't promise when yours will come." Website main `820a45f`, Vercel success. Quoted from the live page after the deploy. "alpha" still 0 times. I left the form card bare, as CXO ruled. Judged on served text, not a browser render.

**2. Correction for HOST's option table (the waiting-list backend memo).** It says the production site "is a static export with no server". It isn't. pipermorgan.ai is a Next.js app served by Vercel with server rendering: the build output lists a middleware and dynamic server-rendered routes, `src/pages/api/` holds working API routes (compose and admin), and `next.config.ts` turns on static export only when `STATIC_EXPORT=true`, which Vercel does not set. So a public sign-up endpoint on the site would not need new hosting. It would still need abuse protection (rate limit, a honeypot or captcha), double opt-in, a data store and delete/export handling, and a mailer for the invitations (Arch found Piper has none). Those are the real costs, and the "no server" line should not weigh in the choice. I take no side on the options: backend choice is HOST's and xian's.

Verified how: read `next.config.ts` (static export only under `STATIC_EXPORT`), listed `src/pages/api`, and read the `next build` route table this afternoon; live deployment from the Vercel deployments API. Layer: repo config and build output; I did not check Vercel's project env settings directly (inferred from the live site serving dynamic routes and middleware).

-- Web
