"""
Notion MCP Spatial Adapter

Notion-specific MCP spatial adapter implementation following the established
spatial adapter pattern for external system integration.
"""

import asyncio
import logging

# Import for service injection pattern
from typing import TYPE_CHECKING, Any, Dict, List, Optional

import aiohttp
from notion_client import Client
from notion_client.errors import APIResponseError, RequestTimeoutError

from config.notion_config import NotionConfig
from services.integrations.spatial_adapter import (
    BaseSpatialAdapter,
    SpatialContext,
    SpatialPosition,
)

if TYPE_CHECKING:
    from services.integrations.notion.config_service import NotionConfigService

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

        # Notion client configuration with service injection pattern
        if config_service:
            # Use service injection pattern (preferred)
            self.config_service = config_service
            self.config = config_service.get_config()
        else:
            # Fallback to static config for backward compatibility
            self.config_service = None
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
            api_key = self.config.get_api_key()
            if api_key:
                self._notion_client = Client(auth=api_key)
                logger.info("Notion client initialized with configuration")
            else:
                logger.warning("NOTION_API_KEY not set - client will be initialized later")
        except Exception as e:
            logger.error(f"Error initializing Notion client: {e}")

    async def connect(self, integration_token: Optional[str] = None) -> bool:
        """Connect to Notion with integration token"""
        try:
            if integration_token:
                # Initialize with provided token
                self._notion_client = Client(auth=integration_token)
            elif not self._notion_client:
                # Try to initialize from configuration
                api_key = self.config.get_api_key()
                if api_key:
                    self._notion_client = Client(auth=api_key)
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

    async def fetch_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """Fetch accessible Notion databases (alias for list_databases)"""
        return await self.list_databases(page_size)

    async def list_databases(self, page_size: int = 100) -> List[Dict[str, Any]]:
        """List all databases using notion_client"""
        try:
            # Search for all databases
            response = self._notion_client.search(
                filter={"property": "object", "value": "database"}, page_size=min(page_size, 100)
            )

            databases = []
            if response and "results" in response:
                databases = response["results"]

            logger.info(f"Found {len(databases)} databases")
            return databases

        except Exception as e:
            logger.error(f"Failed to list databases: {e}")
            return []

    async def get_database(self, database_id: str) -> Optional[Dict[str, Any]]:
        """Get specific database using notion_client"""
        try:
            if not database_id:
                logger.error("database_id is required")
                return None

            # Retrieve database using notion_client
            response = self._notion_client.databases.retrieve(database_id=database_id)

            logger.info(f"Retrieved database: {database_id}")
            return response

        except Exception as e:
            logger.error(f"Failed to get database: {e}")
            return None

    async def query_database(
        self,
        database_id: str,
        filter_params: Optional[Dict] = None,
        sorts: Optional[List] = None,
        page_size: int = 100,
    ) -> List[Dict[str, Any]]:
        """Query database using notion_client"""
        try:
            if not database_id:
                logger.error("database_id is required")
                return []

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

            logger.info(f"Query returned {len(results)} results from database: {database_id}")
            return results

        except Exception as e:
            logger.error(f"Failed to query database: {e}")
            return []

    async def get_page(self, page_id: str) -> Optional[Dict[str, Any]]:
        """Get specific page content and properties using notion_client"""
        try:
            if not page_id:
                logger.error("page_id is required for page retrieval")
                return None

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

        except Exception as e:
            logger.error(f"Failed to get page: {e}")
            return None

    async def get_page_blocks(self, page_id: str, page_size: int = 100) -> List[Dict[str, Any]]:
        """Get page content blocks using notion_client"""
        try:
            if not page_id:
                logger.error("page_id is required")
                return []

            # Get blocks using notion_client
            response = self._notion_client.blocks.children.list(
                block_id=page_id, page_size=min(page_size, 100)
            )

            blocks = []
            if response and "results" in response:
                for block in response["results"]:
                    blocks.append(block)

            return blocks

        except Exception as e:
            logger.error(f"Failed to get blocks: {e}")
            return []

    async def update_page(self, page_id: str, properties: Dict):
        """Update a Notion page using notion_client"""
        try:
            if not page_id:
                logger.error("page_id is required for page update")
                return None

            # Update page using notion_client
            response = self._notion_client.pages.update(page_id=page_id, properties=properties)

            logger.info(f"Page updated successfully: {page_id}")
            return response

        except Exception as e:
            logger.error(f"Failed to update page: {e}")
            return None

    async def create_page(self, parent_id: str, properties: Dict, content: Optional[List] = None):
        """Create a new Notion page using notion_client"""
        try:
            if not parent_id:
                raise ValueError("parent_id is required for page creation")

            # Validate parent exists first
            parent_validation = await self._validate_parent_exists(parent_id)

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
                logger.info(f"Added {len(remaining_content)} additional blocks to page {page_id}")

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

            return response  # Must include 'url' field

        except Exception as e:
            logger.error(f"Failed to create page: {e}")
            raise

    async def create_database_item(
        self, database_id: str, properties: Dict, content: Optional[List] = None
    ):
        """Create a new database item using notion_client"""
        try:
            if not database_id:
                raise ValueError("database_id is required for database item creation")

            # Validate database exists first
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
            response = self._notion_client.pages.create(
                parent={"database_id": database_id}, properties=properties, children=initial_content
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
        """Search Notion workspace using notion_client"""
        try:
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

            logger.info(f"Search found {len(results)} results for query: {query}")
            return results

        except Exception as e:
            logger.error(f"Search failed: {e}")
            return []

    async def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user information using notion_client"""
        try:
            response = self._notion_client.users.retrieve(user_id=user_id)
            if response:
                return {
                    "id": response["id"],
                    "name": response.get("name"),
                    "email": response.get("person", {}).get("email"),
                    "type": response.get("type"),
                }
            return None

        except Exception as e:
            logger.error(f"Error getting user {user_id}: {e}")
            return None

    async def list_users(self) -> List[Dict[str, Any]]:
        """List workspace users using notion_client"""
        try:
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
        if self._session and not self._session.closed:
            asyncio.create_task(self.close())
