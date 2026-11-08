"""#955 (Arch 11-07 20:26): the person-facing forget says "forgotten" only after a
read-back of the store shows the key gone. ``forget_verified_inference(read_back=True)``:
a write that reports success but left the key, or a re-read that fails, is FAILED.

Layer: the function against an in-memory ``users.preferences`` double at its one
persistence seam (``collaboration_gate``), the #2325 tests' shape.
"""

from __future__ import annotations

import pytest

from services.intent_service import verified_inference as vi
from services.intent_service.reminder_clear import inference_key

_USER = "955aaaaa-0000-4000-8000-000000000955"
_KEY = inference_key("clear")

pytestmark = pytest.mark.asyncio


@pytest.fixture
def mem_prefs(monkeypatch):
    store: dict = {_USER: {}}
    calls = {"loads": 0, "fail_load_after": None, "save_lies": False}

    async def _load(user_id):
        calls["loads"] += 1
        if calls["fail_load_after"] is not None and calls["loads"] > calls["fail_load_after"]:
            raise RuntimeError("db down")
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        if calls["save_lies"]:
            return True  # reports success, writes nothing
        store[str(user_id)][key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store, calls


async def test_a_confirmed_delete_is_forgotten(mem_prefs):
    assert await vi.store_verified_inference(_USER, _KEY, "delete")
    result = await vi.forget_verified_inference(_USER, _KEY, read_back=True)
    assert result.outcome is vi.ForgetOutcome.FORGOTTEN
    assert result.record["value"] == "delete"
    assert await vi.get_verified_inference(_USER, _KEY) is None


async def test_a_write_that_says_yes_but_left_the_key_is_failed(mem_prefs):
    _, calls = mem_prefs
    assert await vi.store_verified_inference(_USER, _KEY, "done")
    calls["save_lies"] = True
    result = await vi.forget_verified_inference(_USER, _KEY, read_back=True)
    assert result.outcome is vi.ForgetOutcome.FAILED
    assert result.record["value"] == "done"
    # Without the read-back (the #2325 admin route), the boolean alone is trusted.
    assert (await vi.forget_verified_inference(_USER, _KEY)).outcome is vi.ForgetOutcome.FORGOTTEN


async def test_a_failed_read_back_is_failed_never_forgotten(mem_prefs):
    _, calls = mem_prefs
    assert await vi.store_verified_inference(_USER, _KEY, "done")
    calls["fail_load_after"] = (
        calls["loads"] + 1
    )  # the forget's first read works, the re-read fails
    result = await vi.forget_verified_inference(_USER, _KEY, read_back=True)
    assert result.outcome is vi.ForgetOutcome.FAILED
