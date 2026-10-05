"""#1458 — every resource/tool handler registered on the MCP app resolves identity via
``current_user_id()`` (AST enforcement mirroring ``tests/test_architecture_enforcement.py``'s
idiom: a derived scan over real source, not a hand-maintained allowlist).

Arch's rescoped #1458 ruling (2026-10-05,
``mailboxes/pa/inbox/rule-arch-to-pa-cc-exec-1458-gates-listing-rescoped-to-mcp-reachable-
code-three-acs-already-met-2026-10-05.md``) names this explicitly: the middleware-plus-
raising-accessor in ``identity.py`` is already a mechanism, not a one-off audit, and the
ONE piece still missing is "an AST/enforcement test that every handler registered on the
MCP app (resources now, tools next) calls ``current_user_id()``. That way a new handler
joins the contract by existing."

Mechanism (not a literal substring/regex match — see ``_registered_handler_names`` and
``_referenced_names``):

1. Find every function registered as an MCP handler by its STRUCTURAL call shape —
   ``<expr>.resource(...)(<name>)`` / ``<expr>.tool(...)(<name>)`` (the exact idiom
   ``services/mcp/server/resources.py`` uses) — via AST, so a reformatted call site is
   still found and a non-registration call to something coincidentally named
   ``resource``/``tool`` is not mistaken for one.
2. For each registered handler, compute whether ``current_user_id`` is reachable from
   it, where "reachable" is NOT limited to a direct ``Call`` — it is the transitive
   closure over every NAME referenced anywhere in the function's body that is ALSO a
   function defined in the same source. This is required, not a convenience: the real
   composite tool, ``what_piper_knows_about_me``, never calls ``current_user_id()``
   directly — it calls ``_section(_read_profile)`` / ``_section(_read_colleague_model)``
   / ``_section(_read_github_issues)``, each of which calls it internally. A
   direct-call-only checker would FALSE-POSITIVE on real, compliant code; a reference-
   based transitive checker correctly credits composition while still catching a
   handler that neither calls it nor composes anything that does (pinned by the
   synthetic negative cases below).
3. A registered handler whose body the checker cannot locate in the same source (e.g.
   name registered but imported from elsewhere) is a VIOLATION, not a silent pass —
   "can't prove compliance" must never read as "compliant".

LAYER: static/source (AST), like the rest of ``test_architecture_enforcement.py`` — this
is a build-time contract, not a runtime behavioral proof (that's
``test_two_caller_behavioural_1458.py``, a different file, different layer).

DENOMINATOR: the two files the hosted MCP endpoint can register handlers from today —
``services/mcp/server/resources.py`` (the three resources + the composite tool) and
``services/mcp/server/app.py`` (registers nothing itself today, scanned anyway so a
future handler added there is caught without a test change).
"""

from __future__ import annotations

import ast
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[5]
_RESOURCES_PY = _ROOT / "services" / "mcp" / "server" / "resources.py"
_APP_PY = _ROOT / "services" / "mcp" / "server" / "app.py"

IDENTITY_FUNC_NAME = "current_user_id"
REGISTRATION_METHODS = {"resource", "tool"}


def _module_function_defs(tree: ast.AST) -> dict[str, ast.AST]:
    """Every FunctionDef/AsyncFunctionDef in ``tree`` by name (last-wins on a
    duplicate name, matching Python's own redefinition semantics)."""
    funcs: dict[str, ast.AST] = {}
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            funcs[node.name] = node
    return funcs


def _referenced_names(func_node: ast.AST) -> set[str]:
    """Every ``Name.id`` and ``Attribute.attr`` referenced anywhere in the
    function's body — deliberately broader than "direct Call targets" (see
    module docstring point 2: a handler that passes another function BY NAME
    to a composition helper still reaches that function's contract)."""
    names: set[str] = set()
    for node in ast.walk(func_node):
        if isinstance(node, ast.Name):
            names.add(node.id)
        elif isinstance(node, ast.Attribute):
            names.add(node.attr)
    return names


def _registered_handler_names(tree: ast.AST) -> list[str]:
    """Every function name passed as the handler to a
    ``<expr>.resource(...)(<name>)`` / ``<expr>.tool(...)(<name>)`` call —
    found structurally: the outer Call's ``func`` must itself be a Call whose
    ``func`` is an Attribute named ``resource`` or ``tool``."""
    handlers: list[str] = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        inner = node.func
        if not (
            isinstance(inner, ast.Call)
            and isinstance(inner.func, ast.Attribute)
            and inner.func.attr in REGISTRATION_METHODS
        ):
            continue
        for arg in node.args:
            if isinstance(arg, ast.Name):
                handlers.append(arg.id)
    return handlers


def _handlers_missing_identity_check(sources: list[str]) -> list[str]:
    """The reusable mechanism (module docstring). ``sources`` may be more
    than one file's content so a handler in one file can compose a function
    defined in another."""
    funcs: dict[str, ast.AST] = {}
    handlers: list[str] = []
    for source in sources:
        tree = ast.parse(source)
        funcs.update(_module_function_defs(tree))
        handlers.extend(_registered_handler_names(tree))

    missing: list[str] = []
    for handler in handlers:
        root = funcs.get(handler)
        if root is None:
            # Registered but this checker can't see its body -> can't prove
            # compliance -> violation, never a silent pass.
            missing.append(handler)
            continue

        seen: set[str] = set()
        frontier = [handler]
        found = False
        while frontier and not found:
            name = frontier.pop()
            if name in seen:
                continue
            seen.add(name)
            fn = funcs.get(name)
            if fn is None:
                continue
            refs = _referenced_names(fn)
            if IDENTITY_FUNC_NAME in refs:
                found = True
                break
            frontier.extend(r for r in refs if r in funcs and r not in seen)
        if not found:
            missing.append(handler)

    return missing


class TestRegisteredHandlersCallCurrentUserId:
    """Run the mechanism against the REAL server source."""

    def test_detector_finds_exactly_todays_known_handlers(self) -> None:
        """Vacuity guard (m-44): prove the registration-site scan actually
        matched something, and matched the full known set — not a vacuous
        pass from a detector that silently stopped matching anything."""
        sources = [_RESOURCES_PY.read_text(encoding="utf-8"), _APP_PY.read_text(encoding="utf-8")]
        handlers: list[str] = []
        for src in sources:
            handlers.extend(_registered_handler_names(ast.parse(src)))

        assert set(handlers) == {
            "_read_profile",
            "_read_colleague_model",
            "_read_github_issues",
            "what_piper_knows_about_me",
        }, (
            f"registration-site detector found {sorted(set(handlers))} — the AST shape "
            "changed; fix the detector, not this assertion"
        )

    def test_real_resources_and_tools_all_reach_current_user_id(self) -> None:
        sources = [_RESOURCES_PY.read_text(encoding="utf-8"), _APP_PY.read_text(encoding="utf-8")]
        missing = _handlers_missing_identity_check(sources)
        assert missing == [], (
            f"handler(s) registered on the MCP app with no reachable current_user_id() "
            f"call: {missing} — every resource/tool handler must resolve identity before "
            f"touching server state (#1458)"
        )

    def test_composite_tool_reaches_current_user_id_only_transitively(self) -> None:
        """``what_piper_knows_about_me`` never calls ``current_user_id()`` in
        its OWN body — it composes ``_read_profile`` / ``_read_colleague_model``
        / ``_read_github_issues`` via ``_section(read)``. Pin that premise
        directly, so this test actually exercises the transitive path (module
        docstring point 2) rather than passing by coincidence if resources.py
        is ever rewritten to call it directly."""
        src = _RESOURCES_PY.read_text(encoding="utf-8")
        funcs = _module_function_defs(ast.parse(src))
        composite = funcs["what_piper_knows_about_me"]
        assert IDENTITY_FUNC_NAME not in _referenced_names(composite), (
            "premise changed: what_piper_knows_about_me now references current_user_id "
            "directly — this test no longer proves the transitive path; revisit it "
            "rather than deleting it"
        )
        assert _handlers_missing_identity_check([src]) == []


class TestEnforcementCatchesAMissingCall:
    """The negative case the #1458 dispatch explicitly requires: prove the
    mechanism actually FAILS for a handler that never resolves identity,
    against a synthetic module built for exactly this purpose — not merely
    that it happens to pass against today's real, already-compliant code."""

    @staticmethod
    def _synthetic_module() -> str:
        return (
            "def current_user_id():\n"
            "    return 'stub'\n"
            "\n"
            "def good_handler():\n"
            "    current_user_id()\n"
            "    return {}\n"
            "\n"
            "def bad_handler():\n"
            "    return {}\n"
            "\n"
            "def register(app):\n"
            "    app.resource('piper://good')(good_handler)\n"
            "    app.tool(name='bad')(bad_handler)\n"
        )

    def test_handler_missing_the_call_is_flagged(self) -> None:
        missing = _handlers_missing_identity_check([self._synthetic_module()])
        assert missing == ["bad_handler"]

    def test_compliant_handler_in_the_same_module_is_not_flagged(self) -> None:
        missing = _handlers_missing_identity_check([self._synthetic_module()])
        assert "good_handler" not in missing

    def test_transitive_composition_credited_like_the_real_composite_tool(self) -> None:
        """Mirrors ``what_piper_knows_about_me``'s real shape exactly: a
        composing function that never calls ``current_user_id()`` directly,
        only by referencing another function that does."""
        src = (
            "def current_user_id():\n"
            "    return 'stub'\n"
            "\n"
            "def _read_a():\n"
            "    current_user_id()\n"
            "    return {}\n"
            "\n"
            "def _section(read):\n"
            "    return read()\n"
            "\n"
            "def composite():\n"
            "    _section(_read_a)\n"
            "    return {}\n"
            "\n"
            "def register(app):\n"
            "    app.tool(name='composite')(composite)\n"
        )
        assert _handlers_missing_identity_check([src]) == []

    def test_handler_not_locally_defined_is_flagged_not_silently_passed(self) -> None:
        """A registered name the checker cannot see the body of (e.g.
        imported from elsewhere) must be a violation, never a silent pass."""
        src = "def register(app):\n    app.tool(name='mystery')(some_imported_handler)\n"
        assert _handlers_missing_identity_check([src]) == ["some_imported_handler"]

    def test_non_registration_calls_named_resource_or_tool_are_not_mistaken(self) -> None:
        """A call shaped like ``x.resource(...)(y)`` where ``x`` is NOT the
        MCP app (e.g. some unrelated object happening to have a ``.tool()``
        method) is still structurally identical and WILL be picked up by this
        detector — documenting that as a known, accepted over-inclusion (the
        safe direction: a false positive here is a loud extra check to
        satisfy, never a missed handler) rather than a precision claim this
        test doesn't make."""
        src = (
            "def current_user_id():\n"
            "    return 'stub'\n"
            "\n"
            "def handler():\n"
            "    current_user_id()\n"
            "    return {}\n"
            "\n"
            "def register(unrelated_thing):\n"
            "    unrelated_thing.tool(name='x')(handler)\n"
        )
        # Over-inclusive by design: still finds and correctly clears it.
        assert _handlers_missing_identity_check([src]) == []
