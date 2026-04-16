"""
Enhanced Conversation Context Tracker

Builds on existing ConversationManager and ReferenceResolver to provide
improved context tracking, entity persistence, and conversation continuity.

Issue #248 CORE-UX-CONVERSATION-CONTEXT
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Set, Tuple
from uuid import UUID, uuid4

import structlog

from services.conversation.conversation_manager import ConversationContext, ConversationManager
from services.conversation.reference_resolver import ConversationMemoryService, ResolvedReference
from services.database.repositories import ConversationRepository
from services.database.session_factory import AsyncSessionFactory
from services.domain.models import ConversationTurn
from services.user_context_service import UserContextService

logger = structlog.get_logger()


@dataclass
class EntityMention:
    """Tracks mentions of entities across conversation"""

    entity_id: str
    entity_type: str  # "issue", "project", "file", "user", etc.
    first_mentioned: datetime
    last_mentioned: datetime
    mention_count: int
    aliases: Set[str] = field(default_factory=set)  # "the bug", "that issue", etc.
    context_snippets: List[str] = field(default_factory=list)  # Recent context


@dataclass
class ConversationState:
    """Enhanced conversation state with entity tracking"""

    conversation_id: str
    current_topic: Optional[str] = None
    active_entities: Dict[str, EntityMention] = field(default_factory=dict)
    user_intent_history: List[str] = field(default_factory=list)
    conversation_flow: List[str] = field(
        default_factory=list
    )  # "greeting", "question", "clarification", etc.
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)


@dataclass
class ContextEnrichment:
    """Result of context enrichment process"""

    original_message: str
    enriched_message: str
    resolved_references: List[ResolvedReference]
    active_entities: List[EntityMention]
    conversation_state: ConversationState
    confidence_score: float
    enrichment_metadata: Dict[str, Any]


class EnhancedContextTracker:
    """
    Enhanced conversation context tracker that builds on existing infrastructure
    """

    def __init__(self):
        # Use existing services
        self.conversation_manager = ConversationManager()
        self.memory_service = ConversationMemoryService()
        self.user_context_service = UserContextService()

        # Enhanced tracking
        self.conversation_states: Dict[str, ConversationState] = {}
        self.entity_patterns = self._load_entity_patterns()

        # Performance tracking
        self.enrichment_stats = {
            "total_enrichments": 0,
            "successful_resolutions": 0,
            "entity_extractions": 0,
            "avg_processing_time": 0.0,
        }

    def _load_entity_patterns(self) -> Dict[str, List[str]]:
        """Load patterns for entity extraction"""
        return {
            "issue": [
                r"issue #?(\d+)",
                r"bug #?(\d+)",
                r"ticket #?(\d+)",
                r"(the|this|that) (issue|bug|ticket|problem)",
            ],
            "project": [
                r"project ([a-zA-Z0-9-_]+)",
                r"repo(sitory)? ([a-zA-Z0-9-_/]+)",
                r"(the|this|that) (project|repo|repository)",
            ],
            "file": [
                r"file ([a-zA-Z0-9-_./]+)",
                r"([a-zA-Z0-9-_]+\.(py|js|ts|md|json|yaml|yml))",
                r"(the|this|that) (file|script|document)",
            ],
            "user": [
                r"@([a-zA-Z0-9-_]+)",
                r"user ([a-zA-Z0-9-_]+)",
            ],
        }

    async def enrich_conversation_context(
        self,
        message: str,
        conversation_id: str,
        session_id: Optional[str] = None,
        user_id: Optional[UUID] = None,
    ) -> ContextEnrichment:
        """
        Main method to enrich conversation context
        """
        start_time = time.time()

        try:
            # Get or create conversation state
            conv_state = await self._get_or_create_conversation_state(conversation_id)

            # Resolve references using existing service
            (
                resolved_message,
                resolved_refs,
                resolution_metadata,
            ) = await self.memory_service.resolve_user_message(message, conversation_id)

            # Extract and track entities
            extracted_entities = await self._extract_and_track_entities(
                resolved_message, conv_state
            )

            # Update conversation flow
            await self._update_conversation_flow(message, conv_state)

            # Get user context if available
            user_context = None
            if session_id:
                user_context = await self.user_context_service.get_user_context(session_id)

            # Calculate confidence score
            confidence_score = self._calculate_confidence_score(
                resolved_refs, extracted_entities, conv_state
            )

            # Create enrichment result
            enrichment = ContextEnrichment(
                original_message=message,
                enriched_message=resolved_message,
                resolved_references=resolved_refs,
                active_entities=list(conv_state.active_entities.values()),
                conversation_state=conv_state,
                confidence_score=confidence_score,
                enrichment_metadata={
                    "processing_time": time.time() - start_time,
                    "resolution_metadata": resolution_metadata,
                    "extracted_entities_count": len(extracted_entities),
                    "user_context_available": user_context is not None,
                    "conversation_turn_count": len(conv_state.conversation_flow),
                },
            )

            # Update stats
            self._update_stats(enrichment)

            # Persist conversation state
            await self._persist_conversation_state(conv_state)

            logger.info(
                "conversation_context_enriched",
                conversation_id=conversation_id,
                confidence_score=confidence_score,
                resolved_references=len(resolved_refs),
                active_entities=len(conv_state.active_entities),
                processing_time=enrichment.enrichment_metadata["processing_time"],
            )

            return enrichment

        except Exception as e:
            logger.error(
                "conversation_context_enrichment_failed",
                conversation_id=conversation_id,
                error=str(e),
                processing_time=time.time() - start_time,
            )

            # Return minimal enrichment on error
            return ContextEnrichment(
                original_message=message,
                enriched_message=message,
                resolved_references=[],
                active_entities=[],
                conversation_state=ConversationState(conversation_id=conversation_id),
                confidence_score=0.0,
                enrichment_metadata={"error": str(e)},
            )

    async def _get_or_create_conversation_state(self, conversation_id: str) -> ConversationState:
        """Get existing conversation state or create new one"""
        if conversation_id in self.conversation_states:
            return self.conversation_states[conversation_id]

        # Try to load from existing conversation context
        try:
            context = await self.conversation_manager.get_conversation_context(conversation_id)
            if context:
                # Convert existing context to enhanced state
                conv_state = ConversationState(
                    conversation_id=conversation_id,
                    created_at=context.created_at,
                    updated_at=context.updated_at,
                    metadata=context.metadata,
                )

                # Extract entities from existing turns
                for turn in context.turns:
                    await self._extract_and_track_entities(turn.user_message or "", conv_state)

                self.conversation_states[conversation_id] = conv_state
                return conv_state
        except Exception as e:
            logger.warning(
                "failed_to_load_existing_conversation_context",
                conversation_id=conversation_id,
                error=str(e),
            )

        # Create new conversation state
        conv_state = ConversationState(conversation_id=conversation_id)
        self.conversation_states[conversation_id] = conv_state
        return conv_state

    async def _extract_and_track_entities(
        self, message: str, conv_state: ConversationState
    ) -> List[EntityMention]:
        """Extract entities from message and update tracking"""
        import re

        extracted_entities = []
        current_time = datetime.now()

        for entity_type, patterns in self.entity_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, message, re.IGNORECASE)
                for match in matches:
                    entity_text = match.group(1) if match.groups() else match.group(0)
                    entity_id = f"{entity_type}:{entity_text.lower()}"

                    if entity_id in conv_state.active_entities:
                        # Update existing entity
                        entity = conv_state.active_entities[entity_id]
                        entity.last_mentioned = current_time
                        entity.mention_count += 1
                        entity.aliases.add(match.group(0))

                        # Keep recent context snippets (last 3)
                        context_snippet = message[max(0, match.start() - 20) : match.end() + 20]
                        entity.context_snippets.append(context_snippet)
                        if len(entity.context_snippets) > 3:
                            entity.context_snippets = entity.context_snippets[-3:]
                    else:
                        # Create new entity mention
                        entity = EntityMention(
                            entity_id=entity_id,
                            entity_type=entity_type,
                            first_mentioned=current_time,
                            last_mentioned=current_time,
                            mention_count=1,
                            aliases={match.group(0)},
                            context_snippets=[
                                message[max(0, match.start() - 20) : match.end() + 20]
                            ],
                        )
                        conv_state.active_entities[entity_id] = entity

                    extracted_entities.append(entity)

        return extracted_entities

    async def _update_conversation_flow(self, message: str, conv_state: ConversationState):
        """Update conversation flow tracking"""
        # Simple flow classification
        message_lower = message.lower().strip()

        if any(
            greeting in message_lower
            for greeting in ["hello", "hi", "hey", "good morning", "good afternoon"]
        ):
            flow_type = "greeting"
        elif message_lower.endswith("?"):
            flow_type = "question"
        elif any(word in message_lower for word in ["please", "can you", "could you", "would you"]):
            flow_type = "request"
        elif any(
            word in message_lower
            for word in ["thanks", "thank you", "great", "perfect", "excellent"]
        ):
            flow_type = "acknowledgment"
        elif any(
            word in message_lower for word in ["what", "how", "why", "when", "where", "which"]
        ):
            flow_type = "inquiry"
        else:
            flow_type = "statement"

        conv_state.conversation_flow.append(flow_type)

        # Keep flow history manageable (last 20 turns)
        if len(conv_state.conversation_flow) > 20:
            conv_state.conversation_flow = conv_state.conversation_flow[-20:]

        # Update current topic based on entities and flow
        if conv_state.active_entities:
            # Use most recently mentioned entity as current topic
            most_recent_entity = max(
                conv_state.active_entities.values(), key=lambda e: e.last_mentioned
            )
            conv_state.current_topic = (
                f"{most_recent_entity.entity_type}:{most_recent_entity.entity_id}"
            )

        conv_state.updated_at = datetime.now()

    def _calculate_confidence_score(
        self,
        resolved_refs: List[ResolvedReference],
        extracted_entities: List[EntityMention],
        conv_state: ConversationState,
    ) -> float:
        """Calculate confidence score for context enrichment"""
        score = 0.0

        # Base score for successful reference resolution
        if resolved_refs:
            avg_ref_confidence = sum(ref.confidence for ref in resolved_refs) / len(resolved_refs)
            score += avg_ref_confidence * 0.4

        # Score for entity extraction
        if extracted_entities:
            score += min(len(extracted_entities) * 0.1, 0.3)

        # Score for conversation continuity
        if len(conv_state.conversation_flow) > 1:
            score += 0.2

        # Score for active entity tracking
        if conv_state.active_entities:
            score += min(len(conv_state.active_entities) * 0.05, 0.1)

        return min(score, 1.0)

    def _update_stats(self, enrichment: ContextEnrichment):
        """Update performance statistics"""
        self.enrichment_stats["total_enrichments"] += 1

        if enrichment.resolved_references:
            self.enrichment_stats["successful_resolutions"] += 1

        if enrichment.active_entities:
            self.enrichment_stats["entity_extractions"] += 1

        # Update average processing time
        processing_time = enrichment.enrichment_metadata.get("processing_time", 0.0)
        current_avg = self.enrichment_stats["avg_processing_time"]
        total_enrichments = self.enrichment_stats["total_enrichments"]

        self.enrichment_stats["avg_processing_time"] = (
            current_avg * (total_enrichments - 1) + processing_time
        ) / total_enrichments

    async def _persist_conversation_state(self, conv_state: ConversationState):
        """Persist conversation state to storage"""
        try:
            # Store in conversation manager's context
            await self.conversation_manager.update_conversation_metadata(
                conv_state.conversation_id,
                {
                    "enhanced_context": {
                        "current_topic": conv_state.current_topic,
                        "active_entities_count": len(conv_state.active_entities),
                        "conversation_flow": conv_state.conversation_flow[-5:],  # Last 5 turns
                        "updated_at": conv_state.updated_at.isoformat(),
                    }
                },
            )
        except Exception as e:
            logger.warning(
                "failed_to_persist_conversation_state",
                conversation_id=conv_state.conversation_id,
                error=str(e),
            )

    def _calculate_conversation_age(self, created_at: datetime) -> float:
        """Calculate conversation age in seconds, handling timezone correctly.

        Issue #771: Database now uses timestamptz, so we can use timezone-aware
        datetime comparison directly.
        """
        from services.utils.datetime_utils import ensure_utc, utc_now

        now = utc_now()
        created_utc = ensure_utc(created_at)
        return (now - created_utc).total_seconds()

    async def get_conversation_summary(self, conversation_id: str) -> Dict[str, Any]:
        """Get summary of conversation context"""
        conv_state = self.conversation_states.get(conversation_id)
        if not conv_state:
            return {"error": "Conversation not found"}

        return {
            "conversation_id": conversation_id,
            "current_topic": conv_state.current_topic,
            "active_entities": {
                entity_id: {
                    "type": entity.entity_type,
                    "mention_count": entity.mention_count,
                    "last_mentioned": entity.last_mentioned.isoformat(),
                    "aliases": list(entity.aliases),
                }
                for entity_id, entity in conv_state.active_entities.items()
            },
            "conversation_flow": conv_state.conversation_flow[-10:],  # Last 10 turns
            "stats": {
                "total_turns": len(conv_state.conversation_flow),
                "unique_entities": len(conv_state.active_entities),
                # Issue #768: Use UTC for comparison since created_at may come from database
                "conversation_age": self._calculate_conversation_age(conv_state.created_at),
            },
        }

    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics"""
        return {
            **self.enrichment_stats,
            "active_conversations": len(self.conversation_states),
            "success_rate": (
                self.enrichment_stats["successful_resolutions"]
                / max(self.enrichment_stats["total_enrichments"], 1)
            ),
        }


# Global instance for easy access
enhanced_context_tracker = EnhancedContextTracker()


# Convenience functions
async def enrich_message_context(
    message: str,
    conversation_id: str,
    session_id: Optional[str] = None,
    user_id: Optional[UUID] = None,
) -> ContextEnrichment:
    """Convenience function to enrich message context"""
    return await enhanced_context_tracker.enrich_conversation_context(
        message, conversation_id, session_id, user_id
    )


async def get_conversation_context_summary(conversation_id: str) -> Dict[str, Any]:
    """Convenience function to get conversation summary"""
    return await enhanced_context_tracker.get_conversation_summary(conversation_id)
