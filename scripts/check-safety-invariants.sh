#!/usr/bin/env bash
# check-safety-invariants.sh — assert the environment facts our safety rules SILENTLY depend on.
#
# WHAT THIS IS FOR, AND WHY IT ISN'T THE DRIFT CHECK
# --------------------------------------------------
# `check-derived-drift.sh` asks "does this artifact still match its generator?"
# This asks a different question: **"is the thing that makes a documented rule
# safe still true?"** Several of our rules are safe only because of an ambient
# environment fact that nothing asserts and nobody owns. A perfectly reasonable
# change — often by a human, for a good reason — can silently remove the property
# the rule was resting on, and no error appears anywhere.
#
# THE INSTANCE THAT PROMPTED IT (HOST, 2026-08-01)
# Something runs `git pull -q --rebase` against PM's main checkout on a six-hourly
# cadence. That checkout is where PM edits prose WITHOUT committing — the reason
# CLAUDE.md carries a HARD RULE about it, after PM lost voice-pass edits twice on
# 2026-06-21. Checked at the time: the rebase pull is SAFE, because with
# `rebase.autoStash` unset a rebase against a dirty tree REFUSES rather than
# stashing. **That refusal is the entire safety property, and nothing guards it.**
# `git config --global rebase.autoStash true` is a normal human convenience that
# would convert the refusal into a silent stash of PM's uncommitted work.
#
# READ-ONLY BY CONSTRUCTION. This script never writes, never sets config, never
# touches a working tree. It reports.
#
# Exit 0 = every asserted invariant holds. Exit 1 = at least one does not.
# Coverage is printed either way — a checker that quietly covers three things
# while reading as a clean bill of health is the failure it exists to prevent.
#
# HOST, 2026-08-02.

set -uo pipefail

# Overridable ONLY so the checker itself can be tested against a scratch repo.
# A checker nobody has watched FAIL is a checker nobody has tested — and this one
# guards a data-loss path, so "it passed" is not evidence it works.
MAIN_CHECKOUT="${PM_MAIN_CHECKOUT:-/Users/xian/Development/piper-morgan-product}"
WORKTREE_ROOT="${PM_WORKTREE_ROOT:-/Users/xian/Development/piper-morgan-worktrees}"

fail=0
note() { printf '  %s\n' "$1"; }

echo "── safety invariants ────────────────────────────────────────────────────────"

# ── 1. rebase.autoStash must NOT be true anywhere that applies to PM's checkout ──
echo
echo "▸ [HOST-SCOPED] rebase.autoStash is not enabled (protects PM's uncommitted prose)"
as_local=$(git -C "$MAIN_CHECKOUT" config --local --get rebase.autoStash 2>/dev/null || true)
as_global=$(git config --global --get rebase.autoStash 2>/dev/null || true)
as_eff=$(git -C "$MAIN_CHECKOUT" config --get rebase.autoStash 2>/dev/null || true)
if [ "${as_eff:-}" = "true" ]; then
  note "🔴 VIOLATED — effective value is 'true' (local='${as_local:-unset}' global='${as_global:-unset}')."
  note "   A rebase pull against PM's dirty checkout will now SILENTLY STASH their"
  note "   uncommitted prose instead of refusing. That is the 2026-06-21 data-loss shape."
  note "   Fix: git config --global --unset rebase.autoStash   (and/or --local)"
  fail=1
else
  note "✓ effective: '${as_eff:-unset}' (local='${as_local:-unset}' global='${as_global:-unset}') — a rebase against a dirty tree REFUSES."
fi

# ── 2. PM's main checkout is actually on main ───────────────────────────────────
echo
echo "▸ [HOST-SCOPED] PM's main checkout is on branch 'main'"
if [ -d "$MAIN_CHECKOUT/.git" ] || [ -f "$MAIN_CHECKOUT/.git" ]; then
  br=$(git -C "$MAIN_CHECKOUT" branch --show-current 2>/dev/null)
  if [ "$br" = "main" ]; then
    note "✓ on 'main'"
  else
    note "🔴 VIOLATED — on '${br:-<detached>}'. Agents assume this checkout tracks main;"
    note "   sync-pm-local.sh and every 'is my work reachable' assumption rest on it."
    fail=1
  fi
else
  note "⚠️  $MAIN_CHECKOUT is not a git checkout — THIS CHECK DID NOT RUN."
  fail=1
fi

# ── 3. Every agent worktree tracks origin/main ──────────────────────────────────
# Drifted upstreams broke the MANDATORY sign-off checklist on 2 of 11 seats
# (2026-08-01): `@{u}..HEAD` read 6741 against origin/main..HEAD = 0, and a step
# that cries wolf every session is a step people learn to skip.
echo
echo "▸ [REPO-SCOPED: ${WORKTREE_ROOT}] Every agent worktree tracks origin/main"
bad=0; seen=0
for d in "$WORKTREE_ROOT"/*/; do
  r=$(basename "$d")
  case "$r" in _*) continue;; esac
  [ -e "$d/.git" ] || continue
  seen=$((seen+1))
  u=$(git -C "$d" rev-parse --abbrev-ref '@{u}' 2>/dev/null || echo NONE)
  if [ "$u" != "origin/main" ]; then
    n=$(git -C "$d" log --oneline '@{u}..HEAD' 2>/dev/null | wc -l | tr -d ' ')
    note "🔴 $r tracks '$u' (@{u}..HEAD=$n) — fix: git -C $d branch -u origin/main"
    bad=$((bad+1)); fail=1
  fi
done
[ "$bad" = "0" ] && note "✓ all $seen agent worktrees track origin/main"

# ── coverage ────────────────────────────────────────────────────────────────────
echo
echo "── coverage ─────────────────────────────────────────────────────────────────"
echo "asserted: 3 invariants — 2 HOST-scoped, 1 REPO-scoped."
note "⚠️ The two HOST-scoped invariants read IDENTICALLY whatever PM_WORKTREE_ROOT points at —"
note "  they are facts about this machine and PM's checkout, not about the repo you passed."
note "  Only the third line tells you anything repo-specific. (Web, 2026-08-02, who spotted that"
note "  the output could otherwise be read as having checked all three FOR another repo.)"
echo "NOT asserted (known gaps):"
note "✓ piper-morgan-website — CLOSED 2026-08-02 by Web (its owner): both worktrees track"
note "  origin/main. Verified by running this checker, not assumed."
note "✗ designinproduct, openlaws — same idiom, different owners, nobody with access has run it."
note "  PA's 2026-08-01 census found local 'main' lagging 10–15 in the dinp worktrees."
note "✗ Whether the six-hourly rebase-pull process itself is intended — evidence only;"
note "  Pard/CIO's to name. This script asserts the property that makes it safe, not the cause."
note "✗ Anything about the CONTENT of PM's uncommitted work. This checks that git would"
note "  refuse to touch it, not that it is intact."
echo
if [ "$fail" = "0" ]; then
  echo "✓ All ASSERTED invariants hold. This is not a statement about the gaps above."
else
  echo "⚠️  An invariant a documented safety rule depends on is no longer true."
  echo "   These fail SILENTLY by design — nothing else in the system would have told you."
fi
exit "$fail"
