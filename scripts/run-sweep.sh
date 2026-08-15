#!/usr/bin/env bash
# run-sweep.sh — the canonical test invocations, so nobody hand-assembles the
# env-strip + addopts dance again (360 item 6.3, 2026-08-15).
#
# Usage:
#   scripts/run-sweep.sh smoke        # the CI gating subset (default addopts)
#   scripts/run-sweep.sh unit [PATH]  # -m "not llm" unit run, importlib kept
#   scripts/run-sweep.sh full         # full composition sweep, no early-stop,
#                                     # judged output -> pipe to check_fullsuite_backlog.py
#   scripts/run-sweep.sh ratchets     # completion ratchets + architecture enforcement
set -u
STRIP=(env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS)
PG=POSTGRES_PORT=${POSTGRES_PORT:-5433}
PY=venv/bin/python
MODE=${1:-smoke}; shift || true
case "$MODE" in
  smoke)
    exec "${STRIP[@]}" "$PG" "$PY" -m pytest tests/ -m smoke -q -p no:cacheprovider "$@";;
  unit)
    TARGET=${1:-tests/unit}; shift || true
    exec "${STRIP[@]}" "$PG" "$PY" -m pytest "$TARGET" -m "not llm" -q \
      -o addopts="--tb=line --import-mode=importlib" -p no:cacheprovider "$@";;
  full)
    # keeps every default ignore, drops -x/--maxfail so the backlog judge sees
    # the whole picture; ALWAYS judge with scripts/check_fullsuite_backlog.py
    exec "${STRIP[@]}" "$PG" "$PY" -m pytest tests/ -m "not llm" -q --ignore=tests/frontend \
      -o addopts="--ignore=tests/archive --ignore=services/integrations/*/tests --ignore=services/mcp/server/test_*.py --ignore=dev/ --tb=no --import-mode=importlib" "$@";;
  ratchets)
    exec "${STRIP[@]}" "$PG" "$PY" -m pytest tests/test_completion_ratchets.py tests/test_architecture_enforcement.py -q \
      -o addopts="--import-mode=importlib" -p no:cacheprovider "$@";;
  *) echo "unknown mode: $MODE (smoke|unit|full|ratchets)" >&2; exit 2;;
esac
