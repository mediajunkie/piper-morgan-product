#!/usr/bin/env python3
"""Restore the GitHub Projects v2 "Sprint" field from a dev/snapshots/project-board-*.tsv
backup, after a wipe (see CLAUDE.md's CRITICAL warning: updateProjectV2Field's full-replace
singleSelectOptions argument silently detaches every item's existing value project-wide, with
no ID-preserving path and no reversal via the API -- confirmed twice, ~2026-06-25 and 2026-07-05).

This is the restore half of the backup scripts/snapshot-project-board.sh produces. The snapshot
alone is not a recovery plan -- a spreadsheet of what things used to be is exactly what sat
unused for weeks after the first (2026-06-25) incident, because nothing could turn it back into
board state. This script closes that gap.

Safety model:
  - Reads the snapshot; pulls CURRENT live Sprint values for every issue in one paginated sweep.
  - Only ever touches an issue whose snapshot sprint is non-empty AND differs from live (a real
    drift, e.g. wiped-to-empty, or something changed since the snapshot was taken).
  - Never invents a value for an issue the snapshot itself shows as sprint-less -- restoring
    "nothing" is a no-op, not an assignment.
  - Mutates one item at a time via updateProjectV2ItemFieldValue (the only safe primitive) --
    never a full-field replace.
  - DRY RUN BY DEFAULT. Pass --apply to actually mutate. Always re-verifies live after applying
    and reports any mismatch rather than trusting the mutation's own success response.

Usage:
  python3 scripts/restore-sprint-field-from-snapshot.py                    # dry-run, latest snapshot
  python3 scripts/restore-sprint-field-from-snapshot.py --snapshot PATH    # dry-run, specific file
  python3 scripts/restore-sprint-field-from-snapshot.py --apply           # actually restore
"""
import argparse
import glob
import json
import subprocess
import sys
from collections import defaultdict

PROJECT_ID = "PVT_kwHOADE-8s4A-JwA"
FIELD_ID = "PVTSSF_lAHOADE-8s4A-JwAzg2hWcg"

MUTATION = """
mutation($project: ID!, $item: ID!, $field: ID!, $value: String!) {
  updateProjectV2ItemFieldValue(input: {
    projectId: $project, itemId: $item, fieldId: $field,
    value: { singleSelectOptionId: $value }
  }) { projectV2Item { id } }
}
"""


def run_gh_graphql(query, **variables):
    args = ["gh", "api", "graphql", "-f", f"query={query}"]
    for k, v in variables.items():
        args += ["-f", f"{k}={v}"]
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"gh api graphql failed: {result.stderr[:500]}")
    return json.loads(result.stdout)


def find_latest_snapshot():
    files = sorted(glob.glob("dev/snapshots/project-board-*.tsv"))
    if not files:
        raise SystemExit("No snapshot files found under dev/snapshots/. Run scripts/snapshot-project-board.sh first.")
    return files[-1]


def load_snapshot(path):
    """issue -> (state, milestone, sprint, title). Empty sprint stored as None."""
    rows = {}
    with open(path) as f:
        header = f.readline()
        for line in f:
            parts = line.rstrip("\n").split("\t")
            if len(parts) < 5:
                continue
            issue, state, milestone, sprint, title = parts[0], parts[1], parts[2], parts[3], "\t".join(parts[4:])
            rows[issue] = (state, milestone, sprint or None, title)
    return rows


def pull_live_sprint_values():
    """issue -> (item_id, sprint_name_or_None). Full paginated sweep, current truth."""
    live = {}
    cursor = None
    while True:
        if cursor is None:
            query = """
            query($projectId: ID!) {
              node(id: $projectId) {
                ... on ProjectV2 {
                  items(first: 100) {
                    pageInfo { hasNextPage endCursor }
                    nodes {
                      id
                      content { ... on Issue { number } }
                      fieldValueByName(name: "Sprint") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
                    }
                  }
                }
              }
            }"""
            resp = run_gh_graphql(query, projectId=PROJECT_ID)
        else:
            query = """
            query($projectId: ID!, $cursor: String!) {
              node(id: $projectId) {
                ... on ProjectV2 {
                  items(first: 100, after: $cursor) {
                    pageInfo { hasNextPage endCursor }
                    nodes {
                      id
                      content { ... on Issue { number } }
                      fieldValueByName(name: "Sprint") { ... on ProjectV2ItemFieldSingleSelectValue { name } }
                    }
                  }
                }
              }
            }"""
            resp = run_gh_graphql(query, projectId=PROJECT_ID, cursor=cursor)

        items = resp["data"]["node"]["items"]
        for node in items["nodes"]:
            content = node.get("content") or {}
            num = content.get("number")
            if num is None:
                continue
            sprint = (node.get("fieldValueByName") or {}).get("name")
            live[str(num)] = (node["id"], sprint)

        if not items["pageInfo"]["hasNextPage"]:
            break
        cursor = items["pageInfo"]["endCursor"]

    return live


def pull_option_ids():
    """sprint option name -> option id, current live field state."""
    query = """
    query {
      node(id: "%s") {
        ... on ProjectV2 {
          field(name: "Sprint") {
            ... on ProjectV2SingleSelectField { options { id name } }
          }
        }
      }
    }""" % PROJECT_ID
    resp = run_gh_graphql(query)
    options = resp["data"]["node"]["field"]["options"]
    return {o["name"]: o["id"] for o in options}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--snapshot", help="Path to a specific snapshot TSV (default: most recent in dev/snapshots/)")
    parser.add_argument("--apply", action="store_true", help="Actually mutate. Without this flag, only reports what would change.")
    args = parser.parse_args()

    snapshot_path = args.snapshot or find_latest_snapshot()
    print(f"Snapshot: {snapshot_path}")
    snapshot = load_snapshot(snapshot_path)
    print(f"Snapshot rows: {len(snapshot)}")

    print("Pulling current live Sprint values (paginated sweep)...")
    live = pull_live_sprint_values()
    print(f"Live items: {len(live)}")

    drift = []
    for issue, (state, milestone, sprint, title) in snapshot.items():
        if sprint is None:
            continue  # snapshot itself shows no sprint -- nothing to restore
        if issue not in live:
            continue  # issue no longer on the board (rare; not this script's concern)
        item_id, live_sprint = live[issue]
        if live_sprint != sprint:
            drift.append((issue, item_id, live_sprint, sprint, title))

    if not drift:
        print("\nNo drift found. Live board matches the snapshot for every issue that has a sprint value there.")
        return

    print(f"\n{len(drift)} issue(s) differ from the snapshot:")
    for issue, item_id, live_sprint, snap_sprint, title in drift:
        print(f"  #{issue}: live={live_sprint!r} -> snapshot={snap_sprint!r}  [{title[:60]}]")

    if not args.apply:
        print(f"\nDRY RUN -- no changes made. Re-run with --apply to restore these {len(drift)} value(s).")
        return

    print(f"\nApplying {len(drift)} restoration(s)...")
    option_ids = pull_option_ids()
    ok, fail, skipped = 0, 0, 0
    applied = []
    for issue, item_id, live_sprint, snap_sprint, title in drift:
        opt_id = option_ids.get(snap_sprint)
        if opt_id is None:
            print(f"  SKIP #{issue}: snapshot sprint {snap_sprint!r} has no matching live option (renamed/removed?)")
            skipped += 1
            continue
        result = subprocess.run(
            ["gh", "api", "graphql", "-f", f"query={MUTATION}",
             "-f", f"project={PROJECT_ID}", "-f", f"item={item_id}",
             "-f", f"field={FIELD_ID}", "-f", f"value={opt_id}"],
            capture_output=True, text=True,
        )
        if result.returncode == 0 and '"id"' in result.stdout:
            ok += 1
            applied.append(issue)
            print(f"  OK #{issue} -> {snap_sprint}")
        else:
            fail += 1
            print(f"  FAILED #{issue}: {result.stderr[:200]}")

    print(f"\nApplied: {ok}, failed: {fail}, skipped: {skipped}")

    if applied:
        print("\nRe-verifying live...")
        live_after = pull_live_sprint_values()
        mismatches = []
        for issue in applied:
            expected = dict((i, s) for i, _, _, s, _ in drift)[issue]
            _, actual = live_after.get(issue, (None, None))
            if actual != expected:
                mismatches.append((issue, expected, actual))
        if mismatches:
            print(f"MISMATCH after apply ({len(mismatches)}) -- investigate before trusting this run:")
            for issue, expected, actual in mismatches:
                print(f"  #{issue}: expected {expected!r}, got {actual!r}")
            sys.exit(1)
        else:
            print(f"Verified: all {len(applied)} restored value(s) confirmed live. 0 mismatches.")


if __name__ == "__main__":
    main()
