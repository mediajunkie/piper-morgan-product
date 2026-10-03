"""A-tenancy: heuristic static check of user-scoping. For each SQLAlchemy model class with a user_id/owner_id column,
find select()/update()/delete() statements on that model (single statement text, up to closing of the call chain line-window)
and classify whether the statement mentions user_id/owner_id. Heuristic; sample-verify flagged sites by hand."""
import os, re, sys, collections, ast
root = sys.argv[1]
models_src = open(os.path.join(root, "services/database/models.py")).read()
t = ast.parse(models_src); scoped = {}; allm = []
for n in t.body:
    if isinstance(n, ast.ClassDef):
        seg = ast.get_source_segment(models_src, n)
        allm.append(n.name)
        cols = re.findall(r"^\s+(user_id|owner_id|created_by|actor_user_id)\s*[:=]", seg, re.M)
        if cols: scoped[n.name] = cols[0]
stm = re.compile(r"\b(select|update|delete)\(\s*(%s)\b" % "|".join(map(re.escape, scoped)))
res = collections.Counter(); flagged = []
for d in ("services", "web", "cli"):
    for dp, _, fs in os.walk(os.path.join(root, d)):
        for f in fs:
            if not f.endswith(".py"): continue
            p = os.path.join(dp, f); lines = open(p, errors="ignore").read().split("\n")
            for i, l in enumerate(lines):
                for m in stm.finditer(l):
                    window = "\n".join(lines[i:i+8])
                    # stop window at first blank line / statement end heuristic
                    window = window.split("\n\n")[0]
                    ok = re.search(r"user_id|owner_id|created_by|_user\b|\.user ==|UserScoped|scope_to_user", window)
                    res[("scoped" if ok else "UNSCOPED", m.group(1))] += 1
                    if not ok: flagged.append(f"{os.path.relpath(p, root)}:{i+1} {m.group(1)}({m.group(2)})")
print("models total", len(allm), "with user/owner column", len(scoped))
print(dict(res))
by = collections.Counter(x.split(":")[0] for x in flagged)
print("unscoped statements by file (top):", by.most_common(15))
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "A-tenancy-flagged.txt"), "w").write("\n".join(flagged))
