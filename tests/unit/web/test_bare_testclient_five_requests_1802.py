"""#1802 — a bare `TestClient` gets one authenticated request, not five.

Split out of #1792. #1792 fixed the MESSAGE an unreachable blacklist store
produces (401 "Token has been revoked" -> 503 "couldn't verify"). It did not
fix the reason the store becomes unreachable in a bare `TestClient` at all,
so the practical symptom for test authors survived the fix, just reworded:

    before #1792:  200, 401, 401, 401, 401   ("Token has been revoked")
    after  #1792:  200, 503, 503, 503, 503   ("Couldn't verify your session")
    after  #1802:  200, 200, 200, 200, 200   (this file)

ROOT CAUSE, two layers, both distinct from #1792:

1. A bare `TestClient` never runs the app's startup lifespan, so
   `TokenBlacklist.initialize()` is never called and `_redis_available`
   stays at its `False` default. Every check falls through to
   `_check_database` regardless of whether Redis is actually reachable.
2. `_check_database` used to open its session via `AsyncSessionFactory
   .session_scope()`, which draws from the global `db` singleton
   (services/database/connection.py). That engine binds to whichever event
   loop happens to be running the first time it is lazily created. A bare
   `TestClient` spins a fresh event loop per request, so from request 2
   onward the pooled asyncpg connection belongs to a loop that no longer
   exists: "Task ... got Future ... attached to a different loop", then
   "asyncpg.InterfaceError: cannot perform operation: another operation is
   in progress" (verbatim, reproduced by hand before this fix landed).

THE FIX (this issue): `_check_database` now uses `session_scope_fresh()`
instead — a per-call engine bound to whatever loop is CURRENTLY running.
This is #442's documented manual opt-in for exactly this failure class, the
database-side twin of the same-loop guard #1452 already gave
`RedisFactory.initialize` on the Redis side.

WHY THIS FILE DOES NOT JUST CALL `AsyncSessionFactory()` DIRECTLY (m-43,
"name the layer"). `tests/conftest.py` carries its own autouse fixture,
`_1452_session_scope_nullpool`, that globally monkeypatches
`AsyncSessionFactory.session_scope` to a NullPool-backed engine for EVERY
test in the suite — a deliberate, correctly-motivated cure for the same
poisoned-pool pathology, applied so other tests don't trip over it by
accident. Its side effect for THIS file: under the patched `session_scope`,
the original bug (`_check_database` calling `session_scope()`) does not
reproduce inside the suite either, because NullPool means no connection is
ever held across a checkout for a stale loop to poison. A regression test
built on the patched method would pass identically whether `_check_database`
called `session_scope` or `session_scope_fresh` — it would not have caught
the bug, and it would not catch a future regression back to `session_scope`.

So this file constructs its own `db_session_factory` stand-in,
`_RealSessionSemantics`, that reproduces the two REAL, UNPATCHED production
strategies directly: `.session_scope()` draws from the real global `db`
singleton (services/database/connection.py, never touched by the conftest
patch — only `AsyncSessionFactory.session_scope` is patched, not `db`
itself) exactly as the pre-#1802 code did; `.session_scope_fresh()` IS the
real, untouched `AsyncSessionFactory.session_scope_fresh` (the conftest
comment says as much: "session_scope_fresh is untouched"). Swapping which of
the two `_check_database` calls is exactly the fix under test, verified by
hand: with `.session_scope` wired in, this suite's own five-request test
reproduces 503 from request 2 onward; with `.session_scope_fresh` (the
shipped fix), all five succeed.

LAYER (m-43), continued. Every other part of the stack is the real thing: a
real `AuthMiddleware`, real `JWTService`, real `TokenBlacklist`, the real
test Postgres instance (port 5433, see tests/conftest.py defaults). Only the
one attribute the suite-wide fixture would otherwise mask is reconstructed
to its real, unpatched behavior.

THE PIN IS THE SEQUENCE (per the issue's own AC). A single-request test
passes today and always has — request 1 never touches a stale connection
because nothing stale exists yet. The defect only shows up from request 2
onward, so the assertion must walk all five requests, not sample one.

`@pytest.mark.integration` carries no special requirement in this file
beyond opting OUT of conftest.py's autouse `mock_token_blacklist` fixture,
which pins `TokenBlacklist.is_blacklisted` to `False` for ordinary unit
tests — the very method this file exercises for real.
"""

import uuid
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.auth_middleware import AuthMiddleware
from services.auth.jwt_service import JWTService
from services.auth.token_blacklist import TokenBlacklist
from services.cache.redis_factory import RedisFactory
from services.database.session_factory import AsyncSessionFactory

PROBE_PATH = "/api/v1/probe-1802"
SECRET = "test-secret-1802-not-a-real-key-0123456789"


class _RealSessionSemantics:
    """Stands in for `AsyncSessionFactory` with the two real, UNPATCHED
    production strategies (see module docstring for why this file can't just
    use `AsyncSessionFactory` — the suite's conftest.py monkeypatches its
    `session_scope` for every OTHER test's benefit, which would mask the
    exact defect this file exists to pin).

    `.session_scope()` mirrors the real pre-#1802 `_check_database`: it
    draws from the real global `db` singleton, so its engine binds to
    whichever loop is running the first time it's lazily created — the
    actual pathology. `.session_scope_fresh()` IS the real, untouched
    `AsyncSessionFactory.session_scope_fresh` (a per-call fresh engine,
    #442) — the method the fix switched `_check_database` to.
    """

    @staticmethod
    @asynccontextmanager
    async def session_scope():
        from services.database.connection import db

        session = await db.get_session()
        try:
            yield session
            await session.commit()
        except Exception:
            try:
                await session.rollback()
            except Exception:
                pass
            raise
        finally:
            try:
                await session.close()
            except Exception:
                pass

    session_scope_fresh = staticmethod(AsyncSessionFactory.session_scope_fresh)


def _real_blacklist_never_initialized() -> TokenBlacklist:
    """Real Redis factory + real (unpatched) DB session semantics.
    `.initialize()` is deliberately never called, so `_redis_available`
    stays False — exactly what happens under a bare `TestClient` that skips
    the app's startup lifespan. Every check therefore falls through to
    `_check_database` against the real test Postgres instance.
    """
    return TokenBlacklist(RedisFactory(), _RealSessionSemantics())


def _bare_client_and_jwt_service() -> tuple[TestClient, JWTService]:
    """A bare `TestClient` — no `with` block, so no lifespan runs and each
    dispatched request gets its own fresh event loop (the actual mechanism
    behind the reproduced signature)."""
    blacklist = _real_blacklist_never_initialized()
    jwt_service = JWTService(secret_key=SECRET, blacklist=blacklist)
    app = FastAPI()

    @app.get(PROBE_PATH)
    async def probe():  # pragma: no cover - reached only when auth ALLOWS
        return {"reached_the_route": True}

    app.add_middleware(AuthMiddleware, jwt_service=jwt_service)
    return TestClient(app, raise_server_exceptions=False), jwt_service


def _fresh_token(jwt_service: JWTService) -> str:
    """A freshly minted, valid, never-revoked token — brand-new `jti` every
    call, so a real blacklist hit is never a possible explanation for a
    refusal."""
    user_id = uuid.uuid4()
    return jwt_service.generate_access_token(
        user_id=user_id,
        user_email=f"{user_id}@example.com",
        scopes=["user"],
    )


@pytest.mark.integration
class TestBareTestClientSequentialAuth:
    """An authenticated `TestClient` sequence behaves the same on request 5
    as on request 1 — auth is not a confound in tests that make more than
    one authenticated call."""

    @pytest.mark.smoke
    def test_five_sequential_authenticated_requests_all_succeed(self):
        """THE symptom, pinned as the sequence (not a single-request sample).

        Pre-#1802: [200, 503, 503, 503, 503] — 503 "Couldn't verify your
        session right now" from request 2 onward, `_check_database` binding
        to a dead event loop. Post-#1802: all five succeed.
        """
        client, jwt_service = _bare_client_and_jwt_service()

        statuses = []
        bodies = []
        for _ in range(5):
            token = _fresh_token(jwt_service)
            response = client.get(PROBE_PATH, headers={"Authorization": f"Bearer {token}"})
            statuses.append(response.status_code)
            bodies.append(response.text)

        assert statuses == [200, 200, 200, 200, 200], (
            f"a bare TestClient must authenticate every request, not just the "
            f"first: got {statuses}, bodies={bodies}"
        )
        for body in bodies:
            assert "reached_the_route" in body

    @pytest.mark.smoke
    def test_never_initialized_fallback_is_logged_not_silent(self):
        """#1802 AC item 2: `_redis_available = False` must stop being
        reachable silently. A blacklist that never initialized must not look
        identical, in the logs, to one that initialized and found no Redis.

        This does not change which branch is taken (still database
        fallback either way) — only whether an operator can tell why.
        """
        import structlog

        client, jwt_service = _bare_client_and_jwt_service()
        token = _fresh_token(jwt_service)

        with structlog.testing.capture_logs() as cap:
            response = client.get(PROBE_PATH, headers={"Authorization": f"Bearer {token}"})

        assert response.status_code == 200
        assert any(e.get("event") == "token_blacklist_never_initialized" for e in cap), (
            "expected a loud, distinguishable log line when the blacklist "
            f"falls back to the database having never called initialize(); "
            f"captured events: {[e.get('event') for e in cap]}"
        )
