"""Tests for #1876 — conversational "set my timezone to Helsinki".

UserPreferenceManager.set_reminder_timezone (#1574's store) had ZERO callers
before this issue — no Settings page, no API route, no chat action — so
every clock face (#1576) rendered on DEFAULT_USER_TIMEZONE for everyone. This
is the chat-action leg.

Covers:
- Handler `_handle_set_timezone`:
    * explicit "Continent/City" token → persists via UserPreferenceManager,
      confirms with the zone + a labeled clock face.
    * unambiguous bare city → resolves via the shared resolver, persists.
    * unknown token → honest ask, setter NOT called, no exception.
    * ambiguous token (2+ zones share the city segment) → honest ask NAMING
      every candidate, setter NOT called — NEVER a guess.
- Dispatch: the `set_timezone` action routes through the workflow-dispatcher
  rail to the handler (mirrors #1327's cohort WorkflowEntry/dispatch test).
- Action-registry coverage: registry + example + verb entries are consistent.
- Reachability is deliberately via the LLM classifier only (no pre_classifier
  pattern, per the 2026-08-29 corpus-deposit ruling) — pinned as a negative
  assertion so a future accidental pre_classifier addition doesn't silently
  change this action's reachability story.
"""

import uuid
from unittest.mock import AsyncMock, patch

import pytest

from services.domain.models import Intent
from services.intent.intent_service import IntentProcessingResult, IntentService
from services.intent_service.pre_classifier import PreClassifier
from services.shared_types import IntentCategory

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

# set_reminder_timezone is UUID-typed (unlike #1327's set_default_repo, whose
# ConnectorConfigService counterpart is deliberately Union[str, UUID, None]) —
# the handler converts the stamped principal with UUID(str(_user_id)), which
# is what process_intent ALWAYS stamps in production (a real UUID string).
# Fixtures use a real UUID string so these tests exercise that real shape.
DEFAULT_TEST_USER_ID = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"


@pytest.fixture
def intent_service():
    """IntentService instance with heavy deps patched out (mirrors #1327's
    test_set_default_repo_1327.py fixture)."""
    with patch("services.intent.intent_service.LearningHandler"):
        with patch("services.intent.intent_service.ConversationKnowledgeGraphIntegration"):
            return IntentService()


def _intent(message: str, user_id: str = DEFAULT_TEST_USER_ID) -> Intent:
    return Intent(
        category=IntentCategory.QUERY,
        action="set_timezone",
        context={"original_message": message, "user_id": user_id},
    )


# ---------------------------------------------------------------------------
# Handler tests
# ---------------------------------------------------------------------------


class TestSetTimezoneHandlerResolvedCases:
    @pytest.mark.asyncio
    async def test_explicit_iana_token_persists_and_confirms(self, intent_service):
        intent = _intent("set my timezone to Europe/Helsinki")

        mock_upm = AsyncMock()
        mock_upm.set_reminder_timezone = AsyncMock()
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_upm,
        ):
            result = await intent_service._handle_set_timezone(intent, "wf-1")

        assert isinstance(result, IntentProcessingResult)
        assert result.success is True
        mock_upm.set_reminder_timezone.assert_awaited_once()
        args = mock_upm.set_reminder_timezone.call_args.args
        assert args[0] == uuid.UUID(DEFAULT_TEST_USER_ID)
        assert args[1] == "Europe/Helsinki"
        assert "Europe/Helsinki" in result.message
        assert result.intent_data["context"]["timezone"] == "Europe/Helsinki"
        assert result.requires_clarification is False

    @pytest.mark.asyncio
    async def test_unambiguous_bare_city_resolves_and_persists(self, intent_service):
        intent = _intent("set my timezone to Helsinki")

        mock_upm = AsyncMock()
        mock_upm.set_reminder_timezone = AsyncMock()
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_upm,
        ):
            result = await intent_service._handle_set_timezone(intent, "wf-1")

        assert result.success is True
        mock_upm.set_reminder_timezone.assert_awaited_once_with(
            uuid.UUID(DEFAULT_TEST_USER_ID), "Europe/Helsinki"
        )
        assert "Europe/Helsinki" in result.message

    @pytest.mark.asyncio
    async def test_confirmation_includes_a_labeled_clock_face(self, intent_service):
        """The house face convention (#1576): never a bare time, always zone-labeled."""
        intent = _intent("set my timezone to UTC")

        mock_upm = AsyncMock()
        mock_upm.set_reminder_timezone = AsyncMock()
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_upm,
        ):
            result = await intent_service._handle_set_timezone(intent, "wf-1")

        assert result.success is True
        assert "UTC" in result.message
        # format_user_time always appends a zone abbreviation label.
        import re

        assert re.search(
            r"\d{1,2}:\d{2}\s?[AP]M\s+\S+", result.message
        ), f"no labeled clock face found in: {result.message!r}"


class TestSetTimezoneHandlerHonestFailures:
    @pytest.mark.asyncio
    async def test_unknown_token_is_graceful_no_exception_setter_not_called(self, intent_service):
        intent = _intent("set my timezone to Nowheresville")

        mock_upm = AsyncMock()
        mock_upm.set_reminder_timezone = AsyncMock()
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_upm,
        ):
            result = await intent_service._handle_set_timezone(intent, "wf-1")

        assert isinstance(result, IntentProcessingResult)
        assert result.success is True
        assert result.requires_clarification is True
        mock_upm.set_reminder_timezone.assert_not_awaited()
        assert "Nowheresville" in result.message

    @pytest.mark.asyncio
    async def test_ambiguous_token_names_every_candidate_never_guesses(self, intent_service):
        intent = _intent("set my timezone to Springfield")

        mock_upm = AsyncMock()
        mock_upm.set_reminder_timezone = AsyncMock()
        fake_candidates = ["OtherRegion/Springfield", "Region/Springfield"]
        with (
            patch(
                "services.domain.user_preference_manager.UserPreferenceManager",
                return_value=mock_upm,
            ),
            patch(
                "services.utils.datetime_utils.resolve_timezone_token",
                return_value=(None, fake_candidates),
            ),
        ):
            result = await intent_service._handle_set_timezone(intent, "wf-1")

        assert result.success is True
        assert result.requires_clarification is True
        mock_upm.set_reminder_timezone.assert_not_awaited()
        for candidate in fake_candidates:
            assert candidate in result.message, f"{candidate} missing from ask: {result.message}"

    @pytest.mark.asyncio
    async def test_no_extractable_token_asks_without_crashing(self, intent_service):
        intent = _intent("set my timezone")  # nothing after "timezone"

        mock_upm = AsyncMock()
        mock_upm.set_reminder_timezone = AsyncMock()
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_upm,
        ):
            result = await intent_service._handle_set_timezone(intent, "wf-1")

        assert isinstance(result, IntentProcessingResult)
        assert result.success is True
        assert result.requires_clarification is True
        mock_upm.set_reminder_timezone.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_store_failure_is_reported_honestly_not_success(self, intent_service):
        """A FAILED write must never report success=True (#1423)."""
        intent = _intent("set my timezone to Europe/Helsinki")

        mock_upm = AsyncMock()
        mock_upm.set_reminder_timezone = AsyncMock(side_effect=RuntimeError("db is down"))
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_upm,
        ):
            result = await intent_service._handle_set_timezone(intent, "wf-1")

        assert result.success is False
        assert result.error_type == "set_timezone_error"

    @pytest.mark.asyncio
    async def test_non_uuid_principal_fails_honestly_never_writes_unscoped(self, intent_service):
        """set_reminder_timezone is UUID-typed; a non-UUID/missing principal
        (system call, malformed session) must never silently fall through to
        an unscoped/global write — it's reported as a failure, same as any
        other store failure, and the setter is never reached."""
        intent = _intent("set my timezone to Europe/Helsinki", user_id="not-a-uuid")

        mock_upm = AsyncMock()
        mock_upm.set_reminder_timezone = AsyncMock()
        with patch(
            "services.domain.user_preference_manager.UserPreferenceManager",
            return_value=mock_upm,
        ):
            result = await intent_service._handle_set_timezone(intent, "wf-1")

        assert result.success is False
        assert result.error_type == "set_timezone_error"
        mock_upm.set_reminder_timezone.assert_not_awaited()


# ---------------------------------------------------------------------------
# Dispatch routing test (workflow-dispatcher rail, ADR-059 / #1124)
# ---------------------------------------------------------------------------


class TestSetTimezoneDispatch:
    def test_registered_as_action_triggered_workflow(self):
        from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()  # idempotent
        assert "set_timezone" in WORKFLOW_REGISTRY
        entry = WORKFLOW_REGISTRY["set_timezone"]
        assert entry.action_triggered is True

    @pytest.mark.asyncio
    async def test_dispatch_invokes_handler(self):
        from unittest.mock import MagicMock

        from services.intent_service.workflow_dispatcher import dispatch_workflow
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()

        fake_result = IntentProcessingResult(success=True, message="ok", intent_data={})
        mock_service = MagicMock()
        mock_service._handle_set_timezone = AsyncMock(return_value=fake_result)

        intent = _intent("set my timezone to Europe/Helsinki")

        result = await dispatch_workflow(
            workflow_type="set_timezone",
            session_id="sess-1",
            user_id="user-123",
            context={
                "intent": intent,
                "workflow_id": "wf-1",
                "intent_service": mock_service,
            },
        )

        assert result is fake_result
        mock_service._handle_set_timezone.assert_awaited_once()
        call_args = mock_service._handle_set_timezone.call_args.args
        assert call_args[0] is intent
        assert call_args[1] == "wf-1"


# ---------------------------------------------------------------------------
# Action-registry consistency
# ---------------------------------------------------------------------------


class TestActionRegistryConsistency:
    def test_registry_entry_present(self):
        from services.intent_service.action_registry import (
            ACTION_REGISTRY,
            ActionDisposition,
        )

        assert ("QUERY", "set_timezone") in ACTION_REGISTRY
        assert ACTION_REGISTRY[("QUERY", "set_timezone")] == ActionDisposition.WORKFLOW

    def test_example_present(self):
        from services.intent_service.action_registry import ACTION_EXAMPLES

        assert ("QUERY", "set_timezone") in ACTION_EXAMPLES

    def test_verb_mapping_present(self):
        from services.intent_service.action_registry import (
            Verb,
            get_verb,
            validate_verb_coverage,
        )

        assert get_verb("set_timezone") == Verb.SET
        assert validate_verb_coverage() == []


class TestReachabilityIsLlmOnlyByDesign:
    """#1876 deliberately did NOT add a pre_classifier.py pattern for this
    phrasing (the 2026-08-29 corpus-deposit ruling: TestExtractionPatternRatchet
    forbids new-pattern whack-a-mole). Pinned here as a negative assertion —
    if this ever starts returning non-None, the CHAT_INVISIBLE ledger row in
    chat_pointers.py (and the chat_invisible ceiling bump) both go stale and
    should be revisited (the surface would then deserve a POINTER)."""

    def test_pre_classifier_does_not_deterministically_route_it(self):
        result = PreClassifier.pre_classify("set my timezone to Europe/Helsinki")
        assert result is None or result.action != "set_timezone", (
            "pre_classifier now resolves set_timezone deterministically — "
            "chat_pointers.py's CHAT_INVISIBLE(issue=1876) row and the "
            "chat_invisible ceiling note in scripts/ratchet_ceilings.json are "
            "stale and should be revisited (this surface can become a POINTER)"
        )

    def test_reachable_via_the_rail_regardless(self):
        """Reachability comes from the RAIL registration, not the
        pre-classifier — test_routing_vocabulary_1283.py's
        test_every_registry_canonical_is_reachable is the authority; this is
        a local sanity echo of the same claim."""
        from services.intent_service.workflow_dispatcher import get_action_workflows
        from services.intent_service.workflow_entries import register_default_workflows

        register_default_workflows()
        assert "set_timezone" in get_action_workflows()
