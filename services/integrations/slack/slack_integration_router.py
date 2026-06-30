"""
SlackIntegrationRouter - Feature flag controlled access to Slack integrations

Provides unified interface for Slack operations with support for:
- Spatial intelligence (SlackSpatialAdapter + SlackClient with spatial intelligence)
- Legacy basic Slack operations (basic SlackClient only)
- Feature flag control via USE_SPATIAL_SLACK

Architecture Decision: ADR-039 Slack Integration Router Pattern
Adapting router pattern for non-MCP spatial architecture (SlackSpatialAdapter + SlackClient).
Following pattern established in CalendarIntegrationRouter and NotionIntegrationRouter.
"""

import warnings
from typing import Any, Dict, List, Optional, Tuple

from services.infrastructure.config.feature_flags import FeatureFlags

# Import Slack response type for proper return annotations
from .slack_client import SlackResponse


class SlackIntegrationRouter:
    """
    Router for Slack integration with spatial/legacy delegation.

    Unlike Calendar/Notion MCP pattern, Slack uses direct spatial pattern.
    Coordinates SlackSpatialAdapter + SlackClient for spatial mode.
    Delegates to basic SlackClient for legacy mode.

    Examples:
        # Basic usage with spatial intelligence. The router is a singleton; the
        # per-user SlackClient is built lazily per operation, so pass user_id on
        # each call (#1110, multi-tenancy / ADR-058).
        router = SlackIntegrationRouter(config_service)
        await router.send_message("#general", "Hello world!", user_id="U123")
        channels = await router.list_channels(user_id="U123")

        # Feature flag control
        # USE_SPATIAL_SLACK=true (default) - uses SlackSpatialAdapter + SlackClient
        # USE_SPATIAL_SLACK=false - uses basic SlackClient only

    Architecture:
        - Spatial: SlackSpatialAdapter + SlackClient (coordinated spatial intelligence)
        - Legacy: SlackClient only (basic Slack operations)
        - Feature Flags: USE_SPATIAL_SLACK, ALLOW_LEGACY_SLACK
    """

    def __init__(self, config_service=None):
        """Initialize router with feature flag checking and config service.

        #1110: The router is a startup SINGLETON (e.g. SlackPlugin builds one at
        module import, ReminderScheduler / SlackWebhookRouter each hold one for
        their lifetime). user_id, however, is per-OPERATION (per request, per
        reminder-user, per inbound event). So the underlying ``SlackClient`` —
        which requires a user_id because ``SlackConfigService.get_config`` does —
        is built LAZILY per operation via ``_get_client(user_id)`` rather than
        eagerly here. The spatial adapter (which has no user scoping) is still
        built eagerly because it is shared across users.
        """
        # Use FeatureFlags service for consistency with other routers
        self.use_spatial = FeatureFlags.should_use_spatial_slack()
        self.allow_legacy = FeatureFlags.is_legacy_slack_allowed()

        # Store config service for lazy per-operation SlackClient construction
        self.config_service = config_service

        # Spatial adapter is user-agnostic → safe to build eagerly and share.
        self.spatial_adapter = None

        # Per-user lazily-built clients (keyed by user_id). The router caches one
        # SlackClient per user so repeated operations reuse the HTTP session.
        self._clients_by_user: Dict[str, Any] = {}

        if self.use_spatial:
            try:
                from .spatial_adapter import SlackSpatialAdapter

                self.spatial_adapter = SlackSpatialAdapter()
            except ImportError as e:
                warnings.warn(f"Spatial Slack unavailable: {e}")

    @property
    def spatial_client(self):
        """Deprecated eager accessor retained for status/back-compat.

        #1110: clients are now built lazily per user, so there is no single
        long-lived spatial client. Returns the most-recently-built client if any
        (for ``get_integration_status`` introspection) else None. Operational
        code must go through :meth:`_get_client`.
        """
        return next(iter(self._clients_by_user.values()), None)

    @property
    def legacy_client(self):
        """Deprecated eager accessor; see :attr:`spatial_client`. Kept for
        status introspection only (#1110 lazy-client migration)."""
        return next(iter(self._clients_by_user.values()), None)

    def _get_client(self, user_id: str):
        """Lazily build (and per-user cache) a SlackClient for an operation.

        #1110: user_id is required end-to-end. Raises if no config_service was
        provided at construction (mirrors the prior eager-None behavior) or if
        the caller supplied no user_id (a true user-less Slack op is a bug — see
        the guardrail in the issue).
        """
        if not self.config_service:
            return None
        if not user_id:
            raise ValueError(
                "user_id is required for Slack operations (multi-tenancy, "
                "ADR-058/#734). The router cannot build a SlackClient without it."
            )
        client = self._clients_by_user.get(user_id)
        if client is None:
            from .slack_client import SlackClient

            client = SlackClient(self.config_service, user_id=user_id)
            self._clients_by_user[user_id] = client
        return client

    def _ensure_config_service(self, operation: str):
        """Ensure config service is available for SlackClient operations"""
        if not self.config_service:
            raise RuntimeError(
                f"SlackConfigService required for {operation}. "
                "Initialize router with config_service parameter: "
                "SlackIntegrationRouter(config_service)"
            )

    def _get_preferred_integration(
        self, operation: str, user_id: Optional[str] = None
    ) -> Tuple[Optional[Any], bool]:
        """
        Get preferred Slack integration based on feature flags and availability.

        Args:
            operation: Name of operation being performed
            user_id: User identifier for the operation (#1110). Required for any
                operation that actually issues a Slack API call; may be omitted
                only for user-agnostic introspection (e.g. status/context-mgr).

        Returns:
            Tuple of (slack_client_instance, is_legacy_used)

        Note: For spatial mode, spatial_adapter is available via get_spatial_adapter()
        """
        # #1110: client is built lazily per user. The same SlackClient serves
        # both spatial and legacy delegation; is_legacy reflects the active mode
        # for deprecation warnings only.
        client = self._get_client(user_id) if user_id else None

        # Try spatial first if enabled
        if self.use_spatial and client:
            return client, False

        # Fall back to legacy if allowed
        elif self.allow_legacy and client:
            return client, True

        # No integration available
        else:
            return None, False

    def _warn_deprecation_if_needed(self, operation: str, is_legacy: bool):
        """Issue deprecation warnings when legacy integration is used"""
        if is_legacy:
            warnings.warn(
                f"Using legacy Slack for {operation}. "
                "Consider enabling USE_SPATIAL_SLACK=true for spatial intelligence.",
                DeprecationWarning,
                stacklevel=3,
            )

    # SlackClient method delegation (primary interface)

    async def send_message(
        self, channel: str, text: str, user_id: Optional[str] = None, **kwargs
    ) -> SlackResponse:
        """
        Send message to Slack channel.

        Args:
            channel: Slack channel ID or name
            text: Message text
            user_id: User identifier scoping credentials (#1110, required for the
                underlying Slack API call).
            **kwargs: Additional Slack API parameters

        Returns:
            SlackResponse: Slack API response

        Raises:
            RuntimeError: If no Slack integration is available or config missing
        """
        self._ensure_config_service("send_message")
        client, is_legacy = self._get_preferred_integration("send_message", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("send_message", is_legacy)
            return await client.send_message(channel, text, **kwargs)
        else:
            raise RuntimeError(
                "No Slack integration available for send_message. "
                "Enable USE_SPATIAL_SLACK=true or check SlackClient setup."
            )

    async def get_channel_info(self, channel: str, user_id: Optional[str] = None) -> SlackResponse:
        """
        Get channel information.

        Args:
            channel: Slack channel ID or name
            user_id: User identifier scoping credentials (#1110).

        Returns:
            SlackResponse: Channel information

        Raises:
            RuntimeError: If no Slack integration is available or config missing
        """
        self._ensure_config_service("get_channel_info")
        client, is_legacy = self._get_preferred_integration("get_channel_info", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("get_channel_info", is_legacy)
            return await client.get_channel_info(channel)
        else:
            raise RuntimeError("No Slack integration available for get_channel_info")

    async def list_im_channels(self, user_id: Optional[str] = None) -> SlackResponse:
        """List the authenticated user's direct-message channels (im + mpim).

        Added 2026-05-17 (#1085 slice 2) for recent-activity aggregator.

        Args:
            user_id: User identifier scoping credentials (#1110).
        """
        self._ensure_config_service("list_im_channels")
        client, is_legacy = self._get_preferred_integration("list_im_channels", user_id)
        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("list_im_channels", is_legacy)
            return await client.list_im_channels()
        else:
            raise RuntimeError("No Slack integration available for list_im_channels")

    async def list_channels(self, user_id: Optional[str] = None) -> SlackResponse:
        """
        List all channels.

        Args:
            user_id: User identifier scoping credentials (#1110).

        Returns:
            SlackResponse: List of all channels

        Raises:
            RuntimeError: If no Slack integration is available
        """
        self._ensure_config_service("list_channels")
        client, is_legacy = self._get_preferred_integration("list_channels", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("list_channels", is_legacy)
            return await client.list_channels()
        else:
            raise RuntimeError("No Slack integration available for list_channels")

    async def get_user_info(self, user: str, user_id: Optional[str] = None) -> SlackResponse:
        """
        Get user information.

        Args:
            user: Slack user ID or name (the user to look up)
            user_id: User identifier scoping credentials of the CALLER (#1110).

        Returns:
            SlackResponse: User information

        Raises:
            RuntimeError: If no Slack integration is available
        """
        self._ensure_config_service("get_user_info")
        client, is_legacy = self._get_preferred_integration("get_user_info", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("get_user_info", is_legacy)
            return await client.get_user_info(user)
        else:
            raise RuntimeError("No Slack integration available for get_user_info")

    async def list_users(self, user_id: Optional[str] = None) -> SlackResponse:
        """
        List all users.

        Args:
            user_id: User identifier scoping credentials (#1110).

        Returns:
            SlackResponse: List of all users

        Raises:
            RuntimeError: If no Slack integration is available
        """
        self._ensure_config_service("list_users")
        client, is_legacy = self._get_preferred_integration("list_users", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("list_users", is_legacy)
            return await client.list_users()
        else:
            raise RuntimeError("No Slack integration available for list_users")

    async def test_auth(self, user_id: Optional[str] = None) -> SlackResponse:
        """
        Test authentication.

        Args:
            user_id: User identifier scoping credentials (#1110).

        Returns:
            SlackResponse: Authentication test results

        Raises:
            RuntimeError: If no Slack integration is available
        """
        self._ensure_config_service("test_auth")
        client, is_legacy = self._get_preferred_integration("test_auth", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("test_auth", is_legacy)
            return await client.test_auth()
        else:
            raise RuntimeError("No Slack integration available for test_auth")

    async def get_conversation_history(
        self,
        channel: str,
        limit: int = 100,
        cursor: str = None,
        oldest: Optional[float] = None,
        user_id: Optional[str] = None,
    ) -> SlackResponse:
        """
        Get conversation history for a channel.

        Args:
            channel: Channel ID to get history for
            limit: Number of messages to retrieve (default: 100, max: 1000)
            cursor: Cursor for pagination
            oldest: Slack timestamp; messages older are excluded (#1085 slice 2)
            user_id: User identifier scoping credentials (#1110).

        Returns:
            SlackResponse: Conversation history data

        Raises:
            RuntimeError: If no Slack integration is available or config missing
        """
        self._ensure_config_service("get_conversation_history")
        client, is_legacy = self._get_preferred_integration("get_conversation_history", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("get_conversation_history", is_legacy)
            return await client.get_conversation_history(
                channel, limit=limit, cursor=cursor, oldest=oldest
            )
        else:
            raise RuntimeError("No Slack integration available for get_conversation_history")

    async def get_thread_replies(
        self,
        channel: str,
        thread_ts: str,
        limit: int = 100,
        cursor: str = None,
        user_id: Optional[str] = None,
    ) -> SlackResponse:
        """
        Get replies in a thread.

        Args:
            channel: Channel ID containing the thread
            thread_ts: Timestamp of the parent message
            limit: Number of replies to retrieve (default: 100, max: 1000)
            cursor: Cursor for pagination
            user_id: User identifier scoping credentials (#1110).

        Returns:
            SlackResponse: Thread replies data

        Raises:
            RuntimeError: If no Slack integration is available or config missing
        """
        self._ensure_config_service("get_thread_replies")
        client, is_legacy = self._get_preferred_integration("get_thread_replies", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("get_thread_replies", is_legacy)
            return await client.get_thread_replies(channel, thread_ts, limit, cursor)
        else:
            raise RuntimeError("No Slack integration available for get_thread_replies")

    async def add_reaction(
        self, channel: str, timestamp: str, name: str, user_id: Optional[str] = None
    ) -> SlackResponse:
        """
        Add reaction to a message.

        Args:
            channel: Channel ID containing the message
            timestamp: Timestamp of the message to react to
            name: Reaction name (emoji without colons, e.g., "thumbsup")
            user_id: User identifier scoping credentials (#1110).

        Returns:
            SlackResponse: Reaction addition result

        Raises:
            RuntimeError: If no Slack integration is available or config missing
        """
        self._ensure_config_service("add_reaction")
        client, is_legacy = self._get_preferred_integration("add_reaction", user_id)

        if client:
            if is_legacy:
                self._warn_deprecation_if_needed("add_reaction", is_legacy)
            return await client.add_reaction(channel, timestamp, name)
        else:
            raise RuntimeError("No Slack integration available for add_reaction")

    # Spatial intelligence access methods

    def get_spatial_adapter(self) -> Optional[Any]:
        """
        Get spatial adapter for advanced spatial intelligence operations.

        Returns:
            Optional[SlackSpatialAdapter]: Spatial adapter if available in spatial mode

        Note:
            Only available when USE_SPATIAL_SLACK=true. Used for spatial mapping,
            context storage, and integration with spatial metaphor system.
        """
        if self.use_spatial:
            return self.spatial_adapter
        return None

    async def map_to_position(self, external_id: str, context: Dict[str, Any]):
        """
        Map Slack timestamp to spatial position (spatial intelligence method).

        Args:
            external_id: Slack timestamp
            context: Additional context for spatial mapping

        Returns:
            SpatialPosition: Spatial position mapping

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.map_to_position(external_id, context)
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    async def map_from_position(self, position) -> Optional[str]:
        """
        Map spatial position back to Slack timestamp (spatial intelligence method).

        Args:
            position: SpatialPosition to reverse map

        Returns:
            Optional[str]: Slack timestamp if mapping exists

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.map_from_position(position)
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    async def store_mapping(self, external_id: str, position) -> bool:
        """
        Store mapping between Slack timestamp and spatial position.

        Args:
            external_id: Slack timestamp
            position: SpatialPosition to map to

        Returns:
            bool: True if mapping stored successfully

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.store_mapping(external_id, position)
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    async def get_context(self, external_id: str):
        """
        Get spatial context for Slack timestamp.

        Args:
            external_id: Slack timestamp

        Returns:
            Optional[SpatialContext]: Spatial context if mapping exists

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.get_context(external_id)
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    async def get_mapping_stats(self) -> Dict[str, Any]:
        """
        Get spatial mapping statistics.

        Returns:
            Dict[str, Any]: Mapping statistics

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.get_mapping_stats()
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    # Slack-specific spatial intelligence methods

    async def create_spatial_event_from_slack(
        self, slack_timestamp: str, event_type: str, context: Dict[str, Any]
    ):
        """
        Create spatial event from Slack event (Slack-specific spatial method).

        Args:
            slack_timestamp: Slack message timestamp
            event_type: Type of spatial event
            context: Additional context for the event

        Returns:
            SpatialEvent: Created spatial event

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.create_spatial_event_from_slack(
                slack_timestamp, event_type, context
            )
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    async def create_spatial_object_from_slack(self, slack_object: Dict[str, Any]):
        """
        Create spatial object from Slack object (Slack-specific spatial method).

        Args:
            slack_object: Slack object data

        Returns:
            SpatialObject: Created spatial object

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.create_spatial_object_from_slack(slack_object)
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    async def get_response_context(self, slack_timestamp: str) -> Optional[Dict[str, Any]]:
        """
        Get response context for Slack timestamp (Slack-specific spatial method).

        Args:
            slack_timestamp: Slack message timestamp

        Returns:
            Optional[Dict[str, Any]]: Response context if available

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.get_response_context(slack_timestamp)
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    async def cleanup_old_mappings(self, max_age_hours: int = 24) -> int:
        """
        Clean up old spatial mappings (Slack-specific spatial method).

        Args:
            max_age_hours: Maximum age of mappings to keep

        Returns:
            int: Number of mappings cleaned up

        Raises:
            RuntimeError: If spatial intelligence not available
        """
        if self.spatial_adapter:
            return await self.spatial_adapter.cleanup_old_mappings(max_age_hours)
        else:
            raise RuntimeError("Spatial intelligence not available. Enable USE_SPATIAL_SLACK=true.")

    # Context manager support (for SlackClient compatibility)

    async def __aenter__(self):
        """Async context manager entry"""
        client, _ = self._get_preferred_integration("context_manager")
        if client and hasattr(client, "__aenter__"):
            await client.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        client, _ = self._get_preferred_integration("context_manager")
        if client and hasattr(client, "__aexit__"):
            await client.__aexit__(exc_type, exc_val, exc_tb)

    # Router status and debugging

    def get_integration_status(self) -> Dict[str, Any]:
        """
        Get current integration status for monitoring and debugging.

        Returns:
            Dict[str, Any]: Router status including feature flags and available integrations
        """
        client, is_legacy = self._get_preferred_integration("get_integration_status")

        return {
            "router_initialized": True,
            "using_spatial": not is_legacy if client else False,
            "using_legacy": is_legacy if client else False,
            "spatial_adapter_available": self.spatial_adapter is not None,
            "spatial_client_available": self.spatial_client is not None,
            "legacy_client_available": self.legacy_client is not None,
            "config_service_provided": self.config_service is not None,
            "integration_type": type(client).__name__ if client else None,
            "error": "No Slack integration available" if not client else None,
            "feature_flags": {
                "use_spatial": self.use_spatial,
                "allow_legacy": self.allow_legacy,
            },
        }


# Convenience factory function
def create_slack_integration(config_service=None) -> SlackIntegrationRouter:
    """
    Factory function to create SlackIntegrationRouter instance.

    Args:
        config_service: Optional SlackConfigService instance

    Returns:
        SlackIntegrationRouter: Configured router instance
    """
    return SlackIntegrationRouter(config_service)
