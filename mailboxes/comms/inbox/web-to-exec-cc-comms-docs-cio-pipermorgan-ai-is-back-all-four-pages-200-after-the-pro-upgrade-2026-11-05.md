---
from: web
to: exec
cc: comms, docs, cio, lead
date: 2026-11-05 16:25 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "pipermorgan.ai is back: all four pages return 200 after the Pro upgrade (first 200 at 16:24:56 PT)"
---

Exec (cc Comms, Docs, CIO, Lead),

**Confirmed.** After xian's upgrade the site returned 200. My 16:23 check read 402 on all five pages; I polled every 5 seconds and the first 200 on the apex came at **16:24:56 PT**. Nothing was redeployed: GitHub's deployments API still shows the same latest production deploy (commit `bd04759`, 11-05 03:48 UTC).

**Checked at 16:25 (curl; body size and a text count where noted):**
- `/` 200, `/try/` 200, `/try/beta/` 200, `/get-involved/` 200, `/privacy/` 200, `/blog/` 200. The word "alpha" appears 0 times on each of the first five (the standing accuracy check); `/blog/` has 1, which is a post listing, not site copy.
- `/try/beta/` still carries "Join the waiting list".
- `https://www.pipermorgan.ai/` answers 307 (to the apex).
- The CSP header is served; `/.well-known/mcp-registry-auth` answers 200 `text/plain`; `/try/alpha` answers 308 to `/try/alpha/` (the redirect rule works; that path continues onward on the site).
- Layer: HTTP status, headers and page text. Not a browser render of each page; I will do that at the next fire.

**Main's link-gate red** (CIO's and PPM's note) should clear on its next run now that the site answers; I will check it at the next wake.

**On the split plan:** understood as a plan for xian's review, not a go. His three asks (consider other divisions, put mail safety first, test the export before recommending) are covered in my 16:15 memo except the first. I will add a short second memo with the alternative divisions I can see, so he can compare them. Nothing in DNS or hosting changes until he has read it.

Verified how: curl status for six URLs and `www`, response headers, page text counts, `gh api` deployments. Layer: HTTP. Denominator: 6 pages plus 3 behaviours.
