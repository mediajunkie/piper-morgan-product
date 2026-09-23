#!/usr/bin/env python3
"""#1533 — census of principal-BLIND test suites.

A test file is *keyed* when it calls a surface whose state is keyed by the
composite ``{user_id or 'anonymous'}:{session_id}`` (the two builders are
``services/intent_service/conversation_context.py::_context_key`` and
``services/intent_service/soft_invocation.py::WorkflowOfferService._key``);
it is *blind* when none of those calls passes a non-None ``user_id`` — the
anonymous and authenticated keys then coincide and no assertion in the file
can see the user dimension of what it certifies (m-44: a probe where the
keys coincide is a config check, not a verification).

Usage:
    scripts/census_principal_blind_tests.py            # table, blind files by call count
    scripts/census_principal_blind_tests.py --count    # just the blind count (ratchet-shaped)
    scripts/census_principal_blind_tests.py --json out.json

LAYER: static text scan of tests/**/*.py — a call's balanced-paren text is
searched for a ``user_id=`` kwarg whose value is not the literal ``None``.
DENOMINATOR: printed with every run (files scanned / keyed / blind). Known
blind spots, stated: a real user_id supplied positionally, or via a fixture
that builds the call elsewhere, reads as blind (false-dark, fails loudly by
name rather than passing silently); a ``user_id=some_var`` where the variable
is None at runtime reads as live (false-live). Batch 1 (2026-09-23) fixed
test_multiuser_contracts.py; batch 2 re-censused 1033 / 92 / 35 → 30 blind.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TESTS = ROOT / "tests"

KEYED_CALL_NAMES = (
    "process_intent",
    "get_or_create_context",
    "should_offer",
    "record_offer",
    "clear_context",
)
_CALL = re.compile(r"\b(" + "|".join(KEYED_CALL_NAMES) + r")\s*\(")
_USER_ID_KWARG = re.compile(r"user_id\s*=\s*([^\n,)]+)")


def _call_text(text: str, start: int) -> str:
    i = text.index("(", start)
    depth = 0
    for j in range(i, len(text)):
        if text[j] == "(":
            depth += 1
        elif text[j] == ")":
            depth -= 1
            if depth == 0:
                return text[i : j + 1]
    return text[i:]


def _has_real_user_id(call: str) -> bool:
    m = _USER_ID_KWARG.search(call)
    return bool(m) and m.group(1).strip().rstrip(",") != "None"


def census() -> dict:
    scanned = keyed = 0
    results = []
    for path in sorted(TESTS.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        scanned += 1
        try:
            text = path.read_text()
        except (UnicodeDecodeError, OSError):
            continue
        matches = list(_CALL.finditer(text))
        if not matches:
            continue
        keyed += 1
        real = sum(1 for m in matches if _has_real_user_id(_call_text(text, m.start())))
        results.append(
            {
                "file": str(path.relative_to(ROOT)),
                "total_calls": len(matches),
                "real_user_id_calls": real,
                "blind": real == 0,
            }
        )
    blind = sorted((r for r in results if r["blind"]), key=lambda r: -r["total_calls"])
    return {"scanned": scanned, "keyed": keyed, "blind": len(blind), "results": results, "blind_rows": blind}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--count", action="store_true", help="print only the blind-file count")
    ap.add_argument("--json", metavar="PATH", help="also write the full census as JSON")
    args = ap.parse_args()
    c = census()
    if args.json:
        Path(args.json).write_text(json.dumps(c, indent=2) + "\n")
    if args.count:
        print(c["blind"])
        return 0
    print(f"SCANNED={c['scanned']} KEYED={c['keyed']} BLIND={c['blind']}\n")
    for r in c["blind_rows"]:
        print(f"{r['total_calls']:3d}  {r['file']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
