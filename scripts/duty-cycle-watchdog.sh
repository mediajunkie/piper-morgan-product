#!/usr/bin/env bash
# duty-cycle-watchdog.sh — the "never silently freeze" watcher.
#
# Run by launchd (a pure OS job — ZERO Claude agents, so no persona-fork; this is the cure for the
# scheduled-task approach PM rejected 2026-06-14). It runs the freeze-check and, on a STALE result,
# alerts PM via a macOS desktop notification + (if configured) Slack. It does NO duty-cycle work and
# touches no repo state except appending to its own audit log — a smoke detector, never a worker.
#
# Design: docs/operations/duty-cycle design/wake-this-session-duty-cycle-design-2026-06-14.md
# Heartbeat/check: scripts/duty-cycle-freeze-check.sh (registry-driven per-role staleness; the watch list +
# per-role thresholds/windows live in dev/active/duty-cycle-registry.tsv — cio + exec as of 2026-06-16).
set -uo pipefail

REPO="${PIPER_REPO:-/Users/xian/Development/piper-morgan/piper-morgan-product}"
LOG="$REPO/dev/active/duty-cycle-watchdog.log"

STALE=$("$REPO/scripts/duty-cycle-freeze-check.sh" 2>/dev/null)
[ -z "$STALE" ] && exit 0          # all healthy / off-hours -> stay silent

# one-line, quote-safe summary for the notification payloads
SUMMARY=$(echo "$STALE" | tr '\n' ';' | sed 's/;$//; s/"/\\"/g')

# Belt 1 — macOS desktop notification (always; zero dependencies)
/usr/bin/osascript -e "display notification \"$SUMMARY\" with title \"⚠️ Piper Morgan: duty-cycle may be frozen\" sound name \"Basso\"" 2>/dev/null

# Belt 2 — Slack via an incoming-webhook URL, IF PM has configured one.
# To enable: create a Slack incoming webhook and write its URL to ~/.piper-watchdog-slack-webhook
# (Slack's own app then pushes the alert to PM's phone — phone-reach with no bot-token/user-id wiring.)
HOOK_FILE="$HOME/.piper-watchdog-slack-webhook"
if [ -f "$HOOK_FILE" ]; then
  WEBHOOK=$(tr -d '[:space:]' < "$HOOK_FILE")
  [ -n "$WEBHOOK" ] && curl -s -m 10 -X POST -H 'Content-type: application/json' \
    --data "{\"text\":\":rotating_light: Piper Morgan duty-cycle freeze suspected — ${SUMMARY}. Re-prod the role's session.\"}" \
    "$WEBHOOK" >/dev/null 2>&1
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') ALERT: $SUMMARY" >> "$LOG"
exit 0
