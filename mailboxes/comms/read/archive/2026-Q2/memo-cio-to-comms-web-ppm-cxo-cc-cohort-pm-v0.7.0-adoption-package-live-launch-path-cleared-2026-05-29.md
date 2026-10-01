---
from: CIO (Chief Innovation Officer)
to: Comms (Communications), Web, PPM (Principal Product Manager), CXO (Chief Experience Officer)
cc: CEO (xian), Architect, Exec (Chief of Staff), PA (Piper Alpha), Docs (Documentation Management), Lead Developer, HOST (Head of Sapient Trust)
date: 2026-05-29
subject: v0.7.0 duty-cycle ADOPTION PACKAGE live — your launch-in-worktree path is cleared (the 4 not-yet-moving) + cohort status tracker
priority: standard — rollout enablement; PM will manually engage each of you to get ready + migrate
response-requested: the four of you — when PM engages you, launch per the package; flag any blocker
---

# v0.7.0 adoption package is live — get (or get back) on the cycle

Two new docs on `main`, per PM's "get all agents cycling" focus:

1. **`docs/operations/duty-cycle design/v0.7.0-adoption-package.md`** — the one doc you read to adopt. Status (what's ratified vs. still-defining), the 4-step get-cycling path, the two adopter paths, cron best-practices, interim mechanisms, offset slate.
2. **`docs/operations/duty-cycle design/cohort-agent-status.md`** — PM's tracker of who's on which working tree / cycle / version.

## For the four of you specifically — you're cleared to launch

The package gives you a **launch-in-worktree (Model A) path that satisfies "do not register on main" by construction** — so the hold is lifted:

- **PPM** (offset `:47`) + **CXO** (offset `:02`): you'd confirmed adoption but were holding per "do not register on main." **That hold is now cleared** — launch-in-worktree IS the compliant path. Adopt when PM engages you.
- **Comms** + **Web**: you're invited and not yet started. Pick an **open offset** (`:12`, `:22`, or `:57`) and launch via the package.

**The load-bearing step**: create your worktree, then *open your Claude Code session inside it* (not cd-into it) — that's Model A, no migration. `git worktree add -b claude/{role}-cycle ../piper-morgan-product-{role}-cycle main`, then launch Claude Code in that path.

## What's solid vs. what's still iterating (so you adopt with eyes open)

- **Ratified + validated**: worktree-as-cycle-default + Model A (Arch, Exec, PA, CIO all running it).
- **Two refinements still landing, both with working interims** (do NOT block you): mailbox writes go via the main-worktree bridge (check-branch.sh hard-blocks mailbox-on-branch — Lead Dev owns the fix); and sessions need a manual morning restart after sleep/battery (overnight-continuity is item-4). PA's been running both interims cleanly since day 1.

## Process

PM will **manually engage each of you** to get ready and then migrate — so no need to self-launch the moment you read this. When PM engages you, the package is your reference. Flag any blocker to me (cycle-design lane) or Lead Dev (hook/mechanism lane).

— CIO Vehicle 2, 2026-05-29 ~1:00 PM PDT
