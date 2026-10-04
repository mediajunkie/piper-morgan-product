"""#1930 — step 1 of CXO's 2026-10-04 ruling: stop promising a delete
nothing executes.

The live `_handle_portfolio_query` delete branch used to return
"Are you sure you want to delete 'X'? This action cannot be undone." and
arm `awaiting_confirmation` — but nothing anywhere ever reads that context
back and calls `PortfolioService.delete_project(confirmed=True)` (verified
by the #1595 Phase 3 inventory,
dev/2026/10/04/manage-portfolio-effect-inventory-2026-10-04.md §2 row 4).
That's the product misreporting its own capability.

CXO's ruling (mailboxes/lead/read/rule-cxo-to-lead-cc-arch-ppm-1930-copy-
now-wire-later-1931-out-of-chat-ok-complete-no-shall-i-2026-10-04.md §2):
resolve the project first; not-found keeps today's copy; found (not
archived) gets the exact honest copy below, arming nothing; already
archived says so and does not re-offer archive.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.onboarding.portfolio_service import PortfolioService
from services.shared_types import IntentCategory


class _FakeScope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


def _delete_intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_portfolio",
        confidence=1.0,
        context={"original_message": message},
    )


def _project(name="Test", archived=False):
    p = SimpleNamespace()
    p.id = "proj-1930"
    p.name = name
    p.is_archived = archived
    return p


async def _run_delete(message: str, found_project):
    from services.database.session_factory import AsyncSessionFactory

    handler = CanonicalHandlers()

    async def _find(_self, **kwargs):
        return found_project

    with (
        patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())),
        patch.object(PortfolioService, "find_project_by_name", _find),
    ):
        return await handler._handle_portfolio_query(
            _delete_intent(message), session_id="s1", user_id="u1"
        )


class TestDeleteNeverArms:
    """The pin CXO asked for, verbatim: a delete turn never returns
    awaiting_confirmation and never contains 'cannot be undone' — for
    EVERY resolution outcome (found/active, found/archived, not found)."""

    @pytest.mark.asyncio
    async def test_found_active_project_never_arms(self):
        result = await _run_delete("delete my project Test", _project())
        assert "cannot be undone" not in result["message"]
        assert "awaiting_confirmation" not in result["intent"]["context"]
        assert result["requires_clarification"] is False
        assert result["intent"]["action"] != "delete_confirm"

    @pytest.mark.asyncio
    async def test_found_archived_project_never_arms(self):
        result = await _run_delete("delete my project Test", _project(archived=True))
        assert "cannot be undone" not in result["message"]
        assert "awaiting_confirmation" not in result["intent"]["context"]
        assert result["requires_clarification"] is False

    @pytest.mark.asyncio
    async def test_not_found_project_never_arms(self):
        result = await _run_delete("delete my project Nope", None)
        assert "cannot be undone" not in result["message"]
        assert "awaiting_confirmation" not in result["intent"].get("context", {})


class TestDeleteFoundActiveCopy:
    """CXO's exact copy for the found, not-archived case."""

    @pytest.mark.asyncio
    async def test_exact_copy_and_action_label(self):
        result = await _run_delete("delete my project Test", _project(name="Test"))
        assert result["message"] == (
            "I can't delete projects from chat yet. I can archive 'Test' "
            "instead: it leaves your active list and you can say 'restore "
            "Test' to bring it back. Say 'archive Test' if you'd like that."
        )
        assert result["intent"]["action"] == "delete_unavailable"
        assert result["intent"]["context"]["already_archived"] is False


class TestDeleteFoundArchivedCopy:
    """Already archived — says so, does not re-offer archive (CXO: don't
    offer archive again)."""

    @pytest.mark.asyncio
    async def test_says_already_archived_and_does_not_reoffer_archive(self):
        result = await _run_delete("delete my project Test", _project(name="Test", archived=True))
        assert "already archived" in result["message"].lower()
        # Must not re-offer archiving an already-archived project.
        assert "say 'archive" not in result["message"].lower()
        assert result["intent"]["action"] == "delete_unavailable"
        assert result["intent"]["context"]["already_archived"] is True


class TestDeleteNotFoundUnchanged:
    """Not found keeps today's copy, verbatim (CXO: 'Not found keeps
    today's copy')."""

    @pytest.mark.asyncio
    async def test_not_found_copy_and_action_label_unchanged(self):
        result = await _run_delete("delete my project Nope", None)
        assert result["message"] == (
            "I couldn't find a project called 'nope'. " "Would you like me to list your projects?"
        )
        assert result["intent"]["action"] == "project_not_found"
        assert result["requires_clarification"] is True


class TestDocstringHonesty:
    """The stale docstring claim fixed in the same commit (CXO §2)."""

    def test_docstring_no_longer_claims_delete_project_is_called(self):
        doc = CanonicalHandlers._handle_portfolio_query.__doc__ or ""
        assert 'Delete my project X" → PortfolioService.delete_project()' not in doc
