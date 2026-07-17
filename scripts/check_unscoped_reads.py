#!/usr/bin/env python3
"""check_unscoped_reads.py — ratchet guard for unscoped user-specific reads.

ADR-079 (Owner-Scoping Integrity Contract) D2's mechanical enforcement: every
read of owner-bearing state is owner-scoped by construction; an unscoped read
fails the build unless allowlisted with a reason. Two rule sets:

D2a — CREDENTIAL ACCESS NEEDS A PRINCIPAL (v1, ceiling key `unscoped_reads`):
  - ``*.get_api_key(provider)``      with no ``username=`` and a single positional arg
  - ``*.store_api_key(provider, key)`` with no ``username=`` and ≤2 positional args
  - ``*.delete_api_key(provider)``   with no ``username=`` and a single positional arg
  - calls to the global config-file loader surface (``load_standup_config``,
    ``get_piper_config``) from services/web code where a principal is the norm

D2b — OWNER-BEARING REPOSITORY READS NEED AN OWNER PREDICATE (v2, ceiling key
`unscoped_repo_reads`): a function that queries an owner-bearing model
(``select(Model)`` / ``session.query(Model)``) and never references that
model's owner column (``Model.owner_id`` / ``.user_id`` / ``.session_id`` —
the predicate proxy) is a violation.

D3 — THE OWNER-BEARING MODEL SET IS DERIVED, NEVER HAND-LISTED: any class in
services/ with a ``__tablename__`` and a Column-assigned ``owner_id``/``user_id``
is in scope automatically. A new owner-bearing table is auto-covered; the lint
cannot go stale (make-drift-impossible applied to the enforcement itself).

D4/D6 — ALLOWLIST NAMES *HOW*: reviewed exceptions carry ``# global-ok: <how>``
on the flagged line (or the line above). The rationale must name WHY the read
is legitimately global or HOW the scoping actually happens (e.g. "scoped via
_readable_base_ids(owner_id) subquery, ADR-071 P2") — a bare "cleared" does not
meet the ADR-079 D4 bar. Indirect scoping (join/subquery) is the expected
false-positive class (D6): allowlist it with the named mechanism.

Known under-detection (documented, calibrated in warn-mode per ADR-079):
conditional scoping (``if session_id: query = query.where(...)``) passes D2b
because the predicate appears in the function — but violates D1 (an
owner_id=None branch CAN return cross-user data). Those are tracked as m-40
shims (#1252); the ratchet still catches NEW fully-unscoped reads.

Usage:
  python scripts/check_unscoped_reads.py               # summary (exit 0)
  python scripts/check_unscoped_reads.py --list        # every hit, tagged [cred]/[repo]
  python scripts/check_unscoped_reads.py --count       # bare int: credential rule (D2a)
  python scripts/check_unscoped_reads.py --count-repo  # bare int: repo-read rule (D2b)
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
SCAN_ROOTS = ["services", "web"]
ANNOTATION = "global-ok:"

KEYCHAIN_METHODS = {
    # method name -> max positional args that still means "no principal supplied"
    "get_api_key": 1,
    "delete_api_key": 1,
    "store_api_key": 2,
}
PRINCIPAL_KWARGS = {"username", "user_id", "owner_id"}
CONFIG_LOADER_CALLS = {"load_standup_config", "get_piper_config"}

# Predicate-proxy columns: referencing Model.<one of these> anywhere in the
# querying function counts as owner-scoping intent (session_id included because
# legacy repos filter owner_id via a param named session_id, e.g. KnowledgeNodeDB).
OWNER_COLUMNS = {"owner_id", "user_id", "session_id"}


def _iter_py(root: Path):
    for f in sorted(root.rglob("*.py")):
        if any(p in ("archive", "tests", "__pycache__") for p in f.parts):
            continue
        yield f


def _parse(path: Path) -> ast.AST | None:
    try:
        return ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, UnicodeDecodeError):
        return None


# ---------------------------------------------------------------------------
# D3 — derive the owner-bearing model set
# ---------------------------------------------------------------------------


def derive_owner_models() -> dict[str, str]:
    """Return {model_class_name: 'relpath:line'} for every class in services/
    that has a __tablename__ and a Column/mapped_column-assigned owner_id or
    user_id. Never hand-listed (ADR-079 D3)."""
    models: dict[str, str] = {}
    for f in _iter_py(REPO_ROOT / "services"):
        tree = _parse(f)
        if tree is None:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.ClassDef):
                continue
            has_tablename = False
            owner_col = False
            for stmt in node.body:
                targets = []
                if isinstance(stmt, ast.Assign):
                    targets = [t.id for t in stmt.targets if isinstance(t, ast.Name)]
                    value = stmt.value
                elif isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name):
                    targets = [stmt.target.id]
                    value = stmt.value
                else:
                    continue
                if "__tablename__" in targets:
                    has_tablename = True
                if any(t in ("owner_id", "user_id") for t in targets):
                    if isinstance(value, ast.Call):
                        callee = value.func
                        name = (
                            callee.id
                            if isinstance(callee, ast.Name)
                            else callee.attr if isinstance(callee, ast.Attribute) else ""
                        )
                        if name in ("Column", "mapped_column"):
                            owner_col = True
            if has_tablename and owner_col:
                models[node.name] = f"{f.relative_to(REPO_ROOT)}:{node.lineno}"
    return models


# ---------------------------------------------------------------------------
# D2a — credential/config reads (v1 rule set, unchanged semantics)
# ---------------------------------------------------------------------------


def _annotated(lineno: int, source_lines: list[str]) -> bool:
    idx = lineno - 1
    candidates = source_lines[max(0, idx - 1) : idx + 1]
    return any(ANNOTATION in line for line in candidates)


def _call_name(node: ast.Call) -> str | None:
    if isinstance(node.func, ast.Attribute):
        return node.func.attr
    if isinstance(node.func, ast.Name):
        return node.func.id
    return None


def scan_credential_reads(path: Path) -> list[tuple[int, str]]:
    source = path.read_text(encoding="utf-8")
    tree = _parse(path)
    if tree is None:
        return []
    lines = source.splitlines()
    hits: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node)
        if name in KEYCHAIN_METHODS:
            has_principal_kwarg = any(
                kw.arg in PRINCIPAL_KWARGS for kw in node.keywords if kw.arg
            )
            if len(node.args) <= KEYCHAIN_METHODS[name] and not has_principal_kwarg:
                if not _annotated(node.lineno, lines):
                    hits.append((node.lineno, f"keychain.{name} (no principal)"))
        elif name in CONFIG_LOADER_CALLS:
            if not _annotated(node.lineno, lines):
                hits.append((node.lineno, f"{name} (global config file)"))
    return hits


# ---------------------------------------------------------------------------
# D2b — owner-bearing repository reads (v2 rule set)
# ---------------------------------------------------------------------------


def _queried_owner_models(call: ast.Call, owner_models: set[str]) -> set[str]:
    """Owner-bearing model names queried by a select(...)/.query(...) call."""
    name = _call_name(call)
    if name not in ("select", "query"):
        return set()
    queried: set[str] = set()
    for arg in call.args:
        if isinstance(arg, ast.Name) and arg.id in owner_models:
            queried.add(arg.id)
        # select(Model.col, Model.other) — attribute form
        elif isinstance(arg, ast.Attribute) and isinstance(arg.value, ast.Name):
            if arg.value.id in owner_models:
                queried.add(arg.value.id)
    return queried


def _owner_predicate_models(func: ast.AST, owner_models: set[str]) -> set[str]:
    """Models whose owner column (owner_id/user_id/session_id) is referenced
    anywhere in the function — the predicate proxy."""
    scoped: set[str] = set()
    for node in ast.walk(func):
        if (
            isinstance(node, ast.Attribute)
            and node.attr in OWNER_COLUMNS
            and isinstance(node.value, ast.Name)
            and node.value.id in owner_models
        ):
            scoped.add(node.value.id)
    return scoped


def scan_repo_reads(path: Path, owner_models: set[str]) -> list[tuple[int, str]]:
    source = path.read_text(encoding="utf-8")
    tree = _parse(path)
    if tree is None:
        return []
    lines = source.splitlines()
    hits: list[tuple[int, str]] = []
    for func in ast.walk(tree):
        if not isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        # Collect this function's queried owner-models + its predicate coverage.
        queried: dict[str, int] = {}  # model -> first query lineno
        for node in ast.walk(func):
            if isinstance(node, ast.Call):
                for model in _queried_owner_models(node, owner_models):
                    queried.setdefault(model, node.lineno)
        if not queried:
            continue
        scoped = _owner_predicate_models(func, owner_models)
        for model, lineno in queried.items():
            if model in scoped:
                continue
            if _annotated(lineno, lines):
                continue
            hits.append(
                (lineno, f"repo-read {model} (no owner predicate in {func.name})")
            )
    return hits


# ---------------------------------------------------------------------------


def collect() -> tuple[list[str], list[str]]:
    owner_models = set(derive_owner_models())
    cred: list[str] = []
    repo: list[str] = []
    for root in SCAN_ROOTS:
        for f in _iter_py(REPO_ROOT / root):
            rel = f.relative_to(REPO_ROOT)
            for lineno, kind in scan_credential_reads(f):
                cred.append(f"{rel}:{lineno} · {kind}")
            for lineno, kind in scan_repo_reads(f, owner_models):
                repo.append(f"{rel}:{lineno} · {kind}")
    return cred, repo


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--count", action="store_true", help="D2a credential-rule count")
    parser.add_argument("--count-repo", action="store_true", help="D2b repo-read-rule count")
    parser.add_argument("--models", action="store_true", help="print the derived model set")
    args = parser.parse_args()

    if args.models:
        for name, where in sorted(derive_owner_models().items()):
            print(f"{name}  ({where})")
        return 0

    cred, repo = collect()
    if args.count:
        print(len(cred))
        return 0
    if args.count_repo:
        print(len(repo))
        return 0
    if args.list:
        for h in cred:
            print(f"[cred] {h}")
        for h in repo:
            print(f"[repo] {h}")
    n_models = len(derive_owner_models())
    print(
        f"unscoped-reads guard (ADR-079 D2): {len(cred)} credential hits (D2a), "
        f"{len(repo)} repo-read hits (D2b) across {n_models} derived owner-bearing "
        f"models (D3). Ceilings: scripts/ratchet_ceilings.json. Allowlist with "
        f"'# global-ok: <how it is scoped / why global>' (D4/D6)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
