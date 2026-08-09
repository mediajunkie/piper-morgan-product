"""User context service for multi-user support - GREAT-4C Phase 0."""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional
from uuid import UUID

import structlog

logger = structlog.get_logger()


@dataclass
class UserContext:
    """User-specific context data."""

    user_id: UUID
    organization: Optional[str] = None
    projects: list = field(default_factory=list)
    priorities: list = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)
    # #1530: which source `projects` came from — "database" | "preferences" |
    # "config". Lets the cache-hit refresh path know whether an empty DB read
    # means "all archived, rebuild fallback" or "DB was never the source".
    projects_source: str = "config"


class UserContextService:
    """Manages user-specific context without hardcoding."""

    def __init__(self):
        self.cache = {}
        # Cache metrics (GREAT-4C Phase 3)
        self.cache_hits = 0
        self.cache_misses = 0
        logger.info("UserContextService initialized")

    async def get_user_context(
        self, session_id: str, user_id: Optional[UUID] = None
    ) -> UserContext:
        """
        Get user context from session with optional user-specific data.

        Args:
            session_id: Session identifier
            user_id: Optional user ID to load user-specific preferences from database

        Returns:
            UserContext with user-specific data (if user_id provided) or generic data

        Issue #280: Now supports loading user preferences from alpha_users.preferences
        """
        # Use user_id for cache key if provided, otherwise session_id
        cache_key = f"user:{user_id}" if user_id else f"session:{session_id}"

        # Check cache first
        if cache_key in self.cache:
            self.cache_hits += 1  # GREAT-4C Phase 3: Track cache hit
            logger.debug(
                "user_context_cache_hit",
                cache_key=cache_key,
                user_id=user_id,
                cache_hits=self.cache_hits,
            )
            context = self.cache[cache_key]
            # #1530: this cache is process-lifetime and no project write
            # invalidates it, so a project created/unarchived after first fill
            # was invisible to chat forever while the /projects page (fresh
            # owner-scoped query per request) showed it. Re-read the projects
            # rows on every hit so chat states the same truth the page reads.
            if user_id:
                context = await self._refresh_db_projects(context, session_id, user_id, cache_key)
            return context

        # Cache miss - load from database or config
        self.cache_misses += 1  # GREAT-4C Phase 3: Track cache miss
        logger.debug(
            "user_context_cache_miss",
            cache_key=cache_key,
            user_id=user_id,
            cache_misses=self.cache_misses,
        )

        # Load context (with user preferences if user_id provided)
        context = await self._load_context_from_config(session_id, user_id)

        # Cache it
        self.cache[cache_key] = context
        logger.debug(
            "user_context_cached",
            cache_key=cache_key,
            user_id=user_id,
            org=context.organization,
        )
        return context

    async def _refresh_db_projects(
        self, context: UserContext, session_id: str, user_id: UUID, cache_key: str
    ) -> UserContext:
        """
        #1530: On a cache hit, re-read owner-scoped project rows from the DB.

        Same query the /projects page runs per request
        (ProjectRepository.list_active_projects(owner_id=...)) — so the chat
        surface and the page can never diverge on which projects exist.

        - DB has active rows → they replace the cached list (DB is the
          highest-priority source, mirroring the cold-load precedence).
        - DB has no rows but was the cached source → every project has been
          archived/deleted since fill (or the read failed); rebuild the whole
          context so the cold-load fallback chain (prefs → config) applies and
          stale row names cannot linger.
        - DB has no rows and was never the source → cached prefs/config
          projects stand, exactly as on cold load.
        """
        db_projects = await self._load_projects_from_db(user_id)
        if db_projects:
            context.projects = db_projects
            context.projects_source = "database"
            return context
        if context.projects_source == "database":
            context = await self._load_context_from_config(session_id, user_id)
            self.cache[cache_key] = context
        return context

    async def _load_context_from_config(
        self, session_id: str, user_id: Optional[UUID] = None
    ) -> UserContext:
        """
        Load user context from PIPER.md and optionally user preferences.

        Issue #280: Now loads generic PIPER.md and merges with user preferences
        from alpha_users.preferences JSONB field.

        Issue #582: Now also loads projects from the projects table (portfolio).
        Database projects take precedence over config-based projects.

        Args:
            session_id: Session identifier
            user_id: Optional user ID to load database preferences

        Returns:
            UserContext with merged generic + user-specific data
        """
        from services.configuration.piper_config_loader import piper_config_loader

        try:
            # 1. Load generic PIPER.md (shared across all users)
            generic_config = piper_config_loader.load_config()

            # 2. Load user-specific preferences from database if user_id provided
            user_prefs = {}
            if user_id:
                user_prefs = await self._load_user_preferences_from_db(user_id)

            # 3. Merge configurations (user preferences override generic)
            merged_config = {**generic_config, **user_prefs}

            # 4. Issue #582: Load projects from database (portfolio)
            # Database projects take precedence over config-based projects
            db_projects = []
            if user_id:
                db_projects = await self._load_projects_from_db(user_id)

            # 5. Determine project source with priority:
            #    - Database projects (from portfolio onboarding) - highest priority
            #    - User preferences projects
            #    - Config-based projects (PIPER.md) - fallback
            if db_projects:
                projects = db_projects
                projects_source = "database"
            elif user_prefs:
                projects = self._extract_projects_from_prefs(user_prefs)
                projects_source = "preferences"
            else:
                projects = self._extract_projects(merged_config)
                projects_source = "config"

            # 6. Extract context from merged config
            context = UserContext(
                user_id=user_id or session_id,
                organization=self._extract_organization(merged_config),
                projects=projects,
                projects_source=projects_source,
                priorities=(
                    self._extract_priorities_from_prefs(user_prefs)
                    if user_prefs
                    else self._extract_priorities(merged_config)
                ),
                preferences=user_prefs,  # Store raw preferences for advanced use
            )

            logger.info(
                "user_context_loaded",
                session_id=session_id,
                user_id=user_id,
                has_user_prefs=bool(user_prefs),
                has_db_projects=bool(db_projects),
                org=context.organization,
                project_count=len(context.projects),
                priority_count=len(context.priorities),
            )

            return context

        except Exception as e:
            logger.warning(
                "user_context_load_failed",
                session_id=session_id,
                user_id=user_id,
                error=str(e),
            )
            # Return empty context
            return UserContext(user_id=user_id or session_id)

    async def _load_projects_from_db(self, user_id: UUID) -> list:
        """
        Issue #582: Load projects from the projects table.

        This connects portfolio onboarding (which saves projects to DB)
        with standup/status features (which read from UserContext).

        Args:
            user_id: User UUID

        Returns:
            List of project names, or empty list if none found
        """
        try:
            from services.database.repositories import ProjectRepository
            from services.database.session_factory import AsyncSessionFactory

            async with AsyncSessionFactory.session_scope_fresh() as session:
                project_repo = ProjectRepository(session)
                db_projects = await project_repo.list_active_projects(owner_id=str(user_id))

                if db_projects:
                    project_names = [p.name for p in db_projects]
                    logger.debug(
                        "projects_loaded_from_db",
                        user_id=user_id,
                        project_count=len(project_names),
                        project_names=project_names,
                    )
                    return project_names
                else:
                    logger.debug("no_projects_in_db", user_id=user_id)
                    return []

        except Exception as e:
            logger.warning(
                "projects_db_load_failed",
                user_id=user_id,
                error=str(e),
            )
            return []

    async def _load_user_preferences_from_db(self, user_id: UUID) -> Dict[str, Any]:
        """
        Load user preferences from alpha_users.preferences JSONB field.

        Args:
            user_id: User UUID

        Returns:
            Dictionary of user preferences, or empty dict if not found

        Issue #280: Enables per-user data isolation
        """
        try:
            from sqlalchemy import select

            from services.database.connection import db
            from services.database.models import User
            from services.database.session_factory import AsyncSessionFactory

            # Initialize DB if needed
            if not db._initialized:
                await db.initialize()

            # Query user preferences (Issue #262 - alpha_users merged into users)
            # Use fresh session to avoid event loop mismatch (#442)
            async with AsyncSessionFactory.session_scope_fresh() as session:
                result = await session.execute(select(User).where(User.id == user_id))
                user = result.scalar_one_or_none()

                if user and user.preferences:
                    logger.debug(
                        "user_preferences_loaded",
                        user_id=user_id,
                        pref_keys=list(user.preferences.keys()),
                    )
                    return user.preferences
                else:
                    logger.debug("no_user_preferences_found", user_id=user_id)
                    return {}

        except Exception as e:
            logger.warning("user_preferences_load_failed", user_id=user_id, error=str(e))
            return {}

    def _extract_projects_from_prefs(self, prefs: Dict) -> list:
        """
        Extract projects from user preferences (database format).

        Issue #280: Handles structured project data from alpha_users.preferences
        """
        projects = []
        if "projects" in prefs and isinstance(prefs["projects"], list):
            for project in prefs["projects"]:
                if isinstance(project, dict):
                    # Extract project name and key info
                    project_name = project.get("name", "")
                    allocation = project.get("allocation", 0)
                    if project_name:
                        projects.append(f"{project_name} ({allocation}%)")
                elif isinstance(project, str):
                    projects.append(project)
        return projects

    def _extract_priorities_from_prefs(self, prefs: Dict) -> list:
        """
        Extract priorities from user preferences (database format).

        Issue #280: Handles structured priority data from alpha_users.preferences
        """
        priorities = []
        if "priorities" in prefs and isinstance(prefs["priorities"], list):
            for priority in prefs["priorities"]:
                if isinstance(priority, dict):
                    # Extract priority name
                    priority_name = priority.get("name", "")
                    if priority_name:
                        priorities.append(priority_name)
                elif isinstance(priority, str):
                    priorities.append(priority)
        return priorities

    def _extract_organization(self, config: Dict) -> Optional[str]:
        """Extract organization from config."""
        # Look for organization mentions in config
        for key, value in config.items():
            if "organization" in key.lower():
                return str(value)

            # Also check for common org patterns in section content
            if isinstance(value, str):
                # Look for "Working on [Organization]" patterns
                if "working on" in value.lower() or "organization:" in value.lower():
                    # Try to extract org name
                    lines = value.split("\n")
                    for line in lines:
                        if "organization:" in line.lower():
                            org = line.split(":", 1)[1].strip()
                            return org

        return None

    def _extract_projects(self, config: Dict) -> list:
        """Extract projects from config."""
        projects = []
        for key, value in config.items():
            if "project" in key.lower() or "work" in key.lower():
                # Parse project list from config
                if isinstance(value, list):
                    projects.extend(value)
                elif isinstance(value, str):
                    # Parse from text - look for bulleted lists
                    lines = value.split("\n")
                    for line in lines:
                        stripped = line.strip()
                        # Match bullet points: -, *, •, or numbered lists
                        if stripped.startswith(("-", "*", "•")) or (
                            stripped and stripped[0].isdigit() and "." in stripped
                        ):
                            # Extract project name (remove bullet/number)
                            project = stripped.lstrip("-*•0123456789. ").strip()
                            if project:
                                projects.append(project)

        return projects

    def _extract_priorities(self, config: Dict) -> list:
        """Extract priorities from config."""
        priorities = []
        for key, value in config.items():
            if "priorit" in key.lower() or "focus" in key.lower():
                if isinstance(value, list):
                    priorities.extend(value)
                elif isinstance(value, str):
                    lines = value.split("\n")
                    for line in lines:
                        stripped = line.strip()
                        # Match bullet points or numbered lists
                        if stripped.startswith(("-", "*", "•")) or (
                            stripped and stripped[0].isdigit() and "." in stripped
                        ):
                            priority = stripped.lstrip("-*•0123456789. ").strip()
                            if priority:
                                priorities.append(priority)

        return priorities

    def invalidate_cache(self, session_id: Optional[str] = None):
        """
        Invalidate cached context.

        Args:
            session_id: Optional session to invalidate. If None, clears all cache.
        """
        if session_id:
            if session_id in self.cache:
                del self.cache[session_id]
                logger.debug("user_context_cache_invalidated", session_id=session_id)
        else:
            self.cache.clear()
            logger.debug("user_context_cache_cleared")

    def get_cache_metrics(self) -> Dict[str, Any]:
        """
        Get cache performance metrics.

        Returns:
            Dictionary with cache hits, misses, hit rate, and cache size

        Added in GREAT-4C Phase 3 for cache monitoring.
        """
        total = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total * 100) if total > 0 else 0

        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "total_requests": total,
            "hit_rate_percent": round(hit_rate, 2),
            "cache_size": len(self.cache),
            "cached_sessions": (
                list(self.cache.keys()) if len(self.cache) <= 10 else f"{len(self.cache)} sessions"
            ),
        }

    def clear_metrics(self):
        """
        Reset cache metrics without clearing cache.

        Added in GREAT-4C Phase 3 for metrics management.
        """
        self.cache_hits = 0
        self.cache_misses = 0
        logger.debug("user_context_metrics_cleared")


# Singleton instance
user_context_service = UserContextService()
