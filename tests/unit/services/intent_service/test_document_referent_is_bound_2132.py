"""#2132 — "analyze this document" resolves only to a bound referent.

Arch (15:05) found that with Notion connected and no title named, the handler
searched Notion with the whole message and presented the top hit as the
document asked about. CXO's words (15:25) for the unbound case, and the reply
names the page it read when a title was extracted.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.shared_types import IntentCategory

# #2138 (CXO 18:5x): Notion connected, nothing bound, no title.
NO_DOC_LINE = (
    "I couldn't tell which document you mean. Name an uploaded file or a "
    "Notion page, or paste the text here and I'll work with it."
)


@pytest.fixture
def intent_service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _router():
    r = MagicMock()
    r.is_available.return_value = True
    r.ais_available = AsyncMock(return_value=True)  # #2238: the async gate
    r.connect_for_user = AsyncMock()
    r.search_notion = AsyncMock(
        return_value=[
            {
                "id": "page-roadmap",
                "properties": {"title": {"title": [{"text": {"content": "Q4 Roadmap"}}]}},
            }
        ]
    )
    r.get_page = AsyncMock(
        return_value={"title": "Q4 Roadmap", "url": "https://notion.so/q4", "last_edited_time": "x"}
    )
    r.get_page_blocks = AsyncMock(
        return_value=[
            {"type": "paragraph", "paragraph": {"rich_text": [{"plain_text": "Ship it."}]}}
        ]
    )
    return r


@pytest.mark.asyncio
async def test_no_title_named_gets_cxos_line_and_no_search(intent_service):
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_document",
        context={"original_message": "Analyze this document"},
    )
    router = _router()
    with patch(
        "services.integrations.notion.notion_integration_router.NotionIntegrationRouter",
        return_value=router,
    ):
        result = await intent_service._handle_analyze_document_notion(intent, "wf", "s")
    assert result.message == NO_DOC_LINE
    router.search_notion.assert_not_called()
    router.get_page.assert_not_called()
    assert "Roadmap" not in result.message


@pytest.mark.asyncio
async def test_extracted_title_is_the_query_and_the_reply_names_the_page(intent_service):
    intent = Intent(
        category=IntentCategory.ANALYSIS,
        action="analyze_document",
        context={"original_message": "Analyze the Q4 Roadmap doc", "document_title": "Q4 Roadmap"},
    )
    router = _router()
    with patch(
        "services.integrations.notion.notion_integration_router.NotionIntegrationRouter",
        return_value=router,
    ):
        result = await intent_service._handle_analyze_document_notion(intent, "wf", "s")
    assert router.search_notion.await_args.kwargs["query"] == "Q4 Roadmap"
    assert result.message.startswith("I read 'Q4 Roadmap' in Notion.")
