"""#2171 (Web on alpha 228f3cec14, CXO class 3): the Lists card read "Items: 0" for a list
holding one item. ``GET /api/v1/lists`` sent no count, so the page's ``|| 0`` showed a
number nobody read. Now the route reads the real count per list, a count it couldn't
read is null, and the card shows a count only when a number arrived.
"""

from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

import pytest

ROOT = Path(__file__).resolve().parents[3]


def _list(lid):
    now = datetime.now(timezone.utc)
    return SimpleNamespace(
        id=lid, name="n", description=None, owner_id="u", created_at=now, updated_at=now
    )


def _repo(count):
    repo = MagicMock()
    repo.get_lists_by_owner = AsyncMock(return_value=[_list("L1")])
    repo.get_max_item_added_at = AsyncMock(return_value=None)
    repo.count_items = AsyncMock(**count)
    return repo


@pytest.mark.asyncio
async def test_the_route_sends_the_real_count():
    from web.api.routes.lists import list_lists

    out = await list_lists(
        current_user=SimpleNamespace(sub="u"), list_repo=_repo({"return_value": 1})
    )
    assert out["lists"][0]["item_count"] == 1


@pytest.mark.asyncio
async def test_a_count_that_could_not_be_read_is_null_not_zero():
    from web.api.routes.lists import list_lists

    out = await list_lists(
        current_user=SimpleNamespace(sub="u"),
        list_repo=_repo({"side_effect": RuntimeError("db")}),
    )
    assert out["lists"][0]["item_count"] is None


def test_the_card_shows_a_count_only_when_a_number_arrived():
    src = (ROOT / "templates/lists.html").read_text()
    assert "list.item_count || 0" not in src
    assert "typeof list.item_count === 'number'" in src
    assert "data.count || 0" not in src
