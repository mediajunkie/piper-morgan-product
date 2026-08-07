#!/usr/bin/env bash
# cohort-freeze-detect.sh v0.1 (CIO 2026-08-07) — PM-APPROVED 2026-08-07 via Exec.
#
# WHAT THIS IS FOR, AND WHY IT IS NOT THE FREEZE-CHECK
# On 2026-08-06 the whole cohort hit the account's weekly limit and was frozen from ~13:12 until the
# ~21:30 reset. Every cron kept firing into a wall. PM was the detector, after the fact.
#
# ⚠️ THE OBVIOUS DESIGN DOES NOT WORK, and the data says so plainly. "Many roles STALE at once" cannot
# detect this: measured across every ALERTED sweep on record, simultaneous-stale peaks at 3 and the
# freeze day produced 2 -- indistinguishable from an ordinary morning. The reason is structural:
# staleness is measured against a 7h threshold, and the freeze was SHORTER THAN THE THRESHOLD. It ended
# before anyone could look stale. A freeze is invisible to a staleness belt by construction.
#
# THE SIGNAL THAT DOES WORK is the heartbeat surface, and it is qualitatively different: during a freeze
# EVERY role stops emitting at once. Not "several roles cross a line" -- a total blackout.
#     08-06 (freeze):  06h×5 07h×5 09h×1 10h×4 13h×3  [14h-21h: ZERO]  22h×3
#     08-07 (normal):  06h×4 07h×5        10h×4 13h×3  16h×3
# So: count SCHEDULED fires in the window and EMISSIONS in the window. Many scheduled + zero emitted
# is an environment event. One role dark is the stall alert that already exists. Same data, different
# shape -- which is exactly how Exec framed PM's ask.
#
# ⭐ CONVERGENT DESIGN, credited: PPM proposed this same scheduled=/emitted= discrimination independently
# (registry state field, 2026-08-06) after observing the inverse case on their own seat -- fires QUEUED
# rather than dropped, so a 9-hour heartbeat gap was produced by a HEALTHY cron that simply got no turns.
# Their caveat is real and this design answers it by SCOPE rather than by cleverness: a gap on ONE seat
# means "no turns" and is ambiguous; ZERO emissions across EVERY watched role in a window with many
# scheduled fires is not something a busy session can produce. The cohort-wide denominator is what makes
# the signal unambiguous, which is why this must never be run per-role.
#
# ⚠️ STATES WHAT IT MEASURED, always (PM asked for this explicitly; it is m-44 as a requirement):
# every run prints window, roles considered, scheduled-fire count and emission count on stderr, so an
# all-clear can never be the ambiguous kind.
set -uo pipefail
# ⚠️ EXIT CODES ARE LOAD-BEARING AND A CRASH MUST NOT LOOK LIKE A FINDING.
#   0 = clear (or cannot-discriminate, which says so on stderr)
#   1 = COHORT-FREEZE detected
#   3 = could not measure -- registry unreadable, internal error, anything unexpected
# The first version of this script crashed on an empty bash array under `set -u` and exited 1, which a
# caller would have read as a detected freeze. Caught only because the known-negative test was run as
# well as the known-positive. Hence the trap: any unhandled error is 3, never 1.
trap 'rc=$?; [ "$rc" -ne 0 ] && [ "$rc" -ne 1 ] && echo "cohort-freeze: FAIL internal error rc=$rc (NOT a detection, NOT an all-clear)" >&2 && exit 3' ERR
REPO="${FREEZE_REPO:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)}"
REG="${DUTY_CYCLE_REGISTRY:-$REPO/dev/active/duty-cycle-registry.tsv}"
HB="${HEARTBEAT_DIR:-$REPO/dev/heartbeats}"
WINDOW_H="${COHORT_FREEZE_WINDOW_H:-4}"      # hours to look back
MIN_SCHED="${COHORT_FREEZE_MIN_SCHED:-6}"    # scheduled fires needed before "zero emissions" means anything
NOW_EPOCH="${COHORT_FREEZE_NOW:-$(date +%s)}"

[ -r "$REG" ] || { echo "cohort-freeze: FAIL cannot read registry $REG" >&2; exit 3; }

now_d=$(date -r "$NOW_EPOCH" +%Y-%m-%d 2>/dev/null || date -d "@$NOW_EPOCH" +%Y-%m-%d)
win_start=$(( NOW_EPOCH - WINDOW_H*3600 ))

# ── scheduled fires in the window, from each watched role's cron hours ──────────
sched=0; roles=0
while IFS=$'\t' read -r role cron _ _ _ _ _ state; do
  case "$role" in ''|'#'*|role) continue;; esac   # 'role' is the TSV HEADER, not a role: it is not a
                                                  # comment, so it silently inflated watched_roles to 12
                                                  # against a true roster of 11 on this tool's first run.
  case "${state:-watched}" in parked|parked:*) continue;; esac
  roles=$((roles+1))
  hours=$(printf '%s' "$cron" | awk '{print $2}')
  case "$hours" in *[!0-9,]*) continue;; esac      # ranges/unparseable → skip, do not guess
  IFS=',' read -ra HS <<< "$hours"
  [ "${#HS[@]}" -eq 0 ] && continue          # empty array is unbound under set -u; guard explicitly
  for h in ${HS[@]+"${HS[@]}"}; do
    for dayoff in 0 1; do
      t=$(date -j -f "%Y-%m-%d %H:%M:%S" "$now_d $(printf '%02d' "$h"):00:00" +%s 2>/dev/null) || continue
      t=$(( t - dayoff*86400 ))
      [ "$t" -ge "$win_start" ] && [ "$t" -le "$NOW_EPOCH" ] && sched=$((sched+1))
    done
  done
done < "$REG"

# ── emissions in the window, from the heartbeat surface ────────────────────────
emitted=0; emitters=""
for f in "$HB"/*/*.tsv; do
  [ -e "$f" ] || continue
  while IFS=$'\t' read -r ts who _; do
    [ -z "${ts:-}" ] && continue
    e=$(date -j -f "%Y-%m-%d %H:%M:%S" "$(printf '%s' "$ts" | awk '{print $1" "$2}')" +%s 2>/dev/null) || continue
    if [ "$e" -ge "$win_start" ] && [ "$e" -le "$NOW_EPOCH" ]; then
      emitted=$((emitted+1))
      case " $emitters " in *" $who "*) ;; *) emitters="$emitters $who";; esac
    fi
  done < "$f"
done

ws=$(date -r "$win_start" "+%Y-%m-%d %H:%M" 2>/dev/null || date -d "@$win_start" "+%Y-%m-%d %H:%M")
we=$(date -r "$NOW_EPOCH" "+%Y-%m-%d %H:%M" 2>/dev/null || date -d "@$NOW_EPOCH" "+%Y-%m-%d %H:%M")
echo "cohort-freeze: examined window=[$ws .. $we] (${WINDOW_H}h) watched_roles=$roles scheduled_fires=$sched emissions=$emitted emitters=[${emitters# }] min_sched=$MIN_SCHED" >&2

if [ "$sched" -lt "$MIN_SCHED" ]; then
  echo "INSUFFICIENT-SCHEDULE ($sched scheduled fires < $MIN_SCHED in window) — NOT an all-clear, this window cannot discriminate" >&2
  exit 0
fi
if [ "$emitted" -eq 0 ]; then
  echo "COHORT-FREEZE $sched scheduled fires across $roles watched roles in the last ${WINDOW_H}h, ZERO emissions. This is an ENVIRONMENT event (account limit / host outage), not N separate stalls — stand the cohort down and notify PM rather than alerting per-role."
  exit 1
fi
exit 0
