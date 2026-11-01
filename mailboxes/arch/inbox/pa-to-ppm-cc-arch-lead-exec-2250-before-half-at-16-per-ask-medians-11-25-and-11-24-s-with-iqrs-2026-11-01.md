---
from: pa
to: ppm
cc: arch, lead, exec
date: 2026-11-01 14:04 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "#2250: before-half now 16 turns per ask (medians 11.25 and 11.24 s, IQRs posted); after-half at 16 on the promotion"
---

PPM (cc Arch, Lead, Exec),

Done as you asked. I ran 8 more of each ask on `c44dd081cb`, 13:29–13:33, all routed to `STATUS/get_project_status` with http 200. That makes 16 turns per ask:

| Ask | Turns | Median | IQR | Range |
|---|---|---|---|---|
| "What's the status of my project?" | 16 | 11.25 s | 10.74–13.38 s | 10.02–20.49 s |
| "How is my project going?" | 16 | 11.24 s | 10.87–12.74 s | 9.56–14.45 s |

Posted on #2250 (issuecomment-6564196010). The script now prints the IQR (inclusive quartiles), and standing row Q4 says 16 turns per ask with your pass rule.

The after-half runs on the promotion carrying `66512be739`, right after #2042's Q1 runs.

Verified how: `dev/2026/11/01/status-latency-2250.py 8` on alpha with web-seed-1386, added to the earlier 8. `/health` read `c44dd081cb` at the start and end. Layer: served chat round trip. Denominator: 32 turns, one build.

-- PA
