#!/usr/bin/env python3
"""registry-set.py — read or edit one cell of dev/active/duty-cycle-registry.tsv by column NAME.

#1968 item 3 (CXO 10.4, a wrong-column edit). Rows are positional and up to 8 fields wide, and the state
column is long prose, so an edit by position puts text in the wrong column without any error. This helper
names the column, so a value can only land where the name says.

  scripts/registry-set.py ROLE                    print the row's fields by name
  scripts/registry-set.py ROLE COLUMN VALUE       set one cell; prints old and new
  scripts/registry-set.py ROLE COLUMN VALUE -n    dry run: print, don't write
  scripts/registry-set.py --check                 flag rows whose fields don't fit their column

Columns: role cron_expr threshold_h wake_start wake_end first_fire active_since state.

Edits follow the file's own rule (see its header): never round-trip through the csv module. The target
line is found by its `role<TAB>` prefix, only that line is replaced, and every other byte is written back
unchanged. Exit 0 ok, 1 --check found a problem, 2 usage or lookup error.
Owner: CIO. Review: 2026-12-08.
Concept: .claude/skills/duty-cycle-tick/SKILL.md
"""

import re
import subprocess
import sys
from pathlib import Path

COLUMNS = [
    "role",
    "cron_expr",
    "threshold_h",
    "wake_start",
    "wake_end",
    "first_fire",
    "active_since",
    "state",
]
SHAPES = {
    "threshold_h": re.compile(r"^\d+$"),
    "wake_start": re.compile(r"^\d{1,2}$"),
    "wake_end": re.compile(r"^\d{1,2}$"),
    "first_fire": re.compile(r"^\d{2}:\d{2}$"),
    "active_since": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
}


def registry_path() -> Path:
    top = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"], capture_output=True, text=True
    ).stdout.strip()
    return Path(top or ".") / "dev/active/duty-cycle-registry.tsv"


def data_lines(lines):
    for i, line in enumerate(lines):
        if line.startswith("#") or line.startswith("role\t") or not line.strip():
            continue
        yield i, line


def check(lines) -> int:
    problems = 0
    for i, line in data_lines(lines):
        fields = line.rstrip("\n").split("\t")
        role = fields[0]
        if not 7 <= len(fields) <= 8:
            print(f"line {i + 1} {role}: {len(fields)} fields (want 7 or 8)")
            problems += 1
        for name, shape in SHAPES.items():
            k = COLUMNS.index(name)
            if k < len(fields) and not shape.match(fields[k]):
                print(f"line {i + 1} {role}: {name} = {fields[k][:60]!r} doesn't fit {name}")
                problems += 1
    n = sum(1 for _ in data_lines(lines))
    print(f"registry-set --check: {n} rows, {problems} problem(s)")
    return 1 if problems else 0


def main(argv) -> int:
    dry = "-n" in argv
    args = [a for a in argv if a != "-n"]
    path = registry_path()
    text = path.read_text()
    lines = text.splitlines(keepends=True)
    if args == ["--check"]:
        return check(lines)
    if len(args) not in (1, 3):
        print(__doc__.split("\n\n")[2], file=sys.stderr)
        return 2
    role = args[0]
    hits = [i for i, line in data_lines(lines) if line.startswith(role + "\t")]
    if len(hits) != 1:
        print(f"registry-set: {len(hits)} rows for role {role!r} (need exactly 1)", file=sys.stderr)
        return 2
    i = hits[0]
    end = "\n" if lines[i].endswith("\n") else ""
    fields = lines[i].rstrip("\n").split("\t")
    if len(args) == 1:
        for name, value in zip(COLUMNS, fields):
            print(f"{name:13} {value}")
        return 0
    column, value = args[1], args[2]
    if column not in COLUMNS or column == "role":
        print(
            f"registry-set: unknown or fixed column {column!r}; one of {' '.join(COLUMNS[1:])}",
            file=sys.stderr,
        )
        return 2
    if "\t" in value or "\n" in value:
        print("registry-set: value can't contain a tab or newline", file=sys.stderr)
        return 2
    k = COLUMNS.index(column)
    while len(fields) <= k:
        fields.append("")
    old = fields[k]
    fields[k] = value
    print(f"{role} {column}: {old[:80]!r} -> {value[:80]!r}")
    if dry:
        print("(dry run, nothing written)")
        return 0
    lines[i] = "\t".join(fields) + end
    path.write_text("".join(lines))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
