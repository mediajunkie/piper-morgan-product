"""
Test that all web routes enforce intent classification.
No direct service access should be possible.
"""

import pytest
from fastapi.testclient import TestClient

from web.app import app

# 1637 isolation note: this file used to build `client = TestClient(app)` at
# MODULE level, i.e. at pytest COLLECTION time — before any collected test
# (including every tests/unit test in a combined invocation) has run. A
# collection-time side effect in one tree is exactly the shape that made the
# 2026-08-16 combined-run poisoning possible, and it buys nothing: a fixture
# builds the same client at test time, scoped to this class.


@pytest.fixture(scope="class")
def client():
    return TestClient(app)


class TestWebIntentEnforcement:
    """Ensure all web routes use intent classification."""

    def test_intent_endpoint_exists(self, client):
        """Verify /api/v1/intent endpoint is available."""
        response = client.post("/api/v1/intent", json={"text": "What day is it?"})
        assert response.status_code in [200, 422]  # 200 success or 422 validation

    def test_no_direct_github_access(self, client):
        """Ensure GitHub endpoints require intent."""
        # Try to access GitHub service directly
        response = client.post("/api/github/create_issue", json={"title": "Test", "body": "Test"})
        # Should be 404 (doesn't exist) or 403 (forbidden)
        # 401 = auth middleware refuses before routing — the bypass is still
        # blocked (#1452: added when global auth started answering first)
        assert response.status_code in [404, 403, 405, 401]

    def test_no_direct_slack_access(self, client):
        """Ensure Slack endpoints require intent."""
        response = client.post("/api/slack/send_message", json={"channel": "test", "text": "test"})
        # 401 = auth middleware refuses before routing — the bypass is still
        # blocked (#1452: added when global auth started answering first)
        assert response.status_code in [404, 403, 405, 401]

    def test_no_direct_notion_access(self, client):
        """Ensure Notion endpoints require intent."""
        response = client.post("/api/notion/create_page", json={"title": "Test"})
        # 401 = auth middleware refuses before routing — the bypass is still
        # blocked (#1452: added when global auth started answering first)
        assert response.status_code in [404, 403, 405, 401]

    def test_no_direct_calendar_access(self, client):
        """Ensure Calendar endpoints require intent."""
        response = client.get("/api/calendar/events")
        # 401 = auth middleware refuses before routing — the bypass is still
        # blocked (#1452: added when global auth started answering first)
        assert response.status_code in [404, 403, 405, 401]

    def test_health_endpoint_allowed(self, client):
        """Health checks are explicitly allowed to bypass."""
        response = client.get("/health")
        # GREAT-4F: Health endpoint MUST return 200 (critical for monitoring/load balancers)
        assert response.status_code == 200, "/health endpoint MUST return 200 for monitoring"

    def test_docs_endpoint_allowed(self, client):
        """Documentation is explicitly allowed to bypass."""
        response = client.get("/docs")
        # Docs should work or not exist
        assert response.status_code in [200, 404]
