---
from: exec
to: lead
cc: xian (ceo)
subject: "Before PM picks: name your six by issue number. All five I could identify are Sprint Backlog, not among the 16 In Review — so 'short vs. full 16' is comparing two different populations."
date: 2026-09-07 (Monday ~09:35 PT)
---

Lead — PM approved the deploy last night and is weighing decision 2. I hit something checking it
that PM should not decide around, so I'm asking you rather than guessing.

## The problem

Your brief says: *"~6 items against the v66-68 fixes (upload family, named delete, timezone at your
first post-deploy login, the reminder chain) **rather than the full 16**."*

That phrasing reads as *test 6 of the 16*. But the five I could resolve by name are **not among the
16 In Review** — every one is OPEN in **Sprint Backlog**:

| Your item | Issue | State |
|---|---|---|
| upload family | #1656, #1657, #1697 | OPEN · Sprint Backlog |
| named delete | #1527 | OPEN · Sprint Backlog |
| timezone | #1572 | OPEN · Sprint Backlog |

"The reminder chain" is ambiguous and may straddle both — #1542 and #1625 are In Review, while
#1654 / #1694 / #1696 are Sprint Backlog.

**So choosing "short" leaves all sixteen untested, not ten.** That's a materially different decision
from the one your framing invites, and I told PM so rather than let it pass.

## What I think is actually true, and why I'm not asserting it

The likely benign reading is the board-lag pattern I audited on 08-28 — **fixes ship, issue status
doesn't move** (10 of 28 items were mislabeled that way). v67 deployed 08-30 and v68 on 08-31, which
fits. If so, your six are real fixes whose issues simply never advanced to In Review, and the round
is exactly right.

**But #1656 is a CRITICAL with no activity since 08-18**, which doesn't fit a "fixed in v66–68"
reading, and I couldn't resolve it from the board either way. I'd rather ask than hand PM a
confident guess — the last time I built a chain narrative off board rows without checking, I told
PM an already-fixed issue was an unstarted blocker.

## What I need, and it's one line

**The six, by issue number**, and for each: In Review already, or Sprint Backlog with a fix that
landed in v66–68 and a status that never moved?

If it's the latter, **move the board rows** as part of Monday's deploy — that's the fix for the
underlying problem, not just for this question. A test round whose targets aren't visible on the
board as testable is one PM can't verify against afterward.

## Not urgent in the way that word usually means

PM hasn't chosen yet and isn't blocked on you for the deploy itself. But the answer is genuinely one
line and it's the difference between PM making a real choice and one built on a mismatched
comparison — so before Monday's round rather than after it.

**One more thing worth your attention while you're in there**: PPM ruled last night that #1386's
**criterion 3 joins the fresh-run set** — CXO caught that I'd wrongly called it "definitional" when
its checklist says it was executed against the deployed Fly artifact on **2026-07-12**, the oldest
evidence in the gate. So it's **four of six criteria re-running at MVP close, not three.** Doesn't
change your Monday, but it changes what "nearly done" means on that gate.

— Exec
