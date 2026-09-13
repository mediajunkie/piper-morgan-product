#!/usr/bin/env bash
# run-sweep.sh — the canonical test invocations, so nobody hand-assembles the
# env-strip + addopts dance again (360 item 6.3, 2026-08-15).
#
# Usage:
#   scripts/run-sweep.sh smoke        # the CI gating subset (default addopts)
#   scripts/run-sweep.sh unit [PATH]  # -m "not llm" unit run, importlib kept
#   scripts/run-sweep.sh full         # full composition sweep, no early-stop,
#                                     # judged output -> pipe to check_fullsuite_backlog.py
#   scripts/run-sweep.sh ratchets     # completion ratchets + architecture
#                                     # enforcement + the #1436 mypy gate.
#                                     # Needs venv-mypy-gate/ — build it once with
#                                     # scripts/bootstrap-mypy-gate-venv.sh
set -u
STRIP=(env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS)
PG=POSTGRES_PORT=${POSTGRES_PORT:-5433}
PY=venv/bin/python
# The #1436 mypy gate is measured in its OWN pinned venv, never the dev venv —
# see the long note in the `ratchets` case below for why that is load-bearing.
GATE_PY=venv-mypy-gate/bin/python
MODE=${1:-smoke}; shift || true
case "$MODE" in
  smoke)
    exec "${STRIP[@]}" "$PG" "$PY" -m pytest tests/ -m smoke -q -p no:cacheprovider "$@";;
  unit)
    # Accept MULTIPLE path targets (leading non-option args). The single-TARGET
    # version silently ran NOTHING when handed "path1 path2" as one word —
    # pytest saw a nonexistent space-joined path ("no tests ran in 0.00s"),
    # which reads like a pass at a glance. Word-split a single space-joined
    # arg deliberately; real paths here never contain spaces.
    TARGETS=()
    while [ $# -gt 0 ] && [ "${1#-}" = "$1" ]; do
      for w in $1; do TARGETS+=("$w"); done
      shift
    done
    [ ${#TARGETS[@]} -eq 0 ] && TARGETS=(tests/unit)
    for t in "${TARGETS[@]}"; do
      [ -e "$t" ] || { echo "run-sweep unit: target '$t' does not exist — refusing a silent no-op run" >&2; exit 2; }
    done
    exec "${STRIP[@]}" "$PG" "$PY" -m pytest "${TARGETS[@]}" -m "not llm" -q \
      -o addopts="--tb=line --import-mode=importlib" -p no:cacheprovider "$@";;
  full)
    # keeps every default ignore, drops -x/--maxfail so the backlog judge sees
    # the whole picture; ALWAYS judge with scripts/check_fullsuite_backlog.py
    exec "${STRIP[@]}" "$PG" "$PY" -m pytest tests/ -m "not llm" -q --ignore=tests/frontend \
      -o addopts="--ignore=tests/archive --ignore=services/integrations/*/tests --ignore=services/mcp/server/test_*.py --ignore=dev/ --tb=no --import-mode=importlib" "$@";;
  ratchets)
    # ⚠️ The mypy gate runs here TOO, and that is the whole point of this block.
    # Before 2026-09-13 this mode ran only the two pytest ratchet files, and
    # Architecture Enforcement's mypy step (scripts/check_mypy_gate.py) was a
    # SEPARATE CI step nothing local covered. Result: "ratchets 58 passed" was
    # reported honestly on ten consecutive pushes while the gate was red,
    # because the sentence was true about a denominator that silently excluded
    # the failing gate. Cost: ~2 min. Pay it.
    "${STRIP[@]}" "$PG" "$PY" -m pytest tests/test_completion_ratchets.py tests/test_architecture_enforcement.py -q \
      -o addopts="--import-mode=importlib" -p no:cacheprovider "$@" || exit 1
    # ⚠️ And it runs under $GATE_PY, NOT $PY. This is not a style preference.
    # mypy-gate.ini sets ignore_missing_imports=True, so an import mypy cannot
    # resolve becomes Any and suppresses that module's downstream errors —
    # meaning a venv with MORE packages reports MORE errors. Measured at one
    # commit on 2026-09-13: dev venv/ 1428 errors, CI's pinned venv 1353. The
    # first run of this block used $PY and produced a nine-code "new drift"
    # report (index 63 vs ceiling 44, union-attr 181 vs 156, operator 83 vs 73)
    # that CI never emitted, that no commit in the blame window could explain,
    # and that no code fix could have cleared. CI's real complaint was two
    # codes in the SHRINK direction. Refuse to guess: if the CI-faithful venv
    # is absent, say so and exit non-zero rather than print a number that
    # looks like an answer.
    echo "--- mypy per-code gate (#1436) ---"
    if [ ! -x "$GATE_PY" ]; then
      echo "run-sweep ratchets: $GATE_PY missing — the mypy gate DID NOT RUN." >&2
      echo "  Build it:  scripts/bootstrap-mypy-gate-venv.sh" >&2
      echo "  Do NOT substitute venv/bin/python: it over-reports by ~75 errors" >&2
      echo "  across ~9 codes and none of them are real." >&2
      exit 1
    fi
    exec "${STRIP[@]}" "$PG" "$GATE_PY" scripts/check_mypy_gate.py;;
  *) echo "unknown mode: $MODE (smoke|unit|full|ratchets)" >&2; exit 2;;
esac
