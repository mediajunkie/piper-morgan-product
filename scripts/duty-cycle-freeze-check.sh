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

# REPO resolution (v0.5, CIO 2026-07-26) — was a single hard-coded LAPTOP path. On Amber that path does
# not exist, so the `[ -f "$REG" ] || exit 0` below fired and the check exited 0 printing NOTHING — i.e.
# "registry missing" and "cohort all healthy" were byte-identical outputs. A hand-run on Amber returned a
# silent false all-clear. Now: try known checkouts in order, and FAIL LOUDLY if none has the registry.
REPO="${PIPER_REPO:-}"
if [ -z "$REPO" ]; then
  for cand in /Users/xian/Development/piper-morgan-product \
              /Users/xian/Development/piper-morgan/piper-morgan-product; do
    [ -f "$cand/dev/active/duty-cycle-registry.tsv" ] && { REPO="$cand"; break; }
  done
fi
REG="${DUTY_CYCLE_REGISTRY:-$REPO/dev/active/duty-cycle-registry.tsv}"
FIRST_FIRE_GRACE_MIN="${FIRST_FIRE_GRACE_MIN:-10}"   # minutes past first_fire before a missing log = missed START
now=$(date +%s); hour=${FREEZE_CHECK_NOW_HOUR:-$(date +%-H)}; min=$(date +%-M); now_min=$(( hour * 60 + min ))
today=$(date +%Y/%m/%d); today_dash=$(date +%Y-%m-%d)
git -C "$REPO" fetch origin main -q 2>/dev/null || true

# hours since the role's newest heartbeat on origin/main; non-zero exit if none found.
# Heartbeat = the more-recent of: (a) a "(role)"-tagged commit message, OR (b) any commit touching the
# role's session log (ANY model — opus/sonnet/…). (b) is robust to commit-tag drift — e.g. ppm's
# "docs(session): PPM …" style, which (a)'s "(ppm)" grep misses. (CIO fix 2026-06-22, after ppm
# false-staled 40h while firing every cycle — PM caught it; the (role)-grep + opus-only assumptions
# were migration-era and broke as roles moved to Sonnet + the session-commit tag style.)
age_of() {
  local role="$1" ct ct2 newest
  ct=$(git -C "$REPO" log origin/main -1 --format=%ct -F --grep="($role)" --since="9 days ago" 2>/dev/null)
  ct2=$(git -C "$REPO" log origin/main -1 --format=%ct --since="9 days ago" -- ":(glob)dev/**/*-${role}-code-*log.md" 2>/dev/null)
  newest=$(printf '%s\n%s\n' "$ct" "$ct2" | grep -E '^[0-9]+$' | sort -nr | head -1)
  [ -z "$newest" ] && return 1
  echo $(( (now - newest) / 3600 ))
}

# should this role be checked right now? args: role, first_fire(HH:MM). 0 = check, 1 = skip.
cycling_now() {
  local role="$1" ff="$2" path ff_h ff_m ff_min
  path=$(git -C "$REPO" ls-tree -r --name-only origin/main -- "dev/$today/" 2>/dev/null \
         | grep -E "${role}-code-.*log\.md$" | head -1)   # any model (opus/sonnet/…), not opus-only
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

# v0.4 (2026-06-26) — WAKE-WINDOW-AWARE threshold derived from the role's OWN cron cadence.
# A flat per-role threshold is wrong in both directions: too coarse for a daytime stall (Arch 6/25 — a
# 13.5h daytime stall a flat 8h flagged late; PM beat it at 5.4h) AND too tight overnight (legit overnight
# gaps false-flag). Fix: from the cron's hour-list, find the EXPECTED inter-fire gap that BRACKETS the
# current hour, and flag at ~1.5x that gap + 1h grace. Daytime = dense fires → small gap → tight threshold;
# overnight = one big gap → wide threshold. Self-adjusts per role from its own cron; no manual day/night
# columns. Falls back to the registry flat $thr if the cron hour-list can't be parsed.
# args: now_hour, cron_expr ("MIN HOURS …"), fallback_thr → echoes the effective threshold (hours).
expected_threshold() {
  # All logic runs in awk BEGIN, so inputs come via -v (NOT $0 — $0 is empty in BEGIN).
  awk -v cron="$2" -v nh="$1" -v fb="$3" 'BEGIN {
      if (split(cron, parts, " ") < 2) { print fb; exit }    # cron = "MIN HOURS …"; need the HOURS field
      n = split(parts[2], h, ",")
      if (n < 2) { print fb; exit }                          # single-fire / unparseable → fallback
      for (i=1;i<=n;i++) if (h[i] !~ /^[0-9]+$/) { print fb; exit }
      for (i=1;i<=n;i++) h[i] = h[i] + 0; nh = nh + 0         # numeric coercion (else awk string-compares "10"<"5")
      for (i=1;i<=n;i++) for (j=i+1;j<=n;j++) if (h[j]<h[i]) { t=h[i]; h[i]=h[j]; h[j]=t }
      prev=""; nxt=""
      for (i=1;i<=n;i++) if (h[i] <= nh) prev=h[i]            # latest fire-hour at/before now
      for (i=1;i<=n;i++) if (h[i] >  nh) { nxt=h[i]; break }   # earliest fire-hour after now
      if (prev=="") prev = h[n] - 24                          # before first fire today → last fire yesterday
      if (nxt=="")  nxt  = h[1] + 24                          # after last fire today  → first fire tomorrow
      gap = nxt - prev; if (gap < 1) gap = 1
      print int(gap*3/2) + 1                                  # ~1.5x expected gap + 1h grace
  }'
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
# FAIL LOUDLY, never silently (v0.5). An unreadable registry means this instrument measured NOTHING;
# exiting 0 made that indistinguishable from "measured, all clear" — the same silent-partial-input class
# as the MEMORY.md truncation. A monitor that cannot find its own input must SAY SO, not report calm.
if [ ! -f "$REG" ]; then
  echo "FREEZE-CHECK ERROR: registry not found at '${REG:-<unset>}' — this check measured NOTHING." >&2
  echo "  Set PIPER_REPO to a checkout containing dev/active/duty-cycle-registry.tsv, or DUTY_CYCLE_REGISTRY to the file." >&2
  exit 3
fi
while IFS=$'\t' read -r role cron thr ws we ff since state; do
  case "$role" in '#'*|''|role) continue ;; esac     # skip comments / blank / header
  [ -z "${ff:-}" ] && continue                        # malformed row (missing first_fire column) → skip
  # ── PARKED (v0.5, CIO 2026-07-26, HOST-proposed) ───────────────────────────────────────────────
  # Third state between "watched" and "no row". A deliberately-dark role (awaiting migration, paused
  # tier) is NOT watched for liveness — but it stays in the file and in coverage output, so it cannot
  # be silently forgotten. Before this, parking meant commenting the row out, which the `'#'*` case
  # above skips entirely → the role became structurally invisible, which is finding #6 exactly.
  # Rationale (HOST): a belt that cries wolf and a belt that is silent fail the SAME way — the cohort
  # stops treating its output as information. A mechanism's silence only means "clear" if you've
  # verified its coverage; its alarm only means "act" if you've distinguished expected-dark from failed.
  # Column 8 = `parked` or `parked:<reason>`; empty/absent → `watched` (so all pre-v0.5 rows are
  # unchanged in behavior). Coverage lines print ONLY under DUTY_CYCLE_COVERAGE=1, so the default
  # STALE-only output the watchdog consumes is byte-identical to before.
  case "${state:-watched}" in
    parked|parked:*)
      [ -n "${DUTY_CYCLE_COVERAGE:-}" ] && echo "PARKED $role (not watched — intentionally dark${state#parked}; since $since)"
      continue ;;
  esac
  (( hour < ws || hour >= we )) && continue           # outside this role's waking/alerting window
  cycling_now "$role" "$ff" || continue               # not-should-be-cycling now → skip
  if a=$(age_of "$role"); then
    thr_eff=$(expected_threshold "$hour" "$cron" "$thr")    # v0.4 wake-window-aware (falls back to flat $thr)
    (( a >= thr_eff )) && echo "STALE $role ${a}h (dyn-threshold ${thr_eff}h wake-window-aware; cron '$cron')"
  else
    echo "STALE $role NO-HEARTBEAT (should be cycling but no recent (${role}) commit or session-log update)"
  fi
done < "$REG"
exit 0
