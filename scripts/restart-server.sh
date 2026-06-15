#!/bin/bash
#
# restart-server.sh — Brutally reliable Piper Morgan dev restart
#
# Issue #949: During M1 UAT we repeatedly hit:
#   - Stale .pyc cache serving old code after edits
#   - Orphaned uvicorn worker processes surviving pkill of parent
#   - Multiple project directories (one in /Users/xian/Development/...,
#     one in /Users/xian/cool/piper) confusing which code was running
#   - Server startup taking 10-15s but tests sent before health check
#     was ready, producing empty responses
#
# This script eliminates all of those failure modes:
#   1. Kills EVERY python process bound to port 8001, regardless of PID file
#   2. Verifies port is fully free before proceeding
#   3. Wipes .pyc cache from services/ and web/
#   4. Verifies CWD is the correct piper-morgan-product directory
#   5. Starts the server with PYTHONUNBUFFERED so logs flush in real time
#   6. Waits for /health to return 200 before declaring success
#   7. Reports the exact CWD, PID, and log file location of the new server
#
# Usage:
#   ./scripts/restart-server.sh             # Default (port 8001, log to /tmp)
#   LOG_FILE=/tmp/my-run.log ./scripts/restart-server.sh
#   PORT=8002 ./scripts/restart-server.sh   # Different port
#
# Exit codes:
#   0 — server is up and healthy
#   1 — could not free the port (something we couldn't kill is holding it)
#   2 — wrong working directory (no main.py found)
#   3 — venv missing or broken
#   4 — server failed to come up healthy within timeout

set -uo pipefail

# ── Configuration ─────────────────────────────────────────────────────────────

PORT="${PORT:-8001}"
LOG_FILE="${LOG_FILE:-/tmp/piper-server.log}"
HEALTH_TIMEOUT="${HEALTH_TIMEOUT:-30}"  # Max seconds to wait for health
POSTGRES_PORT="${POSTGRES_PORT:-5433}"  # Override if your .env disagrees

# Resolve script location to find project root reliably
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── Helpers ───────────────────────────────────────────────────────────────────

red()    { printf '\033[0;31m%s\033[0m\n' "$*"; }
green()  { printf '\033[0;32m%s\033[0m\n' "$*"; }
yellow() { printf '\033[0;33m%s\033[0m\n' "$*"; }
bold()   { printf '\033[1m%s\033[0m\n' "$*"; }

step() { bold "→ $*"; }

# ── 1. Verify CWD ─────────────────────────────────────────────────────────────

step "Verifying project root"
cd "$PROJECT_ROOT" || { red "✗ Could not cd to $PROJECT_ROOT"; exit 2; }

if [ ! -f "main.py" ]; then
    red "✗ main.py not found in $PROJECT_ROOT"
    red "  This script must run from a piper-morgan-product checkout."
    exit 2
fi

if [ ! -d "venv" ]; then
    red "✗ venv/ not found in $PROJECT_ROOT"
    red "  Run: python3 -m venv venv && ./venv/bin/pip install -r requirements.txt"
    exit 3
fi

green "✓ Project root: $PROJECT_ROOT"

# ── 2. Kill all server processes ──────────────────────────────────────────────

step "Killing existing server processes on port $PORT"

# First pass: anything bound to the port
PORT_PIDS="$(lsof -ti:$PORT 2>/dev/null || true)"
if [ -n "$PORT_PIDS" ]; then
    yellow "  Found PIDs on port $PORT: $PORT_PIDS"
    # shellcheck disable=SC2086
    kill -TERM $PORT_PIDS 2>/dev/null || true
    sleep 2
    # Force-kill anything still alive
    PORT_PIDS_REMAINING="$(lsof -ti:$PORT 2>/dev/null || true)"
    if [ -n "$PORT_PIDS_REMAINING" ]; then
        yellow "  Force-killing: $PORT_PIDS_REMAINING"
        # shellcheck disable=SC2086
        kill -KILL $PORT_PIDS_REMAINING 2>/dev/null || true
        sleep 1
    fi
fi

# Second pass: any python main.py processes (catches orphaned workers)
MAIN_PIDS="$(pgrep -f 'python.*main.py' 2>/dev/null || true)"
if [ -n "$MAIN_PIDS" ]; then
    yellow "  Found orphaned main.py PIDs: $MAIN_PIDS"
    # shellcheck disable=SC2086
    kill -KILL $MAIN_PIDS 2>/dev/null || true
    sleep 1
fi

# Third pass: verify nothing on the port
FINAL_CHECK="$(lsof -ti:$PORT 2>/dev/null || true)"
if [ -n "$FINAL_CHECK" ]; then
    red "✗ Port $PORT still occupied by PIDs: $FINAL_CHECK"
    red "  Manual intervention required. Try: lsof -i:$PORT"
    exit 1
fi

green "✓ Port $PORT is free"

# ── 3. Clear .pyc cache ───────────────────────────────────────────────────────

step "Clearing Python bytecode cache"

# We only clear caches under services/ and web/ — don't touch venv/.
PYC_BEFORE="$(find services/ web/ -name '*.pyc' 2>/dev/null | wc -l | tr -d ' ')"
PYCACHE_BEFORE="$(find services/ web/ -name '__pycache__' -type d 2>/dev/null | wc -l | tr -d ' ')"

find services/ web/ -name '*.pyc' -delete 2>/dev/null || true
find services/ web/ -name '__pycache__' -type d -exec rm -rf {} + 2>/dev/null || true

green "✓ Cleared $PYC_BEFORE .pyc files and $PYCACHE_BEFORE __pycache__ dirs"

# ── 4. Start the server ───────────────────────────────────────────────────────

step "Starting server (POSTGRES_PORT=$POSTGRES_PORT, log: $LOG_FILE)"

# Truncate log so we can tail cleanly
: > "$LOG_FILE"

# Use unbuffered output so logs appear in real time, not after exit.
# Strip inherited ANTHROPIC_* vars: a Claude Code shell exports an EMPTY ANTHROPIC_API_KEY
# (+ BASE_URL / AUTH_TOKEN / CUSTOM_HEADERS) that shadows the real key in .env (python-dotenv
# won't override an already-set var) → every LLM call fails with APIConnectionError. Diagnosed
# 2026-06-04 (CLAUDE.md). Streamlining #3 (6/15): makes the documented strip automatic.
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
    PYTHONUNBUFFERED=1 POSTGRES_PORT="$POSTGRES_PORT" \
    nohup ./venv/bin/python -u main.py > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

green "✓ Server starting (PID $SERVER_PID)"

# ── 5. Wait for health ────────────────────────────────────────────────────────

step "Waiting for health check (timeout: ${HEALTH_TIMEOUT}s)"

ELAPSED=0
HEALTHY=0
while [ "$ELAPSED" -lt "$HEALTH_TIMEOUT" ]; do
    if curl -s -f "http://localhost:$PORT/health" > /dev/null 2>&1; then
        HEALTHY=1
        break
    fi
    # Check the process is still alive
    if ! kill -0 "$SERVER_PID" 2>/dev/null; then
        red "✗ Server process died during startup (PID $SERVER_PID)"
        red "  Last 30 lines of $LOG_FILE:"
        tail -30 "$LOG_FILE" | sed 's/^/    /'
        exit 4
    fi
    sleep 1
    ELAPSED=$((ELAPSED + 1))
    if [ "$((ELAPSED % 5))" = "0" ]; then
        echo "  ... still waiting (${ELAPSED}s elapsed)"
    fi
done

if [ "$HEALTHY" -ne 1 ]; then
    red "✗ Server did not become healthy within ${HEALTH_TIMEOUT}s"
    red "  Last 30 lines of $LOG_FILE:"
    tail -30 "$LOG_FILE" | sed 's/^/    /'
    exit 4
fi

# ── 6. Verify the running PID matches what we started ────────────────────────

ACTUAL_PIDS="$(lsof -ti:$PORT 2>/dev/null | tr '\n' ' ')"
ACTUAL_CWD="$(lsof -p "$SERVER_PID" 2>/dev/null | awk '/cwd/ {print $NF; exit}')"

# ── 7. Report ─────────────────────────────────────────────────────────────────

echo
green "════════════════════════════════════════════════════════════════"
green "  ✓ Piper Morgan server restarted and healthy"
green "════════════════════════════════════════════════════════════════"
echo "  Started PID:    $SERVER_PID"
echo "  Port $PORT PIDs:    $ACTUAL_PIDS"
echo "  Server CWD:     ${ACTUAL_CWD:-(unknown)}"
echo "  Log file:       $LOG_FILE"
echo "  Health URL:     http://localhost:$PORT/health"
echo "  Time to ready:  ${ELAPSED}s"
echo
echo "  Tail logs:      tail -f $LOG_FILE"
echo "  Stop server:    kill $SERVER_PID  (or re-run this script)"
green "════════════════════════════════════════════════════════════════"

exit 0
