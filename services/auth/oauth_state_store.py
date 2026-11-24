"""#2345: the pending OAuth sign-in state for GitHub and Google Calendar lives in Redis.

Both handlers kept it in a module-level dict, so a restart between Connect and the return
from GitHub or Google lost it (an invalid-state error), and a second machine could never
see it. This is the Slack handler's pattern (#1109): one key per nonce under a prefix of
the connector's own, a TTL equal to the handler's ``STATE_EXPIRATION``, and a single-use
read by ``GETDEL`` so the read and the delete are one atomic call.

The client comes from ``RedisFactory.redis_scope`` (the accessor Slack uses; no second
pool). Any failure to reach Redis raises ``OAuthStateStoreUnavailable``: the start refuses
before any authorize URL exists, and the callback refuses (fail closed). Nothing here logs
a nonce, a key or a state.
"""

from __future__ import annotations

import json
from typing import Any, Dict, Optional

import structlog

from services.cache.redis_factory import RedisFactory

logger = structlog.get_logger(__name__)

# One prefix per connector, distinct from each other and from Slack's
# ``slack:oauth:state:``, so one connector's state can never validate another's.
GITHUB_STATE_KEY_PREFIX = "github:oauth:state:"
CALENDAR_STATE_KEY_PREFIX = "calendar:oauth:state:"


class OAuthStateStoreUnavailable(RuntimeError):
    """Redis could not store or read the pending state. Never carries the nonce."""


async def put_state(prefix: str, nonce: str, payload: Dict[str, Any], ttl_seconds: int) -> None:
    """Store ``payload`` as JSON at ``prefix + nonce`` with a TTL. Raises
    ``OAuthStateStoreUnavailable`` when Redis can't take it."""
    try:
        async with RedisFactory.redis_scope() as redis:
            await redis.setex(f"{prefix}{nonce}", int(ttl_seconds), json.dumps(payload))
    except Exception as e:
        logger.warning(
            "oauth_state_store_unavailable", op="put", prefix=prefix, error=type(e).__name__
        )
        raise OAuthStateStoreUnavailable("oauth state store unavailable") from e


async def take_state(prefix: str, nonce: str) -> Optional[Dict[str, Any]]:
    """Read and delete the state at ``prefix + nonce`` in one ``GETDEL``. None when the
    key is absent (never stored, already used, or expired) or unreadable. Raises
    ``OAuthStateStoreUnavailable`` when Redis can't answer."""
    try:
        async with RedisFactory.redis_scope() as redis:
            raw = await redis.getdel(f"{prefix}{nonce}")
    except Exception as e:
        logger.warning(
            "oauth_state_store_unavailable", op="take", prefix=prefix, error=type(e).__name__
        )
        raise OAuthStateStoreUnavailable("oauth state store unavailable") from e
    if raw is None:
        return None
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode()
    try:
        data = json.loads(raw)
    except (ValueError, TypeError):
        logger.warning("oauth_state_payload_corrupt", prefix=prefix)
        return None
    return data if isinstance(data, dict) else None
