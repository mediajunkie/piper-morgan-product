# Git Worktrees — Model A Setup (CURRENT on Amber)

**Model A — a stable, per-agent worktree at `~/Development/piper-morgan-worktrees/{role}` on `claude/{role}-cycle` — is the current model on Amber** (CLAUDE.md §"Worktree model", revised 2026-07-25, PM-approved). Model B (Claude Desktop's ephemeral auto-worktree) remains correct on Desktop. Pick by host.

*History: this page said "Model A is DEPRECATED as of 2026-06-12; Option B is canonical" until 2026-10-08 (R6 step 4, defect S2). That was true only while the cohort ran on Claude Desktop.* Lifecycle: `docs/internal/operations/amber-worktree-lifecycle.md`.

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
