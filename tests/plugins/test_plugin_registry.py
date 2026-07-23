"""
Plugin Registry Tests

Tests for PluginRegistry lifecycle and operations.
"""

from typing import Any, Dict, Optional

import pytest
from fastapi import APIRouter

from services.plugins import (
    PiperPlugin,
    PluginMetadata,
    PluginRegistry,
    get_plugin_registry,
    reset_plugin_registry,
)


@pytest.fixture
def fresh_registry():
    """Create fresh registry for each test"""
    reset_plugin_registry()
    return get_plugin_registry()


@pytest.fixture
def sample_plugin():
    """Sample plugin for testing"""

    class SamplePlugin(PiperPlugin):
        def get_metadata(self):
            return PluginMetadata(
                name="sample",
                version="1.0.0",
                description="Sample plugin",
                author="Test",
                capabilities=["routes"],
                dependencies=[],
            )

        def get_router(self):
            return None

        def is_configured(self):
            return True

        async def initialize(self):
            pass

        async def shutdown(self):
            pass

        def get_status(self):
            return {"status": "ok"}

    return SamplePlugin()


class TestPluginRegistry:
    """Tests for PluginRegistry class"""

    def test_registry_creation(self, fresh_registry):
        """Test registry can be created"""
        assert fresh_registry is not None
        assert fresh_registry.get_plugin_count() == 0

    def test_singleton_pattern(self):
        """Test registry is singleton"""
        r1 = get_plugin_registry()
        r2 = get_plugin_registry()
        assert r1 is r2

    def test_register_plugin(self, fresh_registry, sample_plugin):
        """Test plugin registration"""
        fresh_registry.register(sample_plugin)
        assert fresh_registry.get_plugin_count() == 1
        assert "sample" in fresh_registry.list_plugins()

    def test_register_duplicate_fails(self, fresh_registry, sample_plugin):
        """Test duplicate registration fails"""
        fresh_registry.register(sample_plugin)
        with pytest.raises(ValueError, match="already registered"):
            fresh_registry.register(sample_plugin)

    def test_get_plugin(self, fresh_registry, sample_plugin):
        """Test getting plugin by name"""
        fresh_registry.register(sample_plugin)
        plugin = fresh_registry.get_plugin("sample")
        assert plugin is sample_plugin

    def test_get_nonexistent_plugin(self, fresh_registry):
        """Test getting nonexistent plugin returns None"""
        plugin = fresh_registry.get_plugin("nonexistent")
        assert plugin is None

    def test_unregister_plugin(self, fresh_registry, sample_plugin):
        """Test plugin unregistration"""
        fresh_registry.register(sample_plugin)
        result = fresh_registry.unregister("sample")
        assert result is True
        assert fresh_registry.get_plugin_count() == 0

    @pytest.mark.asyncio
    async def test_initialize_all(self, fresh_registry, sample_plugin):
        """Test initializing all plugins"""
        fresh_registry.register(sample_plugin)
        results = await fresh_registry.initialize_all()
        assert results["sample"] is True
        assert fresh_registry.is_initialized()

    @pytest.mark.asyncio
    async def test_shutdown_all(self, fresh_registry, sample_plugin):
        """Test shutting down all plugins"""
        fresh_registry.register(sample_plugin)
        await fresh_registry.initialize_all()
        results = await fresh_registry.shutdown_all()
        assert results["sample"] is True
        assert not fresh_registry.is_initialized()

    def test_get_status_all(self, fresh_registry, sample_plugin):
        """Test getting status of all plugins"""
        fresh_registry.register(sample_plugin)
        status = fresh_registry.get_status_all()
        assert "sample" in status
        assert status["sample"]["status"] == "ok"


class TestPluginDiscovery:
    """Tests for plugin discovery mechanism"""

    def test_discover_plugins_finds_all(self, fresh_registry):
        """Test discovery finds all 5 plugins (4 existing + demo)"""
        available = fresh_registry.discover_plugins()

        assert len(available) == 5
        assert "slack" in available
        assert "github" in available
        assert "notion" in available
        assert "calendar" in available
        assert "demo" in available

    def test_discover_plugins_returns_dict(self, fresh_registry):
        """Test discovery returns dict of name to module path"""
        available = fresh_registry.discover_plugins()

        assert isinstance(available, dict)
        for name, module_path in available.items():
            assert isinstance(name, str)
            assert isinstance(module_path, str)
            assert "services.integrations" in module_path

    def test_discover_plugins_correct_module_paths(self, fresh_registry):
        """Test discovery returns correct module paths"""
        available = fresh_registry.discover_plugins()

        # Check expected format
        assert available["slack"] == "services.integrations.slack.slack_plugin"
        assert available["github"] == "services.integrations.github.github_plugin"
        assert available["notion"] == "services.integrations.notion.notion_plugin"
        assert available["calendar"] == "services.integrations.calendar.calendar_plugin"

    def test_discover_plugins_does_not_load(self, fresh_registry):
        """Test discovery does not automatically register plugins"""
        # Start with clean registry
        assert fresh_registry.get_plugin_count() == 0

        # Discovery should not register plugins
        available = fresh_registry.discover_plugins()

        # Registry should still be empty
        assert fresh_registry.get_plugin_count() == 0
        # But we found 5 available plugins (4 existing + demo)
        assert len(available) == 5

    def test_discover_plugins_logs_results(self, fresh_registry, caplog):
        """Test discovery logs what it finds"""
        import logging

        caplog.set_level(logging.INFO)

        available = fresh_registry.discover_plugins()

        assert "Discovery complete" in caplog.text
        assert f"found {len(available)} plugin(s)" in caplog.text


class TestPluginLoading:
    """Tests for dynamic plugin loading"""

    def test_load_plugin_success(self, fresh_registry):
        """Test loading a valid plugin"""
        # Discover plugins first
        available = fresh_registry.discover_plugins()

        # Load slack plugin
        success = fresh_registry.load_plugin("slack", available["slack"])

        assert success is True
        assert "slack" in fresh_registry.list_plugins()

    def test_load_plugin_registers_automatically(self, fresh_registry):
        """Test that loading triggers auto-registration"""
        available = fresh_registry.discover_plugins()

        # Registry should be empty before loading
        assert fresh_registry.get_plugin_count() == 0

        # Load plugin
        fresh_registry.load_plugin("github", available["github"])

        # Plugin should now be registered
        assert fresh_registry.get_plugin_count() == 1
        assert fresh_registry.get_plugin("github") is not None

    def test_load_multiple_plugins(self, fresh_registry):
        """Test loading multiple plugins"""
        available = fresh_registry.discover_plugins()

        # Load all plugins
        results = {}
        for name, module_path in available.items():
            results[name] = fresh_registry.load_plugin(name, module_path)

        # All should succeed (including already-loaded plugins)
        assert all(results.values()), f"Failed plugins: {[k for k, v in results.items() if not v]}"
        # Should have 4 plugins total (some may have been loaded by previous tests)
        assert fresh_registry.get_plugin_count() >= 4

    def test_load_plugin_invalid_module(self, fresh_registry):
        """Test loading with invalid module path"""
        success = fresh_registry.load_plugin("fake", "services.integrations.fake.fake_plugin")

        assert success is False
        assert "fake" not in fresh_registry.list_plugins()

    def test_load_plugin_already_loaded(self, fresh_registry):
        """Test loading same plugin twice"""
        available = fresh_registry.discover_plugins()

        # Load once
        success1 = fresh_registry.load_plugin("notion", available["notion"])
        count1 = fresh_registry.get_plugin_count()

        # Load again
        success2 = fresh_registry.load_plugin("notion", available["notion"])
        count2 = fresh_registry.get_plugin_count()

        # Both should succeed, count shouldn't increase
        assert success1 is True
        assert success2 is True
        assert count1 == count2  # No duplicate registration

    def test_load_plugin_logs_errors(self, fresh_registry, caplog):
        """Test that load failures are logged"""
        import logging

        caplog.set_level(logging.ERROR)

        fresh_registry.load_plugin("invalid", "invalid.module.path")

        assert "Failed to import plugin" in caplog.text


class TestPluginConfig:
    """Tests for plugin configuration"""

    def test_get_enabled_plugins_from_config(self, fresh_registry):
        """Test reading enabled plugins from config"""
        enabled = fresh_registry.get_enabled_plugins()

        # Should read from PIPER.user.md
        assert isinstance(enabled, list)
        # #1452: superset semantics — the registry grows (demo joined the
        # original four); pin the core set, not the count.
        assert len(enabled) >= 4
        assert "slack" in enabled
        assert "github" in enabled
        assert "notion" in enabled
        assert "calendar" in enabled

    def test_load_enabled_plugins_loads_all(self, fresh_registry):
        """Test load_enabled_plugins loads all configured plugins"""
        results = fresh_registry.load_enabled_plugins()

        assert len(results) >= 4
        assert all(results.values())  # All should succeed
        assert fresh_registry.get_plugin_count() >= 4

    def test_load_enabled_plugins_returns_results(self, fresh_registry):
        """Test load_enabled_plugins returns success status"""
        results = fresh_registry.load_enabled_plugins()

        assert isinstance(results, dict)
        for name, success in results.items():
            assert isinstance(name, str)
            assert isinstance(success, bool)
            assert name in ["slack", "github", "notion", "calendar", "demo"]
