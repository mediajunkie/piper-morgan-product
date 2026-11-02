"""#1680 Dashboard Criterion E (landing A): one pin per instrumented site.

Each pin drives the real handler with the GitHub router / Slack client mocked at its
seam and ``audit_logger.log_consequential_action`` replaced by a recorder attached to
the same parent mock, so the pin asserts ORDER (the helper is awaited after the client
call), the site key, the status from the call's outcome, and credits_spent from the
site's own path. DENOMINATOR: the 7 ``instrumented=True`` registry entries; for each,
success and a failure (a definite refusal -> "failed"), plus the unknown-outcome shapes
("unconfirmed") the handlers can produce.
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.integrations.github.github_integration_router import GitHubWriteRefused
from services.intent.intent_service import IntentService
from services.security import audit_logger as al
from services.security.consequential_sites import CONSEQUENTIAL_SITES
from services.shared_types import IntentCategory

ROUTER = "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
_USER = "11111111-1111-1111-1111-111111111111"


@pytest.fixture
def service():
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _parent_with_router(method: str, **kw):
    parent = MagicMock()
    router = MagicMock()
    router.initialize = AsyncMock()
    router.is_available = AsyncMock(return_value=True)
    router.find_open_issue_by_title = AsyncMock(return_value=None)
    setattr(router, method, AsyncMock(**kw))
    parent.attach_mock(getattr(router, method), "client_call")
    audit = AsyncMock(return_value=None)
    parent.attach_mock(audit, "audit")
    return parent, router, audit


def _assert_after_and_one_row(parent, audit, *, site, status, credits_spent):
    names = [c[0] for c in parent.mock_calls if c[0] in ("client_call", "audit")]
    assert names == ["client_call", "audit"], names
    audit.assert_awaited_once()
    kw = audit.await_args.kwargs
    assert kw["site"] == site and site in CONSEQUENTIAL_SITES
    assert CONSEQUENTIAL_SITES[site].instrumented is True
    assert kw["status"] == status
    assert kw["credits_spent"] is credits_spent
    assert kw["user_id"] == _USER
    return kw


def _intent(action, msg, **ctx):
    context = {"original_message": msg, "user_id": _USER, "destructive_confirmed": True}
    context.update(ctx)
    return Intent(category=IntentCategory.EXECUTION, action=action, context=context)


# ── GitHub chat handlers ─────────────────────────────────────────────────────────


class TestCloseIssueSite:
    async def _run(self, service, **kw):
        parent, router, audit = _parent_with_router("update_issue", **kw)
        intent = _intent("close_issue", "yes close #5", repository="o/r")
        with (
            patch(ROUTER, return_value=router),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            result = await service._handle_close_issue_query(intent, "wf")
        return parent, audit, result

    async def test_success(self, service):
        parent, audit, result = await self._run(
            service, return_value={"number": 5, "title": "t", "html_url": "u"}
        )
        kw = _assert_after_and_one_row(
            parent, audit, site="github.chat.close_issue", status="success", credits_spent=False
        )
        assert kw["resource_type"] == "github_issue" and kw["resource_id"] == "5"
        assert result.success is True

    async def test_refused_is_failed(self, service):
        parent, audit, _ = await self._run(service, side_effect=GitHubWriteRefused("no"))
        kw = _assert_after_and_one_row(
            parent, audit, site="github.chat.close_issue", status="failed", credits_spent=False
        )
        assert kw["details"]["error_type"] == "GitHubWriteRefused"

    async def test_maybe_landed_is_unconfirmed(self, service):
        parent, audit, _ = await self._run(
            service, side_effect=Exception("write may or may not have landed")
        )
        kw = _assert_after_and_one_row(
            parent,
            audit,
            site="github.chat.close_issue",
            status="unconfirmed",
            credits_spent=False,
        )
        assert kw["details"]["write_unconfirmed"] == "may_or_may_not_have_landed"


class TestReopenIssueSite:
    async def _run(self, service, **kw):
        parent, router, audit = _parent_with_router("update_issue", **kw)
        intent = _intent("reopen_issue", "yes reopen #6", repository="o/r")
        with (
            patch(ROUTER, return_value=router),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            return parent, audit, await service._handle_reopen_issue_query(intent, "wf")

    async def test_success(self, service):
        parent, audit, result = await self._run(
            service, return_value={"number": 6, "title": "t", "html_url": "u"}
        )
        _assert_after_and_one_row(
            parent, audit, site="github.chat.reopen_issue", status="success", credits_spent=False
        )
        assert result.success is True

    async def test_no_repo_is_failed(self, service):
        parent, audit, _ = await self._run(
            service, side_effect=RuntimeError("no repo could be resolved for this write")
        )
        kw = _assert_after_and_one_row(
            parent, audit, site="github.chat.reopen_issue", status="failed", credits_spent=False
        )
        assert kw["details"]["reason"] == "no_repo_resolved"


class TestCommentIssueSite:
    async def _run(self, service, **kw):
        parent, router, audit = _parent_with_router("add_comment", **kw)
        intent = _intent("comment_issue", "comment on #42 saying green", repository="o/r")
        with (
            patch(ROUTER, return_value=router),
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"issue_number": "42", "comment_text": "green"},
            ),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            return parent, audit, await service._handle_comment_issue_query(intent, "wf")

    async def test_success_spends_credits(self, service):
        parent, audit, result = await self._run(service, return_value={"html_url": "u"})
        _assert_after_and_one_row(
            parent, audit, site="github.chat.comment_issue", status="success", credits_spent=True
        )
        assert result.success is True

    async def test_none_result_is_unconfirmed(self, service):
        parent, audit, result = await self._run(service, return_value=None)
        kw = _assert_after_and_one_row(
            parent,
            audit,
            site="github.chat.comment_issue",
            status="unconfirmed",
            credits_spent=True,
        )
        assert kw["details"]["write_unconfirmed"] == "add_comment_returned_none"
        assert result.success is False

    async def test_refused_is_failed(self, service):
        parent, audit, _ = await self._run(service, side_effect=GitHubWriteRefused("no"))
        _assert_after_and_one_row(
            parent, audit, site="github.chat.comment_issue", status="failed", credits_spent=True
        )


class TestCreateIssueSite:
    async def _run(self, service, **kw):
        parent, router, audit = _parent_with_router("create_issue", **kw)
        intent = _intent(
            "create_issue", "create an issue in o/r", repository="o/r", title="Flaky login"
        )
        with (
            patch(ROUTER, return_value=router),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            return (
                parent,
                audit,
                await service._handle_create_issue(intent, "wf", None, user_id=_USER),
            )

    async def test_success(self, service):
        parent, audit, result = await self._run(
            service, return_value={"number": 10, "title": "Flaky login", "html_url": "u"}
        )
        kw = _assert_after_and_one_row(
            parent, audit, site="github.chat.create_issue", status="success", credits_spent=False
        )
        assert kw["resource_type"] == "github_repository" and kw["resource_id"] == "o/r"
        assert kw["details"] == {"issue_number": 10}
        assert result.success is True

    async def test_refused_is_failed(self, service):
        parent, audit, _ = await self._run(service, side_effect=GitHubWriteRefused("no"))
        _assert_after_and_one_row(
            parent, audit, site="github.chat.create_issue", status="failed", credits_spent=False
        )

    async def test_other_exception_is_unconfirmed(self, service):
        parent, audit, _ = await self._run(service, side_effect=TimeoutError("slow"))
        kw = _assert_after_and_one_row(
            parent,
            audit,
            site="github.chat.create_issue",
            status="unconfirmed",
            credits_spent=False,
        )
        assert kw["details"]["write_unconfirmed"] == "raised_without_verifiable_result"


class TestUpdateIssueSite:
    async def _run(self, service, **kw):
        parent, router, audit = _parent_with_router("update_issue", **kw)
        intent = _intent(
            "update_issue", "update #8", repository="o/r", issue_number=8, title="New title"
        )
        with (
            patch(ROUTER, return_value=router),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            return parent, audit, await service._handle_update_issue(intent, "wf", user_id=_USER)

    async def test_success(self, service):
        parent, audit, result = await self._run(
            service, return_value={"number": 8, "title": "New title", "html_url": "u"}
        )
        kw = _assert_after_and_one_row(
            parent, audit, site="github.chat.update_issue", status="success", credits_spent=False
        )
        assert kw["details"] == {"fields": ["title"]}
        assert result.success is True

    async def test_refused_is_failed(self, service):
        parent, audit, _ = await self._run(service, side_effect=GitHubWriteRefused("no"))
        _assert_after_and_one_row(
            parent, audit, site="github.chat.update_issue", status="failed", credits_spent=False
        )


# ── Slack response sends ─────────────────────────────────────────────────────────


def _slack_handler(**send_kw):
    from services.integrations.slack.response_handler import SlackResponseHandler

    handler = SlackResponseHandler(
        spatial_adapter=MagicMock(),
        intent_classifier=MagicMock(),
        slack_client=MagicMock(),
        intent_service=MagicMock(),
    )
    parent = MagicMock()
    handler.slack_client.send_message = AsyncMock(**send_kw)
    parent.attach_mock(handler.slack_client.send_message, "client_call")
    audit = AsyncMock(return_value=None)
    parent.attach_mock(audit, "audit")
    return handler, parent, audit


def _slack_ctx(channel):
    return {"channel_id": channel, "connector_user_id": _USER, "user_id": "U123"}


@pytest.fixture
def clean_buffer():
    from services.integrations.slack.response_handler import MESSAGE_CONSOLIDATION_BUFFER

    MESSAGE_CONSOLIDATION_BUFFER.clear()
    yield
    MESSAGE_CONSOLIDATION_BUFFER.clear()


class TestSlackIndividualSite:
    async def _run(self, **send_kw):
        handler, parent, audit = _slack_handler(**send_kw)
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            result = await handler._send_slack_response(
                {"type": "simple_response", "content": "hello"}, _slack_ctx("C-ind")
            )
        return parent, audit, result

    async def test_success(self, clean_buffer):
        parent, audit, result = await self._run(return_value=MagicMock(success=True))
        kw = _assert_after_and_one_row(
            parent, audit, site="slack.response.individual", status="success", credits_spent=False
        )
        assert kw["resource_type"] == "slack_channel" and kw["resource_id"] == "C-ind"
        assert result is not None

    async def test_slack_refusal_is_failed(self, clean_buffer):
        parent, audit, _ = await self._run(
            return_value=MagicMock(success=False, error=MagicMock(message="channel_not_found"))
        )
        kw = _assert_after_and_one_row(
            parent, audit, site="slack.response.individual", status="failed", credits_spent=False
        )
        assert kw["details"] == {"error": "channel_not_found"}

    async def test_exception_is_unconfirmed_and_still_handled(self, clean_buffer):
        parent, audit, result = await self._run(side_effect=ConnectionError("reset"))
        _assert_after_and_one_row(
            parent,
            audit,
            site="slack.response.individual",
            status="unconfirmed",
            credits_spent=False,
        )
        assert result is None  # the handler's existing error path is unchanged

    async def test_sender_fallback_principal_passes_through(self, clean_buffer):
        handler, parent, audit = _slack_handler(return_value={"ok": True})
        ctx = {"channel_id": "C-x", "user_id": "U123"}
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await handler._send_slack_response({"type": "simple_response", "content": "hi"}, ctx)
        assert audit.await_args.kwargs["user_id"] == "U123"
        assert audit.await_args.kwargs["status"] == "success"


class TestSlackConsolidatedSite:
    async def _run(self, **send_kw):
        handler, parent, audit = _slack_handler(**send_kw)
        ctx = _slack_ctx("C-con")
        handler._add_to_consolidation_buffer({"content": "a", "type": "simple_response"}, ctx)
        handler._add_to_consolidation_buffer({"content": "b", "type": "simple_response"}, ctx)
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            return parent, audit, handler, ctx

    async def test_success(self, clean_buffer):
        parent, audit, handler, ctx = await self._run(return_value=MagicMock(success=True))
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            result = await handler._send_consolidated_response(ctx)
        _assert_after_and_one_row(
            parent,
            audit,
            site="slack.response.consolidated",
            status="success",
            credits_spent=False,
        )
        assert result["consolidated_count"] == 2

    async def test_exception_records_then_raises(self, clean_buffer):
        parent, audit, handler, ctx = await self._run(
            side_effect=RuntimeError("No Slack integration available for send_message.")
        )
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            with pytest.raises(RuntimeError):
                await handler._send_consolidated_response(ctx)
        kw = _assert_after_and_one_row(
            parent,
            audit,
            site="slack.response.consolidated",
            status="failed",
            credits_spent=False,
        )
        assert kw["details"]["reason"] == "no_slack_integration"
