#!/usr/bin/env python3
"""Validate docs/internal/design/tier1-corpus-manifest.csv (#2355).

One row per Tier 1 corpus item. `item` is the one file Piper reads (user
register, voice-passed, the only path a build may index). `derived_from` lists
what the item's facts are checked against (ADRs, docs, code), never indexed.
`last_verified` is the date those facts were checked against `derived_from` or
the served build, with the method in `notes`.

Errors fail (exit 1). Unverified and past-window rows are notes, and fail only
with --strict, which is the behaviour Lead's deploy check can adopt.

Checks: header, field counts, unique ids, enums, dates, positive integer
windows. Every `item` and `derived_from` path exists. A `path#heading` must
resolve, meaning the file holds a heading or a bold line containing that text.
No item lies under the never-indexed trees (dev/, mailboxes/, omnibus-logs/,
memory). An item may not be an ADR, a .py file or a design record marked "not
ratified" (Arch, 11-13: the build would retrieve internal language or code).
A row past `candidate` needs an item. A `verified` row needs a date.
A part (b) item may not name a member of the offered-connector sets, which code decides at
call time per host (ADR-082, Arch 11-13).
Written by Docs 2026-11-13 as a proposal for Lead to adapt.
Concept: docs/internal/design/tier1-corpus-manifest.md
"""

import csv
import datetime
import os
import re
import sys

PATH = "docs/internal/design/tier1-corpus-manifest.csv"
HEADER = [
    "id",
    "part",
    "topic",
    "item",
    "derived_from",
    "source_kind",
    "tier",
    "status",
    "last_verified",
    "reverify_window_days",
    "owner",
    "voice_pass",
    "notes",
]
PARTS = {"a", "b", "c", "d", "candidate"}
STATUS = {"candidate", "unverified", "verified"}
KINDS = {"doc", "generated"}
VOICE = {"pending", "passed", "returned"}
OWNERS = {"docs", "lead", "cio", "cxo", "arch", "ppm"}
EXCLUDED = ("dev/", "mailboxes/", "docs/omnibus-logs/", ".claude-pm/", "memory/")


def refs(cell):
    """Yield (path, heading or None) for each `;`-joined reference."""
    for part in cell.split(";"):
        part = part.strip()
        if not part:
            continue
        path = part.split("::")[0]
        heading = None
        if "#" in path:
            path, heading = path.split("#", 1)
        yield path, (heading.strip('" ') if heading else None)


def heading_resolves(path, heading):
    want = heading.rstrip(".").lower()
    with open(path, encoding="utf-8") as f:
        for line in f:
            if re.match(r"\s*(#|\*\*)", line) and want in line.lower():
                return True
    return False


def offered_names():
    """Values of the offered-connector dicts, read from source without importing it."""
    import ast

    names = set()
    try:
        tree = ast.parse(open("services/integrations/integration_status_service.py").read())
    except OSError:
        return names
    for node in ast.walk(tree):
        target = getattr(node, "target", None) or (getattr(node, "targets", [None])[0])
        if getattr(target, "id", "") in (
            "BETA_OFFERED_CONNECTORS",
            "STAGING_ONLY_OFFERED_CONNECTORS",
        ) and isinstance(getattr(node, "value", None), ast.Dict):
            names |= {v.value for v in node.value.values if isinstance(v, ast.Constant)}
    return names


def not_ratified(path):
    try:
        with open(path, encoding="utf-8") as f:
            return "not ratified" in "".join(f.readlines()[:15]).lower()
    except OSError:
        return False


def main(argv):
    strict = "--strict" in argv
    today = datetime.date.today()
    errors, notes = [], []
    with open(PATH, newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    if rows[0] != HEADER:
        sys.exit(f"ERROR: header is {rows[0]}, expected {HEADER}")
    seen = set()
    for n, r in enumerate(rows[1:], start=2):
        if len(r) != len(HEADER):
            errors.append(f"row {n}: {len(r)} fields")
            continue
        d = dict(zip(HEADER, r))
        rid = d["id"]
        if not rid or rid in seen:
            errors.append(f"row {n}: id {rid!r} empty or repeated")
        seen.add(rid)
        for col, ok in (
            ("part", PARTS),
            ("status", STATUS),
            ("source_kind", KINDS),
            ("voice_pass", VOICE),
            ("owner", OWNERS),
        ):
            if d[col] not in ok:
                errors.append(f"{rid}: {col}={d[col]!r}")
        if d["tier"] != "1":
            errors.append(f"{rid}: tier={d['tier']!r} (this manifest is Tier 1 only)")
        if not d["reverify_window_days"].isdigit() or int(d["reverify_window_days"]) < 1:
            errors.append(f"{rid}: reverify_window_days={d['reverify_window_days']!r}")
        if d["status"] != "candidate" and not d["item"]:
            errors.append(f"{rid}: status {d['status']} but no item file")
        for col in ("item", "derived_from"):
            for p, h in refs(d[col]):
                if col == "item" and p.startswith(EXCLUDED):
                    errors.append(f"{rid}: item {p} is under a never-indexed tree")
                    continue
                if not os.path.exists(p):
                    errors.append(f"{rid}: {col} {p} does not exist")
                    continue
                if h and not heading_resolves(p, h):
                    errors.append(f"{rid}: {col} {p} has no heading or bold line {h!r}")
                if col == "item" and d["source_kind"] != "generated":
                    if "/adrs/" in p or p.endswith(".py") or not_ratified(p):
                        errors.append(
                            f"{rid}: item {p} is an ADR, code or a not-ratified record, never indexed"
                        )
        if d["part"] == "b" and d["item"] and os.path.exists(d["item"].split("#")[0]):
            text = open(d["item"].split("#")[0], encoding="utf-8").read().lower()
            hit = sorted(n for n in offered_names() if n.lower() in text)
            if hit:
                errors.append(
                    f"{rid}: item names offered connectors {hit}. State the rule, not the members "
                    "(ADR-082): the names come from part (a)"
                )
        lv = d["last_verified"]
        if d["status"] == "verified" and not lv:
            errors.append(f"{rid}: status verified but no last_verified date")
        if lv:
            try:
                age = (today - datetime.date.fromisoformat(lv)).days
                if age > int(d["reverify_window_days"] or 0):
                    notes.append(
                        f"{rid}: verified {lv}, {age} days ago, past its "
                        f"{d['reverify_window_days']}-day window"
                    )
            except ValueError:
                errors.append(f"{rid}: last_verified={lv!r}")
        elif d["status"] != "candidate":
            notes.append(f"{rid}: unverified")
    for e in errors:
        print("ERROR", e)
    for m in notes:
        print("NOTE ", m)
    print(f"{PATH}: {len(rows) - 1} rows, {len(errors)} error(s), {len(notes)} note(s)")
    return 1 if errors or (strict and notes) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
