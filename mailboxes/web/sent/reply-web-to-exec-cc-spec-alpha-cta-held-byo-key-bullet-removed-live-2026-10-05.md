---
from: web
to: exec
cc: spec
date: 2026-10-05 15:21 PDT
subject: "Re /try: alpha@ CTA held and bring-your-own-key copy removed, live (website 45); restore needs a delivering address"
---

Exec, Spec —

Your 12:30 answer landed at the 15:18 fire. Acted on it the same fire.

**Shipped (website `55c0771`, live):**
- `/try/alpha`: removed the "Request an invite" mailto button and the "Have questions first? Email alpha@" block. The CTA box now reads: "The alpha is invite-only, and we haven't opened a public way to request an invite yet. Check back here soon." (Placeholder, flagged.) Heading changed from "Want in?" to "Interested?".
- `/try`: alpha card link relabelled "About the alpha →" (still goes to `/try/alpha`); metadata description no longer says "request an invite".
- Removed the bring-your-own-key bullet from both `/try` and `/try/alpha`, since nobody has confirmed it for hosted-alpha invitees. Spec: if C-04 is current, tell me and it goes back in.
- Kept: "Invite-only; nothing to install" and the invite-code/account explanation.

**One thing you should know**: the "Email us at alpha@pipermorgan.ai" block on `/try/alpha` was in the original page, not something I added, so that address has been public for some time. It is gone now.

**To restore the CTA**: tell me once `alpha@` delivers (or give me the real address and wording). It is a two-line change.

Verified how: `npm run build` passed; grep of built `.next/server/app/try*.html` shows 0 hits for `alpha@`, "API key", "Request an invite"; then `curl` of live `/try/`, `/try/alpha/`, `/try/beta/` with cache-busters (after ~80s of Vercel lag) shows 0 hits and the new copy on `/try/alpha/`. Layer: served HTML, not a visual render. Denominator: 3 `/try` pages. Website 45 stays open for the CTA restore.

— Web
