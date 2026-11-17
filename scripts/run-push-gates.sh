#!/usr/bin/env bash
# run-push-gates.sh — run, locally, the CI gates that the tests and the pre-push smoke
# do NOT run, before pushing code.
#
# Why (Lead, 2026-11-12): two red windows on main in one morning came from pushes whose
# tests and smoke passed. The first was the env credential-read gate in the Code Quality
# workflow; the second was the mypy ratchet in Architecture Enforcement. Neither is a
# pytest test, so neither runs in `pytest` or in the pre-push smoke.
#
# What it runs:
#   1. ruff, as the lint workflow does (`ruff format --check .` and `ruff check .`), with
#      the pinned binary from scripts/ensure-ruff.sh (CIO 2026-11-12: ruff turned main red
#      on 11-11 and the `python scripts/...` lines below don't include it);
#   2. every `python scripts/...` gate command in .github/workflows/lint.yml, read from
#      that file at run time, so a gate added there is run here without editing this;
#   3. the mypy gate (scripts/check_mypy_gate.py) in its own environment, which
#      scripts/bootstrap-mypy-gate-venv.sh builds on first use. The dev venv gives a
#      different count, so it is never used for this.
#
# Usage:  scripts/run-push-gates.sh            # all gates
#         scripts/run-push-gates.sh --no-mypy  # skip the mypy gate
#         scripts/run-push-gates.sh --hook     # as the pre-push hook runs it: never
#                                              # BUILDS the mypy environment (a network
#                                              # pip install at push time); if it isn't
#                                              # there, mypy is reported UNCHECKED and the
#                                              # run goes on
#         scripts/run-push-gates.sh --logs-and-mail
#                                              # only the three lints that read dated
#                                              # session logs and mail (the mailbox bearer
#                                              # lint, which reads file contents, and the
#                                              # mailbox and Windows filename lints). The
#                                              # pre-push hook runs this on a remembered
#                                              # pass (Lead's condition, 2026-11-16): those
#                                              # paths are outside the pass's key.
# Exit 0 only when every gate that ran passed. It changes nothing.
#
# Layer: the same commands CI runs, on your working tree. It does not run the tests,
# the architecture tests or the smoke; run those as well. The pre-push hook runs the fast
# architecture tests and the completion ratchets through scripts/run-push-arch-tests.sh.
#
# Concept: docs/internal/operations/github-and-tooling-gotchas.md
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT" || exit 2
PY="$ROOT/venv/bin/python"
[ -x "$PY" ] || PY="python3"
RUN_MYPY=1
BUILD_MYPY=1
RUN_RUFF=1
# The architecture check (scripts/run-push-arch-tests.sh). By hand it runs when the work not yet on
# origin/main touches templates/, web/ or services/, so "I ran the gates by hand" means all
# fifteen (Arch, Lead, 2026-11-17). Under --hook the hook runs it itself, with its own remembered
# pass, so it is off here. --arch forces it; --no-arch leaves it out.
RUN_ARCH=auto
# Which workflow gate commands to run. --logs-and-mail narrows it to the three lints by name.
GATE_FILTER='.'
LOGS_AND_MAIL_RE='scripts/(mailbox_bearer_lint|mailbox_filename_lint|windows_filename_lint)\.py'
for arg in "$@"; do
  case "$arg" in
    --no-mypy) RUN_MYPY=0 ;;
    --hook) BUILD_MYPY=0; RUN_ARCH=0 ;;
    --logs-and-mail) RUN_MYPY=0; RUN_RUFF=0; RUN_ARCH=0; GATE_FILTER="$LOGS_AND_MAIL_RE" ;;
    --arch) RUN_ARCH=1 ;;
    --no-arch) RUN_ARCH=0 ;;
  esac
done

failed=0
ran=0
unchecked=0

# --- ruff, pinned to CI's version ---
RUFF="$(scripts/ensure-ruff.sh 2>/dev/null || true)"
if [ "$RUN_RUFF" -eq 0 ]; then
  :
elif [ -n "$RUFF" ] && [ -x "$RUFF" ]; then
  for ruff_cmd in "format --check ." "check ."; do
    ran=$((ran + 1))
    # shellcheck disable=SC2086
    if "$RUFF" $ruff_cmd >/tmp/run-push-gates.$$.out 2>&1; then
      echo "PASS  ruff $ruff_cmd"
    else
      echo "FAIL  ruff $ruff_cmd"
      tail -12 /tmp/run-push-gates.$$.out | sed 's/^/      /'
      failed=$((failed + 1))
    fi
  done
else
  echo "UNCHECKED  ruff: no pinned binary (scripts/ensure-ruff.sh printed nothing)"
  unchecked=$((unchecked + 1))
fi
while IFS= read -r line; do
  cmd="${line#"${line%%[![:space:]]*}"}"   # strip leading whitespace
  cmd="${cmd#python }"
  ran=$((ran + 1))
  # shellcheck disable=SC2086  # the workflow line is a command with arguments
  if "$PY" $cmd >/tmp/run-push-gates.$$.out 2>&1; then
    echo "PASS  $cmd"
  else
    echo "FAIL  $cmd"
    tail -12 /tmp/run-push-gates.$$.out | sed 's/^/      /'
    failed=$((failed + 1))
  fi
done < <(grep -E '^[[:space:]]+python scripts/[A-Za-z0-9_./-]+\.py' .github/workflows/lint.yml | grep -E "$GATE_FILTER")
rm -f /tmp/run-push-gates.$$.out

if [ "$ran" -eq 0 ]; then
  echo "FAIL  no gate commands found in .github/workflows/lint.yml (this script needs updating)"
  failed=$((failed + 1))
fi
# The narrowed run must find all three by name. A renamed lint would otherwise pass as "0 failed".
if [ "$GATE_FILTER" != "." ] && [ "$ran" -ne 3 ]; then
  echo "FAIL  --logs-and-mail expected 3 lints in .github/workflows/lint.yml and found $ran"
  failed=$((failed + 1))
fi

if [ "$RUN_MYPY" -eq 1 ]; then
  if [ ! -x "$ROOT/venv-mypy-gate/bin/python" ] && [ "$BUILD_MYPY" -eq 1 ]; then
    echo "----  building the mypy gate environment (first use)"
    scripts/bootstrap-mypy-gate-venv.sh >/dev/null 2>&1 || true
  fi
  if [ ! -x "$ROOT/venv-mypy-gate/bin/python" ] && [ "$BUILD_MYPY" -eq 0 ]; then
    echo "UNCHECKED  mypy gate: environment not built (run scripts/bootstrap-mypy-gate-venv.sh once in this worktree)"
    unchecked=$((unchecked + 1))
  elif [ -x "$ROOT/venv-mypy-gate/bin/python" ]; then
    ran=$((ran + 1))
    if out="$("$ROOT/venv-mypy-gate/bin/python" scripts/check_mypy_gate.py 2>&1)"; then
      echo "PASS  mypy gate"
    else
      echo "FAIL  mypy gate"
      echo "$out" | tail -8 | sed 's/^/      /'
      failed=$((failed + 1))
    fi
  else
    echo "FAIL  mypy gate environment could not be built (scripts/bootstrap-mypy-gate-venv.sh)"
    failed=$((failed + 1))
  fi
fi

if [ "$RUN_ARCH" = "auto" ]; then
  RUN_ARCH=0
  if { git diff --name-only origin/main 2>/dev/null; git ls-files --others --exclude-standard 2>/dev/null; } \
      | grep -qE '^(templates/|web/|services/)'; then
    RUN_ARCH=1
  fi
fi
if [ "$RUN_ARCH" = "1" ]; then
  arch_out="$(scripts/run-push-arch-tests.sh 2>&1)"; arch_rc=$?
  arch_line="$(printf '%s\n' "$arch_out" | grep -E '^run-push-arch-tests:' | tail -1)"
  if [ $arch_rc -eq 0 ]; then
    ran=$((ran + 1)); echo "PASS  architecture check (${arch_line#run-push-arch-tests: })"
  elif [ $arch_rc -eq 3 ]; then
    echo "UNCHECKED  architecture check: ${arch_line#run-push-arch-tests: }"; unchecked=$((unchecked + 1))
  else
    ran=$((ran + 1)); failed=$((failed + 1)); echo "FAIL  architecture check"
    printf '%s\n' "$arch_out" | tail -12 | sed 's/^/      /'
  fi
fi

echo "run-push-gates: $ran gates, $((ran - failed)) passed, $failed failed, $unchecked unchecked"
[ "$failed" -eq 0 ]
