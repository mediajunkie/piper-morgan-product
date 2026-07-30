#!/usr/bin/env python3
"""
reachability-map.py — answer "is this layer live?" from the import graph, not from a name list.

WHY THIS EXISTS (2026-07-29, Arch): I characterized the spatial subsystem three times in
ten hours and was wrong twice, because each time I enumerated modules from a filename
pattern I *recalled* and then verified only those. `github_spatial.py` sat in the exact
directory I was describing and was never checked; a feature-flag string was nearly recorded
as a live importer. The error was not carelessness — it was treating
"I verified the modules I enumerated" as "I verified the layer."

So: enumerate from the FILESYSTEM, resolve importers from the IMPORT GRAPH, and report
transitive reachability from real entrypoints. No hand-kept list to drift.
Related: methodology-44 (Clear Is Not a Measurement), methodology-43 (Name the Layer).

USAGE
  scripts/reachability-map.py services/integrations/spatial services/intelligence/spatial
  scripts/reachability-map.py --entrypoints main.py web/app.py services/mux

The output states its own scope (files scanned, entrypoints used) because a report that
can't show its work is indistinguishable from one that measured nothing.
"""

import argparse
import ast
import os
import sys
from collections import defaultdict

DEFAULT_ENTRYPOINTS = ["main.py", "web/app.py"]
SEARCH_ROOTS = ["services", "web", "main.py"]


def py_files(roots):
    out = []
    for r in roots:
        if os.path.isfile(r) and r.endswith(".py"):
            out.append(r)
        for dirpath, dirnames, filenames in os.walk(r):
            dirnames[:] = [d for d in dirnames if d not in {"__pycache__", ".git"}]
            for fn in filenames:
                if fn.endswith(".py"):
                    out.append(os.path.join(dirpath, fn))
    return sorted(set(out))


def is_test(path):
    base = os.path.basename(path)
    return "test" in path.split(os.sep)[0:1] or base.startswith("test_") or "/tests/" in path


def module_name(path):
    """services/foo/bar.py -> services.foo.bar"""
    return path[:-3].replace(os.sep, ".") if path.endswith(".py") else path


def imports_of(path):
    """Real imports via AST — not a regex. A regex over import lines both misses
    relative forms and invents edges from strings/comments; both failure modes bit me."""
    try:
        tree = ast.parse(open(path, encoding="utf-8", errors="replace").read())
    except SyntaxError:
        return set()
    found = set()
    pkg = os.path.dirname(path).replace(os.sep, ".")
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                found.add(a.name)
        elif isinstance(node, ast.ImportFrom):
            if node.level:  # relative import — resolve against this file's package
                parts = pkg.split(".")
                base = ".".join(parts[: len(parts) - (node.level - 1)]) if node.level > 1 else pkg
                found.add(f"{base}.{node.module}" if node.module else base)
            elif node.module:
                found.add(node.module)
                for a in node.names:  # `from pkg.mod import Thing` may target pkg.mod.Thing
                    found.add(f"{node.module}.{a.name}")
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("targets", nargs="+", help="directories or files to characterize")
    ap.add_argument("--entrypoints", nargs="*", default=DEFAULT_ENTRYPOINTS)
    ap.add_argument("--include-tests", action="store_true")
    args = ap.parse_args()

    all_files = py_files(SEARCH_ROOTS)
    scanned = [f for f in all_files if args.include_tests or not is_test(f)]

    # forward edges: module -> set(imported module names)
    fwd = {module_name(f): imports_of(f) for f in scanned}
    # reverse edges: module -> importers, matching on prefix so pkg.mod.Thing counts for pkg.mod
    rev = defaultdict(set)
    known = set(fwd)
    for src, targets in fwd.items():
        for t in targets:
            if t in known:
                rev[t].add(src)
            else:
                # `from pkg.mod import Thing` -> attribute the edge to pkg.mod
                parent = t.rsplit(".", 1)[0]
                if parent in known:
                    rev[parent].add(src)

    # transitive reachability from entrypoints
    entry_mods = [module_name(e) for e in args.entrypoints if os.path.exists(e)]
    reachable, stack = set(), list(entry_mods)
    while stack:
        m = stack.pop()
        if m in reachable:
            continue
        reachable.add(m)
        for t in fwd.get(m, ()):
            cand = t if t in known else t.rsplit(".", 1)[0]
            if cand in known and cand not in reachable:
                stack.append(cand)

    target_files = py_files(args.targets)
    target_files = [f for f in target_files if args.include_tests or not is_test(f)]

    print(f"SCOPE: {len(scanned)} non-test .py files scanned under {SEARCH_ROOTS}")
    print(f"ENTRYPOINTS: {entry_mods or '(none resolved)'}")
    print(f"TARGETS: {len(target_files)} file(s) under {args.targets}")
    # ⚠️ State the instrument's blindness in its own output, with the number, every run.
    # This app registers routers by STRING (web/app.py: register(app, "web.api.routes.places", ...)),
    # so static import-following cannot cross that boundary and misses most of the app.
    pct = (100 * len(reachable) // max(len(known), 1))
    print(
        f"STATIC-REACH COVERAGE: {len(reachable)} of {len(known)} modules ({pct}%) are reachable by "
        f"following imports from the entrypoints."
    )
    print(
        "  ⚠️ The remaining "
        f"{len(known) - len(reachable)} are NOT known-dead — routers are registered by string in "
        "web/app.py, which static traversal cannot follow. A blank reach column means "
        "UNKNOWN, never 'unreachable'. Use the importer count as the live signal."
    )
    print()
    print(f"{'module':52} {'importers':>9}  {'static':>9}  who")
    print("-" * 112)

    cold = []
    for f in target_files:
        m = module_name(f)
        if m.endswith(".__init__"):
            continue
        importers = sorted(rev.get(m, ()))
        # a module whose only importers are inside the target set is a closed island
        outside = [i for i in importers if not any(i.startswith(module_name(t).rstrip(".")) for t in args.targets)]
        # NEVER print "no" here. Static traversal cannot see string-registered routers, so
        # absence of a static path is INCONCLUSIVE. Rendering it as "no" is precisely the
        # m-44 defect (a clear emitted identically whether it measured or couldn't see).
        reach = "YES" if m in reachable else "unknown"
        if not importers:
            cold.append((m, "no importers"))
        elif not outside:
            cold.append((m, "closed island — importers all inside target set"))
        short = ", ".join(i.replace("services.", "s.") for i in importers[:3]) or "NONE"
        print(f"{m:52} {len(importers):>9}  {reach:>5}  {short}")

    print("\nCOLD CANDIDATES (state the denominator, don't imply a total):")
    if cold:
        for m, why in cold:
            print(f"  - {m}  [{why}]")
    else:
        print("  none")
    print(f"\n{len(cold)} of {len(target_files)} target file(s) have no outside importer.")
    print("NOTE: 'reach' is transitive-static reachability. A deferred (function-level) import")
    print("      still counts as an edge here — construction vs dispatch is a DIFFERENT question")
    print("      this tool does not answer. Check the call site before claiming a module runs.")


if __name__ == "__main__":
    sys.exit(main())
