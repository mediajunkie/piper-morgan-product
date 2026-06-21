#!/usr/bin/env bash
# duty-cycle-watchdog.sh v2 — detect + NUDGE PM (desktop + mailbox memo), dedup'd + infra-collapsed.
#
# Run by launchd (a pure OS job — ZERO Claude agents, no persona-fork; the cure for the scheduled-task
# approach PM rejected 2026-06-14). Hourly it: fetches origin, runs the freeze-check, and on a NEWLY-stale
# role (or a cooldown re-ping) NUDGES PM via (1) a macOS desktop notification + (2) a durable PM-mailbox
# memo (push-to-ref, so PM sees it at session-start even when away from the desktop) + (3) Slack if
# configured. It does no duty-cycle work; the only repo state it writes is its audit log, its nudge-state
# file, and (via push-to-ref, touching no working tree) the alert memo it delivers to PM's inbox.
#
# v2 (2026-06-20, PM-requested after the v1 detected the ~26h cohort stall but only logged it — never
# reached PM, who re-prodded manually ~5×):
#   - FETCH origin before checking — v1 read a possibly-stale local origin/main ref → false-stale on a role
#     that was actively committing. The fetch makes heartbeats accurate during normal operation.
#   - DEDUP — nudge on TRANSITION into stale, not every hour (v1 fired hourly = notification fatigue);
#     re-ping only after a cooldown (default 6h) while still stale. Per-role state in a gitignored TSV.
#   - MAILBOX-MEMO belt — PM asked for "both"; durable, survives being away from the desktop.
#   - INFRA-EVENT collapse — >=N roles stale at once = "infrastructure event suspected" (one nudge, the
#     machine-asleep/backgrounded signature) not N alarms (HOST multi-role-silence flag; CIO freeze lane).
#
# Test hooks (used by scripts/test-duty-cycle-watchdog.sh): WATCHDOG_FREEZE_CMD overrides the detector;
# WATCHDOG_DRYRUN=1 logs "WOULD-NUDGE …" instead of firing belts (+ skips the fetch); WATCHDOG_LOG /
# WATCHDOG_STATE redirect the runtime files; WATCHDOG_NUDGE_COOLDOWN / WATCHDOG_INFRA_THRESHOLD tune.
#
# Design: docs/operations/duty-cycle design/wake-this-session-duty-cycle-design-2026-06-14.md
set -uo pipefail

REPO="${PIPER_REPO:-/Users/xian/Development/piper-morgan/piper-morgan-product}"
LOG="${WATCHDOG_LOG:-$REPO/dev/active/duty-cycle-watchdog.log}"
STATE="${WATCHDOG_STATE:-$REPO/dev/active/duty-cycle-watchdog-nudge-state.tsv}"
COOLDOWN="${WATCHDOG_NUDGE_COOLDOWN:-21600}"   # 6h re-ping while a role stays stale
INFRA_N="${WATCHDOG_INFRA_THRESHOLD:-3}"        # >=N simultaneous stale = infrastructure event
FREEZE_CMD="${WATCHDOG_FREEZE_CMD:-$REPO/scripts/duty-cycle-freeze-check.sh}"
DRYRUN="${WATCHDOG_DRYRUN:-0}"
ts=$(date '+%Y-%m-%d %H:%M:%S'); now=$(date +%s)

# Accurate heartbeats: refresh origin/main before checking (read-only; graceful if offline). Skip in dryrun.
[ "$DRYRUN" = 1 ] || git -C "$REPO" fetch origin main -q 2>/dev/null \
  || echo "$ts WARN: fetch failed (heartbeats may be stale this run)" >> "$LOG"

STALE=$(eval "$FREEZE_CMD" 2>/dev/null)
if [ -z "$STALE" ]; then
  : > "$STATE" 2>/dev/null || true   # all healthy → clear state so a future stall nudges fresh
  exit 0
fi
SUMMARY=$(echo "$STALE" | tr '\n' ';' | sed 's/;$//; s/"/\\"/g')
echo "$ts DETECT: $SUMMARY" >> "$LOG"

stale_roles=$(echo "$STALE" | sed -n 's/^STALE \([^ ]*\).*/\1/p')
n_stale=$(printf '%s\n' "$stale_roles" | grep -c .)

# Nudge-worthy = newly stale OR cooldown elapsed. awk does the assoc (bash 3.2 has no associative arrays)
# and rewrites the state to ONLY currently-stale roles (recovered roles drop out → re-stall nudges fresh).
nudge_roles=$(printf '%s\n' "$stale_roles" | awk -v now="$now" -v cd="$COOLDOWN" -v sf="$STATE" '
  BEGIN { while ((getline l < sf) > 0) { if (split(l,a,"\t")>=2) last[a[1]]=a[2] } close(sf) }
  { r=$1; if (r=="") next; prev=(r in last)?last[r]:0
    if (prev==0 || (now-prev)>=cd) { print r; cur[r]=now } else { cur[r]=prev } }
  END { t=sf".tmp"; for (r in cur) printf "%s\t%s\n", r, cur[r] > t; close(t) }
')
[ -f "$STATE.tmp" ] && mv "$STATE.tmp" "$STATE"

if [ -z "$nudge_roles" ]; then
  echo "$ts (no nudge — all $n_stale stale role(s) within ${COOLDOWN}s cooldown)" >> "$LOG"
  exit 0
fi
nudge_list=$(printf '%s ' $nudge_roles | sed 's/ *$//')

# Framing: infrastructure-event (many at once) vs per-role.
if [ "$n_stale" -ge "$INFRA_N" ]; then
  TITLE="🔴 Piper Morgan: infrastructure event suspected — $n_stale roles silent"
  BODY="$n_stale duty-cycle roles silent at once ($SUMMARY) — likely machine-asleep/backgrounded (cron-survives-doesn't-fire), not individual failures. One wake of the machine/app likely covers it."
else
  TITLE="⚠️ Piper Morgan: duty-cycle stall — $nudge_list"
  BODY="duty-cycle stall ($SUMMARY). The cron object likely survives; the session needs a prod/resume to wake it."
fi

# DRY-RUN (test): record the decision, fire nothing.
if [ "$DRYRUN" = 1 ]; then
  frame=$([ "$n_stale" -ge "$INFRA_N" ] && echo infra || echo perrole)
  echo "$ts WOULD-NUDGE [$frame]: $nudge_list (n_stale=$n_stale)" >> "$LOG"
  exit 0
fi

# Belt 1 — macOS desktop notification (immediate).
/usr/bin/osascript -e "display notification \"$BODY\" with title \"$TITLE\" sound name \"Basso\"" 2>/dev/null

# Belt 2 — durable PM-mailbox memo via push-to-ref (survives being away from the desktop).
MEMO="mailboxes/xian (ceo)/inbox/alert-duty-cycle-stall-$(date '+%Y-%m-%d-%H%M').md"
cat > "$REPO/$MEMO" <<EOF
---
from: duty-cycle-watchdog (automated)
to: xian (ceo)
date: $(date '+%Y-%m-%d')
subject: $TITLE
priority: high — automated freeze-watcher nudge
---

# $TITLE

$BODY

- **Detected**: $ts (freeze-watcher hourly run); thresholds per \`dev/active/duty-cycle-registry.tsv\`.
- **Newly nudge-worthy**: $nudge_list   ·   **all currently stale**: $SUMMARY
- **Action**: re-prod the listed role's session. If many at once, wake the machine/app — one wake covers it.

*(Automated nudge — duty-cycle-watchdog.sh. Dedup'd: re-pings ~$((COOLDOWN/3600))h while still stale. The nudge belt PM asked for 2026-06-20; both belts — desktop + this memo. We'll tune what works.)*
EOF
if PIPER_REPO="$REPO" "$REPO/scripts/mail-send.sh" "mail(watchdog): $TITLE" "$MEMO" >/dev/null 2>&1; then
  rm -f "$REPO/$MEMO"   # delivered to origin/main via push-to-ref; drop the local copy (no main-checkout residue)
  echo "$ts NUDGE sent — desktop + mailbox (roles: $nudge_list; n_stale=$n_stale)" >> "$LOG"
else
  rm -f "$REPO/$MEMO" 2>/dev/null
  echo "$ts NUDGE — desktop only (mail-send failed; roles: $nudge_list)" >> "$LOG"
fi

# Belt 3 — Slack incoming-webhook, if PM configured one (~/.piper-watchdog-slack-webhook).
HOOK_FILE="$HOME/.piper-watchdog-slack-webhook"
if [ -f "$HOOK_FILE" ]; then
  WEBHOOK=$(tr -d '[:space:]' < "$HOOK_FILE")
  [ -n "$WEBHOOK" ] && curl -s -m 10 -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\":rotating_light: ${TITLE} — ${SUMMARY}\"}" "$WEBHOOK" >/dev/null 2>&1
fi
exit 0
