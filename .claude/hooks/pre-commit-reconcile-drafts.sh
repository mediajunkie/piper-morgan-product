#!/usr/bin/env bash
# pre-commit-reconcile-drafts.sh — PreToolUse hook for `git commit*`
#
# Layer C: orphan-prevention check. When a commit touches docs/public/comms/drafts/
# (a new or modified draft file), runs reconcile-drafts-calendar.py to detect
# draft<->calendar drift before it compounds.
#
# Three failure modes caught:
#   1. TRUE ORPHANS    — .md files in drafts/ with no calendar row (lost drafts)
#   2. MISSING DRAFTPATH — scheduled rows with empty draftPath (broken file<->row link)
#   3. STALE DRAFTPATH  — rows whose draftPath file is gone (renamed without updating)
#
# Warn-first behavior (Comms go-signal 2026-06-13, docs/read/layer-c-go-signal-comms):
#   Exit 0 = clean or drafts/ not touched in this commit
#   Exit 2 = drift found (warning shown to agent; commit NOT hard-blocked)
#
# Promote to exit 1 (hard-block) when signal-to-noise confirms it's reliable.
# Pattern-074: Visibility Loss After Premature Retirement.

REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    exit 0
fi
cd "$REPO_ROOT" || exit 0

# Only fire if this commit touches docs/public/comms/drafts/
DRAFTS_TOUCHED=$(git diff --cached --name-only 2>/dev/null | grep -E '^docs/public/comms/drafts/' | head -1)
if [ -z "$DRAFTS_TOUCHED" ]; then
    exit 0
fi

# Run the reconcile script (warn-only mode: capture output, don't block on its exit code)
RECONCILE_OUTPUT=$(python3 scripts/reconcile-drafts-calendar.py 2>&1)
RECONCILE_EXIT=$?

if [ "$RECONCILE_EXIT" = "0" ]; then
    # Clean — print the success line for visibility and pass
    echo "$RECONCILE_OUTPUT" >&2
    exit 0
fi

if [ "$RECONCILE_EXIT" = "2" ]; then
    # Script error (calendar/drafts dir missing) — pass silently, don't block
    exit 0
fi

# Exit 1 from reconcile script = drift found
{
    echo "⚠️  LAYER-C DRAFTS RECONCILIATION WARNING (PreCommit)"
    echo ""
    echo "This commit touches docs/public/comms/drafts/ and the reconcile check"
    echo "found draft<->calendar drift. Details:"
    echo ""
    echo "$RECONCILE_OUTPUT"
    echo ""
    echo "To fix before committing:"
    echo "  TRUE ORPHANS: add a calendar row referencing the draft (draftPath column)"
    echo "  MISSING DRAFTPATH: fill the draftPath column on the calendar row"
    echo "  STALE DRAFTPATH: update the draftPath to match the file's current path"
    echo ""
    echo "Commit is NOT hard-blocked (warn-first mode). Proceed if drift is intentional"
    echo "or you'll fix the calendar in a follow-up commit. Promote to hard-block after"
    echo "signal-to-noise confirms reliability (update check-branch.sh / exit code here)."
    echo ""
    echo "Script: scripts/reconcile-drafts-calendar.py"
} >&2

# exit 0 = warn-only (message reaches the agent, commit proceeds).
# exit 2 would BLOCK the commit — which contradicted the warn-first message
# above and made every drafts commit fail. Fixed 2026-07-26.
# To promote this check to hard-block later, change this to `exit 2` AND
# update the message above to say the commit is blocked.
exit 0
