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
DENOMINATOR: printed with every run (files scanned / keyed / blind /
by-design). ``tests/archive/`` is excluded from the scan entirely (batch 4,
2026-09-23) — it is structurally excluded from pytest collection itself
(``pytest.ini`` ``--ignore=tests/archive``, ``pyproject.toml`` addopts, and
``tests/conftest.py``'s ``collect_ignore_glob``, all independently), so a
file there can never run and was never a real blind spot — it was a census
bug (over-counting a file pytest never touches).

Two additional real-principal shapes are recognized as of batch 4: (1) a
real ``user_id`` supplied POSITIONALLY as the 2nd argument to
``get_or_create_context``/``clear_context`` (both ``(session_id, user_id=None)``
— evidenced in ``test_floor_entry_context_1570.py``'s ``clear_context(session_id,
user_id)`` cleanup calls); (2) a real, non-None ``current_user=`` kwarg on a
``process_intent(`` call — the HTTP route wrapper
(``web.api.routes.intent.process_intent(request, current_user=...)``) shares
its name with ``IntentService.process_intent`` but takes no ``user_id`` kwarg
at all, carrying identity via ``current_user.sub`` instead (evidenced in
``test_intent_conversation_ownership_1532.py``).

A file can also be marked deliberately principal-blind: a standalone comment
line ``# principal-blind-by-design: <reason>`` anywhere in the file moves it
from BLIND to BY-DESIGN (still scanned and keyed, listed separately with its
reason) — for suites where a real principal would change what the anonymous
path they're testing means (e.g. an anonymous-key gate, a session-expired-vs-
never-authenticated distinction).

Known blind spots, still open: a real user_id supplied positionally to
``process_intent``/``should_offer``/``record_offer`` (only ``get_or_create_context``/
``clear_context`` positional args are recognized — extend on the next
evidenced instance, not speculatively); identity threaded via a ``ctx=
RequestContext(...)`` kwarg on ``process_intent``; a fixture/helper that
builds the call elsewhere; a ``user_id=some_var`` where the variable is None
at runtime reads as live (false-live). Batch 1 (2026-09-23) fixed
test_multiuser_contracts.py; batch 2 re-censused 1033 / 92 / 35 → 30 blind;
batch 4 re-censused with the archive-exclusion + positional/current_user
recognition + by-design marking above.
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
_CURRENT_USER_KWARG = re.compile(r"current_user\s*=\s*([^\n,)]+)")
_BY_DESIGN_MARKER = re.compile(r"#\s*principal-blind-by-design:\s*(.+)")

# Functions whose 2nd positional argument (index 1, 0-based, `self` already
# bound) IS user_id — evidenced positional-call shape (batch 4). Extend only
# on a newly-evidenced instance, not speculatively (see module docstring).
_POSITIONAL_USER_ID_INDEX = {
    "get_or_create_context": 1,
    "clear_context": 1,
}


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


def _split_top_level_args(call: str) -> list[str]:
    """Split a call's ``(...)`` text into its top-level comma-separated
    arguments, respecting nested parens/brackets/braces and quoted strings."""
    inner = call.strip()
    if inner.startswith("(") and inner.endswith(")"):
        inner = inner[1:-1]
    args: list[str] = []
    depth = 0
    quote = None
    current: list[str] = []
    for ch in inner:
        if quote:
            current.append(ch)
            if ch == quote:
                quote = None
            continue
        if ch in "'\"":
            quote = ch
            current.append(ch)
            continue
        if ch in "([{":
            depth += 1
            current.append(ch)
            continue
        if ch in ")]}":
            depth -= 1
            current.append(ch)
            continue
        if ch == "," and depth == 0:
            args.append("".join(current))
            current = []
            continue
        current.append(ch)
    if current and "".join(current).strip():
        args.append("".join(current))
    return [a.strip() for a in args if a.strip()]


def _is_none_literal(value: str) -> bool:
    return value.strip().rstrip(",") == "None"


def _has_real_user_id(call: str, func_name: str) -> bool:
    m = _USER_ID_KWARG.search(call)
    if m and not _is_none_literal(m.group(1)):
        return True

    # (1) positional user_id — only for functions with an evidenced
    # positional-call shape in a real test file (see module docstring).
    pos_idx = _POSITIONAL_USER_ID_INDEX.get(func_name)
    if pos_idx is not None:
        args = _split_top_level_args(call)
        if len(args) > pos_idx:
            candidate = args[pos_idx].strip()
            kwarg_form = re.match(r"^([A-Za-z_]\w*)\s*=\s*(.*)$", candidate, re.S)
            if kwarg_form:
                # This position holds a `name=value` kwarg (args passed out
                # of the order we assume). Only trust it when the name IS
                # user_id — anything else means positional inference at
                # this index isn't reliable for this call.
                if kwarg_form.group(1) == "user_id" and not _is_none_literal(kwarg_form.group(2)):
                    return True
            elif not _is_none_literal(candidate):
                return True

    # (2) current_user= — the HTTP route `process_intent` wrapper carries
    # identity this way instead of `user_id=` (see module docstring).
    if func_name == "process_intent":
        cu = _CURRENT_USER_KWARG.search(call)
        if cu and not _is_none_literal(cu.group(1)):
            return True

    return False


def census() -> dict:
    scanned = keyed = 0
    results = []
    for path in sorted(TESTS.rglob("*.py")):
        if "__pycache__" in path.parts:
            continue
        # tests/archive/ is structurally excluded from pytest collection
        # itself (pytest.ini, pyproject.toml addopts, and conftest.py's
        # collect_ignore_glob all agree) — a file there can never run, so
        # it was never a real blind spot. Mirror the same exclusion here.
        if "archive" in path.relative_to(TESTS).parts:
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
        real = sum(1 for m in matches if _has_real_user_id(_call_text(text, m.start()), m.group(1)))
        by_design_match = _BY_DESIGN_MARKER.search(text)
        results.append(
            {
                "file": str(path.relative_to(ROOT)),
                "total_calls": len(matches),
                "real_user_id_calls": real,
                "blind": real == 0 and not by_design_match,
                "by_design": bool(by_design_match),
                "by_design_reason": by_design_match.group(1).strip() if by_design_match else None,
            }
        )
    blind = sorted((r for r in results if r["blind"]), key=lambda r: -r["total_calls"])
    by_design = sorted(
        (r for r in results if r["by_design"] and r["real_user_id_calls"] == 0),
        key=lambda r: r["file"],
    )
    return {
        "scanned": scanned,
        "keyed": keyed,
        "blind": len(blind),
        "by_design": len(by_design),
        "results": results,
        "blind_rows": blind,
        "by_design_rows": by_design,
    }


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
    print(
        f"SCANNED={c['scanned']} KEYED={c['keyed']} BLIND={c['blind']} "
        f"BY-DESIGN={c['by_design']}\n"
    )
    for r in c["blind_rows"]:
        print(f"{r['total_calls']:3d}  {r['file']}")
    if c["by_design_rows"]:
        print("\nBY-DESIGN (marked, excluded from BLIND):")
        for r in c["by_design_rows"]:
            print(f"{r['total_calls']:3d}  {r['file']}  — {r['by_design_reason']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
