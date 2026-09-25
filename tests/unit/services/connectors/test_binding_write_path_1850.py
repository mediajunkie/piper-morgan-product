"""#1850 — write-time enforcement of ADR-070 Amendment A1/A3 on connector_bindings.

The gap: ``ConnectorBindingRepository.upsert`` wrote whatever ``mcp_server_ref`` a
caller passed, verbatim (no validation). Amendment A1 says a managed-connector
binding (``github``/``calendar``/``notion``/``slack``) stores the LOGICAL KEY, not a
topology; A3 carves out exactly one legitimate literal — a scheme-prefixed BYOC
override. Nothing enforced that shape at write time, so a droplet/Fly-hostname
literal for a managed connector would silently write through and reproduce the
2026-07-12 Fly-cutover incident (a binding that reads BOUND-and-healthy while
resolving against a host that no longer exists).

This suite exercises the write path DIRECTLY — a real ``ConnectorBindingRepository``
over an in-memory SQLite ``ConnectorBinding`` table, the same pattern
``test_binding_repository_1229.py`` uses — not just the validator in isolation, per
the issue's AC2 ("a regression test exercises the write path directly, not just the
resolver").
"""

from __future__ import annotations

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.connectors.binding_repository import ConnectorBindingRepository  # noqa: E402
from services.connectors.binding_write_guard import (  # noqa: E402
    ManagedConnectorRefRejected,
    validate_mcp_server_ref,
)
from services.database.models import ConnectorBinding  # noqa: E402

# pytest-asyncio mode is "auto" (pytest.ini) — async test functions are detected
# automatically; no module-level `pytestmark` here because TestValidatorUnit's
# tests below are synchronous and a blanket asyncio marker on them produces a
# PytestWarning (marked-but-not-a-coroutine).

_ALPHA = "11111111-1111-1111-1111-111111111111"

_MANAGED_KEYS = ("github", "calendar", "notion", "slack")

# A literal a caller might plausibly (and wrongly) pass for a managed connector —
# a droplet/Fly hostname with no scheme, exactly the #1278/#1850 failure shape.
_HOSTNAME_LITERAL = "piper-morgan-gh-mcp.internal:8082"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: ConnectorBinding.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


async def _get_ref(session, connector: str) -> str | None:
    row = await ConnectorBindingRepository(session).get(_ALPHA, connector)
    return row.mcp_server_ref if row else None


class TestWritePathRejectsLiteralsForManagedKeys:
    """AC1/AC2: a non-scheme-prefixed literal for a managed key is rejected at
    the write path, for each of the four managed connectors."""

    @pytest.mark.parametrize("connector", _MANAGED_KEYS)
    async def test_hostname_literal_rejected_for_each_managed_key(self, session, connector):
        repo = ConnectorBindingRepository(session)
        with pytest.raises(ManagedConnectorRefRejected) as exc_info:
            await repo.upsert(_ALPHA, connector, mcp_server_ref=_HOSTNAME_LITERAL, status="bound")
        # AC1: the error names the key it should have been.
        assert connector in str(exc_info.value)
        # AC1: nothing was written — the row either doesn't exist or wasn't mutated
        # to hold the rejected literal (the repository raises before flush commits
        # the bad value; a prior row, if any, must be untouched).
        assert await _get_ref(session, connector) != _HOSTNAME_LITERAL

    async def test_rejected_write_does_not_create_a_row(self, session):
        """A rejected write on a brand-new (owner, connector) pair must not leave
        a half-written row behind."""
        repo = ConnectorBindingRepository(session)
        with pytest.raises(ManagedConnectorRefRejected):
            await repo.upsert(_ALPHA, "github", mcp_server_ref=_HOSTNAME_LITERAL)
        # session was never committed; nothing should be flushed as a persisted row
        # reachable through a fresh get() in the same session either.
        assert await repo.get(_ALPHA, "github") is None

    async def test_rejected_write_does_not_clobber_an_existing_row(self, session):
        """A rejected write against an ALREADY-bound row must not leave that row
        mutated — the guard fires before any field assignment."""
        repo = ConnectorBindingRepository(session)
        await repo.upsert(_ALPHA, "calendar", mcp_server_ref="calendar", status="bound")
        await session.commit()
        with pytest.raises(ManagedConnectorRefRejected):
            await repo.upsert(_ALPHA, "calendar", mcp_server_ref=_HOSTNAME_LITERAL)
        row = await repo.get(_ALPHA, "calendar")
        assert row.mcp_server_ref == "calendar"
        assert row.status == "bound"


class TestWritePathAcceptsTheLogicalKey:
    """AC1: the key itself writes through unchanged, for each managed connector."""

    @pytest.mark.parametrize("connector", _MANAGED_KEYS)
    async def test_key_itself_writes_unchanged(self, session, connector):
        repo = ConnectorBindingRepository(session)
        await repo.upsert(_ALPHA, connector, mcp_server_ref=connector, status="bound")
        await session.commit()
        assert await _get_ref(session, connector) == connector


class TestWritePathAcceptsByocLiterals:
    """AC3: a genuine scheme-prefixed BYOC URL still writes through unchanged —
    existing A3 behavior is unaffected by the new enforcement."""

    @pytest.mark.parametrize("connector", _MANAGED_KEYS)
    async def test_scheme_prefixed_url_writes_unchanged(self, session, connector):
        repo = ConnectorBindingRepository(session)
        url = f"https://byoc.example.com/{connector}/mcp"
        await repo.upsert(_ALPHA, connector, mcp_server_ref=url, status="bound")
        await session.commit()
        assert await _get_ref(session, connector) == url

    async def test_http_scheme_also_accepted(self, session):
        repo = ConnectorBindingRepository(session)
        await repo.upsert(_ALPHA, "github", mcp_server_ref="http://byoc.local:9000/mcp")
        await session.commit()
        assert await _get_ref(session, "github") == "http://byoc.local:9000/mcp"


class TestWritePathIgnoresUnmanagedConnectors:
    """A connector outside the four managed keys is not this validator's concern —
    it passes through unvalidated (no enforcement claim is made about it)."""

    async def test_unmanaged_connector_literal_passes_through(self, session):
        repo = ConnectorBindingRepository(session)
        await repo.upsert(_ALPHA, "asana", mcp_server_ref="asana-box.example.internal")
        await session.commit()
        assert await _get_ref(session, "asana") == "asana-box.example.internal"

    async def test_none_ref_is_always_a_noop_for_validation(self, session):
        repo = ConnectorBindingRepository(session)
        row = await repo.upsert(_ALPHA, "github", status="unbound")
        await session.commit()
        assert row.mcp_server_ref is None


class TestValidatorUnit:
    """The validator function itself, over a table of edge forms."""

    @pytest.mark.parametrize(
        "connector,ref,should_reject",
        [
            # Bare hostname/IP/path literals for a managed key: REJECTED.
            ("github", "piper-morgan-gh-mcp.internal", True),
            ("github", "localhost:8001", True),
            ("github", "192.168.1.50:8082", True),
            ("github", "192.168.1.50:8082/mcp", True),
            ("calendar", "gcal-mcp-server", True),
            ("notion", "notion-box.internal", True),
            ("slack", "10.0.0.4", True),
            # Case: 'GITHUB' is not the exact key 'github' — a caller typo, not a
            # scheme-prefixed BYOC literal either. #1850 rules reject (not a
            # silent case-fold), same as any other non-matching literal.
            ("github", "GITHUB", True),
            # The logical key itself, exactly: accepted.
            ("github", "github", False),
            ("calendar", "calendar", False),
            ("notion", "notion", False),
            ("slack", "slack", False),
            # Whitespace around the exact key: accepted (resolve_server_ref itself
            # strips whitespace — the validator mirrors that, not a new leniency).
            ("github", "  github  ", False),
            # http/https BYOC literals: accepted regardless of connector.
            ("github", "http://srv.example.com/mcp", False),
            ("github", "https://srv.example.com/mcp", False),
            ("calendar", "https://cal.example.com/mcp", False),
            # Empty / whitespace-only / None: no-op (nothing to validate).
            ("github", "", False),
            ("github", "   ", False),
            ("github", None, False),
            # A connector outside the managed set: never rejected here.
            ("asana", "asana-box.internal", False),
            ("asana", "anything at all", False),
        ],
    )
    def test_validate_mcp_server_ref_table(self, connector, ref, should_reject):
        if should_reject:
            with pytest.raises(ManagedConnectorRefRejected):
                validate_mcp_server_ref(connector, ref)
        else:
            validate_mcp_server_ref(connector, ref)  # must not raise

    def test_error_names_the_expected_key(self):
        with pytest.raises(ManagedConnectorRefRejected) as exc_info:
            validate_mcp_server_ref("slack", "slack-mcp-box.fly.dev")
        message = str(exc_info.value)
        assert "slack" in message
        assert "slack-mcp-box.fly.dev" in message
