"""#1595 Phase 3 — the `read_canonical` flip group (Arch's ruling 2026-10-03,
rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-
wave2-and-writes-2026-10-03.md, section 3: "Two 'CANONICAL writes' are
reads").

READ rail adapters for two CANONICAL-disposition ops that mutate nothing by
verb: `explain_suggestion` (PROVENANCE, verb EXPLAIN) and
`get_contextual_guidance` (GUIDANCE, verb GET). Each entry wraps the
EXISTING canonical handler (`CanonicalHandlers._handle_provenance_query` /
`_handle_guidance_query`) directly — the `get_current_time` precedent, not
the `read_floor` factory shape, because neither wrapped handler branches on
`intent.category` (verified by reading both before grouping). Disposition
stays CANONICAL; membership is explicit; the flip is Phase-2-gated like any
wave; NOT flipped by this build.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from services.intent_service import workflow_entries as we
from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition
from services.intent_service.workflow_dispatcher import FLIP_GROUPS, get_action_workflows
from services.shared_types import EffectClass

MEMBERS = {
    "explain_suggestion",
    "get_contextual_guidance",
}


def test_members_register_as_read_entries_in_read_canonical():
    we.register_default_workflows()
    rail = get_action_workflows()
    assert "read_canonical" in FLIP_GROUPS
    for op in MEMBERS:
        entry = rail[op]
        assert entry.effect == EffectClass.READ
        assert entry.flip_group == "read_canonical"
        assert entry.action_triggered is True
    # Explicit membership: nothing else carries the group.
    assert {op for op, e in rail.items() if e.flip_group == "read_canonical"} == MEMBERS


def test_disposition_stays_canonical_and_the_table_is_registry_checked():
    for op, (category, _handler_attr) in we._READ_CANONICAL_MEMBERS.items():
        assert ACTION_REGISTRY[(category, op)] is ActionDisposition.CANONICAL
    # A non-canonical member fails loudly at registration, never at a user's turn.
    saved = dict(we._READ_CANONICAL_MEMBERS)
    try:
        we._READ_CANONICAL_MEMBERS["list_todos_query"] = ("QUERY", "_handle_guidance_query")
        with pytest.raises(ValueError, match="not a CANONICAL-disposition"):
            we._read_canonical_entries()
    finally:
        we._READ_CANONICAL_MEMBERS.clear()
        we._READ_CANONICAL_MEMBERS.update(saved)


@pytest.mark.asyncio
async def test_entry_point_calls_the_existing_provenance_handler_directly():
    calls = {}

    async def _provenance(intent, session_id, user_id=None):
        calls["intent"] = intent
        calls["session_id"] = session_id
        calls["user_id"] = user_id
        return {"message": "provenance answer", "intent": {"action": "explain_suggestion"}}

    canonical_handlers = SimpleNamespace(_handle_provenance_query=_provenance)
    svc = SimpleNamespace(canonical_handlers=canonical_handlers)
    intent = SimpleNamespace(action="explain_suggestion", context={})
    run = we._make_read_canonical_entry_point("explain_suggestion", "_handle_provenance_query")
    out = await run("s1", "u1", {"intent": intent, "intent_service": svc})
    assert out.message == "provenance answer"
    assert calls["intent"] is intent
    assert calls["session_id"] == "s1"
    assert calls["user_id"] == "u1"


@pytest.mark.asyncio
async def test_entry_point_calls_the_existing_guidance_handler_directly():
    calls = {}

    async def _guidance(intent, session_id, user_id=None):
        calls["intent"] = intent
        return {"message": "guidance answer", "intent": {"action": "get_contextual_guidance"}}

    canonical_handlers = SimpleNamespace(_handle_guidance_query=_guidance)
    svc = SimpleNamespace(canonical_handlers=canonical_handlers)
    intent = SimpleNamespace(action="get_contextual_guidance", context={})
    run = we._make_read_canonical_entry_point("get_contextual_guidance", "_handle_guidance_query")
    out = await run("s1", "u1", {"intent": intent, "intent_service": svc})
    assert out.message == "guidance answer"
    assert calls["intent"] is intent


@pytest.mark.asyncio
async def test_entry_point_without_context_returns_none_not_a_crash():
    run = we._make_read_canonical_entry_point("explain_suggestion", "_handle_provenance_query")
    assert await run("s1", "u1", {}) is None


def test_live_match_resolves_through_the_group():
    from services.intent_service.inversion_live import resolve_live_match

    we.register_default_workflows()
    entry = get_action_workflows()["explain_suggestion"]
    assert (
        resolve_live_match(
            operation="explain_suggestion",
            canonical="explain_suggestion",
            flip_group=entry.flip_group,
            category="PROVENANCE",
            cats=frozenset({"READ_CANONICAL"}),
        )
        is not None
    )
    assert (
        resolve_live_match(
            operation="explain_suggestion",
            canonical="explain_suggestion",
            flip_group=entry.flip_group,
            category="PROVENANCE",
            cats=frozenset({"READ_FLOOR"}),
        )
        is None
    )


def test_not_live_under_the_current_flag():
    """2026-10-04: read_canonical is NOT in CURRENT_LIVE_CATEGORIES — the PM
    flip token for this wave hasn't been granted yet (Phase-2 gate first,
    per Arch's ruling)."""
    import importlib
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[4]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    gate = importlib.import_module("scripts.inversion_phase3_deletion_gate")
    assert "READ_CANONICAL" not in gate.CURRENT_LIVE_CATEGORIES


def test_entries_carry_the_registry_description_for_the_router():
    """derive_routing_grammar prefers a rail entry's description once an op has
    one — so the adapter must carry ACTION_DESCRIPTIONS' text, or the router
    sees a bare name (same lesson read_floor's TRUST rows taught 2026-10-02)."""
    from services.intent_service.action_registry import ACTION_DESCRIPTIONS
    from services.intent_service.inversion_router import derive_routing_grammar

    we.register_default_workflows()
    by_name = {o.name: o.description for o in derive_routing_grammar().operations}
    for op, (category, _handler_attr) in we._READ_CANONICAL_MEMBERS.items():
        registry_text = ACTION_DESCRIPTIONS[(category, op)]
        assert registry_text[:40] in by_name[op], (op, by_name[op][:80])
