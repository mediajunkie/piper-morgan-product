"""
Issue #553: Standup conversation flow handler.

Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Handles multi-turn standup conversations by:
- Routing based on conversation state
- Generating context-aware follow-up questions
- Processing refinement requests
- Managing graceful fallback

Issue #556: Performance & Reliability enhancements:
- Retry logic for transient failures
- Timeout handling
- Graceful degradation
- Structured performance logging (Phase 4)
"""

import asyncio
import time
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import structlog
from tenacity import (
    AsyncRetrying,
    RetryError,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from services.domain.models import (
    StandupConversation,
    StandupItem,
    StandupPartialCapture,
)
from services.shared_types import StandupConversationState
from services.standup.completion_detector import detect_completion
from services.standup.conversation_manager import StandupConversationManager

# Issue #900 Phase 2: skip-signal phrases (case-insensitive substring match).
# Used by per-part handlers to detect "no items for this part, advance".
_SKIP_SIGNAL_PHRASES = (
    "skip",
    "nothing",
    "n/a",
    "none",
    "no blockers",
    "no, no blockers",
    "nope",
)


def _is_skip_signal(message: str) -> bool:
    """True if the user message reads as a skip/empty signal for the current part."""
    text = message.strip().lower()
    if not text:
        return True
    # Standalone "no" counts as skip; "no blockers right now" also counts.
    if text in ("no", "n", "nah"):
        return True
    return any(phrase in text for phrase in _SKIP_SIGNAL_PHRASES)


def _next_uncaptured_part_state(
    capture: StandupPartialCapture,
) -> StandupConversationState:
    """Pick the gathering state to resume at based on what's already captured.

    Issue #900 Phase 4 resume protocol. Walks the parts in order and returns
    the first one that's still empty. If all three are populated (rare —
    user resumed despite having captured everything), defaults to BLOCKERS
    so the next handler advances to GENERATING.
    """
    if not capture.yesterday:
        return StandupConversationState.GATHERING_YESTERDAY
    if not capture.today:
        return StandupConversationState.GATHERING_TODAY
    if not capture.blockers:
        return StandupConversationState.GATHERING_BLOCKERS
    return StandupConversationState.GATHERING_BLOCKERS


def _format_capture_replay(capture: StandupPartialCapture) -> str:
    """Render captured content for the resume message.

    Returns a markdown-ish block summarizing what's already been captured,
    or an empty string if nothing yet. Each part header only renders if
    that part has items (skip the noise of "Yesterday: (none)").
    """
    blocks: List[str] = []
    if capture.yesterday:
        lines = "\n".join(f"- {item.display}" for item in capture.yesterday)
        blocks.append(f"**Yesterday:**\n{lines}")
    if capture.today:
        lines = "\n".join(f"- {item.display}" for item in capture.today)
        blocks.append(f"**Today:**\n{lines}")
    if capture.blockers:
        lines = "\n".join(f"- {item.display}" for item in capture.blockers)
        blocks.append(f"**Blockers:**\n{lines}")
    return "\n\n".join(blocks)


_RESUME_PROMPTS = {
    StandupConversationState.GATHERING_YESTERDAY: "What did you work on yesterday?",
    StandupConversationState.GATHERING_TODAY: "What's planned for today?",
    StandupConversationState.GATHERING_BLOCKERS: "Any blockers or things you need help with?",
}


def _format_standup_from_capture(capture: StandupPartialCapture) -> str:
    """Render the final standup directly from captured StandupItems.

    Issue #900 Phase 5. The 3-part collection flow puts the user in the
    role of source-of-truth — by the time we reach GENERATING via the
    blockers handler, every standup item has already been authored by
    the user. There's no need for LLM generation; we render the captured
    items into the existing markdown standup format directly.

    Each part renders as a `*Section:*` block with `* item.display`
    bullet lines. Empty parts render with `* Nothing to report.` so the
    standup keeps a consistent shape (a missing section would look like
    truncation).
    """

    def _render_section(title: str, items: List[StandupItem]) -> str:
        if items:
            lines = "\n".join(f"* {it.display}" for it in items)
        else:
            lines = "* Nothing to report."
        return f"*{title}:*\n{lines}"

    return "\n\n".join(
        [
            _render_section("Yesterday", capture.yesterday),
            _render_section("Today", capture.today),
            _render_section("Blockers", capture.blockers),
        ]
    )


def _parse_items_from_message(message: str, *, source: str = "user") -> List[StandupItem]:
    """Parse a user message into a list of StandupItems.

    Splits on newlines and bullet markers; trims whitespace; drops empties.
    Each non-empty line becomes one StandupItem with `source` set (default
    "user"). Icon left blank — these are user-typed entries, not
    integration-sourced.

    Issue #900 Phase 2.
    """
    if not message:
        return []
    items: List[StandupItem] = []
    # Split on newlines first; within a line, also handle leading bullet markers.
    for raw_line in message.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        # Strip common bullet markers
        for marker in ("- ", "* ", "• "):
            if line.startswith(marker):
                line = line[len(marker) :].strip()
                break
        if line:
            items.append(StandupItem(display=line, source=source))
    return items

logger = structlog.get_logger()


# Issue #556: Error categories for retry decisions
class TransientError(Exception):
    """Transient error that may succeed on retry (network, rate limit)."""

    pass


class PermanentError(Exception):
    """Permanent error that won't succeed on retry (config, auth)."""

    pass


@dataclass
class ConversationResponse:
    """Response from conversation handler."""

    message: str
    state: StandupConversationState
    requires_input: bool = True
    standup_content: Optional[str] = None
    suggestions: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class StandupConversationHandler:
    """
    Issue #553: Multi-turn conversation flow for standup generation.

    State Machine Flow:
    INITIATED -> GATHERING_PREFERENCES -> GENERATING -> REFINING -> FINALIZING -> COMPLETE
                                       |            ^
                                       +------------+ (skip preferences)

    Any state can transition to ABANDONED on timeout/cancel.

    Issue #556: Reliability enhancements:
    - Retry transient failures with exponential backoff
    - Timeout handling for slow external services
    - Graceful fallback on persistent failures
    """

    # Issue #556: Retry configuration
    MAX_RETRIES = 3
    RETRY_WAIT_MIN = 0.5  # seconds
    RETRY_WAIT_MAX = 2.0  # seconds
    GENERATION_TIMEOUT = 10.0  # seconds

    def __init__(
        self,
        conversation_manager: Optional[StandupConversationManager] = None,
        standup_workflow: Optional[Any] = None,
    ) -> None:
        """
        Initialize handler.

        Args:
            conversation_manager: State manager instance (creates new if None)
            standup_workflow: optional workflow instance (unused since #1289; assembly handled by StandupAssembler)
        """
        self.manager = conversation_manager or StandupConversationManager()
        self._workflow = standup_workflow

    async def handle_turn(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> ConversationResponse:
        """
        Handle a single conversation turn.

        Routes to appropriate handler based on current state.

        Issue #556 Phase 4: Adds performance monitoring with structured logging.

        Args:
            conversation: Current conversation
            user_message: User's message
            context: Optional additional context

        Returns:
            ConversationResponse with message and state
        """
        start_time = time.perf_counter()
        state = conversation.state
        turn_number = len(conversation.turns) + 1

        # State-based routing
        handlers = {
            StandupConversationState.INITIATED: self._handle_initiated,
            StandupConversationState.GATHERING_PREFERENCES: self._handle_gathering,
            StandupConversationState.GATHERING_YESTERDAY: self._handle_gathering_yesterday,
            StandupConversationState.GATHERING_TODAY: self._handle_gathering_today,
            StandupConversationState.GATHERING_BLOCKERS: self._handle_gathering_blockers,
            StandupConversationState.GENERATING: self._handle_generating,
            StandupConversationState.REFINING: self._handle_refining,
            StandupConversationState.FINALIZING: self._handle_finalizing,
        }

        handler = handlers.get(state)
        if not handler:
            response_time_ms = (time.perf_counter() - start_time) * 1000
            logger.info(
                "standup_turn_no_handler",
                conversation_id=conversation.id,
                state=state.value,
                response_time_ms=round(response_time_ms, 2),
            )
            return ConversationResponse(
                message="This conversation has ended. Start a new one with 'standup'.",
                state=state,
                requires_input=False,
            )

        response = await handler(conversation, user_message, context or {})
        response_time_ms = (time.perf_counter() - start_time) * 1000

        # Issue #556 Phase 4: Structured performance logging
        logger.info(
            "standup_turn_completed",
            conversation_id=conversation.id,
            turn_number=turn_number,
            from_state=state.value,
            to_state=response.state.value,
            response_time_ms=round(response_time_ms, 2),
            requires_input=response.requires_input,
            has_standup_content=response.standup_content is not None,
        )

        return response

    async def start_conversation(
        self,
        session_id: str,
        user_id: str,
        initial_context: Optional[Dict[str, Any]] = None,
    ) -> ConversationResponse:
        """
        Start a new standup conversation.

        Args:
            session_id: Session identifier
            user_id: User identifier
            initial_context: Optional context from integrations

        Returns:
            ConversationResponse with greeting and suggestions
        """
        conversation = await self.manager.create_conversation(
            session_id=session_id,
            user_id=user_id,
            initial_context=initial_context,
        )

        # Generate initial greeting based on available context
        greeting = await self._generate_greeting(conversation, initial_context or {})

        return ConversationResponse(
            message=greeting,
            state=conversation.state,
            requires_input=True,
            suggestions=["Yes, let's do it", "Quick standup", "Not now"],
        )

    async def _handle_initiated(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle INITIATED state - user just started.

        Issue #900 Phase 2: Default flow is now the 3-part structured
        collection (yesterday → today → blockers). Quick/fast/skip still
        bypasses to GENERATING for users who want a one-shot LLM standup.
        """
        message_lower = user_message.lower()

        # Quick/fast/skip → bypass guided collection, go straight to GENERATING
        if any(word in message_lower for word in ["quick", "fast", "skip", "just"]):
            await self.manager.transition_state(
                conversation.id, StandupConversationState.GENERATING
            )
            return await self._generate_standup(conversation, context)

        # Cancel
        if any(word in message_lower for word in ["no", "not now", "cancel", "later", "nope"]):
            await self.manager.transition_state(
                conversation.id, StandupConversationState.ABANDONED
            )
            return ConversationResponse(
                message="No problem! Just say 'standup' when you're ready.",
                state=StandupConversationState.ABANDONED,
                requires_input=False,
            )

        # Default — start the 3-part collection flow
        await self.manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_YESTERDAY
        )
        return ConversationResponse(
            message="What did you work on yesterday?",
            state=StandupConversationState.GATHERING_YESTERDAY,
            requires_input=True,
            suggestions=["nothing", "skip"],
        )

    async def _handle_gathering_yesterday(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Issue #900 Phase 2: Capture yesterday's items, advance to today.

        Phase 3: explicit/natural completion signals jump straight to
        GENERATING (skip the remaining parts).
        """
        capture = conversation.partial_capture or StandupPartialCapture()
        if not _is_skip_signal(user_message):
            capture.yesterday.extend(_parse_items_from_message(user_message))
        conversation = await self.manager.update_partial_capture(
            conversation.id, capture
        )

        signal = detect_completion(
            user_message=user_message,
            capture=capture,
            current_state=StandupConversationState.GATHERING_YESTERDAY,
        )
        if signal.is_complete:
            await self.manager.transition_state(
                conversation.id, StandupConversationState.GENERATING
            )
            return await self._generate_standup(conversation, context)

        await self.manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_TODAY
        )
        return ConversationResponse(
            message="What's planned for today?",
            state=StandupConversationState.GATHERING_TODAY,
            requires_input=True,
            suggestions=["nothing", "skip"],
        )

    async def _handle_gathering_today(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Issue #900 Phase 2: Capture today's items, advance to blockers.

        Phase 3: explicit/natural completion signals jump to GENERATING.
        """
        capture = conversation.partial_capture or StandupPartialCapture()
        if not _is_skip_signal(user_message):
            capture.today.extend(_parse_items_from_message(user_message))
        conversation = await self.manager.update_partial_capture(
            conversation.id, capture
        )

        signal = detect_completion(
            user_message=user_message,
            capture=capture,
            current_state=StandupConversationState.GATHERING_TODAY,
        )
        if signal.is_complete:
            await self.manager.transition_state(
                conversation.id, StandupConversationState.GENERATING
            )
            return await self._generate_standup(conversation, context)

        await self.manager.transition_state(
            conversation.id, StandupConversationState.GATHERING_BLOCKERS
        )
        return ConversationResponse(
            message="Any blockers or things you need help with?",
            state=StandupConversationState.GATHERING_BLOCKERS,
            requires_input=True,
            suggestions=["no blockers", "skip"],
        )

    async def _handle_gathering_blockers(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Issue #900 Phase 2: Capture blockers, transition to GENERATING.

        After capture, route through `_generate_standup` so the LLM
        produces the final standup using all 3 parts. Completion-detection
        rules don't change behavior here — blockers is the final gathering
        state, so we always advance.
        """
        capture = conversation.partial_capture or StandupPartialCapture()
        if not _is_skip_signal(user_message):
            capture.blockers.extend(_parse_items_from_message(user_message))
        conversation = await self.manager.update_partial_capture(conversation.id, capture)

        await self.manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        return await self._generate_standup(conversation, context)

    async def _handle_gathering(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle GATHERING_PREFERENCES state."""
        # Extract preferences from user message
        preferences = self._extract_preferences(user_message)
        await self.manager.update_preferences(conversation.id, preferences)

        # Move to generating
        await self.manager.transition_state(
            conversation.id, StandupConversationState.GENERATING
        )
        return await self._generate_standup(conversation, context)

    async def _handle_generating(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle GENERATING state - standup just generated."""
        # This shouldn't normally be called - generating is transient
        # But handle it by showing current standup
        if conversation.current_standup:
            await self.manager.transition_state(
                conversation.id, StandupConversationState.REFINING
            )
            return ConversationResponse(
                message=(
                    f"Here's your standup:\n\n{conversation.current_standup}\n\n"
                    "Would you like to make any changes?"
                ),
                state=StandupConversationState.REFINING,
                standup_content=conversation.current_standup,
                suggestions=["Looks good", "Add a blocker", "Remove something"],
            )

        return await self._generate_standup(conversation, context)

    async def _handle_refining(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle REFINING state - user providing feedback."""
        message_lower = user_message.lower()

        # Check for acceptance
        acceptance_words = [
            "good",
            "done",
            "looks good",
            "perfect",
            "yes",
            "ok",
            "fine",
            "great",
            "thanks",
        ]
        if any(word in message_lower for word in acceptance_words):
            await self.manager.transition_state(
                conversation.id, StandupConversationState.FINALIZING
            )
            return ConversationResponse(
                message=(
                    f"Great! Here's your final standup:\n\n{conversation.current_standup}\n\n"
                    "Would you like to share this or save your preferences for next time?"
                ),
                state=StandupConversationState.FINALIZING,
                standup_content=conversation.current_standup,
                suggestions=["Just copy it", "Save preferences", "Share with team"],
            )

        # Check for start over
        if "start over" in message_lower or "restart" in message_lower:
            await self.manager.transition_state(
                conversation.id, StandupConversationState.GENERATING
            )
            return await self._generate_standup(conversation, context)

        # Handle refinement request
        refined = await self._apply_refinement(conversation, user_message)
        return ConversationResponse(
            message=f"I've updated your standup:\n\n{refined}\n\nAnything else?",
            state=StandupConversationState.REFINING,
            standup_content=refined,
            suggestions=["Looks good", "More changes", "Start over"],
        )

    async def _handle_finalizing(
        self,
        conversation: StandupConversation,
        user_message: str,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Handle FINALIZING state - confirming completion."""
        await self.manager.transition_state(
            conversation.id, StandupConversationState.COMPLETE
        )
        return ConversationResponse(
            message="Your standup is ready! Have a great day!",
            state=StandupConversationState.COMPLETE,
            standup_content=conversation.current_standup,
            requires_input=False,
        )

    async def _generate_standup(
        self,
        conversation: StandupConversation,
        context: Dict[str, Any],
    ) -> ConversationResponse:
        """Generate standup content using workflow.

        Issue #556: Enhanced with retry logic, timeout handling, and monitoring.
        - Retries transient failures up to MAX_RETRIES times
        - Times out after GENERATION_TIMEOUT seconds
        - Falls back to basic template on persistent failures
        - Logs generation timing and success/failure metrics (Phase 4)

        Issue #900 Phase 5: When a 3-part `partial_capture` is non-empty,
        render the standup directly from captured StandupItems — the user
        has already authored the content, no LLM round-trip needed. The
        legacy LLM-workflow path remains for the quick/skip bypass and
        for installations without a partial capture.
        """
        generation_start = time.perf_counter()
        used_workflow = False
        used_fallback = False
        used_capture = False

        try:
            capture = conversation.partial_capture
            if capture is not None and not capture.is_empty():
                # 3-part flow: user-authored content, render directly.
                standup_content = _format_standup_from_capture(capture)
                used_capture = True
            elif self._workflow:
                # Legacy LLM workflow path (quick/skip bypass)
                standup_content = await self._generate_with_retry(context)
                used_workflow = True
            else:
                # Fallback to basic generation
                standup_content = self._generate_basic_standup(context)

            generation_time_ms = (time.perf_counter() - generation_start) * 1000

            # Issue #556 Phase 4: Log generation success metrics
            logger.info(
                "standup_generation_success",
                conversation_id=conversation.id,
                generation_time_ms=round(generation_time_ms, 2),
                used_workflow=used_workflow,
                used_capture=used_capture,
                content_length=len(standup_content),
                target_met=generation_time_ms < 500,
            )

            await self.manager.set_standup_content(conversation.id, standup_content)
            await self.manager.transition_state(
                conversation.id, StandupConversationState.REFINING
            )

            return ConversationResponse(
                message=(
                    f"Here's your standup:\n\n{standup_content}\n\n"
                    "Would you like to make any changes?"
                ),
                state=StandupConversationState.REFINING,
                standup_content=standup_content,
                suggestions=["Looks good", "Add a blocker", "Focus on something else"],
            )

        except Exception as e:
            generation_time_ms = (time.perf_counter() - generation_start) * 1000

            # Issue #556 Phase 4: Log generation failure metrics
            logger.error(
                "standup_generation_failed",
                conversation_id=conversation.id,
                error=str(e),
                error_type=type(e).__name__,
                generation_time_ms=round(generation_time_ms, 2),
                used_fallback=True,
            )
            return await self._graceful_fallback(conversation, str(e))

    async def _generate_with_retry(self, context: Dict[str, Any]) -> str:
        """Generate standup with retry logic and timeout.

        Issue #556: Reliability enhancement with monitoring (Phase 4).
        - Uses exponential backoff for retries
        - Times out to prevent hanging on slow services
        - Categorizes errors for retry decisions
        - Logs retry metrics for monitoring
        """
        retry_start = time.perf_counter()
        total_attempts = 0

        async def _attempt_generation() -> str:
            """Single attempt at standup generation."""
            try:
                # Apply timeout to the workflow call
                result = await asyncio.wait_for(
                    self._workflow.generate_standup(
                        mode="standard",
                        context=context,
                    ),
                    timeout=self.GENERATION_TIMEOUT,
                )
                return result.summary if hasattr(result, "summary") else str(result)
            except asyncio.TimeoutError:
                logger.warning(
                    "standup_generation_timeout",
                    timeout=self.GENERATION_TIMEOUT,
                    error_type="transient",
                )
                raise TransientError("Generation timed out")
            except ConnectionError as e:
                logger.warning(
                    "standup_generation_connection_error",
                    error=str(e),
                    error_type="transient",
                )
                raise TransientError(str(e))
            except Exception as e:
                # Categorize the error
                error_msg = str(e).lower()
                if any(
                    keyword in error_msg
                    for keyword in ["rate limit", "timeout", "connection", "network"]
                ):
                    raise TransientError(str(e))
                # Permanent errors don't retry
                raise PermanentError(str(e))

        # Use tenacity for retry with exponential backoff
        try:
            async for attempt in AsyncRetrying(
                stop=stop_after_attempt(self.MAX_RETRIES),
                wait=wait_exponential(
                    multiplier=1,
                    min=self.RETRY_WAIT_MIN,
                    max=self.RETRY_WAIT_MAX,
                ),
                retry=retry_if_exception_type(TransientError),
                reraise=True,
            ):
                with attempt:
                    total_attempts = attempt.retry_state.attempt_number
                    logger.debug(
                        "standup_generation_attempt",
                        attempt_number=total_attempts,
                        max_attempts=self.MAX_RETRIES,
                    )
                    result = await _attempt_generation()

                    # Issue #556 Phase 4: Log retry success metrics
                    if total_attempts > 1:
                        retry_time_ms = (time.perf_counter() - retry_start) * 1000
                        logger.info(
                            "standup_generation_retry_success",
                            attempts_used=total_attempts,
                            total_retry_time_ms=round(retry_time_ms, 2),
                        )

                    return result

        except RetryError as e:
            # All retries exhausted
            retry_time_ms = (time.perf_counter() - retry_start) * 1000
            logger.error(
                "standup_generation_retries_exhausted",
                retries=self.MAX_RETRIES,
                total_retry_time_ms=round(retry_time_ms, 2),
                last_error=str(e.last_attempt.exception()),
                error_type=type(e.last_attempt.exception()).__name__,
            )
            raise e.last_attempt.exception()
        except PermanentError as e:
            # Don't retry permanent errors - log for monitoring
            logger.warning(
                "standup_generation_permanent_error",
                error=str(e),
                error_type="permanent",
                attempts_before_fail=total_attempts,
            )
            raise

        # Should not reach here, but return empty string as safety
        return ""

    async def _generate_greeting(
        self,
        conversation: StandupConversation,
        context: Dict[str, Any],
    ) -> str:
        """Generate context-aware greeting."""
        # Basic greeting - can be enhanced with calendar/GitHub context
        return "Good morning! Ready for your standup?"

    def _extract_preferences(self, message: str) -> Dict[str, Any]:
        """Extract preferences from user message."""
        preferences: Dict[str, Any] = {}
        message_lower = message.lower()

        if "github" in message_lower:
            preferences["focus"] = "github"
        elif "calendar" in message_lower:
            preferences["focus"] = "calendar"
        elif "todos" in message_lower or "tasks" in message_lower:
            preferences["focus"] = "todos"

        if "brief" in message_lower or "short" in message_lower:
            preferences["length"] = "brief"
        elif "detailed" in message_lower or "comprehensive" in message_lower:
            preferences["length"] = "detailed"

        return preferences

    async def _apply_refinement(
        self,
        conversation: StandupConversation,
        user_message: str,
    ) -> str:
        """Apply user refinement to standup content."""
        current = conversation.current_standup or ""
        message_lower = user_message.lower()

        # Handle add blocker
        if "add" in message_lower and "blocker" in message_lower:
            # Extract blocker text - remove the "add blocker" prefix
            blocker_text = user_message
            for prefix in ["add blocker", "add a blocker", "add blocker:"]:
                if prefix in message_lower:
                    start_idx = message_lower.find(prefix) + len(prefix)
                    blocker_text = user_message[start_idx:].strip()
                    break

            if blocker_text:
                if "*Blockers:*" in current:
                    # Find the Blockers section and add to it
                    refined = current.replace("*Blockers:*\n", f"*Blockers:*\n* {blocker_text}\n")
                else:
                    # Add a Blockers section
                    refined = current + f"\n\n*Blockers:*\n* {blocker_text}"
                await self.manager.set_standup_content(conversation.id, refined)
                return refined

        # Handle remove request
        if "remove" in message_lower:
            # Extract what to remove
            remove_target = user_message
            for prefix in ["remove", "remove the", "delete"]:
                if prefix in message_lower:
                    start_idx = message_lower.find(prefix) + len(prefix)
                    remove_target = user_message[start_idx:].strip().lower()
                    break

            # Try to remove matching lines
            lines = current.split("\n")
            filtered_lines = [line for line in lines if remove_target not in line.lower()]
            refined = "\n".join(filtered_lines)
            await self.manager.set_standup_content(conversation.id, refined)
            return refined

        # Handle focus request
        if "focus on" in message_lower:
            focus_target = message_lower.split("focus on")[-1].strip()
            preferences = {"focus": focus_target}
            await self.manager.update_preferences(conversation.id, preferences)
            # For now, just note the preference - would regenerate with focus
            return current

        # Default - return current content unchanged
        return current

    def _generate_basic_standup(self, context: Dict[str, Any]) -> str:
        """Generate basic standup when workflow unavailable."""
        return """*Yesterday:*
* Made progress on assigned tasks

*Today:*
* Continue current work items
* Review any blockers

*Blockers:*
* None at this time"""

    async def _graceful_fallback(
        self,
        conversation: StandupConversation,
        error: str,
    ) -> ConversationResponse:
        """Handle graceful fallback when generation fails."""
        basic = self._generate_basic_standup({})
        await self.manager.set_standup_content(conversation.id, basic)
        await self.manager.transition_state(
            conversation.id, StandupConversationState.REFINING
        )

        return ConversationResponse(
            message=(
                f"Here's a basic standup template:\n\n{basic}\n\n"
                "You can customize it to fit your day."
            ),
            state=StandupConversationState.REFINING,
            standup_content=basic,
            suggestions=["Looks good", "Let me customize", "Try again"],
            metadata={"fallback": True, "error": error},
        )
