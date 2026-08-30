#!/usr/bin/env bash
# test-check-refresh-promises-state-files.sh — tests the --state-files mode added 2026-08-30
# (CXO's design, docs/internal/design/tracked-state-staleness-design-2026-08-29.md).
#
# check-refresh-promises.py computes its ROOT relative to its OWN file location, not an
# injectable env var — same constraint as test-check-refresh-promises-trigger-sent.sh, so this
# follows the same pattern: read-only checks against real dev/active/ state (cio and cio's own
# undeclared files, arch/cxo's real live adoptions), plus scratch fixture files under a disposable
# role prefix ("zzzteststate-") that no real role will ever collide with, cleaned up via trap
# regardless of pass/fail.
set -uo pipefail

CHECK="$(cd "$(dirname "$0")" && pwd)/check-refresh-promises.py"
[ -f "$CHECK" ] || { echo "missing $CHECK"; exit 1; }
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PASS=0; FAIL=0
FIXTURES=()
ok(){ echo "  PASS: $1"; PASS=$((PASS+1)); }
no(){ echo "  FAIL: $1"; FAIL=$((FAIL+1)); }
cleanup(){ for f in "${FIXTURES[@]:-}"; do [ -n "$f" ] && rm -f "$f"; done; }
trap cleanup EXIT INT TERM

echo "== T1: a real, undeclared file (cio's own) is reported UNDECLARED, not fabricated as current =="
out1=$(cd "$ROOT" && python3 "$CHECK" --state-files cio 2>&1)
rc1=$?
echo "$out1" | grep -q "cio-carry-forward.md — no currency_claim" && ok "cio-carry-forward correctly reported undeclared" || no "cio-carry-forward not reported undeclared: $out1"
[ "$rc1" -eq 0 ] && ok "exit 0 (undeclared is not a failure)" || no "non-zero exit on undeclared-only scope: $rc1"

echo "== T2: role-scoping actually scopes — cio scope must not mention cxo's real file =="
echo "$out1" | grep -q "cxo-carry-forward" && no "cio scope leaked cxo's file" || ok "cio scope correctly excludes cxo's file"

echo "== T3: full sweep (no role arg) picks up BOTH real live adopters (arch, cxo) as checked+current =="
out3=$(cd "$ROOT" && python3 "$CHECK" --state-files 2>&1)
rc3=$?
echo "$out3" | grep -q "arch-carry-forward.md" && echo "$out3" | grep -A1 "arch-carry-forward.md" | grep -q "current" \
  && ok "arch's real frontmatter reads current" || no "arch's real adoption did not read current: $(echo "$out3" | grep -A1 arch-carry-forward)"
echo "$out3" | grep -q "cxo-carry-forward.md" && echo "$out3" | grep -A1 "cxo-carry-forward.md" | grep -q "current" \
  && ok "cxo's real frontmatter reads current" || no "cxo's real adoption did not read current: $(echo "$out3" | grep -A1 cxo-carry-forward)"
[ "$rc3" -eq 0 ] && ok "full sweep exit 0 (both real declared claims are current)" || no "full sweep non-zero exit: $rc3"

echo "== T4: free-text currency_claim (arch's real wording, not the enum) is accepted, not rejected =="
# arch declared currency_claim as a free-text sentence, not one of per-stop/per-fire/per-day/none —
# a real divergence from the design doc's proposed enum, discovered using this test against real
# state. The checker must treat the claim as a display label, not validate it against a closed set.
echo "$out3" | grep -q "rewritten at substantive-change boundaries" && ok "free-text currency_claim (arch's real adoption) displayed, not rejected as malformed" || no "arch's free-text claim wording missing from output"

echo "== T5: STALE detection fires on a synthetic fixture past its own declared max_age_days =="
FIXTURE5="$ROOT/dev/active/zzzteststate-carry-forward.md"
FIXTURES+=("$FIXTURE5")
cat > "$FIXTURE5" <<'EOF'
---
last_updated: 2020-01-01
currency_claim: per-stop
max_age_days: 1
---
# scratch test fixture, safe to delete
EOF
out5=$(cd "$ROOT" && python3 "$CHECK" --state-files zzzteststate 2>&1)
rc5=$?
echo "$out5" | grep -q "STALE" && ok "reports STALE for a claim far past its own max_age_days" || no "expected STALE, got: $out5"
[ "$rc5" -eq 1 ] && ok "exit 1 when a declared claim is stale" || no "expected exit 1, got $rc5"
rm -f "$FIXTURE5"

echo "== T6: currency_claim: none is honest-declared, never a failure =="
FIXTURE6="$ROOT/dev/active/zzzteststate-carry-forward.md"
FIXTURES+=("$FIXTURE6")
cat > "$FIXTURE6" <<'EOF'
---
last_updated: 2020-01-01
currency_claim: none
---
# scratch test fixture, safe to delete — declares no currency claim at all
EOF
out6=$(cd "$ROOT" && python3 "$CHECK" --state-files zzzteststate 2>&1)
rc6=$?
echo "$out6" | grep -q "currency_claim: none, declared honest" && ok "currency_claim: none reported as declared-honest" || no "expected declared-honest bucket, got: $out6"
[ "$rc6" -eq 0 ] && ok "exit 0 (declared none is not a failure, even with an ancient last_updated)" || no "expected exit 0, got $rc6"
rm -f "$FIXTURE6"

echo "== T7: a file with last_updated but no currency_claim/max_age_days pair is UNDECLARED, not crashed =="
FIXTURE7="$ROOT/dev/active/zzzteststate-standing-items.md"
FIXTURES+=("$FIXTURE7")
cat > "$FIXTURE7" <<'EOF'
---
last_updated: 2026-08-30
---
# scratch test fixture — has last_updated but never migrated to the new claim/max_age fields
EOF
out7=$(cd "$ROOT" && python3 "$CHECK" --state-files zzzteststate 2>&1)
rc7=$?
echo "$out7" | grep -q "not yet migrated" && ok "partial frontmatter (last_updated only) reported as not-yet-migrated, not crashed" || no "expected not-yet-migrated message, got: $out7"
[ "$rc7" -eq 0 ] && ok "exit 0" || no "expected exit 0, got $rc7"
rm -f "$FIXTURE7"

echo "== T8: real registry file / real role files untouched by any fixture write =="
git -C "$ROOT" diff --stat -- dev/active/duty-cycle-registry.tsv dev/active/cio-carry-forward.md dev/active/cio-standing-items.md dev/active/arch-carry-forward.md dev/active/cxo-carry-forward.md | grep -q . \
  && no "a real tracked file shows a diff after this test run" || ok "no real tracked-state file was modified by this test run"

echo ""
echo "==================== RESULT: $PASS passed, $FAIL failed ===================="
[ "$FAIL" -eq 0 ] && exit 0 || exit 1
