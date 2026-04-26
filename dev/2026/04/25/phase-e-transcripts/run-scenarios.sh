#!/usr/bin/env bash
# Phase E Colleague Test runner
# Reads scenarios.json, fires each at the local intent endpoint, captures verbatim response.
#
# PRE-REQ (one of):
#   1. Restart the running server with ENABLE_ETHICS_ENFORCEMENT=true:
#      kill <pid of stale main.py>
#      cd /Users/xian/Development/piper-morgan/piper-morgan-product
#      ENABLE_ETHICS_ENFORCEMENT=true python main.py &
#   2. OR run a fresh server on port 8002 in a separate terminal,
#      then change SERVER below to http://localhost:8002
#
# IMPORTANT: As of 2026-04-25 16:30, the existing server (PID 98441, started Apr 16)
# predates Phases A-D and DOES NOT have the redirect_context / FloorContext denial code.
# Running this against the stale server tests pre-#992 code, NOT the gate code.
# Verify the server has been restarted with the flag set BEFORE running this script.

set -euo pipefail

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
SCENARIOS="$SCRIPT_DIR/scenarios.json"
SERVER="${PHASE_E_SERVER:-http://localhost:8001}"
ENDPOINT="${SERVER}/api/v1/intent"
DATE_TAG=$(date +%Y%m%dT%H%M%S)

echo "Phase E Colleague Test Runner"
echo "Server: $SERVER"
echo "Endpoint: $ENDPOINT"
echo "Scenarios: $SCENARIOS"
echo "Output: $SCRIPT_DIR/run-${DATE_TAG}/"
echo ""

mkdir -p "$SCRIPT_DIR/run-${DATE_TAG}"

# Pre-flight: verify server is responsive
if ! curl -s -o /dev/null -w "%{http_code}" "$SERVER/api/v1/health" | grep -q 200; then
    echo "ERROR: $SERVER not responding on /api/v1/health"
    exit 1
fi
echo "Health check: OK"
echo ""

# Iterate scenarios
jq -c '.[]' "$SCENARIOS" | while read -r scenario; do
    id=$(echo "$scenario" | jq -r '.id')
    session_id=$(echo "$scenario" | jq -r '.session_id')
    user_id=$(echo "$scenario" | jq -r '.user_id')
    message=$(echo "$scenario" | jq -r '.message')
    expected_boundary=$(echo "$scenario" | jq -r '.expected_boundary')

    echo "=== Running: $id ==="
    echo "Expected: $expected_boundary"
    echo ""

    payload=$(jq -nc \
        --arg msg "$message" \
        --arg sid "$session_id" \
        --arg uid "$user_id" \
        '{message: $msg, session_id: $sid, user_id: $uid}')

    response=$(curl -s -X POST "$ENDPOINT" \
        -H "Content-Type: application/json" \
        -d "$payload")

    transcript="$SCRIPT_DIR/run-${DATE_TAG}/${id}.md"
    {
        echo "# Phase E Transcript: $id"
        echo ""
        echo "**Run timestamp**: $(date -u +%Y-%m-%dT%H:%M:%SZ)"
        echo "**Session ID**: $session_id"
        echo "**User ID**: $user_id"
        echo "**Expected boundary**: $expected_boundary"
        echo ""
        echo "## User Message"
        echo ""
        echo '```'
        echo "$message"
        echo '```'
        echo ""
        echo "## Piper Response (verbatim)"
        echo ""
        echo '```'
        echo "$response" | jq -r '.message // .'
        echo '```'
        echo ""
        echo "## Full API Response (debug)"
        echo ""
        echo '```json'
        echo "$response" | jq '.'
        echo '```'
    } > "$transcript"

    echo "Saved: $transcript"
    echo ""
done

echo "All scenarios complete. Transcripts in: $SCRIPT_DIR/run-${DATE_TAG}/"
echo ""
echo "Next: review transcripts, then PM/PPM/CXO score against R/C/T rubric."
