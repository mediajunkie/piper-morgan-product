"""#1430 (F19, census 2026-07-16) — learning dashboard controls bind the real principal.

Before: the dashboard's Export / Clear buttons fetched the Sprint A5
`/controls/export` and `/controls/data/clear` routes with a client-supplied
`user_id='current_user'`. Those routes were decorator-commented in the #300
deprecation (Nov 2025), so the buttons 404'd — and the deprecated handlers
they pointed at trusted a raw client `user_id` with no auth binding.

Now: production routes anchored to the authenticated principal
(`current_user.user_id` via `Depends(get_current_user)`, the #1250/#1252
idiom already used by `/settings` and `/patterns`). Client-supplied user_id
is ignored (not a declared parameter).

Beta-scope cross-user-leakage class (#1419/#1461): the two-user isolation
tests are the point — user A's toggle/clear must never touch user B's state.

DB idiom mirrors tests/integration/test_learning_cycle_phase3_phase4.py:
real dev Postgres via AsyncSessionFactory, fresh users per test, direct
route-function calls with a stand-in claims object carrying only user_id.
"""

import uuid as _uuid
from types import SimpleNamespace

import pytest
import pytest_asyncio
from sqlalchemy import and_, select

from services.database.models import LearnedPattern, LearningSettings, User
from services.database.session_factory import AsyncSessionFactory
from services.shared_types import PatternType
from web.api.routes import learning

pytestmark = pytest.mark.asyncio

# Rebound per test by the fixture below (module globals read at call time).
USER_A = None
USER_B = None
CLAIMS_A = None
CLAIMS_B = None


@pytest_asyncio.fixture(autouse=True)
async def _two_fresh_users():
    """Two fresh users per test; cleanup deletes their learning rows + users."""
    global USER_A, USER_B, CLAIMS_A, CLAIMS_B
    from tests.conftest import delete_test_user_fully

    USER_A = _uuid.uuid4()
    USER_B = _uuid.uuid4()
    CLAIMS_A = SimpleNamespace(user_id=USER_A)
    CLAIMS_B = SimpleNamespace(user_id=USER_B)

    async with AsyncSessionFactory.session_scope_fresh() as session:
        for uid in (USER_A, USER_B):
            session.add(
                User(
                    id=str(uid),
                    username=f"learn1430-{str(uid)[:8]}",
                    email=f"learn1430-{str(uid)[:8]}@example.com",
                    password_hash="x",
                    is_active=True,
                    is_verified=True,
                )
            )
        await session.commit()

    yield

    async with AsyncSessionFactory.session_scope_fresh() as session:
        for uid in (USER_A, USER_B):
            await delete_test_user_fully(session, str(uid))
        await session.commit()


async def _seed_pattern(user_id) -> str:
    """Insert one learned pattern for user_id; returns its id."""
    async with AsyncSessionFactory.session_scope_fresh() as session:
        pattern = LearnedPattern(
            user_id=user_id,
            pattern_type=PatternType.USER_WORKFLOW,
            pattern_data={"query": "seeded", "owner": str(user_id)},
            confidence=0.8,
        )
        session.add(pattern)
        await session.commit()
        return str(pattern.id)


async def _pattern_count(user_id) -> int:
    async with AsyncSessionFactory.session_scope_fresh() as session:
        result = await session.execute(
            select(LearnedPattern).where(LearnedPattern.user_id == user_id)
        )
        return len(result.scalars().all())


# ---- Registration: the dashboard's Export/Clear endpoints exist and are authed ----


def _route_map():
    return {
        (r.path, m) for r in learning.router.routes for m in getattr(r, "methods", set())
    }


async def test_controls_export_and_clear_routes_registered_1430():
    """Failing-first: before #1430 these paths were decorator-commented → 404."""
    routes = _route_map()
    assert ("/api/v1/learning/controls/export", "GET") in routes
    assert ("/api/v1/learning/controls/data/clear", "DELETE") in routes


async def test_controls_routes_take_no_client_user_id_1430():
    """The principal comes from the session dependency; no user_id parameter exists."""
    import inspect

    for fn in (learning.export_learning_data, learning.clear_learning_data):
        params = inspect.signature(fn).parameters
        assert "user_id" not in params, f"{fn.__name__} must not accept client user_id"
        assert "current_user" in params


# ---- Export: scoped to the authenticated principal ----


async def test_export_returns_only_authed_users_data_1430():
    await _seed_pattern(USER_A)
    await _seed_pattern(USER_B)

    data = await learning.export_learning_data(format="json", current_user=CLAIMS_A)

    assert data["user_id"] == str(USER_A)
    owners = {p["pattern_data"]["owner"] for p in data["patterns"]}
    assert owners == {str(USER_A)}  # B's pattern never appears in A's export


async def test_export_ignores_client_supplied_user_id_on_the_wire_1430():
    """?user_id=<B> from the client changes nothing — A gets A's data."""
    from fastapi import FastAPI
    from fastapi.testclient import TestClient

    from services.auth.auth_middleware import get_current_user

    await _seed_pattern(USER_A)
    await _seed_pattern(USER_B)

    app = FastAPI()
    app.include_router(learning.router)
    app.dependency_overrides[get_current_user] = lambda: CLAIMS_A

    with TestClient(app) as client:
        resp = client.get(
            f"/api/v1/learning/controls/export?user_id={USER_B}&format=json"
        )

    assert resp.status_code == 200
    body = resp.json()
    assert body["user_id"] == str(USER_A)  # NOT the client-supplied B
    owners = {p["pattern_data"]["owner"] for p in body["patterns"]}
    assert owners == {str(USER_A)}


# ---- Clear: two-user isolation (the destructive path) ----


async def test_clear_removes_only_authed_users_patterns_1430():
    await _seed_pattern(USER_A)
    await _seed_pattern(USER_B)

    result = await learning.clear_learning_data(data_type="all", current_user=CLAIMS_A)

    assert result["status"] == "success"
    assert result["user_id"] == str(USER_A)
    assert await _pattern_count(USER_A) == 0  # A's data gone
    assert await _pattern_count(USER_B) == 1  # B's data untouched


async def test_clear_rejects_invalid_data_type_1430():
    result = await learning.clear_learning_data(
        data_type="everything", current_user=CLAIMS_A
    )
    # File idiom: error-response helpers return JSONResponse, not raise.
    assert getattr(result, "status_code", 200) == 422


# ---- Settings toggle: the headline two-user isolation AC ----


async def test_settings_toggle_two_user_isolation_1430():
    """User A disables learning; user B's state is unchanged and each sees only
    their own state (the #1419/#1461-class assertion)."""
    update = learning.SettingsUpdate(learning_enabled=False)
    await learning.update_settings(settings_update=update, current_user=CLAIMS_A)

    seen_a = await learning.get_settings(current_user=CLAIMS_A)
    seen_b = await learning.get_settings(current_user=CLAIMS_B)

    assert seen_a["settings"]["learning_enabled"] is False
    assert seen_a["configured"] is True
    # B never toggled: still on defaults, not affected by A's write.
    assert seen_b["settings"]["learning_enabled"] is True
    assert seen_b["configured"] is False

    # And the DB row A created is A's alone.
    async with AsyncSessionFactory.session_scope_fresh() as session:
        result = await session.execute(
            select(LearningSettings).where(
                and_(LearningSettings.user_id.in_([USER_A, USER_B]))
            )
        )
        rows = result.scalars().all()
        assert [str(r.user_id) for r in rows] == [str(USER_A)]
