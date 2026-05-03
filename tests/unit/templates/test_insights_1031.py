"""
#1031 — Insight Journal page wiring tests (templates/insights.html).

Verifies that templates/insights.html:
- Replaces the TODO stub with a real fetch to /api/v1/insights
- Wires custom-event handlers (insight-correct/-confirm/-why/-delete/insights-reset)
  to the corresponding /api/v1/insights/* endpoints
- Server-renders trust_stage into window.trustStage
- Hides the 5 specific topic tabs (Q6 Option 1 — withhold until #1037)
  while keeping the "All" tab visible

Tests are static-template (string + DOM) checks. Live behavior in browser
verified manually per gameplan Phase 6 manual-scenarios.
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def insights_html() -> str:
    return Path("templates/insights.html").read_text()


# =============================================================================
# Real fetch replaces TODO stub
# =============================================================================


class TestRealFetch:
    def test_real_fetch_present(self, insights_html: str):
        assert "fetch('/api/v1/insights'" in insights_html
        assert "credentials: 'include'" in insights_html

    def test_todo_stub_removed(self, insights_html: str):
        """The pre-#1031 stub had `// TODO: Replace with actual API call`
        and `currentInsights = []` simulated empty. Both should be gone."""
        # The TODO line should be replaced
        assert "TODO: Replace with actual API call" not in insights_html
        # The simulated-empty line should be replaced
        assert "// Simulated empty state for now" not in insights_html


# =============================================================================
# Custom-event handlers wired to API
# =============================================================================


class TestCustomEventHandlers:
    @pytest.mark.parametrize(
        "event_name,expected_url",
        [
            ("insight-correct", "/api/v1/insights/${insight.id}/correct"),
            ("insight-confirm", "/api/v1/insights/${insight.id}/confirm"),
            ("insight-why", "/api/v1/insights/${insight.id}/why"),
            ("insight-delete", "/api/v1/insights/${insight.id}"),
            ("insights-reset", "/api/v1/insights"),
        ],
    )
    def test_event_listener_present(
        self, insights_html: str, event_name: str, expected_url: str
    ):
        """Each custom event has a `window.addEventListener('<event>', ...)`
        and the listener body references the corresponding endpoint."""
        listener_marker = f"addEventListener('{event_name}'"
        assert listener_marker in insights_html
        # Expected URL appears somewhere in the file (in the same script block)
        assert expected_url in insights_html


# =============================================================================
# Trust stage server-rendered
# =============================================================================


class TestTrustStagePlumbing:
    def test_window_trust_stage_set_from_template(self, insights_html: str):
        """window.trustStage is set from a server-rendered Jinja value."""
        assert "window.trustStage" in insights_html
        # Jinja template variable
        assert "{{ trust_stage" in insights_html


# =============================================================================
# Topic tabs hidden (Q6 Option 1)
# =============================================================================


class TestTopicTabsWithheld:
    def test_all_tab_outside_jinja_comment(self, insights_html: str):
        """The 'All' tab appears in the source OUTSIDE any {# ... #}
        comment block."""
        import re

        # Strip Jinja comments {# ... #}
        non_comment_source = re.sub(r"\{#.*?#\}", "", insights_html, flags=re.DOTALL)
        soup = BeautifulSoup(non_comment_source, "html.parser")
        tabs = soup.find_all("button", class_="insights-topic-tab")
        all_tab_count = sum(1 for tab in tabs if tab.get("data-topic") == "all")
        assert all_tab_count == 1

    def test_specific_topic_tabs_inside_jinja_comment(self, insights_html: str):
        """The 5 specific topic tabs appear ONLY inside {# ... #} blocks."""
        import re

        non_comment_source = re.sub(r"\{#.*?#\}", "", insights_html, flags=re.DOTALL)
        soup = BeautifulSoup(non_comment_source, "html.parser")
        tabs = soup.find_all("button", class_="insights-topic-tab")
        rendered_topics = {tab.get("data-topic") for tab in tabs}
        for hidden in ["work-patterns", "projects", "preferences", "relationships", "scheduling"]:
            assert hidden not in rendered_topics, (
                f"Topic '{hidden}' should be inside a Jinja comment; found outside"
            )

    def test_specific_tab_markup_preserved_in_source_for_1037(self, insights_html: str):
        """Per Q6 Option 1: tab markup is preserved (commented) so #1037
        can un-hide once topic data flows."""
        # Source file contains the comment marker + the hidden tab data attributes
        # (inside the Jinja comment block)
        assert "Withheld until #1037" in insights_html
        for hidden in ["work-patterns", "projects", "preferences", "relationships", "scheduling"]:
            assert f'data-topic="{hidden}"' in insights_html, (
                f"Hidden topic '{hidden}' should be preserved in Jinja comment"
            )


# =============================================================================
# Cross-reference: page hasn't accidentally introduced surveillance vocabulary
# =============================================================================


class TestVocabularyHygiene:
    """The Insight Journal page is the most prominent insight surface.
    Vocabulary should be reflective, not surveillance/analysis-flavored.
    """

    def test_no_surveillance_words_in_user_facing_strings(self, insights_html: str):
        """User-visible strings should not contain surveillance/analysis vocabulary
        per #1033 D3 anti-pattern principles."""
        soup = BeautifulSoup(insights_html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        visible = soup.get_text().lower()
        forbidden = [
            "monitoring",
            "surveillance",
            "tracking your",
            "analyzed your",
            "i detected",
        ]
        for word in forbidden:
            assert word not in visible, (
                f"Surveillance vocabulary '{word}' appears in user-visible text"
            )
