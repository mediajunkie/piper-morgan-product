"""Regression tests for Issue #1075 route-prefix migration.

Verifies that the transparency router mounts under its new /api/v1/ prefix
(per CLAUDE.md API Conventions) and that auth middleware behaves correctly:

- /api/v1/transparency/* requires auth (no exemption)

Does NOT exercise endpoint logic — those are tested by the underlying
audit_transparency module. This file is a routing-shape regression guard
for the migration itself.

(The admin_compose router was removed 2026-06-20 / #1307 — a misplaced
product-app copy of an editorial UI that belongs in the website repo; as an
auth-exempt + writable + un-env-gated route it was a security gap.)
"""

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """Bare TestClient against the real app — no IntentService stub needed."""
    from web.app import app

    return TestClient(app)


class TestTransparencyRoutePrefixes:
    """#1075 + #1018: transparency router mounted under /api/v1/transparency."""

    def test_audit_log_route_exists(self, client):
        """GET /api/v1/transparency/audit-log/{session_id} — should hit auth gate, not 404."""
        response = client.get("/api/v1/transparency/audit-log/test-session")
        assert response.status_code == 401, (
            f"Expected 401 (auth-required) for unauthenticated request, "
            f"got {response.status_code}. Route may not be mounted."
        )

    def test_audit_summary_route_exists(self, client):
        response = client.get("/api/v1/transparency/audit-summary/test-session")
        assert response.status_code == 401

    def test_stats_route_exists(self, client):
        response = client.get("/api/v1/transparency/stats")
        assert response.status_code == 401

    def test_health_route_exists(self, client):
        response = client.get("/api/v1/transparency/health")
        assert response.status_code == 401

    def test_cleanup_route_exists(self, client):
        response = client.post("/api/v1/transparency/cleanup")
        assert response.status_code == 401

    def test_no_pre_migration_paths_registered(self):
        """Pre-migration /transparency/* paths should not be registered with the app."""
        from web.app import app

        registered_paths = [r.path for r in app.routes if hasattr(r, "path")]
        pre_migration_paths = [
            p for p in registered_paths if p.startswith("/transparency/")
        ]
        assert pre_migration_paths == [], (
            f"Pre-migration paths still registered: {pre_migration_paths}"
        )
