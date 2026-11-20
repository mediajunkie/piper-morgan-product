"""Pass 1 of the 2406 classifier screen: per base, main against control (the floor) and
main against the candidate, on the counted outcome. Usage: analyze_p1.py DIR"""

import sys
from pathlib import Path

D = Path(sys.argv[1])


def load(name: str) -> dict:
    rows = {}
    for line in (D / f"report-p1-{name}.md").read_text().splitlines():
        if not line.startswith("| ") or line.startswith("| phrase"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        rows[cells[0]] = (cells[1].rsplit(" ×", 1)[0].strip("`"), cells[2])
    return rows


for base in "AB":
    main, control, cand = (load(f"{side}-{base}") for side in ("main", "control", "cand"))
    floor = [p for p in main if main[p][0] != control[p][0]]
    moved = [p for p in main if main[p][0] != cand[p][0]]
    new_label = [p for p in moved if cand[p][0] != control[p][0]]
    print(f"## base {base}: {len(main)} rows")
    print(f"main against control differ: {len(floor)}")
    print(
        f"main against candidate differ: {len(moved)} (of which on an outcome the control didn't produce either: {len(new_label)})"
    )
    print(f"beyond the control's rate: {len(moved) - len(floor)}")
    for p in moved:
        print(
            f"  {p!r}: main {main[p][0]} | control {control[p][0]} | cand {cand[p][0]}   raw: {main[p][1]} -> {cand[p][1]}"
        )
    print("floor rows:")
    for p in floor:
        print(f"  {p!r}: main {main[p][0]} | control {control[p][0]}")
    errs = [p for p in main if any(x[p][0] in ("ERROR", "UNPARSED") for x in (main, control, cand))]
    print(f"rows with an ERROR or UNPARSED on any side: {len(errs)} {errs}")
    print()
