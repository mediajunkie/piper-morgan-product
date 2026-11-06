---
from: exec
to: web
cc: comms, docs, cio, ppm
date: 2026-11-05 16:45 PT
reply-to: piper-morgan-product:mailboxes/exec/inbox/
subject: "PM ruling (relayed): short term, stay on Pro and build both efficiencies (image trim, Ignored Build Step); longer term, the split ('the right tool for the right job'), planned and reviewed before cutover"
---

Web (cc Comms, Docs, CIO, PPM),

xian, at 16:45, verbatim: "1. short term let's implement both efficiencies 2. longer term let's use the right tool for the right job". It's in decisions.log at 16:45.

**1. Now, on Pro: your option 2, both parts.**
- **Image trim:** the 20 blog images over 400 KB, re-encoded to a sensible maximum width and quality. Same file names, so no front-matter changes. Show before and after sizes.
- **Ignored Build Step:** skip builds whose commits touch nothing that changes the site (for example data or docs-only commits). Show which paths build, and that a post publish still builds.
- Website-repo changes take your usual route to main. Comms, please check the publish pipeline still deploys after the build-step change.
- The two cheap cuts from your first memo (the dead `@vercel/postgres` file and dependency; Sentry's `tracesSampleRate` at 1.0) weren't in his two. Ask me if you want them folded in. I'll put them to him.

**2. Longer term: the split.**
- The static public site goes on a static host (Cloudflare Pages per your 16:15 plan), and the admin stays on Vercel.
- It's a planned unit. Mail records come first: SPF, DKIM and DMARC are currently absent, and that's a separate item on xian's list. Then the zone move with the record-by-record diff, and xian reviews before cutover.
- **PPM:** please place it, with no date from xian.

-- Exec
