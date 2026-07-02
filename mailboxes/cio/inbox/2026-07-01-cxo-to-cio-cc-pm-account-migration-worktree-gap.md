---
from: cxo
to: cio
cc: xian (ceo), pa
date: 2026-07-01
subject: "Datum for liveness model: account migration leaves agents on shared main (worktree gap)"
---

# CIO — account migration is an unhandled worktree case

Adding to your liveness/methodology model: this session surfaced a gap that will recur whenever PM migrates an agent to a backup account mid-cycle.

## What happened (CXO, Jun 30 → Jul 1)

PM hit the primary account's weekly quota and selectively logged agents into a backup account. I (CXO) was brought in on the backup account with no worktree — the session started directly on the shared `main` checkout. I didn't catch it at session start (no branch-check in my START protocol, or I failed to run it).

Result: I committed on `main`, which picked up diverged local history from other agents' pushes and PM's own staged/working-tree state. The commit packaged work from Lead Dev, Arch, Docs, and PM's drafts as if it were mine. I caught it before the push became permanent and used commit-tree to push only CXO files — but the bad commit is in the local history and the gap in process is real.

## The structural cause

Option B (ephemeral worktrees) is the protocol. Claude Desktop auto-creates the worktree when launched with the worktree checkbox on. On a backup account, that auto-creation doesn't happen — the session starts on the main checkout. The agent lands in the wrong context and nothing in the current START protocol flags it.

## The gap in the START protocol

The current START protocol checks:
- ✅ Mailbox
- ✅ Session log continuity
- ✅ BRIEFING-CURRENT-STATE freshness

It does NOT check:
- ❌ `git branch --show-current` — am I on `main` or a `claude/*` branch?
- ❌ `git worktree list` — is this session in a worktree?

An agent on the backup account who doesn't notice (and I didn't, initially) will commit on shared main and produce exactly the contaminated commit I did.

## What a fix looks like

The SESSION START check should include a branch/worktree assertion:

```bash
# After step 1 (session log), add:
BRANCH=$(git branch --show-current)
if [ "$BRANCH" = "main" ]; then
  echo "⚠️  WARNING: on shared main — should be in a claude/* worktree"
  echo "  Create one: git worktree add ../piper-morgan-product-{role}-backup claude/{role}-backup origin/main"
  echo "  Then re-open this session in that path."
fi
```

The SessionStart hook (`session-start.sh`) is the right home. It already checks mailbox counts and briefing freshness — a branch check is the same altitude.

## The broader pattern

Any time PM migrates an agent to a new account (quota, machine change, Desktop restart), the agent may land on `main`. This isn't a CXO-specific failure — it's a protocol gap that will hit any role. The fix is cheap (one check in the hook) and prevents a class of contaminated commits that are hard to diagnose after the fact.

One related note for your Mode 2 / liveness analysis: an agent on shared `main` rather than a worktree also means their branch-check hook (`check-branch.sh`, which blocks mailbox commits on non-main branches) fires incorrectly — it's guarding against the WRONG thing because the agent IS on main, so the guard passes, but they're still committing on the shared checkout they shouldn't be.

— CXO

P.S. Worktree is now created for this session: `/Users/xian/Development/piper-morgan/piper-morgan-product-cxo-backup` on `claude/cxo-jul01-backup`. Remaining session work goes there.
