"""
Preference Detection Models and Hints

PreferenceHint: Detected preference signal from conversation
PreferenceConfirmation: User-confirmed preference change
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID

from services.personality.personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    TechnicalPreference,
)

# ── The confidence gate's thresholds, hoisted to named constants (#1510) ──
# These are THE shared inference-confidence gate for the cohort: PM's 2026-08-13
# ruling on #1510 (relayed by Exec) directed the verified-inference mechanism to
# EXTEND this existing confidence_score gate rather than build a parallel
# scoring system. `services/intent_service/verified_inference.py` imports these
# same constants — one gate, two consumers, no drift surface. Values unchanged
# from the original inline literals (auto-apply ≥0.9 / suggest ≥0.4).
AUTO_APPLY_THRESHOLD = 0.9
"""Confidence at/above which an inference may be applied without asking."""

SUGGESTION_THRESHOLD = 0.4
"""Confidence floor below which an inference is too weak to even surface."""


class PreferenceDimension(Enum):
    """The 4 dimensions of user preference we detect"""

    WARMTH = "warmth_level"  # How warm/friendly vs professional
    CONFIDENCE = "confidence_style"  # How confidence should be displayed
    ACTION = "action_orientation"  # How action-oriented responses should be
    TECHNICAL = "technical_depth"  # Level of technical detail


class DetectionMethod(Enum):
    """How preference was detected"""

    LANGUAGE_PATTERNS = "language_patterns"  # From word choice/phrasing
    EXPLICIT_FEEDBACK = "explicit_feedback"  # User said they prefer this
    BEHAVIORAL_SIGNALS = "behavioral_signals"  # Inferred from actions
    COMMAND_FREQUENCY = "command_frequency"  # Pattern in command usage
    RESPONSE_PATTERNS = "response_patterns"  # Pattern in response modifications


class ConfidenceLevel(Enum):
    """Confidence that detected preference is accurate"""

    LOW = "low"  # 0.0-0.4 - Weak signal, needs more data
    MEDIUM = "medium"  # 0.4-0.7 - Moderate signal, appears consistent
    HIGH = "high"  # 0.7-0.9 - Strong signal, multiple confirmations
    VERY_HIGH = "very_high"  # 0.9-1.0 - Explicit user confirmation


@dataclass
class PreferenceHint:
    """
    A detected signal that user may have a preference.

    Hints are NOT yet stored in PersonalityProfile - they're observations
    waiting for either:
    1. Automatic application when confidence is very high
    2. User confirmation to convert to PreferenceConfirmation
    """

    id: str  # Unique hint ID
    user_id: str
    dimension: PreferenceDimension
    detected_value: Any  # The value we think they prefer
    current_value: Any  # Their current profile value
    detection_method: DetectionMethod
    confidence_score: float  # 0.0-1.0
    source_text: str  # The conversation excerpt that triggered detection
    evidence: Dict[str, Any] = field(
        default_factory=dict
    )  # Supporting data (e.g., word counts, patterns)
    created_at: datetime = field(default_factory=datetime.now)
    expires_at: Optional[datetime] = None  # When hint becomes stale if not confirmed

    def __post_init__(self):
        """Validate hint constraints"""
        if not (0.0 <= self.confidence_score <= 1.0):
            raise ValueError(f"confidence_score must be 0.0-1.0, got {self.confidence_score}")

    def confidence_level(self) -> ConfidenceLevel:
        """Classify confidence into categories"""
        if self.confidence_score >= AUTO_APPLY_THRESHOLD:
            return ConfidenceLevel.VERY_HIGH
        elif self.confidence_score >= 0.7:
            return ConfidenceLevel.HIGH
        elif self.confidence_score >= SUGGESTION_THRESHOLD:
            return ConfidenceLevel.MEDIUM
        else:
            return ConfidenceLevel.LOW

    def is_ready_for_suggestion(self) -> bool:
        """Should we suggest this preference to user?"""
        # Only suggest if confidence is MEDIUM or higher
        return self.confidence_score >= SUGGESTION_THRESHOLD

    def is_ready_for_auto_apply(self) -> bool:
        """Can we automatically apply this preference?"""
        # Only auto-apply if confidence is VERY_HIGH (0.9+)
        # and it's explicit feedback or behavioral signal (strong evidence)
        return self.confidence_score >= AUTO_APPLY_THRESHOLD and self.detection_method in (
            DetectionMethod.EXPLICIT_FEEDBACK,
            DetectionMethod.BEHAVIORAL_SIGNALS,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "dimension": self.dimension.value,
            "detected_value": str(self.detected_value),
            "current_value": str(self.current_value),
            "detection_method": self.detection_method.value,
            "confidence_score": self.confidence_score,
            "confidence_level": self.confidence_level().value,
            "source_text": self.source_text,
            "is_ready_for_suggestion": self.is_ready_for_suggestion(),
            "is_ready_for_auto_apply": self.is_ready_for_auto_apply(),
            "created_at": self.created_at.isoformat(),
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
        }


@dataclass
class PreferenceConfirmation:
    """
    User has confirmed a preference change.

    This is the result of:
    1. Suggesting a preference hint to user
    2. User explicitly accepting it
    3. Converting to this confirmation for storage

    This gets stored in UserPreferenceManager with key: f"personality_{dimension}"
    """

    id: str  # Unique confirmation ID
    user_id: str
    dimension: PreferenceDimension
    new_value: Any  # The value to apply (from hint.detected_value)
    previous_value: Any  # Their previous profile value
    hint_id: str  # Reference to the PreferenceHint that triggered this
    confirmation_source: str  # "user_explicit", "auto_apply", "learning_system"
    confirmed_at: datetime = field(default_factory=datetime.now)
    applied_at: Optional[datetime] = None  # When it was actually applied to profile

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "dimension": self.dimension.value,
            "new_value": str(self.new_value),
            "previous_value": str(self.previous_value),
            "hint_id": self.hint_id,
            "confirmation_source": self.confirmation_source,
            "confirmed_at": self.confirmed_at.isoformat(),
            "applied_at": self.applied_at.isoformat() if self.applied_at else None,
        }


@dataclass
class PreferenceDetectionResult:
    """
    Result of analyzing conversation for preference hints.

    This is what ConversationAnalyzer returns after each analysis.
    """

    hints: list[PreferenceHint] = field(default_factory=list)  # Newly detected hints
    analysis_summary: str = ""  # Human-readable summary of what was detected
    confidence_summary: Dict[PreferenceDimension, float] = field(
        default_factory=dict
    )  # Confidence scores per dimension
    suggested_hints: list[PreferenceHint] = field(
        default_factory=list
    )  # Hints ready for user suggestion
    auto_apply_hints: list[PreferenceHint] = field(
        default_factory=list
    )  # Hints confident enough to auto-apply
    detected_at: datetime = field(default_factory=datetime.now)

    def has_suggestions(self) -> bool:
        """Are there hints to suggest to user?"""
        return len(self.suggested_hints) > 0

    def has_auto_applies(self) -> bool:
        """Are there hints confident enough to auto-apply?"""
        return len(self.auto_apply_hints) > 0

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary"""
        return {
            "hints": [h.to_dict() for h in self.hints],
            "analysis_summary": self.analysis_summary,
            "confidence_summary": {
                dim.value: score for dim, score in self.confidence_summary.items()
            },
            "suggested_hints": [h.to_dict() for h in self.suggested_hints],
            "auto_apply_hints": [h.to_dict() for h in self.auto_apply_hints],
            "has_suggestions": self.has_suggestions(),
            "has_auto_applies": self.has_auto_applies(),
            "detected_at": self.detected_at.isoformat(),
        }
