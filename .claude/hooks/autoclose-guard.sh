#!/usr/bin/env bash
# autoclose-guard.sh — PreToolUse on `git commit*` (#1691).
#
# GitHub closes issue N when a commit message pushed to main carries a close-keyword
# (close/fix/resolve + forms) within a few tokens of `#N`, whatever the wording around it.
# This hands the Bash tool's JSON input to scripts/check_autoclose_keywords.py
# --bash-tool-input, which extracts ONLY the `-m` commit-message arguments (a heredoc
# elsewhere in the command that mentions an incident subject is not a commit message) and
# refuses when a message would close an issue — unless the trailer `Auto-Close: intentional`
# is present. mail-send.sh runs the same checker on its own commit-tree path.
#
# Advisory-strength like every PreToolUse hook here; the checker is the mechanism, this is
# its git-commit doorway.
set -u
repo=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -f "$repo/scripts/check_autoclose_keywords.py" ] || exit 0
err=$(mktemp "${TMPDIR:-/tmp}/autoclose-guard.XXXXXX")
if ! python3 "$repo/scripts/check_autoclose_keywords.py" --bash-tool-input 2>"$err"; then
    echo "BLOCKED by the auto-close guard (#1691): this commit message would CLOSE a GitHub issue on push."
    sed 's/^/  /' "$err"
    rm -f "$err"
    exit 2
fi
rm -f "$err"
exit 0
