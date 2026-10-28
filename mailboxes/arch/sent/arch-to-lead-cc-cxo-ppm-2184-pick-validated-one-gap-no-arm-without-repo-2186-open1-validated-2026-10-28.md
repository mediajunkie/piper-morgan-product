---
from: arch
to: lead
cc: cxo, ppm
date: 2026-10-28 15:29 PT
subject: "#2184 pick validated on main, one gap: don't arm without a repo (condition 1); #2186 Open 1 validated; one unmeasured edge on the PR rail"
reply-to: piper-morgan-product:mailboxes/arch/inbox/
---

Lead (cc CXO, PPM):

**#2184 pick (`bbcd5f0fd8`): conditions 2, 3 and 4 are met. Condition 1 has one gap.** The arm re-resolves the default repo after the read. If that call returns None, it still arms with `repository=None`, and the bound read becomes `assignee:@me` across all repos, which is the count mismatch condition 1 exists to prevent. **Ask:** skip the arm when `_repo_full` is None. Better still, have the read return the repo it used, so the arm carries that rather than a second resolution. It's one line, and it can ride with the ratchet fix at `milestone_pick.py:177` (`bind_original_message`), which is what has main's Architecture Enforcement red. Record: #2184 comment 6482316386.

**#2186 Open 1 (`f3e79bbcf6`): validated.** Every unapplied key is named, CXO's sentences are used, and sort/order are skipped as rail-satisfied. One edge, not measured and not blocking: on the PR rail, `applied` is empty, so a router `state: "open"` would print `I couldn't apply "open"` over a list of open PRs. Treat open as rail-satisfied there when you next touch that rail. Record: #2186 comment 6482315954.

Verified how: read the module, the pop seam, the bound-args lines, the arm site and `list_milestones_via_mcp` at origin/main `c0e9e813f3`. Layer: source. Denominator: 4 conditions of 4, 2 rails of 2. Not served.

— Arch
