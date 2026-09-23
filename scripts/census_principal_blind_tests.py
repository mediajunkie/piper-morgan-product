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

Batch 5 (2026-09-23, the final triage — drove BLIND to 0) added three more
recognized call shapes, all reused via the SAME generic ``user_id=`` kwarg
check (no special-casing needed — see ``KEYED_CALL_NAMES``' inline comments
for each one's evidence): (3) ``dispatch_workflow`` (the #1124
action-dispatch rail); (4) ``_process_intent_internal`` (``IntentService``'s
real internal entry point — the "_internal" suffix meant ``process_intent(``
alone never matched it); (5) a real principal minted as a JWT access token
and driven through the production ``/api/v1/intent`` route as an
``Authorization: Bearer`` header — identity then flows through route-layer
code the static scan cannot see at all (see
``_ACCESS_TOKEN_CALL``/``_BEARER_TOKEN_USAGE`` above; scoped to files
already matched keyed, so it never inflates KEYED on its own). Batch 5 also
replaced the hand-rolled comment stripper with a stdlib-``tokenize``-based
``_scan_text()``: EVERY ``COMMENT`` and ``STRING`` token (not just whole-line
``#`` comments — also docstrings, and any other string literal, e.g. a
``patch("...process_intent")`` target path) is blanked before the ``_CALL``
scan runs, so call-shaped TEXT that isn't real code can no longer
manufacture a phantom keyed/blind file. Falls back to the untouched
original text on a tokenize failure (a few fixture files are
intentionally-invalid Python) rather than crashing.

Recognizing ``dispatch_workflow``/``_process_intent_internal`` (both real,
general keyed surfaces, not one-off flukes) widened KEYED beyond the 14
originally-known BLIND files — 6 previously wholly-invisible files turned
up BLIND once these surfaces were recognized (5 sharing one action-dispatch
WIRING-test idiom across the github/calendar/document/contextual/
productivity query-handler cohorts, 1 an ethics-denial suite) and were
triaged in the same batch alongside the original 14, on the same
evidentiary standard (see decisions.log for the full batch-5 accounting).

Known blind spots, still open: a real user_id supplied positionally to
``process_intent``/``should_offer``/``record_offer`` (only
``get_or_create_context``/``clear_context`` positional args are recognized —
extend on the next evidenced instance, not speculatively); identity
threaded via a ``ctx=RequestContext(...)`` kwarg on ``process_intent``; a
fixture/helper that builds the call elsewhere; a ``user_id=some_var`` where
the variable is None at runtime reads as live (false-live); any OTHER
production entry point that threads a real user_id into a request-scoped
mock/stub without any of the five recognized shapes above (e.g. a directly-
called handler method like ``_handle_productivity_query(intent, wf_id,
user_id)`` — evidenced as real coverage in
``test_productivity_query_handlers.py`` but deliberately NOT added as a
sixth KEYED_CALL_NAME, since handler method names are an open-ended,
unbounded family — that file was resolved via a by-design marker instead,
pointing at its own real coverage). Batch 1 (2026-09-23) fixed
test_multiuser_contracts.py; batch 2 re-censused 1033 / 92 / 35 → 30 blind;
batch 4 re-censused with the archive-exclusion + positional/current_user
recognition + by-design marking above (30 → 14); batch 5 re-censused with
the three new shapes + tokenize-based scan above, which raised KEYED to 101
(surfacing 6 more files) before triaging the combined 20 down to
BLIND=0 / BY-DESIGN=11 (was 2) — 3 true-blind authenticated-sibling
additions, 9 by-design markers, 8 false-dark census-recognition fixes (no
test-file edit: 1560, 1816, slack_components, 5 web/ JWT-route files,
standup_routing_585 dropped out of KEYED entirely as a pure docstring
false-match).
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
    # batch 5 additions — both evidenced by exactly one file, same user_id=
    # kwarg convention as the original five (generic kwarg detection in
    # _has_real_user_id already covers them; no special-casing needed):
    "dispatch_workflow",  # the #1124 action-dispatch rail (services/intent_service/
    # workflow_dispatcher.py::dispatch_workflow(workflow_type, session_id,
    # user_id=None, ...)) — evidenced in test_create_reminder_rail_1560.py,
    # which threads a real user_id here while the file's only OTHER match on
    # "process_intent" is prose inside the module docstring, not a call.
    "_process_intent_internal",  # IntentService's real internal entry point
    # (services/intent/intent_service.py) — same (message, session_id,
    # user_id=None, ctx=None) signature as the public process_intent() it's
    # wrapped by, but the "_internal" suffix means "process_intent(" alone
    # never matches it. Evidenced in test_consent_read_provenance_1816.py,
    # which calls it directly (bypassing the public wrapper) with a real
    # user_id="user-a".
)
_CALL = re.compile(r"\b(" + "|".join(KEYED_CALL_NAMES) + r")\s*\(")
_USER_ID_KWARG = re.compile(r"user_id\s*=\s*([^\n,)]+)")
_CURRENT_USER_KWARG = re.compile(r"current_user\s*=\s*([^\n,)]+)")
_BY_DESIGN_MARKER = re.compile(r"#\s*principal-blind-by-design:\s*(.+)")


# batch 5 — a comment or a DOCSTRING can contain call-shaped prose (e.g. a
# docstring referencing "process_intent (...)" or "_process_intent_internal()"
# by name to describe production behavior, or a comment mentioning
# "intent_service.process_intent (direct dispatch path)") that the static
# _CALL scan cannot distinguish from a real call. Evidenced in THREE files:
# test_create_reminder_rail_1560.py (module-docstring prose), test_slack_
# components.py (a `#` comment), test_standup_routing_585.py (two
# docstrings, both describing `_process_intent_internal()` with EMPTY
# parens — the file only ever uses `inspect.getsource()` to check the
# production text, never actually calls it). All three manufactured a false
# BLIND: each file's real principal-relevant call, if any, lives elsewhere
# (or doesn't exist at all — standup_routing_585 never calls a keyed
# surface, so it should never have been in KEYED at all).
#
# Uses the stdlib tokenizer (not a hand-rolled comment stripper) so this is
# correct for BOTH comments and docstrings/string literals in one pass,
# including the case a naive line-based comment-only strip would still miss
# (a call name appearing only inside a string literal, e.g. a
# `patch("...process_intent")` target path — not separately evidenced yet,
# but the same false-match mechanism, and free to fix once tokenizing
# anyway). COMMENT and STRING token spans are blanked to same-length
# whitespace (multi-line spans handled per-line) so every character's
# POSITION is preserved — downstream _call_text() offsets, always taken
# against the ORIGINAL text, stay valid. Falls back to the untouched
# original text on any tokenize failure (a handful of test fixture files
# are intentionally-invalid Python fragments) rather than crashing the
# census.
def _scan_text(text: str) -> str:
    import io
    import tokenize

    lines = text.split("\n")
    try:
        tokens = list(tokenize.generate_tokens(io.StringIO(text).readline))
    except (tokenize.TokenError, SyntaxError, IndentationError, ValueError):
        return text
    for tok in tokens:
        if tok.type not in (tokenize.COMMENT, tokenize.STRING):
            continue
        (sr, sc), (er, ec) = tok.start, tok.end
        if sr == er:
            line = lines[sr - 1]
            lines[sr - 1] = line[:sc] + " " * (ec - sc) + line[ec:]
        else:
            first = lines[sr - 1]
            lines[sr - 1] = first[:sc] + " " * (len(first) - sc)
            for ln in range(sr, er - 1):
                lines[ln] = " " * len(lines[ln])
            last = lines[er - 1]
            lines[er - 1] = " " * ec + last[ec:]
    return "\n".join(lines)


# batch 5 — a real principal can also be threaded end-to-end through the
# production `/api/v1/intent` ROUTE via a genuine JWT bearer token, never
# appearing as a literal user_id=/current_user= kwarg in the test file at
# all: the test mints a token for a real user_id, sends it as an
# `Authorization: Bearer` header through a real ASGI TestClient, and the
# route's own `get_current_user_optional` dependency (production code, not
# test text) extracts current_user and threads it to the stubbed
# IntentService. The test file's only KEYED_CALL_NAMES match is then the
# STUB's own `async def process_intent(self, **kwargs):` definition, which
# trivially carries no real kwarg text. Evidenced identically in 5 web/
# files (test_any_provider_gate_1823.py, test_authenticated_keyless_
# server_key_1807.py, test_byoc_key_usable_as_fallback_provider_1815.py,
# test_byoc_user_key_reaches_llm_gate_1814.py, test_keyless_pleasantry_
# 1818.py) sharing one harness idiom: a `_token()` helper calling
# `generate_access_token(user_id=<real uuid>, ...)`, used as
# `Authorization: Bearer {token}"`. Scoped to files ALREADY matched as keyed
# (never inflates the KEYED denominator on its own — plenty of pure-JWT
# tests unrelated to the composite-key concern also call
# generate_access_token, and are correctly left out of KEYED entirely).
_ACCESS_TOKEN_CALL = re.compile(r"\bgenerate_access_token\s*\(")
_BEARER_TOKEN_USAGE = re.compile(r"Bearer \{token")

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
        matches = list(_CALL.finditer(_scan_text(text)))
        if not matches:
            continue
        keyed += 1
        real = sum(1 for m in matches if _has_real_user_id(_call_text(text, m.start()), m.group(1)))
        if real == 0:
            # batch 5 JWT-bearer-route fallback (see _ACCESS_TOKEN_CALL above):
            # only ever promotes an already-keyed file, never adds one.
            token_call = _ACCESS_TOKEN_CALL.search(text)
            if (
                token_call
                and _has_real_user_id(_call_text(text, token_call.start()), "generate_access_token")
                and _BEARER_TOKEN_USAGE.search(text)
            ):
                real = 1
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
