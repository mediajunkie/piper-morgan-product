"""#1570 (c) — archived-projects LIST query gets a rail key (the sanctioned
#1560 pattern), effect=READ.

PM live 2026-08-10: "show me my archived projects" → the floor DENIED the
capability. Verified by direct execution: the pre-classifier claims that
phrasing as STATUS/get_project_status (conf 1.0) — the PORTFOLIO list
pattern rejects the "me" token, so the #1431 archived branch (which lives in
the PORTFOLIO handler) never runs. STATUS always floors, the floor's status
context has no archived data, and — decisively — archived-list had NO
rail/ActionMapper key, so the #1517 capability manifest could not protect it
from improvised denial.

The rail key fixes the structural halves that are fixable under the routing
moratorium (#1559 — no new pre-classifier regexes):
  1. `list_archived_projects` joins wired_chat_actions() → the manifest now
     covers it and the floor may no longer deny it.
  2. An LLM emission of list_archived_projects (or aliases) on phrasings the
     pre-classifier does NOT claim dispatches deterministically, category-
     independent.
The pre-classifier pattern half ("show ME my ..." claimed by STATUS) is
corpus material, reported on the issue — NOT patched here.

Layer honesty (m-43): registration/wiring tests plus a dispatch-layer test
with the portfolio data source stubbed. No live classifier, no DB.
"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.workflow_dispatcher import (
    dispatch_workflow,
    get_action_workflows,
    wired_chat_actions,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory

_ALIASES = [
    "list_archived_projects",
    "show_archived_projects",
    "archived_projects_query",
    "list_archived",
]


class TestArchivedProjectsRailRegistration:
    def test_all_aliases_dispatch_via_the_rail(self):
        register_default_workflows()
        keys = get_action_workflows().keys()
        for alias in _ALIASES:
            assert alias in keys, (
                f"{alias!r} must be rail-dispatchable — without a key the #1517 "
                f"manifest cannot protect archived-list from floor denial (#1570)"
            )

    def test_aliases_share_one_entry_point(self):
        register_default_workflows()
        wf = get_action_workflows()
        assert len({id(wf[a]) for a in _ALIASES}) == 1

    def test_entry_declares_read_effect(self):
        # list_archived_projects is an owner-scoped SELECT; no writes anywhere.
        register_default_workflows()
        entry = get_action_workflows()["list_archived_projects"]
        assert entry.effect == EffectClass.READ
        assert entry.action_triggered is True

    def test_manifest_lists_archived_capability_exactly_once(self):
        """The #1517 protection: wired_chat_actions() (registry ∪ ActionMapper)
        must now carry the archived-list capability, deduped."""
        wired = wired_chat_actions()
        assert wired.count("list_archived_projects") == 1


class TestArchivedProjectsDispatch:
    """The entry point performs the owner-scoped archived read (the same data
    path as the #1431 canonical branch) and returns an honest result."""

    def _project(self, name):
        p = MagicMock()
        p.name = name
        return p

    def _patch_portfolio(self, archived):
        service = MagicMock()
        service.list_archived_projects = AsyncMock(return_value=archived)

        @asynccontextmanager
        async def fake_scope():
            yield MagicMock()

        return (
            patch(
                "services.onboarding.portfolio_service.PortfolioService",
                return_value=service,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope",
                fake_scope,
            ),
            service,
        )

    @pytest.mark.asyncio
    async def test_dispatch_lists_archived_projects_owner_scoped(self):
        register_default_workflows()
        p_service, p_scope, service = self._patch_portfolio(
            [self._project("Old Initiative"), self._project("Sunset App")]
        )
        with p_service, p_scope:
            result = await dispatch_workflow(
                workflow_type="list_archived_projects",
                session_id="sess-1570",
                user_id="user-1570",
                context={
                    "intent": Intent(
                        category=IntentCategory.STATUS,  # category must not matter
                        action="list_archived_projects",
                        context={"original_message": "show me my archived projects"},
                    ),
                    "workflow_id": None,
                    "intent_service": MagicMock(),
                },
            )

        assert result is not None and result.success
        assert "Old Initiative" in result.message
        assert "Sunset App" in result.message
        assert "archived" in result.message.lower()
        service.list_archived_projects.assert_awaited_once_with(user_id="user-1570")

    @pytest.mark.asyncio
    async def test_dispatch_empty_archive_is_honest(self):
        register_default_workflows()
        p_service, p_scope, _ = self._patch_portfolio([])
        with p_service, p_scope:
            result = await dispatch_workflow(
                workflow_type="show_archived_projects",
                session_id="sess-1570",
                user_id="user-1570",
                context={},
            )
        assert result is not None and result.success
        assert "archived" in result.message.lower()
        # honest empty, never a denial of the capability
        assert "can't" not in result.message.lower()

    @pytest.mark.asyncio
    async def test_dispatch_without_user_id_asks_for_sign_in(self):
        register_default_workflows()
        result = await dispatch_workflow(
            workflow_type="list_archived_projects",
            session_id="sess-1570",
            user_id=None,
            context={},
        )
        assert result is not None and result.success
        assert "sign" in result.message.lower()
