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
# Severity tiering (HOST May 10 refinement after 2 incidents in 1 day):
#   HARD     — unpushed commits or commits ahead of main; work not reachable
#              from origin and may be invisible to other agents (load-bearing
#              first-incident catch).
#   SOFT     — only uncommitted changes (no unpushed/ahead), AND those changes
#              are SUBSTANTIVE (not mechanical-only). Files persist through
#              compaction on local disk; risk is rediscovery cost / invisibility
#              to next session, not loss.
#   QUIET    — only uncommitted changes, AND those changes are MECHANICAL-ONLY
#              (MANIFEST regen, .DS_Store, redis runtime noise). No warning.
#
# "Mechanical-only" classifier: every line of `git status --porcelain` must
# match a known-noise pattern (mailbox MANIFEST.md / .DS_Store / data/redis).
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
PORCELAIN=$(git status --porcelain 2>/dev/null)
UNCOMMITTED_COUNT=$(printf '%s\n' "$PORCELAIN" | grep -c '.' || true)
# Edge case: empty porcelain → grep returns 0 lines but exits 1 under set -e (not set here, defensive anyway).
[ -z "$PORCELAIN" ] && UNCOMMITTED_COUNT=0

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

# Classify uncommitted changes as mechanical-only or substantive.
# Mechanical: mailbox MANIFEST.md regen / .DS_Store / data/redis runtime.
# Substantive: anything else (session logs, mail content, code, docs).
#
# Strategy: strip the porcelain status prefix (cols 1-3) to get paths;
# count paths that DON'T match any mechanical pattern. If zero, mechanical-only.
SUBSTANTIVE_PATHS=""
SUBSTANTIVE_COUNT=0
if [ "$UNCOMMITTED_COUNT" -gt 0 ]; then
    # Use `git status --porcelain -z` to handle paths with spaces / specials.
    # Then filter to substantive paths only. Keep this list to surface in the warning.
    SUBSTANTIVE_PATHS=$(git status --porcelain 2>/dev/null \
        | sed -e 's|^...||' -e 's| -> |\n|' \
        | grep -v '^mailboxes/.*/MANIFEST\.md$' \
        | grep -v '^mailboxes/.*/inbox/MANIFEST\.md$' \
        | grep -v '^mailboxes/.*/read/MANIFEST\.md$' \
        | grep -v '^mailboxes/.*/sent/MANIFEST\.md$' \
        | grep -v '^mailboxes/.*\.DS_Store$' \
        | grep -v '^\.DS_Store$' \
        | grep -v '^data/redis/' \
        | grep -v '^$' \
        || true)
    if [ -n "$SUBSTANTIVE_PATHS" ]; then
        SUBSTANTIVE_COUNT=$(printf '%s\n' "$SUBSTANTIVE_PATHS" | grep -c '.' || true)
    fi
fi

# Determine tier.
TIER="QUIET"
if [ "$UNPUSHED_COUNT" -gt 0 ] || [ "$AHEAD_OF_MAIN_COUNT" -gt 0 ]; then
    TIER="HARD"
elif [ "$SUBSTANTIVE_COUNT" -gt 0 ]; then
    TIER="SOFT"
fi

# QUIET tier: only mechanical noise; log silently and exit clean.
TIMESTAMP=$(date -u '+%Y-%m-%dT%H:%M:%SZ')
LOG_DIR="$REPO_ROOT/dev/active"
LOG_FILE="$LOG_DIR/session-end-warnings.log"
mkdir -p "$LOG_DIR" 2>/dev/null

if [ "$TIER" = "QUIET" ]; then
    {
        echo "[$TIMESTAMP] event=PreCompact tier=QUIET branch=$CURRENT_BRANCH uncommitted=$UNCOMMITTED_COUNT (mechanical-only) unpushed=0 ahead_of_main=0 cwd=$REPO_ROOT"
    } >> "$LOG_FILE" 2>/dev/null
    exit 0
fi

# HARD or SOFT: emit warning + log.
if [ "$TIER" = "HARD" ]; then
    >&2 cat <<EOF

⚠️  SIGN-OFF DISCIPLINE WARNING (PreCompact) — HARD TIER

Context is about to be compacted. You have work not yet on origin/main:

Current branch: $CURRENT_BRANCH

  - Uncommitted changes:    $UNCOMMITTED_COUNT (substantive: $SUBSTANTIVE_COUNT)
  - Unpushed commits:       $UNPUSHED_COUNT
  - Commits ahead of main:  $AHEAD_OF_MAIN_COUNT

Unpushed / ahead-of-main work is invisible to other agents and at risk
if your local repo is wiped or your session is on an ephemeral machine.
Compaction proceeds either way, but resume context may not surface this.

Per docs/internal/operations/branch-worktree-mailbox-discipline.md (Rule 2):
either merge to main now, or file a NOTICE memo on main explaining why
work is held on this branch.

Pick one:
  (a) merge your branch to main now (preferred for completed work)
  (b) leave a NOTICE memo to PM/Lead Dev/Docs in mailboxes/{role}/inbox/
  (c) ask PM directly via in-conversation chat for guidance

This warning has been logged to dev/active/session-end-warnings.log
for the Docs merge-keeper sweep.

EOF
else
    # SOFT tier
    >&2 cat <<EOF

ℹ️  SIGN-OFF REMINDER (PreCompact) — SOFT TIER

Context is about to be compacted. You have uncommitted substantive
changes ($SUBSTANTIVE_COUNT files) but nothing ahead of origin/main.

Current branch: $CURRENT_BRANCH

  - Substantive uncommitted: $SUBSTANTIVE_COUNT (of $UNCOMMITTED_COUNT total)
  - Unpushed commits:        0
  - Commits ahead of main:   0

These files persist through compaction on local disk — they are NOT at
risk of loss. The risk is rediscovery cost: your next session may not
know these files matter.

Substantive paths:
$(printf '  - %s\n' $SUBSTANTIVE_PATHS | head -10)

Pick one:
  (a) commit + push these changes now (clearest signal to next session)
  (b) note them in your session log so resume context knows they exist
  (c) accept rediscovery cost and proceed with /compact

This reminder has been logged to dev/active/session-end-warnings.log
for the Docs merge-keeper sweep.

EOF
fi

# Append to the warnings log for Docs sweep. Tail-friendly format.
{
    echo "[$TIMESTAMP] event=PreCompact tier=$TIER branch=$CURRENT_BRANCH uncommitted=$UNCOMMITTED_COUNT substantive=$SUBSTANTIVE_COUNT unpushed=$UNPUSHED_COUNT ahead_of_main=$AHEAD_OF_MAIN_COUNT cwd=$REPO_ROOT"
} >> "$LOG_FILE" 2>/dev/null

# Exit 0 — surface the warning text but never block compaction. Earlier
# exit 2 was wedging agents at compaction limit on Claude Code versions
# that treat exit 2 as a hard block. The May 10–17 wedge incidents
# (PPM, Lead Dev, CXO, CIO) forced this change. Warning role preserved;
# blocking role removed.
exit 0
