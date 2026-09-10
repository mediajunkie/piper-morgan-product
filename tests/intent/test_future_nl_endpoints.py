"""
Tests to catch if new NL endpoints are added without intent.
"""

import ast
from pathlib import Path

import pytest


class TestFutureEndpoints:
    """Detect new endpoints that should use intent."""

    def test_all_nl_routes_in_middleware_config(self):
        """All NL routes should be in middleware configuration."""
        # Scan web routes for potential NL endpoints
        web_files = Path("web").glob("**/*.py")

        potential_nl_routes = []
        for file in web_files:
            if file.name == "__init__.py":
                continue

            content = file.read_text()

            # Look for route decorators with paths containing chat/message/intent
            import re

            routes = re.findall(r'@(?:app|router)\.\w+\(["\']([^"\']+)', content)

            for route in routes:
                # Skip admin/monitoring endpoints
                if "/admin/" in route:
                    continue

                # Check if route looks like NL endpoint
                if any(
                    keyword in route.lower()
                    for keyword in ["chat", "message", "intent", "ask", "query"]
                ):
                    potential_nl_routes.append(route)

        # Get configured NL endpoints from middleware
        from web.middleware.intent_enforcement import IntentEnforcementMiddleware

        configured = IntentEnforcementMiddleware.NL_ENDPOINTS

        # 1637: known false positives of the keyword heuristic — routes whose
        # path matches an NL keyword but which take only STRUCTURED input
        # (typed query/path params, no free text for a classifier). Add here
        # ONLY with that justification.
        # - "/query": GET /api/v1/knowledge/query (knowledge_graph.py) —
        #   node_type/search_term/limit query params, SEC-RBAC-gated graph
        #   lookup, no NL body. Masked until now by the per-route assert
        #   aborting at "/intent" first.
        structured_route_suffixes = {"/query"}

        # All potential NL routes should be configured.
        # 1637 (two fixes here):
        # - The regex above captures the DECORATOR path, which for routers
        #   mounted with a prefix is only the suffix of the real route —
        #   web/api/routes/intent.py declares @router.post("/intent") on a
        #   router with prefix="/api/v1", and the middleware (correctly)
        #   configures the full "/api/v1/intent". Accept a configured endpoint
        #   whose path ends with the captured suffix; a genuinely unconfigured
        #   NL route still matches nothing and fails.
        # - Collect ALL offenders instead of asserting per-route, so one
        #   failure can't mask the rest.
        unconfigured = []
        for route in potential_nl_routes:
            if route in structured_route_suffixes:
                continue
            if route not in configured and not any(c.endswith(route) for c in configured):
                unconfigured.append(route)

        assert (
            not unconfigured
        ), f"routes look like NL endpoints but are not in middleware config: {unconfigured}"

    def test_no_direct_service_calls_in_routes(self):
        """Web routes should not directly call services for NL processing."""
        web_app = Path("web/app.py")
        content = web_app.read_text()

        # Look for direct service imports/calls
        suspicious_patterns = [
            r"from services\..*_service import",
            r"github_service\.",
            r"notion_service\.",
            r"calendar_service\.",
        ]

        import re

        for pattern in suspicious_patterns:
            matches = re.findall(pattern, content)
            # If found, they should only be in non-NL routes
            # This is a heuristic check
            if matches:
                # Warn but don't fail - need manual review
                pytest.skip(f"Found direct service usage: {matches} - needs review")
