"""
Standup Preference Models - User Preference Learning System

Issue #555: STANDUP-LEARNING - User Preference Learning
Epic #242: CONV-MCP-STANDUP-INTERACTIVE

Defines typed preference schema for standup conversations.
Follows DDD patterns from services/domain/models.py.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4


class PreferenceType(Enum):
    """Types of standup preferences.

    PM Decision (2026-01-08): 5 initial categories.
    """

    CONTENT_FILTER = "content_filter"  # "focus on GitHub", "prioritize X"
    EXCLUSION = "exclusion"  # "skip docs", "ignore tests"
    FORMAT = "format"  # "brief", "detailed", "bullet points"
    TIMING = "timing"  # "morning at 9am", "daily", "weekly"
    NOTIFICATION = "notification"  # "notify via Slack", "email summary"


class PreferenceSource(Enum):
    """How the preference was determined."""

    EXPLICIT = "explicit"  # User stated directly: "focus on GitHub"
    INFERRED = "inferred"  # System detected from behavior patterns
    CORRECTED = "corrected"  # User corrected a previous inference


@dataclass
class UserStandupPreference:
    """
    Individual user preference for standup conversations.

    Follows DDD @dataclass pattern from services/domain/models.py.
    Designed for database persistence (Phase 2).

    Examples:
        - focus=github (content_filter)
        - exclude=["docs", "tests"] (exclusion)
        - format=brief (format)
        - schedule=09:00 (timing)
        - channel=slack (notification)
    """

    # Identity
    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: str = ""

    # Preference specification
    preference_type: PreferenceType = PreferenceType.CONTENT_FILTER
    key: str = ""  # "focus", "exclude", "format", "schedule", "channel"
    value: Any = None  # "github", ["docs", "tests"], "brief", "09:00", "slack"

    # Confidence and source
    confidence: float = 0.7  # 0.0 - 1.0 (new preferences start at 0.7)
    source: PreferenceSource = PreferenceSource.EXPLICIT

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Version tracking for conflict resolution
    version: int = 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON/database serialization."""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "preference_type": self.preference_type.value,
            "key": self.key,
            "value": self.value,
            "confidence": self.confidence,
            "source": self.source.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "version": self.version,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "UserStandupPreference":
        """Create from dictionary (JSON/database deserialization)."""
        return cls(
            id=data.get("id", str(uuid4())),
            user_id=data.get("user_id", ""),
            preference_type=PreferenceType(data.get("preference_type", "content_filter")),
            key=data.get("key", ""),
            value=data.get("value"),
            confidence=data.get("confidence", 0.7),
            source=PreferenceSource(data.get("source", "explicit")),
            created_at=(
                datetime.fromisoformat(data["created_at"])
                if data.get("created_at")
                else datetime.now()
            ),
            updated_at=(
                datetime.fromisoformat(data["updated_at"])
                if data.get("updated_at")
                else datetime.now()
            ),
            version=data.get("version", 1),
        )

    def boost_confidence(self, amount: float = 0.1) -> None:
        """Increase confidence when preference is confirmed."""
        self.confidence = min(1.0, self.confidence + amount)
        self.updated_at = datetime.now()
        self.version += 1

    def reduce_confidence(self, amount: float = 0.15) -> None:
        """Decrease confidence when preference is corrected."""
        self.confidence = max(0.0, self.confidence - amount)
        self.updated_at = datetime.now()
        self.version += 1

    def is_high_confidence(self, threshold: float = 0.8) -> bool:
        """Check if preference has high enough confidence to apply automatically."""
        return self.confidence >= threshold

    def needs_confirmation(self, threshold: float = 0.5) -> bool:
        """Check if preference confidence is low enough to prompt user."""
        return self.confidence < threshold

    def is_low_confidence(self) -> bool:
        """#1510 read-back trigger (PM ruling via Exec 2026-08-13): is this
        preference's confidence low enough that Piper should read the
        inference back to the user for verification before relying on it?

        NOTE (resurrection with a correction): #1510's ruling comment named
        this method as "already-defined-but-unused" — it did not in fact
        exist under this name; ``needs_confirmation()`` above was the nearest
        analog. Defined here as the ruling intended, delegating to the SHARED
        confidence gate (services/personality/preference_detection.py
        thresholds via services/intent_service/verified_inference.py) so the
        standup consumer (#1591) and every other consumer ask one gate, not
        two. Lazy import: keeps this dataclass module dependency-free at
        import time.
        """
        from services.intent_service.verified_inference import is_low_confidence

        return is_low_confidence(self.confidence)


@dataclass
class PreferenceChange:
    """
    Record of a preference change for history tracking.

    Enables preference history retrieval (Phase 2 requirement).
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    preference_id: str = ""
    user_id: str = ""

    # What changed
    previous_value: Any = None
    new_value: Any = None
    previous_confidence: float = 0.0
    new_confidence: float = 0.0

    # Why it changed
    change_reason: str = ""  # "user_correction", "repetition", "inference"
    session_id: Optional[str] = None

    # When
    changed_at: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON/database serialization."""
        return {
            "id": self.id,
            "preference_id": self.preference_id,
            "user_id": self.user_id,
            "previous_value": self.previous_value,
            "new_value": self.new_value,
            "previous_confidence": self.previous_confidence,
            "new_confidence": self.new_confidence,
            "change_reason": self.change_reason,
            "session_id": self.session_id,
            "changed_at": self.changed_at.isoformat() if self.changed_at else None,
        }


@dataclass
class ExtractedPreference:
    """
    Result of preference extraction from a conversation turn.

    Used by PreferenceExtractor to return parsed preferences.
    """

    raw_text: str = ""  # Original user message
    preference_type: PreferenceType = PreferenceType.CONTENT_FILTER
    key: str = ""
    value: Any = None
    confidence: float = 0.7
    source: PreferenceSource = PreferenceSource.EXPLICIT

    # Whether this is a temporary override ("just for today")
    is_temporary: bool = False

    def to_preference(self, user_id: str) -> UserStandupPreference:
        """Convert extracted preference to storable preference."""
        return UserStandupPreference(
            user_id=user_id,
            preference_type=self.preference_type,
            key=self.key,
            value=self.value,
            confidence=self.confidence,
            source=self.source,
        )
