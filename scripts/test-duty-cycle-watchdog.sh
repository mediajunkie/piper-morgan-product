#!/usr/bin/env bash
# test-duty-cycle-watchdog.sh — isolated test for the watchdog v2 nudge logic (dedup / cooldown /
# infra-collapse / recovery). Uses WATCHDOG_DRYRUN (fires no belts) + a fixture detector + temp log/state.
set -uo pipefail
W="$(cd "$(dirname "$0")" && pwd)/duty-cycle-watchdog.sh"
[ -f "$W" ] || { echo "missing $W"; exit 1; }
T="$(mktemp -d "${TMPDIR:-/tmp}/wdtest.XXXXXX")"; trap 'rm -rf "$T"' EXIT
LOG="$T/log"; STATE="$T/state"; FIX="$T/fixture"
PASS=0; FAIL=0
ok(){ echo "  ✅ $1"; PASS=$((PASS+1)); }
no(){ echo "  ❌ $1"; FAIL=$((FAIL+1)); }
run(){ # $1 = fixture freeze-output, $2 = cooldown (default 21600)
  printf '%s' "$1" > "$FIX"
  WATCHDOG_DRYRUN=1 WATCHDOG_LOG="$LOG" WATCHDOG_STATE="$STATE" \
    WATCHDOG_NUDGE_COOLDOWN="${2:-21600}" WATCHDOG_INFRA_THRESHOLD=3 \
    WATCHDOG_FREEZE_CMD="cat '$FIX'" bash "$W"
}
lastlog(){ tail -1 "$LOG" 2>/dev/null; }

echo "── T1: cio newly stale → nudge (transition) ──"
run "STALE cio 9h (threshold 8h)
"
lastlog | grep -q "WOULD-NUDGE \[perrole\]: cio" && ok "nudged cio (perrole)" || no "didn't nudge cio → $(lastlog)"

echo "── T2: cio still stale, within cooldown → NO nudge (dedup) ──"
run "STALE cio 10h (threshold 8h)
"
lastlog | grep -q "no nudge" && ok "deduped within cooldown" || no "should dedup → $(lastlog)"

echo "── T3: cio still stale, cooldown=0 → re-nudge ──"
run "STALE cio 11h (threshold 8h)
" 0
lastlog | grep -q "WOULD-NUDGE" && ok "re-nudged after cooldown elapsed" || no "should re-nudge → $(lastlog)"

echo "── T4: 3 roles stale at once → infra-event framing ──"
: > "$STATE"
run "STALE cio 9h
STALE exec 7h
STALE ppm 8h
"
lastlog | grep -q "WOULD-NUDGE \[infra\]" && ok "infra-event framing (n_stale>=3)" || no "should be infra → $(lastlog)"

echo "── T5: all healthy → state cleared, no nudge ──"
run ""
[ ! -s "$STATE" ] && ok "state cleared when healthy" || no "state not cleared → $(cat "$STATE" 2>/dev/null)"

echo "── T6: recovered role drops from state; a new role nudges fresh ──"
: > "$STATE"; run "STALE cio 9h
" >/dev/null
run "STALE ppm 9h
"
lastlog | grep -q "WOULD-NUDGE \[perrole\]: ppm" && ok "new role (ppm) nudged" || no "ppm should nudge → $(lastlog)"
grep -q "^cio" "$STATE" 2>/dev/null && no "recovered cio still in state" || ok "recovered cio dropped from state"

echo "── T7: Belt 0 — DEFAULT OFF (disabled 6/28), but fires when explicitly enabled (=1) ──"
# T7a: default (no WATCHDOG_AUTO_FOREGROUND) → stale → NO foreground (the 6/28 disable)
: > "$LOG"; : > "$STATE"; run "STALE cio 9h
"
grep -q "WOULD-FOREGROUND" "$LOG" && no "Belt 0 fired by default — should be OFF since 6/28 → $(cat "$LOG")" || ok "Belt 0 OFF by default (disabled 6/28)"
# T7b: explicitly enabled (=1) → stale → foreground fires (mechanism preserved for single-window/Mac-Mini)
: > "$LOG"; : > "$STATE"; printf 'STALE cio 9h\n' > "$FIX"
WATCHDOG_DRYRUN=1 WATCHDOG_LOG="$LOG" WATCHDOG_STATE="$STATE" WATCHDOG_AUTO_FOREGROUND=1 \
  WATCHDOG_NUDGE_COOLDOWN=0 WATCHDOG_FREEZE_CMD="cat '$FIX'" bash "$W"
grep -q "WOULD-FOREGROUND" "$LOG" && ok "Belt 0 still fires when explicitly enabled (=1)" || no "Belt 0 didn't fire when enabled → $(cat "$LOG")"

echo "── T8: WATCHDOG_AUTO_FOREGROUND=0 → Belt 0 suppressed (toggle) ──"
: > "$LOG"; : > "$STATE"; printf 'STALE cio 9h\n' > "$FIX"
WATCHDOG_DRYRUN=1 WATCHDOG_LOG="$LOG" WATCHDOG_STATE="$STATE" WATCHDOG_AUTO_FOREGROUND=0 \
  WATCHDOG_NUDGE_COOLDOWN=0 WATCHDOG_FREEZE_CMD="cat '$FIX'" bash "$W"
grep -q "WOULD-FOREGROUND" "$LOG" && no "Belt 0 fired despite toggle off → $(cat "$LOG")" || ok "Belt 0 suppressed by toggle"

echo ""; echo "════ RESULT: $PASS passed, $FAIL failed ════"
[ "$FAIL" = 0 ] && exit 0 || exit 1
