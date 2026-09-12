"""Tests for Demo plugin

This demonstrates standard testing patterns for plugins.
"""

import pytest

from services.integrations.demo.config_service import DemoConfigService
from services.integrations.demo.demo_plugin import DemoPlugin


class TestDemoPlugin:
    """Test suite for Demo plugin"""

    def test_plugin_metadata(self):
        """Test plugin metadata is correct"""
        plugin = DemoPlugin()
        metadata = plugin.get_metadata()

        assert metadata.name == "demo"
        assert metadata.version == "1.0.0"
        assert metadata.description == "Demo integration template for developers"
        assert "routes" in metadata.capabilities

    def test_plugin_has_router(self):
        """Test plugin provides router"""
        plugin = DemoPlugin()
        router = plugin.get_router()

        assert router is not None
        assert router.prefix == "/api/v1/integrations/demo"
        assert "demo" in router.tags

    def test_plugin_is_configured(self):
        """Test plugin configuration check

        Demo plugin should be disabled by default to prevent it from appearing
        in production identity responses. Set DEMO_ENABLED=true to enable.
        """
        plugin = DemoPlugin()

        # Demo plugin should be disabled by default (bead piper-morgan-7ik)
        # This prevents it from appearing in user-facing identity responses
        assert plugin.is_configured() is False

    @pytest.mark.asyncio
    async def test_plugin_lifecycle(self):
        """Test plugin initialization and shutdown"""
        plugin = DemoPlugin()

        # Should not raise errors
        await plugin.initialize()
        await plugin.shutdown()

    def test_plugin_status(self):
        """Test plugin status reporting

        Status should report configured=False by default (bead piper-morgan-7ik).
        """
        plugin = DemoPlugin()
        status = plugin.get_status()

        assert "configured" in status
        assert "router_prefix" in status
        assert "routes" in status
        # Demo plugin disabled by default - won't appear in identity responses
        assert status["configured"] is False
        assert status["router_prefix"] == "/api/v1/integrations/demo"
        assert (
            status["routes"] >= 3
        )  # At least health, echo, status  # At least health, echo, status

    def test_router_has_expected_routes(self):
        """Test router has all expected endpoints"""
        plugin = DemoPlugin()
        router = plugin.get_router()

        # Get all route paths
        paths = [route.path for route in router.routes]

        assert "/api/v1/integrations/demo/health" in paths
        assert "/api/v1/integrations/demo/echo" in paths
        assert "/api/v1/integrations/demo/status" in paths


class TestDemoConfigService:
    """Test suite for Demo config service"""

    def test_config_service_creation(self):
        """Test config service can be created"""
        config = DemoConfigService()
        assert config is not None

    def test_config_is_configured(self):
        """Test is_configured method

        Demo plugin is disabled by default (bead piper-morgan-7ik).
        Set DEMO_ENABLED=true in environment to enable for development.
        """
        config = DemoConfigService()
        # Demo should be disabled by default to prevent showing in identity responses
        assert config.is_configured() is False

    def test_config_get_endpoint(self):
        """Test endpoint retrieval"""
        config = DemoConfigService()
        endpoint = config.get_endpoint()

        assert endpoint is not None
        assert isinstance(endpoint, str)
