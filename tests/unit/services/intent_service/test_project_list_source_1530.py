"""#1530: Chat "what are my projects?" must read the SAME owner-scoped truth
as the /projects page.

Incident: chat answered "two projects: Klatch and One Job" while the /projects
page showed three (CoVa active). Both paths ultimately call
ProjectRepository.list_active_projects(owner_id=...), but the chat path wrapped
it in UserContextService's process-lifetime cache, which no project write ever
invalidates — so a project created (or unarchived) after first cache fill was
invisible to chat forever, while the page ran a fresh query per request.

Fix under test:
1. UserContextService.get_user_context refreshes DB-sourced projects on every
   call with a user_id (cache hit or not) — live rows, same query as the page.
2. Cross-principal guard (#1501 family): the DB read is always owner-scoped.
3. m-44 denominator: ContextAssembler._compute_user_context emits
   project_count derived from the actual rows, so the floor never states a
   count the query didn't produce (the display list is sliced to 10).
"""

from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.domain.models import Intent, IntentCategory
from services.user_context_service import UserContext, UserContextService

pytestmark = pytest.mark.asyncio


EMPTY_CONFIG_PATCH = (
    "services.configuration.piper_config_loader.piper_config_loader.load_config"
)


class TestChatReadsLiveProjectRows:
    """The stale-cache regression itself."""

    async def test_project_created_after_cache_fill_appears_in_chat_context(self):
        """Cache filled with 2 projects; DB now has 3 (CoVa added).

        The next get_user_context call must return 3 — pre-fix it returned the
        cached 2 forever.
        """
        svc = UserContextService()
        user_id = uuid4()

        with patch(EMPTY_CONFIG_PATCH, return_value={}):
            with patch.object(
                svc, "_load_user_preferences_from_db", AsyncMock(return_value={})
            ):
                db_load = AsyncMock(return_value=["Klatch", "One Job"])
                with patch.object(svc, "_load_projects_from_db", db_load):
                    first = await svc.get_user_context("session-1", user_id)
                    assert first.projects == ["Klatch", "One Job"]

                    # CoVa is created (portfolio onboarding / POST /projects).
                    db_load.return_value = ["CoVa", "Klatch", "One Job"]

                    second = await svc.get_user_context("session-1", user_id)

        assert "CoVa" in second.projects, (
            "Project created after cache fill is invisible to chat "
            "(stale UserContextService cache — issue #1530)"
        )
        assert len(second.projects) == 3

    async def test_all_projects_archived_after_cache_fill_do_not_linger(self):
        """Inverse staleness: DB rows cached, then every project archived.

        The stale DB names must not survive; the fallback chain (prefs →
        config) applies exactly as on a cold load.
        """
        svc = UserContextService()
        user_id = uuid4()

        with patch(EMPTY_CONFIG_PATCH, return_value={}):
            with patch.object(
                svc, "_load_user_preferences_from_db", AsyncMock(return_value={})
            ):
                db_load = AsyncMock(return_value=["Klatch", "One Job", "CoVa"])
                with patch.object(svc, "_load_projects_from_db", db_load):
                    first = await svc.get_user_context("session-1", user_id)
                    assert len(first.projects) == 3

                    db_load.return_value = []  # all archived

                    second = await svc.get_user_context("session-1", user_id)

        assert second.projects == [], (
            "Archived projects still reported from stale cache"
        )


class TestCrossPrincipalGuard:
    """#1501 family: another owner's projects never appear."""

    async def test_db_load_is_owner_scoped(self):
        """_load_projects_from_db must pass owner_id=str(user_id) to the same
        repository method the /projects page calls."""
        svc = UserContextService()
        user_id = uuid4()

        repo_instance = MagicMock()
        repo_instance.list_active_projects = AsyncMock(
            return_value=[
                SimpleNamespace(name="Klatch"),
                SimpleNamespace(name="One Job"),
                SimpleNamespace(name="CoVa"),
            ]
        )

        class _FakeScope:
            async def __aenter__(self):
                return MagicMock()

            async def __aexit__(self, *args):
                return False

        with patch(
            "services.database.repositories.ProjectRepository",
            return_value=repo_instance,
        ):
            with patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
                return_value=_FakeScope(),
            ):
                names = await svc._load_projects_from_db(user_id)

        assert names == ["Klatch", "One Job", "CoVa"]
        repo_instance.list_active_projects.assert_awaited_once_with(
            owner_id=str(user_id)
        )

    async def test_two_owners_never_see_each_others_projects(self):
        """Owner A and owner B resolve to disjoint project lists — including on
        the cache-hit refresh path."""
        svc = UserContextService()
        owner_a, owner_b = uuid4(), uuid4()
        rows = {
            str(owner_a): ["Klatch", "One Job", "CoVa"],
            str(owner_b): ["Intruder"],
        }

        async def per_owner(uid):
            return list(rows[str(uid)])

        with patch(EMPTY_CONFIG_PATCH, return_value={}):
            with patch.object(
                svc, "_load_user_preferences_from_db", AsyncMock(return_value={})
            ):
                with patch.object(
                    svc, "_load_projects_from_db", AsyncMock(side_effect=per_owner)
                ):
                    ctx_a = await svc.get_user_context("session-a", owner_a)
                    ctx_b = await svc.get_user_context("session-b", owner_b)
                    # Second round hits the cache — refresh must stay scoped.
                    ctx_a2 = await svc.get_user_context("session-a", owner_a)

        assert "Intruder" not in ctx_a.projects
        assert "Intruder" not in ctx_a2.projects
        assert ctx_b.projects == ["Intruder"]
        assert "CoVa" not in ctx_b.projects


class TestChatAnswerMatchesRows:
    """The chat handler's answer lists all rows and states the row-derived count."""

    async def test_answer_includes_all_three_projects_and_matching_count(self):
        from services.intent_service.canonical_handlers import CanonicalHandlers

        handlers = CanonicalHandlers()
        user_id = str(uuid4())
        ctx = UserContext(
            user_id=user_id, projects=["Klatch", "One Job", "CoVa"]
        )

        intent = Intent(
            category=IntentCategory.STATUS,
            action="provide_status",
            original_message="what are my projects?",
        )

        with patch(
            "services.intent_service.canonical_handlers.user_context_service"
        ) as mock_svc:
            mock_svc.get_user_context = AsyncMock(return_value=ctx)
            with patch.object(
                handlers, "_get_project_metadata", AsyncMock(return_value={})
            ):
                result = await handlers._handle_status_query(
                    intent, "session-1", user_id=user_id
                )

        message = result["message"]
        for name in ("Klatch", "One Job", "CoVa"):
            assert name in message, f"Project {name} missing from chat answer"
        assert "3 active projects" in message, (
            "Stated count must be derived from the actual rows returned (m-44)"
        )
        assert "2 active projects" not in message


class TestM44DenominatorInFloorContext:
    """m-44: never state a count the query didn't produce."""

    async def test_assembler_emits_row_derived_count_alongside_sliced_list(self):
        from services.intent_service.context_assembler import ContextAssembler

        assembler = ContextAssembler()
        projects = [f"Project {i}" for i in range(12)]
        ctx = UserContext(user_id=str(uuid4()), projects=projects)

        with patch(
            "services.user_context_service.user_context_service"
        ) as mock_svc:
            mock_svc.get_user_context = AsyncMock(return_value=ctx)
            result = await assembler._compute_user_context("test-user")

        assert len(result["projects"]) == 10  # display slice
        assert result["project_count"] == 12, (
            "The true denominator must ride with the truncated display list"
        )

    async def test_floor_renders_true_count_and_plain_names(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        floor = ConversationalFloor.__new__(ConversationalFloor)
        domain_context = {
            "projects": [{"name": "Klatch"}, {"name": "One Job"}, {"name": "CoVa"}],
            "project_count": 3,
        }
        rendered = floor._format_domain_context(domain_context)

        assert '"Klatch"' in rendered
        assert '"CoVa"' in rendered
        assert "{'name'" not in rendered, "dict repr leaked into floor context"
        assert "3" in rendered

    async def test_floor_flags_truncation_when_count_exceeds_listed(self):
        from services.intent_service.conversational_floor import ConversationalFloor

        floor = ConversationalFloor.__new__(ConversationalFloor)
        domain_context = {
            "projects": [{"name": f"P{i}"} for i in range(10)],
            "project_count": 12,
        }
        rendered = floor._format_domain_context(domain_context)

        assert "12" in rendered, "true denominator missing"
