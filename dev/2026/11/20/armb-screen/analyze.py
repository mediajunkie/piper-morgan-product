import re, sys, collections
A = sys.argv[1]
def load(name):
    rows = {}
    for line in open(f"{A}/report-{name}.md"):
        if not line.startswith("| ") or line.startswith("| phrase") or line.startswith("|---"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split(" | ")]
        phrase = cells[0]
        def counts(cell):
            out = collections.Counter()
            for part in re.split(r", (?=[`\"(])", cell):
                m = re.match(r"(.*) ×(\d+)$", part.strip())
                if m:
                    out[m.group(1).strip("`")] += int(m.group(2))
            return out
        rows[phrase] = {"routes": counts(cells[1]), "project": counts(cells[3]) if len(cells) > 3 else None,
                        "text": counts(cells[4]) if len(cells) > 4 else None}
    return rows
ids = [l.rstrip("\n").split("|", 1) for l in open(f"{A}/phrases.txt")]
tm, tc = load("table-main"), load("table-cand")
def fmt(c): return ", ".join(f"{k} ×{v}" for k, v in c.most_common()) if c else "-"
print("## TABLE (main | candidate)")
for i, p in ids:
    m, c = tm[p], tc[p]
    print(f"{i} | {p}\n   main: {fmt(m['routes'])} | project: {fmt(m['project'])} | text: {fmt(m['text'])}\n   cand: {fmt(c['routes'])} | project: {fmt(c['project'])} | text: {fmt(c['text'])}")
cm, cc, cd = load("corpus-main"), load("corpus-control"), load("corpus-cand")
print("\n## CORPUS", len(cm), len(cc), len(cd))
top = lambda r: r["routes"].most_common(1)[0][0]
noise = [p for p in cm if top(cm[p]) != top(cc[p])]
print("main vs control differ:", len(noise))
third = [p for p in cm if top(cd[p]) not in (top(cm[p]), top(cc[p]))]
print("candidate on a label neither main nor control produced:", len(third))
for p in third: print(f"  {p!r}: main {top(cm[p])} | control {top(cc[p])} | cand {top(cd[p])}")
diff_main = [p for p in cm if top(cd[p]) != top(cm[p])]
print("candidate differs from main (any):", len(diff_main))
print("\n## candidate corpus replies on create_todo with a project:")
n = 0
for p, r in cd.items():
    if top(r) == "create_todo" and r["project"] and any(k != "(none)" for k in r["project"]):
        n += 1; print(f"  {p!r}: project {fmt(r['project'])}")
print("count:", n, "of", sum(1 for p in cd if top(cd[p]) == "create_todo"), "create_todo rows")
print("candidate corpus rows on list_project_todos:", [p for p in cd if top(cd[p]) == "list_project_todos"])
