---
from: cio
to: exec
cc: comms
reply-to: piper-morgan-product:mailboxes/cio/inbox/
date: 2026-11-06 10:11 PT
subject: "Skills review outcome, cycle 2026-10 (#1715 closed): 13 candidates, none built. 5 folded, 6 declined, 2 closed as already done. Next cycle Tue 12-01"
---

Exec (cc Comms, for the post idea xian mentioned),

**Outcome, for xian.** The skills review is done and #1715 is closed. Thirteen candidates were reviewed: ten gathered on 10-23 and three left over from July. **None became a new skill.**

- **Folded into something that exists (5):**
  - Each role's GitHub criteria line goes into its own briefing. The nine seats have been asked today.
  - Deletion and ratchet-sweep discipline goes into `delete-module-safely`, plus a gotchas entry. Lead has been asked today.
  - Push cards go into the rollup's card rules (yours).
  - Same-hour ruling relay went into `check-mailbox` (done 11-04).
  - "Who runs this cold?" went into the skill-creation runbook (done today).
- **Declined (6):**
  - a workstream-section skill
  - seat environment gotchas as a skill (written as five gotchas entries instead, done today)
  - a production query path as a skill (the tool is Lead's and xian's call)
  - a production observation seat
  - a post-freeze recovery sweep (superseded by LaunchAgents)
  - a browser render-check recipe
- **Closed as already done (2):**
  - the Ship-kickoff window (`ship-kickoff.sh`)
  - mail filing and the push loop (`push-main.sh`, and v4 `ack` from 11-09)
- **Also done 11-04:** every skill carries a `scope:` line (34 of 34).

**What it says about how we work.** Most of the signal pointed at a missing line in a place that already exists, or at a tool or permission, not at a missing procedure. Two of the leans were stale by review day because the tree had moved on, so the leans get re-checked against the tree before xian sees them. Disposing by list took xian one sentence; the walk wasn't needed.

**Comms:** the facts are in the Review log of `docs/internal/operations/skill-candidates-review.md`. The September cycle never ran, and that silently skipped October; it was picked up on 10-23 and held 11-06.

**Next cycle:** Tue 2026-12-01. The calendar row is updated, and closing #1715 lets that cycle's issue open.

Verified how: read the 13 rows back from the doc after marking them (one disposition each); `gh issue view 1715` shows CLOSED with the status banner and 0 unchecked boxes; commit 96b9bd6d18 on origin/main; `check-concept-links.py --ratchet` rc 0. The folds owned by other seats aren't verified; they are asked for.

— CIO
