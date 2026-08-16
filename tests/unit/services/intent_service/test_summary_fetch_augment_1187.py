"""#1187 fetch-augmentation core — `_fetch_summary_source_content` dispatcher.

For a `summarize` request whose source the floor can't reach (github_issue /
commit_range), this fetches the source content (via the _fetch_issue_content /
_fetch_commit_content helpers) so the floor can render the summary from it.
text/conversation are floor-direct (None); document is rail-handled upstream
since #1624 (a stray document emission landing here still degrades to None);
fetch failures degrade to None.

The floor-injection wiring (domain_context + _format_domain_context render branch +
prompt guidance) is a separate, UAT-sensitive step — these tests guard the pure
fetch dispatcher (no LLM, no network — the helpers are mocked).
"""

from contextlib import contextmanager
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
    async def test_document_source_rail_handled_returns_none(self, intent_service):
        # #1624: document summarize dispatches on the pre-floor rail; a stray
        # document emission that reaches this dispatcher anyway fetches nothing
        # (honest floor degrade, never fabrication).
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


# Raw GitHub-API issue shape (body/html_url/comments) — what fetch_issue_with_comments
# returns and what _fetch_issue_content's formatter expects (#1187 Option C).
_RAW_ISSUE = {
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

# Local-import targets inside _fetch_issue_content.
_FETCH = "services.integrations.github.issue_fetch.fetch_issue_with_comments"
_RESOLVE = "services.integrations.github.repo_resolver.resolve_repo"
_CONFIG = "services.integrations.github.config_service.GitHubConfigService"


def _resolved(full="mediajunkie/piper-morgan-product"):
    from services.integrations.github.repo_resolver import ResolvedRepo

    owner, name = full.split("/", 1)
    return ResolvedRepo(owner=owner, name=name, source="user_default")


@contextmanager
def _patched(*, token="ghp_valid", resolved=None, issue=_RAW_ISSUE, resolve_exc=None):
    """Patch the three deps _fetch_issue_content resolves: token (config), repo
    (resolve_repo), and the direct fetch. Yields the fetch mock for call asserts."""
    cfg = MagicMock()
    cfg.get_authentication_token.return_value = token
    resolve_mock = (
        AsyncMock(side_effect=resolve_exc)
        if resolve_exc
        else AsyncMock(return_value=resolved or _resolved())
    )
    with (
        patch(_CONFIG, return_value=cfg),
        patch(_RESOLVE, resolve_mock),
        patch(_FETCH, AsyncMock(return_value=issue)) as fetch_mock,
    ):
        yield fetch_mock


class TestGap1IssueNumberExtraction1187:
    """#1187 Gap 1 + Option C: the classifier tags source_type=github_issue but
    does NOT slot the number; `_fetch_issue_content` parses `#N`, resolves the
    repo (slice a) + token (keychain-first), and fetches the raw issue + comments
    directly. These mock those three deps so the real extraction path is exercised."""

    @pytest.mark.asyncio
    async def test_extracts_issue_number_and_fetches(self, intent_service):
        # No issue_number / repository in context — only the raw message has "#1124".
        with _patched() as fetch_mock:
            content, meta = await intent_service._fetch_issue_content(
                {"original_message": "summarize github issue #1124"}
            )
        # fetch called with (owner, repo, issue_number, token, ...)
        args = fetch_mock.await_args.args
        assert args[0] == "mediajunkie" and args[1] == "piper-morgan-product"
        assert args[2] == 1124
        assert meta["issue_number"] == 1124
        assert "Pre-floor handler migration" in content
        assert "Shim ratified." in content  # comment thread included (Option C)

    @pytest.mark.asyncio
    async def test_uses_resolved_repo_when_not_explicit(self, intent_service):
        with _patched():
            _content, meta = await intent_service._fetch_issue_content(
                {"original_message": "summarize issue 1124"}
            )
        assert meta["repository"] == "mediajunkie/piper-morgan-product"

    @pytest.mark.asyncio
    async def test_explicit_repository_skips_resolve(self, intent_service):
        with _patched() as fetch_mock:
            await intent_service._fetch_issue_content(
                {
                    "original_message": "summarize #1124",
                    "repository": "owner/repo",
                    "issue_number": 1124,
                }
            )
        args = fetch_mock.await_args.args
        assert args[0] == "owner" and args[1] == "repo"

    @pytest.mark.asyncio
    async def test_not_configured_raises(self, intent_service):
        with _patched(token=None):
            with pytest.raises(ValueError, match="not configured"):
                await intent_service._fetch_issue_content(
                    {"original_message": "summarize github issue #1124"}
                )

    @pytest.mark.asyncio
    async def test_no_issue_number_anywhere_raises(self, intent_service):
        with _patched():
            with pytest.raises(ValueError, match="No issue number"):
                await intent_service._fetch_issue_content(
                    {"original_message": "summarize the github issue please"}
                )

    @pytest.mark.asyncio
    async def test_unresolved_repo_raises(self, intent_service):
        from services.integrations.github.repo_resolver import UnresolvedRepoError

        with _patched(resolve_exc=UnresolvedRepoError("none")):
            with pytest.raises(ValueError, match="No repository resolved"):
                await intent_service._fetch_issue_content(
                    {"original_message": "summarize github issue #1124"}
                )

    @pytest.mark.asyncio
    async def test_issue_not_found_raises(self, intent_service):
        # fetch returns None (not found / no access / bad token) → raise inside the
        # try → re-wrapped as the generic "Failed to fetch GitHub issue" (msg kept).
        with _patched(issue=None):
            with pytest.raises(Exception, match="could not be fetched"):
                await intent_service._fetch_issue_content(
                    {"original_message": "summarize github issue #1124"}
                )

    @pytest.mark.asyncio
    async def test_end_to_end_via_fetch_summary_source(self, intent_service):
        intent = Intent(
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            original_message="summarize github issue #1124",
            context={
                "source_type": "github_issue",
                "original_message": "summarize github issue #1124",
            },
        )
        with _patched():
            result = await intent_service._fetch_summary_source_content(intent)
        assert result is not None
        content, meta = result
        assert "Pre-floor handler migration" in content
        assert meta["issue_number"] == 1124

    @pytest.mark.asyncio
    async def test_end_to_end_not_configured_degrades_to_none(self, intent_service):
        # Not configured → _fetch_issue_content raises → dispatcher swallows → None.
        intent = Intent(
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            original_message="summarize github issue #1124",
            context={"source_type": "github_issue"},
        )
        with _patched(token=None):
            assert await intent_service._fetch_summary_source_content(intent) is None

    @pytest.mark.asyncio
    async def test_infers_github_issue_from_collapsed_action_when_source_type_omitted(
        self, intent_service
    ):
        # The full-pipeline classifier (learned-pattern/KG enrichment) collapses to
        # action="summarize_github_issue" and OMITS source_type. The dispatcher must
        # still fire the fetch. (This was the live #1187 UAT bug.)
        intent = Intent(
            category=IntentCategory.SYNTHESIS,
            action="summarize_github_issue",
            original_message="summarize github issue #1124",
            context={"original_message": "summarize github issue #1124", "user_id": "u1"},
        )
        assert "source_type" not in intent.context  # classifier never set it
        with _patched():
            result = await intent_service._fetch_summary_source_content(intent)
        assert result is not None
        content, meta = result
        assert meta["issue_number"] == 1124

    @pytest.mark.asyncio
    async def test_infers_github_issue_from_message_when_action_generic(self, intent_service):
        # action is a generic "summarize" (no collapsed form) but the message clearly
        # references a github issue → infer from the message.
        intent = Intent(
            category=IntentCategory.SYNTHESIS,
            action="summarize",
            original_message="can you summarize github issue #1124 for me",
            context={"original_message": "can you summarize github issue #1124 for me"},
        )
        with _patched():
            result = await intent_service._fetch_summary_source_content(intent)
        assert result is not None

    @pytest.mark.asyncio
    async def test_does_not_infer_for_unrelated_synthesis(self, intent_service):
        # No source_type, no github signal → stays None (floor-direct), no fetch.
        intent = Intent(
            category=IntentCategory.SYNTHESIS,
            action="generate_content",
            original_message="write me a haiku about autumn",
            context={"original_message": "write me a haiku about autumn"},
        )
        with _patched() as fetch_mock:
            assert await intent_service._fetch_summary_source_content(intent) is None
        fetch_mock.assert_not_awaited()
