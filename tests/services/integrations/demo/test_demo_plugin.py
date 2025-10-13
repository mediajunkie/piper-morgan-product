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
        assert router.prefix == "/api/integrations/demo"
        assert "demo" in router.tags

    def test_plugin_is_configured(self):
        """Test plugin configuration check"""
        plugin = DemoPlugin()

        # Demo plugin should always be configured
        assert plugin.is_configured() is True

    @pytest.mark.asyncio
    async def test_plugin_lifecycle(self):
        """Test plugin initialization and shutdown"""
        plugin = DemoPlugin()

        # Should not raise errors
        await plugin.initialize()
        await plugin.shutdown()

    def test_plugin_status(self):
        """Test plugin status reporting"""
        plugin = DemoPlugin()
        status = plugin.get_status()

        assert "configured" in status
        assert "router_prefix" in status
        assert "routes" in status
        assert status["configured"] is True
        assert status["router_prefix"] == "/api/integrations/demo"
        assert status["routes"] >= 3  # At least health, echo, status

    def test_router_has_expected_routes(self):
        """Test router has all expected endpoints"""
        plugin = DemoPlugin()
        router = plugin.get_router()

        # Get all route paths
        paths = [route.path for route in router.routes]

        assert "/api/integrations/demo/health" in paths
        assert "/api/integrations/demo/echo" in paths
        assert "/api/integrations/demo/status" in paths


class TestDemoConfigService:
    """Test suite for Demo config service"""

    def test_config_service_creation(self):
        """Test config service can be created"""
        config = DemoConfigService()
        assert config is not None

    def test_config_is_configured(self):
        """Test is_configured method"""
        config = DemoConfigService()
        # Demo should always be configured
        assert config.is_configured() is True

    def test_config_get_endpoint(self):
        """Test endpoint retrieval"""
        config = DemoConfigService()
        endpoint = config.get_endpoint()

        assert endpoint is not None
        assert isinstance(endpoint, str)
