"""
Tests for #862: Conversational handler — "link repo to project".

Tests pre-classifier pattern detection and handler behavior for
repository management operations (link, unlink, list).
"""

from contextlib import asynccontextmanager
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent_service.canonical_handlers import CanonicalHandlers
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

pytestmark = pytest.mark.unit

# Patch paths — imports are local inside _handle_repo_management,
# so we patch the source modules.
_PATCH_SESSION_FACTORY = "services.database.session_factory.AsyncSessionFactory"
_PATCH_PROJECT_REPO = "services.database.repositories.ProjectRepository"
_PATCH_REPO_REPO = "services.database.repositories.RepositoryRepository"


def _mock_session_factory():
    """Create an async context manager mock for AsyncSessionFactory.session_scope."""
    mock_session = AsyncMock()

    @asynccontextmanager
    async def _session_scope():
        yield mock_session

    mock_factory = MagicMock()
    mock_factory.session_scope = _session_scope
    return mock_factory, mock_session


# ---------------------------------------------------------------------------
# Pre-classifier pattern tests
# ---------------------------------------------------------------------------


class TestRepoManagementPatterns:
    """Test REPO_MANAGEMENT_PATTERNS matching in pre_classifier."""

    @pytest.mark.parametrize(
        "message",
        [
            "link mediajunkie/piper-morgan to my project",
            "link repo to Piper Morgan",
            "connect my repository to Piper Morgan",
            "connect mediajunkie/piper-morgan to project",
            "add my repo to Piper Morgan",
            "add mediajunkie/piper-morgan to my project",
        ],
    )
    def test_link_patterns_detected(self, message: str):
        """Test that link/connect/add repo patterns route to PORTFOLIO/manage_repos."""
        result = PreClassifier.pre_classify(message)

        assert result is not None, f"'{message}' should match a pattern"
        assert (
            result.category == IntentCategory.PORTFOLIO
        ), f"'{message}' should route to PORTFOLIO, got {result.category}"
        assert result.action == "manage_repos"

    @pytest.mark.parametrize(
        "message",
        [
            "unlink my repository",
            "remove the repo from my project",
            "disconnect my repository",
        ],
    )
    def test_unlink_patterns_detected(self, message: str):
        """Test that unlink/remove/disconnect patterns route to
        PORTFOLIO/unlink_repo (#1926 / Arch's 2026-10-04 re-point, §1):
        REPO_UNLINK_PATTERNS now claims these literals (moved out of
        REPO_MANAGEMENT_PATTERNS), so the turn reaches the DESTRUCTIVE
        rail's #1190 confirm instead of the unconfirmed manage_repos
        canonical branch. Was action == 'manage_repos' before the
        re-point."""
        result = PreClassifier.pre_classify(message)

        assert result is not None, f"'{message}' should match a pattern"
        assert (
            result.category == IntentCategory.PORTFOLIO
        ), f"'{message}' should route to PORTFOLIO, got {result.category}"
        assert result.action == "unlink_repo"

    @pytest.mark.parametrize(
        "message",
        [
            "show my linked repos",
            "which repos are linked",
            "show project repositories",
        ],
    )
    def test_list_patterns_detected(self, message: str):
        """Test that list/show/which repo patterns route to PORTFOLIO/manage_repos."""
        result = PreClassifier.pre_classify(message)

        assert result is not None, f"'{message}' should match a pattern"
        assert (
            result.category == IntentCategory.PORTFOLIO
        ), f"'{message}' should route to PORTFOLIO, got {result.category}"
        assert result.action == "manage_repos"

    def test_not_false_positive_report(self):
        """'report on the repo' should NOT match repo management patterns."""
        result = PreClassifier.pre_classify("I need to report on the repo metrics")

        # Should either not match at all, or match something other than manage_repos
        if result is not None:
            assert (
                result.action != "manage_repos"
            ), "Generic 'repo' mention should not trigger repo management"

    def test_multi_intent_includes_manage_repos(self):
        """Multi-intent detection also picks up manage_repos."""
        result = PreClassifier.detect_multiple_intents(
            "link mediajunkie/piper-morgan to Piper Morgan"
        )
        actions = [i.action for i in result.intents]
        assert "manage_repos" in actions


# ---------------------------------------------------------------------------
# Handler dispatch test
# ---------------------------------------------------------------------------


class TestRepoManagementHandlerRouting:
    """Test that portfolio handler delegates manage_repos to _handle_repo_management."""

    @pytest.fixture
    def handler(self):
        return CanonicalHandlers()

    @pytest.mark.asyncio
    async def test_portfolio_delegates_manage_repos(self, handler):
        """manage_repos action should dispatch to _handle_repo_management."""
        intent = Intent(
            category=IntentCategory.PORTFOLIO,
            action="manage_repos",
            confidence=1.0,
            context={"original_message": "link my repo"},
        )

        with patch.object(handler, "_handle_repo_management", new_callable=AsyncMock) as mock_rm:
            mock_rm.return_value = {
                "message": "ok",
                "intent": {"category": "portfolio"},
            }
            await handler.handle(intent, session_id="test-session", user_id="u1")
            mock_rm.assert_called_once()


# ---------------------------------------------------------------------------
# Handler logic tests
# ---------------------------------------------------------------------------


def _make_intent(message: str) -> Intent:
    """Helper to create a PORTFOLIO/manage_repos intent."""
    return Intent(
        category=IntentCategory.PORTFOLIO,
        action="manage_repos",
        confidence=1.0,
        context={"original_message": message},
    )


def _mock_project(name="Piper Morgan", project_id="proj-1", owner_id="u1"):
    """Create a mock domain project."""
    p = MagicMock()
    p.id = project_id
    p.name = name
    p.owner_id = owner_id
    return p


def _mock_repo(
    full_name="mediajunkie/piper-morgan",
    repo_id="repo-1",
    provider="github",
    owner_id="u1",
):
    """Create a mock domain repository."""
    r = MagicMock()
    r.id = repo_id
    r.full_name = full_name
    r.provider = provider
    r.owner_id = owner_id
    r.display_name = full_name.split("/")[-1]
    r.url = f"https://github.com/{full_name}"
    return r


def _mock_project_link(project_id="proj-1"):
    """Create a mock project link."""
    link = MagicMock()
    link.project_id = project_id
    return link


class TestRepoManagementHandler:
    """Test _handle_repo_management for link, unlink, and list operations."""

    @pytest.fixture
    def handler(self):
        return CanonicalHandlers()

    # --- Authentication ---

    @pytest.mark.asyncio
    async def test_no_user_returns_sign_in_message(self, handler):
        """No user_id → sign-in prompt."""
        intent = _make_intent("link mediajunkie/piper-morgan to project")
        result = await handler._handle_repo_management(intent, "sess", user_id=None)

        assert "sign in" in result["message"].lower()
        assert result["requires_clarification"] is False

    # --- Link operation ---

    @pytest.mark.asyncio
    async def test_link_needs_clarification_no_repo(self, handler):
        """'link repo to project' without owner/repo → asks for repo name."""
        intent = _make_intent("link my repo to Piper Morgan")
        result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert result["requires_clarification"] is True
        assert "owner/repo" in result["message"]

    @pytest.mark.asyncio
    async def test_link_without_project_falls_to_list(self, handler):
        """'link owner/repo' without 'to <project>' falls through to list."""
        intent = _make_intent("link mediajunkie/piper-morgan")

        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
            patch(_PATCH_PROJECT_REPO),
        ):
            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_owner.return_value = []

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        # Falls through to list since "link X" without "to Y" doesn't match link patterns
        assert result["requires_clarification"] is False

    @pytest.mark.asyncio
    async def test_link_success(self, handler):
        """Full link flow: project found, repo created, link established."""
        intent = _make_intent("link mediajunkie/piper-morgan to Piper Morgan")

        mock_project = _mock_project()
        mock_repo = _mock_repo()
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = mock_project

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = None  # new repo
            mock_repo_repo.create_repository.return_value = mock_repo
            mock_repo_repo.get_project_links.return_value = []  # not linked yet
            mock_repo_repo.link_to_project.return_value = MagicMock()

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "Done" in result["message"]
        assert "linked" in result["message"].lower()
        assert result["requires_clarification"] is False
        assert result["intent"]["action"] == "link_repo"

    @pytest.mark.asyncio
    async def test_link_project_not_found(self, handler):
        """Link with nonexistent project → project not found message."""
        intent = _make_intent("link mediajunkie/piper-morgan to Nonexistent Project")

        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO),
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = None  # not found

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "couldn't find" in result["message"].lower()
        assert result["intent"]["context"]["error"] == "project_not_found"

    @pytest.mark.asyncio
    async def test_link_already_linked(self, handler):
        """Linking a repo that's already linked → informative message."""
        intent = _make_intent("link mediajunkie/piper-morgan to Piper Morgan")

        mock_project = _mock_project()
        mock_repo = _mock_repo()
        existing_link = _mock_project_link(project_id="proj-1")
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = mock_project

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = mock_repo
            mock_repo_repo.get_project_links.return_value = [existing_link]

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "already linked" in result["message"].lower()
        assert result["intent"]["context"]["status"] == "already_linked"

    # --- Unlink operation ---

    @pytest.mark.asyncio
    async def test_unlink_success(self, handler):
        """Unlink operation removes repo-project link."""
        intent = _make_intent("unlink mediajunkie/piper-morgan from Piper Morgan")

        mock_project = _mock_project()
        mock_repo = _mock_repo()
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = mock_project

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.get_by_full_name.return_value = mock_repo
            mock_repo_repo.unlink_from_project.return_value = True

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "unlinked" in result["message"].lower()
        assert result["intent"]["action"] == "unlink_repo"

    @pytest.mark.asyncio
    async def test_unlink_missing_entities(self, handler):
        """Unlink without specifying both repo and project → clarification."""
        intent = _make_intent("unlink the repo")

        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO),
            patch(_PATCH_REPO_REPO),
        ):
            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert result["requires_clarification"] is True
        assert "owner/repo" in result["message"]

    # --- List operation ---

    @pytest.mark.asyncio
    async def test_list_repos_for_project(self, handler):
        """List repos for a specific project returns formatted list."""
        intent = _make_intent("show repos for Piper Morgan")

        mock_project = _mock_project()
        repo1 = _mock_repo(full_name="mediajunkie/piper-morgan")
        repo2 = _mock_repo(full_name="mediajunkie/other-repo", repo_id="repo-2", provider="gitlab")
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = mock_project

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_project.return_value = [repo1, repo2]

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "2 linked repositories" in result["message"]
        assert "mediajunkie/piper-morgan" in result["message"]
        assert "mediajunkie/other-repo" in result["message"]
        assert result["intent"]["context"]["repo_count"] == 2

    @pytest.mark.asyncio
    async def test_list_all_repos(self, handler):
        """List all user's repos when no project specified."""
        intent = _make_intent("show my repos")

        repo1 = _mock_repo()
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
            patch(_PATCH_PROJECT_REPO),
        ):
            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_owner.return_value = [repo1]

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "1 registered repository" in result["message"]
        assert result["intent"]["action"] == "list_repos"

    @pytest.mark.asyncio
    async def test_list_empty_repos(self, handler):
        """List repos when user has none → helpful suggestion."""
        intent = _make_intent("show my repos")

        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
            patch(_PATCH_PROJECT_REPO),
        ):
            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_owner.return_value = []

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "don't have any" in result["message"].lower()
        assert "link" in result["message"].lower()


# ---------------------------------------------------------------------------
# list_repos not-found fallback (CXO rule, 2026-10-05:
# mailboxes/lead/inbox/rule-cxo-to-lead-cc-arch-list-repos-not-found-keeps-
# the-lookup-answer-with-all-your-repos-corpus-rows-too-2026-10-05.md §2/§5)
# ---------------------------------------------------------------------------


class TestListReposNotFoundFallback:
    """Not-found for a named project must still answer the underlying list
    ask, never dead-end on a bare "couldn't find" — and must echo the
    project name back in the casing the user typed it in."""

    @pytest.fixture
    def handler(self):
        return CanonicalHandlers()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "message",
        [
            "list my repos on github",
            "show all of my repos",
        ],
    )
    async def test_github_and_repos_phrasings_fall_back_to_full_list(self, handler, message):
        """'github'/'repos' get misread as a project name by the extraction
        regex; since no such project exists, the not-found must still
        answer the list ask with the user's actual repos."""
        intent = _make_intent(message)
        repo1 = _mock_repo()
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = None  # not found

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_owner.return_value = [repo1]

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "couldn't find a project called" in result["message"].lower()
        assert "mediajunkie/piper-morgan" in result["message"]
        assert "?" not in result["message"]

    @pytest.mark.asyncio
    async def test_not_found_with_repos_answers_the_list_ask(self, handler):
        """'show repos for Atlas' with no Atlas project still returns the
        full repo list, prefaced with the honest not-found — and the
        preface says "all" so the list doesn't read as Atlas's repos."""
        intent = _make_intent("show repos for Atlas")
        repo1 = _mock_repo()
        repo2 = _mock_repo(full_name="mediajunkie/piper-morgan-product", repo_id="repo-2")
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = None  # no Atlas

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_owner.return_value = [repo1, repo2]

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "couldn't find a project called 'atlas'" in result["message"].lower()
        assert "Here are all 2 of your registered repositories:" in result["message"]
        assert "mediajunkie/piper-morgan" in result["message"]
        assert "mediajunkie/piper-morgan-product" in result["message"]
        assert "?" not in result["message"]

    @pytest.mark.asyncio
    async def test_not_found_with_exactly_one_repo_says_only_not_all_1(self, handler):
        """CXO 2026-10-05: with a single registered repo the n>=2 copy read
        'Here are all 1 of your registered repository:' — ungrammatical and
        'all 1' looks like a bug. n=1 says 'only'; n>=2 is unchanged."""
        intent = _make_intent("show repos for Atlas")
        repo1 = _mock_repo()
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = None  # no Atlas

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_owner.return_value = [repo1]

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "The only repository you have registered is:" in result["message"]
        assert "all 1" not in result["message"]
        assert "mediajunkie/piper-morgan" in result["message"]
        assert "?" not in result["message"]

    @pytest.mark.asyncio
    async def test_not_found_with_zero_repos_returns_the_zero_repos_string(self, handler):
        """Not-found AND zero registered repos → the exact zero-repos
        fallback string, not the list-shaped preface."""
        intent = _make_intent("show repos for Atlas")
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = None  # no Atlas

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_owner.return_value = []

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert result["message"] == (
            "I couldn't find a project called 'Atlas', and you don't have "
            "any registered repositories yet. You can register one by "
            "saying 'link owner/repo to [project]'."
        )
        assert "?" not in result["message"]

    @pytest.mark.asyncio
    async def test_not_found_echoes_original_casing(self, handler):
        """'show repos for Piper Morgan' (project not found) must echo back
        'Piper Morgan' as typed, not the lowercased lookup form."""
        intent = _make_intent("show repos for Piper Morgan")
        repo1 = _mock_repo()
        mock_factory, _ = _mock_session_factory()

        with (
            patch(_PATCH_SESSION_FACTORY, mock_factory),
            patch(_PATCH_PROJECT_REPO) as MockProjRepo,
            patch(_PATCH_REPO_REPO) as MockRepoRepo,
        ):
            mock_proj_repo = AsyncMock()
            MockProjRepo.return_value = mock_proj_repo
            mock_proj_repo.find_by_name.return_value = None  # not found

            mock_repo_repo = AsyncMock()
            MockRepoRepo.return_value = mock_repo_repo
            mock_repo_repo.list_by_owner.return_value = [repo1]

            result = await handler._handle_repo_management(intent, "sess", user_id="u1")

        assert "'Piper Morgan'" in result["message"]
        assert "'piper morgan'" not in result["message"]
        assert "?" not in result["message"]


# ---------------------------------------------------------------------------
# Helper tests
# ---------------------------------------------------------------------------


class TestCleanTrailingWords:
    """Test _clean_trailing_words static method."""

    def test_removes_please(self):
        assert CanonicalHandlers._clean_trailing_words("Piper Morgan please") == "Piper Morgan"

    def test_removes_now(self):
        assert CanonicalHandlers._clean_trailing_words("Piper Morgan now") == "Piper Morgan"

    def test_leaves_clean_name(self):
        assert CanonicalHandlers._clean_trailing_words("Piper Morgan") == "Piper Morgan"

    def test_handles_empty(self):
        assert CanonicalHandlers._clean_trailing_words("") == ""

    def test_handles_none(self):
        assert CanonicalHandlers._clean_trailing_words(None) is None
