"""1795 — a restore/undo ask over reminder vocabulary must not be answered
by the reminder LIST lane.

Surfaced by the 1757 narrowing: "restore my reminders" used to be swallowed
by the greedy PORTFOLIO restore claim ("I couldn't find a project called 'my
reminders'"); once PROJECT_NOUN_REQUIRED applied to the archive/restore
family it fell through to the 1521 reminder LIST lane
(query/list_reminders_query). Neither is right — a WRITE ask answered by a
read. REMINDER_QUERY_BLOCKERS covered creation verbs and destructive verbs
but not restorative ones.

The fix under test is GUARD DISCIPLINE ONLY: REMINDER_QUERY_BLOCKERS gains
the restorative verbs (restore / unarchive / reinstate / reactivate / undo /
bring back). A blocked claim FALLS THROUGH — there is no reminder-restore
rail action at HEAD, so the LLM lane is the honest destination — and no new
pre-classifier claim is created anywhere (TestExtractionPatternRatchet's
pre-classifier count is unchanged; blockers are not summed).

Layer honesty (m-43): every test here calls ``PreClassifier.pre_classify``
AND ``PreClassifier.detect_multiple_intents`` directly — both pattern entry
surfaces, since ``_reminder_query_match`` is the shared helper each
consults. This pins the surface-1 claim only; what the LLM lane emits for
the fall-through is its own layer and is not asserted here.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier

# The issue's three phrasings plus the sibling verbs the blocker names.
RESTORE_PHRASES = (
    "restore my reminders",
    "bring back my reminders",
    "unarchive my reminders",
    "reinstate my reminders",
    "reactivate my reminders",
    "undo that and restore my reminders",
    "please restore my reminders",
)

# 1521 listing pins that must stay green — the blocker narrows, it never
# takes a legitimate read.
LISTING_PHRASES = (
    "show my reminders",
    "what reminders do I have",
    "list my reminders",
    "what are my reminders",
)


def _single(phrase):
    return PreClassifier.pre_classify(phrase)


def _multi(phrase):
    return PreClassifier.detect_multiple_intents(phrase).intents


def _is_reminder_listing(intent) -> bool:
    return intent is not None and intent.action == "list_reminders_query"


class TestRestoreDoesNotClaimListing:
    @pytest.mark.parametrize("phrase", RESTORE_PHRASES)
    def test_single_intent_surface(self, phrase):
        intent = _single(phrase)
        assert not _is_reminder_listing(intent), (
            f"{phrase!r} claimed list_reminders_query at pre_classify — a write ask "
            f"answered by the read lane (1795); got {intent}"
        )

    @pytest.mark.parametrize("phrase", RESTORE_PHRASES)
    def test_multi_intent_surface(self, phrase):
        intents = _multi(phrase)
        assert not any(_is_reminder_listing(i) for i in intents), (
            f"{phrase!r} claimed list_reminders_query at detect_multiple_intents (1795); "
            f"got {[i.action for i in intents]}"
        )

    def test_shared_helper_declines(self):
        """The shared helper both surfaces consult is where the guard lives."""
        for phrase in RESTORE_PHRASES:
            assert PreClassifier._reminder_query_match(phrase) is False, phrase


class TestListingPinsStayGreen:
    @pytest.mark.parametrize("phrase", LISTING_PHRASES)
    def test_single_intent_surface(self, phrase):
        assert _is_reminder_listing(_single(phrase)), phrase

    @pytest.mark.parametrize("phrase", LISTING_PHRASES)
    def test_multi_intent_surface(self, phrase):
        assert any(_is_reminder_listing(i) for i in _multi(phrase)), phrase


class TestGuardIsNotAPattern:
    def test_blocker_list_is_not_summed_by_the_extraction_ratchet(self):
        """Blockers narrow existing claims; they are not extraction surfaces.
        The ratchet sums ``*PATTERNS`` lists only — keep the restorative-verb
        row in REMINDER_QUERY_BLOCKERS, never in a PATTERNS list."""
        blockers = " ".join(PreClassifier.REMINDER_QUERY_BLOCKERS)
        assert "restore" in blockers and "bring" in blockers
        assert not any(
            "restore" in p for p in PreClassifier.REMINDER_QUERY_PATTERNS
        ), "restore must not appear as a reminder QUERY pattern"
