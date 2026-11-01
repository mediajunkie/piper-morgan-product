"""#2250 (PPM 2026-11-01 12:35; Arch's allowed shape 12:10): on the status branch the
milestones read + resolver run CONCURRENTLY with the floor's context gather; a resolved
milestone discards the gather (no floor text reaches the reply, the floor is never
called); none / failed leave today's path: the gather's context reaches the floor.
No wording gate: the task starts on the router's pick (STATUS, get_project_status)."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.conversational_floor import FloorResponse
from services.shared_types import IntentCategory

pytestmark = pytest.mark.asyncio

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
FLOOR_RESPOND = "services.intent_service.conversational_floor.ConversationalFloor.respond"
GATHER = "services.intent_service.context_assembler.ContextAssembler.gather_context"

_USER = "22502250-2250-4250-8250-000000002250"
FLOOR_TEXT = "FLOOR: the project as a whole."
ASK = "what's the progress on the MVP milestone?"
READ: List[Dict[str, Any]] = [
    {
        "title": "MVP",
        "state": "open",
        "due_on": "2026-11-20T00:00:00Z",
        "open_issues": 4,
        "closed_issues": 6,
    },
    {
        "title": "Production",
        "state": "open",
        "due_on": "2026-12-15T00:00:00Z",
        "open_issues": 9,
        "closed_issues": 1,
    },
]
GATHERED = {"active_milestones": [], "status": "whole project"}


class _Store:
    def __init__(self):
        self.slot = None

    def set_pending_offer(self, session_id, offer, user_id=None):
        self.slot = offer

    def get_and_clear_pending_offer(self, session_id, user_id=None):
        offer, self.slot = self.slot, None
        return offer

    def peek_pending_offer(self, session_id, user_id=None):
        return self.slot


class GatedLLM:
    """The resolver's LLM: its reply waits until the gather has STARTED. In the
    serial shape (resolver first, gather after) this times out → outcome failed →
    the floor renders; in the concurrent shape it answers and the render returns."""

    def __init__(self, reply: str, gather_started: asyncio.Event):
        self.reply, self.gather_started, self.calls = reply, gather_started, []

    async def complete(self, **kwargs):
        self.calls.append(kwargs)
        await asyncio.wait_for(self.gather_started.wait(), timeout=1.0)
        kwargs["served"]["usage"] = {"input_tokens": 400, "output_tokens": 8}
        return self.reply


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            svc = IntentService()
    svc.workflow_offer_service = _Store()
    return svc


def _router(read=READ):
    r = MagicMock()
    r.initialize = AsyncMock()
    r.list_milestones_via_mcp = AsyncMock(return_value=[dict(m) for m in read])
    r._resolve_default_repo = AsyncMock(return_value=("mediajunkie", "piper-morgan-product"))
    return r


def _intent(message=ASK):
    return Intent(
        category=IntentCategory.STATUS,
        action="get_project_status",
        confidence=0.9,
        original_message=message,
        context={"original_message": message, "user_id": _USER},
    )


def _floor_and_gather(gather_started: asyncio.Event, gather_raises=None):
    respond = AsyncMock(return_value=FloorResponse(message=FLOOR_TEXT))

    async def gather(*args, **kwargs):
        gather_started.set()
        await asyncio.sleep(0)
        if gather_raises is not None:
            raise gather_raises
        return dict(GATHERED)

    gather_mock = AsyncMock(side_effect=gather)
    return respond, gather_mock


class TestConcurrentStatusBranch:
    async def test_resolver_runs_while_the_gather_runs_and_a_pick_discards_the_gather(
        self, service
    ):
        started = asyncio.Event()
        llm = GatedLLM('{"indices": [0]}', started)
        respond, gather = _floor_and_gather(started)
        service.llm_client = llm
        with (
            patch(ROUTER, return_value=_router()),
            patch(FLOOR_RESPOND, new=respond),
            patch(GATHER, new=gather),
        ):
            res = await service._handle_floor_with_context(_intent(), "s2250", user_id=_USER)
        # Concurrency: the resolver's reply was gated on the gather having started.
        assert len(llm.calls) == 1
        gather.assert_awaited_once()
        # The pick discards the gather: no floor call, no floor text in the reply.
        respond.assert_not_awaited()
        assert res.message.startswith(
            "**MVP**: 6 of 10 issues closed, 4 still open. Due 2026-11-20."
        )
        assert FLOOR_TEXT not in res.message

    async def test_none_lets_the_gathered_context_reach_the_floor_as_today(self, service):
        started = asyncio.Event()
        llm = GatedLLM('{"index": null}', started)
        respond, gather = _floor_and_gather(started)
        service.llm_client = llm
        with (
            patch(ROUTER, return_value=_router()),
            patch(FLOOR_RESPOND, new=respond),
            patch(GATHER, new=gather),
        ):
            res = await service._handle_floor_with_context(_intent(), "s2250", user_id=_USER)
        respond.assert_awaited_once()
        floor_ctx = respond.await_args.args[0]
        assert floor_ctx.domain_context == GATHERED, "today's context reaches the floor"
        assert res.message == FLOOR_TEXT

    async def test_gather_failure_after_a_pick_still_answers_with_the_render(self, service):
        started = asyncio.Event()
        llm = GatedLLM('{"indices": [1]}', started)
        respond, gather = _floor_and_gather(started, gather_raises=RuntimeError("gather down"))
        service.llm_client = llm
        with (
            patch(ROUTER, return_value=_router()),
            patch(FLOOR_RESPOND, new=respond),
            patch(GATHER, new=gather),
        ):
            res = await service._handle_floor_with_context(_intent(), "s2250", user_id=_USER)
        respond.assert_not_awaited()
        assert res.message.startswith("**Production**: 1 of 10 issues closed, 9 still open.")

    async def test_gather_failure_with_no_pick_propagates_and_leaves_no_dangling_task(
        self, service
    ):
        started = asyncio.Event()
        llm = GatedLLM('{"index": null}', started)
        respond, gather = _floor_and_gather(started, gather_raises=RuntimeError("gather down"))
        service.llm_client = llm
        with (
            patch(ROUTER, return_value=_router()),
            patch(FLOOR_RESPOND, new=respond),
            patch(GATHER, new=gather),
        ):
            with pytest.raises(RuntimeError, match="gather down"):
                await service._handle_floor_with_context(_intent(), "s2250", user_id=_USER)
        # The resolver task was awaited to completion before the failure propagated.
        assert len(llm.calls) == 1
        pending = [
            t for t in asyncio.all_tasks() if not t.done() and t is not asyncio.current_task()
        ]
        assert not pending, f"dangling tasks: {pending}"

    async def test_no_task_starts_for_another_action(self, service):
        started = asyncio.Event()
        llm = GatedLLM('{"indices": [0]}', started)
        respond, gather = _floor_and_gather(started)
        service.llm_client = llm
        other = Intent(
            category=IntentCategory.STATUS,
            action="check_completion_status",
            confidence=0.9,
            original_message=ASK,
            context={"original_message": ASK, "user_id": _USER},
        )
        with (
            patch(ROUTER, return_value=_router()) as ctor,
            patch(FLOOR_RESPOND, new=respond),
            patch(GATHER, new=gather),
        ):
            res = await service._handle_floor_with_context(other, "s2250", user_id=_USER)
        ctor.assert_not_called()
        assert llm.calls == []
        assert res.message == FLOOR_TEXT


class HangingLLM:
    """A resolver whose call never returns; records whether it was cancelled."""

    def __init__(self):
        self.cancelled = False
        self.calls = 0

    async def complete(self, **kwargs):
        self.calls += 1
        try:
            await asyncio.Event().wait()
        except asyncio.CancelledError:
            self.cancelled = True
            raise


class TestCancelledTurnStaysCancelled:
    async def test_cancel_during_the_gather_cancels_the_resolver_and_propagates(self, service):
        """Arch 2026-11-01 13:13: a turn cancelled mid-gather must not wait on the
        resolver, and a resolver pick must not swallow the cancellation."""
        llm = HangingLLM()
        respond = AsyncMock(return_value=FloorResponse(message=FLOOR_TEXT))
        gather_entered = asyncio.Event()

        async def hanging_gather(*args, **kwargs):
            gather_entered.set()
            await asyncio.Event().wait()

        service.llm_client = llm
        with (
            patch(ROUTER, return_value=_router()),
            patch(FLOOR_RESPOND, new=respond),
            patch(GATHER, new=AsyncMock(side_effect=hanging_gather)),
        ):
            turn = asyncio.ensure_future(
                service._handle_floor_with_context(_intent(), "s2250", user_id=_USER)
            )
            await asyncio.wait_for(gather_entered.wait(), timeout=1.0)
            await asyncio.sleep(0)  # the resolver task reaches its call
            turn.cancel()
            with pytest.raises(asyncio.CancelledError):
                await turn
            await asyncio.sleep(0)  # the inner cancellation is delivered
        assert llm.calls == 1 and llm.cancelled is True, "the resolver task was cancelled"
        respond.assert_not_awaited()
        pending = [
            t for t in asyncio.all_tasks() if not t.done() and t is not asyncio.current_task()
        ]
        assert not pending, f"dangling tasks: {pending}"
