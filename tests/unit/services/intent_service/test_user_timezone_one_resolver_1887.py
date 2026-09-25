"""1887 — one timezone resolver for the todo/reminder path.

Two timezone homes existed: the zone the user CHOSE ("set my timezone to …",
the Preferences page, PUT /api/v1/preferences/timezone — #1876) lives in the
#1574 store (``users.preferences["upm"]`` via ``UserPreferenceManager``) and
is what every #1576 face reads; the zone the login flow OBSERVED from the
browser (#1572) lives in the flat ``users.preferences["timezone"]`` and was
the ONLY thing ``get_user_timezone`` — the todo/reminder due-date reader —
consulted. So a user who set Helsinki in chat saw Helsinki clock faces while
"remind me tomorrow at 9" was still interpreted in the browser's zone.

The fix under test: ``get_user_timezone`` resolves chosen → observed → None.

Layer (m-43): real Postgres, both stores written through their real writers
(``UserPreferenceManager.set_reminder_timezone`` and ``save_user_timezone``)
and read back through ``get_user_timezone`` — the store, not a mock. The
todo handlers' use of the value is pinned by the #1572 suite; this pins the
resolver order only.
"""

import uuid as _uuid
from uuid import UUID

import pytest

from services.utils.user_timezone import get_user_timezone, save_user_timezone

LA = "America/Los_Angeles"
HELSINKI = "Europe/Helsinki"
TOKYO = "Asia/Tokyo"


@pytest.fixture
async def tz_user():
    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory
    from tests.conftest import delete_test_user_fully

    uid = str(_uuid.uuid4())
    async with AsyncSessionFactory.session_scope_fresh() as session:
        session.add(
            User(
                id=uid,
                username=f"tz1887-{uid[:8]}",
                email=f"tz1887-{uid[:8]}@example.com",
                password_hash="x",
                is_active=True,
                is_verified=True,
            )
        )
        await session.commit()
    yield uid
    async with AsyncSessionFactory.session_scope_fresh() as session:
        await delete_test_user_fully(session, uid)
        await session.commit()


async def _choose(user_id: str, tz: str) -> None:
    from services.domain.user_preference_manager import UserPreferenceManager

    await UserPreferenceManager().set_reminder_timezone(UUID(user_id), tz)


class TestOneResolver1887:
    @pytest.mark.asyncio
    async def test_chosen_zone_wins_over_the_observed_one(self, tz_user):
        """The 1887 hazard itself: login observed LA, the user chose Helsinki
        in chat — due dates must now be read in Helsinki."""
        assert await save_user_timezone(tz_user, LA) is True  # the login capture
        assert await get_user_timezone(tz_user) == LA  # observed only → observed
        await _choose(tz_user, HELSINKI)  # "set my timezone to Helsinki"
        assert await get_user_timezone(tz_user) == HELSINKI

    @pytest.mark.asyncio
    async def test_a_later_choice_replaces_an_earlier_one(self, tz_user):
        await _choose(tz_user, HELSINKI)
        await _choose(tz_user, TOKYO)
        assert await get_user_timezone(tz_user) == TOKYO

    @pytest.mark.asyncio
    async def test_observed_zone_still_serves_when_nothing_was_chosen(self, tz_user):
        assert await save_user_timezone(tz_user, LA) is True
        assert await get_user_timezone(tz_user) == LA

    @pytest.mark.asyncio
    async def test_nothing_known_is_none_not_a_default(self, tz_user):
        """The todo path keeps its pre-#1572 None contract — it must NOT
        inherit the face layer's America/Los_Angeles default, which would
        silently shift instants for a user who never said anything."""
        assert await get_user_timezone(tz_user) is None

    @pytest.mark.asyncio
    async def test_login_observation_never_overrides_a_choice(self, tz_user):
        """A later login from another browser (the flat key changing) leaves
        the chosen zone in charge — observation is a fact, choice is a
        decision, and the #1876 page asks before promoting one to the other."""
        await _choose(tz_user, HELSINKI)
        assert await save_user_timezone(tz_user, TOKYO) is True  # a login from Tokyo
        assert await get_user_timezone(tz_user) == HELSINKI

    @pytest.mark.asyncio
    async def test_the_face_layer_and_the_todo_path_agree_once_chosen(self, tz_user):
        """The whole point: one zone for the clock face and the due date."""
        from services.utils.datetime_utils import user_timezone_name

        await _choose(tz_user, HELSINKI)
        assert await user_timezone_name(tz_user) == HELSINKI
        assert await get_user_timezone(tz_user) == HELSINKI
