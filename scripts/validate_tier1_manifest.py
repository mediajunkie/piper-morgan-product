#!/usr/bin/env python3
"""Validate docs/internal/design/tier1-corpus-manifest.csv (#2355).

One row per Tier 1 corpus item. `item` is the one file Piper reads (user
register, voice-passed, the only path a build may index). `derived_from` lists
what the item's facts are checked against (ADRs, docs, code), never indexed.
`last_verified` is the date those facts were checked against `derived_from` or
the served build, with the method in `notes`.

Errors fail (exit 1). Unverified and past-window rows are notes, and fail only
with --strict (Docs' own stricter read). `--deploy` is the narrower gate for a
deploy check (Lead and Arch, 11-13). A row is indexed only when it is `verified`,
voice_pass is `passed`, its item resolves and it is inside its window. In
`--deploy` mode a row that fails any of those DROPS out of the index and is
reported as a `DROP` line (id and reason, no text), and the deploy is NOT
refused. The deploy is refused (exit 1) only for an indexed item on an excluded
path (dev/, mailboxes/, omnibus-logs, memory, an ADR, a .py file or a
not-ratified record), or a malformed manifest. A generated row carries no date and no window check (its test is the
generator's). Dates are YYYY-MM-DD in Pacific time. Importable as
`scripts.validate_tier1_manifest` (heading_resolves, offered_names).

Fifth condition (Arch and CIO, 11-13): `approved` is the commit sha of the item at
xian's quoted approval. Indexing also needs every non-blank line of the current
item to appear in the item at that sha, so a deleted line keeps the approval and a
new or changed line drops the row ("text changed since approval"). The comparison
needs git history. Generated rows carry their approval on the template instead.

A stand-in line per row (Arch, 11-13): docs/tier1/stand-ins.md holds the template and
one `id: user phrase` line per manifest row, so a dropped row's stand-in never
shows a manifest id. A row without a line is a note, and fails with --strict.

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
import subprocess
import sys
from zoneinfo import ZoneInfo

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
    "approved",
    "notes",
]
PARTS = {"a", "b", "c", "d", "candidate"}
STATUS = {"candidate", "unverified", "verified"}
KINDS = {"doc", "generated", "template"}
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
    with open("services/integrations/integration_status_service.py", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    for node in ast.walk(tree):
        target = getattr(node, "target", None) or (getattr(node, "targets", [None])[0])
        if getattr(target, "id", "") in (
            "BETA_OFFERED_CONNECTORS",
            "STAGING_ONLY_OFFERED_CONNECTORS",
        ) and isinstance(getattr(node, "value", None), ast.Dict):
            names |= {v.value for v in node.value.values if isinstance(v, ast.Constant)}
    if not names:
        # Fail closed (Lead, 11-13): finding neither dict is an error, never an empty pass.
        raise SystemExit(
            "ERROR: could not read BETA_OFFERED_CONNECTORS or STAGING_ONLY_OFFERED_CONNECTORS "
            "as dict literals from services/integrations/integration_status_service.py"
        )
    return names


def approved_text_ok(sha, path):
    """True when every non-blank line of `path` now also appears in `path` at `sha`.
    Deleting a line keeps the approval, adding or changing one needs a new approval.
    Returns None when git cannot show the file at that sha (no history)."""
    try:
        old = subprocess.run(
            ["git", "show", f"{sha}:{path}"], capture_output=True, text=True, check=True
        ).stdout
    except (subprocess.CalledProcessError, OSError):
        return None
    old_lines = {ln.strip() for ln in old.splitlines() if ln.strip()}
    with open(path, encoding="utf-8") as f:
        return all(ln.strip() in old_lines for ln in f if ln.strip())


def not_ratified(path):
    try:
        with open(path, encoding="utf-8") as f:
            return "not ratified" in "".join(f.readlines()[:15]).lower()
    except OSError:
        return False


def main(argv):
    strict = "--strict" in argv
    deploy = "--deploy" in argv
    today = datetime.datetime.now(ZoneInfo("America/Los_Angeles")).date()
    errors, notes, drops = [], [], []
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
        window_ok = d["reverify_window_days"].isdigit() and int(d["reverify_window_days"]) >= 1
        if not window_ok and d["source_kind"] != "template":
            errors.append(f"{rid}: reverify_window_days={d['reverify_window_days']!r}")
        if d["status"] != "candidate" and not d["item"]:
            errors.append(f"{rid}: status {d['status']} but no item file")
        for col in ("item", "derived_from"):
            for p, h in refs(d[col]):
                if col == "item" and p.startswith(EXCLUDED):
                    errors.append(f"{rid}: item {p} is under a never-indexed tree")
                    continue
                if not os.path.exists(p):
                    (drops if deploy else errors).append(f"{rid}: {col} {p} does not exist")
                    continue
                if h and not heading_resolves(p, h):
                    (drops if deploy else errors).append(
                        f"{rid}: {col} {p} has no heading or bold line {h!r}"
                    )
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
        if d["approved"] and not re.fullmatch(r"[0-9a-f]{7,40}", d["approved"]):
            errors.append(f"{rid}: approved={d['approved']!r} is not a commit sha")
        if (d["status"] == "verified" and d["source_kind"] != "generated") or (
            d["source_kind"] == "template" and d["approved"]
        ):
            if deploy and d["voice_pass"] != "passed":
                drops.append(f"{rid}: verified but voice_pass is {d['voice_pass']}")
            if deploy and not d["approved"]:
                drops.append(f"{rid}: verified but not approved (no sha in approved)")
            elif d["approved"] and d["item"]:
                item_path = d["item"].split("#")[0]
                ok = (
                    approved_text_ok(d["approved"], item_path)
                    if os.path.exists(item_path)
                    else None
                )
                if ok is False:
                    drops.append(f"{rid}: text changed since approval")
                elif ok is None and os.path.exists(item_path):
                    if d["source_kind"] == "template":
                        # Arch 11-13: a build that cannot read the stand-in file at its approved
                        # sha can produce no stand-in. That is a build fault, so exit 1.
                        errors.append(
                            f"{rid}: approval sha {d['approved']} not readable (a build fault)"
                        )
                    else:
                        drops.append(f"{rid}: approval can't be checked")
        lv = d["last_verified"]
        generated = d["source_kind"] in ("generated", "template")
        if d["status"] == "verified" and not lv and not generated:
            errors.append(f"{rid}: status verified but no last_verified date")
        if lv:
            try:
                age = (today - datetime.date.fromisoformat(lv)).days
                if generated:
                    pass
                elif (
                    age > int(d["reverify_window_days"] or 0)
                    and deploy
                    and d["status"] == "verified"
                ):
                    drops.append(
                        f"{rid}: verified {lv}, {age} days ago, past its "
                        f"{d['reverify_window_days']}-day window"
                    )
                elif age > int(d["reverify_window_days"] or 0):
                    notes.append(
                        f"{rid}: verified {lv}, {age} days ago, past its "
                        f"{d['reverify_window_days']}-day window"
                    )
            except ValueError:
                errors.append(f"{rid}: last_verified={lv!r}")
        elif d["status"] != "candidate" and not generated:
            notes.append(f"{rid}: unverified")
    stand_ins = "docs/tier1/stand-ins.md"
    if os.path.exists(stand_ins):
        with open(stand_ins, encoding="utf-8") as f:
            have = {ln.split(":", 1)[0].strip() for ln in f if re.match(r"^[a-z]-[\w-]+:", ln)}
        for r in rows[1:]:
            rid = r[0]
            if rid != "s-stand-ins" and rid not in have:
                notes.append(f"{rid}: no line in {stand_ins} (it would fall back to a manifest id)")
    else:
        notes.append(f"{stand_ins} is missing")
    for e in errors:
        print("ERROR", e)
    for m in notes:
        print("NOTE ", m)
    for dr in drops:
        print("DROP ", dr)
    print(f"{PATH}: {len(rows) - 1} rows, {len(errors)} error(s), {len(notes)} note(s)")
    return 1 if errors or (strict and notes) else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
