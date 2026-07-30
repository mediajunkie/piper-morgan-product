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
  # v0.8 (2026-07-28): the HEARTBEAT surface. Work output is a valid liveness signal but not a
  # COMPLETE one -- a compliant quiet fire produces none, which is what made the belt alert on
  # compliance. A heartbeat line means "I woke up" and nothing more, which is exactly the claim
  # a liveness check needs. See scripts/duty-cycle-heartbeat.sh.
  ct3=$(git -C "$REPO" log origin/main -1 --format=%ct --since="9 days ago" -- "dev/heartbeats/*/${role}.tsv" 2>/dev/null)
  newest=$(printf '%s\n%s\n%s\n' "$ct" "$ct2" "$ct3" | grep -E '^[0-9]+$' | sort -nr | head -1)
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
  git -C "$REPO" show "origin/main:$path" 2>/dev/null | grep -qE "^<!-- DAY-CLOSED: $today_dash" && return 1
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
      # ⚠️ 2026-07-28 (CIO): was int(gap*3/2)+1. That is TIGHTER than the 2x-gap a single COMPLIANT
      # quiet fire produces, so a role following the no-churn rule in the skill tripped it by construction
      # (lead, 3x on 07-27, while alive and working). Widened to 2x+1 so one quiet fire is absorbed.
      # ⚠️ THIS IS THE LIVE VALUE. The threshold_h column in the registry is only a FALLBACK for crons that
      # do not parse — every current row parses, so editing that column changes NOTHING. It was edited
      # on 07-27 and announced as shipped; it was a no-op. Change the formula here, not the column.
      # ⚠️ Still does NOT fix low-frequency roles: exec fires 2x/day, so this yields 25h. Widening
      # cannot reconcile detect-fast with tolerate-quiet; the structural fix is the per-fire heartbeat
      # (HOST approved 07-28), which makes liveness independent of whether work happened.
      print int(gap*2) + 1
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

# ── HEARTBEAT-WRITER liveness, G6 (v0.8, 2026-07-28; HOST refinement c) ────────────────────────
# The heartbeat makes quiet fires visible -- but it introduces a new way to be silently wrong: if the
# WRITER breaks (script moved, push failing, path renamed), the files simply stop appearing, which is
# indistinguishable from a cohort that happens to be quiet. That is m-44 rebuilt inside the fix for
# m-44, so it gets designed in rather than retrofitted.
#
# The discriminator is cheap: heartbeats are per-role, so "one role missing" and "NOBODY wrote today"
# are different observations. The second cannot plausibly mean ten roles independently went quiet.
if [ "$hour" -ge 12 ]; then
  # wc -l, not `grep -c . || echo 0`: grep -c prints 0 AND exits 1 on no-match, so the fallback
  # fired too and produced the two-line string "0\n0", which `[` then rejected as non-integer.
  hb_today=$(git -C "$REPO" ls-tree --name-only origin/main "dev/heartbeats/$today_dash/" 2>/dev/null | wc -l | tr -d " ")
  hb_prev=$(git -C "$REPO" log origin/main --since="9 days ago" --format=%H -1 -- "dev/heartbeats/" 2>/dev/null)
  # ⚠️ 2026-07-29: this condition was WRONG on its first real day and false-alarmed on the busiest
  # day on record (122 role-tagged commits). HOST diagnosed it: its own two refinements conflict.
  #   (a) "a work commit IS the heartbeat" → --if-quiet suppresses the write whenever the role
  #       committed, so on any productive day the surface is LEGITIMATELY EMPTY.
  #   (c) "silence must be diagnostic" → alarm on an empty surface.
  # So (a) manufactures precisely the state (c) treats as a broken writer. Both were proposed in
  # adjacent paragraphs of one memo and I implemented both without noticing either.
  #
  # The fix follows from (a)'s own definition: if a commit is a heartbeat, an empty surface on a
  # COMMITTING day is correct. It is only suspicious when there are no heartbeats AND no commits —
  # i.e. genuinely no evidence of life from either source.
  hb_commits=$(git -C "$REPO" log origin/main --since="${today_dash}T00:00" --format=%s 2>/dev/null | grep -cE '\([a-z]+\)' || true)
  if [ "$hb_today" -eq 0 ] && [ -n "$hb_prev" ] && [ "${hb_commits:-0}" -eq 0 ]; then
    echo "HEARTBEAT-WRITER-SILENT — zero heartbeats AND zero role-tagged commits for $today_dash past midday, though the surface has been written before. Neither liveness source shows anything; a broken writer looks exactly like a quiet cohort, so do NOT read this as healthy until explained."
  fi
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
# ── SHOW YOUR WORK (v0.7, CIO 2026-07-27; principle from Janus/DinP after the 389-commit incident) ──
# Janus's cross-project rollup reported "no commits in 24h" on a day with 179. Cause: a bare `git log`
# with no ref, which defaults to HEAD — frozen at an early clone while origin/main moved 389 ahead.
# Its fetch worked; its READ was of the wrong ref. The failure output was silence, i.e. good news.
#
# That is the third silent-monitor failure in three days (this script's own exit-0-on-missing-path, the
# freeze-watchdog running on the retiring laptop, and Janus). Janus's proposed standing principle, which
# I am adopting here rather than only agreeing with: **a check must be able to positively assert WHAT IT
# LOOKED AT — ref, path, and how much it saw — not merely emit a binary clear/alert.** A check that
# cannot show its work is indistinguishable from one that never ran, and "clear" is the dangerous value
# because it is the one nobody investigates.
#
# Emitted on stderr so the STALE-only stdout contract the watchdog parses is unchanged.
# NOTE: no outer `2>/dev/null` here. The first cut wrapped this block in one to suppress git noise —
# which swallowed the very line it exists to print, shipping a show-your-work feature that showed
# nothing. Caught by running it. Suppress per-command, never around the reporting line itself.
_tip=$(git -C "$REPO" log origin/main -1 --format='%h %ad' --date=format:'%Y-%m-%d %H:%M' 2>/dev/null)
_n=$(grep -vcE '^(#|role|$)' "$REG" 2>/dev/null || echo 0)
echo "freeze-check: examined ref=origin/main tip=${_tip:-<NONE — could not read origin/main>} registry=$REG rows=${_n:-0} at $(date '+%Y-%m-%d %H:%M')" >&2

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
  # ── PARK-NO-EXIT detection (v0.6, CIO 2026-07-27; HOST-found, second design) ───────────────────
  # PARKED specified the STATE but not the REASON'S LIFECYCLE. A parked row whose reason has quietly
  # stopped being true is indistinguishable from a correctly-parked one — nobody reading
  # "parked: awaiting Amber migration" can tell it expired without independently checking whether the
  # migration happened. A LIVE role then sits unwatched behind a sentence that expired. Found 3 days
  # after PARKED shipped: arch and cxo were parked awaiting a migration they had ALREADY completed.
  #
  # FIRST ATTEMPT, DISCARDED — worth recording because it is the more obvious idea and it is wrong:
  # "a dark role does not commit, so flag any parked role that committed recently." That fires on
  # pa and ppm too, whose reasons are CORRECT — they are parked because their cron is un-armed, not
  # because they are dark, so they commit whenever prompted. Recent activity is NECESSARY but NOT
  # SUFFICIENT evidence that a park is stale, and shipping it would have re-created exactly the alert
  # fatigue PARKED exists to prevent. Two of four flags would have been noise on day one.
  #
  # WHAT ACTUALLY WORKS is syntactic and needs no judgment: a park reason MUST name a falsifiable
  # CLEARING CONDITION — the observable event that ends the park. pa/ppm already model it: "clear this
  # note only when a cron job is actually armed". arch/cxo state a SITUATION ("awaiting Amber
  # migration"), which can silently expire because nothing says what would end it. A situation rots;
  # a condition can be checked. So flag the reasons that have no exit, not the roles that look busy.
  case "${state:-watched}" in
    parked|parked:*)
      reason="${state#parked}"; reason="${reason#:}"
      if ! printf '%s' "$reason" | grep -qiE 'clear (this|the|it)|until|when .* (is|are|has|have)|expires?'; then
        echo "PARK-NO-EXIT $role — parked with no falsifiable clearing condition, so this row cannot go stale visibly. Reason on file: '${reason# }'"
      fi
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
