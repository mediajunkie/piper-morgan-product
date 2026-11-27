#!/bin/bash
# Snapshots the "Building Piper Morgan" GitHub Projects v2 board (issue#, state, milestone,
# Sprint field value, title, labels, blocked_by) to a git-committed TSV file.
# labels: comma-joined, sorted (carries promise:<id>, journey:<moment>, seam:<name> for the
# living map, round 3). blocked_by: comma-joined issue numbers from GitHub's native
# issue-dependency relation (an edge means "must close before"; Arch, 10-24). Dates are Pacific.
#
# Why this exists: the Sprint field is a Projects v2 custom field with no history/audit trail
# of its own (confirmed empirically 2026-07-05 -- no REST timeline event, no Enterprise audit
# log on a personal-account repo, no GraphQL history field, exposes only current-state
# snapshots). It has been wiped project-wide twice: once ~2026-06-25 (cause unclear) and once
# 2026-07-05 (a full-replace updateProjectV2Field mutation -- see CLAUDE.md's CRITICAL warning).
# Running this script on a regular cadence turns "we lost the whole history" into "we lost
# whatever changed since the last snapshot" -- the git commit history of the output file
# becomes the durable, wipe-proof record the live field cannot provide on its own.
#
# Usage: ./scripts/snapshot-project-board.sh
# Output: dev/snapshots/project-board-YYYY-MM-DD.tsv (git-add + commit it after running)

set -euo pipefail

PROJECT_ID="PVT_kwHOADE-8s4A-JwA"
DATE=$(TZ=America/Los_Angeles date +%Y-%m-%d)
OUTDIR="dev/snapshots"
FINAL="$OUTDIR/project-board-${DATE}.tsv"
# Write to a temp file and move it into place only after every page arrived, so a dropped
# connection mid-run (seen 11-27: "unexpected EOF", "connection reset") exits non-zero
# and leaves the last good snapshot untouched instead of a silently partial one.
OUTFILE="$OUTDIR/.project-board-${DATE}.tsv.partial"
trap 'rm -f "$OUTFILE"' EXIT

mkdir -p "$OUTDIR"

echo "issue	state	milestone	sprint	title	labels	blocked_by	state_reason" > "$OUTFILE"

CURSOR=""
while : ; do
  if [ -z "$CURSOR" ]; then
    RESP=$(gh api graphql -f query='
    query($projectId: ID!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          items(first: 100) {
            pageInfo { hasNextPage endCursor }
            nodes {
              content {
                ... on Issue { number state stateReason title milestone { title } labels(first: 30) { nodes { name } } blockedBy(first: 30) { nodes { number } } }
              }
              fieldValues(first: 30) {
                nodes { ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2SingleSelectField { id } } } }
              }
            }
          }
        }
      }
    }' -f projectId="$PROJECT_ID")
  else
    RESP=$(gh api graphql -f query='
    query($projectId: ID!, $cursor: String!) {
      node(id: $projectId) {
        ... on ProjectV2 {
          items(first: 100, after: $cursor) {
            pageInfo { hasNextPage endCursor }
            nodes {
              content {
                ... on Issue { number state stateReason title milestone { title } labels(first: 30) { nodes { name } } blockedBy(first: 30) { nodes { number } } }
              }
              fieldValues(first: 30) {
                nodes { ... on ProjectV2ItemFieldSingleSelectValue { name field { ... on ProjectV2SingleSelectField { id } } } }
              }
            }
          }
        }
      }
    }' -f projectId="$PROJECT_ID" -f cursor="$CURSOR")
  fi

  echo "$RESP" | python3 -c "
import json, sys
SPRINT_FIELD_ID = 'PVTSSF_lAHOADE-8s4A-JwAzg2hWcg'  # the board's 'Sprint' single-select (epics; not Status, which is ...gxpGyU); its ID survives a rename
d = json.load(sys.stdin)
items = d['data']['node']['items']['nodes']
for it in items:
    c = it.get('content') or {}
    num = c.get('number')
    if num is None:
        continue
    state = c.get('state', '')
    milestone = (c.get('milestone') or {}).get('title', '')
    title = c.get('title', '').replace('\t', ' ')
    # Read the field by its ID, not its name, so a rename (Sprint -> Epic, xian 11-27) cannot blank the column.
    sprint = next((v.get('name', '') for v in (it.get('fieldValues') or {}).get('nodes', [])
                   if (v.get('field') or {}).get('id') == SPRINT_FIELD_ID), '')
    labels = ','.join(sorted(n['name'] for n in (c.get('labels') or {}).get('nodes', [])))
    blocked_by = ','.join(str(n['number']) for n in sorted((c.get('blockedBy') or {}).get('nodes', []), key=lambda n: n['number']))
    state_reason = c.get('stateReason') or ''
    print(f'{num}\t{state}\t{milestone}\t{sprint}\t{title}\t{labels}\t{blocked_by}\t{state_reason}')
" >> "$OUTFILE"

  HASNEXT=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['node']['items']['pageInfo']['hasNextPage'])")
  if [ "$HASNEXT" != "True" ]; then
    break
  fi
  CURSOR=$(echo "$RESP" | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['node']['items']['pageInfo']['endCursor'])")
done

FILLED_CHECK_FILE="$OUTFILE"
FILLED=$(awk -F'\t' 'NR>1 && $4!=""' "$OUTFILE" | wc -l | tr -d ' ')
if [ "$FILLED" = "0" ]; then
  echo "ERROR: no item carries a value in the Sprint/Epic field (ID PVTSSF_lAHOADE-8s4A-JwAzg2hWcg). The field was deleted or replaced; this snapshot is not a usable restore point." >&2
  exit 3
fi
mv "$OUTFILE" "$FINAL"
trap - EXIT
OUTFILE="$FINAL"
echo "Snapshot written to $OUTFILE ($(wc -l < "$OUTFILE") lines)"
echo "Remember to: git add $OUTFILE && git commit -m 'snapshot(board): project board state $DATE' && git push"
