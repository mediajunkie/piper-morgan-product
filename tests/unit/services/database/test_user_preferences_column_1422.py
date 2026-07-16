"""#1422: users.preferences exists again and personality personalization runs.

Regression: #262's alpha_users->users merge dropped the preferences JSONB column
while three services kept reading/writing ``user.preferences`` — every call
raised AttributeError into silent-default fallbacks, so questionnaire
personalization was dead product-wide (census A calibration #2 / census B6,
sprint #1424).

Three layers pinned here:
  1. The questionnaire mapping itself (pure unit — it had never executed).
  2. ORM round-trip: preferences persist and reload through the real column.
  3. load_with_preferences end-to-end: a stored preference produces a
     NON-default profile (the exact user-visible behavior that was dead).

Requires PostgreSQL on 5433 with migrations current (same as the suite's other
DB-backed tests).
"""

from datetime import datetime, timezone
from uuid import uuid4

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    TechnicalPreference,
)

_DB_URL = "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"

QUESTIONNAIRE = {
    "communication_style": "concise",
    "work_style": "structured",
    "decision_making": "data-driven",
    "learning_style": "explanations",
}


def test_questionnaire_mapping_is_not_the_default():
    profile = PersonalityProfile._create_from_preferences("u-test", QUESTIONNAIRE)
    assert profile.warmth_level == 0.4  # concise -> professional
    assert profile.action_orientation == ActionLevel.HIGH  # structured
    assert profile.confidence_style == ConfidenceDisplayStyle.NUMERIC  # data-driven
    assert profile.technical_depth == TechnicalPreference.DETAILED  # explanations

    default = PersonalityProfile.get_default("u-test")
    assert profile.warmth_level != default.warmth_level


@pytest.fixture
async def db_user_with_prefs():
    """Insert a user row, yield its id, clean up."""
    user_id = str(uuid4())
    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as s:
        await s.execute(
            text(
                "INSERT INTO users (id, username, email, is_active, is_verified, "
                "created_at, updated_at, role, is_alpha, preferences) "
                "VALUES (:id, :u, :e, true, true, :now, :now, 'user', true, "
                "CAST(:prefs AS jsonb))"
            ),
            {
                "id": user_id,
                "u": f"prefs1422_{user_id[:8]}",
                "e": f"prefs1422_{user_id[:8]}@test.example.com",
                "now": datetime.now(timezone.utc),
                "prefs": '{"communication_style": "concise", "work_style": "structured", '
                '"decision_making": "data-driven", "learning_style": "explanations"}',
            },
        )
        await s.commit()
    try:
        yield user_id
    finally:
        async with async_session() as s:
            await s.execute(text("DELETE FROM users WHERE id = :uid"), {"uid": user_id})
            await s.commit()
        await engine.dispose()


async def test_preferences_round_trip_through_orm(db_user_with_prefs):
    from services.database.models import User
    from sqlalchemy import select

    engine = create_async_engine(_DB_URL, echo=False)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    try:
        async with async_session() as s:
            user = (
                await s.execute(select(User).where(User.id == db_user_with_prefs))
            ).scalar_one()
            assert user.preferences["communication_style"] == "concise"
            # The onboarding writer's exact idiom (intent_service.py ~:2455)
            prefs = dict(user.preferences or {})
            prefs["feedback_level"] = "detailed"
            user.preferences = prefs
            await s.commit()
        async with async_session() as s:
            user = (
                await s.execute(select(User).where(User.id == db_user_with_prefs))
            ).scalar_one()
            assert user.preferences["feedback_level"] == "detailed"
    finally:
        await engine.dispose()


async def test_load_with_preferences_returns_personalized_profile(db_user_with_prefs):
    """The headline behavior: stored questionnaire answers now shape the profile."""
    profile = await PersonalityProfile.load_with_preferences(db_user_with_prefs)
    assert profile.warmth_level == 0.4
    assert profile.action_orientation == ActionLevel.HIGH
    assert profile.confidence_style == ConfidenceDisplayStyle.NUMERIC
    assert profile.technical_depth == TechnicalPreference.DETAILED
