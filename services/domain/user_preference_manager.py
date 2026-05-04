"""
UserPreferenceManager - Persistent Context Foundation
Phase 1: Core Infrastructure Implementation

Created: 2025-08-20 by Enhanced Autonomy Mission
Follows Excellence Flywheel: Tests First → Implementation → Evidence-based progress
"""

import asyncio
import json
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from zoneinfo import ZoneInfo, available_timezones

from services.session.session_manager import ConversationSession

# ============================================================================
# Reminder Preference Keys (Issue #161 Task 2)
# ============================================================================

STANDUP_REMINDER_ENABLED = "standup_reminder_enabled"
"""Whether daily standup reminders are enabled for this user (bool, default: True)"""

STANDUP_REMINDER_TIME = "standup_reminder_time"
"""Time of day to send reminder in HH:MM format (str, default: "06:00")"""

STANDUP_REMINDER_TIMEZONE = "standup_reminder_timezone"
"""IANA timezone name for reminder time (str, default: "America/Los_Angeles")"""

STANDUP_REMINDER_DAYS = "standup_reminder_days"
"""Days of week to send reminders, 0=Monday, 6=Sunday (List[int], default: [0,1,2,3,4])"""

# ============================================================================
# Learning Preference Keys (Issue #221 CORE-LEARN-A)
# ============================================================================

LEARNING_ENABLED = "learning_enabled"
"""Whether pattern learning is enabled for this user (bool, default: True)"""

LEARNING_MIN_CONFIDENCE = "learning_min_confidence"
"""Minimum confidence threshold for pattern application (float 0.0-1.0, default: 0.5)"""

LEARNING_FEATURES = "learning_features"
"""List of features enabled for learning (List[str], default: [])"""

# ============================================================================
# Calendar Setup Offer Preference Key (Issue #790 MVP trust-gated calendar)
# ============================================================================

CALENDAR_SETUP_OFFERED = "calendar_setup_offered"
"""Tracks whether and how the user has been offered calendar setup help.

States:
    None         — never offered (default)
    "offered"    — offer was presented; awaiting user reaction
    "declined"   — user said no thanks; stay silent unless they ask
    "deferred"   — user said maybe later / not now; stay silent unless they ask
    "accepted"   — user said yes; setup help was provided

Issue #790 trust-gated calendar offer.
"""

CALENDAR_OFFER_STATES = frozenset({"offered", "declined", "deferred", "accepted"})
"""Valid non-None values for CALENDAR_SETUP_OFFERED."""

# ============================================================================
# Default Repo Preference Key (Issue #1042 PRE-1039 hardcoded-repo cleanup)
# ============================================================================

DEFAULT_REPO = "default_repo"
"""User's default GitHub repo as 'owner/name' string.

Used by repo_resolver when no project context is available. Issue #1042
removes hardcoded 'piper-morgan-product' / 'mediajunkie' fallbacks; this
preference is one of the resolution paths (project-scoped → user default →
env-var → UnresolvedRepoError).

UI for setting this preference is folded into #869 (Project config IA) per
PM Q6 disposition 2026-05-04.
"""


@dataclass
class PreferenceItem:
    """Individual preference item with versioning and metadata"""

    value: Any
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    version: datetime = field(default_factory=datetime.now)
    ttl_minutes: Optional[int] = None

    def is_expired(self) -> bool:
        """Check if preference has expired based on TTL"""
        if self.ttl_minutes is None:
            return False
        expiry = self.created_at + timedelta(minutes=self.ttl_minutes)
        return datetime.now() > expiry

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            "value": self.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "version": self.version.isoformat(),
            "ttl_minutes": self.ttl_minutes,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "PreferenceItem":
        """Create from dictionary (JSON deserialization)"""
        return cls(
            value=data["value"],
            created_at=datetime.fromisoformat(data["created_at"]),
            updated_at=datetime.fromisoformat(data["updated_at"]),
            version=datetime.fromisoformat(data["version"]),
            ttl_minutes=data.get("ttl_minutes"),
        )


class UserPreferenceManager:
    """
    Manages user preferences with hierarchical inheritance and persistence.

    Hierarchy: Global → User → Session (session overrides user overrides global)
    Storage: JSON-based using existing ConversationSession.context patterns
    """

    def __init__(self):
        """Initialize preference manager with in-memory storage"""
        # In-memory storage (would be replaced with database persistence)
        self.global_preferences: Dict[str, PreferenceItem] = {}
        self.user_preferences: Dict[str, Dict[str, PreferenceItem]] = {}  # user_id -> preferences
        self.session_preferences: Dict[
            str, Dict[str, PreferenceItem]
        ] = {}  # session_id -> preferences

        # Concurrent access protection
        self._locks: Dict[str, asyncio.Lock] = {}

    def _get_lock(self, key: str) -> asyncio.Lock:
        """Get or create lock for concurrent access protection"""
        if key not in self._locks:
            self._locks[key] = asyncio.Lock()
        return self._locks[key]

    async def set_preference(
        self,
        key: str,
        value: Any,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        scope: Optional[str] = None,
        ttl_minutes: Optional[int] = None,
    ) -> bool:
        """
        Set a preference at the appropriate scope level.

        Args:
            key: Preference key
            value: Preference value (must be JSON serializable)
            user_id: User ID for user-scoped preferences
            session_id: Session ID for session-scoped preferences
            scope: Explicit scope ("global", "user", "session")
            ttl_minutes: Time-to-live in minutes (for session preferences)

        Returns:
            bool: True if preference was set successfully
        """
        lock_key = f"{scope or 'auto'}:{user_id or 'none'}:{session_id or 'none'}:{key}"
        async with self._get_lock(lock_key):
            try:
                # Validate value is JSON serializable
                json.dumps(value)

                preference_item = PreferenceItem(value=value, ttl_minutes=ttl_minutes)

                # Determine scope
                if scope == "global" or (not user_id and not session_id):
                    self.global_preferences[key] = preference_item
                elif session_id:
                    if session_id not in self.session_preferences:
                        self.session_preferences[session_id] = {}
                    self.session_preferences[session_id][key] = preference_item
                elif user_id:
                    if user_id not in self.user_preferences:
                        self.user_preferences[user_id] = {}
                    self.user_preferences[user_id][key] = preference_item
                else:
                    # Default to global if no scope specified
                    self.global_preferences[key] = preference_item

                return True

            except (TypeError, ValueError) as e:
                # Value not JSON serializable
                return False

    async def get_preference(
        self,
        key: str,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        scope: Optional[str] = None,
        default: Any = None,
    ) -> Any:
        """
        Get a preference with hierarchical inheritance.

        Priority: Session > User > Global > Default

        Args:
            key: Preference key
            user_id: User ID for context
            session_id: Session ID for context
            scope: Explicit scope to check ("global", "user", "session")
            default: Default value if preference not found

        Returns:
            Preference value or default
        """
        # Clean up expired preferences first
        await self._cleanup_expired_preferences()

        # If explicit scope requested, only check that scope
        if scope == "global":
            item = self.global_preferences.get(key)
            return item.value if item and not item.is_expired() else default
        elif scope == "user" and user_id:
            user_prefs = self.user_preferences.get(user_id, {})
            item = user_prefs.get(key)
            return item.value if item and not item.is_expired() else default
        elif scope == "session" and session_id:
            session_prefs = self.session_preferences.get(session_id, {})
            item = session_prefs.get(key)
            return item.value if item and not item.is_expired() else default

        # Hierarchical lookup: Session → User → Global → Default
        if session_id:
            session_prefs = self.session_preferences.get(session_id, {})
            item = session_prefs.get(key)
            if item and not item.is_expired():
                return item.value

        if user_id:
            user_prefs = self.user_preferences.get(user_id, {})
            item = user_prefs.get(key)
            if item and not item.is_expired():
                return item.value

        # Check global preferences
        item = self.global_preferences.get(key)
        if item and not item.is_expired():
            return item.value

        return default

    async def get_all_preferences(
        self, user_id: Optional[UUID] = None, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get all preferences for a user/session context.

        Returns merged preferences with hierarchy applied.
        """
        await self._cleanup_expired_preferences()

        result = {}

        # Start with global preferences
        for key, item in self.global_preferences.items():
            if not item.is_expired():
                result[key] = item.value

        # Apply user preferences (override global)
        if user_id and user_id in self.user_preferences:
            for key, item in self.user_preferences[user_id].items():
                if not item.is_expired():
                    result[key] = item.value

        # Apply session preferences (override user and global)
        if session_id and session_id in self.session_preferences:
            for key, item in self.session_preferences[session_id].items():
                if not item.is_expired():
                    result[key] = item.value

        return result

    async def merge_preferences(self, user_id: UUID, session_id: str) -> Dict[str, Any]:
        """
        Merge preferences with full hierarchy for a specific user/session.

        Args:
            user_id: User identifier
            session_id: Session identifier

        Returns:
            Merged preferences dictionary
        """
        return await self.get_all_preferences(user_id=user_id, session_id=session_id)

    async def clear_session_preferences(self, session_id: str) -> bool:
        """
        Clear all preferences for a specific session.

        Args:
            session_id: Session identifier

        Returns:
            True if preferences were cleared
        """
        if session_id in self.session_preferences:
            del self.session_preferences[session_id]

        # Clean up any locks for this session
        lock_keys_to_remove = [key for key in self._locks.keys() if f":{session_id}:" in key]
        for key in lock_keys_to_remove:
            del self._locks[key]

        return True

    async def get_preference_version(
        self, key: str, user_id: Optional[UUID] = None, session_id: Optional[str] = None
    ) -> Optional[datetime]:
        """
        Get the version (last updated timestamp) of a preference.

        Args:
            key: Preference key
            user_id: User ID for context
            session_id: Session ID for context

        Returns:
            Version timestamp or None if preference doesn't exist
        """
        # Check session first, then user, then global
        if session_id and session_id in self.session_preferences:
            item = self.session_preferences[session_id].get(key)
            if item:
                return item.version

        if user_id and user_id in self.user_preferences:
            item = self.user_preferences[user_id].get(key)
            if item:
                return item.version

        item = self.global_preferences.get(key)
        return item.version if item else None

    async def set_preference_with_version(
        self,
        key: str,
        value: Any,
        user_id: Optional[UUID] = None,
        session_id: Optional[str] = None,
        expected_version: Optional[datetime] = None,
    ) -> bool:
        """
        Set preference with version conflict detection.

        Args:
            key: Preference key
            value: New preference value
            user_id: User ID for context
            session_id: Session ID for context
            expected_version: Expected current version for conflict detection

        Returns:
            True if preference was set, False if version conflict
        """
        if expected_version:
            current_version = await self.get_preference_version(key, user_id, session_id)
            if current_version and current_version != expected_version:
                # Version conflict - could implement conflict resolution here
                # For now, we'll allow the update (last write wins)
                pass

        return await self.set_preference(key, value, user_id, session_id)

    async def is_preference_expired(self, key: str, session_id: Optional[str] = None) -> bool:
        """
        Check if a preference has expired (mainly for session preferences with TTL).

        Args:
            key: Preference key
            session_id: Session ID for context

        Returns:
            True if preference exists and is expired
        """
        if session_id and session_id in self.session_preferences:
            item = self.session_preferences[session_id].get(key)
            if item:
                return item.is_expired()

        return False

    async def get_context_format(
        self, user_id: Optional[UUID] = None, session_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get preferences in ConversationSession.context compatible format.

        Args:
            user_id: User ID for context
            session_id: Session ID for context

        Returns:
            Context-compatible dictionary
        """
        await self._cleanup_expired_preferences()

        context_data = {
            "global_preferences": {},
            "user_preferences": {},
            "session_preferences": {},
            "context_version": "1.0",
            "last_updated": datetime.now().isoformat(),
        }

        # Global preferences
        for key, item in self.global_preferences.items():
            if not item.is_expired():
                context_data["global_preferences"][key] = item.value

        # User preferences
        if user_id and user_id in self.user_preferences:
            for key, item in self.user_preferences[user_id].items():
                if not item.is_expired():
                    context_data["user_preferences"][key] = item.value

        # Session preferences
        if session_id and session_id in self.session_preferences:
            for key, item in self.session_preferences[session_id].items():
                if not item.is_expired():
                    context_data["session_preferences"][key] = item.value

        return context_data

    async def update_session_context(
        self, session: ConversationSession, user_id: Optional[UUID] = None
    ) -> bool:
        """
        Update ConversationSession.context with current preferences.

        Args:
            session: ConversationSession instance to update
            user_id: User ID for preference context

        Returns:
            True if context was updated successfully
        """
        try:
            context_data = await self.get_context_format(
                user_id=user_id, session_id=session.session_id
            )

            # Merge with existing context (preserve non-preference data)
            session.context.update(context_data)

            return True

        except Exception:
            return False

    async def load_from_session_context(self, session: ConversationSession) -> bool:
        """
        Load preferences from existing ConversationSession.context.

        Args:
            session: ConversationSession instance to load from

        Returns:
            True if preferences were loaded successfully
        """
        try:
            context = session.context

            # Load global preferences
            if "global_preferences" in context:
                for key, value in context["global_preferences"].items():
                    await self.set_preference(key, value, scope="global")

            # Load user preferences (need user_id from somewhere)
            if "user_preferences" in context:
                # Note: We'd need to get user_id from session or pass it in
                # For now, we'll skip loading user preferences without user_id
                pass

            # Load session preferences
            if "session_preferences" in context:
                for key, value in context["session_preferences"].items():
                    await self.set_preference(key, value, session_id=session.session_id)

            return True

        except Exception:
            return False

    # ========================================================================
    # Reminder Preference Methods (Issue #161 Task 2)
    # ========================================================================

    def _validate_reminder_time(self, time_str: str) -> bool:
        """
        Validate reminder time format (HH:MM).

        Args:
            time_str: Time string in HH:MM format

        Returns:
            True if valid

        Raises:
            ValueError: If format is invalid
        """
        try:
            # Parse HH:MM format
            parts = time_str.split(":")
            if len(parts) != 2:
                raise ValueError("Time must be in HH:MM format")

            hour = int(parts[0])
            minute = int(parts[1])

            # Validate ranges
            if hour < 0 or hour > 23:
                raise ValueError("Hour must be 0-23")
            if minute < 0 or minute > 59:
                raise ValueError("Minute must be 0-59")

            return True

        except (ValueError, AttributeError) as e:
            raise ValueError(f"Invalid time format: {time_str}") from e

    def _validate_timezone(self, tz_str: str) -> bool:
        """
        Validate timezone string (IANA timezone name).

        Args:
            tz_str: Timezone string (e.g., "America/Los_Angeles")

        Returns:
            True if valid

        Raises:
            ValueError: If timezone is invalid
        """
        try:
            # Check if timezone is valid
            if tz_str not in available_timezones():
                raise ValueError(f"Invalid timezone: {tz_str}")

            # Try to create ZoneInfo to ensure it works
            ZoneInfo(tz_str)

            return True

        except Exception as e:
            raise ValueError(f"Invalid timezone: {tz_str}") from e

    def _validate_reminder_days(self, days: List[int]) -> bool:
        """
        Validate reminder days list.

        Args:
            days: List of weekday integers (0=Monday, 6=Sunday)

        Returns:
            True if valid

        Raises:
            ValueError: If days list is invalid
        """
        if not isinstance(days, list):
            raise ValueError("Reminder days must be a list")

        if not days:
            raise ValueError("Reminder days list cannot be empty")

        # Check all values are integers 0-6
        for day in days:
            if not isinstance(day, int):
                raise ValueError("Reminder days must be integers")
            if day < 0 or day > 6:
                raise ValueError("Reminder days must be 0-6 (0=Monday, 6=Sunday)")

        # Check for duplicates
        if len(days) != len(set(days)):
            raise ValueError("Reminder days list contains duplicates")

        return True

    async def get_reminder_enabled(self, user_id: UUID) -> bool:
        """Get whether reminders are enabled for user."""
        return await self.get_preference(STANDUP_REMINDER_ENABLED, user_id=user_id, default=True)

    async def set_reminder_enabled(self, user_id: UUID, enabled: bool):
        """Set whether reminders are enabled for user."""
        await self.set_preference(STANDUP_REMINDER_ENABLED, enabled, user_id=user_id)

    async def get_reminder_time(self, user_id: UUID) -> str:
        """Get reminder time for user (HH:MM format)."""
        return await self.get_preference(STANDUP_REMINDER_TIME, user_id=user_id, default="06:00")

    async def set_reminder_time(self, user_id: UUID, time_str: str):
        """
        Set reminder time for user.

        Args:
            user_id: User ID
            time_str: Time in HH:MM format

        Raises:
            ValueError: If time format is invalid
        """
        # Validate time format
        self._validate_reminder_time(time_str)

        await self.set_preference(STANDUP_REMINDER_TIME, time_str, user_id=user_id)

    async def get_reminder_timezone(self, user_id: UUID) -> str:
        """Get reminder timezone for user."""
        return await self.get_preference(
            STANDUP_REMINDER_TIMEZONE, user_id=user_id, default="America/Los_Angeles"
        )

    async def set_reminder_timezone(self, user_id: UUID, timezone: str):
        """
        Set reminder timezone for user.

        Args:
            user_id: User ID
            timezone: IANA timezone name

        Raises:
            ValueError: If timezone is invalid
        """
        # Validate timezone
        self._validate_timezone(timezone)

        await self.set_preference(STANDUP_REMINDER_TIMEZONE, timezone, user_id=user_id)

    async def get_reminder_days(self, user_id: UUID) -> List[int]:
        """Get reminder days for user."""
        return await self.get_preference(
            STANDUP_REMINDER_DAYS, user_id=user_id, default=[0, 1, 2, 3, 4]
        )

    async def set_reminder_days(self, user_id: UUID, days: List[int]):
        """
        Set reminder days for user.

        Args:
            user_id: User ID
            days: List of weekday integers (0=Monday, 6=Sunday)

        Raises:
            ValueError: If days list is invalid
        """
        # Validate days list
        self._validate_reminder_days(days)

        await self.set_preference(STANDUP_REMINDER_DAYS, days, user_id=user_id)

    async def get_reminder_preferences(self, user_id: UUID) -> dict:
        """
        Get all reminder preferences for user.

        Args:
            user_id: User ID

        Returns:
            Dict with keys: enabled, time, timezone, days
        """
        return {
            "enabled": await self.get_reminder_enabled(user_id),
            "time": await self.get_reminder_time(user_id),
            "timezone": await self.get_reminder_timezone(user_id),
            "days": await self.get_reminder_days(user_id),
        }

    # ========================================================================
    # Learning Preference Methods (Issue #221 CORE-LEARN-A)
    # ========================================================================

    def _validate_learning_confidence(self, confidence: float) -> bool:
        """
        Validate learning confidence threshold.

        Args:
            confidence: Confidence value (0.0-1.0)

        Returns:
            True if valid

        Raises:
            ValueError: If confidence is out of range
        """
        if not isinstance(confidence, (int, float)):
            raise ValueError("Confidence must be a number")

        if confidence < 0.0 or confidence > 1.0:
            raise ValueError("Confidence must be between 0.0 and 1.0")

        return True

    async def get_learning_enabled(self, user_id: UUID) -> bool:
        """Get whether pattern learning is enabled for user."""
        return await self.get_preference(LEARNING_ENABLED, user_id=user_id, default=True)

    async def set_learning_enabled(self, user_id: UUID, enabled: bool):
        """Set whether pattern learning is enabled for user."""
        await self.set_preference(LEARNING_ENABLED, enabled, user_id=user_id)

    async def get_learning_min_confidence(self, user_id: UUID) -> float:
        """Get minimum confidence threshold for pattern application."""
        return await self.get_preference(LEARNING_MIN_CONFIDENCE, user_id=user_id, default=0.5)

    async def set_learning_min_confidence(self, user_id: UUID, confidence: float):
        """
        Set minimum confidence threshold for pattern application.

        Args:
            user_id: User ID
            confidence: Confidence threshold (0.0-1.0)

        Raises:
            ValueError: If confidence is out of range
        """
        # Validate confidence
        self._validate_learning_confidence(confidence)

        await self.set_preference(LEARNING_MIN_CONFIDENCE, confidence, user_id=user_id)

    async def get_learning_features(self, user_id: UUID) -> List[str]:
        """Get list of features enabled for learning."""
        return await self.get_preference(LEARNING_FEATURES, user_id=user_id, default=[])

    async def set_learning_features(self, user_id: UUID, features: List[str]):
        """
        Set list of features enabled for learning.

        Args:
            user_id: User ID
            features: List of feature names

        Raises:
            ValueError: If features list is invalid
        """
        if not isinstance(features, list):
            raise ValueError("Learning features must be a list")

        # Validate all features are strings
        for feature in features:
            if not isinstance(feature, str):
                raise ValueError("Learning features must be strings")

        await self.set_preference(LEARNING_FEATURES, features, user_id=user_id)

    async def get_learning_preferences(self, user_id: UUID) -> dict:
        """
        Get all learning preferences for user.

        Args:
            user_id: User ID

        Returns:
            Dict with keys: enabled, min_confidence, features
        """
        return {
            "enabled": await self.get_learning_enabled(user_id),
            "min_confidence": await self.get_learning_min_confidence(user_id),
            "features": await self.get_learning_features(user_id),
        }

    # ========================================================================
    # Calendar Setup Offer Methods (Issue #790)
    # ========================================================================

    async def get_calendar_setup_offer_state(self, user_id: UUID) -> Optional[str]:
        """Get the calendar-setup offer state for user.

        Returns:
            One of None | "offered" | "declined" | "deferred" | "accepted".
            None means the user has never been offered calendar setup.
        """
        return await self.get_preference(
            CALENDAR_SETUP_OFFERED, user_id=user_id, default=None
        )

    async def set_calendar_setup_offer_state(
        self, user_id: UUID, state: Optional[str]
    ) -> None:
        """Set the calendar-setup offer state for user.

        Args:
            user_id: User ID
            state: One of None | "offered" | "declined" | "deferred" | "accepted"

        Raises:
            ValueError: If state is not None and not a recognized value
        """
        if state is not None and state not in CALENDAR_OFFER_STATES:
            raise ValueError(
                f"Invalid calendar offer state: {state!r}. "
                f"Must be None or one of {sorted(CALENDAR_OFFER_STATES)}."
            )
        await self.set_preference(CALENDAR_SETUP_OFFERED, state, user_id=user_id)

    # ========================================================================
    # Default Repo Preference Methods (Issue #1042)
    # ========================================================================

    async def get_default_repo(self, user_id: UUID) -> Optional[str]:
        """Get the user's default GitHub repo.

        Returns:
            ``owner/name`` string, or None if not set.
        """
        return await self.get_preference(DEFAULT_REPO, user_id=user_id, default=None)

    async def set_default_repo(self, user_id: UUID, value: Optional[str]) -> None:
        """Set the user's default GitHub repo.

        Args:
            user_id: User ID
            value: ``owner/name`` string, or None to clear

        Raises:
            ValueError: When ``value`` is non-None and not in ``owner/name``
                shape (matches ``[A-Za-z0-9._-]+/[A-Za-z0-9._-]+``).
        """
        if value is not None:
            import re

            if not re.match(r"^[A-Za-z0-9._\-]+/[A-Za-z0-9._\-]+$", value):
                raise ValueError(
                    f"Invalid default_repo value {value!r}; "
                    "expected 'owner/name' shape "
                    "(e.g., 'myorg/myproject')"
                )
        await self.set_preference(DEFAULT_REPO, value, user_id=user_id)

    # ========================================================================
    # CORE-LEARN-C: Preference Learning from Patterns (Issue #223)
    # ========================================================================

    async def apply_preference_pattern(
        self,
        pattern: Dict[str, Any],
        user_id: UUID,
        session_id: Optional[str] = None,
        scope: str = "user",
    ) -> bool:
        """
        Apply a learned preference pattern to user preferences.

        Converts implicit preferences (learned patterns) to explicit preferences.
        Only applies patterns with confidence >= 0.7 (high confidence threshold).

        Args:
            pattern: The learned pattern dict (or LearnedPattern object converted to dict)
            user_id: User ID to set preference for
            session_id: Optional session ID for session-scoped preferences
            scope: Preference scope ('user' or 'session')

        Returns:
            bool: True if preference was set, False if pattern confidence too low

        Example:
            pattern = {
                "confidence": 0.85,
                "pattern_data": {
                    "preference_key": "response_style",
                    "preference_value": "concise"
                }
            }
            success = await pm.apply_preference_pattern(pattern, "user123")
        """
        # Extract confidence - handle both dict and object
        confidence = (
            pattern.get("confidence", 0.0)
            if isinstance(pattern, dict)
            else getattr(pattern, "confidence", 0.0)
        )

        # Only apply high-confidence patterns to preferences
        if confidence < 0.7:
            return False

        # Extract pattern data - handle both dict and object
        pattern_data = (
            pattern.get("pattern_data", {})
            if isinstance(pattern, dict)
            else getattr(pattern, "pattern_data", {})
        )

        # Pattern data should contain preference information
        if "preference_key" not in pattern_data or "preference_value" not in pattern_data:
            return False

        preference_key = pattern_data["preference_key"]
        preference_value = pattern_data["preference_value"]

        # Set the preference using existing mechanism
        # This respects all existing validation, hierarchy, etc.
        success = await self.set_preference(
            key=preference_key,
            value=preference_value,
            user_id=user_id,
            session_id=session_id,
            scope=scope,
        )

        return success

    async def _cleanup_expired_preferences(self):
        """Clean up expired preferences across all scopes"""
        current_time = datetime.now()

        # Clean global preferences
        expired_global = [key for key, item in self.global_preferences.items() if item.is_expired()]
        for key in expired_global:
            del self.global_preferences[key]

        # Clean user preferences
        for user_id, user_prefs in self.user_preferences.items():
            expired_user = [key for key, item in user_prefs.items() if item.is_expired()]
            for key in expired_user:
                del user_prefs[key]

        # Clean session preferences
        for session_id, session_prefs in self.session_preferences.items():
            expired_session = [key for key, item in session_prefs.items() if item.is_expired()]
            for key in expired_session:
                del session_prefs[key]
