#!/usr/bin/env bash
# verify-signoff.sh v1.0 (CIO 2026-08-15)
#
# WHY THIS EXISTS
# CLAUDE.md's mandatory sign-off checklist is three git commands, run at the end of nearly every
# fire across all 11 duty-cycle roles. It has already been wrong three separate ways on three
# separate seats (HOST 2026-08-01, corrected by HOST again same day after PA's fleet census; the
# full incident is documented in CLAUDE.md's "Sign-Off Discipline" section):
#   1. WRONG REF   — `@{u}..HEAD` measured against a role-branch upstream instead of origin/main,
#                     reading thousands of "unpushed" commits that were already on main.
#   2. STALE REF   — `main..HEAD` measured against a LOCAL main that lags behind origin/main in a
#                     worktree, misreporting on seats where local main hadn't been fetched recently.
#   3. UNRESOLVED REF — `origin/main..HEAD` on a worktree where that ref doesn't resolve at all exits
#                     128 with EMPTY stdout under `2>/dev/null` — reads as a clean pass while having
#                     measured nothing (this is m-44's shape: a "clear" that never ran).
# Three ways for a hand-typed checklist to lie, and all three read as PASS to someone who didn't
# know to watch for the specific failure. This script is the fixed sequence, so nobody re-derives
# (and re-breaks) it by hand at 22:37.
#
# WHAT IT DOES
# Always measures against `origin/main` explicitly — never a bare upstream (`@{u}`) or local `main`.
# Fails LOUD (explicit STOP, nonzero exit) rather than silently printing nothing if the ref can't be
# resolved. Never uses `2>/dev/null` on the check that matters.
#
# USAGE
#   scripts/verify-signoff.sh              # run all three checks, human-readable
#   scripts/verify-signoff.sh --quiet       # same checks, only prints on failure (exit code only on pass)
#
# EXIT CODES
#   0 = clean (working tree clean, origin/main resolves, nothing unpushed)
#   1 = not clean (uncommitted changes and/or unpushed commits — details printed)
#   2 = origin/main does not resolve — the unpushed-check DID NOT RUN; this is not a pass

set -u

QUIET=0
if [[ "${1:-}" == "--quiet" ]]; then
  QUIET=1
fi

say() {
  if [[ "$QUIET" -eq 0 ]]; then
    echo "$@"
  fi
}

fail() {
  echo "$@" >&2
}

FAIL=0

# --- Step 1: working tree clean? ---
DIRTY="$(git status --porcelain)"
if [[ -n "$DIRTY" ]]; then
  fail "verify-signoff: WORKING TREE NOT CLEAN"
  fail "$DIRTY"
  FAIL=1
else
  say "verify-signoff: working tree clean"
fi

# --- Step 2: does origin/main resolve? (the guard the old checklist was missing) ---
if ! git rev-parse --verify -q origin/main >/dev/null; then
  fail "verify-signoff: STOP — origin/main does not resolve on this worktree."
  fail "verify-signoff: the unpushed-commits check below DID NOT RUN. Empty output is NOT clean."
  fail "verify-signoff: run 'git fetch origin main' and re-check before signing off."
  exit 2
fi
say "verify-signoff: origin/main resolves"

# --- Step 3: anything unpushed, measured against origin/main explicitly (never @{u}, never local main) ---
UNPUSHED="$(git log --oneline origin/main..HEAD)"
if [[ -n "$UNPUSHED" ]]; then
  fail "verify-signoff: UNPUSHED COMMITS (origin/main..HEAD is not empty):"
  fail "$UNPUSHED"
  FAIL=1
else
  say "verify-signoff: nothing unpushed (origin/main..HEAD empty)"
fi

if [[ "$FAIL" -eq 0 ]]; then
  say "verify-signoff: CLEAN — safe to sign off"
  exit 0
else
  fail "verify-signoff: NOT CLEAN. Per CLAUDE.md's checklist, that's fine IF each item above is an"
  fail "verify-signoff: explicit, intentional carry-over named in your session log — it is not fine"
  fail "verify-signoff: left unexplained. This script shows state; it doesn't judge intent."
  exit 1
fi
