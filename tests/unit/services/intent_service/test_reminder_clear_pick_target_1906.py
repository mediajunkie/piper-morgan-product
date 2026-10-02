"""#1906 — arm the "which one do you mean?" clarify.

PM live, 2026-09-30, test card session: 'Also clear the overdue reminder' ->
'I couldn't confidently match 'overdue' to exactly one reminder — you have:
...' -> PM's 'Clear the first one.' had NOTHING to bind to (the unmatched
branch, reminder_clear.py's ``named_target_unmatched``, was the ONE branch
in this module that answered without ``set_pending_offer`` — every other
branch arms). The pick had to re-classify as a fresh turn; on alpha that
turn fell to the floor, which improvised an unarmed yes/no ask outside the
#1855 opener family, and 'Yes' found nothing to execute.

THE FIX: the unmatched branch now arms ``CLEAR_PICK_TARGET_WORKFLOW`` with
the rendered candidate list (+ each candidate's due-ish timestamp) bound at
offer time. The answer binds deterministically — an ordinal, a name/
substring match, or an unambiguous status word ("the overdue one") — and
re-enters ``_act_on_resolved_targets``, the SAME post-resolution flow a
single matched name would have taken (extracted verbatim from
``maybe_handle_clear_family`` so there is one source of truth, not a
parallel copy).

Layer honesty (m-43): the e2e classes drive the REAL
``IntentService.process_intent`` (the #1605/#1653 test idiom), mocked only
at the LLM boundary (explosive), the TodoManagementService boundary
(explosive until a test arms it), and the users.preferences JSONB boundary
(in-memory dict behind collaboration_gate's seam). No live LLM calls are
made anywhere in this file — command-release turns are chosen from
``PreClassifier.pre_classify``'s deterministic surface-1 claims so no
router/LLM stub is needed either.
"""

from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest

from services.domain.models import Intent, Todo
from services.intent.intent_service import IntentService
from services.intent_service import reminder_clear as rc
from services.intent_service.acceptance import (
    AcceptanceTier,
    acceptance_tier,
    declared_axes_for_workflow,
)
from services.intent_service.classifier import IntentClassifier
from services.intent_service.reminder_clear import (
    variant_one_question,
    variant_two_disclosure,
)
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.workflow_dispatcher import (
    get_action_workflows,
    get_registered_workflows,
)
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory

_USER = "3f7b8a52-1906-4b00-9e00-000000001906"  # valid UUID: survives principal parsing

_NOW = datetime.now(timezone.utc)
_PAST = _NOW - timedelta(days=1)
_SOON = _NOW + timedelta(days=1)
_LATER = _NOW + timedelta(days=2)


# ---------------------------------------------------------------------------
# Unit — the binding predicate itself (no service, no DB, pure function)
# ---------------------------------------------------------------------------


class TestResolvePickTargetOrdinal:
    _TEXTS = ["check the test card", "review the pr"]

    @pytest.mark.parametrize(
        "text,expected_index",
        [
            ("Clear the first one.", 0),
            ("the first one", 0),
            ("first", 0),
            ("second", 1),
            ("#2", 1),
            ("2", 1),
            ("last", 1),
        ],
    )
    def test_ordinal_forms_bind(self, text, expected_index):
        assert rc._resolve_pick_target(text, self._TEXTS, [None, None]) == (
            "bound",
            expected_index,
        )

    def test_out_of_range_ordinal_does_not_bind(self):
        """'#108' (an unrelated command's issue number) must never be read
        as a position reference into a 2-item list — it falls through to
        the other binding forms (and here, to 'none')."""
        status, idx = rc._resolve_pick_target("close issue #108", self._TEXTS, [None, None])
        assert status == "none"
        assert idx is None


class TestResolvePickTargetName:
    _TEXTS = ["check the test card", "review the pr"]

    def test_literal_substring_match_binds(self):
        assert rc._resolve_pick_target("review the pr", self._TEXTS, [None, None]) == (
            "bound",
            1,
        )

    def test_partial_significant_word_overlap_binds(self):
        """'the test card one' names no ordinal and isn't a literal
        substring of either candidate, but shares 'test'/'card' with only
        one of the two."""
        assert rc._resolve_pick_target("the test card one", self._TEXTS, [None, None]) == (
            "bound",
            0,
        )

    def test_tied_overlap_is_ambiguous(self):
        texts = ["check the test card", "check the test card again"]
        status, idx = rc._resolve_pick_target("the test card one", texts, [None, None])
        assert status == "ambiguous"
        assert idx is None

    def test_no_overlap_is_none(self):
        status, idx = rc._resolve_pick_target("maybe later", self._TEXTS, [None, None])
        assert status == "none"
        assert idx is None


class TestResolvePickTargetStatus:
    _TEXTS = ["check the test card", "review the pr"]

    def test_unambiguous_overdue_binds(self):
        due = [_PAST.isoformat(), _SOON.isoformat()]
        assert rc._resolve_pick_target("the overdue one", self._TEXTS, due) == (
            "bound",
            0,
        )

    def test_multiple_overdue_is_ambiguous(self):
        due = [_PAST.isoformat(), _PAST.isoformat()]
        status, idx = rc._resolve_pick_target("the overdue one", self._TEXTS, due)
        assert status == "ambiguous"
        assert idx is None

    def test_no_due_data_skips_the_form_honestly(self):
        """No candidate carries a timestamp — 'overdue' resolves to 'none'
        (never guessed), per the task's own instruction to skip the form
        when status isn't available."""
        status, idx = rc._resolve_pick_target("the overdue one", self._TEXTS, [None, None])
        assert status == "none"
        assert idx is None


# ---------------------------------------------------------------------------
# Registry: offer-seam-only entry, effect explicit (#1557), READ (#1906
# mirrors the clarify_reminder_clear_verb / reminder_clear_correction shape)
# ---------------------------------------------------------------------------


class TestRegistryEntry:
    def test_entry_registered_read_private_low_ceremony(self):
        register_default_workflows()
        w = get_registered_workflows()
        entry = w[rc.CLEAR_PICK_TARGET_WORKFLOW]
        assert entry.effect == EffectClass.READ
        axes = declared_axes_for_workflow(rc.CLEAR_PICK_TARGET_WORKFLOW)
        assert axes[0] == EffectClass.READ
        assert acceptance_tier(*axes) == AcceptanceTier.LOW_CEREMONY

    def test_entry_is_not_rail_reachable(self):
        """action_triggered=False: a classifier emission can never fire this
        directly — MAX_DISPATCH_SITES is untouched by this build (no new
        elif intent.action chain; registered via workflow_entries)."""
        register_default_workflows()
        rail = get_action_workflows()
        assert rc.CLEAR_PICK_TARGET_WORKFLOW not in rail


# ---------------------------------------------------------------------------
# End-to-end through the REAL process_intent
# ---------------------------------------------------------------------------


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM. Every turn
    in these tests must resolve deterministically (the stubbed
    classification, the pending-offer seam, or pre_classify's surface-1
    claim — never a live model)."""

    def __getattr__(self, name):
        raise AssertionError(
            f"LLM boundary touched ({name}) — #1906 turns must resolve " "deterministically"
        )


@pytest.fixture
def live_service():
    clf = IntentClassifier(llm_service=_ExplosiveLLM())
    return IntentService(intent_classifier=clf)


def _pending_offers(service):
    return service.workflow_offer_service._pending_offers


def _stub_classification(monkeypatch, service, message, action, category=IntentCategory.EXECUTION):
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

    monkeypatch.setattr(service.intent_classifier, "classify_multiple", _classify_multiple)
    return intent


@pytest.fixture
def pref_store(monkeypatch):
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


def _seed_verb_default(pref_store, value, source="user_verified"):
    pref_store["verified_inferences"] = {
        rc.inference_key("clear"): {
            "value": value,
            "source": source,
            "confidence_at_verification": rc.VERB_CONFIDENCE,
            "verified_at": "2026-09-30T21:00:00+00:00",
        }
    }


def _pm_transcript_todos():
    """PM's own three live candidates, verbatim ('check the test card',
    'check the test card again', 'review the pr'). Todo 1 is overdue
    (reminder_date in the past); the other two are not — exercises the
    'the overdue one' status binding unambiguously."""
    return [
        Todo(
            id=str(uuid4()),
            text="check the test card",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=_PAST,
        ),
        Todo(
            id=str(uuid4()),
            text="check the test card again",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=_SOON,
        ),
        Todo(
            id=str(uuid4()),
            text="review the pr",
            priority="medium",
            status="pending",
            completed=False,
            reminder_date=_LATER,
        ),
    ]


@pytest.fixture
def todo_boundary(monkeypatch):
    from services.todo.todo_management_service import TodoManagementService

    state = {
        "todos": _pm_transcript_todos(),
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
                "turn that must not mutate (#1906 gate breach)"
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
                "executed without a confirmed yes (#1906/#1190 gate breach)"
            )
        state["deleted"].append(str(todo_id))
        return True

    monkeypatch.setattr(TodoManagementService, "list_todos", _list_todos)
    monkeypatch.setattr(TodoManagementService, "complete_todo", _complete)
    monkeypatch.setattr(TodoManagementService, "delete_todo", _delete)
    return state


async def _arm_pick_target(monkeypatch, service, sid, todo_boundary):
    """PM's own turn 1: 'clear the overdue reminder' narrows to a named
    target ('overdue') that matches none of the three candidates literally
    -> the unmatched branch now ARMS (THE regression this issue fixes)."""
    msg = "clear the overdue reminder"
    _stub_classification(monkeypatch, service, msg, "complete_todo")
    result = await service.process_intent(message=msg, session_id=sid, user_id=_USER)
    assert "couldn't confidently match" in result.message
    assert result.intent_data.get("named_target_unmatched") is True
    stored = _pending_offers(service).get(sid)
    assert stored is not None, (
        "#1906 regression: the named-target-unmatched clarify did NOT arm — "
        "the exact bug PM hit on the test card"
    )
    assert stored["pending_action"]["kind"] == rc.CLEAR_PICK_TARGET_KIND
    assert stored["workflow_type"] == rc.CLEAR_PICK_TARGET_WORKFLOW
    assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []
    return stored


class TestArmingRegression:
    """THE pin: 'clear the overdue reminder' must arm, not just answer."""

    pytestmark = pytest.mark.asyncio

    async def test_unmatched_named_target_now_arms(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1906-arms"
        stored = await _arm_pick_target(monkeypatch, live_service, sid, todo_boundary)
        texts = stored["pending_action"]["clear_target_texts"]
        assert texts == [
            "check the test card",
            "check the test card again",
            "review the pr",
        ]
        ids = stored["pending_action"]["clear_target_ids"]
        assert len(ids) == 3
        due = stored["pending_action"]["clear_target_due"]
        assert due[0] is not None and due[1] is not None and due[2] is not None

    async def test_no_candidates_stays_unarmed(self, live_service, monkeypatch, pref_store):
        """The OTHER unmatched case — 'you don't have any right now' — has
        nothing to bind to and correctly stays unarmed."""
        from services.todo.todo_management_service import TodoManagementService

        async def _empty_list(self, user_id, include_completed=False):
            return []

        monkeypatch.setattr(TodoManagementService, "list_todos", _empty_list)
        sid = "e2e-1906-empty"
        msg = "clear the overdue reminder"
        _stub_classification(monkeypatch, live_service, msg, "complete_todo")
        result = await live_service.process_intent(message=msg, session_id=sid, user_id=_USER)
        assert "don't have any right now" in result.message
        assert _pending_offers(live_service).get(sid) is None


class TestBindingContinuesTheFlow:
    """The pick binds, then re-enters the SAME post-resolution flow a
    single matched name would have taken — asserted by proving NO fresh
    classification occurred (the explosive LLM boundary + a single
    classify_multiple stub covering only turn 1) and by the resulting
    action."""

    pytestmark = pytest.mark.asyncio

    async def test_ordinal_pick_with_stored_complete_default_applies(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """'Clear the first one.' (PM's verbatim pick) with a stored
        'complete' default re-enters variant 2: auto-applies to ONLY the
        bound item, never the whole set."""
        sid = "e2e-1906-ordinal"
        _seed_verb_default(pref_store, "complete")
        await _arm_pick_target(monkeypatch, live_service, sid, todo_boundary)
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(
            message="Clear the first one.", session_id=sid, user_id=_USER
        )
        assert result.message.startswith(variant_two_disclosure())
        assert len(todo_boundary["completed"]) == 1
        assert "check the test card" in result.message
        assert "check the test card again" not in result.message

    async def test_name_pick_with_stored_delete_default_confirms_singular(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """'review the pr' binds by name; a stored DELETE default still
        reads back through the REAL #1190 gate (singular grammar, N=1)."""
        sid = "e2e-1906-name"
        _seed_verb_default(pref_store, "delete")
        await _arm_pick_target(monkeypatch, live_service, sid, todo_boundary)
        result = await live_service.process_intent(
            message="review the pr", session_id=sid, user_id=_USER
        )
        assert "delete this reminder? (yes/no)" in result.message
        assert todo_boundary["deleted"] == []
        todo_boundary["allow_delete"] = True
        confirmed = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert len(todo_boundary["deleted"]) == 1
        assert "review the pr" in confirmed.message

    async def test_overdue_pick_binds_to_the_single_overdue_candidate(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1906-overdue"
        _seed_verb_default(pref_store, "complete")
        await _arm_pick_target(monkeypatch, live_service, sid, todo_boundary)
        todo_boundary["allow_complete"] = True
        result = await live_service.process_intent(
            message="the overdue one", session_id=sid, user_id=_USER
        )
        assert len(todo_boundary["completed"]) == 1
        assert "check the test card" in result.message
        assert "check the test card again" not in result.message

    async def test_no_stored_default_reaches_variant_one_question(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        """PM's own transcript: no stored default yet. The bind reaches
        variant 1's either/or — the SAME question a single matched name
        would have reached — never the floor's improvised yes/no ask."""
        sid = "e2e-1906-v1"
        await _arm_pick_target(monkeypatch, live_service, sid, todo_boundary)
        result = await live_service.process_intent(
            message="Clear the first one.", session_id=sid, user_id=_USER
        )
        assert result.message == variant_one_question()
        assert result.requires_clarification is True
        stored = _pending_offers(live_service).get(sid)
        assert stored["pending_action"]["kind"] == rc.CLEAR_VERB_QUESTION_KIND
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []
        # "Yes" now has something real to execute (THE live incident's fix):
        todo_boundary["allow_complete"] = True
        answered = await live_service.process_intent(
            message="mark it done", session_id=sid, user_id=_USER
        )
        assert len(todo_boundary["completed"]) == 1


class TestBareAcceptReasks:
    """'Yes' alone names nothing — re-ask via the registered generic-accept
    landing, never a blind bind."""

    pytestmark = pytest.mark.asyncio

    async def test_bare_yes_reasks_and_rearms(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1906-bareyes"
        await _arm_pick_target(monkeypatch, live_service, sid, todo_boundary)
        result = await live_service.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert "which one" in result.message.lower()
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []
        stored = _pending_offers(live_service).get(sid)
        assert stored is not None
        assert stored["pending_action"]["kind"] == rc.CLEAR_PICK_TARGET_KIND


class TestDeclineReleases:
    pytestmark = pytest.mark.asyncio

    async def test_no_declines_honestly(self, live_service, monkeypatch, pref_store, todo_boundary):
        sid = "e2e-1906-no"
        await _arm_pick_target(monkeypatch, live_service, sid, todo_boundary)
        result = await live_service.process_intent(message="no", session_id=sid, user_id=_USER)
        assert "haven't touched" in result.message
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []
        assert _pending_offers(live_service).get(sid) is None


# ---------------------------------------------------------------------------
# Turn-handler seam (unit-level, deterministic — the #1654 idiom): calling
# ``handle_reminder_clear_turn`` directly against a fake intent_service lets
# the off-intent / second-ambiguous paths be proven WITHOUT a live turn
# through process_intent's downstream routing (GitHub integration, the
# conversational floor's LLM-backed narration) — neither of which this
# carrier's own behavior is about. No LLM, no network, no DB.
# ---------------------------------------------------------------------------


def _fake_service():
    return SimpleNamespace(
        workflow_offer_service=WorkflowOfferService(),
        todo_handlers=SimpleNamespace(todo_service=None),
    )


def _pick_offer(
    ids=None,
    texts=None,
    due=None,
    verb="clear",
    noun="reminder",
    reasked=False,
    candidate_effect="WRITE",
):
    ids = ids or ["id-1", "id-2", "id-3"]
    texts = texts or [
        "check the test card",
        "check the test card again",
        "review the pr",
    ]
    due = due if due is not None else [None, None, None]
    return rc._pick_target_offer(
        _USER,
        verb,
        noun,
        ids,
        texts,
        due,
        "clear the overdue reminder",
        question="I couldn't confidently match 'overdue' to exactly one reminder.",
        reasked=reasked,
        candidate_effect=candidate_effect,
    )


class TestOffIntentReleases:
    """An unrelated product command abandons the pick (returns None —
    nothing re-armed) via the SAME #1899 reads-only discriminator the
    reminder-task carrier uses. 'give me my standup' is claimed
    deterministically at surface 1 (PreClassifier.pre_classify) — no
    router/LLM stub needed, and no live turn through process_intent.

    #1595 Phase 3 fifth deletion (2026-10-02): the original off-intent
    example here was 'close issue #108' (GITHUB_QUERY_PATTERNS). That list
    is now `[]` (tombstoned) — pre_classify no longer claims it, which would
    make `_handle_pick_target_turn`'s #1899 discriminator fall through to
    its re-ask branch instead of releasing (confirmed empirically: a direct
    probe against the live, now-tombstoned PreClassifier returns a
    "Still not sure which one" re-ask, not a release). That is a genuine
    product-behavior question for the discriminator's SECOND escape hatch
    (`read_op_claims_turn`, a destructive/non-READ op like close_issue_query
    was never going to be claimed by a reads-only oracle either) — not
    something this test-only conversion should paper over by picking a new
    example and calling the gap closed. Swapped to 'give me my standup'
    (STATUS_PATTERNS, unaffected by any of the five deletions to date,
    confirmed claiming deterministically at confidence 1.0, this session) —
    same discriminator property (an unrelated, deterministically-claimed
    command releases the pick), different example phrase. The GITHUB-claim
    gap itself is not re-litigated or fixed here (no product code touched in
    this unit)."""

    pytestmark = pytest.mark.asyncio

    async def test_unrelated_command_releases(self):
        from services.intent_service.pre_classifier import PreClassifier

        assert (
            PreClassifier.pre_classify("give me my standup") is not None
        )  # surface-1 claim, pinned

        fake = _fake_service()
        sid = "s-1906-offintent"
        offer = _pick_offer()
        result = await rc.handle_reminder_clear_turn(
            offer, "give me my standup", session_id=sid, user_id=_USER, intent_service=fake
        )
        assert result is None
        assert fake.workflow_offer_service.peek_pending_offer(sid) is None


class TestSecondAmbiguousReleases:
    """A first ambiguous answer re-asks ONCE and re-arms; a second ambiguous
    answer in a row releases honestly (returns None, nothing re-armed)
    rather than looping forever."""

    pytestmark = pytest.mark.asyncio

    async def test_ambiguous_then_ambiguous_again_releases(self):
        fake = _fake_service()
        sid = "s-1906-ambiguous"
        offer = _pick_offer()

        # "the test card one" ties between candidates 0 and 1 (both contain
        # 'test' + 'card') — ambiguous, not a bind.
        first = await rc.handle_reminder_clear_turn(
            offer, "the test card one", session_id=sid, user_id=_USER, intent_service=fake
        )
        assert first is not None
        assert first["requires_clarification"] is True
        assert "Still not sure which one" in first["message"]
        rearmed = fake.workflow_offer_service.peek_pending_offer(sid)
        assert rearmed is not None
        assert rearmed["pending_action"]["kind"] == rc.CLEAR_PICK_TARGET_KIND
        assert rearmed["pending_action"]["pick_target_reasked"] is True

        # Second ambiguous answer in a row (the SAME idiom process_intent
        # uses: pop, then hand the popped record to the turn handler).
        popped = fake.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER)
        second = await rc.handle_reminder_clear_turn(
            popped, "the test card one", session_id=sid, user_id=_USER, intent_service=fake
        )
        assert second is None  # release — no infinite loop
        assert fake.workflow_offer_service.peek_pending_offer(sid) is None


class TestPrincipalMismatch:
    pytestmark = pytest.mark.asyncio

    async def test_different_principal_cannot_bind(
        self, live_service, monkeypatch, pref_store, todo_boundary
    ):
        sid = "e2e-1906-principal"
        await _arm_pick_target(monkeypatch, live_service, sid, todo_boundary)
        other_user = str(uuid4())
        result = await live_service.process_intent(
            message="the first one", session_id=sid, user_id=other_user
        )
        assert "nothing has been changed" in result.message.lower()
        assert todo_boundary["completed"] == [] and todo_boundary["deleted"] == []
