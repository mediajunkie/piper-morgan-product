"""
Calendar Integration Tests

Tests for Calendar integration router and GoogleCalendarMCPAdapter.
CORE-GREAT-2D: Complete Calendar integration testing (5% remaining).
"""

import os
from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pytest


class TestCalendarIntegrationRouter:
    """Test CalendarIntegrationRouter functionality"""

    def test_router_initialization(self):
        """Test that CalendarIntegrationRouter initializes correctly"""
        from services.integrations.calendar import CalendarIntegrationRouter

        router = CalendarIntegrationRouter()

        assert router is not None
        assert hasattr(router, "use_spatial")
        assert hasattr(router, "allow_legacy")
        assert hasattr(router, "spatial_calendar")

    def test_router_feature_flags(self):
        """Test that feature flags are read correctly"""
        from services.integrations.calendar import CalendarIntegrationRouter

        with patch.dict(os.environ, {"USE_SPATIAL_CALENDAR": "true"}):
            router = CalendarIntegrationRouter()
            assert router.use_spatial is True

        with patch.dict(os.environ, {"USE_SPATIAL_CALENDAR": "false"}):
            router = CalendarIntegrationRouter()
            assert router.use_spatial is False

    def test_router_has_calendar_methods(self):
        """Test that router has all required calendar methods"""
        from services.integrations.calendar import CalendarIntegrationRouter

        router = CalendarIntegrationRouter()

        # Calendar operations
        assert hasattr(router, "authenticate")
        assert hasattr(router, "get_todays_events")
        assert hasattr(router, "get_current_meeting")
        assert hasattr(router, "get_next_meeting")
        assert hasattr(router, "get_free_time_blocks")
        assert hasattr(router, "get_temporal_summary")
        assert hasattr(router, "health_check")

    def test_router_has_spatial_methods(self):
        """Test that router has all required spatial adapter methods"""
        from services.integrations.calendar import CalendarIntegrationRouter

        router = CalendarIntegrationRouter()

        # Spatial adapter methods
        assert hasattr(router, "get_context")
        assert hasattr(router, "get_mapping_stats")
        assert hasattr(router, "map_from_position")
        assert hasattr(router, "map_to_position")
        assert hasattr(router, "store_mapping")

    def test_router_get_integration_status(self):
        """Test router integration status reporting"""
        from services.integrations.calendar import CalendarIntegrationRouter

        router = CalendarIntegrationRouter()
        status = router.get_integration_status()

        assert isinstance(status, dict)
        assert "router_initialized" in status
        assert "using_spatial" in status
        assert "using_legacy" in status
        assert "feature_flags" in status

    @pytest.mark.asyncio
    async def test_router_delegation_error_handling(self):
        """Test that router handles missing integration gracefully"""
        from services.integrations.calendar import CalendarIntegrationRouter

        with patch.dict(
            os.environ, {"USE_SPATIAL_CALENDAR": "false", "ALLOW_LEGACY_CALENDAR": "false"}
        ):
            router = CalendarIntegrationRouter()

            # Should raise RuntimeError when no integration available
            with pytest.raises(RuntimeError, match="No calendar integration available"):
                await router.authenticate()


class TestGoogleCalendarMCPAdapter:
    """Test GoogleCalendarMCPAdapter functionality"""

    def test_adapter_inherits_base_spatial_adapter(self):
        """Test that GoogleCalendarMCPAdapter inherits from BaseSpatialAdapter"""
        try:
            from services.integrations.spatial_adapter import BaseSpatialAdapter
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            adapter = GoogleCalendarMCPAdapter()
            assert isinstance(adapter, BaseSpatialAdapter)
        except ImportError:
            pytest.skip("Google Calendar libraries not available")

    def test_adapter_initialization(self):
        """Test adapter initializes with correct configuration"""
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            adapter = GoogleCalendarMCPAdapter()

            assert adapter is not None
            assert hasattr(adapter, "_credentials")
            assert hasattr(adapter, "_service")
            assert hasattr(adapter, "_calendar_id")
            assert hasattr(adapter, "_circuit_open")
        except ImportError:
            pytest.skip("Google Calendar libraries not available")

    def test_adapter_configuration_env_vars(self):
        """Test adapter reads configuration from environment variables"""
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            with patch.dict(
                os.environ,
                {
                    "GOOGLE_CLIENT_SECRETS_FILE": "test_credentials.json",
                    "GOOGLE_TOKEN_FILE": "test_token.json",
                },
            ):
                adapter = GoogleCalendarMCPAdapter()

                assert adapter._client_secrets_file == "test_credentials.json"
                # Issue #734 (multi-tenancy): the config service user-scopes any token
                # filename that doesn't already contain the user_id, to prevent one
                # user's token file from colliding with another's. No user_id passed
                # here -> the adapter defaults to "system", so the env var's raw
                # "test_token.json" is transformed to "test_token_system.json".
                assert adapter._token_file == "test_token_system.json"
        except ImportError:
            pytest.skip("Google Calendar libraries not available")

    def test_adapter_has_calendar_methods(self):
        """Test adapter has all required calendar methods"""
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            adapter = GoogleCalendarMCPAdapter()

            assert hasattr(adapter, "authenticate")
            assert hasattr(adapter, "get_todays_events")
            assert hasattr(adapter, "get_current_meeting")
            assert hasattr(adapter, "get_next_meeting")
            assert hasattr(adapter, "get_free_time_blocks")
            assert hasattr(adapter, "get_temporal_summary")
            assert hasattr(adapter, "health_check")
        except ImportError:
            pytest.skip("Google Calendar libraries not available")

    def test_adapter_has_spatial_methods(self):
        """Test adapter has BaseSpatialAdapter methods"""
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            adapter = GoogleCalendarMCPAdapter()

            # Inherited from BaseSpatialAdapter
            assert hasattr(adapter, "map_to_position")
            assert hasattr(adapter, "map_from_position")
            assert hasattr(adapter, "get_context")
            assert hasattr(adapter, "store_mapping")
            assert hasattr(adapter, "get_mapping_stats")
        except ImportError:
            pytest.skip("Google Calendar libraries not available")

    @pytest.mark.asyncio
    async def test_adapter_health_check(self):
        """Test adapter health check method"""
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            adapter = GoogleCalendarMCPAdapter()
            health = await adapter.health_check()

            assert isinstance(health, dict)
            assert "adapter" in health
            assert "dependencies_available" in health
            assert "authenticated" in health
            assert "circuit_open" in health
            assert health["adapter"] == "google_calendar_mcp"
        except ImportError:
            pytest.skip("Google Calendar libraries not available")

    def test_adapter_circuit_breaker_config(self):
        """Test adapter has circuit breaker configuration"""
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            adapter = GoogleCalendarMCPAdapter()

            assert hasattr(adapter, "_circuit_open")
            assert hasattr(adapter, "_error_count")
            assert hasattr(adapter, "_circuit_timeout")
            assert adapter._circuit_timeout == 300  # 5 minutes
        except ImportError:
            pytest.skip("Google Calendar libraries not available")


class TestCalendarFeatureFlags:
    """Test Calendar feature flag integration"""

    def test_use_spatial_calendar_default(self):
        """Test USE_SPATIAL_CALENDAR defaults to true"""
        from services.infrastructure.config.feature_flags import FeatureFlags

        # Clear any existing env var
        with patch.dict(os.environ, {}, clear=True):
            result = FeatureFlags.should_use_spatial_calendar()
            assert result is True

    def test_use_spatial_calendar_enabled(self):
        """Test USE_SPATIAL_CALENDAR=true"""
        from services.infrastructure.config.feature_flags import FeatureFlags

        with patch.dict(os.environ, {"USE_SPATIAL_CALENDAR": "true"}):
            result = FeatureFlags.should_use_spatial_calendar()
            assert result is True

    def test_use_spatial_calendar_disabled(self):
        """Test USE_SPATIAL_CALENDAR=false"""
        from services.infrastructure.config.feature_flags import FeatureFlags

        with patch.dict(os.environ, {"USE_SPATIAL_CALENDAR": "false"}):
            result = FeatureFlags.should_use_spatial_calendar()
            assert result is False

    def test_allow_legacy_calendar_default(self):
        """Test ALLOW_LEGACY_CALENDAR defaults to false"""
        from services.infrastructure.config.feature_flags import FeatureFlags

        # Clear any existing env var
        with patch.dict(os.environ, {}, clear=True):
            result = FeatureFlags.is_legacy_calendar_allowed()
            assert result is False

    def test_allow_legacy_calendar_enabled(self):
        """Test ALLOW_LEGACY_CALENDAR=true"""
        from services.infrastructure.config.feature_flags import FeatureFlags

        with patch.dict(os.environ, {"ALLOW_LEGACY_CALENDAR": "true"}):
            result = FeatureFlags.is_legacy_calendar_allowed()
            assert result is True


class TestCalendarSpatialContext:
    """Test Calendar spatial context extraction"""

    def test_spatial_context_calendar_specific(self):
        """Test that Calendar adapter extracts calendar-specific spatial context"""
        try:
            from services.mcp.consumer.google_calendar_adapter import GoogleCalendarMCPAdapter

            adapter = GoogleCalendarMCPAdapter()

            # Test context extraction with calendar-specific fields
            context = {
                "meeting_type": "standup",
                "duration_minutes": 30,
                "attendee_count": 5,
                "location": "Zoom",
            }

            spatial_context = adapter._extract_spatial_context(context)

            # Check calendar-specific fields are preserved
            assert spatial_context["meeting_type"] == "standup"
            assert spatial_context["duration_minutes"] == 30
            assert spatial_context["attendee_count"] == 5
            assert spatial_context["location"] == "Zoom"

            # Check default spatial attributes
            assert spatial_context["territory_id"] == "calendar"
            assert spatial_context["room_id"] == "events"
            assert "path_id" in spatial_context
        except ImportError:
            pytest.skip("Google Calendar libraries not available")


class TestCalendarIntegrationUsage:
    """Test Calendar integration is used in production features"""

    def test_calendar_used_in_morning_standup(self):
        """Test that Calendar integration is used by the standup feature.

        #1289 (2026-06-21) retired the old MorningStandupWorkflow engine that
        `services.features.morning_standup` used to house — that module is now
        just back-compat re-exports (StandupItem/StandupResult), with zero
        Calendar reference. The honest replacement, `services.standup.assembler`,
        is where CalendarIntegrationRouter actually lives now (StandupCalendarProvider).
        """
        import inspect

        from services.standup import assembler

        source = inspect.getsource(assembler)
        assert "CalendarIntegrationRouter" in source

    def test_calendar_used_in_canonical_handlers(self):
        """Test that Calendar integration is imported in canonical handlers"""
        # Check that canonical_handlers imports CalendarIntegrationRouter
        import inspect

        from services.intent_service import canonical_handlers

        source = inspect.getsource(canonical_handlers)
        assert "CalendarIntegrationRouter" in source
