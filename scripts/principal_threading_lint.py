#!/usr/bin/env python3
"""#1252 P6 / ADR-071 D5 — principal-threading lint gate.

Catches the *principal-degradation* anti-pattern: pulling the user principal
out of a loose context dict with a silent ``... if ctx else None`` fallback —

    user_id = context.get("user_id") if context else None
    g(user_id=intent.context.get("user_id") if intent.context else None)

— instead of threading the principal as a required parameter from the host
boundary. When the key is absent the principal silently becomes ``None``,
which downstream reads then treat as "unscoped" — the exact recurring failure
ADR-071 exists to stop (#1241: "not our first attempt").

AST-based (the ternary shape is awkward + false-positive-prone via regex).
Ratchet pattern — mirrors scripts/token_lint.py + scripts/native_dialog_lint.py:
pre-existing sites are baselined and tolerated; NEW ones fail CI; the baseline
ratchets to zero as D4 threading replaces each site.

Usage:
    python scripts/principal_threading_lint.py [PATH ...]        # default: services + web
    python scripts/principal_threading_lint.py --summary
    python scripts/principal_threading_lint.py --baseline FILE   # fail only on NEW sites
    python scripts/principal_threading_lint.py --write-baseline FILE
"""

from __future__ import annotations

import ast
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional

PRINCIPAL_KEY = "user_id"


def new_against_baseline(current: Counter, baseline: Counter) -> Counter:
    """Signatures present more often now than in baseline — the ratchet (same as
    the F3 token-lint / F1 native-dialog-lint): pre-existing sites tolerated,
    NEW ones fail CI."""
    return current - baseline  # multiset difference


@dataclass(frozen=True)
class Violation:
    line_no: int
    snippet: str


def _is_get_principal_call(node: ast.AST) -> bool:
    """True for ``<expr>.get("user_id")`` (one positional string arg)."""
    return (
        isinstance(node, ast.Call)
        and isinstance(node.func, ast.Attribute)
        and node.func.attr == "get"
        and len(node.args) >= 1
        and isinstance(node.args[0], ast.Constant)
        and node.args[0].value == PRINCIPAL_KEY
    )


def find_principal_degradations(text: str, filename: Optional[str] = None) -> List[Violation]:
    """The ``<expr>.get("user_id") if <test> else None`` degradation sites in
    one file's source. Robust to unparseable files (returns [])."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return []

    out: List[Violation] = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.IfExp)
            and isinstance(node.orelse, ast.Constant)
            and node.orelse.value is None
            and _is_get_principal_call(node.body)
        ):
            try:
                snippet = ast.unparse(node)
            except Exception:  # pragma: no cover - defensive
                snippet = f"<IfExp at line {node.lineno}>"
            out.append(Violation(node.lineno, snippet[:120]))
    return out


def lint_paths(paths: List[Path]) -> List[tuple]:
    results = []
    for p in paths:
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        for v in find_principal_degradations(text, str(p)):
            results.append((p, v))
    return results


def _signature(path: Path, v: Violation) -> str:
    # No line number — stable across code movement (mirrors native-dialog-lint).
    return f"{path.as_posix()}|{v.snippet}"


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
    "Thread the principal as a required parameter from the host boundary; don't "
    "degrade to None via `context.get('user_id') if ... else None` (ADR-071 D4/D5)."
)


def main(argv: Optional[List[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(
        description="principal-threading lint gate (#1252 P6 / ADR-071 D5)"
    )
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
            f"principal-threading-lint: wrote baseline ({sum(current.values())} site(s)) "
            f"to {ns.write_baseline}"
        )
        return 0

    if ns.summary:
        print(
            f"principal-threading-lint: {len(results)} degradation site(s) across {len(files)} file(s)"
        )
        return 1 if results else 0

    if ns.baseline:
        base = Counter(
            ln for ln in Path(ns.baseline).read_text(encoding="utf-8").splitlines() if ln.strip()
        )
        new = new_against_baseline(current, base)
        if new:
            print(
                f"principal-threading-lint: {sum(new.values())} NEW principal-degradation "
                f"site(s) (not in baseline {ns.baseline}):"
            )
            for sig in sorted(new.elements()):
                path, snip = sig.split("|", 1)
                print(f"  {path}: {snip}")
            print(f"\n{_FIX_HINT}")
            return 1
        fixed = sum((base - current).values())
        msg = f"principal-threading-lint: no new degradations ({sum(current.values())} baselined"
        msg += f"; {fixed} migrated — rerun --write-baseline to ratchet down)." if fixed else ")."
        print(msg)
        return 0

    for p, v in results:
        print(f"{p}:{v.line_no}: {v.snippet}")
    if results:
        print(f"\nprincipal-threading-lint: {len(results)} degradation site(s). {_FIX_HINT}")
    return 1 if results else 0


if __name__ == "__main__":
    raise SystemExit(main())
