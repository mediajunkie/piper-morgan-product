# ⚠️ DEAD-CODE TESTS as of 2026-06-19 — this whole suite tests
# templates/components/navigation.html, which is itself DEAD: no template includes it; the live
# nav is templates/components/nav_rail.html (via app_shell, #1280). These tests pass only because
# the dead file still exists on disk — they verify NO user-facing navigation. Do not extend them,
# and do not "fix" the live nav by editing navigation.html to satisfy them. They retire together
# with the dead file — see tracking issue #1298.
#
# NOTE: test_documents_and_files_both_present (below) encodes a SUPERSEDED decision. The live nav
# (nav_rail.html) collapsed Documents+Files into a single "Documents" surface via #1270's beta
# band-aid (commit a15012f33). The assertion here reflects the OLD dead-file state, not current UX.
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

    def test_lists_labeled_lists(self, nav_content):
        """#1268 (CXO 2026-06-17): the rail is labeled 'Lists' (was 'Collections') — match the
        /lists route + the user's word (descriptive-names discipline)."""
        assert ">Lists</a>" in nav_content
        assert ">Collections</a>" not in nav_content

    def test_history_trigger_labeled_radar(self, nav_content):
        """#1262 (CXO 2026-06-17): the trigger opens the Radar/Layer-2 panel → labeled 'Radar'
        (was 'History'). The id stays nav-history-trigger (JS wiring); only the label changes."""
        assert 'id="nav-history-trigger"' in nav_content  # wiring preserved
        assert 'aria-label="View Radar"' in nav_content
        assert 'aria-label="View history"' not in nav_content

    def test_learning_kept_as_is(self, nav_content):
        """Learning should remain 'Learning' (already action-oriented)."""
        assert ">Learning</a>" in nav_content


class TestNavigationTrustGating:
    """Trust-gating governs Piper CAPABILITY surfaces (Check-in / Learning / Insights),
    NOT the user's own content. Per PM 2026-06-17 + the #732 precedent ("users should
    always see their own history"): a trust gate must never hide a user's own data from
    them — "Your stuff" (todos/projects/work-items/files/documents/lists) is always
    visible. These tests guard that split."""

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

    def test_your_stuff_dropdown_not_trust_gated(self, nav_content):
        """"Your stuff" is the user's OWN content → NOT trust-gated (PM 2026-06-17; cf #732).
        A trust gate governs Piper's autonomy, never a user's access to their own data."""
        assert 'class="nav-dropdown nav-item-trust-gated"' not in nav_content
        assert 'class="nav-dropdown"' in nav_content

    def test_user_content_items_not_trust_gated(self, nav_content):
        """Documents + Collections + Files (the user's own content) are ungated —
        no stage-4 gate remains; they're present (visible at every stage)."""
        assert 'data-min-trust-stage="4"' not in nav_content
        assert "nav-documents" in nav_content
        assert "nav-lists" in nav_content
        assert "nav-files" in nav_content

    def test_capability_surfaces_still_gated(self, nav_content):
        """The trust MECHANISM still applies to Piper CAPABILITY surfaces (not user content):
        Learning stays stage-3 (progressive feature disclosure). Whether those levels are
        right is HOST/CXO's trust-model call — but the mechanism must remain wired."""
        assert 'data-min-trust-stage="3"' in nav_content
        assert "nav-learning" in nav_content

    def test_trust_gated_class_exists(self):
        """Trust-gated CSS rules exist (moved to nav.css by the #1271 extraction; the
        class *usage* on <li>s + the JS still live in navigation.html)."""
        nav_css = Path("web/static/css/nav.css").read_text()
        assert ".nav-item-trust-gated" in nav_css
        assert ".trust-visible" in nav_css

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
    """Test that nav is visually secondary to home state.

    Styles moved to web/static/css/nav.css by the #1271 extraction → these assert
    against the stylesheet now (token usage from #1264 is preserved verbatim)."""

    @pytest.fixture
    def nav_css(self):
        """Load the extracted nav stylesheet (#1271)."""
        return Path("web/static/css/nav.css").read_text()

    def test_nav_has_muted_background(self, nav_css):
        """Nav background is muted (not white)."""
        # #1264: tokenized — the muted nav bg now comes from a token (was #fafafa).
        assert "background: var(--color-neutral-off-white)" in nav_css

    def test_nav_has_no_shadow(self, nav_css):
        """Nav has no box-shadow (less prominent)."""
        assert "box-shadow: none" in nav_css

    def test_nav_links_have_muted_color(self, nav_css):
        """Nav links use muted text color."""
        # #1264: tokenized — the muted nav-link color now comes from a token (was #5a6c7d).
        assert "color: var(--color-text-nav)" in nav_css

    def test_nav_has_smaller_height(self, nav_css):
        """Nav height is reduced (utility, not hero)."""
        assert "height: 52px" in nav_css


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
