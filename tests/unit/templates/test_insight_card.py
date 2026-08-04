"""
Unit tests for Insight Card Detail Component (#424 MUX-IMPLEMENT-COMPOST)

Tests the insight_card.html component for:
- Confidence language selection (D3)
- Type indicators
- Control actions (D2 compliance)
- Correction flow
- Modal behavior
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def insight_html():
    """Load the insight card component HTML."""
    component_path = Path("templates/components/insight_card.html")
    return component_path.read_text()


@pytest.fixture
def soup(insight_html):
    """Parse the component HTML."""
    return BeautifulSoup(insight_html, "html.parser")


class TestInsightCardTemplate:
    """Tests for template structure."""

    def test_template_exists(self, soup):
        """Template element should exist with correct ID."""
        template = soup.find("template", id="insight-card-detail-template")
        assert template is not None

    def test_has_modal_container(self, soup):
        """Template should have modal container."""
        template = soup.find("template", id="insight-card-detail-template")
        modal = template.find("div", class_="insight-modal")
        assert modal is not None

    def test_has_card_detail(self, soup):
        """Template should have card detail container."""
        template = soup.find("template", id="insight-card-detail-template")
        card = template.find("div", class_="insight-card-detail")
        assert card is not None


class TestInsightCardConfidence:
    """Tests for confidence language (D3 compliance)."""

    def test_confidence_language_defined(self, insight_html):
        """Should have confidence language constants."""
        assert "CONFIDENCE_LANGUAGE" in insight_html

    def test_high_confidence_text(self, insight_html):
        """High confidence should use 'I've noticed that...'."""
        # D3: "I've noticed that..." (no qualifier needed)
        assert "I've noticed that" in insight_html

    def test_medium_confidence_text(self, insight_html):
        """Medium confidence should use 'I think...'."""
        # D3: "I think..."
        assert '"I think..."' in insight_html

    def test_low_confidence_text(self, insight_html):
        """Low confidence should use 'I'm not sure...'."""
        # D3: "I'm not sure, but..."
        assert "I'm not sure" in insight_html

    def test_confidence_thresholds(self, insight_html):
        """Should use correct confidence thresholds."""
        # D3: 0.8+ high, 0.6-0.8 medium, below 0.6 low
        assert "confidence >= 0.8" in insight_html
        assert "confidence >= 0.6" in insight_html

    def test_has_confidence_bar(self, soup):
        """Should have visual confidence bar."""
        template = soup.find("template", id="insight-card-detail-template")
        bar = template.find(class_="insight-confidence-bar")
        assert bar is not None

    def test_has_confidence_text(self, soup):
        """Should have confidence text element."""
        template = soup.find("template", id="insight-card-detail-template")
        text = template.find(class_="insight-confidence-text")
        assert text is not None


class TestInsightCardTypes:
    """Tests for insight type indicators."""

    def test_type_labels_defined(self, insight_html):
        """Should have type labels defined."""
        assert "TYPE_LABELS" in insight_html

    def test_pattern_type(self, insight_html):
        """Should have pattern type label."""
        assert '"Pattern"' in insight_html or "'Pattern'" in insight_html

    def test_insight_type(self, insight_html):
        """Should have insight type label."""
        assert '"Insight"' in insight_html or "'Insight'" in insight_html

    def test_correction_type(self, insight_html):
        """Should have correction type label."""
        assert '"Correction"' in insight_html or "'Correction'" in insight_html

    def test_has_type_element(self, soup):
        """Should have type badge element."""
        template = soup.find("template", id="insight-card-detail-template")
        type_el = template.find(class_="insight-card-detail-type")
        assert type_el is not None


class TestInsightCardActions:
    """Tests for control actions (D2 compliance)."""

    def test_has_confirm_action(self, soup):
        """Should have confirm action."""
        template = soup.find("template", id="insight-card-detail-template")
        confirm = template.find(attrs={"data-action": "confirm"})
        assert confirm is not None

    def test_confirm_text(self, insight_html):
        """Confirm button should say 'That's right'."""
        assert "That's right" in insight_html

    def test_has_correct_action(self, soup):
        """Should have correct action."""
        template = soup.find("template", id="insight-card-detail-template")
        correct = template.find(attrs={"data-action": "correct"})
        assert correct is not None

    def test_has_delete_action(self, soup):
        """Should have delete action."""
        template = soup.find("template", id="insight-card-detail-template")
        delete = template.find(attrs={"data-action": "delete"})
        assert delete is not None

    def test_delete_copy_is_honest_about_soft_delete(self, insight_html):
        """#1482 (2026-08-04, supersedes the D2-era permanence pin): insight delete
        is a SOFT delete — the copy must say so honestly, never claim permanence.
        (The old assertion pinned 'cannot be undone', which was FALSE for this
        surface; PA's map + CXO's spec on #1482 carry the sourcing.)"""
        assert "cannot be undone" not in insight_html.lower()
        assert "for a while" in insight_html.lower()


class TestInsightCardCorrectionFlow:
    """Tests for correction flow (D2 compliance)."""

    def test_has_correction_flow(self, soup):
        """Should have correction flow container."""
        template = soup.find("template", id="insight-card-detail-template")
        flow = template.find(class_="insight-correction-flow")
        assert flow is not None

    def test_correction_shows_before(self, soup):
        """Correction flow should show 'before' value."""
        template = soup.find("template", id="insight-card-detail-template")
        before = template.find(class_="insight-correction-before")
        assert before is not None

    def test_correction_has_input(self, soup):
        """Correction flow should have input field."""
        template = soup.find("template", id="insight-card-detail-template")
        input_el = template.find(class_="insight-correction-input")
        assert input_el is not None

    def test_correction_has_submit(self, soup):
        """Correction flow should have submit button."""
        template = soup.find("template", id="insight-card-detail-template")
        submit = template.find(class_="insight-correction-submit")
        assert submit is not None

    def test_correction_has_cancel(self, soup):
        """Correction flow should have cancel button."""
        template = soup.find("template", id="insight-card-detail-template")
        cancel = template.find(class_="insight-correction-cancel")
        assert cancel is not None

    def test_correction_response_d2(self, insight_html):
        """Correction response should match D2 spec."""
        # D2: "Thanks, I'll remember that"
        assert "I'll remember that" in insight_html


class TestInsightCardNarrative:
    """Tests for narrative display."""

    def test_has_narrative_section(self, soup):
        """Should have narrative section."""
        template = soup.find("template", id="insight-card-detail-template")
        narrative = template.find(class_="insight-card-detail-narrative")
        assert narrative is not None

    def test_narrative_has_label(self, soup):
        """Narrative should have label."""
        template = soup.find("template", id="insight-card-detail-template")
        label = template.find(class_="insight-card-detail-narrative-label")
        assert label is not None

    def test_narrative_has_text_element(self, soup):
        """Narrative should have text element."""
        template = soup.find("template", id="insight-card-detail-template")
        text = template.find(class_="insight-card-detail-narrative-text")
        assert text is not None


class TestInsightCardSources:
    """Tests for source display."""

    def test_has_sources_element(self, soup):
        """Should have sources element."""
        template = soup.find("template", id="insight-card-detail-template")
        sources = template.find(class_="insight-card-detail-sources")
        assert sources is not None

    def test_source_count_formatting(self, insight_html):
        """Should format source count naturally."""
        assert "Based on" in insight_html
        assert "observation" in insight_html


class TestInsightCardAccessibility:
    """Tests for accessibility."""

    def test_modal_has_role(self, soup):
        """Modal should have dialog role."""
        template = soup.find("template", id="insight-card-detail-template")
        modal = template.find(class_="insight-modal")
        assert modal.get("role") == "dialog"

    def test_modal_has_aria_modal(self, soup):
        """Modal should have aria-modal."""
        template = soup.find("template", id="insight-card-detail-template")
        modal = template.find(class_="insight-modal")
        assert modal.get("aria-modal") == "true"

    def test_modal_has_aria_labelledby(self, soup):
        """Modal should have aria-labelledby."""
        template = soup.find("template", id="insight-card-detail-template")
        modal = template.find(class_="insight-modal")
        assert modal.has_attr("aria-labelledby")

    def test_close_button_has_aria_label(self, soup):
        """Close button should have aria-label."""
        template = soup.find("template", id="insight-card-detail-template")
        close = template.find(class_="insight-card-detail-close")
        assert close.has_attr("aria-label")


class TestInsightCardJavaScript:
    """Tests for JavaScript API."""

    def test_insight_card_detail_namespace(self, insight_html):
        """Should create InsightCardDetail namespace."""
        assert "window.InsightCardDetail" in insight_html

    def test_open_function_exposed(self, insight_html):
        """Should expose open function."""
        assert "open: open" in insight_html

    def test_close_function_exposed(self, insight_html):
        """Should expose close function."""
        assert "close: close" in insight_html

    def test_format_expression_exposed(self, insight_html):
        """Should expose formatExpression function."""
        assert "formatExpression: formatExpression" in insight_html

    def test_escape_to_close(self, insight_html):
        """Should close on Escape key."""
        assert "Escape" in insight_html


class TestInsightCardNoGuiltLanguage:
    """Tests to ensure no guilt language (D2 compliance)."""

    def test_no_are_you_sure(self, insight_html):
        """Should not use 'Are you sure?' which implies guilt."""
        # D2: Never argue with corrections
        js_section = insight_html.split("<script>")[1].split("</script>")[0]
        # "confirm" is OK for JavaScript confirm(), but not "Are you sure?"
        assert "are you sure" not in js_section.lower()

    def test_no_arguing(self, insight_html):
        """Should not argue with user corrections (D2)."""
        # D2: "Piper never argues with corrections"
        assert "but my data shows" not in insight_html.lower()
        assert "that contradicts" not in insight_html.lower()
