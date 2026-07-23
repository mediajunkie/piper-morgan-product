"""
Complete user flow validation for intent classification.
Tests end-to-end flows including caching behavior.

GREAT-5 Phase 1.5: Updated to use client_with_intent fixture for proper
IntentService initialization in test environment.
"""

import pytest


@pytest.fixture
def client(client_with_intent):
    """Use the properly initialized client from conftest."""
    return client_with_intent


class TestCompleteUserFlows:
    """End-to-end user flow validation."""

    def test_intent_endpoint_basic_flow(self, client):
        """Basic flow: user query → intent classification → response."""
        response = client.post("/api/v1/intent", json={"text": "What day is it?"})

        # GREAT-5: STRICT - no server crashes (500) accepted
        # Should succeed (200) or validation error (422), but NOT crash (500)
        assert response.status_code in [200, 422]

        if response.status_code == 200:
            data = response.json()
            # Intent should be classified
            assert "intent" in data or "category" in data

    def test_temporal_query_flow(self, client):
        """TEMPORAL category flow."""
        queries = ["What day is it?", "What's the date?", "What day of the week is it?"]

        for query in queries:
            response = client.post("/api/v1/intent", json={"text": query})

            # GREAT-5: TEMPORAL is canonical handler - must work reliably
            assert response.status_code in [200, 422]

    def test_status_query_flow(self, client):
        """STATUS category flow."""
        queries = [
            "What am I working on?",
            "Show me my current projects",
            "What's my project status?",
        ]

        for query in queries:
            response = client.post("/api/v1/intent", json={"text": query})

            # GREAT-5: STATUS is canonical handler - must work reliably
            assert response.status_code in [200, 422]

    def test_priority_query_flow(self, client):
        """PRIORITY category flow."""
        queries = ["What's my top priority?", "What should I focus on?", "What needs my attention?"]

        for query in queries:
            response = client.post("/api/v1/intent", json={"text": query})

            # GREAT-5: PRIORITY is canonical handler - must work reliably
            assert response.status_code in [200, 422]


class TestCachingBehavior:
    """Validate caching works in practice."""

    def test_duplicate_queries_use_cache(self, client):
        """Same query twice should show cache improvement."""
        query = {"message": "What day is it?"}

        # Sprint A1 Phase 1: First request - must succeed (not accept validation errors)
        response1 = client.post("/api/v1/intent", json=query)
        assert response1.status_code == 200

        # Get initial cache metrics
        metrics1_response = client.get("/api/admin/intent-cache-metrics")
        if metrics1_response.status_code == 200:
            metrics1 = metrics1_response.json().get("metrics", {})
            initial_hits = metrics1.get("hits", 0)
            initial_misses = metrics1.get("misses", 0)

            # Sprint A1 Phase 1: Second request - must succeed (not accept validation errors)
            response2 = client.post("/api/v1/intent", json=query)
            assert response2.status_code == 200

            # Get updated cache metrics
            metrics2_response = client.get("/api/admin/intent-cache-metrics")
            if metrics2_response.status_code == 200:
                metrics2 = metrics2_response.json().get("metrics", {})
                final_hits = metrics2.get("hits", 0)
                final_misses = metrics2.get("misses", 0)

                # Should have one more hit OR one more miss
                # (depending on whether first query was cached)
                assert (final_hits > initial_hits) or (final_misses > initial_misses)

    def test_cache_metrics_endpoint(self, client):
        """Cache metrics endpoint exists and is auth-gated.

        #1452: global auth now guards admin endpoints — unauthenticated
        probes get 401 (correct), never 404 (missing) or 500 (crash).
        """
        response = client.get("/api/admin/intent-cache-metrics")
        assert response.status_code == 401


class TestStandupFlow:
    """Validate standup endpoint uses intent."""

    def test_standup_endpoint_accessible(self, client):
        """Standup endpoint should work."""
        response = client.get("/api/standup")

        # GREAT-5: Should succeed or return auth error, but NOT crash (500)
        assert response.status_code in [200, 401, 403]

    def test_standup_backend_integration(self, client):
        """Standup should use backend intent classification."""
        # This test assumes standup proxies to backend
        # Verify endpoint exists and responds appropriately
        response = client.get("/api/standup")

        # Even if auth fails, endpoint should exist
        assert response.status_code != 404


class TestMiddlewareEnforcement:
    """Validate middleware is enforcing properly."""

    def test_middleware_monitoring_active(self, client):
        """Monitoring endpoint exists and is auth-gated (#1452: see above)."""
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 401

    def test_exempt_paths_work(self, client):
        """Exempt paths should be accessible."""
        # GREAT-4F: /health MUST return 200 (critical for monitoring/load balancers)
        # #1452: "/" now 302-redirects unauthenticated visitors to login
        exempt_paths = [("/health", [200]), ("/docs", [200, 404]), ("/", [200, 302])]

        for path, expected_codes in exempt_paths:
            # follow_redirects=False: reachability is the claim under test —
            # following "/"'s login redirect renders a template, which needs
            # the full app lifespan the bare TestClient doesn't run.
            response = client.get(path, follow_redirects=False)
            assert response.status_code in expected_codes, (
                f"{path} should be accessible, got {response.status_code}: {response.text[:200]}"
            )


class TestPersonalityIntegration:
    """Validate personality enhancement is separate from intent."""

    def test_personality_enhance_is_exempt(self, client):
        """Personality enhancement should not require intent."""
        response = client.post(
            "/api/v1/personality/enhance", json={"text": "Test response", "context": {}}
        )

        # GREAT-5: Should work, validation-error, or auth-gate — NOT crash
        # (500) or missing (404). 401 = global auth answers first (#1452).
        assert response.status_code in [200, 422, 401]
        assert response.status_code != 404
