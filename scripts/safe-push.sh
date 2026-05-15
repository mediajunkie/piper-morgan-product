#!/usr/bin/env bash
# safe-push.sh — git push with auto-retry on conflict (D-layer companion to
# the pre-commit-broad-staging-warn hook). Issue 12j (PM-directive operational
# deliverable per CIO May 15 disposition).
#
# Problem this solves: when multiple agents commit to main concurrently,
# `git push` rejects with non-fast-forward. The standard recovery is
# fetch + rebase + push — a 3-step dance that's easy to skip or
# get wrong, especially with intervening hooks.
#
# This wrapper does the dance correctly + retries up to 3 times. On
# rebase conflict it bails out (manual resolution required); on push
# success it exits cleanly.
#
# Usage:
#   ./scripts/safe-push.sh                  # pushes current branch to origin
#   ./scripts/safe-push.sh origin main      # explicit remote + branch
#
# Exit codes:
#   0 = pushed cleanly (may have rebased first)
#   1 = rebase conflict; manual resolution required
#   2 = unrelated failure (no remote, no upstream, etc.)
#   3 = 3 retries exhausted without push success

set -uo pipefail

REMOTE="${1:-origin}"
BRANCH="${2:-$(git branch --show-current 2>/dev/null)}"

if [ -z "$BRANCH" ]; then
    echo "safe-push: cannot determine current branch (detached HEAD?)" >&2
    exit 2
fi

MAX_RETRIES=3
ATTEMPT=0

while [ "$ATTEMPT" -lt "$MAX_RETRIES" ]; do
    ATTEMPT=$((ATTEMPT + 1))

    # Attempt the push.
    PUSH_OUTPUT=$(git push "$REMOTE" "$BRANCH" 2>&1)
    PUSH_RC=$?

    if [ "$PUSH_RC" -eq 0 ]; then
        # Success.
        echo "$PUSH_OUTPUT"
        echo "safe-push: pushed cleanly on attempt $ATTEMPT."
        exit 0
    fi

    # Detect non-fast-forward (the retry-able case).
    if echo "$PUSH_OUTPUT" | grep -qE "(non-fast-forward|fetch first|tip of your current branch is behind)"; then
        echo "safe-push: attempt $ATTEMPT rejected (non-fast-forward); fetching + rebasing..." >&2
    else
        # Some other failure — auth, network, unknown ref, etc. Surface and exit.
        echo "$PUSH_OUTPUT" >&2
        echo "safe-push: push failed (unrelated to fast-forward); not retrying." >&2
        exit 2
    fi

    # Check for uncommitted changes; if present, stash to allow rebase.
    STASH_NEEDED=0
    if [ -n "$(git status --porcelain 2>/dev/null)" ]; then
        STASH_NEEDED=1
        git stash push -u -m "safe-push retry $ATTEMPT" >/dev/null
    fi

    # Fetch + rebase.
    git fetch "$REMOTE" "$BRANCH" >/dev/null 2>&1
    if ! git pull --rebase "$REMOTE" "$BRANCH" >/dev/null 2>&1; then
        # Rebase conflict — bail out for manual resolution.
        echo "safe-push: rebase conflict on attempt $ATTEMPT; manual resolution required." >&2
        echo "safe-push: run 'git status' to inspect; resolve + 'git rebase --continue'; then retry." >&2
        if [ "$STASH_NEEDED" = "1" ]; then
            echo "safe-push: NOTE — your uncommitted changes are in 'stash@{0}' (msg: 'safe-push retry $ATTEMPT')." >&2
        fi
        exit 1
    fi

    # Pop the stash if we created one.
    if [ "$STASH_NEEDED" = "1" ]; then
        if ! git stash pop >/dev/null 2>&1; then
            echo "safe-push: stash pop encountered conflicts after rebase; check 'git status'." >&2
            # Continue trying to push anyway — the rebase already succeeded.
        fi
    fi

    # Loop to retry the push.
done

echo "safe-push: exhausted $MAX_RETRIES retries without success." >&2
exit 3
