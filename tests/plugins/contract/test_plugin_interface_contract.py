"""Contract tests for PiperPlugin interface compliance

These tests verify that ALL plugins correctly implement the PiperPlugin
interface. Each test is automatically run against every registered plugin.
"""

from typing import Any, Dict

import pytest
from fastapi import APIRouter

from services.plugins.plugin_interface import PiperPlugin, PluginMetadata


@pytest.mark.contract
class TestPluginInterfaceContract:
    """Verify all plugins implement PiperPlugin interface correctly"""

    def test_plugin_implements_interface(self, plugin_instance):
        """Every plugin must be instance of PiperPlugin"""
        assert isinstance(
            plugin_instance, PiperPlugin
        ), f"Plugin {plugin_instance} does not implement PiperPlugin"

    def test_get_metadata_returns_metadata(self, plugin_instance):
        """get_metadata() must return PluginMetadata instance"""
        metadata = plugin_instance.get_metadata()
        assert isinstance(
            metadata, PluginMetadata
        ), f"get_metadata() must return PluginMetadata, got {type(metadata)}"

    def test_metadata_has_required_fields(self, plugin_instance):
        """Metadata must have all required fields populated"""
        metadata = plugin_instance.get_metadata()

        # Required fields must be non-empty strings
        assert metadata.name, "Metadata must have non-empty name"
        assert metadata.version, "Metadata must have non-empty version"
        assert metadata.description, "Metadata must have non-empty description"
        assert metadata.author, "Metadata must have non-empty author"

        # Capabilities must be a list (can be empty)
        assert isinstance(
            metadata.capabilities, list
        ), f"Capabilities must be list, got {type(metadata.capabilities)}"

    def test_metadata_version_format(self, plugin_instance):
        """Version should follow semantic versioning (X.Y.Z)"""
        metadata = plugin_instance.get_metadata()
        version = metadata.version

        # Check semver format (simple check for X.Y.Z)
        parts = version.split(".")
        assert len(parts) == 3, f"Version should be X.Y.Z format, got {version}"

        # Each part should be numeric
        for part in parts:
            assert part.isdigit(), f"Version parts should be numeric, got {version}"

    def test_get_router_returns_router(self, plugin_instance):
        """get_router() must return APIRouter instance"""
        router = plugin_instance.get_router()
        assert isinstance(
            router, APIRouter
        ), f"get_router() must return APIRouter, got {type(router)}"

    def test_router_has_prefix(self, plugin_instance):
        """Router must have a prefix defined"""
        router = plugin_instance.get_router()
        assert router.prefix, "Router must have non-empty prefix"
        assert router.prefix.startswith(
            "/"
        ), f"Router prefix must start with '/', got {router.prefix}"

    def test_router_has_routes(self, plugin_instance):
        """Router may be empty but must never serve a constant-false /status.

        #1547 (audit F5): the four real plugins' only route was
        ``GET /status`` emitting ``configured: false`` forever (#784) — deleted.
        An empty router is the honest state until a plugin grows real routes;
        what's enforced now is that no plugin reintroduces a /status sub-route
        (per-user truth lives at /api/v1/integrations/health).
        """
        if plugin_instance.get_metadata().name == "demo":
            # Demo's /status is env-fed (DEMO_ENABLED) and truthful at plugin
            # level; demo is excluded from user-facing surfaces structurally
            # (IntegrationStatusService known set), not by route deletion.
            return
        router = plugin_instance.get_router()
        paths = [getattr(r, "path", "") for r in router.routes]
        assert not any(
            p.endswith("/status") and router.prefix.startswith("/api/v1/integrations/")
            for p in paths
        ), "Plugin /status sub-routes are retired (#1547 F5) — do not reintroduce"

    def test_is_configured_returns_bool(self, plugin_instance):
        """is_configured() must return boolean"""
        result = plugin_instance.is_configured()
        assert isinstance(result, bool), f"is_configured() must return bool, got {type(result)}"

    def test_get_status_returns_dict(self, plugin_instance):
        """get_status() must return dictionary"""
        status = plugin_instance.get_status()
        assert isinstance(status, dict), f"get_status() must return dict, got {type(status)}"

    def test_status_has_configured_field(self, plugin_instance):
        """Status dict should include 'configured' field.

        #1547: `configured` may be None — configuration is user-scoped and
        unknowable at plugin level (#784), so user-scoped plugins report None
        (with a `configured_note` pointing at IntegrationStatusService) rather
        than fabricating a boolean. A boolean remains valid for plugins whose
        configuration IS knowable at plugin level (e.g. env-fed demo).
        """
        status = plugin_instance.get_status()
        assert "configured" in status, "Status dict must include 'configured' field"
        assert isinstance(status["configured"], (bool, type(None))), (
            "Status 'configured' field must be boolean or None (user-scoped)"
        )
        if status["configured"] is None:
            assert "configured_note" in status, (
                "A None 'configured' must carry a 'configured_note' naming the "
                "canonical status source (#1547)"
            )
