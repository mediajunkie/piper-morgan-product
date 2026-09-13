from typing import Any, Dict, Optional

import structlog

from services.api.serializers import intent_to_dict
from services.consciousness.conversation_consciousness import format_greeting_conscious
from services.domain.models import Intent
from services.shared_types import IntentCategory, PortfolioOnboardingState

logger = structlog.get_logger()


# Issue #490: Global onboarding manager and handler instances
# These are module-level singletons to persist onboarding state across requests
_onboarding_manager = None
_onboarding_handler = None


def _get_onboarding_components():
    """Lazy-load onboarding components to avoid circular imports."""
    global _onboarding_manager, _onboarding_handler
    if _onboarding_manager is None:
        from services.onboarding import PortfolioOnboardingHandler, PortfolioOnboardingManager

        _onboarding_manager = PortfolioOnboardingManager()
        _onboarding_handler = PortfolioOnboardingHandler(_onboarding_manager)
        # Issue #490 INVESTIGATION: First creation
        print(f"[ConversationHandler] Singleton CREATED: manager id={id(_onboarding_manager)}")
    return _onboarding_manager, _onboarding_handler


# Issue #585: Global standup conversation components (mirrors portfolio pattern)
# These are module-level singletons to persist standup conversation state across requests
_standup_manager = None
_standup_handler = None


def _get_standup_components():
    """Lazy-load standup conversation components to avoid circular imports."""
    global _standup_manager, _standup_handler
    if _standup_manager is None:
        from services.standup.conversation_handler import StandupConversationHandler
        from services.standup.conversation_manager import StandupConversationManager

        _standup_manager = StandupConversationManager()
        _standup_handler = StandupConversationHandler(conversation_manager=_standup_manager)
        # Issue #585 INVESTIGATION: First creation
        print(f"[ConversationHandler] Standup singleton CREATED: manager id={id(_standup_manager)}")
    return _standup_manager, _standup_handler


class ConversationHandler:
    """Handles the greeting conversational intent (calendar-aware, FTUX-aware).

    #1754: this handler is greeting-only. The farewell/thanks/chitchat
    branches (and the RESPONSES canned-copy table) were deleted per the Arch
    GO ruling 2026-09-12 — the action gate (_requires_canonical_handler)
    admits CONVERSATION here only for pure-pleasantry greetings; every other
    conversation action floor-routes, and the floor IS the conversational
    surface. The orphaned canned table was also a #1655-class liability
    (dead example copy that could become a live reply through an unexpected
    path).
    """

    async def respond(
        self, intent: Intent, session_id: str = None, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate the greeting response.

        #1754: greeting-only by contract. A non-greeting action arriving here
        is a gate-contract violation — surface it rather than answer with
        copy this handler no longer owns. The caller
        (canonical_handlers.handle) converts the raise into its honest
        generic fallback.
        """
        # ADR-059: Active onboarding check disabled (onboarding on ice)
        # #1536: fall back to the caller-threaded principal instead of
        # silently dropping it when intent.context lacks user_id.
        user_id = (intent.context or {}).get("user_id") or user_id

        # #1759: the clarification_needed arm/consume pair
        # (_handle_clarification_needed / handle_clarification_response and
        # the session pending_clarification carrier) was deleted as dead code
        # per the #1730 Gap-2 ruling — clarification_needed intents floor-route
        # at the action gate and never reach this handler live.

        if intent.action != "greeting":
            raise ValueError(
                f"ConversationHandler.respond received non-greeting action "
                f"{intent.action!r} — the action gate admits only pure-pleasantry "
                f"'greeting' to this handler (#1754)"
            )

        # Issue #102: Enhanced greeting with calendar awareness
        # Issue #849: Thread user_id for user-scoped calendar auth
        return await self._respond_to_greeting(intent, session_id, user_id=user_id)

    async def _get_calendar_summary(
        self, user_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """Issue #102: Get calendar summary for greeting enhancement."""
        try:
            from services.integrations.calendar.calendar_integration_router import (
                CalendarIntegrationRouter,
            )

            # Issue #849: Thread user_id for user-scoped calendar auth
            calendar_router = CalendarIntegrationRouter(user_id=user_id)
            # #1196: gate on REAL authentication — an unconfigured calendar
            # integration can return an empty-stats stub instead of raising,
            # which the greeting then narrates as "took a look at your
            # calendar... clear day ahead" (fabricated access claim). No
            # auth → no summary → greeting simply omits the calendar.
            if not await calendar_router.authenticate():
                return None
            # #1425: thread the principal explicitly. This call site dropped it,
            # so the adapter computed the day window in its hardcoded fallback
            # timezone rather than the user's.
            summary = await calendar_router.get_temporal_summary(user_id=user_id)
            return summary
        except Exception as e:
            logger.warning(f"Could not fetch calendar for greeting: {e}")
            return None

    async def _respond_to_greeting(
        self, intent: Intent, session_id: str = None, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Issue #102: Generate calendar-aware greeting response.
        Issue #490: Check for portfolio onboarding trigger.
        """
        # Issue #490: Check if this user should be offered portfolio onboarding
        # #1536: fall back to the caller-threaded principal instead of
        # silently dropping it when intent.context lacks user_id.
        user_id = (intent.context or {}).get("user_id") or user_id

        # DEBUG Issue #490: Trace greeting flow
        logger.info(
            "greeting_onboarding_trace",
            user_id=user_id,
            session_id=session_id,
            has_context=intent.context is not None,
            context_keys=list(intent.context.keys()) if intent.context else [],
        )

        # Issue #888: Check for suspended sessions before offering new onboarding
        if user_id:
            reentry_response = await self._check_suspended_session_reentry(
                user_id, session_id=session_id
            )
            if reentry_response:
                return reentry_response

        # ADR-059: Portfolio onboarding offer disabled (onboarding on ice)
        # Was: _check_portfolio_onboarding(user_id, session_id)

        # #1688 FTUX empty-state interview: a COLD user (zero configured
        # integrations) on the FIRST exchange gets the interview opening
        # instead of the canned greeting — the interview OWNS the empty
        # moment (the FTUX model's rule; same family as #1635's empty-state
        # suppression). Copy is CXO's v0.2 verbatim, minus the why_asking
        # promise PPM cut (cross-session recall is #1705, unbuilt). The
        # returned offer record is armed by intent_service at the canonical
        # seam so the next turn's answer binds (#1654 carrier idiom).
        # Fail-graceful: any error → the normal greeting, never a dead turn.
        try:
            from services.intent_service import first_contact as _first_contact

            interview = await _first_contact.ftux_interview_greeting(
                session_id=session_id, user_id=user_id
            )
        except Exception as e:
            logger.warning("ftux_interview_greeting_error", error=str(e))
            interview = None
        if interview:
            interview_intent = intent_to_dict(intent)
            # Top-level flag: _apply_soft_offer's _pending_flags check reads
            # result.intent_data — a soft workflow offer must never clobber
            # the just-armed interview question (the #1605 one-slot rule).
            interview_intent["ftux_interview_question_pending"] = True
            return {
                "message": interview["message"],
                "intent": interview_intent,
                "workflow_id": None,
                # Armed at the intent_service canonical seam (the #846
                # register-embedded-offers seam) — this handler has no
                # access to the session-scoped offer store.
                "ftux_interview_offer": interview["offer"],
            }

        # Get calendar summary (may be None if unavailable)
        # Issue #849: Thread user_id for user-scoped calendar auth
        calendar_summary = await self._get_calendar_summary(user_id=user_id)

        # Issue #407: Use consciousness-enhanced greeting
        response = format_greeting_conscious(calendar_summary=calendar_summary)

        # #1536 FTUX-COLDSTART: on the very first exchange of a conversation,
        # when the user has a configured connector, append a demonstration
        # block built from a read performed this turn — the user's own data,
        # unprompted, instead of a purely generic greeting. The block is
        # DETERMINISTIC (pure string formatting over the gathered payload in
        # first_contact.render_first_contact_block), so this path is
        # structurally incapable of naming an entity the read didn't return.
        # Fail-graceful: any error → the plain greeting, never a dead turn.
        try:
            from services.intent_service import first_contact as _first_contact

            demo_block = await _first_contact.first_contact_demo_block(
                session_id=session_id, user_id=user_id
            )
            if demo_block:
                response = f"{response}\n\n{demo_block}"
        except Exception as e:
            logger.warning("first_contact_greeting_error", error=str(e))

        return {
            "message": response,
            "intent": intent_to_dict(intent),
            "workflow_id": None,
        }

    async def _check_portfolio_onboarding(
        self, user_id: str, session_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Issue #490, #888: Check if user should be offered portfolio onboarding.

        Issue #888: Changed from auto-activate to offer-first model.
        Creates session in OFFERED state (non-active from registry perspective).
        User must explicitly accept before onboarding begins.

        Returns an onboarding offer if the user has no projects,
        otherwise returns None to continue with normal greeting.
        """
        try:
            from services.database.repositories import ProjectRepository
            from services.database.session_factory import AsyncSessionFactory
            from services.onboarding import FirstMeetingDetector

            async with AsyncSessionFactory.session_scope() as db_session:
                project_repo = ProjectRepository(db_session)
                detector = FirstMeetingDetector(project_repo)

                if await detector.should_trigger(user_id):
                    # Issue #888: Offer onboarding (OFFERED state, not INITIATED)
                    _, onboarding_handler = _get_onboarding_components()
                    response = onboarding_handler.offer_onboarding(session_id, user_id)

                    logger.info(
                        "portfolio_onboarding_offered",
                        user_id=user_id,
                        session_id=session_id,
                        onboarding_id=response.metadata.get("onboarding_id"),
                    )

                    return {
                        "message": response.message,
                        "intent": {
                            "category": IntentCategory.GUIDANCE.value,
                            "action": "portfolio_onboarding_offered",
                            "confidence": 1.0,
                            "context": {
                                "onboarding_id": response.metadata.get("onboarding_id"),
                                "state": response.state.value,
                                "offer_pending": True,
                            },
                        },
                        "workflow_id": None,
                        "onboarding_session": response.metadata.get("onboarding_id"),
                    }

        except Exception as e:
            logger.warning(f"Could not check portfolio onboarding: {e}")

        return None

    async def _check_pending_onboarding_offer(
        self, user_id: str, message: str
    ) -> Optional[Dict[str, Any]]:
        """
        Issue #888: Check if user has a pending onboarding offer (OFFERED state).

        When the user sends a message after being offered onboarding,
        this checks for an OFFERED session and routes the response
        to handle_offer_response(). If the user accepts, transitions
        to active onboarding. If declined or ignored, transitions to DECLINED.

        Returns a response dict if the offer was handled, None otherwise.
        """
        try:
            from services.shared_types import PortfolioOnboardingState

            onboarding_manager, onboarding_handler = _get_onboarding_components()
            session = onboarding_manager.get_session_by_user(user_id)

            if not session or session.state != PortfolioOnboardingState.OFFERED:
                return None

            logger.info(
                "checking_pending_onboarding_offer",
                user_id=user_id,
                session_id=session.id,
            )

            response = onboarding_handler.handle_offer_response(session.id, message)

            if response is None:
                # Implicit decline — user ignored the offer. Return None
                # so the message goes through normal classification.
                return None

            return {
                "message": response.message,
                "intent": {
                    "category": IntentCategory.GUIDANCE.value,
                    "action": "portfolio_onboarding",
                    "confidence": 1.0,
                    "context": {
                        "onboarding_id": session.id,
                        "state": response.state.value,
                    },
                },
                "workflow_id": None,
                "onboarding_session": session.id,
            }

        except Exception as e:
            logger.warning(f"Could not check pending onboarding offer: {e}")

        return None

    async def _check_suspended_session_reentry(
        self, user_id: str, session_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Issue #888: Check for suspended sessions and offer to resume.

        PPM direction: "Save state, offer to resume once at next conversation
        start, accept 'no' gracefully." This runs during greeting handling.

        #1529 OFFER-BINDING: when the offer is made, it is RECORDED as a
        one-turn `last_offer` (offer_type="process_resume") on the user-scoped
        conversation context. `_check_pending_resume_offer` (#889) only binds
        bare affirmatives ("yes", "yes please") to a resume while that record
        is pending — without it, any bare "yes" while a suspended standup
        existed resumed the standup, regardless of what was actually offered
        last turn (PM's standup hijack).

        Returns a resume offer if a suspended session exists, None otherwise.
        """
        try:
            from services.process.registry import get_process_registry

            registry = get_process_registry()
            suspended = await registry.check_suspended_processes(user_id)

            if suspended is None:
                return None

            logger.info(
                "offering_suspended_session_reentry",
                user_id=user_id,
                process_type=suspended.process_type.value,
            )

            # Construct a friendly resume offer
            resume_message = (
                f"Welcome back! {suspended.description} "
                "Would you like to continue, or start fresh?"
            )

            # #1529: record the offer so next turn's bare affirmative binds
            # to IT (one-turn memory, same store as #852 contextual offers;
            # user-scoped per #1394, persisted per #953).
            if session_id:
                from services.intent_service.conversation_context import (
                    LastOffer,
                    get_or_create_context,
                )

                try:
                    ctx = get_or_create_context(session_id, user_id=user_id)
                    ctx.last_offer = LastOffer(
                        offer_type="process_resume",
                        continuation_hint=f"resume {suspended.process_type.value}",
                        offer_text=resume_message,
                    )
                except (ValueError, KeyError):
                    pass  # Non-UUID session_id — offer stays greeting-only

            return {
                "message": resume_message,
                "intent": {
                    "category": IntentCategory.GUIDANCE.value,
                    "action": "suspended_session_reentry",
                    "confidence": 1.0,
                    "context": {
                        "suspended_process": suspended.process_type.value,
                        "offer_resume": True,
                    },
                },
                "workflow_id": None,
            }

        except Exception as e:
            logger.warning(f"Could not check suspended sessions: {e}")

        return None

    async def _handle_active_onboarding(
        self, user_id: str, session_id: str, intent: Intent
    ) -> Optional[Dict[str, Any]]:
        """
        Issue #490: Handle messages when user has an active onboarding session.

        Routes user messages to the portfolio onboarding handler if an active
        session exists for this user.
        """
        try:
            onboarding_manager, onboarding_handler = _get_onboarding_components()

            # Check if user has an active onboarding session
            session = onboarding_manager.get_session_by_user(user_id)
            if not session:
                return None

            # Check if session is in a terminal state
            if session.state in (
                PortfolioOnboardingState.COMPLETE,
                PortfolioOnboardingState.DECLINED,
            ):
                return None

            # Route the message to the onboarding handler
            user_message = intent.context.get("original_message", "") if intent.context else ""
            if not user_message:
                return None

            response = onboarding_handler.handle_turn(session.id, user_message)

            # If onboarding completed, persist the projects
            if response.is_complete and response.state == PortfolioOnboardingState.COMPLETE:
                await self._persist_onboarding_projects(user_id, response.captured_projects)

            logger.info(
                "portfolio_onboarding_turn_handled",
                user_id=user_id,
                session_id=session_id,
                onboarding_id=session.id,
                state=response.state.value,
                is_complete=response.is_complete,
            )

            return {
                "message": response.message,
                "intent": {
                    "category": IntentCategory.GUIDANCE.value,
                    "action": "portfolio_onboarding",
                    "confidence": 1.0,
                    "context": {
                        "onboarding_id": session.id,
                        "state": response.state.value,
                    },
                },
                "workflow_id": None,
                "onboarding_session": session.id if not response.is_complete else None,
            }

        except Exception as e:
            logger.warning(f"Could not handle active onboarding: {e}")

        return None

    async def _persist_onboarding_projects(self, user_id: str, captured_projects: list) -> None:
        """
        Issue #490: Persist projects captured during onboarding.

        Creates Project entities in the database for each project the user
        described during the onboarding conversation, then marks the user's
        setup as complete.
        """
        if not captured_projects:
            return

        try:
            from datetime import datetime

            from sqlalchemy import text

            from services.database.repositories import ProjectRepository, RepositoryRepository
            from services.database.session_factory import AsyncSessionFactory
            from services.domain import models as domain

            async with AsyncSessionFactory.session_scope() as db_session:
                project_repo = ProjectRepository(db_session)
                repo_repo = RepositoryRepository(db_session)

                for project_data in captured_projects:
                    # Create the project
                    created_project = await project_repo.create(
                        owner_id=user_id,
                        name=project_data.get("name", "Untitled Project"),
                        description=project_data.get("description", ""),
                        is_default=project_data.get("is_default", False),
                        is_archived=False,
                    )

                    # Issue #863: Link repo if one was provided during onboarding
                    repo_full_name = project_data.get("repo")
                    if repo_full_name:
                        existing = await repo_repo.get_by_full_name(
                            repo_full_name, owner_id=user_id
                        )
                        if existing:
                            repo_entity = existing
                        else:
                            # Issue #867: Soft-validate via GitHub API
                            from services.infrastructure.github_repo_validator import (
                                apply_validation_metadata,
                                validate_github_repo,
                            )

                            validation = await validate_github_repo(repo_full_name)
                            if validation.validated and not validation.exists:
                                logger.warning(
                                    "onboarding_repo_validation_warning",
                                    full_name=repo_full_name,
                                    error=validation.error,
                                )

                            repo_domain = domain.Repository(
                                owner_id=user_id,
                                full_name=repo_full_name,
                                provider="github",
                                url=f"https://github.com/{repo_full_name}",
                            )
                            apply_validation_metadata(repo_domain, validation)
                            repo_entity = await repo_repo.create_repository(repo_domain)

                        await repo_repo.link_to_project(
                            repository_id=repo_entity.id,
                            project_id=created_project.id,
                            linked_by=user_id,
                            is_primary=True,
                        )

                # Mark user's setup as complete (Issue #490)
                await db_session.execute(
                    text(
                        "UPDATE users SET setup_complete = true, "
                        "setup_completed_at = :now WHERE id = :user_id"
                    ),
                    {"now": datetime.now(), "user_id": user_id},
                )

                await db_session.commit()

                repo_count = sum(1 for p in captured_projects if p.get("repo"))
                logger.info(
                    "portfolio_onboarding_projects_persisted",
                    user_id=user_id,
                    project_count=len(captured_projects),
                    repo_count=repo_count,
                    setup_complete=True,
                )

        except Exception as e:
            logger.error(f"Failed to persist onboarding projects: {e}")

    def _format_calendar_greeting(self, summary: Dict[str, Any]) -> str:
        """Issue #102: Format greeting with calendar insights."""
        from datetime import datetime

        now = datetime.now()
        time_greeting = self._get_time_of_day_greeting(now.hour)

        lines = [f"{time_greeting}! Here's your day at a glance:\n"]

        # Current/next meeting
        if summary.get("current_meeting"):
            meeting = summary["current_meeting"]
            lines.append(f"📍 **Now**: {meeting.get('summary', 'Meeting in progress')}")
        elif summary.get("next_meeting"):
            meeting = summary["next_meeting"]
            # Parse start_time to get readable format
            start_time = meeting.get("start_time", "soon")
            if "T" in str(start_time):
                try:
                    dt = datetime.fromisoformat(start_time.replace("Z", "+00:00"))
                    start_time = dt.strftime("%I:%M %p").lstrip("0")
                except (ValueError, AttributeError):
                    pass
            lines.append(f"📅 **Next**: {meeting.get('summary', 'Meeting')} at {start_time}")

        # Free time blocks
        if summary.get("free_blocks"):
            blocks = summary["free_blocks"][:2]  # Show up to 2 free blocks
            if blocks:
                block_texts = []
                for b in blocks:
                    start = b.get("start_time", "")
                    end = b.get("end_time", "")
                    # Format times
                    try:
                        if "T" in str(start):
                            start_dt = datetime.fromisoformat(start.replace("Z", "+00:00"))
                            start = start_dt.strftime("%I:%M").lstrip("0")
                        if "T" in str(end):
                            end_dt = datetime.fromisoformat(end.replace("Z", "+00:00"))
                            end = end_dt.strftime("%I:%M").lstrip("0")
                    except (ValueError, AttributeError):
                        pass
                    block_texts.append(f"{start}-{end}")
                lines.append(f"⏰ **Free time**: {', '.join(block_texts)}")

        # Today's meeting count from stats
        stats = summary.get("stats", {})
        total_meetings = stats.get("total_meetings_today", 0)
        if total_meetings > 0:
            lines.append(f"\n📋 {total_meetings} meeting{'s' if total_meetings != 1 else ''} today")
        else:
            lines.append("\n✨ Clear calendar today!")

        lines.append("\nWhat would you like to focus on?")

        return "\n".join(lines)

    def _get_time_of_day_greeting(self, hour: int) -> str:
        """Issue #102: Return appropriate time-of-day greeting."""
        if hour < 12:
            return "Good morning"
        elif hour < 17:
            return "Good afternoon"
        else:
            return "Good evening"
