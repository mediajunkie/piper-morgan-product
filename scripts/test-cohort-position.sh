#!/usr/bin/env bash
# test-cohort-position.sh — tests scripts/cohort-position.sh against REAL repo state.
#
# Follows the same pattern as scripts/test-check-refresh-promises-trigger-sent.sh in this repo:
# the script under test is read-only against real files (registry + carry-forwards + heartbeats),
# so there's no clean way to fake 11 real carry-forward files without a lot of unnecessary harness
# building — testing against real state is fine and matches how that companion test does it. The
# one thing we CAN'T safely test against real state is "a registry role with no carry-forward
# file," since every real role currently has one — that case uses a scratch COPY of the registry
# with one fake extra role appended (COHORT_POSITION_REGISTRY override), never touching the real
# file.
set -uo pipefail

SCRIPT="$(cd "$(dirname "$0")" && pwd)/cohort-position.sh"
[ -f "$SCRIPT" ] || { echo "missing $SCRIPT"; exit 1; }
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
SCRATCH=""
ok(){ echo "  PASS: $1"; PASS=$((PASS+1)); }
no(){ echo "  FAIL: $1"; FAIL=$((FAIL+1)); }
cleanup(){ [ -n "$SCRATCH" ] && rm -rf "$SCRATCH"; }
trap cleanup EXIT INT TERM

echo "== T1: exits 0 against real repo state =="
out1=$(cd "$ROOT" && "$SCRIPT" 2>/tmp/cohort-position-t1-stderr.$$)
rc1=$?
[ "$rc1" -eq 0 ] && ok "exit 0" || no "exit code was $rc1 (stderr: $(cat /tmp/cohort-position-t1-stderr.$$))"
rm -f "/tmp/cohort-position-t1-stderr.$$"

echo "== T2: output is valid-looking markdown — header row + separator + >=1 data row =="
echo "$out1" | grep -qE '^\| *Role *\|' && ok "has a header row containing 'Role'" || no "no 'Role' header row found"
echo "$out1" | grep -qE '^\|-+\|' && ok "has a separator row" || no "no markdown separator row (|---|---|...) found"
datarows=$(echo "$out1" | grep -cE '^\| *[a-z]+ *\|')
[ "$datarows" -ge 1 ] && ok "has at least one data row (found $datarows)" || no "found zero data rows"

echo "== T3: running twice in a row is byte-identical (idempotency) =="
out2=$(cd "$ROOT" && "$SCRIPT")
if [ "$out1" = "$out2" ]; then
  ok "two consecutive runs produced byte-identical output"
else
  no "two consecutive runs DIFFERED"
  diff <(printf '%s' "$out1") <(printf '%s' "$out2") | head -20
fi

echo "== T4: a role with a real registered row survives roundtrip (spot-check on a known role) =="
# 'cio' is guaranteed present (this worktree's own role) with a real carry-forward file.
echo "$out1" | grep -qE '^\| *cio *\|' && ok "cio's row is present" || no "cio's row is missing from output"

echo "== T5: does not crash on a registry role with NO carry-forward file (scratch copy, real file untouched) =="
SCRATCH=$(mktemp -d)
cp "$ROOT/dev/active/duty-cycle-registry.tsv" "$SCRATCH/duty-cycle-registry.tsv"
# Append a fake role with no corresponding dev/active/zzztest-carry-forward.md anywhere.
printf 'zzztest\t99 6\t7\t6\t22\t06:99\t2026-08-29\n' >> "$SCRATCH/duty-cycle-registry.tsv"
if grep -q '^zzztest' "$ROOT/dev/active/duty-cycle-registry.tsv" 2>/dev/null; then
  no "SAFETY: zzztest leaked into the REAL registry file — aborting further T5 assertions"
else
  ok "real registry file untouched (zzztest not present in it)"
fi
[ -f "$ROOT/dev/active/zzztest-carry-forward.md" ] && no "SAFETY: a real zzztest-carry-forward.md exists — unexpected" || ok "confirmed zzztest has no real carry-forward file"

out5=$(cd "$ROOT" && COHORT_POSITION_REGISTRY="$SCRATCH/duty-cycle-registry.tsv" "$SCRIPT" 2>/tmp/cohort-position-t5-stderr.$$)
rc5=$?
[ "$rc5" -eq 0 ] && ok "still exits 0 with a missing-carry-forward role in the roster" || no "exit code was $rc5 with a missing-carry-forward role (stderr: $(cat /tmp/cohort-position-t5-stderr.$$))"
rm -f "/tmp/cohort-position-t5-stderr.$$"
echo "$out5" | grep -qE '^\| *zzztest *\|' && ok "zzztest's row is present in the output" || no "zzztest's row is missing entirely"
echo "$out5" | grep 'zzztest' | grep -q 'no carry-forward file' && ok "zzztest's row honestly says no carry-forward file was found (not fabricated)" || no "zzztest's row did not say 'no carry-forward file' — check for fabrication"
echo "$out5" | grep 'zzztest' | grep -qE '\| *n/a \(no file\) *\|' && ok "zzztest's Stale? column reads n/a (no file), not a fabricated yes/no" || no "zzztest's Stale? column did not read n/a (no file)"

echo "== T6: a role marked 'parked' in the registry reports Stale?=parked, not yes/no (scratch copy) =="
SCRATCH6=$(mktemp -d)
cp "$ROOT/dev/active/duty-cycle-registry.tsv" "$SCRATCH6/duty-cycle-registry.tsv"
printf 'zzzparked\t99 6\t7\t6\t22\t06:99\t2026-08-29\tparked: test fixture\n' >> "$SCRATCH6/duty-cycle-registry.tsv"
out6=$(cd "$ROOT" && COHORT_POSITION_REGISTRY="$SCRATCH6/duty-cycle-registry.tsv" "$SCRIPT" 2>/dev/null)
rc6=$?
[ "$rc6" -eq 0 ] && ok "still exits 0 with a parked role in the roster" || no "exit code was $rc6 with a parked role"
echo "$out6" | grep -qE '^\| *zzzparked *\| .* \| *parked *\|' && ok "parked role's Stale? column reads 'parked'" || no "parked role's Stale? column did not read 'parked' (got: $(echo "$out6" | grep zzzparked))"
rm -rf "$SCRATCH6"

echo "== T7: malformed / truncated registry line (missing trailing columns) doesn't crash =="
SCRATCH7=$(mktemp -d)
printf 'role\tcron_expr\tthreshold_h\twake_start\twake_end\tfirst_fire\tactive_since\n' > "$SCRATCH7/duty-cycle-registry.tsv"
printf 'zzzshort\n' >> "$SCRATCH7/duty-cycle-registry.tsv"   # a role row with only 1 column, no tabs at all
out7=$(cd "$ROOT" && COHORT_POSITION_REGISTRY="$SCRATCH7/duty-cycle-registry.tsv" "$SCRIPT" 2>&1)
rc7=$?
[ "$rc7" -eq 0 ] && ok "does not crash on a malformed (single-column) registry row" || no "exit code was $rc7 on a malformed registry row"
rm -rf "$SCRATCH7"

echo ""
echo "==================== RESULT: $PASS passed, $FAIL failed ===================="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
