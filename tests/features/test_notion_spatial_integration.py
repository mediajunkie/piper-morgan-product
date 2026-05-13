#!/usr/bin/env python3
"""
Test Notion MCP + Spatial Integration

Comprehensive TDD test suite for Notion integration with MCP+Spatial Intelligence.
Tests cover:
1. Connection and authentication
2. Spatial dimension analysis
3. MCP protocol compliance
4. Full integration workflow

This follows the TDD approach specified in the methodology.
"""

import asyncio
import os
import sys
from typing import Optional
from unittest.mock import AsyncMock, Mock, patch

import pytest

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from services.integrations.mcp.notion_adapter import NotionMCPAdapter
from services.integrations.spatial_adapter import BaseSpatialAdapter

# #1082 (#304 follow-up): The 9 tests in TestNotionConnection +
# TestNotionMCPProtocol + TestNotionFullIntegration target the OLD
# aiohttp-based adapter architecture (mock aiohttp.ClientSession, call
# removed configure_notion_api / _call_notion_api / _notion_token).
# The current adapter uses the notion-client library. Rewriting is
# tracked in #1082 (demand-gated — trigger is regression bug or coverage
# audit). TestNotionSpatialAnalysis still passes against the current
# code (it tests map_to_position which is unchanged).
_STALE_PRE_NOTION_CLIENT_REASON = (
    "Pre-#304 aiohttp architecture; rewrite tracked in #1082. "
    "New code path coverage at tests/unit/services/integrations/mcp/test_notion_adapter.py."
)


@pytest.mark.skip(reason=_STALE_PRE_NOTION_CLIENT_REASON)
class TestNotionConnection:
    """Test Notion connection and authentication"""

    def test_notion_adapter_initialization(self):
        """Test NotionMCPAdapter initializes correctly"""
        adapter = NotionMCPAdapter()
        assert adapter.system_name == "notion_mcp"
        assert isinstance(adapter, BaseSpatialAdapter)
        # Client may be initialized if NOTION_API_KEY is set
        assert hasattr(adapter, "_notion_client")
        # Configuration check works
        assert hasattr(adapter, "is_configured")

    @patch("aiohttp.ClientSession")
    async def test_notion_api_configuration(self, mock_session):
        """Test Notion API configuration"""
        adapter = NotionMCPAdapter()
        mock_session.return_value = AsyncMock()

        result = await adapter.configure_notion_api("test_token")

        assert result is True
        assert adapter._notion_token == "test_token"
        assert adapter._session is not None

    @patch("aiohttp.ClientSession")
    async def test_notion_connection_test_success(self, mock_session):
        """Test successful Notion connection"""
        adapter = NotionMCPAdapter()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"id": "test_user"})

        mock_session_instance = AsyncMock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        mock_session.return_value = mock_session_instance

        await adapter.configure_notion_api("test_token")
        result = await adapter.test_connection()

        assert result is True

    @patch("aiohttp.ClientSession")
    async def test_notion_connection_test_failure(self, mock_session):
        """Test failed Notion connection"""
        adapter = NotionMCPAdapter()
        mock_response = AsyncMock()
        mock_response.status = 401

        mock_session_instance = AsyncMock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        mock_session.return_value = mock_session_instance

        await adapter.configure_notion_api("test_token")
        result = await adapter.test_connection()

        assert result is False


class TestNotionSpatialAnalysis:
    """Test Notion spatial dimension analysis"""

    def test_spatial_position_mapping(self):
        """Test mapping Notion entities to spatial positions"""
        adapter = NotionMCPAdapter()

        # Test mapping a database
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

        # Test with Notion page context
        notion_context = {
            "page_id": "page_789",
            "database_id": "db_456",
            "workspace_id": "workspace_123",
            "last_edited_time": "2025-08-12T12:00:00Z",
            "created_by": "user_123",
            "status": "in_progress",
        }

        position = adapter.map_to_position("page_789", notion_context)

        # Verify spatial context is properly extracted
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


@pytest.mark.skip(reason=_STALE_PRE_NOTION_CLIENT_REASON)
class TestNotionMCPProtocol:
    """Test MCP protocol compliance"""

    @patch("aiohttp.ClientSession")
    async def test_notion_database_operations(self, mock_session):
        """Test Notion database CRUD operations"""
        adapter = NotionMCPAdapter()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
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
        )

        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_response
        mock_session.return_value = mock_session_instance

        await adapter.configure_notion_api("test_token")
        databases = await adapter.list_databases()

        assert len(databases) == 1
        assert databases[0]["id"] == "db_1"
        assert databases[0]["title"] == "Test Database"

    @patch("aiohttp.ClientSession")
    async def test_notion_page_operations(self, mock_session):
        """Test Notion page operations"""
        adapter = NotionMCPAdapter()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(
            return_value={
                "id": "page_1",
                "properties": {"title": {"title": [{"plain_text": "Test Page"}]}},
                "created_time": "2025-08-12T10:00:00Z",
                "last_edited_time": "2025-08-12T12:00:00Z",
                "url": "https://notion.so/page_1",
            }
        )

        mock_session_instance = AsyncMock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        mock_session.return_value = mock_session_instance

        await adapter.configure_notion_api("test_token")
        page = await adapter.get_page("page_1")

        assert page["id"] == "page_1"
        assert page["title"] == "Test Page"

    @patch("aiohttp.ClientSession")
    async def test_notion_rate_limiting(self, mock_session):
        """Test Notion API rate limiting compliance"""
        adapter = NotionMCPAdapter()
        mock_response = AsyncMock()
        mock_response.status = 200
        mock_response.json = AsyncMock(return_value={"id": "test"})

        mock_session_instance = AsyncMock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response
        mock_session.return_value = mock_session_instance

        await adapter.configure_notion_api("test_token")

        # Test rate limiting by timing multiple calls
        start_time = asyncio.get_event_loop().time()

        for _ in range(3):
            await adapter._call_notion_api("test_endpoint")

        end_time = asyncio.get_event_loop().time()
        elapsed_time = end_time - start_time

        # Should take at least 0.68 seconds due to rate limiting
        assert elapsed_time >= 0.6

    @patch("aiohttp.ClientSession")
    async def test_notion_error_handling(self, mock_session):
        """Test Notion error handling and graceful degradation"""
        adapter = NotionMCPAdapter()

        # Test 401 authentication error
        mock_response_401 = AsyncMock()
        mock_response_401.status = 401

        mock_session_instance = AsyncMock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_response_401
        mock_session.return_value = mock_session_instance

        await adapter.configure_notion_api("test_token")
        result = await adapter._call_notion_api("test_endpoint")

        assert result is None  # Should handle 401 gracefully

        # Test 429 rate limit error
        mock_response_429 = AsyncMock()
        mock_response_429.status = 429

        mock_session_instance.get.return_value.__aenter__.return_value = mock_response_429

        result = await adapter._call_notion_api("test_endpoint")
        assert result is None  # Should handle 429 gracefully


@pytest.mark.skip(reason=_STALE_PRE_NOTION_CLIENT_REASON)
class TestNotionFullIntegration:
    """Test full Notion MCP+Spatial integration workflow"""

    @patch("aiohttp.ClientSession")
    async def test_notion_workspace_integration(self, mock_session):
        """Test full workspace integration workflow"""
        adapter = NotionMCPAdapter()

        # Mock workspace info response
        mock_workspace_response = AsyncMock()
        mock_workspace_response.status = 200
        mock_workspace_response.json = AsyncMock(
            return_value={
                "id": "user_123",
                "name": "Test User",
                "person": {"email": "test@example.com"},
                "bot": {"workspace": {"id": "ws_123", "name": "Test Workspace"}},
            }
        )

        mock_session_instance = AsyncMock()
        mock_session_instance.get.return_value.__aenter__.return_value = mock_workspace_response
        mock_session.return_value = mock_session_instance

        await adapter.configure_notion_api("test_token")
        workspace_info = await adapter.get_workspace_info()

        assert workspace_info["workspace_id"] == "ws_123"
        assert workspace_info["workspace_name"] == "Test Workspace"
        assert workspace_info["user_email"] == "test@example.com"

        # Test spatial mapping of workspace
        context = {
            "territory_id": workspace_info["workspace_id"],
            "room_id": "general",
            "attention_level": "medium",
            "navigation_intent": "monitor",
        }

        position = adapter.map_to_position(workspace_info["workspace_id"], context)
        assert position.context["territory_id"] == "ws_123"

    @patch("aiohttp.ClientSession")
    async def test_notion_database_query_integration(self, mock_session):
        """Test database query with spatial mapping"""
        adapter = NotionMCPAdapter()

        # Mock database query response
        mock_query_response = AsyncMock()
        mock_query_response.status = 200
        mock_query_response.json = AsyncMock(
            return_value={
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
        )

        mock_session_instance = AsyncMock()
        mock_session_instance.post.return_value.__aenter__.return_value = mock_query_response
        mock_session.return_value = mock_session_instance

        await adapter.configure_notion_api("test_token")
        pages = await adapter.query_database(
            "db_1", {"Status": {"select": {"equals": "In Progress"}}}
        )

        assert len(pages) == 1
        assert pages[0]["title"] == "Task 1"
        assert pages[0]["properties"]["Status"]["select"]["name"] == "In Progress"

        # Test spatial mapping of query results
        for page in pages:
            context = {
                "territory_id": "ws_123",
                "room_id": "db_1",
                "path_id": page["id"],
                "attention_level": (
                    "high"
                    if page["properties"]["Priority"]["select"]["name"] == "High"
                    else "medium"
                ),
                "navigation_intent": "respond",
            }

            position = adapter.map_to_position(page["id"], context)
            assert position.context["path_id"] == page["id"]


async def run_all_tests():
    """Run all Notion integration tests"""
    print("🚀 Notion MCP + Spatial Integration Test Suite")
    print("=" * 60)

    test_classes = [
        TestNotionConnection,
        TestNotionSpatialAnalysis,
        TestNotionMCPProtocol,
        TestNotionFullIntegration,
    ]

    total_tests = 0
    passed_tests = 0

    for test_class in test_classes:
        print(f"\n📋 Testing {test_class.__name__}")
        print("-" * 40)

        test_instance = test_class()
        test_methods = [method for method in dir(test_instance) if method.startswith("test_")]

        for test_method in test_methods:
            total_tests += 1
            try:
                test_func = getattr(test_instance, test_method)
                if asyncio.iscoroutinefunction(test_func):
                    await test_func()
                else:
                    test_func()
                print(f"  ✅ {test_method}: PASSED")
                passed_tests += 1
            except Exception as e:
                print(f"  ❌ {test_method}: FAILED - {e}")

    print("\n" + "=" * 60)
    print("📊 Test Results Summary")
    print("=" * 60)
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    if passed_tests == total_tests:
        print("\n🎉 All tests passed! Notion MCP+Spatial integration is ready.")
        return True
    else:
        print(f"\n⚠️  {total_tests - passed_tests} tests failed. Review implementation.")
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(run_all_tests())
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⏹️  Test suite interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n💥 Test suite failed with unexpected error: {e}")
        sys.exit(1)
