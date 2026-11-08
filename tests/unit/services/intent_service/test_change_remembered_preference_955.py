"""#955: forget or set the remembered "clear" preference (Arch 11-08 07:18/07:33;
CXO 11-07 18:03 words, 18:15 no confirm).

Layer: the IntentService handler the rail entry dispatches, against an in-memory
``users.preferences`` double at its one persistence seam (``collaboration_gate``).
The alias the classifier names maps to the change through a closed code table;
which preference comes from the person's stored keys, never the words.
"""

from __future__ import annotations

from unittest.mock import MagicMock

import pytest

from services.domain.models import Intent
from services.intent_service import preference_change as pc
from services.intent_service import verified_inference as vi
from services.intent_service.reminder_clear import VALUE_COMPLETE, VALUE_DELETE, inference_key
from services.shared_types import IntentCategory

_USER = "955bbbbb-0000-4000-8000-000000000955"
_CLEAR = inference_key("clear")

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mem_prefs(monkeypatch):
    store: dict = {_USER: {}}
    calls = {"fail_load": False, "save_lies": False, "saves": 0}

    async def _load(user_id):
        if calls["fail_load"]:
            raise RuntimeError("db down")
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        calls["saves"] += 1
        if calls["save_lies"]:
            return True
        store[str(user_id)][key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store, calls


@pytest.fixture
def handler():
    from services.intent.intent_service import IntentService

    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock()
    return svc._handle_change_remembered_preference


def _intent(action, args=None):
    ctx = {"user_id": _USER}
    if args is not None:
        ctx["inversion_args"] = args
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=0.9,
        original_message="(words)",
        context=ctx,
    )


@pytest.fixture(autouse=True)
def _principal(monkeypatch):
    import services.intent.intent_service as svc_mod

    monkeypatch.setattr(svc_mod, "_principal_from_intent", lambda intent: _USER)


async def _stored(key, value):
    assert await vi.store_verified_inference(_USER, key, value)


async def test_forget_says_forgotten_after_the_read_back(mem_prefs, handler):
    await _stored(_CLEAR, VALUE_DELETE)
    result = await handler(_intent("forget_clear_preference"), "wf")
    assert result.message == (
        'Okay. I\'ve forgotten that "clear" means delete it. '
        "Next time you say clear, I'll ask which you want."
    )
    assert await vi.get_verified_inference(_USER, _CLEAR) is None


async def test_forget_with_nothing_stored(mem_prefs, handler):
    _, calls = mem_prefs
    result = await handler(_intent("forget_clear_preference"), "wf")
    assert result.message == (
        "I wasn't remembering a clear preference, so there's nothing to forget. "
        "When you say clear, I ask which you want."
    )
    assert calls["saves"] == 0


async def test_an_unconfirmed_forget_never_says_forgotten(mem_prefs, handler):
    _, calls = mem_prefs
    await _stored(_CLEAR, VALUE_COMPLETE)
    calls["save_lies"] = True
    result = await handler(_intent("forget_clear_preference"), "wf")
    assert result.message == (
        "I couldn't change that just now, so I'm still remembering that \"clear\" means "
        "mark it done. Try again in a moment."
    )
    assert result.success is False


async def test_an_unreadable_store_changes_nothing(mem_prefs, handler):
    _, calls = mem_prefs
    calls["fail_load"] = True
    for action in pc.CHANGE_BY_ACTION:
        result = await handler(_intent(action), "wf")
        assert result.message == pc.UNREADABLE_LINE
    assert calls["saves"] == 0


@pytest.mark.parametrize(
    "action, stored, words",
    [
        ("set_clear_preference_done", VALUE_COMPLETE, "mark it done"),
        ("set_clear_preference_delete", VALUE_DELETE, "delete it"),
    ],
)
async def test_set_directly_renders_from_the_stored_value(
    mem_prefs, handler, action, stored, words
):
    await _stored(_CLEAR, VALUE_COMPLETE if stored == VALUE_DELETE else VALUE_DELETE)
    result = await handler(_intent(action), "wf")
    assert result.message == (
        f'Okay. From now on "clear" means {words}. '
        'Say "forget my clear preference" any time to be asked again.'
    )
    record = await vi.get_verified_inference(_USER, _CLEAR)
    assert record["value"] == stored and record["source"] == vi.SOURCE_USER_DECLARED


async def test_set_directly_never_creates_a_preference(mem_prefs, handler):
    _, calls = mem_prefs
    result = await handler(_intent("set_clear_preference_delete"), "wf")
    assert result.message == pc.NOTHING_STORED_LINE
    assert calls["saves"] == 0


async def test_a_set_that_did_not_stick_says_the_old_value(mem_prefs, handler):
    _, calls = mem_prefs
    await _stored(_CLEAR, VALUE_COMPLETE)
    calls["save_lies"] = True
    result = await handler(_intent("set_clear_preference_delete"), "wf")
    assert 'still remembering that "clear" means mark it done' in result.message


async def test_several_keys_change_nothing_and_name_each(mem_prefs, handler):
    _, calls = mem_prefs
    await _stored(_CLEAR, VALUE_COMPLETE)
    await _stored(inference_key("handle"), VALUE_DELETE)
    before = calls["saves"]
    result = await handler(_intent("forget_clear_preference"), "wf")
    assert result.message == (
        'You have more than one of these remembered: "clear" means mark it done, '
        '"handle" means delete it. I haven\'t changed any of them.'
    )
    assert calls["saves"] == before


async def test_another_family_verb_is_named_by_its_own_label(mem_prefs, handler):
    await _stored(inference_key("handle"), VALUE_DELETE)
    result = await handler(_intent("forget_clear_preference"), "wf")
    assert result.message.startswith('Okay. I\'ve forgotten that "handle" means delete it.')


async def test_the_canonical_binds_only_a_router_change_arg(mem_prefs, handler):
    await _stored(_CLEAR, VALUE_COMPLETE)
    unnamed = await handler(_intent("change_remembered_preference"), "wf")
    assert unnamed.message == 'Right now "clear" means mark it done. I haven\'t changed it.'
    odd = await handler(_intent("change_remembered_preference", {"change": "maybe"}), "wf")
    assert odd.message == unnamed.message
    named = await handler(_intent("change_remembered_preference", {"change": "forget"}), "wf")
    assert named.message.startswith("Okay. I've forgotten")


async def test_one_entry_three_aliases_registered():
    from services.intent_service.action_registry import ACTION_EXAMPLES, ACTION_REGISTRY
    from services.intent_service.workflow_dispatcher import (
        EffectClass,
        Outwardness,
        get_action_workflows,
    )
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    flows = get_action_workflows()
    entry = flows["change_remembered_preference"]
    assert entry.effect is EffectClass.WRITE and entry.outwardness is Outwardness.PRIVATE
    for alias in pc.CHANGE_BY_ACTION:
        assert flows[alias] is entry
        assert ("QUERY", alias) in ACTION_REGISTRY and ("QUERY", alias) in ACTION_EXAMPLES


# ── Arch 11-08 07:53 condition: the landing pin through router_none_stands ─────

_ALPHA_LIVE = (
    "add_project,complete_todo,create_reminder,create_todo,delete_todo,read_canonical,"
    "read_floor,read_portfolio,read_referent,read_status,read_strategic,read_synthesis,"
    "read_temporal"
)


async def test_landing_pin_the_routers_none_does_not_floor_the_hidden_entry(mem_prefs, monkeypatch):
    """Through process_intent with alpha's live set: a live consult that declines with
    router_none at 0.95 leaves the classifier's landing on the hidden entry standing."""
    from types import SimpleNamespace
    from unittest.mock import patch

    import services.intent_service.inversion_live as il
    from services.intent.intent_service import IntentService
    from services.intent_service import conversational_floor as cf
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    floored = []

    async def _floor(self, ctx):
        floored.append(ctx)
        return cf.FloorResponse(message="(floor)")

    monkeypatch.setattr(cf.ConversationalFloor, "respond", _floor)

    class _NoLLM:
        def __getattr__(self, name):
            raise AssertionError(f"LLM touched ({name})")

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            svc = IntentService(intent_classifier=IntentClassifier(llm_service=_NoLLM()))

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        intent = Intent(
            category=IntentCategory.QUERY,
            action="set_clear_preference_done",
            original_message=msg,
            confidence=0.95,
            context={"original_message": msg},
        )
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(svc.intent_classifier, "classify_multiple", _classify_multiple)

    async def _router_none(*a, **k):
        il.publish_live_route_provenance(
            il.LiveRouteProvenance(routed_live=False, reason="router_none", confidence=0.95)
        )
        return None

    monkeypatch.setenv("PIPER_INVERSION_LIVE_CATEGORIES", _ALPHA_LIVE)
    monkeypatch.setattr(il, "consult_inversion_live", _router_none)
    await _stored(_CLEAR, VALUE_DELETE)
    try:
        result = await svc.process_intent(
            message="make clear mean mark it done", session_id="pc-955", user_id=_USER
        )
    finally:
        il.publish_live_route_provenance(None)
    assert floored == []
    # An execute-framed ask (consent PROCEED). The forget asks frame AMBIGUOUS and meet
    # the consent check, which forget proceeds past (Arch 08:05; pinned below).
    assert result.message.startswith('Okay. From now on "clear" means mark it done.')


# ── Arch 11-08 07:53 (3): the standing classifier miss completes nothing ───────


async def test_make_clear_mark_them_done_as_complete_todo_completes_nothing():
    """The classifier reads "make clear mark them done" as complete_todo x6 (main and
    candidate; corpus REVIEW row). The objectless "them" must complete nothing. Today
    it says it couldn't find "them" rather than asking which (reported to Arch)."""
    from unittest.mock import AsyncMock
    from uuid import uuid4

    from services.domain.models import Todo
    from services.intent_service.soft_invocation import WorkflowOfferService
    from services.intent_service.todo_handlers import TodoIntentHandlers

    def todo(text):
        t = Todo(text=text, priority="medium")
        t.id = str(uuid4())
        return t

    h = TodoIntentHandlers()
    h.todo_service = AsyncMock()
    h.todo_service.list_todos = AsyncMock(
        return_value=[todo("review prs"), todo("call the vet"), todo("hydrate")]
    )
    user = uuid4()
    result = await h.handle_complete_todo(
        Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message="make clear mark them done",
            confidence=0.9,
        ),
        "s-955",
        user,
        offer_service=WorkflowOfferService(),
        principal=str(user),
    )
    h.todo_service.complete_todo.assert_not_called()
    assert "Nothing" in result or "couldn't find" in result


# ── Arch 11-08 08:05: forget is consent-narrowing; set-directly keeps the check ──


async def _through_process_intent(monkeypatch, message, action):
    from types import SimpleNamespace
    from unittest.mock import patch

    from services.intent.intent_service import IntentService
    from services.intent_service import conversational_floor as cf
    from services.intent_service.classifier import IntentClassifier
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()

    async def _floor(self, ctx):
        raise AssertionError("floored")

    monkeypatch.setattr(cf.ConversationalFloor, "respond", _floor)

    class _NoLLM:
        def __getattr__(self, name):
            raise AssertionError(f"LLM touched ({name})")

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            svc = IntentService(intent_classifier=IntentClassifier(llm_service=_NoLLM()))

    async def _classify_multiple(msg, context=None, user_id=None, session_id=None):
        intent = Intent(
            category=IntentCategory.QUERY,
            action=action,
            original_message=msg,
            confidence=0.95,
            context={"original_message": msg},
        )
        return SimpleNamespace(
            intents=[intent],
            is_multi_intent=False,
            has_greeting=False,
            has_substantive_intent=True,
            primary_intent=intent,
            secondary_intents=[],
        )

    monkeypatch.setattr(svc.intent_classifier, "classify_multiple", _classify_multiple)
    return await svc.process_intent(message=message, session_id="pc-955b", user_id=_USER)


@pytest.mark.parametrize(
    "words",
    [
        "forget my clear preference",
        "stop remembering that",
        "don't remember what clear means",
        "when I say clear, ask me",
    ],
)
async def test_ambiguous_forget_asks_reach_forget_in_collaborate_mode(
    mem_prefs, monkeypatch, words
):
    from services.intent_service.collaboration_gate import FRAMING_AMBIGUOUS, classify_framing

    assert classify_framing(words) == FRAMING_AMBIGUOUS
    await _stored(_CLEAR, VALUE_DELETE)
    result = await _through_process_intent(monkeypatch, words, "forget_clear_preference")
    assert result.message.startswith('Okay. I\'ve forgotten that "clear" means delete it.')
    assert await vi.get_verified_inference(_USER, _CLEAR) is None


async def test_an_ambiguous_set_still_checks_with_cxos_yes_no(mem_prefs, monkeypatch):
    """Set-directly keeps the consent check (Arch 08:05); the check asks CXO's 08:09
    yes/no, built from the stored key and target value. Nothing changes until "yes"."""
    await _stored(_CLEAR, VALUE_DELETE)
    result = await _through_process_intent(
        monkeypatch, "don't delete when I clear", "set_clear_preference_done"
    )
    assert result.message.endswith('Change "clear" from delete it to mark it done? (yes/no)')
    assert (await vi.get_verified_inference(_USER, _CLEAR))["value"] == VALUE_DELETE


async def test_the_set_ask_with_the_value_already_stored_says_so(mem_prefs):
    from services.intent_service.write_confirm_words import WriteAskRequest

    await _stored(_CLEAR, VALUE_COMPLETE)
    ask = await pc.change_preference_write_ask(
        WriteAskRequest(intent=_intent("set_clear_preference_done"), message="x", principal=_USER)
    )
    assert ask.reply == '"clear" already means mark it done, so I haven\'t changed anything.'
    assert ask.words is None


async def test_the_set_ask_carries_cxos_decline(mem_prefs):
    from services.intent_service.write_confirm_words import WriteAskRequest

    await _stored(_CLEAR, VALUE_COMPLETE)
    ask = await pc.change_preference_write_ask(
        WriteAskRequest(intent=_intent("set_clear_preference_delete"), message="x", principal=_USER)
    )
    assert ask.words.question == 'Change "clear" from mark it done to delete it? (yes/no)'
    assert ask.words.decline == "Okay. I won't change it."


async def test_ask_me_each_time_is_forget(mem_prefs, handler):
    await _stored(_CLEAR, VALUE_DELETE)
    result = await handler(_intent("set_clear_preference_ask"), "wf")
    assert result.message.startswith('Okay. I\'ve forgotten that "clear" means delete it.')


# ── CXO 08:09: several keys, the armed forget pick over exactly the rows shown ──


async def test_several_keys_arm_the_forget_pick_and_a_number_forgets_that_row(mem_prefs):
    from services.intent_service.soft_invocation import WorkflowOfferService

    await _stored(_CLEAR, VALUE_COMPLETE)
    await _stored(inference_key("handle"), VALUE_DELETE)
    store = WorkflowOfferService()
    out = await pc.change_remembered_preference(
        _intent("forget_clear_preference"), _USER, session_id="s-pick", offer_service=store
    )
    assert out["message"] == (
        "I'm remembering more than one of these:\n\n"
        '1. "clear" means mark it done\n2. "handle" means delete it\n\n'
        "Which one should I forget? Say the number, or 'never mind' to leave them alone."
    )
    offer = store.peek_pending_offer("s-pick", _USER)
    assert offer["decline_message"] == "Okay. I haven't forgotten anything."
    picked = await pc.handle_forget_pick_turn(offer, "2", session_id="s-pick", user_id=_USER)
    assert picked["message"].startswith('Okay. I\'ve forgotten that "handle" means delete it.')
    assert await vi.get_verified_inference(_USER, inference_key("handle")) is None
    assert (await vi.get_verified_inference(_USER, _CLEAR))["value"] == VALUE_COMPLETE
    # An off-list number or words bind nothing (the generic seam takes them).
    assert await pc.handle_forget_pick_turn(offer, "7", session_id="s", user_id=_USER) is None
    assert await pc.handle_forget_pick_turn(offer, "clear", session_id="s", user_id=_USER) is None


async def test_several_keys_with_no_session_change_nothing(mem_prefs, handler):
    _, calls = mem_prefs
    await _stored(_CLEAR, VALUE_COMPLETE)
    await _stored(inference_key("handle"), VALUE_DELETE)
    before = calls["saves"]
    result = await handler(_intent("forget_clear_preference"), "wf")
    assert "I haven't changed any of them." in result.message
    assert calls["saves"] == before


async def test_a_narrowing_action_off_the_allowlist_fails_at_construction():
    from services.intent_service.workflow_dispatcher import (
        CONSENT_NARROWING_ALLOWLIST,
        EffectClass,
        WorkflowEntry,
    )

    assert CONSENT_NARROWING_ALLOWLIST == frozenset(
        {
            "forget_clear_preference",
            "set_clear_preference_ask",
            "forget_handle_preference",
            "forget_take_care_of_preference",
            "forget_reset_preference",
        }
    )

    async def _ep(*a, **k):
        return None

    with pytest.raises(ValueError, match="CONSENT_NARROWING_ALLOWLIST"):
        WorkflowEntry(
            entry_point=_ep,
            effect=EffectClass.WRITE,
            consent_narrowing_actions=frozenset({"set_clear_preference_delete"}),
        )


# ── Arch 11-08 09:28: one store, one vocabulary (the clear path's own values) ──


async def test_the_module_holds_no_value_strings_of_its_own():
    from services.intent_service import reminder_clear as rc

    assert pc.STORED_VALUE == {"done": rc.VALUE_COMPLETE, "delete": rc.VALUE_DELETE}
    assert set(pc.MEANING_WORDS) == {rc.VALUE_COMPLETE, rc.VALUE_DELETE}


async def test_a_row_the_clear_path_wrote_is_read_forgotten_and_set_over(mem_prefs, handler):
    """The clear path's own write (its first-time 'mark it done' answer and its
    meta-auto store both write VALUE_COMPLETE under inference_key(verb))."""
    from services.intent_service import reminder_clear as rc
    from services.intent_service.verified_inference import (
        SOURCE_USER_VERIFIED,
        store_verified_inference,
    )

    async def clear_path_answer(value):
        assert await store_verified_inference(
            _USER,
            rc.inference_key("clear"),
            value,
            source=SOURCE_USER_VERIFIED,
            confidence=rc.VERB_CONFIDENCE,
        )

    await clear_path_answer(rc.VALUE_COMPLETE)
    already = await handler(_intent("set_clear_preference_done"), "wf")
    assert already.message == '"clear" already means mark it done, so I haven\'t changed anything.'
    gone = await handler(_intent("forget_clear_preference"), "wf")
    assert gone.message.startswith('Okay. I\'ve forgotten that "clear" means mark it done.')

    await clear_path_answer(rc.VALUE_DELETE)
    set_done = await handler(_intent("set_clear_preference_done"), "wf")
    assert set_done.message.startswith('Okay. From now on "clear" means mark it done.')
    # What the clear path's next turn compares against: its own VALUE_COMPLETE.
    stored = await vi.get_verified_inference(_USER, rc.inference_key("clear"))
    assert stored["value"] == rc.VALUE_COMPLETE


# ── Arch 11-08 13:20/13:21: per-verb aliases act only on that verb's stored key ──

_HANDLE = inference_key("handle")


async def test_forget_handle_forgets_only_the_handle_key(mem_prefs, handler):
    await _stored(_CLEAR, VALUE_COMPLETE)
    await _stored(_HANDLE, VALUE_DELETE)
    result = await handler(_intent("forget_handle_preference"), "wf")
    assert result.message == (
        'Okay. I\'ve forgotten that "handle" means delete it. '
        "Next time you say handle, I'll ask which you want."
    )
    assert await vi.get_verified_inference(_USER, _HANDLE) is None
    assert (await vi.get_verified_inference(_USER, _CLEAR))["value"] == VALUE_COMPLETE


async def test_a_per_verb_ask_for_an_unstored_verb_never_touches_another_key(mem_prefs, handler):
    _, calls = mem_prefs
    await _stored(_CLEAR, VALUE_COMPLETE)
    before = calls["saves"]
    for action in ("forget_reset_preference", "set_reset_preference_delete"):
        result = await handler(_intent(action), "wf")
        assert result.message == (
            "I wasn't remembering a reset preference, so there's nothing to forget. "
            "When you say reset, I ask which you want."
        )
    assert calls["saves"] == before
    assert (await vi.get_verified_inference(_USER, _CLEAR))["value"] == VALUE_COMPLETE


async def test_set_handle_done_over_a_real_handle_row(mem_prefs, handler):
    await _stored(_HANDLE, VALUE_DELETE)
    result = await handler(_intent("set_handle_preference_done"), "wf")
    assert result.message == (
        'Okay. From now on "handle" means mark it done. '
        'Say "forget my handle preference" any time to be asked again.'
    )
    assert (await vi.get_verified_inference(_USER, _HANDLE))["value"] == VALUE_COMPLETE


async def test_take_care_of_is_named_by_its_label(mem_prefs, handler):
    key = inference_key("take care of")
    await _stored(key, VALUE_COMPLETE)
    result = await handler(_intent("forget_take_care_of_preference"), "wf")
    assert result.message.startswith(
        'Okay. I\'ve forgotten that "take care of" means mark it done.'
    )


async def test_per_verb_forget_is_consent_narrowing_per_verb_set_asks(mem_prefs, monkeypatch):
    await _stored(_HANDLE, VALUE_DELETE)
    forgot = await _through_process_intent(
        monkeypatch, "forget my handle preference", "forget_handle_preference"
    )
    assert forgot.message.startswith('Okay. I\'ve forgotten that "handle" means delete it.')
    await _stored(_HANDLE, VALUE_DELETE)
    asked = await _through_process_intent(
        monkeypatch, "when I say handle, mark it done", "set_handle_preference_done"
    )
    assert asked.message.endswith('Change "handle" from delete it to mark it done? (yes/no)')
    assert (await vi.get_verified_inference(_USER, _HANDLE))["value"] == VALUE_DELETE


async def test_every_per_verb_alias_is_on_the_one_entry():
    from services.intent_service.workflow_dispatcher import get_action_workflows
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    flows = get_action_workflows()
    entry = flows["change_remembered_preference"]
    assert len(pc.VERB_BY_ACTION) == 9
    for alias in pc.VERB_BY_ACTION:
        assert flows[alias] is entry
    assert entry.consent_narrowing_actions >= pc.PER_VERB_FORGET_ACTIONS
    assert not any(a.startswith("set_") for a in pc.PER_VERB_FORGET_ACTIONS)
