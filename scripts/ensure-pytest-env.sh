#!/usr/bin/env bash
# ensure-pytest-env.sh — print the path to the shared pytest interpreter pinned to CI's Python
# minor and requirements.txt, shared across every worktree on the host.
#
# Shape is Pard's (mailboxes/lead/read/reply-pard-to-lead-cio-item5-shared-env-and-the-one-line-
# that-must-not-be-copied-2026-10-04.md), extending CIO's scripts/ensure-ruff.sh pattern.
#
# ONE DELIBERATE DIFFERENCE FROM ensure-ruff.sh: this VERIFIES, it does not build by default.
# ensure-ruff.sh builds on first use behind a 30x1s wait, correct for one wheel (~10-20s). This
# env is 219 pinned packages and minutes of install; a hook blocking behind that wait would fall
# through to the give-up path, and the give-up path is "pushing UNCHECKED" — a gate that fails
# open while its own environment is still installing is worse than one that says "not
# provisioned yet". So: provisioning is Pard's (via --build, below, or by hand), verification is
# this script's, and the caller (scripts/git-hooks/pre-push) decides how loudly to say so on a
# miss.
#
# Env key = sha256(requirements.txt)[0:12] — NOT requirements.lock. Pard's correction
# (same memo): test.yml runs `pip install -r requirements.txt` and caches on
# hashFiles('**/requirements.txt'); requirements.lock is ~5 months stale and ResolutionImpossible
# (pins fastapi==0.104.1 against anyio==4.12.1/httpx==0.28.1 elsewhere) — nothing installs it, so
# keying on it would never invalidate when CI's actual deps change.
#
# The aiosqlite finding (mailboxes/lead/read/finding-pard-to-lead-cio-spec-ci-skips-47-files-for-
# an-undeclared-aiosqlite-2026-10-04.md): this env deliberately reproduces CI's requirements.txt
# faithfully, including its gaps. When requirements.txt gains aiosqlite, the hash changes, the
# key changes, and the old env is simply superseded — that's the invalidation a per-seat venv
# doesn't give you, not a bug in this script.
#
# PY_MINOR is read from .github/workflows/test.yml's `python-version: "3.11"` line when that
# parses to a clean "3.<digits>" value; else it falls back to the hardcoded pin below, which must
# then be kept in sync with test.yml by hand.
#
# Usage:
#   scripts/ensure-pytest-env.sh            # verify only: print interpreter path + exit 0,
#                                            #   or print NOTHING on stdout + exit 1
#   scripts/ensure-pytest-env.sh --build    # Pard's provisioning step, not the hook's: build if
#                                            #   missing (python${PY_MINOR} -m venv + pip install
#                                            #   -r requirements.txt), then print + exit 0. Ask
#                                            #   Pard before relying on this path — see the memo.
set -u

top="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 1

py_minor_raw="$(grep -m1 -E 'python-version:' "$top/.github/workflows/test.yml" 2>/dev/null \
  | grep -oE '3\.[0-9]+')"
if [ -n "$py_minor_raw" ]; then
  PY_MINOR="$py_minor_raw"
else
  PY_MINOR="3.11"   # fallback pin — test.yml's python-version line didn't parse cleanly; keep
                     # this in sync with .github/workflows/test.yml by hand if it ever triggers.
fi

req="$top/requirements.txt"
[ -f "$req" ] || exit 1
key="$(shasum -a 256 "$req" | cut -c1-12)"

base="${XDG_CACHE_HOME:-$HOME/.cache}/piper-morgan"
env="$base/pytest-py${PY_MINOR}-${key}"
py="$env/bin/python"

if [ "${1:-}" = "--build" ]; then
  if [ -x "$py" ]; then echo "$py"; exit 0; fi
  interp="$(command -v "python${PY_MINOR}" 2>/dev/null)"
  [ -n "$interp" ] || interp="/opt/homebrew/bin/python${PY_MINOR}"
  if [ ! -x "$interp" ] && ! command -v "$interp" >/dev/null 2>&1; then
    echo "ensure-pytest-env --build: no python${PY_MINOR} found on PATH or at /opt/homebrew/bin. Ask Pard." >&2
    exit 1
  fi
  mkdir -p "$base" 2>/dev/null || exit 1
  echo "ensure-pytest-env: building $env from $req (one-time, per host/key)..." >&2
  "$interp" -m venv "$env" >/dev/null 2>&1 && "$env/bin/pip" install -q -r "$req" >/dev/null 2>&1
  if [ ! -x "$py" ]; then
    echo "ensure-pytest-env --build: install failed — env not usable. Ask Pard." >&2
    exit 1
  fi
  echo "$py"
  exit 0
fi

# Default: VERIFY, DON'T BUILD. On a miss, print nothing to stdout and exit 1 — the caller
# decides how loudly to report it.
if [ -x "$py" ]; then
  echo "$py"
  exit 0
fi
exit 1
