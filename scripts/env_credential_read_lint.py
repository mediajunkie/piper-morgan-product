#!/usr/bin/env python3
"""#1551 workstream 5 (Arch's design 2026-11-04 15:54; xian: lands before any new invite) —
the tenancy guard's lint half: an env read of a credential- or identity-shaped name is a
site that must be ruled.

The class it stops (#1461, #2123, #2266, and on 11-04 ``PIPER_GITHUB_HANDLE`` and
``PIPER_DEFAULT_REPO``): a deployment-wide value read from the environment stands in
for an account's credential or identity on a path that serves a user principal. The
13:16 family rule: no ``PIPER_*`` or provider env value stands in for a per-account
setting or identity on a path serving a user principal. A read is allowed only where
the module is ruled SYSTEM_ONLY (below, each with its reason) or baselined for a ruling.

What is a site: a read through ``os.environ[...]``, ``os.environ.get(...)``,
``os.getenv(...)``, ``environ.get(...)`` or ``getenv(...)`` whose first argument is a
string, either written there or resolved from a module-level constant in the same file
(``ENV_DEFAULT_REPO = "PIPER_DEFAULT_REPO"`` then ``os.environ.get(ENV_DEFAULT_REPO)``,
the shape a literal regex misses) or imported by name from another module under the repo
(Arch 16:38), and whose name contains one of the CREDENTIAL_WORDS.
Also a call to one of the known config HELPERS that themselves read such names.

Ratchet pattern (mirrors scripts/principal_threading_lint.py): today's sites are
baselined; a NEW site fails CI; the baseline ratchets to zero as each site is ruled
system-only (moved to SYSTEM_ONLY with its reason) or made per-account.

Usage:
    python scripts/env_credential_read_lint.py [PATH ...]         # default: services + web
    python scripts/env_credential_read_lint.py --summary
    python scripts/env_credential_read_lint.py --baseline FILE    # fail only on NEW sites
    python scripts/env_credential_read_lint.py --write-baseline FILE

Concept: docs/internal/architecture/current/multi-tenancy-audit-2026-07-16.md
"""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

CREDENTIAL_WORDS = (
    "TOKEN",
    "KEY",
    "SECRET",
    "HANDLE",
    "LOGIN",
    "REPO",
    "OWNER",
    "EMAIL",
    "PASSWORD",
    "CREDENTIAL",
    "USERNAME",
    # plurals, so a file or list of them counts too
    "TOKENS",
    "KEYS",
    "SECRETS",
    "REPOS",
    "CREDENTIALS",
)


def _is_credential_name(name: str) -> bool:
    """A segment of the name is one of the words (``GITHUB_TOKEN`` yes; ``PIPER_KEYCHAIN_TIMEOUT``
    no: KEYCHAIN is not KEY)."""
    return any(seg in CREDENTIAL_WORDS for seg in name.upper().split("_"))


# Config helpers that read credential names on the caller's behalf. A call to one of
# these is a site too, so a read cannot hide behind a wrapper (Arch 15:54: "or the
# config helpers"). Names, not paths: the helper's own module carries its read as well.
HELPERS = frozenset(
    {
        "get_authentication_token",  # GitHubConfigService: env token when no user key
        "get_environment",  # the connector config services' env snapshot
    }
)

# Modules whose env reads are system-only by construction: the value is the
# deployment's own (its database, its signing key, its OAuth App registration), never
# a stand-in for an account's credential or identity. Each entry carries its reason.
# Adding a module here is a ruling (Arch), not a convenience.
SYSTEM_ONLY: Dict[str, str] = {
    # (filled by rulings; empty at the baseline commit so every site is visible)
}


def new_against_baseline(current: Counter, baseline: Counter) -> Counter:
    """Signatures present more often now than in the baseline: the ratchet."""
    return current - baseline


@dataclass(frozen=True)
class Violation:
    line_no: int
    env_name: str
    snippet: str


def _module_path(module: str, roots: Optional[List[Path]] = None) -> Optional[Path]:
    """The file for a dotted module name under the repo root, else None."""
    rel = Path(*module.split("."))
    for cand in (rel.with_suffix(".py"), rel / "__init__.py"):
        if cand.is_file():
            return cand
    return None


def _imported_constants(tree: ast.AST, depth: int = 0) -> Dict[str, str]:
    """``from pkg.mod import NAME`` where NAME is a string constant in that module (Arch
    2026-11-04 16:38: the constant may live in another module, not only locally). One
    level of indirection is followed; deeper chains stay unresolved and are a lint gap
    to name, not a false negative to accept silently."""
    out: Dict[str, str] = {}
    if depth > 1:
        return out
    for node in getattr(tree, "body", []):
        if not isinstance(node, ast.ImportFrom) or not node.module or node.level:
            continue
        path = _module_path(node.module)
        if path is None:
            continue
        try:
            other = ast.parse(path.read_text(encoding="utf-8", errors="replace"))
        except (OSError, SyntaxError):
            continue
        consts = _module_constants(other, follow_imports=False)
        for alias in node.names:
            if alias.name in consts:
                out[alias.asname or alias.name] = consts[alias.name]
    return out


def _module_constants(tree: ast.AST, follow_imports: bool = True) -> Dict[str, str]:
    """Module-level ``NAME = "STRING"`` assignments, so a read through a constant
    resolves to the environment variable it names; plus such constants imported
    by name from another module under the repo."""
    out: Dict[str, str] = _imported_constants(tree) if follow_imports else {}
    for node in getattr(tree, "body", []):
        if isinstance(node, ast.Assign) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str):
                for t in node.targets:
                    if isinstance(t, ast.Name):
                        out[t.id] = node.value.value
        elif isinstance(node, ast.AnnAssign) and isinstance(node.value, ast.Constant):
            if isinstance(node.value.value, str) and isinstance(node.target, ast.Name):
                out[node.target.id] = node.value.value
    return out


def _env_name(arg: ast.AST, constants: Dict[str, str]) -> Optional[str]:
    if isinstance(arg, ast.Constant) and isinstance(arg.value, str):
        return arg.value
    if isinstance(arg, ast.Name):
        return constants.get(arg.id)
    return None


def _is_env_read(node: ast.AST) -> Optional[ast.AST]:
    """The name argument when ``node`` reads the environment, else None."""
    if isinstance(node, ast.Subscript):
        v = node.value
        if isinstance(v, ast.Attribute) and v.attr == "environ":
            return node.slice
        if isinstance(v, ast.Name) and v.id == "environ":
            return node.slice
        return None
    if isinstance(node, ast.Call) and node.args:
        f = node.func
        if isinstance(f, ast.Attribute):
            if f.attr == "getenv":  # os.getenv(NAME)
                return node.args[0]
            if f.attr == "get" and (
                (isinstance(f.value, ast.Attribute) and f.value.attr == "environ")
                or (isinstance(f.value, ast.Name) and f.value.id == "environ")
            ):
                return node.args[0]
        if isinstance(f, ast.Name) and f.id == "getenv":
            return node.args[0]
    return None


def _helper_call(node: ast.AST) -> Optional[str]:
    if isinstance(node, ast.Call):
        f = node.func
        name = (
            f.attr if isinstance(f, ast.Attribute) else (f.id if isinstance(f, ast.Name) else None)
        )
        if name in HELPERS:
            return name
    return None


def find_credential_env_reads(text: str, filename: Optional[str] = None) -> List[Violation]:
    """Every site in one file's source. Unparseable files yield []."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []
    constants = _module_constants(tree)
    out: List[Violation] = []
    for node in ast.walk(tree):
        arg = _is_env_read(node)
        if arg is not None:
            name = _env_name(arg, constants)
            if name and _is_credential_name(name):
                out.append(Violation(node.lineno, name, _snip(node)))
            continue
        helper = _helper_call(node)
        if helper:
            out.append(Violation(node.lineno, f"helper:{helper}", _snip(node)))
    return out


def _snip(node: ast.AST) -> str:
    try:
        return ast.unparse(node)[:120]
    except Exception:  # pragma: no cover - defensive
        return f"<read at line {getattr(node, 'lineno', '?')}>"


def lint_paths(paths: List[Path]) -> List[tuple]:
    results = []
    for p in paths:
        if p.as_posix() in SYSTEM_ONLY:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for v in find_credential_env_reads(text, str(p)):
            results.append((p, v))
    return results


def _signature(path: Path, v: Violation) -> str:
    # No line number: stable across code movement (as the sibling lints).
    return f"{path.as_posix()}|{v.env_name}|{v.snippet}"


def _gather(targets: List[str]) -> List[Path]:
    roots = [Path(t) for t in targets] if targets else [Path("services"), Path("web")]
    files: List[Path] = []
    for r in roots:
        if r.is_dir():
            files.extend(sorted(r.rglob("*.py")))
        elif r.suffix == ".py":
            files.append(r)
    return files


_FIX_HINT = (
    "A deployment env value must not stand in for an account's credential or identity on a "
    "path that serves a user principal (#1551, the 2026-11-04 family rule). Read the account's "
    "own value through its store, refuse honestly, or have Arch rule the module SYSTEM_ONLY "
    "with its reason."
)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="env credential-read lint gate (#1551)")
    parser.add_argument("paths", nargs="*", help="files/dirs (default: services + web)")
    parser.add_argument("--summary", action="store_true")
    parser.add_argument(
        "--baseline", metavar="FILE", help="ratchet: fail only on sites NOT in FILE"
    )
    parser.add_argument("--write-baseline", metavar="FILE", help="snapshot current sites to FILE")
    ns = parser.parse_args(argv)

    files = _gather(ns.paths)
    results = lint_paths(files)
    current = Counter(_signature(p, v) for p, v in results)

    if ns.write_baseline:
        Path(ns.write_baseline).write_text(
            "\n".join(sorted(current.elements())) + "\n", encoding="utf-8"
        )
        print(
            f"env-credential-read-lint: wrote baseline ({sum(current.values())} site(s)) "
            f"to {ns.write_baseline}"
        )
        return 0

    if ns.summary:
        files_hit = len({p for p, _ in results})
        names = Counter(v.env_name for _, v in results)
        print(
            f"env-credential-read-lint: {len(results)} site(s) in {files_hit} file(s) "
            f"across {len(files)} scanned; {len(names)} distinct name(s)"
        )
        for name, n in names.most_common():
            print(f"  {n:3d} {name}")
        return 1 if results else 0

    if ns.baseline:
        base = Counter(
            ln for ln in Path(ns.baseline).read_text(encoding="utf-8").splitlines() if ln.strip()
        )
        new = new_against_baseline(current, base)
        if new:
            print(
                f"env-credential-read-lint: {sum(new.values())} NEW credential env read "
                f"site(s) (not in baseline {ns.baseline}):"
            )
            for sig in sorted(new.elements()):
                path, name, snip = sig.split("|", 2)
                print(f"  {path}: {name}: {snip}")
            print(f"\n{_FIX_HINT}")
            return 1
        fixed = sum((base - current).values())
        msg = f"env-credential-read-lint: no new sites ({sum(current.values())} baselined"
        msg += f"; {fixed} ruled — rerun --write-baseline to ratchet down)." if fixed else ")."
        print(msg)
        return 0

    for p, v in results:
        print(f"{p}:{v.line_no}: {v.env_name}: {v.snippet}")
    if results:
        print(f"\nenv-credential-read-lint: {len(results)} site(s). {_FIX_HINT}")
    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())
