"""Arch's 2026-10-04 ruling (generalizing #1926, mailboxes/lead/inbox/rule-
arch-to-lead-cc-cxo-exec-cio-canonical-must-not-claim-any-rail-key-hold-
read-portfolio-flip-pard-findings-2026-10-04.md §1): "the rail owns every
rail key" — CanonicalHandlers.can_handle now declines ANY action with a
rail entry, not just needs_confirm ones (#1926's narrower predecessor).
Arch's two pins, verified directly against the live dispatch order
(``_should_route_to_floor -> can_handle -> _dispatch_action_rail``), never
assumed:

  (a) A full ``process_intent`` turn with a dispatched ``list_repos`` Intent
      reaches ``_dispatch_action_rail`` and returns the repo list — NOT
      ``portfolio_help`` (the exact failure Arch traced for the
      ``read_portfolio`` flip: "a router-named list_repos or search_projects
      goes to _handle_portfolio_query, the handler where you watched
      unlink_repo answer portfolio_help"). Driven via the live-consult seam
      (``consult_inversion_live`` monkeypatched to return a dispatched
      Intent), same seam Arch names as the real caller of this rail key
      today.

  (b) A PORTFOLIO WRITE (``archive_project``) reaches the #1509 consent
      block — ``consent_gate.evaluate_consent`` is actually called (spied,
      call-through) with ``EffectClass.WRITE``, which could not happen
      before this generalization: the canonical whole-category claim
      swallowed the turn before ``_dispatch_action_rail``'s consent check
      was ever reached.

Mocking idiom mirrors
tests/unit/services/intent_service/test_inversion_write_allowlist_unlink_repo_1926.py
(DB layer patched, never a live router or LLM call — m-43 layer honesty:
this is unit-layer, not e2e).
"""

from __future__ import annotations

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory

pytestmark = pytest.mark.unit

_USER = "3f7b8a52-1926-4b00-9e00-000000001926"
_SESSION = "sess-1926-rail-owns-rail-keys"

_PATCH_SESSION_FACTORY = "services.database.session_factory.AsyncSessionFactory"
_PATCH_PROJECT_REPO = "services.database.repositories.ProjectRepository"
_PATCH_REPO_REPO = "services.database.repositories.RepositoryRepository"


def _mock_session_factory():
    mock_session = AsyncMock()

    @asynccontextmanager
    async def _session_scope():
        yield mock_session

    mock_factory = MagicMock()
    mock_factory.session_scope = _session_scope
    return mock_factory


@pytest.fixture(autouse=True)
def _rail_registered():
    register_default_workflows()


# ---------------------------------------------------------------------------
# Pin (a): list_repos via the live-consult seam reaches the rail, not the
# portfolio help menu.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestPinAListRepoReachesTheRail:
    async def test_can_handle_declines_a_classified_list_repos_intent(self):
        """The unit-level fact the end-to-end pin below depends on."""
        handler = CanonicalHandlers()
        intent = Intent(
            category=IntentCategory.PORTFOLIO,
            action="list_repos",
            confidence=0.95,
            original_message="list my repos",
            context={"original_message": "list my repos"},
        )
        assert handler.can_handle(intent) is False

    async def test_full_process_intent_turn_returns_the_repo_list_not_portfolio_help(self):
        """Arch's pin (a): drive a dispatched list_repos Intent through the
        LIVE-CONSULT seam (consult_inversion_live) — the same seam Arch
        named as this rail key's real caller today — into a full
        ``process_intent`` turn, and assert the repo list comes back, not
        the portfolio help menu ``_handle_portfolio_query`` would have
        rendered under the PRE-generalization whole-category claim."""
        repo = MagicMock()
        repo.id = "repo-1"
        repo.full_name = "mediajunkie/piper-morgan"
        repo.provider = "github"

        mock_factory = _mock_session_factory()
        mock_repo_repo = AsyncMock()
        mock_repo_repo.list_by_owner = AsyncMock(return_value=[repo])

        msg = "list my repos"
        dispatched_intent = Intent(
            category=IntentCategory.PORTFOLIO,
            action="list_repos",
            confidence=0.95,
            original_message=msg,
            context={"original_message": msg},
        )

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO),
            patch(_PATCH_REPO_REPO, return_value=mock_repo_repo),
            patch(
                "services.intent_service.inversion_live.consult_inversion_live",
                new=AsyncMock(return_value=dispatched_intent),
            ),
        ):
            service = IntentService()
            result = await service.process_intent(message=msg, session_id=_SESSION, user_id=_USER)

        assert "mediajunkie/piper-morgan" in result.message
        assert "registered" in result.message.lower()
        # The #1766 portfolio_help menu's own signature line — proves the
        # OLD (pre-generalization) swallow path was NOT taken.
        assert "what would you like to do" not in result.message.lower()
        assert result.intent_data.get("action") == "list_repos"
        mock_repo_repo.list_by_owner.assert_awaited_once()


# ---------------------------------------------------------------------------
# Pin (b): a PORTFOLIO WRITE (archive_project) reaches the #1509 consent
# block.
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
class TestPinBArchiveProjectReachesTheConsentBlock:
    async def test_can_handle_declines_a_classified_archive_project_intent(self):
        handler = CanonicalHandlers()
        intent = Intent(
            category=IntentCategory.PORTFOLIO,
            action="archive_project",
            confidence=0.95,
            original_message="archive project Foo",
            context={"original_message": "archive project Foo"},
        )
        assert handler.can_handle(intent) is False

    async def test_full_process_intent_turn_evaluates_the_1509_consent_decision(self):
        """Arch's pin (b): the #1509 consent gate (consent_gate.evaluate_consent)
        must actually be CALLED for a classified archive_project turn —
        something that could not happen before this generalization, since
        PORTFOLIO's whole-category canonical claim swallowed the turn
        BEFORE ``_dispatch_action_rail``'s needs_consent check was ever
        reached. Spied (call-through, never mocked-out) so the assertion is
        "this ran", mirroring the existing consent-gate test idiom
        (test_consent_gate_1509.py) rather than a parallel implementation."""
        from services.intent_service import consent_gate as real_consent_gate

        calls = []
        _real_evaluate_consent = real_consent_gate.evaluate_consent

        async def _spy_evaluate_consent(effect, message, user_id, outwardness=None):
            calls.append({"effect": effect, "message": message, "user_id": user_id})
            if outwardness is None:
                return await _real_evaluate_consent(effect, message, user_id)
            return await _real_evaluate_consent(effect, message, user_id, outwardness=outwardness)

        mock_factory = _mock_session_factory()
        mock_project_repo = AsyncMock()
        mock_project_repo.find_by_name = AsyncMock(return_value=None)  # project-not-found leg

        msg = "archive project Foo"
        dispatched_intent = Intent(
            category=IntentCategory.PORTFOLIO,
            action="archive_project",
            confidence=0.95,
            original_message=msg,
            context={"original_message": msg},
        )

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(
                "services.onboarding.portfolio_service.PortfolioService.find_project_by_name",
                new=AsyncMock(return_value=None),
            ),
            patch.object(real_consent_gate, "evaluate_consent", new=_spy_evaluate_consent),
            patch(
                "services.intent_service.inversion_live.consult_inversion_live",
                new=AsyncMock(return_value=dispatched_intent),
            ),
        ):
            service = IntentService()
            result = await service.process_intent(message=msg, session_id=_SESSION, user_id=_USER)

        assert len(calls) == 1, "evaluate_consent (the #1509 decision) was never evaluated"
        assert calls[0]["effect"] == EffectClass.WRITE
        # The handler ran for real (project-not-found leg) — the write path
        # reached _handle_archive_project, not the old canonical swallow.
        assert "foo" in result.message.lower()
        assert result.intent_data.get("action") in ("archive_project", "project_not_found")
