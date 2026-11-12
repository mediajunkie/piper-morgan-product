"""#2342 (ADR-081 D3): the cutover's data step (``services/connectors/github_app_cutover``).

Arch's rulings: it selects by grant, not by status; revokes, marks STALE with
``cutover`` and deletes the token; is idempotent; is a dry run by default; never touches
``connector_configs``; refuses to apply unless App mode is on.

Layer: unit. Real ``connector_bindings`` and ``connector_configs`` tables (in-memory
SQLite); the grant store and GitHub's revoke are fakes. No value here is token-shaped.
"""

from __future__ import annotations

import contextlib

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors import github_app_cutover as cut  # noqa: E402
from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.database.models import ConnectorBinding, ConnectorConfig  # noqa: E402
from services.mcp.consumer import github_app_grant as grant_mod  # noqa: E402
from services.mcp.consumer.connector import ConnectorStatusState  # noqa: E402
from services.mcp.consumer.github_app_grant import REASON_CUTOVER, GitHubAppGrant  # noqa: E402

pytestmark = pytest.mark.asyncio

_A = "11111111-1111-1111-1111-111111111111"
_B = "22222222-2222-2222-2222-222222222222"
_C = "33333333-3333-3333-3333-333333333333"
_D = "44444444-4444-4444-4444-444444444444"
_APP_RECORD = GitHubAppGrant("access-app", 2_000_000_000, "refresh-app", 2_100_000_000).encode()


class _Grants:
    values: dict = {}
    deleted: list = []

    async def get_encrypted_strict(self, session, user_id, connector):
        value = _Grants.values.get(str(user_id))
        if isinstance(value, Exception):
            raise value
        return value

    async def delete(self, session, user_id, connector):
        if str(user_id) not in _Grants.values:
            return False
        del _Grants.values[str(user_id)]
        _Grants.deleted.append(str(user_id))
        return True


class _Revoker:
    def __init__(self, fail_for=()):
        self.calls = []
        self.fail_for = set(fail_for)

    async def revoke_grant(self, token):
        self.calls.append(token)
        return token not in self.fail_for


@pytest_asyncio.fixture
async def world(monkeypatch):
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
        await conn.run_sync(lambda c: ConnectorConfig.__table__.create(c, checkfirst=True))
    sm = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    @contextlib.asynccontextmanager
    async def _scope():
        async with sm() as s:
            yield s
            await s.commit()

    monkeypatch.setattr(cut.AsyncSessionFactory, "session_scope", staticmethod(_scope))
    _Grants.values, _Grants.deleted = {}, []
    monkeypatch.setattr(cut, "ConnectorGrantStore", _Grants)

    async def _owners():
        return list(_Grants.values)

    monkeypatch.setattr(cut, "_grant_owner_ids", _owners)
    revoker = _Revoker()
    monkeypatch.setattr(cut, "_classic_handler", lambda: revoker)
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_ID, "app-client-id")
    monkeypatch.setenv(grant_mod.ENV_APP_CLIENT_SECRET, "app-client-secret")
    yield sm, revoker
    await engine.dispose()


async def _bind(sm, owner, status=ConnectorStatusState.BOUND.value, reason=None):
    async with sm() as s:
        repo = ConnectorBindingRepository(s)
        await repo.upsert(owner, "github", status=status, mcp_server_ref="github")
        if reason:
            await repo.set_status(owner, "github", status, reason=reason)
        await s.commit()


async def _binding(sm, owner):
    async with sm() as s:
        return await ConnectorBindingRepository(s).get(owner, "github")


async def _configs(sm):
    async with sm() as s:
        rows = (await s.execute(select(ConnectorConfig))).scalars().all()
        return sorted(
            (str(r.id), str(r.owner_id), r.connector, repr(r.config), str(r.updated_at))
            for r in rows
        )


async def _seed_three(sm):
    """A: classic and BOUND. B: classic and already marked by the resolver. C: a GitHub
    App grant. D: classic with an UNBOUND binding."""
    await _bind(sm, _A)
    await _bind(sm, _B, ConnectorStatusState.STALE.value, REASON_CUTOVER)
    await _bind(sm, _C)
    await _bind(sm, _D, ConnectorStatusState.UNBOUND.value)
    _Grants.values = {_A: "classic-a", _B: "classic-b", _C: _APP_RECORD, _D: "classic-d"}


class TestDryRun:
    async def test_the_default_changes_nothing_and_counts_what_it_would_do(self, world):
        sm, revoker = world
        await _seed_three(sm)
        counts = await cut.run_cutover()
        assert counts == {
            "seen": 3,
            "marked": 1,
            "already_marked": 1,
            "deleted": 0,
            "revoke_ok": 0,
            "revoke_failed": 0,
            "app_grants": 1,
            "unreadable": 0,
        }
        assert revoker.calls == [] and _Grants.deleted == []
        assert (await _binding(sm, _A)).status == ConnectorStatusState.BOUND.value
        assert "DRY RUN" in cut.format_counts(counts, applied=False)


class TestApply:
    async def test_every_classic_grant_ends_stale_with_its_token_deleted(self, world):
        sm, revoker = world
        await _seed_three(sm)
        counts = await cut.run_cutover(apply=True)
        assert counts == {
            "seen": 3,
            "marked": 1,
            "already_marked": 1,
            "deleted": 3,
            "revoke_ok": 3,
            "revoke_failed": 0,
            "app_grants": 1,
            "unreadable": 0,
        }
        for owner in (_A, _B):
            row = await _binding(sm, owner)
            assert row.status == ConnectorStatusState.STALE.value
            assert row.status_reason == REASON_CUTOVER
        assert sorted(revoker.calls) == ["classic-a", "classic-b", "classic-d"]
        assert sorted(_Grants.deleted) == [_A, _B, _D]
        assert set(_Grants.values) == {_C}  # the App grant is left alone

    async def test_selection_is_by_grant_so_a_binding_already_marked_still_loses_its_token(
        self, world
    ):
        sm, revoker = world
        await _bind(sm, _B, ConnectorStatusState.STALE.value, REASON_CUTOVER)
        _Grants.values = {_B: "classic-b"}
        counts = await cut.run_cutover(apply=True)
        assert counts["already_marked"] == 1 and counts["deleted"] == 1
        assert revoker.calls == ["classic-b"]

    async def test_an_unbound_row_is_never_resurrected(self, world):
        sm, _ = world
        await _seed_three(sm)
        await cut.run_cutover(apply=True)
        row = await _binding(sm, _D)
        assert row.status == ConnectorStatusState.UNBOUND.value and row.status_reason is None

    async def test_a_github_app_connection_is_untouched(self, world):
        sm, revoker = world
        await _seed_three(sm)
        await cut.run_cutover(apply=True)
        row = await _binding(sm, _C)
        assert row.status == ConnectorStatusState.BOUND.value and row.status_reason is None
        assert _Grants.values[_C] == _APP_RECORD and "access-app" not in revoker.calls

    async def test_a_failed_revoke_is_counted_and_does_not_block(self, world, monkeypatch):
        sm, _ = world
        await _seed_three(sm)
        revoker = _Revoker(fail_for={"classic-a"})
        monkeypatch.setattr(cut, "_classic_handler", lambda: revoker)
        counts = await cut.run_cutover(apply=True)
        assert counts["revoke_failed"] == 1 and counts["revoke_ok"] == 2
        assert counts["deleted"] == 3  # the token is deleted here all the same
        assert (await _binding(sm, _A)).status_reason == REASON_CUTOVER

    async def test_a_second_run_finds_nothing(self, world):
        sm, revoker = world
        await _seed_three(sm)
        await cut.run_cutover(apply=True)
        revoker.calls.clear()
        again = await cut.run_cutover(apply=True)
        assert again["seen"] == 0 and again["deleted"] == 0 and again["marked"] == 0
        assert again["app_grants"] == 1 and revoker.calls == []

    async def test_a_damaged_or_unreadable_row_is_left_alone_and_counted(self, world):
        sm, revoker = world
        await _bind(sm, _A)
        await _bind(sm, _B)
        _Grants.values = {_A: '{"minted_by":"github_app"', _B: RuntimeError("decrypt failed")}
        counts = await cut.run_cutover(apply=True)
        assert counts["unreadable"] == 2 and counts["seen"] == 0
        assert revoker.calls == [] and _Grants.deleted == []
        assert (await _binding(sm, _A)).status == ConnectorStatusState.BOUND.value

    async def test_an_app_record_that_lost_its_marker_is_never_deleted(self, world):
        # Arch 2026-11-12 07:24: a JSON object without the marker is damage, not a
        # classic grant. The script counts it and leaves it alone.
        sm, revoker = world
        await _bind(sm, _A)
        _Grants.values = {_A: '{"access_token":"access-app","refresh_token":"refresh-app"}'}
        counts = await cut.run_cutover(apply=True)
        assert counts["unreadable"] == 1 and counts["seen"] == 0 and counts["deleted"] == 0
        assert revoker.calls == [] and _A in _Grants.values
        assert (await _binding(sm, _A)).status == ConnectorStatusState.BOUND.value

    async def test_saved_repository_choices_are_byte_identical_afterwards(self, world):
        sm, _ = world
        await _seed_three(sm)
        async with sm() as s:
            s.add(
                ConnectorConfig(
                    owner_id=_A,
                    connector="github",
                    config={"default_repo": "owner/name", "selected": ["owner/name", "o/other"]},
                )
            )
            s.add(ConnectorConfig(owner_id=_B, connector="github", config={"selected": []}))
            await s.commit()
        before = await _configs(sm)
        assert len(before) == 2
        await cut.run_cutover(apply=True)
        assert await _configs(sm) == before


class TestRefusal:
    async def test_apply_is_refused_with_app_mode_off_and_nothing_changes(self, world, monkeypatch):
        sm, revoker = world
        await _seed_three(sm)
        monkeypatch.delenv(grant_mod.ENV_APP_CLIENT_SECRET)
        with pytest.raises(cut.CutoverRefused):
            await cut.run_cutover(apply=True)
        assert revoker.calls == [] and _Grants.deleted == []
        assert (await _binding(sm, _A)).status == ConnectorStatusState.BOUND.value

    async def test_a_dry_run_is_allowed_with_app_mode_off(self, world, monkeypatch):
        sm, _ = world
        await _seed_three(sm)
        monkeypatch.delenv(grant_mod.ENV_APP_CLIENT_ID)
        assert (await cut.run_cutover())["seen"] == 3


class TestScriptOutput:
    async def test_the_printed_lines_carry_counts_only(self, world):
        sm, _ = world
        await _seed_three(sm)
        counts = await cut.run_cutover(apply=True)
        shown = cut.format_counts(counts, applied=True)
        assert "APPLIED" in shown
        for secret in ("classic-a", "classic-b", "access-app", _A, _B):
            assert secret not in shown
