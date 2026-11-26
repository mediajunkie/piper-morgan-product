"""Issue 2448: when the close/reopen gate cannot check, it says so and arms nothing.

Arch (on the issue, and mail 01M8CXG89D, 2026-11-26): the gate has five awaited reads.
Until now any of them raising fell into one catch-all that armed the generic yes/no
confirm, so a person was asked to confirm an action Piper could not check. Each read
now has its own ``try``, and the line is chosen by WHICH read failed, never by matching
on the exception:

1. ``resolve_credential``             -> the connection line (CXO 01M8CVRV9K)
2. ``resolve_repo_name``              -> the issue line
3. ``get_user_write_target``          -> the default-repository line (CXO 01M8CX1FXS):
                                         the one failure that is Piper's own
4. ``github_app_write_refusal_line``  -> the issue line
5. ``probe_issue_connector``          -> the issue line

All are passthroughs marked DEGRADED with nothing armed. The gate's deliberate
fallbacks (a repository that resolved to nothing, a malformed repository string, an
unparseable probe, no principal) are not exceptions and are unchanged; the no-principal
one is issue 2450.

LAYER: the real ``build_close_reopen_confirmation``, and the rail through
``process_intent`` for what is armed. Nothing here is a browser.
"""

import inspect
from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentService
from services.intent_service.classifier import IntentClassifier
from services.intent_service.destructive_confirm import build_close_reopen_confirmation
from services.intent_service.not_performed import NOT_PERFORMED_KEY, NotPerformed
from services.mcp.consumer.github_adapter import (
    GITHUB_CONNECTION_COULD_NOT_CHECK_REPLY,
    GITHUB_DEFAULT_REPOSITORY_COULD_NOT_LOOK_UP_REPLY,
    GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    GitHubCredential,
)
from services.shared_types import IntentCategory

RESOLVE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.resolve_credential"
PROBE = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter.probe_issue_connector"
APP_LINE = "services.mcp.consumer.github_adapter.github_app_write_refusal_line"
WRITE_TARGET = "services.integrations.github.repo_resolver.get_user_write_target"
REPO_NAME = "services.intent_service.repo_clarification.resolve_repo_name"

_USER = "3f7b8a52-2448-4b00-9e00-000000002448"
_REPO = "mediajunkie/test-piper-morgan"
_CONNECTED = GitHubCredential(owner_id=_USER, mcp_server_ref="github", token="t", leg="oauth")
ACTIONS = [
    pytest.param("close_issue_query", id="close"),
    pytest.param("reopen_issue_query", id="reopen"),
]


class _ExplosiveLLM:
    def __getattr__(self, name):
        raise AssertionError(f"LLM boundary touched ({name})")


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService(intent_classifier=IntentClassifier(llm_service=_ExplosiveLLM()))


def _intent(message, action, **context):
    return Intent(
        category=IntentCategory.QUERY,
        action=action,
        confidence=1.0,
        original_message=message,
        context={"original_message": message, "user_id": _USER, **context},
    )


def _raises(text="the database is away"):
    return AsyncMock(side_effect=RuntimeError(text))


def _assert_could_not_check(gate, line):
    assert gate.offer is None, "a confirmation was armed for an action that could not be checked"
    result = gate.passthrough_result
    assert result is not None
    assert result["message"] == line
    assert result["requires_clarification"] is False
    assert result["intent_data"] == {NOT_PERFORMED_KEY: NotPerformed.DEGRADED}
    assert "the database is away" not in str(result)


# ── The words ────────────────────────────────────────────────────────────────


def test_the_three_lines_are_cxos_and_one_family():
    assert GITHUB_CONNECTION_COULD_NOT_CHECK_REPLY == (
        "I couldn't check your GitHub connection just now, so I haven't done anything. "
        "Try again in a moment; if it keeps failing, tell us."
    )
    assert GITHUB_DEFAULT_REPOSITORY_COULD_NOT_LOOK_UP_REPLY == (
        "I couldn't look up which repository to use just now, so I haven't done anything. "
        "Try again in a moment; if it keeps failing, tell us."
    )
    assert GITHUB_ISSUE_COULD_NOT_CHECK_REPLY == (
        "I couldn't check that issue just now, so I haven't done anything. Try again in a "
        "moment; if it keeps failing, tell us."
    )
    tail = "so I haven't done anything. Try again in a moment; if it keeps failing, tell us."
    lines = (
        GITHUB_CONNECTION_COULD_NOT_CHECK_REPLY,
        GITHUB_DEFAULT_REPOSITORY_COULD_NOT_LOOK_UP_REPLY,
        GITHUB_ISSUE_COULD_NOT_CHECK_REPLY,
    )
    assert all(line.endswith(tail) for line in lines) and len(set(lines)) == 3


def test_the_gate_carries_no_copy_of_the_sentences():
    source = inspect.getsource(build_close_reopen_confirmation)
    assert "just now" not in source and "keeps failing" not in source


# ── Each of the five reads, raising ──────────────────────────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ACTIONS)
async def test_read_1_the_resolver_raises(service, action):
    with patch(RESOLVE, _raises()):
        gate = await build_close_reopen_confirmation(
            _intent("close issue 5", action), service, "wf"
        )
    _assert_could_not_check(gate, GITHUB_CONNECTION_COULD_NOT_CHECK_REPLY)


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ACTIONS)
async def test_read_2_the_repository_name_lookup_raises(service, action):
    message = "close issue 5 in the widgets repository"
    with patch(RESOLVE, AsyncMock(return_value=_CONNECTED)), patch(REPO_NAME, _raises()) as lookup:
        gate = await build_close_reopen_confirmation(_intent(message, action), service, "wf")
    lookup.assert_awaited_once()
    _assert_could_not_check(gate, GITHUB_ISSUE_COULD_NOT_CHECK_REPLY)


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ACTIONS)
async def test_read_3_pipers_own_default_repository_read_raises(service, action):
    with patch(RESOLVE, AsyncMock(return_value=_CONNECTED)), patch(WRITE_TARGET, _raises()) as read:
        gate = await build_close_reopen_confirmation(
            _intent("close issue 5", action), service, "wf"
        )
    read.assert_awaited_once()
    _assert_could_not_check(gate, GITHUB_DEFAULT_REPOSITORY_COULD_NOT_LOOK_UP_REPLY)


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ACTIONS)
async def test_read_4_the_app_installation_check_raises(service, action):
    with patch(RESOLVE, AsyncMock(return_value=_CONNECTED)), patch(APP_LINE, _raises()) as check:
        gate = await build_close_reopen_confirmation(
            _intent("close issue 5", action, repository=_REPO), service, "wf"
        )
    check.assert_awaited_once()
    _assert_could_not_check(gate, GITHUB_ISSUE_COULD_NOT_CHECK_REPLY)


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ACTIONS)
async def test_read_5_the_issue_probe_raises(service, action):
    with (
        patch(RESOLVE, AsyncMock(return_value=_CONNECTED)),
        patch(APP_LINE, AsyncMock(return_value=None)),
        patch(PROBE, _raises()) as probe,
    ):
        gate = await build_close_reopen_confirmation(
            _intent("close issue 5", action, repository=_REPO), service, "wf"
        )
    probe.assert_awaited_once()
    _assert_could_not_check(gate, GITHUB_ISSUE_COULD_NOT_CHECK_REPLY)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "error", [RuntimeError("x"), ValueError("x"), KeyError("x"), TimeoutError(), OSError("x")]
)
async def test_the_line_does_not_depend_on_the_kind_of_error(service, error):
    with patch(RESOLVE, AsyncMock(side_effect=error)):
        gate = await build_close_reopen_confirmation(
            _intent("close issue 5", "close_issue_query"), service, "wf"
        )
    _assert_could_not_check(gate, GITHUB_CONNECTION_COULD_NOT_CHECK_REPLY)


# ── Nothing awaited can reach the outer catch-all ────────────────────────────


def test_every_await_in_the_gate_sits_in_its_own_try():
    """Arch: the outer catch-all stays as a last resort, and nothing awaited reaches it.
    Read from the source: every ``await`` in the gate is inside a ``try`` other than the
    outermost one. A sixth read added bare fails here until it gets its own line."""
    import ast
    import textwrap

    tree = ast.parse(textwrap.dedent(inspect.getsource(build_close_reopen_confirmation)))
    func = tree.body[0]
    outer = next(node for node in func.body if isinstance(node, ast.Try))

    bare = []

    def visit(node, inner_tries):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.Lambda)):
            return  # a nested helper's body is not the gate's own flow
        if isinstance(node, ast.Try):
            for part in node.body:
                visit(part, inner_tries + 1)
            for part in node.handlers + node.orelse + node.finalbody:
                visit(part, inner_tries)
            return
        if isinstance(node, ast.Await) and inner_tries == 0:
            bare.append(ast.unparse(node)[:80])
        for child in ast.iter_child_nodes(node):
            visit(child, inner_tries)

    for statement in outer.body:
        visit(statement, 0)
    assert bare == []


def test_the_gate_names_exactly_five_reads():
    source = inspect.getsource(build_close_reopen_confirmation)
    names = [
        "resolve_credential",
        "resolve_repo_name",
        "get_user_write_target",
        "github_app_write_refusal_line",
        "probe_issue_connector",
    ]
    for name in names:
        assert source.count(f'"{name}")') == 1 or source.count(f'"{name}"\n') == 1, name
    assert source.count("_could_not_check(") == len(names) + 1  # five uses and the def


# ── What did not change ──────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_a_repository_that_resolved_to_nothing_still_falls_back(service):
    """A deliberate fallback, not an exception: unchanged by this issue."""
    from types import SimpleNamespace

    message = "close issue 5 in the widgets repository"
    with (
        patch(RESOLVE, AsyncMock(return_value=_CONNECTED)),
        patch(REPO_NAME, AsyncMock(return_value=SimpleNamespace(status="none", full_name=None))),
    ):
        gate = await build_close_reopen_confirmation(
            _intent(message, "close_issue_query"), service, "wf"
        )
    assert gate.passthrough_result is None and gate.offer is not None


@pytest.mark.asyncio
async def test_a_found_open_issue_is_still_confirmed(service):
    with (
        patch(RESOLVE, AsyncMock(return_value=_CONNECTED)),
        patch(APP_LINE, AsyncMock(return_value=None)),
        patch(
            PROBE,
            AsyncMock(
                return_value=("found", {"title": "A bug", "state": "open", "number": 5}, None)
            ),
        ),
    ):
        gate = await build_close_reopen_confirmation(
            _intent("close issue 5", "close_issue_query", repository=_REPO), service, "wf"
        )
    assert gate.passthrough_result is None and gate.offer is not None


# ── The rail: one turn, nothing pending ──────────────────────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize("action", ACTIONS)
async def test_through_the_rail_nothing_is_left_pending(service, monkeypatch, action):
    from services.intent_service.not_performed import SAID_INSTEAD_KEY
    from services.intent_service.workflow_entries import register_default_workflows

    register_default_workflows()
    verb = "close" if action.startswith("close") else "reopen"

    async def _classify(message, *args, **kwargs):
        return Intent(
            category=IntentCategory.QUERY,
            action=action,
            confidence=1.0,
            original_message=message,
            context={"original_message": message},
        )

    monkeypatch.setattr(service.intent_classifier, "classify", _classify)
    monkeypatch.setattr(RESOLVE, _raises())
    sid = f"e2e-2448-{uuid4()}"
    result = await service.process_intent(
        message=f"{verb} issue 999999", session_id=sid, user_id=_USER
    )
    assert service.workflow_offer_service._pending_offers.get(sid) is None
    assert result.message == GITHUB_CONNECTION_COULD_NOT_CHECK_REPLY
    assert result.success is False
    assert result.requires_clarification is False
    assert result.intent_data[NOT_PERFORMED_KEY] == NotPerformed.DEGRADED
    assert result.intent_data[SAID_INSTEAD_KEY] is True
