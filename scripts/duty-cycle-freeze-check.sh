#!/usr/bin/env bash
# duty-cycle-freeze-check.sh — detect a SILENTLY frozen duty cycle (the "never silently freeze" backstop).
#
# REGISTRY MODE (default): reads dev/active/duty-cycle-registry.tsv — the opt-in list of which roles to
#   watch, each with its OWN threshold + waking window + first-fire time. A role is checked only while it
#   SHOULD be cycling, derived from the session-log lifecycle the agent already maintains (m-36):
#     • today's session log carries  <!-- DAY-CLOSED -->        → cleanly STOPped today → skip.
#     • no today-log AND before first_fire (+grace)             → legitimately not STARTed yet → skip
#         (kills the morning false-positive).
#     • no today-log AND PAST first_fire (+grace)               → SHOULD be cycling → CHECK heartbeat age.
#         This is the closed→never-restarted catch (Exec 2026-06-17): a role that cleanly STOPped, went
#         dormant overnight, and missed its morning START shows a stale heartbeat past first_fire → flagged.
#         (The prior "no today-log → always skip" rule let the load-bearing overnight-dormancy Gap-C through.)
#     • else (STARTed, not yet STOPped)                         → CHECK heartbeat age vs threshold.
#   A live cycle commits every fire (push-to-main-routinely), so age > threshold here = genuinely frozen.
#   An UNlisted role is never watched (not opted in / not migrated).
# LEGACY/TEST MODE: set DUTY_CYCLE_ROLES (+ optional DUTY_CYCLE_STALE_H / WAKE_START / WAKE_END) to force a
#   check of those roles against one global threshold, bypassing the registry AND the cycling-state gate.
#
# Heartbeat / session log / DAY-CLOSED are all read from origin/main (no working-tree currency dependency).
# Output: "STALE <role> <detail>" per frozen role; empty = healthy / off-hours / not-cycling. Exit 0 always
# (a watchdog must never fail loudly itself). A wrapper (launchd) turns STALE lines into the PM alert.
#
# COVERAGE BOUNDARY (CXO battery-outage 2026-06-18): this catches a session-freeze on a LIVE machine. It
# CANNOT catch a machine-death (battery/crash/logout) while it's happening — the launchd watcher runs ON the
# same machine, so it dies too; it can only alert AFTER the machine returns (the next run sees stale
# heartbeats). Machine-death detection during the outage requires an OFF-machine monitor (the Routines
# watchdog, PM-deferred $70/mo). Re-raise that only if outages recur or cost work.
#
# v0.3 ENHANCEMENT (HOST welfare-criteria, 2026-06-19) — multi-role simultaneous-silence flag: when the
# two-tier output (🟡 ≥threshold / 🔴 ≥1.5× OR no-heartbeat) lands, add a cohort-scale read: if ≥N roles
# go 🔴 at the SAME moment, that's an infrastructure event (the machine-death case above at cohort scale),
# NOT N individual failures — the dashboard should say "infrastructure event suspected (N roles silent
# since HH:MM)" rather than alarm on N agents. Gated on the welfare-criteria two-tier build; noted here so
# the implementer finds it. (HOST welfare-criteria v0.3; CIO freeze-registry lane.)
set -uo pipefail

REPO="${PIPER_REPO:-/Users/xian/Development/piper-morgan/piper-morgan-product}"
REG="${DUTY_CYCLE_REGISTRY:-$REPO/dev/active/duty-cycle-registry.tsv}"
FIRST_FIRE_GRACE_MIN="${FIRST_FIRE_GRACE_MIN:-10}"   # minutes past first_fire before a missing log = missed START
now=$(date +%s); hour=$(date +%-H); min=$(date +%-M); now_min=$(( hour * 60 + min ))
today=$(date +%Y/%m/%d); today_dash=$(date +%Y-%m-%d)
git -C "$REPO" fetch origin main -q 2>/dev/null || true

# hours since the role's newest "(role)"-tagged commit on origin/main; non-zero exit if none found
age_of() {
  local role="$1" ct
  ct=$(git -C "$REPO" log origin/main -1 --format=%ct -F --grep="($role)" --since="9 days ago" 2>/dev/null)
  [ -z "$ct" ] && return 1
  echo $(( (now - ct) / 3600 ))
}

# should this role be checked right now? args: role, first_fire(HH:MM). 0 = check, 1 = skip.
cycling_now() {
  local role="$1" ff="$2" path ff_h ff_m ff_min
  path=$(git -C "$REPO" ls-tree -r --name-only origin/main -- "dev/$today/" 2>/dev/null \
         | grep -E "${role}-code-opus-log\.md$" | head -1)
  if [ -z "$path" ]; then
    # No today-log. Distinguish "legitimately pre-START" from "missed START → frozen" (Exec 2026-06-17 fix,
    # closes the closed→never-restarted blind spot — the overnight-dormancy Gap-C). Gate on first_fire+grace.
    ff_h=${ff%%:*}; ff_m=${ff##*:}
    (( now_min < 10#$ff_h * 60 + 10#$ff_m + FIRST_FIRE_GRACE_MIN )) && return 1   # before first START → skip
    return 0                                                                        # past first START, no log → CHECK
  fi
  # Has a today-log. Skip only if it carries the CANONICAL close sentinel for TODAY — not a prose mention of
  # "DAY-CLOSED" (e.g. a continuity link to yesterday). A loose match here is a false-NEGATIVE; keep it strict.
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
while IFS=$'\t' read -r role cron thr ws we ff since; do
  case "$role" in '#'*|''|role) continue ;; esac     # skip comments / blank / header
  [ -z "${ff:-}" ] && continue                        # malformed row (missing first_fire column) → skip
  (( hour < ws || hour >= we )) && continue           # outside this role's waking/alerting window
  cycling_now "$role" "$ff" || continue               # not-should-be-cycling now → skip
  if a=$(age_of "$role"); then
    (( a >= thr )) && echo "STALE $role ${a}h (threshold ${thr}h; cron '$cron')"
  else
    echo "STALE $role NO-HEARTBEAT (should be cycling but no recent (${role})-tagged commit)"
  fi
done < "$REG"
exit 0
