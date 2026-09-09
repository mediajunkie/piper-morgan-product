"""1717 registry derivation — the source-failed flag list has ONE source of truth.

CXO's structural review (2026-09-09, voice-watch memo) found the real gap in
the landed #1717 wrinkle-1 work: ``_format_domain_context`` enumerated the
source-failed flags twice (five hand-written render sites + a hand-maintained
tuple gating the scope directive), and the composition tests keyed off a
third hand copy. A sixth ``*_source_failed`` flag added tomorrow would render
its FAILED line, silently escape the scope-directive gate, and stay green
under test — a turn where ONLY the sixth failed would get no scope directive,
the exact report-failures-that-didn't-happen leak wrinkle 1 exists to stop.

The fix: ``SOURCE_FAILED_FLAGS`` in ``conversational_floor.py`` is the single
registry; the scope-directive gate iterates it, and the 1717 composition
tests derive their DIRECTIVES denominator from it. The five render sites stay
hand-placed (each FAILED line belongs inside its topical section, with the
scope directive after the last of them), so THIS file enforces the remaining
association structurally — the enforcement-test idiom (cf. the 1685
alias-family mapper tests): parse the renderer's source AST and fail if the
flags the render sites actually check ever diverge from the registry.

Layer honesty (m-43): this file measures SOURCE STRUCTURE (which flag keys
the renderer reads, and what the gate iterates) — not rendered output. The
behavioral half lives in test_source_failed_composition_1717.py, whose pins
assert the registry-derived prefixes appear in real renderer output; the two
files together make a sixth flag unaddable without the registry knowing.
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
    order. The scope-directive gate reads ``domain_context.get(flag)`` with a
    NAME argument, so it is (correctly) invisible here — this collects only
    the hand-written render sites."""
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
    def test_registry_keys_match_render_sites_exactly_and_in_order(self):
        # (a) The registry's keys ARE the flags the render sites actually
        # check — same set, same source order, no duplicates. A sixth site
        # without a registry entry (or a registry entry without a site, or a
        # reordering that would misplace the scope directive) fails here.
        site_flags = _literal_flag_reads(_renderer_tree())
        registry_flags = [flag for flag, _ in SOURCE_FAILED_FLAGS]
        assert len(site_flags) == len(
            set(site_flags)
        ), f"duplicate source-failed reads in _format_domain_context: {site_flags}"
        assert site_flags == registry_flags, (
            "SOURCE_FAILED_FLAGS has drifted from the render sites.\n"
            f"  sites check (in order):  {site_flags}\n"
            f"  registry says (in order): {registry_flags}\n"
            "Add/remove/reorder the registry entry to match — the registry is "
            "the single source of truth the scope-directive gate and the 1717 "
            "composition tests derive from."
        )

    def test_scope_directive_gate_derives_from_registry(self):
        # (b) The wrinkle-1 gate is `any(... for ... in SOURCE_FAILED_FLAGS)`
        # — exactly one such gate, iterating the registry by name.
        tree = _renderer_tree()
        gates = [
            node
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "any"
            and node.args
            and isinstance(node.args[0], ast.GeneratorExp)
            and isinstance(node.args[0].generators[0].iter, ast.Name)
            and node.args[0].generators[0].iter.id == REGISTRY_NAME
        ]
        assert len(gates) == 1, (
            f"expected exactly one any(...) gate iterating {REGISTRY_NAME} in "
            f"_format_domain_context, found {len(gates)}"
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

    def test_registry_prefixes_pin_the_failed_line_convention(self):
        # CXO's honest-limit note: derivation keys off convention, so pin it.
        # Every registered directive's rendered-line prefix must carry the
        # "check FAILED:" marker the composition tests count as their
        # denominator, and prefixes must be distinct (a shared prefix would
        # let one rendered line satisfy two flags' pins).
        prefixes = [prefix for _, prefix in SOURCE_FAILED_FLAGS]
        assert len(prefixes) == len(set(prefixes)), f"duplicate prefixes: {prefixes}"
        for prefix in prefixes:
            assert prefix.startswith("- "), f"not a rendered context line: {prefix!r}"
            assert "check FAILED:" in prefix, (
                f"{prefix!r} lacks the 'check FAILED:' marker — the composition "
                "tests' count-based denominator and the scope directive's "
                "'listed as FAILED above' both depend on that convention."
            )
