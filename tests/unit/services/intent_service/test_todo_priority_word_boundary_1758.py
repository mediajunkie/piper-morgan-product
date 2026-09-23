"""Issue #1758: create-todo PRIORITY extraction — substring false positives.

`TodoIntentHandlers._extract_priority` checked `'high' in message_lower` /
`'low' in message_lower` / `'urgent' in message_lower` with no word
boundaries, so any todo whose TASK TEXT merely contained those letter
sequences got a silently wrong priority: 'add todo: highlight the report'
came back HIGH, 'add todo: buy a high chair' came back HIGH (task content,
not a priority marker), 'follow up'/'flow'/'slow'/'below' all contain 'low'.

Fix is a word-boundary tightening of the SAME three existing literals
(urgent/high/low) — no new pattern family. `_extract_priority` joins the
#1124-sibling extraction-pattern ratchet (SURFACE_SPANS["todo-create"] in
tests/test_architecture_enforcement.py; ceiling 11 -> 14, exactly the 3
`re.search` calls this fix adds).

Discovered gap, reported not fixed (per the #1758 gameplan: word-boundary
tightening only, STOP if further distinguishing needs a new pattern
family): a bare content word that IS 'high'/'low' with no explicit marker
is still ambiguous either way — 'buy a high chair' (should stay default)
and 'this is high importance' (existing regression, must stay 'high') are
both bare 'high' with no marker and opposite intended priority; nothing
word-boundary-level can tell them apart without a new pattern family.
"""

import pytest

from services.intent_service.todo_handlers import TodoIntentHandlers


@pytest.fixture
def handlers():
    return TodoIntentHandlers()


class TestPriorityFalsePositives1758:
    """The issue's exact false-positive cases — task-text content
    containing 'high'/'low'/'urgent' as a substring of another word must
    NOT set priority."""

    def test_highlight_the_report_is_medium(self, handlers):
        assert handlers._extract_priority("add todo: highlight the report") == "medium"

    def test_follow_up_with_sam_is_medium_not_low(self, handlers):
        assert handlers._extract_priority("add todo: follow up with Sam") == "medium"

    def test_follow_up_on_the_slow_lane_is_not_low(self, handlers):
        # 'follow' AND 'slow' both contain the substring 'low' —
        # double false-positive source in one message.
        assert handlers._extract_priority("follow up on the slow lane") != "low"
        assert handlers._extract_priority("follow up on the slow lane") == "medium"


class TestPriorityExplicitMarkersStillWork1758:
    """An explicit priority marker (word-bounded) must still fire."""

    def test_high_priority_marker_with_task_content(self, handlers):
        assert handlers._extract_priority("add todo: call the dentist, high priority") == "high"

    def test_urgent_marker(self, handlers):
        assert handlers._extract_priority("urgent: fix the build") == "urgent"

    def test_low_priority_marker(self, handlers):
        assert handlers._extract_priority("add todo: low priority cleanup") == "low"


class TestPriorityExistingBehaviorUnchanged1758:
    """Pre-existing behavioral tests (tests/intent_service/test_todo_handlers.py)
    pinned again here so a future extraction change can't silently regress
    them without failing THIS file too."""

    def test_fix_urgent_bug(self, handlers):
        assert handlers._extract_priority("fix urgent bug") == "urgent"

    def test_high_priority_task(self, handlers):
        assert handlers._extract_priority("high priority task") == "high"

    def test_bare_high_word_still_sets_high(self, handlers):
        """Documented tension, not a bug in this fix: a bare 'high' with no
        marker still sets priority (this is what keeps 'buy a high chair'
        unresolved — see module docstring)."""
        assert handlers._extract_priority("this is high importance") == "high"

    def test_low_priority_cleanup(self, handlers):
        assert handlers._extract_priority("low priority cleanup") == "low"

    def test_normal_task_defaults_to_medium(self, handlers):
        assert handlers._extract_priority("normal task") == "medium"


class TestBuyAHighChairKnownGap1758:
    """'add todo: buy a high chair' is the issue's headline example of the
    bug, but it is NOT in the GH issue's formal Acceptance Criteria
    checklist (only 'highlight the report' and 'follow up with Sam' are).
    It remains UNFIXED by this change and is pinned here as a documented,
    reported gap rather than silently left uncovered — see the module
    docstring for why: word-boundary tightening cannot distinguish this
    bare 'high' (task content) from 'this is high importance' (existing
    pinned regression, bare 'high' meaning priority) without a new pattern
    family, which is out of scope per the #1758 gameplan's STOP clause.
    """

    def test_buy_a_high_chair_still_misreads_as_high_documented_gap(self, handlers):
        # KNOWN GAP, reported not fixed — flip this pin if/when a
        # reviewed marker-vs-content-word design lands.
        assert handlers._extract_priority("add todo: buy a high chair") == "high"


class TestPriorityWordBoundaryEdgeCases1758:
    """Additional substring traps named in the issue body."""

    def test_thigh_does_not_set_high(self, handlers):
        assert handlers._extract_priority("add todo: stretch my thigh") == "medium"

    def test_highway_does_not_set_high(self, handlers):
        assert handlers._extract_priority("add todo: check the highway exit") == "medium"

    def test_below_does_not_set_low(self, handlers):
        assert handlers._extract_priority("add todo: see the note below") == "medium"

    def test_flow_does_not_set_low(self, handlers):
        assert handlers._extract_priority("add todo: fix the data flow") == "medium"
