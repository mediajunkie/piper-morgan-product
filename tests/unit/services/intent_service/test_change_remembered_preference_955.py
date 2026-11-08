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
from services.intent_service.reminder_clear import inference_key
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
    await _stored(_CLEAR, "delete")
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
    await _stored(_CLEAR, "done")
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
        ("set_clear_preference_done", "done", "mark it done"),
        ("set_clear_preference_delete", "delete", "delete it"),
    ],
)
async def test_set_directly_renders_from_the_stored_value(
    mem_prefs, handler, action, stored, words
):
    await _stored(_CLEAR, "done" if stored == "delete" else "delete")
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
    await _stored(_CLEAR, "done")
    calls["save_lies"] = True
    result = await handler(_intent("set_clear_preference_delete"), "wf")
    assert 'still remembering that "clear" means mark it done' in result.message


async def test_several_keys_change_nothing_and_name_each(mem_prefs, handler):
    _, calls = mem_prefs
    await _stored(_CLEAR, "done")
    await _stored(inference_key("handle"), "delete")
    before = calls["saves"]
    result = await handler(_intent("forget_clear_preference"), "wf")
    assert result.message == (
        'You have more than one of these remembered: "clear" means mark it done, '
        '"handle" means delete it. I haven\'t changed any of them.'
    )
    assert calls["saves"] == before


async def test_another_family_verb_is_named_by_its_own_label(mem_prefs, handler):
    await _stored(inference_key("handle"), "delete")
    result = await handler(_intent("forget_clear_preference"), "wf")
    assert result.message.startswith('Okay. I\'ve forgotten that "handle" means delete it.')


async def test_the_canonical_binds_only_a_router_change_arg(mem_prefs, handler):
    await _stored(_CLEAR, "done")
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
