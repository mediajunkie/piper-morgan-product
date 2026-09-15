"""#1810 — setup's ``/complete`` route stored a GLOBAL unprefixed copy of the
caller's OpenAI/Anthropic key on EVERY completion (``web/api/routes/setup.py``,
~:1021-1041, citing #724) in addition to the correct per-user
``{user_id}_{provider}_api_key`` entry. The global slot IS what
``LLMConfigService.get_api_key()`` / ``LLMClient._init_clients()`` resolve as
"the server's key" — every user who finished setup silently overwrote
whichever key the operator (or any earlier user) had in place, last-writer-
wins, no audit, no confirmation (#1810 issue body).

PM ruling 2026-09-14 (decisions.log): the server-key concept "is not a real
concept and will not be supported in any sense." That removes the blocking
question and pins the fix: the per-user write must survive untouched; the
global write must be gone.

These tests drive the REAL route function (``complete_setup``, not a mock of
a helper) against the REAL ``KeychainService`` abstraction — forced onto the
encrypted-DB backend (#1382) so the assertions read real Postgres rows
instead of the local OS keychain. Nothing on ``KeychainService`` itself
(``get_api_key``/``store_api_key``/``delete_api_key``) is mocked.
"""

from __future__ import annotations

import secrets
import uuid

import pytest
from sqlalchemy import text

from services.auth.password_service import PasswordService
from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.infrastructure.keychain_service import KeychainService
from web.api.routes.setup import SetupCompleteRequest, complete_setup

pytestmark = pytest.mark.unit

# Same value used by tests/security/test_secure_credential_store_1382.py — a
# valid urlsafe-base64-encoded 32-byte key.
_MASTER_KEY = "S" * 43 + "="

_GLOBAL_PROVIDERS = ("openai", "anthropic")
_PER_USER_KEYS = ("openai", "anthropic", "authorized_llm_providers", "default_llm_provider")


def _valid_key(prefix: str, min_len: int, target_len: int) -> str:
    """A real-format, high-entropy key that clears format + strength + leak
    validation (services/security/api_key_validator.py) WITHOUT mocking the
    validator. Random token_urlsafe output essentially never collides with
    the local weak-pattern/known-test-key quick checks; retried defensively.
    """
    body_len = max(min_len, target_len) - len(prefix)
    for _ in range(20):
        candidate = prefix + secrets.token_urlsafe(body_len + 10)[:body_len]
        if len(candidate) >= min_len:
            return candidate
    raise RuntimeError("could not generate a validator-acceptable test key")


def _openai_key() -> str:
    return _valid_key("sk-", 20, 40)


def _anthropic_key() -> str:
    return _valid_key("sk-ant-", 100, 110)


def _mk_user() -> User:
    name = f"u1810_{uuid.uuid4().hex[:12]}"
    return User(
        id=uuid.uuid4(),
        username=name,
        email=f"{name}@test.invalid",
        password_hash=PasswordService().hash_password("Test-Passw0rd-1!"),
        is_active=True,
    )


async def _cleanup_user(user_id: str, keychain: KeychainService) -> None:
    """Best-effort teardown: real rows in a real (shared, non-transactional)
    dev Postgres — must be deleted explicitly, not rolled back."""
    for provider in _PER_USER_KEYS:
        keychain.delete_api_key(provider, username=user_id)
    keychain.delete_cli_token(user_id)
    async with AsyncSessionFactory.session_scope_fresh() as session:
        await session.execute(
            text("DELETE FROM user_api_keys WHERE user_id = :uid"), {"uid": user_id}
        )
        await session.execute(text("DELETE FROM users WHERE id = :uid"), {"uid": user_id})
        await session.commit()


@pytest.fixture(autouse=True)
def _db_backed_keychain_and_global_key_protection(monkeypatch):
    """Force every KeychainService() construction in this test module onto
    the real encrypted-DB store (#1382) instead of the OS keychain —
    deterministic, no Keychain-access dialogs, still the real
    KeychainService/get_api_key/store_api_key abstraction end to end.

    Also snapshots the two GLOBAL provider slots before the test and
    restores them after: if the bug is present the test will WRITE to
    ``openai_api_key``/``anthropic_api_key`` (the whole point of the pin),
    and this repo's Postgres is a real, possibly-shared dev database — we
    must not leave a global slot in a different state than we found it,
    and must never blind-delete a real pre-existing value (CLAUDE.md:
    pause before irreversible actions).
    """
    monkeypatch.setenv("PIPER_CREDENTIAL_STORE", "db")
    monkeypatch.setenv("ENCRYPTION_MASTER_KEY", _MASTER_KEY)

    keychain = KeychainService()
    before = {p: keychain.get_api_key(p) for p in _GLOBAL_PROVIDERS}

    yield

    for provider, prior_value in before.items():
        current = keychain.get_api_key(provider)
        if prior_value is None:
            if current is not None:
                keychain.delete_api_key(provider)
        elif current != prior_value:
            keychain.store_api_key(provider, prior_value)


class TestNoGlobalKeyWriteOnSetupComplete:
    @pytest.mark.asyncio
    async def test_complete_setup_writes_per_user_key_never_global(self):
        user = _mk_user()
        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(user)
            await session.commit()

        user_id = str(user.id)
        openai_key = _openai_key()
        anthropic_key = _anthropic_key()
        keychain = KeychainService()

        try:
            req = SetupCompleteRequest(
                user_id=user_id,
                openai_key=openai_key,
                anthropic_key=anthropic_key,
            )
            response = await complete_setup(req)
            assert response.success is True

            # Per-user entries: present and correct — #1810's scope keeps
            # this path untouched.
            assert keychain.get_api_key("openai", username=user_id) == openai_key
            assert keychain.get_api_key("anthropic", username=user_id) == anthropic_key

            # Global unprefixed entries: MUST NOT exist. This is the
            # red-first assertion — pre-fix, these equal openai_key /
            # anthropic_key because setup.py wrote them unconditionally
            # ("No username = global").
            assert keychain.get_api_key("openai") is None, (
                "setup completion wrote a GLOBAL unprefixed openai key — "
                "this is the #1810 cross-user credential write"
            )
            assert keychain.get_api_key("anthropic") is None, (
                "setup completion wrote a GLOBAL unprefixed anthropic key — "
                "this is the #1810 cross-user credential write"
            )
        finally:
            await _cleanup_user(user_id, keychain)

    @pytest.mark.asyncio
    async def test_second_user_completion_cannot_clobber_first_users_key(self):
        """The exact scenario #1810 names: 'every user who completes setup
        overwrites the operator's server key with their own. Last writer
        wins, silently.' With the global write gone there is nothing left
        for a second user's completion to clobber."""
        user_a, user_b = _mk_user(), _mk_user()
        async with AsyncSessionFactory.session_scope_fresh() as session:
            session.add(user_a)
            session.add(user_b)
            await session.commit()

        uid_a, uid_b = str(user_a.id), str(user_b.id)
        key_a, key_b = _openai_key(), _openai_key()
        keychain = KeychainService()

        try:
            await complete_setup(SetupCompleteRequest(user_id=uid_a, openai_key=key_a))
            await complete_setup(SetupCompleteRequest(user_id=uid_b, openai_key=key_b))

            # Both users retain their OWN key — the second completion did
            # not touch the first user's per-user entry.
            assert keychain.get_api_key("openai", username=uid_a) == key_a
            assert keychain.get_api_key("openai", username=uid_b) == key_b

            # Neither completion ever wrote the global slot, so there was
            # never a shared slot for the second write to clobber.
            assert keychain.get_api_key("openai") is None
        finally:
            await _cleanup_user(uid_a, keychain)
            await _cleanup_user(uid_b, keychain)
