"""
PersonalityProfileRepository - Data access layer
Handles database operations and PIPER.user.md integration
"""

import logging
import os
from typing import Any, Dict, Optional
from uuid import UUID

import yaml
from sqlalchemy import delete, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from services.database.connection import db
from services.database.session_factory import AsyncSessionFactory

from .exceptions import ConfigurationError, ProfileLoadError
# #1312 unify-Base (Arch ruling 2026-07-08, re-confirming 2026-06-25): the sibling
# models.py was a stale pre-#262 duplicate on an ACCIDENTAL separate declarative_base
# (String user_id vs the DB's UUID) — deleted; this repo now uses the canonical model
# on the shared Base.
from services.database.models import PersonalityProfileModel
from .personality_profile import (
    ActionLevel,
    ConfidenceDisplayStyle,
    PersonalityProfile,
    TechnicalPreference,
)

logger = logging.getLogger(__name__)


class PersonalityProfileRepository:
    """Repository for personality profiles with PIPER.user.md integration"""

    def __init__(self):
        self.config_cache = {}  # Cache for PIPER.user.md overrides
        self.config_cache_ttl = 300  # 5 minutes

    async def get_by_user_id(
        self, user_id: str, is_admin: bool = False
    ) -> Optional[PersonalityProfile]:
        """Load PersonalityProfile with PIPER.user.md overrides (SEC-RBAC Phase 3: admins can access any profile)"""
        try:
            # Load base profile from database
            base_profile = await self._load_from_database(user_id)

            if not base_profile:
                # Create default profile
                base_profile = PersonalityProfile.get_default(user_id)
                await self.save(base_profile)

            # Apply PIPER.user.md overrides
            overrides = await self._load_piper_config_overrides()
            if overrides:
                profile = self._apply_overrides(base_profile, overrides)
            else:
                profile = base_profile

            return profile

        except Exception as e:
            logger.error(f"Error loading profile for user {user_id}: {e}")
            raise ProfileLoadError(f"Failed to load profile: {e}")

    async def save(self, profile: PersonalityProfile) -> None:
        """Save PersonalityProfile to database"""
        try:
            async with AsyncSessionFactory.session_scope() as session:
                # Check if profile exists
                stmt = select(PersonalityProfileModel).where(
                    PersonalityProfileModel.user_id == profile.user_id
                )
                result = await session.execute(stmt)
                existing = result.scalar_one_or_none()

                if existing:
                    # Update existing
                    update_stmt = (
                        update(PersonalityProfileModel)
                        .where(PersonalityProfileModel.user_id == profile.user_id)
                        .values(
                            warmth_level=profile.warmth_level,
                            confidence_style=profile.confidence_style.value,
                            action_orientation=profile.action_orientation.value,
                            technical_depth=profile.technical_depth.value,
                            updated_at=profile.updated_at,
                            is_active=profile.is_active,
                        )
                    )
                    await session.execute(update_stmt)
                else:
                    # Create new
                    model = PersonalityProfileModel(
                        user_id=profile.user_id,
                        warmth_level=profile.warmth_level,
                        confidence_style=profile.confidence_style.value,
                        action_orientation=profile.action_orientation.value,
                        technical_depth=profile.technical_depth.value,
                        created_at=profile.created_at,
                        updated_at=profile.updated_at,
                        is_active=profile.is_active,
                    )
                    session.add(model)

                await session.commit()

        except SQLAlchemyError as e:
            logger.error(f"Database error saving profile for user {profile.user_id}: {e}")
            raise ProfileLoadError(f"Failed to save profile: {e}")

    async def delete(self, user_id: str, is_admin: bool = False) -> bool:
        """Delete PersonalityProfile for user (SEC-RBAC Phase 3: admins can delete any profile)"""
        try:
            async with AsyncSessionFactory.session_scope() as session:
                stmt = delete(PersonalityProfileModel).where(
                    PersonalityProfileModel.user_id == user_id
                )
                result = await session.execute(stmt)
                await session.commit()
                return result.rowcount > 0

        except SQLAlchemyError as e:
            logger.error(f"Database error deleting profile for user {user_id}: {e}")
            return False

    async def get_default(self) -> PersonalityProfile:
        """Return default Piper personality"""
        return PersonalityProfile.get_default("default_user")

    async def _load_from_database(self, user_id: str) -> Optional[PersonalityProfile]:
        """Load PersonalityProfile from database"""
        try:
            async with AsyncSessionFactory.session_scope() as session:
                stmt = select(PersonalityProfileModel).where(
                    PersonalityProfileModel.user_id == user_id,
                    PersonalityProfileModel.is_active == True,
                )
                result = await session.execute(stmt)
                model = result.scalar_one_or_none()

                if not model:
                    return None

                return PersonalityProfile(
                    id=str(model.id),
                    user_id=model.user_id,
                    warmth_level=model.warmth_level,
                    confidence_style=ConfidenceDisplayStyle(model.confidence_style),
                    action_orientation=ActionLevel(model.action_orientation),
                    technical_depth=TechnicalPreference(model.technical_depth),
                    created_at=model.created_at,
                    updated_at=model.updated_at,
                    is_active=model.is_active,
                )

        except SQLAlchemyError as e:
            logger.error(f"Database error loading profile for user {user_id}: {e}")
            return None

    async def _load_piper_config_overrides(self) -> Optional[Dict[str, Any]]:
        """Load personality overrides from PIPER.user.md"""
        try:
            config_path = "config/PIPER.user.md"

            if not os.path.exists(config_path):
                return None

            # Check if file was modified recently
            mtime = os.path.getmtime(config_path)
            cache_key = f"{config_path}:{mtime}"

            if cache_key in self.config_cache:
                return self.config_cache[cache_key]

            # Read and parse YAML
            with open(config_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Extract YAML front matter or find personality section
            if content.startswith("---"):
                # YAML front matter
                yaml_content = content.split("---")[1]
            else:
                # Look for personality section
                lines = content.split("\n")
                yaml_lines = []
                in_personality = False

                for line in lines:
                    if line.strip().startswith("personality:"):
                        in_personality = True
                        yaml_lines.append(line)
                    elif in_personality:
                        if line.startswith("  ") or line.strip() == "":
                            yaml_lines.append(line)
                        else:
                            break

                if not yaml_lines:
                    return None

                yaml_content = "\n".join(yaml_lines)

            data = yaml.safe_load(yaml_content)
            personality_config = data.get("personality") if data else None

            # Cache the result
            self.config_cache[cache_key] = personality_config

            return personality_config

        except yaml.YAMLError as e:
            logger.warning(f"YAML parse error in PIPER.user.md: {e}")
            return None
        except Exception as e:
            logger.warning(f"Error reading PIPER.user.md: {e}")
            return None

    def _apply_overrides(
        self, base_profile: PersonalityProfile, overrides: Dict[str, Any]
    ) -> PersonalityProfile:
        """Apply PIPER.user.md overrides to base profile"""
        try:
            # Extract override values with validation
            warmth_level = overrides.get("warmth_level", base_profile.warmth_level)
            confidence_style = overrides.get(
                "confidence_style", base_profile.confidence_style.value
            )
            action_orientation = overrides.get(
                "action_orientation", base_profile.action_orientation.value
            )
            technical_depth = overrides.get("technical_depth", base_profile.technical_depth.value)

            # Validate warmth_level
            if not isinstance(warmth_level, (int, float)) or not (0.0 <= warmth_level <= 1.0):
                logger.warning(f"Invalid warmth_level {warmth_level}, using default")
                warmth_level = base_profile.warmth_level

            # Validate enums
            try:
                confidence_style_enum = ConfidenceDisplayStyle(confidence_style)
            except ValueError:
                logger.warning(f"Invalid confidence_style {confidence_style}, using default")
                confidence_style_enum = base_profile.confidence_style

            try:
                action_orientation_enum = ActionLevel(action_orientation)
            except ValueError:
                logger.warning(f"Invalid action_orientation {action_orientation}, using default")
                action_orientation_enum = base_profile.action_orientation

            try:
                technical_depth_enum = TechnicalPreference(technical_depth)
            except ValueError:
                logger.warning(f"Invalid technical_depth {technical_depth}, using default")
                technical_depth_enum = base_profile.technical_depth

            # Create override profile
            return PersonalityProfile(
                id=base_profile.id,
                user_id=base_profile.user_id,
                warmth_level=float(warmth_level),
                confidence_style=confidence_style_enum,
                action_orientation=action_orientation_enum,
                technical_depth=technical_depth_enum,
                created_at=base_profile.created_at,
                updated_at=base_profile.updated_at,
                is_active=base_profile.is_active,
            )

        except Exception as e:
            logger.error(f"Error applying overrides: {e}")
            raise ConfigurationError(f"Invalid PIPER.user.md configuration: {e}")
