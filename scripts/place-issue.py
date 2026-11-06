#!/usr/bin/env python3
"""Place one issue in Production: milestone, board Status, and a plan row beside an anchor.

Usage: python3 scripts/place-issue.py N SECTION ANCHOR "note" [--status backlog|progress] [--dry-run]
  N        the issue to place
  SECTION  a plan section letter: PUB, H, D, C, V, E, T, Doc, Dist, Q
  ANCHOR   an issue whose plan row the new row goes after (must be in SECTION)
  note     the parenthetical after the title: date, source, why here

Does the mechanical half of a PPM placement (Agent 360 v0.6, 6.3): sets the milestone,
adds the issue to project #1 with a Status, inserts the row, bumps the section's row
count and prefixes the Total line. It never touches the Sprint field (PM-gated) or
priority labels. The placement judgment (which milestone, section and anchor, and the
issue comment) stays with the caller. Afterwards: snapshot, regenerate and publish the map.
"""

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

PLAN = "docs/internal/planning/production-sprint-proposal-2026-10-23.md"
OWNER = "mediajunkie"
PROJECT_NUMBER = "1"
PROJECT_ID = "PVT_kwHOADE-8s4A-JwA"
STATUS_FIELD = "PVTSSF_lAHOADE-8s4A-JwAzgxpGyU"
STATUS = {"backlog": "e7d1c990", "progress": "47fc9ee4"}
SECTIONS = {"PUB", "H", "D", "C", "V", "E", "T", "Doc", "Dist", "Q"}


def gh(*args):
    return subprocess.run(["gh", *args], check=True, capture_output=True, text=True).stdout.strip()


def edit_plan(text, n, section, anchor, title, note, stamp):
    if re.search(rf"^\| #{n} \|", text, re.M):
        sys.exit(f"#{n} already has a plan row; nothing to add")
    heads = list(re.finditer(r"^### (\w+): .*\((\d+)\)$", text, re.M))
    idx = next((i for i, h in enumerate(heads) if h.group(1) == section), None)
    if idx is None:
        sys.exit(f"no '### {section}:' section in the plan")
    head = heads[idx]
    end = heads[idx + 1].start() if idx + 1 < len(heads) else len(text)
    row = re.compile(rf"^\| #{anchor} \|.*$", re.M).search(text, head.end(), end)
    if not row:
        sys.exit(f"#{anchor} has no row in section {section}")
    new_row = f"| #{n} | {title} ({note}) | — |"
    text = text[: row.end()] + "\n" + new_row + text[row.end() :]
    count = int(head.group(2))
    head_line = head.group(0)
    text = text.replace(head_line, head_line[: -len(f"({count})")] + f"({count + 1})", 1)
    total = re.search(r"^Total: (\d+) open \(", text, re.M)
    if not total:
        sys.exit("no 'Total: N open (' line in the plan")
    old = int(total.group(1))
    event = f"{stamp}: #{n} placed in {section} beside #{anchor}"
    text = text.replace(total.group(0), f"Total: {old + 1} open ({event}; {old} at {stamp}: ", 1)
    return text, new_row, old + 1


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("n", type=int)
    ap.add_argument("section", choices=sorted(SECTIONS))
    ap.add_argument("anchor", type=int)
    ap.add_argument("note")
    ap.add_argument("--status", choices=sorted(STATUS), default="backlog")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    issue = json.loads(gh("issue", "view", str(a.n), "--json", "title,state,milestone"))
    if issue["state"] != "OPEN":
        sys.exit(f"#{a.n} is {issue['state']}; the plan holds open issues")
    if (issue.get("milestone") or {}).get("title") == "Production":
        sys.exit(f"#{a.n} is already in Production; move its row by hand if it needs one")
    stamp = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%m-%d %H:%M")
    title = issue["title"].replace("|", "/")
    with open(PLAN) as f:
        text, new_row, total = edit_plan(f.read(), a.n, a.section, a.anchor, title, a.note, stamp)

    print(new_row)
    print(f"Total {total}; section {a.section} +1; Status {a.status}; Sprint left unset")
    if a.dry_run:
        print("dry run: nothing written")
        return

    gh("issue", "edit", str(a.n), "--milestone", "Production")
    url = f"https://github.com/{OWNER}/piper-morgan-product/issues/{a.n}"
    item = gh(
        "project",
        "item-add",
        PROJECT_NUMBER,
        "--owner",
        OWNER,
        "--url",
        url,
        "--format",
        "json",
        "--jq",
        ".id",
    )
    gh(
        "project",
        "item-edit",
        "--id",
        item,
        "--project-id",
        PROJECT_ID,
        "--field-id",
        STATUS_FIELD,
        "--single-select-option-id",
        STATUS[a.status],
    )
    with open(PLAN, "w") as f:
        f.write(text)
    live = gh(
        "issue",
        "list",
        "--milestone",
        "Production",
        "--state",
        "open",
        "--limit",
        "1000",
        "--json",
        "number",
        "--jq",
        "length",
    )
    print(
        f"gh open Production: {live} (plan Total {total}; a lag of one is GitHub's list catching up)"
    )


if __name__ == "__main__":
    main()
