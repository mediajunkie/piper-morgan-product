"""
#984: Cache-invalidation hooks for ContextAssembler caches.

Single source of truth for which cache keys are affected by which mutations.
Mutation sites call the public functions; they don't need to know which
specific keys exist for a given domain.

PM Q3=(c) hybrid: eager invalidation only on todos + trust-stage changes.
Other surfaces (projects, calendar, user_context) rely on TTL expiry.

Usage:

    from services.intent_service.cache_invalidation import (
        invalidate_user_todos,
        invalidate_user_trust,
    )

    # After any todo CRUD:
    await invalidate_user_todos(user_id)

    # After trust-stage transition:
    await invalidate_user_trust(user_id)

All functions are fail-graceful — if the cache is unavailable, the
mutation still succeeds; the cached entry will expire on its TTL.
"""

from typing import Union
from uuid import UUID

import structlog

from services.intent_service.context_cache import ContextCache

logger = structlog.get_logger()

# Module-level singleton. Mutation sites get a stable reference without
# needing dependency injection. Tests can replace this via monkeypatch.
_default_cache = ContextCache()


def _get_cache() -> ContextCache:
    """Return the module-level cache. Indirection allows test overrides."""
    return _default_cache


async def invalidate_user_todos(user_id: Union[str, UUID]) -> int:
    """Invalidate all todo-derived caches for a user.

    Clears pending_todos, completed_todos, and reminders caches — all three
    are todo-derived and any todo mutation potentially affects them.

    Returns count of keys actually deleted (0–3). On Redis unavailable
    or error, returns 0 silently.
    """
    user_id_str = str(user_id)
    cache = _get_cache()
    total = 0
    for method in ("pending_todos", "completed_todos", "reminders"):
        key = f"context:{method}:{user_id_str}"
        if await cache.invalidate(key):
            total += 1
    logger.info(
        "context_cache_user_todos_invalidated",
        user_id=user_id_str,
        keys_cleared=total,
    )
    return total


async def invalidate_user_trust(user_id: Union[str, UUID]) -> bool:
    """Invalidate the trust-profile cache for a user.

    Call after UserTrustProfileRepository.update_stage successfully
    transitions a user to a new trust stage. The next floor query will
    re-fetch the profile and reflect the new stage immediately.

    Returns True if the key was present and cleared, False otherwise
    (miss, Redis unavailable, or error — all silently).
    """
    user_id_str = str(user_id)
    cache = _get_cache()
    ok = await cache.invalidate(f"context:trust:{user_id_str}")
    logger.info(
        "context_cache_user_trust_invalidated",
        user_id=user_id_str,
        cleared=ok,
    )
    return ok
