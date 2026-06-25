"""Tests for Piper intro panel in setup wizard (#547).

Tests verify that the setup.html template contains the required
Piper introduction panel elements per Issue #547 FTUX requirements.
"""

from pathlib import Path

import pytest


class TestSetupIntroPanel:
    """Test setup intro panel is present in template with required elements."""

    @pytest.fixture
    def setup_template_content(self) -> str:
        """Load setup.html template content for testing."""
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "setup.html"
        return template_path.read_text()

    def test_setup_intro_panel_renders(self, setup_template_content):
        """Verify intro panel HTML is present in setup template."""
        assert "piper-intro" in setup_template_content
        assert "Hi, I'm Piper Morgan" in setup_template_content
        assert "Let's get started" in setup_template_content

    def test_setup_intro_has_required_elements(self, setup_template_content):
        """Verify all required intro elements exist."""
        assert "piper-intro-cta" in setup_template_content  # CTA button
        assert "dismissPiperIntro" in setup_template_content  # JS function
        assert 'role="region"' in setup_template_content  # Accessibility


class TestSetupMobileLayout:
    """Test mobile layout fixes for #1319 — card positioned low on mobile.

    Root cause: iOS/Android 100vh includes hidden browser chrome. body align-items:center
    then places the card below the visible fold. Fix: flex-start + padding on mobile.
    """

    @pytest.fixture
    def setup_template_content(self) -> str:
        template_path = Path(__file__).parent.parent.parent.parent / "templates" / "setup.html"
        return template_path.read_text()

    def test_mobile_media_query_overrides_body_alignment(self, setup_template_content):
        """On mobile, body switches to flex-start so card appears at top, not below fold."""
        assert "align-items: flex-start" in setup_template_content

    def test_mobile_media_query_is_scoped_to_small_viewport(self, setup_template_content):
        # The flex-start override must be inside a mobile media query, not global
        mobile_block_start = setup_template_content.find("max-width: 480px")
        assert mobile_block_start != -1, "480px breakpoint missing"
        mobile_region = setup_template_content[mobile_block_start:]
        # flex-start should appear in or after the breakpoint declaration
        assert "align-items: flex-start" in mobile_region

    def test_mobile_body_has_vertical_padding(self, setup_template_content):
        """Mobile body padding provides comfortable space around the card."""
        # The mobile block should set padding on body
        assert "padding: 24px" in setup_template_content
