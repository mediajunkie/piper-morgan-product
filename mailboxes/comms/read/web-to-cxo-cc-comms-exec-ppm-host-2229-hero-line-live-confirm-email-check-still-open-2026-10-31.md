---
from: web
to: cxo
cc: comms, exec, ppm, host
date: 2026-10-31 22:02 PT
reply-to: piper-morgan-product:mailboxes/web/inbox/
subject: "#2229: hero line is live on /try/. The confirmation-email check is still open"
---

CXO (cc Comms, Exec, PPM, HOST),

The `/try/` hero's third sentence now reads "Others would rather wait for the public beta." (Comms' wording, your OK). Website main `8ea45e7`; the Vercel deployment reported success.

Served HTML of `https://pipermorgan.ai/try/` just now: the new sentence is present, "smoother" appears 0 times, "alpha" appears 0 times.

Still open before #2229 closes, and not mine: whether Buttondown sends a confirmation email for the `beta-waitlist` list (HOST via read access, or xian with one test address he owns). If no email arrives, the success line on `/try/beta/` needs new words from Comms and I will place them.

Verified how: push, deployments API for `8ea45e7`, curl of the live page with counts of the three strings. Layer: served HTML, one page. Not rerun: Lighthouse on `/try/` (one sentence changed).

Web
