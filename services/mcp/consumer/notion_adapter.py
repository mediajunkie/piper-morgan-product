"""Notion — the #1232 Connector-contract home (ADR-070 D5).

Per Arch's 2026-07-04 3-layer connector-alignment ruling: the #1232 interface
(`connect`/`status`/`resolve`/`degrade`) is Layer 1 -- no exceptions. Notion's
credential backend (Layer 2) is the per-user keychain entry `NotionConfigService`
already reads (`keychain.get_api_key("notion", username=user_id)`, ADR-058) -- a
keychain-backed connector conforms to the contract the same as a binding-table
one; the credential model is below the interface, not a contract variant.

Consolidated here (2026-07-04) per Arch's follow-through on the reference-port
review: this class was originally a subclass of
`services.integrations.mcp.notion_adapter.NotionMCPAdapter`, inheriting its 22
data-operation methods (get_page, search_notion, query_database, etc.) rather
than duplicating them. Closing the "single canonical adapter" invariant (the
same one the GitBook duplicate-adapter finding named) means this IS now that
canonical adapter -- the legacy module's own class body moved here verbatim
(no behavior changes), and the legacy module is now a thin re-export so the
~20 existing callers (production + the full test suite + debug/manual
scripts) keep working with zero changes to their own code.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Dict, List, Optional

import aiohttp
from notion_client import Client
from notion_client.client import ClientOptions
from notion_client.errors import APIResponseError, RequestTimeoutError

from config.notion_config import NotionConfig
from services.integrations.mcp.token_counter import TokenCounter
from services.integrations.notion.config_service import NotionConfigService
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

from .connector import (
    Binding,
    ConnectorStatus,
    ConnectorStatusState,
    ConnectRequired,
    ConnectResult,
    DegradationReason,
    DegradationResponse,
    ResolveMiss,
    ResolveResult,
    ResourceQuery,
)

logger = logging.getLogger(__name__)


class NotionMCPAdapter(BaseSpatialAdapter):
    
    """
    Notion MCP spatial adapter implementation.

    Maps Notion page and database IDs to spatial positions using MCP protocol
    for external service integration.
    """

    def __init__(self, config_service: Optional["NotionConfigService"] = None):
        super().__init__("notion_mcp")
        self._lock = asyncio.Lock()
        self._page_to_position: Dict[str, int] = {}
        self._position_to_page: Dict[int, str] = {}
        self._context_storage: Dict[str, Dict[str, Any]] = {}

        # Token counting for MCP operations (Issue #306)
        self.token_counter = TokenCounter()

        # Notion client configuration with service injection pattern
        # Note: We use lazy config loading - don't call get_config() here because
        # at startup time there's no user context. Config is loaded when needed.
        # Issue #781: Fixed crash from calling get_config() without user_id
        self.config_service = config_service
        self.config = None  # Lazy load when user context available
        if not config_service:
            # Fallback to static config for backward compatibility (no user context)
            self.config = NotionConfig()

        self._notion_client: Optional[Client] = None
        self._session: Optional[aiohttp.ClientSession] = None

        # Initialize client if configuration is available
        self._initialize_client()

        logger.info(
            "NotionMCPAdapter initialized with %s",
            "service injection" if config_service else "static config",
        )

    def _initialize_client(self):
        """Initialize Notion client with configuration."""
        try:
            # Skip initialization if config not yet loaded (lazy loading)
            if self.config is None:
                logger.debug("Skipping client init - config not loaded (lazy loading)")
                return
            api_key = self.config.get_api_key()
            if api_key:
                # Use API version 2025-09-03 with ClientOptions
                options = ClientOptions(auth=api_key, notion_version="2025-09-03")
                self._notion_client = Client(options=options)
                logger.info("Notion client initialized with API version 2025-09-03")
            else:
                logger.warning("NOTION_API_KEY not set - client will be initialized later")
        except Exception as e:
            logger.error(f"Error initializing Notion client: {e}")

    async def connect_with_token(self, integration_token: Optional[str] = None) -> bool:
        """Connect to Notion with integration token.

        Renamed from `connect` (2026-07-04): the #1232 Connector contract's
        `connect(user_id) -> ConnectResult` now owns that name on
        `services.mcp.consumer.notion_adapter.NotionMCPAdapter` (the subclass
        that adds the 4 contract methods on top of this class, unchanged).
        This method's own behavior is identical to before the rename.
        """
        try:
            if integration_token:
                # Initialize with provided token using API version 2025-09-03
                options = ClientOptions(auth=integration_token, notion_version="2025-09-03")
                self._notion_client = Client(options=options)
            elif not self._notion_client:
                # Try to initialize from configuration
                api_key = self.config.get_api_key()
                if api_key:
                    options = ClientOptions(auth=api_key, notion_version="2025-09-03")
                    self._notion_client = Client(options=options)
                else:
                    logger.error("No Notion API key available")
                    return False

            # Test connection
            return await self.test_connection()

        except Exception as e:
            logger.error(f"Error connecting to Notion: {e}")
            return False

    async def test_connection(self) -> bool:
        """Test Notion API connection and authentication"""
        try:
            if not self._notion_client:
                logger.error("Notion client not initialized")
                return False

            # Test with a simple API call to retrieve user info
            try:
                user_info = self._notion_client.users.me()
                logger.info(
                    f"Notion API connection successful - User: {user_info.get('name', 'Unknown')}"
                )
                return True
            except APIResponseError as e:
                logger.error(f"Notion API authentication failed: {e}")
                return False
            except RequestTimeoutError as e:
                logger.error(f"Notion API request timeout: {e}")
                return False

        except Exception as e:
            logger.error(f"Error testing Notion connection: {e}")
            return False

    def is_configured(self) -> bool:
        """Check if Notion adapter is properly configured."""
        return self.config.validate_config() and self._notion_client is not None

    async def get_workspace_info(self) -> Optional[Dict[str, Any]]:
        """Get Notion workspace information using notion_client"""
        try:
            # Note: Notion doesn't have a direct workspace endpoint
            # We'll use the user info as a proxy for workspace access
            user_info = self._notion_client.users.me()
            if user_info:
                return {
                    "workspace_id": user_info.get("bot", {}).get("workspace", {}).get("id"),
                    "workspace_name": user_info.get("bot", {}).get("workspace", {}).get("name"),
                    "user_id": user_info.get("id"),
                    "user_name": user_info.get("name"),
                    "user_email": user_info.get("person", {}).get("email"),
                }
            return None

        except Exception as e:
            logger.error(f"Error getting workspace info: {e}")
            return None

    async def get_current_user(self) -> Optional[Dict[str, Any]]:
        """
        Get current authenticated Notion user.

        Retrieves information about the user associated with the API token.
        Used by enhanced validation in configuration loader to verify API connectivity.

        Returns:
            Dict with user information:
            {
                "id": str,          # User ID
                "name": str,        # User name
                "email": str,       # User email (if person)
                "type": str,        # "person" or "bot"
                "workspace": {      # Workspace info (if bot)
                    "id": str,
                    "name": str
                }
            }
            Returns None if not authenticated or connection fails.

        Raises:
            APIResponseError: If Notion API returns an error
            RequestTimeoutError: If API request times out

        Example:
            >>> adapter = NotionMCPAdapter()
            >>> await adapter.connect_with_token()
            >>> user = await adapter.get_current_user()
            >>> print(f"Authenticated as: {user['name']}")
        """
        try:
            if not self._notion_client:
                logger.error("Notion client not initialized")
                return None

            # Get current user info from Notion API
            # Uses same pattern as test_connection() and get_workspace_info()
            user_info = self._notion_client.users.me()

            if not user_info:
                logger.warning("Notion API returned empty user info")
                return None

            # Extract and normalize user information
            result = {
                "id": user_info.get("id"),
                "name": user_info.get("name"),
                "type": user_info.get("type"),
            }

            # Add email for person users
            if user_info.get("person"):
                result["email"] = user_info.get("person", {}).get("email")

            # Add workspace info for bot users
            if user_info.get("bot"):
                result["workspace"] = {
                    "id": user_info.get("bot", {}).get("workspace", {}).get("id"),
                    "name": user_info.get("bot", {}).get("workspace", {}).get("name"),
                }

            logger.info(f"Retrieved current user: {result.get('name')} ({result.get('id')})")
            return result

        except APIResponseError as e:
            logger.error(f"Notion API error getting current user: {e}")
            raise
        except RequestTimeoutError as e:
            logger.error(f"Notion API timeout getting current user: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting current user: {e}")
            return None

    async def fetch_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """Fetch accessible Notion databases (alias for list_databases)"""
        return await self.list_databases(page_size)

    async def list_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """List all databases using notion_client (with token counting)"""
        try:
            # Wrap with token counting (Issue #306)
            async def _fetch_databases():
                response = self._notion_client.search(
                    filter={"property": "object", "value": "database"},
                    page_size=min(page_size, 100),
                )
                databases = []
                if response and "results" in response:
                    databases = response["results"]
                return databases

            databases = await self.token_counter.wrap_mcp_call(
                "notion_list_databases",
                _fetch_databases(),
                input_data=f"page_size={page_size}",
            )

            logger.info(f"Found {len(databases)} databases")
            return databases

        except Exception as e:
            logger.error(f"Failed to list databases: {e}")
            return []

    async def get_database(self, database_id: str) -> Optional[Dict[str, Any]]:
        """Get specific database using notion_client (with token counting)"""
        try:
            if not database_id:
                logger.error("database_id is required")
                return None

            # Wrap with token counting (Issue #306 Phase 2)
            async def _get():
                # Retrieve database using notion_client
                response = self._notion_client.databases.retrieve(database_id=database_id)
                return response

            response = await self.token_counter.wrap_mcp_call(
                "notion_get_database",
                _get(),
                input_data=f"database_id={database_id}",
            )

            logger.info(f"Retrieved database: {database_id}")
            return response

        except Exception as e:
            logger.error(f"Failed to get database: {e}")
            return None

    async def get_data_source_id(self, database_id: str) -> Optional[str]:
        """
        Get the primary data_source_id for a Notion database.

        Required for Notion API version 2025-09-03 which separates databases from data sources.
        For single-source databases, returns the first (and only) data source ID.
        For multi-source databases, returns the primary data source ID.

        Args:
            database_id: The Notion database ID to get the data source for

        Returns:
            str: The data_source_id if found
            None: If database not found or has no data sources

        Raises:
            ValueError: If database_id is empty or database not found
            APIResponseError: If Notion API returns an error
            RequestTimeoutError: If API request times out

        Example:
            >>> adapter = NotionMCPAdapter()
            >>> await adapter.connect_with_token()
            >>> data_source_id = await adapter.get_data_source_id("25e11704d8bf80deaac2f806390fe7da")
            >>> print(f"Data source: {data_source_id}")

        Note:
            This method is required for API version 2025-09-03 which requires data_source_id
            instead of database_id for certain operations like creating pages in databases.
        """
        try:
            if not database_id:
                raise ValueError("database_id is required")

            if not self._notion_client:
                logger.error("Notion client not initialized")
                return None

            # Retrieve database metadata to get data_sources list
            try:
                db_info = self._notion_client.databases.retrieve(database_id=database_id)
            except APIResponseError as e:
                logger.error(f"Failed to retrieve database {database_id}: {e}")
                raise ValueError(
                    f"Cannot get data_source_id for database '{database_id}': Database not found or not accessible\n"
                    f"Error: {str(e)}\n"
                    f"Options:\n"
                    f"  1. Use 'piper notion databases' to see available databases\n"
                    f"  2. Check database permissions in Notion\n"
                    f"  3. Verify database ID is correct"
                )
            except RequestTimeoutError as e:
                logger.error(f"Timeout retrieving database {database_id}: {e}")
                raise

            # Extract data_sources list from database info
            data_sources = db_info.get("data_sources", [])

            if not data_sources:
                logger.warning(
                    f"Database {database_id} has no data sources listed. "
                    f"This may indicate the workspace hasn't migrated to API version 2025-09-03 yet."
                )
                return None

            # For single-source databases (most common), return the first data source
            # For multi-source databases, return the first (primary) data source
            primary_data_source = data_sources[0]
            data_source_id = primary_data_source.get("id")

            if not data_source_id:
                logger.error(f"Data source entry missing 'id' field: {primary_data_source}")
                return None

            logger.info(
                f"Retrieved data_source_id for database {database_id}: {data_source_id} "
                f"({len(data_sources)} total data sources)"
            )
            return data_source_id

        except (ValueError, APIResponseError, RequestTimeoutError):
            # Re-raise expected exceptions
            raise
        except Exception as e:
            logger.error(f"Unexpected error getting data_source_id: {e}")
            return None

    async def query_database(
        self,
        database_id: str,
        filter_params: Optional[Dict] = None,
        sorts: Optional[List] = None,
        page_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query database using notion_client (with token counting)"""
        try:
            if not database_id:
                logger.error("database_id is required")
                return []

            # Wrap with token counting (Issue #306)
            async def _query():
                # Build query parameters
                query_params = {"database_id": database_id, "page_size": min(page_size, 100)}

                if filter_params:
                    query_params["filter"] = filter_params

                if sorts:
                    query_params["sorts"] = sorts

                # Query database using notion_client
                response = self._notion_client.databases.query(**query_params)

                results = []
                if response and "results" in response:
                    results = response["results"]
                return results

            results = await self.token_counter.wrap_mcp_call(
                "notion_query_database",
                _query(),
                input_data=str(
                    {"database_id": database_id, "filter": filter_params, "page_size": page_size}
                ),
            )

            logger.info(f"Query returned {len(results)} results from database: {database_id}")
            return results

        except Exception as e:
            logger.error(f"Failed to query database: {e}")
            return []

    async def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Get specific page content and properties using notion_client (with token counting)"""
        try:
            if not page_id:
                logger.error("page_id is required for page retrieval")
                return None

            # Wrap with token counting (Issue #306)
            async def _get():
                # Retrieve page using notion_client
                response = self._notion_client.pages.retrieve(page_id=page_id)

                # Extract title safely
                title = "Untitled"
                if "properties" in response and "title" in response["properties"]:
                    title_prop = response["properties"]["title"]
                    if "title" in title_prop and len(title_prop["title"]) > 0:
                        title = title_prop["title"][0]["text"]["content"]

                return {
                    "id": response["id"],
                    "title": title,
                    "url": response.get("url"),
                    "properties": response.get("properties", {}),
                    "created_time": response.get("created_time"),
                    "last_edited_time": response.get("last_edited_time"),
                }

            page_data = await self.token_counter.wrap_mcp_call(
                "notion_get_page",
                _get(),
                input_data=f"page_id={page_id}",
            )

            return page_data

        except Exception as e:
            logger.error(f"Failed to get page: {e}")
            return None

    async def get_page_blocks(self, page_id: str, page_size: int = 100) -> List[Dict[str, Any]]:
        """Get page content blocks using notion_client (with token counting)"""
        try:
            if not page_id:
                logger.error("page_id is required")
                return []

            # Wrap with token counting (Issue #306 Phase 2)
            async def _get():
                # Get blocks using notion_client
                response = self._notion_client.blocks.children.list(
                    block_id=page_id, page_size=min(page_size, 100)
                )

                blocks = []
                if response and "results" in response:
                    for block in response["results"]:
                        blocks.append(block)
                return blocks

            blocks = await self.token_counter.wrap_mcp_call(
                "notion_get_page_blocks",
                _get(),
                input_data=f"page_id={page_id},page_size={page_size}",
            )

            return blocks

        except Exception as e:
            logger.error(f"Failed to get blocks: {e}")
            return []

    async def update_page(self, page_id: str, properties: Dict):
        """Update a Notion page using notion_client (with token counting)"""
        try:
            if not page_id:
                logger.error("page_id is required for page update")
                return None

            # Wrap with token counting (Issue #306 Phase 2)
            async def _update():
                # Update page using notion_client
                response = self._notion_client.pages.update(page_id=page_id, properties=properties)
                return response

            response = await self.token_counter.wrap_mcp_call(
                "notion_update_page",
                _update(),
                input_data=str({"page_id": page_id, "properties_count": len(properties)}),
            )

            logger.info(f"Page updated successfully: {page_id}")
            return response

        except Exception as e:
            logger.error(f"Failed to update page: {e}")
            return None

    async def append_blocks(self, page_id: str, blocks: List[Dict[str, Any]]):
        """Append content blocks to a Notion page using notion_client.

        Added 2026-05-18 (#1080 V1 — Pattern-073 instance 12 closure). The
        previous `_handle_update_document_notion` handler called `update_page`
        with empty properties and asserted "Updated X" — false. This method
        is the actual mechanism for "append content to a doc" semantics.

        Wraps `blocks.children.append` per Notion's data model: a page has
        properties (metadata) and child blocks (content). For "update doc
        with new content" semantics, appending blocks is the natural move.

        Args:
            page_id: Notion page ID (the parent block)
            blocks: List of block dicts following Notion's block schema
                    (e.g., [{"object": "block", "type": "paragraph",
                             "paragraph": {"rich_text": [...]}}])

        Returns:
            Response dict from Notion API on success, None on error.
        """
        try:
            if not page_id:
                logger.error("page_id is required for append_blocks")
                return None
            if not blocks:
                logger.warning("append_blocks called with empty blocks list — no-op")
                return None

            async def _append():
                response = self._notion_client.blocks.children.append(
                    block_id=page_id, children=blocks
                )
                return response

            response = await self.token_counter.wrap_mcp_call(
                "notion_append_blocks",
                _append(),
                input_data=str({"page_id": page_id, "block_count": len(blocks)}),
            )

            logger.info(f"Appended {len(blocks)} block(s) to page: {page_id}")
            return response

        except Exception as e:
            logger.error(f"Failed to append blocks: {e}")
            return None

    async def create_page(self, parent_id: str, properties: Dict, content: Optional[List] = None):
        """Create a new Notion page using notion_client (with token counting)"""
        try:
            if not parent_id:
                raise ValueError("parent_id is required for page creation")

            # Validate parent exists first
            parent_validation = await self._validate_parent_exists(parent_id)

            # Wrap with token counting (Issue #306)
            async def _create():
                # Chunk content if too large (Notion limit is 100 blocks)
                initial_content = []
                remaining_content = []

                if content and len(content) > 100:
                    initial_content = content[:100]
                    remaining_content = content[100:]
                    logger.info(
                        f"Content chunked: {len(initial_content)} initial blocks, {len(remaining_content)} remaining"
                    )
                else:
                    initial_content = content if content else []

                # Create page with first 100 blocks
                response = self._notion_client.pages.create(
                    parent={"page_id": parent_id}, properties=properties, children=initial_content
                )

                # Add remaining blocks if any
                if remaining_content and response:
                    page_id = response["id"]
                    # Notion requires adding additional blocks via the blocks endpoint
                    self._notion_client.blocks.children.append(
                        block_id=page_id, children=remaining_content
                    )
                    logger.info(
                        f"Added {len(remaining_content)} additional blocks to page {page_id}"
                    )

                # CRITICAL: Ensure URL is in response for publisher consumption
                if response and "id" in response:
                    # Notion API response already includes 'url' field, but ensure it's present
                    if "url" not in response or not response["url"]:
                        # Fallback: construct URL from page ID if missing
                        page_id = response["id"].replace("-", "")
                        response["url"] = f"https://www.notion.so/{page_id}"

                    logger.info(f"Page created successfully: {response['url']}")
                else:
                    logger.error(f"Notion API response missing required fields: {response}")
                    raise ValueError("Notion API did not return valid page response")

                return response

            response = await self.token_counter.wrap_mcp_call(
                "notion_create_page",
                _create(),
                input_data=str(
                    {
                        "parent_id": parent_id,
                        "properties_count": len(properties),
                        "content_blocks": len(content) if content else 0,
                    }
                ),
            )

            return response  # Must include 'url' field

        except Exception as e:
            logger.error(f"Failed to create page: {e}")
            raise

    async def create_database_item(
        self, database_id: str, properties: Dict, content: Optional[List] = None
    ):
        """Create a new database item using notion_client with API version 2025-09-03 support (with token counting)"""
        try:
            if not database_id:
                raise ValueError("database_id is required for database item creation")

            # Validate database exists and get data_source_id for API 2025-09-03
            try:
                self._notion_client.databases.retrieve(database_id=database_id)
            except Exception as e:
                raise ValueError(
                    f"Cannot create item in database '{database_id}': Database not found or not accessible\n"
                    f"Error: {str(e)}\n"
                    f"Options:\n"
                    f"  1. Use 'piper notion databases' to see available databases\n"
                    f"  2. Check database permissions in Notion\n"
                    f"  3. Verify database ID is correct"
                )

            # Get data_source_id for API version 2025-09-03
            # This is required for the new API format that separates databases from data sources
            try:
                data_source_id = await self.get_data_source_id(database_id)
                if data_source_id:
                    logger.info(
                        f"Using data_source_id: {data_source_id} for database: {database_id}"
                    )
                else:
                    # Fallback: workspace may not have multi-source enabled yet
                    # API will accept database_id format for backward compatibility
                    logger.info(f"No data_source_id available, using database_id format")
                    data_source_id = None
            except Exception as e:
                # If get_data_source_id fails, log warning and continue with database_id format
                logger.warning(f"Could not get data_source_id: {e}. Using database_id format.")
                data_source_id = None

            # Wrap with token counting (Issue #306)
            async def _create():
                # Chunk content if too large (Notion limit is 100 blocks)
                initial_content = []
                remaining_content = []

                if content and len(content) > 100:
                    initial_content = content[:100]
                    remaining_content = content[100:]
                    logger.info(
                        f"Content chunked: {len(initial_content)} initial blocks, {len(remaining_content)} remaining"
                    )
                else:
                    initial_content = content if content else []

                # Create database item with first 100 blocks
                # Use data_source_id if available (API 2025-09-03), otherwise use database_id (backward compat)
                if data_source_id:
                    # New format for API 2025-09-03: use data_source_id
                    parent_param = {"type": "data_source_id", "data_source_id": data_source_id}
                    logger.debug(f"Creating database item with data_source_id: {data_source_id}")
                else:
                    # Legacy format: use database_id
                    parent_param = {"database_id": database_id}
                    logger.debug(f"Creating database item with database_id: {database_id}")

                response = self._notion_client.pages.create(
                    parent=parent_param, properties=properties, children=initial_content
                )

                # Add remaining blocks if any
                if remaining_content and response:
                    page_id = response["id"]
                    # Notion requires adding additional blocks via the blocks endpoint
                    self._notion_client.blocks.children.append(
                        block_id=page_id, children=remaining_content
                    )
                    logger.info(
                        f"Added {len(remaining_content)} additional blocks to database item {page_id}"
                    )

                # CRITICAL: Ensure URL is in response for publisher consumption
                if response and "id" in response:
                    # Notion API response already includes 'url' field, but ensure it's present
                    if "url" not in response or not response["url"]:
                        # Fallback: construct URL from page ID if missing
                        page_id = response["id"].replace("-", "")
                        response["url"] = f"https://www.notion.so/{page_id}"

                    logger.info(f"Database item created successfully: {response['url']}")
                else:
                    logger.error(f"Notion API response missing required fields: {response}")
                    raise ValueError("Notion API did not return valid database item response")

                return response

            response = await self.token_counter.wrap_mcp_call(
                "notion_create_database_item",
                _create(),
                input_data=str(
                    {
                        "database_id": database_id,
                        "properties_count": len(properties),
                        "content_blocks": len(content) if content else 0,
                    }
                ),
            )

            return response  # Must include 'url' field

        except Exception as e:
            logger.error(f"Failed to create database item: {e}")
            raise

    async def _validate_parent_exists(self, parent_id: str):
        """Validate parent page exists before creation attempt"""
        if not parent_id:
            raise ValueError("Parent ID is required for page creation")

        try:
            # Try to retrieve the parent page to validate it exists
            self._notion_client.pages.retrieve(parent_id)
            return True
        except APIResponseError as e:
            # Provide helpful error message with options
            error_msg = str(e)
            if "Could not find page" in error_msg or "not found" in error_msg:
                raise ValueError(
                    f"Cannot create page under parent '{parent_id}': Parent page not found or not accessible\n"
                    f"Options:\n"
                    f"  1. Use 'piper notion pages' to see available parents\n"
                    f"  2. Specify different parent with --location\n"
                    f"  3. Check parent page permissions in Notion"
                )
            else:
                raise ValueError(
                    f"Cannot create page under parent '{parent_id}': {error_msg}\n"
                    f"Options:\n"
                    f"  1. Use 'piper notion pages' to see available parents\n"
                    f"  2. Specify different parent with --location\n"
                    f"  3. Check parent page permissions"
                )

    async def search_notion(
        self, query: str, filter_type: Optional[str] = None, page_size: int = 100
    ) -> List[Dict[str, Any]]:
        """Search Notion workspace using notion_client (with token counting)"""
        try:
            # Wrap with token counting (Issue #306 Phase 2)
            async def _search():
                # Build search parameters
                search_params = {"query": query, "page_size": min(page_size, 100)}

                # Add filter if specified
                if filter_type:
                    search_params["filter"] = {"property": "object", "value": filter_type}

                # Search using notion_client
                response = self._notion_client.search(**search_params)

                # Extract results
                results = []
                if response and "results" in response:
                    for item in response["results"]:
                        results.append(item)
                return results

            results = await self.token_counter.wrap_mcp_call(
                "notion_search",
                _search(),
                input_data=str({"query": query, "filter": filter_type, "page_size": page_size}),
            )

            logger.info(f"Search found {len(results)} results for query: {query}")
            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information using notion_client (with token counting)"""
        try:
            # Wrap with token counting (Issue #306 Phase 2)
            async def _get():
                response = self._notion_client.users.retrieve(user_id=user_id)
                if response:
                    return {
                        "id": response["id"],
                        "name": response.get("name"),
                        "email": response.get("person", {}).get("email"),
                        "type": response.get("type"),
                    }
                return None

            user_data = await self.token_counter.wrap_mcp_call(
                "notion_get_user",
                _get(),
                input_data=f"user_id={user_id}",
            )

            return user_data

        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None

    async def list_users(self) -> List[Dict[str, Any]]:
        """List workspace users using notion_client (with token counting)"""
        try:
            # Wrap with token counting (Issue #306 Phase 2)
            async def _list():
                response = self._notion_client.users.list()
                if response and "results" in response:
                    users = []
                    for user in response["results"]:
                        users.append(
                            {
                                "id": user["id"],
                                "name": user.get("name"),
                                "email": user.get("person", {}).get("email"),
                                "type": user.get("type"),
                            }
                        )
                    return users
                return []

            users = await self.token_counter.wrap_mcp_call(
                "notion_list_users",
                _list(),
                input_data="",
            )

            return users

        except Exception as e:
            logger.error(f"Error listing users: {e}")
            return []

    def get_mapping_stats(self) -> Dict[str, Any]:
        """Get statistics about current mappings"""
        base_stats = super().get_mapping_stats()
        base_stats.update(
            {
                "notion_specific": {
                    "pages_mapped": len(self._page_to_position),
                    "positions_mapped": len(self._position_to_page),
                    "contexts_stored": len(self._context_storage),
                }
            }
        )
        return base_stats

    async def close(self):
        """Clean up resources"""
        try:
            if self._session:
                await self._session.close()
                self._session = None
            logger.info("NotionMCPAdapter resources cleaned up")
        except Exception as e:
            logger.error(f"Error closing NotionMCPAdapter: {e}")

    def __del__(self):
        """Destructor to ensure cleanup"""
        # Issue #781: Guard against AttributeError if __init__ failed early
        if hasattr(self, "_session") and self._session and not self._session.closed:
            asyncio.create_task(self.close())

    # #1232: AST-guard enforces the 4 methods on declared conformers.
    IMPLEMENTS_CONNECTOR = True

    async def connect(self, user_id: str) -> ConnectResult:
        """Bound already (keychain has a Notion API key for this user) -> Binding;
        otherwise the must-be-handled ConnectRequired. Notion's credential backend
        is keychain (ADR-058), not the connector_bindings table -- the Binding here
        is a pointer to that keychain grant (Arch's Layer-2 ruling: keychain is
        just another encrypted grant store, not a contract variant)."""
        config_service = self.config_service or NotionConfigService()
        if config_service.is_configured(user_id):
            return Binding(binding_id=f"notion-keychain:{user_id}")
        return ConnectRequired(degradation=await self.degrade(DegradationReason.CONNECT_REQUIRED))

    async def status(self, user_id: str) -> ConnectorStatus:
        """The user's Notion connection health -- keychain-backed, no separate
        binding row to query (D3/D5: health without a resource fetch or token)."""
        config_service = self.config_service or NotionConfigService()
        if config_service.is_configured(user_id):
            return ConnectorStatus(state=ConnectorStatusState.BOUND, detail="Notion API key configured.")
        return ConnectorStatus(
            state=ConnectorStatusState.UNBOUND,
            detail="No Notion API key configured -- connect to continue.",
        )

    async def resolve(self, user_id: str, resource: ResourceQuery) -> ResolveResult:
        """Notion has no per-user default-resource concept yet (no analog to
        GitHub's default_repo preference) -- honest RESOURCE_NOT_FOUND rather than
        inventing selection semantics that don't exist anywhere in the codebase
        today (checked: no default-database/default-page concept found). Revisit
        if/when a default-database preference is added."""
        config_service = self.config_service or NotionConfigService()
        if not config_service.is_configured(user_id):
            return ResolveMiss(await self.degrade(DegradationReason.CONNECT_REQUIRED))
        return ResolveMiss(await self.degrade(DegradationReason.RESOURCE_NOT_FOUND))

    async def degrade(self, reason: DegradationReason) -> DegradationResponse:
        messages = {
            DegradationReason.CONNECT_REQUIRED: "Connect Notion to continue.",
            DegradationReason.RESOURCE_NOT_FOUND: "That Notion resource wasn't found.",
            DegradationReason.UNREACHABLE: "Notion is unreachable right now.",
            DegradationReason.STALE_TOKEN: "Your Notion connection needs re-authorizing.",
        }
        return DegradationResponse(
            reason=reason, user_message=messages.get(reason, "The Notion connector is degraded.")
        )
