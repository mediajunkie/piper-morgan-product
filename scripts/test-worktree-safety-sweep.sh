#!/usr/bin/env bash
# Regression tests for worktree-safety-sweep.sh (standing-item 7r, 2026-09-06).
#
# Builds a real bare-origin + real-clone fixture with real `git worktree add` worktrees (not mocked
# git output) — the content-vs-ref distinction this script exists to make is exactly the kind of
# thing a hand-rolled mock could get subtly wrong, so these exercise real git plumbing throughout.
set -uo pipefail

SC="$(cd "$(dirname "$0")" && pwd)/worktree-safety-sweep.sh"
PASS=0; FAIL=0; TMPS=()
ok(){ echo "  ✓ $1"; PASS=$((PASS+1)); }
no(){ echo "  ✗ $1"; FAIL=$((FAIL+1)); }
cleanup(){ for d in "${TMPS[@]:-}"; do [ -n "$d" ] && rm -rf "$d"; done; }
trap cleanup EXIT INT TERM

# Fixture: bare origin + a "main repo" clone with one commit on main, plus a WTDIR containing
# worktrees in each of the four states this script must distinguish.
mkfixture(){
  local TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  git init --bare -q "$TMP/o.git"
  git clone -q "$TMP/o.git" "$TMP/main" 2>/dev/null
  ( cd "$TMP/main"
    git config user.email t@t.test; git config user.name tester
    echo "base" > base.txt; git add -A; git commit -qm "base commit"
    git push -q origin HEAD:main 2>/dev/null )
  mkdir -p "$TMP/main/.claude/worktrees"

  # 1. SAFE-TO-REMOVE: a branch whose one commit is content-identical (same diff, via patch-id) to
  #    a commit already on main — simulates "subagent's work was committed to main by the
  #    dispatcher, under a different commit object, worktree abandoned."
  ( cd "$TMP/main"
    git branch wt-safe
    git worktree add -q ".claude/worktrees/wt-safe" wt-safe
    ( cd ".claude/worktrees/wt-safe"
      echo "shipped feature" > shipped.txt; git add -A; git commit -qm "feat: shipped feature" )
    # Land the SAME content change on main directly (main's working tree is still checked out on
    # main; this is a different commit object with identical diff, exactly how a dispatcher's own
    # commit of the same work would look). Targeted `git add shipped.txt`, NOT `-A` — `-A` from
    # here would also stage .claude/worktrees/wt-safe itself as a gitlink (an "embedded git
    # repository"), which changes this commit's diff and breaks the patch-id match this test
    # depends on. Found live: the fixture's own first draft used -A and silently failed T1/T5.
    echo "shipped feature" > shipped.txt; git add shipped.txt; git commit -qm "feat: shipped feature (landed on main)"
    git push -q origin HEAD:main 2>/dev/null )

  # 2. UNMERGED-CONTENT: a branch with a real commit that never reached main (the #1602 shape).
  ( cd "$TMP/main"
    git branch wt-lost
    git worktree add -q ".claude/worktrees/wt-lost" wt-lost
    ( cd ".claude/worktrees/wt-lost"
      echo "never shipped" > lost.txt; git add -A; git commit -qm "fix: never shipped this" ) )

  # 3. DIRTY: uncommitted changes sitting on disk.
  ( cd "$TMP/main"
    git branch wt-dirty
    git worktree add -q ".claude/worktrees/wt-dirty" wt-dirty
    echo "uncommitted" > ".claude/worktrees/wt-dirty/scratch.txt" )

  # 4. A clean worktree with NO extra commits at all (branch == main exactly) — also SAFE-TO-REMOVE,
  #    the trivial case, worth its own assertion since cherry against an identical branch is edge-y.
  ( cd "$TMP/main"
    git branch wt-clean
    git worktree add -q ".claude/worktrees/wt-clean" wt-clean )

  echo "$TMP"
}

echo "worktree-safety-sweep tests:"

TMP=$(mkfixture)
out=$(WORKTREE_SAFETY_REPO="$TMP/main" WORKTREE_SAFETY_UPSTREAM="origin/main" bash "$SC" 2>/tmp/wss-stderr.$$)
err=$(cat /tmp/wss-stderr.$$); rm -f /tmp/wss-stderr.$$

echo "$out" | grep -q "^SAFE-TO-REMOVE .*/wt-safe wt-safe" && ok "T1 content-identical-to-main branch -> SAFE-TO-REMOVE" || no "T1 expected SAFE-TO-REMOVE for wt-safe, got: $out"
echo "$out" | grep -q "^UNMERGED-CONTENT .*/wt-lost wt-lost — 1 commit" && ok "T2 real unmerged commit -> UNMERGED-CONTENT with correct count" || no "T2 expected UNMERGED-CONTENT(1) for wt-lost, got: $out"
echo "$out" | grep -q "^DIRTY .*/wt-dirty wt-dirty" && ok "T3 uncommitted changes -> DIRTY" || no "T3 expected DIRTY for wt-dirty, got: $out"
echo "$out" | grep -q "^SAFE-TO-REMOVE .*/wt-clean wt-clean" && ok "T4 branch identical to main (no extra commits) -> SAFE-TO-REMOVE" || no "T4 expected SAFE-TO-REMOVE for wt-clean, got: $out"

echo "$out" | grep -q "^UNMERGED-CONTENT .*/wt-safe" && no "T5 REGRESSION: wt-safe (content already on main) wrongly flagged UNMERGED-CONTENT — this is exactly the ahead/behind false-alarm the script exists to avoid: $out" || ok "T5 wt-safe never flagged UNMERGED-CONTENT despite its branch never having been merged as a ref"

echo "$err" | grep -qE "checked 4 of 4" && ok "T6 denominator line states checked-of-disk-total correctly (4 of 4)" || no "T6 expected 'checked 4 of 4' on stderr, got: $err"
echo "$err" | grep -q "MISMATCH" && no "T6b false MISMATCH warning fired when counts actually agree: $err" || ok "T6b no false mismatch warning when git-worktree-list and disk agree"

# T7 — denominator mismatch detection: a directory on disk with no git worktree registration at all
# (simulates a manually-deleted .git worktree link leaving orphaned files behind).
mkdir -p "$TMP/main/.claude/worktrees/wt-untracked-orphan"
echo "orphan file, no git worktree link" > "$TMP/main/.claude/worktrees/wt-untracked-orphan/file.txt"
out2=$(WORKTREE_SAFETY_REPO="$TMP/main" WORKTREE_SAFETY_UPSTREAM="origin/main" bash "$SC" 2>/tmp/wss-stderr2.$$)
err2=$(cat /tmp/wss-stderr2.$$); rm -f /tmp/wss-stderr2.$$
echo "$err2" | grep -q "MISMATCH" && ok "T7 an on-disk directory git doesn't know about triggers the MISMATCH warning rather than being silently skipped" || no "T7 expected MISMATCH warning, got: $err2"
echo "$err2" | grep -qE "checked 4 of 5" && ok "T7b mismatch states both numbers correctly (4 checked, 5 on disk)" || no "T7b expected 'checked 4 of 5', got: $err2"

# T8 — nonexistent repo path -> loud failure (rc=3), never a silent empty pass.
out3=$(WORKTREE_SAFETY_REPO="/tmp/does-not-exist-$$" bash "$SC" 2>&1); rc3=$?
[ "$rc3" -eq 3 ] && ok "T8 nonexistent repo path exits 3 (loud failure), not a silent all-clear" || no "T8 expected rc=3 on missing repo, got rc=$rc3"
echo "$out3" | grep -q "measured NOTHING" && ok "T8b failure message states it measured nothing, per m-44 discipline" || no "T8b missing the 'measured NOTHING' assertion: $out3"

echo "── $PASS passed, $FAIL failed ──"
[ "$FAIL" -eq 0 ]
