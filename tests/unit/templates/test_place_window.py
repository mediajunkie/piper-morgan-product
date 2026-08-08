"""
Tests for place_window component (#684 MUX-NAV-PLACES).

⚠️ DEAD-TWIN NOTICE (#1522 step 1, 2026-08-08): place_window.html has NO live
includer — the "What I'm seeing" panel it implements was consolidated into the
Radar by #1236 (Places render as Radar work_item entities). These tests pin a
component no page renders; do not treat green here as evidence the panel
works. Deletion of the component + this suite is a #1522 step-2 candidate.

Tests:
- Template structure
- Type-specific styling (atmosphere)
- Confidence-based display modes
- Trust-gated visibility
- Icon definitions
"""

from pathlib import Path

import pytest


class TestPlaceWindowStructure:
    """Test that place_window has required structure."""

    @pytest.fixture
    def component_content(self):
        """Load place_window template content."""
        path = Path("templates/components/place_window.html")
        return path.read_text()

    def test_template_exists(self, component_content):
        """Template element exists for cloning."""
        assert 'id="place-window-template"' in component_content

    def test_has_place_window_class(self, component_content):
        """Window element has place-window class."""
        assert 'class="place-window"' in component_content

    def test_has_data_attributes(self, component_content):
        """Window element has required data attributes."""
        assert "data-place-id" in component_content
        assert "data-place-type" in component_content
        assert "data-confidence" in component_content
        assert "data-hardness" in component_content
        assert "data-source-url" in component_content

    def test_has_header_section(self, component_content):
        """Window has header with name and icon."""
        assert "place-window-header" in component_content
        assert "place-window-name" in component_content
        assert "place-window-icon" in component_content

    def test_has_summary_section(self, component_content):
        """Window has summary section for Piper's perspective."""
        assert "place-window-summary" in component_content

    def test_has_staleness_indicator(self, component_content):
        """Window has staleness indicator."""
        assert "place-window-staleness" in component_content

    def test_has_actions_section(self, component_content):
        """Window has actions section."""
        assert "place-window-actions" in component_content
        assert "place-window-expand" in component_content
        assert "place-window-visit" in component_content


class TestPlaceWindowAtmosphere:
    """Test type-specific atmosphere styling."""

    @pytest.fixture
    def component_content(self):
        """Load place_window template content."""
        path = Path("templates/components/place_window.html")
        return path.read_text()

    def test_issue_tracking_atmosphere(self, component_content):
        """ISSUE_TRACKING has distinct styling."""
        assert 'data-place-type="issue_tracking"' in component_content
        # Should have gray/blue palette
        assert "issue_tracking" in component_content

    def test_temporal_atmosphere(self, component_content):
        """TEMPORAL has distinct styling."""
        assert 'data-place-type="temporal"' in component_content

    def test_communication_atmosphere(self, component_content):
        """COMMUNICATION has distinct styling."""
        assert 'data-place-type="communication"' in component_content

    def test_documentation_atmosphere(self, component_content):
        """DOCUMENTATION has distinct styling."""
        assert 'data-place-type="documentation"' in component_content


class TestPlaceWindowConfidence:
    """Test confidence-based display modes."""

    @pytest.fixture
    def component_content(self):
        """Load place_window template content."""
        path = Path("templates/components/place_window.html")
        return path.read_text()

    def test_confidence_data_attribute(self, component_content):
        """Confidence is tracked in data attribute."""
        assert "data-confidence" in component_content

    def test_low_confidence_styling(self, component_content):
        """LOW confidence has distinct styling."""
        assert 'data-confidence="low"' in component_content

    def test_expand_action_for_details(self, component_content):
        """Expand action available for HIGH confidence with details."""
        assert "place-window-expand" in component_content
        assert "Show details" in component_content

    def test_visit_source_action(self, component_content):
        """Visit source action always available."""
        assert "place-window-visit" in component_content
        assert "Visit source" in component_content


class TestPlaceWindowTrustGating:
    """Test trust-gated visibility."""

    @pytest.fixture
    def component_content(self):
        """Load place_window template content."""
        path = Path("templates/components/place_window.html")
        return path.read_text()

    def test_trust_visibility_classes(self, component_content):
        """Trust visibility CSS classes exist."""
        assert "place-trust-hidden" in component_content
        assert "place-trust-visible" in component_content

    def test_apply_trust_visibility_function(self, component_content):
        """JavaScript function to apply trust visibility exists."""
        assert "applyTrustVisibility" in component_content

    def test_get_min_trust_stage_function(self, component_content):
        """Function to convert hardness to min stage exists."""
        assert "getMinTrustStage" in component_content

    def test_reads_window_trust_stage(self, component_content):
        """Reads trust stage from window.trustStage."""
        assert "window.trustStage" in component_content


class TestPlaceWindowIcons:
    """Test Place type icons."""

    @pytest.fixture
    def component_content(self):
        """Load place_window template content."""
        path = Path("templates/components/place_window.html")
        return path.read_text()

    def test_icons_object_exists(self, component_content):
        """PLACE_ICONS object exists."""
        assert "PLACE_ICONS" in component_content

    def test_issue_tracking_icon(self, component_content):
        """Issue tracking icon defined."""
        assert "issue_tracking:" in component_content

    def test_temporal_icon(self, component_content):
        """Temporal icon defined."""
        assert "temporal:" in component_content

    def test_communication_icon(self, component_content):
        """Communication icon defined."""
        assert "communication:" in component_content

    def test_documentation_icon(self, component_content):
        """Documentation icon defined."""
        assert "documentation:" in component_content


class TestPlaceWindowAPI:
    """Test JavaScript API."""

    @pytest.fixture
    def component_content(self):
        """Load place_window template content."""
        path = Path("templates/components/place_window.html")
        return path.read_text()

    def test_create_function_exposed(self, component_content):
        """PlaceWindow.create function exposed."""
        assert "window.PlaceWindow" in component_content
        assert "create: createPlaceWindow" in component_content

    def test_render_function_exposed(self, component_content):
        """PlaceWindow.render function exposed."""
        assert "render: renderPlaces" in component_content

    def test_loaded_flag_set(self, component_content):
        """placeWindowLoaded flag set when loaded."""
        assert "window.placeWindowLoaded = true" in component_content


class TestPlaceWindowAccessibility:
    """Test accessibility features."""

    @pytest.fixture
    def component_content(self):
        """Load place_window template content."""
        path = Path("templates/components/place_window.html")
        return path.read_text()

    def test_window_has_role_region(self, component_content):
        """Window has role='region' for landmark navigation."""
        assert 'role="region"' in component_content

    def test_window_has_aria_label(self, component_content):
        """Window has aria-label for screen readers."""
        assert "aria-label" in component_content

    def test_icon_hidden_from_screen_readers(self, component_content):
        """Decorative icons are aria-hidden."""
        assert 'aria-hidden="true"' in component_content

    def test_visit_link_has_rel_noopener(self, component_content):
        """External links have rel='noopener' for security."""
        assert 'rel="noopener"' in component_content
