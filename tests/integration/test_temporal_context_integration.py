"""Temporal context — current-contract suite (#1452 wave 5 rewrite, 2026-07-21).

The original PM-034-era file (460 lines) tested a ConversationQueryService
shape that no longer exists: `get_focus_guidance`, `_format_calendar_context`,
`_get_calendar_from_mcp`, mock-calendar dynamic integration, and
temporal-awareness pins on STATUS/PRIORITY canonical handlers (whose honest
replacements deliberately answer differently). This rewrite pins what the LIVE
system does:

- CanonicalHandlers TEMPORAL: the honest "Today is <date>." answer
- CanonicalHandlers GUIDANCE: time-of-day-aware framing

2026-08-30 surgery (Batch-2 census-dead-family disposal): the
TestTemporalContextService half (5 tests pinning ConversationQueryService
directly) was excised when services/queries/ was disposed — the census +
fresh delete-time sweep found ZERO production callers of the service; the
2026-07-21 rewrite's "LIVE system" framing was true of the handlers, not
the service. The CanonicalHandlers half below is the live-path coverage
and is unchanged. Disposed module retrievable by commit hash per the
disposal record in decisions.log.

Pruned tests and what they pinned (delete-record discipline):
get_focus_guidance ×5 (method removed), _format_calendar_context ×3 (removed),
_get_calendar_from_mcp readiness ×2 (removed), get_time_aware_priority ×1
(removed), mock-calendar dynamic formatting ×2 (the dynamic-calendar path never
shipped; the service reads static PIPER.md patterns), STATUS/PRIORITY handler
temporal-awareness ×2 (contract deliberately changed), performance targets ×1
(pinned removed methods' latency).
"""

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.canonical_handlers import CanonicalHandlers


@pytest.fixture
def handlers():
    return CanonicalHandlers()


@pytest.mark.asyncio
class TestCanonicalHandlersTemporal:
    async def test_temporal_handler_answers_today(self, handlers):
        intent = Intent(
            category=IntentCategory.TEMPORAL,
            action="get_temporal_context",
            confidence=0.9,
            context={"query": "What day is it?"},
        )
        out = await handlers.handle(intent, session_id="t-temporal", user_id=None)
        msg = out["message"] if isinstance(out, dict) else str(out)
        assert msg.startswith("Today is ")
        # timezone-agnostic (#1452: the handler answers in PT; the CI runner's
        # local day is UTC and can differ — asserting the runner's weekday
        # name was itself a clock bug). Pin the shape, not the day.
        import re as _re

        assert _re.search(
            r"Today is (Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday), ", msg
        )

    async def test_guidance_handler_is_time_of_day_aware(self, handlers):
        intent = Intent(
            category=IntentCategory.GUIDANCE,
            action="get_guidance",
            confidence=0.9,
            context={"query": "what should I focus on"},
        )
        out = await handlers.handle(intent, session_id="t-guidance", user_id=None)
        msg = out["message"] if isinstance(out, dict) else str(out)
        assert "Right Now" in msg or "time of day" in msg
