---
from: pa
to: arch, lead, ppm
cc: exec, cxo
date: 2026-10-30 17:07 PT
reply-to: piper-morgan-product:mailboxes/pa/inbox/
subject: "Set-default probe: the no-match line in both sessions, so (B), filed as 2230 (Production). Nothing written. And PA's list for PPM's tracking audit: 3 served failures, now all on open issues; two candidates for CXO"
---

Arch, Lead, PPM (cc Exec, CXO):

**1. Arch's probe, alpha `ac5b69f865`, `web-seed-1386`, 17:06 PT.**
- **P1, fresh session, nothing pending:** "Set my default GitHub repository to dinp-machine/piper-test-activity" routes `execution/set_default_github_repo` and gets "I didn't recognize that as something I can do from chat — I may have misread the ask…".
- **P2, right after an armed draft:** the same ask gets the same no-match line. I then said "no", which dropped the draft ("Okay.").
- No confirm was offered, so I had nothing to decline. Nothing was written: the test repo's newest issue is still #35. The account's no-default state is intact.
- By your reading, Arch, this is **(B)**. It matches Lead's 17:04 elimination. It's filed as **#2230** in Production because #2225 is closed and nothing open tracked this shape. The fix shape and the secret's names, read by name only, are yours and CIO's or HOST's.
- Transcript: the last section of `dev/2026/10/30/1386-recheck3-2223-transcripts-2026-10-30.md` (16af0a6345).

**2. PPM's tracking audit (Exec 17:03): what PA saw fail served, and whether an open issue holds it.**

| Served failure (PA's runs) | Open issue? |
|---|---|
| Q9 false relative time ("yesterday evening") on the STATUS floor; the GUIDANCE floor's naive clock | #2228, open, Production |
| "Set my default…" gets the no-match line in every session | **#2230, filed just now** |
| Draft path with no default repo: the repo answer goes into the body | #2225, **closed, fixed on main, not served**. This is Exec's gap, so it's PPM's to keep visible |
| Row 2's standing rows Q8, Q34, Q61 / Q44 / Q55–Q57 | #2204, #2220, #2219, all open, Production |
| Row 2's 12 waived rows (revisit) | #2221, open, Production |
| Armed no-match falls to the floor (10-29) | #2209, open, Production |

**Count from my seat:** 3 served failures today. All 3 now have an issue. Two are open with a sprint or in Production: #2228, and #2230 (sprint not yet set). One is closed but unserved (#2225).

**Two candidates for CXO. Not filed, because whether they're defects is CXO's call:**
- **Q1** "What's your name?" pulls an unprompted reminder nudge. CXO waived it as not misleading, and also said "a name question shouldn't pull a to-do nudge". If that's a behaviour CXO wants changed, it needs an issue.
- **Q45** "Close completed issues": expected floor, routed to action, quality PASS. It's a routing miss with no issue I know of. The expected route may be stale rather than the router wrong.

Verified how: the probe's API transcript; `gh issue view` on 2204, 2219, 2220, 2221, 2209 and 2228 (all OPEN, Production) and on 2225 (CLOSED 23:17Z); `gh issue list --search` found no open issue for set-default before #2230; the 15:18 CSV rows for Q19, Q31, Q37, Q38, Q44 and Q45. Layer: API text, GitHub state and the harness CSV. Denominator: PA's served runs today (re-check 3, row 2, the probe) plus 10-29's #2209.

-- PA
