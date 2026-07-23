"""
Integration tests for Integration Health Dashboard
Issue #530: ALPHA-SETUP-VERIFY

Tests the full flow of the integrations dashboard including:
- API endpoint accessibility
- Response schema validation
- Error handling across the stack

Note: These tests require authentication. They are designed to work
with the existing test infrastructure that provides auth fixtures.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

def _fake_claims():
    """#1452: the dashboard routes grew `current_user: JWTClaims =
    Depends(get_current_user)` after these direct-call tests were written —
    calling the functions bare leaked the Depends sentinel into
    current_user.sub. Direct calls must supply claims explicitly."""
    import time as _time

    from services.auth.jwt_service import JWTClaims

    now = int(_time.time())
    from uuid import uuid4

    uid = uuid4()
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub=str(uid),
        exp=now + 3600,
        iat=now,
        jti="test-jti",
        user_id=uid,
        user_email="dash-test@example.com",
        username="dash-test",
        scopes=["user"],
        token_type="access",
    )


# Mark all tests in this module as integration tests
pytestmark = pytest.mark.integration


class TestIntegrationsAPIWithMocks:
    """
    Integration tests for the integrations health API.

    These tests verify the API logic works correctly using mocks
    for the actual integration testing functions.
    """

    @pytest.mark.asyncio
    async def test_health_endpoint_returns_all_integrations(self):
        """Health endpoint should return status for all 4 integrations"""
        from web.api.routes.integrations import get_integrations_health

        response = await get_integrations_health(current_user=_fake_claims())

        assert response.total_count == 4
        integration_names = {i.name for i in response.integrations}
        assert integration_names == {"notion", "slack", "github", "calendar"}

    @pytest.mark.asyncio
    async def test_health_endpoint_returns_correct_schema(self):
        """Health response should contain expected fields"""
        from web.api.routes.integrations import get_integrations_health

        response = await get_integrations_health(current_user=_fake_claims())

        # Required fields via Pydantic model
        assert response.overall_status is not None
        assert response.timestamp is not None
        assert response.integrations is not None
        assert response.healthy_count is not None
        assert response.total_count is not None

        # Types
        assert isinstance(response.integrations, list)
        assert isinstance(response.healthy_count, int)
        assert isinstance(response.total_count, int)

    @pytest.mark.asyncio
    async def test_test_endpoint_unknown_integration_raises_404(self):
        """Testing unknown integration should raise 404"""
        from fastapi import HTTPException

        from web.api.routes.integrations import check_integration_connection

        with pytest.raises(HTTPException) as exc_info:
            await check_integration_connection("unknown_integration", current_user=_fake_claims())

        assert exc_info.value.status_code == 404
        assert "Unknown integration" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_test_endpoint_with_mocked_success(self):
        """Test endpoint should return success when integration passes"""
        from web.api.routes.integrations import check_integration_connection

        with patch("web.api.routes.integrations._test_notion", new_callable=AsyncMock) as mock:
            mock.return_value = {"success": True}

            response = await check_integration_connection("notion", current_user=_fake_claims())

            assert response.success is True
            assert response.integration == "notion"
            assert response.latency_ms is not None
            assert response.latency_ms >= 0

    @pytest.mark.asyncio
    async def test_test_endpoint_with_mocked_failure(self):
        """Test endpoint should return failure with error info when integration fails"""
        from web.api.routes.integrations import check_integration_connection

        with patch("web.api.routes.integrations._test_notion", new_callable=AsyncMock) as mock:
            mock.return_value = {
                "success": False,
                "error_type": "api_key_invalid",
                "error": "Invalid API key",
            }

            response = await check_integration_connection("notion", current_user=_fake_claims())

            assert response.success is False
            assert response.integration == "notion"
            assert response.message is not None
            assert response.fix_suggestion is not None

    @pytest.mark.asyncio
    async def test_test_all_endpoint_returns_results_for_all(self):
        """Test all should return results for all integrations"""
        from web.api.routes.integrations import check_all_connections

        with patch("web.api.routes.integrations._test_integration", new_callable=AsyncMock) as mock:
            mock.return_value = {"success": True}

            results = await check_all_connections(current_user=_fake_claims())

            assert len(results) == 4
            integration_names = {r.integration for r in results}
            assert integration_names == {"notion", "slack", "github", "calendar"}


class TestIntegrationHealthMonitorIntegration:
    """Tests for IntegrationHealthMonitor integration"""

    @pytest.mark.asyncio
    async def test_health_monitor_initialization(self):
        """Health monitor should be properly initialized"""
        from web.api.routes.integrations import _get_health_monitor

        monitor = _get_health_monitor()
        assert monitor is not None

        # Should have all integrations registered
        for integration in ["notion", "slack", "github", "calendar"]:
            health = monitor.get_component_health(integration)
            assert health is not None

    @pytest.mark.asyncio
    async def test_health_monitor_records_success_on_test(self):
        """Health monitor should record success when test passes"""
        from services.health.integration_health_monitor import ComponentStatus
        from web.api.routes.integrations import _get_health_monitor, check_integration_connection

        with patch("web.api.routes.integrations._test_notion", new_callable=AsyncMock) as mock:
            mock.return_value = {"success": True}

            monitor = _get_health_monitor()

            await check_integration_connection("notion", current_user=_fake_claims())

            # Verify health was recorded
            health = monitor.get_component_health("notion")
            assert health is not None
            assert health.status == ComponentStatus.HEALTHY

    @pytest.mark.asyncio
    async def test_health_monitor_records_failure_on_test(self):
        """Health monitor should record failure when test fails"""
        from web.api.routes.integrations import _get_health_monitor, check_integration_connection

        with patch("web.api.routes.integrations._test_notion", new_callable=AsyncMock) as mock:
            mock.return_value = {
                "success": False,
                "error_type": "api_key_invalid",
                "error": "Invalid API key",
            }

            monitor = _get_health_monitor()

            # Reset component to ensure clean state
            monitor.reset_component_health("notion")
            initial_error_count = monitor.get_component_health("notion").error_count

            await check_integration_connection("notion", current_user=_fake_claims())

            # Verify failure was recorded
            health = monitor.get_component_health("notion")
            assert health is not None
            # Error count should have increased
            assert health.error_count > initial_error_count
            # Last error should be recorded
            assert health.last_error == "Invalid API key"


class TestIntegrationErrorHandling:
    """Tests for error handling in integration endpoints"""

    @pytest.mark.asyncio
    async def test_test_endpoint_handles_exception_in_test(self):
        """Test endpoint should handle exceptions during testing"""
        from web.api.routes.integrations import check_integration_connection

        with patch("web.api.routes.integrations._test_notion", new_callable=AsyncMock) as mock:
            mock.side_effect = Exception("Network timeout")

            response = await check_integration_connection("notion", current_user=_fake_claims())

            assert response.success is False
            assert "Network timeout" in response.message or "Network timeout" in str(response.error)


class TestIntegrationRegistry:
    """Tests for the integration registry configuration"""

    def test_registry_has_all_integrations(self):
        """Registry should have all 4 integrations"""
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        assert "notion" in INTEGRATION_REGISTRY
        assert "slack" in INTEGRATION_REGISTRY
        assert "github" in INTEGRATION_REGISTRY
        assert "calendar" in INTEGRATION_REGISTRY

    def test_registry_has_complete_error_guidance(self):
        """Each integration should have error guidance"""
        from web.api.routes.integrations import INTEGRATION_REGISTRY

        for name, config in INTEGRATION_REGISTRY.items():
            assert "errors" in config, f"{name} missing errors"
            assert len(config["errors"]) >= 1, f"{name} has no error definitions"

            for error_type, error_info in config["errors"].items():
                assert "message" in error_info, f"{name}/{error_type} missing message"
                assert "fix" in error_info, f"{name}/{error_type} missing fix"
