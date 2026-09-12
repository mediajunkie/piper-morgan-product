"""#1769 — the resume-offer seam adopts THE acceptance contract (#1739).

The seam (``IntentService._check_pending_resume_offer``, the #889 mechanic)
carried a fully bespoke inline accept/decline vocabulary — four frozensets
consulted by exact full-message match, invisible to BOTH #1739 ratchet scans
(it called no legacy detector and referenced no shared vocabulary name).

Red-first disagreement pins (inline word-sets vs ``evaluate_acceptance``),
each found by feeding both surfaces the same turn:

- "yes?" (a question containing an accept word): both refuse to fire, but
  the contract SURVIVES the arm (§5a silent re-arm) where the word-sets
  silently let the one-turn offer expire.
- "Yes." / "yes!" / "go ahead" (the #1694 strict-direction failure): the
  exact-match sets did NOTHING; the contract accepts.
- "resume." (punctuated explicit command, unarmed): exact match failed; the
  taught-command surface accepts anytime.
- "restart": taught by ``_start_standup_conversation``'s own ask copy
  ("Reply 'continue' or 'restart'") and consumed by NOTHING before this
  adoption.
- "please hold on a sec" (sub-#1631-floor aside opening with a greedy
  LOW-tier accept row): the word-sets ignored it; the contract accepts —
  the inherited LOW-tier greedy residue, pinned DELIBERATELY (CXO-owned
  tightening lands here automatically).
- "not now" (deferral phrasing): word-sets ignored it (flow stayed
  suspended); the shared decline vocabulary declines → abandon. Pinned
  deliberately; the deferral-vs-abandon vocabulary question is filed.
- "n" / "yea": bespoke-only tokens, no longer in any vocabulary — narrowing
  pinned (the flow stays suspended for greeting re-entry; nothing is lost).

Arm half (#1766 census rows): ``_start_standup_conversation`` (session-
exists ask) and ``_resume_suspended_standup`` (legacy either/or ask) now arm
the one-turn process-resume offer with their RENDERED ask threaded as
``question=`` — both census rows shrink out in this commit.
"""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import pytest

from services.intent_service.acceptance import (
    AcceptanceVerdict,
    evaluate_acceptance,
)
from services.process.registry import ProcessType, SuspendedInfo
from services.shared_types import EffectClass, Outwardness, StandupConversationState

RESUME_ASK = "Welcome back! Your standup was paused. Would you like to continue, or start fresh?"


def _suspended_standup() -> SuspendedInfo:
    return SuspendedInfo(
        process_type=ProcessType.STANDUP,
        suspended_at=datetime.now(),
        description="Your standup was paused.",
    )


def _service():
    from services.intent.intent_service import IntentService

    return IntentService()


class _SeamHarness:
    """The #889 test harness shape: mocked registry + spied resume/abandon."""

    def __init__(self, service, suspended=True):
        self.service = service
        self._suspended = _suspended_standup() if suspended else None
        self.resume = None
        self.abandon = None

    def __enter__(self):
        self._patches = [
            patch("services.intent.intent_service.get_process_registry"),
            patch.object(
                self.service,
                "_resume_suspended_standup",
                new_callable=AsyncMock,
                return_value=MagicMock(success=True),
            ),
            patch.object(
                self.service,
                "_abandon_suspended_standup",
                new_callable=AsyncMock,
                return_value=MagicMock(success=True),
            ),
        ]
        registry_fn = self._patches[0].__enter__()
        self.resume = self._patches[1].__enter__()
        self.abandon = self._patches[2].__enter__()
        mock_registry = MagicMock()
        mock_registry.check_suspended_processes = AsyncMock(return_value=self._suspended)
        registry_fn.return_value = mock_registry
        return self

    def __exit__(self, *exc):
        for p in reversed(self._patches):
            p.__exit__(*exc)
        return False


class TestQuestionsNeverFireTheResume:
    """Contract axis (a): a question is a state query, never consent."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "question",
        ["yes?", "resume?", "should we resume?", "are we still doing the standup"],
    )
    async def test_question_forms_never_resume_and_never_abandon(self, question):
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                question,
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is None, f"{question!r} must not claim the turn"
            h.resume.assert_not_called()
            h.abandon.assert_not_called()

    @pytest.mark.asyncio
    async def test_state_question_survives_the_arm_silently(self):
        """§5a SILENT survival (LOW tier): the one-turn arm is re-armed so
        next turn's bare "yes" still binds — the word-sets let it expire.
        DISAGREEMENT PIN (red before adoption)."""
        from services.intent_service.conversation_context import get_or_create_context

        service = _service()
        session_id = str(uuid4())
        user_id = str(uuid4())
        with _SeamHarness(service):
            result = await service._check_pending_resume_offer(
                user_id,
                session_id,
                "yes?",
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
        assert result is None
        ctx = get_or_create_context(session_id, user_id=user_id)
        assert ctx.last_offer is not None, "the survived arm must be re-armed"
        assert ctx.last_offer.offer_type == "process_resume"
        assert ctx.last_offer.offer_text == RESUME_ASK

    @pytest.mark.asyncio
    async def test_unarmed_question_survives_nothing(self):
        """No arm pending → nothing to survive; the question just routes."""
        from services.intent_service.conversation_context import get_or_create_context

        service = _service()
        session_id = str(uuid4())
        user_id = str(uuid4())
        with _SeamHarness(service):
            result = await service._check_pending_resume_offer(
                user_id, session_id, "should we resume?"
            )
        assert result is None
        ctx = get_or_create_context(session_id, user_id=user_id)
        assert ctx.last_offer is None


class TestContractAcceptsTheWordSetsMissed:
    """#1694's direction: the exact-match sets failed strict — these did
    NOTHING before adoption (disagreement pins, red first)."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("turn", ["Yes.", "yes!", "go ahead", "do it", "sounds good"])
    async def test_armed_affirmative_variants_now_resume(self, turn):
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                turn,
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is not None, f"{turn!r} must resume while armed"
            h.resume.assert_called_once()

    @pytest.mark.asyncio
    async def test_punctuated_explicit_command_resumes_anytime(self):
        """ "resume." — the taught command surface is punctuation-tolerant
        (the predicate's taught normalization); the exact-match set was not."""
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer("user-1", str(uuid4()), "resume.")
            assert result is not None
            h.resume.assert_called_once()

    @pytest.mark.asyncio
    async def test_restart_now_declines_when_armed(self):
        """The ask copy taught 'restart'; no vocabulary consumed it."""
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                "restart",
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is not None
            h.abandon.assert_called_once()

    @pytest.mark.asyncio
    async def test_greedy_low_tier_residue_inherited_deliberately(self):
        """ "please hold on a sec" (sub-floor aside, greedy "^please\\s" row)
        now ACCEPTS while armed — the inherited LOW-tier residue, pinned so
        the CXO-owned vocabulary tightening lands here automatically and
        VISIBLY. Recoverable: the accept re-enters a flow the user can end
        or re-suspend; WRITE×PRIVATE."""
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                "please hold on a sec",
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is not None
            h.resume.assert_called_once()

    @pytest.mark.asyncio
    async def test_deferral_phrasing_declines_deliberately(self):
        """ "not now" takes the SHARED decline vocabulary → abandon (the
        seam's #888 decline semantics). Pinned deliberately; whether
        deferral rows should defer rather than abandon at resumable-flow
        seams is filed vocabulary-lane work."""
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                "not now",
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is not None
            h.abandon.assert_called_once()


class TestBespokeOnlyTokensNarrowedDeliberately:
    """Tokens only the bespoke sets knew. The contract vocabulary governs;
    a PASS leaves the flow suspended for greeting re-entry — nothing lost."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("turn", ["n", "yea"])
    async def test_bespoke_only_tokens_no_longer_claim_the_turn(self, turn):
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                turn,
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is None
            h.resume.assert_not_called()
            h.abandon.assert_not_called()


class TestOfferBindingPreserved:
    """#1529 pins: explicit commands anytime; bare vocabulary only armed."""

    @pytest.mark.asyncio
    @pytest.mark.parametrize("turn", ["yes", "yes please", "sure", "ok", "y", "go ahead"])
    async def test_unarmed_bare_affirmatives_never_resume(self, turn):
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer("user-1", str(uuid4()), turn)
            assert result is None, f"unbound {turn!r} must not claim the turn"
            h.resume.assert_not_called()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("turn", ["continue", "resume", "pick it up", "let's continue"])
    async def test_explicit_resume_commands_work_anytime(self, turn):
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer("user-1", str(uuid4()), turn)
            assert result is not None, f"{turn!r} names the flow — honored anytime"
            h.resume.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("turn", ["start over", "start fresh"])
    async def test_explicit_restart_commands_work_anytime(self, turn):
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer("user-1", str(uuid4()), turn)
            assert result is not None
            h.abandon.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.parametrize("turn", ["fresh", "new", "restart"])
    async def test_armed_only_decline_tokens_require_the_arm(self, turn):
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer("user-1", str(uuid4()), turn)
            assert result is None, f"unarmed {turn!r} must not abandon the flow"
            h.abandon.assert_not_called()

    @pytest.mark.asyncio
    async def test_flow_exit_stays_deterministic_and_first(self):
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                "end standup",
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is not None
            h.abandon.assert_called_once()
            h.resume.assert_not_called()

    @pytest.mark.asyncio
    async def test_prose_aside_neither_accepts_nor_steals(self):
        """#1631 floor: a long single-line prose reply opening 'yes, ' PASSes."""
        prose = (
            "yes, I know the standup is sitting there but before anything else "
            "I need to write up the incident notes from this morning and check "
            "whether the deploy went out — remind me about it later please."
        )
        assert len(prose) >= 160
        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                prose,
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is None
            h.resume.assert_not_called()
            h.abandon.assert_not_called()


class TestStoredAskThreaded:
    """#1665 input adequacy: the seam consults THE predicate with the
    arm-site's rendered ask threaded — never a bespoke decision."""

    @pytest.mark.asyncio
    async def test_seam_threads_the_stored_ask_into_the_predicate(self, monkeypatch):
        import services.intent_service.acceptance as acceptance_mod

        seen = {}
        real = acceptance_mod.evaluate_acceptance

        def spy(message, **kwargs):
            seen.setdefault("calls", []).append(kwargs)
            return real(message, **kwargs)

        monkeypatch.setattr(acceptance_mod, "evaluate_acceptance", spy)

        service = _service()
        with _SeamHarness(service) as h:
            result = await service._check_pending_resume_offer(
                "user-1",
                str(uuid4()),
                "yes",
                resume_offer_pending=True,
                resume_offer_question=RESUME_ASK,
            )
            assert result is not None
            h.resume.assert_called_once()
        assert seen.get("calls"), "the seam must consult evaluate_acceptance"
        assert any(k.get("armed_question") == RESUME_ASK for k in seen["calls"])
        assert all(
            k.get("effect") is EffectClass.WRITE and k.get("outwardness") is Outwardness.PRIVATE
            for k in seen["calls"]
        ), "axes are the registry-declared WRITE×PRIVATE (standup_interview)"


class TestArmHalfCensusRows:
    """#1766: the two ask sites arm the one-turn offer with their rendered
    ask threaded as question= — their census rows shrink out."""

    @pytest.mark.asyncio
    async def test_start_standup_existing_session_arms_the_resume_offer(self):
        from services.intent_service.conversation_context import get_or_create_context

        service = _service()
        session_id = str(uuid4())
        user_id = str(uuid4())

        existing = MagicMock()
        existing.id = "conv-1"
        existing.state = StandupConversationState.GATHERING_TODAY
        manager = MagicMock()
        manager.get_conversation_by_session = AsyncMock(return_value=existing)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._start_standup_conversation(user_id, session_id)

        assert "in progress" in result.message
        ctx = get_or_create_context(session_id, user_id=user_id)
        assert ctx.last_offer is not None, "the session-exists ask must arm"
        assert ctx.last_offer.offer_type == "process_resume"
        assert ctx.last_offer.offer_text == result.message

    @pytest.mark.asyncio
    async def test_legacy_resume_ask_arms_the_resume_offer(self):
        from services.intent_service.conversation_context import get_or_create_context
        from tests.unit.services.standup._fake_conversation_manager import (
            FakeStandupConversationManager,
        )

        service = _service()
        session_id = str(uuid4())
        user_id = str(uuid4())

        manager = FakeStandupConversationManager()
        conv = await manager.create_conversation("old-sess", user_id)
        await manager.transition_state(conv.id, StandupConversationState.GENERATING)
        await manager.set_standup_content(conv.id, "**Yesterday**: shipped X")
        await manager.transition_state(conv.id, StandupConversationState.SUSPENDED)

        with patch(
            "services.conversation.conversation_handler._get_standup_components",
            return_value=(manager, MagicMock()),
        ):
            result = await service._resume_suspended_standup(user_id, session_id)

        assert "start fresh" in result.message
        ctx = get_or_create_context(session_id, user_id=user_id)
        assert ctx.last_offer is not None, "the legacy either/or ask must arm"
        assert ctx.last_offer.offer_type == "process_resume"
        assert ctx.last_offer.offer_text == result.message


class TestTaughtDeclines:
    """The predicate extension this adoption needed: taught DECLINE phrases,
    full-message only, LOW tier only — symmetric with taught_accepts."""

    def test_taught_decline_full_message_only(self):
        assert (
            evaluate_acceptance(
                "start fresh",
                effect=EffectClass.WRITE,
                outwardness=Outwardness.PRIVATE,
                armed_question=RESUME_ASK,
                taught_declines=("start fresh",),
            )
            is AcceptanceVerdict.DECLINE
        )
        assert (
            evaluate_acceptance(
                "start fresh with just the blockers section rewritten",
                effect=EffectClass.WRITE,
                outwardness=Outwardness.PRIVATE,
                armed_question=RESUME_ASK,
                taught_declines=("start fresh",),
            )
            is AcceptanceVerdict.PASS
        )

    def test_taught_decline_never_loosens_the_strict_tier(self):
        assert (
            evaluate_acceptance(
                "start fresh",
                effect=EffectClass.DESTRUCTIVE,
                outwardness=Outwardness.PRIVATE,
                armed_question="Delete all 3 reminders?",
                taught_declines=("start fresh",),
            )
            is AcceptanceVerdict.PASS
        )

    def test_question_shape_beats_taught_decline(self):
        assert (
            evaluate_acceptance(
                "start fresh?",
                effect=EffectClass.WRITE,
                outwardness=Outwardness.PRIVATE,
                armed_question=RESUME_ASK,
                taught_declines=("start fresh",),
            )
            is AcceptanceVerdict.STATE_QUESTION
        )
