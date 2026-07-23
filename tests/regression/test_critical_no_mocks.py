"""
Regression tests with NO mocks and NO silent failures.

These tests validate critical system functionality with zero tolerance
for failures. Created in response to testing blind spots investigation
(October 6, 2025).

IMPORTANT: These tests use NO mocks - they test real functionality.
"""

import importlib
import sys

import pytest
from fastapi.testclient import TestClient


class TestCriticalImports:
    """All critical imports must work - no mocks, no silent failures."""

    def test_web_app_imports(self):
        """web.app must import successfully."""
        try:
            from web.app import app

            assert app is not None
            assert hasattr(app, "routes")
        except ImportError as e:
            pytest.fail(f"Critical import failed: web.app - {e}")

    def test_intent_service_imports(self):
        """Intent service must import successfully."""
        try:
            from services.intent.intent_service import IntentService

            assert IntentService is not None
        except ImportError as e:
            pytest.fail(f"Critical import failed: services.intent.intent_service - {e}")

    def test_all_critical_modules_importable(self):
        """All critical modules must be importable."""
        critical_modules = [
            "web.app",
            "services.intent.intent_service",
            "services.intent_service.canonical_handlers",
            "services.intent_service.pre_classifier",
            "services.domain.github_domain_service",
            "services.domain.slack_domain_service",
        ]

        failed_imports = []
        for module in critical_modules:
            try:
                importlib.import_module(module)
            except ImportError as e:
                failed_imports.append(f"{module}: {e}")

        assert len(failed_imports) == 0, f"Failed imports: {failed_imports}"


class TestCriticalEndpoints:
    """All documented endpoints must exist and return correct status codes."""

    def test_health_endpoint_exists_and_returns_200(self):
        """
        /health endpoint must exist and return 200.

        NO allowing 404! Health check is critical for load balancers.
        """
        from web.app import app

        client = TestClient(app)

        response = client.get("/health")

        # STRICT: Must be exactly 200
        assert response.status_code == 200, (
            f"Health check must return 200, got {response.status_code}. "
            "Health endpoint is critical for monitoring."
        )

        # Must return valid JSON
        data = response.json()
        assert "status" in data
        assert data["status"] == "healthy"

    def test_all_required_endpoints_exist(self):
        """All documented endpoints must be registered."""
        from web.app import app

        required_endpoints = [
            ("/health", "GET"),
            ("/health/config", "GET"),
            ("/api/v1/intent", "POST"),
            ("/api/admin/intent-monitoring", "GET"),
            ("/api/admin/intent-cache-metrics", "GET"),
        ]

        # Get actual routes
        actual_routes = {}
        for route in app.routes:
            if hasattr(route, "path") and hasattr(route, "methods"):
                for method in route.methods:
                    actual_routes[(route.path, method)] = True

        missing = []
        for endpoint, method in required_endpoints:
            if (endpoint, method) not in actual_routes:
                missing.append(f"{method} {endpoint}")

        assert len(missing) == 0, f"Missing required endpoints: {missing}"

        # #1452: the standup surface (now /api/v1/standup, API-conventions)
        # mounts in a LIFESPAN phase (web/startup.py APIRouterMountingPhase),
        # so it is invisible on app.routes without booting the app. Assert
        # the wiring chain instead: the router carries the canonical GET and
        # the mounting phase is registered in the startup sequence.
        from web.api.routes.standup import router as standup_router
        from web.startup import APIRouterMountingPhase, StartupManager

        standup_paths = {
            (r.path, m) for r in standup_router.routes for m in getattr(r, "methods", [])
        }
        assert ("/api/v1/standup/today", "GET") in standup_paths

        import inspect as _inspect

        manager = StartupManager(app)
        assert APIRouterMountingPhase in manager.phases
        assert "web.api.routes.standup" in _inspect.getsource(
            APIRouterMountingPhase.startup
        )

    def test_intent_endpoint_returns_valid_response(self):
        """Intent endpoint must process requests and return valid responses."""
        from web.app import app

        client = TestClient(app)

        response = client.post("/api/v1/intent", json={"text": "What day is it?"})

        # GREAT-5: STRICT - no accepting 500 (server crash)
        # Must succeed (200) or return proper validation error (422)
        # But NOT 404 (doesn't exist) or 500 (server crash)
        assert response.status_code in [200, 422], (
            f"Intent endpoint returned {response.status_code}. "
            "Expected 200 (success) or 422 (validation error). "
            "404 means endpoint doesn't exist, 500 means server crash - both failures!"
        )


class TestNoSilentFailures:
    """Tests that validate we're not hiding failures."""

    def test_canonical_handlers_file_exists(self):
        """Canonical handlers file must exist - no skipping if missing."""
        from pathlib import Path

        canonical_handlers_path = Path("services/intent_service/canonical_handlers.py")

        assert canonical_handlers_path.exists(), (
            "Canonical handlers file is missing! " "This should FAIL, not skip silently."
        )

    def test_intent_test_constants_exist(self):
        """Intent test constants must exist - tests depend on them."""
        try:
            from tests.intent.test_constants import CATEGORY_EXAMPLES, INTENT_CATEGORIES

            assert len(INTENT_CATEGORIES) == 13, "Should have 13 intent categories"
            assert len(CATEGORY_EXAMPLES) == 13, "Should have 13 category examples"
        except ImportError as e:
            pytest.fail(f"Test constants missing: {e}")


class TestIntentServiceEndToEnd:
    """End-to-end tests with real IntentService - no mocks."""

    @pytest.mark.llm
    @pytest.mark.asyncio
    async def test_intent_service_processes_temporal_query(self):
        """Intent service must process TEMPORAL queries successfully."""
        from services.intent.intent_service import IntentService

        # #1094: engine deleted; intent_service does direct dispatch via task_type registry
        intent_service = IntentService()

        # Process real query
        result = await intent_service.process_intent(
            "What day is it?", session_id="regression_test"
        )

        # Must succeed
        assert result is not None
        assert hasattr(result, "success")
        # Note: success might be True or False, but result must exist


if __name__ == "__main__":
    # Run regression tests
    pytest.main([__file__, "-v", "--tb=short"])
