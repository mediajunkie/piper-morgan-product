#!/usr/bin/env bash
# issue-checkbox-lint.sh — PostToolUse hook for Bash (post-commit)
#
# When a commit message references an issue via "Closes #N" / "Fixes #N" /
# "Resolves #N", GitHub auto-closes the issue when the commit lands on the
# default branch (via PR merge or direct push to main). But the issue body
# checkboxes don't get updated automatically. Agents have repeatedly closed
# issues via this path while leaving [ ] checkboxes in the description —
# memory entry `feedback_close_issue_properly_skill_recurring_miss.md`
# tracks this as a recurring failure; 13 closures May 7-13 missed it.
#
# This hook scans the most-recent commit's message for close-magic-strings
# and warns if any referenced issue body still has unchecked checkboxes.
#
# Trigger: PostToolUse on Bash. Exits early if HEAD didn't move (commit
# didn't happen) OR the commit message doesn't reference issues to close.
#
# Exit 2 = warn (stderr); never blocks. The commit already happened; the
# warning gives the agent a chance to update the issue body BEFORE pushing.
#
# Filed #1083 TOOL-ISSUE-CHECKBOX-LINT; closes the loop on Pattern-046
# (Completion Discipline) variant at the issue-tracker layer.

set -uo pipefail

# Resolve repo root; bail silently if not in a git tree.
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null)
if [ -z "$REPO_ROOT" ]; then
    exit 0
fi
cd "$REPO_ROOT" || exit 0

# Was the most recent reflog entry a commit?
# `git reflog -1 --format=%gs` returns something like "commit: foo" or
# "checkout: moving from main to claude/branch" or "pull: Fast-forward".
# We only want to fire if the last operation was a commit on HEAD.
LAST_REF=$(git reflog -1 --format='%gs' 2>/dev/null || echo "")
case "$LAST_REF" in
    commit:*|commit\ \(initial\):*|commit\ \(merge\):*|commit\ \(amend\):*)
        # Commit just landed; proceed.
        ;;
    *)
        # Not a commit; bail.
        exit 0
        ;;
esac

# Get the most recent commit message.
MSG=$(git log -1 --pretty=%B 2>/dev/null || echo "")
if [ -z "$MSG" ]; then
    exit 0
fi

# Scan for Closes/Resolves/Fixes #N (case-insensitive, word-boundary).
# GitHub's official close-magic-strings list:
#   close, closes, closed, fix, fixes, fixed, resolve, resolves, resolved
ISSUE_NUMS=$(printf "%s" "$MSG" \
    | grep -oEi '\b(close[sd]?|fix(e[sd])?|resolve[sd]?)[[:space:]]+#[0-9]+' \
    | grep -oE '#[0-9]+' \
    | grep -oE '[0-9]+' \
    | sort -u)

if [ -z "$ISSUE_NUMS" ]; then
    exit 0
fi

# Find gh CLI; bail silently if unavailable (don't fail builds on dev machines
# without gh installed — the lint is opportunistic, not a hard gate).
GH=$(command -v gh 2>/dev/null || command -v /opt/homebrew/bin/gh 2>/dev/null || echo "")
if [ -z "$GH" ]; then
    exit 0
fi

# For each referenced issue, fetch body + count unchecked checkboxes.
# Issue #1098 fix: honor the annotation pattern documented in the close-
# issue-properly skill. A `[ ]` row carrying `*N/A:*` / `*N/A (...)*` /
# `*Deferred:*` / `*Deferred ...*` annotation is INTENTIONALLY unchecked
# (the item is dealt with, just not via [x]). Exclude annotated rows from
# the count so the hook doesn't false-positive on properly-dispositioned
# items.
WARNINGS=""
TOTAL_UNCHECKED=0
for n in $ISSUE_NUMS; do
    # Issue 1618 fix: only warn on OPEN issues. A close-keyword next to a
    # closed issue's number can't auto-close anything, so the warning's
    # premise ("update the body before this push closes it") doesn't hold —
    # and in practice such matches are often not issue references at all
    # (checklist item numbers, PR numbers). The real 1618 incident matched
    # "Resolved #5" (an internal checklist item) against closed issue 5.
    BODY=$("$GH" issue view "$n" --json body,state \
        --jq 'if .state == "OPEN" then .body else "" end' 2>/dev/null || echo "")
    if [ -z "$BODY" ]; then
        # Issue doesn't exist, isn't open, or gh failed — skip silently
        continue
    fi
    # Count lines matching unchecked checkbox pattern, EXCLUDING lines that
    # carry an N/A or Deferred annotation marker. The skill format is
    # `[ ] Item - *N/A: reason*` or `[ ] Item - *Deferred: where*`.
    UNCHECKED=$(printf "%s" "$BODY" \
        | grep -E '^[[:space:]]*[-*][[:space:]]+\[[[:space:]]\]' 2>/dev/null \
        | grep -vEi '\*[[:space:]]*(N/?A|Deferred|Skipped|Won.?t[[:space:]]*do)\b' 2>/dev/null \
        | wc -l \
        | tr -d ' ')
    UNCHECKED=${UNCHECKED:-0}
    if [ "$UNCHECKED" -gt 0 ]; then
        WARNINGS+=$'\n'"  #$n — $UNCHECKED unchecked checkbox(es) still in description body"
        TOTAL_UNCHECKED=$((TOTAL_UNCHECKED + UNCHECKED))
    fi
done

if [ "$TOTAL_UNCHECKED" -eq 0 ]; then
    # All referenced issues either have no checkboxes or are fully checked.
    exit 0
fi

# Warn to stderr; exit 2 surfaces to agent.
cat >&2 <<EOF
⚠️  issue-checkbox-lint (#1083): commit references issue(s) with unchecked
checkboxes in their description bodies:
${WARNINGS}

(Note: this lint pattern-matches "closes/fixes/resolves #N" loosely — if the
number wasn't meant as a GitHub issue reference, verify relevance and ignore.)

The close-issue-properly skill requires description-first updates: each
[ ] should become [x] OR carry an explicit annotation (e.g.,
"*N/A: <reason>*" or "*Deferred: <where>*"). Comment-only close leaves
the [ ] in the body forever and looks incomplete to future readers.

Before pushing this commit, consider updating the issue body(ies):
  gh issue view <N> --json body --jq '.body' > /tmp/issue-N-body.md
  # Edit /tmp/issue-N-body.md: mark [x] or annotate unchecked
  gh issue edit <N> --body-file /tmp/issue-N-body.md

Then add the closing comment + push. The skill at
.claude/skills/close-issue-properly/SKILL.md has the full procedure.
EOF
exit 2
