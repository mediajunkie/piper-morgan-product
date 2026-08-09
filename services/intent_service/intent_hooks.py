"""
Intent Processing Hooks - Post-Classification Processing

Hooks called after intent classification to:
1. Detect user preferences
2. Enrich intent with additional context
3. Prepare data for response generation

These hooks enable extensibility without modifying core classifier logic.
"""

import logging
from typing import Any, Dict, Optional

# #1436: this imported the SQLAlchemy row (services.database.models.Intent)
# while every caller (classifier.py) passes the domain Intent — the annotation
# was drift, not the callers. The hook never touches the object's attributes.
from services.domain.models import Intent
from services.intent_service.preference_handler import PreferenceDetectionHandler
from services.personality.personality_profile import PersonalityProfile

logger = logging.getLogger(__name__)


class IntentProcessingHooks:
    """
    Central hook dispatcher for post-intent processing.

    Called after intent is classified but before response generation.
    Enables plugins to extend intent classification without modifying core logic.
    """

    def __init__(self, preference_handler: Optional[PreferenceDetectionHandler] = None):
        """
        Initialize hooks with dependencies.

        Args:
            preference_handler: PreferenceDetectionHandler for preference detection.
                               If None, preference detection is skipped.
        """
        self.preference_handler = preference_handler

    async def on_intent_classified(
        self,
        user_id: str,
        message: str,
        intent: Intent,
        session_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Called after intent is classified, before response generation.

        This is the main hook that runs all post-classification processing.

        Args:
            user_id: User ID
            message: Original user message
            intent: Classified intent object
            session_id: Current session ID (optional)

        Returns:
            Dict with hook results:
            {
                "preferences": {
                    "hints": [PreferenceHint.to_dict(), ...],
                    "has_suggestions": bool,
                    "has_auto_applies": bool,
                    "analysis_summary": str
                },
                "success": bool
            }
        """
        result = {
            "preferences": None,
            "success": True,
        }

        # Run preference detection if handler available
        if self.preference_handler:
            try:
                pref_result = await self._run_preference_detection(
                    user_id=user_id,
                    message=message,
                    session_id=session_id,
                )
                result["preferences"] = pref_result
            except Exception as e:
                logger.error(f"Error in preference detection hook for {user_id}: {e}")
                # Don't fail the intent classification if preference detection fails
                result["preferences"] = None

        return result

    async def _run_preference_detection(
        self,
        user_id: str,
        message: str,
        session_id: Optional[str],
    ) -> Dict[str, Any]:
        """
        Run preference detection on user message.

        Args:
            user_id: User ID
            message: User message
            session_id: Session ID (optional)

        Returns:
            Dict with preference detection results
        """
        try:
            # Load current personality profile
            current_profile = await PersonalityProfile.load_with_preferences(user_id)

            # Analyze message for preferences
            detection_result = self.preference_handler.analyzer.analyze_message(
                user_id=user_id,
                message=message,
                current_profile=current_profile,
            )

            # Process auto-apply hints (high confidence)
            if detection_result.auto_apply_hints:
                await self.preference_handler.apply_auto_preferences(
                    user_id=user_id,
                    session_id=session_id,
                    hints=detection_result.auto_apply_hints,
                )

            # Store suggested hints in session for later retrieval
            if detection_result.suggested_hints and session_id:
                await self.preference_handler._store_hints_in_session(
                    session_id=session_id,
                    hints=detection_result.suggested_hints,
                )

            # Return preference metadata for response
            return {
                "hints": [h.to_dict() for h in detection_result.suggested_hints],
                "has_suggestions": detection_result.has_suggestions(),
                "has_auto_applies": detection_result.has_auto_applies(),
                "analysis_summary": detection_result.analysis_summary,
            }

        except Exception as e:
            logger.error(f"Preference detection failed: {e}")
            return {
                "hints": [],
                "has_suggestions": False,
                "has_auto_applies": False,
                "analysis_summary": "",
            }
