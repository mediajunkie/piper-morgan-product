"""A-dupes: duplicate basenames across packages + identical function bodies (>=8 lines, normalized AST dump)."""
import ast, os, sys, hashlib, collections
root = sys.argv[1]; names = collections.defaultdict(list); bodies = collections.defaultdict(list)
for d in ("services", "web", "cli"):
    for dp, _, fs in os.walk(os.path.join(root, d)):
        for f in fs:
            if not f.endswith(".py") or f == "__init__.py": continue
            p = os.path.join(dp, f); names[f].append(os.path.relpath(p, root))
            try: t = ast.parse(open(p, errors="ignore").read())
            except Exception: continue
            for n in ast.walk(t):
                if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.end_lineno - n.lineno >= 8:
                    b = n.body[1:] if (n.body and isinstance(n.body[0], ast.Expr) and isinstance(getattr(n.body[0], "value", None), ast.Constant)) else n.body
                    h = hashlib.md5("".join(ast.dump(x) for x in b).encode()).hexdigest()
                    bodies[h].append((os.path.relpath(p, root), n.name, n.end_lineno - n.lineno))
dn = {k: v for k, v in names.items() if len(v) > 1}
print("duplicate basenames:", len(dn))
for k, v in sorted(dn.items(), key=lambda x: -len(x[1]))[:25]: print(" ", k, v)
db = [v for v in bodies.values() if len(v) > 1 and len({x[0] for x in v}) > 1]
print("identical function bodies across files (>=8 lines):", len(db), "groups;", sum(len(v) for v in db), "functions;", sum(v[0][2]*(len(v)-1) for v in db), "redundant lines")
for v in sorted(db, key=lambda v: -v[0][2])[:12]: print(" ", v[0][2], [(a, b) for a, b, _ in v])
