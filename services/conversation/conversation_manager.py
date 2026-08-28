"""
PM-034 Phase 3: ConversationManager - Core Conversation Context Management
Built on bulletproof foundation: AsyncSessionFactory + Circuit Breaker + Health Monitoring
Target: 10-turn context window, <150ms additional latency, 90% reference resolution

Architecture (#1207 unification, 2026-06-12 — single source of truth):
- The DOMAIN owns the concepts: ``Conversation`` + ``ConversationTurn``
  (services/domain/models.py). This manager is the application-service
  access path to them (ADR-029 mediation) — it persists turns and reads
  them back; it does NOT define its own context aggregate. (The anemic
  manager-local ``ConversationContext`` class was eliminated per the
  ADR-005 dual-implementation rule: "conversation + turns" is what the
  domain ``Conversation`` already expresses.)
- The DATABASE (conversation_turns + conversations.context JSONB) is the
  system of record. Redis, when configured, is a read-through cache of
  recent-turn lists; the production container currently constructs this
  manager WITHOUT a redis client, so reads come from the DB.
- The in-process discourse working state
  (services/intent_service/conversation_context.ConversationContext —
  lens stack, last offer, floor flags, provenance sidecar, recent-turn
  window) is a PROJECTION over this manager's data: it hydrates via
  ``get_recent_turns()`` (#1122) and ``load_context_state()`` (#953), and
  every completed turn is written back through ``save_conversation_turn``
  at the process_intent outer seam. It never persists anything itself.
"""

import json
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

import redis.asyncio as redis
import structlog

from services.conversation.reference_resolver import ReferenceResolver, ResolvedReference
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import ConversationTurn
from services.health.integration_health_monitor import health_monitor

logger = structlog.get_logger()

# #1532 F3: sentinel distinguishing "caller did not thread a principal" (legacy /
# internal callers — unscoped m-40 shim, WARNs) from "caller threaded user_id=None"
# (a genuinely anonymous principal — ENFORCED: may only read conversations that
# have no owner). Mirrors the ConversationRepository.get_by_id D3 shim (#1252).
UNSCOPED_PRINCIPAL = object()


def _owner_matches(owner, principal) -> bool:
    """#1532 F3 ownership contract for conversation reads/appends.

    - anonymous-owned row (owner None) → readable ONLY by the anonymous path
      (principal None). An authenticated principal hitting an anonymous-owned
      conversation id is treated as NOT-FOUND (the safe contract).
    - owned row → readable ONLY by that owner (string-compared, like the REST
      rule at web/api/routes/conversations.py:173).
    - anonymous principal hitting an owned row → NOT-FOUND (never leak).

    Single source of truth: delegates to the shared repository-layer rule so
    the read side and the append side (ensure_conversation_exists) can't drift.
    """
    from services.database.repositories import conversation_ownership_matches

    return conversation_ownership_matches(owner, principal)


class ConversationManager:
    """
    Core conversation persistence + recent-turn access (single access path)

    Features:
    - 10-turn context window
    - Redis caching (5-min TTL) of recent-turn lists, when configured
    - Anaphoric reference resolution
    - Circuit breaker protection
    - Stateless design (no global state)
    """

    def __init__(
        self,
        redis_client: Optional[redis.Redis] = None,
        context_window_size: int = 10,
        cache_ttl: int = 300,  # 5 minutes
    ):
        self.redis_client = redis_client
        self.context_window_size = context_window_size
        self.cache_ttl = cache_ttl
        self.reference_resolver = ReferenceResolver()

        # Circuit breaker for Redis operations
        self.redis_failure_count = 0
        self.redis_last_failure = 0
        self.redis_circuit_open = False
        self.circuit_breaker_threshold = 3
        self.circuit_breaker_timeout = 60  # 1 minute

        logger.info(
            "ConversationManager initialized",
            context_window=context_window_size,
            cache_ttl=cache_ttl,
        )

    async def get_recent_turns(
        self, conversation_id: str, limit: Optional[int] = None, user_id=UNSCOPED_PRINCIPAL
    ) -> List[ConversationTurn]:
        """Get the recent persisted turns for a conversation (cache → DB).

        THE read path for conversation history (#1207): the discourse
        working state hydrates from here, and reference resolution reads
        from here. Returns domain ``ConversationTurn`` objects ordered by
        turn_number; empty list when the conversation has no turns (or on
        any failure — read is best-effort, never raises).

        #1532 F3: ``user_id`` is the requesting principal. When threaded, the
        read verifies conversation ownership FIRST (before cache or DB): an
        owner mismatch behaves as not-found (empty list) + a warning log with
        both ids — turns are never leaked across principals. When omitted
        (legacy sentinel) the read is unscoped and WARNs (m-40 shim). The
        ownership probe runs before the cache read on purpose: the cache key
        is not principal-scoped, so the check must gate BOTH sources.
        """
        limit = limit or self.context_window_size
        try:
            if user_id is UNSCOPED_PRINCIPAL:
                logger.warning(
                    "conversation_turns_read_without_principal",
                    conversation_id=str(conversation_id),
                )
            elif not await self._principal_owns_conversation(
                conversation_id, user_id, surface="get_recent_turns"
            ):
                return []
            # Try Redis cache first (with circuit breaker)
            cached_turns = await self._get_from_cache(conversation_id)
            if cached_turns:
                health_monitor.record_success(
                    "conversation_cache", 5.0, {"cache": "hit", "conversation_id": conversation_id}
                )
                return cached_turns[-limit:]

            # Fallback to database
            db_turns = await self._get_from_database(conversation_id)
            if db_turns:
                # Cache for future use
                await self._save_to_cache(conversation_id, db_turns)
                health_monitor.record_success(
                    "conversation_cache",
                    25.0,
                    {"cache": "miss", "conversation_id": conversation_id},
                )
                return db_turns[-limit:]

            return []

        except Exception as e:
            logger.error(f"Failed to get recent turns: {e}")
            health_monitor.record_failure("conversation_cache", str(e))
            return []

    async def save_conversation_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str,
        entities: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        provenance: Optional[dict] = None,
        context_state: Optional[dict] = None,
        intent: Optional[str] = None,
    ) -> ConversationTurn:
        """Save new conversation turn and update context.

        Args:
            conversation_id: The conversation/session ID
            user_message: The user's message
            assistant_response: The assistant's response
            entities: Optional list of extracted entities
            user_id: Optional user ID for conversation ownership (Issue #563)
            provenance: Optional provenance dict (Issue #1030 R4) — gets nested
                into turn.metadata['provenance'] for cross-session lookup
                (PM Q1 disposition: GUARANTEED cross-session).
            context_state: Optional Layer-4 context slice (Issue #953) — lens_stack
                + last_offer + floor flags — persisted into ConversationDB.context
                in the SAME session as the turn (row guaranteed via save_turn's
                ensure_conversation_exists). Best-effort; None = skip.
            intent: Optional resolved intent label (Issue #1518) — persisted to
                conversation_turns.intent ("category:action" or bare category)
                so routing telemetry exists for every turn. Before #1518 this
                was never passed and the column was always NULL on live turns.

        Returns:
            The saved ConversationTurn
        """
        # Issue #1030 R4: provenance nested into metadata for JSONB persistence
        metadata = {}
        if provenance:
            metadata["provenance"] = provenance

        turn = ConversationTurn(
            id=str(uuid4()),
            conversation_id=conversation_id,
            turn_number=await self._get_next_turn_number(conversation_id),
            user_message=user_message,
            assistant_response=assistant_response,
            intent=intent,
            entities=entities or [],
            metadata=metadata,
            created_at=datetime.now(),
        )

        # Save to database (pass user_id for conversation ownership)
        await self._save_turn_to_database(turn, user_id=user_id, context_state=context_state)

        # Update cached context
        await self._update_cached_context(conversation_id, turn)

        logger.info(
            "Conversation turn saved",
            conversation_id=conversation_id,
            turn_id=turn.id,
            turn_number=turn.turn_number,
        )

        return turn

    async def resolve_references_in_message(
        self, message: str, conversation_id: str, user_id=UNSCOPED_PRINCIPAL
    ) -> Tuple[str, List[ResolvedReference]]:
        """Resolve anaphoric references using conversation context.

        #1532 F3: threads the requesting principal through to the ownership-
        checked ``get_recent_turns`` read (sentinel pass-through preserved).
        """
        start_time = time.time()

        try:
            # Last 5 turns for performance
            recent_turns = await self.get_recent_turns(conversation_id, limit=5, user_id=user_id)
            if not recent_turns:
                return message, []

            # Resolve references
            resolved_message, references = self.reference_resolver.resolve_references(
                message, recent_turns
            )

            resolution_time = (time.time() - start_time) * 1000  # Convert to ms

            health_monitor.record_success(
                "reference_resolution",
                resolution_time,
                {
                    "references_resolved": len(references),
                    "conversation_id": conversation_id,
                    "performance_target": resolution_time < 150,
                },
            )

            logger.info(
                "References resolved",
                conversation_id=conversation_id,
                original_message=message,
                resolved_message=resolved_message,
                references_count=len(references),
                latency_ms=resolution_time,
            )

            return resolved_message, references

        except Exception as e:
            resolution_time = (time.time() - start_time) * 1000
            logger.error(f"Reference resolution failed: {e}")
            health_monitor.record_failure(
                "reference_resolution", str(e), {"latency_ms": resolution_time}
            )
            return message, []  # Graceful degradation

    async def _get_from_cache(self, conversation_id: str) -> Optional[List[ConversationTurn]]:
        """Get recent turns from Redis cache with circuit breaker.

        Key prefix is ``conversation_turns:`` (#1207 — the old
        ``conversation:`` entries serialized the deleted context aggregate;
        prefix change orphans them safely, TTL reaps them).
        """
        if self.redis_circuit_open or not self.redis_client:
            return None

        try:
            cache_key = f"conversation_turns:{conversation_id}"
            cached_data = await self.redis_client.get(cache_key)

            if cached_data:
                data = json.loads(cached_data)
                return [
                    ConversationTurn(
                        id=turn_data["id"],
                        conversation_id=turn_data["conversation_id"],
                        turn_number=turn_data["turn_number"],
                        user_message=turn_data["user_message"],
                        assistant_response=turn_data["assistant_response"],
                        entities=turn_data["entities"],
                        created_at=datetime.fromisoformat(turn_data["created_at"]),
                    )
                    for turn_data in data["turns"]
                ]

            return None

        except Exception as e:
            await self._handle_redis_failure(e)
            return None

    async def _save_to_cache(self, conversation_id: str, turns: List[ConversationTurn]) -> None:
        """Save recent turns to Redis cache with circuit breaker"""
        if self.redis_circuit_open or not self.redis_client:
            return

        try:
            cache_key = f"conversation_turns:{conversation_id}"

            # Serialize to JSON (bounded by the context window)
            data = {
                "turns": [
                    {
                        "id": turn.id,
                        "conversation_id": turn.conversation_id,
                        "turn_number": turn.turn_number,
                        "user_message": turn.user_message,
                        "assistant_response": turn.assistant_response,
                        "entities": turn.entities,
                        "created_at": turn.created_at.isoformat(),
                    }
                    for turn in turns[-self.context_window_size :]
                ],
            }

            await self.redis_client.setex(cache_key, self.cache_ttl, json.dumps(data))

        except Exception as e:
            await self._handle_redis_failure(e)

    async def _get_from_database(self, conversation_id: str) -> List[ConversationTurn]:
        """Get recent turns from database using AsyncSessionFactory"""
        try:
            async with AsyncSessionFactory.session_scope() as session:
                from services.database.repositories import ConversationRepository

                repo = ConversationRepository(session)
                # #1223: this is the "recent turns" fallback — fetch the NEWEST
                # window, not the oldest. (Cache path already returns newest.)
                return await repo.get_conversation_turns(
                    conversation_id, limit=self.context_window_size, most_recent=True
                )

        except Exception as e:
            logger.error(f"Database query failed: {e}")
            return []

    async def _save_turn_to_database(
        self,
        turn: ConversationTurn,
        user_id: Optional[str] = None,
        context_state: Optional[dict] = None,
    ) -> None:
        """Save conversation turn to database using AsyncSessionFactory.

        Args:
            turn: The ConversationTurn to save
            user_id: Optional user ID for conversation ownership (Issue #563)
            context_state: Optional Layer-4 context slice (#953) persisted in the
                same session, after the turn (so the conversation row exists).
        """
        try:
            async with AsyncSessionFactory.session_scope() as session:
                from services.database.repositories import ConversationRepository

                repo = ConversationRepository(session)
                await repo.save_turn(turn, user_id=user_id)
                # #953: persist the context slice in the same transaction. save_turn
                # ran ensure_conversation_exists, so the row is present.
                if context_state is not None:
                    await repo.save_context_state(turn.conversation_id, context_state)

        except Exception as e:
            logger.error(f"Failed to save turn to database: {e}")

    async def load_context_state(
        self, conversation_id: str, user_id=UNSCOPED_PRINCIPAL
    ) -> Optional[dict]:
        """#953: load the persisted Layer-4 context slice for a conversation,
        or None. Best-effort (returns None on any error / missing row).

        #1532 F3: when a principal is threaded, ownership is verified first —
        an owner mismatch behaves as not-found (None) + warning log; the
        state is never leaked across principals. Omitted principal = unscoped
        m-40 shim (WARNs)."""
        try:
            if user_id is UNSCOPED_PRINCIPAL:
                logger.warning(
                    "conversation_state_read_without_principal",
                    conversation_id=str(conversation_id),
                )
            elif not await self._principal_owns_conversation(
                conversation_id, user_id, surface="load_context_state"
            ):
                return None
            async with AsyncSessionFactory.session_scope() as session:
                from services.database.repositories import ConversationRepository

                repo = ConversationRepository(session)
                return await repo.load_context_state(conversation_id)
        except Exception as e:
            logger.error(f"Failed to load context state: {e}")
            return None

    async def _principal_owns_conversation(
        self, conversation_id: str, user_id: Optional[str], surface: str
    ) -> bool:
        """#1532 F3 ownership probe — runs BEFORE any turn/state read when a
        principal is threaded. Missing row → vacuously True (there is nothing
        to protect; downstream reads return empty anyway). Owner mismatch →
        False + a warning naming both ids. Raises on DB failure so callers'
        best-effort except blocks fail CLOSED (empty/None), never open."""
        async with AsyncSessionFactory.session_scope() as session:
            from services.database.models import ConversationDB

            row = await session.get(ConversationDB, conversation_id)
            if row is None:
                return True
            owner = row.user_id  # read inside the session (avoid detached access)
        if _owner_matches(owner, user_id):
            return True
        logger.warning(
            "conversation_owner_mismatch",
            surface=surface,
            conversation_id=str(conversation_id),
            conversation_owner=str(owner),
            requesting_principal=str(user_id) if user_id is not None else "anonymous",
        )
        return False

    async def _get_next_turn_number(self, conversation_id: str) -> int:
        """Get next turn number for conversation"""
        try:
            async with AsyncSessionFactory.session_scope() as session:
                from services.database.repositories import ConversationRepository

                repo = ConversationRepository(session)
                return await repo.get_next_turn_number(conversation_id)

        except Exception as e:
            logger.error(f"Failed to get next turn number: {e}")
            return 1  # Fallback to turn 1

    async def _update_cached_context(
        self, conversation_id: str, new_turn: ConversationTurn
    ) -> None:
        """Append a new turn to the cached recent-turn list (if cached)"""
        turns = await self._get_from_cache(conversation_id)
        if turns:
            turns.append(new_turn)
            await self._save_to_cache(conversation_id, turns)

    async def _handle_redis_failure(self, error: Exception) -> None:
        """Handle Redis failures with circuit breaker pattern"""
        self.redis_failure_count += 1
        self.redis_last_failure = time.time()

        if self.redis_failure_count >= self.circuit_breaker_threshold:
            self.redis_circuit_open = True
            logger.warning(
                "Redis circuit breaker opened",
                failure_count=self.redis_failure_count,
                error=str(error),
            )

        # Check if we should close the circuit breaker
        if (
            self.redis_circuit_open
            and time.time() - self.redis_last_failure > self.circuit_breaker_timeout
        ):
            self.redis_circuit_open = False
            self.redis_failure_count = 0
            logger.info("Redis circuit breaker closed")

    async def get_manager_stats(self) -> Dict[str, Any]:
        """Get conversation manager statistics"""
        return {
            "conversation_manager": "active",
            "context_window_size": self.context_window_size,
            "cache_ttl": self.cache_ttl,
            "redis_available": self.redis_client is not None,
            "redis_circuit_open": self.redis_circuit_open,
            "redis_failure_count": self.redis_failure_count,
            "components": {
                "reference_resolver": True,
                "redis_cache": not self.redis_circuit_open,
                "database_fallback": True,
            },
        }
