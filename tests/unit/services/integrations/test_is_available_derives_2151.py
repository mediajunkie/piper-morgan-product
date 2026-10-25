"""#2151 (Arch 10-24 16:49): ``is_available()`` derives from ``resolve_credential``, and the
resolver's PAT legs tell absence from failure.

- Not connected (False) means only CONNECT_REQUIRED: no binding, or an unbound one, and no
  stored PAT. Any other degrade, or a store that didn't answer, raises ``GitHubReadFailed``.
- A PAT leg answers None only on verified absence; a failed read raises
  ``detail="store_failed"``, and the resolver degrades UNREACHABLE, never CONNECT_REQUIRED.
- Every ``is_available()`` gate in ``intent_service.py`` catches the raise onto an honest
  line (the forcing test at the bottom), so a new gate can't skip it.
"""

import ast
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.infrastructure.keychain_service import SecretProvenance, SecretRead
from services.integrations.github.read_failed import GitHubReadFailed
from services.mcp.consumer.connector import DegradationReason, DegradationResponse

USER = "694d8f4e-0000-0000-0000-000000000042"
REPO_ROOT = Path(__file__).resolve().parents[4]


# ── the at-rest leg: retrieve_user_key_strict ──────────────────────────────────


def _session_with(row):
    result = MagicMock()
    result.scalar_one_or_none.return_value = row
    session = MagicMock()
    session.execute = AsyncMock(return_value=result)
    return session


def _service(read: SecretRead, decrypted=None):
    from services.security.user_api_key_service import UserAPIKeyService

    keychain = MagicMock()
    keychain.aread_secret = AsyncMock(return_value=read)
    svc = UserAPIKeyService(keychain_service=keychain, field_encryption_service=MagicMock())
    svc._decrypt_secret = MagicMock(return_value=decrypted)
    return svc


class TestRetrieveUserKeyStrict:
    @pytest.mark.asyncio
    async def test_no_active_row_is_absence(self):
        svc = _service(SecretRead(SecretProvenance.VERIFIED_ABSENT))
        assert await svc.retrieve_user_key_strict(_session_with(None), USER, "github") is None

    @pytest.mark.asyncio
    async def test_a_decrypted_row_serves(self):
        svc = _service(SecretRead(SecretProvenance.VERIFIED_ABSENT), decrypted="fake-token-row")
        row = MagicMock(encrypted_secret="ciphertext")
        assert await svc.retrieve_user_key_strict(_session_with(row), USER, "github") == (
            "fake-token-row"
        )

    @pytest.mark.asyncio
    async def test_the_keychain_fallback_serves(self):
        svc = _service(SecretRead(SecretProvenance.PRESENT, value="fake-token-kc"))
        row = MagicMock(encrypted_secret=None)
        assert await svc.retrieve_user_key_strict(_session_with(row), USER, "github") == (
            "fake-token-kc"
        )

    @pytest.mark.parametrize(
        "read",
        [
            SecretRead(SecretProvenance.VERIFIED_ABSENT),
            SecretRead(SecretProvenance.STORE_FAILED, error="keychain timeout"),
        ],
        ids=["row-but-keychain-empty", "keychain-store-failed"],
    )
    @pytest.mark.asyncio
    async def test_an_active_row_that_cant_be_read_raises(self, read):
        """Arch: a row that exists is not absence."""
        from services.security.user_api_key_service import UserKeyReadFailed

        svc = _service(read, decrypted=None)
        row = MagicMock(encrypted_secret="ciphertext")
        with pytest.raises(UserKeyReadFailed):
            await svc.retrieve_user_key_strict(_session_with(row), USER, "github")

    @pytest.mark.asyncio
    async def test_the_lenient_read_keeps_its_contract(self):
        """Other callers only try a key: ``retrieve_user_key`` still answers None."""
        svc = _service(SecretRead(SecretProvenance.STORE_FAILED, error="x"))
        svc._keychain.get_api_key.side_effect = RuntimeError("store down")
        row = MagicMock(encrypted_secret=None)
        assert await svc.retrieve_user_key(_session_with(row), USER, "github") is None


# ── the keychain leg: GitHubConfigService.read_user_token ──────────────────────


def _keychain_reading(read: SecretRead):
    kc = MagicMock()
    kc.read_secret.return_value = read
    return patch("services.infrastructure.keychain_service.KeychainService", return_value=kc)


class TestKeychainLeg:
    def test_verified_absent_is_none(self):
        from services.integrations.github.config_service import GitHubConfigService

        with _keychain_reading(SecretRead(SecretProvenance.VERIFIED_ABSENT)):
            assert GitHubConfigService().read_user_token(USER) is None

    def test_present_serves(self):
        from services.integrations.github.config_service import GitHubConfigService

        with _keychain_reading(SecretRead(SecretProvenance.PRESENT, value="fake-token-kc")):
            assert GitHubConfigService().read_user_token(USER) == "fake-token-kc"

    def test_store_failed_raises(self):
        from services.integrations.github.config_service import (
            GitHubConfigService,
            GitHubTokenStoreFailed,
        )

        with _keychain_reading(SecretRead(SecretProvenance.STORE_FAILED, error="timeout")):
            with pytest.raises(GitHubTokenStoreFailed):
                GitHubConfigService().read_user_token(USER)

    def test_a_store_failure_is_not_cached(self):
        """Arch: ``get_authentication_token`` mustn't cache a store failure."""
        from services.integrations.github.config_service import GitHubConfigService

        svc = GitHubConfigService()
        with _keychain_reading(SecretRead(SecretProvenance.STORE_FAILED, error="timeout")):
            assert svc.get_authentication_token(USER) is None
        with _keychain_reading(SecretRead(SecretProvenance.PRESENT, value="fake-token-kc")):
            assert svc.get_authentication_token(USER) == "fake-token-kc"


# ── the adapter's legs and resolver ─────────────────────────────────────────────


def _adapter():
    from services.mcp.consumer.github_adapter import GitHubMCPSpatialAdapter

    return GitHubMCPSpatialAdapter()


def _binding(status):
    return None if status is None else MagicMock(status=status, owner_id=USER, mcp_server_ref="gh")


def _resolve(adapter, *, binding=None, at_rest=None, keychain=None):
    def leg(value):
        if isinstance(value, Exception):
            return {"side_effect": value}
        return {"return_value": value}

    return (
        patch(
            "services.mcp.consumer.github_adapter.ConnectorBindingRepository.get",
            new=AsyncMock(return_value=binding),
        ),
        patch.object(type(adapter), "_user_pat_at_rest", new=AsyncMock(**leg(at_rest))),
        patch.object(type(adapter), "_user_pat", **leg(keychain)),
    )


STORE_FAILED = GitHubReadFailed("x", None, detail="store_failed")


class TestPatLegsRaise:
    @pytest.mark.asyncio
    async def test_at_rest_failure_raises_store_failed(self):
        with patch(
            "services.security.user_api_key_service.UserAPIKeyService.retrieve_user_key_strict",
            new=AsyncMock(side_effect=RuntimeError("db down")),
        ):
            with pytest.raises(GitHubReadFailed) as caught:
                await _adapter()._user_pat_at_rest(USER)
        assert caught.value.detail == "store_failed"

    def test_keychain_failure_raises_store_failed(self):
        from services.integrations.github.config_service import GitHubTokenStoreFailed

        with patch(
            "services.integrations.github.config_service.GitHubConfigService.read_user_token",
            side_effect=GitHubTokenStoreFailed("timeout"),
        ):
            with pytest.raises(GitHubReadFailed) as caught:
                _adapter()._user_pat(USER)
        assert caught.value.detail == "store_failed"


class TestResolver:
    @pytest.mark.asyncio
    async def test_no_binding_and_verified_absent_is_connect_required(self):
        adapter = _adapter()
        b, a, k = _resolve(adapter)
        with b, a, k:
            got = await adapter.resolve_credential(USER)
        assert got.reason is DegradationReason.CONNECT_REQUIRED

    @pytest.mark.parametrize("failing", ["at_rest", "keychain"])
    @pytest.mark.asyncio
    async def test_a_failed_leg_is_never_connect_required(self, failing):
        adapter = _adapter()
        b, a, k = _resolve(adapter, **{failing: STORE_FAILED})
        with b, a, k:
            got = await adapter.resolve_credential(USER)
        assert isinstance(got, DegradationResponse)
        assert got.reason is DegradationReason.UNREACHABLE
        assert "isn't connected" not in got.user_message

    @pytest.mark.asyncio
    async def test_a_failed_at_rest_leg_still_serves_the_keychain_pat(self):
        adapter = _adapter()
        b, a, k = _resolve(adapter, at_rest=STORE_FAILED, keychain="fake-token-kc")
        with b, a, k:
            got = await adapter.resolve_credential(USER)
        assert getattr(got, "leg", None) == "pat"

    @pytest.mark.asyncio
    async def test_a_stale_binding_keeps_its_reason(self):
        adapter = _adapter()
        b, a, k = _resolve(adapter, binding=_binding("stale"), at_rest=STORE_FAILED)
        with b, a, k:
            got = await adapter.resolve_credential(USER)
        assert got.reason is DegradationReason.STALE_TOKEN


# ── is_available ───────────────────────────────────────────────────────────────


def _router():
    from services.integrations.github.github_integration_router import GitHubIntegrationRouter

    r = GitHubIntegrationRouter()
    r._user_id = USER
    return r


def _degrade(reason):
    return DegradationResponse(reason=reason, user_message="x")


class TestIsAvailable:
    @pytest.mark.asyncio
    async def test_connect_required_is_the_only_false(self):
        r = _router()
        with patch.object(
            r.mcp_adapter,
            "resolve_credential",
            new=AsyncMock(return_value=_degrade(DegradationReason.CONNECT_REQUIRED)),
        ):
            assert await r.is_available() is False

    @pytest.mark.parametrize(
        "reason",
        [
            DegradationReason.STALE_TOKEN,
            DegradationReason.UNREACHABLE,
            DegradationReason.MISCONFIGURED,
        ],
    )
    @pytest.mark.asyncio
    async def test_any_other_degrade_raises_with_its_reason(self, reason):
        r = _router()
        with patch.object(
            r.mcp_adapter, "resolve_credential", new=AsyncMock(return_value=_degrade(reason))
        ):
            with pytest.raises(GitHubReadFailed) as caught:
                await r.is_available()
        assert caught.value.reason is reason

    @pytest.mark.asyncio
    async def test_a_resolver_exception_raises_store_failed(self):
        r = _router()
        with patch.object(
            r.mcp_adapter, "resolve_credential", new=AsyncMock(side_effect=RuntimeError("db"))
        ):
            with pytest.raises(GitHubReadFailed) as caught:
                await r.is_available()
        assert caught.value.detail == "store_failed"

    @pytest.mark.asyncio
    async def test_a_credential_is_true(self):
        from services.mcp.consumer.github_adapter import GitHubCredential

        r = _router()
        cred = GitHubCredential(owner_id=USER, mcp_server_ref="gh", token="fake-token", leg="pat")
        with patch.object(r.mcp_adapter, "resolve_credential", new=AsyncMock(return_value=cred)):
            assert await r.is_available() is True


# ── the gate's honest line ─────────────────────────────────────────────────────


class TestGateLine:
    def _svc(self):
        from services.intent.intent_service import IntentService

        return IntentService.__new__(IntentService)

    @pytest.mark.parametrize(
        "rf",
        [
            GitHubReadFailed("x", DegradationReason.UNREACHABLE, detail="store_failed"),
            GitHubReadFailed("x", DegradationReason.MISCONFIGURED, detail="misconfigured"),
            GitHubReadFailed("x", DegradationReason.STALE_TOKEN, detail="stale_token"),
        ],
        ids=["store-failed", "misconfigured", "stale"],
    )
    def test_a_failed_check_never_says_not_connected(self, rf):
        svc = self._svc()
        svc.logger = MagicMock()
        out = svc._github_gate_failed(rf, "close_issue", "close that issue")
        assert out.success is False
        assert "isn't connected" not in out.message
        assert "close that issue" in out.message
        assert out.intent_data["context"]["read_failed"] == rf.reason_code

    def test_stale_says_reauthorize(self):
        svc = self._svc()
        svc.logger = MagicMock()
        rf = GitHubReadFailed("x", DegradationReason.STALE_TOKEN, detail="stale_token")
        assert "re-authorizing" in svc._github_gate_failed(rf, "a", "do it").message


# ── forcing test: every gate catches the raise ─────────────────────────────────

GATE_SITES = 10  # Arch 10-24 16:49 listed ten; a new gate raises this, never skips the catch


def _handler_names(handler: ast.ExceptHandler):
    t = handler.type
    elts = t.elts if isinstance(t, ast.Tuple) else [t]
    return {getattr(e, "id", getattr(e, "attr", None)) for e in elts if e is not None}


def _is_available_awaits(tree):
    """Each ``await <x>.is_available()`` with the chain of its enclosing nodes."""
    found = []

    def walk(node, parents):
        if (
            isinstance(node, ast.Await)
            and isinstance(node.value, ast.Call)
            and isinstance(node.value.func, ast.Attribute)
            and node.value.func.attr == "is_available"
        ):
            found.append((node, list(parents)))
        for child in ast.iter_child_nodes(node):
            walk(child, parents + [node])

    walk(tree, [])
    return found


def test_every_is_available_gate_catches_github_read_failed():
    src = (REPO_ROOT / "services/intent/intent_service.py").read_text()
    sites = _is_available_awaits(ast.parse(src))
    assert len(sites) == GATE_SITES, (
        f"{len(sites)} is_available() gates (pinned {GATE_SITES}). A new gate must catch "
        "GitHubReadFailed onto an honest line (_github_gate_failed), then update the pin."
    )
    uncaught = []
    for node, parents in sites:
        guarded = False
        for i, parent in enumerate(parents):
            if not isinstance(parent, ast.Try):
                continue
            child = parents[i + 1] if i + 1 < len(parents) else node
            if child in parent.body and any(
                "GitHubReadFailed" in _handler_names(h) for h in parent.handlers
            ):
                guarded = True
        if not guarded:
            uncaught.append(node.lineno)
    assert not uncaught, f"is_available() gates with no GitHubReadFailed catch: {uncaught}"


# ── the productivity summary (CXO 10-24 16:54) ─────────────────────────────────


@pytest.fixture
def intent_service():
    from services.intent.intent_service import IntentService

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


async def _productivity(intent_service, gate):
    from services.domain.models import Intent, IntentCategory

    with (
        patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter,
        patch("services.repositories.todo_repository.TodoRepository") as MockRepo,
        patch("services.intent.intent_service.AsyncSessionFactory.session_scope") as scope,
    ):
        mock_router = MagicMock()
        mock_router.is_available = AsyncMock(**gate)
        mock_router.initialize = AsyncMock()
        mock_router.get_closed_issues = AsyncMock(return_value=[])
        MockRouter.return_value = mock_router
        repo = MagicMock()
        repo.get_completion_stats = AsyncMock(
            return_value={"completed": 2, "total_created": 3, "active": 1, "completion_rate": 66.7}
        )
        MockRepo.return_value = repo
        scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
        scope.return_value.__aexit__ = AsyncMock(return_value=False)
        intent = Intent(
            category=IntentCategory.QUERY,
            action="productivity",
            confidence=0.9,
            context={"user_id": USER, "session_id": "s-1", "original_message": "productivity"},
        )
        return await intent_service._handle_productivity_query(intent, "wf", "s-1")


@pytest.mark.asyncio
async def test_a_failed_gate_gets_the_couldnt_check_line_after_the_summary(intent_service):
    from services.intent.intent_service import PRODUCTIVITY_GITHUB_CHECK_FAILED

    rf = GitHubReadFailed("x", DegradationReason.UNREACHABLE, detail="store_failed")
    result = await _productivity(intent_service, {"side_effect": rf})
    assert result.message.endswith("\n\n" + PRODUCTIVITY_GITHUB_CHECK_FAILED)
    assert "**GitHub:**" not in result.message
    assert "Issues/PRs Closed" not in result.message


@pytest.mark.asyncio
async def test_not_connected_gets_no_line(intent_service):
    from services.intent.intent_service import PRODUCTIVITY_GITHUB_CHECK_FAILED

    result = await _productivity(intent_service, {"return_value": False})
    assert PRODUCTIVITY_GITHUB_CHECK_FAILED not in result.message
    assert "GitHub" not in result.message
