"""#1436 B15: the feedback routes must call the FeedbackService API that exists.

Regression: all three routes had drifted against the real service — submit built
a nonexistent ``domain.Feedback`` and called a nonexistent ``submit_feedback``;
the reads called nonexistent ``get_feedback_by_id``/``get_feedback_by_user`` and
read a nonexistent ``.content`` field. Every feedback request 500'd; the routes
had never been exercised end-to-end (census B15, sprint #1424).

These tests run the route functions against the REAL FeedbackService on the dev
DB (same pattern as the #1421/#1422 DB-backed tests): submit -> get -> list,
plus the ownership scope (user B cannot read A's feedback).
"""

from datetime import datetime, timezone
from types import SimpleNamespace
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.feedback.feedback_service import FeedbackService
from web.api.routes.feedback import get_feedback, list_feedback, submit_feedback

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"


@pytest.fixture
async def db_users():
    """Two users; yields (engine, session_factory, a_id, b_id); cleans up."""
    engine = create_async_engine(_DB_URL, echo=False)
    factory = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    a_id, b_id = str(uuid4()), str(uuid4())
    now = datetime.now(timezone.utc)
    async with factory() as s:
        for uid in (a_id, b_id):
            await s.execute(
                text(
                    "INSERT INTO users (id, username, email, is_active, is_verified, "
                    "created_at, updated_at, role, is_alpha) "
                    "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true)"
                ),
                {"id": uid, "u": f"fb1436_{uid[:8]}", "e": f"fb1436_{uid[:8]}@test.example.com", "now": now},
            )
        await s.commit()
    try:
        yield engine, factory, a_id, b_id
    finally:
        async with factory() as s:
            for uid in (a_id, b_id):
                await s.execute(
                    text("DELETE FROM feedback WHERE user_id = CAST(:u AS uuid)"), {"u": uid}
                )
                await s.execute(text("DELETE FROM users WHERE id = :u"), {"u": uid})
            await s.commit()
        await engine.dispose()


def _claims(uid: str):
    return SimpleNamespace(sub=uid)


async def test_submit_get_list_round_trip(db_users):
    engine, factory, a_id, _b = db_users
    async with factory() as s:
        svc = FeedbackService(s)
        created = await submit_feedback(
            content="The picker works now — nice.",
            feedback_type="general",
            current_user=_claims(a_id),
            feedback_service=svc,
        )
    assert created["id"] and created["content"] == "The picker works now — nice."

    async with factory() as s:
        svc = FeedbackService(s)
        got = await get_feedback(
            feedback_id=created["id"], current_user=_claims(a_id), feedback_service=svc
        )
        assert got["content"] == "The picker works now — nice."
        listed = await list_feedback(current_user=_claims(a_id), feedback_service=svc)
        assert listed["count"] == 1
        assert listed["feedback"][0]["id"] == created["id"]


async def test_other_user_cannot_read_it(db_users):
    from fastapi import HTTPException

    engine, factory, a_id, b_id = db_users
    async with factory() as s:
        created = await submit_feedback(
            content="private note",
            feedback_type="general",
            current_user=_claims(a_id),
            feedback_service=FeedbackService(s),
        )
    async with factory() as s:
        svc = FeedbackService(s)
        with pytest.raises(HTTPException) as exc:
            await get_feedback(
                feedback_id=created["id"], current_user=_claims(b_id), feedback_service=svc
            )
        assert exc.value.status_code == 404  # scoped read: not-yours == not-found
        listed = await list_feedback(current_user=_claims(b_id), feedback_service=svc)
        assert listed["count"] == 0
