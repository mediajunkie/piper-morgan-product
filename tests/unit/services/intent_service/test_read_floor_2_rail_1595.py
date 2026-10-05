"""#1595 Phase 3 wave 2 — the `read_floor_2` flip group (Arch's ruling 2026-10-03,
rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-
wave2-and-writes-2026-10-03.md).

A SECOND, separate group of FLOOR-disposition rail adapters — built apart
from `read_floor` (not a widening of it) because `read_floor` is already
LIVE on alpha; adding members to it would make them live on the next deploy
with no PM flag token. Same adapter shape as `read_floor`: one factory
(reused, not duplicated — `_make_read_floor_entry_point` is already
op/category-generic), an entry per member, each calling the existing
`_handle_floor_with_context` with the Intent re-keyed to the op's own
registry category. Disposition stays FLOOR; membership is explicit; the
flip is Phase-2-gated like any wave; NOT flipped by this build.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from services.intent_service import workflow_entries as we
from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition
from services.intent_service.workflow_dispatcher import FLIP_GROUPS, get_action_workflows
from services.shared_types import EffectClass, IntentCategory

MEMBERS = {
    "get_feature_info",
    "check_completion_status",
    "write_stakeholder_update",
    "get_identity",
}


def test_members_register_as_read_entries_in_read_floor_2():
    we.register_default_workflows()
    rail = get_action_workflows()
    assert "read_floor_2" in FLIP_GROUPS
    for op in MEMBERS:
        entry = rail[op]
        assert entry.effect == EffectClass.READ
        assert entry.flip_group == "read_floor_2"
        assert entry.action_triggered is True
    # Explicit membership: nothing else carries the group.
    assert {op for op, e in rail.items() if e.flip_group == "read_floor_2"} == MEMBERS


def test_read_floor_2_is_a_distinct_group_from_read_floor():
    """The whole point of building a second group: read_floor is already
    live, so its membership must be untouched by this wave."""
    we.register_default_workflows()
    rail = get_action_workflows()
    read_floor_members = {op for op, e in rail.items() if e.flip_group == "read_floor"}
    read_floor_2_members = {op for op, e in rail.items() if e.flip_group == "read_floor_2"}
    assert read_floor_members.isdisjoint(read_floor_2_members)
    assert read_floor_members == {
        "get_capabilities",
        "explain_trust",
        "get_memory",
        "pull_insights",
        "analyze_blockers",
    }


def test_disposition_stays_floor_and_the_table_is_registry_checked():
    for op, category in we._READ_FLOOR_2_MEMBERS.items():
        assert ACTION_REGISTRY[(category, op)] is ActionDisposition.FLOOR
    # A non-floor member fails loudly at registration, never at a user's turn.
    saved = dict(we._READ_FLOOR_2_MEMBERS)
    try:
        we._READ_FLOOR_2_MEMBERS["list_todos_query"] = "QUERY"
        with pytest.raises(ValueError, match="not a FLOOR-disposition"):
            we._read_floor_2_entries()
    finally:
        we._READ_FLOOR_2_MEMBERS.clear()
        we._READ_FLOOR_2_MEMBERS.update(saved)


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
    # adapter re-keys it to the registry's (IDENTITY) before the floor runs.
    intent = SimpleNamespace(category=IntentCategory.QUERY, action="get_identity", context={})
    run = we._make_read_floor_entry_point("get_identity", "IDENTITY")
    out = await run("s1", "u1", {"intent": intent, "intent_service": svc})
    assert out.message == "floor answer"
    assert calls["intent"].category is IntentCategory.IDENTITY
    assert calls["intent"].action == "get_identity"
    assert calls["formality"] == 0.42 and calls["trust"] == "BUILDING"


@pytest.mark.asyncio
async def test_entry_point_without_context_returns_none_not_a_crash():
    run = we._make_read_floor_entry_point("check_completion_status", "STATUS")
    assert await run("s1", "u1", {}) is None


def test_live_match_resolves_through_the_group():
    from services.intent_service.inversion_live import resolve_live_match

    we.register_default_workflows()
    entry = get_action_workflows()["get_feature_info"]
    assert (
        resolve_live_match(
            operation="get_feature_info",
            canonical="get_feature_info",
            flip_group=entry.flip_group,
            category="QUERY",
            cats=frozenset({"READ_FLOOR_2"}),
        )
        is not None
    )
    assert (
        resolve_live_match(
            operation="get_feature_info",
            canonical="get_feature_info",
            flip_group=entry.flip_group,
            category="QUERY",
            cats=frozenset({"READ_FLOOR"}),
        )
        is None
    )


def test_entries_carry_the_registry_description_for_the_router():
    """derive_routing_grammar prefers a rail entry's description once an op has
    one — so the adapter must carry ACTION_DESCRIPTIONS' text, or the router
    sees a bare name (same lesson read_floor's TRUST rows taught 2026-10-02)."""
    from services.intent_service.action_registry import ACTION_DESCRIPTIONS
    from services.intent_service.inversion_router import derive_routing_grammar

    we.register_default_workflows()
    by_name = {o.name: o.description for o in derive_routing_grammar().operations}
    for op, category in we._READ_FLOOR_2_MEMBERS.items():
        registry_text = ACTION_DESCRIPTIONS[(category, op)]
        assert registry_text[:40] in by_name[op], (op, by_name[op][:80])


class TestGateFloorCreditBehindUnflippedEntry:
    """2026-10-03 (Lead): building a read_floor_2 adapter must not withdraw the
    floor credit a deleted list's rows earned while the group is unflipped —
    production still reaches the op by category through the floor. Found when
    the build turned the TEMPORAL ledger's 'did I finish the report yesterday'
    (check_completion_status) row red."""

    def _helper(self):
        import importlib
        import sys
        from pathlib import Path

        root = Path(__file__).resolve().parents[4]
        if str(root) not in sys.path:
            sys.path.insert(0, str(root))
        gate = importlib.import_module("scripts.inversion_phase3_deletion_gate")
        p1 = importlib.import_module("scripts.inversion_phase1_shadow_score")
        return gate, p1._op_category_map()

    def test_unflipped_floor_member_keeps_floor_credit(self, monkeypatch):
        """read_floor_2 went LIVE on alpha 2026-10-05 (12 tokens), so the
        real set no longer has an unflipped floor group to point at — the
        unflipped branch is exercised against a set WITHOUT it, and the live
        set is pinned the other way below."""
        gate, cats = self._helper()
        monkeypatch.setattr(
            gate,
            "CURRENT_LIVE_CATEGORIES",
            frozenset(gate.CURRENT_LIVE_CATEGORIES - {"READ_FLOOR_2"}),
        )
        assert gate._floor_op_behind_unflipped_entry("check_completion_status", cats) is True

    def test_live_floor_2_member_is_served_by_name(self):
        gate, cats = self._helper()
        assert "READ_FLOOR_2" in gate.CURRENT_LIVE_CATEGORIES
        assert gate._floor_op_behind_unflipped_entry("check_completion_status", cats) is False

    def test_live_group_member_does_not(self):
        gate, cats = self._helper()
        assert "READ_FLOOR" in gate.CURRENT_LIVE_CATEGORIES
        assert gate._floor_op_behind_unflipped_entry("get_capabilities", cats) is False

    def test_non_floor_op_does_not(self):
        gate, cats = self._helper()
        assert gate._floor_op_behind_unflipped_entry("manage_repos", cats) is False
