"""#2327 at the DB layer: the counter's upsert and the admin read, against Postgres.

The unit suite replaces the counter write with a mock, which proves the note and the
name rule and CANNOT prove the statement is valid SQL, that the conflict target is
the table's key, or that a second sighting adds one instead of a second row. This
file runs the real upsert and the real endpoint function.

m-43 (name the layer): the DB layer and only that. It skips, saying why, on a
database that does not have migration ``v2327floored`` yet (a local database another
checkout has not migrated); CI runs ``alembic upgrade head`` first, so it runs there.
"""

import uuid
from datetime import datetime, timezone

import pytest
from sqlalchemy import text

from services.database.session_factory import AsyncSessionFactory
from services.intent_service import floored_action_audit as audit

pytestmark = [pytest.mark.integration, pytest.mark.asyncio]


@pytest.fixture
async def scratch_name():
    """A name unique to this run that fits the recorded shape; its rows are removed."""
    async with AsyncSessionFactory.session_scope() as s:
        exists = (
            await s.execute(text("SELECT to_regclass('public.floored_action_counts')"))
        ).scalar()
    if exists is None:
        pytest.skip("migration v2327floored is not applied to this database")
    name = f"zz_2327_{uuid.uuid4().hex[:12]}"
    yield name
    async with AsyncSessionFactory.session_scope() as s:
        await s.execute(text("DELETE FROM floored_action_counts WHERE name = :n"), {"n": name})
        await s.commit()


async def _rows(name):
    async with AsyncSessionFactory.session_scope() as s:
        result = await s.execute(
            text(
                "SELECT site, day, count FROM floored_action_counts "
                "WHERE name = :n ORDER BY site"
            ),
            {"n": name},
        )
        return [tuple(r) for r in result.all()]


async def test_a_second_sighting_adds_one_to_the_same_row(scratch_name):
    today = datetime.now(timezone.utc).date()
    await audit._increment(scratch_name, audit.SITE_QUERY_ACTION)
    await audit._increment(scratch_name, audit.SITE_QUERY_ACTION)
    await audit._increment(scratch_name, audit.SITE_ACTION_GATE)
    assert await _rows(scratch_name) == [
        (audit.SITE_ACTION_GATE, today, 1),
        (audit.SITE_QUERY_ACTION, today, 2),
    ]


async def test_the_note_writes_the_row_for_an_invented_name(scratch_name):
    await audit.note_floored_action(audit.SITE_ANALYSIS_ACTION, scratch_name, "some message")
    rows = await _rows(scratch_name)
    assert [(site, count) for site, _day, count in rows] == [(audit.SITE_ANALYSIS_ACTION, 1)]


async def test_the_admin_read_returns_the_rows_and_the_window(scratch_name):
    from web.api.routes.admin import floored_actions

    await audit._increment(scratch_name, audit.SITE_QUERY_ACTION)
    today = datetime.now(timezone.utc).date().isoformat()
    payload = await floored_actions(days=1, admin=None)
    assert payload["window"] == {"days": 1, "since": today, "through": today}
    mine = [r for r in payload["rows"] if r["name"] == scratch_name]
    assert mine == [
        {"name": scratch_name, "site": audit.SITE_QUERY_ACTION, "day": today, "count": 1}
    ]
    assert payload["row_count"] == len(payload["rows"]) >= 1
    assert payload["first_day"] == today and payload["last_day"] == today
    # HOST's bar: a row holds these four fields and nothing else.
    assert all(set(r) == {"name", "site", "day", "count"} for r in payload["rows"])


async def test_the_window_is_capped():
    from web.api.routes import admin

    async with AsyncSessionFactory.session_scope() as s:
        exists = (
            await s.execute(text("SELECT to_regclass('public.floored_action_counts')"))
        ).scalar()
    if exists is None:
        pytest.skip("migration v2327floored is not applied to this database")
    payload = await admin.floored_actions(days=100000, admin=None)
    assert payload["window"]["days"] == admin.FLOORED_ACTIONS_MAX_DAYS
    assert (await admin.floored_actions(days=0, admin=None))["window"]["days"] == 1
