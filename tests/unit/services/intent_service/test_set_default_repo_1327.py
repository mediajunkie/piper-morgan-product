"""Tests for RECONNECT #1327 gap 1 — conversational "set my default repo".

Covers:
- Pre-classifier patterns: "set my default repo to owner/name" + variants
  classify to (QUERY, set_default_repo) and carry original_message.
- Handler `_handle_set_default_repo`:
    * valid "owner/name" → calls ConnectorConfigService.set_default_repo with the
      principal + the repo, returns a confirmation naming the repo.
    * bad shape → graceful chat message, NO exception, setter NOT called.
    * preference is independent of OAuth binding (no GitHub-connected gating).
- Dispatch: the `set_default_repo` action routes through the workflow-dispatcher
  rail to the handler (mirrors the cohort WorkflowEntry/dispatch tests).
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


class TestPreClassifierSetDefaultRepoPatterns:
    """The 'set default repo' phrasings classify to (QUERY, set_default_repo)."""

    @pytest.mark.parametrize(
        "message",
        [
            "set my default repo to mediajunkie/piper-morgan-product",
            "set default repo mediajunkie/piper-morgan-product",
            "use mediajunkie/piper-morgan-product as my default repo",
            "make mediajunkie/piper-morgan-product my default repo",
            "set my default repository to owner/name",
            "change my default repo to owner/name",
        ],
    )
    def test_set_default_repo_patterns_classify(self, message):
        result = PreClassifier.pre_classify(message)
        assert result is not None, f"{message!r} did not pre-classify"
        assert result.category == IntentCategory.QUERY, (
            f"{message!r} -> {result.category} (expected QUERY)"
        )
        assert result.action == "set_default_repo", (
            f"{message!r} -> action {result.action!r} (expected set_default_repo)"
        )
        # The handler reads the repo from original_message — must be preserved verbatim.
        assert result.context.get("original_message") == message

    @pytest.mark.parametrize(
        "message",
        [
            # These belong to OTHER repo flows (link/show), not set-default — must NOT
            # be captured by the set-default patterns.
            "link mediajunkie/piper-morgan-product to project Foo",
            "show my linked repos",
        ],
    )
    def test_does_not_swallow_other_repo_flows(self, message):
        result = PreClassifier.pre_classify(message)
        # Either no match, or matched as repo-management — never set_default_repo.
        if result is not None:
            assert result.action != "set_default_repo"


# ---------------------------------------------------------------------------
# Handler tests
# ---------------------------------------------------------------------------


class TestSetDefaultRepoHandler:
    """_handle_set_default_repo: validate, persist, confirm; graceful on bad shape."""

    @pytest.mark.asyncio
    async def test_valid_repo_persists_and_confirms(self, intent_service):
        """A valid 'owner/name' is persisted via ConnectorConfigService.set_default_repo
        with the principal, and the confirmation names the repo."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="set_default_repo",
            context={
                "original_message": "set my default repo to mediajunkie/piper-morgan-product",
                "user_id": "user-123",
            },
        )

        mock_config_service = MagicMock()
        mock_config_service.set_default_repo = AsyncMock()

        # Patch the ConnectorConfigService where the handler imports it, plus the
        # session factory so no real DB is touched.
        with patch(
            "services.connectors.config_service.ConnectorConfigService",
            return_value=mock_config_service,
        ), patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope"
        ) as mock_scope:
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await intent_service._handle_set_default_repo(intent, "wf-1")

        assert isinstance(result, IntentProcessingResult)
        assert result.success is True
        mock_config_service.set_default_repo.assert_awaited_once()
        args, kwargs = mock_config_service.set_default_repo.call_args
        # Principal first, repo value second (positional-or-kw tolerant).
        called = list(args) + list(kwargs.values())
        assert "user-123" in called, f"principal not passed: {called}"
        assert "mediajunkie/piper-morgan-product" in called, f"repo not passed: {called}"
        # Confirmation names the repo.
        assert "mediajunkie/piper-morgan-product" in result.message

    @pytest.mark.asyncio
    async def test_bad_shape_is_graceful_no_exception(self, intent_service):
        """A malformed repo (no owner/name) → graceful message, setter NOT called."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="set_default_repo",
            context={
                "original_message": "set my default repo to not-a-real-repo-shape",
                "user_id": "user-123",
            },
        )

        mock_config_service = MagicMock()
        mock_config_service.set_default_repo = AsyncMock()

        with patch(
            "services.connectors.config_service.ConnectorConfigService",
            return_value=mock_config_service,
        ), patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope"
        ) as mock_scope:
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            # Must not raise.
            result = await intent_service._handle_set_default_repo(intent, "wf-1")

        assert isinstance(result, IntentProcessingResult)
        # Graceful: no persist, a helpful nudge mentioning the expected shape.
        mock_config_service.set_default_repo.assert_not_awaited()
        assert "owner/name" in result.message
        # Suggest the canonical example so the user can self-correct.
        assert "mediajunkie/piper-morgan-product" in result.message

    @pytest.mark.asyncio
    async def test_works_without_github_connected(self, intent_service):
        """Setting the default is a PREFERENCE — it must NOT gate on a GitHub OAuth
        binding (the value is consumed later by resolve_repo). The handler must not
        construct any GitHub router/connector to persist the preference."""
        intent = Intent(
            category=IntentCategory.QUERY,
            action="set_default_repo",
            context={
                "original_message": "use owner/name as my default repo",
                "user_id": "user-xyz",
            },
        )

        mock_config_service = MagicMock()
        mock_config_service.set_default_repo = AsyncMock()

        with patch(
            "services.connectors.config_service.ConnectorConfigService",
            return_value=mock_config_service,
        ), patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope"
        ) as mock_scope, patch(
            "services.integrations.github.github_integration_router.GitHubIntegrationRouter"
        ) as MockRouter:
            mock_scope.return_value.__aenter__ = AsyncMock(return_value=MagicMock())
            mock_scope.return_value.__aexit__ = AsyncMock(return_value=False)

            result = await intent_service._handle_set_default_repo(intent, "wf-1")

        assert result.success is True
        mock_config_service.set_default_repo.assert_awaited_once()
        # No GitHub router/connector construction for a pure preference write.
        MockRouter.assert_not_called()


# ---------------------------------------------------------------------------
# Dispatch routing test (workflow-dispatcher rail, ADR-059 / #1124)
# ---------------------------------------------------------------------------


class TestSetDefaultRepoDispatch:
    """The set_default_repo action is an action-triggered workflow that dispatches
    to _handle_set_default_repo via the rail (no hand-coded elif branch)."""

    def test_registered_as_action_triggered_workflow(self):
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()  # idempotent
        assert "set_default_repo" in WORKFLOW_REGISTRY
        assert WORKFLOW_REGISTRY["set_default_repo"].action_triggered is True

    @pytest.mark.asyncio
    async def test_dispatch_invokes_handler(self):
        """dispatch_workflow('set_default_repo', ...) calls the IntentService handler
        with (intent, workflow_id) and returns its result."""
        from services.intent_service.workflow_dispatcher import dispatch_workflow
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()

        fake_result = IntentProcessingResult(
            success=True, message="ok", intent_data={}
        )
        mock_service = MagicMock()
        mock_service._handle_set_default_repo = AsyncMock(return_value=fake_result)

        intent = Intent(
            category=IntentCategory.QUERY,
            action="set_default_repo",
            context={"original_message": "set default repo owner/name"},
        )

        result = await dispatch_workflow(
            workflow_type="set_default_repo",
            session_id="sess-1",
            user_id="user-123",
            context={
                "intent": intent,
                "workflow_id": "wf-1",
                "intent_service": mock_service,
            },
        )

        assert result is fake_result
        mock_service._handle_set_default_repo.assert_awaited_once()
        call_args = mock_service._handle_set_default_repo.call_args.args
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

        assert ("QUERY", "set_default_repo") in ACTION_REGISTRY
        assert (
            ACTION_REGISTRY[("QUERY", "set_default_repo")] == ActionDisposition.WORKFLOW
        )

    def test_example_present_and_classifies(self):
        from services.intent_service.action_registry import ACTION_EXAMPLES

        key = ("QUERY", "set_default_repo")
        assert key in ACTION_EXAMPLES
        result = PreClassifier.pre_classify(ACTION_EXAMPLES[key])
        assert result is not None
        assert result.category.value.upper() == "QUERY"
        assert result.action == "set_default_repo"

    def test_verb_mapping_present(self):
        from services.intent_service.action_registry import (
            Verb,
            get_verb,
            validate_verb_coverage,
        )

        assert get_verb("set_default_repo") == Verb.SET
        assert validate_verb_coverage() == []
