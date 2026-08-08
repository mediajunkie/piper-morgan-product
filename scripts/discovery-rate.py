#!/usr/bin/env python3
"""discovery-rate.py — THE convergence indicator (PM commitment, 2026-08-08).

Computes new-issues-per-week (the discovery rate) from GitHub issue creation
timestamps — a source that cannot drift, be forgotten, or be gamed by anyone's
optimism. Committed the day PM asked "who's going to be keeping track of that
number? Who's the source of authority?" — answer: GitHub's created_at is the
authority; this script is the arithmetic; Exec's daily rollup is the surface;
any agent can verify by rerunning it.

Interpretation contract (from dev/active/honest-mvp-ledger-2026-08-08.html and
memory pin project_pm_confidence_crisis_2026_08_08):
- Structural work (routing front-door, floor honesty, corpus growth) is
  supposed to BEND this curve downward over ~3 weeks from 2026-08-08.
- Flat or rising curve at ~2026-09-01 => the hard re-scoping conversation,
  held WITH this data.
- m-44: the script prints its denominator (issues counted, window, filters).

Usage: python3 scripts/discovery-rate.py [weeks]   (default 8)
Requires: gh CLI authenticated. Uses REST (survives GraphQL quota exhaustion).
"""

import json
import subprocess
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone

REPO = "mediajunkie/piper-morgan-product"


def fetch_issues(since: datetime) -> list:
    """All issues (not PRs) created since `since`, via REST with pagination."""
    issues, page = [], 1
    while True:
        out = subprocess.run(
            ["gh", "api",
             f"repos/{REPO}/issues?state=all&since={since.strftime('%Y-%m-%dT%H:%M:%SZ')}"
             f"&per_page=100&page={page}&sort=created&direction=desc"],
            capture_output=True, text=True, check=True,
        ).stdout
        batch = [i for i in json.loads(out) if "pull_request" not in i]
        issues.extend(batch)
        if len(json.loads(out)) < 100:
            break
        page += 1
    # `since` filters by UPDATE time; re-filter by creation time (the honest field)
    return [i for i in issues
            if datetime.fromisoformat(i["created_at"].replace("Z", "+00:00")) >= since]


def main() -> None:
    weeks = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    now = datetime.now(timezone.utc)
    since = now - timedelta(weeks=weeks)
    issues = fetch_issues(since)

    per_week: Counter = Counter()
    for i in issues:
        created = datetime.fromisoformat(i["created_at"].replace("Z", "+00:00"))
        week_idx = int((now - created).days // 7)  # 0 = this week
        per_week[week_idx] += 1

    print(f"DISCOVERY RATE — new issues created per trailing week ({REPO})")
    print(f"denominator: {len(issues)} issues (PRs excluded) created since "
          f"{since.date()} ({weeks}w window), source: GitHub created_at via REST")
    print()
    for w in range(weeks - 1, -1, -1):
        start = (now - timedelta(weeks=w + 1)).date()
        end = (now - timedelta(weeks=w)).date()
        n = per_week[w]
        bar = "#" * n
        label = "this week →" if w == 0 else f"{start}..{end}"
        print(f"  {label:>24}  {n:3d}  {bar}")
    print()
    print("contract: structural work should BEND this downward from 2026-08-08;")
    print("flat/rising at 2026-09-01 => the hard conversation, with this data.")


if __name__ == "__main__":
    main()
