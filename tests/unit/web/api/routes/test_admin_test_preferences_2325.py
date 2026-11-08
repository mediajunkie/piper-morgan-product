"""#2325: the admin reset of one stored preference on one named test account, built on
Arch's one deletion path (``forget_verified_inference``, #955/#2325, 2026-11-07 18:03).

Layer: the function against the in-memory ``users.preferences`` double at its one
persistence seam (``collaboration_gate``), and the route coroutine called directly with
the username lookup and the audit writer recorded at their boundaries. The admin gate
itself is ``require_admin``, pinned by #1485's and #1598's tests; here it is the route's
declared dependency.
"""

from __future__ import annotations

import inspect
import uuid
from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from services.auth.auth_middleware import require_admin
from services.intent_service import verified_inference as vi
from services.intent_service.reminder_clear import inference_key
from web.api.routes import admin_test_preferences as api

_USER = "2325aaaa-0000-4000-8000-000000002325"
_KEY = inference_key("clear")
_ADMIN = SimpleNamespace(user_id=uuid.uuid4())


@pytest.fixture
def mem_prefs(monkeypatch):
    store: dict = {_USER: {}}
    calls = {"save": 0, "fail_load": False, "fail_save": False}

    async def _load(user_id):
        if calls["fail_load"]:
            raise RuntimeError("db down")
        return dict(store.get(str(user_id), {}))

    async def _save(user_id, key, value):
        calls["save"] += 1
        if calls["fail_save"]:
            raise RuntimeError("db down")
        if str(user_id) not in store:
            return False
        store[str(user_id)][key] = value
        return True

    from services.intent_service import collaboration_gate

    monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
    monkeypatch.setattr(collaboration_gate, "_save_preference", _save)
    return store, calls


async def _store_clear(value="delete"):
    assert await vi.store_verified_inference(_USER, _KEY, value)


class TestForgetFunction:
    @pytest.mark.asyncio
    async def test_forget_deletes_the_row_so_the_next_read_is_unset(self, mem_prefs):
        store, _ = mem_prefs
        await _store_clear("done")
        await vi.store_verified_inference(_USER, inference_key("handle"), "delete")
        result = await vi.forget_verified_inference(_USER, _KEY)
        assert result.outcome is vi.ForgetOutcome.FORGOTTEN
        assert result.record["value"] == "done"
        assert await vi.get_verified_inference(_USER, _KEY) is None
        # Only that key goes: another stored verb stays.
        assert await vi.get_verified_inference(_USER, inference_key("handle")) is not None

    @pytest.mark.asyncio
    async def test_nothing_stored_writes_nothing(self, mem_prefs):
        _, calls = mem_prefs
        result = await vi.forget_verified_inference(_USER, _KEY)
        assert result.outcome is vi.ForgetOutcome.NOTHING_STORED
        assert calls["save"] == 0

    @pytest.mark.asyncio
    async def test_a_failed_read_is_failed_never_nothing_stored(self, mem_prefs):
        _, calls = mem_prefs
        calls["fail_load"] = True
        result = await vi.forget_verified_inference(_USER, _KEY)
        assert result.outcome is vi.ForgetOutcome.FAILED

    @pytest.mark.asyncio
    async def test_a_failed_write_is_failed_and_the_value_stays(self, mem_prefs):
        _, calls = mem_prefs
        await _store_clear("delete")
        calls["fail_save"] = True
        result = await vi.forget_verified_inference(_USER, _KEY)
        assert result.outcome is vi.ForgetOutcome.FAILED
        assert result.record["value"] == "delete"
        calls["fail_save"] = False
        assert (await vi.get_verified_inference(_USER, _KEY))["value"] == "delete"

    @pytest.mark.asyncio
    async def test_absent_user_row_is_failed(self, mem_prefs, monkeypatch):
        store, _ = mem_prefs
        await _store_clear()
        # The row exists in the double's read but the seam's save says "no user row".
        store_copy = dict(store[_USER])
        del store[_USER]

        async def _load(user_id):
            return store_copy

        from services.intent_service import collaboration_gate

        monkeypatch.setattr(collaboration_gate, "_load_preferences", _load)
        result = await vi.forget_verified_inference(_USER, _KEY)
        assert result.outcome is vi.ForgetOutcome.FAILED


@pytest.fixture
def route(monkeypatch, mem_prefs):
    audits: list = []
    users = {"web-seed-1386": _USER, "web-fresh-test": None}

    async def _lookup(username):
        return users.get(username)

    async def _audit(**kw):
        audits.append(kw)

    monkeypatch.setattr(api, "_user_id_for", _lookup)
    monkeypatch.setattr(api, "_write_audit", _audit)
    return audits


class TestAdminRoute:
    def test_the_route_requires_admin(self):
        param = inspect.signature(api.forget_test_preference).parameters["admin"]
        assert param.default.dependency is require_admin

    @pytest.mark.asyncio
    async def test_forgets_on_a_listed_test_account_and_audits(self, route, mem_prefs):
        await _store_clear("delete")
        out = await api.forget_test_preference(
            api.ForgetRequest(username="web-seed-1386", key=_KEY), admin=_ADMIN
        )
        assert out.outcome == "forgotten"
        assert await vi.get_verified_inference(_USER, _KEY) is None
        assert route == [
            {
                "actor_user_id": _ADMIN.user_id,
                "username": "web-seed-1386",
                "key": _KEY,
                "outcome": "forgotten",
            }
        ]

    @pytest.mark.asyncio
    async def test_an_unlisted_account_is_refused_before_anything(self, route, mem_prefs):
        _, calls = mem_prefs
        with pytest.raises(HTTPException) as e:
            await api.forget_test_preference(
                api.ForgetRequest(username="someone-real", key=_KEY), admin=_ADMIN
            )
        assert e.value.status_code == 403
        assert route == [] and calls["save"] == 0

    @pytest.mark.asyncio
    async def test_an_unlisted_key_is_refused(self, route, mem_prefs):
        with pytest.raises(HTTPException) as e:
            await api.forget_test_preference(
                api.ForgetRequest(username="web-seed-1386", key="standup_mode"), admin=_ADMIN
            )
        assert e.value.status_code == 422
        assert route == []

    @pytest.mark.asyncio
    async def test_a_listed_name_with_no_account_is_404(self, route):
        with pytest.raises(HTTPException) as e:
            await api.forget_test_preference(
                api.ForgetRequest(username="web-fresh-test", key=_KEY), admin=_ADMIN
            )
        assert e.value.status_code == 404

    @pytest.mark.asyncio
    async def test_nothing_stored_is_said_and_audited(self, route):
        out = await api.forget_test_preference(
            api.ForgetRequest(username="web-seed-1386", key=_KEY), admin=_ADMIN
        )
        assert out.outcome == "nothing_stored"
        assert route[0]["outcome"] == "nothing_stored"

    @pytest.mark.asyncio
    async def test_a_failed_write_is_503_and_audited_failed(self, route, mem_prefs):
        _, calls = mem_prefs
        await _store_clear("done")
        calls["fail_save"] = True
        with pytest.raises(HTTPException) as e:
            await api.forget_test_preference(
                api.ForgetRequest(username="web-seed-1386", key=_KEY), admin=_ADMIN
            )
        assert e.value.status_code == 503
        assert route[0]["outcome"] == "failed"
