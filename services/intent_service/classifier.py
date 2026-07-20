"""
PM-039 Action Normalization/Unification

- All document/file search actions (find_documents, search_files, etc.) are normalized to 'search_documents'.
- This ensures robust, maintainable, and unified handling of all search intents.
- See tests/test_intent_coverage_pm039.py for comprehensive coverage and scenarios.
"""

# services/intent_service/classifier.py
import json
import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

import structlog

from services.api.errors import (
    IntentClassificationFailedError,
    LowConfidenceIntentError,
    NoRelevantKnowledgeError,
)
from services.api.serializers import intent_to_dict
from services.domain.models import Intent, IntentCategory

# GREAT-4B Phase 3: Intent caching
from services.intent_service.cache import IntentCache

# Conversation context (Issue #427)
from services.intent_service.conversation_context import (
    ConversationContext,
    detect_follow_up,
    extract_temporal_reference,
    extract_topic,
    get_or_create_context,
    resolve_follow_up,
)

# --- Add fuzzy matcher import ---
from services.intent_service.fuzzy_matcher import correct_common_typos, fuzzy_match
from services.intent_service.honest_failure import (
    HonestFailureHandler,
    create_graceful_error_response,
)
from services.intent_service.intent_hooks import IntentProcessingHooks

# Grammar-conscious classification components (Issue #619)
from services.intent_service.intent_types import IntentClassificationContext, IntentUnderstanding

# Lens inference (#763 GLUE-FOLLOWUP)
from services.intent_service.lens_inference import (
    decode_follow_up_with_llm,
    extract_lens_from_intent,
    is_lens_reset,
    should_try_llm_decoder,
)
from services.intent_service.personality_bridge import PersonalityBridge
from services.intent_service.place_detector import PlaceDetector
from services.intent_service.pre_classifier import MultiIntentResult, PreClassifier
from services.intent_service.preference_handler import PreferenceDetectionHandler
from services.intent_service.prompts import INTENT_CLASSIFICATION_PROMPT
from services.intent_service.warmth_calibration import WarmthCalibrator
from services.knowledge_graph import get_ingester

# Orientation system (Issue #410)
from services.mux.orientation import ChannelType, OrientationState, TrustContext

# Recognition system (Issue #411) - late import to avoid circular dependency
# RecognitionTrigger and create_recognition_understanding are imported in __init__
from shared.events import EventBus

logger = structlog.get_logger()


# --- B3: pre-classifier referent resolution (#1394 / ADR-078 D2) ---------------
# Resolve a follow-up like "change the title" → the issue created earlier this
# session, so it routes to update_issue instead of the document/Notion handler.
# DETERMINISTIC (OQ-2, Arch-ruled) + CONSERVATIVE: the issue-field-word
# requirement below IS the N2 over-resolution guard — "the roadmap needs work"
# carries no field word, so it never resolves. Only a high-confidence referent
# resolves; everything else passes through untouched.

# The fields _handle_update_issue accepts — presence of one of these is what
# makes a "the X"/"it" a resolvable ISSUE referent (not an arbitrary topic).
_ISSUE_FIELD_WORDS = r"title|body|description|label|labels|assignee|assignees|state"
# Verbs that modify an existing issue (create/close/reopen are their own handlers).
_UPDATE_VERB = r"change|update|rename|edit|modify|set|add"
# An explicit issue number already present → nothing to resolve; let normal routing run.
_EXPLICIT_ISSUE_RE = re.compile(r"#\d+|\bissue\s+\d+\b", re.IGNORECASE)
# "change the title", "update the label", "set the body"
_FIELD_REFERENT_RE = re.compile(
    rf"\b({_UPDATE_VERB})\b.*\bthe\s+({_ISSUE_FIELD_WORDS})\b", re.IGNORECASE
)
# "add a label … to it", "change … it/that" with a field word present
_PRONOUN_REFERENT_RE = re.compile(
    rf"\b({_UPDATE_VERB})\b.*\b({_ISSUE_FIELD_WORDS})\b.*\b(it|that)\b", re.IGNORECASE
)


def _detect_issue_referent(message: str) -> bool:
    """True iff the message is an issue-update follow-up with an UNRESOLVED referent
    (an issue-field edit with no explicit issue number). Deterministic + conservative:
    requires an update verb AND an issue-field word — the field-word requirement is the
    N2 guard (a fresh definite-article topic without a field word never matches)."""
    if not message:
        return False
    if _EXPLICIT_ISSUE_RE.search(message):
        return False  # explicit issue # present → nothing to resolve
    return bool(_FIELD_REFERENT_RE.search(message) or _PRONOUN_REFERENT_RE.search(message))


class IntentClassifier:
    def __init__(
        self,
        llm_service=None,
        event_bus: Optional[EventBus] = None,
        knowledge_graph_service=None,  # Issue #278: Graph-first retrieval
    ):
        """
        Initialize IntentClassifier.

        Args:
            llm_service: LLM service instance (optional, will get from container if not provided)
            event_bus: Event bus for classifier events
            knowledge_graph_service: Knowledge graph service for context (optional, Issue #278)
        """
        self._llm = llm_service  # Accept via dependency injection
        self.event_bus = event_bus
        self.knowledge_graph_service = knowledge_graph_service  # Issue #278
        self.knowledge_hierarchy = [
            "pm_fundamentals",  # Your book, PM best practices
            "business_context",  # Client/domain specific
            "product_context",  # Specific product details
            "task_context",  # Current task specifics
        ]
        # GREAT-4B Phase 3: Initialize cache with 1-hour TTL
        self.cache = IntentCache(ttl=3600)
        logger.info("IntentCache integrated with classifier", ttl_seconds=3600)

        # Issue #248: Initialize preference detection handler and hooks
        self.preference_handler = PreferenceDetectionHandler()
        self.hooks = IntentProcessingHooks(self.preference_handler)
        logger.info("Preference detection hooks initialized for #248")

        # Issue #619: Grammar-conscious classification components
        self.place_detector = PlaceDetector()
        self.personality_bridge = PersonalityBridge()
        self.warmth_calibrator = WarmthCalibrator()
        self.failure_handler = HonestFailureHandler(self.warmth_calibrator)
        logger.info("Grammar-conscious classification components initialized (#619)")

        # Issue #411: Recognition trigger for low-confidence handling
        # Late import to avoid circular dependency with intent_types
        from services.mux.recognition_trigger import RecognitionTrigger

        self.recognition_trigger = RecognitionTrigger()
        logger.info("Recognition trigger initialized (#411)")

    @property
    def llm(self):
        """Lazy-load LLM service from ServiceContainer if not injected.

        DEPRECATION WARNING (Issue #322):
        Direct ServiceContainer() access is deprecated. Pass llm_service
        via constructor instead. This fallback will be removed when
        horizontal scaling is enabled.
        """
        if self._llm is None:
            import warnings

            from services.container import ServiceContainer

            warnings.warn(
                "IntentClassifier: Direct ServiceContainer() access is deprecated. "
                "Pass llm_service via constructor. (Issue #322 - ARCH-FIX-SINGLETON)",
                DeprecationWarning,
                stacklevel=2,
            )
            container = ServiceContainer()
            self._llm = container.get_service("llm")
        return self._llm

    @staticmethod
    async def _resolve_issue_referent(
        message: str, user_id: Optional[str], session_id: Optional[str]
    ) -> Optional[Intent]:
        """B3 (#1394 / ADR-078 D2/OQ-3) — resolve an issue-update follow-up against the
        session-activity ledger and EMIT the resolved ``update_issue`` intent directly.

        Emit-directly (OQ-3, Arch-ruled): since detection is deterministic, we hand the
        classifier a self-contained resolved intent rather than a rewritten string to
        re-classify — the create_issue-duplicate hazard is then impossible by construction
        (N3). D4 held: the LLM classifier is never consulted for the resolved path.

        Guards:
        - N1 (no-referent / empty ledger): returns None → caller falls through unchanged.
        - N2 (fresh topic): _detect_issue_referent already declined (no issue-field word).
        - D1a: reads the ledger owner-scoped; with no principal/session, returns None
          (never an unscoped read).
        Returns the emitted Intent, or None to pass through to normal classification.
        """
        if not user_id or not session_id:
            return None  # D1a: no owner-scoped read possible → don't resolve
        if not _detect_issue_referent(message):
            return None  # N2 / not a follow-up referent
        # Owner-scoped ledger read (B4's reader) — most recent creation this session.
        from services.database.repositories import SessionActivityRepository
        from services.database.session_factory import AsyncSessionFactory

        try:
            async with AsyncSessionFactory.session_scope() as session:
                activities = await SessionActivityRepository(session).list_for_session(
                    owner_id=str(user_id), conversation_id=str(session_id)
                )
        except Exception as e:
            logger.warning("b3_ledger_read_failed", error=str(e))
            return None  # degrade to pass-through, never block classification
        # N1: nothing created this session → don't fabricate a target.
        latest_issue = next(
            (a for a in activities if a.action_type == "issue_created"), None
        )
        if latest_issue is None:
            return None
        # target_ref is "owner/repo#107" — split into the fields the handler reads.
        ref = latest_issue.target_ref or ""
        if "#" not in ref:
            return None
        repository, _, num = ref.rpartition("#")
        if not repository or not num.isdigit():
            return None
        logger.info(
            "b3_referent_resolved",
            session_id=session_id,
            resolved_ref=ref,
            action="update_issue",
        )
        return Intent(
            original_message=message,  # RAW preserved (#1332) — audit + slot-fill source
            category=IntentCategory.QUERY,  # matches update_issue's registry category
            action="update_issue",
            confidence=1.0,
            context={
                "original_message": message,  # handler slot-fills the new title from this
                "repository": repository,
                "issue_number": int(num),
                "b3_resolved": True,  # provenance: this referent was ledger-resolved
            },
        )

    async def classify(
        self,
        message: str,
        context: Optional[Dict] = None,
        session: Optional[Any] = None,
        spatial_context: Optional[Dict] = None,
        use_cache: bool = True,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> Intent:
        """
        Classify user intent with optional caching.

        Args:
            message: User input text
            context: Optional context dict
            session: Optional session object
            spatial_context: Optional spatial context
            use_cache: Whether to use cache (default True). Caching only applies
                      to simple message-only classifications without context.
            user_id: Optional resolved principal (ADR-075 D4) — scopes the
                classification system prompt to this user's personalization
                rather than the unscoped file, when provided.

        Returns:
            Intent object with classification results
        """
        # Stage 0: B3 referent resolution (#1394 / ADR-078 D2) — BEFORE the cache,
        # pre_classify, and the LLM. Resolves "change the title" → the issue created
        # THIS session and emits update_issue directly (owner-scoped ledger read;
        # async, which is why it can't live in the sync PreClassifier). Passes through
        # untouched when there's no high-confidence referent (N1/N2). D4 held: the
        # classifier never sees history — session_id is the ledger-scoping KEY, not
        # history, and arrives as its own kwarg so it never touches the LLM prompt
        # or the cache key. ABOVE the cache because referent messages are
        # session-relative: serving "change the title" from a cross-session cache
        # entry would bypass resolution by construction.
        b3_intent = await self._resolve_issue_referent(message, user_id, session_id)
        if b3_intent is not None:
            logger.info(
                "intent_classification",
                source="B3_REFERENT_RESOLUTION",
                action=b3_intent.action,
                message_preview=message[:50],
            )
            return b3_intent

        # GREAT-4B Phase 3: Check cache for simple message-only queries
        # Only cache when no context/session/spatial_context (to keep cache simple)
        cache_eligible = use_cache and not context and not session and not spatial_context

        if cache_eligible:
            # Try cache first
            cached_result = self.cache.get(message)
            if cached_result is not None:
                logger.info(
                    "intent_from_cache",
                    message_preview=message[:50],
                    action=cached_result.get("action"),
                )
                # Reconstruct Intent object from cached dict
                intent_obj = Intent(
                    original_message=message,  # #1332/#1220: attribute was never set — see classify docstring note
                    category=IntentCategory(cached_result["category"]),
                    action=cached_result["action"],
                    confidence=cached_result.get("confidence", 1.0),
                    context=cached_result.get("context", {}),
                )
                # Add optional attributes if they exist
                if "entities" in cached_result:
                    intent_obj.entities = cached_result["entities"]
                if "learning_signals" in cached_result:
                    intent_obj.learning_signals = cached_result["learning_signals"]

                # Issue #248: Run preference detection hooks for cached intents too
                user_id = (context or {}).get("user_id")
                session_id = context.get("session_id") if context else None
                if user_id:
                    try:
                        pref_result = await self.hooks.on_intent_classified(
                            user_id=user_id,
                            message=message,
                            intent=intent_obj,
                            session_id=session_id,
                        )
                        if pref_result.get("preferences"):
                            intent_obj.preferences = pref_result["preferences"]
                    except Exception as e:
                        logger.error(f"Preference detection hook failed for cached intent: {e}")

                return intent_obj

        # Stage 1: Pre-classification
        pre_intent = PreClassifier.pre_classify(message)
        if pre_intent:
            # #1332/#1220 completion (found via #1417, 2026-07-16): the
            # pre-classifier's ~31 emission sites set only
            # context["original_message"] — the Intent FIELD stayed "" through
            # this handoff, so every field-reading consumer downstream
            # (e.g. _detect_setup_request's canonical-gate) saw an empty
            # message and mis-routed pre-classified intents to the floor.
            # Normalize once here, mirroring the cache-reconstruction fix.
            if not pre_intent.original_message:
                pre_intent.original_message = message
            logger.info(
                "intent_classification",
                source="PRE_CLASSIFIER",
                action=pre_intent.action,
                message_length=len(message),
                message_preview=message[:50],
            )  # First 50 chars for debugging

            # GREAT-4B Phase 3: Cache pre-classifier results too
            if cache_eligible:
                cache_data = {
                    "category": pre_intent.category.value,
                    "action": pre_intent.action,
                    "confidence": pre_intent.confidence,
                    "context": pre_intent.context or {},
                    "entities": getattr(pre_intent, "entities", {}),
                    "learning_signals": getattr(pre_intent, "learning_signals", []),
                }
                self.cache.set(message, cache_data)
                logger.debug("intent_cached_preclassifier", message_preview=message[:50])

            return pre_intent

        # Stage 2: LLM classification
        logger.info(
            "intent_classification_attempt",
            source="LLM",
            message_length=len(message),
            message_preview=message[:50],
        )

        # Issue #278: Get graph context for improved classification
        graph_context = {}
        user_id = (context or {}).get("user_id")
        if user_id:
            graph_context = await self._get_graph_context(message, user_id)

        # Check for file references
        has_file_reference = PreClassifier.detect_file_reference(message)

        # Prepare file context
        file_context = ""
        if session and has_file_reference:
            recent_files = session.get_recent_files()
            if recent_files:
                file_context = f"Recent uploads: {[f['filename'] for f in recent_files]}"

        # Capture input context for learning
        classification_context = {
            "message": message,
            "timestamp": datetime.now().isoformat(),
            "available_knowledge": self._assess_available_knowledge(context),
            "user_context": context or {},
            "has_file_reference": has_file_reference,
            "file_context": file_context,
            "spatial_context": spatial_context or {},
            "graph_context": graph_context,  # Issue #278: Include graph context
        }

        try:
            # Perform classification with confidence scoring
            intent, reasoning = await self._classify_with_reasoning(
                message, context, file_context, spatial_context, user_id
            )

            # --- ACTION NORMALIZATION ---
            action_normalization_map = {
                "find_specifications": "search_documents",
                "find_documentation": "search_documents",
                "list_project_plans": "search_documents",
                "list_documents": "search_documents",
                "search_requirements": "search_documents",
                "get_documents": "search_documents",
                "locate_documentation": "search_documents",
                "find_documents": "search_documents",
                "search_files": "search_documents",
                "find_requirements": "search_documents",
                "find_files": "search_documents",
                "find_docs": "search_documents",
                "search_docs": "search_documents",
                "search_documents": "search_documents",  # idempotent
                # Document analysis intents (Issue #290)
                "analyze": "analyze_document",
                "analyze_document": "analyze_document",  # idempotent
                "summarize": "summarize_document",
                "summarize_document": "summarize_document",  # idempotent
                "what_does": "qa_document",
                "question_document": "qa_document",
                "qa_document": "qa_document",  # idempotent
                "compare": "compare_documents",
                "compare_documents": "compare_documents",  # idempotent
            }
            if intent.action in action_normalization_map:
                logger.info(
                    "action_normalization",
                    original_action=intent.action,
                    normalized_action=action_normalization_map[intent.action],
                )
                intent.action = action_normalization_map[intent.action]

            # Check for truly vague intents that need clarification
            # Lower confidence threshold to avoid overriding legitimate classifications
            if intent.confidence < 0.3 or self._seems_vague(intent):
                logger.info("Low confidence or vague intent detected, requesting clarification")
                return Intent(
                    original_message=message,  # #1332/#1220
                    category=IntentCategory.CONVERSATION,
                    action="clarification_needed",
                    confidence=intent.confidence,
                    context={
                        "original_classification": intent_to_dict(intent),
                        "trigger": (
                            "low_confidence" if intent.confidence < 0.3 else "vague_pattern"
                        ),
                    },
                )

            # Identify learning opportunities
            intent.learning_signals = self._identify_learning_signals(message, intent, reasoning)

            # Emit event for future learning system if event bus is available
            if self.event_bus:
                await self.event_bus.emit(
                    "intent.classified",
                    {
                        "intent_id": intent.id,
                        "classification_context": classification_context,
                        "intent": intent_to_dict(intent),
                        "reasoning": reasoning,
                        "learning_signals": intent.learning_signals,
                    },
                )

            # After successful LLM classification
            logger.info(
                "intent_classification",
                source="LLM",
                action=intent.action,
                message_length=len(message),
                confidence=intent.confidence,
            )

            # GREAT-4B Phase 3: Cache the result if cache-eligible
            if cache_eligible:
                cache_data = {
                    "category": intent.category.value,
                    "action": intent.action,
                    "confidence": intent.confidence,
                    "context": intent.context or {},
                    "entities": getattr(intent, "entities", {}),
                    "learning_signals": getattr(intent, "learning_signals", []),
                }
                self.cache.set(message, cache_data)
                logger.debug("intent_cached", message_preview=message[:50])

            # Issue #248: Run preference detection hooks (async, non-blocking)
            user_id = (context or {}).get("user_id")
            session_id = context.get("session_id") if context else None
            if user_id:
                try:
                    pref_result = await self.hooks.on_intent_classified(
                        user_id=user_id,
                        message=message,
                        intent=intent,
                        session_id=session_id,
                    )
                    # Attach preferences to intent for passing to response generation
                    if pref_result.get("preferences"):
                        intent.preferences = pref_result["preferences"]
                except Exception as e:
                    logger.error(f"Preference detection hook failed: {e}")
                    # Don't fail classification if hook fails

            return intent

        except LowConfidenceIntentError:
            # Re-raise to be caught by the middleware
            raise
        except Exception as e:
            logger.error(f"Classification failed: {e}", exc_info=True)
            # Raise a structured error instead of falling back
            raise IntentClassificationFailedError(details={"original_error": str(e)})

    async def classify_conscious(
        self,
        message: str,
        context: Optional[Dict] = None,
        session: Optional[Any] = None,
        spatial_context: Optional[Dict] = None,
        use_cache: bool = True,
        user_id: Optional[str] = None,
    ) -> IntentUnderstanding:
        """
        Grammar-conscious intent classification (Issue #619).

        This method returns IntentUnderstanding instead of raw Intent,
        providing experiential framing of Piper's understanding.

        For backward compatibility, use classify() which returns Intent.
        New code should prefer this method for richer responses.

        Integration point (Issue #410, Arch Decision 2026-01-23):
        Request → PlaceDetector → OrientationState.gather() → IntentClassifier → Handler

        Args:
            message: User input text
            context: Optional context dict
            session: Optional session object
            spatial_context: Optional spatial context
            use_cache: Whether to use cache (default True)

        Returns:
            IntentUnderstanding with Piper's experiential understanding
        """
        # Detect Place first
        place, place_settings = self.place_detector.detect_with_settings(spatial_context)

        # Issue #410: Gather orientation after PlaceDetector, before classification
        # This is Piper perceiving the current Situation through multiple lenses
        orientation = self._gather_orientation(
            context=context,
            place=place,
            spatial_context=spatial_context,
        )

        # Build rich classification context
        classification_context = IntentClassificationContext.from_classify_args(
            message=message,
            context=context,
            spatial_context=spatial_context,
            place=place,
        )

        # Attach orientation to classification context for downstream use
        classification_context.orientation = orientation

        # Issue #427: Get or create conversation context for follow-up detection
        session_id = context.get("session_id") if context else None
        conv_context: Optional[ConversationContext] = None
        if session_id:
            conv_context = get_or_create_context(session_id)
            classification_context.conversation_context = conv_context

        try:
            # Issue #427: Check for conversational follow-up before LLM classification
            # This enables "How about today?" after asking about tomorrow
            intent: Optional[Intent] = None
            if conv_context and conv_context.is_active:
                follow_up_result = detect_follow_up(message, conv_context)
                if follow_up_result:
                    follow_up_type, extracted_data = follow_up_result
                    resolved_intent = resolve_follow_up(
                        follow_up_type, extracted_data, conv_context
                    )
                    if resolved_intent:
                        logger.info(
                            "follow_up_resolved",
                            follow_up_type=follow_up_type.value,
                            resolved_action=resolved_intent.action,
                            inherited_from=(
                                str(conv_context.last_turn.id) if conv_context.last_turn else None
                            ),
                        )
                        intent = resolved_intent

            # #763 Phase 3: If rules didn't match but lens is active,
            # try the LLM decoder for complex follow-ups
            if intent is None and conv_context:
                current_lens = conv_context.current_lens
                if should_try_llm_decoder(message, current_lens):
                    decoded = await decode_follow_up_with_llm(
                        message=message,
                        turns=conv_context.turns,
                        current_lens=current_lens,
                        llm_service=self.llm,
                    )
                    if decoded:
                        logger.info(
                            "follow_up_llm_decoded",
                            action=decoded.action,
                            lens=decoded.context.get("inherited_lens"),
                        )
                        intent = decoded

            # If not a follow-up, use existing classify() for the raw Intent
            if intent is None:
                intent = await self.classify(
                    message=message,
                    context=context,
                    session=session,
                    spatial_context=spatial_context,
                    use_cache=use_cache,
                    user_id=user_id,
                )

            # Issue #427: Record this turn in conversation context
            if conv_context:
                temporal_ref = extract_temporal_reference(message)
                topic = extract_topic(message, intent)

                # #763: Extract lens — for follow-ups, inherit from context;
                # for new queries, infer from the classified intent
                lens = intent.context.get("inherited_lens") or extract_lens_from_intent(intent)

                # #763 Phase 4: Detect lens reset (explicit topic change)
                if is_lens_reset(lens, conv_context.current_lens, intent):
                    conv_context.reset_lens()
                elif lens and conv_context.current_lens and lens != conv_context.current_lens:
                    # #827: Lens changed but NOT a reset — this is a sub-topic
                    # digression (e.g., calendar → "who's attending?" → people lens).
                    # Check if the new lens matches a previous stack entry (returning
                    # from digression) or is a new digression (push current lens).
                    if lens in conv_context.lens_stack:
                        # Returning to a previous topic — pop back to it
                        while conv_context.lens_stack and conv_context.lens_stack[-1] != lens:
                            conv_context.pop_lens()
                        # Pop the matching entry itself (it becomes current via add_turn)
                        conv_context.pop_lens()
                    else:
                        # New sub-topic digression — save current lens for later
                        conv_context.push_lens(lens)

                conv_context.add_turn(
                    message=message,
                    intent=intent,
                    temporal_reference=temporal_ref,
                    topic=topic,
                    lens=lens,
                )

            # Issue #411: Check for recognition opportunity before failure handling
            # Recognition fills the gap between confident action and honest failure
            # by offering contextual options when confidence is moderate
            recognition_result = self.recognition_trigger.evaluate(
                intent=intent,
                context=classification_context,
                channel=self._get_channel_type(spatial_context),
                trust_stage=self._get_trust_stage(context),
            )

            if recognition_result.should_trigger:
                logger.debug(
                    "Recognition triggered",
                    confidence=intent.confidence,
                    options_count=(
                        recognition_result.recognition_options.options
                        if recognition_result.recognition_options
                        else 0
                    ),
                    reason=recognition_result.reason,
                )
                # Late import to avoid circular dependency
                from services.mux.recognition_trigger import create_recognition_understanding

                return create_recognition_understanding(
                    intent=intent,
                    context=classification_context,
                    recognition_options=recognition_result.recognition_options,
                    formatted_response=recognition_result.formatted_response,
                )

            # Check for low confidence - handle specially (below recognition threshold)
            if intent.confidence < 0.35:
                return self.failure_handler.handle_low_confidence(
                    intent=intent,
                    context=classification_context,
                    place_settings=place_settings,
                )

            # Check for vague intent
            if self._seems_vague(intent):
                return self.failure_handler.handle_vague_intent(
                    intent=intent,
                    context=classification_context,
                    place_settings=place_settings,
                )

            # Transform to grammar-conscious understanding
            understanding = self.personality_bridge.transform(
                intent=intent,
                context=classification_context,
                place_settings=place_settings,
            )

            # Record for pattern detection
            if classification_context.user_id:
                self.personality_bridge.record_intent(
                    classification_context.user_id,
                    intent.action,
                )

            return understanding

        except Exception as e:
            logger.error(f"Grammar-conscious classification failed: {e}", exc_info=True)
            # Return graceful failure instead of raising
            return create_graceful_error_response(
                context=classification_context,
                place_settings=place_settings,
                error=e,
            )

    def _gather_orientation(
        self,
        context: Optional[Dict] = None,
        place: Optional[Any] = None,
        spatial_context: Optional[Dict] = None,
    ) -> Optional[OrientationState]:
        """
        Gather Piper's orientation state.

        Issue #410: This is Piper perceiving the current Situation
        through multiple lenses (Identity, Temporal, Spatial, Agency, Prediction).

        Integration point per Arch Decision 2026-01-23:
        After PlaceDetector, before IntentClassifier.

        Args:
            context: Request context dict
            place: Detected InteractionSpace
            spatial_context: Spatial context dict

        Returns:
            OrientationState or None if gathering fails
        """
        try:
            # Gather orientation from available context
            # Note: ConsciousnessContext and UserContext would be passed
            # from higher layers when available. For now, we gather what we can.
            orientation = OrientationState.gather(
                place=place,
                # Future: pass user_context, consciousness_context, trust_context
                # These will be wired in as the integration matures
            )

            logger.debug(
                "orientation_gathered",
                place=str(place) if place else None,
                identity_confidence=orientation.identity.confidence,
                temporal_confidence=orientation.temporal.confidence,
                spatial_confidence=orientation.spatial.confidence,
            )

            return orientation

        except Exception as e:
            # Orientation is supplementary - don't fail classification if it fails
            logger.warning(f"Orientation gathering failed (non-fatal): {e}")
            return None

    def _get_channel_type(
        self,
        spatial_context: Optional[Dict] = None,
    ) -> ChannelType:
        """
        Determine channel type from spatial context.

        Issue #411: Channel affects recognition formatting.

        Args:
            spatial_context: Spatial context dict

        Returns:
            ChannelType for current request
        """
        if not spatial_context:
            return ChannelType.WEB

        channel = spatial_context.get("channel", "").lower()

        if channel == "slack":
            return ChannelType.SLACK
        elif channel == "cli":
            return ChannelType.CLI
        elif channel == "api":
            return ChannelType.API
        else:
            return ChannelType.WEB

    def _get_trust_stage(
        self,
        context: Optional[Dict] = None,
    ) -> int:
        """
        Get trust stage from context.

        Issue #411: Trust stage affects recognition language.

        Args:
            context: Request context dict

        Returns:
            Trust stage (1-4), defaults to 1 for new users
        """
        if not context:
            return 1

        # Trust stage may be in context or user context
        trust_stage = context.get("trust_stage")
        if trust_stage is not None:
            return int(trust_stage)

        # Check user context
        user_context = context.get("user_context", {})
        if isinstance(user_context, dict):
            trust_stage = user_context.get("trust_stage")
            if trust_stage is not None:
                return int(trust_stage)

        # Default to stage 1 (new user)
        return 1

    async def classify_multiple(
        self,
        message: str,
        context: Optional[Dict] = None,
        session: Optional[Any] = None,
        spatial_context: Optional[Dict] = None,
        user_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ) -> MultiIntentResult:
        """
        Detect and classify multiple intents in a message (Issue #595).

        This method first uses rule-based multi-intent detection for common
        patterns (like "Hi Piper! What's on my agenda?"), then falls back to
        LLM classification for unmatched messages.

        The detection logic is designed to be reusable for #427
        (Unified Conversation Model).

        Args:
            message: User input text
            context: Optional context dict
            session: Optional session object
            spatial_context: Optional spatial context

        Returns:
            MultiIntentResult containing all detected intents
        """
        # Stage 0 here TOO (#1394/B3): detect_multiple_intents pattern-matches
        # update-verb messages (e.g. "change the title to X" → update_document_query)
        # and returns BEFORE classify() — so B3 must be consulted first at THIS
        # entry as well, or referent follow-ups misroute to document handlers
        # (the live 2026-07-12 Scenario-B turn-3 mechanism). Cheap for
        # non-referent messages: the detection regex fails fast, no ledger read.
        b3_intent = await self._resolve_issue_referent(message, user_id, session_id)
        if b3_intent is not None:
            logger.info(
                "intent_classification",
                source="B3_REFERENT_RESOLUTION",
                action=b3_intent.action,
                message_preview=message[:50],
            )
            return MultiIntentResult(
                intents=[b3_intent],
                original_message=message,
                is_multi_intent=False,
            )

        # First, try rule-based multi-intent detection
        multi_result = PreClassifier.detect_multiple_intents(message)

        if multi_result.intents:
            logger.info(
                "multi_intent_preclassified",
                message_preview=message[:50],
                intent_count=len(multi_result.intents),
                is_multi_intent=multi_result.is_multi_intent,
            )
            return multi_result

        # Fall back to standard LLM classification (returns single intent)
        # Wrap in MultiIntentResult for consistent interface
        try:
            single_intent = await self.classify(
                message=message,
                context=context,
                session=session,
                spatial_context=spatial_context,
                user_id=user_id,
                session_id=session_id,
            )
            return MultiIntentResult(
                intents=[single_intent],
                original_message=message,
                is_multi_intent=False,
            )
        except Exception as e:
            logger.error(f"Multi-intent classification failed: {e}", exc_info=True)
            # Return empty result on failure
            return MultiIntentResult(
                intents=[],
                original_message=message,
                is_multi_intent=False,
            )

    async def _classify_with_reasoning(
        self,
        message: str,
        context: Optional[Dict] = None,
        file_context: str = "",
        spatial_context: Optional[Dict] = None,
        user_id: Optional[str] = None,
    ) -> Tuple[Intent, Dict[str, Any]]:
        """Classify intent with detailed reasoning"""
        # Prepare context for LLM
        context_info = ""
        if context:
            context_info = f"\nContext: {json.dumps(context, indent=2)}"

            # Issue #852: Enrich with explicit continuation hint for LLM
            continuation_hint = context.get("contextual_continuation_hint")
            if continuation_hint:
                context_info += (
                    f'\n\nIMPORTANT: The user was just offered "{continuation_hint}" '
                    "and is responding affirmatively. Classify their intent as "
                    "accepting this offer — determine the appropriate category "
                    "and action for fulfilling the offered topic."
                )

        # Prepare spatial context for LLM
        spatial_context_info = ""
        if spatial_context:
            spatial_context_info = f"\nSpatial Context: {json.dumps(spatial_context, indent=2)}"

        # Build prompt with context
        prompt = INTENT_CLASSIFICATION_PROMPT.format(
            user_message=message,
            context_info=context_info,
            file_context=file_context,
            spatial_context=spatial_context_info,
        )

        try:
            # ADR-075 D4: resolve the classification system prompt through the
            # per-principal PersonalizationService rather than the unscoped
            # loader directly — the #1366 leak closure for this call site.
            from services.configuration.personalization_service import (
                personalization_service,
            )

            system_prompt = await personalization_service.resolve_system_prompt_standalone(
                user_id
            )

            # Use your task-based routing with "intent_classification" task type
            # #988: pass response_format={"type": "json_object"} so Gemini
            # (which needs an explicit flag) returns structured JSON. OpenAI
            # honors this natively; Anthropic ignores it (its prompt-following
            # for JSON is reliable without).
            response = await self.llm.complete(
                task_type="intent_classification",
                prompt=prompt,
                context=context,
                system=system_prompt,
                response_format={"type": "json_object"},
            )

            # Parse JSON response
            # Extract the first JSON object from the response
            json_match = re.search(r"\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}", response, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
                parsed = json.loads(json_str)
            else:
                raise ValueError("No valid JSON object found in response")

            # Build context with spatial information
            intent_context = {
                "original_message": message,
                "knowledge_used": parsed.get("knowledge_used", []),
            }

            # Add spatial context if available
            if spatial_context:
                intent_context["spatial_context"] = spatial_context
                # Add spatial coordinates for response targeting
                if "room_id" in spatial_context:
                    intent_context["response_target"] = {
                        "channel_id": spatial_context.get("room_id"),
                        "thread_ts": spatial_context.get("path_id"),
                        "workspace_id": spatial_context.get("territory_id"),
                    }

            intent = Intent(
                original_message=message,  # #1332/#1220: the MAIN path never set the
                # attribute (only context["original_message"]) — every downstream
                # reader of intent.original_message got "" (the floor's "came
                # through empty", slot-fills, regex fallbacks). Found live 2026-07-09.
                category=IntentCategory(parsed["category"].lower()),
                action=parsed["action"],
                confidence=parsed["confidence"],
                context=intent_context,
            )

            reasoning = {
                "classification_reasoning": parsed["reasoning"],
                "helpful_knowledge_domains": parsed.get("knowledge_domains", []),
                "ambiguity_notes": parsed.get("ambiguity_notes", []),
                "knowledge_used": parsed.get("knowledge_used", []),
            }

            return intent, reasoning

        except (json.JSONDecodeError, KeyError) as e:
            logger.error(f"Failed to parse or read LLM response: {e}", raw_response=response)
            raise IntentClassificationFailedError(
                details={
                    "reason": "LLM response was malformed",
                    "raw_response": response[:200],
                }
            )

    def _identify_learning_signals(self, message: str, intent: Intent, reasoning: Dict) -> Dict:
        """Identify what learning opportunities this interaction presents"""

        signals = {
            "confidence_level": intent.confidence,
            "knowledge_gaps": [],
            "clarification_needed": [],
            "pattern_matches": [],
        }

        # Low confidence suggests learning opportunity
        if intent.confidence < 0.7:
            signals["knowledge_gaps"].append(
                {
                    "type": "uncertain_classification",
                    "domain": reasoning.get("helpful_knowledge_domains", []),
                }
            )

        # Check for ambiguous language
        ambiguity_markers = [
            "something like",
            "maybe",
            "not sure",
            "could you",
            "might",
            "possibly",
        ]
        if any(marker in message.lower() for marker in ambiguity_markers):
            signals["clarification_needed"].append("ambiguous_request")

        # Check knowledge hierarchy needs
        for domain in reasoning.get("helpful_knowledge_domains", []):
            if domain not in self.knowledge_hierarchy:
                signals["knowledge_gaps"].append({"type": "missing_domain", "domain": domain})

        return signals

    def _assess_available_knowledge(self, context: Dict) -> List[str]:
        """Determine what knowledge is currently available"""
        # For now, return empty list
        # Later: Query knowledge graph for available domains
        return []

    def _fallback_classify(self, message: str) -> Intent:
        """Simple keyword-based classification as fallback, now with typo correction and fuzzy matching"""
        # --- Apply typo correction ---
        message_lower = correct_common_typos(message.lower())
        context = {"original_message": message, "method": "fallback"}

        # --- Define all pattern phrases for fuzzy matching ---
        pattern_action_map = {
            # Core find/search patterns
            "find documents": (IntentCategory.QUERY, "find_documents"),
            "find files": (IntentCategory.QUERY, "find_documents"),
            "find technical specifications": (IntentCategory.QUERY, "search_documents"),
            "find architecture documents": (IntentCategory.QUERY, "search_documents"),
            "find docs": (IntentCategory.QUERY, "find_documents"),
            "locate files": (IntentCategory.QUERY, "search_documents"),
            "locate documents": (IntentCategory.QUERY, "search_documents"),
            "locate api documentation": (IntentCategory.QUERY, "search_documents"),
            "locate api specifications": (IntentCategory.QUERY, "search_documents"),
            "locate specs": (IntentCategory.QUERY, "search_documents"),
            "look for files": (IntentCategory.QUERY, "find_documents"),
            "look for documents": (IntentCategory.QUERY, "find_documents"),
            "look for docs": (IntentCategory.QUERY, "find_documents"),
            "search for files": (IntentCategory.QUERY, "search_files"),
            "search for documents": (IntentCategory.QUERY, "search_files"),
            "search for docs": (IntentCategory.QUERY, "search_files"),
            "get all design docs": (IntentCategory.QUERY, "search_documents"),
            "get all documents": (IntentCategory.QUERY, "search_documents"),
            "get all files": (IntentCategory.QUERY, "search_documents"),
            "get documents": (IntentCategory.QUERY, "search_documents"),
            "get files": (IntentCategory.QUERY, "search_documents"),
            "show me all project plans": (IntentCategory.QUERY, "search_documents"),
            "show me all documents": (IntentCategory.QUERY, "search_documents"),
            "show me all files": (IntentCategory.QUERY, "search_documents"),
            "show me project plans": (IntentCategory.QUERY, "search_documents"),
            "search files": (IntentCategory.QUERY, "search_files"),
            "search documents": (IntentCategory.QUERY, "search_files"),
            "file search": (IntentCategory.QUERY, "search_files"),
            "document search": (IntentCategory.QUERY, "search_files"),
            "search for": (IntentCategory.QUERY, "search_files"),
            "show me files": (IntentCategory.QUERY, "find_documents"),
            "show me documents": (IntentCategory.QUERY, "find_documents"),
        }
        # --- Fuzzy match the message to a pattern ---
        matched_pattern = fuzzy_match(message_lower, list(pattern_action_map.keys()), cutoff=0.8)
        if matched_pattern:
            category, action = pattern_action_map[matched_pattern]
            # Use comprehensive extraction for search_query
            context["search_query"] = self._extract_search_query_comprehensive(message)
            return Intent(
                original_message=message,  # #1332/#1220
                category=category,
                action=action,
                confidence=0.7,  # Higher confidence for fuzzy match
                context=context,
            )
        # Explicit project query mappings
        if "how many projects" in message_lower or (
            "how many" in message_lower and "project" in message_lower
        ):
            category = IntentCategory.QUERY
            action = "count_projects"
        elif "default project" in message_lower:
            category = IntentCategory.QUERY
            action = "get_default_project"
        elif "find project" in message_lower:
            category = IntentCategory.QUERY
            action = "find_project"
        elif "project details" in message_lower:
            category = IntentCategory.QUERY
            action = "get_project_details"
        elif "get project" in message_lower and "id" in message_lower:
            category = IntentCategory.QUERY
            action = "get_project"
        elif any(word in message_lower for word in ["create", "make", "build", "add", "new"]):
            category = IntentCategory.EXECUTION
            action = "create_item"
        # Order matters: more specific patterns first
        elif any(
            phrase in message_lower
            for phrase in [
                "find files containing",
                "look for documents with",
                "files containing",
                "documents with",
                "search content",
                "search for content",
                "find content",
                "content search",
            ]
        ):
            category = IntentCategory.QUERY
            action = "search_content"
            context["search_query"] = self._extract_search_query(
                message,
                [
                    "find files containing",
                    "look for documents with",
                    "files containing",
                    "documents with",
                    "search content",
                    "search for content",
                    "find content",
                    "content search",
                ],
            )
        elif any(
            phrase in message_lower
            for phrase in [
                # Core find patterns
                "find documents",
                "find files",
                "find technical specifications",
                "find architecture documents",
                "find docs",
                # Common typos for find patterns
                "find tehcnical specifications",
                "find technical specfications",
                "find requirements",
                # Locate patterns
                "locate files",
                "locate documents",
                "locate api documentation",
                "locate api specifications",
                "locate specs",
                # Look for patterns
                "look for files",
                "look for documents",
                "look for docs",
                # Search for patterns
                "search for files",
                "search for documents",
                "search for docs",
                # Get patterns
                "get all design docs",
                "get all documents",
                "get all files",
                "get documents",
                "get files",
                # Show me patterns (specific)
                "show me all project plans",
                "show me all documents",
                "show me all files",
                "show me project plans",
            ]
        ):
            category = IntentCategory.QUERY
            action = "find_documents"
            context["search_query"] = self._extract_search_query_comprehensive(message)
        elif any(
            phrase in message_lower
            for phrase in [
                # Basic search patterns
                "search files",
                "search documents",
                "file search",
                "document search",
                # Search for patterns (general)
                "search for",
                "search for requirements files",
                "search for meeting notes files",
                # Common typos for search patterns
                "serach for requirments files",
                "search for requirments files",
                "search files",
                # Show me patterns (general)
                "show me files",
                "show me documents",
            ]
        ):
            category = IntentCategory.QUERY
            action = "search_files"
            context["search_query"] = self._extract_search_query_comprehensive(message)
        elif "find" in message_lower and any(
            keyword in message_lower
            for keyword in ["about", "regarding", "related to", "concerning"]
        ):
            category = IntentCategory.QUERY
            action = "find_documents"
            context["search_query"] = self._extract_search_query_about(message)
        elif any(
            phrase in message_lower for phrase in ["show me", "show me the", "display"]
        ) and any(keyword in message_lower for keyword in ["files", "documents", "docs"]):
            category = IntentCategory.QUERY
            action = "find_documents"
            context["search_query"] = self._extract_search_query_show_me(message)
        elif any(word in message_lower for word in ["analyze", "check", "review", "look at"]):
            category = IntentCategory.ANALYSIS
            action = "analyze_data"
        elif any(word in message_lower for word in ["summarize", "document", "write", "report"]):
            category = IntentCategory.SYNTHESIS
            action = "generate_content"
        elif any(word in message_lower for word in ["plan", "strategy", "prioritize", "decide"]):
            category = IntentCategory.STRATEGY
            action = "strategic_planning"
        elif any(
            word in message_lower
            for word in ["list", "show", "get", "find", "what", "which", "how many"]
        ):
            category = IntentCategory.QUERY
            action = "list_items"
        else:
            category = IntentCategory.LEARNING
            action = "learn_pattern"

        return Intent(
            original_message=message,  # #1332/#1220
            category=category,
            action=action,
            confidence=0.5,  # Lower confidence for fallback
            context=context,
        )

    def _seems_vague(self, intent: Intent) -> bool:
        """Detects if the intent/action is vague/underspecified."""
        vague_actions = {
            "clarification_needed",
            "unknown",
            "get_greeting",
            "get_help",
            "get_info",
            "get_something",
        }
        # Removed "problem", "issue", "bug", "fix" as these are legitimate in bug reports
        # Removed "improve", "change", "update" as these are legitimate in feature requests
        # Only keep truly vague words that indicate unclear intent
        vague_keywords = ["thing", "something", "it", "this", "that", "help"]
        # If action is a known vague action
        if intent.action in vague_actions:
            return True
        # If action or context contains vague keywords (as whole words)
        import re

        action_lower = (intent.action or "").lower()
        for word in vague_keywords:
            # Use word boundaries to avoid false positives like "it" in "create_item"
            if re.search(r"\b" + re.escape(word) + r"\b", action_lower):
                return True
        # If ambiguity notes are present in context
        ambiguity_notes = intent.context.get("ambiguity_notes") if intent.context else None
        if ambiguity_notes and any(isinstance(note, str) and note for note in ambiguity_notes):
            return True
        return False

    def _extract_search_query(self, message: str, trigger_phrases: List[str]) -> str:
        """Extract search query from message after removing trigger phrases"""
        message_lower = message.lower()

        # Find which trigger phrase was used
        for phrase in trigger_phrases:
            if phrase in message_lower:
                # Remove the trigger phrase and common prepositions
                query = message_lower.replace(phrase, "").strip()
                # Remove common prepositions and articles
                query = re.sub(
                    r"\b(for|about|on|in|with|by|from|to|at|of|the|a|an)\b", "", query
                ).strip()
                # Clean up extra spaces
                query = re.sub(r"\s+", " ", query).strip()
                return query if query else message.strip()

        # Fallback: return the original message
        return message.strip()

    def _extract_search_query_about(self, message: str) -> str:
        """Extract search query from 'find ... about ...' patterns"""
        message_lower = message.lower()

        # Pattern: "find documents about project timeline"
        if "about" in message_lower:
            parts = message_lower.split("about", 1)
            if len(parts) > 1:
                query = parts[1].strip()
                # Clean up the query
                query = re.sub(r"\b(the|a|an)\b", "", query).strip()
                query = re.sub(r"\s+", " ", query).strip()
                return query if query else message.strip()

        # Pattern: "find ... regarding ..." or "find ... related to ..."
        for keyword in ["regarding", "related to", "concerning"]:
            if keyword in message_lower:
                parts = message_lower.split(keyword, 1)
                if len(parts) > 1:
                    query = parts[1].strip()
                    query = re.sub(r"\b(the|a|an)\b", "", query).strip()
                    query = re.sub(r"\s+", " ", query).strip()
                    return query if query else message.strip()

        # Fallback: return the original message
        return message.strip()

    def _extract_search_query_show_me(self, message: str) -> str:
        """Extract search query from 'show me' patterns"""
        message_lower = message.lower()

        # Pattern: "show me files about X" or "show me documents related to Y"
        for prefix in [
            "show me files",
            "show me documents",
            "show me docs",
            "show me the files",
            "show me the documents",
            "show me",
        ]:
            if prefix in message_lower:
                # Remove the prefix
                query = message_lower.replace(prefix, "").strip()
                # Remove common prepositions
                for prep in [
                    "about",
                    "related to",
                    "concerning",
                    "regarding",
                    "with",
                    "containing",
                ]:
                    if prep in query:
                        query = query.split(prep, 1)[1].strip()
                        break
                # Clean up articles
                query = re.sub(r"\b(the|a|an)\b", "", query).strip()
                query = re.sub(r"\s+", " ", query).strip()
                return query if query else message.strip()

        # Fallback: return the original message
        return message.strip()

    def _extract_search_query_comprehensive(self, message: str) -> str:
        """Comprehensive search query extraction for all patterns"""
        message_lower = message.lower()

        # Define comprehensive trigger phrases with their priorities (most specific first)
        trigger_patterns = [
            # Very specific patterns
            "find technical specifications",
            "find architecture documents",
            "locate api documentation",
            "locate api specifications",
            "get all design docs",
            "show me all project plans",
            "search for requirements files",
            "search for meeting notes files",
            # Moderately specific patterns
            "find documents",
            "find files",
            "find docs",
            "locate files",
            "locate documents",
            "locate specs",
            "look for files",
            "look for documents",
            "look for docs",
            "search for files",
            "search for documents",
            "search for docs",
            "get all documents",
            "get all files",
            "get documents",
            "get files",
            "show me all documents",
            "show me all files",
            "show me project plans",
            "show me files",
            "show me documents",
            # General patterns
            "search files",
            "search documents",
            "file search",
            "document search",
            "search for",
        ]

        # Try each pattern from most specific to least
        for pattern in trigger_patterns:
            if pattern in message_lower:
                # Remove the trigger phrase
                query = message_lower.replace(pattern, "").strip()

                # Handle specific pattern extractions
                if "about" in query:
                    # "find documents about X" → extract "X"
                    parts = query.split("about", 1)
                    if len(parts) > 1:
                        query = parts[1].strip()
                elif any(prep in query for prep in ["related to", "regarding", "concerning"]):
                    # Handle other prepositions
                    for prep in ["related to", "regarding", "concerning"]:
                        if prep in query:
                            query = query.split(prep, 1)[1].strip()
                            break
                elif query.startswith("all "):
                    # "get all design docs" → extract "design docs"
                    query = query[4:].strip()

                # Clean up the query
                if query:
                    # Remove common articles and prepositions
                    query = re.sub(
                        r"\b(the|a|an|with|containing|for|on|in|at|of)\b", "", query
                    ).strip()
                    # Clean up multiple spaces
                    query = re.sub(r"\s+", " ", query).strip()

                    # Extract file type if present
                    if " files" in query:
                        query = query.replace(" files", "").strip()

                    return query if query else self._extract_from_context(message)

        # Fallback: try to extract meaningful terms
        return self._extract_from_context(message)

    def _extract_from_context(self, message: str) -> str:
        """Extract search terms from message context when no specific pattern matches"""
        message_lower = message.lower()

        # Remove common command words
        stop_words = [
            "find",
            "search",
            "locate",
            "get",
            "show",
            "me",
            "all",
            "the",
            "a",
            "an",
            "for",
            "about",
        ]
        words = message_lower.split()
        meaningful_words = [word for word in words if word not in stop_words and len(word) > 2]

        if meaningful_words:
            return " ".join(meaningful_words)

        # Ultimate fallback
        return message.strip()

    # Issue #278: Graph-first retrieval pattern methods
    async def _get_graph_context(
        self, message: str, user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get context from knowledge graph for improved intent classification.

        Args:
            message: User message
            user_id: User ID for personalization

        Returns:
            Dictionary with graph context information
        """
        if not self.knowledge_graph_service or not user_id:
            return {}

        try:
            context = await self.knowledge_graph_service.get_relevant_context(
                user_query=message,
                user_id=user_id,
                max_nodes=10,
            )
            return context
        except Exception as e:
            logger.warning(
                "Failed to get graph context",
                error=str(e),
                message_preview=message[:50],
            )
            return {}

    def _extract_intent_hints_from_graph(self, graph_context: Dict[str, Any]) -> List[str]:
        """
        Extract intent hints from graph context to improve classification.

        Analyzes reasoning chains and node names to identify relevant intent keywords.

        Args:
            graph_context: Context dictionary from get_relevant_context

        Returns:
            List of intent hint keywords
        """
        hints = []

        # Extract hints from reasoning chains
        for chain in graph_context.get("reasoning_chains", []):
            hints.append(chain.get("edge_type", "").lower())
            hints.append(chain.get("source", "").lower())
            hints.append(chain.get("target", "").lower())

        # Extract hints from node names
        for node in graph_context.get("nodes", []):
            node_name = getattr(node, "name", "").lower()
            if node_name:
                hints.append(node_name)

        # Clean and deduplicate hints
        hints = list(set([h.strip() for h in hints if h.strip()]))

        logger.debug(
            "Extracted intent hints from graph",
            hint_count=len(hints),
            hints=hints[:5],  # Log first 5 for debugging
        )

        return hints


# Create a singleton instance without event bus for backward compatibility
classifier = IntentClassifier()
