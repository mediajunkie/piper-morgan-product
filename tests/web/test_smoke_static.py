"""
Test suite for Issue #350: TEST-SMOKE-STATIC
Add smoke tests for static file serving

These tests verify critical infrastructure that was previously not tested:
- Static file mounting (CSS, JS, images)
- Template loading
- Infrastructure issues caught early

Context:
Static file mounting was broken on Saturday (Nov 16) but no smoke tests
caught it. These tests ensure static file serving infrastructure is working.
"""

import pytest
from fastapi.testclient import TestClient


class TestSmokeStatic:
    """Verify static files are served correctly"""

    def test_static_css_loads(self, client_with_intent: TestClient):
        """
        Verify CSS files are served.

        Success Criteria:
        - Request to /static/css/* returns 200
        - Response has correct content type
        - Content is not empty
        """
        # Using a file we know exists: dialog.css (from UX-TRANCHE3)
        response = client_with_intent.get("/static/css/dialog.css")
        assert response.status_code == 200, "Static CSS should be accessible"
        assert "text/css" in response.headers.get(
            "content-type", ""
        ), "CSS should have correct content type"
        assert len(response.content) > 0, "CSS file should have content"

    def test_static_js_loads(self, client_with_intent: TestClient):
        """
        Verify JavaScript files are served.

        Success Criteria:
        - Request to /static/js/* returns 200
        - Response has correct content type
        - Content is not empty
        """
        # Using a file we know exists: dialog.js (from UX-TRANCHE3)
        response = client_with_intent.get("/static/js/dialog.js")
        assert response.status_code == 200, "Static JS should be accessible"
        assert "javascript" in response.headers.get(
            "content-type", ""
        ) or "text/plain" in response.headers.get(
            "content-type", ""
        ), "JS should have correct content type"
        assert len(response.content) > 0, "JS file should have content"

    def test_template_renders(self, client_with_intent: TestClient):
        """
        Verify templates render without errors.

        Success Criteria:
        - Home page returns 200 (or redirect if not authenticated)
        - Response contains HTML structure
        - No 500 errors (which would indicate template/mounting failure)
        """
        response = client_with_intent.get("/")
        # Could be 200 or 307 redirect depending on auth
        assert response.status_code in [
            200,
            307,
        ], f"Home page should render, got {response.status_code}"
        if response.status_code == 200:
            # Follow redirects to check HTML
            response = client_with_intent.get("/", follow_redirects=True)
            assert (
                "<!DOCTYPE html>" in response.text or "<html" in response.text
            ), "Should return HTML"

    def test_static_mounting_verified(self, client_with_intent: TestClient):
        """
        Verify /static route is mounted and accessible.

        Success Criteria:
        - Existing static files return 200
        - Missing files return 404 (not 500)
        - Mounting is working correctly
        """
        # Test with a file that exists
        response = client_with_intent.get("/static/css/dialog.css")
        assert response.status_code == 200, "Existing static file should be accessible"

        # Test with a file that doesn't exist
        response = client_with_intent.get("/static/css/nonexistent-file-xyz.css")
        assert (
            response.status_code == 404
        ), "Missing static file should return 404, not 500 (mounting is working)"
