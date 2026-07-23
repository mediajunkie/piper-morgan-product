"""
Integration tests for complete intent system.

GREAT-5 Phase 1.5: Updated to use client_with_intent fixture for proper
IntentService initialization in test environment.
"""

import pytest


@pytest.fixture
def client(client_with_intent):
    """Use the properly initialized client from conftest."""
    return client_with_intent


class TestIntentSystemIntegration:
    """Full system integration tests."""

    def test_complete_pipeline_exists(self, client):
        """Verify all pipeline components exist."""
        # 1. Intent endpoint exists
        response = client.post("/api/v1/intent", json={"text": "test"})
        # GREAT-5: Intent endpoint must work reliably - no server crashes (500)
        assert response.status_code in [200, 422]

        # 2. Middleware monitoring exists — auth-gated since global auth
        # (#1452): 401 proves the route exists (a missing route would 404)
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 401

        # 3. Cache monitoring exists (same contract)
        response = client.get("/api/admin/intent-cache-metrics")
        assert response.status_code == 401

    def test_nl_endpoints_configured(self):
        """All NL endpoints should be in middleware config.

        #1452: the admin endpoint is auth-gated now — read the enforcement
        middleware's config directly instead of probing over HTTP.
        """
        from web.middleware.intent_enforcement import IntentEnforcementMiddleware

        nl_endpoints = getattr(IntentEnforcementMiddleware, "NL_ENDPOINTS", None)
        if nl_endpoints is None:
            import web.middleware.intent_enforcement as m

            nl_endpoints = getattr(m, "NL_ENDPOINTS", [])
        assert "/api/v1/intent" in nl_endpoints
        assert "/api/standup" in nl_endpoints

    def test_cache_operational(self):
        """Cache should be operational (checked in-process — the HTTP
        surface is auth-gated since #1452)."""
        from services.intent_service.cache import IntentCache

        cache = IntentCache()
        metrics = cache.get_metrics()
        assert "hits" in metrics and "misses" in metrics
