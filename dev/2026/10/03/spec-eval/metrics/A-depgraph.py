"""A-depgraph: import graph over snapshot-code python (services, web, cli, main*.py).
Usage: python A-depgraph.py /home/user/snapshot-code"""
import ast, os, sys, collections, json
root = sys.argv[1]
SRC = ["services", "web", "cli", "shared"]
mods = {}
def modname(p):
    rel = os.path.relpath(p, root)[:-3].replace(os.sep, ".")
    return rel[:-9] if rel.endswith(".__init__") else rel
files = []
for d in SRC:
    for dp, _, fs in os.walk(os.path.join(root, d)):
        for f in fs:
            if f.endswith(".py"): files.append(os.path.join(dp, f))
files += [os.path.join(root, f) for f in ("main.py", "main_mcp.py")]
for f in files: mods[modname(f)] = f
# importers from everywhere (incl tests/scripts) for dead-code detection
allfiles = list(files)
for d in ["tests", "scripts", "tools", "alembic"]:
    for dp, _, fs in os.walk(os.path.join(root, d)):
        for f in fs:
            if f.endswith(".py"): allfiles.append(os.path.join(dp, f))
allfiles += [os.path.join(root, f) for f in os.listdir(root) if f.endswith(".py")]
def resolve(name):
    while name:
        if name in mods: return name
        name = name.rpartition(".")[0]
    return None
edges = collections.defaultdict(set)   # prod-only edges
str_edges = collections.defaultdict(set)  # dynamic string-literal module refs
import re
imported_by_any = collections.defaultdict(set)
funcs = []; parse_err = []
for f in set(allfiles):
    try: tree = ast.parse(open(f, encoding="utf-8", errors="ignore").read())
    except Exception as e: parse_err.append(f); continue
    me = modname(f) if os.path.relpath(f, root).split(os.sep)[0] in SRC or f.endswith(("main.py","main_mcp.py")) else None
    pkg = (modname(f) if f.endswith("__init__.py") else modname(f).rpartition(".")[0])
    for n in ast.walk(tree):
        targets = []
        if isinstance(n, ast.Import): targets = [a.name for a in n.names]
        elif isinstance(n, ast.ImportFrom):
            base = n.module or ""
            if n.level:
                parts = pkg.split(".")
                parts = parts[:len(parts)-(n.level-1)] if n.level > 1 else parts
                base = ".".join(parts + ([base] if base else []))
            targets = [base + "." + a.name for a in n.names] + [base]
        for t in targets:
            r = resolve(t)
            if r and r != (me or modname(f)):
                imported_by_any[r].add(modname(f))
                if me: edges[me].add(r)
        if me and isinstance(n, ast.Constant) and isinstance(n.value, str) and re.fullmatch(r"[a-z_][\w.]*(:\w+)?", n.value) and "." in n.value:
            r = resolve(n.value.split(":")[0])
            if r and r != me: str_edges[me].add(r)
        if me and isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs.append((n.end_lineno - n.lineno + 1, os.path.relpath(f, root), n.name))
# also string-based dynamic imports (importlib / include_router strings)
txt_all = {f: open(f, encoding="utf-8", errors="ignore").read() for f in allfiles}
def top(m): p = m.split("."); return ".".join(p[:2]) if p[0] in ("services","web") else p[0]
pk = collections.defaultdict(set)
for a, bs in edges.items():
    for b in bs:
        if top(a) != top(b): pk[top(a)].add(top(b))
fanin = collections.Counter(b for a in pk for b in pk[a])
out = {}
out["n_prod_modules"] = len([m for m in mods])
out["parse_errors"] = parse_err
out["pkg_fanout_top"] = sorted(((len(v), k) for k, v in pk.items()), reverse=True)[:15]
out["pkg_fanin_top"] = fanin.most_common(15)
# SCC (Tarjan) at module level
sys.setrecursionlimit(100000)
idx = {}; low = {}; st = []; on = set(); sccs = []; c = [0]
def sc(v):
    idx[v] = low[v] = c[0]; c[0] += 1; st.append(v); on.add(v)
    for w in edges.get(v, ()):
        if w not in idx: sc(w); low[v] = min(low[v], low[w])
        elif w in on: low[v] = min(low[v], idx[w])
    if low[v] == idx[v]:
        comp = []
        while True:
            w = st.pop(); on.discard(w); comp.append(w)
            if w == v: break
        if len(comp) > 1: sccs.append(comp)
for v in list(mods):
    if v not in idx: sc(v)
out["module_cycles_count"] = len(sccs)
out["module_cycle_sizes"] = sorted((len(s) for s in sccs), reverse=True)
out["largest_cycle_sample"] = sorted(max(sccs, key=len))[:25] if sccs else []
# pkg-level cycles
pidx = {}; plow = {}; pst = []; pon = set(); psccs = []; pc = [0]
def psc(v):
    pidx[v] = plow[v] = pc[0]; pc[0] += 1; pst.append(v); pon.add(v)
    for w in pk.get(v, ()):
        if w not in pidx: psc(w); plow[v] = min(plow[v], plow[w])
        elif w in pon: plow[v] = min(plow[v], pidx[w])
    if plow[v] == pidx[v]:
        comp = []
        while True:
            w = pst.pop(); pon.discard(w); comp.append(w)
            if w == v: break
        if len(comp) > 1: psccs.append(sorted(comp))
for v in list(pk):
    if v not in pidx: psc(v)
out["pkg_cycles"] = psccs
# module fan-in (prod)
mfanin = collections.Counter(b for a in edges for b in edges[a])
out["module_fanin_top"] = mfanin.most_common(12)
out["module_fanout_top"] = sorted(((len(v), k) for k, v in edges.items()), reverse=True)[:12]
# dead: prod modules with no importer from anywhere and no dotted-path string mention
dead = []
for m, f in mods.items():
    if m.endswith("__init__") or f.endswith("__init__.py") or m in ("main", "main_mcp"): continue
    if imported_by_any.get(m): continue
    short = m
    mentioned = any((short in t) for ff, t in txt_all.items() if ff != f)
    dead.append((m, sum(1 for _ in open(f, errors="ignore")), mentioned))
out["no_importer_count"] = len(dead)
out["no_importer_not_even_string_mentioned"] = len([d for d in dead if not d[2]])
out["no_importer_loc"] = sum(d[1] for d in dead)
out["no_importer_strict_loc"] = sum(d[1] for d in dead if not d[2])
# prod-only reachability from entry points
reach = set(); stack = [m for m in ("main", "main_mcp") if m in mods] + [m for m in mods if m.startswith("cli.")]
while stack:
    v = stack.pop()
    if v in reach: continue
    reach.add(v)
    # importing a.b.c also executes a and a.b
    p = v
    while "." in p:
        p = p.rpartition(".")[0]
        if p in mods: stack.append(p)
    stack.extend(edges.get(v, ())); stack.extend(str_edges.get(v, ()))
unreach = [m for m in mods if m not in reach]
out["prod_modules_total"] = len(mods)
out["static_unreachable_from_entrypoints"] = len(unreach)
out["static_unreachable_loc"] = sum(sum(1 for _ in open(mods[m], errors="ignore")) for m in unreach)
by = collections.Counter(top(m) for m in unreach)
out["unreachable_by_pkg_top"] = by.most_common(15)
funcs.sort(reverse=True)
out["largest_functions"] = funcs[:12]
out["functions_over_200"] = len([x for x in funcs if x[0] > 200])
out["functions_total"] = len(funcs)
json.dump(out, open(os.path.join(os.path.dirname(__file__), "A-depgraph.out.json"), "w"), indent=1)
json.dump({"dead": sorted(dead, key=lambda d: -d[1]), "unreach": sorted(unreach)}, open(os.path.join(os.path.dirname(__file__), "A-dead.out.json"), "w"), indent=1)
for k, v in out.items(): print(k, ":", v)
