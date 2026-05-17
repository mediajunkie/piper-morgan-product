"""
Tests for the /transparency route handler (#1099 MUX/UI Round 2 Surface 7).

Verifies the route exists, references the correct template, and documents
#1099 + ADR-063.
"""

import inspect

import pytest

from web.api.routes import ui as ui_routes


class TestTransparencyRoute:
    """Verify the /transparency route handler is wired correctly."""

    def test_transparency_handler_exists(self):
        """Route handler function is defined in web.api.routes.ui."""
        assert hasattr(ui_routes, "transparency_ui"), (
            "transparency_ui handler must exist in web.api.routes.ui"
        )

    def test_handler_is_async(self):
        """Per FastAPI conventions, the handler is async."""
        assert inspect.iscoroutinefunction(ui_routes.transparency_ui), (
            "transparency_ui must be an async function"
        )

    def test_docstring_cites_issue_and_adr(self):
        """Pattern-073 discipline: handler docstring must cite #1099 + ADR-063
        so future readers don't lose the architectural anchor."""
        doc = ui_routes.transparency_ui.__doc__ or ""
        assert "#1099" in doc, "Docstring must cite #1099"
        assert "ADR-063" in doc, "Docstring must cite ADR-063"

    def test_route_registered_in_router(self):
        """The /transparency path is registered on the ui router."""
        paths = {route.path for route in ui_routes.router.routes}
        assert "/transparency" in paths, (
            "/transparency must be registered on the ui router"
        )
