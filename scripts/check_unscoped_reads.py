#!/usr/bin/env python3
"""check_unscoped_reads.py — ratchet guard for unscoped user-specific reads (#1419).

The multi-tenancy audit (docs/internal/architecture/current/multi-tenancy-audit-2026-07-16.md)
found the codebase's default posture is single-tenant: user-specific credentials and
config are read from GLOBAL slots (no principal), so one user's setup silently
governs every user. This guard makes the global read the *flagged* case instead of
the silent default — "nothing should be global; it should be impossible" (PM).

v1 scope — the credential layer (extends scripts/check-keychain-scoping.sh (#849),
which covers web/api/routes/ only, to ALL of services/ + web/):
  - ``*.get_api_key(provider)``      with no ``username=`` and a single positional arg
  - ``*.store_api_key(provider, key)`` with no ``username=`` and ≤2 positional args
  - ``*.delete_api_key(provider)``   with no ``username=`` and a single positional arg
  - calls to the global config-file loader surface (``load_standup_config``,
    ``get_piper_config``) from services/web code where a principal is the norm

v2 (design ratified with Arch before build): repository query methods over
owner-bearing tables whose WHERE carries no owner predicate (the #1420/#1421 class).

Reviewed exceptions carry ``# global-ok: <reason>`` on the call line (or the line
above): server-fallback keys, OAuth *app* credentials, socket-mode app token — the
audit's CLEARED set. An unannotated new global read raises the count and fails the
ratchet (tests/test_completion_ratchets.py).

Usage:
  python scripts/check_unscoped_reads.py            # summary (exit 0)
  python scripts/check_unscoped_reads.py --list     # every hit as file:line · kind
  python scripts/check_unscoped_reads.py --count    # bare integer (for the ratchet)
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


def scan_file(path: Path) -> list[tuple[int, str]]:
    """Return [(lineno, kind)] for unscoped-read hits in the file."""
    try:
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
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


def collect() -> list[str]:
    out: list[str] = []
    for root in SCAN_ROOTS:
        for f in sorted((REPO_ROOT / root).rglob("*.py")):
            if any(part in ("archive", "tests", "__pycache__") for part in f.parts):
                continue
            for lineno, kind in scan_file(f):
                out.append(f"{f.relative_to(REPO_ROOT)}:{lineno} · {kind}")
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--list", action="store_true")
    parser.add_argument("--count", action="store_true")
    args = parser.parse_args()

    hits = collect()
    if args.count:
        print(len(hits))
        return 0
    if args.list:
        for h in hits:
            print(h)
    print(
        f"unscoped-reads guard: {len(hits)} unannotated global reads of user-specific "
        f"credential/config state in services/+web/. Ceiling: scripts/ratchet_ceilings.json "
        f"(#1419 / #1424). Annotate reviewed globals with '# global-ok: <reason>'."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
