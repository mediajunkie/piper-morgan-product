"""
Unit tests for Insight Journal Page (#424 MUX-IMPLEMENT-COMPOST)

Tests the insights.html page for:
- Route accessibility
- Topic organization
- Control actions (D2 compliance)
- Empty state
- Trust-gating
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def insights_html():
    """Load the insights page HTML."""
    page_path = Path("templates/insights.html")
    return page_path.read_text()


@pytest.fixture
def soup(insights_html):
    """Parse the page HTML."""
    return BeautifulSoup(insights_html, "html.parser")


class TestInsightsPageStructure:
    """Tests for page structure."""

    def test_page_has_title(self, insights_html):
        """Page should have proper title."""
        assert "Insight Journal" in insights_html

    def test_page_has_subtitle(self, insights_html):
        """Page should have Piper-voice subtitle."""
        assert "What I've learned from our work together" in insights_html

    def test_page_extends_base(self, insights_html):
        """Page should extend the app_shell layout (F2 #1171 migration)."""
        assert '{% extends "layouts/app_shell.html" %}' in insights_html

    def test_has_insights_container(self, soup):
        """Page should have main insights container."""
        container = soup.find("div", id="insights-container")
        assert container is not None

    def test_has_insights_grid(self, soup):
        """Page should have insights grid."""
        grid = soup.find("div", id="insights-grid")
        assert grid is not None


class TestInsightsTopicOrganization:
    """Tests for topic organization."""

    def test_has_topic_tabs(self, soup):
        """Page should have topic filter tabs."""
        tabs = soup.find("nav", class_="insights-topics")
        assert tabs is not None

    def test_has_all_topics(self, insights_html):
        """Page should have all required topics."""
        required_topics = [
            "Work Patterns",
            "Projects",
            "Preferences",
            "Relationships",
            "Scheduling",
        ]
        for topic in required_topics:
            assert topic in insights_html, f"Missing topic: {topic}"

    def test_topics_have_counts(self, soup):
        """Each topic tab should have a count badge."""
        topics = ["all", "work-patterns", "projects", "preferences", "relationships", "scheduling"]
        for topic in topics:
            count_el = soup.find("span", id=f"count-{topic}")
            assert count_el is not None, f"Missing count for topic: {topic}"

    def test_tabs_have_aria_selected(self, soup):
        """Topic tabs should have aria-selected attribute."""
        tabs = soup.find_all(class_="insights-topic-tab")
        for tab in tabs:
            assert tab.has_attr("aria-selected")


class TestInsightsControlActions:
    """Tests for control actions (D2 compliance)."""

    def test_has_correct_action(self, insights_html):
        """Page should have Correct action."""
        assert 'data-action="correct"' in insights_html
        # Check for button text (may have whitespace)
        assert "Correct" in insights_html

    def test_has_confirm_action(self, insights_html):
        """Page should have Confirm action (That's right)."""
        assert 'data-action="confirm"' in insights_html
        assert "That's right" in insights_html

    def test_has_delete_action(self, insights_html):
        """Page should have Delete action."""
        assert 'data-action="delete"' in insights_html
        assert "Delete" in insights_html

    def test_has_why_action(self, insights_html):
        """Page should have Why action."""
        assert 'data-action="why"' in insights_html
        assert "Why?" in insights_html

    def test_delete_has_confirmation(self, insights_html):
        """Delete should require confirmation (D2)."""
        # D2: "This deletion is permanent—I can't undo it."
        assert "cannot be undone" in insights_html.lower() or "can't undo" in insights_html.lower()

    def test_delete_response_matches_d2(self, insights_html):
        """Delete response should match D2 spec."""
        # D2: "Got it, that's gone"
        assert "that's gone" in insights_html.lower()


class TestInsightsResetFlow:
    """Tests for reset flow (D2 compliance)."""

    def test_has_reset_button(self, soup):
        """Page should have reset button."""
        reset_btn = soup.find("button", id="reset-all-btn")
        assert reset_btn is not None

    def test_reset_requires_typing(self, insights_html):
        """Reset should require typing RESET (D2)."""
        # D2: 'Type "RESET" to confirm'
        assert "RESET" in insights_html

    def test_reset_response_matches_d2(self, insights_html):
        """Reset response should match D2 spec."""
        # D2: "Starting fresh"
        assert "Starting fresh" in insights_html


class TestInsightsEmptyState:
    """Tests for empty state."""

    def test_has_empty_state(self, soup):
        """Page should have empty state element."""
        empty = soup.find("div", id="insights-empty")
        assert empty is not None

    def test_empty_state_message(self, insights_html):
        """Empty state should have friendly message."""
        # Per gameplan: "No insights yet - we'll learn together"
        assert "No insights yet" in insights_html
        assert "learn together" in insights_html.lower()


class TestInsightsAccessibility:
    """Tests for accessibility."""

    def test_container_has_role(self, soup):
        """Container should have main role."""
        container = soup.find("div", id="insights-container")
        assert container.get("role") == "main"

    def test_topics_have_tablist_role(self, soup):
        """Topic tabs container should have tablist role."""
        tabs = soup.find("nav", class_="insights-topics")
        assert tabs.get("role") == "tablist"

    def test_grid_has_list_role(self, soup):
        """Grid should have list role."""
        grid = soup.find("div", id="insights-grid")
        assert grid.get("role") == "list"

    def test_actions_have_aria_labels(self, insights_html):
        """Action buttons should have aria-labels."""
        assert 'aria-label="Correct this insight"' in insights_html
        assert 'aria-label="Delete this insight"' in insights_html
        assert 'aria-label="Confirm this insight"' in insights_html


class TestInsightsTrustGating:
    """Tests for trust gating."""

    def test_container_has_min_stage(self, soup):
        """Container should have data-min-stage attribute."""
        container = soup.find("div", id="insights-container")
        assert container.has_attr("data-min-stage")

    def test_container_starts_hidden(self, soup):
        """Container should start with trust-hidden class."""
        container = soup.find("div", id="insights-container")
        assert "trust-hidden" in container.get("class", [])


class TestInsightsJavaScript:
    """Tests for JavaScript functionality."""

    def test_insight_journal_namespace(self, insights_html):
        """Should create InsightJournal namespace."""
        assert "window.InsightJournal" in insights_html

    def test_load_insights_function(self, insights_html):
        """Should have loadInsights function."""
        assert "loadInsights" in insights_html

    def test_confidence_language(self, insights_html):
        """Should have confidence language constants."""
        assert "CONFIDENCE_TEXT" in insights_html
        assert "high confidence" in insights_html
        assert "medium confidence" in insights_html


class TestInsightsNoSurveillanceLanguage:
    """Tests to ensure no surveillance language (D3 compliance)."""

    def test_no_monitoring_word(self, insights_html):
        """Should not contain 'monitoring' in user-facing text."""
        # Check only in string literals and HTML content
        # Exclude technical code comments
        assert '"monitoring' not in insights_html.lower()
        assert "'monitoring" not in insights_html.lower()

    def test_no_tracking_word(self, insights_html):
        """Should not contain 'tracking' in user-facing text."""
        assert '"tracking' not in insights_html.lower()
        assert "'tracking" not in insights_html.lower()


class TestInsightCardTemplate:
    """Tests for insight card template."""

    def test_card_template_exists(self, soup):
        """Insight card template should exist."""
        template = soup.find("template", id="insight-card-template")
        assert template is not None

    def test_card_has_topic(self, soup):
        """Card should have topic element."""
        template = soup.find("template", id="insight-card-template")
        topic = template.find(class_="insight-card-topic")
        assert topic is not None

    def test_card_has_confidence(self, soup):
        """Card should have confidence element."""
        template = soup.find("template", id="insight-card-template")
        conf = template.find(class_="insight-card-confidence")
        assert conf is not None

    def test_card_has_text(self, soup):
        """Card should have text element."""
        template = soup.find("template", id="insight-card-template")
        text = template.find(class_="insight-card-text")
        assert text is not None

    def test_card_has_sources(self, soup):
        """Card should have sources element."""
        template = soup.find("template", id="insight-card-template")
        sources = template.find(class_="insight-card-sources")
        assert sources is not None


class TestInsightsMigratedToAppShell1171:
    """F2 #1171: /insights migrated onto app_shell — the global nav chrome is now
    SHELL-provided (the #1251 item-1 per-page nav include is retired; the shell makes
    the chrome structurally unavoidable rather than per-page-included)."""

    def test_extends_app_shell(self, insights_html):
        assert '{% extends "layouts/app_shell.html" %}' in insights_html

    def test_per_page_nav_include_retired(self, insights_html):
        # app_shell owns the chrome now — no per-page nav include needed/wanted.
        assert "{% include 'components/navigation.html' %}" not in insights_html

    def test_uses_shell_block_names(self, insights_html):
        assert "{% block main %}" in insights_html
        assert "{% block page_title %}" in insights_html
        assert "{% block head_extra %}" in insights_html

    def test_renders_with_global_nav_via_shell(self):
        # Real template.render() (NOT curl-200) — the migrated page renders inside the
        # shell: global nav chrome present, page content lands in {% block main %},
        # and the #1251 item-3 "Correct this" label is applied.
        from jinja2 import Environment, FileSystemLoader

        templates = Path(__file__).resolve().parents[3] / "templates"
        env = Environment(loader=FileSystemLoader(str(templates)), autoescape=True)
        html = env.get_template("insights.html").render(trust_stage=1)
        assert "global-nav" in html  # chrome provided by app_shell
        assert "Insight Journal" in html  # page content rendered into {% block main %}
        assert "Correct this" in html  # #1251 item-3
