#!/usr/bin/env python3
"""check_silent_death.py — ratchet guard for the silent-death exception pattern (#1423).

The pattern: a broad ``except Exception`` (or bare ``except``) handler that never
re-raises — converting a broken feature into a plausible default so the failure is
invisible to users and tests. Census A (2026-07-16, epic #1424) classified all 274
core-path instances; this guard holds the line so the count can only go DOWN.

What counts as a hit:
  - an ``except`` handler whose type is ``Exception``/``BaseException`` (alone or in
    a tuple), or a bare ``except:``, AND
  - the handler body contains no ``raise``, AND
  - the handler's first line carries no ``# silent-ok: <reason>`` annotation.

``# silent-ok:`` is the reviewed-exception mechanism: a handler that is genuinely a
LEGIT boundary (per Census A's classification) gets annotated with a one-line
rationale when touched, which removes it from the count. New code must either
narrow the exception type, re-raise, or carry the annotation — an unannotated new
broad swallow raises the count and fails the ratchet (tests/test_completion_ratchets.py).

Usage:
  python scripts/check_silent_death.py            # summary + count (exit 0)
  python scripts/check_silent_death.py --list     # every hit as file:line
  python scripts/check_silent_death.py --count    # bare integer (for the ratchet)

Scope: the Census A core-path module set (see CORE_PATHS). Extending scope means
re-freezing the ceiling in scripts/ratchet_ceilings.json in the same commit.
"""

from __future__ import annotations

import argparse
import ast
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Census A scope (2026-07-16). Keep in lockstep with ratchet_ceilings.json.
CORE_PATHS = [
    "services/intent",
    "services/intent_service",
    "services/personality",
    "services/knowledge",
    "services/knowledge_graph",
    "services/consciousness",
    "services/llm",
    "services/config",
    "services/todo",
    "web/api/routes/intent.py",
]

ANNOTATION = "silent-ok:"


def _is_broad(handler: ast.ExceptHandler) -> bool:
    """True for ``except:``, ``except Exception``, ``except BaseException`` (incl. tuples)."""
    t = handler.type
    if t is None:
        return True
    names = []
    if isinstance(t, ast.Name):
        names = [t.id]
    elif isinstance(t, ast.Tuple):
        names = [e.id for e in t.elts if isinstance(e, ast.Name)]
    return any(n in ("Exception", "BaseException") for n in names)


def _reraises(handler: ast.ExceptHandler) -> bool:
    return any(isinstance(node, ast.Raise) for node in ast.walk(handler))


def _annotated(handler: ast.ExceptHandler, source_lines: list[str]) -> bool:
    """``# silent-ok: <reason>`` on the except line or the line directly above it."""
    idx = handler.lineno - 1
    candidates = source_lines[max(0, idx - 1) : idx + 1]
    return any(ANNOTATION in line for line in candidates)


def scan_file(path: Path) -> list[tuple[int, bool]]:
    """Return [(lineno, annotated)] for every broad no-reraise handler in the file."""
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return []
    lines = source.splitlines()
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler) and _is_broad(node) and not _reraises(node):
            hits.append((node.lineno, _annotated(node, lines)))
    return hits


def collect() -> tuple[list[str], int]:
    """Return (unannotated hit list as 'path:line', annotated count)."""
    unannotated: list[str] = []
    annotated_count = 0
    for rel in CORE_PATHS:
        base = REPO_ROOT / rel
        files = [base] if base.is_file() else sorted(base.rglob("*.py"))
        for f in files:
            if "archive" in f.parts or "tests" in f.parts:
                continue
            for lineno, is_annotated in scan_file(f):
                if is_annotated:
                    annotated_count += 1
                else:
                    unannotated.append(f"{f.relative_to(REPO_ROOT)}:{lineno}")
    return unannotated, annotated_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true", help="print every unannotated hit")
    parser.add_argument("--count", action="store_true", help="print bare count only")
    args = parser.parse_args()

    unannotated, annotated = collect()
    if args.count:
        print(len(unannotated))
        return 0
    if args.list:
        for hit in unannotated:
            print(hit)
    print(
        f"silent-death guard: {len(unannotated)} unannotated broad no-reraise handlers "
        f"on the core path ({annotated} annotated silent-ok). "
        f"Ceiling lives in scripts/ratchet_ceilings.json (#1423 / #1424)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
