"""
Unit tests for Project Settings UI page.
Issue #861: Settings page — project integration management.
Issue #869 Phase 2 (May 5, 2026): repos+integrations markup + JS
extracted into `components/project_config_panel.html` shared partial
used by both settings_projects and project_detail. Many of these
"template content" assertions now read both files concatenated since
the included partial supplies the markers tested.
"""

import os

import pytest

pytestmark = pytest.mark.unit


def _settings_projects_with_partial() -> str:
    """Read settings_projects.html + the included config-panel partial.

    Mirrors what a Jinja-rendered settings/projects page contains for
    the purposes of substring assertions in this file's tests.
    """
    parts = []
    for path in (
        "templates/settings_projects.html",
        "templates/components/project_config_panel.html",
    ):
        with open(path) as f:
            parts.append(f.read())
    return "\n".join(parts)


class TestSettingsProjectsRoute:
    """Test that settings/projects route exists and is properly configured."""

    def test_route_exists_in_ui_module(self):
        """Verify settings_projects_page is importable from ui routes."""
        from web.api.routes.ui import settings_projects_page

        assert callable(settings_projects_page)

    def test_route_has_docstring(self):
        """Verify the route function has a docstring referencing #861."""
        from web.api.routes.ui import settings_projects_page

        assert settings_projects_page.__doc__ is not None
        assert "861" in settings_projects_page.__doc__

    def test_route_function_signature(self):
        """Verify the route expects a Request parameter."""
        import inspect

        from web.api.routes.ui import settings_projects_page

        sig = inspect.signature(settings_projects_page)
        assert "request" in sig.parameters


class TestSettingsProjectsCard:
    """Test that the Projects card appears in settings-index.html."""

    def test_projects_card_in_settings_index(self):
        """Verify settings-index.html contains Projects card linking to /settings/projects."""
        with open("templates/settings-index.html") as f:
            content = f.read()
        assert "/settings/projects" in content
        assert "Projects" in content

    def test_projects_card_has_description(self):
        """Verify Projects card has descriptive text."""
        with open("templates/settings-index.html") as f:
            content = f.read()
        assert "Repository linking" in content or "repositories" in content.lower()
        assert "Integration config" in content or "integrations" in content.lower()


class TestSettingsProjectsTemplate:
    """Test that settings_projects.html template exists and has required elements."""

    def test_template_exists(self):
        """Verify template file exists."""
        assert os.path.exists("templates/settings_projects.html")

    APP_SHELL = "templates/layouts/app_shell.html"

    def _shell_chrome(self):
        """#1452: this template migrated onto app_shell (#1171) — nav, toast,
        and tokens are the SHELL's job now. Assert the two-hop contract:
        the child extends app_shell, and app_shell carries the chrome."""
        with open("templates/settings_projects.html") as f:
            child = f.read()
        assert 'extends "layouts/app_shell.html"' in child
        with open(self.APP_SHELL) as f:
            return f.read()

    def test_template_includes_navigation(self):
        """Navigation is delivered by the shell (nav_rail include)."""
        shell = self._shell_chrome()
        assert "components/nav_rail.html" in shell

    def test_template_includes_breadcrumbs(self):
        """Verify template includes breadcrumbs component."""
        with open("templates/settings_projects.html") as f:
            content = f.read()
        assert "components/breadcrumbs.html" in content

    def test_template_includes_toast(self):
        """Verify template includes toast notification component."""
        with open("templates/settings_projects.html") as f:
            content = f.read()
        assert "components/toast.html" in content

    def test_template_overview_links_to_project_detail_settings_tab(self):
        """#869 Phase 3: each row deep-links to the Project Detail Config tab."""
        with open("templates/settings_projects.html") as f:
            content = f.read()
        assert "?tab=settings" in content
        assert "/projects/" in content

    def test_template_includes_toast_js(self):
        """toast.js is delivered by the shell."""
        shell = self._shell_chrome()
        assert "toast.js" in shell

    def test_template_uses_design_tokens(self):
        """tokens.css is delivered by the shell."""
        shell = self._shell_chrome()
        assert "tokens.css" in shell

    def test_template_calls_projects_api(self):
        """Verify template calls the projects API endpoint."""
        with open("templates/settings_projects.html") as f:
            content = f.read()
        assert "/api/v1/projects" in content

    def test_template_calls_repositories_api(self):
        """Verify template calls the repositories API endpoint."""
        content = _settings_projects_with_partial()
        assert "/api/v1/repositories" in content

    def test_template_has_projects_overview(self):
        """#869 Phase 3: settings page is now an overview list, not a per-project selector."""
        with open("templates/settings_projects.html") as f:
            content = f.read()
        assert "projects-overview-list" in content

    def test_template_has_repositories_section(self):
        """Verify rendered page has a repositories section (#869 Phase 2: in partial)."""
        content = _settings_projects_with_partial()
        assert "repositories-section" in content

    def test_template_has_integrations_section(self):
        """Verify rendered page has an integrations section (#869 Phase 2: in partial)."""
        content = _settings_projects_with_partial()
        assert "integrations-section" in content

    def test_template_has_aria_labels(self):
        """Verify template includes ARIA labels for accessibility."""
        with open("templates/settings_projects.html") as f:
            content = f.read()
        assert "aria-label" in content

    def test_template_uses_credentials_include(self):
        """Verify all fetch calls include credentials for auth."""
        content = _settings_projects_with_partial()
        # Every fetch call should include credentials
        assert content.count("credentials: 'include'") >= 3

    def test_template_has_back_link(self):
        """Verify template has a back link to settings."""
        with open("templates/settings_projects.html") as f:
            content = f.read()
        assert 'href="/settings"' in content
        assert "Back to Settings" in content

    def test_template_has_empty_states(self):
        """Verify template handles empty states for repos and integrations."""
        content = _settings_projects_with_partial()
        assert "No repositories linked" in content or "No repositories" in content.lower()
        assert "No integrations configured" in content or "No integrations" in content.lower()

    def test_template_has_integration_type_metadata(self):
        """Verify template defines metadata for all integration types."""
        content = _settings_projects_with_partial()
        assert "github" in content
        assert "jira" in content
        assert "linear" in content
        assert "slack" in content
