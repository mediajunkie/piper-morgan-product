"""#2024 (Arch ruling, CXO copy, 2026-10-15): a contextual offer
(``offer_hint``, the #852 rail) arms only on ONE yes/no question, and its
``offer_text`` is that question as the user sees it.

- ``_format_project_setup_guidance`` and ``_handle_project_setup_request``
  ask a single question (the either/or had no yes-answer); the other half
  is a statement with no offer attached.
- The professional branch of ``_handle_project_setup_request`` renders a
  statement, so it arms nothing.
- #2035 (Arch's rule, CXO's shape B): the two project-setup questions lead
  to a WRITE, so they arm the #846 store (``write_offer``, the
  offer_add_project landing), no longer an ``offer_hint``; the stored
  question is the rendered one (the same #1665/#1739 (a) adequacy).
- The archive / restore / search not-found replies keep their
  "Say 'list my ...'" directive and build no ``offer_hint`` (a directive is
  not an offer: nothing for a "yes" to bind).
"""

from __future__ import annotations

import re
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.onboarding.portfolio_service import PortfolioService
from services.shared_types import IntentCategory

_QUESTION = re.compile(r"[^.!?\n]*\?")


def _questions(text: str) -> list[str]:
    return [" ".join(q.split()) for q in _QUESTION.findall(text) if q.strip()]


def _intent(message: str, category=IntentCategory.PORTFOLIO, action="manage_portfolio"):
    return Intent(
        category=category,
        action=action,
        confidence=1.0,
        context={"original_message": message},
    )


class _FakeScope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


# ---------------------------------------------------------------------------
# Single yes/no offers (2383 / 2458)
# ---------------------------------------------------------------------------


def test_project_setup_guidance_asks_one_question_and_arms_it():
    out = CanonicalHandlers()._format_project_setup_guidance()
    msg = out["message"]
    assert _questions(msg) == ["Are you ready to set up your first project?"]
    assert out["write_offer"]["question"] == "Are you ready to set up your first project?"
    assert out["write_offer"]["workflow_type"] == "offer_add_project"
    assert "offer_hint" not in out  # #2035: off the #852 rail
    assert "Ask me how project context works any time." in msg
    assert "explain more" not in msg
    assert msg.rstrip().endswith("Are you ready to set up your first project?")


async def _setup_request(label: str):
    ctx = MagicMock()
    ctx.projects = ["Alpha", "Beta"]
    with (
        patch(
            "services.intent_service.canonical_handlers.user_context_service.get_user_context",
            new_callable=AsyncMock,
            return_value=ctx,
        ),
        patch("services.personality.formality.formality_label", return_value=label),
    ):
        return await CanonicalHandlers()._handle_project_setup_request(
            _intent("set up my projects", IntentCategory.GUIDANCE, "setup_projects"),
            "sess-2024",
            "user-2024",
        )


@pytest.mark.asyncio
@pytest.mark.parametrize("label", ["warm", "balanced"])
async def test_setup_request_asks_one_question_and_arms_it(label):
    out = await _setup_request(label)
    msg = out["message"]
    assert _questions(msg) == ["Want to add another?"]
    assert out["write_offer"]["question"] == "Want to add another?"
    assert out["write_offer"]["workflow_type"] == "offer_add_project"
    assert "offer_hint" not in out  # #2035: off the #852 rail
    assert "Say 'list my projects' to review what you have." in msg
    assert ", or " not in msg  # no either/or


@pytest.mark.asyncio
async def test_setup_request_professional_branch_states_and_does_not_arm():
    out = await _setup_request("professional")
    assert _questions(out["message"]) == []
    assert "I can help you add a new project or review your existing portfolio." in out["message"]
    assert "offer_hint" not in out
    assert "write_offer" not in out


# ---------------------------------------------------------------------------
# Directive not-found replies build no offer_hint (archive / restore / search)
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_archive_not_found_keeps_directive_and_builds_no_offer():
    from services.database.session_factory import AsyncSessionFactory

    with (
        patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())),
        patch.object(PortfolioService, "find_project_by_name", AsyncMock(return_value=None)),
        # #2271: archive resolves by exact name on the active, then archived, list.
        patch.object(PortfolioService, "list_active_projects", AsyncMock(return_value=[])),
        patch.object(PortfolioService, "list_archived_projects", AsyncMock(return_value=[])),
    ):
        out = await CanonicalHandlers()._handle_archive_project(
            _intent("archive project Zephyr"), "s1", "u1"
        )
    assert out["intent"]["action"] == "project_not_found"
    # #2271 (CXO 11-06): the not-found line is now CXO's, still a directive.
    assert 'Check the name, or say "show my projects".' in out["message"]
    assert "offer_hint" not in out


@pytest.mark.asyncio
async def test_restore_not_found_keeps_directive_and_builds_no_offer():
    from services.database.session_factory import AsyncSessionFactory

    with (
        patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())),
        patch.object(PortfolioService, "find_project_by_name", AsyncMock(return_value=None)),
    ):
        out = await CanonicalHandlers()._handle_restore_project(
            _intent("restore project Zephyr"), "s1", "u1"
        )
    assert out["intent"]["action"] == "project_not_found"
    assert "Say 'list my archived projects' to see what you have." in out["message"]
    assert "offer_hint" not in out


@pytest.mark.asyncio
async def test_search_no_results_keeps_directive_and_builds_no_offer():
    from services.database.session_factory import AsyncSessionFactory

    with (
        patch.object(AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())),
        patch.object(PortfolioService, "search_projects", AsyncMock(return_value=[])),
    ):
        out = await CanonicalHandlers()._handle_search_projects(
            _intent("search projects for nothing"), "s1", "u1"
        )
    assert "Say 'list my projects' to see what you have." in out["message"]
    assert "offer_hint" not in out
