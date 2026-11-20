"""Pass 2 of the 2406 classifier screen: each re-screened row, x6 on main and the
candidate, judged by the 10-30 clauses on the counted outcome, with main's most
frequent outcome as the expected label. Usage: analyze_p2.py DIR"""

import re
import sys
from collections import Counter
from pathlib import Path

D = Path(sys.argv[1])


def load(name: str) -> dict:
    rows = {}
    for line in (D / f"report-p2-{name}.md").read_text().splitlines():
        if not line.startswith("| ") or line.startswith("| phrase"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        counts: Counter = Counter()
        for part in cells[1].split(", "):
            m = re.match(r"`(.*)` ×(\d+)$", part)
            if m:
                counts[m.group(1)] += int(m.group(2))
        rows[cells[0]] = counts
    return rows


def show(c: Counter) -> str:
    return ", ".join(f"{k} ×{v}" for k, v in c.most_common())


failed = 0
for base in "AB":
    main, cand = load(f"main-{base}"), load(f"cand-{base}")
    print(f"## base {base}: {len(main)} rows")
    for phrase, m in main.items():
        c = cand[phrase]
        label, main_n = m.most_common(1)[0]
        cand_n = c.get(label, 0)
        reasons = []
        if main_n >= 5 and cand_n < 5:
            reasons.append(f"clause 1: main {main_n}/6 on {label}, candidate {cand_n}/6")
        if main_n <= 4 and cand_n < main_n - 1:
            reasons.append(f"clause 2: main {main_n}/6 on {label}, candidate {cand_n}/6")
        new = [f"{k} {v}/6" for k, v in c.items() if k not in m and v >= 3]
        if new:
            reasons.append("clause 3: new outcome " + ", ".join(new))
        failed += bool(reasons)
        print(f"{'FAIL' if reasons else 'pass'} | {phrase}")
        print(f"     main: {show(m)}")
        print(f"     cand: {show(c)}")
        for r in reasons:
            print(f"     {r}")
    print()
print(f"rows failing: {failed}")
