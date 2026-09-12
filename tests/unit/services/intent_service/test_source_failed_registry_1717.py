"""1717 registry derivation — the source-failed flag list has ONE source of truth.

CXO's structural review (2026-09-09, voice-watch memo) found the real gap in
the landed #1717 wrinkle-1 work: ``_format_domain_context`` enumerated the
source-failed flags twice (five hand-written render sites + a hand-maintained
tuple gating the scope directive), and the composition tests keyed off a
third hand copy. A sixth ``*_source_failed`` flag added tomorrow would render
its FAILED line, silently escape the scope-directive gate, and stay green
under test — a turn where ONLY the sixth failed would get no scope directive,
the exact report-failures-that-didn't-happen leak wrinkle 1 exists to stop.

The 2026-09-12 composition fix (#1717, epic 5 / GatherOutcome opener)
completed the single-sourcing the registry round started: the five
hand-placed render sites are GONE. ``SOURCE_FAILED_FLAGS`` (now a tuple of
``SourceFailedDirective`` named tuples: flag, check_name, directive) is the
single source, and ``_format_domain_context`` has exactly ONE composition
site that derives the armed subset from it — rendering the registered
per-source directive at N == 1, the aggregate clause at N >= 2, and the
scope directive whenever N >= 1.

What this file now enforces structurally (the drift form inverted): before
the fix, the risk was a site WITHOUT a registry entry; after it, the risk is
a hand site REAPPEARING beside the registry — a seventh-flag author patching
a new ``if domain_context.get("x_source_failed")`` block back in instead of
registering. That is a fork of the single source and fails here.

To add a sixth source-failed directive: add ONE ``SourceFailedDirective``
entry to the registry. Nothing else — the composition site, the scope gate,
and the composition tests all derive from it.

Layer honesty (m-43): this file measures SOURCE STRUCTURE (what the renderer
derives from, and that no literal flag reads remain) — not rendered output.
The behavioral half lives in test_source_failed_composition_1717.py, whose
pins assert registry-derived directives and check names appear in real
renderer output; the two files together make a sixth flag unaddable without
the registry knowing.
"""

import ast
import inspect
import textwrap

from services.intent_service.conversational_floor import (
    SOURCE_FAILED_FLAGS,
    ConversationalFloor,
)

REGISTRY_NAME = "SOURCE_FAILED_FLAGS"


def _is_source_failed_key(key: object) -> bool:
    return isinstance(key, str) and (key == "source_failed" or key.endswith("_source_failed"))


def _renderer_tree() -> ast.Module:
    src = inspect.getsource(ConversationalFloor._format_domain_context)
    return ast.parse(textwrap.dedent(src))


def _literal_flag_reads(tree: ast.Module) -> list:
    """Every ``domain_context.get("<literal *source_failed key>")`` in source
    order. The composition site reads flags via attribute access on registry
    entries (``domain_context.get(entry.flag)``), so it is (correctly)
    invisible here — this collects only hand-written per-flag sites, which
    must no longer exist."""
    reads = []
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Call)
            and isinstance(node.func, ast.Attribute)
            and node.func.attr == "get"
            and isinstance(node.func.value, ast.Name)
            and node.func.value.id == "domain_context"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and _is_source_failed_key(node.args[0].value)
        ):
            reads.append((node.lineno, node.args[0].value))
    reads.sort()
    return [key for _, key in reads]


class TestRegistryDerivation:
    def test_no_hand_render_sites_remain(self):
        # (a) Single-source composition: the renderer must not read any
        # source-failed flag by literal key. A literal read is a forked
        # render site outside the registry — the pre-2026-09-12 additive
        # shape reappearing one flag at a time.
        site_flags = _literal_flag_reads(_renderer_tree())
        assert site_flags == [], (
            "hand-written source-failed render site(s) found in "
            f"_format_domain_context: {site_flags}. The #1717 composition fix "
            f"derives ALL source-failed handling from {REGISTRY_NAME} — "
            "register the flag there instead of adding a per-flag if-block."
        )

    def test_exactly_one_composition_site_iterates_registry(self):
        # (b) The composition site derives the armed subset from the registry
        # by name, exactly once — one comprehension/generator iterating
        # SOURCE_FAILED_FLAGS. Zero means the directives went dark; two means
        # a second derivation is drifting into existence.
        tree = _renderer_tree()
        registry_iterations = [
            node
            for node in ast.walk(tree)
            if isinstance(node, (ast.ListComp, ast.GeneratorExp, ast.SetComp))
            and isinstance(node.generators[0].iter, ast.Name)
            and node.generators[0].iter.id == REGISTRY_NAME
        ]
        assert len(registry_iterations) == 1, (
            f"expected exactly one comprehension iterating {REGISTRY_NAME} in "
            f"_format_domain_context, found {len(registry_iterations)}"
        )

    def test_no_hand_maintained_flag_tuple_remains(self):
        # The pre-fix drift form: a literal tuple/list of two-or-more
        # *_source_failed strings inside the renderer. Its reappearance is a
        # second list by definition — fail it regardless of contents.
        tree = _renderer_tree()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Tuple, ast.List)):
                literal_flags = [
                    el.value
                    for el in node.elts
                    if isinstance(el, ast.Constant) and _is_source_failed_key(el.value)
                ]
                assert len(literal_flags) < 2, (
                    "hand-maintained source-failed flag sequence found in "
                    f"_format_domain_context (line {node.lineno}): {literal_flags}. "
                    f"Derive from {REGISTRY_NAME} instead."
                )

    def test_registry_entries_pin_the_conventions(self):
        # CXO's honest-limit note: derivation keys off convention, so pin it.
        # Flags: well-formed and distinct. Directives: rendered context lines
        # carrying the "check FAILED:" marker (the N==1 shape the composition
        # tests count, and what makes the scope directive's "listed as FAILED
        # above" literally true). Check names: distinct, aggregate-safe (they
        # are comma-joined into one clause — a comma or FAILED marker inside
        # a name would garble the aggregate or double-count the denominator).
        flags = [entry.flag for entry in SOURCE_FAILED_FLAGS]
        assert len(flags) == len(set(flags)), f"duplicate flags: {flags}"
        for flag in flags:
            assert _is_source_failed_key(flag), f"unconventional flag key: {flag!r}"

        directives = [entry.directive for entry in SOURCE_FAILED_FLAGS]
        assert len(directives) == len(set(directives)), "duplicate directives"
        for directive in directives:
            assert directive.startswith("- "), f"not a rendered context line: {directive!r}"
            assert "check FAILED:" in directive, (
                f"{directive!r} lacks the 'check FAILED:' marker — the "
                "composition tests' count-based denominator and the scope "
                "directive's 'listed as FAILED above' both depend on that "
                "convention."
            )

        names = [entry.check_name for entry in SOURCE_FAILED_FLAGS]
        assert len(names) == len(set(names)), f"duplicate check names: {names}"
        for name in names:
            assert name and "\n" not in name, f"malformed check name: {name!r}"
            assert "," not in name, f"comma would garble the aggregate clause: {name!r}"
            assert "FAILED" not in name, f"marker collision in check name: {name!r}"
