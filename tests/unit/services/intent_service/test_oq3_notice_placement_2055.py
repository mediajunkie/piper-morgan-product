"""#2055: ADR-075 OQ-3 first-response notice placement.

CXO ruling / Arch amendment 2026-10-16: the one-time notice shows only on a
greeting or a capability/help reply, never under a list or result; a
suppressed notice does not mark the record shown; once per principal.

The fake service below reproduces the real contract of
``maybe_consume_first_response_notice`` (return the wording and mark shown on
the first call per principal, None after). Gating happens BEFORE the call, so
"not marked shown" is observable as "the call never happened".
"""

from unittest.mock import AsyncMock, MagicMock

import pytest

import services.configuration.personalization_service as ps
from services.intent.intent_service import IntentService
from services.intent_service.conversation_context import clear_context

_SID = "sess-2055-test"
_UID = "user-2055-test"
_NOTICE = "(Nothing about your role or preferences needs setting up first.)"


class _FakeNoticeService:
    def __init__(self):
        self.shown = set()
        self.calls = 0

    async def maybe_consume_first_response_notice(self, user_id):
        self.calls += 1
        if user_id in self.shown:
            return None
        self.shown.add(user_id)
        return ps.FIRST_RESPONSE_PERSONALIZATION_NOTICE


@pytest.fixture
def fake(monkeypatch):
    f = _FakeNoticeService()
    monkeypatch.setattr(ps, "personalization_service", f)
    clear_context(_SID)
    yield f
    clear_context(_SID)


async def _turn(intent_data, message="Reply."):
    svc = IntentService.__new__(IntentService)
    svc.logger = MagicMock()
    internal = MagicMock()
    internal.success = True
    internal.message = message
    internal.intent_data = intent_data
    svc._process_intent_internal = AsyncMock(return_value=internal)
    svc._observe_action_verb = MagicMock()
    svc._record_session_activity = AsyncMock()
    svc.conversation_manager = MagicMock()
    svc.conversation_manager.save_conversation_turn = AsyncMock()
    return await svc.process_intent("x", session_id=_SID, user_id=_UID)


DATA = {"category": "query", "action": "list_issues"}
TODO = {"category": "execution", "action": "list_todos"}
HELLO = {"category": "conversation", "action": "greeting"}
CAPS = {"category": "discovery", "action": "get_capabilities"}


def test_wording_is_byte_identical():
    assert ps.FIRST_RESPONSE_PERSONALIZATION_NOTICE == _NOTICE


@pytest.mark.asyncio
async def test_data_first_then_hello_then_hello(fake):
    r = await _turn(DATA)
    assert _NOTICE not in r.message
    assert fake.calls == 0 and not fake.shown  # not marked shown

    r = await _turn(HELLO)
    assert r.message.endswith(f"\n\n{_NOTICE}")
    assert fake.shown == {_UID}

    r = await _turn(HELLO)
    assert _NOTICE not in r.message


@pytest.mark.asyncio
async def test_todo_read_is_also_suppressed(fake):
    r = await _turn(TODO)
    assert _NOTICE not in r.message and not fake.shown


@pytest.mark.asyncio
async def test_fresh_principal_hello_first_shows_once(fake):
    assert _NOTICE in (await _turn(HELLO)).message
    assert _NOTICE not in (await _turn(HELLO)).message


@pytest.mark.asyncio
async def test_capabilities_reply_shows_once(fake):
    assert _NOTICE in (await _turn(CAPS)).message
    assert _NOTICE not in (await _turn(CAPS)).message


@pytest.mark.asyncio
async def test_capabilities_after_hello_does_not_repeat(fake):
    await _turn(HELLO)
    assert _NOTICE not in (await _turn(CAPS)).message


@pytest.mark.asyncio
async def test_uppercase_category_label_still_qualifies(fake):
    # The floor path builds intent_data with an uppercase category string.
    r = await _turn({"category": "CONVERSATION", "action": "greeting"})
    assert _NOTICE in r.message


@pytest.mark.asyncio
async def test_unlabelled_reply_never_carries_notice(fake):
    r = await _turn(None)
    assert _NOTICE not in r.message and fake.calls == 0
