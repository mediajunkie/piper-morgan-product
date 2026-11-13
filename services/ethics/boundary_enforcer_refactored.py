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
from services.ethics.audit_transparency import audit_transparency
from services.ethics.semantic_boundary_detector import (
    AMBIGUOUS_THRESHOLD,
    BLOCK_THRESHOLD,
    REFUSAL_FALLBACK,
    SEMANTIC_DETECTOR_PROMPT_V0_2,
    SemanticBoundaryDetector,
    SemanticDetectorOutput,
    classify_decision,
    is_unavailable,
)
from services.infrastructure.logging.config import get_ethics_logger
from services.infrastructure.monitoring.ethics_metrics import (
    EthicsDecisionType,
    EthicsMetrics,
    EthicsViolationType,
    ethics_metrics,
)

# REMOVED: from fastapi import Request (Line 21 in original)

# The detector prompt the served enforcer uses (#2364). v0.2 is CXO's calibrated
# body (2026-04-27). Changing this needs a live run of the probe set first.
LIVE_SEMANTIC_PROMPT = SEMANTIC_DETECTOR_PROMPT_V0_2


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

    def __init__(
        self,
        semantic_detector: Optional[SemanticBoundaryDetector] = None,
        enable_semantic: bool = True,
    ):
        self.ethics_logger = get_ethics_logger(__name__)
        self.metrics = ethics_metrics

        # #1004 Fix B — semantic detector (lazy-injectable for tests). It is the only
        # layer that decides a boundary (#2364): `enable_semantic=False` means nothing
        # is checked. On first real call we lazy-initialize so module import doesn't
        # require an LLM client to be present in test environments.
        self._enable_semantic = enable_semantic
        self._semantic_detector = semantic_detector

        # Substring lists. #2364 (Arch, 2026-11-13): these no longer decide a turn in
        # `enforce_boundaries`; a substring declined "home page" and "private repo"
        # before the semantic detector saw the message. They stay for one reader, the
        # knowledge graph's privacy level (`check_harassment_patterns`,
        # `check_inappropriate_content`; #1089, and #2365 for that reader's own question).
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

        # Perform boundary checks
        # #1019 (Path C, May 2026): adaptive_boundaries scaffolding removed —
        # learned patterns never influenced enforcement (always-zero adjustment).
        # Substrate for any future learning loop is the #1004 semantic detector;
        # framework-level learning will be revisited under #1016.
        violation_detected = False
        boundary_type = None

        explanation = ""
        confidence = 0.0

        # #1004 Fix B — semantic detector dispatch. #2364: it runs for every message;
        # the substring fast path that used to run first, and skip it on a hit, is
        # gone. Confidence tiering: ≥BLOCK_THRESHOLD → block / AMBIGUOUS_THRESHOLD–BLOCK
        # → ambiguous-pass / <AMBIGUOUS → pass. Per contract §"New internal flow".
        semantic_output: Optional[SemanticDetectorOutput] = None
        cache_hit = False
        if self._enable_semantic:
            detector_instance = self._get_semantic_detector()
            if detector_instance is None:
                # #2134 edge (Arch 14:30): enabled but the detector failed to build: the
                # layer did not run, so it records "unavailable", never "pass".
                semantic_output = REFUSAL_FALLBACK
            if detector_instance is not None:
                cache_hit = detector_instance.cache_lookup(content)
                semantic_output = await detector_instance.detect(content, context=context)
                if (
                    semantic_output.violation_detected
                    and semantic_output.confidence >= BLOCK_THRESHOLD
                    and semantic_output.category != "none"
                ):
                    violation_detected = True
                    boundary_type = self._semantic_category_to_boundary_type(
                        semantic_output.category
                    )
                    explanation = semantic_output.reasoning
                    confidence = semantic_output.confidence

        # Record decision with enhanced data (UNCHANGED)
        response_time_ms = (time.time() - start_time) * 1000
        decision_id = f"bd_{int(time.time() * 1000)}"

        # #1004 Fix C1 — detector marker: which detection path engaged. Since #2364
        # the values are "semantic", "semantic-unavailable" and "none".
        if is_unavailable(semantic_output):
            # #2134: the semantic layer did not run; never recorded as "none"
            detector = "semantic-unavailable"
        elif (
            semantic_output is not None
            and semantic_output.violation_detected
            and semantic_output.confidence >= BLOCK_THRESHOLD
            and semantic_output.category != "none"
        ):
            detector = "semantic"
        else:
            detector = "none"

        # #1004 contract — decision tier on the audit envelope (telemetry-ready).
        if is_unavailable(semantic_output):
            # #2134 (Arch): a failure is not a reading; "pass" would hide it in the envelope
            decision_tier = "unavailable"
        elif semantic_output is not None:
            decision_tier = classify_decision(semantic_output.confidence)
        else:
            decision_tier = "pass"

        semantic_confidence = semantic_output.confidence if semantic_output is not None else None
        semantic_reasoning = semantic_output.reasoning if semantic_output is not None else None
        semantic_redirect_hint = (
            semantic_output.redirect_hint if semantic_output is not None else None
        )

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
                "detector": detector,
                "decision_tier": decision_tier,
                "semantic_confidence": semantic_confidence,
                "semantic_reasoning": semantic_reasoning,
                "cache_hit": cache_hit,
            },
            timestamp=datetime.now(timezone.utc),
        )

        await self.audit_decision(decision)

        # #1019 (Path C): adaptive_boundaries.learn_from_decision removed —
        # the learning loop's outputs were never read by enforcement.
        await audit_transparency.log_ethics_decision(decision)

        # #1004 Telemetry Phase 1 — structured boundary_enforcement emission.
        # Per contract §"Telemetry Phase 1 (ships with B)": every call gets the
        # full discriminator set so operators can slice by detector path,
        # decision tier, and cache hit. Phase 2 (FLOOR_IMPLICIT_ETHICS counter)
        # ships separately within ~2 weeks of Phase 1.
        self.ethics_logger.log_decision_point(
            "boundary_enforcement",
            {
                "decision_id": decision_id,
                "session_id": session_id,
                "detector": detector,
                "violation_detected": violation_detected,
                "boundary_type": boundary_type,
                "decision_tier": decision_tier,
                "confidence": confidence,
                "semantic_confidence": semantic_confidence,
                "latency_ms": response_time_ms,
                "cache_hit": cache_hit,
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
                context=f"confidence:{confidence:.2f}",
                session_id=session_id,
            )

            # Log violation with details
            self.ethics_logger.log_boundary_violation(
                boundary_type,
                {
                    "decision_id": decision_id,
                    "confidence": confidence,
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
                "detector": detector,
                "decision_tier": decision_tier,
                "semantic_confidence": semantic_confidence,
                "semantic_reasoning": semantic_reasoning,
                "cache_hit": cache_hit,
            },
            session_id=session_id,
            redirect_context=self._compute_redirect_context(
                violation_detected,
                detector,
                boundary_type,
                semantic_redirect_hint,
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

    # ------------------------------------------------------------------
    # #1004 Fix B helpers
    # ------------------------------------------------------------------

    def _get_semantic_detector(self) -> Optional[SemanticBoundaryDetector]:
        """Lazy-initialize the semantic detector on the live prompt. Returns None on
        init failure; the caller records the layer as unavailable (#2134)."""
        if self._semantic_detector is not None:
            return self._semantic_detector
        try:
            # #2364: the prompt is passed here, not left to the constructor's default.
            # The default stayed on v0.1 from April to November while v0.2 was the
            # calibrated one; the pin asserts the prompt on this built instance.
            self._semantic_detector = SemanticBoundaryDetector(prompt=LIVE_SEMANTIC_PROMPT)
            return self._semantic_detector
        except Exception as exc:  # noqa: BLE001
            self.ethics_logger.log_decision_point(
                "semantic_detector_init_failure",
                {"error": str(exc), "exc_type": type(exc).__name__},
            )
            return None

    @staticmethod
    def _semantic_category_to_boundary_type(category: str) -> Optional[str]:
        """Map a SemanticDetectorOutput category to the BoundaryType constant."""
        mapping = {
            "harassment": BoundaryType.HARASSMENT,
            "professional": BoundaryType.PROFESSIONAL,
            "personal": BoundaryType.PERSONAL,
            "data_privacy": BoundaryType.DATA_PRIVACY,
            "inappropriate_content": BoundaryType.INAPPROPRIATE_CONTENT,
            "none": None,
        }
        return mapping.get(category)

    def _compute_redirect_context(
        self,
        violation_detected: bool,
        detector: str,
        boundary_type: Optional[str],
        semantic_hint: Optional[str],
    ) -> Optional[str]:
        """Choose redirect_context source.

        Per Architect's prompt-body-ack observation (memo 2026-04-26): the LLM-
        produced hint is acceptable because (a) the prompt enumerates the
        no-quoting / no-pattern-name / no-template-phrase rules and (b) the
        probe set asserts those properties at CI time.
        """
        if not violation_detected:
            return None
        if detector == "semantic" and semantic_hint:
            return semantic_hint
        return self._derive_redirect_context(boundary_type)

    async def check_harassment_patterns(self, content: str) -> bool:
        """Substring check, read only by the knowledge graph's privacy level (#1089)."""
        content_lower = content.lower()

        for pattern in self.harassment_patterns:
            if pattern in content_lower:
                return True

        return False

    async def check_inappropriate_content(self, content: str) -> bool:
        """Substring check, read only by the knowledge graph's privacy level (#1089)."""
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
