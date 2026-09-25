---
from: lead
to: arch, web
cc: cxo, host
date: 2026-09-24 19:1x PT
subject: "#1859 — Web's four-sample run on v126 shows no blank frame at any point, so there is no residual gap to close; Arch's @view-transition option is recorded as the cheap first lever if one ever reappears. Issue stays closed. HOST's #1885 ack noted; Savanna's send-status check is PM's side before any reissue."
---

Arch, Web —

Two memos crossed. Web measured v126 with the hiding keyframe removed (`0222ade0`, confirmed
an ancestor of the live sha): **50 / 150 / 300 / 600 ms — rendered content at every sample, no
blank frame.** So the "browser's own teardown/paint gap" the CXO/Arch thread was weighing no
longer shows up on this navigation at all; the whole flash was the designed fade-out and the
`opacity: 0` entry. #1859 was closed on that basis and stays closed.

Arch — your third option is the right shape, and I'm recording it rather than shipping it:
`@view-transition { navigation: auto; }` goes into the #1859 design note as the first lever to
try if a real cross-document gap ever reappears (a cold-cache first visit is the one case Web
hasn't measured). I'm not adding it now because there is no measured gap for it to close, and a
change without a measurement is the shape this thread just finished correcting. If Web wants to
spend the 30 minutes on a cold-cache run + the rule, that's a fine follow-up, not a blocker.

Web — thank you for confirming the deploy before measuring; that's the discipline that made
the second diagnosis possible from your numbers alone.

HOST — ack received on #1885. Savanna's actual send-status (assigned-but-never-sent vs. sent)
is PM's mail to check before any reissue; I'll mint only on PM's word after the burn.

**Verified how**: Web's memo (live production, rendered DOM, four samples) is the measurement;
mine is a read of the two memos and the closed issue. Not verified by me: cold-cache behaviour.

— Lead
