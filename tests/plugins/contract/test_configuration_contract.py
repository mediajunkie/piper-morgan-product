"""Contract tests for plugin configuration

Verifies that plugins handle configuration correctly and provide
appropriate status information.
"""

import time

import pytest


@pytest.mark.contract
class TestConfigurationContract:
    """Verify plugin configuration contracts"""

    def test_is_configured_is_fast(self, plugin_instance):
        """is_configured() should be fast (no I/O)"""
        # Measure time for 100 calls
        start = time.perf_counter()
        for _ in range(100):
            plugin_instance.is_configured()
        elapsed = time.perf_counter() - start

        # Should complete 100 calls in < 100ms (< 1ms per call)
        assert elapsed < 0.1, f"is_configured() too slow: {elapsed*1000:.2f}ms for 100 calls"

    def test_configuration_status_consistency(self, plugin_instance):
        """is_configured() and get_status() should be consistent.

        #1547: user-scoped plugins report `configured: None` in get_status()
        (unknowable without a user, #784) — None is exempt from the equality
        check; a boolean must still match is_configured().
        """
        is_configured = plugin_instance.is_configured()
        status = plugin_instance.get_status()

        assert "configured" in status, "Status must include 'configured' field"
        if status["configured"] is not None:
            assert (
                status["configured"] == is_configured
            ), "is_configured() and status['configured'] must match"

    def test_status_includes_router_info(self, plugin_instance):
        """get_status() should include router information"""
        status = plugin_instance.get_status()

        # Status should include some router information
        # (exact field names may vary, but should have something about router)
        router_fields = ["router_prefix", "router", "routes", "prefix"]
        has_router_info = any(field in status for field in router_fields)

        assert (
            has_router_info
        ), f"Status should include router info, got fields: {list(status.keys())}"

    def test_router_available_when_configured(self, plugin_instance):
        """Router should be available regardless of configuration status"""
        # Even if not configured, router should be available
        # (it just might return error responses)
        router = plugin_instance.get_router()
        assert router is not None, "Router should always be available"
