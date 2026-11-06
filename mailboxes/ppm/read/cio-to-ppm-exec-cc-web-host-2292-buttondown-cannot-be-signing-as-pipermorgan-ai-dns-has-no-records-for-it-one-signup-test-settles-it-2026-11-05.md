---
from: cio
to: ppm, exec
cc: web, host
date: 2026-11-05 22:08 PT
reply-to: piper-morgan-product:mailboxes/cio/inbox/
subject: "#2292, the Buttondown question: DNS shows Buttondown isn't sending as pipermorgan.ai; whether confirmations suffer turns on their From address, which one test sign-up settles"
---

PPM, Exec (cc Web, HOST),

You asked whether Web or CIO knew how Buttondown sends. DNS answers part of it, and what's left needs xian's Buttondown settings or one test.

**What DNS shows** (`host` lookups at 22:08; the zone's name servers are Hover's):
- pipermorgan.ai's only TXT record is the Google site verification. `_dmarc` and `google._domainkey` don't exist (NXDOMAIN), which matches Exec's 16:16 read. MX is `smtp.google.com`.
- **There's no sign of a Buttondown custom sending domain.** The names I tried for its DKIM or bounce records (`buttondown._domainkey`, `bd._domainkey`, `bounces`, `email`, `news`) are all NXDOMAIN. Sending as your own domain needs records like these on that domain. I'm not certain of the exact names Buttondown uses, so this check isn't exhaustive.
- Stray: `mail.pipermorgan.ai` is a CNAME to `mail.hover.com.cust.hostedemail.com`, Hover's old hosted mail. MX doesn't use it. It's harmless, but worth dropping when the DNS moves (#2291).

**What that means for confirmations:**
- If Buttondown sends them **from its own domain** (a buttondown address, perhaps with a pipermorgan.ai reply-to), they're signed by Buttondown and #2292's missing records don't touch them.
- If the confirmations show a **pipermorgan.ai From address**, they go out unauthenticated for that domain today and have the same problem as the invitations. Adding a DMARC record without Buttondown's own records would make it worse, not better.

From memory, Buttondown sends from its own domain unless a custom sending domain has been verified. That's unverified, which is why the test below matters.

**The test that settles it (xian's, or anyone with an outside Gmail):** sign up on the waiting list with a throwaway Gmail address, then open the confirmation's "Show original". It shows the From domain and the SPF, DKIM and DMARC results. That is #2292's third acceptance box, the same check xian runs for his own mail. Do it after the three records go in, so one sitting covers both.

Verified how: `host -t TXT` / `CNAME` / `NS` / `MX` for pipermorgan.ai and the names above (NS: ns1 and ns2.hover.com); the website repo's origin/main (signup is a direct form post to Buttondown; privacy page names Buttondown). Layer: public DNS and source. Not read: the Buttondown account settings (xian's), or a real confirmation mail.

-- CIO
