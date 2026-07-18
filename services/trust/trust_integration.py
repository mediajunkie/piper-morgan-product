"""
Trust Integration - Connects trust computation to intent processing.

Issue #648: TRUST-LEVELS-2 - Integration
ADR-053: Trust Computation Architecture

This module provides the integration layer between:
- Intent processing (services/intent/)
- Trust computation (services/trust/)

Key responsibilities:
1. Record interaction outcomes after intent processing
2. Detect conversational signals for stage transitions
3. Provide proactivity configuration for response generation
"""

import logging
from typing import Optional
from uuid import UUID

from services.domain.models import RequestContext
from services.trust.outcome_classifier import OutcomeClassifier, OutcomeType
from services.trust.proactivity_gate import ProactivityGate
from services.trust.signal_detector import SignalDetector, SignalType
from services.trust.trust_computation_service import TrustComputationService

logger = logging.getLogger(__name__)


class TrustIntegration:
    """
    Integration layer for trust computation in intent processing.

    This class coordinates between OutcomeClassifier, SignalDetector,
    ProactivityGate, and TrustComputationService to:

    1. After each interaction, classify outcome and record to trust profile
    2. Detect escalation signals for Stage 3→4 progression
    3. Detect complaint signals that may trigger regression
    4. Provide proactivity configuration for response generation

    Usage in IntentService.process_intent():
        trust = TrustIntegration(trust_service)

        # After processing intent
        result = await self._process_intent_internal(...)

        # Record the interaction outcome
        await trust.process_interaction(
            user_id=user_id,
            user_message=message,
            processing_result=result,
        )

        # Get proactivity config for response generation
        proactivity = await trust.get_proactivity_config(user_id)
    """

    def __init__(self, trust_service: TrustComputationService):
        """
        Initialize with trust computation service.

        Args:
            trust_service: The TrustComputationService instance
        """
        self.trust_service = trust_service
        self.outcome_classifier = OutcomeClassifier()
        self.signal_detector = SignalDetector()
        self.proactivity_gate = ProactivityGate()

    async def process_interaction(
        self,
        user_id: UUID,
        user_message: str,
        processing_result: "IntentProcessingResult",
        ctx: Optional[RequestContext] = None,
    ) -> dict:
        """
        Process an interaction for trust computation.

        This is the main integration point called after intent processing.
        It handles:
        1. Outcome classification based on result success/message
        2. Signal detection for stage transitions
        3. Recording the interaction with appropriate outcome

        Args:
            user_id: The authenticated user's ID
            user_message: The user's original message
            processing_result: The result from intent processing
            ctx: Optional RequestContext

        Returns:
            Dict with trust processing results:
            {
                "outcome": "successful"|"neutral"|"negative",
                "trust_stage": <current stage after processing>,
                "stage_changed": bool,
                "escalation_detected": bool,
                "complaint_detected": bool,
                "soft_regression_detected": bool,
            }
        """
        try:
            # 1. Check for conversational signals first
            signal_result = self.signal_detector.detect(user_message)

            # 2. Handle escalation signals (Stage 3→4 progression)
            if signal_result.signal_type == SignalType.ESCALATION:
                logger.info(  # #1436: stdlib logger — kwargs raised TypeError
                    f"trust_escalation_signal_detected user={user_id} patterns={signal_result.patterns_matched}"
                )
                # Attempt to progress to TRUSTED stage
                escalation_result = await self.trust_service.progress_to_trusted(
                    user_id=user_id,
                    reason=signal_result.reasoning,
                )
                if escalation_result:
                    return {
                        "outcome": "successful",
                        "trust_stage": escalation_result.current_stage.value,
                        "stage_changed": True,
                        "escalation_detected": True,
                        "complaint_detected": False,
                        "soft_regression_detected": False,
                    }

            # 3. Handle complaint signals - immediate regression to Stage 2
            # Per ADR-053 and PPM guidance: explicit complaint → Stage 2 floor
            complaint_detected = False
            if signal_result.signal_type == SignalType.COMPLAINT:
                logger.info(  # #1436: stdlib logger — kwargs raised TypeError
                    f"trust_complaint_signal_detected user={user_id} patterns={signal_result.patterns_matched}"
                )
                complaint_detected = True
                # Immediate regression to BUILDING (not gradual via consecutive_negative)
                profile = await self.trust_service.handle_explicit_complaint(
                    user_id=user_id,
                    complaint=signal_result.reasoning,
                )
                return {
                    "outcome": "negative",
                    "trust_stage": profile.current_stage.value,
                    "stage_changed": True,  # Complaint always triggers stage evaluation
                    "escalation_detected": False,
                    "complaint_detected": True,
                    "soft_regression_detected": False,
                }

            # 4. Handle soft regression signals - one stage drop (not to floor)
            # Per PPM guidance: "ask me first next time" is softer than complaint
            if signal_result.signal_type == SignalType.SOFT_REGRESSION:
                logger.info(  # #1436: stdlib logger — kwargs raised TypeError
                    f"trust_soft_regression_signal_detected user={user_id} patterns={signal_result.patterns_matched}"
                )
                profile = await self.trust_service.handle_soft_regression(
                    user_id=user_id,
                    reason=signal_result.reasoning,
                )
                return {
                    "outcome": "neutral",  # Not negative, just a preference signal
                    "trust_stage": profile.current_stage.value,
                    "stage_changed": True,
                    "escalation_detected": False,
                    "complaint_detected": False,
                    "soft_regression_detected": True,
                }

            # 5. Classify outcome based on processing result
            context = {
                "task_completed": processing_result.success,
                "error_occurred": processing_result.error is not None,
            }
            outcome_result = self.outcome_classifier.classify(
                user_message=user_message,
                context=context,
            )

            # 5. Record the interaction
            profile = await self.trust_service.record_interaction(
                user_id=user_id,
                outcome=outcome_result.outcome.value,
                context=f"Intent processing: {outcome_result.reasoning}",
            )

            logger.info(  # #1436: stdlib logger — kwargs raised TypeError
                f"trust_interaction_recorded user={user_id} "
                f"outcome={outcome_result.outcome.value} "
                f"trust_stage={profile.current_stage.value}"
            )

            return {
                "outcome": outcome_result.outcome.value,
                "trust_stage": profile.current_stage.value,
                "stage_changed": False,  # Will be updated by TrustComputationService
                "escalation_detected": False,
                "complaint_detected": False,
                "soft_regression_detected": False,
            }

        except Exception as e:
            logger.error(f"Trust integration error: {e}", exc_info=True)
            # Fail gracefully - don't break intent processing
            return {
                "outcome": "neutral",
                "trust_stage": 1,  # NEW stage as fallback
                "stage_changed": False,
                "escalation_detected": False,
                "complaint_detected": False,
                "soft_regression_detected": False,
                "error": str(e),
            }

    async def get_proactivity_config(self, user_id: UUID) -> dict:
        """
        Get proactivity configuration for a user based on their trust stage.

        Used by response generation to determine what proactive behaviors
        are allowed.

        Args:
            user_id: The user's ID

        Returns:
            Proactivity configuration dict
        """
        try:
            stage = await self.trust_service.get_trust_stage(user_id)
            config = self.proactivity_gate.get_proactivity_config(stage)
            config["trust_stage"] = stage.value
            config["trust_stage_name"] = stage.name
            return config
        except Exception as e:
            logger.error(f"Failed to get proactivity config: {e}")
            # Return restrictive defaults (NEW stage behavior)
            return {
                "can_offer_hints": False,
                "can_suggest": False,
                "can_act_autonomously": False,
                "max_suggestions_per_session": 0,
                "suggestion_delay_seconds": 0,
                "trust_stage": 1,
                "trust_stage_name": "NEW",
            }

    async def should_be_proactive(
        self,
        user_id: UUID,
        behavior_type: str,
    ) -> bool:
        """
        Quick check if a specific proactive behavior is allowed.

        Args:
            user_id: The user's ID
            behavior_type: One of "hints", "suggestions", "autonomous"

        Returns:
            True if the behavior is allowed at user's trust stage
        """
        try:
            stage = await self.trust_service.get_trust_stage(user_id)

            if behavior_type == "hints":
                return self.proactivity_gate.can_offer_capability_hints(stage)
            elif behavior_type == "suggestions":
                return self.proactivity_gate.can_proactive_suggest(stage)
            elif behavior_type == "autonomous":
                return self.proactivity_gate.can_act_without_asking(stage)
            else:
                logger.warning(f"Unknown behavior type: {behavior_type}")
                return False

        except Exception as e:
            logger.error(f"Proactivity check failed: {e}")
            return False

    async def get_welcome_back_message(self, user_id: UUID) -> Optional[str]:
        """
        Get welcome back message if user has regressed due to inactivity.

        Per ADR-053, when a user returns after inactivity-based regression,
        we should acknowledge the relationship reset.

        Args:
            user_id: The user's ID

        Returns:
            Welcome back message if needed, None otherwise
        """
        try:
            # This would check if user recently regressed
            # For MVP, we'll use explain_trust_state which includes
            # information about the current relationship state
            explanation = await self.trust_service.explain_trust_state(user_id)

            # Check if explanation mentions regression or getting to know
            if "getting to know" in explanation.lower():
                return (
                    "Welcome back! It's been a while since we last worked together. "
                    "I'm starting fresh with our working relationship - just let me know "
                    "how I can help."
                )

            return None

        except Exception as e:
            logger.error(f"Welcome back check failed: {e}")
            return None
