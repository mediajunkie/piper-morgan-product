"""#1194 / #1033: HomeStateService surfaces composted insights (Stage 3+).

generate_home_state must pull unsurfaced insights, frame them, mark them surfaced
(so they don't repeat), and only do so for ESTABLISHED+ users. Journal is mocked.
"""

from datetime import datetime, timezone
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

import pytest

from services.home.home_state_service import HomeStateContext, HomeStateService
from services.shared_types import TrustStage


def _ctx(stage):
    return HomeStateContext(
        user_id=uuid4(), trust_stage=stage, timestamp=datetime.now(timezone.utc), time_of_day="morning"
    )


def _mock_journal(insights):
    j = MagicMock()
    j.get_unsurfaced = AsyncMock(return_value=insights)
    j.mark_surfaced = AsyncMock()
    return j


def _insight(_id, description):
    learning = MagicMock()
    learning.description = description
    learning.expression = ""
    learning.learning_type = "general"
    learning.requires_attention = False
    ins = MagicMock()
    ins.id = _id
    ins.learning = learning
    return ins


class TestHomeSurfacesInsights:
    @pytest.mark.asyncio
    async def test_stage4_surfaces_and_marks(self):
        journal = _mock_journal([_insight("i1", "the rail migration held"), _insight("i2", "tests stayed green")])
        svc = HomeStateService(journal=journal)
        res = await svc.generate_home_state(_ctx(TrustStage.TRUSTED))
        assert len(res.surfaced_insights) == 2
        assert all("text" in s and "id" in s for s in res.surfaced_insights)
        assert "the rail migration held" in res.surfaced_insights[0]["text"]
        # marked surfaced so they don't repeat
        assert journal.mark_surfaced.await_count == 2

    @pytest.mark.asyncio
    async def test_stage2_does_not_surface(self):
        journal = _mock_journal([_insight("i1", "should not surface")])
        svc = HomeStateService(journal=journal)
        res = await svc.generate_home_state(_ctx(TrustStage.BUILDING))
        assert res.surfaced_insights == []
        journal.get_unsurfaced.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_surfacing_failure_degrades_to_empty(self):
        journal = MagicMock()
        journal.get_unsurfaced = AsyncMock(side_effect=RuntimeError("db down"))
        svc = HomeStateService(journal=journal)
        res = await svc.generate_home_state(_ctx(TrustStage.TRUSTED))
        assert res.surfaced_insights == []  # greeting still works; no crash
        assert res.greeting  # greeting unaffected
