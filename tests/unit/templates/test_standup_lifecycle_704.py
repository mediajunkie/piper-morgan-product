"""
#704 MUX-LIFECYCLE-UI-A — standup.html lifecycle indicator tests.

Verifies that templates/standup.html:
- includes the lifecycle_indicator component template
- emits a lifecycle-slot placeholder when item has lifecycle_state
- omits the slot when item lacks lifecycle_state (graceful degradation)
- post-processes slots into real LifecycleIndicator elements via the
  window.LifecycleIndicator.create() API
- preserves the icon prefix per Q1 disposition (Option (b): icon BEFORE
  the indicator-slot, display AFTER)
- contains no technical lifecycle stage names as visible text in the
  static template (experience phrases live in the JS API)

These are static-template tests (string + DOM matching). Live behavior
in the browser (tooltip on hover, color per stage) is verified by manual
scenario per the gameplan's Phase 3.
"""

from pathlib import Path

import pytest
from bs4 import BeautifulSoup


@pytest.fixture
def standup_html() -> str:
    return Path("templates/standup.html").read_text()


@pytest.fixture
def soup(standup_html: str) -> BeautifulSoup:
    return BeautifulSoup(standup_html, "html.parser")


# =============================================================================
# Component inclusion
# =============================================================================


class TestLifecycleComponentIncluded:
    def test_includes_lifecycle_indicator_component(self, standup_html: str):
        """standup.html must {% include %} the indicator component template
        so the <template id="lifecycle-indicator-template"> is in the DOM
        and window.LifecycleIndicator is defined when loadStandup runs."""
        assert "components/lifecycle_indicator.html" in standup_html


# =============================================================================
# Render-loop slot emission
# =============================================================================


class TestLifecycleSlotEmission:
    def test_slot_emitted_when_lifecycle_state_present(self, standup_html: str):
        """When item.lifecycle_state is truthy, render emits a
        <span class="lifecycle-slot" data-stage="..."> placeholder."""
        assert "lifecycle-slot" in standup_html
        assert 'data-stage="${item.lifecycle_state}"' in standup_html

    def test_slot_omitted_when_no_lifecycle_state(self, standup_html: str):
        """The render loop conditionally emits the slot — items without
        lifecycle_state get an empty string in that position (graceful
        degradation, no broken markup, no console error)."""
        # The conditional uses a ternary `: ''` — verify that fallback exists
        assert "item.lifecycle_state" in standup_html
        # The conditional pattern: `item.lifecycle_state ? <slot> : ''`
        assert "? `<span" in standup_html or '? "<span' in standup_html

    def test_render_loop_preserves_icon_prefix(self, standup_html: str):
        """Per Q1 disposition Option (b): icon BEFORE indicator slot, display AFTER.
        The render loop builds `${iconPart}${lifecycleSlot}${item.display ...}`."""
        # Verify the order of variables in the template literal
        assert "${iconPart}${lifecycleSlot}${item.display" in standup_html

    def test_render_loop_handles_legacy_string_items(self, standup_html: str):
        """Per #1034 Q4 safety fallback: if item is a bare string (legacy
        shape), render `<li>${item}</li>` directly — no broken markup."""
        # The conditional `if (typeof item !== 'object' || item === null)` short-circuits
        assert "typeof item !== 'object'" in standup_html


# =============================================================================
# Post-render LifecycleIndicator replacement
# =============================================================================


class TestLifecycleSlotPostprocess:
    def test_postprocess_replaces_slots_with_indicator(self, standup_html: str):
        """After innerHTML is set, render walks .lifecycle-slot elements
        and replaces each with LifecycleIndicator.create(stage, true) clone."""
        assert "querySelectorAll('.lifecycle-slot')" in standup_html
        assert "LifecycleIndicator.create(stage, true)" in standup_html
        assert "slot.replaceWith(indicator)" in standup_html

    def test_postprocess_uses_compact_mode(self, standup_html: str):
        """Indicators in standup are compact (dot-only with hover tooltip),
        not expanded (dot + phrase). Q2 disposition: existing tooltip behavior
        sufficient; the compact=true arg drives that."""
        assert "LifecycleIndicator.create(stage, true)" in standup_html

    def test_postprocess_guarded_by_window_check(self, standup_html: str):
        """The postprocess block guards on `window.LifecycleIndicator` existing
        so missing-include scenarios don't throw. Defensive consistency with
        the rest of the loadStandup error handling."""
        assert "window.LifecycleIndicator" in standup_html


# =============================================================================
# Conceptual integrity — no technical labels in static template
# =============================================================================


class TestNoTechnicalLabelsInTemplate:
    """Per gameplan AC: 'No technical labels visible (e.g., no "RATIFIED")'.

    The static template should not contain bare uppercase stage names as
    visible text. Stage names appear ONLY as data attributes (lowercase)
    and as keys in the JS API (lowercase). The user-visible text comes from
    EXPERIENCE_PHRASES populated by createIndicator at runtime.
    """

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
    def test_no_uppercase_stage_name_in_visible_text(
        self, standup_html: str, stage_name: str
    ):
        """No bare uppercase stage name should appear in standup.html as
        visible text. (Not a hard test — uppercase names may appear in code
        comments. So we check that the count is zero in *visible* text by
        parsing.)"""
        soup = BeautifulSoup(standup_html, "html.parser")
        # Get all visible text (no script/style)
        for tag in soup(["script", "style"]):
            tag.decompose()
            # Note: soup is now mutated; re-parse for a clean tree if needed
        visible_text = soup.get_text()
        assert (
            stage_name not in visible_text
        ), f"Stage name '{stage_name}' appears in visible standup.html text"

    def test_lifecycle_state_only_in_data_attribute(self, standup_html: str):
        """`lifecycle_state` from the API should only appear as a data
        attribute (`data-stage="${item.lifecycle_state}"`), never as visible
        rendered text."""
        # The literal substring `${item.lifecycle_state}` should only appear
        # inside the data-stage attribute, not as inline text in <li>.
        # Cheap proxy: count occurrences and assert all are inside data-stage.
        substring = "${item.lifecycle_state}"
        # All occurrences should be preceded by `data-stage="`
        idx = 0
        while True:
            found = standup_html.find(substring, idx)
            if found == -1:
                break
            # Look at what's before this position
            preceding = standup_html[max(0, found - 25) : found]
            assert (
                'data-stage="' in preceding
            ), f"item.lifecycle_state appears outside data-stage attribute at position {found}: {preceding!r}"
            idx = found + len(substring)
