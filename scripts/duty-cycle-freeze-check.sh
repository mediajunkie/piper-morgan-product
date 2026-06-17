#!/usr/bin/env bash
# duty-cycle-freeze-check.sh — detect a SILENTLY frozen duty cycle (the "never silently freeze" backstop).
#
# REGISTRY MODE (default): reads dev/active/duty-cycle-registry.tsv — the opt-in list of which roles to
#   watch, each with its OWN threshold + waking window. A role is checked only while it is ACTIVELY CYCLING
#   right now, which we derive from the session-log lifecycle the agent already maintains (Exec's
#   register/de-register intent, realized without a parallel mutation — m-36):
#     • today's session log for the role does NOT exist on origin/main  → hasn't STARTed yet → skip
#       (kills the morning false-positive: heartbeat is last night's STOP until the first fire creates the log)
#     • today's session log carries  <!-- DAY-CLOSED -->                → cleanly STOPped → skip
#       (kills the post-STOP / overnight false-positive)
#     • else (STARTed, not yet STOPped, inside the waking window)       → check heartbeat age vs threshold
#   A live cycle commits every fire (push-to-main-routinely), so age > threshold here = genuinely frozen.
#   An UNlisted role is never watched (not opted in / not migrated). Both v1 false-positives dissolve.
# LEGACY/TEST MODE: set DUTY_CYCLE_ROLES (+ optional DUTY_CYCLE_STALE_H / WAKE_START / WAKE_END) to force a
#   check of those roles against one global threshold, bypassing the registry AND the cycling-state gate.
#
# Heartbeat / session log / DAY-CLOSED are all read from origin/main (no working-tree currency dependency).
# Output: "STALE <role> <detail>" per frozen role; empty = healthy / off-hours / not-cycling. Exit 0 always
# (a watchdog must never fail loudly itself). A wrapper (launchd) turns STALE lines into the PM alert.
set -uo pipefail

REPO="${PIPER_REPO:-/Users/xian/Development/piper-morgan/piper-morgan-product}"
REG="${DUTY_CYCLE_REGISTRY:-$REPO/dev/active/duty-cycle-registry.tsv}"
now=$(date +%s); hour=$(date +%-H); today=$(date +%Y/%m/%d); today_dash=$(date +%Y-%m-%d)
git -C "$REPO" fetch origin main -q 2>/dev/null || true

# hours since the role's newest "(role)"-tagged commit on origin/main; non-zero exit if none found
age_of() {
  local role="$1" ct
  ct=$(git -C "$REPO" log origin/main -1 --format=%ct -F --grep="($role)" --since="9 days ago" 2>/dev/null)
  [ -z "$ct" ] && return 1
  echo $(( (now - ct) / 3600 ))
}

# is the role actively cycling right now? (today's session log on origin/main exists AND not yet DAY-CLOSED)
cycling_now() {
  local role="$1" path
  path=$(git -C "$REPO" ls-tree -r --name-only origin/main -- "dev/$today/" 2>/dev/null \
         | grep -E "${role}-code-opus-log\.md$" | head -1)
  [ -z "$path" ] && return 1                                                   # not STARTed today
  # match the CANONICAL close sentinel for TODAY only — `<!-- DAY-CLOSED: YYYY-MM-DD -->` — not a prose
  # mention of "DAY-CLOSED" (e.g. a continuity link to yesterday). A loose match here is a false-NEGATIVE
  # (watchdog skips a live-but-frozen role), so keep it strict.
  git -C "$REPO" show "origin/main:$path" 2>/dev/null | grep -q "<!-- DAY-CLOSED: $today_dash" && return 1
  return 0
}

# ── LEGACY / TEST mode (explicit env override; bypasses registry + cycling gate) ──
if [ -n "${DUTY_CYCLE_ROLES:-}" ]; then
  thr="${DUTY_CYCLE_STALE_H:-6}"; ws="${WAKE_START:-7}"; we="${WAKE_END:-23}"
  (( hour < ws || hour >= we )) && exit 0
  for role in $DUTY_CYCLE_ROLES; do
    if a=$(age_of "$role"); then (( a >= thr )) && echo "STALE $role ${a}h (threshold ${thr}h, test mode)"; fi
  done
  exit 0
fi

# ── REGISTRY mode (default) ──
[ -f "$REG" ] || exit 0
while IFS=$'\t' read -r role cron thr ws we since; do
  case "$role" in '#'*|''|role) continue ;; esac     # skip comments / blank / header
  [ -z "${we:-}" ] && continue                        # malformed row → skip
  (( hour < ws || hour >= we )) && continue           # outside this role's waking/alerting window
  cycling_now "$role" || continue                     # pre-START or post-STOP → not cycling now → skip
  if a=$(age_of "$role"); then
    (( a >= thr )) && echo "STALE $role ${a}h (threshold ${thr}h; cron '$cron')"
  else
    echo "STALE $role NO-HEARTBEAT (cycling today but no recent (${role})-tagged commit)"
  fi
done < "$REG"
exit 0
