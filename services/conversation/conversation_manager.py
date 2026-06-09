"""
PM-034 Phase 3: ConversationManager - Core Conversation Context Management
Built on bulletproof foundation: AsyncSessionFactory + Circuit Breaker + Health Monitoring
Target: 10-turn context window, <150ms additional latency, 90% reference resolution
"""

import json
import time
from dataclasses import asdict, dataclass
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


@dataclass
class ConversationContext:
    """Conversation context with bounded window"""

    conversation_id: str
    turns: List[ConversationTurn]
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any]

    def get_recent_turns(self, limit: int = 10) -> List[ConversationTurn]:
        """Get most recent turns within window limit"""
        return sorted(self.turns, key=lambda t: t.created_at)[-limit:]

    def add_turn(self, turn: ConversationTurn) -> None:
        """Add turn and maintain window size"""
        self.turns.append(turn)
        # Keep only last 10 turns for performance
        if len(self.turns) > 10:
            self.turns = self.turns[-10:]
        self.updated_at = datetime.now()


class ConversationManager:
    """
    Core conversation context management with Redis caching

    Features:
    - 10-turn context window
    - Redis caching (5-min TTL)
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

    async def get_conversation_context(self, conversation_id: str) -> Optional[ConversationContext]:
        """Get conversation context with Redis caching"""
        try:
            # Try Redis cache first (with circuit breaker)
            cached_context = await self._get_from_cache(conversation_id)
            if cached_context:
                health_monitor.record_success(
                    "conversation_cache", 5.0, {"cache": "hit", "conversation_id": conversation_id}
                )
                return cached_context

            # Fallback to database
            db_context = await self._get_from_database(conversation_id)
            if db_context:
                # Cache for future use
                await self._save_to_cache(db_context)
                health_monitor.record_success(
                    "conversation_cache",
                    25.0,
                    {"cache": "miss", "conversation_id": conversation_id},
                )
                return db_context

            return None

        except Exception as e:
            logger.error(f"Failed to get conversation context: {e}")
            health_monitor.record_failure("conversation_cache", str(e))
            return None

    async def save_conversation_turn(
        self,
        conversation_id: str,
        user_message: str,
        assistant_response: str,
        entities: Optional[List[str]] = None,
        user_id: Optional[str] = None,
        provenance: Optional[dict] = None,
        context_state: Optional[dict] = None,
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
        self, message: str, conversation_id: str
    ) -> Tuple[str, List[ResolvedReference]]:
        """Resolve anaphoric references using conversation context"""
        start_time = time.time()

        try:
            # Get conversation context
            context = await self.get_conversation_context(conversation_id)
            if not context:
                return message, []

            # Get recent turns for reference resolution
            recent_turns = context.get_recent_turns(limit=5)  # Last 5 turns for performance

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

    async def _get_from_cache(self, conversation_id: str) -> Optional[ConversationContext]:
        """Get conversation context from Redis cache with circuit breaker"""
        if self.redis_circuit_open or not self.redis_client:
            return None

        try:
            cache_key = f"conversation:{conversation_id}"
            cached_data = await self.redis_client.get(cache_key)

            if cached_data:
                data = json.loads(cached_data)
                # Reconstruct ConversationContext
                turns = [
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

                return ConversationContext(
                    conversation_id=data["conversation_id"],
                    turns=turns,
                    created_at=datetime.fromisoformat(data["created_at"]),
                    updated_at=datetime.fromisoformat(data["updated_at"]),
                    metadata=data["metadata"],
                )

            return None

        except Exception as e:
            await self._handle_redis_failure(e)
            return None

    async def _save_to_cache(self, context: ConversationContext) -> None:
        """Save conversation context to Redis cache with circuit breaker"""
        if self.redis_circuit_open or not self.redis_client:
            return

        try:
            cache_key = f"conversation:{context.conversation_id}"

            # Serialize to JSON
            data = {
                "conversation_id": context.conversation_id,
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
                    for turn in context.turns
                ],
                "created_at": context.created_at.isoformat(),
                "updated_at": context.updated_at.isoformat(),
                "metadata": context.metadata,
            }

            await self.redis_client.setex(cache_key, self.cache_ttl, json.dumps(data))

        except Exception as e:
            await self._handle_redis_failure(e)

    async def _get_from_database(self, conversation_id: str) -> Optional[ConversationContext]:
        """Get conversation context from database using AsyncSessionFactory"""
        try:
            async with AsyncSessionFactory.session_scope() as session:
                from services.database.repositories import ConversationRepository

                repo = ConversationRepository(session)
                turns = await repo.get_conversation_turns(
                    conversation_id, limit=self.context_window_size
                )

                if not turns:
                    return None

                return ConversationContext(
                    conversation_id=conversation_id,
                    turns=turns,
                    created_at=min(turn.created_at for turn in turns),
                    updated_at=max(turn.created_at for turn in turns),
                    metadata={},
                )

        except Exception as e:
            logger.error(f"Database query failed: {e}")
            return None

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

    async def load_context_state(self, conversation_id: str) -> Optional[dict]:
        """#953: load the persisted Layer-4 context slice for a conversation,
        or None. Best-effort (returns None on any error / missing row)."""
        try:
            async with AsyncSessionFactory.session_scope() as session:
                from services.database.repositories import ConversationRepository

                repo = ConversationRepository(session)
                return await repo.load_context_state(conversation_id)
        except Exception as e:
            logger.error(f"Failed to load context state: {e}")
            return None

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
        """Update cached conversation context with new turn"""
        context = await self._get_from_cache(conversation_id)
        if context:
            context.add_turn(new_turn)
            await self._save_to_cache(context)

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
