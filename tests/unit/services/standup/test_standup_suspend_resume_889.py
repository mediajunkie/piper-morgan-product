"""
Tests for Issue #889: Standup suspend/resume bug fixes.

Category A fixes:
1. SUSPENDED state excluded from active conversation lookups
2. Resume acceptance wiring (SUSPENDED → INITIATED)
3. Resume decline wiring (SUSPENDED → ABANDONED)
4. Dead code cleanup (_check_active_standup deprecation)

These tests verify the standup suspend/resume path works correctly
for users, even without the Category B enhancements (3-part structural
collection, #900).

Issue #1053 (May 7, 2026): Migrated to async + FakeStandupConversationManager.
After #1052 Phase 2 rewrote the production manager to be async + repository-backed,
these tests use the in-memory Fake test double (no DB). All manager method
calls go through `await`. Tests use the public API exclusively.

Issue #1052 Phase 2: Added bind_session_id() to manager. Phase 3 of #1053
adds end-to-end coverage (TestBindSessionIdResume) for resume-into-different-session.
"""

from datetime import datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
import pytest_asyncio

from services.shared_types import StandupConversationState
from services.standup.conversation_manager import StandupConversationManager
from tests.unit.services.standup._fake_conversation_manager import (
    FakeStandupConversationManager,
)


class TestSuspendedExclusionInLookups:
    """Issue #889: SUSPENDED conversations should not be returned by default lookups."""

    @pytest_asyncio.fixture(autouse=True)
    async def _setup(self):
        self.manager = FakeStandupConversationManager()

    @pytest.mark.asyncio
    async def test_get_conversation_by_session_excludes_suspended(self):
        """SUSPENDED conversations are not 'active' and should not be found by default."""
        conv = await self.manager.create_conversation("sess-1", "user-1")
        await self.manager.transition_state(conv.id, StandupConversationState.GATHERING_PREFERENCES)
        await self.manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        result = await self.manager.get_conversation_by_session("sess-1")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_conversation_by_session_includes_suspended_when_requested(self):
        """With include_suspended=True, SUSPENDED conversations are returned."""
        conv = await self.manager.create_conversation("sess-1", "user-1")
        await self.manager.transition_state(conv.id, StandupConversationState.GATHERING_PREFERENCES)
        await self.manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        result = await self.manager.get_conversation_by_session("sess-1", include_suspended=True)
        assert result is not None
        assert result.id == conv.id
        assert result.state == StandupConversationState.SUSPENDED

    @pytest.mark.asyncio
    async def test_get_conversation_by_user_excludes_suspended(self):
        """SUSPENDED conversations are not returned by user lookup by default."""
        conv = await self.manager.create_conversation("sess-1", "user-1")
        await self.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await self.manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        result = await self.manager.get_conversation_by_user("user-1")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_conversation_by_user_includes_suspended_when_requested(self):
        """With include_suspended=True, SUSPENDED conversations are returned."""
        conv = await self.manager.create_conversation("sess-1", "user-1")
        await self.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await self.manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        result = await self.manager.get_conversation_by_user("user-1", include_suspended=True)
        assert result is not None
        assert result.state == StandupConversationState.SUSPENDED

    @pytest.mark.asyncio
    async def test_active_conversation_still_found(self):
        """Active (non-suspended, non-terminal) conversations are still found."""
        conv = await self.manager.create_conversation("sess-1", "user-1")
        await self.manager.transition_state(conv.id, StandupConversationState.GENERATING)

        result = await self.manager.get_conversation_by_session("sess-1")
        assert result is not None
        assert result.state == StandupConversationState.GENERATING

    @pytest.mark.asyncio
    async def test_complete_conversation_still_excluded(self):
        """COMPLETE conversations are still excluded (regression check)."""
        conv = await self.manager.create_conversation("sess-1", "user-1")
        await self.manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await self.manager.transition_state(conv.id, StandupConversationState.FINALIZING)
        await self.manager.transition_state(conv.id, StandupConversationState.COMPLETE)

        result = await self.manager.get_conversation_by_session("sess-1")
        assert result is None

    @pytest.mark.asyncio
    async def test_abandoned_conversation_still_excluded(self):
        """ABANDONED conversations are still excluded (regression check)."""
        conv = await self.manager.create_conversation("sess-1", "user-1")
        await self.manager.transition_state(conv.id, StandupConversationState.ABANDONED)

        result = await self.manager.get_conversation_by_session("sess-1")
        assert result is None


class TestResumeAcceptanceWiring:
    """Issue #889: When user says 'yes' to resume offer, standup resumes."""

    @pytest.mark.asyncio
    async def test_resume_transitions_suspended_to_initiated(self):
        """Accepting resume offer transitions SUSPENDED → INITIATED."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = FakeStandupConversationManager()

        # Create a suspended standup for the user
        conv = await manager.create_conversation("old-sess", "user-1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._resume_suspended_standup("user-1", "new-sess")

        assert result.success is True
        assert "pick up where we left off" in result.message
        assert result.intent_data["action"] == "standup_conversation_resumed"
        # Re-fetch the conv to see the updated state (production code has
        # transitioned SUSPENDED → INITIATED via the manager).
        updated = await manager.get_conversation(conv.id)
        assert updated.state == StandupConversationState.INITIATED
        assert updated.session_id == "new-sess"  # Updated to current session

    @pytest.mark.asyncio
    async def test_resume_shows_existing_content(self):
        """Resume message includes previously captured standup content."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = FakeStandupConversationManager()

        conv = await manager.create_conversation("old-sess", "user-1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.set_standup_content(
            conv.id, "**Yesterday**: Worked on auth\n**Today**: Continue auth"
        )
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._resume_suspended_standup("user-1", "new-sess")

        assert "Worked on auth" in result.message
        assert "Continue auth" in result.message

    @pytest.mark.asyncio
    async def test_resume_no_suspended_session_gives_fallback(self):
        """If no suspended session exists, a fallback message is returned."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = FakeStandupConversationManager()

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._resume_suspended_standup("user-1", "new-sess")

        assert result.success is True
        assert "couldn't find" in result.message
        assert "/standup" in result.message


class TestResumeDeclineWiring:
    """Issue #889: When user says 'no' to resume offer, session is abandoned."""

    @pytest.mark.asyncio
    async def test_decline_transitions_suspended_to_abandoned(self):
        """Declining resume offer transitions SUSPENDED → ABANDONED."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = FakeStandupConversationManager()

        conv = await manager.create_conversation("old-sess", "user-1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._abandon_suspended_standup("user-1")

        assert result.success is True
        assert "No problem" in result.message
        updated = await manager.get_conversation(conv.id)
        assert updated.state == StandupConversationState.ABANDONED


class TestPendingResumeOfferDetection:
    """Issue #889: _check_pending_resume_offer correctly detects accept/decline."""

    @pytest.mark.asyncio
    async def test_accept_signals_trigger_resume(self):
        """Accept phrases trigger resume — with #1529 offer-binding:
        explicit resume commands work anytime; bare affirmatives only while
        the resume offer is actually pending (made on the previous turn)."""
        from services.intent.intent_service import IntentService
        from services.process.registry import ProcessType, SuspendedInfo

        service = IntentService()

        suspended_info = SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )

        # (phrase, resume_offer_pending) — explicit commands need no pending
        # offer; bare affirmatives do (#1529: an unbound "yes" resumes nothing).
        accept_cases = [
            ("continue", False),
            ("resume", False),
            ("yes", True),
            ("sure", True),
            ("ok", True),
            ("yes please", True),
        ]

        for phrase, pending in accept_cases:
            with (
                patch(
                    "services.intent.intent_service.get_process_registry",
                ) as mock_registry_fn,
                patch.object(
                    service,
                    "_resume_suspended_standup",
                    new_callable=AsyncMock,
                    return_value=MagicMock(success=True),
                ) as mock_resume,
            ):
                mock_registry = MagicMock()
                mock_registry.check_suspended_processes = AsyncMock(return_value=suspended_info)
                mock_registry_fn.return_value = mock_registry

                result = await service._check_pending_resume_offer(
                    "user-1", "sess-1", phrase, resume_offer_pending=pending
                )
                assert result is not None, f"'{phrase}' should trigger resume"
                mock_resume.assert_called_once()

    @pytest.mark.asyncio
    async def test_bare_affirmative_without_pending_offer_does_not_resume(self):
        """#1529 offer-binding: a bare 'yes' with NO resume offer pending
        binds to nothing — it must NOT resume the suspended flow (this is
        the standup-hijack mechanism, pinned)."""
        from services.intent.intent_service import IntentService
        from services.process.registry import ProcessType, SuspendedInfo

        service = IntentService()

        suspended_info = SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )

        for phrase in ["yes", "yes please", "sure", "ok", "y"]:
            with (
                patch(
                    "services.intent.intent_service.get_process_registry",
                ) as mock_registry_fn,
                patch.object(
                    service,
                    "_resume_suspended_standup",
                    new_callable=AsyncMock,
                    return_value=MagicMock(success=True),
                ) as mock_resume,
            ):
                mock_registry = MagicMock()
                mock_registry.check_suspended_processes = AsyncMock(return_value=suspended_info)
                mock_registry_fn.return_value = mock_registry

                result = await service._check_pending_resume_offer("user-1", "sess-1", phrase)
                assert result is None, f"unbound '{phrase}' must not claim the turn"
                mock_resume.assert_not_called()

    @pytest.mark.asyncio
    async def test_end_standup_abandons_suspended_flow(self):
        """#1529 part 3: 'end standup' against a suspended standup abandons
        it deterministically — never falls through to a classifier."""
        from services.intent.intent_service import IntentService
        from services.process.registry import ProcessType, SuspendedInfo

        service = IntentService()

        suspended_info = SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )

        with (
            patch(
                "services.intent.intent_service.get_process_registry",
            ) as mock_registry_fn,
            patch.object(
                service,
                "_abandon_suspended_standup",
                new_callable=AsyncMock,
                return_value=MagicMock(success=True),
            ) as mock_abandon,
        ):
            mock_registry = MagicMock()
            mock_registry.check_suspended_processes = AsyncMock(return_value=suspended_info)
            mock_registry_fn.return_value = mock_registry

            result = await service._check_pending_resume_offer("user-1", "sess-1", "end standup")
            assert result is not None
            mock_abandon.assert_called_once()

    @pytest.mark.asyncio
    async def test_decline_signals_trigger_abandon(self):
        """Decline phrases trigger abandon — with #1529 offer-binding:
        explicit restart commands work anytime; bare negatives only while
        the resume offer is actually pending."""
        from services.intent.intent_service import IntentService
        from services.process.registry import ProcessType, SuspendedInfo

        service = IntentService()

        suspended_info = SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )

        decline_cases = [
            ("start over", False),
            ("start fresh", False),
            ("no", True),
            ("fresh", True),
            ("nah", True),
            ("no thanks", True),
        ]

        for phrase, pending in decline_cases:
            with (
                patch(
                    "services.intent.intent_service.get_process_registry",
                ) as mock_registry_fn,
                patch.object(
                    service,
                    "_abandon_suspended_standup",
                    new_callable=AsyncMock,
                    return_value=MagicMock(success=True),
                ) as mock_abandon,
            ):
                mock_registry = MagicMock()
                mock_registry.check_suspended_processes = AsyncMock(return_value=suspended_info)
                mock_registry_fn.return_value = mock_registry

                result = await service._check_pending_resume_offer(
                    "user-1", "sess-1", phrase, resume_offer_pending=pending
                )
                assert result is not None, f"'{phrase}' should trigger abandon"
                mock_abandon.assert_called_once()

    @pytest.mark.asyncio
    async def test_unrelated_message_returns_none(self):
        """Messages that aren't accept/decline are ignored — normal classification proceeds."""
        from services.intent.intent_service import IntentService
        from services.process.registry import ProcessType, SuspendedInfo

        service = IntentService()

        suspended_info = SuspendedInfo(
            process_type=ProcessType.STANDUP,
            suspended_at=datetime.now(),
            description="Your standup was paused.",
        )

        with patch(
            "services.intent.intent_service.get_process_registry",
        ) as mock_registry_fn:
            mock_registry = MagicMock()
            mock_registry.check_suspended_processes = AsyncMock(return_value=suspended_info)
            mock_registry_fn.return_value = mock_registry

            result = await service._check_pending_resume_offer(
                "user-1", "sess-1", "show me my calendar"
            )
            assert result is None

    @pytest.mark.asyncio
    async def test_no_suspended_session_returns_none(self):
        """When there's no suspended session, returns None immediately."""
        from services.intent.intent_service import IntentService

        service = IntentService()

        with patch(
            "services.intent.intent_service.get_process_registry",
        ) as mock_registry_fn:
            mock_registry = MagicMock()
            mock_registry.check_suspended_processes = AsyncMock(return_value=None)
            mock_registry_fn.return_value = mock_registry

            result = await service._check_pending_resume_offer("user-1", "sess-1", "yes")
            assert result is None


class TestDeprecatedCheckActiveStandup:
    """Issue #889: _check_active_standup is deprecated but still functional."""

    def test_method_still_exists(self):
        """_check_active_standup exists for backward compatibility."""
        from services.intent.intent_service import IntentService

        assert hasattr(IntentService, "_check_active_standup")

    @pytest.mark.asyncio
    async def test_excludes_suspended_conversations(self):
        """_check_active_standup now skips SUSPENDED state (bug fix)."""
        from services.intent.intent_service import IntentService

        service = IntentService()
        manager = FakeStandupConversationManager()

        conv = await manager.create_conversation("sess-1", "user-1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._check_active_standup("user-1", "sess-1", "hello")

        # Should return None because SUSPENDED is not active
        assert result is None

    def test_deprecation_noted_in_docstring(self):
        """The method's docstring notes its deprecation."""
        import inspect

        from services.intent.intent_service import IntentService

        source = inspect.getsource(IntentService._check_active_standup)
        assert "DEPRECATED" in source or "deprecated" in source

    def test_no_debug_prints(self):
        """Issue #889 cleanup: debug print statements removed."""
        import inspect

        from services.intent.intent_service import IntentService

        source = inspect.getsource(IntentService._check_active_standup)
        assert "print(" not in source


class TestBindSessionIdResume:
    """Issue #1052 Phase 2 / #1053 Phase 3: bind_session_id end-to-end coverage.

    Verifies the production fix for resume-after-restart: a user suspends mid-flow
    on session-A, then resumes on session-B; the conversation must be reachable
    via session-B (and unreachable via session-A) once bind_session_id is called.
    """

    @pytest.mark.asyncio
    async def test_bind_session_id_makes_conv_findable_by_new_session(self):
        """After bind_session_id, the conv is findable via the new session id."""
        manager = FakeStandupConversationManager()

        conv = await manager.create_conversation("sess-A", "user-1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        # Pre-bind: findable by old session (with include_suspended)
        before = await manager.get_conversation_by_session("sess-A", include_suspended=True)
        assert before is not None
        assert before.id == conv.id

        # Bind the conversation to the new session id
        await manager.bind_session_id(conv.id, "sess-B")

        # Post-bind: findable by new session, NOT findable by old session
        after_new = await manager.get_conversation_by_session("sess-B", include_suspended=True)
        assert after_new is not None
        assert after_new.id == conv.id
        assert after_new.session_id == "sess-B"

        after_old = await manager.get_conversation_by_session("sess-A", include_suspended=True)
        assert (
            after_old is None
        ), "Old session should no longer find the conversation after re-binding"

    @pytest.mark.asyncio
    async def test_bind_session_id_preserves_conversation_state(self):
        """Re-binding does not alter conversation state or accumulated content."""
        manager = FakeStandupConversationManager()

        conv = await manager.create_conversation("sess-A", "user-1")
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.set_standup_content(conv.id, "**Yesterday**: shipped X\n**Today**: ship Y")
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        await manager.bind_session_id(conv.id, "sess-B")

        rebound = await manager.get_conversation(conv.id)
        assert rebound.state == StandupConversationState.SUSPENDED
        assert rebound.current_standup == "**Yesterday**: shipped X\n**Today**: ship Y"
        assert rebound.session_id == "sess-B"
