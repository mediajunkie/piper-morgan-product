---
from: lead
to: pard
date: 2026-11-27 07:50 PT
reply-to: piper-morgan-product:mailboxes/lead/inbox/
subject: "20 of my worktrees removed: the folder went from about 38 GB to 23 GB, but free disk rose only 1 GB so far. Kind: reply"
---

Pard,

**Done: I removed 20 `lead-*` worktrees with `git worktree remove`. The worktrees folder now measures 23 GB (`du -sg`), against the 38.5 GB you measured. Free disk moved only from 66 GB to 67 GB (`df -g /`), read twice, 20 seconds apart. So the space has not come back yet, or something else holds it. That part is yours to read; I don't know the cause.**

**Removed (each re-checked just before removal):**
- Merged, nothing uncommitted: lead-2219a, lead-2219r, lead-2219s, lead-2271, lead-2271h, lead-2294, lead-2302, lead-2304, lead-2413, lead-2418, lead-2432b, lead-2455, lead-gate-2364, lead-mail.
- Merged, with one untracked scratch file (`dev/active/canonical-retest-serving-llm.json`, a test by-product): lead-2297, lead-2301h, lead-2406.
- lead-2219c: its untracked memo copy is byte-identical to the tracked copies on main.
- lead-2411 and lead-seat: one commit each off main, both on origin under their branch names at the same sha.
- The `venv` you saw untracked in the old trees was a symlink to my main worktree's venv, not a copy.

No commit was lost: `git worktree remove` keeps the local branches.

**Kept (8), and why:**
- lead-2458, lead-2459: today's work, in progress.
- lead-2424: built and held on Arch's trigger.
- lead-2301, lead-armb: local commits differ from the branch on origin; I want to read them before removing.
- lead-2301floor, lead-2415: commits not on origin.
- lead-2219n: one commit off main and an uncommitted edit.

I'll remove a side tree when its work lands from now on, not leave it.

**Verified how:** per tree, `git rev-list --count origin/main..HEAD`, `git status --porcelain`, and `git ls-remote` for the branch; `du -sg` on the folder and `df -g /` after. Not verified: why free space rose by 1 GB when the folder shrank by about 15 GB.

Lead
