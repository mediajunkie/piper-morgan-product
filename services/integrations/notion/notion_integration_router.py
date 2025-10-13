"""
NotionIntegrationRouter - Feature flag controlled access to Notion integrations

Provides unified interface for Notion operations with support for:
- Spatial intelligence (MCP-based NotionMCPAdapter with 22 complete methods)
- Legacy basic Notion operations (if future implementation exists)
- Feature flag control via USE_SPATIAL_NOTION

Architecture Decision: ADR-038 Notion Integration Router Pattern
Following pattern established in CalendarIntegrationRouter.
"""

import warnings
from typing import Any, Dict, List, Optional, Tuple

from services.infrastructure.config.feature_flags import FeatureFlags
from services.integrations.spatial_adapter import SpatialContext, SpatialPosition

from .config_service import NotionConfigService


class NotionIntegrationRouter:
    """
    Router for Notion integration with spatial/legacy delegation.

    Follows pattern established in CalendarIntegrationRouter.
    Delegates to NotionMCPAdapter (spatial) or future legacy implementation.

    Examples:
        # Basic usage with spatial intelligence
        router = NotionIntegrationRouter()
        await router.connect()
        databases = await router.list_databases()

        # Feature flag control
        # USE_SPATIAL_NOTION=true (default) - uses NotionMCPAdapter
        # USE_SPATIAL_NOTION=false - uses legacy if available, else raises error

    Architecture:
        - Spatial: NotionMCPAdapter with API token authentication and full CRUD
        - Legacy: Placeholder for future basic Notion implementation
        - Feature Flags: USE_SPATIAL_NOTION, ALLOW_LEGACY_NOTION
    """

    def __init__(self, config_service: Optional[NotionConfigService] = None):
        """Initialize router with feature flag checking and config service"""
        # Use FeatureFlags service for consistency with Calendar router
        self.use_spatial = FeatureFlags.should_use_spatial_notion()
        self.allow_legacy = FeatureFlags.is_legacy_notion_allowed()

        # Store config service for adapter initialization
        self.config_service = config_service

        # Initialize spatial integration
        self.spatial_notion = None
        if self.use_spatial:
            try:
                from services.integrations.mcp.notion_adapter import NotionMCPAdapter

                # Pass config to adapter if available
                if config_service:
                    self.spatial_notion = NotionMCPAdapter(config_service)
                else:
                    # Graceful degradation - adapter handles missing config
                    self.spatial_notion = NotionMCPAdapter()

            except ImportError as e:
                warnings.warn(f"Spatial Notion unavailable: {e}")

        # Initialize legacy integration (placeholder for future)
        self.legacy_notion = None
        if self.allow_legacy:
            # Future: Import legacy Notion client if exists
            # For now, no legacy implementation exists
            pass

    def _get_preferred_integration(self, operation: str) -> Tuple[Optional[Any], bool]:
        """
        Get preferred Notion integration based on feature flags and availability.

        Args:
            operation: Name of operation being performed

        Returns:
            Tuple of (integration_instance, is_legacy_used)
        """
        # Try spatial first if enabled
        if self.use_spatial and self.spatial_notion:
            return self.spatial_notion, False

        # Fall back to legacy if allowed (future implementation)
        elif self.allow_legacy and self.legacy_notion:
            return self.legacy_notion, True

        # No integration available
        else:
            return None, False

    def _warn_deprecation_if_needed(self, operation: str, is_legacy: bool):
        """Issue deprecation warnings when legacy integration is used"""
        if is_legacy:
            warnings.warn(
                f"Using legacy Notion for {operation}. "
                "Consider enabling USE_SPATIAL_NOTION=true for spatial intelligence.",
                DeprecationWarning,
                stacklevel=3,
            )

    # Connection methods

    async def connect(self, integration_token: Optional[str] = None) -> bool:
        """
        Connect to Notion API with optional integration token.

        Args:
            integration_token: Optional Notion integration token

        Returns:
            bool: True if connection successful, False otherwise

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("connect")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("connect", is_legacy)
            return await integration.connect(integration_token)
        else:
            raise RuntimeError(
                "No Notion integration available for connect. "
                "Enable USE_SPATIAL_NOTION=true or check NotionMCPAdapter setup."
            )

    async def test_connection(self) -> bool:
        """
        Test Notion API connection.

        Returns:
            bool: True if connection test successful, False otherwise

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("test_connection")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("test_connection", is_legacy)
            return await integration.test_connection()
        else:
            raise RuntimeError("No Notion integration available for test_connection")

    def is_configured(self) -> bool:
        """
        Check if Notion integration is configured.

        Returns:
            bool: True if Notion is configured, False otherwise

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("is_configured")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("is_configured", is_legacy)
            return integration.is_configured()
        else:
            raise RuntimeError("No Notion integration available for is_configured")

    # Workspace methods

    async def get_workspace_info(self) -> Optional[Dict[str, Any]]:
        """
        Get Notion workspace information.

        Returns:
            Optional[Dict[str, Any]]: Workspace information or None

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_workspace_info")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_workspace_info", is_legacy)
            return await integration.get_workspace_info()
        else:
            raise RuntimeError("No Notion integration available for get_workspace_info")

    async def list_users(self) -> List[Dict[str, Any]]:
        """
        List users in Notion workspace.

        Returns:
            List[Dict[str, Any]]: List of workspace users

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("list_users")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("list_users", is_legacy)
            return await integration.list_users()
        else:
            raise RuntimeError("No Notion integration available for list_users")

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific user information.

        Args:
            user_id: Notion user ID

        Returns:
            Optional[Dict[str, Any]]: User information or None

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_user")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_user", is_legacy)
            return await integration.get_user(user_id)
        else:
            raise RuntimeError("No Notion integration available for get_user")

    # Database methods

    async def fetch_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """
        Fetch all accessible databases.

        Args:
            page_size: Number of databases to fetch per page

        Returns:
            List[Dict[str, Any]]: List of accessible databases

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("fetch_databases")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("fetch_databases", is_legacy)
            return await integration.fetch_databases(page_size)
        else:
            raise RuntimeError("No Notion integration available for fetch_databases")

    async def list_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """
        List databases (alias for fetch_databases).

        Args:
            page_size: Number of databases to fetch per page

        Returns:
            List[Dict[str, Any]]: List of accessible databases

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("list_databases")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("list_databases", is_legacy)
            return await integration.list_databases(page_size)
        else:
            raise RuntimeError("No Notion integration available for list_databases")

    async def get_database(self, database_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific database.

        Args:
            database_id: Notion database ID

        Returns:
            Optional[Dict[str, Any]]: Database information or None

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_database")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_database", is_legacy)
            return await integration.get_database(database_id)
        else:
            raise RuntimeError("No Notion integration available for get_database")

    async def query_database(
        self,
        database_id: str,
        filter_params: Optional[Dict] = None,
        sorts: Optional[List] = None,
        page_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """
        Query database with filters and sorting.

        Args:
            database_id: Notion database ID
            filter_params: Optional filter parameters
            sorts: Optional sort parameters
            page_size: Number of items to fetch per page

        Returns:
            List[Dict[str, Any]]: Query results

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("query_database")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("query_database", is_legacy)
            return await integration.query_database(database_id, filter_params, sorts, page_size)
        else:
            raise RuntimeError("No Notion integration available for query_database")

    # Page methods

    async def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """
        Get specific page.

        Args:
            page_id: Notion page ID

        Returns:
            Optional[Dict[str, Any]]: Page information or None

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_page")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_page", is_legacy)
            return await integration.get_page(page_id)
        else:
            raise RuntimeError("No Notion integration available for get_page")

    async def get_page_blocks(self, page_id: str, page_size: int = 100) -> List[Dict[str, Any]]:
        """
        Get blocks from a page.

        Args:
            page_id: Notion page ID
            page_size: Number of blocks to fetch per page

        Returns:
            List[Dict[str, Any]]: List of page blocks

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_page_blocks")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_page_blocks", is_legacy)
            return await integration.get_page_blocks(page_id, page_size)
        else:
            raise RuntimeError("No Notion integration available for get_page_blocks")

    async def update_page(self, page_id: str, properties: Dict) -> Dict[str, Any]:
        """
        Update page properties.

        Args:
            page_id: Notion page ID
            properties: Properties to update

        Returns:
            Dict[str, Any]: Updated page information

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("update_page")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("update_page", is_legacy)
            return await integration.update_page(page_id, properties)
        else:
            raise RuntimeError("No Notion integration available for update_page")

    async def create_page(
        self, parent_id: str, properties: Dict, content: Optional[List] = None
    ) -> Dict[str, Any]:
        """
        Create new page.

        Args:
            parent_id: Parent page or database ID
            properties: Page properties
            content: Optional page content blocks

        Returns:
            Dict[str, Any]: Created page information

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("create_page")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("create_page", is_legacy)
            return await integration.create_page(parent_id, properties, content)
        else:
            raise RuntimeError("No Notion integration available for create_page")

    # Item methods

    async def create_database_item(
        self, database_id: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create item in database.

        Args:
            database_id: Notion database ID
            properties: Item properties

        Returns:
            Dict[str, Any]: Created item information

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("create_database_item")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("create_database_item", is_legacy)
            return await integration.create_database_item(database_id, properties)
        else:
            raise RuntimeError("No Notion integration available for create_database_item")

    # Search methods

    async def search_notion(
        self, query: str, filter_type: Optional[str] = None, page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """
        Search Notion workspace.

        Args:
            query: Search query string
            filter_type: Optional filter type
            page_size: Number of results to fetch per page

        Returns:
            List[Dict[str, Any]]: Search results

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("search_notion")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("search_notion", is_legacy)
            return await integration.search_notion(query, filter_type, page_size)
        else:
            raise RuntimeError("No Notion integration available for search_notion")

    # Spatial intelligence methods (BaseSpatialAdapter delegation)

    def map_to_position(self, external_id: str, context: Dict[str, Any]) -> SpatialPosition:
        """
        Map external Notion ID to spatial position.

        Args:
            external_id: Notion page/database/block ID
            context: Additional context for spatial mapping

        Returns:
            SpatialPosition with spatial intelligence mapping

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("map_to_position")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("map_to_position", is_legacy)
            return integration.map_to_position(external_id, context)
        else:
            raise RuntimeError("No Notion integration available for map_to_position")

    def map_from_position(self, position) -> Optional[str]:
        """
        Map spatial position back to external Notion ID.

        Args:
            position: SpatialPosition to reverse map

        Returns:
            Optional[str]: Notion ID if mapping exists, None otherwise

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("map_from_position")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("map_from_position", is_legacy)
            return integration.map_from_position(position)
        else:
            raise RuntimeError("No Notion integration available for map_from_position")

    def store_mapping(self, external_id: str, position) -> bool:
        """
        Store mapping between external Notion ID and spatial position.

        Args:
            external_id: Notion page/database/block ID
            position: SpatialPosition to map to

        Returns:
            bool: True if mapping stored successfully, False otherwise

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("store_mapping")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("store_mapping", is_legacy)
            return integration.store_mapping(external_id, position)
        else:
            raise RuntimeError("No Notion integration available for store_mapping")

    def get_context(self, external_id: str) -> Optional[SpatialContext]:
        """
        Get spatial context for external Notion ID.

        Args:
            external_id: Notion page/database/block ID

        Returns:
            Optional[SpatialContext]: Spatial context if mapping exists, None otherwise

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_context")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_context", is_legacy)
            return integration.get_context(external_id)
        else:
            raise RuntimeError("No Notion integration available for get_context")

    # Utility methods

    def get_mapping_stats(self) -> Dict[str, Any]:
        """
        Get spatial mapping statistics.

        Returns:
            Dict[str, Any]: Mapping statistics

        Raises:
            RuntimeError: If no Notion integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_mapping_stats")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_mapping_stats", is_legacy)
            return integration.get_mapping_stats()
        else:
            raise RuntimeError("No Notion integration available for get_mapping_stats")

    async def close(self) -> None:
        """
        Close Notion connection.

        Note: No error if no integration - closing is optional.
        """
        integration, is_legacy = self._get_preferred_integration("close")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("close", is_legacy)
            await integration.close()
        # No error if no integration - closing is optional

    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get current integration status for monitoring and debugging.

        Returns:
            Dict[str, Any]: Router status including feature flags and available integrations
        """
        integration, is_legacy = self._get_preferred_integration("get_integration_status")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_integration_status", is_legacy)
            # Get status from integration if it supports it, otherwise return router status
            if hasattr(integration, "get_integration_status"):
                return integration.get_integration_status()
            else:
                # Fallback to router-level status
                return {
                    "router_initialized": True,
                    "using_spatial": not is_legacy,
                    "using_legacy": is_legacy,
                    "integration_type": type(integration).__name__,
                    "feature_flags": {
                        "use_spatial": self.use_spatial,
                        "allow_legacy": self.allow_legacy,
                    },
                }
        else:
            return {
                "router_initialized": True,
                "using_spatial": False,
                "using_legacy": False,
                "integration_type": None,
                "error": "No Notion integration available",
                "feature_flags": {
                    "use_spatial": self.use_spatial,
                    "allow_legacy": self.allow_legacy,
                },
            }


# Convenience factory function
def create_notion_integration() -> NotionIntegrationRouter:
    """
    Factory function to create NotionIntegrationRouter instance.

    Returns:
        NotionIntegrationRouter: Configured router instance
    """
    return NotionIntegrationRouter()
