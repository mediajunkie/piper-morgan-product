"""
Unit tests for Notion document handlers in IntentService.

Issue #515: Canonical Query #17 - Document Analysis
Issue #516: Canonical Query #20 - Document Search

Tests cover:
- Handler routing for document actions
- Graceful fallback when Notion is not configured
- Search result formatting
- Document analysis response formatting
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.workflow_dispatcher import dispatch_workflow
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import IntentCategory


@pytest.fixture
def mock_workflow():
    """Mock workflow object"""
    workflow = MagicMock()
    workflow.id = "test-workflow-id"
    return workflow


@pytest.fixture
def intent_service():
    """Create IntentService instance for testing"""
    # Patch dependencies to avoid initialization issues
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            service = IntentService()
            return service


class TestDocumentSearchRouting:
    """Test routing to document search handler"""

    @pytest.mark.asyncio
    async def test_routes_search_documents_action(self, intent_service, mock_workflow):
        """Test that search_documents action routes to Notion handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_documents",
            context={"original_message": "search for architecture docs"},
        )

        with patch.object(
            intent_service, "_handle_search_documents_notion", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Found 3 documents",
                intent_data={"category": "query", "action": "search_documents"},
            )

            # #1124: document search queries now dispatch via the action-dispatch rail —
            # _handle_query_intent's elif was removed. Factory threads
            # (intent, workflow_id, session_id).
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id, "test-session")

    @pytest.mark.asyncio
    async def test_routes_find_documents_action(self, intent_service, mock_workflow):
        """Test that find_documents action also routes to Notion handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="find_documents",
            context={"original_message": "find all ADRs"},
        )

        with patch.object(
            intent_service, "_handle_search_documents_notion", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Found 5 documents",
                intent_data={"category": "query", "action": "find_documents"},
            )

            # #1124: document search queries now dispatch via the action-dispatch rail.
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()

    @pytest.mark.asyncio
    async def test_routes_search_notion_action(self, intent_service, mock_workflow):
        """Test that search_notion action routes to Notion handler"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_notion",
            context={"original_message": "search notion for meeting notes"},
        )

        with patch.object(
            intent_service, "_handle_search_documents_notion", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Found 2 documents",
                intent_data={"category": "query", "action": "search_notion"},
            )

            # #1124: document search queries now dispatch via the action-dispatch rail.
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()


class TestDocumentAnalysisRouting:
    """Test routing to document analysis handler"""

    @pytest.mark.asyncio
    async def test_routes_analyze_document_action(self, intent_service, mock_workflow):
        """Test that analyze_document action routes to Notion handler"""
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze this document"},
        )

        with patch.object(
            intent_service, "_handle_analyze_document_notion", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="Document analysis complete",
                intent_data={"category": "analysis", "action": "analyze_document"},
            )

            # #1124: analyze_document/analyze_file now dispatch via the action-dispatch
            # rail (final-if-heads, pass_session_id) — _handle_analysis_intent's if-head
            # was removed. Route by intent.action through the real rail.
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once_with(intent, mock_workflow.id, "test-session")

    @pytest.mark.asyncio
    async def test_routes_analyze_file_action(self, intent_service, mock_workflow):
        """Test that analyze_file action also routes to Notion handler"""
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_file",
            context={"original_message": "analyze the report"},
        )

        with patch.object(
            intent_service, "_handle_analyze_document_notion", new_callable=AsyncMock
        ) as mock_handler:
            mock_handler.return_value = IntentProcessingResult(
                success=True,
                message="File analysis complete",
                intent_data={"category": "analysis", "action": "analyze_file"},
            )

            # #1124: analyze_document/analyze_file now dispatch via the action-dispatch
            # rail (final-if-heads, pass_session_id) — _handle_analysis_intent's if-head
            # was removed. Route by intent.action through the real rail.
            register_default_workflows()
            await dispatch_workflow(
                workflow_type=intent.action,
                session_id="test-session",
                user_id=None,
                context={
                    "intent": intent,
                    "workflow_id": mock_workflow.id,
                    "intent_service": intent_service,
                },
            )

            mock_handler.assert_called_once()


class TestNotionNotConfiguredGracefulDegradation:
    """Test graceful fallback when Notion is not configured"""

    @pytest.mark.asyncio
    async def test_search_returns_graceful_message_when_notion_not_configured(self, intent_service):
        """Test search handler returns helpful message when Notion not configured"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_documents",
            context={"original_message": "search for docs"},
        )

        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = False
            mock_router.is_available.return_value = False  # #1383 gate
            MockRouter.return_value = mock_router

            result = await intent_service._handle_search_documents_notion(
                intent, "workflow-id", "session-id"
            )

            assert result.success is True
            assert "Notion isn't configured yet" in result.message
            assert "NOTION_API_KEY" in result.message
            assert result.implemented is False

    @pytest.mark.asyncio
    async def test_analysis_returns_graceful_message_when_notion_not_configured(
        self, intent_service
    ):
        """Test analysis handler returns helpful message when Notion not configured"""
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze this doc"},
        )

        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = False
            mock_router.is_available.return_value = False  # #1383 gate
            MockRouter.return_value = mock_router

            result = await intent_service._handle_analyze_document_notion(
                intent, "workflow-id", "session-id"
            )

            assert result.success is True
            assert "Notion isn't configured yet" in result.message
            assert "NOTION_API_KEY" in result.message
            assert result.implemented is False


class TestDocumentSearchResults:
    """Test document search result formatting"""

    @pytest.mark.asyncio
    async def test_formats_search_results_correctly(self, intent_service):
        """Test search results are formatted properly"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_documents",
            context={"original_message": "search for ADR"},
        )

        mock_search_results = [
            {
                "id": "page-1",
                "url": "https://notion.so/page-1",
                "last_edited_time": "2025-12-24T10:00:00Z",
                "properties": {
                    "title": {"title": [{"text": {"content": "ADR-001: Architecture"}}]}
                },
            },
            {
                "id": "page-2",
                "url": "https://notion.so/page-2",
                "last_edited_time": "2025-12-23T10:00:00Z",
                "properties": {"Name": {"title": [{"text": {"content": "ADR-002: Database"}}]}},
            },
        ]

        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock()
            mock_router.connect_for_user = AsyncMock()  # #1383
            mock_router.search_notion = AsyncMock(return_value=mock_search_results)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_search_documents_notion(
                intent, "workflow-id", "session-id"
            )

            assert result.success is True
            # Grammar-conscious formatting may use different phrasing (Issue #633-638)
            assert "2" in result.message and (
                "found" in result.message.lower() or "result" in result.message.lower()
            )
            assert "ADR-001: Architecture" in result.message
            assert "ADR-002: Database" in result.message
            assert result.intent_data["result_count"] == 2

    @pytest.mark.asyncio
    async def test_handles_no_search_results(self, intent_service):
        """Test handling when no documents match search"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_documents",
            context={"original_message": "search for nonexistent"},
        )

        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock()
            mock_router.connect_for_user = AsyncMock()  # #1383
            mock_router.search_notion = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_search_documents_notion(
                intent, "workflow-id", "session-id"
            )

            assert result.success is True
            # Grammar-conscious formatting may use different phrasing (Issue #633-638)
            assert (
                "didn't find" in result.message.lower()
                or "no documents" in result.message.lower()
                or "no results" in result.message.lower()
            )
            assert result.intent_data["result_count"] == 0


class TestDocumentAnalysisResults:
    """Test document analysis result formatting"""

    @pytest.mark.asyncio
    async def test_analyzes_document_content(self, intent_service):
        """Test document analysis extracts and summarizes content"""
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={
                "document_id": "page-123",
                "original_message": "analyze this document",
            },
        )

        mock_page_data = {
            "id": "page-123",
            "title": "Test Document",
            "url": "https://notion.so/page-123",
            "last_edited_time": "2025-12-24T10:00:00Z",
        }

        mock_blocks = [
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "This is the first paragraph."}]},
            },
            {
                "type": "heading_1",
                "heading_1": {"rich_text": [{"plain_text": "Section Header"}]},
            },
            {
                "type": "paragraph",
                "paragraph": {"rich_text": [{"plain_text": "More content here."}]},
            },
        ]

        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock()
            mock_router.connect_for_user = AsyncMock()  # #1383
            mock_router.get_page = AsyncMock(return_value=mock_page_data)
            mock_router.get_page_blocks = AsyncMock(return_value=mock_blocks)
            MockRouter.return_value = mock_router

            result = await intent_service._handle_analyze_document_notion(
                intent, "workflow-id", "session-id"
            )

            assert result.success is True
            assert "Document Analysis: Test Document" in result.message
            assert "Word count:" in result.message
            assert "Sections:" in result.message
            assert result.intent_data["document_id"] == "page-123"

    @pytest.mark.asyncio
    async def test_requires_clarification_when_no_document_found(self, intent_service):
        """Test handler asks for clarification when document not found"""
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={"original_message": "analyze something vague"},
        )

        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock()
            mock_router.connect_for_user = AsyncMock()  # #1383
            mock_router.search_notion = AsyncMock(return_value=[])
            MockRouter.return_value = mock_router

            result = await intent_service._handle_analyze_document_notion(
                intent, "workflow-id", "session-id"
            )

            assert result.success is True
            assert result.requires_clarification is True
            assert "couldn't find" in result.message.lower()


class TestDocumentHandlerErrors:
    """Test error handling in document handlers"""

    @pytest.mark.asyncio
    async def test_search_handles_notion_error(self, intent_service):
        """Test search handler gracefully handles Notion API errors"""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="search_documents",
            context={"original_message": "search for docs"},
        )

        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock(side_effect=Exception("API connection failed"))
            mock_router.connect_for_user = AsyncMock(side_effect=Exception("API connection failed"))  # #1383
            MockRouter.return_value = mock_router

            result = await intent_service._handle_search_documents_notion(
                intent, "workflow-id", "session-id"
            )

            assert result.success is False
            # Grammar-conscious error formatting (Issue #633-638)
            assert (
                "problem" in result.message.lower()
                or "unable" in result.message.lower()
                or "error" in result.message.lower()
            )
            assert result.error is not None
            assert result.error_type == "NotionSearchError"

    @pytest.mark.asyncio
    async def test_analysis_handles_notion_error(self, intent_service):
        """Test analysis handler gracefully handles Notion API errors"""
        intent = Intent(
            category=IntentCategory.ANALYSIS,
            action="analyze_document",
            context={
                "document_id": "page-123",
                "original_message": "analyze this",
            },
        )

        with patch(
            "services.integrations.notion.notion_integration_router.NotionIntegrationRouter"
        ) as MockRouter:
            mock_router = MagicMock()
            mock_router.is_configured.return_value = True
            mock_router.is_available.return_value = True  # #1383 gate
            mock_router.connect = AsyncMock()
            mock_router.connect_for_user = AsyncMock()  # #1383
            mock_router.get_page = AsyncMock(side_effect=Exception("Page not accessible"))
            MockRouter.return_value = mock_router

            result = await intent_service._handle_analyze_document_notion(
                intent, "workflow-id", "session-id"
            )

            assert result.success is False
            assert "analyzing that document" in result.message
            assert result.error is not None
            assert result.error_type == "NotionAnalysisError"
