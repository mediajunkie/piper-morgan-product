"""#2195: the router catalog's order is an append-only ledger.

Arch's ruling, decisions.log 2026-10-29 19:39: ``derive_routing_grammar`` derives
WHICH ops exist from the registries; their ORDER comes from
``CATALOG_ORDER_LEDGER``. A ledger op renders at its slot whichever pass produced
it, a new op renders after every ledger op until it is appended, and a stale name
is skipped. The ledger unit's rendered request was byte-identical to main's
(616/616 corpus requests, ``scripts/router_batch.py render --corpus``, cmp equal).
"""

from __future__ import annotations

from dataclasses import dataclass

from services.intent_service.inversion_router import (
    _SYSTEM_PROMPT,
    CLARIFY_ROUTE,
    NONE_ROUTE,
    build_routing_prompt,
    derive_routing_grammar,
)
from services.intent_service.router_catalog_order import (
    CATALOG_ORDER_LEDGER,
    ledger_drift,
    order_operations,
)
from services.intent_service.workflow_dispatcher import (
    WORKFLOW_REGISTRY,
    WorkflowEntry,
    register_workflow,
)
from services.shared_types import EffectClass

PHRASE = "show milestones"


def _catalog_names(prompt: str) -> list[str]:
    lines = prompt.split("\n")
    start = next(i for i, line in enumerate(lines) if line.startswith("Operation catalog"))
    names = []
    for line in lines[start + 1 :]:
        if not line.startswith("- "):
            break
        names.append(line[2:].split(":", 1)[0])
    return names


def _rendered_request() -> tuple[str, str]:
    """The two prompt texts the live router sends (scripts/router_batch.py
    renders the same pair): the system prompt and the catalog user prompt."""
    return _SYSTEM_PROMPT, build_routing_prompt(PHRASE, derive_routing_grammar())


def _drift_message(missing: list[str], stale: list[str]) -> str:
    parts = []
    if missing:
        parts.append(f"ops missing from CATALOG_ORDER_LEDGER (append them at the END): {missing}")
    if stale:
        parts.append(
            f"stale CATALOG_ORDER_LEDGER names with no op (removal is a rule-7 unit): {stale}"
        )
    return "; ".join(parts)


@dataclass(frozen=True)
class _Op:
    name: str
    tag: str = ""


class TestOrderOperations:
    def test_ledger_ops_in_ledger_order_then_new_ops_in_derivation_order(self):
        ops = [_Op("new_b"), _Op("c"), _Op("a"), _Op("new_a"), _Op("b")]
        ordered = order_operations(ops, ledger=("a", "b", "c"))
        assert [o.name for o in ordered] == ["a", "b", "c", "new_b", "new_a"]

    def test_stale_ledger_name_is_skipped(self):
        ordered = order_operations([_Op("b"), _Op("a")], ledger=("a", "gone", "b"))
        assert [o.name for o in ordered] == ["a", "b"]

    def test_input_not_mutated_and_no_op_dropped(self):
        ops = [_Op("b"), _Op("a", "x"), _Op("a", "y")]
        snapshot = list(ops)
        ordered = order_operations(ops, ledger=("a", "b"))
        assert ops == snapshot
        assert ordered == [_Op("a", "x"), _Op("a", "y"), _Op("b")]

    def test_ledger_has_no_duplicates(self):
        assert len(CATALOG_ORDER_LEDGER) == len(set(CATALOG_ORDER_LEDGER))


class TestCatalogOrderLedger2195:
    def test_rendered_catalog_order_is_the_ledger_order(self):
        """(a) Byte identity with main's render, pinned structurally: every grammar
        op is a ledger name (completeness, below) and the rendered catalog lines
        follow the ledger exactly, so the order cannot drift from the 2026-10-29
        capture without a ledger edit."""
        grammar = derive_routing_grammar()
        names = _catalog_names(build_routing_prompt(PHRASE, grammar))
        assert names[-2:] == [NONE_ROUTE, CLARIFY_ROUTE]
        assert names[:-2] == list(grammar.names())
        assert names[:-2] == [n for n in CATALOG_ORDER_LEDGER if n in set(grammar.names())]

    def test_ledger_matches_derived_membership(self):
        """(b) One test flags both directions: a derived op missing from the
        ledger (append it) and a ledger name with no op (stale)."""
        missing, stale = ledger_drift(derive_routing_grammar().names())
        assert (missing, stale) == ([], []), _drift_message(missing, stale)

    def test_rail_entry_for_registry_only_op_keeps_its_slot(self, monkeypatch):
        """(c) get_project_status promoted through the real read_floor_2 adapter
        factory (monkeypatched membership, never committed) keeps its ledger slot:
        the rendered ORDER of catalog names is unchanged. Measured 2026-10-29: the
        whole request is byte-identical too, so it is pinned."""
        from services.intent_service import workflow_entries as we

        op = "get_project_status"
        grammar = derive_routing_grammar()
        assert {o.name: o.source for o in grammar.operations}[op] == "action_registry"
        before = _rendered_request()

        monkeypatch.setattr(we, "_READ_FLOOR_2_MEMBERS", {op: "STATUS"})
        entry = we._read_floor_2_entries()[op]
        try:
            register_workflow(op, entry)
            promoted = derive_routing_grammar()
            assert {o.name: o.source for o in promoted.operations}[op] == "rail"
            after = _rendered_request()
        finally:
            WORKFLOW_REGISTRY.pop(op, None)
        assert _catalog_names(after[1]) == _catalog_names(before[1])
        assert after == before

    def test_every_registry_only_op_promotes_without_moving_a_line(self):
        """(c), registry-wide: a rail entry carrying each registry-only op's own
        ACTION_DESCRIPTIONS text (plus an issue marker the rail strips) leaves the
        rendered request byte-identical. Stays meaningful after get_project_status
        gains its real entry (the test above then needs a new registry-only op)."""
        from services.intent_service.action_registry import ACTION_DESCRIPTIONS, ACTION_REGISTRY

        async def _noop(session_id, user_id=None, context=None):  # pragma: no cover
            return None

        category_by_action = {a: c for (c, a) in ACTION_REGISTRY}
        registry_only = [
            o.name for o in derive_routing_grammar().operations if o.source == "action_registry"
        ]
        assert registry_only, "no registry-only ops left; pin is vacuous"
        before = _rendered_request()
        differing = []
        for op in registry_only:
            text = ACTION_DESCRIPTIONS[(category_by_action[op], op)]
            entry = WorkflowEntry(
                entry_point=_noop,
                effect=EffectClass.READ,
                description=f"{text} (#2195 probe)",
                action_triggered=True,
            )
            try:
                register_workflow(op, entry)
                if _rendered_request() != before:
                    differing.append(op)
            finally:
                WORKFLOW_REGISTRY.pop(op, None)
        assert differing == []
        assert _rendered_request() == before

    def test_new_op_renders_after_every_ledger_op_and_fails_completeness(self):
        """(d) An op the ledger does not name renders after all ledger ops, and the
        completeness comparison (b) reports it as missing."""

        async def _noop(session_id, user_id=None, context=None):  # pragma: no cover
            return None

        op = "zz_probe_unledgered_op_2195"
        assert op not in WORKFLOW_REGISTRY
        entry = WorkflowEntry(
            entry_point=_noop,
            effect=EffectClass.READ,
            description="probe op for the ledger test",
            action_triggered=True,
        )
        try:
            register_workflow(op, entry)
            grammar = derive_routing_grammar()
            names = _catalog_names(build_routing_prompt(PHRASE, grammar))[:-2]
            missing, stale = ledger_drift(grammar.names())
        finally:
            WORKFLOW_REGISTRY.pop(op, None)
        assert names[-1] == op
        assert set(names[:-1]) <= set(CATALOG_ORDER_LEDGER)
        assert (missing, stale) == ([op], [])
        assert "append them at the END" in _drift_message(missing, stale)

    def test_stale_ledger_name_is_flagged(self):
        names = derive_routing_grammar().names()
        missing, stale = ledger_drift(names, ledger=CATALOG_ORDER_LEDGER + ("retired_op",))
        assert (missing, stale) == ([], ["retired_op"])
        assert "stale" in _drift_message(missing, stale)
