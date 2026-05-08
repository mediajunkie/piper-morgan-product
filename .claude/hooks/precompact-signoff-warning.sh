#!/usr/bin/env bash
# precompact-signoff-warning.sh — PreCompact hook for sign-off discipline.
#
# Fires before context compaction. Warns the agent if their work is at risk
# of being stranded: uncommitted changes, unpushed commits, or commits not
# yet reachable from origin/main. Compaction proceeds either way (warn-only;
# PreCompact cannot block), but the warning is loud and the failure is
# logged to dev/active/session-end-warnings.log for the Docs sweep.
#
# Per Docs Apr 29 go-ahead: warn-only is the surface; sign-off discipline
# + merge-keeper sweep stay load-bearing. The hook is a third layer of
# defense — make the failure VISIBLE at the moment context is about to
# be lost.
#
# Exit 2 (stderr surfaces); never blocks (PreCompact cannot block anyway).

# Resolve repo root; if we're not in a git working tree, exit silently.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    exit 0
fi
cd "$REPO_ROOT" || exit 0

CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)
if [ -z "$CURRENT_BRANCH" ]; then
    # Detached HEAD or no branch — skip; not enough signal to warn meaningfully.
    exit 0
fi

# 1. Uncommitted changes (modified, staged, or untracked tracked-paths).
UNCOMMITTED_COUNT=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')

# 2. Unpushed commits (commits on local branch not in upstream).
#    Only meaningful if branch has an upstream.
UNPUSHED_COUNT=0
if git rev-parse --abbrev-ref --symbolic-full-name '@{u}' >/dev/null 2>&1; then
    UNPUSHED_COUNT=$(git log --oneline '@{u}..HEAD' 2>/dev/null | wc -l | tr -d ' ')
fi

# 3. Commits ahead of origin/main (work not yet reachable from trunk).
#    Skip the fetch — too slow for a hook; rely on whatever was last fetched.
AHEAD_OF_MAIN_COUNT=0
if git rev-parse --verify origin/main >/dev/null 2>&1; then
    AHEAD_OF_MAIN_COUNT=$(git log --oneline 'origin/main..HEAD' 2>/dev/null | wc -l | tr -d ' ')
fi

# If everything is clean and reachable from origin/main, no warning.
if [ "$UNCOMMITTED_COUNT" = "0" ] && [ "$UNPUSHED_COUNT" = "0" ] && [ "$AHEAD_OF_MAIN_COUNT" = "0" ]; then
    exit 0
fi

# Otherwise: warn loudly + log.
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')

>&2 cat <<EOF

⚠️  SIGN-OFF DISCIPLINE WARNING (PreCompact)

Context is about to be compacted. Your session may resume with stale
context post-compaction; work that isn't durable on origin/main may
become invisible to future sessions.

Current branch: $CURRENT_BRANCH

  - Uncommitted changes:    $UNCOMMITTED_COUNT
  - Unpushed commits:       $UNPUSHED_COUNT
  - Commits ahead of main:  $AHEAD_OF_MAIN_COUNT

Per docs/internal/operations/branch-worktree-mailbox-discipline.md (Rule 2):
either merge to main now, or file a NOTICE memo on main explaining why
work is held on this branch.

Three "pick one" options:
  (a) merge your branch to main now (preferred for completed work)
  (b) leave a NOTICE memo to PM/Lead Dev/Docs in mailboxes/{role}/inbox/
  (c) ask PM directly via in-conversation chat for guidance

This warning has been logged to dev/active/session-end-warnings.log
for the Docs merge-keeper sweep.

EOF

# Append to the warnings log for Docs sweep. Tail-friendly format.
LOG_DIR="$REPO_ROOT/dev/active"
LOG_FILE="$LOG_DIR/session-end-warnings.log"
mkdir -p "$LOG_DIR" 2>/dev/null
{
    echo "[$TIMESTAMP] event=PreCompact branch=$CURRENT_BRANCH uncommitted=$UNCOMMITTED_COUNT unpushed=$UNPUSHED_COUNT ahead_of_main=$AHEAD_OF_MAIN_COUNT cwd=$REPO_ROOT"
} >> "$LOG_FILE" 2>/dev/null

# Exit 2 surfaces stderr to the agent. Cannot block PreCompact regardless.
exit 2
