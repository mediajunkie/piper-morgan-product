#!/usr/bin/env bash
# ci_liveness_check.sh — the "red nobody sees" detector (#1608).
#
# For every workflow in the repo: when did it last SUCCEED? A workflow whose
# last success is older than MAX_AGE_DAYS (or that has never succeeded in its
# recent runs) is flagged. Three instances earned this (see #1608): a gating
# workflow red 2 days (#1600), a publishing workflow dead 2.5 MONTHS
# (pages-build-deployment), and the inverted twin (#1593, green-that-lies —
# which THIS check cannot see; the ratchet gate in link-checker.yml is its
# companion. A liveness check alone reports that workflow healthy forever).
#
# Design constraints carried from the postmortem family:
#   - states its DENOMINATOR (workflows checked / flagged / dormant-ok) — m-44
#   - its own failure is LOUD: an API error exits non-zero, never "all clear"
#   - dormant-ok is an ALLOWLIST WITH REASONS, not a silent exclusion
#
# Usage: REPO=owner/name MAX_AGE_DAYS=10 scripts/ci_liveness_check.sh
# Exit: 0 = all live (and says how many it checked); 1 = flagged workflows
#       exist (list on stdout); 2 = the check itself could not measure.

set -u
REPO="${REPO:-mediajunkie/piper-morgan-product}"
MAX_AGE_DAYS="${MAX_AGE_DAYS:-10}"

# Deliberately-dormant workflows: name-pattern<TAB>reason. A row here is a
# CLAIM with an owner-visible reason, reviewed when this list changes — never
# a silent skip.
DORMANT_OK=$(cat <<'EOF'
Quarterly Maintenance Reminder	fires quarterly by design; 10-day liveness is the wrong clock for it
Monthly Housekeeping Audit	fires monthly by design
Windows Compatibility Tests	push-gated on rarely-touched paths; dormancy = no trigger, not death
EOF
)

now_epoch=$(date +%s)
flagged=0
checked=0
dormant=0
report=""

workflows_json=$(gh api "repos/$REPO/actions/workflows?per_page=100" 2>/dev/null)
if [ -z "$workflows_json" ]; then
  echo "LIVENESS CHECK FAILED TO MEASURE: workflows API returned nothing — this is NOT an all-clear" >&2
  exit 2
fi

total=$(echo "$workflows_json" | python3 -c "import json,sys; print(len(json.load(sys.stdin)['workflows']))")

while IFS=$'\t' read -r wf_id wf_name wf_state; do
  [ -z "$wf_id" ] && continue
  # disabled workflows are their own (visible) state — skip but count
  if [ "$wf_state" != "active" ]; then
    dormant=$((dormant+1))
    report="$report
- ⚪ $wf_name — state=$wf_state (visible in the Actions UI; not a silent death)"
    continue
  fi
  # EXACT name match on field 1 — a substring match here silently dormant-ok'd
  # "Tests" via the "Windows Compatibility Tests" row on this script's very
  # first run: a false clear inside the false-clear detector. Caught by
  # reading the first run's output against the workflow list, not by tests.
  if echo "$DORMANT_OK" | cut -f1 | grep -qxF "$wf_name"; then
    dormant=$((dormant+1))
    reason=$(echo "$DORMANT_OK" | awk -F'\t' -v n="$wf_name" '$1==n{print $2}')
    report="$report
- 💤 $wf_name — dormant-ok: $reason"
    continue
  fi
  checked=$((checked+1))
  last_success=$(gh api "repos/$REPO/actions/workflows/$wf_id/runs?status=success&per_page=1" \
    --jq '.workflow_runs[0].created_at // ""' 2>/dev/null)
  rc=$?
  if [ $rc -ne 0 ]; then
    echo "LIVENESS CHECK FAILED TO MEASURE runs for '$wf_name' — refusing to report it healthy" >&2
    exit 2
  fi
  if [ -z "$last_success" ]; then
    flagged=$((flagged+1))
    report="$report
- 🔴 **$wf_name** — NO successful run on record at all"
    continue
  fi
  s_epoch=$(python3 -c "from datetime import datetime; print(int(datetime.fromisoformat('$last_success'.replace('Z','+00:00')).timestamp()))")
  age_days=$(( (now_epoch - s_epoch) / 86400 ))
  if [ "$age_days" -gt "$MAX_AGE_DAYS" ]; then
    flagged=$((flagged+1))
    report="$report
- 🔴 **$wf_name** — last success $age_days days ago ($last_success)"
  fi
done < <(echo "$workflows_json" | python3 -c "
import json, sys
for w in json.load(sys.stdin)['workflows']:
    print(f\"{w['id']}\t{w['name']}\t{w['state']}\")")

echo "## CI liveness (#1608) — denominator: $total workflows total; $checked liveness-checked, $dormant dormant-ok/disabled, threshold ${MAX_AGE_DAYS}d"
echo "$report"
echo
if [ "$flagged" -gt 0 ]; then
  echo "RESULT: $flagged workflow(s) FLAGGED — red nobody sees, until now"
  exit 1
fi
echo "RESULT: all $checked checked workflows have a success within ${MAX_AGE_DAYS}d (this line asserts a measurement, not an absence of news)"
exit 0
