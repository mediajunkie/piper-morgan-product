"""#2304, Arch 11-06 13:23 (2): what the question shows is what "yes" writes.

A builder that reuses its handler's resolver BINDS the values it named into the
Intent the armed record carries (``write_confirm_words.WRITE_ASK_BOUND_KEY``), and
the handler writes those bound values on the confirmed turn, never a re-extraction.

One pin per reusing op, through the yes path: the ask is built and armed (the #1190
carrier's record), then the message the record carries is swapped for one whose
re-extraction would name something else, and the REAL
``run_confirm_pending_action_workflow`` runs the op. The value that reaches the write
(or the write's own lookup) is the value the question showed. Only the storage or
GitHub seam below the handler is replaced.
"""

import contextlib
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.destructive_confirm import build_confirmation_offer
from services.intent_service.workflow_dispatcher import get_action_workflows
from services.intent_service.workflow_entries import (
    register_default_workflows,
    run_confirm_pending_action_workflow,
)
from services.intent_service.write_confirm_words import (
    WRITE_ASK_BOUND_KEY,
    WriteAskRequest,
    resolve_write_ask,
)
from services.shared_types import IntentCategory
from tests.unit.services.intent_service.test_floor_category_write_2219 import (  # noqa: F401
    _USER,
    _service,
    boundary,
)

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"


def _intent(action, message, **context):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        confidence=0.9,
        original_message=message,
        context={"original_message": message, "user_id": _USER, **context},
    )


async def _ask_then_yes(service, action, asked, swapped, sid, **context):
    """Arm the op's question for ``asked``; then make the carried message ``swapped``
    (what a re-extraction would read) and run the confirmed yes. Returns the question."""
    register_default_workflows()
    intent = _intent(action, asked, **context)
    ask = await resolve_write_ask(
        get_action_workflows()[action],
        WriteAskRequest(
            intent=intent,
            message=asked,
            intent_service=service,
            principal=_USER,
            session_id=sid,
            user_id=_USER,
        ),
    )
    assert ask.words is not None, ask
    offer = build_confirmation_offer(intent, ask.words)
    carried = offer.offer["pending_action"]["intent"]
    assert carried.context[WRITE_ASK_BOUND_KEY]["op"]  # bound into the armed record
    carried.original_message = swapped
    carried.context = {**carried.context, "original_message": swapped}
    await run_confirm_pending_action_workflow(
        sid,
        _USER,
        context={"pending_action": offer.offer["pending_action"], "intent_service": service},
    )
    return ask.words.question


@pytest.mark.asyncio
async def test_create_todo_writes_the_title_it_showed(boundary):
    question = await _ask_then_yes(
        _service(action="create_todo"),
        "create_todo",
        "add todo: buy milk",
        "add todo: sell bread",
        "s-2304-bind-todo",
    )
    assert question == 'Add "buy milk" to your todos? (yes/no)'
    assert boundary["created"] == ["buy milk"]


@pytest.mark.asyncio
async def test_create_reminder_writes_the_task_and_time_it_showed(boundary, monkeypatch):
    from services.todo.todo_management_service import TodoManagementService
    from services.utils import user_timezone

    async def _no_tz(user_id):
        return None

    monkeypatch.setattr(user_timezone, "get_user_timezone", _no_tz)
    written = []

    async def _create(self, user_id, text, priority="medium", **kwargs):
        written.append((text, kwargs.get("reminder_date")))
        return MagicMock(id="r1", text=text)

    monkeypatch.setattr(TodoManagementService, "create_todo", _create)
    service = _service(action="create_reminder")
    sid = "s-2304-bind-reminder"
    question = await _ask_then_yes(
        service,
        "create_reminder",
        "remind me to call mom tomorrow at 3pm",
        "remind me to walk the dog in 2 hours",
        sid,
    )
    assert question == 'Set a reminder "call mom" for tomorrow at 3pm? (yes/no)'
    [(text, when)] = written
    assert text == "call mom"
    assert (when.hour, when.minute) == (15, 0)


@contextlib.contextmanager
def _portfolio_lookup(found):
    """The archive/restore lookup seam: record the name the handler looks up."""

    @contextlib.asynccontextmanager
    async def _scope():
        yield MagicMock()

    async def _find(self, name, user_id, include_archived=False):
        found.append(name)
        return None

    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            new=staticmethod(_scope),
        ),
        patch(
            "services.onboarding.portfolio_service.PortfolioService.find_project_by_name",
            new=_find,
        ),
        # #2271 (b): archive resolves exact names over the active and archived lists
        # first; empty lists send the bound name on to the near-name ladder, where
        # _find records the name it was given.
        patch(
            "services.onboarding.portfolio_service.PortfolioService.list_active_projects",
            new=AsyncMock(return_value=[]),
        ),
        patch(
            "services.onboarding.portfolio_service.PortfolioService.list_archived_projects",
            new=AsyncMock(return_value=[]),
        ),
    ):
        yield


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "action,asked,swapped,question",
    [
        (
            "archive_project",
            "archive project Bar",
            "archive project Quux",
            'Archive the project "Bar"? (yes/no)',
        ),
        (
            "restore_project",
            "restore project Bar",
            "restore project Quux",
            'Restore the project "Bar"? (yes/no)',
        ),
    ],
)
async def test_archive_and_restore_look_up_the_name_they_showed(
    boundary, action, asked, swapped, question
):
    found = []
    with _portfolio_lookup(found):
        shown = await _ask_then_yes(
            _service(action=action), action, asked, swapped, f"s-2304-bind-{action}"
        )
    assert shown == question
    assert found == ["Bar"]


@pytest.mark.asyncio
async def test_add_project_adds_the_name_it_showed(boundary):
    from services.intent_service.canonical_handlers import CanonicalHandlers

    created = []

    async def _create(self, name, **kwargs):
        created.append(name)
        return {
            "message": f"Added {name}.",
            "intent": {
                "category": "portfolio",
                "action": "add_project",
                "confidence": 1.0,
                "context": {},
            },
            "requires_clarification": False,
        }

    with patch.object(CanonicalHandlers, "_create_or_report_project", new=_create):
        shown = await _ask_then_yes(
            _service(action="add_project"),
            "add_project",
            "add a project called Klatch",
            "add a project called Quux",
            "s-2304-bind-add",
        )
    assert shown == 'Add a project called "Klatch"? (yes/no)'
    assert created == ["Klatch"]


@pytest.mark.asyncio
async def test_create_issue_creates_the_title_in_the_repo_it_showed(boundary):
    created = AsyncMock(
        return_value={"number": 10, "title": "Login bug", "html_url": "https://x/10"}
    )
    with (
        patch(
            "services.configuration.piper_config_loader.piper_config_loader.load_github_config",
            return_value=MagicMock(default_labels=[]),
        ),
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.find_open_issue_by_title", new=AsyncMock(return_value=None)),
        patch(f"{ROUTER}.create_issue", new=created),
    ):
        shown = await _ask_then_yes(
            _service(action="create_issue"),
            "create_issue",
            'create an issue titled "Login bug" in acme/web',
            'create an issue titled "Other thing" in foo/bar',
            "s-2304-bind-create-issue",
        )
    assert shown == 'Create an issue titled "Login bug" in acme/web? (yes/no)'
    kwargs = created.await_args.kwargs
    assert (kwargs["title"], kwargs["owner"], kwargs["repo_name"]) == ("Login bug", "acme", "web")


@pytest.mark.asyncio
async def test_update_issue_changes_the_issue_repo_and_field_it_showed(boundary):
    updated = AsyncMock(return_value={"number": 108, "title": "Q3 roadmap"})
    with (
        patch(f"{ROUTER}.initialize", new=AsyncMock()),
        patch(f"{ROUTER}.is_available", new=AsyncMock(return_value=True)),
        patch(f"{ROUTER}.update_issue", new=updated),
    ):
        shown = await _ask_then_yes(
            _service(action="update_issue"),
            "update_issue",
            'set the title of issue #108 in acme/roadmap to "Q3 roadmap"',
            'set the title of issue #7 in foo/bar to "Something else"',
            "s-2304-bind-update-issue",
        )
    assert shown == "Change the title of issue #108 in acme/roadmap? (yes/no)"
    kwargs = updated.await_args.kwargs
    assert kwargs["issue_number"] == 108
    assert (kwargs["owner"], kwargs["repo_name"]) == ("acme", "roadmap")
    assert kwargs["title"] == "Q3 roadmap"
