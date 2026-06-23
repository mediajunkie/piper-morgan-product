"""#1269 — GET /api/v1/standup/today serves the honest DERIVED standup (StandupAssembler),
parallel to the legacy POST /generate (no contract change there). Tests the route wiring
(auth → assembler → prose+summary response) with the assembler glue patched; the glue +
assembler themselves are tested in tests/unit/services/standup/.
"""

from __future__ import annotations

from types import SimpleNamespace

import services.standup.assembler as asm
from services.domain.models import StandupItem, StandupSummary
from web.api.routes.standup import get_today_standup


async def test_today_returns_prose_and_structured_summary(monkeypatch):
    known = StandupSummary(
        yesterday=[
            StandupItem(display="auth PR", source="radar:work_item", lifecycle_state="closed")
        ],
        today=[StandupItem(display="onboarding", source="radar:work_item", lifecycle_state="open")],
    )

    async def fake_build(user_id):
        assert user_id == "u-1"  # scopes to the authenticated user
        return known

    monkeypatch.setattr(asm, "build_user_standup_summary", fake_build)

    res = await get_today_standup(current_user=SimpleNamespace(sub="u-1"))
    assert "**Today**" in res.prose and "onboarding" in res.prose
    assert res.summary["yesterday"][0]["display"] == "auth PR"
    assert res.summary["today"][0]["display"] == "onboarding"


async def test_today_anonymous_is_honest_empty(monkeypatch):
    async def fake_build(user_id):
        assert user_id is None  # anonymous → no user
        return StandupSummary()

    monkeypatch.setattr(asm, "build_user_standup_summary", fake_build)

    res = await get_today_standup(current_user=None)
    assert "Nothing to show yet" in res.prose
    assert res.summary == {"yesterday": [], "today": [], "watch": []}
