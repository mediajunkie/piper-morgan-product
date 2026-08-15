"""#1605 — reminder/todo "clear"-family verb disambiguation (three-variant copy).

The CXO/PPM jointly-signed-off design (FINAL copy memo 2026-08-13 22:17, PPM
sign-off 22:22). The three variant strings are RATIFIED copy — a drifted word
is a bug, so this file pins them EXACTLY.

Layer honesty (m-43): the end-to-end classes drive the REAL entry the web
route calls (``IntentService.process_intent``, the #1190/#1411 test idiom),
mocked ONLY at the LLM boundary (explosive — classification is stubbed
deterministically per turn; answer turns must resolve at the pending-offer
seam, which runs before classification), the TodoManagementService boundary
(explosive wherever nothing should mutate), and the users.preferences JSONB
boundary (an in-memory dict behind collaboration_gate's _load/_save seam —
the REAL verified-inference read/write paths run against it).

Consent-matrix mapping (PPM verified the cells; asserted here behaviorally):
- Variant 1 = the #1510 rail's READ_BACK over an unverified verb mapping.
- Variant 2 = stored WRITE mapping auto-applies (no consent block for WRITE
  under an explicit imperative; disclosure-after is the design's own copy).
- Variant 3 = stored DESTRUCTIVE mapping -> CONFIRM in EVERY cell
  (decide_consent: DESTRUCTIVE x any framing x any mode = CONFIRM; and
  decide_verb_interpretation: DESTRUCTIVE candidate reads back even under
  TRUST_INFERENCES — the pinned meta cell). A stored preference changes the
  MAPPING, never the consent tier.
"""

from types import SimpleNamespace
from uuid import UUID, uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent.intent_service import IntentService
from services.intent_service import reminder_clear as rc
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import (
    CONFIRM_PENDING_ACTION_WORKFLOW,
)
from services.intent_service.reminder_clear import (
    detect_clear_family_ask,
    variant_one_question,
    variant_three_question,
    variant_two_disclosure,
)
from services.intent_service.workflow_dispatcher import (
    get_action_workflows,
    get_registered_workflows,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory

_USER = "3f7b8a52-1605-4b00-9e00-000000001605"  # valid UUID: survives principal parsing

# ---------------------------------------------------------------------------
# RATIFIED COPY PINS — exact strings (CXO FINAL 2026-08-13, PPM signed off)
# ---------------------------------------------------------------------------


class TestRatifiedCopyPins:
    def test_variant_one_verbatim(self):
        assert variant_one_question() == (
            "Before I touch these — when you say 'clear' on a reminder, "
            "do you want me to mark it done, or delete it? "
            "I'll remember for next time."
        )

    def test_variant_two_verbatim(self):
        assert variant_two_disclosure() == (
            "Marking these done — that's what 'clear' has meant for you. "
            "Say so if you meant delete this time."
        )

    def test_variant_three_verbatim(self):
        assert variant_three_question(5) == (
            "You've set 'clear' to mean delete — delete these 5 reminders? (yes/no)"
        )

    def test_variant_three_singular_grammar(self):
        """N==1 takes the grammatical singular (seam note in the module);
        the ratified N-form is the plural pinned above."""
        assert variant_three_question(1) == (
            "You've set 'clear' to mean delete — delete this reminder? (yes/no)"
        )

    def test_vocabulary_parametrization_todo_noun(self):
        """#1569 vocabulary rule: the noun tracks the user's own noun."""
        assert "'clear' on a todo" in variant_one_question(noun="todo")
        assert "delete these 3 todos?" in variant_three_question(3, noun="todo")


# ---------------------------------------------------------------------------
# Detection — clear family over the reminder/todo domain, handler-internal
# ---------------------------------------------------------------------------


class TestDetection:
    @pytest.mark.parametrize(
        "message,verb,noun",
        [
            ("clear my reminders", "clear", "reminder"),
            ("please clear the reminders", "clear", "reminder"),
            ("handle my reminders", "handle", "reminder"),
            ("take care of my todos", "take care of", "todo"),
            ("reset my todos", "reset", "todo"),
            ("can you clear my todo list", "clear", "todo"),
        ],
    )
    def test_family_verbs_detected(self, message, verb, noun):
        ask = detect_clear_family_ask(message)
        assert ask is not None
        assert ask.verb == verb
        assert ask.noun == noun
        assert ask.has_exception is False

    def test_pm_transcript_phrasing_carries_exception(self):
        """PM's original #1605 transcript phrasing — the pinned case."""
        ask = detect_clear_family_ask(
            "please clear the reminders except for 'Review the PR'"
        )
        assert ask is not None
        assert ask.has_exception is True

    @pytest.mark.parametrize(
        "message",
        [
            "delete todo 3",  # explicit verb — the gate confiscates ambiguity, never imperatives
            "complete the PR review todo",
            "mark my todos done",
            "clear my schedule",  # no reminder/todo noun
            "remove my reminders",  # explicit delete-family verb
            "",
        ],
    )
    def test_explicit_or_out_of_domain_not_claimed(self, message):
        assert detect_clear_family_ask(message) is None

    def test_reminder_wins_mixed_noun_mention(self):
        ask = detect_clear_family_ask("clear my todos and reminders")
        assert ask.noun == "reminder"


# ---------------------------------------------------------------------------
# Registry: offer-seam-only entries, effects explicit (#1557)
# ---------------------------------------------------------------------------


class TestRegistryEntries:
    def test_entries_registered_with_explicit_effects(self):
        register_default_workflows()
        w = get_registered_workflows()
        assert w[rc.CLARIFY_CLEAR_VERB_WORKFLOW].effect == EffectClass.READ
        assert w[rc.CLEAR_CORRECTION_WORKFLOW].effect == EffectClass.READ
        assert w[rc.CLEAR_DELETE_WORKFLOW].effect == EffectClass.DESTRUCTIVE

    def test_entries_are_not_rail_reachable(self):
        """action_triggered=False: a classifier emission can never fire the
        batch delete (or the re-ask entries) directly — and the destructive
        rail-scope denominator in test_destructive_confirm_1190 stays true."""
        register_default_workflows()
        rail = get_action_workflows()
        for key in (
            rc.CLARIFY_CLEAR_VERB_WORKFLOW,
            rc.CLEAR_CORRECTION_WORKFLOW,
            rc.CLEAR_DELETE_WORKFLOW,
        ):
            assert key not in rail


# ---------------------------------------------------------------------------
# The pinned meta cell (mechanism level): a DESTRUCTIVE candidate reads back
# even under "stop asking me every time" — process steering never lowers a
# destructive ask. (The behavioral halves are in the e2e class below.)
# ---------------------------------------------------------------------------


class TestMetaCellPin:
    def test_destructive_candidate_reads_back_under_trust(self):
        from services.intent_service.consent_gate import decide_verb_interpretation
        from services.intent_service.verified_inference import (
            VerificationDecision,
            VerificationMetaMode,
        )

        assert (
            decide_verb_interpretation(
                rc.VERB_CONFIDENCE,
                EffectClass.DESTRUCTIVE,
                VerificationMetaMode.TRUST_INFERENCES,
            )
            is VerificationDecision.READ_BACK
        )

    def test_write_candidate_auto_applies_under_trust(self):
        from services.intent_service.consent_gate import decide_verb_interpretation
        from services.intent_service.verified_inference import (
            VerificationDecision,
            VerificationMetaMode,
        )

        assert (
            decide_verb_interpretation(
                rc.VERB_CONFIDENCE,
                EffectClass.WRITE,
                VerificationMetaMode.TRUST_INFERENCES,
            )
            is VerificationDecision.AUTO_APPLY
        )


# ---------------------------------------------------------------------------
# End-to-end through the REAL process_intent
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn in
    these tests must resolve deterministically (the stubbed classification or
    the pending-offer seam, which runs before classification)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1605 turns must resolve "
            "deterministically"
        )


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _stub_classification(monkeypatch, service, message, action, category=IntentCategory.EXECUTION):
    """Deterministic classification for turn 1 (the LLM boundary stays
    explosive for everything else)."""
    intent = Intent(
        category=category,
        action=action,
        original_message=message,
        confidence=0.95,
        context={"original_message": message},
    )

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(
        service.intent_classifier, "classify_multiple", _classify_multiple
    )
    return intent


@pytest.fixture
def pref_store(monkeypatch):
    """In-memory users.preferences JSONB behind collaboration_gate's seam —
    the REAL verified-inference read/write code runs against it."""
    from services.intent_service import collaboration_gate as cg

    store: dict = {}

    async def _load(user_id):
        return dict(store)

    async def _save(user_id, key, value):
        store[key] = value
        return True

    monkeypatch.setattr(cg, "_load_preferences", _load)
    monkeypatch.setattr(cg, "_save_preference", _save)
    return store


def _reminder_todos():
    return [
        Todo(
            id=str(uuid4()),
            text="Review the PR",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=__import__("datetime").datetime(
                2026, 8, 13, 9, 0, tzinfo=__import__("datetime").timezone.utc
            ),
        ),
        Todo(
            id=str(uuid4()),
            text="Call the vendor",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=__import__("datetime").datetime(
                2026, 8, 13, 10, 0, tzinfo=__import__("datetime").timezone.utc
            ),
        ),
    ]


@pytest.fixture
def todo_boundary(monkeypatch):
    """TodoManagementService boundary: list is deterministic; complete/delete
    are EXPLOSIVE until a test arms them (nothing may mutate unconfirmed)."""
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": _reminder_todos(),
        "completed": [],
        "deleted": [],
        "allow_complete": False,
        "allow_delete": False,
    }

    async def _list_todos(self, user_id, include_completed=False):
        return list(state["todos"])

    async def _complete(self, todo_id, user_id):
        if not state["allow_complete"]:
            raise AssertionError(
                "todo_service.complete_todo FIRED — a mutation executed on a "
                "turn that must not mutate (#1605 gate breach)"
            )
        state["completed"].append(str(todo_id))
        for t in state["todos"]:
            if t.id == str(todo_id):
                return t
        return None

    async def _delete(self, todo_id, user_id):
        if not state["allow_delete"]:
            raise AssertionError(
                "todo_service.delete_todo FIRED — a destructive mutation "
                "executed without a confirmed yes (#1605/#1190 gate breach)"
            )
        state["deleted"].append(str(todo_id))
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "complete_todo", _complete)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


def _seed_verb_default(pref_store, value, source="user_verified"):
    pref_store["verified_inferences"] = {
        rc.inference_key("clear"): {
            "value": value,
            "source": source,
            "confidence_at_verification": rc.VERB_CONFIDENCE,
            "verified_at": "2026-08-13T22:22:00+00:00",
        }
    }


def _seed_meta_trust(pref_store):
    pref_store["inference_verification_meta"] = {
        "mode": "trust_inferences",
        "set_at": "2026-08-13T22:22:00+00:00",
    }


class TestEndToEndVariantOne:
    pytestmark = pytest.mark.asyncio

    async def test_first_encounter_asks_variant_one_verbatim(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """RED before the build: 'clear my reminders' classified complete_todo
        executed the completion guess (or, unmapped, produced a capability
        denial). GREEN: nothing mutates; the ratified variant-1 question is
        THE message; the answer binds via the pending-offer seam."""
        sid = "e2e-1605-v1"
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message == variant_one_question()
        assert result.intent_data.get("verb_disambiguation_pending") is True
        assert result.requires_clarification is True
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["pending_action"]["kind"] == rc.CLEAR_VERB_QUESTION_KIND
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []

    async def test_answer_mark_done_stores_and_completes(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """Variant 1's answer stores via the rail (store-on-verify, distinct
        provenance) AND acts on the asked-about items."""
        sid = "e2e-1605-v1-done"
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(
            message="mark them done", session_id=sid, user_id=_USER
        )
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == "complete"
        assert record["source"] == "user_verified"
        assert len(todo_boundary["completed"]) == 2
        assert "Marked 2 reminders done" in result.message
        assert "Review the PR" in result.message

    async def test_answer_delete_stores_then_confirms_before_deleting(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """'delete' as the variant-1 answer stores the mapping but does NOT
        delete — the batch still routes through the #1190 confirm (a stored
        preference changes the mapping, never the consent tier)."""
        sid = "e2e-1605-v1-delete"
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="delete them", session_id=sid, user_id=_USER
        )
        assert result.message.startswith(variant_three_question(2))
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == "delete"
        assert todo_boundary["deleted"] == []  # explosive until confirmed
        stored = _pending_offers(live_service).get(sid)
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW

        todo_boundary["allow_delete"] = True
        confirmed = await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        assert len(todo_boundary["deleted"]) == 2
        assert "Deleted 2 reminders" in confirmed.message

    async def test_decline_variant_one_changes_nothing(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-v1-no"
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="no", session_id=sid, user_id=_USER
        )
        assert "haven't touched" in result.message
        assert "verified_inferences" not in pref_store  # nothing stored
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []


class TestEndToEndVariantTwo:
    pytestmark = pytest.mark.asyncio

    async def test_stored_complete_auto_applies_with_disclosure(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """A second 'clear' auto-applies per the stored default: variant-2
        ratified disclosure leads the message, no block, items completed."""
        sid = "e2e-1605-v2"
        _seed_verb_default(pref_store, "complete")
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message.startswith(variant_two_disclosure())
        assert len(todo_boundary["completed"]) == 2
        assert result.intent_data.get("verb_default_applied") == "complete"
        # The one-turn correction window is armed.
        stored = _pending_offers(live_service).get(sid)
        assert stored["pending_action"]["kind"] == rc.CLEAR_CORRECTION_KIND

    async def test_same_turn_correction_phrase_actually_works(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """'I meant delete' on the following turn re-asks via a REAL #1190
        confirm over the just-completed items; 'yes' deletes them. The
        stored default stays 'complete' (ratified copy: 'this time')."""
        sid = "e2e-1605-v2-correct"
        _seed_verb_default(pref_store, "complete")
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        todo_boundary["allow_complete"] = True
        await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        correction = await live_service.process_intent(
            message="I meant delete", session_id=sid, user_id=_USER
        )
        assert "(yes/no)" in correction.message
        assert todo_boundary["deleted"] == []  # still gated
        todo_boundary["allow_delete"] = True
        confirmed = await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        assert len(todo_boundary["deleted"]) == 2
        assert "Deleted 2 reminders" in confirmed.message
        # This-time-only: the stored mapping did not flip.
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == "complete"


class TestEndToEndVariantThree:
    pytestmark = pytest.mark.asyncio

    async def test_stored_delete_blocks_through_real_1190_gate(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """Variant 3 reaches the REAL #1190 gate: the ratified question, the
        confirm_pending_action carrier, and NO delete until the explicit
        yes (explosive service boundary proves it)."""
        sid = "e2e-1605-v3"
        _seed_verb_default(pref_store, "delete")
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message == variant_three_question(2)
        assert result.intent_data.get("destructive_confirmation_pending") is True
        stored = _pending_offers(live_service).get(sid)
        assert stored["workflow_type"] == CONFIRM_PENDING_ACTION_WORKFLOW
        assert stored["pending_action"]["action"] == rc.CLEAR_DELETE_WORKFLOW
        assert todo_boundary["deleted"] == []

        todo_boundary["allow_delete"] = True
        confirmed = await live_service.process_intent(
            message="yes", session_id=sid, user_id=_USER
        )
        assert len(todo_boundary["deleted"]) == 2
        assert "Deleted 2 reminders" in confirmed.message
        assert "Review the PR" in confirmed.message

    async def test_no_cancels_honestly_and_nothing_fires(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-v3-no"
        _seed_verb_default(pref_store, "delete")
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="no", session_id=sid, user_id=_USER
        )
        assert "won't delete" in result.message
        assert todo_boundary["deleted"] == []
        assert _pending_offers(live_service).get(sid) is None


class TestMetaChannelStillGoverns:
    """The pinned cell pair: 'stop asking me every time' shifts variant-1
    asks per the rail's existing semantics — BUT variant 3 still blocks."""

    pytestmark = pytest.mark.asyncio

    async def test_trust_meta_auto_applies_write_candidate(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-meta-write"
        _seed_meta_trust(pref_store)
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        # No question — applied, disclosed, correctable; stored meta_auto.
        assert "(yes/no)" not in result.message
        assert result.message.startswith("Marking these done.")
        assert len(todo_boundary["completed"]) == 2
        record = pref_store["verified_inferences"][rc.inference_key("clear")]
        assert record["value"] == "complete"
        assert record["source"] == "meta_auto"

    async def test_trust_meta_does_not_lower_variant_three(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """THE cell: stored delete + TRUST_INFERENCES meta -> still the
        blocking (yes/no) confirm, nothing deleted."""
        sid = "e2e-1605-meta-destructive"
        _seed_meta_trust(pref_store)
        _seed_verb_default(pref_store, "delete")
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message == variant_three_question(2)
        assert "(yes/no)" in result.message
        assert todo_boundary["deleted"] == []

    async def test_trust_meta_destructive_candidate_still_asks_variant_one(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """Effect weighting (#1557): the classifier guessed delete_todo
        (DESTRUCTIVE candidate) — TRUST meta does NOT auto-apply; the
        variant-1 ask fires."""
        sid = "e2e-1605-meta-delete-cand"
        _seed_meta_trust(pref_store)
        _stub_classification(monkeypatch, live_service, "clear my reminders", "delete_todo")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message == variant_one_question()
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []


class TestExceptionClauseFallback:
    pytestmark = pytest.mark.asyncio

    async def test_pm_transcript_phrasing_gets_fallback(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """PM's original transcript phrasing: set-complement scope is #1563's
        lane — clarify the whole ask (variant-1-style), guess nothing, touch
        nothing, bind nothing."""
        sid = "e2e-1605-exception"
        message = "please clear the reminders except for 'Review the PR'"
        _stub_classification(monkeypatch, live_service, message, "complete_todo")
        result = await live_service.process_intent(
            message=message, session_id=sid, user_id=_USER
        )
        assert variant_one_question() in result.message
        assert result.intent_data.get("exception_clause_fallback") is True
        # 2026-08-15 contract change (PM live find): the offer IS bound now —
        # with NO targets — so the bare verb answer the question invites has
        # somewhere to land (it was falling to the floor's canned denial).
        bound = _pending_offers(live_service).get(sid)
        assert bound is not None
        assert bound["pending_action"]["exception_no_targets"] is True
        assert bound["pending_action"]["clear_target_ids"] == []  # set never resolved
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []

    async def test_exception_beats_stored_delete_default(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """Even with a stored delete default, an exception clause must not
        produce a whole-set confirm — the set can't be guessed."""
        sid = "e2e-1605-exception-stored"
        _seed_verb_default(pref_store, "delete")
        message = "please clear the reminders except for 'Review the PR'"
        _stub_classification(monkeypatch, live_service, message, "delete_todo")
        result = await live_service.process_intent(
            message=message, session_id=sid, user_id=_USER
        )
        assert "(yes/no)" not in result.message
        assert todo_boundary["deleted"] == []


class TestUnmappedSiblingClaim:
    pytestmark = pytest.mark.asyncio

    async def test_unmapped_clear_emission_gets_disambiguation_not_denial(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """The #1605 transcript bug: an unmapped clear-family emission
        ('clear_reminders') used to land on the honest-decline — a FALSE
        capability denial. Now it gets the variant-1 ask."""
        sid = "e2e-1605-unmapped"
        _stub_classification(monkeypatch, live_service, "clear my reminders", "clear_reminders")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message == variant_one_question()
        assert "can't" not in result.message.lower()
        assert result.intent_data.get("unwired_action") is None

    async def test_non_domain_unmapped_action_still_declines(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """The #1333 honest-decline is untouched for genuinely unwired asks
        (no claim widening beyond the reminder/todo domain)."""
        sid = "e2e-1605-unwired"
        _stub_classification(
            monkeypatch, live_service, "compact the database", "compact_database"
        )
        result = await live_service.process_intent(
            message="compact the database", session_id=sid, user_id=_USER
        )
        assert result.intent_data.get("unwired_action") is True


class TestExplicitVerbsUnaffected:
    pytestmark = pytest.mark.asyncio

    async def test_explicit_delete_passes_through(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """'delete todo 1' is an imperative, not an ambiguity — the flow
        returns None and the existing handler path runs unchanged."""
        sid = "e2e-1605-explicit"
        _stub_classification(monkeypatch, live_service, "delete todo 1", "delete_todo")
        todo_boundary["allow_delete"] = True
        result = await live_service.process_intent(
            message="delete todo 1", session_id=sid, user_id=_USER
        )
        assert variant_one_question() not in result.message
        assert len(todo_boundary["deleted"]) == 1  # the handler's own path ran


class TestEmptyTargets:
    pytestmark = pytest.mark.asyncio

    async def test_no_reminders_is_honest_empty_not_a_question(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-empty"
        todo_boundary["todos"] = []
        _seed_verb_default(pref_store, "delete")
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert "there are none to clear" in result.message
        assert "(yes/no)" not in result.message
        assert "Nothing has been changed" in result.message


class TestAlwaysAskLeadingQuestion:
    """CXO/PPM ruling 2026-08-14 (ratified 07:19/confirmed 07:22): under
    ALWAYS_ASK a stored complete-default is NOT flushed — a prior explicit
    answer is not an assumption — but V2's form flips from assert-then-
    disclose to a QUESTION leading with the stored value. V3 unchanged
    (already blocks in every mode)."""

    pytestmark = pytest.mark.asyncio

    def test_ratified_copy_pin(self):
        assert rc.variant_two_always_ask_question() == (
            "Want me to mark these done, like usual, or something different this time?"
        )

    async def test_always_ask_with_stored_complete_asks_instead_of_applying(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-aa"
        _seed_verb_default(pref_store, "complete")
        pref_store["inference_verification_meta"] = {
            "mode": "always_ask", "set_at": "2026-08-14T07:22:00+00:00",
        }
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message.startswith(rc.variant_two_always_ask_question())
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []
        assert result.intent_data.get("verb_disambiguation_pending") is True

    async def test_usual_answer_completes_without_flipping_store(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-aa-usual"
        _seed_verb_default(pref_store, "complete")
        pref_store["inference_verification_meta"] = {
            "mode": "always_ask", "set_at": "2026-08-14T07:22:00+00:00",
        }
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        todo_boundary["allow_complete"] = True
        await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="yes, like usual", session_id=sid, user_id=_USER
        )
        assert len(todo_boundary["completed"]) == 2
        # stored default untouched, no re-store ceremony in the copy
        assert pref_store["verified_inferences"][rc.inference_key("clear")]["value"] == "complete"
        assert "remember" not in result.message.lower()

    async def test_different_this_time_blocks_via_v3_and_keeps_store(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-aa-diff"
        _seed_verb_default(pref_store, "complete")
        pref_store["inference_verification_meta"] = {
            "mode": "always_ask", "set_at": "2026-08-14T07:22:00+00:00",
        }
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="something different this time — delete them", session_id=sid, user_id=_USER
        )
        assert "(yes/no)" in result.message
        assert todo_boundary["deleted"] == []  # gated pre-confirm
        # stored default NOT flipped ('this time' honored)
        assert pref_store["verified_inferences"][rc.inference_key("clear")]["value"] == "complete"
        assert result.intent_data.get("this_time_only") is True

    async def test_default_meta_mode_unchanged_v2_still_discloses(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-aa-default"
        _seed_verb_default(pref_store, "complete")
        _stub_classification(monkeypatch, live_service, "clear my reminders", "complete_todo")
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(
            message="clear my reminders", session_id=sid, user_id=_USER
        )
        assert result.message.startswith(variant_two_disclosure())


class TestExceptionClauseAnswerBinding:
    """PM live 2026-08-15 (v53): the exception fallback asked the verb
    question, then the bare 'delete' answer fell to the floor's canned
    denial — the question invited an answer it had nowhere to land. The
    offer now arms with NO targets: the verb stores, nothing executes,
    the explicit list is re-requested."""

    pytestmark = pytest.mark.asyncio

    async def test_pm_sequence_delete_answer_stores_and_asks_for_list(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-exc"
        _stub_classification(
            monkeypatch, live_service,
            'clear all reminders except "make sure this reminder isn\'t cleared"',
            "delete_todo",
        )
        first = await live_service.process_intent(
            message='clear all reminders except "make sure this reminder isn\'t cleared"',
            session_id=sid, user_id=_USER,
        )
        assert "carved out an exception" in first.message
        result = await live_service.process_intent(
            message="delete", session_id=sid, user_id=_USER
        )
        # the PM-hit failure was the canned denial; pin its absence
        assert "can't do that from chat" not in result.message
        assert "'clear' means delete" in result.message
        assert "exactly which" in result.message
        # verb stored; NOTHING deleted (set was never resolved)
        assert pref_store["verified_inferences"][rc.inference_key("clear")]["value"] == "delete"
        assert todo_boundary["deleted"] == []
        assert result.intent_data.get("exception_list_pending") is True

    async def test_exception_complete_answer_same_shape(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-exc2"
        _stub_classification(
            monkeypatch, live_service,
            "clear my reminders except the PR one", "complete_todo",
        )
        await live_service.process_intent(
            message="clear my reminders except the PR one", session_id=sid, user_id=_USER
        )
        result = await live_service.process_intent(
            message="mark them done", session_id=sid, user_id=_USER
        )
        assert "'clear' means mark done" in result.message
        assert todo_boundary["completed"] == []  # set never guessed


class TestNamedTargetNarrowing:
    """PM live 2026-08-15: `clear the "test the safe clarfication" reminder`
    marked ALL FOUR done. A named target now narrows to the single match or
    clarifies — never the whole set."""

    pytestmark = pytest.mark.asyncio

    async def test_pm_quoted_single_target_acts_on_one(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-named"
        _seed_verb_default(pref_store, "complete")
        msg = 'clear the "Review the PR" reminder'
        _stub_classification(monkeypatch, live_service, msg, "complete_todo")
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(message=msg, session_id=sid, user_id=_USER)
        assert len(todo_boundary["completed"]) == 1  # ONE, not the set
        assert "Review the PR" in result.message

    async def test_unmatched_named_target_clarifies_never_bulk(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-named2"
        _seed_verb_default(pref_store, "complete")
        msg = 'clear the "nonexistent thing" reminder'
        _stub_classification(monkeypatch, live_service, msg, "complete_todo")
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(message=msg, session_id=sid, user_id=_USER)
        assert todo_boundary["completed"] == []  # NOTHING acted on
        assert "couldn't confidently match" in result.message
        assert result.intent_data.get("named_target_unmatched") is True

    async def test_named_target_with_stored_delete_confirms_count_of_one(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1605-named3"
        _seed_verb_default(pref_store, "delete")
        msg = 'clear the "Review the PR" reminder'
        _stub_classification(monkeypatch, live_service, msg, "delete_todo")
        result = await live_service.process_intent(message=msg, session_id=sid, user_id=_USER)
        # V3's ratified singular grammar: N=1 renders "delete this reminder?"
        assert "delete this reminder? (yes/no)" in result.message
        assert todo_boundary["deleted"] == []  # still gated pre-confirm
