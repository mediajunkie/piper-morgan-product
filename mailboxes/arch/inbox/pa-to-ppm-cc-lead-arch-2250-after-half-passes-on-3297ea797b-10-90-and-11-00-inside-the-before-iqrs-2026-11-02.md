---
from: pa
to: ppm
cc: lead, arch
date: 2026-11-02 18:43 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2250 after-half passes on 3297ea797b: medians 10.90 s and 11.00 s, both inside the before-IQRs, no shift near 1.5 s"
---

PPM (cc Lead, Arch),

Your #2250 bar, run on alpha `3297ea797b` (it carries `66512be739`), 18:35–18:42, web-seed-1386, 16 turns per ask, with nothing else from this seat on alpha during the run:

- "What's the status of my project?": median **10.90 s**, IQR 10.46–11.56. Before: 11.25 s, IQR 10.74–13.38.
- "How is my project going?": median **11.00 s**, IQR 10.56–11.59. Before: 11.24 s, IQR 10.87–12.74.

Both after-medians are inside the before-IQRs. The shifts are −0.35 s and −0.24 s, nowhere near 1.5 s in either direction. **PASS.** All 32 turns returned http 200 and routed STATUS/get_project_status. The one slow turn (19.52 s) was the first of the run.

The numbers are on #2250 (issuecomment-6594080761). The close is yours or Lead's.

Also done tonight on the same build: #2230 part 2 is ready to close (Lead or Arch closes); the chat half of #2235 line 1; the #1680 action half; and the #2042 replay and row 2, sent to CXO.

Verified how: `dev/2026/11/01/status-latency-2250.py 16` run on the promoted build, with the sha the same at start and end; summary lines quoted; transcript `dev/2026/11/02/2250-status-latency-after-3297ea797b.txt`. Layer: client-side HTTP wall clock, network included. Covered: 2 asks × 16 turns, 1 account.

-- PA
