"""1756 — the READ lanes decline destructive asks at surface 1.

The 2026-09-13 census ran 100 destructive shapes through the REAL
pre-classifier on BOTH entry paths (``pre_classify_with_pattern_list`` and
``detect_multiple_intents``). Four read lanes claimed them:

    STATUS_PATTERNS .......... 30/30  ("get rid of my tasks" -> status/get_project_status)
    TEMPORAL_PATTERNS ........ 24/24  ("delete the meeting tomorrow" -> temporal/get_current_time)
    MEMORY_PATTERNS .......... 15/15  ("delete our conversation history" -> memory/get_memory)
    CALENDAR_QUERY_PATTERNS ... 5/6   ("delete my meetings this week" -> query/week_calendar)

(The issue named the first three; CALENDAR_QUERY is the same failure class on
the same vocabulary — "delete my meetings this week" is a sibling of the
issue's own "delete the meeting tomorrow" — and was found by this census.
INSIGHT_PULL_PATTERNS was probed too and claimed 0/5: no work needed there.)

Why this is the higher-stakes member of the #1527 family: a surface-1 claim
SHORT-CIRCUITS the LLM lane (``classifier.py`` returns on the ``pre_classify``
branch before the LLM call, and ``classify_multiple`` returns on any non-empty
detection). The destructive ask therefore never becomes a DESTRUCTIVE rail
action, and the #1190 confirm gate — which only ever inspects rail actions —
never gets a turn on it. The user asks for a deletion and is handed a status
report, the current time, or their own memory contents.

The fix is the blocker idiom (REMINDER_QUERY_BLOCKERS #1521 /
INTEGRATION_CONNECT_BLOCKERS #1471) narrowed by POSITION rather than by
vocabulary: ``DESTRUCTIVE_ASK_BLOCKERS`` fires only when the destructive verb
heads the turn or sits under an explicit request frame. #1527's positive
evidence has no analogue here — a read lane's legitimate claim space is not
marked by any one noun. NARROWING ONLY: a blocked lane falls through, never
reroutes, and no new claim is created.

Layer honesty (m-43): every assertion below calls ``PreClassifier`` directly —
surface 1, the layer that can wrongly claim. ``TestGateSeesTheFallThrough``
checks the rail layer (registry effect declarations); it does NOT run the LLM
classifier, which needs credentials no unit test has. What is verified is the
two links this change owns: surface 1 declines, and the rail family a
destructive ask lands in is declared DESTRUCTIVE so the gate fires on it.

Denominator (m-44): 100 destructive shapes (30 STATUS / 24 TEMPORAL /
15 MEMORY / 5 INSIGHT_PULL / 6 CALENDAR / 20 misc) plus 50 read controls;
the sets below are that census verbatim, minus the 6 GITHUB_QUERY shapes,
which are a DIFFERENT lane and filed as separate discovered work.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

# ── Destructive asks, by the lane that wrongly claimed them ────────────────

STATUS_LANE_DESTRUCTIVE = (
    "get rid of my tasks",  # the issue's own probe phrase
    "delete my tasks",
    "remove my tasks",
    "clear my tasks",
    "cancel my tasks",
    "erase my tasks",
    "wipe my tasks",
    "delete my current tasks",
    "delete all active tasks",
    "remove that task status",
    "delete my assignments",
    "get rid of my assignments",
    "remove my current assignments",
    "get rid of my portfolio",
    "delete my portfolio",
    "wipe my portfolio",
    "get rid of my current work",
    "delete my current work",
    "remove my active work",
    "delete my status",
    "clear my status",
    "erase my progress",
    "delete my progress",
    "remove my progress report",
    "delete my standup",
    "cancel my standup",
    "remove the upcoming milestone",
    "delete my work status",
)

TEMPORAL_LANE_DESTRUCTIVE = (
    "delete the meeting tomorrow",  # the issue's own probe phrase
    "cancel the meeting tomorrow",
    "delete my meetings",
    "cancel my meetings",
    "remove my next meeting",
    "cancel my next meeting",
    "delete my upcoming meetings",
    "cancel the meeting today",
    "clear my calendar",
    "delete my calendar",
    "wipe my calendar",
    "clear my schedule",
    "delete my schedule",
    "erase my schedule",
    "delete my appointments",
    "cancel my appointments",
    "delete my events",
    "cancel my events",
    "remove my upcoming events",
    "delete the next event",
    "clear my free time",
    "delete my open slots",
)

MEMORY_LANE_DESTRUCTIVE = (
    "delete our conversation history",  # the issue's own probe phrase
    "delete my conversation history",
    "delete my history",
    "erase our conversation history",
    "wipe my history",
    "clear my conversation history",
    "remove my conversation history",
    "delete our past conversations",
    "erase past conversations",
    "delete previous messages",
    "remove previous conversations",
    "clear my conversation log",
    "delete the conversation log",
    "get rid of my history",
    "get rid of our conversation history",
)

CALENDAR_LANE_DESTRUCTIVE = (
    "delete my meetings this week",
    "cancel tomorrow's schedule",
    "cancel my agenda for today",
    "clear my agenda",
    "delete what's on my calendar",
)

ALL_DESTRUCTIVE = (
    STATUS_LANE_DESTRUCTIVE
    + TEMPORAL_LANE_DESTRUCTIVE
    + MEMORY_LANE_DESTRUCTIVE
    + CALENDAR_LANE_DESTRUCTIVE
)

# Categories a read lane claims into. A destructive ask reaching ANY of these
# at surface 1 is the bug — asserting on the category set (not one action)
# keeps the pin honest if a lane's action string is ever renamed.
READ_LANE_CATEGORIES = frozenset(
    {
        IntentCategory.STATUS,
        IntentCategory.TEMPORAL,
        IntentCategory.MEMORY,
        IntentCategory.QUERY,
    }
)

# ── Legitimate reads that must KEEP their claim (no over-narrowing) ────────

STATUS_READS = (
    "what am i working on",
    "my tasks",
    "show my tasks",
    "what's my status",
    "my progress",
    "project status",
    "my assignments",
    "daily standup",
    "active projects",
    "my portfolio",
    "current tasks",
    "list my tasks",
    "status report",
)
TEMPORAL_READS = (
    "what time is it",
    "what's the date",
    "my calendar",
    "show my calendar",
    "my schedule",
    "my meetings",
    "next meeting",
    "upcoming meetings",
    "my appointments",
    "my events",
    "upcoming events",
    "when am i free",
    "free time",
    "what happened yesterday",
)
MEMORY_READS = (
    "what do you remember",
    "do you remember",
    "show my history",
    "my conversation history",
    "past conversations",
    "previous conversations",
    "conversation log",
    "search my history",
    "what did we talk about",
    "how much do you remember",
    "remember when we discussed the api",
)
CALENDAR_READS = (
    "what's on my calendar",
    "meetings this week",
    "tomorrow's schedule",
)

# The load-bearing distinction: a destructive VERB in a read turn is a read
# ABOUT deletion, not a deletion. Position, not vocabulary — this is the set a
# naive `\bdelete\b` blocklist would have broken.
READS_MENTIONING_DESTRUCTIVE_VERBS = (
    "what did i delete yesterday",
    "show me my cancelled tasks",
    "what meetings did i cancel yesterday",
    "do you remember what i deleted",
    "what did we discuss about deleting projects",
)
# Deliberately NOT in the keep set: "show me my cancelled meetings" and
# "what's the status of the delete feature" claim nothing at surface 1 BEFORE
# this change either (census baseline, 2026-09-13). Pinning them as keeps
# would assert a claim that never existed — they belong to the pre-existing
# surface-1 coverage gap, not to this narrowing. They ARE pinned below in
# TestBlockerIsPositionalNotVocabulary, where the claim under test is the
# guard's own verdict rather than a lane's.

KEEP_CLAIMING = (
    STATUS_READS + TEMPORAL_READS + MEMORY_READS + CALENDAR_READS
) + READS_MENTIONING_DESTRUCTIVE_VERBS


def _single(phrase):
    return PreClassifier.pre_classify(phrase)


def _multi(phrase):
    return PreClassifier.detect_multiple_intents(phrase).intents


class TestDestructiveAsksFallThroughSingleIntentPath:
    """RED pre-fix: each phrase was claimed by a read lane at confidence 1.0.
    GREEN: no read-lane claim — the turn falls through surface 1."""

    @pytest.mark.parametrize("phrase", ALL_DESTRUCTIVE)
    def test_no_read_lane_claim(self, phrase):
        intent = _single(phrase)
        assert intent is None or intent.category not in READ_LANE_CATEGORIES, (
            f"read lane still claims the destructive ask {phrase!r} -> "
            f"{intent.category.value}/{intent.action}"
        )


class TestDestructiveAsksFallThroughMultiIntentPath:
    """The multi path is a live claim surface too — classify_multiple returns
    on any non-empty detection, so a claim here short-circuits the LLM lane
    exactly as the single path does."""

    @pytest.mark.parametrize("phrase", ALL_DESTRUCTIVE)
    def test_no_read_lane_claim(self, phrase):
        claimed = [i for i in _multi(phrase) if i.category in READ_LANE_CATEGORIES]
        assert claimed == [], (
            f"read lane still claims the destructive ask {phrase!r} on the "
            f"multi path -> {[f'{i.category.value}/{i.action}' for i in claimed]}"
        )


class TestReadsKeepTheirClaim:
    """No over-narrowing. Includes the reads that MENTION a destructive verb
    without being one — the shapes a vocabulary blocklist would have eaten."""

    @pytest.mark.parametrize("phrase", KEEP_CLAIMING)
    def test_single_intent_path_still_claims(self, phrase):
        intent = _single(phrase)
        assert intent is not None, f"read lost its claim: {phrase!r}"
        assert intent.category in READ_LANE_CATEGORIES
        assert intent.confidence == 1.0

    @pytest.mark.parametrize("phrase", KEEP_CLAIMING)
    def test_multi_intent_path_still_claims(self, phrase):
        claimed = [i for i in _multi(phrase) if i.category in READ_LANE_CATEGORIES]
        assert claimed, f"read lost its multi-path claim: {phrase!r}"


class TestBlockerIsPositionalNotVocabulary:
    """The guard's contract, pinned directly: ASK position blocks, mention
    does not. This is what keeps the narrowing from becoming the blocklist
    #1527 proved cannot contain an open claim space."""

    @pytest.mark.parametrize(
        "phrase",
        [
            "delete my tasks",
            "please delete my tasks",
            "just clear my calendar",
            "can you delete my tasks",
            "could you please cancel my meetings",
            "i want to delete my tasks",
            "i need you to wipe my history",
            "let's clear my calendar",
            "help me delete my tasks",
            "get rid of my tasks",
        ],
    )
    def test_ask_position_blocks(self, phrase):
        assert PreClassifier._is_destructive_ask(phrase) is True

    @pytest.mark.parametrize(
        "phrase",
        [
            "what did i delete yesterday",
            "show me my cancelled tasks",
            "show me my cancelled meetings",
            "what meetings did i cancel yesterday",
            "do you remember what i deleted",
            "what did we discuss about deleting projects",
            "what's the status of the delete feature",
            "my tasks",
            "what time is it",
        ],
    )
    def test_mention_does_not_block(self, phrase):
        assert PreClassifier._is_destructive_ask(phrase) is False


class TestGateSeesTheFallThrough:
    """The point of the narrowing, at the rail layer.

    With surface 1 declining, a destructive ask reaches the LLM lane, whose
    emission dispatches the action rail — and every member of the delete-todo
    family (the rail family "delete my tasks" / "get rid of my tasks" lands
    in) is declared DESTRUCTIVE, which is exactly what derives the #1190
    ``needs_confirm`` verdict. m-43: this asserts the registry's declarations,
    not a live LLM round-trip.
    """

    def test_delete_todo_family_is_confirm_gated(self):
        from services.intent_service.destructive_confirm import _DELETE_TODO_FAMILY
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()  # idempotent; the registry is import-empty
        rail = get_action_workflows()
        missing = [a for a in _DELETE_TODO_FAMILY if a not in rail]
        assert not missing, f"delete-todo rail keys unregistered: {missing}"
        ungated = [a for a in _DELETE_TODO_FAMILY if not rail[a].needs_confirm]
        assert not ungated, (
            f"rail keys reachable after the #1756 fall-through are NOT #1190 "
            f"confirm-gated: {ungated}"
        )

    @pytest.mark.parametrize("phrase", ["delete my tasks", "get rid of my tasks"])
    def test_surface_one_leaves_the_turn_for_the_gate(self, phrase):
        """Both entry paths must be silent — a claim on EITHER one returns
        before the LLM call, so the gate never sees the action."""
        assert _single(phrase) is None
        assert _multi(phrase) == []
