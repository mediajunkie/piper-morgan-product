"""
Preference Detection Handler - Post-Intent Processing Hook

Integrates ConversationAnalyzer into intent service to detect and apply
user personality preferences from conversation patterns.

Flow:
1. After intent classification → detect preferences from message
2. After response generation → analyze user's reaction
3. Before returning to user → suggest or auto-apply detected preferences
4. When preference confirmed → store via UserPreferenceManager (user-scoped)

1613: confirmed preferences are stored ONLY through the user-scoped
UserPreferenceManager. The former hand-off to the cross-user pooled learning
store (QueryLearningLoop) was severed per PM ruling 2026-08-31 — pooling by
source_feature contradicted published privacy claims.
"""

import logging
from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from services.domain.user_preference_manager import UserPreferenceManager
from services.personality.conversation_analyzer import ConversationAnalyzer
from services.personality.personality_profile import PersonalityProfile
from services.personality.preference_detection import (
    PreferenceConfirmation,
    PreferenceDimension,
    PreferenceHint,
)

logger = logging.getLogger(__name__)

# Session-based storage for temporary hints (30-minute TTL)
# Maps: session_id -> {hint_id -> PreferenceHint}
_SESSION_HINTS: Dict[str, Dict[str, dict]] = {}


class PreferenceDetectionHandler:
    """
    Handles preference detection and application throughout conversation flow.

    Integration points:
    1. Post-intent-classification hook → detect from message
    2. Post-response-generation hook → analyze user reaction
    3. Post-response-delivery hook → suggest or auto-apply
    4. Preference-confirmation hook → store via user-scoped UserPreferenceManager
    """

    def __init__(self):
        """Initialize handler with dependencies"""
        self.analyzer = ConversationAnalyzer()
        self.preference_manager = UserPreferenceManager()

    async def handle_message_analysis(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str],
        current_profile: PersonalityProfile,
    ) -> Dict[str, Any]:
        """
        Analyze user message for preference signals.

        Called after intent classification, before response generation.

        Args:
            user_id: User ID
            message: User's message text
            session_id: Current session ID (optional)
            current_profile: User's current personality profile

        Returns:
            Dict with detected hints and metadata
            {
                "hints": [PreferenceHint, ...],
                "has_suggestions": bool,
                "has_auto_applies": bool,
                "analysis_summary": str
            }
        """
        try:
            # Run preference detection
            detection_result = self.analyzer.analyze_message(user_id, message, current_profile)

            # Log detection results
            if detection_result.hints:
                logger.info(
                    f"Preference analysis for {user_id}: "
                    f"{len(detection_result.hints)} hints detected, "
                    f"{len(detection_result.suggested_hints)} ready for suggestion"
                )

            # Store hints in session context for later retrieval (30-minute TTL)
            if session_id:
                await self._store_hints_in_session(session_id, detection_result.suggested_hints)

            return {
                "success": True,
                "hints": [h.to_dict() for h in detection_result.hints],
                "suggested_hints": [h.to_dict() for h in detection_result.suggested_hints],
                "auto_apply_hints": [h.to_dict() for h in detection_result.auto_apply_hints],
                "has_suggestions": detection_result.has_suggestions(),
                "has_auto_applies": detection_result.has_auto_applies(),
                "analysis_summary": detection_result.analysis_summary,
            }

        except Exception as e:
            logger.error(f"Error in preference detection for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "hints": [],
                "has_suggestions": False,
                "has_auto_applies": False,
            }

    async def handle_response_analysis(
        self,
        user_id: str,
        user_message: str,
        system_response: str,
        session_id: Optional[str],
        current_profile: PersonalityProfile,
    ) -> Dict[str, Any]:
        """
        Analyze user's reaction to system response for preferences.

        Called after response is generated, before sending to user.

        Args:
            user_id: User ID
            user_message: Original user message
            system_response: System's response text
            session_id: Current session ID (optional)
            current_profile: User's current personality profile

        Returns:
            Dict with refined hints and metadata
        """
        try:
            # Analyze how user reacted to response
            detection_result = self.analyzer.analyze_response(
                user_id, user_message, system_response, current_profile
            )

            if detection_result.hints:
                logger.info(
                    f"Response analysis for {user_id}: "
                    f"{len(detection_result.hints)} refinements detected"
                )

            return {
                "success": True,
                "hints": [h.to_dict() for h in detection_result.hints],
                "analysis_summary": detection_result.analysis_summary,
            }

        except Exception as e:
            logger.error(f"Error in response analysis for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "hints": [],
            }

    async def apply_auto_preferences(
        self,
        user_id: str,
        session_id: Optional[str],
        hints: list[PreferenceHint],
    ) -> Dict[str, Any]:
        """
        Auto-apply hints with very high confidence.

        Called before returning response if auto_apply_hints exist.

        Args:
            user_id: User ID
            session_id: Current session ID (optional)
            hints: List of PreferenceHint objects with high confidence

        Returns:
            Dict with applied changes and metadata
        """
        applied = []
        errors = []

        for hint in hints:
            if not hint.is_ready_for_auto_apply():
                continue

            try:
                # Create confirmation for auto-apply
                confirmation = PreferenceConfirmation(
                    id=f"confirm_{uuid4().hex[:8]}",
                    user_id=user_id,
                    dimension=hint.dimension,
                    new_value=hint.detected_value,
                    previous_value=hint.current_value,
                    hint_id=hint.id,
                    confirmation_source="auto_apply",
                )

                # Store confirmation
                await self.preference_manager.apply_preference_pattern(
                    pattern={
                        "dimension": confirmation.dimension.value,
                        "new_value": str(confirmation.new_value),
                        "hint_id": confirmation.hint_id,
                        "source": "auto_apply",
                    },
                    user_id=user_id,
                    session_id=session_id,
                    scope="session" if session_id else "user",
                )

                applied.append(
                    {
                        "dimension": hint.dimension.value,
                        "previous_value": str(hint.current_value),
                        "new_value": str(hint.detected_value),
                        "hint_id": hint.id,
                    }
                )

                logger.info(
                    f"Auto-applied preference for {user_id}: "
                    f"{hint.dimension.value} = {hint.detected_value}"
                )

            except Exception as e:
                logger.error(f"Error auto-applying preference for {user_id}: {e}")
                errors.append(
                    {
                        "hint_id": hint.id,
                        "dimension": hint.dimension.value,
                        "error": str(e),
                    }
                )

        return {
            "success": len(errors) == 0,
            "applied": applied,
            "errors": errors,
        }

    async def suggest_preferences(
        self,
        user_id: str,
        session_id: Optional[str],
        hints: list[PreferenceHint],
    ) -> Dict[str, Any]:
        """
        Prepare suggestions for user to accept/reject.

        Called before returning response if suggested_hints exist.

        Args:
            user_id: User ID
            session_id: Current session ID (optional)
            hints: List of PreferenceHint objects ready for suggestion

        Returns:
            Dict with prepared suggestions for UI display
        """
        suggestions = []

        for hint in hints:
            if not hint.is_ready_for_suggestion():
                continue

            suggestions.append(
                {
                    "hint_id": hint.id,
                    "dimension": hint.dimension.value,
                    "current_value": str(hint.current_value),
                    "suggested_value": str(hint.detected_value),
                    "confidence_score": hint.confidence_score,
                    "confidence_level": hint.confidence_level().value,
                    "explanation": self._generate_suggestion_explanation(hint),
                }
            )

        logger.info(f"Prepared {len(suggestions)} preference suggestions for {user_id}")

        return {
            "success": True,
            "suggestions": suggestions,
            "has_suggestions": len(suggestions) > 0,
        }

    async def confirm_preference(
        self,
        user_id: str,
        session_id: Optional[str],
        hint_id: str,
        accepted: bool,
    ) -> Dict[str, Any]:
        """
        Handle user's acceptance/rejection of preference suggestion.

        Called when user interacts with suggestion UI (Phase 2.2).

        Args:
            user_id: User ID
            session_id: Current session ID (optional)
            hint_id: ID of the hint being confirmed
            accepted: True if user accepted, False if rejected

        Returns:
            Dict with confirmation result and updated preference info
        """
        # Handle rejection (no storage needed)
        if not accepted:
            logger.info(f"User {user_id} rejected preference hint {hint_id}")
            # In future phases: log rejection to learning system for refinement
            return {
                "success": True,
                "action": "rejected",
                "hint_id": hint_id,
            }

        try:
            # Retrieve hint from session storage
            hint_dict = await self._retrieve_hint_from_session(session_id, hint_id)
            if not hint_dict:
                logger.warning(
                    f"Preference hint {hint_id} not found in session {session_id} for user {user_id}"
                )
                return {
                    "success": False,
                    "error": "Preference suggestion not found or expired",
                    "hint_id": hint_id,
                }

            # Reconstruct hint data
            # hint_dict["dimension"] contains enum value like "warmth_level"
            # We need to find the enum member with that value
            dimension_value = hint_dict["dimension"]
            dimension = None
            for dim in PreferenceDimension:
                if dim.value == dimension_value:
                    dimension = dim
                    break
            if not dimension:
                raise ValueError(f"Unknown preference dimension: {dimension_value}")
            current_value = hint_dict["current_value"]
            detected_value = hint_dict["detected_value"]

            # Store preference in UserPreferenceManager (persistent)
            pref_key = f"personality_{dimension.value}"
            await self.preference_manager.set_preference(
                key=pref_key,
                value=str(detected_value),
                user_id=UUID(user_id) if user_id != "user_id" else None,
                scope="user" if user_id else "global",
            )

            logger.info(
                f"User {user_id} accepted and applied preference: "
                f"{dimension.value} = {detected_value}"
            )

            return {
                "success": True,
                "action": "accepted",
                "hint_id": hint_id,
                "dimension": dimension.value,
                "previous_value": str(current_value),
                "new_value": str(detected_value),
                "message": f"Preference updated! Your {dimension.value} setting is now {detected_value}",
            }

        except Exception as e:
            logger.error(f"Error confirming preference for {user_id}: {e}")
            return {
                "success": False,
                "error": str(e),
                "hint_id": hint_id,
            }

    # Private helper methods

    def _generate_suggestion_explanation(self, hint: PreferenceHint) -> str:
        """
        Generate user-friendly explanation for why we're suggesting this.

        Args:
            hint: PreferenceHint to explain

        Returns:
            Human-readable explanation
        """
        dimension = hint.dimension.value.replace("_", " ")

        if hint.detection_method.value == "language_patterns":
            return (
                f"We noticed you tend to use {dimension}-related language, "
                f"so you might prefer: {hint.detected_value}"
            )
        elif hint.detection_method.value == "explicit_feedback":
            return (
                f"You mentioned you prefer {hint.detected_value}, "
                f"so we're updating your {dimension} preference"
            )
        elif hint.detection_method.value == "behavioral_signals":
            return (
                f"Based on your recent interactions, "
                f"we think you'd prefer {hint.detected_value} for {dimension}"
            )
        else:
            return f"We think you might prefer: {hint.detected_value}"

    async def _store_hints_in_session(self, session_id: str, hints: list[PreferenceHint]) -> None:
        """
        Store preference hints in session context for later retrieval.

        Hints are stored temporarily with 30-minute TTL for use by confirm_preference().

        Args:
            session_id: Current session ID
            hints: List of PreferenceHint objects to store
        """
        if not session_id or not hints:
            return

        try:
            # Initialize session storage if needed
            if session_id not in _SESSION_HINTS:
                _SESSION_HINTS[session_id] = {}

            # Store each hint as dict for JSON serialization
            for hint in hints:
                _SESSION_HINTS[session_id][hint.id] = {
                    "id": hint.id,
                    "dimension": hint.dimension.value,
                    "current_value": str(hint.current_value),
                    "detected_value": str(hint.detected_value),
                    "confidence_score": hint.confidence_score,
                    "detection_method": hint.detection_method.value,
                    "stored_at": datetime.now().isoformat(),
                    "ttl_minutes": 30,
                }

            logger.debug(f"Stored {len(hints)} preference hints in session {session_id}")

        except Exception as e:
            logger.error(f"Error storing hints in session {session_id}: {e}")

    async def _retrieve_hint_from_session(
        self, session_id: Optional[str], hint_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve a preference hint from session storage.

        Checks expiration (30-minute TTL) and removes expired hints.

        Args:
            session_id: Current session ID (required to find hint)
            hint_id: ID of the hint to retrieve

        Returns:
            Hint dict if found and not expired, None otherwise
        """
        if not session_id or session_id not in _SESSION_HINTS:
            return None

        if hint_id not in _SESSION_HINTS[session_id]:
            return None

        try:
            hint_dict = _SESSION_HINTS[session_id][hint_id]

            # Check expiration (30-minute TTL)
            stored_at = datetime.fromisoformat(hint_dict["stored_at"])
            age_minutes = (datetime.now() - stored_at).total_seconds() / 60
            if age_minutes > 30:
                # Expired - remove it
                del _SESSION_HINTS[session_id][hint_id]
                logger.debug(f"Preference hint {hint_id} expired (age: {age_minutes:.1f} min)")
                return None

            return hint_dict

        except Exception as e:
            logger.error(f"Error retrieving hint {hint_id} from session {session_id}: {e}")
            return None
