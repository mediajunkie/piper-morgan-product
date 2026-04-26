#!/usr/bin/env bash
# check-branch.sh — PreToolUse hook for git commit
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

if [ "$CURRENT_BRANCH" = "main" ]; then
    exit 0
fi

# On a non-main branch. Check if any staged file is in mailboxes/.
STAGED_MAIL=$(git diff --cached --name-only 2>/dev/null | grep -E '^mailboxes/' | head -5)

if [ -n "$STAGED_MAIL" ]; then
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
    echo "  2. Stash or commit non-mail changes on this branch first"
    echo "  3. git checkout main && git pull origin main"
    echo "  4. Re-stage and commit your mail changes on main"
    echo "  5. git push origin main"
    echo "  6. git checkout $CURRENT_BRANCH"
    echo ""
    echo "If you genuinely need to bypass (e.g., committing a mail-shaped artifact"
    echo "that isn't real mail), commit with --no-verify and document why."
    exit 2
fi

# Non-mail commit on a feature branch — warn but allow.
echo "Note: committing on '$CURRENT_BRANCH' (not main). That's fine for code work."
echo "Reminder: merge to main and push before signing off, or your work is invisible."
exit 0
