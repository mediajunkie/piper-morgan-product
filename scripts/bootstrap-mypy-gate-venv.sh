#!/usr/bin/env bash
# bootstrap-mypy-gate-venv.sh — build the ONE environment the #1436 mypy gate
# may be measured in (2026-09-13).
#
# WHY THIS EXISTS, and why you must not shortcut it with the dev venv:
#
# mypy-gate.ini sets `ignore_missing_imports = True`. That is load-bearing in a
# direction nobody expected: an import mypy CANNOT resolve becomes `Any`, and
# every downstream error in that module disappears. So INSTALLING MORE PACKAGES
# MAKES THE ERROR COUNT GO UP. The dev venv/ has 228 packages; CI installs 15.
# Measured 2026-09-13 at the same commit: dev venv 1428 errors, CI venv 1353 —
# a 75-error gap concentrated in the third-party adapters (notion_adapter +70,
# staging_health +26), files untouched for months.
#
# The cost of learning that the hard way: ten consecutive red pushes were
# investigated against a nine-code "new drift" report (index 63 vs ceiling 44,
# union-attr 181 vs 156, operator 83 vs 73) that CI never emitted and no commit
# could explain. CI's actual complaint was two codes in the SHRINK direction.
# A gate measured in the wrong environment does not read as broken — it reads
# as a codebase problem, and sends you hunting call sites that are fine.
#
# The pins below MUST stay identical to the `pip install` line in
# .github/workflows/architecture-enforcement.yml (job: mypy-signature-drift-gate).
# If you change one, change both, in the same commit.
#
# Usage:  scripts/bootstrap-mypy-gate-venv.sh   (idempotent; ~30s cold)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV="$REPO_ROOT/venv-mypy-gate"
PY_VERSION=3.11 # CI: actions/setup-python with python-version "3.11"
PINS=("mypy==2.3.0" "sqlalchemy==2.0.23" "pydantic==2.12.5" "fastapi==0.115.14")

if ! command -v "python$PY_VERSION" >/dev/null 2>&1; then
  echo "bootstrap-mypy-gate-venv: python$PY_VERSION not on PATH." >&2
  echo "  CI runs the gate on $PY_VERSION; a different minor version is a different" >&2
  echo "  measurement, so this script will not silently substitute one." >&2
  exit 2
fi

if [ ! -x "$VENV/bin/python" ]; then
  echo "--- creating $VENV (python$PY_VERSION)"
  "python$PY_VERSION" -m venv "$VENV"
fi

"$VENV/bin/python" -m pip install --quiet --upgrade pip
"$VENV/bin/python" -m pip install --quiet "${PINS[@]}"

echo "--- resolved toolchain (compare against the CI job's pip freeze):"
"$VENV/bin/python" -VV
"$VENV/bin/python" -m pip freeze
echo "--- ready: $VENV/bin/python scripts/check_mypy_gate.py"
