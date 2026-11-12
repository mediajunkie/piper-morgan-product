"""#2348 (Arch's shape, 2026-11-12): /health reports Redis from the RECORDED ping and
the store this process checks revoked tokens in. It never pings, and no part of the
Redis address reaches the body."""

from __future__ import annotations

from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

import web.api.routes.admin as admin_module
from services.auth.container import AuthContainer
from services.auth.token_blacklist import TokenBlacklist
from services.cache.redis_factory import RedisFactory
from services.infrastructure import turn_activity
from web.api.routes.admin import router as admin_router

ADDRESS = "redis://default:made-up-word@fly-example-db.upstash.io:6379"


class _FakeConnection:
    async def execute(self, _statement):
        return None


class _FakeEngine:
    @asynccontextmanager
    async def connect(self):
        yield _FakeConnection()

    async def dispose(self):
        return None


@pytest.fixture
def health(monkeypatch):
    monkeypatch.setattr(admin_module, "create_async_engine", lambda *a, **k: _FakeEngine())
    monkeypatch.setenv("DATABASE_URL", "postgresql://piper:pw@db-x.flycast:5432/piper")
    monkeypatch.setenv("REDIS_URL", ADDRESS)
    monkeypatch.setattr(turn_activity, "TURN_ACTIVITY", turn_activity.TurnActivity())
    monkeypatch.setattr(RedisFactory, "_last_ping_ok", None)
    blacklist = TokenBlacklist(redis_factory=RedisFactory(), db_session_factory=None)
    monkeypatch.setattr(AuthContainer, "_token_blacklist", blacklist)

    async def no_ping(cls=None):
        raise AssertionError("/health took a Redis client; it must only read the record")

    monkeypatch.setattr(RedisFactory, "create_client", classmethod(no_ping))
    app = FastAPI()
    app.include_router(admin_router)
    client = TestClient(app)
    return lambda: client.get("/health").json(), blacklist


def test_no_ping_yet_reads_unavailable_and_database(health):
    read, _ = health
    services = read()["services"]
    assert services["redis"] == "unavailable"
    assert services["revocation_source"] == "database"


def test_a_recorded_good_ping_reads_ok(health, monkeypatch):
    read, blacklist = health
    monkeypatch.setattr(RedisFactory, "_last_ping_ok", True)
    blacklist._redis_available = True
    services = read()["services"]
    assert services["redis"] == "ok"
    assert services["revocation_source"] == "redis"


def test_a_recorded_failed_ping_reads_unavailable(health, monkeypatch):
    read, _ = health
    monkeypatch.setattr(RedisFactory, "_last_ping_ok", False)
    assert read()["services"]["redis"] == "unavailable"


def test_the_two_fields_are_independent(health, monkeypatch):
    """A process that started with Redis down stays on the database after Redis returns."""
    read, blacklist = health
    monkeypatch.setattr(RedisFactory, "_last_ping_ok", True)
    blacklist._redis_available = False
    services = read()["services"]
    assert (services["redis"], services["revocation_source"]) == ("ok", "database")


def test_neither_field_changes_the_overall_status(health, monkeypatch):
    read, _ = health
    before = read()["status"]
    monkeypatch.setattr(RedisFactory, "_last_ping_ok", False)
    assert read()["status"] == before


def test_no_part_of_the_address_reaches_the_body(health, monkeypatch):
    read, _ = health
    monkeypatch.setattr(RedisFactory, "_last_ping_ok", True)
    body = str(read())
    for part in ("made-up-word", "upstash", "6379", "redis://", "default:"):
        assert part not in body


def test_only_the_two_ruled_values_are_ever_served(health, monkeypatch):
    read, _ = health
    seen = set()
    for state in (None, True, False):
        monkeypatch.setattr(RedisFactory, "_last_ping_ok", state)
        seen.add(read()["services"]["redis"])
    assert seen == {"ok", "unavailable"}


@pytest.mark.asyncio
async def test_the_pool_records_each_ping_outcome(monkeypatch):
    """The record /health reads is written by the pool's own health ping."""

    class _Client:
        def __init__(self, ok):
            self.ok = ok

        async def ping(self):
            if not self.ok:
                raise ConnectionError("refused")

    async def no_init(cls=None):
        return None

    monkeypatch.setattr(RedisFactory, "initialize", classmethod(no_init))
    for ok, expected in ((True, "ok"), (False, "unavailable")):
        monkeypatch.setattr(RedisFactory, "_last_health_ping", None)
        monkeypatch.setattr(RedisFactory, "_last_ping_ok", None)
        monkeypatch.setattr("services.cache.redis_factory.redis.Redis", lambda **k: _Client(ok))
        await RedisFactory.create_client()
        assert RedisFactory.recorded_health() == expected
