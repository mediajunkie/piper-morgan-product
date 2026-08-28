#!/usr/bin/env python3
"""check-staleness.py — flag silently-stale operating docs (#972 MEM-TEMPORAL, P1).

The lint that catches the failure mode that bit us: an operating doc nobody has re-confirmed,
quietly drifting out of date. Per the ratified #972 decision it WARNS (+ you capture fix-tasks) —
it never blocks a commit.

Freshness signal, in priority order:
  1. `last_verified`  — when someone last CONFIRMED the doc is still accurate (#972's new field)
  2. `last_updated`   — when the doc was last edited (existing convention; a usable fallback —
                        editing implies verification at that moment)
A doc with neither can't be assessed → flagged NO-DATES. `valid_until` in the past → EXPIRED.

The lint runs off `last_updated` TODAY (zero bulk-stamping needed) and rewards adopting
`last_verified` — which lets a doc be marked confirmed-current WITHOUT a content edit (the only
way to clear staleness on a doc that's correct but simply hasn't been touched).

Usage:
  scripts/check-staleness.py                 # default doc set (docs/briefing/*.md)
  scripts/check-staleness.py path ...        # explicit files/globs
  STALE_DAYS=21 scripts/check-staleness.py   # tune the staleness threshold (default 21)
Exit code is always 0 (warn-only). Prints a report; the EXPIRED/STALE list is your task queue.
"""

import datetime
import glob
import os
import re
import sys

REPO = os.environ.get("PIPER_REPO", os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
STALE_DAYS = int(os.environ.get("STALE_DAYS", "21"))
TODAY = datetime.date.today()

# Operating docs = how the cohort works *now* (drift-prone), NOT point-in-time artifacts. We extend by
# PRECISE globs, not whole-dir sweeps — the candidate dirs mix the two (survey 2026-06-16):
#   - docs/agent-protocols/  → all 6 are how-we-work protocols (no archives) → glob the dir.
#   - docs/briefs/cross-pollination/ → 1 live brief (current.md) + ~89 dated archives → current.md ONLY.
#   - docs/internal/operations/ → runbooks (operating) MIXED with dated audits/reports (snapshots, correctly
#     "stale" forever). A blanket glob would flood false NO-DATES, so it's DEFERRED to per-doc curation
#     (Docs-owned: pick the operating-runbook subset + give them freshness frontmatter). Tracked follow-up.
DEFAULT_GLOBS = [
    "docs/briefing/*.md",  # role briefings + ROSTER + ROLE-PORTFOLIO (original set)
    "docs/agent-protocols/*.md",  # how-we-work protocols (debugging, git, issue-closure, e2e, …)
    "docs/briefs/cross-pollination/current.md",  # the LIVE cross-project brief (NOT the dated archive)
]

DATE_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def frontmatter(path):
    """Return the YAML-ish frontmatter dict (first --- ... --- block), or {} if none."""
    try:
        with open(path, encoding="utf-8") as fh:
            text = fh.read()
    except Exception:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    fm = {}
    for line in text[3:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            fm[k.strip()] = v.strip().strip('"').strip("'")
    return fm


def parse_date(val):
    if not val:
        return None
    m = DATE_RE.match(val.strip())
    if not m:
        return None
    try:
        return datetime.date.fromisoformat(m.group(1))
    except ValueError:
        return None


def collect(globs):
    paths = []
    for g in globs:
        g = g if os.path.isabs(g) else os.path.join(REPO, g)
        paths.extend(glob.glob(g))
    return sorted(set(paths))


def main():
    globs = sys.argv[1:] or DEFAULT_GLOBS
    paths = collect(globs)
    expired, stale, nodates, ok = [], [], [], []
    has_lv = 0
    for p in paths:
        rel = os.path.relpath(p, REPO)
        fm = frontmatter(p)
        lv = parse_date(fm.get("last_verified"))
        lu = parse_date(fm.get("last_updated"))
        vu = parse_date(fm.get("valid_until"))
        if fm.get("last_verified"):
            has_lv += 1
        if vu and vu < TODAY:
            expired.append((rel, f"valid_until {vu} is past"))
            continue
        fresh = lv or lu
        if not fresh:
            nodates.append((rel, "no last_verified / last_updated"))
            continue
        age = (TODAY - fresh).days
        tag = "last_verified" if lv else "last_updated"
        if age > STALE_DAYS:
            stale.append((rel, f"{age}d since {tag} ({fresh})"))
        else:
            ok.append((rel, f"{age}d ({tag})"))

    def block(title, items):
        if not items:
            return
        print(f"\n{title} ({len(items)}):")
        for rel, why in items:
            print(f"  - {rel} — {why}")

    print(f"check-staleness: {len(paths)} operating doc(s), threshold {STALE_DAYS}d, {TODAY}")
    block("⛔ EXPIRED (valid_until past)", expired)
    block("⚠️  STALE — re-verify + bump last_verified, or update", stale)
    block("❓ NO DATES — add valid_from + last_verified", nodates)
    print(f"\n✓ OK: {len(ok)}   |   #972 adoption: {has_lv}/{len(paths)} carry last_verified")
    actionable = len(expired) + len(stale) + len(nodates)
    if actionable:
        print(
            f"\n→ {actionable} doc(s) need attention. Per #972: capture a fix-task for each (warn, not block)."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
