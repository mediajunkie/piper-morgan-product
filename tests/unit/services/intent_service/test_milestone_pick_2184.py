"""#2184 — the milestones list arms an exact-title milestone pick (Arch's four conditions, 12:45 10-28).

Halves under test, as the #1987 pick tests do: ``arm_milestone_pick`` (ARM), ``handle_milestone_pick_turn``
(ANSWER at the pop seam), ``run_clarify_milestone_pick_workflow`` (bare-affirmative landing), plus the two
code-bound scope keys the issues handler honours and the milestones handler's arm site (repo carried; no arm
on an empty read or when a remainder offer was armed).
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, call, patch

import pytest

from services.domain.models import Intent
from services.intent_service import milestone_pick as mp
from services.intent_service.workflow_dispatcher import get_registered_workflows
from services.intent_service.workflow_entries import register_default_workflows
from services.mcp.consumer.github_adapter import GitHubIssuesResult
from services.shared_types import EffectClass, IntentCategory

TITLES = ["MVP", "Production", "Beta Blockers - Hard Gates Only"]
REPO = "mediajunkie/piper-morgan-product"
_SESSION = "s2184"
_USER = "11111111-1111-1111-1111-111111111111"


class _Store:
    def __init__(self):
        self.slot = None
        self.calls = []

    def set_pending_offer(self, session_id, offer, user_id=None):
        self.slot = offer
        self.calls.append((session_id, offer, user_id))

    def get_and_clear_pending_offer(self, session_id, user_id=None):
        offer, self.slot = self.slot, None
        return offer


def _armed_record():
    store = _Store()
    assert mp.arm_milestone_pick(
        session_id=_SESSION,
        principal=_USER,
        offer_service=store,
        titles=TITLES,
        repository=REPO,
        original_message="can you show me issues from just one milestone?",
    )
    return store.slot


class TestNormalize:
    @pytest.mark.parametrize("raw", ["MVP", " mvp ", '"MVP"', "MVP.", "Mvp!", "`MVP`", "'MVP'?"])
    def test_exact_after_trimming(self, raw):
        assert mp.match_title(raw, TITLES) == "MVP"

    @pytest.mark.parametrize(
        "raw", ["MVP issues", "show MVP", "1", "2", "the first one", "", "   "]
    )
    def test_anything_else_does_not_bind(self, raw):
        assert mp.match_title(raw, TITLES) is None

    def test_multi_word_title_binds_whole(self):
        assert mp.match_title("beta blockers - hard gates only", TITLES) == TITLES[2]


class TestArm:
    def test_record_carries_titles_repo_and_kind(self):
        rec = _armed_record()
        pa = rec["pending_action"]
        assert rec["workflow_type"] == mp.MILESTONE_PICK_WORKFLOW
        assert pa["kind"] == mp.MILESTONE_PICK_KIND
        assert pa["pick_titles"] == TITLES and pa["repository"] == REPO and pa["user_id"] == _USER
        assert rec["question"] == ""  # silent arm: the list is the question

    def test_no_session_no_store_no_titles_does_not_arm(self):
        store = _Store()
        assert not mp.arm_milestone_pick(
            session_id=None,
            principal=_USER,
            offer_service=store,
            titles=TITLES,
            repository=REPO,
            original_message="x",
        )
        assert not mp.arm_milestone_pick(
            session_id=_SESSION,
            principal=_USER,
            offer_service=None,
            titles=TITLES,
            repository=REPO,
            original_message="x",
        )
        assert not mp.arm_milestone_pick(
            session_id=_SESSION,
            principal=_USER,
            offer_service=store,
            titles=[],
            repository=REPO,
            original_message="x",
        )
        assert store.slot is None


class TestAnswer:
    @pytest.mark.asyncio
    async def test_exact_title_runs_the_issues_read_with_milestone_and_repo_code_bound(self):
        rec = _armed_record()
        svc = SimpleNamespace(
            _handle_list_issues_query=AsyncMock(
                return_value=SimpleNamespace(
                    message='You have **3 open issues** in milestone "MVP".',
                    intent_data={"context": {}},
                )
            )
        )
        out = await mp.handle_milestone_pick_turn(
            rec, "MVP", session_id=_SESSION, user_id=_USER, intent_service=svc
        )
        assert out is not None and out["message"].startswith("You have **3 open issues**")
        intent = svc._handle_list_issues_query.await_args.args[0]
        assert intent.action == "list_issues_query"
        assert intent.context["list_scope_milestone"] == "MVP"
        assert intent.context["list_scope_repository"] == REPO
        assert svc._handle_list_issues_query.await_args.kwargs == {"session_id": _SESSION}

    @pytest.mark.asyncio
    async def test_non_title_falls_through(self):
        rec = _armed_record()
        svc = SimpleNamespace(_handle_list_issues_query=AsyncMock())
        for text in ["show me the rest", "1", "yes", "MVP issues please"]:
            assert (
                await mp.handle_milestone_pick_turn(
                    rec, text, session_id=_SESSION, user_id=_USER, intent_service=svc
                )
                is None
            )
        svc._handle_list_issues_query.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_foreign_kind_and_other_principal_fall_through(self):
        rec = _armed_record()
        svc = SimpleNamespace(_handle_list_issues_query=AsyncMock())
        assert (
            await mp.handle_milestone_pick_turn(
                {"pending_action": {"kind": "other"}},
                "MVP",
                session_id=_SESSION,
                user_id=_USER,
                intent_service=svc,
            )
            is None
        )
        assert (
            await mp.handle_milestone_pick_turn(
                rec, "MVP", session_id=_SESSION, user_id="someone-else", intent_service=svc
            )
            is None
        )
        svc._handle_list_issues_query.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_bare_yes_landing_reasks_and_rearms(self):
        rec = _armed_record()
        store = _Store()
        svc = SimpleNamespace(workflow_offer_service=store)
        out = await mp.run_clarify_milestone_pick_workflow(
            _SESSION, _USER, {"pending_action": rec["pending_action"], "intent_service": svc}
        )
        assert (
            out["message"]
            == mp.MILESTONE_PICK_REASK_QUESTION
            == "Which milestone? Say its name from the list above."
        )
        assert out["intent_data"][mp.PICK_PENDING_FLAG] is True
        assert (
            store.slot["pending_action"]["pick_titles"] == TITLES
            and store.slot["question"] == out["message"]
        )

    def test_landing_is_registered_read_and_not_action_triggered(self):
        register_default_workflows()
        entry = get_registered_workflows()[mp.MILESTONE_PICK_WORKFLOW]
        assert entry.effect == EffectClass.READ and entry.action_triggered is False


# ── the issues handler honours the code-bound keys; the milestones handler arms ──

_CONN = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.list_open_issues"
_NATIVE = "services.intent.intent_service.IntentService._get_github_router"


@pytest.fixture
def intent_service():
    from services.intent.intent_service import IntentService

    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


@pytest.mark.asyncio
async def test_issues_handler_honours_code_bound_scope_over_the_guard(intent_service):
    # The user said only "MVP"; the repo is not in their words. Code-bound keys still apply.
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_issues_query",
        context={
            "original_message": "MVP",
            "list_scope_milestone": "MVP",
            "list_scope_repository": REPO,
        },
    )
    intent.original_message = "MVP"
    page = [{"number": 2018, "title": "Settings", "labels": []}]
    with patch(_CONN, new=AsyncMock(return_value=GitHubIssuesResult(issues=page, total=3))) as stub:
        res = await intent_service._handle_list_issues_query(intent, "wf")
    assert stub.await_args == call(None, limit=50, repository=REPO, milestone="MVP")
    # CXO 13:04: singular confirmed on the code-bound path too.
    with patch(_CONN, new=AsyncMock(return_value=GitHubIssuesResult(issues=page, total=1))):
        one = await intent_service._handle_list_issues_query(intent, "wf")
    assert f'You have **1 open issue** in {REPO} in milestone "MVP".' in one.message
    # CXO 12:47: the header names the milestone AND the repo it was read in (Arch's condition 1).
    assert f'in {REPO} in milestone "MVP"' in res.message and "couldn't" not in res.message


def _milestones(n):
    return [{"title": t, "due_on": None, "open_issues": 3, "closed_issues": 1} for t in TITLES[:n]]


@pytest.mark.asyncio
async def test_milestones_handler_arms_with_the_listed_repo(intent_service):
    store = _Store()
    intent_service.workflow_offer_service = store
    router = MagicMock()
    router.initialize = AsyncMock()
    router.list_milestones_via_mcp = AsyncMock(return_value=_milestones(3))
    router._resolve_default_repo = AsyncMock(return_value=("mediajunkie", "piper-morgan-product"))
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_milestones_query",
        context={"original_message": "can you show me issues from just one milestone?"},
    )
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
        return_value=router,
    ):
        res = await intent_service._handle_list_milestones_query(intent, "wf", session_id=_SESSION)
    assert res.success and "MVP" in res.message
    assert res.intent_data[mp.PICK_PENDING_FLAG] is True
    pa = store.slot["pending_action"]
    assert (
        pa["kind"] == mp.MILESTONE_PICK_KIND
        and pa["pick_titles"] == TITLES
        and pa["repository"] == REPO
    )


@pytest.mark.asyncio
async def test_milestones_handler_does_not_arm_on_an_empty_read(intent_service):
    store = _Store()
    intent_service.workflow_offer_service = store
    router = MagicMock()
    router.initialize = AsyncMock()
    router.list_milestones_via_mcp = AsyncMock(return_value=[])
    router._resolve_default_repo = AsyncMock(return_value=("o", "r"))
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_milestones_query",
        context={"original_message": "show milestones"},
    )
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
        return_value=router,
    ):
        res = await intent_service._handle_list_milestones_query(intent, "wf", session_id=_SESSION)
    assert store.slot is None and mp.PICK_PENDING_FLAG not in res.intent_data


@pytest.mark.asyncio
async def test_milestones_handler_does_not_arm_when_the_repo_cannot_be_resolved(intent_service):
    # Arch's condition 1 (15:29 10-28): no repo, no arm — a repo-less bound read would be
    # assignee:@me across all repos and disagree with the counts just listed.
    store = _Store()
    intent_service.workflow_offer_service = store
    router = MagicMock()
    router.initialize = AsyncMock()
    router.list_milestones_via_mcp = AsyncMock(return_value=_milestones(3))
    router._resolve_default_repo = AsyncMock(return_value=None)
    intent = Intent(
        category=IntentCategory.QUERY,
        action="list_milestones_query",
        context={"original_message": "show milestones"},
    )
    with patch(
        "services.integrations.github.github_integration_router.GitHubIntegrationRouter",
        return_value=router,
    ):
        res = await intent_service._handle_list_milestones_query(intent, "wf", session_id=_SESSION)
    assert res.success and store.slot is None and mp.PICK_PENDING_FLAG not in res.intent_data
