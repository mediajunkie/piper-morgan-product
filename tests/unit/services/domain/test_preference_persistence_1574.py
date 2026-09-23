"""#1574 — UserPreferenceManager's user scope survives a process restart (audit F6).

Before: every preference lived in one process's dicts — all silently reset per restart, so the
tz preference was a facade and the calendar-setup offer re-nagged after each deploy. After: user
scope is read-through/write-through to ``users.preferences["upm"]`` (namespaced so #280's and
#1510's keys in the same JSONB column are never touched); session scope stays in-memory by design.

LAYER (m-43): the REAL local Postgres through the real session factory — a fresh manager instance
is the restart. Per-run UUID users, deleted in ``finally`` by exact id (#1813: no fixed PKs, no
residue). DENOMINATOR: restart survival · collision safety · version/TTL round-trip · session
scope NOT persisted · non-UUID ids stay in-memory.
"""

from __future__ import annotations

import uuid
from datetime import datetime

import pytest
import pytest_asyncio
from sqlalchemy import delete, select

from services.database.models import User
from services.database.session_factory import AsyncSessionFactory
from services.domain.user_preference_manager import UserPreferenceManager

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def db_user():
    uid = uuid.uuid4()
    tag = uid.hex[:12]
    async with AsyncSessionFactory.session_scope_fresh() as s:
        s.add(
            User(
                id=uid,
                username=f"pref-1574-{tag}",
                email=f"pref-1574-{tag}@test.local",
                is_active=True,
                is_verified=True,
                preferences={"existing_key": "untouched", "standup_prefs": {"fmt": "brief"}},
            )
        )
        await s.commit()
    try:
        yield uid
    finally:
        async with AsyncSessionFactory.session_scope_fresh() as s:
            await s.execute(delete(User).where(User.id == uid))
            await s.commit()


async def _row_prefs(uid):
    async with AsyncSessionFactory.session_scope_fresh() as s:
        return (await s.execute(select(User.preferences).where(User.id == uid))).scalar_one()


class TestRestartSurvival:
    async def test_user_pref_survives_a_fresh_manager(self, db_user):
        """THE #1574 pin: a new manager instance (= a restart) reads what the old one set."""
        a = UserPreferenceManager()
        assert await a.set_preference("timezone", "Europe/Helsinki", user_id=db_user, scope="user")
        b = UserPreferenceManager()
        assert await b.get_preference("timezone", user_id=db_user) == "Europe/Helsinki"
        assert (await b.get_all_preferences(user_id=db_user))["timezone"] == "Europe/Helsinki"

    async def test_second_key_does_not_clobber_the_first_across_processes(self, db_user):
        """A cold process must hydrate before it writes, or its first set wipes the stored map."""
        a = UserPreferenceManager()
        await a.set_preference("timezone", "Asia/Tokyo", user_id=db_user, scope="user")
        cold = UserPreferenceManager()
        await cold.set_preference("reminder_time", "09:30", user_id=db_user, scope="user")
        c = UserPreferenceManager()
        assert await c.get_preference("timezone", user_id=db_user) == "Asia/Tokyo"
        assert await c.get_preference("reminder_time", user_id=db_user) == "09:30"


class TestCollisionSafety:
    async def test_other_keys_in_the_jsonb_are_never_touched(self, db_user):
        m = UserPreferenceManager()
        await m.set_preference("timezone", "America/Denver", user_id=db_user, scope="user")
        prefs = await _row_prefs(db_user)
        assert prefs["existing_key"] == "untouched"
        assert prefs["standup_prefs"] == {"fmt": "brief"}
        assert prefs["upm"]["timezone"]["value"] == "America/Denver"


class TestRoundTrip:
    async def test_version_and_ttl_survive(self, db_user):
        a = UserPreferenceManager()
        await a.set_preference("scratch", 1, user_id=db_user, scope="user", ttl_minutes=60)
        v = await a.get_preference_version("scratch", user_id=db_user)
        b = UserPreferenceManager()
        assert await b.get_preference("scratch", user_id=db_user) == 1
        assert await b.get_preference_version("scratch", user_id=db_user) == v
        assert isinstance(v, datetime)


class TestScopeBoundaries:
    async def test_session_scope_is_not_persisted_by_design(self, db_user):
        a = UserPreferenceManager()
        await a.set_preference("mode", "quick", user_id=db_user, session_id="sess-1")
        b = UserPreferenceManager()
        assert await b.get_preference("mode", user_id=db_user, session_id="sess-1") is None
        assert "upm" not in (await _row_prefs(db_user)) or "mode" not in (
            await _row_prefs(db_user)
        ).get("upm", {})

    async def test_non_uuid_user_id_stays_in_memory_without_error(self):
        a = UserPreferenceManager()
        assert await a.set_preference("k", "v", user_id="not-a-uuid", scope="user")
        assert await a.get_preference("k", user_id="not-a-uuid") == "v"
        b = UserPreferenceManager()
        assert await b.get_preference("k", user_id="not-a-uuid") is None


class TestMixedIdTypes:
    async def test_str_and_uuid_ids_share_one_map(self, db_user):
        """Callers pass both str and UUID for the same user (preferences routes vs handlers):
        one user must be ONE in-process map, or the two diverge and the last write-through
        wins the JSONB — silently dropping the other's keys."""
        m = UserPreferenceManager()
        await m.set_preference("timezone", "Pacific/Auckland", user_id=db_user, scope="user")
        await m.set_preference("reminder_time", "07:15", user_id=str(db_user), scope="user")
        assert await m.get_preference("timezone", user_id=str(db_user)) == "Pacific/Auckland"
        assert await m.get_preference("reminder_time", user_id=db_user) == "07:15"
        stored = (await _row_prefs(db_user))["upm"]
        assert set(stored) >= {"timezone", "reminder_time"}
