"""#1431 (REOPENED 2026-08-09): "list my archived projects" answered the ACTIVE list.

PM verification fail evidence (dev/2026/08/09 lead log): the utterance was asked
twice and both times got "You have 3 active projects: ..." — the archived list
never rendered. Second defect in the same screenshots: a per-intent status-fetch
failure string was space-joined onto the last list bullet, rendering as
"- One Job I wasn't able to check on project status ...".

Reachability trace (intent-routing-stack.md surfaces):
  Surface 1 (pre-classifier) CLAIMS the utterance deterministically —
  PORTFOLIO_PATTERNS' list pattern
  r"\\b(?:show|list|view)\\s+(?:my\\s+)?(?:all\\s+)?(?:archived\\s+)?projects\\b"
  matches "list my archived projects" → PORTFOLIO / manage_portfolio →
  canonical_handlers._handle_portfolio_query. Inside that handler, the
  operation sniffing checked ARCHIVE/DELETE/RESTORE patterns (none match:
  ARCHIVE_PATTERNS require "archive\\s+", not "archived"), then fell into the
  generic list branch (any of "show"/"list"/"view"), which called
  list_active_projects unconditionally. The archived token was matched by the
  routing pattern and then DISCARDED by the handler.

Moratorium note: the fix adds NO routing pattern — the claiming pattern
already recognizes the archived variant. The narrowing ("archived" token →
list_archived operation) lives inside the already-claiming handler: seam
work, not a new claim.

Defect 2 (F20) is covered at the repo/service layer by the real-DB tests in
tests/unit/services/database/test_list_archived_projects_1431.py; this file
covers the dispatch seam above it with mocks.
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.orchestrator import (
    IntentExecutionResult,
    IntentOrchestrator,
    OrchestratedResponse,
)
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


# ---------------------------------------------------------------------------
# Reachability: the pre-classifier claims the utterance (surface 1),
# so the fix site is the claiming handler — not a new pattern.
# ---------------------------------------------------------------------------


class TestArchivedListReachability:
    @pytest.mark.parametrize(
        "message",
        [
            "list my archived projects",
            "List my archived projects",
            "show my archived projects",
            "show archived projects",
            "view my archived projects",
        ],
    )
    def test_archived_list_claimed_by_portfolio(self, message):
        intent = PreClassifier.pre_classify(message)
        assert intent is not None, f"pre-classifier did not claim {message!r}"
        assert intent.category == IntentCategory.PORTFOLIO
        assert intent.action == "manage_portfolio"

    def test_plain_list_still_claimed_by_portfolio(self):
        """Regression guard: the active-list phrasing keeps its claim."""
        intent = PreClassifier.pre_classify("list my projects")
        assert intent is not None
        assert intent.category == IntentCategory.PORTFOLIO
        assert intent.action == "manage_portfolio"


# ---------------------------------------------------------------------------
# The handler seam: archived phrasing must dispatch to
# PortfolioService.list_archived_projects, never list_active_projects.
# ---------------------------------------------------------------------------


def _portfolio_intent(message: str) -> Intent:
    return Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_portfolio",
        confidence=1.0,
        context={"original_message": message},
    )


class _FakeScope:
    async def __aenter__(self):
        return MagicMock()

    async def __aexit__(self, *args):
        return False


@pytest.fixture
def handler():
    return CanonicalHandlers()


async def _run_portfolio(handler, message, archived_rows, active_rows):
    """Drive _handle_portfolio_query with both service methods mocked.

    Returns (result_dict, archived_mock, active_mock).
    """
    archived_mock = AsyncMock(return_value=archived_rows)
    active_mock = AsyncMock(return_value=active_rows)

    from services.database.session_factory import AsyncSessionFactory
    from services.onboarding.portfolio_service import PortfolioService

    with patch.object(
        AsyncSessionFactory, "session_scope", staticmethod(lambda: _FakeScope())
    ):
        with patch.object(PortfolioService, "list_archived_projects", archived_mock):
            with patch.object(PortfolioService, "list_active_projects", active_mock):
                result = await handler._handle_portfolio_query(
                    _portfolio_intent(message), session_id="s1", user_id="u1"
                )
    return result, archived_mock, active_mock


ARCHIVED_ROWS = [
    SimpleNamespace(name="Old Prototype"),
    SimpleNamespace(name="Sunset Initiative"),
]
ACTIVE_ROWS = [
    SimpleNamespace(name="Klatch"),
    SimpleNamespace(name="One Job"),
    SimpleNamespace(name="CoVa"),
]


class TestArchivedListDispatch1431:
    @pytest.mark.asyncio
    async def test_archived_phrasing_reads_archived_rows(self, handler):
        """THE reopened defect: 'list my archived projects' must never answer
        with the active list."""
        result, archived_mock, active_mock = await _run_portfolio(
            handler, "list my archived projects", ARCHIVED_ROWS, ACTIVE_ROWS
        )
        archived_mock.assert_awaited_once()
        active_mock.assert_not_awaited()
        msg = result["message"]
        assert "archived" in msg.lower()
        assert "active projects" not in msg.lower(), (
            "archived query answered with the ACTIVE list (PM fail 2026-08-09)"
        )
        assert "Old Prototype" in msg
        assert "Sunset Initiative" in msg

    @pytest.mark.asyncio
    async def test_archived_dispatch_is_owner_scoped(self, handler):
        """The service call must carry the asking user's id (F20 owner scoping)."""
        _, archived_mock, _ = await _run_portfolio(
            handler, "list my archived projects", ARCHIVED_ROWS, ACTIVE_ROWS
        )
        assert archived_mock.await_args.kwargs.get("user_id") == "u1"

    @pytest.mark.asyncio
    async def test_archived_intent_action_labeled(self, handler):
        result, _, _ = await _run_portfolio(
            handler, "show my archived projects", ARCHIVED_ROWS, ACTIVE_ROWS
        )
        assert result["intent"]["action"] == "list_archived_projects"

    @pytest.mark.asyncio
    async def test_empty_archived_list_is_honest(self, handler):
        """No archived rows → say so; do NOT fall back to the active list."""
        result, archived_mock, active_mock = await _run_portfolio(
            handler, "list my archived projects", [], ACTIVE_ROWS
        )
        archived_mock.assert_awaited_once()
        active_mock.assert_not_awaited()
        msg = result["message"].lower()
        assert "archived" in msg
        assert "klatch" not in msg

    @pytest.mark.asyncio
    async def test_plain_list_still_reads_active_rows(self, handler):
        """Regression guard: the active list path is unchanged."""
        result, archived_mock, active_mock = await _run_portfolio(
            handler, "list my projects", ARCHIVED_ROWS, ACTIVE_ROWS
        )
        active_mock.assert_awaited_once()
        archived_mock.assert_not_awaited()
        msg = result["message"]
        assert "3 active projects" in msg
        assert "Klatch" in msg


# ---------------------------------------------------------------------------
# Bonus defect (same screenshots): the aggregator's failure note must be its
# own paragraph, never space-joined onto the last content line (which rendered
# as "- One Job I wasn't able to check on project status ...").
# ---------------------------------------------------------------------------


class TestFailureNoteOwnLine1431:
    @pytest.fixture
    def orchestrator(self):
        return IntentOrchestrator(canonical_handlers=MagicMock())

    def _intent(self, category, action):
        return Intent(category=category, action=action, confidence=1.0)

    def test_failure_note_not_merged_into_bullet(self, orchestrator):
        bullet_list = (
            "You have 3 active projects:\n\n- Klatch\n- CoVa\n- One Job"
        )
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=self._intent(IntentCategory.PORTFOLIO, "manage_portfolio"),
                    response=bullet_list,
                    success=True,
                ),
                IntentExecutionResult(
                    intent=self._intent(IntentCategory.STATUS, "get_project_status"),
                    success=False,
                    error="Timeout",
                ),
            ]
        )
        msg = orchestrator._aggregate_messages(response)
        # The failure note must still be present...
        assert "wasn't able" in msg
        # ...but on its own line, never glued to the last bullet.
        offending_lines = [
            line
            for line in msg.splitlines()
            if line.lstrip().startswith("-") and "wasn't able" in line
        ]
        assert not offending_lines, (
            f"failure note merged into a list bullet: {offending_lines!r}"
        )
        # The last bullet survives intact as its own line.
        assert "- One Job" in msg.splitlines()

    def test_multi_failure_note_own_line(self, orchestrator):
        response = OrchestratedResponse(
            results=[
                IntentExecutionResult(
                    intent=self._intent(IntentCategory.QUERY, "meeting_time"),
                    response="Your next meeting is at 2pm.",
                    success=True,
                ),
                IntentExecutionResult(
                    intent=self._intent(IntentCategory.STATUS, "get_project_status"),
                    success=False,
                ),
                IntentExecutionResult(
                    intent=self._intent(IntentCategory.QUERY, "github_query"),
                    success=False,
                ),
            ]
        )
        msg = orchestrator._aggregate_messages(response)
        assert "wasn't able" in msg
        note_line = next(line for line in msg.splitlines() if "wasn't able" in line)
        assert "2pm" not in note_line, "failure note shares a line with content"
