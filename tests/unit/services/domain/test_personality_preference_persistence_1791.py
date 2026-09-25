"""#1791 — personality preferences persist per-user through UserPreferenceManager's
real store (#1574's `users.preferences["upm"]`), the same way #1574/#1876 already
proved for timezone. Before this issue, `PiperConfigParser` ignored `user_id` and
read/wrote one instance-wide file (`config/PIPER.user.md`) — every alpha tester
shared one personality.

LAYER (m-43): the REAL local Postgres through the real session factory, mirroring
tests/unit/services/domain/test_preference_persistence_1574.py's harness exactly —
a fresh `UserPreferenceManager()` instance is the "restart". Per-run UUID users,
deleted in `finally` by exact id (no fixed PKs, no residue).

DENOMINATOR: restart survival for the personality key specifically · two real
users' rows never collide · a user with nothing saved gets `None` (the
load-bearing "fall back to the instance default" signal, not an error or an
empty dict) · the `personality_profile` key lives under `upm` and does not
collide with sibling `#1574`/`#1876`/`#280`/`#1510` keys in the same JSONB
column. Does NOT cover the HTTP layer (routes) — see
tests/unit/web/api/routes/test_personality_principal_from_session_1751.py and
tests/unit/web/api/routes/test_personality_put_admin_gated_1734.py for that.
"""

from __future__ import annotations

import uuid

import pytest
import pytest_asyncio
from sqlalchemy import delete, select

from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.domain.user_preference_manager import PERSONALITY_PROFILE, UserPreferenceManager

pytestmark = pytest.mark.asyncio

PROFILE_A = {
    "warmth_level": 0.93,
    "confidence_style": "descriptive",
    "action_orientation": "medium",
    "technical_depth": "simplified",
}

PROFILE_B = {
    "warmth_level": 0.1,
    "confidence_style": "numeric",
    "action_orientation": "low",
    "technical_depth": "detailed",
}


@pytest_asyncio.fixture
async def db_user():
    uid = uuid.uuid4()
    tag = uid.hex[:12]
    async with AsyncSessionFactory.session_scope_fresh() as s:
        s.add(
            User(
                id=uid,
                username=f"pers-1791-{tag}",
                email=f"pers-1791-{tag}@test.local",
                is_active=True,
                is_verified=True,
                preferences={"existing_key": "untouched"},
            )
        )
        await s.commit()
    try:
        yield uid
    finally:
        async with AsyncSessionFactory.session_scope_fresh() as s:
            await s.execute(delete(User).where(User.id == uid))
            await s.commit()


@pytest_asyncio.fixture
async def two_db_users(db_user):
    uid_b = uuid.uuid4()
    tag = uid_b.hex[:12]
    async with AsyncSessionFactory.session_scope_fresh() as s:
        s.add(
            User(
                id=uid_b,
                username=f"pers-1791-b-{tag}",
                email=f"pers-1791-b-{tag}@test.local",
                is_active=True,
                is_verified=True,
                preferences={},
            )
        )
        await s.commit()
    try:
        yield db_user, uid_b
    finally:
        async with AsyncSessionFactory.session_scope_fresh() as s:
            await s.execute(delete(User).where(User.id == uid_b))
            await s.commit()


async def _row_prefs(uid):
    async with AsyncSessionFactory.session_scope_fresh() as s:
        return (await s.execute(select(User.preferences).where(User.id == uid))).scalar_one()


class TestNoSavedProfileIsNoneNotEmpty:
    async def test_get_personality_returns_none_when_never_set(self, db_user):
        """None is load-bearing: PiperConfigParser reads this as "fall back to
        the instance default", not as an empty/zeroed profile."""
        m = UserPreferenceManager()
        assert await m.get_personality(db_user) is None


class TestRestartSurvival:
    async def test_saved_profile_survives_a_fresh_manager(self, db_user):
        """THE #1791 pin, mirroring #1574's own: a new manager instance (=
        a process restart) reads what the old one set."""
        a = UserPreferenceManager()
        await a.set_personality(db_user, PROFILE_A)

        b = UserPreferenceManager()
        assert await b.get_personality(db_user) == PROFILE_A


class TestTwoUsersNeverCollide:
    async def test_each_user_gets_their_own_profile_back(self, two_db_users):
        uid_a, uid_b = two_db_users
        m = UserPreferenceManager()
        await m.set_personality(uid_a, PROFILE_A)
        await m.set_personality(uid_b, PROFILE_B)

        assert await m.get_personality(uid_a) == PROFILE_A
        assert await m.get_personality(uid_b) == PROFILE_B

    async def test_a_third_user_with_nothing_saved_is_unaffected_by_the_other_two(
        self, two_db_users
    ):
        uid_a, uid_b = two_db_users
        m = UserPreferenceManager()
        await m.set_personality(uid_a, PROFILE_A)
        await m.set_personality(uid_b, PROFILE_B)

        uid_c = uuid.uuid4()
        assert await m.get_personality(uid_c) is None


class TestCollisionSafety:
    async def test_other_keys_and_upm_siblings_are_never_touched(self, db_user):
        m = UserPreferenceManager()
        await m.set_preference("timezone", "Europe/Helsinki", user_id=db_user, scope="user")
        await m.set_personality(db_user, PROFILE_A)

        prefs = await _row_prefs(db_user)
        assert prefs["existing_key"] == "untouched"
        assert prefs["upm"]["timezone"]["value"] == "Europe/Helsinki"
        assert prefs["upm"][PERSONALITY_PROFILE]["value"] == PROFILE_A
