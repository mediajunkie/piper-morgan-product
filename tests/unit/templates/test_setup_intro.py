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


class TestSetupJsApiPaths:
    """#1320: setup.js must call setup API routes under the /api/v1 prefix.

    Regression guard for the check-keychain calls that shipped without /api/v1
    (→ 404s on the onboarding page). The router prefix is /api/v1/setup, so every
    setup fetch must carry it. (All API routes use /api/v1/ per CLAUDE.md.)
    """

    @pytest.fixture
    def setup_js(self) -> str:
        js_path = Path(__file__).parent.parent.parent.parent / "web" / "static" / "js" / "setup.js"
        return js_path.read_text()

    def test_check_keychain_uses_api_v1_prefix(self, setup_js):
        assert "/api/v1/setup/check-keychain/" in setup_js

    def test_no_unprefixed_setup_fetches(self, setup_js):
        # No fetch() to a bare `/setup/...` API path (must be /api/v1/setup/...).
        # Matches the backtick-template call form setup.js uses.
        assert "fetch(`/setup/" not in setup_js
        assert 'fetch("/setup/' not in setup_js
        assert "fetch('/setup/" not in setup_js
