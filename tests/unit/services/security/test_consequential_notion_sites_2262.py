"""#2262 (Arch's option 2, 2026-11-03; PPM placed it in Production C): the Notion writes
are #1680 consequential sites. Each pin drives the real function with the Notion client
mocked, and ``audit_logger.log_consequential_action`` replaced by a recorder on the same
parent mock, so it asserts ORDER (the row is written after the write), the site key, the
status from the outcome, ``credits_spent`` from the site's own path, and the principal.

DENOMINATOR: the four registered Notion sites (chat append, standup page, the operator
CLI's page and database entry). For each, success and an empty result; for the two
person-facing sites, a raised write too. Then one scratch-database row per site, counted
by the real admin read, and the person-facing words.
"""

import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.security import audit_logger as al
from services.security import consequential_outcomes as co
from services.security.consequential_sites import CONSEQUENTIAL_SITES, NOTION, action_line

_USER = "11111111-1111-1111-1111-111111111111"
NOTION_SITES = (
    "notion.chat.append_blocks",
    "notion.standup.create_page",
    "notion.publish.create_page",
    "notion.publish.create_database_item",
)


def _recorder(client_mock):
    parent = MagicMock()
    parent.attach_mock(client_mock, "client_call")
    audit = AsyncMock(return_value=None)
    parent.attach_mock(audit, "audit")
    return parent, audit


def _order(parent):
    return [c[0] for c in parent.mock_calls if c[0] in ("client_call", "audit")]


def _row(parent, audit, *, site, status, user_id, credits_spent):
    assert _order(parent) == ["client_call", "audit"], _order(parent)
    (call,) = audit.await_args_list
    kw = call.kwargs
    assert kw["site"] == site and CONSEQUENTIAL_SITES[site].instrumented is True
    assert kw["status"] == status
    assert kw["credits_spent"] is credits_spent
    assert kw["user_id"] == user_id
    return kw


class TestOutcomes:
    def test_a_result_is_success_and_none_is_unconfirmed(self):
        assert co.notion_write_result_outcome({"id": "p"}) == ("success", {})
        assert co.notion_write_result_outcome(None)[0] == "unconfirmed"

    def test_a_raised_write_is_unconfirmed_never_failed(self):
        status, details = co.notion_write_outcome(RuntimeError("boom"))
        assert status == "unconfirmed" and details == {"write_error": "RuntimeError"}


# ── Chat: update a document (append_blocks) ──────────────────────────────────────


class TestChatAppendSite:
    async def _run(self, append):
        from services.domain.models import Intent
        from services.intent.intent_service import IntentService
        from services.shared_types import IntentCategory

        intent = Intent(
            category=IntentCategory.QUERY,
            action="update_document_query",
            confidence=1.0,
            context={"original_message": "update the README with new text", "user_id": _USER},
        )
        router = MagicMock()
        router.ais_available = AsyncMock(return_value=True)
        router.connect_for_user = AsyncMock()
        router.search_notion = AsyncMock(
            return_value=[
                {
                    "id": "page-123",
                    "url": "https://notion.so/readme",
                    "properties": {"title": {"title": [{"text": {"content": "README"}}]}},
                }
            ]
        )
        router.append_blocks = append
        parent, audit = _recorder(append)
        with (
            patch(
                "services.integrations.notion.notion_integration_router.NotionIntegrationRouter",
                return_value=router,
            ),
            patch(
                "services.slot_filling.slot_extractor.extract_slots",
                new_callable=AsyncMock,
                return_value={"doc_name": "README", "content": "new text"},
            ),
            patch("services.intent.intent_service._principal_from_intent", return_value=_USER),
            patch.object(al.audit_logger, "log_consequential_action", audit),
        ):
            result = await IntentService()._handle_update_document_notion(intent, "wf", "s")
        return parent, audit, result

    async def test_success(self):
        parent, audit, result = await self._run(AsyncMock(return_value={"results": [{}]}))
        kw = _row(
            parent,
            audit,
            site="notion.chat.append_blocks",
            status="success",
            user_id=_USER,
            credits_spent=True,
        )
        assert kw["resource_type"] == "notion_page" and kw["resource_id"] == "page-123"
        assert result.success is True

    async def test_an_empty_result_is_unconfirmed(self):
        parent, audit, result = await self._run(AsyncMock(return_value=None))
        _row(
            parent,
            audit,
            site="notion.chat.append_blocks",
            status="unconfirmed",
            user_id=_USER,
            credits_spent=True,
        )
        assert result.success is False

    async def test_a_raised_write_is_unconfirmed(self):
        parent, audit, _ = await self._run(AsyncMock(side_effect=RuntimeError("down")))
        kw = _row(
            parent,
            audit,
            site="notion.chat.append_blocks",
            status="unconfirmed",
            user_id=_USER,
            credits_spent=True,
        )
        assert kw["details"] == {"write_error": "RuntimeError"}


# ── Standup to Notion (create_page) ──────────────────────────────────────────────


class TestStandupPageSite:
    async def _run(self, create):
        from services.integrations.mcp.skills.standup_workflow_skill import StandupWorkflowSkill

        skill = StandupWorkflowSkill.__new__(StandupWorkflowSkill)
        skill._notion_service = SimpleNamespace(create_page=create)
        skill._get_user_notion_database = AsyncMock(return_value="db-9")
        parent, audit = _recorder(create)
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            result = await skill._update_notion(_USER, {"summary": "s"})
        return parent, audit, result

    async def test_success(self):
        parent, audit, result = await self._run(AsyncMock(return_value={"id": "page-7"}))
        kw = _row(
            parent,
            audit,
            site="notion.standup.create_page",
            status="success",
            user_id=_USER,
            credits_spent=False,
        )
        assert kw["resource_type"] == "notion_database" and kw["resource_id"] == "db-9"
        assert result["success"] is True

    async def test_an_empty_result_is_unconfirmed(self):
        parent, audit, result = await self._run(AsyncMock(return_value=None))
        _row(
            parent,
            audit,
            site="notion.standup.create_page",
            status="unconfirmed",
            user_id=_USER,
            credits_spent=False,
        )
        assert result["success"] is False

    async def test_a_raised_write_is_unconfirmed(self):
        parent, audit, result = await self._run(AsyncMock(side_effect=RuntimeError("down")))
        _row(
            parent,
            audit,
            site="notion.standup.create_page",
            status="unconfirmed",
            user_id=_USER,
            credits_spent=False,
        )
        assert result["success"] is False


# ── The operator CLI's publisher (create_page, create_database_item) ─────────────


class TestPublisherSites:
    def _publisher(self, **methods):
        from services.publishing.publisher import Publisher

        pub = Publisher.__new__(Publisher)
        pub.notion = SimpleNamespace(connect=AsyncMock(), **methods)
        return pub

    @pytest.mark.parametrize("returned, status", [({"id": "p1"}, "success"), (None, "unconfirmed")])
    async def test_page(self, returned, status):
        create = AsyncMock(return_value=returned)
        parent, audit = _recorder(create)
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await self._publisher(create_page=create)._publish_to_notion(
                "# Title\n\nbody", "parent-1", "markdown", "doc.md"
            )
        kw = _row(
            parent,
            audit,
            site="notion.publish.create_page",
            status=status,
            user_id=None,
            credits_spent=False,
        )
        assert kw["resource_id"] == "parent-1"

    @pytest.mark.parametrize("returned, status", [({"id": "p1"}, "success"), (None, "unconfirmed")])
    async def test_database_entry(self, returned, status):
        create = AsyncMock(return_value=returned)
        parent, audit = _recorder(create)
        adr = "# ADR-1: Title\n\n- Status: Accepted\n- Author: someone\n\nbody"
        with patch.object(al.audit_logger, "log_consequential_action", audit):
            await self._publisher(create_database_item=create)._publish_to_notion_database(
                adr, "db-1", "markdown", "adr-001.md"
            )
        kw = _row(
            parent,
            audit,
            site="notion.publish.create_database_item",
            status=status,
            user_id=None,
            credits_spent=False,
        )
        assert kw["resource_id"] == "db-1"


# ── Words and the admin read ─────────────────────────────────────────────────────


def test_cxos_slotless_words_and_the_hidden_publisher():
    assert action_line("notion.chat.append_blocks", "page-123", done=True) == (
        "Added to your Notion page"
    )
    assert action_line("notion.standup.create_page", None, done=False) == (
        "post your standup to Notion"
    )
    sites = {k: s for k, s in CONSEQUENTIAL_SITES.items() if s.family == NOTION}
    assert set(sites) == set(NOTION_SITES)
    assert {k for k, s in sites.items() if not s.user_visible} == {
        "notion.publish.create_page",
        "notion.publish.create_database_item",
    }
    for site in sites.values():
        assert "{" not in site.phrase + site.done  # a page id never prints


@pytest.mark.consequential_audit_db
@pytest.mark.parametrize("site", NOTION_SITES)
async def test_the_admin_read_counts_each_notion_site(site):
    from sqlalchemy import text

    from services.database.session_factory import AsyncSessionFactory
    from tests.unit.web.api.routes.test_admin_consequential_1680 import PATH, _client, _db_ready

    await _db_ready()
    before = _client().get(PATH).json()["actions"]["by_site"].get(site, 0)
    log = await al.audit_logger.log_consequential_action(
        site=site,
        status="success",
        user_id=None,
        message=f"#2262 admin read counts {site} {uuid.uuid4().hex[:8]}",
        credits_spent=False,
    )
    assert log is not None
    try:
        after = _client().get(PATH).json()["actions"]["by_site"].get(site, 0)
        assert after - before == 1
    finally:
        async with AsyncSessionFactory.session_scope_fresh() as s:
            await s.execute(text("DELETE FROM audit_logs WHERE id = :id"), {"id": log.id})
            await s.commit()
