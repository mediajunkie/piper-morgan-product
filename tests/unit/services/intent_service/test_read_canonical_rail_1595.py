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
FLIPPED CANONICAL -> WORKFLOW (Arch's 2026-10-04 ruling, generalizing
#1926: CanonicalHandlers.can_handle now declines any action with a rail
entry, not just needs_confirm ones, so neither op's category is a whole
category it claims unconditionally any more); membership is explicit; the
flip is Phase-2-gated like any wave; NOT flipped by this build (#1595) —
the disposition flip is the later, separate 2026-10-04 generalization.
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


def test_disposition_flips_to_workflow_and_the_table_is_registry_checked():
    """Arch's 2026-10-04 ruling (generalizing #1926): both members' live
    runtime now resolves WORKFLOW (CanonicalHandlers.can_handle declines
    any action with a rail entry), so the registry row must say WORKFLOW
    too — the _read_canonical_entries() validator was updated alongside
    this flip (it used to require CANONICAL; see its own docstring)."""
    for op, (category, _handler_attr) in we._READ_CANONICAL_MEMBERS.items():
        assert ACTION_REGISTRY[(category, op)] is ActionDisposition.WORKFLOW
    # A mismatched-disposition member still fails loudly at registration,
    # never at a user's turn — ("ANALYSIS", "analyze_blockers") is FLOOR,
    # not WORKFLOW, so it still trips the validator post-flip.
    saved = dict(we._READ_CANONICAL_MEMBERS)
    try:
        we._READ_CANONICAL_MEMBERS["analyze_blockers"] = ("ANALYSIS", "_handle_guidance_query")
        with pytest.raises(ValueError, match="not a WORKFLOW-disposition"):
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
    svc = SimpleNamespace(
        canonical_handlers=canonical_handlers,
        # 2026-10-04 Arch's adapter-parity ruling: _finalize_canonical_rail_
        # result now calls these two on intent_service — stub them so this
        # stays a thin "calls the handler directly" check, not a parity test
        # (that lives in test_rail_adapter_canonical_parity_1926.py).
        _is_generic_canonical_response=lambda *a, **k: False,
        _track_offer_hint=lambda *a, **k: None,
    )
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
    svc = SimpleNamespace(
        canonical_handlers=canonical_handlers,
        _is_generic_canonical_response=lambda *a, **k: False,
        _track_offer_hint=lambda *a, **k: None,
    )
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


def test_live_under_the_current_flag():
    """2026-10-04 this pinned NOT live (Phase-2 gate first, per Arch's
    ruling). PM granted the token and alpha v169 went live with it on
    2026-10-05 (12 tokens); the gate mirrors the flag, so the pin flips."""
    import importlib
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[4]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    gate = importlib.import_module("scripts.inversion_phase3_deletion_gate")
    assert "READ_CANONICAL" in gate.CURRENT_LIVE_CATEGORIES


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
