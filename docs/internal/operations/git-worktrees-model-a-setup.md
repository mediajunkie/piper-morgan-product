# Git Worktrees — Model A Setup (DEPRECATED)

**Model A (dedicated `claude/{role}-cycle` worktrees) is DEPRECATED as of 2026-06-12.** The Option B ephemeral worktree model is canonical for all roles. PM-approved exceptions only; no current exceptions. See `dev/active/cohort-plan-of-record-2026-06-12.html` for the full decision record.

This document is retained for the exception case and history only.

---

## Why worktrees matter (branch collision context)

A git repo can have only one branch checked out at a time per working tree. If two Claude Code sessions are running in the same directory and one checks out a feature branch, the git HEAD flips for the other session too — file contents change out from under the other agent. This happened 2026-04-22 when Lead Dev checked out `claude/992-ethics-activate` while a Docs session was mid-work.

**Use a worktree when**: an agent will be working on a `claude/*` or other non-main branch while another agent is likely working in the same repo on `main`.

**Not needed when**: both agents are on `main`. They can share the one working tree fine.

---

## Setup (Model A — dedicated worktree)

One-time setup per feature branch:

```bash
# From the main repo dir, create a sibling checkout of the feature branch:
git worktree add ../piper-morgan-product-{branch-suffix} {branch-name}

# Example for the #992 ETHICS-ACTIVATE branch:
git worktree add ../piper-morgan-product-992-ethics-activate claude/992-ethics-activate
```

Open Claude Code in the worktree path, not the main checkout. Both sessions share `.git/` metadata but have independent checked-out branches and file contents.

## Cleanup

```bash
git worktree remove ../piper-morgan-product-{branch-suffix}
```

Run when the feature branch is merged and no longer needed. The worktree list lives in `.git/worktrees/`.
