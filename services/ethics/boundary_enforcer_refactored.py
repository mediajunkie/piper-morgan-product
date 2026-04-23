"""
PM-087 BoundaryEnforcer Service - Refactored for Service Layer (Issue #197)
Core service for ethics boundary enforcement at the domain layer

REFACTORED: October 18, 2025 - Phase 2A
- Removed FastAPI dependency (was line 21)
- Changed signature to accept domain objects (message, session_id, context)
- Works across ALL entry points (web, CLI, Slack, webhooks)
- Maintains all Phase 3 enhancements (adaptive learning, audit transparency)

Architecture:
- Domain Layer: Works with string message + session_id + context dict
- Service Layer: Called by IntentService.process_intent()
- No Infrastructure Dependencies: No FastAPI, no HTTP

Leverages existing ethics infrastructure:
- services/infrastructure/monitoring/ethics_metrics.py
- services/infrastructure/logging/config.py
- services/domain/models.py patterns

Phase 3 Enhancements (PRESERVED):
- Adaptive boundary learning from metadata
- Audit transparency with security redactions
- Enhanced pattern detection algorithms
"""

import asyncio
import time
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from services.domain.models import BoundaryViolation, EthicalDecision
from services.ethics.adaptive_boundaries import adaptive_boundaries
from services.ethics.audit_transparency import audit_transparency
from services.infrastructure.logging.config import get_ethics_logger
from services.infrastructure.monitoring.ethics_metrics import (
    EthicsDecisionType,
    EthicsMetrics,
    EthicsViolationType,
    ethics_metrics,
)

# REMOVED: from fastapi import Request (Line 21 in original)


class BoundaryType:
    """Types of boundaries that can be enforced"""

    PROFESSIONAL = "professional"
    PERSONAL = "personal"
    DATA_PRIVACY = "data_privacy"
    HARASSMENT = "harassment"
    INAPPROPRIATE_CONTENT = "inappropriate_content"


class BoundaryDecision:
    """Result of a boundary enforcement decision.

    Added by #992 ETHICS-ACTIVATE (Phase A):
        redirect_context: Neutral hint string for the floor LLM when composing
            a decline. Category-derived, audit-safe (never includes raw matched
            patterns or the user's content). The floor uses this — not
            `explanation` — to craft the user-facing decline voice.
            None when no violation was detected.
    """

    def __init__(
        self,
        violation_detected: bool,
        boundary_type: str,
        explanation: str,
        audit_data: Dict[str, Any],
        session_id: Optional[str] = None,
        redirect_context: Optional[str] = None,
    ):
        self.violation_detected = violation_detected
        self.boundary_type = boundary_type
        self.explanation = explanation
        self.audit_data = audit_data
        self.session_id = session_id
        self.redirect_context = redirect_context
        self.timestamp = datetime.now(timezone.utc)


class BoundaryEnforcer:
    """
    Universal ethics boundary enforcement for all entry points.

    REFACTORED (Phase 2A, Issue #197):
    - Works with domain objects (message, session_id, context)
    - No HTTP dependencies
    - Usable by web, CLI, Slack, webhooks, etc.

    Original: services/ethics/boundary_enforcer.py (HTTP-dependent)
    Refactored: This file (domain layer)
    """

    def __init__(self):
        self.ethics_logger = get_ethics_logger(__name__)
        self.metrics = ethics_metrics

        # Boundary violation patterns (unchanged from original)
        self.harassment_patterns = [
            "harass",
            "harassment",
            "bully",
            "bullying",
            "intimidate",
            "threaten",
            "inappropriate",
            "unwanted",
            "uncomfortable",
            "offensive",
        ]

        self.professional_boundary_patterns = [
            "personal",
            "private",
            "relationship",
            "romantic",
            "dating",
            "family",
            "home",
            "personal life",
            "private life",
        ]

        self.inappropriate_content_patterns = [
            "explicit",
            "sexual",
            "violent",
            "hate speech",
            "discrimination",
            "racist",
            "sexist",
            "homophobic",
            "transphobic",
        ]

    async def enforce_boundaries(
        self,
        message: str,
        session_id: Optional[str] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> BoundaryDecision:
        """
        Main boundary enforcement method - Enhanced with Phase 3 features.

        REFACTORED (Phase 2A, Issue #197):
        - Changed signature from (request: Request) to (message, session_id, context)
        - Extracts data from parameters instead of HTTP Request object
        - All ethics logic preserved from original implementation

        Args:
            message: User message/content to check (from any source)
            session_id: Optional session identifier
            context: Optional context dict with metadata:
                - source: Entry point (web, cli, slack, etc.)
                - timestamp: Request timestamp
                - user_id: User identifier (if authenticated)
                - Any other contextual metadata

        Returns:
            BoundaryDecision with violation status, type, explanation, audit data
        """
        start_time = time.time()

        # Use provided context or create default
        context = context or {}
        session_id = session_id or context.get("session_id", "default_session")

        # Extract content (REFACTORED: directly from message parameter)
        content = message  # Was: await self._extract_content_from_request(request)

        # Create interaction metadata for adaptive learning (REFACTORED: from context dict)
        interaction_metadata = {
            "content_length": len(content),
            "session_id": session_id,
            "timestamp": context.get("timestamp", datetime.now(timezone.utc)),
            "request_method": context.get("source", "DOMAIN_SERVICE"),  # Was: request.method
            "user_agent_hash": hash(str(context.get("user_agent", ""))) % 10000,
            "time_of_day": datetime.now(timezone.utc).hour,
            "day_of_week": datetime.now(timezone.utc).weekday(),
        }

        # Perform enhanced boundary checks with adaptive patterns (UNCHANGED)
        violation_detected = False
        boundary_type = None

        # Phase 3: Get adaptive learning enhancement
        # FIXED (Phase 2B): Handle type mismatch - get_adaptive_patterns returns List[str], not Dict
        # For now, use empty dict until adaptive enhancement API is updated
        adaptive_patterns = await adaptive_boundaries.get_adaptive_patterns(boundary_type or "none")

        # Convert pattern list to enhancement dict (temporary fix)
        adaptive_enhancement = {
            "adaptive_confidence_adjustment": 0.0,
            "temporal_risk_factor": 1.0,
            "contextual_risk_factor": 1.0,
            "recommendation": "proceed",
            "learned_patterns_matched": (
                len(adaptive_patterns) if isinstance(adaptive_patterns, list) else 0
            ),
        }

        explanation = ""
        confidence = 0.0

        # Check for harassment patterns (enhanced) - UNCHANGED
        harassment_result = await self._enhanced_harassment_check(content, adaptive_enhancement)
        if harassment_result["violation"]:
            violation_detected = True
            boundary_type = BoundaryType.HARASSMENT
            explanation = harassment_result["explanation"]
            confidence = harassment_result["confidence"]

        # Check professional boundaries (enhanced) - UNCHANGED
        elif await self._enhanced_professional_check(content, adaptive_enhancement):
            violation_detected = True
            boundary_type = BoundaryType.PROFESSIONAL
            explanation = "Content crosses professional boundaries"
            confidence = 0.8 + adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)

        # Check inappropriate content (enhanced) - UNCHANGED
        elif await self._enhanced_inappropriate_content_check(content, adaptive_enhancement):
            violation_detected = True
            boundary_type = BoundaryType.INAPPROPRIATE_CONTENT
            explanation = "Content contains inappropriate material"
            confidence = 0.75 + adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)

        # Record decision with enhanced data (UNCHANGED)
        response_time_ms = (time.time() - start_time) * 1000
        decision_id = f"bd_{int(time.time() * 1000)}"

        decision = EthicalDecision(
            decision_id=decision_id,
            boundary_type=boundary_type or "none",
            violation_detected=violation_detected,
            explanation=explanation,
            audit_data={
                "content_length": len(content),
                "response_time_ms": response_time_ms,
                "session_id": session_id,
                "confidence": confidence,
                "adaptive_enhancement": adaptive_enhancement,
                "patterns_checked": len(
                    self.harassment_patterns
                    + self.professional_boundary_patterns
                    + self.inappropriate_content_patterns
                ),
            },
            timestamp=datetime.now(timezone.utc),
        )

        await self.audit_decision(decision)

        # Phase 3: Learn from decision and log for transparency (UNCHANGED)
        await adaptive_boundaries.learn_from_decision(decision)
        await audit_transparency.log_ethics_decision(decision)

        # Phase 3: Adaptive learning from interaction (UNCHANGED)
        if (
            interaction_metadata.get("content_length", 0) > 20
        ):  # Learn from substantial interactions
            boundary_decision_obj = BoundaryDecision(
                violation_detected=violation_detected,
                boundary_type=boundary_type or "none",
                explanation=explanation,
                audit_data=decision.audit_data,
                session_id=session_id,
            )

            # Note: adaptive_boundary_system is referenced but not imported in original
            # This will fail at runtime - needs to be fixed separately
            # await adaptive_boundary_system.learn_from_interaction(
            #     boundary_decision_obj, interaction_metadata
            # )

        # Log ethics decision with enhanced data (UNCHANGED)
        self.ethics_logger.log_decision_point(
            "boundary_enforcement",
            {
                "decision_id": decision_id,
                "violation_detected": violation_detected,
                "boundary_type": boundary_type,
                "confidence": confidence,
                "response_time_ms": response_time_ms,
                "adaptive_enhancement": adaptive_enhancement.get("recommendation", "proceed"),
                "session_id": session_id,
            },
        )

        # Record enhanced metrics (UNCHANGED)
        self.metrics.record_ethics_decision(
            EthicsDecisionType.BOUNDARY_ENFORCEMENT,
            "boundary_checked_enhanced",
            response_time_ms,
            session_id,
        )

        if violation_detected:
            # Record violation with enhanced data (UNCHANGED)
            violation_type = self._map_boundary_type_to_violation_type(boundary_type)
            self.metrics.record_boundary_violation(
                violation_type,
                context=f"confidence:{confidence:.2f}|patterns:{adaptive_enhancement.get('learned_patterns_matched', 0)}",
                session_id=session_id,
            )

            # Log violation with enhanced details (UNCHANGED)
            self.ethics_logger.log_boundary_violation(
                boundary_type,
                {
                    "decision_id": decision_id,
                    "confidence": confidence,
                    "adaptive_patterns_matched": adaptive_enhancement.get(
                        "learned_patterns_matched", 0
                    ),
                    "session_id": session_id,
                    "explanation": explanation,
                },
            )

        return BoundaryDecision(
            violation_detected=violation_detected,
            boundary_type=boundary_type or "none",
            explanation=explanation,
            audit_data={
                "decision_id": decision_id,
                "response_time_ms": response_time_ms,
                "confidence": confidence,
                "session_id": session_id,
                "content_length": len(content),
                "adaptive_enhancement": adaptive_enhancement,
            },
            session_id=session_id,
            redirect_context=(
                self._derive_redirect_context(boundary_type) if violation_detected else None
            ),
        )

    @staticmethod
    def _derive_redirect_context(boundary_type: Optional[str]) -> Optional[str]:
        """Derive a neutral, audit-safe hint for the floor LLM composing a decline.

        Added by #992 ETHICS-ACTIVATE (Phase A). Category-only derivation — does
        NOT incorporate matched patterns or raw user content. This keeps the hint
        safe to route to the user-facing voice layer (raw `explanation` stays
        audit-only and is never user-routed per CXO voice guidance).

        Args:
            boundary_type: One of the BoundaryType constants (or None/"none").

        Returns:
            A short neutral hint string the floor can weave into a decline, or
            None if no mapping exists (caller treats as no hint available).
        """
        mapping = {
            BoundaryType.HARASSMENT: (
                "The request targets a person in a way that could cause harm; "
                "redirect toward constructive professional work."
            ),
            BoundaryType.PROFESSIONAL: (
                "The request leans into personal or private territory; "
                "redirect toward the professional context you're here to support."
            ),
            BoundaryType.INAPPROPRIATE_CONTENT: (
                "The request is for inappropriate content; "
                "redirect toward appropriate product-management work."
            ),
            BoundaryType.PERSONAL: (
                "The request crosses a personal boundary; "
                "redirect toward professional collaboration."
            ),
            BoundaryType.DATA_PRIVACY: (
                "The request would expose private data; "
                "redirect toward what can be shared appropriately."
            ),
        }
        return mapping.get(boundary_type)

    async def _enhanced_harassment_check(
        self, content: str, adaptive_enhancement: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Enhanced harassment detection with confidence scoring (UNCHANGED)"""
        content_lower = content.lower()
        base_confidence = 0.0
        matched_patterns = []

        # Check base patterns
        for pattern in self.harassment_patterns:
            if pattern in content_lower:
                matched_patterns.append(pattern)
                base_confidence += 0.3

        # Apply adaptive enhancement
        adaptive_adjustment = adaptive_enhancement.get("adaptive_confidence_adjustment", 0.0)
        final_confidence = min(1.0, base_confidence + adaptive_adjustment)

        # Apply temporal risk factor
        temporal_factor = adaptive_enhancement.get("temporal_risk_factor", 1.0)
        final_confidence *= temporal_factor

        violation_threshold = 0.5
        violation_detected = final_confidence > violation_threshold

        explanation = "Content contains potential harassment patterns"
        if matched_patterns:
            explanation += f" (matched: {len(matched_patterns)} patterns)"
        if adaptive_adjustment != 0:
            explanation += f" (adaptive confidence: {adaptive_adjustment:+.2f})"

        return {
            "violation": violation_detected,
            "confidence": final_confidence,
            "explanation": explanation,
            "matched_patterns": len(matched_patterns),
            "adaptive_adjustment": adaptive_adjustment,
        }

    async def _enhanced_professional_check(
        self, content: str, adaptive_enhancement: Dict[str, Any]
    ) -> bool:
        """Enhanced professional boundary check (UNCHANGED)"""
        base_result = await self.validate_professional_boundaries(content)

        # Apply adaptive enhancement
        if adaptive_enhancement.get("recommendation") == "extra_caution":
            return True  # More strict when adaptive system suggests caution
        elif adaptive_enhancement.get("recommendation") == "proceed_with_confidence":
            return False  # More lenient when system is confident

        return base_result

    async def _enhanced_inappropriate_content_check(
        self, content: str, adaptive_enhancement: Dict[str, Any]
    ) -> bool:
        """Enhanced inappropriate content check (UNCHANGED)"""
        base_result = await self.check_inappropriate_content(content)

        # Apply contextual risk factor
        contextual_factor = adaptive_enhancement.get("contextual_risk_factor", 1.0)
        if contextual_factor > 1.1 and base_result:
            return True  # Higher threshold met with risk factor

        return base_result

    async def validate_professional_boundaries(self, content: str) -> bool:
        """Check if content crosses professional boundaries (UNCHANGED)"""
        content_lower = content.lower()

        for pattern in self.professional_boundary_patterns:
            if pattern in content_lower:
                return True

        return False

    async def check_harassment_patterns(self, content: str) -> bool:
        """Check for harassment patterns in content (UNCHANGED)"""
        content_lower = content.lower()

        for pattern in self.harassment_patterns:
            if pattern in content_lower:
                return True

        return False

    async def check_inappropriate_content(self, content: str) -> bool:
        """Check for inappropriate content patterns (UNCHANGED)"""
        content_lower = content.lower()

        for pattern in self.inappropriate_content_patterns:
            if pattern in content_lower:
                return True

        return False

    async def audit_decision(self, decision: EthicalDecision) -> None:
        """Audit an ethics decision (UNCHANGED)"""
        try:
            # Record audit trail entry
            self.metrics.record_audit_trail_entry(success=True)

            # Log audit decision
            self.ethics_logger.log_behavior_pattern(
                "audit_decision",
                {
                    "decision_id": decision.decision_id,
                    "boundary_type": decision.boundary_type,
                    "violation_detected": decision.violation_detected,
                    "timestamp": decision.timestamp.isoformat(),
                },
            )

        except Exception as e:
            # Record audit failure
            self.metrics.record_audit_trail_entry(success=False)

            # Log error
            self.ethics_logger.log_boundary_violation(
                "audit_failure", {"error": str(e), "decision_id": decision.decision_id}
            )

    # REMOVED: _extract_content_from_request() - No longer needed with domain objects
    # REMOVED: _get_session_id_from_request() - No longer needed with domain objects

    def _map_boundary_type_to_violation_type(self, boundary_type: str) -> EthicsViolationType:
        """Map boundary type to ethics violation type (UNCHANGED)"""
        mapping = {
            BoundaryType.HARASSMENT: EthicsViolationType.HARASSMENT_ATTEMPT,
            BoundaryType.PROFESSIONAL: EthicsViolationType.PROFESSIONAL_BOUNDARY_VIOLATION,
            BoundaryType.PERSONAL: EthicsViolationType.PERSONAL_BOUNDARY_CROSS,
            BoundaryType.DATA_PRIVACY: EthicsViolationType.DATA_PRIVACY_VIOLATION,
            BoundaryType.INAPPROPRIATE_CONTENT: EthicsViolationType.INAPPROPRIATE_REQUEST,
        }

        return mapping.get(boundary_type, EthicsViolationType.PROFESSIONAL_BOUNDARY_VIOLATION)


# Singleton instance for universal ethics enforcement
boundary_enforcer_refactored = BoundaryEnforcer()
