#!/usr/bin/env bash
# tests-queue-eta.sh: when would a push to main now get its Tests verdict?
#
# Tests runs on main queue; they are not cancelled by a newer push
# (.github/workflows/test.yml cancels superseded runs on pull requests only).
# So a push lands behind every run already queued or in progress, and the
# promote gate waits for Tests on the sha staging serves.
#
# Prints the runs ahead, an estimate of when a run started by a push now would
# finish, and whether that is before a cutoff (default 20:50 PT, ten minutes
# inside the grant's 21:00 limit). Read-only: GitHub API reads only.
#
# Usage: scripts/tests-queue-eta.sh [--cutoff HH:MM]
# Exit: 0 = estimate before the cutoff, 1 = after it, 3 = could not measure.
# Concept: docs/internal/operations/alpha-promotion-standing-grant.md (the "Tests runs on main queue" procedure note)
# CIO, 2026-11-27, after Lead's 11-26 20:22 landing (xian's question via Exec 01M8F6RY8H).

set -uo pipefail
REPO="mediajunkie/piper-morgan-product"
CUTOFF="20:50"
if [ "${1:-}" = "--cutoff" ] && [ -n "${2:-}" ]; then CUTOFF="$2"; fi

runs=$(gh run list -R "$REPO" --workflow test.yml --branch main --limit 30 \
  --json databaseId,status,createdAt,startedAt,headSha 2>/dev/null) || { echo "tests-queue-eta: could not read runs (gh failed); not measured"; exit 3; }
hist=$(gh run list -R "$REPO" --workflow test.yml --branch main --status success --limit 40 \
  --json startedAt,updatedAt 2>/dev/null) || { echo "tests-queue-eta: could not read history; not measured"; exit 3; }

python3 - "$runs" "$hist" "$CUTOFF" <<'PY'
import json, sys, statistics
from datetime import datetime, timezone, timedelta
from zoneinfo import ZoneInfo
runs, hist, cutoff = json.loads(sys.argv[1]), json.loads(sys.argv[2]), sys.argv[3]
pt = ZoneInfo("America/Los_Angeles")
p = lambda s: datetime.fromisoformat(s.replace("Z", "+00:00"))
durs = sorted((p(r["updatedAt"]) - p(r["startedAt"])).total_seconds() for r in hist if r.get("startedAt"))
if len(durs) < 5:
    print(f"tests-queue-eta: only {len(durs)} timed runs; not measured"); sys.exit(3)
med = statistics.median(durs)
now = datetime.now(timezone.utc)
running = [r for r in runs if r["status"] == "in_progress"]
queued = [r for r in runs if r["status"] in ("queued", "waiting", "pending", "requested")]
t = now
for r in running:
    left = med - (now - p(r["startedAt"])).total_seconds() if r.get("startedAt") else med
    t = max(t, now + timedelta(seconds=max(left, 60)))
t += timedelta(seconds=med * len(queued))
eta = t + timedelta(seconds=med)
hh, mm = map(int, cutoff.split(":"))
local_now = now.astimezone(pt)
cut = local_now.replace(hour=hh, minute=mm, second=0, microsecond=0)
print(f"Tests on main: {len(running)} running, {len(queued)} queued "
      f"(median run {med/60:.0f} min over the last {len(durs)} green runs).")
for r in running + queued:
    print(f"  {r['status']:<11} {r['headSha'][:10]}  run {r['databaseId']}")
print(f"A push now would get its Tests verdict at about {eta.astimezone(pt):%H:%M} PT (estimate, not a measurement).")
if eta.astimezone(pt) <= cut:
    print(f"Before the {cutoff} cutoff."); sys.exit(0)
print(f"AFTER the {cutoff} cutoff: if a promotion is still planned today, promote first, then push.")
sys.exit(1)
PY
