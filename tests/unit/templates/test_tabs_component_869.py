"""Tests for the generic Tabs component (#869 Project Config IA Phase 1)."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tabs_html() -> str:
    """Load tabs.html partial."""
    return Path("templates/components/tabs.html").read_text()


@pytest.fixture
def project_detail_html() -> str:
    """Load project_detail.html (consumer of the tabs component)."""
    return Path("templates/project_detail.html").read_text()


class TestTabsComponentStructure:
    """Tabs component file shape."""

    def test_component_file_exists(self, tabs_html):
        assert tabs_html  # non-empty

    def test_has_documentation_header(self, tabs_html):
        # Issue #869 attribution + usage example
        assert "#869" in tabs_html
        assert "data-tabs-container" in tabs_html

    def test_has_styles_block(self, tabs_html):
        assert "<style>" in tabs_html
        assert ".tabs-strip" in tabs_html
        assert ".tab-button" in tabs_html
        assert ".tab-panel" in tabs_html

    def test_has_active_state_styling(self, tabs_html):
        # Active tab uses aria-selected="true" + bottom-border
        assert 'aria-selected="true"' in tabs_html

    def test_panel_hide_styling(self, tabs_html):
        # Hidden tab panels should not display
        assert ".tab-panel[hidden]" in tabs_html
        assert "display: none" in tabs_html


class TestTabsComponentJavaScript:
    """Tabs activation logic."""

    def test_has_activation_script(self, tabs_html):
        assert "<script>" in tabs_html
        assert "TabsComponent" in tabs_html

    def test_url_param_lookup(self, tabs_html):
        # ?tab=<id> drives initial activation
        assert "URLSearchParams" in tabs_html
        assert "getTabIdFromURL" in tabs_html

    def test_history_replace_state(self, tabs_html):
        # Click updates URL without reload
        assert "history.replaceState" in tabs_html

    def test_keyboard_navigation(self, tabs_html):
        # Arrow keys move between tabs (a11y baseline)
        assert "ArrowLeft" in tabs_html
        assert "ArrowRight" in tabs_html

    def test_idempotent_init(self, tabs_html):
        # Safe to load multiple times
        assert "window.TabsComponent" in tabs_html
        assert "if (window.TabsComponent) return" in tabs_html

    def test_dom_content_loaded_handler(self, tabs_html):
        # Auto-runs at page load
        assert "DOMContentLoaded" in tabs_html

    def test_default_first_tab_when_no_url_param(self, tabs_html):
        # Falls back to first tab if URL param missing/invalid
        assert "validTabIds.includes(urlTab)" in tabs_html or "firstTab" in tabs_html


class TestTabsComponentAccessibility:
    """A11y baseline for tabs (per Q2: PM 'acceptable' to create generic component)."""

    def test_aria_role_attributes_referenced_in_docs(self, tabs_html):
        # Usage example documents role="tablist" and role="tab"
        assert "tablist" in tabs_html
        assert "role=" in tabs_html or 'aria-selected' in tabs_html

    def test_focus_visible_styling(self, tabs_html):
        # Keyboard focus has visible outline
        assert ":focus-visible" in tabs_html

    def test_aria_selected_toggling_logic(self, tabs_html):
        # JS toggles aria-selected on activation
        assert 'setAttribute(\'aria-selected\'' in tabs_html or "setAttribute('aria-selected'" in tabs_html


class TestProjectDetailTabsIntegration:
    """Project Detail page is wired to use the tabs component (Phase 1 acceptance)."""

    def test_includes_tabs_component(self, project_detail_html):
        assert "{% include 'components/tabs.html' %}" in project_detail_html

    def test_has_tabs_container(self, project_detail_html):
        assert "data-tabs-container" in project_detail_html

    def test_has_overview_tab(self, project_detail_html):
        assert 'data-tab-id="overview"' in project_detail_html
        assert 'id="tab-button-overview"' in project_detail_html
        assert 'id="tab-panel-overview"' in project_detail_html

    def test_has_settings_tab(self, project_detail_html):
        # The Config tab uses tab-id="settings" (matches /projects/{id}?tab=settings URL)
        assert 'data-tab-id="settings"' in project_detail_html
        assert 'id="tab-button-settings"' in project_detail_html
        assert 'id="tab-panel-settings"' in project_detail_html

    def test_overview_default_aria_selected(self, project_detail_html):
        # Overview tab is the default (aria-selected="true" before JS runs)
        # This is the SSR-time default; JS overrides based on URL param
        overview_idx = project_detail_html.find('data-tab-id="overview"')
        # Find the aria-selected attribute near the overview button
        chunk = project_detail_html[overview_idx : overview_idx + 500]
        assert 'aria-selected="true"' in chunk

    def test_work_items_section_inside_overview_panel(self, project_detail_html):
        # Existing Work Items markup must live under the Overview tab so
        # nothing breaks for users hitting /projects/{id} directly.
        overview_panel_idx = project_detail_html.find('id="tab-panel-overview"')
        next_panel_idx = project_detail_html.find('id="tab-panel-settings"')
        assert overview_panel_idx > 0
        assert next_panel_idx > overview_panel_idx
        overview_chunk = project_detail_html[overview_panel_idx:next_panel_idx]
        assert "work-items-section" in overview_chunk
        assert 'id="work-item-count"' in overview_chunk
        assert 'id="work-items-container"' in overview_chunk

    def test_settings_panel_hidden_by_default(self, project_detail_html):
        # Settings panel ships with hidden attribute; tabs JS un-hides on activation
        settings_idx = project_detail_html.find('id="tab-panel-settings"')
        chunk = project_detail_html[settings_idx : settings_idx + 500]
        # The panel element itself has hidden attribute
        assert "hidden" in chunk

    def test_settings_panel_includes_config_panel_partial(self, project_detail_html):
        # Phase 2 (#869): Config tab includes the shared
        # components/project_config_panel.html partial.
        assert "components/project_config_panel.html" in project_detail_html
