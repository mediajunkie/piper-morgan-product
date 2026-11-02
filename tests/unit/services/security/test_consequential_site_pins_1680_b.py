"""#1680 Dashboard Criterion E (landing B): one pin set per site instrumented in landing B.

Same shape as landing A's ``test_consequential_site_pins_1680.py``: each pin drives the
real function with its client mocked at the seam the existing tests use, and
``audit_logger.log_consequential_action`` replaced by a recorder attached to the same
parent mock, so the pin asserts ORDER (the row is written after the client call), the
site key, the status from the call's outcome, ``credits_spent`` from the site's own
path, and the principal. DENOMINATOR: the 9 sites landing B instrumented; for each, a
success pin and at least one failed/unconfirmed pin (25 pins), plus the outcome mappers
in ``services/security/consequential_outcomes.py``.
"""

from contextlib import contextmanager
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from slack_sdk.errors import SlackApiError

from services.integrations.github.github_integration_router import GitHubWriteRefused
from services.security import audit_logger as al
from services.security import consequential_outcomes as co
from services.security.consequential_sites import CONSEQUENTIAL_SITES

_USER = "11111111-1111-1111-1111-111111111111"
SKILL_MODULE = "services.integrations.mcp.skills.standup_workflow_skill"
SLACK_SEND_SEAM = (
    "services.integrations.slack.slack_integration_router.SlackIntegrationRouter.send_message"
)


def _recorder(client_mock):
    """(parent, audit): the client call and the audit helper on one parent mock."""
    parent = MagicMock()
    parent.attach_mock(client_mock, "client_call")
    audit = AsyncMock(return_value=None)
    parent.attach_mock(audit, "audit")
    return parent, audit


def _order(parent):
    return [c[0] for c in parent.mock_calls if c[0] in ("client_call", "audit")]


def _assert_rows(parent, audit, *, site, statuses, user_id=_USER, credits_spent=False):
    """Every client call is followed by its row; returns the rows' kwargs."""
    assert _order(parent) == ["client_call", "audit"] * len(statuses), _order(parent)
    assert audit.await_count == len(statuses)
    rows = [c.kwargs for c in audit.await_args_list]
    for kw, status in zip(rows, statuses):
        assert kw["site"] == site and CONSEQUENTIAL_SITES[site].instrumented is True
        assert kw["status"] == status
        assert kw["credits_spent"] is credits_spent
        assert kw["user_id"] == user_id
    return rows


def _api_error(code):
    return SlackApiError("refused", SimpleNamespace(data={"ok": False, "error": code}))


# ── SlackDomainService.post_message ──────────────────────────────────────────────


class TestSlackDomainPostMessageSite:
    async def _run(self, **send_kw):
        from services.domain.slack_domain_service import SlackDomainService

        send = AsyncMock(**send_kw)
        parent, audit = _recorder(send)
        with (
            patch(SLACK_SEND_SEAM, new=send),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            result = await SlackDomainService().post_message(
                channel="C-dom", message="hi", user_id=_USER
            )
        return parent, audit, result

    async def test_success(self):
        from services.integrations.slack.slack_client import SlackResponse

        parent, audit, result = await self._run(
            return_value=SlackResponse(success=True, data={"channel": "C-dom", "ts": "1.2"})
        )
        (kw,) = _assert_rows(parent, audit, site="slack.domain.post_message", statuses=["success"])
        assert kw["resource_type"] == "slack_channel" and kw["resource_id"] == "C-dom"
        assert result["success"] is True

    async def test_slack_refusal_is_failed(self):
        from services.integrations.slack.slack_client import (
            SlackError,
            SlackErrorType,
            SlackResponse,
        )

        parent, audit, result = await self._run(
            return_value=SlackResponse(
                success=False,
                data={},
                error=SlackError(type=SlackErrorType.API_ERROR, message="channel_not_found"),
            )
        )
        (kw,) = _assert_rows(parent, audit, site="slack.domain.post_message", statuses=["failed"])
        assert kw["details"] == {"error": "channel_not_found"}
        assert result == {"success": False, "error": "channel_not_found"}

    async def test_transport_exception_is_unconfirmed_and_still_returned(self):
        parent, audit, result = await self._run(side_effect=ConnectionError("reset"))
        (kw,) = _assert_rows(
            parent, audit, site="slack.domain.post_message", statuses=["unconfirmed"]
        )
        assert kw["details"]["error_type"] == "ConnectionError"
        assert result["success"] is False  # the existing envelope is unchanged


# ── StandupWorkflowSkill ─────────────────────────────────────────────────────────


@contextmanager
def _patched_skill_deps():
    with (
        patch(f"{SKILL_MODULE}.GitHubDomainService"),
        patch(f"{SKILL_MODULE}.SlackDomainService"),
        patch(f"{SKILL_MODULE}.NotionDomainService"),
        patch(f"{SKILL_MODULE}.UserPreferenceManager"),
    ):
        yield


def _skill():
    from services.integrations.mcp.skills.standup_workflow_skill import StandupWorkflowSkill

    with _patched_skill_deps():
        return StandupWorkflowSkill()


class TestStandupSlackPostSite:
    async def _run(self, **post_kw):
        skill = _skill()
        skill._get_user_slack_workspace = AsyncMock(return_value={"default_channel": "#su"})
        skill._format_for_slack = MagicMock(return_value={"text": "standup", "blocks": []})
        skill.slack_service = MagicMock()
        skill.slack_service.post_message = AsyncMock(**post_kw)
        parent, audit = _recorder(skill.slack_service.post_message)
        with (
            patch(f"{SKILL_MODULE}.user_timezone_name", new=AsyncMock(return_value="UTC")),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            result = await skill._post_to_slack(_USER, {"text": "x"})
        return parent, audit, result

    async def test_success(self):
        parent, audit, result = await self._run(
            return_value={"success": True, "channel": "C9", "ts": "1.0"}
        )
        (kw,) = _assert_rows(parent, audit, site="slack.standup.post", statuses=["success"])
        assert kw["resource_id"] == "#su"
        assert CONSEQUENTIAL_SITES["slack.standup.post"].proactive is True
        assert result["success"] is True

    async def test_envelope_failure_is_unconfirmed(self):
        parent, audit, result = await self._run(
            return_value={"success": False, "error": "channel_not_found"}
        )
        (kw,) = _assert_rows(parent, audit, site="slack.standup.post", statuses=["unconfirmed"])
        assert kw["details"] == {
            "write_unconfirmed": "domain_envelope_not_success",
            "error": "channel_not_found",
        }
        assert result["success"] is False

    async def test_raise_records_then_is_handled_as_before(self):
        parent, audit, result = await self._run(side_effect=RuntimeError("boom"))
        _assert_rows(parent, audit, site="slack.standup.post", statuses=["unconfirmed"])
        assert result == {"success": False, "error": "boom"}  # existing envelope


class TestStandupGithubItemsSite:
    STANDUP = {"today_priorities": ["Ship B"], "blockers": ["CI red"], "generated_at": "now"}

    async def _run(self, **create_kw):
        skill = _skill()
        skill._get_user_github_repo = AsyncMock(return_value="o/r")
        skill.github_service = MagicMock()
        skill.github_service.create_issue = AsyncMock(**create_kw)
        parent, audit = _recorder(skill.github_service.create_issue)
        with (
            patch(f"{SKILL_MODULE}.user_timezone_name", new=AsyncMock(return_value="UTC")),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            result = await skill._process_github_items(_USER, dict(self.STANDUP))
        return parent, audit, result

    async def test_success_one_row_per_issue(self):
        parent, audit, result = await self._run(
            side_effect=[{"number": 1, "html_url": "u1"}, {"number": 2, "html_url": "u2"}]
        )
        rows = _assert_rows(
            parent, audit, site="github.standup.create_issue", statuses=["success", "success"]
        )
        assert [r["details"] for r in rows] == [{"issue_number": 1}, {"issue_number": 2}]
        assert rows[0]["resource_type"] == "github_repository" and rows[0]["resource_id"] == "o/r"
        assert result["issues_created"] == 2

    async def test_refused_is_failed_and_the_loop_continues(self):
        parent, audit, result = await self._run(
            side_effect=[GitHubWriteRefused("no"), {"number": 2, "html_url": "u2"}]
        )
        rows = _assert_rows(
            parent, audit, site="github.standup.create_issue", statuses=["failed", "success"]
        )
        assert rows[0]["details"] == {"error_type": "GitHubWriteRefused"}
        assert result["issues_created"] == 1

    async def test_empty_result_is_unconfirmed(self):
        parent, audit, _ = await self._run(return_value={})
        _assert_rows(
            parent,
            audit,
            site="github.standup.create_issue",
            statuses=["unconfirmed", "unconfirmed"],
        )


# ── SlackSocketModeRunner ────────────────────────────────────────────────────────

DM_EVENT = {
    "type": "message",
    "channel_type": "im",
    "channel": "D1",
    "text": "hi",
    "ts": "100.0",
    "user": "U777",
}


def _socket_runner():
    from services.integrations.slack.socket_mode_runner import SlackSocketModeRunner

    intent = MagicMock()
    intent.process_intent = AsyncMock(return_value=SimpleNamespace(message="Hello"))
    r = SlackSocketModeRunner(
        intent_service=intent, app_token="xapp", bot_token="xoxb", bound_user_id=_USER
    )
    r._web = MagicMock()
    return r


class TestSocketPlaceholderSite:
    async def _run(self, **post_kw):
        r = _socket_runner()
        r._web.chat_postMessage = AsyncMock(**post_kw)
        r._post_or_update = AsyncMock()  # the reply site has its own pins below
        parent, audit = _recorder(r._web.chat_postMessage)
        parent.attach_mock(r.intent_service.process_intent, "llm_turn")
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await r._handle_event(dict(DM_EVENT))
        return r, parent, audit

    async def test_success_row_precedes_the_llm_turn(self):
        r, parent, audit = await self._run(return_value={"ok": True, "ts": "999.0"})
        (kw,) = _assert_rows(parent, audit, site="slack.socket.placeholder", statuses=["success"])
        # credits_spent=False is the rule applied: no LLM call precedes this write
        names = [c[0] for c in parent.mock_calls if c[0] in ("audit", "llm_turn")]
        assert names == ["audit", "llm_turn"], names
        assert kw["details"] == {"slack_user": "U777"}
        assert kw["resource_id"] == "D1"
        assert r._post_or_update.await_args.args[1] == "999.0"  # placeholder ts still used

    async def test_ok_false_is_failed(self):
        _, parent, audit = await self._run(return_value={"ok": False, "error": "not_in_channel"})
        (kw,) = _assert_rows(parent, audit, site="slack.socket.placeholder", statuses=["failed"])
        assert kw["details"]["error"] == "not_in_channel"

    async def test_known_api_refusal_is_failed_and_reply_still_runs(self):
        r, parent, audit = await self._run(side_effect=_api_error("channel_not_found"))
        (kw,) = _assert_rows(parent, audit, site="slack.socket.placeholder", statuses=["failed"])
        assert kw["details"]["error"] == "channel_not_found"
        r._post_or_update.assert_awaited_once()  # existing fallback path unchanged

    async def test_other_exception_is_unconfirmed(self):
        _, parent, audit = await self._run(side_effect=TimeoutError("slow"))
        _assert_rows(parent, audit, site="slack.socket.placeholder", statuses=["unconfirmed"])


class TestSocketReplySite:
    async def _run(self, ts, *, update_kw=None, post_kw=None):
        r = _socket_runner()
        parent = MagicMock()
        r._web.chat_update = AsyncMock(**(update_kw or {}))
        r._web.chat_postMessage = AsyncMock(**(post_kw or {}))
        parent.attach_mock(r._web.chat_update, "client_call")
        audit = AsyncMock(return_value=None)
        parent.attach_mock(audit, "audit")
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await r._post_or_update("D1", ts, "Hello", None)
        return r, parent, audit

    async def test_update_success_one_row(self):
        r, parent, audit = await self._run("999.0", update_kw={"return_value": {"ok": True}})
        (kw,) = _assert_rows(parent, audit, site="slack.socket.reply", statuses=["success"])
        assert kw["details"] == {"call": "chat_update"}
        r._web.chat_postMessage.assert_not_awaited()

    async def test_fresh_post_success(self):
        r = _socket_runner()
        r._web.chat_postMessage = AsyncMock(return_value={"ok": True, "ts": "1.0"})
        parent, audit = _recorder(r._web.chat_postMessage)
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await r._post_or_update("D1", None, "Hello", "5.0")
        (kw,) = _assert_rows(parent, audit, site="slack.socket.reply", statuses=["success"])
        assert kw["details"] == {"call": "chat_postMessage"}

    async def test_update_refused_then_fallback_post_two_rows(self):
        r = _socket_runner()
        parent = MagicMock()
        r._web.chat_update = AsyncMock(side_effect=_api_error("message_not_found"))
        r._web.chat_postMessage = AsyncMock(return_value={"ok": True, "ts": "2.0"})
        parent.attach_mock(r._web.chat_update, "client_call")
        parent.attach_mock(r._web.chat_postMessage, "post")
        audit = AsyncMock(return_value=None)
        parent.attach_mock(audit, "audit")
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await r._post_or_update("D1", "999.0", "Hello", None)
        names = [c[0] for c in parent.mock_calls if c[0] in ("client_call", "post", "audit")]
        assert names == ["client_call", "audit", "post", "audit"], names
        rows = [c.kwargs for c in audit.await_args_list]
        assert [r_["status"] for r_ in rows] == ["failed", "success"]
        assert rows[0]["details"]["call"] == "chat_update"
        assert rows[0]["details"]["error"] == "message_not_found"
        assert rows[1]["details"] == {"call": "chat_postMessage"}
        assert all(r_["credits_spent"] is False and r_["user_id"] == _USER for r_ in rows)

    async def test_fallback_post_raises_records_then_raises(self):
        r = _socket_runner()
        r._web.chat_postMessage = AsyncMock(side_effect=ConnectionError("reset"))
        parent, audit = _recorder(r._web.chat_postMessage)
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            with pytest.raises(ConnectionError):
                await r._post_or_update("D1", None, "Hello", None)
        (kw,) = _assert_rows(parent, audit, site="slack.socket.reply", statuses=["unconfirmed"])
        assert kw["details"]["call"] == "chat_postMessage"

    async def test_test_double_response_is_unconfirmed_not_success(self):
        # an SDK result with no readable ``ok`` (here a bare MagicMock) is not proof
        _, parent, audit = await self._run("999.0", update_kw={"return_value": MagicMock()})
        _assert_rows(parent, audit, site="slack.socket.reply", statuses=["unconfirmed"])


SLASH_PAYLOAD = {
    "command": "/piper",
    "text": "help",
    "user_id": "U123",
    "team_id": "T123",
    "channel_id": "C123",
    "response_url": "https://hooks.slack.com/commands/T123/respond",
}


class TestSocketSlashReplySite:
    async def _run(self, **send_kw):
        r = _socket_runner()
        router = MagicMock()
        router._process_slash_command = AsyncMock(
            return_value={"response_type": "ephemeral", "text": "help text"}
        )
        webhook = MagicMock()
        webhook.send_dict = AsyncMock(**send_kw)
        parent, audit = _recorder(webhook.send_dict)
        with (
            patch(
                "services.integrations.slack.webhook_router.SlackWebhookRouter",
                return_value=router,
            ),
            patch("slack_sdk.webhook.async_client.AsyncWebhookClient", return_value=webhook),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            await r._handle_slash_command(dict(SLASH_PAYLOAD))
        return parent, audit

    async def test_http_200_is_success(self):
        parent, audit = await self._run(return_value=SimpleNamespace(status_code=200, body="ok"))
        (kw,) = _assert_rows(
            parent, audit, site="slack.socket.slash_reply", statuses=["success"], user_id="U123"
        )
        assert kw["resource_id"] == "C123"

    async def test_http_4xx_is_failed(self):
        parent, audit = await self._run(
            return_value=SimpleNamespace(status_code=404, body="expired_url")
        )
        (kw,) = _assert_rows(
            parent, audit, site="slack.socket.slash_reply", statuses=["failed"], user_id="U123"
        )
        assert kw["details"] == {"status_code": 404, "error": "expired_url"}

    async def test_raise_is_unconfirmed_and_contained(self):
        parent, audit = await self._run(side_effect=ConnectionError("reset"))
        _assert_rows(
            parent,
            audit,
            site="slack.socket.slash_reply",
            statuses=["unconfirmed"],
            user_id="U123",
        )  # and the handler did not raise into the socket loop


# ── GithubIssueCommand.execute ───────────────────────────────────────────────────


class TestGithubIssueCommandSite:
    async def _run(self, **create_kw):
        from services.actions.commands.github_issue_command import GithubIssueCommand

        svc = MagicMock()
        svc.create_issue = AsyncMock(**create_kw)
        parent, audit = _recorder(svc.create_issue)
        cmd = GithubIssueCommand(
            {"title": "T", "repo": "o/r"}, {"github_service": svc, "user_id": _USER}
        )
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            result = await cmd.execute()
        return parent, audit, result

    async def test_success(self):
        parent, audit, result = await self._run(return_value={"number": 9, "html_url": "u"})
        (kw,) = _assert_rows(
            parent, audit, site="github.command.create_issue", statuses=["success"]
        )
        assert kw["details"] == {"issue_number": 9} and kw["resource_id"] == "o/r"
        assert result["status"] == "success"

    async def test_refused_is_failed_and_envelope_unchanged(self):
        parent, audit, result = await self._run(side_effect=GitHubWriteRefused("no"))
        _assert_rows(parent, audit, site="github.command.create_issue", statuses=["failed"])
        assert result["status"] == "error"

    async def test_timeout_is_unconfirmed(self):
        parent, audit, result = await self._run(side_effect=TimeoutError("slow"))
        (kw,) = _assert_rows(
            parent, audit, site="github.command.create_issue", statuses=["unconfirmed"]
        )
        assert kw["details"]["write_unconfirmed"] == "raised_without_verifiable_result"
        assert result["status"] == "error"


# ── GitHubDomainService ──────────────────────────────────────────────────────────


def _domain(method, **kw):
    from services.domain.github_domain_service import GitHubDomainService

    agent = MagicMock()
    setattr(agent, method, AsyncMock(**kw))
    parent, audit = _recorder(getattr(agent, method))
    return GitHubDomainService(github_agent=agent), agent, parent, audit


class TestGithubDomainCreateIssueSite:
    async def test_slug_branch_success(self):
        svc, agent, parent, audit = _domain("create_issue", return_value={"number": 3})
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            assert await svc.create_issue("o/r", "T", "B") == {"number": 3}
        (kw,) = _assert_rows(
            parent, audit, site="github.domain.create_issue", statuses=["success"], user_id=None
        )
        assert kw["details"] == {"issue_number": 3}
        assert agent.create_issue.await_args.kwargs["owner"] == "o"

    async def test_bare_name_branch_success(self):
        svc, agent, parent, audit = _domain("create_issue", return_value={"number": 4})
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await svc.create_issue("r", "T", "B")
        _assert_rows(
            parent, audit, site="github.domain.create_issue", statuses=["success"], user_id=None
        )
        assert "owner" not in agent.create_issue.await_args.kwargs

    async def test_refused_records_then_raises(self):
        svc, _, parent, audit = _domain("create_issue", side_effect=GitHubWriteRefused("no"))
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            with pytest.raises(GitHubWriteRefused):
                await svc.create_issue("o/r", "T", "B")
        _assert_rows(
            parent, audit, site="github.domain.create_issue", statuses=["failed"], user_id=None
        )

    async def test_empty_result_is_unconfirmed(self):
        svc, _, parent, audit = _domain("create_issue", return_value={})
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await svc.create_issue("o/r", "T", "B")
        _assert_rows(
            parent,
            audit,
            site="github.domain.create_issue",
            statuses=["unconfirmed"],
            user_id=None,
        )


class TestGithubDomainUpdateIssueSite:
    async def test_success(self):
        svc, _, parent, audit = _domain("update_issue", return_value={"number": 5})
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            assert await svc.update_issue("o/r", 5, state="closed") == {"number": 5}
        (kw,) = _assert_rows(
            parent, audit, site="github.domain.update_issue", statuses=["success"], user_id=None
        )
        assert kw["resource_type"] == "github_issue" and kw["resource_id"] == "5"
        assert kw["details"] == {"repo": "o/r", "fields": ["state"]}

    async def test_maybe_landed_is_unconfirmed_and_raises(self):
        svc, _, parent, audit = _domain(
            "update_issue", side_effect=RuntimeError("write may or may not have landed")
        )
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            with pytest.raises(RuntimeError):
                await svc.update_issue("o/r", 5, title="New")
        (kw,) = _assert_rows(
            parent,
            audit,
            site="github.domain.update_issue",
            statuses=["unconfirmed"],
            user_id=None,
        )
        assert kw["details"]["write_unconfirmed"] == "may_or_may_not_have_landed"


# ── Outcome mappers ──────────────────────────────────────────────────────────────


class TestSlackSdkOutcome:
    def test_ok_true_false_and_absent(self):
        assert co.slack_sdk_outcome({"ok": True}) == ("success", {})
        assert co.slack_sdk_outcome({"ok": False, "error": "is_archived"}) == (
            "failed",
            {"error": "is_archived"},
        )
        assert co.slack_sdk_outcome(None)[0] == "unconfirmed"
        assert co.slack_sdk_outcome(MagicMock())[0] == "unconfirmed"

    def test_sdk_slack_response_reads_data(self):
        assert co.slack_sdk_outcome(SimpleNamespace(data={"ok": True}))[0] == "success"

    def test_webhook_status_codes(self):
        assert co.slack_sdk_outcome(SimpleNamespace(status_code=200, body="ok"))[0] == "success"
        assert co.slack_sdk_outcome(SimpleNamespace(status_code=403, body="x"))[0] == "failed"
        assert co.slack_sdk_outcome(SimpleNamespace(status_code=500, body="x"))[0] == (
            "unconfirmed"
        )

    def test_api_error_known_code_failed_unknown_unconfirmed(self):
        assert co.slack_sdk_error_outcome(_api_error("not_in_channel"))[0] == "failed"
        status, details = co.slack_sdk_error_outcome(_api_error("internal_error"))
        assert status == "unconfirmed" and details["error"] == "internal_error"
        assert co.slack_sdk_error_outcome(TimeoutError())[0] == "unconfirmed"

    def test_domain_envelope(self):
        assert co.domain_send_result_outcome({"success": True}) == ("success", {})
        assert co.domain_send_result_outcome({"success": False})[0] == "unconfirmed"
        assert co.domain_send_result_outcome(None)[0] == "unconfirmed"

    def test_landing_a_names_still_resolve_to_the_shared_mappers(self):
        from services.integrations.slack import response_handler as rh
        from services.intent import intent_service as isvc

        assert isvc._github_write_audit_outcome is co.github_write_outcome
        assert rh._slack_send_audit_outcome is co.slack_send_outcome
        assert rh._slack_send_error_outcome is co.slack_send_error_outcome
