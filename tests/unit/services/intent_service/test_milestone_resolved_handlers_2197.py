"""#2197 — a progress ask about a named milestone is answered about THAT milestone, by code.

The status branch in ``_handle_floor_with_context`` (get_project_status under STATUS only), the
list branch in ``_handle_list_milestones_query``, and the one-title accept on the #2184 pick's
re-ask landing. The resolver's model is a fake whose ``complete`` returns canned JSON; GitHub is
a stub router; the floor's model and context assembly are AsyncMocks that record every call.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any, Dict, List
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.integrations.github.read_failed import GitHubReadFailed
from services.intent.intent_service import IntentService
from services.intent_service import milestone_pick as mp
from services.intent_service import milestone_render as mr
from services.intent_service.conversational_floor import FloorResponse
from services.llm.request_key import UnboundLLMKeyError
from services.mcp.consumer.connector import DegradationReason
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
FLOOR_RESPOND = "services.intent_service.conversational_floor.ConversationalFloor.respond"
GATHER = "services.intent_service.context_assembler.ContextAssembler.gather_context"

_USER = "21972197-2197-4197-8197-000000002197"
_REPO = "mediajunkie/piper-morgan-product"
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
    {
        "title": "Alpha",
        "state": "closed",
        "due_on": "2026-09-01T00:00:00Z",
        "open_issues": 0,
        "closed_issues": 12,
    },
]


class FakeLLM:
    def __init__(self, reply=None, raises=None):
        self.reply, self.raises, self.calls = reply, raises, []

    async def complete(self, **kwargs):
        self.calls.append(kwargs)
        if self.raises is not None:
            raise self.raises
        kwargs["served"]["usage"] = {"input_tokens": 400, "output_tokens": 8}
        return self.reply


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


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            svc = IntentService()
    svc.workflow_offer_service = _Store()
    return svc


@pytest.fixture
def floor():
    respond = AsyncMock(return_value=FloorResponse(message=FLOOR_TEXT))
    gather = AsyncMock(return_value={"active_milestones": [], "status": "whole project"})
    with patch(FLOOR_RESPOND, new=respond), patch(GATHER, new=gather):
        yield SimpleNamespace(respond=respond, gather=gather)


def _router(read=READ, repo=("mediajunkie", "piper-morgan-product"), raises=None):
    r = MagicMock()
    r.initialize = AsyncMock()
    r.list_milestones_via_mcp = (
        AsyncMock(side_effect=raises) if raises else AsyncMock(return_value=[dict(m) for m in read])
    )
    r._resolve_default_repo = AsyncMock(return_value=repo)
    return r


def _status_intent(message=ASK, category=IntentCategory.STATUS, action="get_project_status"):
    return Intent(
        category=category,
        action=action,
        confidence=0.9,
        original_message=message,
        context={"original_message": message, "user_id": _USER},
    )


async def _status(service, router, llm, intent=None, sid="s2197"):
    service.llm_client = llm
    with patch(ROUTER, return_value=router) as ctor:
        res = await service._handle_floor_with_context(
            intent or _status_intent(), sid, user_id=_USER
        )
    return res, ctor


@pytest.mark.asyncio
class TestStatusBranch:
    async def test_picked_renders_the_read_and_never_calls_the_floor(self, service, floor):
        router = _router()
        llm = FakeLLM('{"indices": [0], "title": "INVENTED BY MODEL"}')
        res, _ = await _status(service, router, llm)
        # CXO's pins: title and counts from the read; no model text; due date part exactly.
        assert res.message == (
            "**MVP**: 6 of 10 issues closed, 4 still open. Due 2026-11-20.\n\n"
            "Want to see the open issues?"
        )
        assert "INVENTED" not in res.message and "2026-11-19" not in res.message
        # Arch's condition: the floor and the context assembler are not called on this branch.
        floor.respond.assert_not_awaited()
        floor.gather.assert_not_awaited()
        assert "floor_hit" not in res.intent_data
        router.list_milestones_via_mcp.assert_awaited_once_with(state="all")
        # The one-title pick is armed with the read's title and repo.
        pa = service.workflow_offer_service.slot["pending_action"]
        assert pa["pick_titles"] == ["MVP"] and pa["repository"] == _REPO
        assert pa[mp.ORIGIN_KEY] == mp.ORIGIN_RESOLVED and pa["user_id"] == _USER
        assert res.intent_data[mp.PICK_PENDING_FLAG] is True
        assert llm.calls[0]["user_id"] == _USER

    async def test_picked_closed_milestone_has_no_offer(self, service, floor):
        res, _ = await _status(service, _router(), FakeLLM('{"indices": [2]}'))
        assert res.message == "**Alpha** is closed: 12 of 12 issues done."
        assert service.workflow_offer_service.slot is None
        floor.respond.assert_not_awaited()

    async def test_picked_with_no_repo_renders_without_offer_or_arm(self, service, floor):
        res, _ = await _status(service, _router(repo=None), FakeLLM('{"indices": [1]}'))
        assert res.message == "**Production**: 1 of 10 issues closed, 9 still open. Due 2026-12-15."
        assert mr.OPEN_ISSUES_OFFER_QUESTION not in res.message
        assert service.workflow_offer_service.slot is None

    @pytest.mark.parametrize(
        "reply,line",
        [
            ('{"index": null, "named_absent": true, "title": "Gamma"}', mr.NAMED_ABSENT_LINE),
            ('{"indices": [0, 1]}', mr.TIE_LINE),
        ],
    )
    async def test_named_absent_and_tie_prefix_the_floors_whole_project_answer(
        self, service, floor, reply, line
    ):
        res, _ = await _status(service, _router(), FakeLLM(reply))
        assert res.message == f"{line}\n{mr.STATUS_LEAD_IN}\n\n{FLOOR_TEXT}"
        assert "Gamma" not in res.message  # never the model's string
        floor.respond.assert_awaited_once()
        # The floor receives nothing new: the assembler's own context, untouched.
        floor_ctx = floor.respond.await_args.args[0]
        assert floor_ctx.domain_context == {"active_milestones": [], "status": "whole project"}
        assert service.workflow_offer_service.slot is None

    async def test_next_is_codes_earliest_due_open_whatever_index_the_model_sends(
        self, service, floor
    ):
        res, _ = await _status(
            service,
            _router(),
            FakeLLM('{"selector": "next", "indices": [1]}'),
            intent=_status_intent("any update on the next milestone"),
        )
        assert res.message.startswith("**MVP**: 6 of 10 issues closed")
        floor.respond.assert_not_awaited()

    async def test_next_with_undated_or_tied_earliest_is_the_tie_default(self, service, floor):
        undated = [dict(m, due_on=None) for m in READ]
        res, _ = await _status(
            service,
            _router(read=undated),
            FakeLLM('{"selector": "next"}'),
            intent=_status_intent("any update on the next milestone"),
        )
        assert res.message == f"{mr.TIE_LINE}\n{mr.STATUS_LEAD_IN}\n\n{FLOOR_TEXT}"

    @pytest.mark.parametrize("reply", ['{"index": null}', '{"indices": [9]}', "not json"])
    async def test_none_and_failed_are_the_silent_default(self, service, floor, reply):
        res, _ = await _status(service, _router(), FakeLLM(reply))
        assert res.message == FLOOR_TEXT and res.intent_data["floor_hit"] is True

    async def test_key_refusal_is_failed_and_the_floor_renders(self, service, floor):
        res, _ = await _status(service, _router(), FakeLLM(raises=UnboundLLMKeyError("no key")))
        assert res.message == FLOOR_TEXT

    @pytest.mark.parametrize(
        "exc",
        [
            GitHubReadFailed("down", DegradationReason.UNREACHABLE, detail="no_response"),
            GitHubReadFailed("not connected", DegradationReason.CONNECT_REQUIRED),
        ],
    )
    async def test_failed_or_not_performed_read_makes_no_call(self, service, floor, exc):
        llm = FakeLLM('{"indices": [0]}')
        res, _ = await _status(service, _router(raises=exc), llm)
        assert res.message == FLOOR_TEXT and llm.calls == []

    async def test_empty_read_makes_no_call(self, service, floor):
        llm = FakeLLM('{"indices": [0]}')
        res, _ = await _status(service, _router(read=[]), llm)
        assert res.message == FLOOR_TEXT and llm.calls == []

    @pytest.mark.parametrize(
        "category,action",
        [
            (IntentCategory.STATUS, "check_completion_status"),
            (IntentCategory.QUERY, "get_project_status"),
            (IntentCategory.DISCOVERY, "get_capabilities"),
            (IntentCategory.CONVERSATION, "chitchat"),
        ],
    )
    async def test_skipped_for_every_other_action(self, service, floor, category, action):
        llm = FakeLLM('{"indices": [0]}')
        res, ctor = await _status(
            service, _router(), llm, intent=_status_intent(ASK, category, action)
        )
        assert res.message == FLOOR_TEXT and llm.calls == []
        ctor.assert_not_called()

    async def test_skipped_for_guidance(self, service, floor):
        llm = FakeLLM('{"indices": [0]}')
        intent = _status_intent(ASK, IntentCategory.GUIDANCE, "get_project_status")
        with patch.object(service, "_assemble_guidance_context", new=AsyncMock(return_value={})):
            res, ctor = await _status(service, _router(), llm, intent=intent)
        assert res.message == FLOOR_TEXT and llm.calls == []
        ctor.assert_not_called()


# ── the list branch ──


async def _list(service, router, llm, message, sid="s2197-list"):
    service.llm_client = llm
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_milestones_query",
        original_message=message,
        context={"original_message": message, "user_id": _USER},
    )
    with patch(ROUTER, return_value=router):
        return await service._handle_list_milestones_query(intent, "wf", session_id=sid)


OPEN_READ = [m for m in READ if m["state"] == "open"]


@pytest.mark.asyncio
class TestListBranch:
    async def test_none_keeps_todays_list_arm_and_question(self, service):
        res = await _list(
            service, _router(read=OPEN_READ), FakeLLM('{"index": null}'), "list my milestones"
        )
        assert res.message.startswith("You have **2 open milestones**.")
        assert res.message.endswith("\n\n" + mp.MILESTONE_PICK_ARM_QUESTION)
        assert service.workflow_offer_service.slot["pending_action"]["pick_titles"] == [
            "MVP",
            "Production",
        ]
        assert (
            service.workflow_offer_service.slot["pending_action"][mp.ORIGIN_KEY] == mp.ORIGIN_LIST
        )

    async def test_failed_keeps_todays_list(self, service):
        res = await _list(
            service,
            _router(read=OPEN_READ),
            FakeLLM(raises=UnboundLLMKeyError("x")),
            "list my milestones",
        )
        assert res.message.startswith("You have **2 open milestones**.")

    async def test_next_renders_one_milestone_with_the_one_title_offer(self, service):
        res = await _list(
            service,
            _router(read=OPEN_READ),
            FakeLLM('{"selector": "next"}'),
            "what's the next milestone?",
        )
        assert res.message == (
            "**MVP**: 6 of 10 issues closed, 4 still open. Due 2026-11-20.\n\nWant to see the open issues?"
        )
        assert res.intent_data["action"] == "list_milestones_query"
        assert service.workflow_offer_service.slot["pending_action"]["pick_titles"] == ["MVP"]

    async def test_picked_renders_one_milestone(self, service):
        res = await _list(
            service, _router(read=OPEN_READ), FakeLLM('{"indices": [1]}'), "when's Production due"
        )
        assert res.message.startswith(
            "**Production**: 1 of 10 issues closed, 9 still open. Due 2026-12-15."
        )

    @pytest.mark.parametrize(
        "reply,line",
        [
            ('{"index": null, "named_absent": true}', mr.NAMED_ABSENT_LINE),
            ('{"indices": [0, 1]}', mr.TIE_LINE),
        ],
    )
    async def test_named_absent_and_tie_prefix_todays_list(self, service, reply, line):
        res = await _list(
            service, _router(read=OPEN_READ), FakeLLM(reply), "when's the Gamma milestone due"
        )
        assert res.message.startswith(
            f"{line}\n{mr.LIST_LEAD_IN}\n\nYou have **2 open milestones**."
        )


# ── the one-title accept (Lead's design inside the ruled shape) ──


def _one_title_record(principal=_USER):
    store = _Store()
    assert mp.arm_milestone_pick(
        session_id="s1",
        principal=principal,
        offer_service=store,
        titles=["MVP"],
        repository=_REPO,
        original_message=ASK,
        origin=mp.ORIGIN_RESOLVED,
    )
    return store.slot


def _issues_service():
    return SimpleNamespace(
        _handle_list_issues_query=AsyncMock(
            return_value=SimpleNamespace(
                message='You have **4 open issues** in milestone "MVP".', intent_data={}
            )
        ),
        workflow_offer_service=_Store(),
        _milestone_pick_no_match={},
    )


@pytest.mark.asyncio
class TestOneTitleAccept:
    async def test_bare_affirmative_runs_the_bound_read_for_the_one_title(self):
        rec = _one_title_record()
        svc = _issues_service()
        out = await mp.run_clarify_milestone_pick_workflow(
            "s1", _USER, {"pending_action": rec["pending_action"], "intent_service": svc}
        )
        assert out["message"].startswith("You have **4 open issues**")
        intent = svc._handle_list_issues_query.await_args.args[0]
        assert intent.context["list_scope_milestone"] == "MVP"
        assert intent.context["list_scope_repository"] == _REPO
        assert svc.workflow_offer_service.slot is None  # no re-ask

    async def test_another_principal_binds_nothing(self):
        rec = _one_title_record()
        svc = _issues_service()
        out = await mp.run_clarify_milestone_pick_workflow(
            "s1", "someone-else", {"pending_action": rec["pending_action"], "intent_service": svc}
        )
        assert out is None
        svc._handle_list_issues_query.assert_not_awaited()

    async def test_exact_title_still_binds(self):
        rec = _one_title_record()
        svc = _issues_service()
        out = await mp.handle_milestone_pick_turn(rec, "mvp", "s1", _USER, svc)
        assert out is not None
        assert (
            svc._handle_list_issues_query.await_args.args[0].context["list_scope_milestone"]
            == "MVP"
        )

    async def test_anything_else_falls_through_and_sets_no_no_match_marker(self):
        rec = _one_title_record()
        svc = _issues_service()
        out = await mp.handle_milestone_pick_turn(rec, "what about Production?", "s1", _USER, svc)
        assert out is None and svc._milestone_pick_no_match == {}
        svc._handle_list_issues_query.assert_not_awaited()

    async def test_a_multi_title_pick_still_reasks(self):
        store = _Store()
        mp.arm_milestone_pick(
            session_id="s1",
            principal=_USER,
            offer_service=store,
            titles=["MVP", "Production"],
            repository=_REPO,
            original_message="x",
        )
        svc = _issues_service()
        out = await mp.run_clarify_milestone_pick_workflow(
            "s1", _USER, {"pending_action": store.slot["pending_action"], "intent_service": svc}
        )
        assert out["message"] == mp.MILESTONE_PICK_REASK_QUESTION
        svc._handle_list_issues_query.assert_not_awaited()
