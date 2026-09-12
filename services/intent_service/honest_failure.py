"""
Honest failure handling for grammar-conscious intent classification.

When Piper can't understand something, she should admit it gracefully
rather than throwing technical errors. This transforms:
  "IntentClassificationFailedError: LLM response malformed"
into:
  "I'm having trouble understanding that. Could you rephrase it?"

The principle: Piper is a colleague who admits when she's confused,
not a system that "fails."

See: #619 GRAMMAR-TRANSFORM: Intent Classification
Pattern: Pattern-054 (Honest Failure)
"""

from typing import Any, Dict, Optional

from services.domain.models import Intent
from services.intent_service.intent_types import IntentClassificationContext, IntentUnderstanding
from services.intent_service.warmth_calibration import WarmthCalibrator
from services.shared_types import IntentCategory, InteractionSpace, PerceptionMode


class HonestFailureHandler:
    """
    Handles classification failures with grace and warmth.

    Instead of raising exceptions that surface as technical errors,
    this handler creates IntentUnderstanding responses that express
    Piper's confusion appropriately for the context.
    """

    # Confusion narratives by formality
    CONFUSION_NARRATIVES = {
        "casual": "I'm having trouble understanding that one.",
        "professional": "I'm having difficulty interpreting your request.",
        "warm": "I want to help, but I'm not quite following.",
        "terse": "Unable to interpret.",
        "neutral": "I'm not sure I understand.",
    }

    # Follow-up suggestions by formality
    FOLLOW_UP_SUGGESTIONS = {
        "casual": "Could you say that differently?",
        "professional": "Could you please rephrase your request?",
        "warm": "Could you tell me more about what you're looking for?",
        "terse": "Please clarify.",
        "neutral": "Could you rephrase that?",
    }

    def __init__(self, warmth_calibrator: Optional[WarmthCalibrator] = None):
        """
        Initialize the failure handler.

        Args:
            warmth_calibrator: Optional calibrator for error gentleness.
                              If not provided, creates a default one.
        """
        self.warmth_calibrator = warmth_calibrator or WarmthCalibrator()

    def handle_classification_failure(
        self,
        context: IntentClassificationContext,
        place_settings: Dict[str, Any],
        error_detail: Optional[str] = None,
    ) -> IntentUnderstanding:
        """
        Handle a classification failure gracefully.

        Instead of raising an exception, create a warm response that
        asks for clarification.

        Args:
            context: The classification context that failed
            place_settings: Settings from PlaceDetector
            error_detail: Optional technical error detail (for logging)

        Returns:
            IntentUnderstanding that asks for clarification
        """
        formality = place_settings.get("formality", "professional")

        # Create clarification-seeking intent
        clarification_intent = Intent(
            category=IntentCategory.CONVERSATION,
            action="clarification_needed",
            confidence=0.0,
            context={
                "original_message": context.message,
                "failure_type": "classification",
                "needs_human_help": True,
            },
        )

        # Add error detail for debugging (not shown to user)
        if error_detail:
            clarification_intent.context["_error_detail"] = error_detail

        # Get appropriate confusion narrative
        narrative = self.CONFUSION_NARRATIVES.get(formality, self.CONFUSION_NARRATIVES["neutral"])

        # Get appropriate follow-up
        follow_up = self.FOLLOW_UP_SUGGESTIONS.get(formality, self.FOLLOW_UP_SUGGESTIONS["neutral"])

        return IntentUnderstanding(
            intent=clarification_intent,
            understanding_narrative=narrative,
            confidence_expression="",  # No confidence to express
            place_awareness="",  # Don't call out Place during confusion
            perception_mode=PerceptionMode.NOTICING,
            follow_up_suggestion=follow_up,
        )

    def handle_low_confidence(
        self,
        intent: Intent,
        context: IntentClassificationContext,
        place_settings: Dict[str, Any],
    ) -> IntentUnderstanding:
        """
        Handle low-confidence classification by expressing uncertainty.

        When Piper has a guess but isn't confident, she should express
        that uncertainty rather than acting confident.

        Args:
            intent: The low-confidence Intent
            context: Classification context
            place_settings: Settings from PlaceDetector

        Returns:
            IntentUnderstanding that expresses uncertainty
        """
        formality = place_settings.get("formality", "professional")

        # Build uncertain narrative
        uncertain_narratives = {
            "casual": f"I think you might want to {self._humanize_action(intent.action)}, but I'm not sure.",
            "professional": f"I believe you may be asking to {self._humanize_action(intent.action)}, though I'm uncertain.",
            "warm": f"It seems like you might want to {self._humanize_action(intent.action)}—is that right?",
            "terse": f"Uncertain: {intent.action}?",
            "neutral": f"I think you want to {self._humanize_action(intent.action)}, but please confirm.",
        }

        narrative = uncertain_narratives.get(formality, uncertain_narratives["neutral"])

        # Confidence expression for uncertainty
        confidence_expressions = {
            "casual": "I'm not totally sure though",
            "professional": "However, I'm not entirely certain.",
            "warm": "I want to make sure I got that right.",
            "terse": "Unconfirmed.",
            "neutral": "Please confirm.",
        }

        confidence_expr = confidence_expressions.get(formality, confidence_expressions["neutral"])

        return IntentUnderstanding(
            intent=intent,
            understanding_narrative=narrative,
            confidence_expression=confidence_expr,
            place_awareness="",
            perception_mode=PerceptionMode.NOTICING,
            follow_up_suggestion="Is that what you meant?",
        )

    # #1759: handle_vague_intent was deleted with the dead clarify-carrier
    # machinery — its only caller was classify_conscious's vague branch
    # (itself zero-caller dead), removed per the #1730 Gap-2 ruling.

    def _humanize_action(self, action: str) -> str:
        """Convert technical action to human-readable form."""
        # Simple conversion: replace underscores with spaces
        return action.replace("_", " ")


def create_graceful_error_response(
    context: IntentClassificationContext,
    place_settings: Dict[str, Any],
    error: Exception,
) -> IntentUnderstanding:
    """
    Factory function to create graceful error response.

    Use this in try/except blocks instead of re-raising:

    try:
        result = await classify(...)
    except Exception as e:
        return create_graceful_error_response(context, settings, e)

    Args:
        context: Classification context
        place_settings: Place settings
        error: The caught exception

    Returns:
        IntentUnderstanding expressing confusion
    """
    handler = HonestFailureHandler()
    return handler.handle_classification_failure(
        context=context,
        place_settings=place_settings,
        error_detail=str(error),
    )
