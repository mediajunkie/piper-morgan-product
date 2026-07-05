#!/usr/bin/env python3
"""
Test Notion MCP + Spatial Integration

Comprehensive test suite for Notion integration with MCP+Spatial Intelligence.
Tests cover:
1. Connection and authentication (notion-client library — post-#304)
2. Spatial dimension analysis (unchanged across the aiohttp→notion-client migration)
3. MCP protocol compliance (database/page operations via notion-client)
4. Full integration workflow

Issue #1082 (#304 follow-up): the previous version of this file targeted the
pre-#304 aiohttp adapter (mocking aiohttp.ClientSession, calling removed
configure_notion_api / _call_notion_api). Rewritten 2026-05-24 to mock
notion_client.Client directly (sync API) and exercise the post-#304 surface.

Coverage relationship:
- tests/unit/services/integrations/mcp/test_notion_adapter.py — get_current_user
  surface (10 tests, all pass; person/bot, error paths, edge cases)
- THIS FILE — broader integration surface: connection, database operations,
  page operations, workspace mapping, spatial dimension analysis
- Both run under the standard pytest harness with notion-client mocks.
"""

from unittest.mock import MagicMock, patch

import pytest
from notion_client.errors import APIResponseError, RequestTimeoutError

from services.integrations.mcp.notion_adapter import NotionMCPAdapter
from services.integrations.spatial_adapter import BaseSpatialAdapter


def _adapter_with_mock_client() -> NotionMCPAdapter:
    """Build a NotionMCPAdapter with a mocked _notion_client.

    Mirrors the setup_method pattern in test_notion_adapter.py — patches
    NotionConfig so __init__ doesn't try to read env / validate config,
    then injects a MagicMock for the notion-client.Client surface.
    """
    with patch("services.mcp.consumer.notion_adapter.NotionConfig"):
        adapter = NotionMCPAdapter()
    adapter._notion_client = MagicMock()
    return adapter


# ---------------------------------------------------------------------------
# Connection + Authentication
# ---------------------------------------------------------------------------


class TestNotionConnection:
    """Test Notion connection and authentication (post-#304 notion-client)."""

    def test_notion_adapter_initialization(self):
        """NotionMCPAdapter initializes with expected attributes."""
        adapter = NotionMCPAdapter()
        assert adapter.system_name == "notion_mcp"
        assert isinstance(adapter, BaseSpatialAdapter)
        # _notion_client attribute exists (may be None if NOTION_API_KEY not set,
        # or a Client instance if set — both valid post-init states).
        assert hasattr(adapter, "_notion_client")
        # is_configured method exists for config introspection.
        assert hasattr(adapter, "is_configured")

    @pytest.mark.asyncio
    async def test_test_connection_success(self):
        """test_connection() returns True when users.me() succeeds."""
        adapter = _adapter_with_mock_client()
        adapter._notion_client.users.me.return_value = {
            "id": "user-123",
            "name": "Test User",
            "type": "person",
        }

        result = await adapter.test_connection()

        assert result is True
        adapter._notion_client.users.me.assert_called_once()

    @pytest.mark.asyncio
    async def test_test_connection_failure_auth_error(self):
        """test_connection() returns False on APIResponseError (e.g. 401)."""
        adapter = _adapter_with_mock_client()
        mock_response = MagicMock()
        mock_response.status_code = 401
        adapter._notion_client.users.me.side_effect = APIResponseError(
            response=mock_response, message="Unauthorized", code="unauthorized"
        )

        result = await adapter.test_connection()

        assert result is False

    @pytest.mark.asyncio
    async def test_test_connection_failure_no_client(self):
        """test_connection() returns False when _notion_client is None."""
        with patch("services.mcp.consumer.notion_adapter.NotionConfig"):
            adapter = NotionMCPAdapter()
        adapter._notion_client = None

        result = await adapter.test_connection()

        assert result is False


# ---------------------------------------------------------------------------
# Spatial Dimension Analysis (unchanged across migration)
# ---------------------------------------------------------------------------


class TestNotionSpatialAnalysis:
    """Test Notion spatial dimension analysis.

    Preserved from pre-#304 test file — this surface (map_to_position) didn't
    change across the aiohttp→notion-client migration.
    """

    def test_spatial_position_mapping(self):
        """Test mapping Notion entities to spatial positions"""
        adapter = NotionMCPAdapter()
        context = {
            "territory_id": "workspace_123",
            "room_id": "database_456",
            "attention_level": "high",
            "navigation_intent": "explore",
        }

        position = adapter.map_to_position("db_123", context)

        assert position.position > 0
        assert position.context["external_id"] == "db_123"
        assert position.context["external_system"] == "notion_mcp"
        assert position.context["territory_id"] == "workspace_123"
        assert position.context["room_id"] == "database_456"

    def test_spatial_context_extraction(self):
        """Test extraction of spatial context from Notion data"""
        adapter = NotionMCPAdapter()
        notion_context = {
            "page_id": "page_789",
            "database_id": "db_456",
            "workspace_id": "workspace_123",
            "last_edited_time": "2025-08-12T12:00:00Z",
            "created_by": "user_123",
            "status": "in_progress",
        }

        position = adapter.map_to_position("page_789", notion_context)

        assert "spatial_context" in position.context
        assert position.context["page_id"] == "page_789"
        assert position.context["database_id"] == "db_456"
        assert position.context["workspace_id"] == "workspace_123"

    def test_multiple_entity_mapping(self):
        """Test mapping multiple Notion entities to spatial positions"""
        adapter = NotionMCPAdapter()

        entities = [
            ("db_1", {"territory_id": "ws_1", "room_id": "db_1"}),
            ("db_2", {"territory_id": "ws_1", "room_id": "db_2"}),
            ("page_1", {"territory_id": "ws_1", "room_id": "db_1", "path_id": "page_1"}),
        ]

        positions = []
        for entity_id, context in entities:
            position = adapter.map_to_position(entity_id, context)
            positions.append(position)

        # Verify unique positions assigned
        position_numbers = [p.position for p in positions]
        assert len(set(position_numbers)) == len(position_numbers)

        # Verify mappings stored
        stats = adapter.get_mapping_stats()
        assert stats["total_mappings"] == 3


# ---------------------------------------------------------------------------
# MCP Protocol — Database + Page Operations (post-#304 notion-client mocks)
# ---------------------------------------------------------------------------


class TestNotionMCPProtocol:
    """Test MCP protocol compliance via notion-client surface."""

    @pytest.mark.asyncio
    async def test_list_databases(self):
        """list_databases() returns the 'results' list from search()."""
        adapter = _adapter_with_mock_client()
        adapter._notion_client.search.return_value = {
            "results": [
                {
                    "id": "db_1",
                    "title": [{"plain_text": "Test Database"}],
                    "created_time": "2025-08-12T10:00:00Z",
                    "last_edited_time": "2025-08-12T12:00:00Z",
                    "url": "https://notion.so/db_1",
                }
            ]
        }

        databases = await adapter.list_databases()

        assert len(databases) == 1
        assert databases[0]["id"] == "db_1"
        adapter._notion_client.search.assert_called_once()

    @pytest.mark.asyncio
    async def test_list_databases_empty_results(self):
        """list_databases() returns [] when search returns no results."""
        adapter = _adapter_with_mock_client()
        adapter._notion_client.search.return_value = {"results": []}

        databases = await adapter.list_databases()

        assert databases == []

    @pytest.mark.asyncio
    async def test_list_databases_api_error_returns_empty(self):
        """list_databases() catches exceptions and returns [] (fail-graceful)."""
        adapter = _adapter_with_mock_client()
        mock_response = MagicMock()
        mock_response.status_code = 500
        adapter._notion_client.search.side_effect = APIResponseError(
            response=mock_response, message="Server error", code="server_error"
        )

        databases = await adapter.list_databases()

        assert databases == []

    @pytest.mark.asyncio
    async def test_get_page(self):
        """get_page() returns shaped page dict with title extracted."""
        adapter = _adapter_with_mock_client()
        adapter._notion_client.pages.retrieve.return_value = {
            "id": "page_1",
            "properties": {"title": {"title": [{"text": {"content": "Test Page"}}]}},
            "url": "https://notion.so/page_1",
            "created_time": "2025-08-12T10:00:00Z",
            "last_edited_time": "2025-08-12T12:00:00Z",
        }

        page = await adapter.get_page("page_1")

        assert page is not None
        assert page["id"] == "page_1"
        assert page["title"] == "Test Page"
        assert page["url"] == "https://notion.so/page_1"
        adapter._notion_client.pages.retrieve.assert_called_once_with(page_id="page_1")

    @pytest.mark.asyncio
    async def test_get_page_empty_page_id_returns_none(self):
        """get_page() returns None when page_id is empty."""
        adapter = _adapter_with_mock_client()

        result = await adapter.get_page("")

        assert result is None
        adapter._notion_client.pages.retrieve.assert_not_called()

    @pytest.mark.asyncio
    async def test_get_database_error_handling(self):
        """get_database() returns None on API error (fail-graceful)."""
        adapter = _adapter_with_mock_client()
        mock_response = MagicMock()
        mock_response.status_code = 401
        adapter._notion_client.databases.retrieve.side_effect = APIResponseError(
            response=mock_response, message="Unauthorized", code="unauthorized"
        )

        result = await adapter.get_database("db_1")

        assert result is None


# ---------------------------------------------------------------------------
# Full Integration — Workspace + Query
# ---------------------------------------------------------------------------


class TestNotionFullIntegration:
    """Test full Notion MCP+Spatial integration workflow."""

    @pytest.mark.asyncio
    async def test_workspace_integration_bot_user(self):
        """get_workspace_info() extracts workspace metadata from bot user response."""
        adapter = _adapter_with_mock_client()
        adapter._notion_client.users.me.return_value = {
            "id": "user_123",
            "name": "Test Bot",
            "type": "bot",
            "person": {"email": "test@example.com"},
            "bot": {"workspace": {"id": "ws_123", "name": "Test Workspace"}},
        }

        workspace_info = await adapter.get_workspace_info()

        assert workspace_info is not None
        assert workspace_info["workspace_id"] == "ws_123"
        assert workspace_info["workspace_name"] == "Test Workspace"
        assert workspace_info["user_email"] == "test@example.com"

        # Spatial mapping still works against workspace
        context = {
            "territory_id": workspace_info["workspace_id"],
            "room_id": "general",
            "attention_level": "medium",
            "navigation_intent": "monitor",
        }
        position = adapter.map_to_position(workspace_info["workspace_id"], context)
        assert position.context["territory_id"] == "ws_123"

    @pytest.mark.asyncio
    async def test_workspace_integration_error_returns_none(self):
        """get_workspace_info() returns None on API failure (fail-graceful)."""
        adapter = _adapter_with_mock_client()
        adapter._notion_client.users.me.side_effect = RequestTimeoutError("timeout")

        result = await adapter.get_workspace_info()

        assert result is None

    @pytest.mark.asyncio
    async def test_database_query_integration(self):
        """query_database() returns results list + spatial mapping works on results."""
        adapter = _adapter_with_mock_client()
        adapter._notion_client.databases.query.return_value = {
            "results": [
                {
                    "id": "page_1",
                    "properties": {
                        "Title": {"title": [{"plain_text": "Task 1"}]},
                        "Status": {"select": {"name": "In Progress"}},
                        "Priority": {"select": {"name": "High"}},
                    },
                    "created_time": "2025-08-12T10:00:00Z",
                    "last_edited_time": "2025-08-12T12:00:00Z",
                    "url": "https://notion.so/page_1",
                }
            ]
        }

        pages = await adapter.query_database(
            "db_1",
            filter_params={"Status": {"select": {"equals": "In Progress"}}},
        )

        assert len(pages) == 1
        assert pages[0]["id"] == "page_1"
        adapter._notion_client.databases.query.assert_called_once()

        # Spatial mapping of query results
        for page in pages:
            priority = page["properties"]["Priority"]["select"]["name"]
            context = {
                "territory_id": "ws_123",
                "room_id": "db_1",
                "path_id": page["id"],
                "attention_level": "high" if priority == "High" else "medium",
                "navigation_intent": "respond",
            }
            position = adapter.map_to_position(page["id"], context)
            assert position.context["path_id"] == page["id"]

    @pytest.mark.asyncio
    async def test_database_query_empty_database_id(self):
        """query_database() returns [] for empty database_id (defensive)."""
        adapter = _adapter_with_mock_client()

        pages = await adapter.query_database("")

        assert pages == []
        adapter._notion_client.databases.query.assert_not_called()
