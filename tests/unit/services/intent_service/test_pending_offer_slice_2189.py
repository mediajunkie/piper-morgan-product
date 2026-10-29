"""#2189 row 1 — the #846 pending offer rides the hydrated conversation slice.

Arch's direction and condition (#2189 comments 22:36Z, 22:44Z, 23:10Z) and
CXO's verdicts (22:48Z):

- the offer round-trips through ``to_persistable_state`` /
  ``apply_persisted_state`` beside ``last_offer`` and the #1784 tombstone;
- a restart re-arms it (the #953 hydrate), a stale one is dropped silently
  unless the next message is accept-shaped (then CXO's line);
- popping a WRITE/DESTRUCTIVE offer persists the cleared slice BEFORE the
  action runs; if that write fails the action still runs, the failure is
  logged, and the consumed offer id keeps a re-hydrated copy from running
  twice;
- row 11 (session push mute) rides the same carrier.

The "DB" here is a fake ConversationManager that JSON-round-trips every
slice it stores, so a record that is not JSON-safe fails these tests.
"""

from __future__ import annotations

import json
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import pytest
from structlog.testing import capture_logs

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service import conversation_context as cc
from services.intent_service import pending_offer_slice as pos
from services.intent_service.classifier import IntentClassifier
from services.intent_service.conversation_context import ConversationContext
from services.intent_service.list_remainder import REMAINDER_MAX_AGE_MINUTES
from services.intent_service.soft_invocation import WorkflowOfferService
from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY, WorkflowEntry
from services.intent_service.workflow_entries import register_default_workflows
from services.shared_types import EffectClass, IntentCategory, Outwardness

_USER = "2189aaaa-0000-4000-8000-000000002189"
_WRITE_WF = "test_write_offer_2189"


class _ExplosiveLLM:
    """Any attribute access = the classifier consulted the LLM."""

    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


def _json_round_trip(value: Any) -> Any:
    return json.loads(json.dumps(value))


class _FakeDB:
    def __init__(self) -> None:
        self.state: Dict[str, dict] = {}


class _FakeConversationManager:
    """The three calls IntentService makes, against an in-memory 'DB'.

    ``drop_turn_saves`` = the process dies before the end-of-turn write.
    ``fail_persist`` = the early persist raises.
    """

    def __init__(self, db: _FakeDB, *, drop_turn_saves=False, fail_persist=False):
        self.db = db
        self.drop_turn_saves = drop_turn_saves
        self.fail_persist = fail_persist
        self.early_persists = 0

    async def load_context_state(self, conversation_id, user_id=None):
        state = self.db.state.get(conversation_id)
        return _json_round_trip(state) if state is not None else None

    async def get_recent_turns(self, *args, **kwargs):
        return []

    async def save_conversation_turn(self, conversation_id, context_state=None, **kwargs):
        if self.drop_turn_saves or context_state is None:
            return
        self.db.state[conversation_id] = _json_round_trip(context_state)

    async def persist_context_state(self, conversation_id, context_state, user_id=None):
        if self.fail_persist:
            raise RuntimeError("database unavailable")
        self.early_persists += 1
        self.db.state[conversation_id] = _json_round_trip(context_state)
        return True


def _service(cm: Optional[_FakeConversationManager] = None) -> IntentService:
    return IntentService(
        intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()),
        conversation_manager=cm,
    )


def _restart(session_id: str, *, new_process: bool = True) -> None:
    """The process dies: its context registry entries (and, for a new
    process, the in-process consumed-id set) are gone."""
    for key in [k for k in cc._conversation_contexts if k.endswith(f":{session_id}")]:
        del cc._conversation_contexts[key]
    if new_process:
        pos._consumed_offer_ids.clear()


def _meeting_offer() -> Dict[str, Any]:
    """The registered READ-tier soft offer ("meeting"), no pending_action."""
    ask = "I could help set up a meeting. Want me to find a time?"
    return {
        "workflow_type": "meeting",
        "offer_message": ask,
        "question": ask,
        "decline_message": "No worries, just let me know if you change your mind.",
        "trigger_message": "we should sync up about the launch",
    }


def _confirm_record() -> Dict[str, Any]:
    """A #1190 confirm-carrier-shaped record: it binds a live Intent."""
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="close_issue",
        context={"issue_number": 42, "repository": "o/r"},
        confidence=0.9,
        original_message="close issue 42",
    )
    return {
        "workflow_type": "confirm_pending_action",
        "question": 'Close issue #42 "title"? (yes/no)',
        "pending_action": {
            "kind": "destructive_confirm",
            "action": "close_issue",
            "intent": intent,
            "summary": "close issue #42",
            "armed_on": datetime(2026, 10, 29, 7, 0, 0),
            "pair": ("a", 1),
            "effect": EffectClass.DESTRUCTIVE,
        },
        "decline_message": "Okay, I haven't closed it.",
    }


@pytest.fixture
def write_workflow(monkeypatch):
    """A WRITE-effect offer-only workflow whose action counts its runs."""
    register_default_workflows()
    calls = []

    async def _run(session_id, user_id=None, context=None):
        calls.append(session_id)
        return {"message": "Done: the write ran.", "intent_data": {"action": _WRITE_WF}}

    monkeypatch.setitem(
        WORKFLOW_REGISTRY,
        _WRITE_WF,
        WorkflowEntry(
            entry_point=_run,
            effect=EffectClass.WRITE,
            outwardness=Outwardness.PRIVATE,
            description="#2189 test write offer",
        ),
    )
    return calls


def _write_offer() -> Dict[str, Any]:
    return {
        "workflow_type": _WRITE_WF,
        "question": "Want me to save that?",
        "offer_message": "Want me to save that?",
        "decline_message": "Okay, nothing saved.",
    }


# ---------------------------------------------------------------------------
# 1. The slice: round trip, codec, fail-safe hydration, stale drop
# ---------------------------------------------------------------------------


class TestSliceRoundTrip:
    def test_offer_round_trips_through_json_with_id_and_armed_at(self):
        ctx = ConversationContext()
        offer_id = ctx.arm_pending_offer(_meeting_offer())
        state = _json_round_trip(ctx.to_persistable_state())

        fresh = ConversationContext()
        fresh.apply_persisted_state(state)
        assert fresh.pending_offer == _meeting_offer()
        assert fresh.pending_offer_id == offer_id
        assert fresh.pending_offer_armed_at == ctx.pending_offer_armed_at

    def test_confirm_carrier_intent_and_tagged_values_rebuild_exactly(self):
        ctx = ConversationContext()
        ctx.arm_pending_offer(_confirm_record())
        state = _json_round_trip(ctx.to_persistable_state())

        fresh = ConversationContext()
        fresh.apply_persisted_state(state)
        pa = fresh.pending_offer["pending_action"]
        original = _confirm_record()["pending_action"]["intent"]
        assert isinstance(pa["intent"], Intent)
        assert pa["intent"].category is IntentCategory.EXECUTION
        assert pa["intent"].action == "close_issue"
        assert pa["intent"].context["issue_number"] == 42
        assert pa["intent"].original_message == original.original_message
        assert pa["armed_on"] == datetime(2026, 10, 29, 7, 0, 0)
        assert pa["pair"] == ("a", 1)
        assert pa["effect"] is EffectClass.DESTRUCTIVE

    def test_unpersistable_record_writes_none_and_never_raises(self):
        ctx = ConversationContext()
        ctx.arm_pending_offer({"workflow_type": "meeting", "thing": object()})
        with capture_logs() as logs:
            state = ctx.to_persistable_state()
        json.dumps(state)  # the slice write is never taken down
        assert state["pending_offer"] is None
        assert any(e["event"] == "pending_offer_not_persistable" for e in logs)
        assert ctx.pending_offer is not None  # in-process lifetime unchanged

    @pytest.mark.parametrize(
        "persisted",
        [
            "garbage",
            ["a"],
            {"offer_id": 5, "armed_at": datetime.now().isoformat(), "record": {}},
            {"offer_id": "x", "armed_at": datetime.now().isoformat(), "record": "nope"},
            {
                "offer_id": "x",
                "armed_at": datetime.now().isoformat(),
                "record": {"__piper_uuid__": "bad"},
            },
        ],
    )
    def test_malformed_values_are_ignored(self, persisted):
        fresh = ConversationContext()
        fresh.apply_persisted_state({"pending_offer": persisted})
        assert fresh.pending_offer is None
        assert fresh.pending_offer_id is None

    def test_legacy_state_without_the_keys_leaves_defaults(self):
        fresh = ConversationContext()
        fresh.apply_persisted_state({"last_response_was_floor": True})
        assert fresh.pending_offer is None
        assert fresh.last_consumed_offer_id is None
        assert fresh.push_session_muted_at is None

    def test_stale_offer_is_dropped_and_marks_lapsed(self):
        ctx = ConversationContext()
        ctx.arm_pending_offer(_meeting_offer())
        ctx.pending_offer_armed_at = datetime.now() - timedelta(
            minutes=REMAINDER_MAX_AGE_MINUTES, seconds=5
        )
        state = _json_round_trip(ctx.to_persistable_state())

        fresh = ConversationContext()
        fresh.apply_persisted_state(state)
        assert fresh.pending_offer is None
        assert fresh.pending_offer_lapsed is True

    def test_offer_just_inside_the_window_survives(self):
        ctx = ConversationContext()
        ctx.arm_pending_offer(_meeting_offer())
        ctx.pending_offer_armed_at = datetime.now() - timedelta(
            minutes=REMAINDER_MAX_AGE_MINUTES - 1
        )
        fresh = ConversationContext()
        fresh.apply_persisted_state(_json_round_trip(ctx.to_persistable_state()))
        assert fresh.pending_offer == _meeting_offer()
        assert fresh.pending_offer_lapsed is False

    def test_bad_armed_at_fails_toward_stale(self):
        ctx = ConversationContext()
        ctx.arm_pending_offer(_meeting_offer())
        state = _json_round_trip(ctx.to_persistable_state())
        state["pending_offer"]["armed_at"] = "not-a-time"
        fresh = ConversationContext()
        fresh.apply_persisted_state(state)
        assert fresh.pending_offer is None

    def test_a_live_in_memory_offer_is_never_overwritten_by_hydration(self):
        old = ConversationContext()
        old.arm_pending_offer(_meeting_offer())
        live = ConversationContext()
        live.arm_pending_offer(_write_offer())
        live.apply_persisted_state(_json_round_trip(old.to_persistable_state()))
        assert live.pending_offer == _write_offer()

    def test_consumed_id_on_the_slice_drops_the_offer(self):
        ctx = ConversationContext()
        offer_id = ctx.arm_pending_offer(_meeting_offer())
        state = _json_round_trip(ctx.to_persistable_state())
        state["last_consumed_offer_id"] = offer_id
        pos._consumed_offer_ids.clear()  # durable half only
        fresh = ConversationContext()
        fresh.apply_persisted_state(state)
        assert fresh.pending_offer is None
        assert fresh.last_consumed_offer_id == offer_id

    def test_every_arm_gets_a_fresh_uuid4_id(self):
        ctx = ConversationContext()
        first = ctx.arm_pending_offer(_meeting_offer())
        ctx.pop_pending_offer()
        second = ctx.arm_pending_offer(_meeting_offer())  # a re-arm is a new offer
        assert first != second
        assert len(first) == 36 and first.count("-") == 4


# ---------------------------------------------------------------------------
# 2. The service writes through; the dict is a cache of the slice
# ---------------------------------------------------------------------------


class TestServiceWriteThrough:
    def test_set_writes_the_slice_and_pop_clears_it_recording_the_id(self):
        sid = "wt-2189-a"
        svc = WorkflowOfferService()
        svc.set_pending_offer(sid, _meeting_offer(), user_id=_USER)
        ctx = cc.get_or_create_context(sid, user_id=_USER)
        armed_id = ctx.pending_offer_id
        assert ctx.pending_offer == _meeting_offer() and armed_id

        assert svc.get_and_clear_pending_offer(sid, user_id=_USER) == _meeting_offer()
        assert ctx.pending_offer is None
        assert ctx.last_consumed_offer_id == armed_id
        assert pos.was_consumed(armed_id)

    def test_a_fresh_cache_reads_the_slice(self):
        """Restart shape: a new service instance (empty cache) still peeks
        and pops the offer the slice holds."""
        sid = "wt-2189-b"
        WorkflowOfferService().set_pending_offer(sid, _meeting_offer(), user_id=_USER)
        fresh = WorkflowOfferService()
        assert fresh._pending_offers == {}
        assert fresh.peek_pending_offer(sid, user_id=_USER) == _meeting_offer()
        assert fresh.get_and_clear_pending_offer(sid, user_id=_USER) == _meeting_offer()
        assert fresh.peek_pending_offer(sid, user_id=_USER) is None

    def test_store_stays_session_keyed_across_a_principal_change(self):
        """#846's reason for session keying: alice arms, the next turn
        arrives as anonymous. The slice lookup spans principal keys."""
        sid = "wt-2189-c"
        WorkflowOfferService().set_pending_offer(sid, _meeting_offer(), user_id=_USER)
        fresh = WorkflowOfferService()
        assert fresh.get_and_clear_pending_offer(sid, user_id=None) == _meeting_offer()
        assert cc.get_or_create_context(sid, user_id=_USER).pending_offer is None

    def test_peek_identity_is_stable_for_the_before_after_arm_check(self):
        """The multi-intent loop compares peeks by identity (``after is not
        before``); a slice-backed peek must return the same object."""
        sid = "wt-2189-d"
        WorkflowOfferService().set_pending_offer(sid, _meeting_offer(), user_id=_USER)
        fresh = WorkflowOfferService()
        assert fresh.peek_pending_offer(sid, user_id=_USER) is fresh.peek_pending_offer(
            sid, user_id=_USER
        )

    def test_no_clobber_guard_peeks_the_rehydrated_slice(self):
        """#1753/#1770: ``_apply_soft_offer``'s guard peeks the store before
        arming a soft offer. After a restart only the slice holds the arm; the
        peek must still see it, or a soft offer would clobber the re-armed
        one."""
        sid = "wt-2189-e"
        old = ConversationContext()
        old.arm_pending_offer(_write_offer())
        state = _json_round_trip(old.to_persistable_state())
        _restart(sid)
        cc.get_or_create_context(sid, user_id=_USER).apply_persisted_state(state)

        svc = _service()
        assert svc.workflow_offer_service._pending_offers == {}
        assert svc.workflow_offer_service.peek_pending_offer(sid, user_id=_USER) == _write_offer()


# ---------------------------------------------------------------------------
# 3. Restart, end to end through process_intent
# ---------------------------------------------------------------------------


class TestRestartEndToEnd:
    pytestmark = pytest.mark.asyncio

    async def test_read_offer_survives_a_restart_and_is_consumable(self):
        sid = "e2e-2189-read"
        db = _FakeDB()
        svc = _service(_FakeConversationManager(db))
        svc.workflow_offer_service.set_pending_offer(sid, _meeting_offer(), user_id=_USER)
        # the end-of-turn write of the arming turn
        db.state[sid] = _json_round_trip(cc.snapshot_session_slice(sid, user_id=_USER))
        assert db.state[sid]["pending_offer"] is not None

        _restart(sid)
        restarted = _service(_FakeConversationManager(db))
        assert restarted.workflow_offer_service._pending_offers == {}
        result = await restarted.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.success
        assert result.intent_data.get("action") != "pending_offer_lapsed"
        # consumed: the end-of-turn write carried the cleared slice
        assert db.state[sid]["pending_offer"] is None
        assert db.state[sid]["last_consumed_offer_id"]

    async def test_read_offer_rides_the_end_of_turn_write_only(self):
        sid = "e2e-2189-read-no-early"
        db = _FakeDB()
        cm = _FakeConversationManager(db)
        svc = _service(cm)
        svc.workflow_offer_service.set_pending_offer(sid, _meeting_offer(), user_id=_USER)
        await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert cm.early_persists == 0

    async def test_stale_offer_then_yes_gets_cxos_line(self):
        sid = "e2e-2189-stale-yes"
        db = _FakeDB()
        old = ConversationContext()
        old.arm_pending_offer(_write_offer())
        old.pending_offer_armed_at = datetime.now() - timedelta(
            minutes=REMAINDER_MAX_AGE_MINUTES + 5
        )
        db.state[sid] = _json_round_trip(old.to_persistable_state())

        _restart(sid)
        svc = _service(_FakeConversationManager(db))
        result = await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.message == pos.LAPSED_OFFER_REPLY
        assert result.message == (
            "That was a while ago, so I let it go. Ask me again and I'll pick it up."
        )

    async def test_stale_offer_then_other_message_is_silent(self):
        sid = "e2e-2189-stale-other"
        ctx = cc.get_or_create_context(sid, user_id=_USER)
        ctx.pending_offer_lapsed = True
        svc = _service()
        assert svc._lapsed_offer_reply(sid, _USER, "what's on my calendar") is None
        assert ctx.pending_offer_lapsed is False  # one turn only
        assert svc._lapsed_offer_reply(sid, _USER, "yes") is None  # already spent


# ---------------------------------------------------------------------------
# 4. Arch's condition: the crash test, both arms
# ---------------------------------------------------------------------------


async def _yes_lands_on_nothing(service: IntentService, sid: str) -> None:
    """With no offer armed, "yes" is an ordinary fresh message: the offer seam
    does not claim it and it reaches the classifier, whose LLM boundary is
    explosive here. Reaching that boundary is the proof nothing was armed."""
    from services.intent.intent_service import IntentProcessingError

    with pytest.raises(IntentProcessingError, match="INTENT_CLASSIFICATION_FAILED"):
        await service.process_intent(message="yes", session_id=sid, user_id=_USER)


class TestWriteOfferEarlyPersistCrash:
    pytestmark = pytest.mark.asyncio

    async def _arm_and_persist(self, svc, db, sid):
        svc.workflow_offer_service.set_pending_offer(sid, _write_offer(), user_id=_USER)
        db.state[sid] = _json_round_trip(cc.snapshot_session_slice(sid, user_id=_USER))
        armed_id = db.state[sid]["pending_offer"]["offer_id"]
        assert armed_id
        return armed_id

    async def test_a_persist_succeeds_then_crash_a_fresh_hydrate_has_no_offer(self, write_workflow):
        sid = "crash-2189-a"
        db = _FakeDB()
        cm = _FakeConversationManager(db, drop_turn_saves=True)  # dies before end-of-turn
        svc = _service(cm)
        armed_id = await self._arm_and_persist(svc, db, sid)

        result = await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.message == "Done: the write ran."
        assert write_workflow == [sid]
        assert cm.early_persists == 1
        assert db.state[sid]["pending_offer"] is None  # cleared BEFORE the action
        assert db.state[sid]["last_consumed_offer_id"] == armed_id

        # crash: a new process, nothing in memory
        _restart(sid, new_process=True)
        fresh = ConversationContext()
        fresh.apply_persisted_state(_json_round_trip(db.state[sid]))
        assert fresh.pending_offer is None

        restarted = _service(_FakeConversationManager(db))
        assert restarted.workflow_offer_service.peek_pending_offer(sid, user_id=_USER) is None
        await _yes_lands_on_nothing(restarted, sid)
        assert write_workflow == [sid]  # the same "yes" did not write twice

    async def test_b_persist_fails_action_still_runs_and_consumed_id_drops_it(self, write_workflow):
        sid = "crash-2189-b"
        db = _FakeDB()
        cm = _FakeConversationManager(db, drop_turn_saves=True, fail_persist=True)
        svc = _service(cm)
        armed_id = await self._arm_and_persist(svc, db, sid)

        with capture_logs() as logs:
            result = await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert result.message == "Done: the write ran."  # not refused over storage
        assert write_workflow == [sid]
        failed = [e for e in logs if e["event"] == "pending_offer_early_persist_failed"]
        assert len(failed) == 1
        assert failed[0]["session_id"] == sid and failed[0]["offer_id"] == armed_id
        assert failed[0]["log_level"] == "warning"
        # ids and the error type only: no user text, no exception message
        assert set(failed[0]) == {"event", "log_level", "session_id", "offer_id", "error_type"}
        assert failed[0]["error_type"] == "RuntimeError"

        # the previous slice still holds the spent offer
        assert db.state[sid]["pending_offer"]["offer_id"] == armed_id

        # a fresh context hydrated from that slice drops it by the consumed id
        _restart(sid, new_process=False)
        fresh = ConversationContext()
        fresh.apply_persisted_state(_json_round_trip(db.state[sid]))
        assert fresh.pending_offer is None

        restarted = _service(_FakeConversationManager(db))
        await _yes_lands_on_nothing(restarted, sid)
        assert write_workflow == [sid]  # never runs twice

    async def test_the_end_of_turn_write_and_the_early_write_share_the_snapshot(
        self, write_workflow, monkeypatch
    ):
        """Both seams call ``snapshot_session_slice``: the factored
        "persist this session's slice now" path."""
        sid = "crash-2189-shared"
        db = _FakeDB()
        svc = _service(_FakeConversationManager(db))
        await self._arm_and_persist(svc, db, sid)
        seen = []
        real = cc.snapshot_session_slice

        def _spy(session_id, user_id=None):
            seen.append(session_id)
            return real(session_id, user_id=user_id)

        import services.intent.intent_service as isvc

        monkeypatch.setattr(isvc, "snapshot_session_slice", _spy)
        await svc.process_intent(message="yes", session_id=sid, user_id=_USER)
        assert seen == [sid, sid]  # early persist, then end of turn


class TestOfferEffect:
    def test_write_and_destructive_entries_are_write_effect(self):
        register_default_workflows()
        assert pos.offer_is_write_effect({"workflow_type": "confirm_pending_action"})
        assert pos.offer_is_write_effect({"workflow_type": "standup_complete_todo"})

    def test_plain_read_offer_is_not(self):
        register_default_workflows()
        assert not pos.offer_is_write_effect(_meeting_offer())

    def test_unknown_entry_or_seam_owned_read_offer_fails_safe_to_write(self):
        register_default_workflows()
        assert pos.offer_is_write_effect({"workflow_type": "no_such_workflow"})
        # #1648: clarify_reminder_time is READ, but its seam saves the reminder
        assert pos.offer_is_write_effect(
            {"workflow_type": "clarify_reminder_time", "pending_action": {"kind": "x"}}
        )


# ---------------------------------------------------------------------------
# 5. Row 19: the Slack path's IntentService sees the same offer per session
# ---------------------------------------------------------------------------


class TestSlackPathSharesTheSlice:
    def test_slack_handlers_intent_service_sees_the_web_arm(self):
        from services.integrations.slack.response_handler import SlackResponseHandler

        sid = "slack-2189"
        web = _service()
        web.workflow_offer_service.set_pending_offer(sid, _meeting_offer(), user_id=_USER)

        slack_service = SlackResponseHandler().intent_service
        assert slack_service is not web
        assert slack_service.workflow_offer_service is not web.workflow_offer_service
        offers = slack_service.workflow_offer_service
        assert offers.peek_pending_offer(sid, user_id=_USER) == _meeting_offer()
        assert offers.get_and_clear_pending_offer(sid, user_id=_USER) == _meeting_offer()
        # one record: the Slack pop spent it for the web service too
        assert web.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER) in (
            None,
            _meeting_offer(),
        )
        assert cc.get_or_create_context(sid, user_id=_USER).pending_offer is None


# ---------------------------------------------------------------------------
# 6. Row 11: the session push mute rides the slice
# ---------------------------------------------------------------------------


class TestPushMuteOnSlice:
    def test_mute_round_trips_and_is_read_after_a_restart(self):
        from services.intent_service import conversational_floor as cf

        sid = "mute-2189"
        cf._record_push_mute_on_slice(sid, _USER)
        state = _json_round_trip(cc.snapshot_session_slice(sid, user_id=_USER))
        assert state["push_session_muted_at"]

        _restart(sid)
        cf.ConversationalFloor._push_session_state.pop(sid, None)  # process memory gone
        assert cf._push_muted_on_slice(sid, _USER) is False
        cc.get_or_create_context(sid, user_id=_USER).apply_persisted_state(state)
        assert cf._push_muted_on_slice(sid, _USER) is True

    def test_floor_mute_utterance_writes_the_slice(self):
        from services.intent_service import conversational_floor as cf

        sid = "mute-2189-floor"
        assert cc.get_or_create_context(sid, user_id=_USER).push_session_muted_at is None
        cf._record_push_mute_on_slice(sid, _USER)
        first = cc.get_or_create_context(sid, user_id=_USER).push_session_muted_at
        cf._record_push_mute_on_slice(sid, _USER)  # idempotent: keeps the first time
        assert cc.get_or_create_context(sid, user_id=_USER).push_session_muted_at == first
