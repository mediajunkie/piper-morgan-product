#!/usr/bin/env bash
# Layer C of the editorial-pipeline orphan-prevention framework (warn-first).
#
# Runs scripts/reconcile-drafts-calendar.py to flag drafts<->calendar drift
# (true-orphan drafts with no calendar row; calendar rows with missing/stale
# draftPath). WARN-ONLY by default: it prints any drift but DOES NOT block the
# commit. Promote to blocking by exporting BLOCK=1 once the warn period is clean.
#
# Docs-endorsed warn-first-then-promote (2026-05-29 process-tightening proposal;
# 2026-05-31 Layer-C precondition landed in draft-blog-post; this is the
# git-hook promotion of the same check). Comms-owned.
#
# Pre-commit runs hooks from the repo root, so the script's repo-relative paths
# resolve correctly here.
set -uo pipefail

BLOCK="${BLOCK:-0}"

out="$(python3 scripts/reconcile-drafts-calendar.py 2>&1)"
code=$?

if [ "$code" -ne 0 ]; then
  echo "⚠️  Editorial-calendar / drafts drift detected (Layer C):"
  echo "$out" | sed 's/^/    /'
  if [ "$BLOCK" = "1" ]; then
    echo "    (BLOCK=1) Failing the commit — resolve the drift first."
    exit 1
  fi
  echo "    (warn-only — commit allowed.) Fix with: python3 scripts/reconcile-drafts-calendar.py"
  echo "    then the /update-calendar skill. Set BLOCK=1 to make this blocking."
fi

exit 0
