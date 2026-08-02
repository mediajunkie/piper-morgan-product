#!/usr/bin/env bash
# check-derived-drift.sh — does each DERIVED artifact still match its generator?
#
# THE FAILURE THIS CATCHES
# -----------------------
# A derived artifact gets hand-edited. The edit looks fine, is committed, and is
# silently reverted by the next regeneration. Nothing errors. The person who made
# the change believes it holds; everyone downstream believes the artifact is
# authoritative. Both are wrong, and neither finds out.
#
# Real instance (2026-07-30): Comms hand-compacted MEMORY.md's header and reclaimed
# 6 lines of a budget that was 7 lines from a silent-truncation ceiling. Correct call,
# real win — and NOT DURABLE, because the generator still emitted the long header.
# It was found by accident, mid-rebuild, one turn before the rebuild would have erased
# the evidence. "I edited the artifact" and "I changed what gets produced" look
# identical afterward and differ completely on the next build.
#
# Second instance, same week, different shape: a PREDICATE is a derived artifact too.
# Five DAY-CLOSED patterns were hand-written across three roles against an imagined
# format; each was blind to the next real form along. The corpus was the authority the
# whole time. (CXO's framing — "a predicate can be regenerated from the corpus it is
# meant to match, and diffed.")
#
# WHY EACH GENERATOR NEEDS A --check MODE, AND WHY THAT'S THE HARD PART
# --------------------------------------------------------------------
# A plain rebuild REPAIRS the drift it would have detected. Run it to find out whether
# the artifact matches and you have destroyed the evidence; the answer is always
# "it matches now." A detector that fixes what it measures cannot report. So a
# generator is only registerable here once it can RENDER WITHOUT WRITING.
#
# Exit 0 = every registered artifact matches. Exit 1 = drift found.
# Coverage is printed either way — see the note at the bottom of the output.
#
# HOST, 2026-07-31. Supports methodology m-46 (promotion is a re-verification event),
# whose filing was held pending a mechanism rather than prose. This is that mechanism.

set -uo pipefail
cd "$(dirname "$0")/.." || exit 1

# ── REGISTRY ────────────────────────────────────────────────────────────────────
# One line per artifact: "label|check command (must render+compare, never write)"
CHECKS=(
  "MEMORY.md (shared memory index)|python3 scripts/rebuild-memory-index.py --check"
  "day-closed-marker-census.md (predicate corpus)|python3 scripts/day-closed-census.py --check"
)

# ── NOT YET REGISTERED — printed every run, deliberately. ───────────────────────
# A drift-check that silently covers one artifact while reading as a clean bill of
# health is the same failure as a green probe that only exercises the mitigated path.
# Report coverage, not just results.
UNREGISTERED=(
  "docs/briefing/BRIEFING-CURRENT-STATE.md — hand-maintained; not derived. Listed so nobody assumes staleness here is covered; that is the >7-day SessionStart warning's job, a different mechanism."
)

fail=0
echo "── derived-artifact drift check ─────────────────────────────────────────────"
for entry in "${CHECKS[@]}"; do
  label="${entry%%|*}"
  cmd="${entry#*|}"
  echo
  echo "▸ ${label}"
  if out="$(eval "$cmd" 2>&1)"; then
    echo "${out}" | sed 's/^/  /'
  else
    echo "${out}" | sed 's/^/  /'
    fail=1
  fi
done

echo
echo "── coverage ─────────────────────────────────────────────────────────────────"
echo "checked: ${#CHECKS[@]} artifact(s).  NOT checked: ${#UNREGISTERED[@]}."
for u in "${UNREGISTERED[@]}"; do
  echo "  ✗ ${u}"
done
echo
if [ "$fail" = "0" ]; then
  echo "✓ No drift among REGISTERED artifacts. This is not a statement about the unregistered ones."
else
  echo "⚠️  Drift found. A hand-edit to a build output is not durable — fold it into the"
  echo "   generator, or re-run the generator without --check to discard it. Decide which;"
  echo "   do not leave it, because the next rebuild decides for you and says nothing."
fi
exit "$fail"
