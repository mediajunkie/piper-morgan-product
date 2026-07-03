---
from: ppm
to: xian (ceo)
cc: lead
subject: "#1235 Sprint field — clarification + decision request"
date: 2026-07-03 15:52 PT
---

# #1235 Sprint Field — PPM Clarification + PM Decision Request

**From**: Principal Product Manager (PPM)
**To**: PM
**CC**: Lead Dev
**Date**: July 3, 2026
**Re**: #1235 Sprint field — Lead Dev asked for my intent; PM's call on final disposition

---

## Answering Lead's question

Lead asked whether my rationale for moving #1235 to M3-Quality was cherry-pick/early-completion (Option 1) or topical-only (Option 2).

It was **Option 2 — topical/categorical only**. My reasoning this morning: #1235 is a `#1223`-family conversation display bug; RECONNECT WS-2's scope is GitHub MCP + calendar integration; #1235 doesn't belong in RECONNECT categorically. That's a mis-tag, not a statement about when the work happened or which sprint it was "done for." I wasn't claiming it was cherry-picked M3-Quality work.

Lead's revert was the right call. PM's flag is correct — moving a closed issue into an unstarted sprint misrepresents both the issue's timeline and the sprint's scope, especially given the sprint-board history. I should have flagged the closed→unstarted-sprint ambiguity when making the call rather than routing it as a straightforward reassignment. That's on me.

---

## Your decision: three options

#1235 is currently back in RECONNECT (its pre-edit state). The Sprint field is PM-gated per standing norm. Three clean options:

| Option | Action | Effect |
|--------|--------|--------|
| **A — Clear the field** | Remove RECONNECT, leave Sprint unset | No timing misrepresentation; #1235 surfaces naturally in M3-Quality triage when that sprint opens. **PPM lean.** |
| **B — Leave in RECONNECT** | No change; accept the categorical mis-tag | Stable, no further board churn. Accepted as wrong-but-stable. |
| **C — Move to M3-Quality** | Move Sprint field to M3-Quality with PM sign-off | Correct categorically, but requires PM's explicit OK on closed→unstarted-sprint optics. Lead Dev will not execute without that. |

**PPM lean: Option A (clear the field)**. Cleanest — avoids the timing problem and doesn't force a choice between two imperfect labels. The issue will come up naturally in M3-Quality triage.

No urgency — #1235 is closed and not blocking anything. Whenever you have a moment.

---

*PPM — July 3, 2026*
