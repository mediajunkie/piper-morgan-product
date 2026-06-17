"""
Tests for navigation component (#420 MUX-NAV-UTILITY).

Tests vocabulary changes, trust-gated visibility, and command palette integration.
"""

from pathlib import Path

import pytest


class TestNavigationVocabulary:
    """Test that navigation uses consciousness-grammar vocabulary."""

    @pytest.fixture
    def nav_content(self):
        """Load navigation template content."""
        nav_path = Path("templates/components/navigation.html")
        return nav_path.read_text()

    def test_standup_renamed_to_check_in(self, nav_content):
        """Standup should be labeled 'Check in' (natural language)."""
        assert "Check in</a>" in nav_content
        # Old label should not be in nav links
        assert ">Standup</a>" not in nav_content

    def test_my_work_renamed_to_your_stuff(self, nav_content):
        """My Work dropdown should be labeled 'Your stuff'."""
        assert "Your stuff" in nav_content
        # Old label should not be present
        assert ">My Work<" not in nav_content

    def test_todos_renamed_to_to_dos(self, nav_content):
        """Todos should be labeled 'To-dos' (natural language)."""
        assert ">To-dos</a>" in nav_content
        # Old label should not be present (checking nav context, not URL)
        assert ">Todos</a>" not in nav_content

    def test_documents_and_files_both_present(self, nav_content):
        """Both 'Documents' (knowledge docs) and 'Files' (uploads/artifacts) are
        distinct nav entries — PM-confirmed 2026-06-15. #1146 wired the /files
        orphan page as its own entry, superseding the earlier Files→Documents
        consciousness-relabel (#419/#684) which predated that distinct page."""
        assert ">Documents</a>" in nav_content
        assert ">Files</a>" in nav_content

    def test_lists_renamed_to_collections(self, nav_content):
        """Lists should be labeled 'Collections'."""
        assert ">Collections</a>" in nav_content
        assert ">Lists</a>" not in nav_content

    def test_learning_kept_as_is(self, nav_content):
        """Learning should remain 'Learning' (already action-oriented)."""
        assert ">Learning</a>" in nav_content


class TestNavigationTrustGating:
    """Test that navigation items are trust-gated."""

    @pytest.fixture
    def nav_content(self):
        """Load navigation template content."""
        nav_path = Path("templates/components/navigation.html")
        return nav_path.read_text()

    def test_check_in_requires_stage_3(self, nav_content):
        """Check in (Standup) requires trust stage 3+."""
        # Find the Check in link and verify it has trust-gating
        assert 'data-min-trust-stage="3"' in nav_content
        # Specifically check standup link is gated
        assert "nav-standup" in nav_content

    def test_your_stuff_dropdown_requires_stage_3(self, nav_content):
        """Your stuff dropdown requires trust stage 3+."""
        assert 'class="nav-dropdown nav-item-trust-gated"' in nav_content

    def test_documents_requires_stage_4(self, nav_content):
        """Documents (Files) requires trust stage 4+."""
        # Check for stage 4 gating on files
        assert 'data-min-trust-stage="4"' in nav_content
        assert "nav-files" in nav_content

    def test_collections_requires_stage_4(self, nav_content):
        """Collections (Lists) requires trust stage 4+."""
        assert "nav-lists" in nav_content

    def test_trust_gated_class_exists(self, nav_content):
        """Trust-gated CSS class exists for hiding items."""
        assert ".nav-item-trust-gated" in nav_content
        assert ".trust-visible" in nav_content

    def test_trust_stage_javascript_exists(self, nav_content):
        """JavaScript for trust-gating exists."""
        assert "window.trustStage" in nav_content
        assert "data-min-trust-stage" in nav_content


class TestNavigationSearchTrigger:
    """Test command palette integration (#421)."""

    @pytest.fixture
    def nav_content(self):
        """Load navigation template content."""
        nav_path = Path("templates/components/navigation.html")
        return nav_path.read_text()

    def test_search_trigger_exists(self, nav_content):
        """Search trigger button exists."""
        assert 'id="nav-search-trigger"' in nav_content

    def test_search_trigger_has_keyboard_hint(self, nav_content):
        """Search trigger shows keyboard shortcut hint."""
        assert "⌘K" in nav_content

    def test_keyboard_shortcut_handler_exists(self, nav_content):
        """Cmd/Ctrl+K keyboard handler exists."""
        assert "e.metaKey || e.ctrlKey" in nav_content
        assert "e.key === 'k'" in nav_content

    def test_custom_event_dispatched(self, nav_content):
        """Custom event is dispatched for command palette."""
        assert "openCommandPalette" in nav_content


class TestNavigationVisualHierarchy:
    """Test that nav is visually secondary to home state."""

    @pytest.fixture
    def nav_content(self):
        """Load navigation template content."""
        nav_path = Path("templates/components/navigation.html")
        return nav_path.read_text()

    def test_nav_has_muted_background(self, nav_content):
        """Nav background is muted (not white)."""
        assert "background: #fafafa" in nav_content

    def test_nav_has_no_shadow(self, nav_content):
        """Nav has no box-shadow (less prominent)."""
        assert "box-shadow: none" in nav_content

    def test_nav_links_have_muted_color(self, nav_content):
        """Nav links use muted text color."""
        assert "color: #5a6c7d" in nav_content

    def test_nav_has_smaller_height(self, nav_content):
        """Nav height is reduced (utility, not hero)."""
        assert "height: 52px" in nav_content


class TestNavigationAccessibility:
    """Test accessibility features are maintained."""

    @pytest.fixture
    def nav_content(self):
        """Load navigation template content."""
        nav_path = Path("templates/components/navigation.html")
        return nav_path.read_text()

    def test_nav_has_aria_label(self, nav_content):
        """Nav has aria-label for screen readers."""
        assert 'aria-label="Main navigation"' in nav_content

    def test_dropdowns_have_aria_haspopup(self, nav_content):
        """Dropdown buttons have aria-haspopup."""
        assert 'aria-haspopup="true"' in nav_content

    def test_dropdowns_have_aria_expanded(self, nav_content):
        """Dropdown buttons have aria-expanded."""
        assert 'aria-expanded="false"' in nav_content

    def test_hamburger_has_aria_label(self, nav_content):
        """Hamburger button has aria-label."""
        assert 'aria-label="Toggle menu"' in nav_content

    def test_search_trigger_has_aria_label(self, nav_content):
        """Search trigger has aria-label."""
        assert 'aria-label="Search' in nav_content
