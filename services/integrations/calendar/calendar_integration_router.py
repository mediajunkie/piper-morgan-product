"""
CalendarIntegrationRouter - Feature flag controlled access to calendar integrations

Provides unified interface for calendar operations with support for:
- Spatial intelligence (MCP-based GoogleCalendarMCPAdapter)
- Legacy basic calendar operations (if future implementation exists)
- Feature flag control via USE_SPATIAL_CALENDAR

Architecture Decision: ADR-037 Calendar Integration Router Pattern
Following pattern established in CORE-GREAT-2B GitHubIntegrationRouter.
"""

import os
import warnings
from typing import Any, Dict, List, Optional, Tuple

from services.infrastructure.config.feature_flags import FeatureFlags

from .config_service import CalendarConfigService


class CalendarIntegrationRouter:
    """
    Router for calendar integration with spatial/legacy delegation.

    Follows pattern established in CORE-GREAT-2B GitHubIntegrationRouter.
    Delegates to GoogleCalendarMCPAdapter (spatial) or future legacy implementation.

    Examples:
        # Basic usage with spatial intelligence
        router = CalendarIntegrationRouter()
        events = await router.get_todays_events()

        # Feature flag control
        # USE_SPATIAL_CALENDAR=true (default) - uses GoogleCalendarMCPAdapter
        # USE_SPATIAL_CALENDAR=false - uses legacy if available, else raises error

    Architecture:
        - Spatial: GoogleCalendarMCPAdapter with OAuth2 and circuit breaker
        - Legacy: Placeholder for future basic calendar implementation
        - Feature Flags: USE_SPATIAL_CALENDAR, ALLOW_LEGACY_CALENDAR
    """

    def __init__(
        self,
        config_service: Optional[CalendarConfigService] = None,
        user_id: Optional[str] = None,
    ):
        """
        Initialize router with feature flag checking and config service.

        Issue #586: Added user_id parameter for timezone-aware calendar queries.
        Issue #843: Passes user_id to adapter for user-scoped authentication.

        Args:
            config_service: Optional CalendarConfigService instance
            user_id: Optional user ID for timezone-aware queries and user-scoped auth
        """
        # Use FeatureFlags service for consistency with GitHub router
        self.use_spatial = FeatureFlags.should_use_spatial_calendar()
        self.allow_legacy = FeatureFlags.is_legacy_calendar_allowed()

        # Store config service (create default if not provided)
        self.config_service = config_service or CalendarConfigService()

        # Issue #586: Store user_id for timezone-aware queries
        self._user_id = user_id

        # Initialize spatial integration
        self.spatial_calendar = None
        if self.use_spatial:
            try:
                from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

                # Issue #843: Pass user_id to adapter for user-scoped keychain auth
                self.spatial_calendar = GoogleCalendarMCPAdapter(
                    self.config_service, user_id=user_id
                )
            except ImportError as e:
                warnings.warn(f"Spatial calendar unavailable: {e}")

        # Initialize legacy integration (placeholder for future)
        self.legacy_calendar = None
        if self.allow_legacy:
            # Future: Import legacy calendar client if exists
            # For now, no legacy implementation exists
            pass

    def _get_preferred_integration(self, operation: str) -> Tuple[Optional[Any], bool]:
        """
        Get preferred calendar integration based on feature flags and availability.

        Args:
            operation: Name of operation being performed

        Returns:
            Tuple of (integration_instance, is_legacy_used)
        """
        # Try spatial first if enabled
        if self.use_spatial and self.spatial_calendar:
            return self.spatial_calendar, False

        # Fall back to legacy if allowed (future implementation)
        elif self.allow_legacy and self.legacy_calendar:
            return self.legacy_calendar, True

        # No integration available
        else:
            return None, False

    def _warn_deprecation_if_needed(self, operation: str, is_legacy: bool):
        """Issue deprecation warnings when legacy integration is used"""
        if is_legacy:
            warnings.warn(
                f"Using legacy calendar for {operation}. "
                "Consider enabling USE_SPATIAL_CALENDAR=true for spatial intelligence.",
                DeprecationWarning,
                stacklevel=3,
            )

    # Calendar Operations (7 methods)

    async def authenticate(self) -> bool:
        """
        Authenticate with Google Calendar via OAuth2.

        Returns:
            bool: True if authentication successful, False otherwise

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("authenticate")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("authenticate", is_legacy)
            return await integration.authenticate()
        else:
            raise RuntimeError(
                "No calendar integration available for authenticate. "
                "Enable USE_SPATIAL_CALENDAR=true or check GoogleCalendarMCPAdapter setup."
            )

    async def get_todays_events(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get today's calendar events from Google Calendar.

        Issue #586: Added user_id parameter for timezone-aware queries.

        Args:
            user_id: Optional user ID for timezone-aware queries.
                    If not provided, uses self._user_id from __init__.

        Returns:
            List[Dict[str, Any]]: List of today's calendar events

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_todays_events")

        # Issue #586: Use provided user_id or fall back to instance user_id
        effective_user_id = user_id or self._user_id

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_todays_events", is_legacy)
            return await integration.get_todays_events(user_id=effective_user_id)
        else:
            raise RuntimeError("No calendar integration available for get_todays_events")

    async def get_current_meeting(self) -> Optional[Dict[str, Any]]:
        """
        Get currently active meeting if any.

        Returns:
            Optional[Dict[str, Any]]: Current meeting details or None

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_current_meeting")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_current_meeting", is_legacy)
            return await integration.get_current_meeting()
        else:
            raise RuntimeError("No calendar integration available for get_current_meeting")

    async def get_next_meeting(self) -> Optional[Dict[str, Any]]:
        """
        Get next upcoming meeting today.

        Returns:
            Optional[Dict[str, Any]]: Next meeting details or None

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_next_meeting")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_next_meeting", is_legacy)
            return await integration.get_next_meeting()
        else:
            raise RuntimeError("No calendar integration available for get_next_meeting")

    async def get_free_time_blocks(self) -> List[Dict[str, Any]]:
        """
        Calculate free time blocks between meetings.

        Returns:
            List[Dict[str, Any]]: Available free time blocks

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_free_time_blocks")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_free_time_blocks", is_legacy)
            return await integration.get_free_time_blocks()
        else:
            raise RuntimeError("No calendar integration available for get_free_time_blocks")

    async def get_temporal_summary(self, user_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get comprehensive temporal summary for standup integration.

        Issue #596: Added user_id parameter for timezone-aware queries.

        #1425: falls back to the instance ``user_id``, exactly as
        ``get_todays_events`` already did. It did not, so the greeting path
        (which builds the router WITH a user, then calls this with no argument)
        reached the adapter as ``user_id=None`` — and the adapter's
        ``_get_user_timezone(None)`` skips the preference lookup entirely and
        returns its hardcoded ``America/Los_Angeles`` fallback. The day-boundary
        window therefore belonged to no particular user. What a user's timezone
        SHOULD be, system-wide, is #1572; this is only the plumbing.

        Args:
            user_id: Optional user ID for timezone-aware day boundaries.
                    If not provided, uses self._user_id from __init__.

        Returns:
            Dict[str, Any]: Temporal awareness summary with current meeting,
                          next meeting, free blocks, and recommendations

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_temporal_summary")

        effective_user_id = user_id or self._user_id

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_temporal_summary", is_legacy)
            return await integration.get_temporal_summary(user_id=effective_user_id)
        else:
            raise RuntimeError("No calendar integration available for get_temporal_summary")

    async def health_check(self) -> Dict[str, Any]:
        """
        Check calendar integration health and authentication status.

        Returns:
            Dict[str, Any]: Health check results including authentication status,
                          dependencies, and service availability

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("health_check")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("health_check", is_legacy)
            return await integration.health_check()
        else:
            raise RuntimeError("No calendar integration available for health_check")

    async def get_events_in_range(self, start_date, end_date) -> List[Dict[str, Any]]:
        """
        Get calendar events within a date range.

        Issue #518: Added for Query #61 (week calendar) to support router pattern.

        Args:
            start_date: Start of date range (datetime)
            end_date: End of date range (datetime)

        Returns:
            List[Dict[str, Any]]: List of calendar events in range

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_events_in_range")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_events_in_range", is_legacy)
            return await integration.get_events_in_range(start_date, end_date)
        else:
            raise RuntimeError("No calendar integration available for get_events_in_range")

    async def get_recurring_events(self, days_ahead: int = 30) -> List[Dict[str, Any]]:
        """
        Get recurring calendar events.

        Issue #518: Added for Query #35 (recurring meetings) to support router pattern.

        Args:
            days_ahead: Number of days to look ahead (default 30)

        Returns:
            List[Dict[str, Any]]: List of recurring events with frequency info

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_recurring_events")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_recurring_events", is_legacy)
            return await integration.get_recurring_events(days_ahead)
        else:
            raise RuntimeError("No calendar integration available for get_recurring_events")

    # Spatial Intelligence Methods (from BaseSpatialAdapter)

    def get_context(self, external_id: str):
        """
        Get spatial context for external system identifier.

        Args:
            external_id: External system identifier (e.g., calendar event ID)

        Returns:
            Optional[SpatialContext]: Spatial context or None

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_context")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_context", is_legacy)
            return integration.get_context(external_id)
        else:
            raise RuntimeError("No calendar integration available for get_context")

    def get_mapping_stats(self) -> Dict[str, Any]:
        """
        Get statistics about current spatial mappings.

        Returns:
            Dict[str, Any]: Mapping statistics including counts and health

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("get_mapping_stats")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("get_mapping_stats", is_legacy)
            return integration.get_mapping_stats()
        else:
            raise RuntimeError("No calendar integration available for get_mapping_stats")

    def map_from_position(self, position):
        """
        Map spatial position back to external system identifier.

        Args:
            position: Spatial position to convert

        Returns:
            Optional[str]: External ID or None

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("map_from_position")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("map_from_position", is_legacy)
            return integration.map_from_position(position)
        else:
            raise RuntimeError("No calendar integration available for map_from_position")

    def map_to_position(self, external_id: str, context: Dict[str, Any]):
        """
        Map external system identifier to spatial position.

        Args:
            external_id: External system identifier
            context: Additional context for mapping

        Returns:
            SpatialPosition: Mapped spatial position

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("map_to_position")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("map_to_position", is_legacy)
            return integration.map_to_position(external_id, context)
        else:
            raise RuntimeError("No calendar integration available for map_to_position")

    def store_mapping(self, external_id: str, position) -> bool:
        """
        Store mapping between external ID and spatial position.

        Args:
            external_id: External system identifier
            position: Spatial position to map

        Returns:
            bool: True if stored successfully

        Raises:
            RuntimeError: If no calendar integration is available
        """
        integration, is_legacy = self._get_preferred_integration("store_mapping")

        if integration:
            if is_legacy:
                self._warn_deprecation_if_needed("store_mapping", is_legacy)
            return integration.store_mapping(external_id, position)
        else:
            raise RuntimeError("No calendar integration available for store_mapping")

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
                "error": "No calendar integration available",
                "feature_flags": {
                    "use_spatial": self.use_spatial,
                    "allow_legacy": self.allow_legacy,
                },
            }


# Convenience factory function
def create_calendar_integration(user_id: Optional[str] = None) -> CalendarIntegrationRouter:
    """
    Factory function to create CalendarIntegrationRouter instance.

    Args:
        user_id: Optional user ID for user-scoped keychain authentication

    Returns:
        CalendarIntegrationRouter: Configured router instance
    """
    # Issue #849: Accept user_id for user-scoped calendar auth
    return CalendarIntegrationRouter(user_id=user_id)
