"""#2271: archive resolves by EXACT name for every archive_project turn (Arch's
ruling (b), decisions.log 2026-11-06 12:51; CXO's words 12:5x).

With the surface-1 hide literal absent, the legacy classifier emits
``execution/hide_project`` for "hide the project Beta" (10/10). ``hide_project`` is a
rail alias of the archive_project entry (the #1527 discipline) and behaves exactly
like a typed ``archive_project``: one exact (case-insensitive) active match archives;
a near match from today's find_by_name ladder is OFFERED with one armed yes/no and
"yes" archives exactly the bound id; several ask an armed pick; an exact name that
is only archived points at restore; none archives nothing.

These drive the REAL ``process_intent`` and classifier chain with only the LLM boundary
pinned; the database is replaced by an in-memory portfolio behind the real
``PortfolioService`` method names (the near-match lookup runs the repository's own
#1857 ladder, ``_resolve_unambiguous_normalized_match``, over those rows). The
surface-1 hide literal is deleted (2026-11-06), the condition under which
``hide_project`` is emitted. The real-database restore check is in
tests/unit/services/database/test_archive_exact_restore_2271.py.
"""

import contextlib
import json
from types import SimpleNamespace

import pytest

from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.project_archive_pick import (
    PROJECT_ARCHIVE_CONFIRM_KIND,
    PROJECT_ARCHIVE_PICK_KIND,
    exact_matches,
    name_candidates,
)
from services.intent_service.unwired_writes import GENERIC_UNWIRED_WRITE_DECLINE
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import register_default_workflows

_USER = "3f7b8a52-2271-4b00-9e00-00000000a271"
NAMES = ["hide_project", "archive_project"]
_NEAR = 'I don\'t have a project called "Beta". Archive "Beta Launch" instead? (yes/no)'


def _archived_line(name):
    return (
        f'Archived "{name}". It\'s out of your active list. '
        f'Say "restore project {name}" to bring it back.'
    )


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

    async def _archived_list(self, user_id):
        return [p for p in state["projects"] if p.is_archived]

    async def _find(self, name, user_id, include_archived=False):
        """The repository's own ladder (exact lower, then #1857), over these rows."""
        from services.database.repositories import _resolve_unambiguous_normalized_match

        rows = [p for p in state["projects"] if include_archived or not p.is_archived]
        exact = [p for p in rows if p.name.lower() == name.lower()]
        if exact:
            return exact[0]
        return _resolve_unambiguous_normalized_match(name, rows)

    monkeypatch.setattr(session_factory.AsyncSessionFactory, "session_scope", _scope)
    monkeypatch.setattr(ps.PortfolioService, "list_active_projects", _active)
    monkeypatch.setattr(ps.PortfolioService, "get_project", _get)
    monkeypatch.setattr(ps.PortfolioService, "archive_project", _archive)
    monkeypatch.setattr(ps.PortfolioService, "list_archived_projects", _archived_list)
    monkeypatch.setattr(ps.PortfolioService, "find_project_by_name", _find)
    return state


@pytest.fixture
def hide_literal_absent():
    """The hide literal is deleted (Arch's GO 2026-11-06 14:09); this guards that it
    stays gone, the condition under which ``hide_project`` is emitted."""
    from services.intent_service.pre_classifier import PreClassifier

    assert not [p for p in PreClassifier.PORTFOLIO_PATTERNS if p.startswith(r"\bhide\s+")]


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


async def _say(service, sid, message):
    return await service.process_intent(message=message, session_id=sid, user_id=_USER)


def _armed(service, sid):
    return service.workflow_offer_service.peek_pending_offer(sid, user_id=_USER)


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_one_exact_match_archives_it_with_cxos_reply(portfolio, hide_literal_absent, action):
    portfolio["projects"] = [_project("p-1", "zz share-hide project"), _project("p-2", "Beta")]
    result = await _say(
        _service(action), f"e2e-2271-one-{action}", "hide the project zz share-hide project"
    )
    assert result.message != GENERIC_UNWIRED_WRITE_DECLINE
    assert "didn't recognize" not in result.message
    assert result.message == _archived_line("zz share-hide project")
    assert portfolio["archived"] == ["p-1"]


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_the_reply_names_the_project_as_stored(portfolio, hide_literal_absent, action):
    portfolio["projects"] = [_project("p-2", "Beta")]
    result = await _say(_service(action), f"e2e-2271-case-{action}", "hide the project beta")
    assert result.message == _archived_line("Beta")
    assert portfolio["archived"] == ["p-2"]


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_a_near_match_is_offered_never_acted_on(portfolio, hide_literal_absent, action):
    """Arch (b) 2: "Beta" is not "Beta Launch"; the ladder's single prefix candidate
    is offered with one armed yes/no, bound by id, and nothing is archived yet."""
    portfolio["projects"] = [_project("p-3", "Beta Launch")]
    service = _service(action)
    sid = f"e2e-2271-near-{action}"
    result = await _say(service, sid, "hide the project Beta")
    assert result.message == _NEAR
    assert portfolio["archived"] == []
    record = _armed(service, sid)
    assert record is not None, "the near-match offer must be ARMED"
    assert record["pending_action"]["kind"] == PROJECT_ARCHIVE_CONFIRM_KIND
    assert record["pending_action"]["project_id"] == "p-3"

    yes = await _say(service, sid, "yes")
    assert portfolio["archived"] == ["p-3"]
    assert yes.message == _archived_line("Beta Launch")


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_a_no_to_the_near_match_archives_nothing(portfolio, hide_literal_absent, action):
    portfolio["projects"] = [_project("p-3", "Beta Launch")]
    service = _service(action)
    sid = f"e2e-2271-near-no-{action}"
    await _say(service, sid, "hide the project Beta")
    declined = await _say(service, sid, "no")
    assert declined.message == 'Okay, I won\'t archive "Beta Launch". Nothing has been changed.'
    assert portfolio["archived"] == []
    assert _armed(service, sid) is None


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_no_match_archives_nothing(portfolio, hide_literal_absent, action):
    portfolio["projects"] = [_project("p-3", "Gamma")]
    result = await _say(_service(action), f"e2e-2271-none-{action}", "hide the project Beta")
    assert result.message == (
        "I couldn't find a project called \"Beta\", so I haven't archived anything. "
        'Check the name, or say "show my projects".'
    )
    assert portfolio["archived"] == []


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_an_archived_exact_name_points_at_restore(portfolio, hide_literal_absent, action):
    portfolio["projects"] = [_project("p-7", "Beta", archived=True)]
    result = await _say(_service(action), f"e2e-2271-arch-{action}", "hide the project beta")
    assert (
        result.message == '"Beta" is already archived. Say "restore project Beta" to bring it back.'
    )
    assert portfolio["archived"] == []


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_an_active_exact_name_wins_over_an_archived_one(
    portfolio, hide_literal_absent, action
):
    portfolio["projects"] = [_project("p-7", "Beta", archived=True), _project("p-8", "beta")]
    result = await _say(_service(action), f"e2e-2271-both-{action}", "hide the project Beta")
    assert result.message == _archived_line("beta")
    assert "already archived" not in result.message
    assert portfolio["archived"] == ["p-8"]


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_several_exact_matches_ask_armed_and_the_number_archives_that_one(
    portfolio, hide_literal_absent, action
):
    portfolio["projects"] = [_project("p-4", "Beta"), _project("p-5", "beta")]
    service = _service(action)
    sid = f"e2e-2271-several-{action}"
    result = await _say(service, sid, "hide the project Beta")
    assert result.message == (
        "I found more than one project with that name: 1. Beta 2. beta. "
        "Which one should I archive? Say the number."
    )
    assert portfolio["archived"] == []
    record = _armed(service, sid)
    assert record is not None, "the several-match question must be ARMED"
    assert record["pending_action"]["kind"] == PROJECT_ARCHIVE_PICK_KIND
    assert record["pending_action"]["pick_ids"] == ["p-4", "p-5"]

    answer = await _say(service, sid, "2")
    assert portfolio["archived"] == ["p-5"]
    assert answer.message == _archived_line("beta")


@pytest.mark.asyncio
async def test_a_no_to_the_pick_archives_nothing(portfolio, hide_literal_absent):
    portfolio["projects"] = [_project("p-4", "Beta"), _project("p-5", "beta")]
    service = _service()
    sid = "e2e-2271-hide-several-no"
    asked = await _say(service, sid, "hide the project Beta")
    assert asked.message.startswith("I found more than one project with that name")
    declined = await _say(service, sid, "no")
    assert declined.message == 'Okay, I won\'t archive "Beta". Nothing has been changed.'
    assert portfolio["archived"] == []
    assert _armed(service, sid) is None


@pytest.mark.asyncio
async def test_a_bare_yes_to_the_pick_reasks_and_rearms(portfolio, hide_literal_absent):
    portfolio["projects"] = [_project("p-4", "Beta"), _project("p-5", "beta")]
    service = _service()
    sid = "e2e-2271-hide-several-yes"
    asked = await _say(service, sid, "hide the project Beta")
    again = await _say(service, sid, "yes")
    assert again.message == asked.message
    assert portfolio["archived"] == []
    assert _armed(service, sid)["pending_action"]["pick_ids"] == ["p-4", "p-5"]
    await _say(service, sid, "the first one")
    assert portfolio["archived"] == ["p-4"]


@pytest.mark.asyncio
async def test_typed_archive_literal_exact_match_archives_with_cxos_words(portfolio):
    """The typed path (surface-1 archive literal -> #2057 hand-off -> archive_project):
    same effect as before on an exact name, now in CXO's words."""
    portfolio["projects"] = [_project("p-6", "Beta")]
    result = await _say(_service("archive_project"), "e2e-2271-typed", "archive project Beta")
    assert result.message == _archived_line("Beta")
    assert portfolio["archived"] == ["p-6"]


@pytest.mark.asyncio
async def test_typed_archive_literal_fuzzy_single_match_asks_and_writes_nothing(portfolio):
    portfolio["projects"] = [_project("p-9", "Beta Launch")]
    service = _service("archive_project")
    sid = "e2e-2271-typed-fuzzy"
    result = await _say(service, sid, "archive project Beta")
    assert result.message == _NEAR
    assert portfolio["archived"] == []
    assert _armed(service, sid)["pending_action"]["project_id"] == "p-9"


@pytest.mark.asyncio
@pytest.mark.parametrize("action", NAMES)
async def test_order_an_archived_exact_name_beats_a_near_active_match(
    portfolio, hide_literal_absent, action
):
    """CXO's order: exact active -> exact archived -> one near match -> none."""
    portfolio["projects"] = [_project("p-7", "Beta", archived=True), _project("p-3", "Beta Launch")]
    service = _service(action)
    sid = f"e2e-2271-order-{action}"
    result = await _say(service, sid, "hide the project Beta")
    assert (
        result.message == '"Beta" is already archived. Say "restore project Beta" to bring it back.'
    )
    assert portfolio["archived"] == []
    assert _armed(service, sid) is None


@pytest.mark.asyncio
async def test_same_named_projects_show_their_stored_created_date_and_the_reask_matches():
    """CXO 11-14: the several-match pick's names are the same (case aside), so each
    line shows the row's stored created date. The re-ask is the same text."""
    import datetime as dt

    from services.intent_service import project_archive_pick as pick

    projects = [
        SimpleNamespace(id="p-4", name="Beta", created_at=dt.datetime(2026, 11, 3, 23, 30)),
        SimpleNamespace(id="p-5", name="beta", created_at=dt.datetime(2026, 11, 9, 1, 0)),
    ]
    record = pick.build_pick_offer(_USER, projects, "hide the project Beta")
    assert record["question"] == (
        "I found more than one project with that name: 1. Beta (created 3 Nov) "
        "2. beta (created 9 Nov). Which one should I archive? Say the number."
    )
    # Ids and plain names are unchanged: the number still writes to the bound id.
    assert record["pending_action"]["pick_ids"] == ["p-4", "p-5"]
    assert record["pending_action"]["pick_names"] == ["Beta", "beta"]

    class _Store:
        def set_pending_offer(self, _sid, rec, user_id=None):
            self.rec = rec

    store = _Store()
    out = await pick.run_clarify_project_archive_pick_workflow(
        "s1",
        _USER,
        {
            "pending_action": record["pending_action"],
            "intent_service": SimpleNamespace(workflow_offer_service=store),
        },
    )
    assert out["message"] == record["question"]
    assert store.rec["question"] == record["question"]


def test_a_row_with_no_created_date_shows_the_name_alone():
    from services.intent_service import project_archive_pick as pick

    assert pick.pick_label(_project("p-1", "Beta")) == "Beta"
