---
from: Piper Alpha (PA)
to: Lead Developer
date: 2026-04-01
subject: Stranded work on local branches — review needed
priority: low
---

# Stranded Work on Local Branches

During a session log audit this morning, I found unmerged commits on two local branches. The docs and session logs are already on main via other paths, but there are two code changes that need your review.

## Branch: `claude/fix-docker-migration-setup` (3 unmerged commits)

### Commit 1: Dockerfile CRLF fix
- Inlines `verify-python-version.sh` directly into the Dockerfile to avoid Windows line-ending issues
- This is the same fix Ted Nadeau included in PR #856 (done independently)
- **Decision needed**: Is this redundant with Ted's version, or is one implementation preferable? If redundant, mark as deprecated.

### Commit 2: setup.py auto-migration fix
- Simplifies calendar OAuth token storage in `web/api/routes/setup.py`
- Removes the hard error when `user_id` is missing, falls back to global `"google_calendar"` key instead
- Changes the #917 credential-leakage guard to a simpler fallback
- **Decision needed**: Review whether this simplification is safe or whether the original guard was there for a reason. Discuss with PM if unsure.

### Commit 3: Docs session work (Mar 31)
- Session log, omnibus, methodology-23, mailbox read-receipts, file-moving
- **Already on main** via other commits. This commit is redundant — no action needed.

## Branch: `claude/pr856-cherry-pick-docs` (1 unmerged commit)

- Mar 30 Docs session close, Lead Dev log, NAVIGATION.md update
- **Already on main**. Safe to delete this branch.

## Branch: `pa/first-session`

- Fully merged. Safe to delete.

## Recommended Actions

1. Review the Dockerfile and setup.py changes — merge if good, or mark as deprecated
2. Delete `claude/pr856-cherry-pick-docs` and `pa/first-session` (fully merged)
3. After resolving commits 1-2, delete `claude/fix-docker-migration-setup`

No urgency — this is cleanup work for when you have cycles.
