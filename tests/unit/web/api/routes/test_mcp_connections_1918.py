"""#1918 backend — Settings "Connected apps" list + revoke.

Pins the owner-scoping property the issue's acceptance criteria name
explicitly: a user can never list or revoke another user's MCP grants, a
revoke stamps BOTH the access token AND the refresh token for a client (so
a revoked client can't silently refresh back in), revoke is idempotent, and
revocation is effective on the next MCP call — proven against the real
``MCPTokenVerifier`` (unit 1), not asserted.

LAYER (m-43): the HTTP surface (``web/api/routes/mcp_connections.py``) is
exercised through a real ``TestClient`` with ONLY the auth dependency
overridden (the ``test_preferences_timezone_1876.py`` idiom: a minimal
``FastAPI()`` app with just this router mounted, `get_current_user`
overridden to a real ``JWTClaims`` for a given user id) — the real Pydantic
models and the real route bodies run. ``AsyncSessionFactory.session_scope``
is monkeypatched to an in-memory-SQLite-backed scope (the
``test_identity_unit1.py`` / ``test_oauth_as_unit4.py`` pattern), so the
router's own session-scope usage, `services/mcp/server/connections.py`'s
queries, and `MCPTokenVerifier.verify_token` all read/write the SAME store.

DENOMINATOR: the list + revoke routes and their owner-scoping, plus one
end-to-end pin that a revoke actually changes what the real token verifier
resolves. NOT covered here: the Settings UI card (separate, CXO-designed),
and the OAuth AS's own `/revoke` RFC-7009 endpoint (`oauth_provider.py`'s
`revoke_token`, already covered by `test_oauth_as_unit4.py`) — this is the
NEW user-facing revoke path, which goes directly at the DB rows rather than
through that RFC endpoint.
"""

from __future__ import annotations

import hashlib
import uuid
from contextlib import asynccontextmanager
from datetime import datetime, timedelta, timezone
from uuid import UUID, uuid4

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from fastapi import FastAPI  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.pool import StaticPool  # noqa: E402

from services.auth.auth_middleware import get_current_user  # noqa: E402
from services.auth.jwt_service import JWTClaims  # noqa: E402
from services.database.models import (  # noqa: E402
    MCPAccessToken,
    MCPOAuthClient,
    MCPOAuthRefreshToken,
)
from services.database.session_factory import AsyncSessionFactory  # noqa: E402
from services.mcp.server.identity import MCPTokenVerifier, hash_credential  # noqa: E402
from services.mcp.server.oauth_provider import OAUTH_LABEL_PREFIX  # noqa: E402
from web.api.routes.mcp_connections import router  # noqa: E402

pytestmark = pytest.mark.asyncio

USER_A = UUID("aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa")
USER_B = UUID("bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb")

CLIENT_X = "client-x"
CLIENT_Z = "client-z"

LIST_PATH = "/api/v1/settings/mcp-connections"


def _revoke_path(client_id: str) -> str:
    return f"/api/v1/settings/mcp-connections/{client_id}/revoke"


def _claims(user_id: UUID) -> JWTClaims:
    return JWTClaims(
        iss="piper-morgan",
        aud="piper-morgan-api",
        sub=str(user_id),
        exp=9999999999,
        iat=1000000000,
        jti=str(uuid4()),
        user_id=user_id,
        user_email=f"{user_id}@test.local",
        username="mcp-conn-1918",
        scopes=["user"],
        token_type="access",
        session_id=None,
    )


def _client_as(user_id: UUID) -> TestClient:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_current_user] = lambda: _claims(user_id)
    return TestClient(app)


@pytest_asyncio.fixture
async def store(monkeypatch):
    """In-memory SQLite holding the three tables this surface touches,
    with ``AsyncSessionFactory.session_scope`` monkeypatched to it so the
    router, the service module, AND ``MCPTokenVerifier`` (default
    constructor) all read/write the same store. Disposed on teardown
    regardless of outcome (test_identity_unit1.py's documented reason:
    skipping disposal leaves aiosqlite's worker thread running)."""
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
        connect_args={"check_same_thread": False},
    )
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def _scope():
        session = factory()
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

    async with engine.begin() as conn:
        for model in (MCPAccessToken, MCPOAuthClient, MCPOAuthRefreshToken):
            await conn.run_sync(
                lambda c, m=model: m.__table__.create(c, checkfirst=True)  # type: ignore[attr-defined]
            )

    monkeypatch.setattr(AsyncSessionFactory, "session_scope", _scope)

    yield factory

    await engine.dispose()


def _hash(raw: str) -> str:
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


async def _seed_access_token(
    factory,
    *,
    user_id: UUID,
    raw_token: str,
    label: str,
    created_at: datetime | None = None,
    last_used_at: datetime | None = None,
    revoked_at: datetime | None = None,
) -> None:
    async with factory() as session:
        session.add(
            MCPAccessToken(
                id=uuid.uuid4(),
                user_id=user_id,
                token_hash=_hash(raw_token),
                label=label,
                created_at=created_at or datetime.now(timezone.utc),
                last_used_at=last_used_at,
                revoked_at=revoked_at,
            )
        )
        await session.commit()


async def _seed_refresh_token(
    factory,
    *,
    user_id: UUID,
    client_id: str,
    raw_token: str,
    created_at: datetime | None = None,
    revoked_at: datetime | None = None,
) -> None:
    async with factory() as session:
        session.add(
            MCPOAuthRefreshToken(
                id=uuid.uuid4(),
                token_hash=_hash(raw_token),
                client_id=client_id,
                user_id=user_id,
                scopes=["resources:read"],
                created_at=created_at or datetime.now(timezone.utc),
                revoked_at=revoked_at,
            )
        )
        await session.commit()


async def _seed_client(factory, *, client_id: str, client_name: str | None) -> None:
    async with factory() as session:
        session.add(
            MCPOAuthClient(
                client_id=client_id,
                redirect_uris=["https://example.test/callback"],
                client_name=client_name,
                grant_types=["authorization_code", "refresh_token"],
                response_types=["code"],
            )
        )
        await session.commit()


class TestListIsOwnerScoped:
    async def test_list_returns_only_the_callers_grants(self, store):
        factory = store
        await _seed_client(factory, client_id=CLIENT_X, client_name="ChatGPT")
        await _seed_access_token(
            factory, user_id=USER_A, raw_token="a1", label=f"{OAUTH_LABEL_PREFIX}{CLIENT_X}"
        )
        await _seed_refresh_token(factory, user_id=USER_A, client_id=CLIENT_X, raw_token="a1r")
        await _seed_access_token(factory, user_id=USER_A, raw_token="a-manual", label="ops-mint")

        other_client = "client-only-b"
        await _seed_access_token(
            factory,
            user_id=USER_B,
            raw_token="b1",
            label=f"{OAUTH_LABEL_PREFIX}{other_client}",
        )

        resp = _client_as(USER_A).get(LIST_PATH)
        assert resp.status_code == 200, resp.text
        body = resp.json()

        assert len(body["oauth_connections"]) == 1
        conn = body["oauth_connections"][0]
        assert conn["client_id"] == CLIENT_X
        assert conn["client_name"] == "ChatGPT"
        assert conn["active"] is True

        assert len(body["manual_tokens"]) == 1
        assert body["manual_tokens"][0]["label"] == "ops-mint"

        # B's grant never appears for A, under any label.
        all_client_ids = [c["client_id"] for c in body["oauth_connections"]]
        assert other_client not in all_client_ids


class TestRevokeOwnership:
    async def test_user_b_revoking_as_client_is_404_and_as_rows_untouched(self, store):
        factory = store
        await _seed_access_token(
            factory, user_id=USER_A, raw_token="a1", label=f"{OAUTH_LABEL_PREFIX}{CLIENT_X}"
        )
        await _seed_refresh_token(factory, user_id=USER_A, client_id=CLIENT_X, raw_token="a1r")

        resp = _client_as(USER_B).post(_revoke_path(CLIENT_X))
        assert resp.status_code == 404, resp.text

        # A's rows are untouched: still listed, still active.
        listing = _client_as(USER_A).get(LIST_PATH).json()
        assert listing["oauth_connections"][0]["client_id"] == CLIENT_X
        assert listing["oauth_connections"][0]["active"] is True

    async def test_unknown_client_id_is_404(self, store):
        resp = _client_as(USER_A).post(_revoke_path("no-such-client"))
        assert resp.status_code == 404, resp.text


class TestRevokeStampsBothAccessAndRefresh:
    async def test_revoke_stamps_both_token_families_and_spares_other_clients(self, store):
        factory = store
        await _seed_access_token(
            factory, user_id=USER_A, raw_token="x1", label=f"{OAUTH_LABEL_PREFIX}{CLIENT_X}"
        )
        await _seed_refresh_token(factory, user_id=USER_A, client_id=CLIENT_X, raw_token="x1r")
        # A second, unrelated client for the SAME user — must survive untouched.
        await _seed_access_token(
            factory, user_id=USER_A, raw_token="z1", label=f"{OAUTH_LABEL_PREFIX}{CLIENT_Z}"
        )
        await _seed_refresh_token(factory, user_id=USER_A, client_id=CLIENT_Z, raw_token="z1r")

        resp = _client_as(USER_A).post(_revoke_path(CLIENT_X))
        assert resp.status_code == 200, resp.text
        assert resp.json() == {"revoked": True, "client_id": CLIENT_X}

        listing = _client_as(USER_A).get(LIST_PATH).json()
        by_client = {c["client_id"]: c for c in listing["oauth_connections"]}
        assert by_client[CLIENT_X]["active"] is False
        assert by_client[CLIENT_Z]["active"] is True

        # Direct DB check that BOTH families were stamped for CLIENT_X.
        async with factory() as session:
            from sqlalchemy import select

            access_rows = (
                (
                    await session.execute(
                        select(MCPAccessToken).where(
                            MCPAccessToken.user_id == USER_A,
                            MCPAccessToken.label == f"{OAUTH_LABEL_PREFIX}{CLIENT_X}",
                        )
                    )
                )
                .scalars()
                .all()
            )
            refresh_rows = (
                (
                    await session.execute(
                        select(MCPOAuthRefreshToken).where(
                            MCPOAuthRefreshToken.user_id == USER_A,
                            MCPOAuthRefreshToken.client_id == CLIENT_X,
                        )
                    )
                )
                .scalars()
                .all()
            )

        assert all(r.revoked_at is not None for r in access_rows)
        assert all(r.revoked_at is not None for r in refresh_rows)


class TestRevokeIsIdempotent:
    async def test_second_revoke_is_a_success_no_op(self, store):
        factory = store
        await _seed_access_token(
            factory, user_id=USER_A, raw_token="idem1", label=f"{OAUTH_LABEL_PREFIX}{CLIENT_X}"
        )
        await _seed_refresh_token(factory, user_id=USER_A, client_id=CLIENT_X, raw_token="idem1r")

        client = _client_as(USER_A)
        first = client.post(_revoke_path(CLIENT_X))
        second = client.post(_revoke_path(CLIENT_X))

        assert first.status_code == 200, first.text
        assert second.status_code == 200, second.text
        assert second.json() == {"revoked": True, "client_id": CLIENT_X}


class TestRevokeIsEffectiveImmediately:
    async def test_bearer_valid_before_revoke_refused_after(self, store):
        """END-TO-END: the same bearer `MCPTokenVerifier().verify_token`
        accepts before the revoke call resolves to None after it — pinning
        that this surface and unit 1's verifier agree on "revoked", not just
        that a `revoked_at` column got set somewhere."""
        factory = store
        raw_token = "mcp_e2e_for_1918"
        await _seed_access_token(
            factory, user_id=USER_A, raw_token=raw_token, label=f"{OAUTH_LABEL_PREFIX}{CLIENT_X}"
        )
        await _seed_refresh_token(factory, user_id=USER_A, client_id=CLIENT_X, raw_token="e2er")

        verifier = MCPTokenVerifier()  # default session_scope -> the monkeypatched one

        before = await verifier.verify_token(raw_token)
        assert before is not None
        assert before.client_id == str(USER_A)

        resp = _client_as(USER_A).post(_revoke_path(CLIENT_X))
        assert resp.status_code == 200, resp.text

        after = await verifier.verify_token(raw_token)
        assert after is None
