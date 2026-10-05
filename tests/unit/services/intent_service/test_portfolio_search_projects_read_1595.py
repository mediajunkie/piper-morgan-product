"""#1595 Phase 3 — search_projects, the READ fourth of manage_portfolio's
split (Arch's 2026-10-04 ruling §1, mailboxes/lead/read/rule-arch-to-lead-
cc-cxo-ppm-exec-list-projects-reuse-live-entry-edit-literals-stay-my-miss-
1933-endorsed-2026-10-04.md): "list_projects: reuse the LIVE QUERY entry
and add search_projects to read_portfolio, with no re-home."

New READ rail entry wrapping an EXISTING (hoisted) canonical handler
directly — the get_current_time/list_repos precedent. Disposition FLIPPED
CANONICAL -> WORKFLOW (Arch's 2026-10-04 ruling, generalizing #1926:
CanonicalHandlers.can_handle() now declines any action with a rail entry,
so PORTFOLIO is no longer a whole category it claims unconditionally);
flip_group read_portfolio, joining list_repos in that group (not a new
group); `list_projects` itself is NOT touched — regression guard mirrored
from test_portfolio_write_split_1595.py.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.intent_service import workflow_entries as we
from services.intent_service.action_registry import ACTION_REGISTRY, ActionDisposition, get_verb
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.onboarding.portfolio_service import PortfolioService
from services.shared_types import EffectClass

# ---------------------------------------------------------------------------
# 1. Registration shape — READ, read_portfolio flip_group, action_triggered
# ---------------------------------------------------------------------------


def test_registers_as_a_read_entry_in_read_portfolio():
    we.register_default_workflows()
    rail = get_action_workflows()
    entry = rail["search_projects"]
    assert entry.effect == EffectClass.READ
    assert entry.flip_group == "read_portfolio"
    assert entry.action_triggered is True


def test_joins_list_repos_in_the_same_group_not_a_new_one():
    we.register_default_workflows()
    rail = get_action_workflows()
    assert rail["list_repos"].flip_group == rail["search_projects"].flip_group == "read_portfolio"


def test_disposition_flips_to_workflow():
    """Arch's 2026-10-04 ruling (generalizing #1926): CanonicalHandlers.
    can_handle() now declines any action with a rail entry, so this op's
    registry disposition must be WORKFLOW — CANONICAL would fail
    test_registry_disposition_matches_live_runtime's oracle (tested
    directly, parametrized over ACTION_REGISTRY, in
    test_action_registry.py)."""
    assert ACTION_REGISTRY[("PORTFOLIO", "search_projects")] is ActionDisposition.WORKFLOW


def test_has_a_registered_verb():
    assert get_verb("search_projects") is not None


# ---------------------------------------------------------------------------
# 2. Entry point calls the existing handler directly, never reimplements
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_entry_point_calls_the_existing_handler_directly():
    calls = {}

    async def _search(intent, session_id, user_id=None):
        calls["intent"] = intent
        calls["session_id"] = session_id
        calls["user_id"] = user_id
        return {
            "message": "found some",
            "intent": {"action": "search_projects"},
            "requires_clarification": False,
        }

    canonical_handlers = SimpleNamespace(_handle_search_projects=_search)
    svc = SimpleNamespace(canonical_handlers=canonical_handlers)
    intent = SimpleNamespace(action="search_projects", context={})
    out = await we.run_search_projects_workflow(
        "s1", "u1", {"intent": intent, "intent_service": svc}
    )
    assert out.message == "found some"
    assert calls["intent"] is intent
    assert calls["session_id"] == "s1"
    assert calls["user_id"] == "u1"


@pytest.mark.asyncio
async def test_entry_point_without_context_returns_none_not_a_crash():
    assert await we.run_search_projects_workflow("s1", "u1", {}) is None


# ---------------------------------------------------------------------------
# 3. Legacy canonical dispatch delegates to the SAME hoisted method
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_legacy_search_branch_delegates_to_the_hoisted_method(monkeypatch):
    handler = CanonicalHandlers()
    calls = {}

    async def _fake_search(intent, session_id, user_id=None):
        calls["called"] = True
        return {"message": "delegated", "intent": {"action": "search_projects"}}

    monkeypatch.setattr(handler, "_handle_search_projects", _fake_search)

    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    intent = Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_portfolio",
        confidence=1.0,
        context={"original_message": "search projects for Foo"},
    )
    result = await handler._handle_portfolio_query(intent, "sess", user_id="u1")
    assert calls.get("called") is True
    assert result["message"] == "delegated"


# ---------------------------------------------------------------------------
# 4. The hoisted method's own behaviour — read-only, correct copy
# ---------------------------------------------------------------------------


class _FakeScope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


def _search_intent(message: str):
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    return Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_portfolio",
        confidence=1.0,
        context={"original_message": message},
    )


async def _run_search(message: str, results):
    from services.database.session_factory import AsyncSessionFactory

    handler = CanonicalHandlers()

    async def _search(_self, **kwargs):
        return results

    with (
        patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())),
        patch.object(PortfolioService, "search_projects", _search),
    ):
        return await handler._handle_search_projects(
            _search_intent(message), session_id="s1", user_id="u1"
        )


def _project(name):
    p = SimpleNamespace()
    p.id = "proj-" + name
    p.name = name
    return p


class TestSearchProjectsFoundResults:
    @pytest.mark.asyncio
    async def test_renders_all_results_and_correct_action(self):
        results = [_project("Alpha"), _project("Atlas")]
        out = await _run_search("search projects for a", results)
        assert "Found 2 projects matching" in out["message"]
        assert "Alpha" in out["message"]
        assert "Atlas" in out["message"]
        assert out["intent"]["action"] == "search_projects"
        assert out["requires_clarification"] is False


class TestSearchProjectsNoResultsIsImperativeNotInterrogative:
    """The #1766 fix applied again: the old copy ended '...all your
    projects?' (interrogative); re-housing it unchanged into a NEW holder
    would have registered a new unarmed-ask site, so it's rewritten
    non-interrogative here, same shape as archive/restore's own not-found
    branches."""

    @pytest.mark.asyncio
    async def test_no_results_copy_is_imperative(self):
        out = await _run_search("search projects for nothing", [])
        assert not out["message"].rstrip().endswith("?")
        assert "say 'list my projects'" in out["message"].lower()
        assert out["requires_clarification"] is True

    @pytest.mark.asyncio
    async def test_no_results_offer_hint_is_also_imperative(self):
        out = await _run_search("search projects for nothing", [])
        assert not out["offer_hint"]["offer_text"].rstrip().endswith("?")


class TestSearchProjectsNoUser:
    @pytest.mark.asyncio
    async def test_no_user_id_short_circuits_before_db(self):
        handler = CanonicalHandlers()
        out = await handler._handle_search_projects(
            _search_intent("search projects for x"), session_id="s1", user_id=None
        )
        assert out["intent"]["action"] == "portfolio_no_user"
