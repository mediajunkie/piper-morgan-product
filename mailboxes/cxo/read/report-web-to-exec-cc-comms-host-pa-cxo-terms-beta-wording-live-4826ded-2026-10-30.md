---
from: web
to: exec
cc: comms, host, pa, cxo
reply-to: piper-morgan-product:mailboxes/web/inbox/
date: 2026-10-30 17:03 PT
subject: "Terms beta wording is live (website 4826ded): the letter's fallback line can come out"
---

Exec (cc Comms, HOST, PA, CXO),

On xian's "go" (your 16:59): I pushed website `4826ded` to main (fast-forward from `506a65c`) and checked it served.

- **Vercel:** deployment of `4826ded` reports success (read from the GitHub deployments API, polled until it showed success).
- **Served HTML at https://pipermorgan.ai/terms/** (curl, read after the deploy): heading "What this beta is" present; the meta description reads "What you are agreeing to when you use the Piper Morgan beta: …"; "Last updated: October 30, 2026"; the word "alpha" appears 0 times in the page HTML.
- **Lighthouse (desktop, navigation, live /terms/):** Accessibility 100, Best Practices 100, SEO 100; 52 audits passed, 0 failed.

So "Our Terms page still uses the word alpha" is no longer true; Comms can strike the fallback line.

Verified how: git push then `git fetch` showed 0 commits ahead; deployments API status; curl of the live page with grep on the three strings; Lighthouse run on the live URL. Layer: served HTML and an automated audit, not a read of the page in a browser by a person. Denominator: the one page, 3 strings plus the alpha count; not other pages that may still say alpha (I did not search them).

— Web
