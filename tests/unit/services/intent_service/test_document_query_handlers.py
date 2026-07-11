"""
Tests for Document Query Handlers.

Issue #522: Canonical Query #40 - "Update the X document"

Test categories:
1. Pre-classifier routing integration tests (verify full path)
2. Handler unit tests (verify handler logic)
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory


class TestPreClassifierDocumentRouting:
    """Test pre-classifier routes document update queries correctly.

    Issue #521 learning: Routing integration tests verify the full path
    from pre-classifier → intent service → handler.
    """

    @pytest.mark.parametrize(
        "query",
        [
            "update the README document",
            "update the project plan doc",
            "edit the meeting notes document",
            "modify the status document",
            "change the spec doc",
        ],
    )
    def test_document_update_queries_route_to_update_action(self, query):
        """Verify document update queries reach correct classification."""
        pre_classifier = PreClassifier()
        intent = pre_classifier.pre_classify(query)

        assert intent is not None, f"Query '{query}' should be classified"
        assert intent.category == IntentCategory.QUERY
        assert intent.action == "update_document_query"

    @pytest.mark.parametrize(
        "query",
        [
            "add to the notes document new items",
            "append to the log doc",
        ],
    )
    def test_document_add_queries_route_correctly(self, query):
        """Verify 'add to document' queries route correctly."""
        pre_classifier = PreClassifier()
        intent = pre_classifier.pre_classify(query)

        assert intent is not None, f"Query '{query}' should be classified"
        assert intent.category == IntentCategory.QUERY
        assert intent.action == "update_document_query"

    @pytest.mark.parametrize(
        "query",
        [
            "update project plan with new deadline",
            "edit the report with corrections",
        ],
    )
    def test_document_update_with_content_routes_correctly(self, query):
        """Verify update queries with content route correctly."""
        pre_classifier = PreClassifier()
        intent = pre_classifier.pre_classify(query)

        assert intent is not None, f"Query '{query}' should be classified"
        assert intent.category == IntentCategory.QUERY
        assert intent.action == "update_document_query"


class TestDocumentSlotExtraction:
    """Test the slot-filling extraction that replaces _parse_document_update_query.

    Issue #1121 MIGRATE-UPDATE-DOCUMENT-TO-SLOT-FILLING (2026-05-27):
    Original tests exercised a 5-pattern regex helper (deleted). LLM-driven
    extraction via extract_slots() + DOCUMENT_UPDATE_TEMPLATE handles the
    natural-language phrasings the regex flunked (parens, colons, antecedents).
    These tests verify the template shape; LLM behavior is mocked at the
    extract_slots layer in the handler tests below.
    """

    def test_template_shape(self):
        """DOCUMENT_UPDATE_TEMPLATE has the expected slots + required flags."""
        from services.slot_filling.slot_template import DOCUMENT_UPDATE_TEMPLATE

        assert DOCUMENT_UPDATE_TEMPLATE.name == "update_document"
        slot_names = [s.name for s in DOCUMENT_UPDATE_TEMPLATE.slots]
        assert "doc_name" in slot_names
        assert "content" in slot_names
        # Both required — handler returns clarification when extractor misses them
        for slot in DOCUMENT_UPDATE_TEMPLATE.slots:
            if slot.name in ("doc_name", "content"):
                assert slot.required, f"slot '{slot.name}' should be required"

    def test_template_extraction_hints_reference_natural_phrasings(self):
        """The template's extraction_hint fields name the kinds of phrasings
        that flunked the old regex (parens, 'by adding ... to it', etc.).
        This is a doc-comment-style assertion — it doesn't run the LLM but
        guards against the hints being dropped/simplified to the regex's
        narrow surface."""
        from services.slot_filling.slot_template import DOCUMENT_UPDATE_TEMPLATE

        slots = {s.name: s for s in DOCUMENT_UPDATE_TEMPLATE.slots}
        # doc_name hint should mention 'doc' or 'document' (the surface variants)
        assert "doc" in slots["doc_name"].extraction_hint.lower()
        # content hint should mention multiple phrasings, not just 'with'
        content_hint = slots["content"].extraction_hint.lower()
        assert any(
            phrase in content_hint for phrase in ["with", "by adding", "paragraph"]
        ), "content extraction_hint should name the natural-phrasing variants"


class TestUpdateDocumentNotConfigured:
    """Test graceful degradation when Notion is not configured."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance."""
        from services.intent.intent_service import IntentService

        return IntentService()

    @pytest.fixture
    def mock_intent(self):
        """Create mock intent for testing."""
        return Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the README document"},
        )

    @pytest.mark.asyncio
    async def test_not_configured_returns_graceful_message(self, intent_service, mock_intent):
        """Test handler returns helpful message when Notion not configured."""
        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = False
            mock_router.is_available.return_value = False  # #1383 gate
            MockRouter.return_value = mock_router

            result = await intent_service._handle_update_document_notion(
                mock_intent, "workflow-123", "session-456"
            )

            assert result.success is True
            assert "Notion isn't configured" in result.message
            assert result.implemented is False


class TestUpdateDocumentNotFound:
    """Test handling when document is not found."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance."""
        from services.intent.intent_service import IntentService

        return IntentService()

    @pytest.fixture
    def mock_intent(self):
        """Create mock intent for testing."""
        return Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the nonexistent document"},
        )

    @pytest.mark.asyncio
    async def test_document_not_found_returns_clarification(self, intent_service, mock_intent):
        """Test handler asks for clarification when document not found.

        #1121 update 2026-05-27: extract_slots is patched to return the slots
        the LLM would have extracted from the message — keeps the test focused
        on the not-found branch without touching live LLM.
        """
        with (
            patch(
                "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
            ) as MockRouter,
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"doc_name": "nonexistent", "content": None},
            ),
        ):
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock()
            mock_router.connect_for_user = AsyncMock()  # #1383
            mock_router.search_notion = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_update_document_notion(
                mock_intent, "workflow-123", "session-456"
            )

            assert result.success is True
            assert "No document found" in result.message
            assert result.requires_clarification is True


class TestUpdateDocumentMultipleMatches:
    """Test handling when multiple documents match."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance."""
        from services.intent.intent_service import IntentService

        return IntentService()

    @pytest.fixture
    def mock_intent(self):
        """Create mock intent for testing."""
        return Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the project document"},
        )

    @pytest.mark.asyncio
    async def test_multiple_matches_asks_for_clarification(self, intent_service, mock_intent):
        """Test handler asks which document when multiple match.

        #1121 update 2026-05-27: extract_slots patched (no live LLM).
        """
        with (
            patch(
                "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
            ) as MockRouter,
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"doc_name": "project", "content": None},
            ),
        ):
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock()
            mock_router.connect_for_user = AsyncMock()  # #1383
            mock_router.search_notion = AsyncMock(
                return_value=[
                    {
                        "id": "page-1",
                        "url": "https://notion.so/page-1",
                        "properties": {"title": {"title": [{"text": {"content": "Project Plan"}}]}},
                    },
                    {
                        "id": "page-2",
                        "url": "https://notion.so/page-2",
                        "properties": {
                            "title": {"title": [{"text": {"content": "Project Notes"}}]}
                        },
                    },
                ]
            )
            MockRouter.return_value = mock_router

            result = await intent_service._handle_update_document_notion(
                mock_intent, "workflow-123", "session-456"
            )

            assert result.success is True
            assert "Found 2 documents" in result.message
            assert "Project Plan" in result.message
            assert "Project Notes" in result.message
            assert result.requires_clarification is True
            assert result.clarification_type == "multiple_matches"


class TestUpdateDocumentSuccess:
    """Test successful document update flow."""

    @pytest.fixture
    def intent_service(self):
        """Create IntentService instance."""
        from services.intent.intent_service import IntentService

        return IntentService()

    @pytest.fixture
    def mock_intent_with_content(self):
        """Create mock intent with update content."""
        return Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the README document with new instructions"},
        )

    @pytest.mark.asyncio
    async def test_single_match_proceeds_to_update(self, intent_service, mock_intent_with_content):
        """Test handler proceeds to update when single document found.

        #1121 update 2026-05-27: extract_slots patched (no live LLM).
        Also: handler now uses append_blocks (post-#1080), not update_page
        — mock updated accordingly.
        """
        with (
            patch(
                "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
            ) as MockRouter,
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"doc_name": "README", "content": "new instructions"},
            ),
        ):
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock()
            mock_router.connect_for_user = AsyncMock()  # #1383
            mock_router.search_notion = AsyncMock(
                return_value=[
                    {
                        "id": "page-123",
                        "url": "https://notion.so/readme",
                        "properties": {"title": {"title": [{"text": {"content": "README"}}]}},
                    }
                ]
            )
            # #1080 ships append_blocks (not update_page) for the
            # update_document handler — see services/intent/intent_service.py
            # _handle_update_document_notion lines ~2790-2810
            mock_router.append_blocks = AsyncMock(return_value={"results": [{"id": "block-456"}]})
            MockRouter.return_value = mock_router

            result = await intent_service._handle_update_document_notion(
                mock_intent_with_content, "workflow-123", "session-456"
            )

            assert result.success is True
            # Post-#1080 response says "Appended to ..." not "Updated"
            assert "Appended to" in result.message or "README" in result.message
            assert result.intent_data.get("document_title") == "README"
