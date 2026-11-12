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
    monkeypatch.setattr(RedisFactory, "_last_ping_recorded_at", None)
    blacklist = TokenBlacklist(redis_factory=RedisFactory(), db_session_factory=None)
    monkeypatch.setattr(AuthContainer, "_token_blacklist", blacklist)

    async def no_ping(cls=None):
        raise AssertionError("/health took a Redis client; it must only read the record")

    monkeypatch.setattr(RedisFactory, "create_client", classmethod(no_ping))
    app = FastAPI()
    app.include_router(admin_router)
    app.state.intent_service = object()  # so only Redis can move the status below
    client = TestClient(app)
    return lambda: client.get("/health").json(), blacklist


def _record(monkeypatch, ok, age_s):
    """Set the pool's recorded ping: its outcome and how long ago it happened."""
    import time

    monkeypatch.setattr(RedisFactory, "_last_ping_ok", ok)
    monkeypatch.setattr(RedisFactory, "_last_ping_recorded_at", time.monotonic() - age_s)


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


def test_a_fresh_unavailable_degrades_the_status(health, monkeypatch):
    """Arch 2026-11-12: without Redis every page is a 503, so the host is down for users."""
    read, _ = health
    _record(monkeypatch, False, 5)
    body = read()
    assert body["services"]["redis"] == "unavailable"
    assert body["status"] == "degraded"
    assert 5 <= body["services"]["redis_checked_s"] < 30


def test_a_stale_unavailable_does_not_degrade_and_shows_its_age(health, monkeypatch):
    """On a host with no traffic an old failure must not hold promotions or keep alerting."""
    read, _ = health
    _record(monkeypatch, False, admin_module.REDIS_FRESH_SECONDS + 60)
    body = read()
    assert body["services"]["redis"] == "unavailable"
    assert body["status"] == "healthy"
    assert body["services"]["redis_checked_s"] >= admin_module.REDIS_FRESH_SECONDS + 60


def test_ok_is_healthy_and_no_ping_yet_is_healthy_with_a_null_age(health, monkeypatch):
    read, _ = health
    body = read()
    assert body["status"] == "healthy" and body["services"]["redis_checked_s"] is None
    _record(monkeypatch, True, 3)
    body = read()
    assert body["status"] == "healthy" and body["services"]["redis"] == "ok"


def test_the_http_code_is_200_whatever_redis_reads(health, monkeypatch):
    """Fly's machine check reads the code; a Redis outage must not restart the machine."""
    _record(monkeypatch, False, 1)
    app = FastAPI()
    app.include_router(admin_router)
    app.state.intent_service = object()
    response = TestClient(app).get("/health")
    assert response.status_code == 200 and response.json()["status"] == "degraded"


def test_the_window_is_120_seconds(health):
    assert admin_module.REDIS_FRESH_SECONDS == 120


def test_revocation_source_database_never_degrades(health, monkeypatch):
    read, blacklist = health
    _record(monkeypatch, True, 1)
    blacklist._redis_available = False
    body = read()
    assert body["services"]["revocation_source"] == "database" and body["status"] == "healthy"


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
