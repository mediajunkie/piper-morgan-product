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
OUTFILE="$OUTDIR/project-board-${DATE}.tsv"

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
              fieldValueByName(name: "Sprint") {
                ... on ProjectV2ItemFieldSingleSelectValue { name }
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
              fieldValueByName(name: "Sprint") {
                ... on ProjectV2ItemFieldSingleSelectValue { name }
              }
            }
          }
        }
      }
    }' -f projectId="$PROJECT_ID" -f cursor="$CURSOR")
  fi

  echo "$RESP" | python3 -c "
import json, sys
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
    sprint = (it.get('fieldValueByName') or {}).get('name', '')
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

echo "Snapshot written to $OUTFILE ($(wc -l < "$OUTFILE") lines)"
echo "Remember to: git add $OUTFILE && git commit -m 'snapshot(board): project board state $DATE' && git push"
