r"""#1124 Phase 2: _handle_comment_issue_query uses LLM slot-filling (extract_slots
+ COMMENT_ISSUE_TEMPLATE) instead of the old hand-regex (re.search(r"#?(\d+)") +
comment_patterns list). These tests patch extract_slots (no live LLM) to verify the
handler reads issue_number + comment_text from the extracted slots, parses the issue
number out of an ENTITY string, posts the comment, and asks for clarification when a
required slot is missing.
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


def _intent(msg="please comment on issue 42 that the build is green"):
    return Intent(
        category=IntentCategory.QUERY,
        action="comment_issue_query",
        context={"original_message": msg},
    )


def _mock_router():
    router = MagicMock()
    router.config_service.is_configured.return_value = True
    # #1220/#1382: the gate is now router.is_available() (binding OR PAT)
    router.is_available = AsyncMock(return_value=True)
    router.initialize = AsyncMock()
    router.add_comment = AsyncMock(return_value={"html_url": "https://github.com/o/r/issues/42#c1"})
    return router


class TestCommentIssueSlotFilling1124:
    @pytest.mark.asyncio
    async def test_extracted_slots_drive_add_comment(self, intent_service):
        router = _mock_router()
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"issue_number": "42", "comment_text": "the build is green"},
            ),
        ):
            result = await intent_service._handle_comment_issue_query(_intent(), "wf")

        router.add_comment.assert_awaited_once_with(42, "the build is green")
        assert result.success is True
        assert result.requires_clarification is False
        assert result.intent_data["issue_number"] == 42

    @pytest.mark.asyncio
    async def test_issue_number_parsed_from_hash_entity_string(self, intent_service):
        """The ENTITY slot may arrive as '#123' or 'issue 123' — the handler pulls digits."""
        router = _mock_router()
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"issue_number": "#123", "comment_text": "looks good"},
            ),
        ):
            await intent_service._handle_comment_issue_query(_intent(), "wf")
        router.add_comment.assert_awaited_once_with(123, "looks good")

    @pytest.mark.asyncio
    async def test_missing_issue_number_asks_for_clarification(self, intent_service):
        router = _mock_router()
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"issue_number": None, "comment_text": "great work"},
            ),
        ):
            result = await intent_service._handle_comment_issue_query(_intent(), "wf")

        assert result.requires_clarification is True
        assert "issue number" in result.message.lower()
        router.add_comment.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_missing_comment_text_asks_for_clarification(self, intent_service):
        router = _mock_router()
        with (
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
                return_value=router,
            ),
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"issue_number": "42", "comment_text": None},
            ),
        ):
            result = await intent_service._handle_comment_issue_query(_intent(), "wf")

        assert result.requires_clarification is True
        assert "comment" in result.message.lower()
        router.add_comment.assert_not_awaited()
