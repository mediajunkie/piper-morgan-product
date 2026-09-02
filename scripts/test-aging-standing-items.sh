#!/usr/bin/env bash
# test-aging-standing-items.sh — tests aging-standing-items.sh (added 2026-08-31).
#
# Same pattern as test-check-refresh-promises-state-files.sh: read-only assertions
# against REAL dev/active/ state first (there's no clean way to fake 10 real files
# without a lot of unnecessary harness-building, and the script is read-only anyway),
# then scratch fixture files under a disposable role prefix ("zzztest-") that no real
# role will ever collide with, cleaned up via trap regardless of pass/fail.
set -uo pipefail

SCRIPT="$(cd "$(dirname "$0")" && pwd)/aging-standing-items.sh"
[ -f "$SCRIPT" ] || {
    echo "missing $SCRIPT"
    exit 1
}
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FIXTURE="$ROOT/dev/active/zzztest-standing-items.md"
PASS=0
FAIL=0
ok() {
    echo "  PASS: $1"
    PASS=$((PASS + 1))
}
no() {
    echo "  FAIL: $1"
    FAIL=$((FAIL + 1))
}
cleanup() { rm -f "$FIXTURE"; }
trap cleanup EXIT INT TERM

if [ -e "$FIXTURE" ]; then
    echo "REFUSING TO RUN: $FIXTURE already exists and isn't ours to clobber."
    exit 1
fi

echo "== T1: real repo — host-standing-items.md (formally RETIRED) is skipped entirely =="
real_out=$(cd "$ROOT" && bash "$SCRIPT" 2>&1)
real_rc=$?
echo "$real_out" | grep -q "AGING: host " && no "host appeared in the AGING list despite being retired" || ok "host does not appear in the AGING list"
echo "$real_out" | grep -A5 "retired (skipped" | grep -q "· host" && ok "host is named in the coverage 'retired' bucket" || no "host not named under the retired bucket"

echo "== T2: real repo — script exits 0 (advisory, never fails a caller) =="
[ "$real_rc" -eq 0 ] && ok "exit 0 against real repo state" || no "expected exit 0, got $real_rc"

echo "== T3: real repo — coverage summary is present and non-empty =="
echo "$real_out" | grep -q "── coverage ──" && ok "coverage section header present" || no "coverage section header missing"
echo "$real_out" | grep -q "standing-items files found:" && ok "file-count line present" || no "file-count line missing"
echo "$real_out" | grep -qE "no parseable per-item date column at all \(COVERAGE GAP\): [0-9]+" && ok "coverage-gap count line present" || no "coverage-gap count line missing"

echo "== T1b: real repo — host-standing-items.md is not the only retired file (ppm retired same-day) =="
echo "$real_out" | grep -A5 "retired (skipped" | grep -q "· ppm$" && ok "ppm is named in the coverage 'retired' bucket" || no "ppm not named under the retired bucket"

echo "== T4: real repo — denominator honesty: files with no parseable date column are individually named =="
# ⚠️ THIS LIST IS A MOVING TARGET, BY DESIGN — testing against real files means this
# assertion tracks real cohort adoption, not a frozen fixture. As of 2026-08-31 (v1.1,
# after the inline-bold-label + Blocked-on-column fixes): docs/web/cxo adopted a
# recognized format same-day and dropped out of this gap; arch/comms/lead had not yet.
# If this test starts failing because MORE roles have since adopted a format, that is
# the mechanism working, not a regression — update this list to match, don't just widen
# the match to make it pass.
for role in arch comms lead; do
    echo "$real_out" | grep -A20 "no parseable per-item date column" | grep -q "· $role$" \
        && ok "$role correctly named in the no-date-column coverage gap" \
        || no "$role missing from the no-date-column coverage gap"
done

echo "== T5: real repo — roles with a real parseable date are NOT in the gap bucket =="
echo "$real_out" | grep -A20 "no parseable per-item date column" | grep -q "· cio$" && no "cio wrongly listed as a coverage gap" || ok "cio correctly excluded from the coverage gap (it has a real Filed column)"
echo "$real_out" | grep -A20 "no parseable per-item date column" | grep -q "· pa$" && no "pa wrongly listed as a coverage gap" || ok "pa correctly excluded from the coverage gap (it has a real Noted/Filed column)"

echo "== T5b: real repo — docs is readable via the NEW inline-bold-label path (v1.1 fix, Web's finding) =="
echo "$real_out" | grep -A20 "no parseable per-item date column" | grep -q "· docs$" && no "docs still in the coverage gap — inline-label fix regressed" || ok "docs correctly excluded (inline **Added**: date now recognized)"

echo "== T5c: real repo — cxo's structural Blocked-on column now suppresses its 2 known false positives (v1.1 fix, CXO's finding) =="
echo "$real_out" | grep -q "AGING: cxo — .*Spatial committed-theory review" && no "cxo's Spatial-committed-theory row still false-positives — Blocked-on-column fix regressed" || ok "cxo's Blocked-on-column row no longer false-positives"

echo "== T6: fixture — an old (30d), unblocked row IS flagged AGING =="
DATE_OLD=$(date -v-30d +%Y-%m-%d)
DATE_RECENT=$(date -v-5d +%Y-%m-%d)
cat >"$FIXTURE" <<EOF
# ZZZTest Standing Items (scratch fixture, safe to delete)

### Genuinely still open, carried forward

| # | Item | Filed | Status |
|---|---|---|---|
| 1 | **Old unblocked item** | $DATE_OLD | Nothing blocking, just never scheduled. |
| 2 | **Old but pending PM** | $DATE_OLD | Pending PM decision before proceeding. |
| 3 | **Recent item** | $DATE_RECENT | Filed recently, not aging yet. |
EOF
out6=$(cd "$ROOT" && bash "$SCRIPT" 2>&1)
rc6=$?
echo "$out6" | grep -q "AGING: zzztest #1" && ok "30-day-old unblocked row flagged AGING" || no "expected AGING: zzztest #1, got: $(echo "$out6" | grep zzztest)"

echo "== T7: fixture — an equally old row WITH blocking language ('Pending PM') is NOT flagged =="
echo "$out6" | grep -q "AGING: zzztest #2" && no "row #2 ('Pending PM') was wrongly flagged AGING" || ok "row #2 ('Pending PM') correctly excluded despite being old"

echo "== T8: fixture — a 5-day-old row is NOT flagged (too recent) =="
echo "$out6" | grep -q "AGING: zzztest #3" && no "row #3 (5 days old) was wrongly flagged AGING" || ok "row #3 (5 days old) correctly not flagged"

echo "== T9: fixture — exit code still 0 with real findings present =="
[ "$rc6" -eq 0 ] && ok "exit 0 even with AGING findings (advisory, never fails)" || no "expected exit 0, got $rc6"

rm -f "$FIXTURE"

echo "== T10: fixture — a formally RETIRED file is skipped entirely, not counted as a gap =="
cat >"$FIXTURE" <<EOF
---
retired: 2026-01-01
retirement_reason: "scratch test fixture — pretends to have migrated elsewhere"
---

# ZZZTest Standing Items (RETIRED, scratch fixture)

| # | Item | Filed | Status |
|---|---|---|---|
| 1 | **Should never be seen** | $(date -v-90d +%Y-%m-%d) | Ancient and unblocked, but the file is retired. |
EOF
out10=$(cd "$ROOT" && bash "$SCRIPT" 2>&1)
echo "$out10" | grep -q "AGING: zzztest" && no "retired fixture's row leaked into the AGING list" || ok "retired fixture produced no AGING line"
echo "$out10" | grep -A5 "retired (skipped" | grep -q "· zzztest$" && ok "retired fixture correctly named in the retired bucket" || no "retired fixture not named in the retired bucket"
echo "$out10" | grep -A20 "no parseable per-item date column" | grep -q "· zzztest$" && no "retired fixture ALSO double-counted as a coverage gap (should be retired-only)" || ok "retired fixture not double-counted as a coverage gap"

rm -f "$FIXTURE"

echo "== T12: fixture — v1.1 inline-bold-label path (Web's finding): unblocked heading flagged,"
echo "        blocked heading excluded, recent heading not flagged =="
cat >"$FIXTURE" <<EOF
# ZZZTest Standing Items (v1.1 fixture — inline bold-label, non-tabular shape)

## An unblocked heading item
**Filed**: $DATE_OLD

This item has no blocking language anywhere in its own prose.

## A blocked heading item
**Filed**: $DATE_OLD

Blocked on: PPM picking a slot.

## A recent heading item
**Added**: $DATE_RECENT

Too new to flag either way.
EOF
out12=$(cd "$ROOT" && bash "$SCRIPT" 2>&1)
rc12=$?
echo "$out12" | grep -q "AGING: zzztest — An unblocked heading item" && ok "unblocked inline-labeled heading IS flagged AGING" || no "expected AGING for the unblocked heading, got: $(echo "$out12" | grep zzztest)"
echo "$out12" | grep -q "AGING: zzztest — A blocked heading item" && no "blocked inline-labeled heading was WRONGLY flagged" || ok "blocked inline-labeled heading correctly excluded (blocking language found in the look-ahead window)"
echo "$out12" | grep -q "AGING: zzztest — A recent heading item" && no "recent inline-labeled heading was WRONGLY flagged" || ok "recent inline-labeled heading correctly not flagged (too new)"
[ "$rc12" -eq 0 ] && ok "exit 0 with the inline-label path exercised" || no "expected exit 0, got $rc12"
rm -f "$FIXTURE"

echo "== T13: fixture — v1.1 structural Blocked-on column (CXO's finding): a non-empty cell blocks"
echo "        regardless of wording, even generic wording no phrase list would catch =="
cat >"$FIXTURE" <<EOF
# ZZZTest Standing Items (v1.1 fixture — structural Blocked-on column)

| Filed | Item | Blocked on | Recheck trigger |
|---|---|---|---|
| $DATE_OLD | **Genuinely unblocked** | | |
| $DATE_OLD | **Structurally blocked, generic wording** | Someone else has to go first | when they do |
EOF
out13=$(cd "$ROOT" && bash "$SCRIPT" 2>&1)
rc13=$?
echo "$out13" | grep -q "AGING: zzztest — .*Genuinely unblocked" && ok "row with an EMPTY Blocked-on cell IS flagged AGING" || no "expected AGING for the genuinely-unblocked row, got: $(echo "$out13" | grep zzztest)"
echo "$out13" | grep -q "AGING: zzztest — .*Structurally blocked" && no "row with a non-empty Blocked-on cell was WRONGLY flagged, despite wording no BLOCK_PHRASES entry matches" || ok "row with a non-empty Blocked-on cell correctly excluded, even with generic wording"
[ "$rc13" -eq 0 ] && ok "exit 0 with the Blocked-on-column path exercised" || no "expected exit 0, got $rc13"
rm -f "$FIXTURE"

echo "== T15: v1.2 stale-blocker-rot (CXO's finding, 2026-09-02) — blocker cites a CLOSED #NNNN =="
# Mock `gh` so this is deterministic and offline — no real network/auth dependency. #999991 is
# "closed", #999992 is "open"; neither is a real issue number.
MOCKDIR="$(mktemp -d)"
cat >"$MOCKDIR/gh" <<'MOCKEOF'
#!/usr/bin/env bash
if [ "$1" = "issue" ] && [ "$2" = "view" ]; then
    case "$3" in
        999991) echo "CLOSED" ;;
        999992) echo "OPEN" ;;
        *) exit 1 ;;
    esac
fi
MOCKEOF
chmod +x "$MOCKDIR/gh"
cat >"$FIXTURE" <<EOF
# ZZZTest Standing Items (v1.2 fixture — stale-blocker-rot)

| Filed | Item | Blocked on | Recheck trigger |
|---|---|---|---|
| $DATE_RECENT | **Blocker actually closed** | Rides #999991 closing | when #999991 closes |
| $DATE_RECENT | **Blocker still open** | Rides #999992 closing | when #999992 closes |
| $DATE_RECENT | **Person-named blocker, no issue** | Waiting on PPM to pick a slot | when PPM decides |
EOF
out15=$(cd "$ROOT" && PATH="$MOCKDIR:$PATH" bash "$SCRIPT" 2>&1)
rc15=$?
echo "$out15" | grep -q "STALE-BLOCKER: zzztest — .*Blocker actually closed.*#999991" && ok "row citing a CLOSED #NNNN is flagged STALE-BLOCKER" || no "expected STALE-BLOCKER for the closed-issue row, got: $(echo "$out15" | grep zzztest)"
echo "$out15" | grep -q "STALE-BLOCKER: zzztest — .*Blocker still open" && no "row citing an OPEN #NNNN was WRONGLY flagged STALE-BLOCKER" || ok "row citing an OPEN #NNNN correctly not flagged"
echo "$out15" | grep -q "STALE-BLOCKER: zzztest — .*Person-named blocker" && no "person-named blocker (no #NNNN) was WRONGLY flagged — out of mechanical scope" || ok "person-named blocker correctly not flagged (CXO's own caveat: needs discipline, not tooling)"
# Since these rows are RECENT (not >= AGE_THRESHOLD_DAYS), none should appear as plain AGING —
# proves the stale-blocker check runs independent of the age gate, not gated behind it.
echo "$out15" | grep -q "^AGING: zzztest" && no "a recent row leaked into plain AGING output" || ok "recent rows correctly absent from plain AGING (stale-blocker check is age-independent, as designed)"
echo "$out15" | grep -q "flagged STALE-BLOCKER (blocker cites a closed #NNNN): 1" && ok "coverage summary reports exactly 1 stale-blocker" || no "coverage summary stale-blocker count wrong: $(echo "$out15" | grep 'STALE-BLOCKER (blocker')"
[ "$rc15" -eq 0 ] && ok "exit 0 with the stale-blocker path exercised" || no "expected exit 0, got $rc15"
rm -rf "$MOCKDIR"
rm -f "$FIXTURE"

echo "== T16: v1.2 stale-blocker-rot — gh unavailable/failing never manufactures a false flag =="
BADMOCKDIR="$(mktemp -d)"
cat >"$BADMOCKDIR/gh" <<'MOCKEOF'
#!/usr/bin/env bash
exit 1
MOCKEOF
chmod +x "$BADMOCKDIR/gh"
cat >"$FIXTURE" <<EOF
# ZZZTest Standing Items (v1.2 fixture — gh failure)

| Filed | Item | Blocked on | Recheck trigger |
|---|---|---|---|
| $DATE_RECENT | **Blocker cites an issue, gh fails** | Rides #999993 closing | when #999993 closes |
EOF
out16=$(cd "$ROOT" && PATH="$BADMOCKDIR:$PATH" bash "$SCRIPT" 2>&1)
rc16=$?
echo "$out16" | grep -q "STALE-BLOCKER: zzztest" && no "a failed gh lookup was WRONGLY treated as CLOSED" || ok "a failed gh lookup correctly does not manufacture a STALE-BLOCKER flag"
[ "$rc16" -eq 0 ] && ok "exit 0 even when gh itself fails (advisory, never crashes the caller)" || no "expected exit 0, got $rc16"
rm -rf "$BADMOCKDIR"
rm -f "$FIXTURE"

echo "== T14: no real tracked file was touched by this test run =="
git -C "$ROOT" status --porcelain dev/active/duty-cycle-registry.tsv | grep -q . \
    && no "duty-cycle-registry.tsv shows a change" || ok "duty-cycle-registry.tsv untouched"
git -C "$ROOT" diff --stat -- 'dev/active/*-standing-items.md' | grep -q . \
    && no "a real *-standing-items.md file shows a diff" || ok "no real *-standing-items.md file was modified"

echo ""
echo "==================== RESULT: $PASS passed, $FAIL failed ===================="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
