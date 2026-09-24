"""
Notion Domain Service
Mediates all Notion MCP operations for the domain layer following DDD principles

Created: 2025-09-12 by Code Agent Step 5 - Domain Service Mediation Completion
Addresses architectural violation: Direct Notion MCP integration access from CLI and features layers
"""

from typing import Any, Dict, List, Optional

import structlog
from notion_client.errors import APIResponseError, RequestTimeoutError

from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

# Re-export exceptions for clean domain boundary
__all__ = ["NotionDomainService", "APIResponseError", "RequestTimeoutError"]

logger = structlog.get_logger()


class NotionDomainService:
    """
    Domain service for Notion MCP operations mediation

    Encapsulates Notion MCP integration access following DDD principles:
    - Mediates between application layer and Notion MCP integration layer
    - Provides clean domain interface for Notion operations
    - Handles Notion-specific error translation to domain exceptions
    - Manages Notion MCP adapter lifecycle and configuration
    """

    def __init__(self, notion_adapter: Optional[NotionIntegrationRouter] = None):
        """Initialize with optional Notion integration router injection"""
        try:
            self._notion_adapter = notion_adapter or NotionIntegrationRouter()
            logger.info(
                "Notion domain service initialized",
                adapter_type=type(self._notion_adapter).__name__,
            )
        except Exception as e:
            logger.error("Failed to initialize Notion domain service", error=str(e))
            raise

    # Connection and Configuration Operations

    async def connect(self, integration_token: Optional[str] = None) -> bool:
        """Connect to Notion for domain consumption"""
        try:
            return await self._notion_adapter.connect(integration_token)
        except APIResponseError as e:
            logger.error("Notion API error during connection", error=str(e))
            raise
        except RequestTimeoutError as e:
            logger.error("Notion request timeout during connection", error=str(e))
            raise
        except Exception as e:
            logger.error("Notion connection failed", error=str(e))
            raise

    async def test_connection(self) -> bool:
        """Test Notion connection for domain monitoring"""
        try:
            return await self._notion_adapter.test_connection()
        except APIResponseError as e:
            logger.error("Notion API error during connection test", error=str(e))
            return False
        except RequestTimeoutError as e:
            logger.error("Notion request timeout during connection test", error=str(e))
            return False
        except Exception as e:
            logger.error("Notion connection test failed", error=str(e))
            return False

    def is_configured(self) -> bool:
        """Check if Notion is configured for domain consumption"""
        try:
            return self._notion_adapter.is_configured()
        except Exception as e:
            logger.error("Notion configuration check failed", error=str(e))
            return False

    # Workspace Operations

    async def get_workspace_info(self) -> Optional[Dict[str, Any]]:
        """Get Notion workspace information for domain consumption"""
        try:
            return await self._notion_adapter.get_workspace_info()
        except APIResponseError as e:
            logger.error("Notion API error getting workspace info", error=str(e))
            return None
        except RequestTimeoutError as e:
            logger.error("Notion request timeout getting workspace info", error=str(e))
            return None
        except Exception as e:
            logger.error("Notion workspace info retrieval failed", error=str(e))
            return None

    # Database Operations

    async def list_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """List Notion databases for domain consumption"""
        try:
            return await self._notion_adapter.list_databases(page_size)
        except APIResponseError as e:
            logger.error("Notion API error listing databases", error=str(e))
            return []
        except RequestTimeoutError as e:
            logger.error("Notion request timeout listing databases", error=str(e))
            return []
        except Exception as e:
            logger.error("Notion database listing failed", error=str(e))
            return []

    async def get_database(self, database_id: str) -> Optional[Dict[str, Any]]:
        """Get Notion database for domain consumption"""
        try:
            return await self._notion_adapter.get_database(database_id)
        except APIResponseError as e:
            logger.error("Notion API error getting database", database_id=database_id, error=str(e))
            return None
        except RequestTimeoutError as e:
            logger.error(
                "Notion request timeout getting database", database_id=database_id, error=str(e)
            )
            return None
        except Exception as e:
            logger.error("Notion database retrieval failed", database_id=database_id, error=str(e))
            return None

    async def query_database(
        self,
        database_id: str,
        filter_condition: Optional[Dict] = None,
        sorts: Optional[List[Dict]] = None,
        page_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query Notion database for domain consumption"""
        try:
            return await self._notion_adapter.query_database(
                database_id, filter_condition, sorts, page_size
            )
        except APIResponseError as e:
            logger.error(
                "Notion API error querying database", database_id=database_id, error=str(e)
            )
            return []
        except RequestTimeoutError as e:
            logger.error(
                "Notion request timeout querying database", database_id=database_id, error=str(e)
            )
            return []
        except Exception as e:
            logger.error("Notion database query failed", database_id=database_id, error=str(e))
            return []

    # Page Operations

    async def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Get Notion page for domain consumption"""
        try:
            return await self._notion_adapter.get_page(page_id)
        except APIResponseError as e:
            logger.error("Notion API error getting page", page_id=page_id, error=str(e))
            return None
        except RequestTimeoutError as e:
            logger.error("Notion request timeout getting page", page_id=page_id, error=str(e))
            return None
        except Exception as e:
            logger.error("Notion page retrieval failed", page_id=page_id, error=str(e))
            return None

    async def get_page_blocks(self, page_id: str, page_size: int = 100) -> List[Dict[str, Any]]:
        """Get Notion page blocks for domain consumption"""
        try:
            return await self._notion_adapter.get_page_blocks(page_id, page_size)
        except APIResponseError as e:
            logger.error("Notion API error getting page blocks", page_id=page_id, error=str(e))
            return []
        except RequestTimeoutError as e:
            logger.error(
                "Notion request timeout getting page blocks", page_id=page_id, error=str(e)
            )
            return []
        except Exception as e:
            logger.error("Notion page blocks retrieval failed", page_id=page_id, error=str(e))
            return []

    async def update_page(self, page_id: str, properties: Dict) -> Optional[Dict[str, Any]]:
        """Update Notion page for domain consumption"""
        try:
            return await self._notion_adapter.update_page(page_id, properties)
        except APIResponseError as e:
            logger.error("Notion API error updating page", page_id=page_id, error=str(e))
            return None
        except RequestTimeoutError as e:
            logger.error("Notion request timeout updating page", page_id=page_id, error=str(e))
            return None
        except Exception as e:
            logger.error("Notion page update failed", page_id=page_id, error=str(e))
            return None

    async def create_page(
        self, parent_id: str, properties: Dict, content: Optional[List] = None
    ) -> Optional[Dict[str, Any]]:
        """Create Notion page for domain consumption"""
        try:
            return await self._notion_adapter.create_page(parent_id, properties, content)
        except APIResponseError as e:
            logger.error("Notion API error creating page", parent_id=parent_id, error=str(e))
            return None
        except RequestTimeoutError as e:
            logger.error("Notion request timeout creating page", parent_id=parent_id, error=str(e))
            return None
        except Exception as e:
            logger.error("Notion page creation failed", parent_id=parent_id, error=str(e))
            return None

    # Search Operations

    async def search_notion(
        self, query: str, filter_type: Optional[str] = None, page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Search Notion workspace for domain consumption.

        #1873: added to complete the mediation pattern every other operation on
        this class already follows -- the router
        (NotionIntegrationRouter.search_notion) has always had this method;
        this class simply never grew the passthrough, so
        cli/commands/notion.py's search/pages/create subcommands had nothing
        on this domain service to call (they referenced an unassigned
        `self.adapter` instead -- see notion.py's #1873 comment).
        """
        try:
            return await self._notion_adapter.search_notion(query, filter_type, page_size)
        except APIResponseError as e:
            logger.error("Notion API error searching workspace", query=query, error=str(e))
            return []
        except RequestTimeoutError as e:
            logger.error("Notion request timeout searching workspace", query=query, error=str(e))
            return []
        except Exception as e:
            logger.error("Notion workspace search failed", query=query, error=str(e))
            return []

    # Health and Status Operations

    def get_connection_status(self) -> Dict[str, Any]:
        """Get Notion connection status for domain monitoring"""
        try:
            configured = self.is_configured()

            return {
                "connected": configured,
                "configured": configured,
                "adapter_type": type(self._notion_adapter).__name__,
                "service_available": self._notion_adapter is not None,
            }
        except Exception as e:
            logger.error("Notion connection status check failed", error=str(e))
            return {"connected": False, "error": str(e)}
