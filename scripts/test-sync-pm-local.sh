#!/usr/bin/env bash
# test-sync-pm-local.sh — isolated test harness for the 3-tier PM-checkout sync classifier (#1368).
# Builds a throwaway origin + a "PM checkout" clone in a temp dir; never touches the real repo or
# the real PM checkout. Exercises: tier-1 clearing, tier-2 whitespace/growth heuristic, tier-3 hard
# stop, dry-run (no mutation), and branch/no-op safety.
set -uo pipefail

SYNC="$(cd "$(dirname "$0")" && pwd)/sync-pm-local.sh"
[ -f "$SYNC" ] || { echo "missing $SYNC"; exit 1; }
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=t@t
T="$(mktemp -d "${TMPDIR:-/tmp}/synctest.XXXXXX")"
trap 'rm -rf "$T"' EXIT
PASS=0; FAIL=0
ok(){ echo "  ✅ $1"; PASS=$((PASS+1)); }
no(){ echo "  ❌ $1"; FAIL=$((FAIL+1)); }

ORIGIN="$T/origin.git"; git init --bare -q "$ORIGIN"
SEED="$T/seed"; git clone -q "$ORIGIN" "$SEED"
mkdir -p "$SEED"/mailboxes/lead/inbox "$SEED"/dev/active "$SEED"/docs/internal/architecture/decisions "$SEED"/docs/internal/planning/comms
printf 'old manifest\n' > "$SEED/mailboxes/lead/inbox/MANIFEST.md"
printf 'old carry-forward\n' > "$SEED/dev/active/lead-carry-forward.md"
printf 'line1\nline2\n' > "$SEED/docs/internal/architecture/decisions/decisions.log"
git -C "$SEED" add -A; git -C "$SEED" commit -qm seed; git -C "$SEED" push -q origin HEAD:main

clone_pm(){ git clone -q "$ORIGIN" "$T/$1"; git -C "$T/$1" checkout -q -b main-tmp 2>/dev/null; git -C "$T/$1" branch -q -f main; git -C "$T/$1" checkout -q main; git -C "$T/$1" branch -q -D main-tmp 2>/dev/null || true; }

push_upstream_change(){
    # a second agent worktree pushes a real change to origin/main
    W="$T/agentwt"; rm -rf "$W"; git clone -q "$ORIGIN" "$W"
    printf 'new manifest content\n' > "$W/mailboxes/lead/inbox/MANIFEST.md"
    printf 'new carry-forward content\n' > "$W/dev/active/lead-carry-forward.md"
    git -C "$W" add -A; git -C "$W" commit -qm "agent push: manifest + carry-forward update" >/dev/null 2>&1
    git -C "$W" push -q origin HEAD:main
}

echo "── T1: tier-1 clearing (MANIFEST.md + carry-forward drift) → cleared, PM checkout fast-forwards ──"
clone_pm pmA
printf 'LOCAL drift, agent hook wrote this\n' > "$T/pmA/mailboxes/lead/inbox/MANIFEST.md"
printf 'LOCAL drift carry-forward\n' > "$T/pmA/dev/active/lead-carry-forward.md"
push_upstream_change
out=$(PM_CHECKOUT="$T/pmA" bash "$SYNC" 2>&1)
[ "$(cat "$T/pmA/mailboxes/lead/inbox/MANIFEST.md")" = "new manifest content" ] && ok "MANIFEST.md now matches origin/main" || no "MANIFEST.md not cleared correctly"
[ "$(cat "$T/pmA/dev/active/lead-carry-forward.md")" = "new carry-forward content" ] && ok "carry-forward now matches origin/main" || no "carry-forward not cleared correctly"
head_pmA=$(git -C "$T/pmA" rev-parse HEAD); head_origin=$(git -C "$T/pmA" rev-parse origin/main)
[ "$head_pmA" = "$head_origin" ] && ok "PM checkout fast-forwarded to origin/main tip" || no "PM checkout did NOT fast-forward"
[ -z "$(git -C "$T/pmA" status --porcelain)" ] && ok "PM checkout is fully clean after sync" || no "PM checkout still dirty after sync"
echo "$out" | grep -q "fast-forwarded" && ok "reported success" || no "did not report fast-forward success"

echo "── T2: per-path exclusion — an untracked PM file does NOT block clearing disjoint tier-1 drift ──"
clone_pm pmB
printf 'LOCAL drift\n' > "$T/pmB/mailboxes/lead/inbox/MANIFEST.md"
printf 'PM real prose WIP, untracked\n' > "$T/pmB/docs/public-draft-untracked.md"
push_upstream_change
before_untracked=$(cat "$T/pmB/docs/public-draft-untracked.md")
out=$(PM_CHECKOUT="$T/pmB" bash "$SYNC" 2>&1)
[ "$(cat "$T/pmB/mailboxes/lead/inbox/MANIFEST.md")" = "new manifest content" ] && ok "tier-1 MANIFEST still cleared despite unrelated untracked file" || no "MANIFEST was NOT cleared — over-blocked by an unrelated tier-3 file"
[ -f "$T/pmB/docs/public-draft-untracked.md" ] && [ "$(cat "$T/pmB/docs/public-draft-untracked.md")" = "$before_untracked" ] && ok "PM's untracked prose file untouched and unchanged" || no "PM's untracked file was altered/removed — should NEVER happen"
head_pmB=$(git -C "$T/pmB" rev-parse HEAD); head_origin=$(git -C "$T/pmB" rev-parse origin/main)
[ "$head_pmB" = "$head_origin" ] && ok "PM checkout still fast-forwarded despite the untracked file" || no "fast-forward did not happen"
echo "$out" | grep -qi "leaving those alone" && ok "reported the tier-3 path was left alone (not a whole-sync skip)" || no "did not report the per-path exclusion"

echo "── T3: per-path exclusion — an unknown MODIFIED (tracked) path is left alone, tier-1 still clears ──"
clone_pm pmC
printf 'LOCAL drift\n' > "$T/pmC/mailboxes/lead/inbox/MANIFEST.md"
printf 'seed\n' > "$T/pmC/config-local.md"; git -C "$T/pmC" add config-local.md; git -C "$T/pmC" commit -qm "seed unknown tracked file" >/dev/null 2>&1
git -C "$T/pmC" push -q origin HEAD:main
printf 'PM edited this directly\n' >> "$T/pmC/config-local.md"
push_upstream_change
out=$(PM_CHECKOUT="$T/pmC" bash "$SYNC" 2>&1)
echo "$out" | grep -q "config-local.md" && ok "unknown modified path named as left-alone" || no "unknown modified path not named"
[ "$(tail -1 "$T/pmC/config-local.md")" = "PM edited this directly" ] && ok "unknown modified path left untouched" || no "unknown modified path was altered"
[ "$(cat "$T/pmC/mailboxes/lead/inbox/MANIFEST.md")" = "new manifest content" ] && ok "tier-1 MANIFEST still cleared despite the unrelated unknown modified path" || no "MANIFEST was NOT cleared — over-blocked"

echo "── T4: tier-2 content-heuristic — whitespace-only diff clears, real growth holds ──"
clone_pm pmD
printf 'line1  \nline2\n' > "$T/pmD/docs/internal/architecture/decisions/decisions.log"  # trailing whitespace only
out=$(PM_CHECKOUT="$T/pmD" bash "$SYNC" --dry-run 2>&1)
echo "$out" | grep -q "decisions.log" && echo "$out" | grep -q "would clear" && ok "whitespace-only decisions.log slated for clearing" || no "whitespace-only decisions.log not classified as clearable"

clone_pm pmE
printf 'line1\nline2\nPM added a real new decision here\n' > "$T/pmE/docs/internal/architecture/decisions/decisions.log"  # net growth, real content
out=$(PM_CHECKOUT="$T/pmE" bash "$SYNC" --dry-run 2>&1)
echo "$out" | grep -q "holding for manual review" && echo "$out" | grep -q "decisions.log" && ok "grown decisions.log held for manual review, not auto-cleared" || no "grown decisions.log was NOT held — risk of discarding PM's real edit"
[ "$(cat "$T/pmE/docs/internal/architecture/decisions/decisions.log")" = "$(printf 'line1\nline2\nPM added a real new decision here\n')" ] && ok "dry-run made no actual changes to the file" || no "dry-run mutated the file — should never happen"

echo "── T5: dry-run never mutates anything, even when tier-1 clearing would otherwise apply ──"
clone_pm pmF
printf 'LOCAL drift\n' > "$T/pmF/mailboxes/lead/inbox/MANIFEST.md"
before_head=$(git -C "$T/pmF" rev-parse HEAD)
before_content=$(cat "$T/pmF/mailboxes/lead/inbox/MANIFEST.md")
out=$(PM_CHECKOUT="$T/pmF" bash "$SYNC" --dry-run 2>&1)
after_head=$(git -C "$T/pmF" rev-parse HEAD)
after_content=$(cat "$T/pmF/mailboxes/lead/inbox/MANIFEST.md")
[ "$before_head" = "$after_head" ] && ok "dry-run: HEAD unchanged" || no "dry-run moved HEAD"
[ "$before_content" = "$after_content" ] && ok "dry-run: file content unchanged on disk" || no "dry-run mutated file content"
echo "$out" | grep -q "DRY RUN" && ok "dry-run clearly labeled its own output" || no "dry-run output not clearly labeled"

echo "── T6: not on main → skip, untouched (existing v1 safety, preserved) ──"
clone_pm pmG
git -C "$T/pmG" checkout -q -b some-other-branch
before_head=$(git -C "$T/pmG" rev-parse HEAD)
out=$(PM_CHECKOUT="$T/pmG" bash "$SYNC" 2>&1)
after_head=$(git -C "$T/pmG" rev-parse HEAD)
[ "$before_head" = "$after_head" ] && ok "non-main branch left untouched" || no "non-main branch was modified"
echo "$out" | grep -q "not main" && ok "reported the non-main skip reason" || no "did not report non-main skip"

echo "── T7: fully clean checkout → plain fast-forward still works (no drift to classify) ──"
clone_pm pmH
push_upstream_change
out=$(PM_CHECKOUT="$T/pmH" bash "$SYNC" 2>&1)
head_pmH=$(git -C "$T/pmH" rev-parse HEAD); head_origin=$(git -C "$T/pmH" rev-parse origin/main)
[ "$head_pmH" = "$head_origin" ] && ok "clean checkout still fast-forwards normally" || no "clean checkout failed to fast-forward"

echo "── T8: git-quoted paths (parens trigger porcelain quoting) still classify as tier-1 ──"
# Real-world case: "mailboxes/xian (ceo)/inbox/MANIFEST.md" — git wraps this in literal double
# quotes in --porcelain output because of the parens, independent of core.quotepath.
clone_pm pmI
mkdir -p "$T/pmI/mailboxes/xian (ceo)/inbox"
printf 'seed\n' > "$T/pmI/mailboxes/xian (ceo)/inbox/MANIFEST.md"
git -C "$T/pmI" add "mailboxes/xian (ceo)/inbox/MANIFEST.md"
git -C "$T/pmI" commit -qm "seed the parenthesized mailbox path" >/dev/null 2>&1
git -C "$T/pmI" push -q origin HEAD:main
printf 'LOCAL drift on a quoted path\n' > "$T/pmI/mailboxes/xian (ceo)/inbox/MANIFEST.md"
W="$T/agentwt2"; rm -rf "$W"; git clone -q "$ORIGIN" "$W"
printf 'new content from an agent push\n' > "$W/mailboxes/xian (ceo)/inbox/MANIFEST.md"
git -C "$W" add -A; git -C "$W" commit -qm "agent push to parenthesized mailbox" >/dev/null 2>&1
git -C "$W" push -q origin HEAD:main
out=$(PM_CHECKOUT="$T/pmI" bash "$SYNC" 2>&1)
[ "$(cat "$T/pmI/mailboxes/xian (ceo)/inbox/MANIFEST.md")" = "new content from an agent push" ] \
    && ok "quoted/parenthesized path correctly cleared to origin/main's version" \
    || no "quoted/parenthesized path NOT cleared — quoting bug regression"
echo "$out" | grep -q "unknown-path" && no "quoted path was misclassified as tier-3 unknown" || ok "quoted path was NOT misclassified as tier-3"

echo "── T9: the actual safety backstop — a TRUE collision (tier-3 file also changed upstream) fails loudly, never silently overwrites ──"
clone_pm pmJ
printf 'seed\n' > "$T/pmJ/docs/public-draft-untracked-tracked.md"
git -C "$T/pmJ" add docs/public-draft-untracked-tracked.md
git -C "$T/pmJ" commit -qm "seed a file that will collide" >/dev/null 2>&1
git -C "$T/pmJ" push -q origin HEAD:main
printf 'PM local edit, uncommitted\n' >> "$T/pmJ/docs/public-draft-untracked-tracked.md"
# a second agent ALSO pushes a change to that exact same file -- a genuine collision
W="$T/agentwt3"; rm -rf "$W"; git clone -q "$ORIGIN" "$W"
printf 'seed\nagent change to the SAME file\n' > "$W/docs/public-draft-untracked-tracked.md"
git -C "$W" add -A; git -C "$W" commit -qm "agent touches the same file PM is editing (shouldn't happen, but verify the backstop)" >/dev/null 2>&1
git -C "$W" push -q origin HEAD:main
before_local=$(cat "$T/pmJ/docs/public-draft-untracked-tracked.md")
out=$(PM_CHECKOUT="$T/pmJ" bash "$SYNC" 2>&1)
after_local=$(cat "$T/pmJ/docs/public-draft-untracked-tracked.md")
[ "$before_local" = "$after_local" ] && ok "PM's dirty content in the colliding file is NEVER overwritten" || no "DATA LOSS — colliding file was silently overwritten"
echo "$out" | grep -qi "fast-forward failed" && ok "the collision surfaced as a loud failure, not silence" || no "collision was not reported"

echo ""
echo "════════ RESULT: $PASS passed, $FAIL failed ════════"
[ "$FAIL" = 0 ] && exit 0 || exit 1
