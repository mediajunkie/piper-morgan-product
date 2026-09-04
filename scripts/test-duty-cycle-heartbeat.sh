#!/usr/bin/env bash
# test-duty-cycle-heartbeat.sh — isolated test harness for the --if-quiet suppression window.
# Builds a throwaway origin + clone in a temp dir; never touches the real repo or real heartbeats.
# Exercises the 2026-08-28 fix (Web's false-positive finding): the suppression window must be short
# enough that a role on the cohort's tightest cadence (3h) never goes silent longer than its own
# dynamic threshold can tolerate.
set -uo pipefail

HB="$(cd "$(dirname "$0")" && pwd)/duty-cycle-heartbeat.sh"
[ -f "$HB" ] || { echo "missing $HB"; exit 1; }
export GIT_AUTHOR_NAME=test GIT_AUTHOR_EMAIL=t@t GIT_COMMITTER_NAME=test GIT_COMMITTER_EMAIL=t@t
T="$(mktemp -d "${TMPDIR:-/tmp}/hbtest.XXXXXX")"
trap 'rm -rf "$T"' EXIT
PASS=0; FAIL=0
ok(){ echo "  ✅ $1"; PASS=$((PASS+1)); }
no(){ echo "  ❌ $1"; FAIL=$((FAIL+1)); }

ORIGIN="$T/origin.git"; git init --bare -q "$ORIGIN"
mkclone(){ local name="$1"; git clone -q "$ORIGIN" "$T/$name"; echo "$T/$name"; }

# Seed a role-tagged commit at a given epoch offset (seconds ago) into a fresh clone, push to origin.
# Each call uses the origin's own commit count as a uniqueness marker — clones made from a shared
# bare origin otherwise inherit earlier tests' identically-named/identically-content seed files, and
# `git add -A` silently finds nothing to commit (a real bug this test hit on its first draft).
seed_commit_ago() {
    local wd="$1" role="$2" secs_ago="$3" now epoch uniq
    now=$(date +%s); epoch=$((now - secs_ago))
    uniq="$(git -C "$wd" rev-list --count HEAD 2>/dev/null || echo 0)-$$-$RANDOM"
    mkdir -p "$wd/dev/2026/08/28"
    printf 'seed %s\n' "$uniq" > "$wd/dev/2026/08/28/seed-${role}-${uniq}.md"
    (cd "$wd" && git add -A && \
     GIT_AUTHOR_DATE="@$epoch +0000" GIT_COMMITTER_DATE="@$epoch +0000" \
     git commit -qm "log($role): seeded commit $secs_ago s ago" -- "dev/2026/08/28/seed-${role}-${uniq}.md" >/dev/null && \
     git push -q origin HEAD:main >/dev/null)
}

echo "── T1: commit 2h ago (within new 3h window) → --if-quiet suppresses the ROW, writes nothing to the day's TSV ──"
W1=$(mkclone w1)
seed_commit_ago "$W1" testrole $((2*3600))
out=$(cd "$W1" && bash "$HB" testrole work --if-quiet 2>&1)
[ ! -f "$W1/dev/heartbeats/$(date +%Y-%m-%d)/testrole.tsv" ] && ok "no heartbeat file written (suppressed)" || no "heartbeat file was written — should have suppressed"
echo "$out" | grep -q "row suppressed" && ok "reported suppression correctly" || no "did not report suppression"

echo "── T2: commit 4h ago (past new 3h window) → --if-quiet writes a heartbeat ──"
W2=$(mkclone w2)
seed_commit_ago "$W2" testrole $((4*3600))
out=$(cd "$W2" && bash "$HB" testrole work --if-quiet 2>&1)
[ -f "$W2/dev/heartbeats/$(date +%Y-%m-%d)/testrole.tsv" ] && ok "heartbeat file WAS written (not suppressed past 3h)" || no "heartbeat missing — should have written past the 3h window"
git -C "$W2" fetch -q origin
git -C "$W2" cat-file -e "origin/main:dev/heartbeats/$(date +%Y-%m-%d)/testrole.tsv" 2>/dev/null \
    && ok "heartbeat landed on origin/main" || no "heartbeat did not land on origin/main"

echo "── T3: THE ACTUAL BUG — two consecutive quiet fires 3h apart, worst-case silence bounded ──"
# Web's exact shape: a role fires every 3h. Simulate fire N (commit), fire N+1 (+3h, quiet),
# fire N+2 (+6h, quiet) using the OLD 6h window would suppress both, leaving 6h of silence with
# no heartbeat until fire N+3. With the NEW 3h window, fire N+1 (elapsed exactly 3h) is
# borderline/suppressed, but fire N+2 (elapsed 6h) must NOT suppress — bounding worst-case
# silence to ~2 intervals (6h), not 3 (9h), safely under a 3h-cadence role's 7h threshold.
W3=$(mkclone w3)
seed_commit_ago "$W3" testrole $((6*3600))   # simulates being at "fire N+2" with commit from fire N
out=$(cd "$W3" && bash "$HB" testrole work --if-quiet 2>&1)
[ -f "$W3/dev/heartbeats/$(date +%Y-%m-%d)/testrole.tsv" ] && ok "at 6h elapsed (2 fire-intervals), heartbeat writes — old 6h window would have suppressed this" || no "REGRESSION: 6h elapsed still suppressed — Web's exact failure mode is back"

echo "── T4: no prior commit at all → --if-quiet writes (first-ever fire) ──"
W4=$(mkclone w4)
out=$(cd "$W4" && bash "$HB" testrole work --if-quiet 2>&1)
[ -f "$W4/dev/heartbeats/$(date +%Y-%m-%d)/testrole.tsv" ] && ok "heartbeat written when no prior commit exists" || no "heartbeat missing on first-ever fire"

echo "── T5: START always writes regardless of --if-quiet, unaffected by this fix ──"
W5=$(mkclone w5)
seed_commit_ago "$W5" testrole $((1*3600))   # well within any suppression window
out=$(cd "$W5" && bash "$HB" testrole START --if-quiet 2>&1)
[ -f "$W5/dev/heartbeats/$(date +%Y-%m-%d)/testrole.tsv" ] && ok "START wrote despite --if-quiet and a recent commit (unchanged behavior)" || no "START was suppressed — should never happen"
echo "$out" | grep -q "START always writes" && ok "reported the START-always-writes override" || no "did not report the override"

echo "── T6: v1.1 (2026-09-04, CXO's finding) — suppression STILL lands the last-invoked marker ──"
# The whole point of 7j: a suppressed fire must not be completely invisible. Reproduces CXO's real
# shape (writer invoked, then a long silent stretch that's indistinguishable from "never invoked"
# without this marker) by checking the marker is written and pushed even when the row is suppressed.
W6=$(mkclone w6)
seed_commit_ago "$W6" testrole $((2*3600))
out=$(cd "$W6" && bash "$HB" testrole work --if-quiet 2>&1)
[ -f "$W6/dev/heartbeats/last-invoked/testrole.txt" ] && ok "last-invoked marker written locally even though the row was suppressed" || no "marker missing after suppression"
git -C "$W6" fetch -q origin
git -C "$W6" cat-file -e "origin/main:dev/heartbeats/last-invoked/testrole.txt" 2>/dev/null \
    && ok "last-invoked marker landed on origin/main despite suppression" || no "marker did not land on origin/main"
echo "$out" | grep -q "marker updated" && ok "reported the marker update in output" || no "did not report the marker update"

echo "── T7: v1.1 — a full (non-suppressed) write lands the marker in the SAME commit, not a second one ──"
W7=$(mkclone w7)
seed_commit_ago "$W7" testrole $((4*3600))   # past the 3h window → writes for real
git -C "$W7" fetch -q origin
before_origin=$(git -C "$W7" rev-list --count origin/main)
out=$(cd "$W7" && bash "$HB" testrole work --if-quiet 2>&1)
git -C "$W7" fetch -q origin
after_origin=$(git -C "$W7" rev-list --count origin/main)
[ "$((after_origin - before_origin))" = 1 ] && ok "exactly ONE new commit landed (row + marker together, not two pushes)" || no "expected exactly 1 new commit, delta was $((after_origin - before_origin))"
git -C "$W7" cat-file -e "origin/main:dev/heartbeats/last-invoked/testrole.txt" 2>/dev/null \
    && ok "last-invoked marker present after a full write too" || no "marker missing after a full write"

echo "── T8: v1.1 — the marker is OVERWRITTEN across invocations, not appended (bounded size) ──"
W8=$(mkclone w8)
seed_commit_ago "$W8" testrole $((2*3600))
cd "$W8" && bash "$HB" testrole work --if-quiet >/dev/null 2>&1
first_line_count=$(wc -l < dev/heartbeats/last-invoked/testrole.txt | tr -d ' ')
git fetch -q origin && git merge -q origin/main --no-edit >/dev/null 2>&1
seed_commit_ago "$W8" testrole $((2*3600))
bash "$HB" testrole work --if-quiet >/dev/null 2>&1
second_line_count=$(wc -l < dev/heartbeats/last-invoked/testrole.txt | tr -d ' ')
cd - >/dev/null
[ "$first_line_count" = "1" ] && [ "$second_line_count" = "1" ] && ok "marker stays 1 line across repeated suppressed invocations (overwritten, not appended)" || no "marker grew — expected overwrite, got $first_line_count then $second_line_count lines"

echo ""
echo "════════ RESULT: $PASS passed, $FAIL failed ════════"
[ "$FAIL" = 0 ] && exit 0 || exit 1
