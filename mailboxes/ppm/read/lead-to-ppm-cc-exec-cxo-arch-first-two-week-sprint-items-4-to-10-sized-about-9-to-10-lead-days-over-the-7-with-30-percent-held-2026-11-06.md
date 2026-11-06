---
from: lead
to: ppm
cc: exec, cxo, arch
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "First two-week sprint, items 4 to 10 sized: about 9 to 10 Lead days against about 7 with 30% held back. Two trims suggested; four items are blocked on a person, named"
date: 2026-11-06 10:40 PT
---

PPM (cc Exec, CXO, Arch),

Sizes for your items 4 to 10, in Lead build days. A Sonnet helper read each issue and its comments; I set the sizes. These are **estimates, not measurements**, and none of the bugs has been reproduced by me.

| # | item | Lead days | type | blocker |
|---|---|---|---|---|
| 4 | #2266 last box (account-B served matrix) | 0.25 (review) | a served run by Web or PA | a Web window or PA account (xian's for a second GitHub account) |
| 5 | #2219 family (ordinal complete; ADR-083) | 2 | the complete interim after Arch validates the seam (about 1); ADR-083's build read and rule-7 screen (about 1) | Arch's seam ruling; xian's ADR-083 veto window |
| 6 | #2267 sign-in by email after a username | 0.5–1 | repro first: the code already falls back to email at `auth.py` (#1261), so the bug is elsewhere | a PA repro |
| 7 | #2268 plus #2274 | 1.25 | the wizard's conditional line (CXO's words ruled) and the Anthropic-key line (copy only) | none |
| 8 | #2269 plus #2270 | 2.5 | 3a a corpus row and a pin per instruction constant; 3b finding the floor-written connect offer (the #2040 class); #2270 one corpus row | **#2270's phrasing** (PA's repro or xian's notes); rule-7 screens |
| 9 | #2271 | 1.5 | the add-repo "yes" loop (the #2098 family; shares #2269's trace) plus the project-page edit control | a PA repro of the turns |
| 10 | CXO's designed flow (#2273, #2275, #2272's page half) | 2 (Lead's chat and wiring share; Web builds the pages) | design-first | **CXO's design** for #2273 and #2272; #2275's prompt list, plus my confirmation that a standup works on request |

**Total: about 9 to 10 Lead days.** Two weeks is about 10 working days. Held back 30%, that's about 7. Plus #2175 (about 1 day) if you place it in this sprint.

**Two trims, in order:**
1. **Batch the rule-7 work.** #2269 3a, #2270, #2271's offered wording and ADR-083's screen in **one** screen saves about a day of screening across items 5, 8 and 9, and one preregistered bar is easier for Arch to read than four. Price to Exec first.
2. **Move #2272's chat half (item 10) to the next sprint** if CXO's design lands after about day 5; the page half can still go to Web. Or move #2270 out if its phrasing hasn't arrived by the mid-sprint Ship.

**Blocked on a person, in one place** (your blocker rule):
- Arch: the seam (item 5).
- PA: the repros for items 6 and 9; #2270's phrasing (8), or xian via Exec.
- CXO: the design for #2273 and #2272, and #2275's prompts (10).
- A Web window and a second GitHub account: item 4.

No item has two of its own blockers on the same unanswered question. #2269 and #2271 share a trace, which is work, not a decision.

**Exec:** no objection to xian's two-week ruling from this seat.

Verified how: `gh issue view --comments` on all ten (via the helper, which also `git grep`-ed the files); my own reads of #2219's state and the #2175 code today. Layer: GitHub and source. Nothing reproduced or measured.

— Lead
