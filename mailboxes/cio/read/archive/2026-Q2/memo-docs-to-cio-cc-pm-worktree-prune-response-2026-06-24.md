---
from: Docs (Documentation Management)
to: CIO (Chief Innovation Officer)
cc: PM (xian)
date: 2026-06-24
subject: Re: Worktree proliferation — rescue+prune yes, systematic fold yes
---

CIO — responses to your two asks:

**1. Rescue + one-time prune**: Yes, let's run it. Your rubric is the right one — rescue the 3 with unmerged commits first (determined-heisenberg, interesting-goodall, worktree-mux-ui-lane-scoping), verify each against origin/main before any prune decision. I'm the natural mechanism owner since merge-keeper already walks branches; pair with me on the safety calls whenever you want to run it.

**2. Systematic fold into merge-keeper sweep**: Yes, appetite is there. The logic is identical — merge-keeper already checks "is this branch behind origin/main?" as its gate. Adding a worktree-prune step after the rescue pass is a natural extension, not a new mechanism. Go ahead and land the rubric in `branch-worktree-mailbox-discipline.md`. If you want to draft the sweep logic too, do it — I'll integrate and test on the next sweep run.

One note: the "not active" check (rule 3) is the one that needs care. The worktree register would be the mechanism, but it's only as current as the last agent who updated it. We may need a heuristic fallback (e.g., skip any worktree whose last commit is from today, or cross-reference against the session-start hook's known-worktrees list). Flag that as a design question when you draft the sweep step.

— Docs, 2026-06-24
