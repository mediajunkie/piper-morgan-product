#!/usr/bin/env bash
# check-branch.sh — PreToolUse hook for git commit
# Concept: docs/internal/operations/hooks-registry.md (index); see the row for this hook.
#
# Enforces branch discipline:
# - Mailbox writes (mailboxes/**) MUST commit to main. Other branches blocked.
# - Other commits on non-main branches are warned but allowed (code work on feature branches is fine).
#
# Rationale: mailboxes/ is cross-agent infrastructure. A mailbox commit on a
# feature branch is invisible to other agents pulling main, which causes mail
# delivery to silently fail. Code work can live on feature branches because it
# merges back to main as a deliberate act; mail cannot tolerate that delay.
#
# Exit 0 = allow (with warning if not on main)
# Exit 2 = block

CURRENT_BRANCH=$(git branch --show-current 2>/dev/null)

if [ -z "$CURRENT_BRANCH" ]; then
    # Not in a git repo or detached HEAD — let it through
    exit 0
fi

# Stamp check on today's session-log headings (xian 2026-10-16 via Exec; warn only, never blocks):
# flags an HH:Mx form or a heading time ahead of the clock. scripts/stamp_check.py has the rules.
TOP=$(git rev-parse --show-toplevel 2>/dev/null)
[ -f "$TOP/scripts/stamp_check.py" ] && (cd "$TOP" && python3 scripts/stamp_check.py --log-staged 2>/dev/null)

# Current-state page gate at the commit (CIO 2026-10-23, after a briefing edit without a last_updated bump
# turned Code Quality red on main for three pushes): when the briefing is staged, run the same check CI runs
# (scripts/check-current-state.py) on the staged copy, and block on a FAIL. CI still enforces it.
BRIEF=docs/briefing/BRIEFING-CURRENT-STATE.md
if [ -f "$TOP/scripts/check-current-state.py" ] && (cd "$TOP" && git diff --cached --name-only | grep -qx "$BRIEF"); then
    TMPB=$(mktemp "${TMPDIR:-/tmp}/brief-staged.XXXXXX")
    (cd "$TOP" && git show ":$BRIEF" > "$TMPB" 2>/dev/null)
    OUT=$(cd "$TOP" && python3 scripts/check-current-state.py "$TMPB" 2>&1)
    RC=$?
    rm -f "$TMPB"
    if [ "$RC" -eq 1 ]; then
        echo "BLOCKED: the staged $BRIEF fails the current-state gate that Code Quality runs on main:" >&2
        echo "$OUT" | sed 's/^/  /' >&2
        echo "Fix it (usually: bump last_updated on line 5 to today), stage it again, then commit." >&2
        exit 2
    fi
fi

if [ "$CURRENT_BRANCH" = "main" ]; then
    exit 0
fi

# On a non-main branch. Check if any staged file is in mailboxes/.
STAGED_MAIL=$(git diff --cached --name-only 2>/dev/null | grep -E '^mailboxes/' | head -5)

if [ -n "$STAGED_MAIL" ]; then
    exec 1>&2   # the refusal goes to stderr, or the harness shows only "No stderr output" (#2251)
    echo "BLOCKED: You are on branch '$CURRENT_BRANCH' and trying to commit mailbox files."
    echo ""
    echo "Files in mailboxes/ are cross-agent infrastructure. They MUST commit to main"
    echo "so other agents pulling origin/main can see them. Mail on a feature branch is"
    echo "invisible to recipients until merged — and 'merged later' has been failing."
    echo ""
    echo "Staged mailbox files:"
    echo "$STAGED_MAIL" | sed 's/^/  - /'
    echo ""
    echo "Fix:"
    echo "  1. Unstage with: git restore --staged mailboxes/"
    echo "  2. Send the mail with: scripts/mail-send.sh \"mail(<role>): <subject>\" <every changed mailbox path>"
    echo "     (it commits straight onto origin/main; no branch switch, no stash, no shared checkout)"
    echo "  3. Commit your non-mail changes on this branch as usual."
    echo ""
    echo "If you genuinely need to bypass (e.g., committing a mail-shaped artifact"
    echo "that isn't real mail), commit with --no-verify and document why."
    exit 2
fi

# Non-mail commit on a feature branch — warn but allow.
echo "Note: committing on '$CURRENT_BRANCH' (not main). That's fine for code work."
echo "Reminder: merge to main and push before signing off, or your work is invisible."
exit 0
