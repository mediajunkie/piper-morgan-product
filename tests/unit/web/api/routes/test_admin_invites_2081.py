"""#2081 — the admin Invites API: mint (raw codes once), list (masked), revoke.

HOST's rulings (issue comment, 2026-10-18): admin only via the real
``require_admin`` (the DB read patched at its one-line boundary, the
refuse/allow logic runs for real); raw codes only in the mint response with
no-store; N bounded 1..20 per request and 20 per UTC day; the list shows masked
forms and a revoked code as its own status, never a redemption; one audit row
per mint and revoke with masked forms only.

Layer: the route coroutines called directly against an in-memory SQLite
database holding the real ``invite_tokens`` and ``users`` tables (the audit
writer is recorded at its boundary: ``audit_logs`` uses a Postgres UUID column
type SQLite cannot create). The admin gate is exercised through a TestClient
on the real router, where the refusal happens before any database read, so the
sync client and the async database never share a loop.
"""

from __future__ import annotations

import contextlib
import uuid
from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest
import pytest_asyncio
from fastapi import FastAPI, HTTPException, Response
from fastapi.testclient import TestClient
from pydantic import ValidationError
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from services.auth import invite_admin_service as svc
from services.auth.auth_middleware import get_current_user
from services.database.models import InviteToken
from tests.utils.made_up_credentials import invite_code
from web.api.routes import admin_invites as api

ADMIN_ID = uuid.uuid4()
NON_ADMIN_ID = uuid.uuid4()
ADMIN = SimpleNamespace(user_id=ADMIN_ID, sub=str(ADMIN_ID))


@pytest_asyncio.fixture
async def db(monkeypatch):
    """The real ``invite_tokens`` table plus a two-column ``users`` stand-in
    (the full User model carries Postgres-only column types SQLite cannot
    create; the service reads only ``users.id`` and ``users.username``)."""
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    try:
        async with engine.begin() as conn:
            await conn.execute(
                text("CREATE TABLE users (id CHAR(36) PRIMARY KEY, username VARCHAR(100))")
            )
            await conn.run_sync(lambda c: InviteToken.__table__.create(c, checkfirst=True))
        maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

        @contextlib.asynccontextmanager
        async def _scope():
            async with maker() as s:
                yield s
                await s.commit()

        import services.database.session_factory as sf

        monkeypatch.setattr(sf.AsyncSessionFactory, "session_scope", staticmethod(_scope))
        yield maker
    finally:
        await engine.dispose()


@pytest.fixture
def audit(monkeypatch):
    calls: list = []

    async def _record(session, *, actor_user_id, action, message, masked):
        calls.append({"actor": str(actor_user_id), "action": action, "masked": list(masked)})

    monkeypatch.setattr(svc, "_write_audit", _record)
    return calls


async def _rows(maker):
    async with maker() as s:
        return (await s.execute(select(InviteToken))).scalars().all()


async def _seed(maker, *tokens):
    async with maker() as s:
        for t in tokens:
            s.add(t)
        await s.commit()


# ---- admin only (through the real dependency, before any DB read) -----------


def test_non_admin_is_refused_on_every_route():
    app = FastAPI()
    app.include_router(api.router)
    claims = MagicMock()
    claims.user_id = NON_ADMIN_ID
    claims.sub = str(NON_ADMIN_ID)
    app.dependency_overrides[get_current_user] = lambda: claims

    async def fake(user_id):
        return False

    with patch("services.auth.auth_middleware._user_is_admin", side_effect=fake):
        c = TestClient(app, raise_server_exceptions=False)
        assert c.get("/api/v1/admin/invites").status_code == 403
        assert c.post("/api/v1/admin/invites", json={"count": 1}).status_code == 403
        assert c.post("/api/v1/admin/invites/ABCD…WXYZ/revoke").status_code == 403


# ---- mint -------------------------------------------------------------------


@pytest.mark.asyncio
async def test_mint_returns_raw_codes_once_with_no_store_and_audits_masked_only(db, audit):
    response = Response()
    out = await api.mint_invite_codes(api.MintRequest(count=3), response, ADMIN)
    assert response.headers["cache-control"] == "no-store"
    assert len(out.codes) == 3 and all(len(code) == 24 for code in out.codes)
    assert out.masked == [svc.mask(code) for code in out.codes]
    assert out.minted_today == 3 and out.daily_limit == 20
    rows = await _rows(db)
    assert sorted(t.token for t in rows) == sorted(out.codes)
    assert audit == [{"actor": str(ADMIN_ID), "action": "invite_mint", "masked": out.masked}]
    for code in out.codes:
        assert code not in str(audit)
    # No later read returns a raw code.
    listing = await api.list_invite_codes(Response(), ADMIN)
    assert listing.minted_today == 3
    for code in out.codes:
        assert code not in listing.model_dump_json()


@pytest.mark.parametrize("count", [0, 21, -1])
def test_mint_count_bounds(count):
    with pytest.raises(ValidationError):
        api.MintRequest(count=count)


@pytest.mark.asyncio
async def test_mint_daily_cap_refuses_before_writing(db, audit):
    await api.mint_invite_codes(api.MintRequest(count=20), Response(), ADMIN)
    with pytest.raises(HTTPException) as exc:
        await api.mint_invite_codes(api.MintRequest(count=1), Response(), ADMIN)
    assert exc.value.status_code == 429
    assert "20 of 20" in exc.value.detail
    assert len(await _rows(db)) == 20
    assert len(audit) == 1


# ---- list -------------------------------------------------------------------


@pytest.mark.asyncio
async def test_list_shows_masked_forms_and_distinguishes_redeemed_from_revoked(db, audit):
    tester_id = uuid.uuid4()
    now = datetime.now(timezone.utc)
    async with db() as s:
        await s.execute(
            text("INSERT INTO users (id, username) VALUES (:id, :name)"),
            {"id": str(tester_id), "name": "alpha-tester-1"},
        )
        await s.commit()
    await _seed(
        db,
        InviteToken(token="AAAA0000000000000000ZZZZ"),
        InviteToken(token="BBBB1111111111111111YYYY", used_at=now, used_by_user_id=tester_id),
        InviteToken(token="CCCC2222222222222222XXXX", used_at=now, used_by_user_id=None),
    )
    body = await api.list_invite_codes(Response(), ADMIN)
    by_mask = {row.masked: row for row in body.invites}
    assert set(by_mask) == {"AAAA…ZZZZ", "BBBB…YYYY", "CCCC…XXXX"}
    assert by_mask["AAAA…ZZZZ"].status == "unused" and by_mask["AAAA…ZZZZ"].used_by is None
    assert by_mask["BBBB…YYYY"].status == "redeemed"
    assert by_mask["BBBB…YYYY"].used_by == "alpha-tester-1"
    assert by_mask["CCCC…XXXX"].status == "revoked" and by_mask["CCCC…XXXX"].used_by is None
    assert "AAAA0000000000000000ZZZZ" not in body.model_dump_json()


# ---- revoke -----------------------------------------------------------------


@pytest.mark.asyncio
async def test_revoke_marks_an_unused_code_as_revoked_not_redeemed(db, audit):
    await _seed(db, InviteToken(token="DDDD3333333333333333WWWW"))
    out = await api.revoke_invite_code("DDDD…WWWW", ADMIN)
    assert out["revoked"] == "DDDD…WWWW"
    rows = await _rows(db)
    assert rows[0].used_at is not None and rows[0].used_by_user_id is None
    assert audit[-1] == {"actor": str(ADMIN_ID), "action": "invite_revoke", "masked": ["DDDD…WWWW"]}
    listing = await api.list_invite_codes(Response(), ADMIN)
    assert listing.invites[0].status == "revoked"


@pytest.mark.asyncio
async def test_revoke_refusals_not_found_ambiguous_already_used(db, audit):
    now = datetime.now(timezone.utc)
    await _seed(
        db,
        InviteToken(token="EEEE4444444444444444VVVV"),
        InviteToken(token="EEEE5555555555555555VVVV"),
        InviteToken(token="FFFF6666666666666666TTTT", used_at=now, used_by_user_id=None),
    )

    async def _status(masked):
        with pytest.raises(HTTPException) as exc:
            await api.revoke_invite_code(masked, ADMIN)
        return exc.value.status_code, exc.value.detail

    assert (await _status("GGGG…HHHH"))[0] == 404
    code, detail = await _status("EEEE…VVVV")
    assert code == 409 and "More than one" in detail
    code, detail = await _status("FFFF…TTTT")
    assert code == 409 and "already revoked" in detail
    assert (await _status("not-a-mask"))[0] == 422
    assert audit == []
    rows = await _rows(db)
    assert sum(1 for t in rows if t.used_at is None) == 2


def test_mask_shape():
    code = invite_code("mask shape")
    assert svc.mask(code) == f"{code[:4]}…{code[-4:]}"
    assert svc.mask("short") == "…"


@pytest.mark.asyncio
async def test_list_is_no_store_so_a_refetch_after_mint_or_revoke_is_never_stale(db, audit):
    """xian's D5 read (2026-10-19): the page re-fetched the list after a mint and after
    a revoke and still showed the old rows until a manual reload. The list carries
    no-store, the same as the mint response."""
    response = Response()
    await api.list_invite_codes(response, ADMIN)
    assert response.headers["cache-control"] == "no-store"
