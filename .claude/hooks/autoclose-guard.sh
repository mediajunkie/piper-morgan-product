#!/usr/bin/env bash
# autoclose-guard.sh — PreToolUse on `git commit*` (#1691, #1845).
#
# GitHub closes issue N when a commit message pushed to main carries a close-keyword
# (close/fix/resolve + forms) within a few tokens of `#N`, whatever the wording around it.
# This hands the Bash tool's JSON input to scripts/check_autoclose_keywords.py
# --bash-tool-input, which extracts ONLY the `-m` commit-message arguments (a heredoc
# elsewhere in the command that mentions an incident subject is not a commit message) and
# refuses when a message would close an issue — unless the trailer `Auto-Close: intentional`
# is present. mail-send.sh runs the same checker on its own commit-tree path.
#
# #1845 (added 2026-10-04): the same checker ALSO refuses a commit message carrying a
# bearer-credential shape (invite token / API key) — the thing mailbox_bearer_lint.py misses
# because it only reads FILES, never the message itself. A real invite token sat in a commit
# SUBJECT on main (`7941ae4b97`). The `Auto-Close: intentional` trailer waives the auto-close
# concern only; it does not waive a bearer-credential hit.
#
# Advisory-strength like every PreToolUse hook here; the checker is the mechanism, this is
# its git-commit doorway.
set -u
repo=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
[ -f "$repo/scripts/check_autoclose_keywords.py" ] || exit 0
# #1934: the block reason MUST land on STDERR. A PreToolUse hook that exits
# 2 only surfaces its STDERR to the model/committer — the harness shows
# "No stderr output" and swallows stdout entirely when this wrote there
# instead, so the credential-rotate / reword advice never reached anyone.
# Verified behaviorally (HOST, 2026-10-04): byte-counted stdout vs stderr on
# a real blocked run. Everything below goes to >&2 for exactly that reason.
err=$(mktemp "${TMPDIR:-/tmp}/autoclose-guard.XXXXXX")
if ! python3 "$repo/scripts/check_autoclose_keywords.py" --bash-tool-input 2>"$err"; then
    echo "BLOCKED by the commit-message guard (#1691 auto-close and/or #1845 bearer-credential):" >&2
    sed 's/^/  /' "$err" >&2
    rm -f "$err"
    exit 2
fi
rm -f "$err"
exit 0
