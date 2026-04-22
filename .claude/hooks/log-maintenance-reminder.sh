#!/usr/bin/env bash
# log-maintenance-reminder.sh — PostToolUse hook for Bash
#
# Fires after Bash tool calls. Uses a counter file to avoid noise —
# only reminds every 15 Bash calls. Checks whether a session log
# for today exists and was modified recently.
#
# Token budget: Under 200 characters when triggered.
# Safety: Must NEVER exit non-zero.

set -uo pipefail

PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
COUNTER_FILE="/tmp/piper-log-reminder-counter"

# ─── Increment counter ──────────────────────────────────────────────────────
COUNT=0
if [ -f "$COUNTER_FILE" ]; then
    COUNT=$(cat "$COUNTER_FILE" 2>/dev/null || echo 0)
fi
COUNT=$((COUNT + 1))
echo "$COUNT" > "$COUNTER_FILE"

# Only check every 15 Bash calls
if [ $((COUNT % 15)) -ne 0 ]; then
    exit 0
fi

# ─── Find today's session log ───────────────────────────────────────────────
TODAY=$(date +%Y-%m-%d)
YEAR=$(date +%Y)
MONTH=$(date +%m)
DAY=$(date +%d)

# Check both dev/YYYY/MM/DD/ and dev/active/ for today's logs
LOG_FILE=""
for dir in "$PROJECT_ROOT/dev/$YEAR/$MONTH/$DAY" "$PROJECT_ROOT/dev/active"; do
    if [ -d "$dir" ]; then
        FOUND=$(find "$dir" -name "*${TODAY}*log*" -type f 2>/dev/null | head -1)
        if [ -n "$FOUND" ]; then
            LOG_FILE="$FOUND"
            break
        fi
    fi
done

if [ -z "$LOG_FILE" ]; then
    echo "LOG REMINDER: No session log found for today ($TODAY). Create one before continuing."
    exit 0
fi

# ─── Check freshness ────────────────────────────────────────────────────────
NOW_EPOCH=$(date +%s)
if stat -f %m "$LOG_FILE" >/dev/null 2>&1; then
    MOD_EPOCH=$(stat -f %m "$LOG_FILE")
else
    MOD_EPOCH=$(stat -c %Y "$LOG_FILE")
fi
AGE_MINUTES=$(( (NOW_EPOCH - MOD_EPOCH) / 60 ))

if [ "$AGE_MINUTES" -gt 30 ]; then
    echo "LOG REMINDER: Session log last updated ${AGE_MINUTES}m ago. Add a timestamped entry for your recent work."
fi

exit 0
