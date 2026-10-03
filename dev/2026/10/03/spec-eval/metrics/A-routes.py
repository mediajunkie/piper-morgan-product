"""A-routes: static enumeration of FastAPI routes (router prefix + decorator path), auth-dependency detection,
and match against AuthMiddleware exempt list (startswith semantics, as in _should_exclude_path)."""
import ast, os, sys, re, collections
root = sys.argv[1]
mw = open(os.path.join(root, "services/auth/auth_middleware.py")).read()
seg = mw[mw.index("EXEMPT_OPENAPI_PATHS"):mw.index("AUTH_EXEMPT_JUSTIFIED: Dict")]
exempt = sorted(set(re.findall(r'^\s*"(/[^"]*)"', seg, re.M)))
routes = []
AUTHDEP = re.compile(r"get_current_user|require_auth|require_admin|get_user_id|current_user|require_user|get_authenticated|verify_token|require_dev_environment|_require_")
for dp, _, fs in os.walk(root):
    if "/tests" in dp or "node_modules" in dp or "skunkworks" in dp: continue
    for f in fs:
        if not f.endswith(".py"): continue
        p = os.path.join(dp, f); src = open(p, errors="ignore").read()
        if "APIRouter" not in src and "FastAPI(" not in src: continue
        t = ast.parse(src); prefixes = {}
        for n in ast.walk(t):
            if isinstance(n, ast.Assign) and isinstance(n.value, ast.Call) and getattr(n.value.func, "id", getattr(n.value.func, "attr", "")) in ("APIRouter", "FastAPI"):
                pre = ""; deps = False
                for k in n.value.keywords:
                    if k.arg == "prefix" and isinstance(k.value, ast.Constant): pre = k.value.value
                    if k.arg == "dependencies": deps = True
                for tg in n.targets:
                    if isinstance(tg, ast.Name): prefixes[tg.id] = (pre, deps)
        for n in ast.walk(t):
            if not isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)): continue
            for d in n.decorator_list:
                if isinstance(d, ast.Call) and isinstance(d.func, ast.Attribute) and d.func.attr in ("get", "post", "put", "patch", "delete", "api_route", "websocket") and isinstance(d.func.value, ast.Name) and d.func.value.id in prefixes:
                    path = d.args[0].value if d.args and isinstance(d.args[0], ast.Constant) else "?"
                    pre, rdeps = prefixes[d.func.value.id]
                    body = ast.get_source_segment(src, n) or ""
                    sig = body.split(":\n", 1)[0]
                    routes.append(dict(file=os.path.relpath(p, root), line=n.lineno, method=d.func.attr.upper(), path=pre + path,
                                       sig_auth=bool(AUTHDEP.search(sig)) or rdeps, body_user=bool(re.search(r"user_id|request\.state\.user", body))))
def exempted(path): return [e for e in exempt if path.startswith(e)]
out = collections.Counter()
ex_rows = []
for r in routes:
    e = exempted(r["path"])
    r["exempt"] = bool(e)
    out["total"] += 1
    out["sig_auth"] += r["sig_auth"]
    if e:
        out["exempt"] += 1
        ex_rows.append(r)
print("exempt list:", len(exempt), "entries")
print(dict(out))
print("routes w/o signature-level auth dep (rely on global middleware):", sum(1 for r in routes if not r["sig_auth"]))
print("\nEXEMPT routes (startswith match):")
for r in sorted(ex_rows, key=lambda r: r["path"]):
    print(f'  {r["method"]:6} {r["path"]:70} sigauth={int(r["sig_auth"])} user_ref={int(r["body_user"])} {r["file"]}:{r["line"]}')
