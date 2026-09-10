"""
Integration tests for intent enforcement.

GREAT-5 Phase 1.5: Updated to use client_with_intent fixture for proper
IntentService initialization in test environment.
"""

import pytest


@pytest.fixture
def client(client_with_intent):
    """Use the properly initialized client from conftest."""
    return client_with_intent


class TestEnforcementIntegration:
    """Test full enforcement pipeline."""

    def test_intent_endpoint_works(self, client):
        """Primary intent endpoint should work."""
        response = client.post("/api/v1/intent", json={"text": "What day is it?"})
        # GREAT-5: Should succeed or validation error, but NOT crash (500)
        assert response.status_code in [200, 422]

    def test_standup_uses_backend_intent(self, client):
        """Standup endpoint should proxy to backend that uses intent."""
        response = client.get("/api/standup")
        # GREAT-5: Should succeed or auth error, but NOT crash (500)
        assert response.status_code in [200, 401]

    def test_monitoring_endpoint_exists_and_is_gated(self, client):
        """Admin monitoring endpoint exists — and refuses the unauthenticated.

        1637: this test pinned the pre-#1598 contract (unauthenticated 200).
        #1598 admin-gated every read on the admin surface, so 401 IS the
        current contract for this client, which carries no token. The
        endpoint's payload shape and its admin-side 200 are pinned where the
        gate lives: tests/unit/web/api/routes/test_admin_readonly_routes_gated_1598.py.
        What remains this file's concern is that the route is mounted at all
        (401 from the gate, never 404) — a vanished monitoring endpoint would
        otherwise hide behind the gate's refusal.
        """
        response = client.get("/api/admin/intent-monitoring")
        assert response.status_code == 401, (
            f"expected 401 (mounted but gated, #1598) — got {response.status_code}; "
            "404 would mean the monitoring endpoint is gone, 200 would mean the gate is off"
        )
