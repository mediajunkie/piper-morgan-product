"""
Integration Tests for GitHub Deprecation Infrastructure
PM-033b-deprecation: Safe 4-week deprecation strategy validation

Tests the feature flag-based switching between GitHubSpatialIntelligence
and legacy GitHub integration during the deprecation timeline.

Test Scenarios:
1. Week 1: Parallel operation with spatial as default
2. Week 2: Deprecation warnings when legacy used
3. Week 3: Legacy disabled by default with emergency rollback
4. Week 4: Spatial-only operation validation

Architecture: ADR-013 MCP+Spatial Integration Pattern compliance
"""

import asyncio
import os
from typing import Any, Dict
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.infrastructure.config.feature_flags import FeatureFlags
from services.integrations.github.github_integration_router import GitHubIntegrationRouter


class TestGitHubDeprecationInfrastructure:
    """Test suite for GitHub deprecation infrastructure and feature flag handling"""

    @pytest.fixture
    def mock_spatial_github(self):
        """Mock GitHubSpatialIntelligence for testing"""
        mock = AsyncMock()
        mock.initialize = AsyncMock()
        mock.get_issue = AsyncMock(
            return_value={
                "number": 123,
                "title": "Test Issue",
                "state": "open",
                "created_at": "2025-08-12T10:00:00Z",
                "updated_at": "2025-08-12T12:00:00Z",
                "repository": {"owner": "test", "name": "repo"},
            }
        )
        mock.create_spatial_context = AsyncMock(
            return_value=MagicMock(
                attention_level="high",
                emotional_valence="neutral",
                navigation_intent="investigate",
                external_context={"test": "spatial_data"},
            )
        )
        return mock

    @pytest.fixture
    def mock_legacy_github(self):
        """Mock legacy GitHubAgent for testing"""
        mock = AsyncMock()
        mock.initialize = AsyncMock()
        mock.get_issue = AsyncMock(
            return_value={"number": 123, "title": "Test Issue (Legacy)", "state": "open"}
        )
        mock.create_issue = AsyncMock(
            return_value={"number": 124, "title": "Created Issue (Legacy)", "state": "open"}
        )
        return mock

    # WEEK 1 TESTS: Parallel Operation
    @pytest.mark.asyncio
    async def test_week1_spatial_integration_default(self, mock_spatial_github):
        """Test Week 1: Spatial integration is used by default when both available"""

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "true",
                "GITHUB_DEPRECATION_WARNINGS": "false",
            },
        ):
            with patch(
                "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
                return_value=mock_spatial_github,
            ):
                router = GitHubIntegrationRouter()
                await router.initialize()

                # Should use spatial integration
                result = await router.get_issue("test-repo", 123)

                assert "spatial_intelligence" in result
                assert result["spatial_intelligence"]["attention_level"] == "high"
                mock_spatial_github.get_issue.assert_called_once_with("test-repo", 123)

    @pytest.mark.asyncio
    async def test_week1_legacy_fallback_available(self, mock_spatial_github, mock_legacy_github):
        """Test Week 1: Legacy fallback works when spatial fails"""

        # Make spatial integration fail
        mock_spatial_github.get_issue.side_effect = Exception("Spatial failed")

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "true",
                "GITHUB_DEPRECATION_WARNINGS": "false",
            },
        ):
            with (
                patch(
                    "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
                    return_value=mock_spatial_github,
                ),
                patch(
                    "services.integrations.github.github_agent.GitHubAgent",
                    return_value=mock_legacy_github,
                ),
            ):
                router = GitHubIntegrationRouter()
                await router.initialize()

                result = await router.get_issue("test-repo", 123)

                # Should fall back to legacy
                assert result["title"] == "Test Issue (Legacy)"
                assert "spatial_intelligence" not in result
                mock_legacy_github.get_issue.assert_called_once_with("test-repo", 123)

    @pytest.mark.asyncio
    async def test_week1_parallel_operation_status(self):
        """Test Week 1: Integration status shows both integrations available"""

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "true",
                "GITHUB_DEPRECATION_WARNINGS": "false",
            },
        ):
            with (
                patch("services.integrations.spatial.github_spatial.GitHubSpatialIntelligence"),
                patch("services.integrations.github.github_agent.GitHubAgent"),
            ):
                router = GitHubIntegrationRouter()
                status = router.get_integration_status()

                assert status["feature_flags"]["use_spatial"] == True
                assert status["feature_flags"]["allow_legacy"] == True
                assert status["feature_flags"]["warn_deprecation"] == False
                assert status["integrations"]["spatial_available"] == True
                assert status["integrations"]["legacy_available"] == True
                assert status["preferred_integration"] == "spatial"

    # WEEK 2 TESTS: Deprecation Warnings
    @pytest.mark.asyncio
    async def test_week2_deprecation_warnings_enabled(self, mock_legacy_github, caplog):
        """Test Week 2: Deprecation warnings appear when legacy used"""

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "false",  # Force legacy usage
                "ALLOW_LEGACY_GITHUB": "true",
                "GITHUB_DEPRECATION_WARNINGS": "true",
            },
        ):
            with patch(
                "services.integrations.github.github_agent.GitHubAgent",
                return_value=mock_legacy_github,
            ):
                router = GitHubIntegrationRouter()
                await router.initialize()

                await router.get_issue("test-repo", 123)

                # Should show deprecation warning
                assert "DEPRECATION WARNING" in caplog.text
                assert "Legacy GitHub integration used" in caplog.text

    # WEEK 3 TESTS: Legacy Disabled by Default
    @pytest.mark.asyncio
    async def test_week3_legacy_disabled_by_default(self, mock_spatial_github):
        """Test Week 3: Legacy integration disabled by default"""

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "false",  # Week 3: disabled by default
                "GITHUB_DEPRECATION_WARNINGS": "true",
            },
        ):
            with patch(
                "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
                return_value=mock_spatial_github,
            ):
                router = GitHubIntegrationRouter()
                status = router.get_integration_status()

                assert status["feature_flags"]["allow_legacy"] == False
                assert status["integrations"]["legacy_available"] == False
                assert status["preferred_integration"] == "spatial"

    @pytest.mark.asyncio
    async def test_week3_emergency_rollback_capability(self, mock_legacy_github):
        """Test Week 3: Emergency rollback to legacy still possible"""

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "false",  # Emergency: disable spatial
                "ALLOW_LEGACY_GITHUB": "true",  # Emergency: re-enable legacy
                "GITHUB_DEPRECATION_WARNINGS": "true",
            },
        ):
            with patch(
                "services.integrations.github.github_agent.GitHubAgent",
                return_value=mock_legacy_github,
            ):
                router = GitHubIntegrationRouter()
                await router.initialize()

                result = await router.get_issue("test-repo", 123)

                # Should work with legacy as emergency fallback
                assert result["title"] == "Test Issue (Legacy)"
                mock_legacy_github.get_issue.assert_called_once()

    # WEEK 4 TESTS: Spatial-Only Operation
    @pytest.mark.asyncio
    async def test_week4_spatial_only_operation(self, mock_spatial_github):
        """Test Week 4: Only spatial integration available (legacy removed)"""

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "false",  # Week 4: legacy removed
                "GITHUB_DEPRECATION_WARNINGS": "false",  # No warnings needed
            },
        ):
            with patch(
                "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
                return_value=mock_spatial_github,
            ):
                router = GitHubIntegrationRouter()
                await router.initialize()

                result = await router.get_issue("test-repo", 123)

                # Should only use spatial integration
                assert "spatial_intelligence" in result
                assert result["spatial_intelligence"]["attention_level"] == "high"
                mock_spatial_github.get_issue.assert_called_once()

    @pytest.mark.asyncio
    async def test_week4_no_fallback_available(self):
        """Test Week 4: Error when spatial fails and no legacy available"""

        mock_failing_spatial = AsyncMock()
        mock_failing_spatial.get_issue.side_effect = Exception("Spatial failed")

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "false",  # Week 4: no fallback
                "GITHUB_DEPRECATION_WARNINGS": "false",
            },
        ):
            with patch(
                "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
                return_value=mock_failing_spatial,
            ):
                router = GitHubIntegrationRouter()
                await router.initialize()

                # Should raise exception with no fallback available
                with pytest.raises(Exception, match="Spatial failed"):
                    await router.get_issue("test-repo", 123)

    # FEATURE FLAG VALIDATION TESTS
    @pytest.mark.asyncio
    async def test_feature_flag_validation(self):
        """Test feature flag parsing and validation"""

        # Test all valid boolean representations
        test_cases = [
            ("true", True),
            ("TRUE", True),
            ("1", True),
            ("yes", True),
            ("on", True),
            ("enabled", True),
            ("false", False),
            ("FALSE", False),
            ("0", False),
            ("no", False),
            ("off", False),
            ("disabled", False),
        ]

        for env_value, expected in test_cases:
            with patch.dict(os.environ, {"USE_SPATIAL_GITHUB": env_value}):
                assert FeatureFlags.should_use_spatial_github() == expected

    # INTEGRATION HEALTH TESTS
    @pytest.mark.asyncio
    async def test_integration_health_monitoring(self, mock_spatial_github, mock_legacy_github):
        """Test integration health status for monitoring"""

        with patch.dict(
            os.environ,
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "true",
                "GITHUB_DEPRECATION_WARNINGS": "false",
            },
        ):
            with (
                patch(
                    "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
                    return_value=mock_spatial_github,
                ),
                patch(
                    "services.integrations.github.github_agent.GitHubAgent",
                    return_value=mock_legacy_github,
                ),
            ):
                router = GitHubIntegrationRouter()
                await router.initialize()

                health = router.get_integration_status()

                # Validate health status structure
                assert "router_initialized" in health
                assert "feature_flags" in health
                assert "integrations" in health
                assert "preferred_integration" in health
                assert "deprecation_timeline" in health

                # Validate deprecation timeline
                timeline = health["deprecation_timeline"]
                assert "week" in timeline
                assert "legacy_removal_date" in timeline
                assert timeline["legacy_removal_date"] == "2025-09-09"

    # PERFORMANCE TESTS
    @pytest.mark.asyncio
    async def test_deprecation_performance_impact(self, mock_spatial_github):
        """Test that deprecation infrastructure has minimal performance impact"""

        with patch(
            "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
            return_value=mock_spatial_github,
        ):
            router = GitHubIntegrationRouter()
            await router.initialize()

            import time

            # Measure performance of multiple operations
            start_time = time.time()
            for i in range(10):
                await router.get_issue("test-repo", i)
            elapsed = time.time() - start_time

            # Should complete 10 operations in under 50ms (5ms per operation)
            assert (
                elapsed < 0.05
            ), f"Performance impact too high: {elapsed*1000:.2f}ms for 10 operations"

    # ERROR HANDLING TESTS
    @pytest.mark.asyncio
    async def test_robust_error_handling(self):
        """Test robust error handling when both integrations fail to initialize"""

        with patch.dict(os.environ, {"USE_SPATIAL_GITHUB": "true", "ALLOW_LEGACY_GITHUB": "true"}):
            with (
                patch(
                    "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
                    side_effect=Exception("Spatial init failed"),
                ),
                patch(
                    "services.integrations.github.github_agent.GitHubAgent",
                    side_effect=Exception("Legacy init failed"),
                ),
            ):
                # Should raise clear error about both integrations failing
                with pytest.raises(
                    RuntimeError, match="Legacy GitHub failed and spatial not available"
                ):
                    router = GitHubIntegrationRouter()

    # COMPREHENSIVE END-TO-END TEST
    @pytest.mark.asyncio
    async def test_comprehensive_deprecation_workflow(
        self, mock_spatial_github, mock_legacy_github
    ):
        """Test complete deprecation workflow from Week 1 to Week 4"""

        test_scenarios = [
            # Week 1: Parallel operation
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "true",
                "GITHUB_DEPRECATION_WARNINGS": "false",
                "expected_integration": "spatial",
                "expected_warnings": False,
            },
            # Week 2: Deprecation warnings
            {
                "USE_SPATIAL_GITHUB": "false",  # Force legacy to test warnings
                "ALLOW_LEGACY_GITHUB": "true",
                "GITHUB_DEPRECATION_WARNINGS": "true",
                "expected_integration": "legacy",
                "expected_warnings": True,
            },
            # Week 3: Legacy disabled by default
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "false",
                "GITHUB_DEPRECATION_WARNINGS": "true",
                "expected_integration": "spatial",
                "expected_warnings": False,
            },
            # Week 4: Spatial only
            {
                "USE_SPATIAL_GITHUB": "true",
                "ALLOW_LEGACY_GITHUB": "false",
                "GITHUB_DEPRECATION_WARNINGS": "false",
                "expected_integration": "spatial",
                "expected_warnings": False,
            },
        ]

        for i, scenario in enumerate(test_scenarios):
            with patch.dict(os.environ, scenario):
                with (
                    patch(
                        "services.integrations.spatial.github_spatial.GitHubSpatialIntelligence",
                        return_value=mock_spatial_github,
                    ),
                    patch(
                        "services.integrations.github.github_agent.GitHubAgent",
                        return_value=mock_legacy_github,
                    ),
                ):
                    router = GitHubIntegrationRouter()
                    await router.initialize()

                    status = router.get_integration_status()
                    result = await router.get_issue("test-repo", 123)

                    # Validate expected behavior for each week
                    if scenario["expected_integration"] == "spatial":
                        assert "spatial_intelligence" in result
                        assert status["preferred_integration"] == "spatial"
                    else:
                        assert "spatial_intelligence" not in result
                        assert status["preferred_integration"] == "legacy"

                    # Reset mocks for next scenario
                    mock_spatial_github.reset_mock()
                    mock_legacy_github.reset_mock()

        print("✅ Complete 4-week deprecation workflow validated successfully")
