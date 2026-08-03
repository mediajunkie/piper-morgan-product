"""#1466 — Slack linking consumed by the Slack surfaces.

Covers:
- /link slash command: redeem outcomes → CXO copy (verbatim constants).
- /standup principal resolution through the slack_identities mapping —
  a linked user's standup queries THEIR todos end-to-end (DB-backed).
- Two-workspace isolation at the router level.
- The unlinked decline carries the CXO §2 deep link (opaque Slack params).
- response_handler (Arch condition 3): an unlinked Slack caller with an
  owner-scoped intent gets the honest decline — never a raw Slack id passed
  where a Piper UUID is expected (the :605-614 crash), never a default owner.

DB-backed via db_session (Postgres 5433, l1466slack applied). The router's
internal reads use AsyncSessionFactory.session_scope_fresh() against the same
database.
"""

import uuid
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import UUID, uuid4

import pytest

from services.auth.slack_link_service import mint_link_code, resolve_slack_principal
from services.database.models import User
from services.domain.models import Intent
from services.integrations.slack import link_copy
from services.integrations.slack.response_handler import SlackResponseHandler
from services.integrations.slack.webhook_router import SlackWebhookRouter
from services.shared_types import IntentCategory


def _make_user() -> User:
    suffix = uuid.uuid4().hex[:8]
    return User(
        id=uuid.uuid4(), username=f"u_{suffix}", email=f"{suffix}@test.invalid", is_alpha=True
    )


def _slack_user() -> str:
    return f"U{uuid.uuid4().hex[:10].upper()}"


def _slack_team() -> str:
    return f"T{uuid.uuid4().hex[:10].upper()}"


def _todo(text, completed=False, completed_at=None, priority="high"):
    from types import SimpleNamespace

    return SimpleNamespace(
        text=text, completed=completed, completed_at=completed_at, priority=priority
    )


@pytest.fixture
def router():
    return SlackWebhookRouter()


# ---- /link slash command ----


class TestLinkCommand1466:
    @pytest.mark.asyncio
    async def test_link_valid_code_links_and_confirms_with_cxo_copy(self, router, db_session):
        user = _make_user()
        db_session.add(user)
        await db_session.commit()
        code, _ = await mint_link_code(db_session, user.id)
        await db_session.commit()

        su, st = _slack_user(), _slack_team()
        result = await router._process_slash_command(
            {
                "command": "/link",
                "text": code,
                "user_id": su,
                "channel_id": "C456",
                "team_id": st,
            }
        )

        text = result.get("text", "")
        assert result["response_type"] == "ephemeral"
        # CXO §3b Slack-side confirmation: names the next action.
        assert "Linked — you're" in text
        assert "/standup" in text
        # And the mapping actually exists.
        assert await resolve_slack_principal(db_session, su, st) == user.id

    @pytest.mark.asyncio
    async def test_link_without_code_prompts_with_deep_link(self, router):
        result = await router._process_slash_command(
            {
                "command": "/link",
                "text": "",
                "user_id": _slack_user(),
                "channel_id": "C456",
                "team_id": _slack_team(),
            }
        )
        text = result.get("text", "")
        assert "/link" in text
        assert "/settings/integrations/slack" in text  # a link, not just prose

    @pytest.mark.asyncio
    async def test_link_invalid_code_honest_decline(self, router, db_session):
        result = await router._process_slash_command(
            {
                "command": "/link",
                "text": "000000",
                "user_id": _slack_user(),
                "channel_id": "C456",
                "team_id": _slack_team(),
            }
        )
        text = result.get("text", "")
        assert "didn't match an active link code" in text

    @pytest.mark.asyncio
    async def test_link_already_linked_fails_closed_with_unlink_path(self, router, db_session):
        user_a, user_b = _make_user(), _make_user()
        db_session.add_all([user_a, user_b])
        await db_session.commit()

        su, st = _slack_user(), _slack_team()
        code_a, _ = await mint_link_code(db_session, user_a.id)
        await db_session.commit()
        first = await router._process_slash_command(
            {"command": "/link", "text": code_a, "user_id": su, "channel_id": "C", "team_id": st}
        )
        assert "Linked — you're" in first.get("text", "")

        code_b, _ = await mint_link_code(db_session, user_b.id)
        await db_session.commit()
        second = await router._process_slash_command(
            {"command": "/link", "text": code_b, "user_id": su, "channel_id": "C", "team_id": st}
        )
        text = second.get("text", "")
        assert "already linked" in text
        assert "unlink first" in text.lower()
        # Owner NOT overwritten.
        assert await resolve_slack_principal(db_session, su, st) == user_a.id


# ---- /standup resolution through the mapping ----


class TestStandupResolution1466:
    @pytest.mark.asyncio
    async def test_linked_users_standup_shows_their_real_todos(self, router, db_session):
        user = _make_user()
        db_session.add(user)
        await db_session.commit()
        code, _ = await mint_link_code(db_session, user.id)
        await db_session.commit()

        su, st = _slack_user(), _slack_team()
        await router._process_slash_command(
            {"command": "/link", "text": code, "user_id": su, "channel_id": "C", "team_id": st}
        )

        todos = [_todo("Ship the #1466 mapping", priority="urgent")]
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(return_value=todos)
            result = await router._process_slash_command(
                {
                    "command": "/standup",
                    "text": "",
                    "user_id": su,
                    "channel_id": "C456",
                    "team_id": st,
                }
            )
            # The todo service was queried AS the linked Piper user.
            called_kwargs = mock_svc.return_value.list_todos.await_args.kwargs
            assert called_kwargs.get("user_id") == user.id

        text = result.get("text", "")
        assert "Ship the #1466 mapping" in text
        assert "isn't linked" not in text

    @pytest.mark.asyncio
    async def test_two_workspace_isolation_at_router_level(self, router, db_session):
        """Same Slack user id in two workspaces → each standup queries the
        RIGHT owner's todos (the cross-tenant leakage test that matters)."""
        user_a, user_b = _make_user(), _make_user()
        db_session.add_all([user_a, user_b])
        await db_session.commit()

        su = _slack_user()
        team_1, team_2 = _slack_team(), _slack_team()
        for owner, team in ((user_a, team_1), (user_b, team_2)):
            code, _ = await mint_link_code(db_session, owner.id)
            await db_session.commit()
            await router._process_slash_command(
                {"command": "/link", "text": code, "user_id": su, "channel_id": "C", "team_id": team}
            )

        seen = {}
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(return_value=[])
            for team in (team_1, team_2):
                await router._process_slash_command(
                    {"command": "/standup", "text": "", "user_id": su, "channel_id": "C", "team_id": team}
                )
                seen[team] = mock_svc.return_value.list_todos.await_args.kwargs.get("user_id")

        assert seen[team_1] == user_a.id
        assert seen[team_2] == user_b.id

    @pytest.mark.asyncio
    async def test_unlinked_standup_keeps_honest_copy_and_carries_deep_link(
        self, router, db_session
    ):
        """#1429 regression + CXO §2: the not-linked copy stays, and the decline
        carries the one-click deep link with the caller's opaque Slack params."""
        su, st = _slack_user(), _slack_team()
        with patch(
            "services.todo.todo_management_service.TodoManagementService"
        ) as mock_svc:
            mock_svc.return_value.list_todos = AsyncMock(return_value=[])
            result = await router._process_slash_command(
                {"command": "/standup", "text": "", "user_id": su, "channel_id": "C", "team_id": st}
            )
            mock_svc.return_value.list_todos.assert_not_awaited()

        text = result.get("text", "")
        assert "isn't linked" in text  # #1429 honest copy preserved
        assert "Link your account" in text  # the link as a link (CXO §3a)
        assert f"slack_user_id={su}" in text  # opaque params carried (CXO §2)
        assert f"slack_team_id={st}" in text

    @pytest.mark.asyncio
    async def test_resolve_todo_principal_uuid_passthrough(self, router):
        piper_id = uuid4()
        assert await router._resolve_todo_principal(str(piper_id)) == piper_id

    @pytest.mark.asyncio
    async def test_resolve_todo_principal_fails_closed_without_team(self, router):
        """A Slack id with no workspace context resolves to None — never a
        cross-workspace guess, never a default owner."""
        assert await router._resolve_todo_principal("U123ABC", None) is None


# ---- Arch condition 3: response_handler honest decline (the :605-614 crash) ----


def _handler() -> SlackResponseHandler:
    return SlackResponseHandler(
        spatial_adapter=MagicMock(),
        intent_classifier=MagicMock(),
        slack_client=MagicMock(),
        intent_service=MagicMock(),
    )


def _execution_intent(action="create_todo", message="add a todo to test linking"):
    return Intent(
        category=IntentCategory.EXECUTION,
        action=action,
        original_message=message,
        confidence=0.95,
    )


class TestResponseHandlerUnlinkedDecline1466:
    @pytest.mark.asyncio
    async def test_unlinked_owner_scoped_intent_declines_honestly(self):
        handler = _handler()
        handler.intent_service.process_intent = AsyncMock()

        su, st = _slack_user(), _slack_team()
        result = await handler._process_through_orchestration(
            _execution_intent(),
            {"user_id": su, "workspace_id": st, "channel_id": "C1"},
        )

        # Honest decline, not a raise, not a dispatch with a Slack id.
        handler.intent_service.process_intent.assert_not_awaited()
        assert result is not None
        content = result.get("content", "")
        assert link_copy.UNLINKED_DECLINE_PROSE in content
        assert f"slack_user_id={su}" in content  # deep link with opaque params

    @pytest.mark.asyncio
    async def test_linked_slack_caller_dispatches_as_their_piper_uuid(self, db_session):
        user = _make_user()
        db_session.add(user)
        await db_session.commit()
        code, _ = await mint_link_code(db_session, user.id)
        su, st = _slack_user(), _slack_team()
        from services.auth.slack_link_service import redeem_link_code

        assert (await redeem_link_code(db_session, code, su, st)).status == "linked"
        await db_session.commit()

        handler = _handler()
        handler.intent_service.process_intent = AsyncMock(
            return_value=MagicMock(success=True, message="done")
        )
        result = await handler._process_through_orchestration(
            _execution_intent(),
            {"user_id": su, "workspace_id": st, "channel_id": "C1"},
        )

        called_kwargs = handler.intent_service.process_intent.await_args.kwargs
        assert called_kwargs.get("user_id") == str(user.id)
        assert result is not None and result.get("type") == "workflow_result"

    @pytest.mark.asyncio
    async def test_piper_uuid_caller_passes_through_unchanged(self):
        handler = _handler()
        handler.intent_service.process_intent = AsyncMock(
            return_value=MagicMock(success=True, message="done")
        )
        piper_id = str(uuid4())
        await handler._process_through_orchestration(
            _execution_intent(),
            {"user_id": piper_id, "workspace_id": _slack_team(), "channel_id": "C1"},
        )
        assert handler.intent_service.process_intent.await_args.kwargs.get("user_id") == piper_id

    @pytest.mark.asyncio
    async def test_unlinked_non_owner_scoped_intent_still_dispatches(self):
        """The decline is scoped to owner-scoped actions — an unlinked caller's
        non-personal EXECUTION intent still dispatches (with no principal),
        it is not blanket-refused."""
        handler = _handler()
        handler.intent_service.process_intent = AsyncMock(
            return_value=MagicMock(success=True, message="done")
        )
        await handler._process_through_orchestration(
            _execution_intent(action="create_issue", message="file a bug about the header"),
            {"user_id": _slack_user(), "workspace_id": _slack_team(), "channel_id": "C1"},
        )
        called_kwargs = handler.intent_service.process_intent.await_args.kwargs
        assert called_kwargs.get("user_id") is None  # no principal — never a Slack id
