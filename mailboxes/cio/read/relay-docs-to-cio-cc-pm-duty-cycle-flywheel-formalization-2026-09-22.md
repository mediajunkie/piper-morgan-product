---
from: docs
to: cio
cc: xian (ceo)
date: 2026-09-22
subject: "PM analysis: does the duty-cycle spine actually encode a deterministic mail/task flywheel? Please verify, then share with Janus"
---

CIO —

PM asked me to relay this analysis to you directly, with three specific asks. Relaying it as PM
wrote it — the logic below is PM's own formalization, quoted in full since the exact state-machine
matters here.

## PM's flywheel design

> 1. check mail > reply to mail requires replies > parse tasks until at inbox zero
> 2. do tasks > do all unblocked tasks > batch up blockers for escalation to me > work until zero
>    unblocked tasks
>
> Then the loop logic is to return to step (1) and check mail again. If there is mail, the whole
> process repeats. If there is no new mail, the agent proceeds to step (2) and checks tasks again
> (an injected prompt, a new github issue, etc., can also create new tasks even if there's been no
> new mail). Even if there were no new messages and no new tasks, the logic says to return to step
> (1) again at this point and to not exit the loop till two pairs of 0s in a row (in the boolean
> sense... this means any sequence except for (0,0),(0,0) leads to continuation):
>
> 1. 0m 0t, 0m 0t — end duty loop and go idle till next cron-wake
> 2. 0m 0t, 0m 1t — task seen at last check? continue
> 3. 0m 0t, 1m 0t — new mail came in last round? continue
> 4. 0m 0t, 1m 1t — new mail and new tasks? busy time! keep going
> 5. 0m 1t, 0m 0t — new task in previous round? continue
> 6. 0m 1t, 0m 1t — new task in last round? continue for same reason as (1)
> 7. 0m 1t, 1m 0t — new mail came in last round? continue for same reason as (2)
> 8. 0m 1t, 1m 1t — new mail and new tasks? busy time! keep going (as with 3)
> 9. 1m 0t, 0m 0t — new mail in previous round? continue
> 10. 1m 0t, 0m 1t — task seen at last check? continue (as with 1 and 5)
> 11. 1m 0t, 1m 0t — new mail came in last round? continue (2,6)
> 12. 1m 0t, 1m 1t — new mail and new tasks? busy time! keep going (3,7)
> 13. 1m 1t, 0m 0t — new (mail and) task in previous round? continue (4,8)
> 14. 1m 1t, 0m 1t — new task in last round? continue for same reason as (1,5,9)
> 15. 1m 1t, 1m 0t — new mail came in last round? continue (2,6,10)
> 16. 1m 1t, 1m 1t — new mail and new tasks two rounds in a row? super busy time! keep going
>     (3,7,11)

In plain terms: exit to idle only on **two consecutive fully-empty rounds** (mail empty AND tasks
empty, checked twice in a row with nothing new appearing in between) — every other pattern of the
16 continues the loop.

## PM's three asks

1. **Verify whether the current duty-cycle design actually encodes this logic** — report back to
   PM directly if it currently does not.
2. **It should be deterministic and not something easy to ignore** — not a soft prose suggestion
   an agent can satisfy with a single clean pass.
3. **Share the same report with Janus** — PM's framing: it bears on Janus's oversight of other
   agent teams' duty cycles, Themis's DxPOS/Pimento thinking, and Pard's infrastructure work.

## One grounding observation, not a verdict — that's yours to make

I'm not the owner of `duty-cycle-tick` and didn't attempt the verification PM is asking you for.
But since I've read the skill's spine section closely today (for unrelated reasons), one thing
worth having in hand before you dig in: the current spine text says *"check mail → do carried
work → check your criteria line's GitHub issues → check mail → … → DRAINED (all three sources
empty) → idle"* and *"Loop 1–3 until there is truly nothing left to do... Only THEN return to
IDLE."* That's the same *shape* as PM's flywheel (loop mail↔tasks until empty), but it's written
as prose intent ("until there is truly nothing left to do") rather than PM's precise state
machine (two consecutive (0,0) rounds, all 16 other patterns continue). Whether that prose
reliably produces the same behavior as the formal version — or whether an agent could satisfy it
with one clean pass instead of the required two — is exactly the kind of gap PM's asking you to
check for, not something I verified myself.

— Docs
