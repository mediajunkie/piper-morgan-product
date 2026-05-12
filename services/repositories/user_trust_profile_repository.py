"""
User Trust Profile Repository

Issue #647: TRUST-LEVELS-1 - Core Infrastructure
ADR-053: Trust Computation Architecture

Repository for managing UserTrustProfile persistence using SQLAlchemy.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.models import UserTrustProfileDB
from services.database.repositories import BaseRepository
from services.domain.models import TrustEvent, UserTrustProfile
from services.shared_types import TrustStage


class UserTrustProfileRepository(BaseRepository):
    """Repository for user trust profile operations using SQLAlchemy."""

    model = UserTrustProfileDB

    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_by_user_id(self, user_id: UUID) -> Optional[UserTrustProfile]:
        """Get trust profile by user ID.

        Returns None if no profile exists (user is implicitly NEW).
        """
        result = await self.session.execute(
            select(UserTrustProfileDB).where(UserTrustProfileDB.user_id == user_id)
        )
        db_profile = result.scalar_one_or_none()
        return db_profile.to_domain() if db_profile else None

    async def create_or_update(self, profile: UserTrustProfile) -> UserTrustProfile:
        """Create or update a trust profile.

        Uses upsert pattern - creates if not exists, updates if exists.
        """
        # Check if profile exists
        existing = await self.session.execute(
            select(UserTrustProfileDB).where(UserTrustProfileDB.user_id == profile.user_id)
        )
        db_profile = existing.scalar_one_or_none()

        if db_profile:
            # Update existing profile
            db_profile.current_stage = profile.current_stage.value
            db_profile.highest_stage_achieved = profile.highest_stage_achieved.value
            db_profile.successful_count = profile.successful_count
            db_profile.neutral_count = profile.neutral_count
            db_profile.negative_count = profile.negative_count
            db_profile.consecutive_negative = profile.consecutive_negative
            db_profile.recent_events = [e.to_dict() for e in profile.recent_events]
            # Serialize stage_history tuples to JSON-compatible dicts
            db_profile.stage_history = [
                {
                    "timestamp": ts.isoformat(),
                    "stage": stage.value,
                    "reason": reason,
                }
                for ts, stage, reason in profile.stage_history
            ]
            db_profile.last_interaction_at = profile.last_interaction_at
            db_profile.last_stage_change_at = profile.last_stage_change_at
            db_profile.updated_at = datetime.now(timezone.utc)
        else:
            # Create new profile
            db_profile = UserTrustProfileDB.from_domain(profile)
            self.session.add(db_profile)

        await self.session.flush()
        await self.session.refresh(db_profile)
        return db_profile.to_domain()

    async def record_event(
        self,
        user_id: UUID,
        event: TrustEvent,
        max_recent_events: int = 20,
    ) -> UserTrustProfile:
        """Record a trust event for a user.

        Creates profile if it doesn't exist.
        Maintains a rolling window of recent events.

        Args:
            user_id: User's UUID
            event: The TrustEvent to record
            max_recent_events: Maximum events to keep in recent_events list

        Returns:
            Updated UserTrustProfile
        """
        profile = await self.get_by_user_id(user_id)

        if profile is None:
            # Create new profile for user
            profile = UserTrustProfile(
                user_id=user_id,
                current_stage=TrustStage.NEW,
                highest_stage_achieved=TrustStage.NEW,
                successful_count=0,
                neutral_count=0,
                negative_count=0,
                consecutive_negative=0,
                recent_events=[],
                stage_history=[],
                last_interaction_at=datetime.now(timezone.utc),
                last_stage_change_at=None,
            )

        # Update counters based on outcome
        if event.outcome == "successful":
            profile.successful_count += 1
            profile.consecutive_negative = 0
        elif event.outcome == "neutral":
            profile.neutral_count += 1
            # Neutral doesn't reset consecutive negative per ADR-053
        elif event.outcome == "negative":
            profile.negative_count += 1
            profile.consecutive_negative += 1

        # Add event to recent events, maintaining window size
        profile.recent_events.append(event)
        if len(profile.recent_events) > max_recent_events:
            profile.recent_events = profile.recent_events[-max_recent_events:]

        profile.last_interaction_at = event.timestamp

        return await self.create_or_update(profile)

    async def get_recent_events(
        self,
        user_id: UUID,
        limit: int = 10,
    ) -> List[TrustEvent]:
        """Get recent trust events for a user.

        Returns empty list if user has no profile or no events.
        """
        profile = await self.get_by_user_id(user_id)
        if profile is None:
            return []

        # Return most recent events (already stored in chronological order)
        return profile.recent_events[-limit:]

    async def update_stage(
        self,
        user_id: UUID,
        new_stage: TrustStage,
        reason: str,
    ) -> Optional[UserTrustProfile]:
        """Update user's trust stage with history tracking.

        Records stage change in stage_history.
        Updates highest_stage_achieved if applicable.

        Returns None if user has no profile.
        """
        profile = await self.get_by_user_id(user_id)
        if profile is None:
            return None

        now = datetime.now(timezone.utc)

        # Record in stage history as tuple (timestamp, new_stage, reason)
        profile.stage_history.append((now, new_stage, reason))

        # Update current stage
        profile.current_stage = new_stage
        profile.last_stage_change_at = now

        # Track highest stage achieved
        if new_stage.value > profile.highest_stage_achieved.value:
            profile.highest_stage_achieved = new_stage

        result = await self.create_or_update(profile)

        # #984: Invalidate the cached trust-profile entry so the next floor
        # query reflects the new stage immediately. Done after persistence
        # so we don't invalidate on failure.
        if result is not None:
            from services.intent_service.cache_invalidation import invalidate_user_trust

            await invalidate_user_trust(user_id)

        return result

    async def delete_by_user_id(self, user_id: UUID) -> bool:
        """Delete a user's trust profile.

        Returns True if deleted, False if not found.
        """
        result = await self.session.execute(
            select(UserTrustProfileDB).where(UserTrustProfileDB.user_id == user_id)
        )
        db_profile = result.scalar_one_or_none()

        if db_profile:
            await self.session.delete(db_profile)
            await self.session.flush()
            return True
        return False
