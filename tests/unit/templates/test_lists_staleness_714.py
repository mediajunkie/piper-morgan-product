"""
#714 — lists.html staleness UI tests.

Verifies that templates/lists.html:
- has the .resource-item.is-stale CSS rule (muted treatment)
- has the .staleness-hint CSS rule
- emits the stalenessClass + stalenessHint variables in the render loop
- conditionally adds is-stale class only when list.staleness.is_stale
- conditionally renders the hint only when staleness data is present
- uses Q5-compliant vocabulary ("Last updated", "stale") in static template
- does NOT use forbidden vocabulary (archived, RATIFIED, etc.) in visible text
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def lists_html() -> str:
    return Path("templates/lists.html").read_text()


@pytest.fixture
def soup(lists_html: str) -> BeautifulSoup:
    return BeautifulSoup(lists_html, "html.parser")


# =============================================================================
# CSS rules for muted treatment
# =============================================================================


class TestStalenessCssRules:
    def test_is_stale_class_styled(self, lists_html: str):
        """`.resource-item.is-stale` must have a CSS rule."""
        assert ".resource-item.is-stale" in lists_html

    def test_is_stale_uses_muted_treatment(self, lists_html: str):
        """The muted treatment uses opacity + tertiary background."""
        # Check both visual signals are in the rule block
        # Locate the rule by string proximity
        idx = lists_html.find(".resource-item.is-stale")
        assert idx != -1
        # Within 200 chars should be the opacity + background-color
        block = lists_html[idx : idx + 200]
        assert "opacity" in block
        assert "background-color" in block

    def test_staleness_hint_class_styled(self, lists_html: str):
        assert ".staleness-hint" in lists_html


# =============================================================================
# Render-loop conditional emission
# =============================================================================


class TestRenderLoopEmission:
    def test_staleness_class_var_emitted(self, lists_html: str):
        """Render builds stalenessClass = 'is-stale' when list.staleness.is_stale."""
        assert "stalenessClass" in lists_html
        assert "is-stale" in lists_html

    def test_staleness_hint_var_emitted(self, lists_html: str):
        """Render builds stalenessHint with 'Last updated N' wording."""
        assert "stalenessHint" in lists_html
        assert "Last updated" in lists_html

    def test_class_conditioned_on_is_stale(self, lists_html: str):
        """The class is added only when staleness.is_stale is truthy
        (graceful when staleness is absent)."""
        assert "list.staleness && list.staleness.is_stale" in lists_html

    def test_hint_conditioned_on_data_presence(self, lists_html: str):
        """The hint only renders when staleness data is present."""
        assert "list.staleness && list.staleness.last_updated_human" in lists_html


# =============================================================================
# Conceptual integrity (Q5)
# =============================================================================


class TestConceptualIntegrityVocabulary:
    """Static template should use Q5 vocabulary ('Last updated', 'stale')
    and never lifecycle stage names as visible text."""

    @pytest.mark.parametrize(
        "stage_name",
        [
            "EMERGENT",
            "DERIVED",
            "NOTICED",
            "PROPOSED",
            "RATIFIED",
            "DEPRECATED",
            "ARCHIVED",
            "COMPOSTED",
        ],
    )
    def test_no_uppercase_lifecycle_in_visible_text(
        self, lists_html: str, stage_name: str
    ):
        """No bare uppercase lifecycle stage in visible (non-script/style) text."""
        soup = BeautifulSoup(lists_html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        visible = soup.get_text()
        assert (
            stage_name not in visible
        ), f"Stage name '{stage_name}' appears in visible lists.html text"

    def test_no_archived_word_in_visible_text(self, lists_html: str):
        """The user-facing vocabulary is 'stale' / 'old' / 'untouched' /
        'last updated', NOT 'archived' (which is a lifecycle ARCHIVED concept,
        distinct from list staleness per #714 audit Q5)."""
        soup = BeautifulSoup(lists_html, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        visible = soup.get_text().lower()
        # Visible text should not contain "archived" anywhere user-facing.
        # Note: lists.html may have legitimate is_archived references in script
        # context (e.g., the API response has is_archived field) — but those
        # are in <script> which we stripped.
        assert "archived" not in visible
