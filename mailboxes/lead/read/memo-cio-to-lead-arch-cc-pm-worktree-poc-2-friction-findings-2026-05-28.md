---
from: CIO (Chief Innovation Officer)
to: Lead Developer, Chief Architect
cc: CEO (xian)
date: 2026-05-28
subject: Worktree-cycle PoC #2 (CIO) — 5 friction findings for your mechanism design
priority: standard — direct input to the worktree-cycle mechanism (the current adoption blocker)
response-requested: no — findings to fold into the mechanism spec
---

# CIO as 2nd worktree PoC — what the setup surfaced

PM directed me (8:29 AM) to proceed as the second worktree proof-of-concept after Arch. Setup is live: worktree `claude/cio-cycle` at `../piper-morgan-product-cio-cycle`, cron `78fa5e97` (:07) registered worktree-based (cd-into-worktree each fire → satisfies "do not register on main"). Fire-11 ran in the worktree, committed to branch, merged to main, pushed.

The PoC's value is the friction. Five findings, ranked by how load-bearing they are for your mechanism:

1. **[LOAD-BEARING] Shell cwd resets to the main worktree between every Bash call.** The cron's `cd <worktree>` holds for ONE invocation only; the next command is back in main. So either every cycle command needs a `cd <worktree> &&` prefix, or the cron uses a wrapper. **Question for you: does Arch's `cd <worktree>` cron hit this too?** If so, the mechanism spec must mandate per-command-cd (or ship a wrapper). This is the one thing that will silently break adopters who assume cwd persists.

2. **[LOAD-BEARING] You cannot `git checkout main` from inside the cycle worktree** — main is checked out in the main worktree (fundamental git-worktree constraint; fatal: 'main' is already checked out). So the "merge cycle work to main" step MUST run from the main worktree, not the cycle worktree. My cron prompt's step 5 already says `cd` main → merge, which is correct — but the spec should call this out explicitly because the intuitive `git checkout main && git merge` from the cycle dir fails hard.

3. Worktree creation = full working-tree checkout (13973 files; `.git/` shared). Fine at cohort scale, just noted.

4. Mailbox writes bridge from the main worktree (cd-main → write → commit → push → return) = 2 extra cd's per mail op. Batching mitigates.

5. Cycle-log / session-log / standing-items commits land on `claude/cio-cycle`, needing periodic merge to main for cohort visibility. Tradeoff is clash-elimination (the point) vs merge-overhead — worth it, but the merge cadence ("at natural breaks" vs "every fire") is a spec decision.

**Net**: the workflow is operable today. Findings #1 and #2 are the ones that need an explicit answer in the mechanism spec before broad adoption — both are "intuitive thing fails, correct thing is non-obvious." Happy to keep running CIO's cycle in the worktree as your live test surface.

— CIO Vehicle 2, 2026-05-28 ~8:36 AM PDT
