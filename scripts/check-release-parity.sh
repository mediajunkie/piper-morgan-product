#!/usr/bin/env bash
# check-release-parity.sh — #1413 content-parity gate at cut time.
#
# THE INCIDENT (2026-07-16): a "full-parity" release claim aged 48 minutes;
# main kept moving during a fix-and-deploy evening, a later deploy from the
# release branch silently dropped a live login fix, and beta login regressed
# for a two-day latent window. A parity CLAIM is a statement about a moment;
# this script makes it a statement about NOW, verified.
#
# Usage: scripts/check-release-parity.sh [release-ref]   (default: origin/production)
# Exit 0: content-identical across product paths, or every diff line is
#         explained in RELEASE_EXCLUSIONS (stdin prompt refused in CI — the
#         explanation file is the mechanism, not an interactive shrug).
# Exit 1: unexplained content gap — the release may not ship.
set -euo pipefail

REF="${1:-origin/production}"
PATHS=(services/ web/ templates/ alembic/ static/ requirements.txt fly.toml Dockerfile)
EXCLUSIONS_FILE="${RELEASE_EXCLUSIONS_FILE:-release-exclusions.txt}"

git fetch origin main -q
DIFF=$(git diff --name-only "$REF" origin/main -- "${PATHS[@]}" || true)

if [ -z "$DIFF" ]; then
  echo "PARITY OK: $REF is content-identical to origin/main across product paths."
  exit 0
fi

echo "CONTENT GAP between $REF and origin/main:"
echo "$DIFF" | sed 's/^/  /'

if [ -f "$EXCLUSIONS_FILE" ]; then
  UNEXPLAINED=""
  while IFS= read -r f; do
    grep -qF "$f" "$EXCLUSIONS_FILE" || UNEXPLAINED="$UNEXPLAINED$f\n"
  done <<< "$DIFF"
  if [ -z "$UNEXPLAINED" ]; then
    echo "PARITY OK-WITH-EXCLUSIONS: every gap line is named in $EXCLUSIONS_FILE."
    echo "Release notes MUST carry these exclusions verbatim (#1413)."
    exit 0
  fi
  echo "UNEXPLAINED lines (not in $EXCLUSIONS_FILE):"; printf "$UNEXPLAINED" | sed 's/^/  /'
fi

echo ""
echo "REFUSING (#1413): a parity claim with silent gaps is how the 7/16 login"
echo "regression shipped. Either fast-forward $REF, or name every excluded"
echo "path with a reason in $EXCLUSIONS_FILE and carry it into the release notes."
exit 1
