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
import re
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


CLASS_RE = re.compile(r"^\s*Class:\s*(.+?)\s*$", re.MULTILINE | re.IGNORECASE)


def issue_class(issue: dict) -> str:
    """The `Class:` tag from an issue body, or "" if untagged.

    Exec's amended contract (2026-08-10) measures the NEW-CLASS rate, not the
    raw rate: raw cannot distinguish "the fix worked" from "PM tested less" —
    same curve, opposite readings. The class vocabulary lives at
    docs/internal/operations/failure-class-vocabulary.md.
    """
    m = CLASS_RE.search(issue.get("body") or "")
    if not m:
        return ""
    # "NEW — foo" and "NEW: foo" both mean a newly-named class; keep the name.
    return m.group(1).lstrip("—:- ").strip()


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

    # ---- NEW-CLASS rate (Exec's amended contract, 2026-08-10) ----------------
    # Reports its own coverage FIRST and refuses to compute a rate it cannot
    # support. An unclassified corpus must read as "not measured", never as
    # "no new classes" — that is the m-44 failure this instrument would
    # otherwise reproduce (a false all-clear is emitted identically to a real
    # one). See failure-class-vocabulary.md class 5.
    tagged = {i["number"]: issue_class(i) for i in issues if issue_class(i)}
    print()
    print("NEW-CLASS RATE — of this week's findings, how many are already-named classes?")
    print(f"coverage: {len(tagged)} of {len(issues)} issues carry a `Class:` tag "
          f"({100 * len(tagged) // max(len(issues), 1)}%)")
    if not tagged:
        print("  NOT MEASURED — no issue in the window carries a `Class:` tag.")
        print("  This is a coverage gap, NOT a finding of zero new classes.")
        print("  Add `Class: <family>` at filing time; vocabulary at")
        print("  docs/internal/operations/failure-class-vocabulary.md")
        return

    # A class is "new" in the week it first appears anywhere in the window.
    first_seen: dict = {}
    for i in sorted(issues, key=lambda x: x["created_at"]):
        c = issue_class(i)
        if c and c not in first_seen:
            created = datetime.fromisoformat(i["created_at"].replace("Z", "+00:00"))
            first_seen[c] = int((now - created).days // 7)

    # Per-week COVERAGE, because a week with no tagged issues has zero coverage
    # and NOT zero new classes. Printing "(all previously named)" for an
    # untagged week is the false-clear this instrument is supposed to detect.
    tagged_per_week: Counter = Counter()
    for i in issues:
        if issue_class(i):
            created = datetime.fromisoformat(i["created_at"].replace("Z", "+00:00"))
            tagged_per_week[int((now - created).days // 7)] += 1

    print()
    for w in range(weeks - 1, -1, -1):
        start = (now - timedelta(weeks=w + 1)).date()
        end = (now - timedelta(weeks=w)).date()
        new_here = sorted(c for c, wk in first_seen.items() if wk == w)
        label = "this week →" if w == 0 else f"{start}..{end}"
        if not tagged_per_week[w]:
            print(f"  {label:>24}    – NOT MEASURED "
                  f"(0 of {per_week[w]} issues tagged)")
            continue
        cov = f"[{tagged_per_week[w]}/{per_week[w]} tagged]"
        print(f"  {label:>24}  {len(new_here):3d} new {cov:>16}  "
              f"{', '.join(new_here) if new_here else '(all previously named)'}")
    print()
    print("read: falling NEW-CLASS count = convergence (we keep finding the same")
    print("families). Falling RAW count alone proves nothing — it reads the same")
    print("whether the structural work landed or PM simply tested less.")


if __name__ == "__main__":
    main()
