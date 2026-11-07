"""#2308's link_repo slice (#2271; PPM 11-06 16:24; Arch 15:59 (4)(b); CXO 15:58, 16:33).

A held link_repo turn names the thing, from the handler's own parse
(``canonical_handlers.resolve_link_repo_request``) and its own project lookup, and writes
nothing before "yes":

- project found, repo missing: ``Which repository should I link to {project}? Say it
  as owner/name.``, ARMED; the owner/name answer arms ``Link {owner/name} to
  {project}? (yes/no)`` with the values bound; "yes" links exactly that repo to that
  project;
- both named: the bound yes/no; "yes" writes the bound values even when the carried
  message is swapped (the #2304 binding pin shape);
- a named project that doesn't exist: the handler's not-found line, nothing armed;
- neither, or a repo with no project: the not-sure line, nothing armed.

Drives the REAL ``process_intent`` with only the LLM boundary pinned (the #2219
harness), and the REAL ``run_confirm_pending_action_workflow`` for the swap pins.
Only the storage seam below the handler is replaced (project lookup, repository rows,
the link insert, GitHub's soft validation).
"""

import contextlib
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import resolve_link_repo_request
from services.intent_service.destructive_confirm import build_confirmation_offer
from services.intent_service.link_repo_ask import (
    CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW,
    LINK_REPO_REPOSITORY_KIND,
)
from services.intent_service.workflow_dispatcher import (
    get_action_workflows,
    get_registered_workflows,
)
from services.intent_service.workflow_entries import (
    register_default_workflows,
    run_confirm_pending_action_workflow,
)
from services.intent_service.write_confirm_words import (
    NOT_SURE_STATEMENT,
    WRITE_ASK_BOUND_KEY,
    WriteAskRequest,
    resolve_write_ask,
)
from services.shared_types import IntentCategory
from tests.unit.services.intent_service.test_floor_category_write_2219 import (
    _USER,
    _service,
)

_PROJECT = "zz share-hide project"
_OTHER = "Piper Test Activity"
_REPO = "dinp-machine/piper-test-activity"
_HELD_ADD = "I want to add a repo to my zz share-hide project"
_WHICH = "Which repository should I link to zz share-hide project? Say it as owner/name."
_CONFIRM = f"Link {_REPO} to {_PROJECT}? (yes/no)"
# CXO 11-06 16:33 (final): the decline, and the reply after "yes".
_DECLINE = f"Okay, I won't link {_REPO} to {_PROJECT}. Nothing has been changed."
_LINKED = f"Linked {_REPO} to {_PROJECT}."
_PROJECTS = {
    _PROJECT.casefold(): SimpleNamespace(id="proj-zz", name=_PROJECT),
    _OTHER.casefold(): SimpleNamespace(id="proj-pta", name=_OTHER),
}


@pytest.fixture
def store():
    """The storage seam: project lookups recorded, repository rows and links kept."""
    state = {"looked_up": [], "repos": [], "links": []}

    @contextlib.asynccontextmanager
    async def _scope():
        yield SimpleNamespace()

    async def _find_by_name(self, name, owner_id=None, is_admin=False, include_archived=False):
        state["looked_up"].append(name)
        return _PROJECTS.get(str(name).casefold())

    async def _get_by_full_name(self, full_name, provider="github", owner_id=None):
        return None

    async def _create_repository(self, repo):
        row = SimpleNamespace(id=f"repo-{len(state['repos']) + 1}", full_name=repo.full_name)
        state["repos"].append(repo.full_name)
        return row

    async def _get_project_links(self, repository_id):
        return []

    async def _link_to_project(self, repository_id, project_id, linked_by=None, **kwargs):
        state["links"].append((repository_id, project_id))
        return SimpleNamespace()

    async def _validate(repo_name, user_id):
        return SimpleNamespace(validated=False, exists=False)

    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            new=staticmethod(_scope),
        ),
        patch("services.database.repositories.ProjectRepository.find_by_name", new=_find_by_name),
        patch(
            "services.database.repositories.RepositoryRepository.get_by_full_name",
            new=_get_by_full_name,
        ),
        patch(
            "services.database.repositories.RepositoryRepository.create_repository",
            new=_create_repository,
        ),
        patch(
            "services.database.repositories.RepositoryRepository.get_project_links",
            new=_get_project_links,
        ),
        patch(
            "services.database.repositories.RepositoryRepository.link_to_project",
            new=_link_to_project,
        ),
        patch(
            "services.infrastructure.github_repo_validator.validate_github_repo_for_account",
            new=_validate,
        ),
        patch(
            "services.infrastructure.github_repo_validator.apply_validation_metadata",
            new=lambda repo, validation: None,
        ),
    ):
        yield state


def _linked(state):
    """(repo full name, project id) for each link written."""
    names = {f"repo-{i}": n for i, n in enumerate(state["repos"], 1)}
    return [(names[r], p) for r, p in state["links"]]


def _pending(service, sid):
    return service.workflow_offer_service.peek_pending_offer(sid, _USER)


# ── the shared resolver: the handler's own parse, read by the ask ──


def test_the_ask_and_the_handler_read_one_parse():
    assert resolve_link_repo_request(_HELD_ADD) == (None, _PROJECT)
    assert resolve_link_repo_request(f"link repo {_REPO} to {_PROJECT}") == (_REPO, _PROJECT)
    assert resolve_link_repo_request(_REPO) == (_REPO, None)
    assert resolve_link_repo_request("link it up") == (None, None)


def test_the_which_repository_landing_is_registered_offer_only_and_reads():
    register_default_workflows()
    entry = get_registered_workflows()[CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW]
    assert entry.action_triggered is False
    assert entry.effect.name == "READ"
    assert CLARIFY_LINK_REPO_REPOSITORY_WORKFLOW not in get_action_workflows()


# ── row 1: the served phrasing, the armed which-repository ask, the answer, the yes ──


@pytest.mark.asyncio
async def test_held_add_a_repo_asks_which_repository_armed_and_writes_nothing(store):
    service = _service("execution", "link_repo")
    sid = "s-2308-held-add"
    result = await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
    assert result.message == _WHICH
    assert result.requires_clarification is True
    record = _pending(service, sid)
    assert record["pending_action"]["kind"] == LINK_REPO_REPOSITORY_KIND
    assert record["question"] == _WHICH
    assert record["pending_action"]["project_id"] == "proj-zz"
    assert record["pending_action"]["user_id"] == _USER
    assert store["links"] == [] and store["repos"] == []


@pytest.mark.asyncio
async def test_the_answer_arms_the_bound_confirm_and_yes_links_exactly_that(store):
    service = _service("execution", "link_repo")
    sid = "s-2308-answer"
    await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
    confirm = await service.process_intent(message=_REPO, session_id=sid, user_id=_USER)
    assert confirm.message == _CONFIRM
    record = _pending(service, sid)
    carried = record["pending_action"]["intent"]
    assert carried.action == "link_repo"
    assert carried.context[WRITE_ASK_BOUND_KEY] == {
        "op": "link_repo",
        "repo_name": _REPO,
        "project_name": _PROJECT,
        "project_id": "proj-zz",
    }
    assert store["links"] == []  # nothing before "yes"
    done = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert _linked(store) == [(_REPO, "proj-zz")]
    assert done.message == _LINKED
    assert _pending(service, sid) is None


@pytest.mark.asyncio
async def test_the_answered_confirm_writes_its_bound_values_when_the_message_is_swapped(store):
    service = _service("execution", "link_repo")
    sid = "s-2308-answer-swap"
    await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
    await service.process_intent(message=_REPO, session_id=sid, user_id=_USER)
    record = _pending(service, sid)
    carried = record["pending_action"]["intent"]
    swapped = f"link repo acme/other to {_OTHER}"
    carried.original_message = swapped
    carried.context = {**carried.context, "original_message": swapped}
    await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert _linked(store) == [(_REPO, "proj-zz")]


@pytest.mark.asyncio
async def test_no_to_the_which_repository_question_links_nothing(store):
    service = _service("execution", "link_repo")
    sid = "s-2308-no"
    await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
    declined = await service.process_intent(message="no", session_id=sid, user_id=_USER)
    assert declined.message == (
        "Okay, I won't link a repository to zz share-hide project. Nothing has been changed."
    )
    assert store["links"] == [] and _pending(service, sid) is None


@pytest.mark.asyncio
async def test_a_bare_yes_to_the_which_repository_question_asks_again_armed(store):
    service = _service("execution", "link_repo")
    sid = "s-2308-bare-yes"
    await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
    again = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert again.message == _WHICH
    assert _pending(service, sid)["pending_action"]["kind"] == LINK_REPO_REPOSITORY_KIND
    assert store["links"] == []


@pytest.mark.asyncio
async def test_a_short_answer_with_no_owner_name_is_a_statement_and_arms_nothing(store):
    service = _service("execution", "link_repo")
    sid = "s-2308-no-repo"
    await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
    said = await service.process_intent(
        message="piper-test-activity", session_id=sid, user_id=_USER
    )
    assert said.message == (
        "I didn't see a repository in owner/name form, so I haven't linked anything to "
        "zz share-hide project."
    )
    assert _pending(service, sid) is None
    assert store["links"] == []


@pytest.mark.asyncio
@pytest.mark.parametrize("turn", ["bye", "show my todos"])
async def test_a_farewell_or_unrelated_command_releases_the_question(store, monkeypatch, turn):
    from services.intent_service import link_repo_ask

    seen = []
    real = link_repo_ask.handle_link_repo_repository_turn

    async def _spy(*args, **kwargs):
        out = await real(*args, **kwargs)
        seen.append(out)
        return out

    monkeypatch.setattr(link_repo_ask, "handle_link_repo_repository_turn", _spy)
    service = _service("execution", "link_repo")
    sid = f"s-2308-release-{turn.split()[0]}"
    await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
    released = await service.process_intent(message=turn, session_id=sid, user_id=_USER)
    assert seen == [None]  # released to the generic seam, never swallowed
    assert "repository" not in released.message
    record = _pending(service, sid)
    assert record is None or record["pending_action"].get("kind") != LINK_REPO_REPOSITORY_KIND
    assert store["links"] == []


@pytest.mark.asyncio
async def test_another_principal_cannot_answer_the_question(store):
    from services.intent_service.link_repo_ask import handle_link_repo_repository_turn

    service = _service("execution", "link_repo")
    sid = "s-2308-principal"
    await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
    record = service.workflow_offer_service.get_and_clear_pending_offer(sid, user_id=_USER)
    out = await handle_link_repo_repository_turn(
        record, _REPO, session_id=sid, user_id="someone-else", intent_service=service
    )
    assert out["intent_data"]["principal_mismatch"] is True
    assert _pending(service, sid) is None
    assert store["links"] == []


# ── row 2: both named on a held turn: the bound confirm, and the swap pin ──


@pytest.mark.asyncio
async def test_both_named_on_a_held_turn_ask_the_bound_confirm_and_yes_links_it(store):
    service = _service("conversation", "link_repo")  # a floor-category write is held
    sid = "s-2308-both"
    asked = await service.process_intent(
        message=f"link repo {_REPO} to {_PROJECT}", session_id=sid, user_id=_USER
    )
    assert asked.message == _CONFIRM
    assert store["links"] == []
    done = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert _linked(store) == [(_REPO, "proj-zz")]
    assert done.message == _LINKED


@pytest.mark.asyncio
async def test_the_consent_held_turn_asks_the_bound_confirm_last(store):
    """The #1509 consent check (an "I want to" framing): the teaching line, then the
    bound question last; "yes" links it."""
    service = _service("execution", "link_repo")
    sid = "s-2308-consent"
    asked = await service.process_intent(
        message=f"I want to link repo {_REPO} to {_PROJECT}", session_id=sid, user_id=_USER
    )
    assert asked.message.endswith("\n\n" + _CONFIRM)
    assert store["links"] == []
    done = await service.process_intent(message="yes", session_id=sid, user_id=_USER)
    assert _linked(store) == [(_REPO, "proj-zz")]
    assert done.message == _LINKED


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "category,first",
    [
        ("conversation", f"link repo {_REPO} to {_PROJECT}"),  # the floor-write confirm
        ("execution", f"I want to link repo {_REPO} to {_PROJECT}"),  # the consent check
        ("execution", None),  # the answered which-repository confirm
    ],
)
async def test_no_to_the_confirm_says_cxos_decline_and_links_nothing(store, category, first):
    service = _service(category, "link_repo")
    sid = f"s-2308-decline-{category}-{first is None}"
    if first is None:
        await service.process_intent(message=_HELD_ADD, session_id=sid, user_id=_USER)
        first = _REPO
    asked = await service.process_intent(message=first, session_id=sid, user_id=_USER)
    assert asked.message.endswith(_CONFIRM)
    declined = await service.process_intent(message="no", session_id=sid, user_id=_USER)
    assert declined.message == _DECLINE
    assert store["links"] == [] and store["repos"] == []
    assert _pending(service, sid) is None


@pytest.mark.asyncio
async def test_a_direct_imperative_link_says_what_was_linked(store):
    """Nothing bound (a direct, unheld turn): CXO 17:52, the same one sentence as the
    held path; no "I can now help you track …" tail (a link doesn't change what Piper
    reads, #2272)."""
    from services.intent_service.canonical_handlers import CanonicalHandlers

    intent = Intent(
        category=IntentCategory.PORTFOLIO,
        action="link_repo",
        confidence=1.0,
        original_message=f"link repo {_REPO} to {_PROJECT}",
        context={"original_message": f"link repo {_REPO} to {_PROJECT}"},
    )
    result = await CanonicalHandlers()._handle_link_repo(intent, "s-2308-direct", _USER)
    assert result["message"] == f"Linked {_REPO} to {_PROJECT}."
    assert _linked(store) == [(_REPO, "proj-zz")]


@pytest.mark.asyncio
async def test_both_named_yes_writes_the_bound_values_when_the_message_is_swapped(store):
    """The #2304 binding pin shape: arm, swap the carried message for one whose
    re-extraction names another repo and project, run the REAL confirm workflow."""
    register_default_workflows()
    asked = f"link repo {_REPO} to {_PROJECT}"
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="link_repo",
        confidence=0.9,
        original_message=asked,
        context={"original_message": asked, "user_id": _USER},
    )
    service = _service("execution", "link_repo")
    ask = await resolve_write_ask(
        get_action_workflows()["link_repo"],
        WriteAskRequest(
            intent=intent,
            message=asked,
            intent_service=service,
            principal=_USER,
            session_id="s-2308-swap",
            user_id=_USER,
        ),
    )
    assert ask.words.question == _CONFIRM
    assert ask.words.summary == f"link {_REPO} to {_PROJECT}"
    offer = build_confirmation_offer(intent, ask.words)
    carried = offer.offer["pending_action"]["intent"]
    swapped = f"link repo acme/other to {_OTHER}"
    carried.original_message = swapped
    carried.context = {**carried.context, "original_message": swapped}
    await run_confirm_pending_action_workflow(
        "s-2308-swap",
        _USER,
        context={"pending_action": offer.offer["pending_action"], "intent_service": service},
    )
    assert _linked(store) == [(_REPO, "proj-zz")]
    assert _OTHER not in store["looked_up"]


# ── rows 3 and 4: not found; neither; repo with no project. Statements, nothing armed ──


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "category,message,expected",
    [
        (
            "execution",
            "I want to add a repo to my Nonesuch",
            "I couldn't find a project called 'nonesuch'. Check the name and try again, "
            "or say 'show my projects' to see your project list.",
        ),
        ("conversation", "link it up", NOT_SURE_STATEMENT),
        # CXO's table has no row for a repo with no project: the not-sure line.
        ("conversation", f"I'd like {_REPO} linked", NOT_SURE_STATEMENT),
    ],
)
async def test_unresolved_held_turns_are_statements_and_arm_nothing(
    store, category, message, expected
):
    service = _service(category, "link_repo")
    sid = f"s-2308-unresolved-{category}-{len(message)}"
    said = await service.process_intent(message=message, session_id=sid, user_id=_USER)
    assert said.message == expected
    assert _pending(service, sid) is None
    assert store["links"] == [] and store["repos"] == []
