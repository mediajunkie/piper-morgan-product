#!/usr/bin/env bash
# Regression test for the FALSE-STALE bug PM caught 2026-06-22.
#
# Symptom: ppm was flagged 40h-stale by the freeze-check while it was firing every
# cycle. Two migration-era assumptions in duty-cycle-freeze-check.sh caused it:
#   (1) age_of() found a heartbeat ONLY from a "(role)"-tagged commit message — it
#       missed ppm's "docs(session): PPM …" tag style → looked dead.
#   (2) cycling_now() matched ONLY "${role}-code-opus-log.md" — it missed Sonnet-model
#       logs (…-code-sonnet-log.md) → the live session log was invisible.
# Fix (commit a92619f9b): age_of() also reads the role's session-log path as a heartbeat
# (ANY model), and cycling_now() matches "${role}-code-.*log.md" (any model).
#
# This test reproduces a role that is cycling via a SONNET log under an UNTAGGED commit
# (exactly the ppm shape) and asserts it is NOT flagged stale; plus a negative control
# (a genuinely old heartbeat MUST still be flagged), so the fix can't regress to either
# a false-positive or a false-negative.
set -uo pipefail

FC="$(cd "$(dirname "$0")" && pwd)/duty-cycle-freeze-check.sh"
today=$(date +%Y/%m/%d); today_dash=$(date +%Y-%m-%d)
PASS=0; FAIL=0; TMPS=()
ok(){ echo "  ✓ $1"; PASS=$((PASS+1)); }
no(){ echo "  ✗ $1"; FAIL=$((FAIL+1)); }
cleanup(){ for d in "${TMPS[@]:-}"; do [ -n "$d" ] && rm -rf "$d"; done; }
trap cleanup EXIT INT TERM

# Build a fixture repo (bare origin + clone) whose testrole TODAY session log is a
# SONNET log committed at $1 (unix epoch seconds), under an UNTAGGED "docs(session): …"
# message. Epoch + "+0000" is the portable GIT_*_DATE form (approxidate is rejected on
# some gits). Echoes the clone path (use as PIPER_REPO).
mkfixture(){
  local when="$1" TMP; TMP=$(mktemp -d); TMPS+=("$TMP")
  git init --bare -q "$TMP/o.git"
  git clone -q "$TMP/o.git" "$TMP/w" 2>/dev/null
  ( cd "$TMP/w"
    git config user.email t@t.test; git config user.name tester
    mkdir -p "dev/$today"
    echo "# session log testrole (sonnet)" > "dev/$today/${today_dash}-testrole-code-sonnet-log.md"
    git add -A
    GIT_AUTHOR_DATE="@$when +0000" GIT_COMMITTER_DATE="@$when +0000" \
      git commit -qm "docs(session): TestRole afternoon work"   # NO "(testrole)" tag — the ppm shape
    git push -q origin HEAD:main 2>/dev/null )
  echo "$TMP/w"
}

# A registry with just testrole: cron, threshold 6h, window 0–24, first_fire 00:00 (past), since today.
mkreg(){ local TMP="$1"; printf 'role\tcron\tthr\tws\twe\tff\tsince\n' > "$TMP/reg.tsv"
         printf 'testrole\t0 7,13\t6\t0\t24\t00:00\t%s\n' "$today_dash" >> "$TMP/reg.tsv"; echo "$TMP/reg.tsv"; }

echo "freeze-check false-stale regression:"

# Test 1 — REGRESSION: fresh sonnet log + untagged commit → must NOT be stale.
W=$(mkfixture "$(date +%s)"); R=$(mkreg "$(dirname "$W")")
out=$(PIPER_REPO="$W" DUTY_CYCLE_REGISTRY="$R" bash "$FC" 2>/dev/null)
[ -z "$out" ] && ok "live role (sonnet log, untagged commit) → not flagged" \
              || no "FALSE-STALE regressed — flagged a live role: $out"

# Test 2 — NEGATIVE CONTROL: same shape but heartbeat 10h old → MUST be flagged stale.
W=$(mkfixture "$(( $(date +%s) - 36000 ))"); R=$(mkreg "$(dirname "$W")")
out=$(PIPER_REPO="$W" DUTY_CYCLE_REGISTRY="$R" bash "$FC" 2>/dev/null)
echo "$out" | grep -q "STALE testrole" && ok "genuinely-stale role (10h) → correctly flagged" \
                                        || no "FALSE-NEGATIVE — missed a stale role: '${out:-<empty>}'"

echo "── $PASS passed, $FAIL failed ──"
[ "$FAIL" -eq 0 ]
