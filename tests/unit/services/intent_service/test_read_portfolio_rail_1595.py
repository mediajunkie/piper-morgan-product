"""#1595 Phase 3 — the `read_portfolio` flip group (Arch's ruling 2026-10-03,
rule-arch-to-lead-cc-cxo-exec-phase3-rail-shapes-one-entry-per-effect-class-
wave2-and-writes-2026-10-03.md, section 2: "manage_repos: split into three
ops").

READ rail adapter for the LIST half of `manage_repos` — `list_repos`
(PORTFOLIO, CANONICAL, verb LIST). Wraps the EXISTING canonical handler
(`CanonicalHandlers._handle_list_repos`, itself hoisted out of
`_handle_repo_management`'s LIST branch for this build) directly — the
`get_current_time` precedent, same shape as `read_canonical`'s adapters.
Disposition FLIPPED CANONICAL -> WORKFLOW (Arch's 2026-10-04 ruling,
generalizing #1926: CanonicalHandlers.can_handle now declines any action
with a rail entry, not just needs_confirm ones — "the rail owns every rail
key" — so PORTFOLIO is no longer a whole category can_handle claims
unconditionally; verified against `test_registry_disposition_matches_live_
runtime`'s oracle, test_action_registry.py); membership is explicit; the
flip is Phase-2-gated like any wave; NOT flipped by this build. link/unlink
(WRITE/DESTRUCTIVE) are separate tasks and are not members of this group.

Widened 2026-10-04 (Arch's ruling, rule-arch-to-lead-cc-cxo-ppm-exec-list-
projects-reuse-live-entry-edit-literals-stay-my-miss-1933-endorsed-
2026-10-04.md §1): `search_projects` — the READ fourth of
`manage_portfolio`'s OWN split (a different CANONICAL action, same
PORTFOLIO category) — JOINS this group rather than opening a new one
("add search_projects to read_portfolio, with no re-home"). `MEMBERS`
below is re-measured, not assumed, same discipline as its original
single-member assertion.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from services.intent_service import workflow_entries as we
from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition
from services.intent_service.workflow_dispatcher import FLIP_GROUPS, get_action_workflows
from services.shared_types import EffectClass

MEMBERS = {"list_repos", "search_projects"}


def test_member_registers_as_a_read_entry_in_read_portfolio():
    we.register_default_workflows()
    rail = get_action_workflows()
    assert "read_portfolio" in FLIP_GROUPS
    entry = rail["list_repos"]
    assert entry.effect == EffectClass.READ
    assert entry.flip_group == "read_portfolio"
    assert entry.action_triggered is True
    # Explicit membership: ONLY these two carry the group (link/unlink are
    # NOT built here; manage_portfolio's active-list READ, `list_projects`,
    # deliberately stays on its existing QUERY-category rail key — see
    # the 2026-10-04 widening note in this module's docstring).
    assert {op for op, e in rail.items() if e.flip_group == "read_portfolio"} == MEMBERS


def test_disposition_flips_to_workflow():
    """Arch's 2026-10-04 ruling (generalizing #1926): CanonicalHandlers.
    can_handle() now declines any action with a rail entry, so list_repos's
    registry disposition must be WORKFLOW — CANONICAL would fail
    test_registry_disposition_matches_live_runtime's oracle (it resolves
    can_handle() before ever consulting the rail, and can_handle() now
    returns False for this action)."""
    assert ACTION_REGISTRY[("PORTFOLIO", "list_repos")] is ActionDisposition.WORKFLOW


@pytest.mark.asyncio
async def test_entry_point_calls_the_existing_list_repos_handler_directly():
    calls = {}

    async def _list_repos(intent, session_id, user_id=None):
        calls["intent"] = intent
        calls["session_id"] = session_id
        calls["user_id"] = user_id
        return {
            "message": "repo list answer",
            "intent": {"action": "list_repos"},
            "requires_clarification": False,
        }

    canonical_handlers = SimpleNamespace(_handle_list_repos=_list_repos)
    svc = SimpleNamespace(canonical_handlers=canonical_handlers)
    intent = SimpleNamespace(action="list_repos", context={})
    out = await we.run_list_repos_workflow("s1", "u1", {"intent": intent, "intent_service": svc})
    assert out.message == "repo list answer"
    assert calls["intent"] is intent
    assert calls["session_id"] == "s1"
    assert calls["user_id"] == "u1"


@pytest.mark.asyncio
async def test_entry_point_without_context_returns_none_not_a_crash():
    assert await we.run_list_repos_workflow("s1", "u1", {}) is None


def test_live_match_resolves_through_the_group():
    from services.intent_service.inversion_live import resolve_live_match

    we.register_default_workflows()
    entry = get_action_workflows()["list_repos"]
    assert (
        resolve_live_match(
            operation="list_repos",
            canonical="list_repos",
            flip_group=entry.flip_group,
            category="PORTFOLIO",
            cats=frozenset({"READ_PORTFOLIO"}),
        )
        is not None
    )
    assert (
        resolve_live_match(
            operation="list_repos",
            canonical="list_repos",
            flip_group=entry.flip_group,
            category="PORTFOLIO",
            cats=frozenset({"READ_FLOOR"}),
        )
        is None
    )


def test_not_live_under_the_current_flag():
    """2026-10-04: read_portfolio is NOT in CURRENT_LIVE_CATEGORIES — the PM
    flip token for this wave hasn't been granted yet (Phase-2 gate first,
    per Arch's ruling)."""
    import importlib
    import sys
    from pathlib import Path

    root = Path(__file__).resolve().parents[4]
    if str(root) not in sys.path:
        sys.path.insert(0, str(root))
    gate = importlib.import_module("scripts.inversion_phase3_deletion_gate")
    assert "READ_PORTFOLIO" not in gate.CURRENT_LIVE_CATEGORIES


def test_entry_carries_the_registry_description_for_the_router():
    """derive_routing_grammar prefers a rail entry's description once an op
    has one — so the adapter must carry meaningful text, or the router sees
    a bare name (the read_floor TRUST-row lesson, 2026-10-02)."""
    from services.intent_service.inversion_router import derive_routing_grammar

    we.register_default_workflows()
    by_name = {o.name: o.description for o in derive_routing_grammar().operations}
    assert "list_repos" in by_name
    assert "repositories linked to a project" in by_name["list_repos"]


@pytest.mark.asyncio
async def test_legacy_canonical_list_branch_delegates_to_the_same_handler(monkeypatch):
    """_handle_repo_management's LIST case must call _handle_list_repos —
    the hoist's whole point (one source of the list response for both the
    legacy canonical dispatch and this rail op)."""
    from services.intent_service.canonical_handlers import CanonicalHandlers

    handler = CanonicalHandlers()
    calls = {}

    async def _fake_list_repos(intent, session_id, user_id=None):
        calls["called"] = True
        calls["intent"] = intent
        calls["session_id"] = session_id
        calls["user_id"] = user_id
        return {
            "message": "delegated",
            "intent": {"action": "list_repos"},
            "requires_clarification": False,
        }

    monkeypatch.setattr(handler, "_handle_list_repos", _fake_list_repos)

    intent = SimpleNamespace(
        action="manage_repos",
        context={"original_message": "show my repos"},
    )
    result = await handler._handle_repo_management(intent, "sess", user_id="u1")

    assert calls.get("called") is True
    assert result["message"] == "delegated"
    assert calls["session_id"] == "sess"
    assert calls["user_id"] == "u1"
