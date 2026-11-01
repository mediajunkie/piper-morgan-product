"""#2238: on hosted, the user's own Notion key is the only source, read the way the save wrote it.

Arch's finding (10-30, #1442's N1/C1): ``NotionConfigService`` resolved env
``NOTION_API_KEY`` > ``PIPER.user.md`` > the user's keychain key, and a keyless
user fell back to ``connect()``'s env/static resolution. On a hosted deployment
a global env key would override every user's own key and a keyless user would
read the global workspace. Not live (no such secret is set), but one env var away.

Lead's store caveat: ``save_notion_key`` writes the keychain (best-effort) and
then the encrypted ``user_api_keys`` row; status read the row, chat read the
keychain. A failed keychain write left a key status saw and chat could not use.

Built here (the issue's two requirements):
1. Hosted: no env, no PIPER.user.md for the key; no key means not connected and
   never the legacy connect. Decided by ``is_hosted_deployment()``, never by
   probing local state. Local single-tenant behaviour is unchanged.
2. One read path: ``NotionConfigService.aget_user_api_key`` is
   ``UserAPIKeyService.retrieve_user_key`` (the encrypted row, then the keychain),
   the same read the save writes and the status surface already uses. The chat
   gates (``ais_available``), ``connect_for_user``, the MCP connector and the two
   Notion routes read through it.

LAYER: the config service, router and status service with the store faked or
the real ``UserAPIKeyService`` over a fake session and a fake keychain (the real
encryptor). Nothing served; the served save-then-chat is the issue's second
acceptance line, PA's.
"""

from __future__ import annotations

import uuid
from contextlib import asynccontextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest

from services.infrastructure.keychain_service import SecretProvenance, SecretRead
from services.integrations.notion.config_service import NotionConfigService
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter
from services.security.field_encryption import FieldEncryptionService
from services.security.user_api_key_service import UserAPIKeyService

pytestmark = pytest.mark.asyncio

HOSTED = "services.infrastructure.deployment.is_hosted_deployment"
KEYCHAIN_GET = "services.infrastructure.keychain_service.KeychainService.get_api_key"
USER = str(uuid.uuid4())


@asynccontextmanager
async def _no_session():
    yield None


class _FakeKeyService:
    """Stands in for UserAPIKeyService: a dict of user -> key, or a raise."""

    def __init__(self, table=None, raises=None):
        self.table = table or {}
        self.raises = raises
        self.calls = 0

    async def retrieve_user_key(self, session, user_id, provider):
        self.calls += 1
        assert provider == "notion"
        if self.raises:
            raise self.raises
        return self.table.get(str(user_id))


def _svc(table=None, raises=None) -> tuple[NotionConfigService, _FakeKeyService]:
    fake = _FakeKeyService(table, raises)
    return NotionConfigService(user_key_service=fake, session_scope=_no_session), fake


# ─────────────────────────── requirement 1: hosted sources ───────────────────


class TestHostedKeySource:
    async def test_hosted_env_key_set_and_user_key_present_uses_the_users_key(self, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "secret_global_env")
        svc, fake = _svc({USER: "secret_user_own"})
        with patch(HOSTED, return_value=True), patch(KEYCHAIN_GET, return_value=None):
            cfg = await svc.aget_config(USER)
            assert cfg.api_key == "secret_user_own"
            assert svc.get_config(USER).api_key == "secret_user_own", "the cache converges"
            assert await svc.ais_configured(USER) is True
        assert fake.calls >= 1

    async def test_hosted_keyless_with_env_set_is_not_connected(self, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "secret_global_env")
        svc, _ = _svc({})
        with patch(HOSTED, return_value=True), patch(KEYCHAIN_GET, return_value=None):
            assert (await svc.aget_config(USER)).api_key == ""
            assert await svc.ais_configured(USER) is False
            assert svc.get_config(USER).api_key == "", "the sync chain never reads env on hosted"

    async def test_hosted_never_reads_piper_user_md(self, monkeypatch):
        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        svc, _ = _svc({})
        with (
            patch(HOSTED, return_value=True),
            patch(KEYCHAIN_GET, return_value=None),
            patch.object(
                NotionConfigService,
                "_load_from_user_config",
                return_value={"authentication": {"api_key": "secret_from_file"}},
            ) as loader,
        ):
            assert (await svc.aget_config(USER)).api_key == ""
        loader.assert_not_called()

    async def test_local_env_key_still_wins_and_the_store_is_not_consulted(self, monkeypatch):
        """Local single-tenant behaviour is unchanged."""
        monkeypatch.setenv("NOTION_API_KEY", "secret_local_env")
        svc, fake = _svc(raises=RuntimeError("must not be read"))
        with patch(HOSTED, return_value=False):
            assert (await svc.aget_config(USER)).api_key == "secret_local_env"
        assert fake.calls == 0

    async def test_local_keyless_falls_back_to_the_user_store(self, monkeypatch):
        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        svc, _ = _svc({USER: "secret_user_own"})
        with (
            patch(HOSTED, return_value=False),
            patch(KEYCHAIN_GET, return_value=None),
            patch.object(NotionConfigService, "_load_from_user_config", return_value={}),
        ):
            assert (await svc.aget_config(USER)).api_key == "secret_user_own"


class TestHostedConnectNeverLegacy:
    async def test_hosted_keyless_connect_for_user_refuses_and_builds_no_client(self, monkeypatch):
        monkeypatch.setenv("NOTION_API_KEY", "secret_global_env")
        svc, _ = _svc({})
        router = NotionIntegrationRouter(config_service=svc)
        with (
            patch(HOSTED, return_value=True),
            patch(KEYCHAIN_GET, return_value=None),
            patch.object(
                NotionIntegrationRouter, "connect", new=AsyncMock(return_value=True)
            ) as connect,
        ):
            assert await router.connect_for_user(USER) is False
            assert await router.ais_available(USER) is False
        connect.assert_not_awaited()

    async def test_hosted_user_with_key_connects_with_that_key(self):
        svc, _ = _svc({USER: "secret_user_own"})
        router = NotionIntegrationRouter(config_service=svc)
        with (
            patch(HOSTED, return_value=True),
            patch(KEYCHAIN_GET, return_value=None),
            patch.object(
                NotionIntegrationRouter, "connect", new=AsyncMock(return_value=True)
            ) as connect,
        ):
            assert await router.ais_available(USER) is True
            assert await router.connect_for_user(USER) is True
        connect.assert_awaited_once_with(integration_token="secret_user_own")

    async def test_local_keyless_still_falls_back_to_legacy_connect(self, monkeypatch):
        monkeypatch.delenv("NOTION_API_KEY", raising=False)
        svc, _ = _svc({})
        router = NotionIntegrationRouter(config_service=svc)
        with (
            patch(HOSTED, return_value=False),
            patch(KEYCHAIN_GET, return_value=None),
            patch.object(NotionConfigService, "_load_from_user_config", return_value={}),
            patch.object(
                NotionIntegrationRouter, "connect", new=AsyncMock(return_value=False)
            ) as connect,
        ):
            await router.connect_for_user(USER)
        connect.assert_awaited_once_with(integration_token=None)

    async def test_a_failed_store_read_gates_closed_not_500(self):
        svc, _ = _svc(raises=RuntimeError("db down"))
        router = NotionIntegrationRouter(config_service=svc)
        with patch(HOSTED, return_value=True), patch(KEYCHAIN_GET, return_value=None):
            assert await router.ais_available(USER) is False
            assert (await svc.aget_config(USER)).api_key == ""


# ─────────────────────────── requirement 2: one read path ────────────────────


class _FakeKeychain:
    """The keychain half of the save: records writes, or refuses them."""

    def __init__(self, write_raises: Exception | None = None):
        self.store: dict[tuple[str, str | None], str] = {}
        self.write_raises = write_raises

    def store_api_key(self, provider, api_key, username=None):
        if self.write_raises:
            raise self.write_raises
        self.store[(provider, username)] = api_key

    def get_api_key(self, provider, username=None):
        return self.store.get((provider, username))

    async def aread_secret(self, provider, username=None):
        value = self.store.get((provider, username))
        if value:
            return SecretRead(provenance=SecretProvenance.PRESENT, value=value)
        return SecretRead(provenance=SecretProvenance.VERIFIED_ABSENT)


class _FakeSession:
    """One user_api_keys row at most; the save adds it, the read selects it."""

    def __init__(self):
        self.rows: list = []

    def add(self, obj):
        self.rows.append(obj)

    async def execute(self, stmt):
        row = self.rows[0] if self.rows else None
        return SimpleNamespace(
            scalar_one_or_none=lambda: row,
            scalars=lambda: SimpleNamespace(all=lambda: list(self.rows)),
        )

    async def commit(self):
        pass

    async def flush(self):
        pass

    async def refresh(self, obj):
        pass


def _real_key_service(keychain: _FakeKeychain) -> UserAPIKeyService:
    return UserAPIKeyService(
        keychain_service=keychain,  # type: ignore[arg-type]
        field_encryption_service=FieldEncryptionService(b"2238-test-master-key-32-bytes!!!"),
    )


class TestOneReadPath:
    async def _save(self, keychain: _FakeKeychain) -> tuple[UserAPIKeyService, _FakeSession]:
        service = _real_key_service(keychain)
        session = _FakeSession()
        with patch(
            "services.security.user_api_key_service.audit_logger.log_api_key_event",
            new=AsyncMock(),
        ):
            await service.store_user_key(
                session, USER, "notion", "secret_saved_abc", validate=False, security_check=False
            )
        return service, session

    async def test_save_then_chat_read_on_the_encrypted_db_keychain(self):
        """The save writes the keychain and the encrypted row; the chat read
        goes through retrieve_user_key, the same function status uses."""
        keychain = _FakeKeychain()
        service, session = await self._save(keychain)
        assert keychain.store[("notion", USER)] == "secret_saved_abc"
        assert session.rows and session.rows[0].encrypted_secret

        @asynccontextmanager
        async def scope():
            yield session

        svc = NotionConfigService(user_key_service=service, session_scope=scope)
        with patch(HOSTED, return_value=True), patch(KEYCHAIN_GET, return_value=None):
            assert (await svc.aget_config(USER)).api_key == "secret_saved_abc"
            assert await svc.ais_configured(USER) is True
        # Status reads the same function, so it cannot disagree.
        assert await service.retrieve_user_key(session, USER, "notion") == "secret_saved_abc"

    async def test_a_failed_keychain_write_is_read_back_the_same_way(self):
        """The half-save: the keychain write fails, the encrypted row is written.
        Before #2238 status said configured and chat (keychain only) saw nothing.
        Now both read the row first."""
        keychain = _FakeKeychain(write_raises=RuntimeError("no keyring backend"))
        service, session = await self._save(keychain)
        assert ("notion", USER) not in keychain.store, "the keychain write did fail"
        assert session.rows and session.rows[0].encrypted_secret

        @asynccontextmanager
        async def scope():
            yield session

        svc = NotionConfigService(user_key_service=service, session_scope=scope)
        with patch(HOSTED, return_value=True), patch(KEYCHAIN_GET, return_value=None):
            assert (await svc.aget_config(USER)).api_key == "secret_saved_abc"
            router = NotionIntegrationRouter(config_service=svc)
            assert await router.ais_available(USER) is True
        assert await service.retrieve_user_key(session, USER, "notion") == "secret_saved_abc"

    async def test_the_chat_read_is_the_status_read_by_construction(self):
        """The config service's user-key read calls UserAPIKeyService.retrieve_user_key
        with the save's provider, nothing else."""
        svc, fake = _svc({USER: "secret_user_own"})
        with patch(HOSTED, return_value=True), patch(KEYCHAIN_GET, return_value=None):
            assert await svc.aget_user_api_key(USER) == "secret_user_own"
        assert fake.calls == 1


class TestStatusSurfaceOnHosted:
    async def test_hosted_status_does_not_call_an_env_key_configured(self, monkeypatch):
        from services.integrations.integration_status_service import IntegrationStatusService

        monkeypatch.setenv("NOTION_API_KEY", "secret_global_env")
        monkeypatch.delenv("NOTION_API_TOKEN", raising=False)
        with (
            patch(HOSTED, return_value=True),
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
                new=_no_session,
            ),
            patch.object(UserAPIKeyService, "retrieve_user_key", new=AsyncMock(return_value=None)),
        ):
            status = await IntegrationStatusService().get_status("u1", "notion")
        assert status["configured"] is False
        assert status.get("via") != "env"

    async def test_local_status_still_reports_the_env_key(self, monkeypatch):
        from services.integrations.integration_status_service import IntegrationStatusService

        monkeypatch.setenv("NOTION_API_KEY", "secret_global_env")
        with patch(HOSTED, return_value=False):
            status = await IntegrationStatusService().get_status("u1", "notion")
        assert status["configured"] is True
        assert status["via"] == "env"
