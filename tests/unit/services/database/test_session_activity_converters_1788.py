"""#1788 — SessionActivityDB.from_domain / to_domain round-trip.

#1788's PM-056 job 2 (`scripts/check_conversion_methods.py`) was red because
`SessionActivityDB` carried `to_domain` but no `from_domain`. Arch's ruling
(2026-09-13) allows a converter only where a live path actually round-trips the
row -- and this one does: the observer at `IntentService._record_session_activity`
writes via `SessionActivityRepository.record`, and the B4 recall reader
(`session_activity_read` -> `list_for_session`) returns `domain.SessionActivity`.

These tests exercise the round-trip through a real database, not the presence of
a method: a POPULATED domain record is converted, persisted, re-read, and
converted back, then compared field for field. A converter that silently dropped
a field would pass a "the method exists" smoke check and fail here.

In-memory SQLite (#1035 pattern), matching test_document_model_1238.py.
"""

from __future__ import annotations

import uuid
from datetime import datetime, timedelta, timezone

import pytest
import pytest_asyncio

aiosqlite = pytest.importorskip("aiosqlite")

from sqlalchemy import select  # noqa: E402
from sqlalchemy.ext.asyncio import (  # noqa: E402
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from services.database.models import SessionActivityDB  # noqa: E402
from services.domain.models import SessionActivity  # noqa: E402

pytestmark = pytest.mark.asyncio

_OWNER = "a25db09c-6d79-41e4-8d82-87b6a005bbb0"
_OTHER_OWNER = "0f2e1d5b-7c44-4a10-9b2e-3c6a8e9f1d22"


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    async with engine.begin() as conn:
        await conn.run_sync(lambda c: SessionActivityDB.__table__.create(c, checkfirst=True))
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with SessionLocal() as s:
        yield s
    await engine.dispose()


def _same_instant(a: datetime | None, b: datetime | None) -> bool:
    """Compare two timestamps as instants, tolerating a dropped tzinfo.

    NOT a weakened assertion -- a storage-layer fact. `created_at` is
    `DateTime(timezone=True)`, which Postgres round-trips with its offset intact,
    but the SQLite driver these unit tests run on returns a NAIVE datetime with
    the same UTC wall-clock. Asserting exact equality would test the test
    database's driver rather than the converter. The contract that matters, and
    that this checks, is that the same instant comes back.
    """
    if a is None or b is None:
        return a is b
    if a.tzinfo is None:
        a = a.replace(tzinfo=timezone.utc)
    if b.tzinfo is None:
        b = b.replace(tzinfo=timezone.utc)
    return a == b


def _populated(**overrides) -> SessionActivity:
    """A domain record with EVERY field set to a distinct, non-default value.

    Distinct values matter: if `from_domain` transposed two fields, defaults or
    repeated values would hide it.
    """
    base = dict(
        id=str(uuid.uuid4()),
        conversation_id=str(uuid.uuid4()),
        owner_id=_OWNER,
        action_type="issue_created",
        target_ref="mediajunkie/piper-morgan-product#1788",
        turn_id=str(uuid.uuid4()),
        target_title="PM-056 job 2: DB models lacking converters",
        created_at=datetime(2026, 9, 13, 21, 48, 0, tzinfo=timezone.utc),
    )
    base.update(overrides)
    return SessionActivity(**base)


async def test_from_domain_to_domain_round_trips_through_the_database(session):
    """Populated domain record -> row -> persisted -> re-read -> domain record.

    The assertion is field-for-field equality on the FULL field set, so a dropped
    or transposed field fails rather than passing as a partial conversion.
    """
    original = _populated()

    session.add(SessionActivityDB.from_domain(original))
    await session.commit()

    row = (
        await session.execute(select(SessionActivityDB).where(SessionActivityDB.id == original.id))
    ).scalar_one()
    restored = row.to_domain()

    assert restored.id == original.id
    assert restored.conversation_id == original.conversation_id
    assert restored.owner_id == original.owner_id
    assert restored.action_type == original.action_type
    assert restored.target_ref == original.target_ref
    assert restored.turn_id == original.turn_id
    assert restored.target_title == original.target_title
    assert _same_instant(restored.created_at, original.created_at)


async def test_round_trip_covers_every_domain_field(session):
    """Guard against the field sets drifting apart under this converter.

    `SessionActivity` is a frozen dataclass; if someone adds a field to it (or to
    the table) without extending `from_domain`, the loop below starts comparing a
    field the converter never carried and fails. This is the check that keeps the
    converter honest as the model evolves, rather than a snapshot of today.
    """
    original = _populated()

    session.add(SessionActivityDB.from_domain(original))
    await session.commit()
    row = (
        await session.execute(select(SessionActivityDB).where(SessionActivityDB.id == original.id))
    ).scalar_one()
    restored = row.to_domain()

    fields = [f.name for f in original.__dataclass_fields__.values()]
    assert set(fields) == {
        "id",
        "conversation_id",
        "owner_id",
        "action_type",
        "target_ref",
        "turn_id",
        "target_title",
        "created_at",
    }, "SessionActivity field set changed -- extend from_domain and this guard together"

    for name in fields:
        restored_value, original_value = getattr(restored, name), getattr(original, name)
        if isinstance(original_value, datetime):
            assert _same_instant(
                restored_value, original_value
            ), f"field lost in round trip: {name}"
        else:
            assert restored_value == original_value, f"field lost in round trip: {name}"


async def test_optional_fields_round_trip_as_none(session):
    """`turn_id` and `target_title` are Optional -- None must survive as None.

    A converter that coerced these to "" would round-trip a *different* record
    while still looking like it worked.
    """
    original = _populated(turn_id=None, target_title=None)

    session.add(SessionActivityDB.from_domain(original))
    await session.commit()
    row = (
        await session.execute(select(SessionActivityDB).where(SessionActivityDB.id == original.id))
    ).scalar_one()
    restored = row.to_domain()

    assert restored.turn_id is None
    assert restored.target_title is None
    assert restored.target_ref == original.target_ref


async def test_created_at_none_defers_to_the_column_default(session):
    """`created_at` defaults on the domain dataclass to None.

    `SessionActivityRepository.record` never sets the column -- it relies on the
    server_default -- so `from_domain` must not write an explicit NULL into a
    NOT NULL column and blow up on a record built without a timestamp.
    """
    original = _populated(created_at=None)

    session.add(SessionActivityDB.from_domain(original))
    await session.commit()
    row = (
        await session.execute(select(SessionActivityDB).where(SessionActivityDB.id == original.id))
    ).scalar_one()

    assert row.created_at is not None
    assert row.to_domain().id == original.id


async def test_owner_id_is_carried_not_defaulted(session):
    """D1a: `owner_id` is the read-scoping key and is NOT NULL on the table.

    The converter must carry the record's own owner through -- a from_domain that
    dropped or defaulted it would manufacture rows attributable to the wrong
    principal, which is the ADR-071 cross-user class this ledger is scoped to
    prevent.
    """
    mine = _populated(owner_id=_OWNER)
    theirs = _populated(owner_id=_OTHER_OWNER)

    session.add(SessionActivityDB.from_domain(mine))
    session.add(SessionActivityDB.from_domain(theirs))
    await session.commit()

    scoped = (
        (
            await session.execute(
                select(SessionActivityDB).where(SessionActivityDB.owner_id == _OWNER)
            )
        )
        .scalars()
        .all()
    )

    assert [r.id for r in scoped] == [mine.id]
    assert scoped[0].to_domain().owner_id == _OWNER


async def test_from_domain_is_a_classmethod_returning_an_unpersisted_row(session):
    """Shape contract the PM-056 checker enforces: `from_domain` is a classmethod.

    Also pins that it returns a row the caller still owns -- it does not add to or
    touch a session (the repository owns the transaction).
    """
    assert isinstance(
        SessionActivityDB.__dict__["from_domain"], classmethod
    ), "from_domain must be a @classmethod (PM-056 conversion-methods contract)"

    original = _populated()
    row = SessionActivityDB.from_domain(original)

    assert isinstance(row, SessionActivityDB)
    assert row.id == original.id

    # Nothing was written: the caller had not added it to the session.
    found = (
        await session.execute(select(SessionActivityDB).where(SessionActivityDB.id == original.id))
    ).scalar_one_or_none()
    assert found is None


async def test_repository_write_shape_matches_from_domain(session):
    """The converter and the live writer must produce the same row.

    `SessionActivityRepository.record` builds `SessionActivityDB(...)` by hand
    (`services/database/repositories.py`). If the two construction paths drift,
    one of them is wrong -- this compares them on the same inputs.
    """
    created = datetime.now(timezone.utc) - timedelta(minutes=5)
    original = _populated(created_at=created)

    via_converter = SessionActivityDB.from_domain(original)
    via_repository_shape = SessionActivityDB(
        id=original.id,
        owner_id=str(original.owner_id),
        conversation_id=str(original.conversation_id),
        action_type=original.action_type,
        target_ref=original.target_ref,
        turn_id=original.turn_id,
        target_title=original.target_title,
        created_at=created,
    )

    for name in (
        "id",
        "conversation_id",
        "owner_id",
        "action_type",
        "target_ref",
        "turn_id",
        "target_title",
        "created_at",
    ):
        assert getattr(via_converter, name) == getattr(via_repository_shape, name), name
