"""#2405 (Arch's ruling 2026-11-18, CXO's line the same day): on a local install the key
saved at the terminal (guide step 5) becomes the FIRST account's own key at ``/complete``
when that account took it with "Use saved key". Nobody else's.

Arch's tests (a) to (f), and CXO's: a later account's ``use-keychain`` answers exactly the
one constant, the first account's answers the tick line. Key values come from
``tests/utils/made_up_credentials.py``; none was ever issued.
"""

from __future__ import annotations

import uuid
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pydantic import ValidationError
from sqlalchemy import text

import web.api.routes.setup as setup
from tests.utils.made_up_credentials import GOOD_ANTHROPIC_KEY

pytestmark = pytest.mark.unit

_MASTER_KEY = "S" * 43 + "="  # the value test_setup_global_key_write_1810.py uses


def _req(**kw):
    kw.setdefault("default_llm_provider", "anthropic")
    return setup.SetupCompleteRequest(**kw)


class _Rows:
    def __init__(self, row):
        self._row = row

    def first(self):
        return self._row


class FakeSession:
    def __init__(self, existing_row=None):
        self.existing_row = existing_row

    async def execute(self, *a, **k):
        return _Rows(self.existing_row)


class FakeService:
    def __init__(self, fail=False):
        self.calls = []
        self.fail = fail

    async def store_user_key(self, **kw):
        self.calls.append(kw)
        if self.fail:
            raise RuntimeError("store refused")


class FakeKeychain:
    saved = GOOD_ANTHROPIC_KEY

    def get_api_key(self, provider, username=None):
        return self.saved if (provider == "anthropic" and username is None) else None

    async def aget_api_key(self, provider, username=None):
        return self.get_api_key(provider, username)


class LogRecorder:
    def __init__(self):
        self.lines = []

    def info(self, event, **kw):
        self.lines.append((event, kw))

    warning = error = info


@pytest.fixture
def wired(monkeypatch):
    """Local install, first account, a saved key, no row yet: every condition holds.
    Each test turns one off."""
    state = SimpleNamespace(hosted=False, other_account=False)
    monkeypatch.setattr(
        "services.infrastructure.deployment.is_hosted_deployment", lambda: state.hosted
    )

    async def other(principal):
        return state.other_account

    monkeypatch.setattr(setup, "_another_account_completed_setup", other)
    monkeypatch.setattr("services.infrastructure.keychain_service.KeychainService", FakeKeychain)
    state.log = LogRecorder()
    monkeypatch.setattr(setup, "logger", state.log)
    return state


PRINCIPAL = str(uuid.uuid4())


async def _copy(req, session=None, service=None):
    service = service or FakeService()
    copied = await setup._copy_saved_key_for_first_account(
        session or FakeSession(), PRINCIPAL, req, service
    )
    return copied, service


# ── the conditions (rule 2) ──────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_first_local_account_gets_its_own_copy(wired):
    copied, service = await _copy(_req(saved_key_provider="anthropic"))
    assert copied == "anthropic"
    assert service.calls == [
        {
            "user_id": PRINCIPAL,
            "provider": "anthropic",
            "api_key": GOOD_ANTHROPIC_KEY,
            "session": service.calls[0]["session"],
            "validate": False,
        }
    ]


@pytest.mark.asyncio
async def test_b_hosted_copies_nothing(wired):
    wired.hosted = True
    copied, service = await _copy(_req(saved_key_provider="anthropic"))
    assert copied is None and service.calls == []
    assert (
        "saved_key_copy_skipped",
        {"provider": "anthropic", "reason": "hosted"},
    ) in wired.log.lines


@pytest.mark.asyncio
async def test_c_a_later_account_copies_nothing(wired):
    wired.other_account = True
    copied, service = await _copy(_req(saved_key_provider="anthropic"))
    assert copied is None and service.calls == []


@pytest.mark.asyncio
async def test_d_a_pasted_key_wins(wired):
    pasted = GOOD_ANTHROPIC_KEY[::-1]
    copied, service = await _copy(_req(saved_key_provider="anthropic", anthropic_key=pasted))
    assert copied is None and service.calls == []  # the route stores the pasted key itself


@pytest.mark.asyncio
async def test_an_existing_row_is_never_overwritten(wired):
    copied, service = await _copy(
        _req(saved_key_provider="anthropic"), session=FakeSession(existing_row=(1,))
    )
    assert copied is None and service.calls == []


@pytest.mark.asyncio
async def test_no_saved_key_copies_nothing(wired, monkeypatch):
    monkeypatch.setattr(FakeKeychain, "saved", None)
    copied, service = await _copy(_req(saved_key_provider="anthropic"))
    assert copied is None and service.calls == []


@pytest.mark.asyncio
async def test_no_field_no_copy_even_with_a_null_key(wired):
    """Rule 1: the server never infers the copy from a null key."""
    copied, service = await _copy(_req(anthropic_key=None))
    assert copied is None and service.calls == []


@pytest.mark.asyncio
async def test_a_failed_store_breaks_nothing_and_logs_no_key(wired):
    copied, service = await _copy(
        _req(saved_key_provider="anthropic"), service=FakeService(fail=True)
    )
    assert copied is None
    assert GOOD_ANTHROPIC_KEY not in repr(wired.log.lines)
    assert any(event == "saved_key_copy_failed" for event, _ in wired.log.lines)


@pytest.mark.asyncio
async def test_no_log_line_carries_the_key(wired):
    for hosted, other in ((False, False), (True, False), (False, True)):
        wired.hosted, wired.other_account = hosted, other
        await _copy(_req(saved_key_provider="anthropic"))
    assert GOOD_ANTHROPIC_KEY not in repr(wired.log.lines)


# ── (e) the field is validated like default_llm_provider ─────────────────────


@pytest.mark.parametrize("value", ["gemini", "notion", "anthropic; drop table", ""])
def test_e_a_provider_no_reply_is_served_on_is_refused(value):
    with pytest.raises(ValidationError):
        _req(saved_key_provider=value)


# ── (f) the principal is the session ─────────────────────────────────────────


@pytest.mark.asyncio
async def test_f_a_body_user_id_that_is_not_the_session_is_403_before_any_copy(monkeypatch):
    async def must_not_run(*a, **k):
        pytest.fail("the copy ran for a refused principal")

    monkeypatch.setattr(setup, "_copy_saved_key_for_first_account", must_not_run)
    with pytest.raises(HTTPException) as refused:
        await setup.complete_setup(
            _req(saved_key_provider="anthropic", user_id=str(uuid.uuid4())),
            current_user=SimpleNamespace(sub=PRINCIPAL),
        )
    assert refused.value.status_code == 403


# ── rule 5 and CXO's test shape: what each account hears at the button ──────


@pytest.mark.asyncio
@pytest.mark.parametrize("route", ["use", "check"])
async def test_a_later_account_hears_exactly_cxos_line(wired, route):
    wired.other_account = True
    if route == "use":
        r = await setup.use_keychain(setup.KeychainUseRequest(provider="anthropic"))
        assert (r.success, r.valid) == (False, False)
    else:
        r = await setup.check_keychain("anthropic")
        assert r.exists is False
    assert r.message == setup.SAVED_KEY_BELONGS_TO_FIRST_ACCOUNT_MESSAGE
    assert r.message == (
        "The saved key on this computer belongs to the first account set up here. "
        "Paste your own key here."
    )


@pytest.mark.asyncio
async def test_the_first_account_hears_the_tick_line(wired):
    r = await setup.use_keychain(setup.KeychainUseRequest(provider="anthropic"))
    assert (r.success, r.valid) == (True, True)
    assert r.message == "Using the Anthropic key you already saved."


@pytest.mark.asyncio
async def test_a_signed_in_first_account_is_not_a_later_one(monkeypatch):
    seen = []

    async def other(principal):
        seen.append(principal)
        return False

    monkeypatch.setattr(setup, "_another_account_completed_setup", other)
    monkeypatch.setattr("services.infrastructure.deployment.is_hosted_deployment", lambda: False)
    monkeypatch.setattr("services.infrastructure.keychain_service.KeychainService", FakeKeychain)
    await setup.use_keychain(
        setup.KeychainUseRequest(provider="anthropic"), current_user=SimpleNamespace(sub=PRINCIPAL)
    )
    assert seen == [PRINCIPAL]


# ── (a) end to end through the real route, store and resolver ────────────────


@pytest.fixture
def db_store_and_global_slot(monkeypatch):
    """The real encrypted-DB store, and the install-wide anthropic slot snapshotted and
    put back after (the shared dev database's value is never lost), as 1810's file does."""
    from services.infrastructure.keychain_service import KeychainService

    monkeypatch.setenv("PIPER_CREDENTIAL_STORE", "db")
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", _MASTER_KEY)
    keychain = KeychainService()
    before = keychain.get_api_key("anthropic")
    yield keychain
    current = keychain.get_api_key("anthropic")
    if before is None:
        if current is not None:
            keychain.delete_api_key("anthropic")
    elif current != before:
        keychain.store_api_key("anthropic", before)


@pytest.mark.asyncio
async def test_a_the_copied_row_is_the_one_chat_resolves(db_store_and_global_slot, monkeypatch):
    from services.auth.password_service import PasswordService
    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory
    from web.utils.llm_key import resolve_user_llm_key

    keychain = db_store_and_global_slot
    keychain.store_api_key("anthropic", GOOD_ANTHROPIC_KEY)  # guide step 5's call

    async def first_account(principal):
        return False  # the shared dev database holds other accounts; this pins the first

    monkeypatch.setattr(setup, "_another_account_completed_setup", first_account)
    monkeypatch.setattr("services.infrastructure.deployment.is_hosted_deployment", lambda: False)

    name = f"u2405_{uuid.uuid4().hex[:12]}"
    user = User(
        id=uuid.uuid4(),
        username=name,
        email=f"{name}@test.invalid",
        password_hash=PasswordService().hash_password("Test-Passw0rd-1!"),
        is_active=True,
    )
    uid = str(user.id)
    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(user)
        await session.commit()
    try:
        r = await setup.complete_setup(
            _req(saved_key_provider="anthropic"), current_user=SimpleNamespace(sub=uid)
        )
        assert r.success
        assert await resolve_user_llm_key(None, uid) == GOOD_ANTHROPIC_KEY
        consent = keychain.get_api_key("authorized_llm_providers", username=uid) or ""
        assert "anthropic" in consent.split(",")
        assert keychain.get_api_key("anthropic") == GOOD_ANTHROPIC_KEY  # copy, not move
    finally:
        for p in ("anthropic", "authorized_llm_providers", "default_llm_provider"):
            keychain.delete_api_key(p, username=uid)
        keychain.delete_cli_token(uid)
        async with AsyncSessionFactory.session_scope_fresh() as session:
            await session.execute(text("DELETE FROM user_api_keys WHERE user_id = :u"), {"u": uid})
            await session.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid})
            await session.commit()
