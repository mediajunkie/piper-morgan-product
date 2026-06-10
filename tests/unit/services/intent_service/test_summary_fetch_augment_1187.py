"""#1187 fetch-augmentation core — `_fetch_summary_source_content` dispatcher.

For a `summarize` request whose source the floor can't reach (github_issue /
commit_range), this fetches the source content (reusing the dormant _handle_summarize
helpers) so the floor can render the summary from it. text/conversation are
floor-direct (None); document is deferred (None); fetch failures degrade to None.

The floor-injection wiring (domain_context + _format_domain_context render branch +
prompt guidance) is a separate, UAT-sensitive step — these tests guard the pure
fetch dispatcher (no LLM, no network — the helpers are mocked).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent(source_type=None, **extra):
    ctx = {"original_message": "summarize it"}
    if source_type is not None:
        ctx["source_type"] = source_type
    ctx.update(extra)
    return Intent(category=IntentCategory.SYNTHESIS, action="summarize", context=ctx)


class TestFetchSummarySourceContent1187:
    @pytest.mark.asyncio
    async def test_github_issue_dispatches_to_issue_fetch(self, intent_service):
        intent_service._fetch_issue_content = AsyncMock(
            return_value=("issue 42 body + comments", {"issue_number": 42})
        )
        result = await intent_service._fetch_summary_source_content(_intent("github_issue"))
        assert result == ("issue 42 body + comments", {"issue_number": 42})
        intent_service._fetch_issue_content.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_commit_range_dispatches_to_commit_fetch_with_workflow_id(self, intent_service):
        intent_service._fetch_commit_content = AsyncMock(
            return_value=("commits this week", {"count": 7})
        )
        result = await intent_service._fetch_summary_source_content(
            _intent("commit_range"), workflow_id="wf-1"
        )
        assert result == ("commits this week", {"count": 7})
        # commit fetch needs the workflow_id (its 2nd arg).
        args = intent_service._fetch_commit_content.await_args.args
        assert args[1] == "wf-1"

    @pytest.mark.asyncio
    async def test_text_source_is_floor_direct_returns_none(self, intent_service):
        assert await intent_service._fetch_summary_source_content(_intent("text")) is None

    @pytest.mark.asyncio
    async def test_conversation_source_returns_none(self, intent_service):
        assert await intent_service._fetch_summary_source_content(_intent("conversation")) is None

    @pytest.mark.asyncio
    async def test_document_source_deferred_returns_none(self, intent_service):
        assert await intent_service._fetch_summary_source_content(_intent("document")) is None

    @pytest.mark.asyncio
    async def test_no_source_type_returns_none(self, intent_service):
        assert await intent_service._fetch_summary_source_content(_intent()) is None

    @pytest.mark.asyncio
    async def test_fetch_failure_degrades_to_none(self, intent_service):
        intent_service._fetch_issue_content = AsyncMock(side_effect=RuntimeError("GitHub 503"))
        # Graceful: returns None (floor degrades to "couldn't pull it") — does not raise.
        assert await intent_service._fetch_summary_source_content(_intent("github_issue")) is None
