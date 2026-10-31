#!/usr/bin/env bash
# Pre-move reference check (issue #1719, candidate 2): before you git mv or git rm files, find every
# tracked file that still points at them. Prints each live reference and exits 1 if there are any,
# so the move waits until the references are updated (or you accept the breakage on purpose).
#
# Usage: scripts/check-move-refs.sh PATH [PATH...]      (paths as they exist now, repo-relative)
#
# A reference is a literal occurrence of the full repo path. Historical records are not live
# references and are skipped: dated session logs (dev/YYYY/), omnibus logs, mailboxes, and the
# files being moved themselves. Basename-only mentions are listed separately as "possible".
set -u
cd "$(git rev-parse --show-toplevel)" || exit 2
[ "$#" -ge 1 ] || { echo "usage: $0 PATH [PATH...]" >&2; exit 2; }

SKIP='^(dev/[0-9]{4}/|docs/omnibus-logs/|mailboxes/)'
found=0
for p in "$@"; do
  p="${p#./}"
  base="$(basename "$p")"
  hits="$(git grep -n -I -F -- "$p" 2>/dev/null | grep -v -E "$SKIP" | grep -v -F -- "$p:" || true)"
  # drop lines from any of the moved files themselves
  for q in "$@"; do hits="$(printf '%s\n' "$hits" | grep -v -F -- "${q#./}:" || true)"; done
  hits="$(printf '%s\n' "$hits" | sed '/^$/d')"
  if [ -n "$hits" ]; then
    found=1
    echo "LIVE reference(s) to $p:"
    printf '%s\n' "$hits" | sed 's/^/  /' | cut -c1-200
  fi
  maybe="$(git grep -n -I -F -- "$base" -- '*.md' '*.sh' '*.py' '*.yml' 2>/dev/null | grep -v -E "$SKIP" | grep -v -F -- "$p" || true)"
  for q in "$@"; do maybe="$(printf '%s\n' "$maybe" | grep -v -F -- "${q#./}:" || true)"; done
  maybe="$(printf '%s\n' "$maybe" | sed '/^$/d' | head -5)"
  if [ -n "$maybe" ]; then
    echo "possible (basename only) for $p, first 5:"
    printf '%s\n' "$maybe" | sed 's/^/  /' | cut -c1-200
  fi
done
if [ "$found" -eq 0 ]; then echo "check-move-refs: no live references to the $# path(s)"; exit 0; fi
echo "check-move-refs: update the references above before moving, or move anyway on purpose." >&2
exit 1
