"""Tests for GitHub MCP Router Integration.

CORE-MCP-MIGRATION #198: Test GitHubIntegrationRouter MCP adapter integration.

Verifies:
- MCP adapter initializes when USE_MCP_GITHUB=true
- Router prefers MCP adapter when available
- Graceful fallback to GitHubSpatialIntelligence
- Feature flag control works correctly
"""

import os
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.integrations.github.config_service import GitHubConfigService
from services.integrations.github.github_integration_router import GitHubIntegrationRouter


class TestGitHubMCPRouterIntegration:
    """Test GitHubIntegrationRouter MCP adapter integration."""

    def test_router_initializes_with_mcp_adapter_by_default(self):
        """Test router initializes with MCP adapter when USE_MCP_GITHUB=true (default)."""
        # Default is true
        router = GitHubIntegrationRouter()

        # Should have MCP adapter
        assert router.mcp_adapter is not None, "MCP adapter should be initialized by default"
        # Should also have spatial fallback
        assert router.spatial_github is not None, "Spatial fallback should be initialized"

    def test_router_skips_mcp_when_disabled(self):
        """Test router skips MCP adapter when USE_MCP_GITHUB=false."""
        with patch.dict(os.environ, {"USE_MCP_GITHUB": "false"}):
            router = GitHubIntegrationRouter()

            # Should NOT have MCP adapter
            assert router.mcp_adapter is None, "MCP adapter should not initialize when disabled"
            # Should have spatial
            assert router.spatial_github is not None, "Spatial should still initialize"

    def test_router_accepts_config_service_injection(self):
        """Test router accepts config service for dependency injection."""
        config_service = GitHubConfigService()
        router = GitHubIntegrationRouter(config_service)

        assert router.config_service is config_service
        assert router.mcp_adapter is not None

    def test_get_integration_prefers_mcp_adapter(self):
        """Test _get_integration returns MCP adapter when available."""
        router = GitHubIntegrationRouter()

        # Should prefer MCP adapter
        integration = router._get_integration("test_operation")

        # Verify it's the MCP adapter (check class name)
        assert integration is router.mcp_adapter, "Should return MCP adapter when available"

    def test_get_integration_falls_back_to_spatial(self):
        """Test _get_integration falls back to spatial when MCP not available."""
        with patch.dict(os.environ, {"USE_MCP_GITHUB": "false"}):
            router = GitHubIntegrationRouter()

            # Should use spatial
            integration = router._get_integration("test_operation")

            assert (
                integration is router.spatial_github
            ), "Should fall back to spatial when MCP disabled"

    def test_get_integration_raises_when_none_available(self):
        """Test _get_integration raises error when no integration available."""
        router = GitHubIntegrationRouter()

        # Manually disable both
        router.mcp_adapter = None
        router.spatial_github = None

        # Should raise RuntimeError
        with pytest.raises(RuntimeError, match="No GitHub integration available"):
            router._get_integration("test_operation")

    def test_integration_status_shows_mcp(self):
        """Test get_integration_status shows MCP adapter status."""
        router = GitHubIntegrationRouter()

        status = router.get_integration_status()

        assert status["mcp_adapter_available"] is True, "Status should show MCP available"
        assert status["using_mcp"] is True, "Status should show using MCP"
        assert status["mcp_migration_complete"] is True, "Status should show migration complete"
        assert "mcp_integration_date" in status["deprecation_timeline"]

    def test_integration_status_without_mcp(self):
        """Test get_integration_status when MCP not available."""
        with patch.dict(os.environ, {"USE_MCP_GITHUB": "false"}):
            router = GitHubIntegrationRouter()

            status = router.get_integration_status()

            assert status["mcp_adapter_available"] is False
            assert status["using_mcp"] is False
            assert status["spatial_available"] is True

    def test_mcp_adapter_has_correct_type(self):
        """Test MCP adapter is GitHubMCPSpatialAdapter instance."""
        router = GitHubIntegrationRouter()

        # Check class name
        assert router.mcp_adapter.__class__.__name__ == "GitHubMCPSpatialAdapter"

    def test_spatial_intelligence_has_correct_type(self):
        """Test spatial intelligence is GitHubSpatialIntelligence instance."""
        router = GitHubIntegrationRouter()

        # Check class name
        assert router.spatial_github.__class__.__name__ == "GitHubSpatialIntelligence"

    def test_graceful_degradation_when_mcp_fails(self):
        """Test graceful fallback to spatial when MCP initialization fails."""
        # Mock MCP adapter to raise exception during import
        # Need to patch where it's imported from
        with patch(
            "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter",
            side_effect=Exception("MCP init failed"),
        ):
            router = GitHubIntegrationRouter()

            # MCP should be None (failed to initialize)
            assert router.mcp_adapter is None, "MCP should be None after init failure"
            # Spatial should still work
            assert router.spatial_github is not None, "Spatial should work as fallback"

class TestGitHubMCPFeatureFlags:
    """Test GitHub MCP feature flag behavior."""

    def test_use_mcp_github_defaults_to_true(self):
        """Test USE_MCP_GITHUB defaults to true."""
        # Clear any env var
        with patch.dict(os.environ, {}, clear=True):
            router = GitHubIntegrationRouter()

            assert router.use_mcp is True, "USE_MCP_GITHUB should default to true"

    def test_use_mcp_github_respects_env_var(self):
        """Test USE_MCP_GITHUB respects environment variable."""
        test_cases = [
            ("true", True),
            ("false", False),
            ("1", True),
            ("0", False),
            ("yes", True),
            ("no", False),
        ]

        for env_value, expected in test_cases:
            with patch.dict(os.environ, {"USE_MCP_GITHUB": env_value}):
                router = GitHubIntegrationRouter()
                assert (
                    router.use_mcp is expected
                ), f"USE_MCP_GITHUB={env_value} should result in {expected}"


class TestGitHubMCPBackwardCompatibility:
    """Test backward compatibility with existing code."""

    def test_router_still_provides_spatial_methods(self):
        """Test router still provides all expected methods for backward compatibility."""
        router = GitHubIntegrationRouter()

        # Verify all expected methods exist
        expected_methods = [
            "get_issue",
            "list_issues",
            "create_issue",
            "update_issue",
            "get_open_issues",
            "get_recent_issues",
            "get_recent_activity",
            "list_repositories",
            "create_pm_issue",
            "get_integration_status",
            "test_connection",
        ]

        for method_name in expected_methods:
            assert hasattr(router, method_name), f"Router should have {method_name} method"
            assert callable(getattr(router, method_name)), f"{method_name} should be callable"

    def test_existing_code_continues_to_work(self):
        """Test existing code using GitHubIntegrationRouter continues to work."""
        # Simulate existing code usage
        router = GitHubIntegrationRouter()

        # Should not raise exceptions
        assert router is not None
        assert router.config_service is not None

        # Status check should work
        status = router.get_integration_status()
        assert status["router_initialized"] is True
