"""
Tests for Places integration in home.html (#684 MUX-NAV-PLACES).

Tests:
- Places section exists
- Trust-gated visibility (Stage 3+)
- Place window component included
- JavaScript initialization
"""

from pathlib import Path

import pytest


class TestHomePlacesSection:
    """Test Places section in home.html."""

    @pytest.fixture
    def home_content(self):
        """Load home template content."""
        path = Path("templates/home.html")
        return path.read_text()

    def test_places_section_exists(self, home_content):
        """Places section element exists."""
        assert 'id="places-section"' in home_content

    def test_places_container_exists(self, home_content):
        """Places container for rendering windows."""
        assert 'id="places-container"' in home_content

    def test_places_header_exists(self, home_content):
        """Places section has header."""
        # Re-skinned to the Card component (CXO design language, 6/12):
        # header is now card__title (lowercase per the design language).
        assert 'id="places-heading"' in home_content
        assert "what i'm seeing" in home_content


class TestHomePlacesTrustGating:
    """Test trust-gated visibility for Places."""

    @pytest.fixture
    def home_content(self):
        """Load home template content."""
        path = Path("templates/home.html")
        return path.read_text()

    def test_trust_stage_3_condition(self, home_content):
        """Places section requires trust stage 3+."""
        # Jinja2 condition for Stage 3+
        assert "trust_stage|default(1) >= 3" in home_content

    def test_places_section_has_trust_data_attribute(self, home_content):
        """Places section has data-trust-stage attribute."""
        assert "data-trust-stage=" in home_content


class TestHomePlacesComponent:
    """Test place_window component integration."""

    @pytest.fixture
    def home_content(self):
        """Load home template content."""
        path = Path("templates/home.html")
        return path.read_text()

    def test_place_window_included(self, home_content):
        """Place window component is included."""
        assert "{% include 'components/place_window.html' %}" in home_content

    def test_place_window_inside_trust_gate(self, home_content):
        """Place window included within trust-gated block."""
        # The include should come after the trust gate condition
        trust_gate_pos = home_content.find("trust_stage|default(1) >= 3")
        include_pos = home_content.find("{% include 'components/place_window.html' %}")
        endif_pos = home_content.find("{% endif %}", include_pos)

        assert trust_gate_pos < include_pos < endif_pos


class TestHomePlacesJavaScript:
    """Test JavaScript initialization for Places."""

    @pytest.fixture
    def home_content(self):
        """Load home template content."""
        path = Path("templates/home.html")
        return path.read_text()

    def test_places_loading_script(self, home_content):
        """JavaScript for loading Places exists."""
        assert "loadPlaces" in home_content

    def test_trust_stage_check(self, home_content):
        """JavaScript checks trust stage before loading."""
        assert "window.trustStage < 3" in home_content

    def test_place_window_loaded_check(self, home_content):
        """JavaScript checks if place_window component is loaded."""
        assert "window.placeWindowLoaded" in home_content

    def test_dom_content_loaded_listener(self, home_content):
        """Places load on DOMContentLoaded."""
        assert "DOMContentLoaded', loadPlaces" in home_content


class TestHomePlacesStyling:
    """Test Places section styling."""

    @pytest.fixture
    def home_content(self):
        """Load home template content."""
        path = Path("templates/home.html")
        return path.read_text()

    def test_places_section_styling(self, home_content):
        """Places section has styling."""
        assert ".places-section {" in home_content

    def test_places_container_styling(self, home_content):
        """Places container has flex layout."""
        assert ".places-container {" in home_content

    def test_places_loading_styling(self, home_content):
        """Loading state has styling."""
        assert ".places-loading {" in home_content
