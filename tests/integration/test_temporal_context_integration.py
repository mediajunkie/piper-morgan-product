"""Temporal context — current-contract suite (#1452 wave 5 rewrite, 2026-07-21).

The original PM-034-era file (460 lines) tested a ConversationQueryService
shape that no longer exists: `get_focus_guidance`, `_format_calendar_context`,
`_get_calendar_from_mcp`, mock-calendar dynamic integration, and
temporal-awareness pins on STATUS/PRIORITY canonical handlers (whose honest
replacements deliberately answer differently). This rewrite pins what the LIVE
system does:

- ConversationQueryService.get_temporal_context: time + day + week + PIPER.md
  calendar patterns (static; no MCP path exists in the service anymore)
- ConversationQueryService.get_guidance: temporal-aware guidance text
- CanonicalHandlers TEMPORAL: the honest "Today is <date>." answer
- CanonicalHandlers GUIDANCE: time-of-day-aware framing

Pruned tests and what they pinned (delete-record discipline):
get_focus_guidance ×5 (method removed), _format_calendar_context ×3 (removed),
_get_calendar_from_mcp readiness ×2 (removed), get_time_aware_priority ×1
(removed), mock-calendar dynamic formatting ×2 (the dynamic-calendar path never
shipped; the service reads static PIPER.md patterns), STATUS/PRIORITY handler
temporal-awareness ×2 (contract deliberately changed), performance targets ×1
(pinned removed methods' latency).
"""

from datetime import datetime

import pytest

from services.domain.models import Intent, IntentCategory
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.queries.conversation_queries import ConversationQueryService


@pytest.fixture
def service():
    return ConversationQueryService()


@pytest.fixture
def handlers():
    return CanonicalHandlers()


@pytest.mark.asyncio
class TestTemporalContextService:
    async def test_temporal_context_has_time_day_week(self, service):
        out = await service.get_temporal_context()
        assert "**Current Time**:" in out
        assert "**Day of Week**:" in out
        assert f"**Week**: Week {datetime.now().isocalendar()[1]}" in out

    async def test_temporal_context_reports_today(self, service):
        out = await service.get_temporal_context()
        assert datetime.now().strftime("%A") in out

    async def test_calendar_patterns_included_when_configured(self, service):
        """PIPER.md's Calendar Patterns section rides along when present —
        static config, the only calendar source the service has."""
        out = await service.get_temporal_context()
        config = service.config_loader.load_config()
        if config and config.get("Calendar Patterns", ""):
            assert "**Calendar Context**:" in out
        else:
            assert "**Calendar Context**:" not in out

    async def test_guidance_is_time_aware(self, service):
        out = await service.get_guidance()
        assert out and len(out) > 0
        # the guidance surface frames by time-of-day context
        assert "Guidance" in out or "Right Now" in out

    async def test_core_query_methods_alive(self, service):
        """The service's stable public surface answers non-empty."""
        for method in ("get_greeting", "get_help", "get_status", "get_identity"):
            out = await getattr(service, method)()
            assert out and len(out) > 0, method


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
        assert datetime.now().strftime("%A") in msg

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
