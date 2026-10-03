"""#1595 Phase 3 — the `read_floor` flip group (Arch's ruling 2026-10-02).

FLOOR-disposition ops whose pattern lists the deletion gate found load-bearing
(the LLM classifier never emits DISCOVERY/TRUST/MEMORY) get a rail ADAPTER:
one factory, an entry per member, each calling the existing
`_handle_floor_with_context` with the Intent re-keyed to the op's own registry
category. Disposition stays FLOOR; membership is explicit; the flip is
Phase-2-gated like any wave.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from services.intent_service import workflow_entries as we
from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition
from services.intent_service.workflow_dispatcher import FLIP_GROUPS, get_action_workflows
from services.shared_types import EffectClass, IntentCategory

MEMBERS = {"get_capabilities", "explain_trust", "get_memory", "pull_insights", "analyze_blockers"}


def test_members_register_as_read_entries_in_read_floor():
    we.register_default_workflows()
    rail = get_action_workflows()
    assert "read_floor" in FLIP_GROUPS
    for op in MEMBERS:
        entry = rail[op]
        assert entry.effect == EffectClass.READ
        assert entry.flip_group == "read_floor"
        assert entry.action_triggered is True
    # Explicit membership: nothing else carries the group.
    assert {op for op, e in rail.items() if e.flip_group == "read_floor"} == MEMBERS


def test_disposition_stays_floor_and_the_table_is_registry_checked():
    for op, category in we._READ_FLOOR_MEMBERS.items():
        assert ACTION_REGISTRY[(category, op)] is ActionDisposition.FLOOR
    # A non-floor member fails loudly at registration, never at a user's turn.
    saved = dict(we._READ_FLOOR_MEMBERS)
    try:
        we._READ_FLOOR_MEMBERS["list_todos_query"] = "QUERY"
        with pytest.raises(ValueError, match="not a FLOOR-disposition"):
            we._read_floor_entries()
    finally:
        we._READ_FLOOR_MEMBERS.clear()
        we._READ_FLOOR_MEMBERS.update(saved)


@pytest.mark.asyncio
async def test_entry_point_calls_the_existing_floor_under_the_ops_own_category():
    calls = {}

    async def _floor(intent, session_id, user_id=None, formality_baseline=None, trust_stage=None):
        calls["intent"] = intent
        calls["formality"] = formality_baseline
        calls["trust"] = trust_stage
        return SimpleNamespace(success=True, message="floor answer")

    async def _fmt(user_id):
        return 0.42

    async def _trust(user_id):
        return "BUILDING"

    svc = SimpleNamespace(
        _handle_floor_with_context=_floor,
        _resolve_formality_baseline=_fmt,
        _resolve_trust_stage=_trust,
    )
    # The rail builds a QUERY Intent for a key with no registry category; the
    # adapter re-keys it to the registry's (DISCOVERY) before the floor runs.
    intent = SimpleNamespace(category=IntentCategory.QUERY, action="get_capabilities", context={})
    run = we._make_read_floor_entry_point("get_capabilities", "DISCOVERY")
    out = await run("s1", "u1", {"intent": intent, "intent_service": svc})
    assert out.message == "floor answer"
    assert calls["intent"].category is IntentCategory.DISCOVERY
    assert calls["intent"].action == "get_capabilities"
    assert calls["formality"] == 0.42 and calls["trust"] == "BUILDING"


@pytest.mark.asyncio
async def test_entry_point_without_context_returns_none_not_a_crash():
    run = we._make_read_floor_entry_point("explain_trust", "TRUST")
    assert await run("s1", "u1", {}) is None


def test_live_match_resolves_through_the_group():
    from services.intent_service.inversion_live import resolve_live_match

    we.register_default_workflows()
    entry = get_action_workflows()["get_capabilities"]
    assert (
        resolve_live_match(
            operation="get_capabilities",
            canonical="get_capabilities",
            flip_group=entry.flip_group,
            category="DISCOVERY",
            cats=frozenset({"READ_FLOOR"}),
        )
        is not None
    )
    assert (
        resolve_live_match(
            operation="get_capabilities",
            canonical="get_capabilities",
            flip_group=entry.flip_group,
            category="DISCOVERY",
            cats=frozenset({"READ_STATUS"}),
        )
        is None
    )


def test_entries_carry_the_registry_description_for_the_router():
    """derive_routing_grammar prefers a rail entry's description once an op has
    one — so the adapter must carry ACTION_DESCRIPTIONS' text, or the router
    sees a bare name (2026-10-02: every TRUST row declined until this)."""
    from services.intent_service.action_registry import ACTION_DESCRIPTIONS
    from services.intent_service.inversion_router import derive_routing_grammar

    we.register_default_workflows()
    by_name = {o.name: o.description for o in derive_routing_grammar().operations}
    for op, category in we._READ_FLOOR_MEMBERS.items():
        registry_text = ACTION_DESCRIPTIONS[(category, op)]
        assert registry_text[:40] in by_name[op], (op, by_name[op][:80])
