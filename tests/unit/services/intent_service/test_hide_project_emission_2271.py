"""#2271 (Arch 11-06 11:26; CXO's words): with the surface-1 hide literal absent, the
legacy classifier emits ``execution/hide_project`` for "hide the project Beta" (10/10),
an invented op that reached the generic decline.

The fix is the #1527 alias discipline: ``hide_project`` is a rail alias of the
archive_project entry and inherits every gate. On that emission the archive handler
resolves the project by EXACT name (case-insensitive) among the person's own active
projects: one match archives it and says how to restore it; none archives nothing;
several archive nothing and ask which, armed (the #1987 shape, ids bound at ask time).

These drive the REAL ``process_intent`` and classifier chain with only the LLM boundary
pinned; the database is replaced by an in-memory portfolio (``PortfolioService`` read
and write methods and the session scope), so every archive call is recorded. The
surface-1 hide literal (``PreClassifier.PORTFOLIO_PATTERNS``) is removed for the
emission tests, the condition under which the classifier emits ``hide_project``.
"""

import contextlib
import json
from types import SimpleNamespace

import pytest

from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.project_archive_pick import (
    PROJECT_ARCHIVE_PICK_KIND,
    exact_matches,
    name_candidates,
)
from services.intent_service.unwired_writes import GENERIC_UNWIRED_WRITE_DECLINE
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2271-4b00-9e00-00000000a271"


class _PinnedEmissionLLM:
    def __init__(self, action="hide_project"):
        self._payload = json.dumps(
            {
                "category": "execution",
                "action": action,
                "confidence": 0.9,
                "reasoning": "hide a project",
            }
        )

    async def complete(self, task_type=None, **kwargs):
        if task_type != "intent_classification":
            raise AssertionError(f"LLM boundary touched for task_type={task_type!r}")
        return self._payload


def _project(pid, name, archived=False):
    return SimpleNamespace(id=pid, name=name, owner_id=_USER, is_archived=archived)


@pytest.fixture
def portfolio(monkeypatch):
    """An in-memory portfolio behind the real PortfolioService method names."""
    from services.database import session_factory
    from services.onboarding import portfolio_service as ps

    state = {"projects": [], "archived": []}

    @contextlib.asynccontextmanager
    async def _scope(*args, **kwargs):
        yield SimpleNamespace()

    async def _active(self, user_id):
        assert user_id == _USER
        return [p for p in state["projects"] if not p.is_archived]

    async def _get(self, project_id, user_id):
        return next(
            (p for p in state["projects"] if p.id == project_id and p.owner_id == user_id), None
        )

    async def _archive(self, project_id, user_id):
        project = await _get(self, project_id, user_id)
        project.is_archived = True
        state["archived"].append(project_id)
        return ps.PortfolioResult(
            status=ps.PortfolioActionResult.SUCCESS,
            project=project,
            message=f"I've archived {project.name}. You can restore it anytime.",
        )

    async def _find(self, name, user_id, include_archived=False):
        raise AssertionError("hide_project must not use the tolerant find_project_by_name")

    monkeypatch.setattr(session_factory.AsyncSessionFactory, "session_scope", _scope)
    monkeypatch.setattr(ps.PortfolioService, "list_active_projects", _active)
    monkeypatch.setattr(ps.PortfolioService, "get_project", _get)
    monkeypatch.setattr(ps.PortfolioService, "archive_project", _archive)
    monkeypatch.setattr(ps.PortfolioService, "find_project_by_name", _find)
    return state


@pytest.fixture
def hide_literal_absent(monkeypatch):
    from services.intent_service.pre_classifier import PreClassifier

    kept = [p for p in PreClassifier.PORTFOLIO_PATTERNS if not p.startswith(r"\bhide\s+")]
    assert len(kept) == len(PreClassifier.PORTFOLIO_PATTERNS) - 1
    monkeypatch.setattr(PreClassifier, "PORTFOLIO_PATTERNS", kept)


def _service(action="hide_project"):
    register_default_workflows()
    return IntentService(intent_classifier=IntentClassifier(llm_service=_PinnedEmissionLLM(action)))


def test_hide_project_is_the_archive_project_entry():
    register_default_workflows()
    wf = get_action_workflows()
    assert wf["hide_project"] is wf["archive_project"]


def test_exact_name_resolution_is_whole_name_case_insensitive():
    projects = [
        _project("1", "Beta"),
        _project("2", "Beta Launch"),
        _project("3", "alphabet"),
        _project("4", "zz share-hide project"),
    ]
    assert [p.id for p in exact_matches(projects, "the project Beta")] == ["1"]
    assert [p.id for p in exact_matches(projects, "BETA please")] == ["1"]
    assert exact_matches(projects, "bet") == []  # no prefix/substring match
    assert exact_matches(projects, "launch") == []
    assert [p.id for p in exact_matches(projects, "zz share-hide project")] == ["4"]
    assert "beta" in name_candidates("the project Beta")


@pytest.mark.asyncio
async def test_one_exact_match_archives_it_with_cxos_reply(portfolio, hide_literal_absent):
    portfolio["projects"] = [_project("p-1", "zz share-hide project"), _project("p-2", "Beta")]
    result = await _service().process_intent(
        message="hide the project zz share-hide project",
        session_id="e2e-2271-hide-one",
        user_id=_USER,
    )
    assert result.message != GENERIC_UNWIRED_WRITE_DECLINE
    assert "didn't recognize" not in result.message
    assert result.message == (
        'Archived "zz share-hide project". It\'s out of your active list. '
        'Say "restore project zz share-hide project" to bring it back.'
    )
    assert portfolio["archived"] == ["p-1"]


@pytest.mark.asyncio
async def test_the_reply_names_the_project_as_stored(portfolio, hide_literal_absent):
    portfolio["projects"] = [_project("p-2", "Beta")]
    result = await _service().process_intent(
        message="hide the project beta", session_id="e2e-2271-hide-case", user_id=_USER
    )
    assert result.message == (
        'Archived "Beta". It\'s out of your active list. '
        'Say "restore project Beta" to bring it back.'
    )
    assert portfolio["archived"] == ["p-2"]


@pytest.mark.asyncio
async def test_no_exact_match_archives_nothing(portfolio, hide_literal_absent):
    portfolio["projects"] = [_project("p-3", "Beta Launch")]
    result = await _service().process_intent(
        message="hide the project Beta", session_id="e2e-2271-hide-none", user_id=_USER
    )
    assert result.message == (
        "I couldn't find a project called \"Beta\", so I haven't archived anything. "
        'Check the name, or say "show my projects".'
    )
    assert portfolio["archived"] == []


@pytest.mark.asyncio
async def test_several_exact_matches_ask_armed_and_the_number_archives_that_one(
    portfolio, hide_literal_absent
):
    portfolio["projects"] = [_project("p-4", "Beta"), _project("p-5", "beta")]
    service = _service()
    sid = "e2e-2271-hide-several"
    result = await service.process_intent(
        message="hide the project Beta", session_id=sid, user_id=_USER
    )
    assert result.message == (
        "I found more than one project with that name: 1. Beta 2. beta. "
        "Which one should I archive? Say the number."
    )
    assert portfolio["archived"] == []
    record = service.workflow_offer_service.peek_pending_offer(sid, user_id=_USER)
    assert record is not None, "the several-match question must be ARMED"
    payload = record["pending_action"]
    assert payload["kind"] == PROJECT_ARCHIVE_PICK_KIND
    assert payload["pick_ids"] == ["p-4", "p-5"]

    answer = await service.process_intent(message="2", session_id=sid, user_id=_USER)
    assert portfolio["archived"] == ["p-5"]
    assert answer.message == (
        'Archived "beta". It\'s out of your active list. '
        'Say "restore project beta" to bring it back.'
    )


@pytest.mark.asyncio
async def test_a_no_to_the_pick_archives_nothing(portfolio, hide_literal_absent):
    portfolio["projects"] = [_project("p-4", "Beta"), _project("p-5", "beta")]
    service = _service()
    sid = "e2e-2271-hide-several-no"
    asked = await service.process_intent(
        message="hide the project Beta", session_id=sid, user_id=_USER
    )
    assert asked.message.startswith("I found more than one project with that name")
    declined = await service.process_intent(message="no", session_id=sid, user_id=_USER)
    assert declined.message == 'Okay, I won\'t archive "Beta". Nothing has been changed.'
    assert portfolio["archived"] == []
    assert service.workflow_offer_service.peek_pending_offer(sid, user_id=_USER) is None


@pytest.mark.asyncio
async def test_a_bare_yes_to_the_pick_reasks_and_rearms(portfolio, hide_literal_absent):
    portfolio["projects"] = [_project("p-4", "Beta"), _project("p-5", "beta")]
    service = _service()
    sid = "e2e-2271-hide-several-yes"
    asked = await service.process_intent(
        message="hide the project Beta", session_id=sid, user_id=_USER
    )
    again = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert again.message == asked.message
    assert portfolio["archived"] == []
    record = service.workflow_offer_service.peek_pending_offer(sid, user_id=_USER)
    assert record["pending_action"]["pick_ids"] == ["p-4", "p-5"]
    await service.process_intent(message="the first one", session_id=sid, user_id=_USER)
    assert portfolio["archived"] == ["p-4"]


@pytest.mark.asyncio
async def test_a_typed_archive_project_keeps_todays_lookup_and_copy(monkeypatch, portfolio):
    """Arch's condition 1/4: only the hide_project emission takes the exact path."""
    from services.onboarding import portfolio_service as ps

    calls = []

    async def _find(self, name, user_id, include_archived=False):
        calls.append(name)
        return portfolio["projects"][0]

    monkeypatch.setattr(ps.PortfolioService, "find_project_by_name", _find)
    portfolio["projects"] = [_project("p-6", "Beta")]
    result = await _service("archive_project").process_intent(
        message="archive project Beta", session_id="e2e-2271-archive", user_id=_USER
    )
    assert calls == ["beta"]
    assert result.message == "I've archived Beta. You can restore it anytime."
