---
type: protocol
title: Git Workflow Protocol
valid_from: "2026-01-24"
last_verified: "2026-10-31"
---

# Git Workflow Protocol

How agents use git in this repo. The rules live in `CLAUDE.md` ("Worktrees", "Hard rules", "Git, push, sign-off"). This page is the working summary. If it ever disagrees with `CLAUDE.md`, `CLAUDE.md` wins and this page is stale.

*Rewritten 2026-10-31 (Docs, issue 1726). The earlier version described session-ID feature branches and a rule never to push to `main`. That is no longer how this cohort works.*

---

## Where you work

- **Amber (the cohort host):** your stable worktree `~/Development/piper-morgan-worktrees/{role}` on branch `claude/{role}-cycle`, reused every session.
- **Claude Desktop:** the ephemeral worktree Desktop creates for the session.
- **Never** work in the shared checkout `~/Development/piper-morgan-product`. It is the PM's live workspace with uncommitted edits.
- **Lane branches.** A worktree or subagent on `claude/{role}-{issue}` commits there and pushes the branch itself (`git push origin claude/{role}-{issue}`), never `HEAD:main`. The lane's owner merges it into their cycle branch, runs the landing gate and pushes to `main`, so a coding agent on a lane never lands its own work. Desktop and Web seats push `HEAD:main` the same way as any cycle branch.

---

## Session start

```bash
git fetch origin main
git rev-list --count HEAD..origin/main   # must be 0; if not, git merge origin/main
git branch --show-current                # your claude/{role}-cycle branch, not main in the shared checkout
```

Before reading git or file state to answer a question, fetch and fast-forward again if more than a few minutes have passed.

---

## Development workflow

```bash
# 1. Make changes in your worktree

# 2. Before committing
./scripts/fix-newlines.sh

# 3. Stage in one call, commit in the next
git add <specific-files>        # explicit paths, never "git add .", "-A" or "-u"
git commit -m "your message"

# 4. Push the finished unit to main
git push origin HEAD:main
```

Why two calls for stage and commit: a mailbox hook reads the index before a compound `git add && git commit` runs.

Work that is not on `origin/main` is invisible to other agents, so push each finished unit as you go. Commit your session-log entry with the unit it describes.

Mail files are the exception: write the memo and send it with `scripts/mail-send.sh`. Do not `git add` or commit mailbox files yourself.

If the push is rejected because another agent pushed first, `git fetch origin main && git merge origin/main`, then push again. A push is a dispatch, so re-read your inbox before the retry when more than a few minutes have passed.

---

## Commit message trap

A commit message that pairs close, fix or resolve with `#N` closes issue N, whatever the surrounding words. Write the number without `#`, or add the trailer `Auto-Close: intentional` when closing is intended. `.claude/hooks/autoclose-guard.sh` enforces this.

---

## Before every commit

- [ ] `git branch --show-current` shows your own branch
- [ ] You ran `./scripts/fix-newlines.sh`
- [ ] You staged explicit paths
- [ ] After subagent work, `git status` shows nothing unexplained left in `services/`, `tests/` or `web/`

---

## Sign-off

```bash
git status
git fetch origin main
git rev-parse --verify -q origin/main >/dev/null || echo "STOP: origin/main did not resolve; the check below did not run"
git log --oneline origin/main..HEAD   # must be empty
```

If it is not empty: `git fetch origin main && git merge origin/main && git push origin HEAD:main`, or leave a NOTICE memo saying why the work is held, or ask the PM. At idle points run `scripts/sync-pm-local.sh` to fast-forward the PM's checkout (it never touches the PM's prose edits).

---

## Hard rules for the shared checkout

In `~/Development/piper-morgan-product` never run: `git checkout -- <path>` or `.`, `git reset --hard`, `git stash`, `git clean`, or anything else that discards working-tree changes. If a merge or rebase there is blocked by unstaged changes, stop and push from your own worktree instead.

Before any `git checkout <ref> -- <path>` anywhere, run `git diff HEAD -- <path>`. If it is non-empty you are about to discard uncommitted work.

The stash stack is shared across the main checkout and all worktrees, and other sessions push and pop it concurrently. Never run bare `git stash` or `git stash pop`, a pop can take someone else's work. Prefer a temporary WIP commit. If you must stash: `git stash push -u -m "<unique-tag>"`, record its SHA from `git stash list --format='%H %gs'`, restore with `git stash apply <sha>` (not pop), then drop the entry by re-finding it by tag.

No `git push --force` or `--force-with-lease` to `main`, and no `git reset --hard` on a lane branch. Both are denied on the auto-mode seats, and hard rule 7 covers force-push.

---

## If you worked in the wrong place

Stop. Do not reset or clean anything. Check `git status` and `git log origin/main..HEAD`, then ask the PM how to recover.

---

## Server Restart (if stuck)

```bash
# Find what's on port 8001
lsof -i :8001

# Kill by PID (column 2 of lsof output)
kill <PID>

# Verify port is free
lsof -i :8001  # Should return nothing

# Start fresh, from a Claude Code shell: strip the inherited Anthropic variables or every LLM call fails
export JWT_SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(32))')   # main.py refuses to start without it
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
  POSTGRES_PORT=5433 nohup venv/bin/python main.py > /tmp/piper-server.log 2>&1 &

# Verify
lsof -i :8001  # Should show new PID
```

Note: use the port-based `kill <PID>` above. `pkill` is denied on the auto-mode seats, and `pkill -f "python main.py"` can miss a process whose name differs. The same start command is in CLAUDE.md "Quick reference".
