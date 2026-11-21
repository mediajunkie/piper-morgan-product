"""Arch's 20:00Z 2026-11-20 bar on issue 2301, read from the five parsed reports.

Usage: bar.py <folder holding report-*.md and phrases.txt>
Clause 4 is judged from the route and project columns, which the report counts
separately; where both are 6 of 6 the joint count is 6 of 6. Any other row is
printed for a read of the raw replies.
"""

import collections
import re
import sys

A = sys.argv[1]
READ_TARGETS = ["T4", "T5", "T6", "T7"]
QUOTED_IN_THE_LINE = "T4"
PROJECT_OF = {
    "T4": "Mobile Redesign",
    "T5": "Launch",
    "T6": "Mobile Redesign",
    "T7": "Website Refresh",
}


def counts(cell):
    out = collections.Counter()
    for part in re.split(r", (?=[`\"(])", cell):
        m = re.match(r"(.*) ×(\d+)$", part.strip())
        if m:
            out[m.group(1).strip("`")] += int(m.group(2))
    return out


def load(name):
    rows = {}
    for line in open(f"{A}/report-{name}.md"):
        if not line.startswith("| ") or line.startswith("| phrase") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        rows[cells[0]] = {
            "routes": counts(cells[1]),
            "project": counts(cells[3]) if len(cells) > 3 else collections.Counter(),
            "text": counts(cells[4]) if len(cells) > 4 else collections.Counter(),
        }
    return rows


def fmt(c):
    return ", ".join(f"{k} ×{v}" for k, v in c.most_common()) if c else "-"


def top(r):
    return r["routes"].most_common(1)[0][0]


ids = [line.rstrip("\n").split("|", 1) for line in open(f"{A}/phrases.txt")]
tm, tc = load("table-main"), load("table-cand")
fails = []

print("## TABLE (main | candidate)")
for i, p in ids:
    m, c = tm[p], tc[p]
    print(f"{i} | {p}")
    print(f"   main: {fmt(m['routes'])} | project: {fmt(m['project'])} | text: {fmt(m['text'])}")
    print(f"   cand: {fmt(c['routes'])} | project: {fmt(c['project'])} | text: {fmt(c['text'])}")

print("\n## CLAUSE 1 and 2 (every row except the read targets; K1 and K2 are in the table)")
for i, p in ids:
    if i in READ_TARGETS:
        continue
    m, c = tm[p]["routes"], tc[p]["routes"]
    label, n = m.most_common(1)[0]
    got = c.get(label, 0)
    need = 5 if n >= 5 else n - 1
    new = {k: v for k, v in c.items() if k not in m and v >= 3}
    ok = got >= need and not new
    if not ok:
        fails.append(f"clause 1: {i} {label} main {n}/6, cand {got}/6 (need {need}); new {new}")
    print(
        f"  {i}: {label} main {n}/6 cand {got}/6 need {need}; new label >=3: {new or 'none'}  {'ok' if ok else 'FAIL'}"
    )

print("\n## CLAUSE 3 (no dropped todo)")
for i, p in ids:
    if i in ("D2", "D4"):
        none = tc[p]["project"].get("(none)", 0)
        total = sum(tc[p]["project"].values())
        ok = none == total
        if not ok:
            fails.append(f"clause 3: {i} carries a project: {fmt(tc[p]['project'])}")
        print(f"  {i}: cand project {fmt(tc[p]['project'])}  {'ok' if ok else 'FAIL'}")
    if i.startswith("C"):
        mt, ct = tm[p]["text"], tc[p]["text"]
        kept_m = sum(v for k, v in mt.items() if k != "(none)")
        kept_c = sum(v for k, v in ct.items() if k != "(none)")
        ok = kept_c >= kept_m
        if not ok:
            fails.append(f"clause 3: {i} text kept main {kept_m}/6, cand {kept_c}/6")
        print(f"  {i}: text kept main {kept_m}/6 cand {kept_c}/6  {'ok' if ok else 'FAIL'}")

print("\n## CLAUSE 4 (the read targets)")
lower = {}
for i, p in ids:
    if i not in READ_TARGETS:
        continue
    c = tc[p]
    route = c["routes"].get("list_project_todos", 0)
    named = sum(
        v
        for k, v in c["project"].items()
        if k.strip('"').casefold()
        in (PROJECT_OF[i].casefold(), PROJECT_OF[i].casefold() + " project")
    )
    lower[i] = max(0, route + named - 6)  # the joint count's lower bound
    upper = min(route, named)
    exact = (
        ""
        if lower[i] == upper
        else f" (joint between {lower[i]} and {upper}: read the raw replies)"
    )
    print(
        f"  {i}: list_project_todos {route}/6, project named {named}/6{exact}; main: {fmt(tm[p]['routes'])}"
    )
counted = [i for i in READ_TARGETS if i != QUOTED_IN_THE_LINE]
passing = [i for i in counted if lower[i] >= 5]
if len(passing) < 3:
    fails.append(f"clause 4: {len(passing)} of the 3 counted targets at 5 of 6 or more ({passing})")
if lower["T7"] < 5:
    fails.append("clause 4: T7 does not pass")
if any(v < 3 for v in lower.values()):
    fails.append(f"clause 4: a target below 3 of 6: {lower}")

cm, cc, cd = load("corpus-main"), load("corpus-control"), load("corpus-cand")
print("\n## CLAUSE 5 (corpus)", len(cm), len(cc), len(cd))
noise = [p for p in cm if top(cm[p]) != top(cc[p])]
print("main against control differ:", len(noise))
third = [p for p in cm if top(cd[p]) not in (top(cm[p]), top(cc[p]))]
print("candidate on a label neither main nor control produced:", len(third))
for p in third:
    print(f"  {p!r}: main {top(cm[p])} | control {top(cc[p])} | cand {top(cd[p])}")
if len(third) > 40:
    fails.append(f"clause 5: {len(third)} rows on a third label (over 40)")
print("candidate differs from main (any):", sum(1 for p in cm if top(cd[p]) != top(cm[p])))
on_read = [p for p in cd if top(cd[p]) == "list_project_todos"]
print("candidate corpus rows on list_project_todos:", on_read)

print("\n## VERDICT")
if fails:
    print("NO-GO")
    for f in fails:
        print("  -", f)
else:
    print(
        f"table clauses 1 to 4 pass; corpus: {len(third)} rows for the x6 re-screen under clause 1"
    )
