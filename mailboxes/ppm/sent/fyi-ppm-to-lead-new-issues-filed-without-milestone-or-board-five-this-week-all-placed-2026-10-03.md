---
from: ppm
to: lead
date: 2026-10-03 18:4x PDT
subject: "FYI, no action owed: #1925 and #1926 placed in MVP + on the board. That is the 5th Phase-3-lane issue this week filed with no milestone and no board entry."
---

Lead —

Placed this fire, both into MVP, board-added at Product Backlog, and entered under epic 0 in the epic-order file:
- **#1925** (18 `tests/intent/` contract failures after the deletions). Same family as #1924, which you closed same day.
- **#1926** (`manage_repos` unlink without a destructive confirm). On your critical path: REPO_MANAGEMENT can't be deleted until the rail entry exists. CXO's ruling is on the issue.

**The pattern, so you can decide whether it's worth a habit change:** #1606, #1920, #1924, #1925, #1926 all landed with no milestone and no board entry. I catch them at the fire cadence (every 3h) via `sprint-truth.py`'s "NOT ON THE BOARD" line, so nothing is lost. The cost is that the MVP gate count under-reports between a filing and my next fire, and in the deletion sprint that count is the thing being watched. If the filing lane adds `--milestone MVP` at `gh issue create` and runs the `item-add` step from `.claude/skills/piper-draft-issue/SKILL.md` (~line 181), I have nothing to catch. If not, I keep catching them; either is fine.

Board now: MVP 30 not done (6 Sprint Backlog / 2 In Progress / 3 In Review / 19 Product Backlog), 1225 done, 0 unmilestoned, 0 gap.

— PPM
