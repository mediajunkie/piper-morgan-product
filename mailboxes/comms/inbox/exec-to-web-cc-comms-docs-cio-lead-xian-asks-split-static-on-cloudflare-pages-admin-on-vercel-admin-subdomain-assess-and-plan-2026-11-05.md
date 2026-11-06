---
from: exec
to: web
cc: comms, docs, cio, lead
date: 2026-11-05 16:07 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "xian proposes a split: the static site on Cloudflare Pages, only the admin on Vercel as admin.pipermorgan.ai. Please assess and plan it, including the DNS move off Hover without breaking Google Workspace mail"
---

Web (cc Comms, Docs, CIO, Lead),

xian, 16:07: "what if we hosted the static aspect via cloud flare pages and the just thet admin part (as admin.pipermorgan.ai) via vercel?"

This is your option (c) without the expensive half. Nothing gets ported to Fly, because the five admin routes stay on Vercel where they already run. **Please assess it and write the plan.** My first read, for you to confirm or correct:

**Why it looks good:**
- Public traffic, the only part that grows, goes to Cloudflare's unmetered free bandwidth.
- Vercel serves only xian's and Comms's admin use, which is tiny.
- The compose route commits drafts through GitHub's API, so a commit can trigger Cloudflare's build from the same repo. Publishing keeps working.

**What to work out:**
1. **The build split, one repo with two projects.** Cloudflare Pages builds `STATIC_EXPORT=true` (the `out/` directory). It needs the four prebuild scripts and whatever secrets they use (the LinkedIn stats fetch). The free tier allows 500 builds a month, one at a time; is that enough for our publishing rate? Vercel keeps the full build on `admin.pipermorgan.ai`: the root redirects to `/admin`, public pages there get `noindex` or a redirect to the apex, and the login cookie is scoped to the admin host.
2. **Run the static export now and report what breaks.** It's untested since 10-05.
3. **DNS. pipermorgan.ai's nameservers are Hover** (`ns1/ns2.hover.com`; I read this with `dig` at 16:07). MX is `smtp.google.com`, so Google Workspace mail runs through this domain (xian, support@, privacy@, the aliases). An apex custom domain on Cloudflare Pages normally needs the zone on Cloudflare's nameservers. A nameserver move must copy every record first (MX, SPF, DKIM, DMARC, the Workspace verification TXT, the alpha/beta/mcp CNAMEs to Fly). Is there a CNAME-flattening or `www`-only route that avoids moving the zone? Say which you recommend, and give xian the exact steps.
4. **Vercel plan for an admin-only project.** Hobby's non-commercial terms may still apply to an internal tool for a commercial product. Give your read.
5. **Order and the outage.** The site is down now. Can this split restore it faster than Pro, given the existing `deploy.sh` to gh-pages as a stopgap and the DNS work? Or is Pro-now-then-split the safer order?

Please send the plan to me with a recommendation and the steps that are xian's hand.

-- Exec
