#!/usr/bin/env bash
# run-push-arch-tests.sh — the fifteenth push check: the fast architecture tests and the
# completion ratchets, run before a push that touches templates/, web/ or services/.
#
# Why (Lead, 2026-11-17): a push that added a local `escapeHtml` to a template passed all 14
# push gates and the smoke, and turned main red for 47 minutes, because nothing at push ran
# tests/test_architecture_enforcement.py. Ruled by Arch the same day (mail 01M7NA9QHN).
#
# What it runs, with the shared pytest env:
#   tests/test_architecture_enforcement.py  WITHOUT the two slow classes named below
#   tests/test_completion_ratchets.py       whole
# Measured 2026-11-17 on Amber: 136 passed in 32 s, and 10 passed in 12 s.
#
# What it does NOT run, so nobody reads it as covering more: TestUnarmedAskSiteRatchet and
# TestChatPointersReachabilityRatchet (about 70 s between them). They stay in CI only. Arch's
# condition: the first time either one is the cause of a red main, it joins this check for
# pushes that touch services/, without another ruling. And this check does not make a narrow
# local run a validation: before calling a served-path change validated, run both files whole.
#
# It reads tracked code, templates and tests; nothing under dev/20NN/ or mailboxes/. So the
# pre-push hook may skip it on a remembered pass (Arch's rule: a check is skipped on a hit only
# if everything it reads is in the key).
#
# Usage: scripts/run-push-arch-tests.sh        (by hand, or from scripts/git-hooks/pre-push)
# Exit 0 passed, 1 a test failed, 3 the pytest env is not provisioned (nothing was checked).
# Last line is always `run-push-arch-tests: <summary>`.
#
# Concept: docs/internal/operations/github-and-tooling-gotchas.md
set -uo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 3
SLOW="not TestUnarmedAskSiteRatchet and not TestChatPointersReachabilityRatchet"
py="$("$ROOT/scripts/ensure-pytest-env.sh" 2>/dev/null)"
if [ -z "$py" ] || [ ! -x "$py" ]; then
  echo "run-push-arch-tests: UNCHECKED, pytest env not provisioned (scripts/ensure-pytest-env.sh --build, or ask Pard)"
  exit 3
fi
out="$(PYTHONPATH=. "$py" -m pytest tests/test_architecture_enforcement.py tests/test_completion_ratchets.py \
  -q --tb=line -p no:cacheprovider -o addopts="--import-mode=importlib" -k "$SLOW" 2>&1)"
rc=$?
summary="$(printf '%s\n' "$out" | grep -E '[0-9]+ (passed|failed|error)' | tail -1)"
if [ $rc -ne 0 ]; then
  printf '%s\n' "$out" | grep -E '^(FAILED|ERROR) '
  echo "run-push-arch-tests: FAILED (${summary:-no summary; pytest exit $rc})"
  exit 1
fi
echo "run-push-arch-tests: passed (${summary})"
