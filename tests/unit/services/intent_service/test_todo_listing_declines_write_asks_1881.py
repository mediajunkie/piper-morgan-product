"""1881 — the TODO listing lane declines write asks (destructive AND
restorative) instead of answering them with a listing.

Found closing #1795 (2026-09-24): "delete my todos", "clear my todos",
"get rid of my todos", "restore my todos", "unarchive my todos" all resolved
to query/list_todos_query at surface 1 — the #1521/#1756 class (a user asks
for a write and is handed a read), on the one read lane the #1756 census had
not guarded (DESTRUCTIVE_ASK_BLOCKERS covered STATUS/TEMPORAL/MEMORY/
CALENDAR_QUERY; the todo lane had no guard at all).

The fix under test is GUARD DISCIPLINE ONLY: a shared ``_todo_query_match``
helper applies ``_is_destructive_ask`` (#1756's position-narrowed idiom)
plus the new, identically-shaped RESTORATIVE_ASK_BLOCKERS before the todo
query patterns, at BOTH entry surfaces. A decline is a fall-through to the
LLM lane (whose delete_todo emission dispatches the #1190-gated rail);
no new claim is created anywhere and TestExtractionPatternRatchet's
pre-classifier count is unchanged (blockers are not summed).

Layer honesty (m-43): every test here drives ``PreClassifier.pre_classify``
AND ``PreClassifier.detect_multiple_intents`` — the surface-1 claim only.
What the LLM lane then emits for the fall-through is its own layer.

#1595 Phase 3 (second deletion, 2026-09-27): TODO_QUERY_PATTERNS' literals
were deleted (scripts/inversion_phase3_deleted_patterns.json) — surface 1
no longer claims ANY todo-listing phrase, read or write. ``TestWriteAsksDecline``
is unaffected (an empty list still claims nothing — the WRITE_ASKS phrases
never claimed here in the first place, only the THREAT of a positional-guard
regression did, and that threat is now structurally impossible: an empty
pattern list can't be shadow-claimed by a WRITE phrase because it can't
claim anything). ``TestReadsKeepTheirClaim`` is the affected half — the
WRITE-vs-READ *guard predicate* (``_todo_query_match``'s RESTORATIVE_ASK_BLOCKERS
/ DESTRUCTIVE_ASK_BLOCKERS check) is now INERT (see the "INERT since
2026-09-27" comment on RESTORATIVE_ASK_BLOCKERS in pre_classifier.py): its
final line ANDs the guard result against ``TODO_QUERY_PATTERNS``, which is
now always False regardless of what the guard decides, so there is no
longer a surface-1 mechanism left to prove "these decline, those don't"
against. Converted to the two-part #1595 idiom instead: (a) surface 1
declines (true for every phrase now, read or write — the honest new fact),
(b) the Inversion routes the legitimate READ phrases to list_todos_query
(a stubbed router call, never a live LLM) — preserving the semantic claim
this file exists to make (these ARE reads, and route as reads downstream)
without pretending the now-inert surface-1 guard still does the work.
"""

import pytest

from services.intent_service.pre_classifier import PreClassifier
from tests.unit.services.intent_service._inversion_pin_helper import (
    assert_inversion_routes,
)

WRITE_ASKS = (
    # destructive, imperative head / request frame / intent frame / phrasal
    "delete my todos",
    "clear my todos",
    "please remove my todos",
    "can you delete my todos",
    "I want to clear my todos",
    "get rid of my todos",
    # restorative, same four positions
    "restore my todos",
    "unarchive my todos",
    "can you restore my todos",
    "let's reinstate my todos",
    "bring back my todos",
)

# Reads that mention a write verb in NON-ask position keep their claim — the
# guard is narrowed by position, not vocabulary (#1756's rule).
READS = (
    "show my todos",
    "list my todos",
    "what are my todos",
    "my todos",
    "what did I delete from my todos",
    "show my todos I restored yesterday",
)


def _single(phrase):
    return PreClassifier.pre_classify(phrase)


def _multi(phrase):
    return PreClassifier.detect_multiple_intents(phrase).intents


def _is_todo_listing(intent) -> bool:
    return intent is not None and intent.action in ("list_todos_query", "next_todo_query")


class TestWriteAsksDecline:
    @pytest.mark.parametrize("phrase", WRITE_ASKS)
    def test_single_intent_surface(self, phrase):
        intent = _single(phrase)
        assert not _is_todo_listing(
            intent
        ), f"{phrase!r} was claimed by the todo READ lane at pre_classify (1881); got {intent}"

    @pytest.mark.parametrize("phrase", WRITE_ASKS)
    def test_multi_intent_surface(self, phrase):
        intents = _multi(phrase)
        assert not any(_is_todo_listing(i) for i in intents), (
            f"{phrase!r} was claimed by the todo READ lane at detect_multiple_intents (1881); "
            f"got {[i.action for i in intents]}"
        )

    def test_shared_helper_declines(self):
        # The surfaces hand the helper the CLEANED (lower-cased) message.
        for phrase in WRITE_ASKS:
            assert PreClassifier._todo_query_match(phrase.lower()) is False, phrase


class TestReadsKeepTheirClaim:
    """#1595 Phase 3 (second deletion): surface 1 no longer claims these
    either — converted to the two-part decline+inversion-routes idiom (see
    the module docstring)."""

    @pytest.mark.parametrize("phrase", READS)
    def test_single_intent_surface(self, phrase):
        intent = _single(phrase)
        assert intent is None, (
            f"TODO_QUERY_PATTERNS is deleted — pre-classifier should no "
            f"longer claim {phrase!r} (got {intent!r})"
        )

    @pytest.mark.parametrize("phrase", READS)
    def test_multi_intent_surface(self, phrase):
        intents = _multi(phrase)
        assert intents == [], (
            f"TODO_QUERY_PATTERNS is deleted — detect_multiple_intents should "
            f"no longer claim {phrase!r} (got {[i.action for i in intents]})"
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize("phrase", READS)
    async def test_inversion_routes_the_read(self, phrase, monkeypatch):
        routed = await assert_inversion_routes(
            monkeypatch,
            phrase,
            live_categories="read_status,create_reminder",
            expected_action="list_todos_query",
        )
        assert _is_todo_listing(routed), phrase


class TestGuardIsNotAPattern:
    def test_restorative_blockers_mirror_the_destructive_shape(self):
        """Same four positions as DESTRUCTIVE_ASK_BLOCKERS — head, request
        frame, intent frame, phrasal — so the two guards stay symmetric."""
        assert len(PreClassifier.RESTORATIVE_ASK_BLOCKERS) == len(
            PreClassifier.DESTRUCTIVE_ASK_BLOCKERS
        )

    def test_no_todo_query_pattern_carries_a_write_verb(self):
        for p in PreClassifier.TODO_QUERY_PATTERNS:
            assert not any(v in p for v in ("delete", "restore", "unarchive")), p
