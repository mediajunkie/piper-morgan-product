"""Tests for RECONNECT #1327 gap (build #2) — conversational "what's my default repo".

The INVERSE of set_default_repo (build #1): a read of the per-user default-repo
preference from ``connector_configs``, so Piper can answer "what is my default repo
again?" instead of flooring with "I don't have it in context" (PM UAT 2026-06-30).

Covers:
- Pre-classifier patterns: "what's/which/show my default repo" + variants classify
  to (QUERY, get_default_repo) and carry original_message.
- The new GET patterns do NOT hijack the set-default phrasings (set/change/use/make)
  — the two flows stay disjoint (collision guard).
- Handler `_handle_get_default_repo`:
    * default set → calls ConnectorConfigService.get_default_repo(principal),
      returns a confirmation naming the repo.
    * default unset (None) → graceful helpful nudge telling the user how to set one;
      NO exception; getter still called (it's how we learned it's None).
    * the read is independent of OAuth binding (no GitHub-connected gating, no router).
- Dispatch: the `get_default_repo` action routes through the workflow-dispatcher rail
  to the handler (mirrors the cohort WorkflowEntry/dispatch tests).
- Action-registry coverage: the new action has registry + example + verb entries
  (consistency the startup validators + the registry test-suite enforce).
"""

from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture
def intent_service():
    """IntentService instance with heavy deps patched out (mirrors cohort tests)."""
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


# ---------------------------------------------------------------------------
# Pre-classifier pattern tests
# ---------------------------------------------------------------------------


class TestPreClassifierGetDefaultRepoPatterns:
    """The 'what's my default repo' phrasings used to classify to
    (QUERY, get_default_repo) at surface 1.

    #1595 Phase 3, sixteenth deletion (2026-10-03): GET_DEFAULT_REPO_PATTERNS
    is now `[]` (tombstoned, FULL deletion) — none of these phrasings claim
    at surface 1 any more. See
    TestGetDefaultRepoInversionRoutesSurvive below for the live-routes proof
    that get_default_repo is still reachable through the Inversion."""

    @pytest.mark.parametrize(
        "message",
        [
            "what is my default repo?",
            "what's my default repo",
            "what is my default repo again?",
            "which repo is my default?",
            "which is my default repo",
            "show my default repo",
            "what's my default repository?",
            "what default repo do I have set",
        ],
    )
    def test_get_default_repo_patterns_no_longer_classify(self, message):
        result = PreClassifier.pre_classify(message)
        assert result is None, f"unexpectedly still classifies: {message!r} -> {result!r}"

    @pytest.mark.parametrize(
        "message",
        [
            # These belong to the SET flow (build #1) — the GET patterns must NOT
            # capture them, and they must continue to classify as set_default_repo.
            "set my default repo to mediajunkie/piper-morgan-product",
            "set default repo mediajunkie/piper-morgan-product",
            "use mediajunkie/piper-morgan-product as my default repo",
            "make mediajunkie/piper-morgan-product my default repo",
            "change my default repo to owner/name",
        ],
    )
    def test_does_not_hijack_set_default_flow(self, message):
        """Collision guard: set-default phrasings still route to set_default_repo,
        NOT to the new get_default_repo (the two flows must stay disjoint)."""
        result = PreClassifier.pre_classify(message)
        assert result is not None, f"{message!r} stopped pre-classifying"
        assert (
            result.action == "set_default_repo"
        ), f"{message!r} -> {result.action!r} (set-default flow was hijacked)"

    @pytest.mark.parametrize(
        "message",
        [
            # These belong to OTHER repo flows (link/show-linked), not get-default.
            "show my linked repos",
            "which repos are linked",
        ],
    )
    def test_does_not_swallow_other_repo_flows(self, message):
        result = PreClassifier.pre_classify(message)
        # Either no match, or matched as repo-management — never get_default_repo.
        if result is not None:
            assert result.action != "get_default_repo"


# ---------------------------------------------------------------------------
# Handler tests
# ---------------------------------------------------------------------------


class TestGetDefaultRepoHandler:
    """_handle_get_default_repo: read, report; helpful nudge when unset; graceful."""

    @pytest.mark.asyncio
    async def test_set_default_is_reported(self, intent_service):
        """A persisted default is read via ConnectorConfigService.get_default_repo with
        the principal, and the message names the repo."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="get_default_repo",
            context={
                "original_message": "what is my default repo again?",
                "user_id": "user-123",
            },
        )

        mock_config_service = MagicMock()
        mock_config_service.get_default_repo = AsyncMock(
            return_value="mediajunkie/piper-morgan-product"
        )

        with (
            patch(
                "services.connectors.config_service.ConnectorConfigService",
                return_value=mock_config_service,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope"
            ) as mock_scope,
        ):
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await intent_service._handle_get_default_repo(intent, "wf-1")

        assert isinstance(result, IntentProcessingResult)
        assert result.success is True
        mock_config_service.get_default_repo.assert_awaited_once()
        args, kwargs = mock_config_service.get_default_repo.call_args
        called = list(args) + list(kwargs.values())
        assert "user-123" in called, f"principal not passed: {called}"
        # The confirmation names the repo.
        assert "mediajunkie/piper-morgan-product" in result.message

    @pytest.mark.asyncio
    async def test_unset_default_gives_helpful_nudge(self, intent_service):
        """No default set (None) → graceful, helpful message telling the user how to
        set one. The getter IS called (that's how we learned it's None); no exception."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="get_default_repo",
            context={
                "original_message": "what's my default repo?",
                "user_id": "user-123",
            },
        )

        mock_config_service = MagicMock()
        mock_config_service.get_default_repo = AsyncMock(return_value=None)

        with (
            patch(
                "services.connectors.config_service.ConnectorConfigService",
                return_value=mock_config_service,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope"
            ) as mock_scope,
        ):
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            # Must not raise.
            result = await intent_service._handle_get_default_repo(intent, "wf-1")

        assert isinstance(result, IntentProcessingResult)
        assert result.success is True
        mock_config_service.get_default_repo.assert_awaited_once()
        # Helpful: tells the user they haven't set one + how to (mentions "set" the repo).
        assert "set" in result.message.lower()
        assert "default repo" in result.message.lower()

    @pytest.mark.asyncio
    async def test_works_without_github_connected(self, intent_service):
        """Reading the default is a PREFERENCE read — it must NOT gate on a GitHub OAuth
        binding and must NOT construct any GitHub router/connector to answer."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="get_default_repo",
            context={
                "original_message": "which repo is my default?",
                "user_id": "user-xyz",
            },
        )

        mock_config_service = MagicMock()
        mock_config_service.get_default_repo = AsyncMock(return_value="owner/name")

        with (
            patch(
                "services.connectors.config_service.ConnectorConfigService",
                return_value=mock_config_service,
            ),
            patch(
                "services.database.session_factory.AsyncSessionFactory.session_scope"
            ) as mock_scope,
            patch(
                "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
            ) as MockRouter,
        ):
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await intent_service._handle_get_default_repo(intent, "wf-1")

        assert result.success is True
        mock_config_service.get_default_repo.assert_awaited_once()
        # No GitHub router/connector construction for a pure preference read.
        MockRouter.assert_not_called()


# ---------------------------------------------------------------------------
# Dispatch routing test (workflow-dispatcher rail, ADR-059 / #1124)
# ---------------------------------------------------------------------------


class TestGetDefaultRepoDispatch:
    """The get_default_repo action is an action-triggered workflow that dispatches
    to _handle_get_default_repo via the rail (no hand-coded elif branch)."""

    def test_registered_as_action_triggered_workflow(self):
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()  # idempotent
        assert "get_default_repo" in WORKFLOW_REGISTRY
        assert WORKFLOW_REGISTRY["get_default_repo"].action_triggered is True

    @pytest.mark.asyncio
    async def test_dispatch_invokes_handler(self):
        """dispatch_workflow('get_default_repo', ...) calls the IntentService handler
        with (intent, workflow_id) and returns its result."""
        from services.intent_service.workflow_dispatcher import dispatch_workflow
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()

        fake_result = IntentProcessingResult(success=True, message="ok", intent_data={})
        mock_service = MagicMock()
        mock_service._handle_get_default_repo = AsyncMock(return_value=fake_result)

        intent = Intent(
            category=IntentCategory.QUERY,
            action="get_default_repo",
            context={"original_message": "what is my default repo?"},
        )

        result = await dispatch_workflow(
            workflow_type="get_default_repo",
            session_id="sess-1",
            user_id="user-123",
            context={
                "intent": intent,
                "workflow_id": "wf-1",
                "intent_service": mock_service,
            },
        )

        assert result is fake_result
        mock_service._handle_get_default_repo.assert_awaited_once()
        call_args = mock_service._handle_get_default_repo.call_args.args
        assert call_args[0] is intent
        assert call_args[1] == "wf-1"


# ---------------------------------------------------------------------------
# Action-registry consistency
# ---------------------------------------------------------------------------


class TestActionRegistryConsistency:
    """The new action is wired consistently across registry/example/verb maps."""

    def test_registry_entry_present(self):
        from services.intent_service.action_registry import (
            ACTION_REGISTRY,
            ActionDisposition,
        )

        assert ("QUERY", "get_default_repo") in ACTION_REGISTRY
        assert ACTION_REGISTRY[("QUERY", "get_default_repo")] == ActionDisposition.WORKFLOW

    def test_example_present(self):
        """#1595 Phase 3, sixteenth deletion (2026-10-03): the example phrase
        ("what is my default repo?") itself still exists in ACTION_EXAMPLES
        — unaffected, that registry entry isn't touched by a pre-classifier
        pattern deletion — but it no longer classifies at surface 1
        (GET_DEFAULT_REPO_PATTERNS is `[]` now), so this no longer asserts
        pre_classify succeeds on it. Same stale-example shape this registry
        already carries for shipped_query/close_issue_query ("What shipped
        this week?" / "Close issue #42") since GITHUB_QUERY_PATTERNS' own
        fifth deletion — not a regression introduced here, a pre-existing
        property of this registry once ANY of an action's claiming patterns
        are deleted."""
        from services.intent_service.action_registry import ACTION_EXAMPLES

        key = ("QUERY", "get_default_repo")
        assert key in ACTION_EXAMPLES
        assert ACTION_EXAMPLES[key] == "what is my default repo?"

    def test_verb_mapping_present(self):
        from services.intent_service.action_registry import (
            Verb,
            get_verb,
            validate_verb_coverage,
        )

        assert get_verb("get_default_repo") == Verb.GET
        assert validate_verb_coverage() == []


class TestGetDefaultRepoInversionRoutesSurvive:
    """#1595 Phase 3 sixteenth deletion: get_default_repo still routes
    correctly through the Inversion's live consult (stubbed router — no LLM
    call, ever), proving it didn't just vanish when surface 1 stopped
    claiming it."""

    @pytest.mark.asyncio
    async def test_routes_live(self, monkeypatch):
        from tests.unit.services.intent_service._inversion_pin_helper import (
            assert_inversion_routes,
        )

        await assert_inversion_routes(
            monkeypatch,
            "what is my default repo?",
            live_categories="read_status",
            expected_action="get_default_repo",
        )
