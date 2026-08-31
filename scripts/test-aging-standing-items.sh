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

echo "== T4: real repo — denominator honesty: files with no parseable date column are individually named =="
# arch/docs/lead/web are non-tabular (bullet lists); comms/cxo/ppm are tabular but with
# no recognized date-column header. All seven are real, sampled by hand before writing
# the parser — this pins that the coverage bucket actually names them, not just counts.
for role in arch docs lead web comms cxo ppm; do
    echo "$real_out" | grep -A20 "no parseable per-item date column" | grep -q "· $role$" \
        && ok "$role correctly named in the no-date-column coverage gap" \
        || no "$role missing from the no-date-column coverage gap"
done

echo "== T5: real repo — cio and pa (the two roles with a real parseable date column) are NOT in the gap bucket =="
echo "$real_out" | grep -A20 "no parseable per-item date column" | grep -q "· cio$" && no "cio wrongly listed as a coverage gap" || ok "cio correctly excluded from the coverage gap (it has a real Filed column)"
echo "$real_out" | grep -A20 "no parseable per-item date column" | grep -q "· pa$" && no "pa wrongly listed as a coverage gap" || ok "pa correctly excluded from the coverage gap (it has a real Noted/Filed column)"

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

echo "== T11: no real tracked file was touched by this test run =="
git -C "$ROOT" status --porcelain dev/active/duty-cycle-registry.tsv | grep -q . \
    && no "duty-cycle-registry.tsv shows a change" || ok "duty-cycle-registry.tsv untouched"
git -C "$ROOT" diff --stat -- 'dev/active/*-standing-items.md' | grep -q . \
    && no "a real *-standing-items.md file shows a diff" || ok "no real *-standing-items.md file was modified"

echo ""
echo "==================== RESULT: $PASS passed, $FAIL failed ===================="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
