"""
PM-034 Phase 2: Anaphoric Reference Resolution System
Resolves pronouns and references in conversation context
Target: 90% resolution accuracy, <150ms additional latency
"""

import re
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Tuple
from uuid import uuid4

from services.domain.models import ConversationTurn


@dataclass
class ReferenceCandidate:
    """Potential target for anaphoric reference"""

    entity: str
    entity_type: str  # "issue", "project", "file", "user", etc.
    source_turn: ConversationTurn
    confidence_score: float
    context: str


@dataclass
class ResolvedReference:
    """Successfully resolved anaphoric reference"""

    original_text: str
    resolved_entity: str
    entity_type: str
    confidence: float
    replacement_text: str


class ReferenceResolver:
    """
    Core anaphoric reference resolution system
    Identifies and resolves: "it", "that", "this", "the issue", etc.
    """

    # Reference patterns to detect (ordered by specificity)
    REFERENCE_PATTERNS = {
        "definite": [
            r"\bthe (issue|bug|feature|project|file|document|report)\b",
            r"\bthe (last|previous|recent|first|second|third|main|primary|original) (issue|bug|feature|project)\b",
            r"\bthe (login|logout|authentication|security|database|api|frontend|backend) (issue|bug|feature|project)\b",
            r"\bthat (issue|bug|feature|project|file|document|report)\b",
            r"\bthis (issue|bug|feature|project|file|document|report)\b",
        ],
        "implicit": [
            r"\bshow (it|that|this)\b",
            r"\bupdate (it|that|this)\b",
            r"\bclose (it|that|this)\b",
            r"\bcheck (it|that|this)\b",
            r"\breview (it|that|this)\b",
            r"\bsend me (it|that|this)\b",
        ],
        "pronoun": [
            r"\bit\b(?!\s+(?:is|was|will|should|can|could))",  # Exclude "it is", "it was"
            r"\bthat\b(?!\s+(?:is|was|will|should|can|could))",  # Exclude "that is"
            r"\bthis\b(?!\s+(?:is|was|will|should|can|could))",  # Exclude "this is"
            r"\bthose\b",
            r"\bthese\b",
        ],
    }

    # Entity extraction patterns from assistant responses
    ENTITY_PATTERNS = {
        "github_issue": [
            r"issue\s+#(\d+)",
            r"GitHub issue\s+#(\d+)",
            r"created issue\s+#(\d+)",
            r"issue\s+(\d+)",
        ],
        "project": [
            r'project\s+"([^"]+)"',
            r"working on\s+([A-Za-z][A-Za-z0-9\-\s]+)",
            r"project:\s+([A-Za-z][A-Za-z0-9\-\s]+)",
        ],
        "file": [
            r'file\s+"([^"]+)"',
            r"uploaded\s+([^\s]+\.(pdf|doc|txt|md|py|js|html))",
            r'document\s+"([^"]+)"',
        ],
    }

    def __init__(self, context_window_turns: int = 10):
        self.context_window_turns = context_window_turns

    def resolve_references(
        self, user_message: str, conversation_history: List[ConversationTurn]
    ) -> Tuple[str, List[ResolvedReference]]:
        """
        Main entry point: resolve all references in user message

        Args:
            user_message: Current user input with potential references
            conversation_history: Recent conversation turns (newest first)

        Returns:
            Tuple of (resolved_message, list_of_resolved_references)
        """
        start_time = datetime.now()

        # Detect references in user message
        references = self._detect_references(user_message)
        if not references:
            return user_message, []

        # Get relevant context from conversation history (most recent first)
        # Reverse to get most recent turns first
        sorted_turns = sorted(conversation_history, key=lambda t: t.turn_number, reverse=True)
        context_turns = sorted_turns[: self.context_window_turns]

        # Find candidates for each reference
        resolved_references = []
        resolved_message = user_message

        # Process references in order of specificity (definite first, then implicit, then pronouns)
        reference_priority = {"definite": 1, "implicit": 2, "pronoun": 3}
        references_sorted = sorted(references, key=lambda x: reference_priority.get(x[1], 4))

        for ref_text, ref_type in references_sorted:
            candidates = self._find_candidates(ref_text, ref_type, context_turns)

            if candidates:
                best_candidate = self._score_candidates(candidates)

                # Lower threshold for more specific references
                confidence_threshold = 0.5 if ref_type in ["definite", "implicit"] else 0.7

                if best_candidate.confidence_score >= confidence_threshold:
                    resolved_ref = ResolvedReference(
                        original_text=ref_text,
                        resolved_entity=best_candidate.entity,
                        entity_type=best_candidate.entity_type,
                        confidence=best_candidate.confidence_score,
                        replacement_text=self._generate_replacement(
                            best_candidate.entity, best_candidate.entity_type
                        ),
                    )

                    resolved_references.append(resolved_ref)

                    # Replace in message (case insensitive)
                    import re

                    pattern = re.escape(ref_text)
                    resolved_message = re.sub(
                        pattern,
                        resolved_ref.replacement_text,
                        resolved_message,
                        count=1,
                        flags=re.IGNORECASE,
                    )

        # Performance tracking
        processing_time = (datetime.now() - start_time).total_seconds() * 1000

        return resolved_message, resolved_references

    def _detect_references(self, text: str) -> List[Tuple[str, str]]:
        """Detect potential anaphoric references in text"""
        references = []
        text_lower = text.lower()

        for ref_type, patterns in self.REFERENCE_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text_lower, re.IGNORECASE)
                for match in matches:
                    references.append((match.group(), ref_type))

        return references

    def _find_candidates(
        self, reference: str, ref_type: str, context_turns: List[ConversationTurn]
    ) -> List[ReferenceCandidate]:
        """Find potential entities this reference could resolve to"""
        candidates = []

        # #1234: respect the context window HERE too. _find_candidates can be called
        # directly (not only via resolve_references, which pre-windows at line ~116), so
        # limit to the most recent N turns — otherwise anaphora can match stale,
        # out-of-window entities. (Re-windowing an already-windowed list is a no-op.)
        windowed_turns = sorted(
            context_turns, key=lambda t: t.turn_number, reverse=True
        )[: self.context_window_turns]

        for turn in windowed_turns:
            # Extract entities from assistant responses
            entities = self._extract_entities(turn.assistant_response)

            for entity, entity_type in entities:
                candidate = ReferenceCandidate(
                    entity=entity,
                    entity_type=entity_type,
                    source_turn=turn,
                    confidence_score=0.0,  # Will be calculated in scoring
                    context=f"{turn.user_message} -> {turn.assistant_response[:100]}...",
                )
                candidates.append(candidate)

        # Filter candidates based on reference context
        filtered_candidates = []
        reference_lower = reference.lower()

        for candidate in candidates:
            # If reference mentions specific type, prioritize matching types
            if "issue" in reference_lower and candidate.entity_type == "github_issue":
                candidate.confidence_score += 0.2  # Type match bonus
            elif "project" in reference_lower and candidate.entity_type == "project":
                candidate.confidence_score += 0.2
            elif "file" in reference_lower and candidate.entity_type == "file":
                candidate.confidence_score += 0.2
            elif "document" in reference_lower and candidate.entity_type == "file":
                candidate.confidence_score += 0.2

            filtered_candidates.append(candidate)

        return filtered_candidates

    def _extract_entities(self, text: str) -> List[Tuple[str, str]]:
        """Extract structured entities from assistant responses"""
        entities = []

        for entity_type, patterns in self.ENTITY_PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    if entity_type == "github_issue":
                        entity = f"#{match.group(1)}"
                    else:
                        entity = match.group(1).strip()

                    entities.append((entity, entity_type))

        return entities

    def _score_candidates(self, candidates: List[ReferenceCandidate]) -> ReferenceCandidate:
        """Score candidates by recency and type match, return best"""
        if not candidates:
            return None

        scored_candidates = []
        current_time = datetime.now()

        # Sort by turn number descending (most recent first) to give position scores
        candidates_by_recency = sorted(
            candidates, key=lambda c: c.source_turn.turn_number, reverse=True
        )

        for i, candidate in enumerate(candidates_by_recency):
            score = 0.0

            # Start with existing candidate confidence (includes type match bonus)
            score += candidate.confidence_score

            # Recency scoring based on turn position (most recent = highest)
            position_score = 1.0 - (i * 0.1)  # Each position back reduces by 0.1
            score += max(position_score, 0.1) * 0.4  # 40% weight, minimum 0.1

            # Entity type relevance scoring
            if candidate.entity_type == "github_issue":
                score += 0.35  # Issues are most common references
            elif candidate.entity_type == "project":
                score += 0.25
            elif candidate.entity_type == "file":
                score += 0.15  # Lower score for files unless specifically requested
            else:
                score += 0.1

            # Boost score if this is the most recent entity of its type
            if i == 0:
                score += 0.05  # Small recency boost

            candidate.confidence_score = min(score, 1.0)
            scored_candidates.append(candidate)

        # Return highest scoring candidate
        return max(scored_candidates, key=lambda c: c.confidence_score)

    def _generate_replacement(self, entity: str, entity_type: str) -> str:
        """Generate appropriate replacement text for resolved entity"""
        if entity_type == "github_issue":
            return f"GitHub issue {entity}"
        elif entity_type == "project":
            return f'project "{entity}"'
        elif entity_type == "file":
            return f'file "{entity}"'
        else:
            return entity

    def get_resolution_stats(self, conversation_history: List[ConversationTurn]) -> Dict[str, Any]:
        """Get statistics about reference resolution capability"""
        stats = {
            "total_turns": len(conversation_history),
            "turns_with_references": 0,
            "entities_available": 0,
            "entity_types": {},
            "context_window_coverage": min(self.context_window_turns, len(conversation_history)),
        }

        for turn in conversation_history:
            entities = self._extract_entities(turn.assistant_response)
            if entities:
                stats["entities_available"] += len(entities)

                for entity, entity_type in entities:
                    stats["entity_types"][entity_type] = (
                        stats["entity_types"].get(entity_type, 0) + 1
                    )

        return stats


class ConversationMemoryService:
    """
    Service to retrieve conversation turns from database
    Integrates with Phase 1 database foundation
    """

    def __init__(self):
        # Integrate with AsyncSessionFactory from Phase 1
        from services.database.repositories import ConversationRepository
        from services.database.session_factory import AsyncSessionFactory

        self.session_factory = AsyncSessionFactory()
        self.reference_resolver = ReferenceResolver()

    async def resolve_user_message(
        self, user_message: str, conversation_id: str
    ) -> Tuple[str, List[ResolvedReference], Dict[str, Any]]:
        """
        High-level service method for reference resolution

        Returns:
            Tuple of (resolved_message, resolved_references, metadata)
        """
        # Get conversation history from database
        conversation_history = await self._get_conversation_history(conversation_id)

        resolved_message, resolved_refs = self.reference_resolver.resolve_references(
            user_message, conversation_history
        )

        metadata = {
            "original_message": user_message,
            "resolution_count": len(resolved_refs),
            "confidence_scores": [r.confidence for r in resolved_refs],
            "context_window_size": len(conversation_history[:10]),
        }

        return resolved_message, resolved_refs, metadata

    async def _get_conversation_history(self, conversation_id: str) -> List[ConversationTurn]:
        """Retrieve conversation turns from database (Phase 1 foundation)"""
        try:
            async with self.session_factory.get_session() as session:
                # Get recent conversation turns (last 10 for context window)
                from services.database.repositories import ConversationRepository

                repo = ConversationRepository(session)
                # #1223: reference resolution needs the most-recent turns for
                # the context window, not the oldest.
                turns = await repo.get_conversation_turns(
                    conversation_id, limit=10, most_recent=True
                )
                return turns
        except Exception as e:
            # Log error but don't fail - return empty context
            import structlog

            logger = structlog.get_logger()
            logger.warning(
                "Failed to retrieve conversation history",
                conversation_id=conversation_id,
                error=str(e),
            )
            return []
