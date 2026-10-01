#!/usr/bin/env bash
# pre-commit-ruff-warn.sh — git-native pre-commit WARNING for ruff drift in staged .py (exit 0 always)
#
# 2026-10-01 (CIO, on Docs's datum + Lead's widening): the ruff advisory lived in
# .claude/hooks/post-commit.sh §2, but the post-commit shim has been DISARMED since the 09-21
# runaway (`.git/hooks/post-commit.DISARMED-2026-09-21-runaway`, re-arm pending a joint decision
# with Pard). So it never fired for any seat, before or after the widening. This runs from the
# ARMED common-dir pre-commit instead (canonical source: scripts/git-hooks/pre-commit), the same
# home as the broad-staging warning (#1798):
#   - it reads only, never commits, so it can't recurse (the 09-21 failure shape);
#   - its stderr lands in `git commit`'s own output, so the agent sees it;
#   - it checks the STAGED blob (via stdin), not the working-tree file, so it judges what is being
#     committed;
#   - the binary is the CI-pinned ruff from scripts/ensure-ruff.sh, created once per host.
# Still advisory (Lead 10-01: watch a week of real firing before considering a blocking push gate).
REPO_ROOT=$(git rev-parse --show-toplevel 2>/dev/null) || exit 0
cd "$REPO_ROOT" || exit 0
# Mid-merge: the staged set is other people's already-pushed work. Not ours to warn about here.
git rev-parse -q --verify MERGE_HEAD >/dev/null 2>&1 && exit 0
PY="$(git diff --cached --name-only --diff-filter=ACMR -- '*.py' 2>/dev/null)"
[ -n "$PY" ] || exit 0
RUFF="$(bash "$REPO_ROOT/scripts/ensure-ruff.sh" 2>/dev/null)"
if [ -z "$RUFF" ]; then
  echo "pre-commit(ruff, advisory): pinned ruff unavailable (scripts/ensure-ruff.sh failed), so $(printf '%s\n' "$PY" | grep -c .) staged .py file(s) are UNCHECKED" >&2
  exit 0
fi
BAD=""
while IFS= read -r f; do
  [ -n "$f" ] || continue
  # Exit codes, never output text: ruff prints "already formatted" / "All checks passed!" on success.
  git show ":$f" | "$RUFF" format --check --stdin-filename "$f" - >/dev/null 2>&1 || BAD="$BAD  $f (format)\n"
  git show ":$f" | "$RUFF" check --stdin-filename "$f" - >/dev/null 2>&1 || BAD="$BAD  $f (lint)\n"
done <<EOF_PY
$PY
EOF_PY
if [ -n "$BAD" ]; then
  {
    echo "⚠️  pre-commit(ruff, advisory, not blocking): drift in staged .py. main's Code Quality WILL go red if pushed as-is:"
    printf "$BAD"
    echo "  Fix: $RUFF format <file> && $RUFF check --fix <file>, re-stage, and amend before pushing."
  } >&2
fi
exit 0
