#!/usr/bin/env bash
# duty-cycle-freeze-check.sh — detect a SILENTLY frozen duty cycle (the "never silently freeze" backstop).
#
# Heartbeat = a role's most recent commit on origin/main. We mandate push-to-main-routinely, so a live
# cycle commits regularly; a frozen one stops. No dedicated heartbeat file needed.
#
# This is the CHECK only (implementation-agnostic). A watcher wraps it and, on STALE output, sends the
# alert (PushNotification + Slack). Recommended watcher = a launchd OS-job (zero Claude agents); a
# notify-only scheduled-task is the fallback. The watcher must NEVER do duty-cycle work — read + ping only.
#
# Output: one line per stale role  ->  "STALE <role> <hours>h"   (empty output = all healthy / off-hours)
# Exit 0 always (a watchdog must not fail loudly itself).
set -uo pipefail

REPO="${PIPER_REPO:-/Users/xian/Development/piper-morgan/piper-morgan-product}"
THRESHOLD_H="${DUTY_CYCLE_STALE_H:-6}"        # hours w/o a tagged commit = suspect freeze (>2 windowed gaps)
WAKE_START="${WAKE_START:-7}"; WAKE_END="${WAKE_END:-23}"   # only alert during waking hours (local time)
# Roles to watch. START CIO-ONLY (dogfood — the proven-frozen role). The full-cohort default over-flagged
# on test (host/cxo/ppm/arch/exec/web read "stale" but were merely quiet or not-yet-migrated, not frozen):
# a commit-tag heartbeat can't tell "frozen" from "idle / not currently cycling." Cohort extension needs
# active->silent transition detection (was-committing-recently, then stopped) or an explicit opt-in registry.
ROLES="${DUTY_CYCLE_ROLES:-cio}"

hour=$(date +%-H)
if (( hour < WAKE_START || hour >= WAKE_END )); then exit 0; fi   # quiet outside waking hours

git -C "$REPO" fetch origin main -q 2>/dev/null || true
now=$(date +%s)

for role in $ROLES; do
  # newest origin/main commit whose message carries the role tag "(role)" (e.g. "log(cio):", "mail(docs):")
  ct=$(git -C "$REPO" log origin/main -1 --format=%ct -F --grep="($role)" --since="7 days ago" 2>/dev/null)
  [ -z "$ct" ] && continue          # no recent tagged commit -> treat as not-cycling; skip (avoid false alarms)
  age_h=$(( (now - ct) / 3600 ))
  (( age_h >= THRESHOLD_H )) && echo "STALE $role ${age_h}h"
done
exit 0
