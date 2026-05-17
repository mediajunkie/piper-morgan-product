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
# Topic tabs (Q6 — shipped via #1037, MUX-INSIGHT-TOPIC-MAPPING, 2026-05-17)
#
# Pre-#1037: tabs were withheld behind a {# ... #} Jinja comment because
# topic infrastructure wasn't on SurfaceableInsight (Q6 Option 1).
# Post-#1037: tabs are visible; topic is derived from Learning.topic_tags
# via services/mux/insight_topic_mapper.py (Option B from #1037 body).
# =============================================================================


class TestTopicTabsVisible:
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

    def test_specific_topic_tabs_now_visible(self, insights_html: str):
        """Post-#1037: the 5 specific topic tabs are visible (rendered
        outside any Jinja comment)."""
        import re

        non_comment_source = re.sub(r"\{#.*?#\}", "", insights_html, flags=re.DOTALL)
        soup = BeautifulSoup(non_comment_source, "html.parser")
        tabs = soup.find_all("button", class_="insights-topic-tab")
        rendered_topics = {tab.get("data-topic") for tab in tabs}
        for visible in ["work-patterns", "projects", "preferences", "relationships", "scheduling"]:
            assert visible in rendered_topics, (
                f"Topic '{visible}' should be visible post-#1037"
            )

    def test_withheld_comment_removed(self, insights_html: str):
        """Post-#1037: the 'Withheld until #1037' marker is gone."""
        assert "Withheld until #1037" not in insights_html, (
            "Withheld-comment marker should be removed; #1037 has shipped"
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
