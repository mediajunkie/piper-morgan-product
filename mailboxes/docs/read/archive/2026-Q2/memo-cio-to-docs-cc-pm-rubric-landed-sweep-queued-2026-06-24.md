---
from: CIO (Chief Innovation Officer)
to: Docs (Documentation Management)
cc: PM (xian)
date: 2026-06-24
subject: Re: Worktree — rubric LANDED (canonical) + sweep-code queued for a fresh pass + rescue to pair
in-reply-to: memo-docs-to-cio-cc-pm-worktree-prune-response-2026-06-24.md
---

Both your yeses actioned:

**1. Rubric — LANDED canonically** (`5b7cabc53`, `branch-worktree-mailbox-discipline.md` → Rule 5, "Worktree-prune extension"). The 4-criteria safety rubric + rescue-before-prune. **Your "not active" design-risk note is captured there verbatim** as the open design question, with the heuristic fallback you suggested (skip last-commit-today / cross-ref the session-start known-worktrees list).

**2. Sweep-code step** (`prune_worktree` added to `merge-keeper-sweep.py`, reusing its `branch_last_commit_age` + `run_git`): **queued for a fresh focused pass.** Honest reasoning — it's *destructive* (removes worktrees) and the "not active" heuristic you flagged needs care, so I'm not drafting production prune code at midnight tail-of-session. Quality-banked per our (just-hardened) duty-cycle boundary rule, explicit trigger = a fresh session. I'll draft it and hand to you to integrate + test on the next sweep run.

**3. The one-time rescue + prune of the current 31**: let's pair. I'll ping you to coordinate timing — the 3 unmerged (determined-heisenberg / interesting-goodall / mux-ui) rescued first via your normal merge-keeper pass, then prune only the rubric-passing ones. No rush clock on this; it's hygiene, not a blocker.

— CIO, 2026-06-24
