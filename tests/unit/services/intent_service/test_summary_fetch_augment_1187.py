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


class TestSummarizeFloorWiring1187:
    """The floor-injection wiring: _handle_synthesis_intent fetches + injects the
    source into domain_context; the floor renders it via _format_domain_context."""

    @pytest.mark.asyncio
    async def test_synthesis_injects_fetched_source_into_domain_context(self, intent_service):
        intent_service._fetch_summary_source_content = AsyncMock(
            return_value=("issue 42 body + comments", {"issue_number": 42})
        )
        intent_service._handle_unknown_intent = AsyncMock(return_value=MagicMock())
        await intent_service._handle_synthesis_intent(_intent("github_issue"), None, "sess-1")
        dc = intent_service._handle_unknown_intent.await_args.kwargs["domain_context"]
        assert dc["summary_source"]["content"] == "issue 42 body + comments"
        assert dc["summary_source"]["metadata"] == {"issue_number": 42}

    @pytest.mark.asyncio
    async def test_synthesis_no_fetch_passes_none_domain_context(self, intent_service):
        # text source → fetch returns None → floor with no injected source (floor-direct).
        intent_service._fetch_summary_source_content = AsyncMock(return_value=None)
        intent_service._handle_unknown_intent = AsyncMock(return_value=MagicMock())
        await intent_service._handle_synthesis_intent(_intent("text"), None, "sess-1")
        assert intent_service._handle_unknown_intent.await_args.kwargs["domain_context"] is None

    def test_floor_renders_summary_source_with_summarize_guidance(self):
        from services.intent_service.conversational_floor import ConversationalFloor
        block = ConversationalFloor()._format_domain_context(
            {"summary_source": {"content": "the issue body here", "metadata": {}}}
        )
        assert "SUMMARIZE" in block
        assert "the issue body here" in block

    def test_floor_skips_empty_summary_source(self):
        from services.intent_service.conversational_floor import ConversationalFloor
        block = ConversationalFloor()._format_domain_context(
            {"summary_source": {"content": "", "metadata": {}}}
        )
        assert "SUMMARIZE" not in block


_MOCK_ISSUE = {
    "number": 1124,
    "title": "Pre-floor handler migration",
    "body": "Migrate the legacy elif intent.action dispatch chains onto the rail.",
    "state": "closed",
    "user": {"login": "mediajunkie"},
    "created_at": "2026-06-01T00:00:00Z",
    "html_url": "https://github.com/mediajunkie/piper-morgan-product/issues/1124",
    "comments": [
        {"user": {"login": "arch"}, "body": "Shim ratified.", "created_at": "2026-06-02T00:00:00Z"},
    ],
}


def _mock_router(*, configured=True, issue=_MOCK_ISSUE):
    """A GitHubIntegrationRouter test double: lazy-init no-op, is_configured
    gate, and an async get_issue. Patch the class to return this instance."""
    router = MagicMock()
    router.initialize = AsyncMock(return_value=None)
    router.config_service.is_configured.return_value = configured
    router.get_issue = AsyncMock(return_value=issue)
    return router


_ROUTER_PATCH = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


class TestGap1IssueNumberExtraction1187:
    """#1187 Gap 1: the classifier tags source_type=github_issue but does NOT slot
    the issue number. `_fetch_issue_content` must parse `#N` from the raw message
    and fetch via the router (which resolves the repo internally, #1042). These
    mock the ROUTER (not the helper) so the real extraction path is exercised."""

    @pytest.mark.asyncio
    async def test_extracts_issue_number_from_bare_message(self, intent_service):
        # No issue_number / repository in context — only the raw message has "#1124".
        router = _mock_router()
        with patch(_ROUTER_PATCH, return_value=router):
            content, meta = await intent_service._fetch_issue_content(
                {"original_message": "summarize github issue #1124"}
            )
        # Router was asked for issue 1124 (parsed from the message).
        assert router.get_issue.await_args.args[0] == 1124
        assert meta["issue_number"] == 1124
        assert "Pre-floor handler migration" in content
        assert "Shim ratified." in content  # comments included

    @pytest.mark.asyncio
    async def test_repository_derived_from_html_url_when_not_explicit(self, intent_service):
        with patch(_ROUTER_PATCH, return_value=_mock_router()):
            _content, meta = await intent_service._fetch_issue_content(
                {"original_message": "summarize issue 1124"}
            )
        assert meta["repository"] == "mediajunkie/piper-morgan-product"

    @pytest.mark.asyncio
    async def test_explicit_repository_passed_to_router(self, intent_service):
        router = _mock_router()
        with patch(_ROUTER_PATCH, return_value=router):
            await intent_service._fetch_issue_content(
                {"original_message": "summarize #1124", "repository": "owner/repo", "issue_number": 1124}
            )
        kwargs = router.get_issue.await_args.kwargs
        assert kwargs["owner"] == "owner" and kwargs["repo_name"] == "repo"

    @pytest.mark.asyncio
    async def test_not_configured_raises(self, intent_service):
        with patch(_ROUTER_PATCH, return_value=_mock_router(configured=False)):
            with pytest.raises(ValueError, match="not configured"):
                await intent_service._fetch_issue_content(
                    {"original_message": "summarize github issue #1124"}
                )

    @pytest.mark.asyncio
    async def test_no_issue_number_anywhere_raises(self, intent_service):
        with patch(_ROUTER_PATCH, return_value=_mock_router()):
            with pytest.raises(ValueError, match="No issue number"):
                await intent_service._fetch_issue_content(
                    {"original_message": "summarize the github issue please"}
                )

    @pytest.mark.asyncio
    async def test_issue_not_found_raises(self, intent_service):
        # Router returns None (no repo resolved / issue missing) → raise → caller degrades.
        # The None-check raises inside the fetch try-block, so it's re-wrapped as the
        # generic "Failed to fetch GitHub issue: ..." Exception (message preserved).
        with patch(_ROUTER_PATCH, return_value=_mock_router(issue=None)):
            with pytest.raises(Exception, match="could not be fetched"):
                await intent_service._fetch_issue_content(
                    {"original_message": "summarize github issue #1124"}
                )

    @pytest.mark.asyncio
    async def test_end_to_end_via_fetch_summary_source(self, intent_service):
        # The #1187 entry point: bare message on intent.original_message, source_type
        # tagged, nothing slotted. Should produce (content, metadata) for the floor.
        intent = Intent(
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            original_message="summarize github issue #1124",
            context={"source_type": "github_issue", "original_message": "summarize github issue #1124"},
        )
        with patch(_ROUTER_PATCH, return_value=_mock_router()):
            result = await intent_service._fetch_summary_source_content(intent)
        assert result is not None
        content, meta = result
        assert "Pre-floor handler migration" in content
        assert meta["issue_number"] == 1124

    @pytest.mark.asyncio
    async def test_end_to_end_not_configured_degrades_to_none(self, intent_service):
        # Not configured → _fetch_issue_content raises → _fetch_summary_source_content
        # swallows it → None → floor degrades gracefully (no crash).
        intent = Intent(
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            original_message="summarize github issue #1124",
            context={"source_type": "github_issue"},
        )
        with patch(_ROUTER_PATCH, return_value=_mock_router(configured=False)):
            assert await intent_service._fetch_summary_source_content(intent) is None
