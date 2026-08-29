# ADR-054: Cross-Session Memory Architecture

**Status**: APPROVED
**Date**: 2026-01-13
**Authors**: Chief Architect
**Deciders**: PM, CXO, PPM
**References**: PDR-002 (Conversational Glue), ADR-053 (Trust Computation), CXO UX Summary Report (Jan 3, 2026)

---

## Context

### Problem Statement

PDR-002 establishes a Three-Layer Context Persistence Model for Piper's memory:

| Layer | Scope | Purpose |
|-------|-------|---------|
| **Conversational Memory** | 24-hour window | Natural continuity ("yesterday we discussed...") |
| **User History** | All past conversations | User-accessible archive (Claude-style chat list) |
| **Composted Learning** | Extracted patterns | Informs behavior without explicit recall |

This ADR specifies the architectural implementation for cross-session memory (Layers 1 and 2). Layer 3 (Composted Learning) is addressed separately as part of the Learning System architecture.

### Design Constraints

From PDR-002 and CXO guidance:

1. **Explicit, not implicit**: When Piper references past context, it must be transparent ("Yesterday you asked about X—shall I pick up?")
2. **"Thoughtful colleague" test**: Remember work context and stated preferences; don't remember casual asides or inferred personal details
3. **Never trap users**: Always offer the pivot to fresh context
4. **Selective memory is more human**: "Remember everything" rejected as creepy
5. **Privacy mode consideration**: Users should be able to exclude sessions from memory

### Current State

- **Session memory**: 10-turn rolling window within a session (implemented)
- **Conversation persistence**: Database storage via `conversation_turns` table (implemented, Issue #563)
- **Cross-session continuity**: Partial (localStorage for active conversation, Issue #583)
- **Context-aware greetings**: Not implemented (design in PDR-001/002)

---

## Decision

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────┐
│                     Cross-Session Memory System                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────┐    ┌─────────────────┐    ┌────────────────┐  │
│  │  Layer 1:       │    │  Layer 2:       │    │  Layer 3:      │  │
│  │  Conversational │───▶│  User History   │───▶│  Composted     │  │
│  │  Memory (24hr)  │    │  (All Time)     │    │  Learning      │  │
│  └────────┬────────┘    └────────┬────────┘    └────────────────┘  │
│           │                      │                    (separate)    │
│           ▼                      ▼                                  │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                  MemoryRetrievalService                      │   │
│  │  - getRecentContext(user_id, window=24h)                     │   │
│  │  - getConversationSummary(conversation_id)                   │   │
│  │  - getGreetingContext(user_id) → GreetingContext             │   │
│  │  - searchHistory(user_id, query) → [Conversations]           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Layer 1: Conversational Memory (24-Hour Window)

**Purpose**: Enable natural continuity references ("yesterday we discussed...")

```python
# services/memory/conversational_memory.py

@dataclass
class ConversationalMemoryEntry:
    """A memorable item from recent conversation"""
    conversation_id: UUID
    timestamp: datetime
    topic_summary: str           # Brief summary of what was discussed
    entities_mentioned: List[str] # Projects, issues, people referenced
    outcome: Optional[str]        # What was decided/accomplished
    user_sentiment: Optional[str] # positive/neutral/negative (for greeting)

@dataclass
class ConversationalMemoryWindow:
    """24-hour memory window for a user"""
    user_id: UUID
    entries: List[ConversationalMemoryEntry]
    window_start: datetime
    window_end: datetime

    def get_most_recent(self) -> Optional[ConversationalMemoryEntry]:
        """Get most recent conversation in window"""
        return self.entries[0] if self.entries else None

    def get_active_topics(self) -> List[str]:
        """Get topics discussed in window"""
        return list(set(e.topic_summary for e in self.entries))

    def get_active_entities(self) -> List[str]:
        """Get all entities mentioned in window"""
        entities = []
        for entry in self.entries:
            entities.extend(entry.entities_mentioned)
        return list(set(entities))


class ConversationalMemoryService:
    """Manages 24-hour conversational memory"""

    WINDOW_HOURS = 24

    async def record_conversation_end(
        self,
        user_id: UUID,
        conversation_id: UUID,
        summary: str,
        entities: List[str],
        outcome: Optional[str] = None,
        sentiment: Optional[str] = None
    ) -> None:
        """Record conversation summary when session ends"""

        entry = ConversationalMemoryEntry(
            conversation_id=conversation_id,
            timestamp=datetime.utcnow(),
            topic_summary=summary,
            entities_mentioned=entities,
            outcome=outcome,
            user_sentiment=sentiment
        )

        await self.repository.save_entry(user_id, entry)
        await self._prune_old_entries(user_id)

    async def get_memory_window(self, user_id: UUID) -> ConversationalMemoryWindow:
        """Get 24-hour memory window for user"""

        window_start = datetime.utcnow() - timedelta(hours=self.WINDOW_HOURS)
        entries = await self.repository.get_entries_since(user_id, window_start)

        return ConversationalMemoryWindow(
            user_id=user_id,
            entries=entries,
            window_start=window_start,
            window_end=datetime.utcnow()
        )

    async def _prune_old_entries(self, user_id: UUID) -> None:
        """Remove entries older than window"""
        cutoff = datetime.utcnow() - timedelta(hours=self.WINDOW_HOURS)
        await self.repository.delete_entries_before(user_id, cutoff)
```

### Layer 2: User History (All Conversations)

**Purpose**: User-accessible archive with search capability

```python
# services/memory/user_history.py

@dataclass
class ConversationSummary:
    """Summary of a conversation for history display"""
    conversation_id: UUID
    title: str                   # Auto-generated or user-set
    started_at: datetime
    last_activity: datetime
    turn_count: int
    topics: List[str]
    preview: str                 # First user message or summary
    is_private: bool = False     # Privacy mode flag

@dataclass
class UserHistoryPage:
    """Paginated conversation history"""
    conversations: List[ConversationSummary]
    total_count: int
    page: int
    page_size: int
    has_more: bool


class UserHistoryService:
    """Manages user's conversation history"""

    DEFAULT_PAGE_SIZE = 20

    async def get_history(
        self,
        user_id: UUID,
        page: int = 1,
        page_size: int = DEFAULT_PAGE_SIZE,
        include_private: bool = False
    ) -> UserHistoryPage:
        """Get paginated conversation history"""

        conversations = await self.repository.get_conversations(
            user_id=user_id,
            offset=(page - 1) * page_size,
            limit=page_size,
            include_private=include_private
        )

        total = await self.repository.count_conversations(user_id, include_private)

        return UserHistoryPage(
            conversations=conversations,
            total_count=total,
            page=page,
            page_size=page_size,
            has_more=(page * page_size) < total
        )

    async def search_history(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10
    ) -> List[ConversationSummary]:
        """Search conversation history by content"""

        # Full-text search on conversation content
        return await self.repository.search_conversations(
            user_id=user_id,
            query=query,
            limit=limit
        )

    async def get_conversation_detail(
        self,
        user_id: UUID,
        conversation_id: UUID
    ) -> Optional[ConversationDetail]:
        """Get full conversation with all turns"""

        # Verify ownership
        conversation = await self.repository.get_conversation(conversation_id)
        if not conversation or conversation.user_id != user_id:
            return None

        turns = await self.turn_repository.get_turns(conversation_id)

        return ConversationDetail(
            conversation=conversation,
            turns=turns
        )

    async def mark_private(
        self,
        user_id: UUID,
        conversation_id: UUID
    ) -> bool:
        """Mark conversation as private (excluded from memory/learning)"""

        return await self.repository.set_private(
            user_id=user_id,
            conversation_id=conversation_id,
            is_private=True
        )
```

### Greeting Context Generation

**Purpose**: Power context-aware greetings per PDR-001/002

```python
# services/memory/greeting_context.py

class GreetingCondition(Enum):
    """Conditions from PDR-002 greeting table"""
    SAME_DAY_RECENT = "same_day_recent"      # Back within hours
    NEXT_DAY_ACTIVE = "next_day_active"      # Next day, was working on something
    WEEK_GAP = "week_gap"                    # 1+ week since last session
    MONTH_GAP = "month_gap"                  # 1+ month gap
    PREVIOUS_TRIVIAL = "previous_trivial"   # Last session was brief/unimportant
    PREVIOUS_NEGATIVE = "previous_negative" # Last session ended badly
    FIRST_SESSION = "first_session"         # Brand new user


@dataclass
class GreetingContext:
    """Context for generating appropriate greeting"""
    condition: GreetingCondition
    last_session: Optional[ConversationalMemoryEntry]
    time_since_last: Optional[timedelta]
    suggested_greeting_approach: str
    can_reference_work: bool
    offer_fresh_start: bool

    # For templating
    topic_reference: Optional[str] = None
    entity_references: List[str] = field(default_factory=list)


class GreetingContextService:
    """Generates greeting context based on user history"""

    async def get_greeting_context(self, user_id: UUID) -> GreetingContext:
        """Determine appropriate greeting context for user"""

        memory_window = await self.memory_service.get_memory_window(user_id)
        last_entry = memory_window.get_most_recent()

        # Determine condition
        condition = self._determine_condition(last_entry)

        # Build context
        return GreetingContext(
            condition=condition,
            last_session=last_entry,
            time_since_last=self._time_since(last_entry),
            suggested_greeting_approach=self._get_approach(condition),
            can_reference_work=condition in [
                GreetingCondition.SAME_DAY_RECENT,
                GreetingCondition.NEXT_DAY_ACTIVE
            ],
            offer_fresh_start=condition in [
                GreetingCondition.WEEK_GAP,
                GreetingCondition.MONTH_GAP,
                GreetingCondition.PREVIOUS_NEGATIVE
            ],
            topic_reference=last_entry.topic_summary if last_entry else None,
            entity_references=last_entry.entities_mentioned if last_entry else []
        )

    def _determine_condition(
        self,
        last_entry: Optional[ConversationalMemoryEntry]
    ) -> GreetingCondition:
        """Determine greeting condition from last session"""

        if not last_entry:
            return GreetingCondition.FIRST_SESSION

        hours_since = (datetime.utcnow() - last_entry.timestamp).total_seconds() / 3600

        # Check for negative sentiment (bad session)
        if last_entry.user_sentiment == "negative":
            return GreetingCondition.PREVIOUS_NEGATIVE

        # Time-based conditions
        if hours_since < 8:
            return GreetingCondition.SAME_DAY_RECENT
        elif hours_since < 36:  # Within "next day"
            return GreetingCondition.NEXT_DAY_ACTIVE
        elif hours_since < 168:  # Within a week
            return GreetingCondition.WEEK_GAP
        else:
            return GreetingCondition.MONTH_GAP

    def _get_approach(self, condition: GreetingCondition) -> str:
        """Get suggested greeting approach per PDR-002"""

        approaches = {
            GreetingCondition.SAME_DAY_RECENT:
                "Reference specific work: 'Back already! We were working on [X]—continue?'",
            GreetingCondition.NEXT_DAY_ACTIVE:
                "Light reference: 'Yesterday we discussed [X]. Continue, or different focus?'",
            GreetingCondition.WEEK_GAP:
                "Offer choice: 'It's been a bit! Want to pick up where we left off, or start fresh?'",
            GreetingCondition.MONTH_GAP:
                "Gentle reorientation: 'Welcome back! Want me to catch you up, or start fresh?'",
            GreetingCondition.PREVIOUS_TRIVIAL:
                "No reference: 'What can I help with?'",
            GreetingCondition.PREVIOUS_NEGATIVE:
                "Clean slate: 'What would you like to work on?' (no reference to prior context)",
            GreetingCondition.FIRST_SESSION:
                "Welcome: Per FTUX flow (PDR-001)"
        }
        return approaches.get(condition, "What can I help with?")
```

### Memory Retrieval Service (Unified Interface)

```python
# services/memory/memory_retrieval_service.py

class MemoryRetrievalService:
    """Unified interface for memory retrieval across layers"""

    def __init__(
        self,
        conversational_memory: ConversationalMemoryService,
        user_history: UserHistoryService,
        greeting_context: GreetingContextService
    ):
        self.conversational_memory = conversational_memory
        self.user_history = user_history
        self.greeting_context = greeting_context

    async def get_context_for_request(
        self,
        user_id: UUID,
        conversation_id: Optional[UUID] = None
    ) -> RequestMemoryContext:
        """Get all relevant memory context for processing a request"""

        # Layer 1: Recent conversational memory
        memory_window = await self.conversational_memory.get_memory_window(user_id)

        # Current conversation context (if continuing)
        current_conversation = None
        if conversation_id:
            current_conversation = await self.user_history.get_conversation_detail(
                user_id, conversation_id
            )

        return RequestMemoryContext(
            memory_window=memory_window,
            current_conversation=current_conversation,
            active_topics=memory_window.get_active_topics(),
            active_entities=memory_window.get_active_entities()
        )

    async def get_greeting_context(self, user_id: UUID) -> GreetingContext:
        """Get context for generating session greeting"""
        return await self.greeting_context.get_greeting_context(user_id)

    async def search_user_history(
        self,
        user_id: UUID,
        query: str,
        limit: int = 10
    ) -> List[ConversationSummary]:
        """Search user's conversation history"""
        return await self.user_history.search_history(user_id, query, limit)
```

### Database Schema

```python
# New table for conversational memory entries
class ConversationalMemoryEntryDB(Base):
    __tablename__ = "conversational_memory_entries"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), index=True)
    conversation_id = Column(UUID(as_uuid=True), ForeignKey("conversations.id"))

    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    topic_summary = Column(String(500))
    entities_mentioned = Column(JSON, default=list)
    outcome = Column(String(500), nullable=True)
    user_sentiment = Column(String(20), nullable=True)  # positive/neutral/negative

    created_at = Column(DateTime, default=datetime.utcnow)

# Add to existing conversations table
class ConversationDB(Base):
    # ... existing fields ...

    # New fields for history features
    title = Column(String(200), nullable=True)  # Auto-generated or user-set
    is_private = Column(Boolean, default=False, index=True)  # Privacy mode
    topics = Column(JSON, default=list)  # Extracted topics for search

    # Full-text search index on conversation content
    # (Implemented via PostgreSQL tsvector)
```

### Privacy Mode Integration

```python
class PrivacyModeService:
    """Handles privacy mode interactions with memory"""

    async def start_private_session(self, user_id: UUID) -> UUID:
        """Start a session that won't be remembered"""

        conversation = await self.conversation_repo.create(
            user_id=user_id,
            is_private=True
        )

        return conversation.id

    async def exclude_from_memory(
        self,
        user_id: UUID,
        conversation_id: UUID
    ) -> bool:
        """Retroactively mark conversation as private"""

        # Mark conversation
        await self.conversation_repo.set_private(conversation_id, True)

        # Remove any memory entries
        await self.memory_repo.delete_entries_for_conversation(conversation_id)

        # Note: Does NOT affect composted learning (that's already extracted)
        # This is a design decision - we could add "forget learning" later

        return True
```

---

## Alternatives Considered

### Alternative A: No Memory Window (Session-Only)
Each session starts fresh with no reference to previous sessions.

**Rejected because**: PDR-002 explicitly rejects session isolation. "Destroys the colleague relationship."

### Alternative B: Infinite Memory (Remember Everything)
Store and reference all historical context indefinitely.

**Rejected because**: PDR-002 rejects as "creepy." Selective memory is more human.

### Alternative C: User-Controlled Retention Period
Let users configure their retention period (1 day, 1 week, forever).

**Deferred**: Could be added later. Current design uses 24-hour window as sensible default per CXO guidance. User History (Layer 2) is indefinite but user-controlled via delete.

### Alternative D: In-Memory Only (Redis/Cache)
Use Redis TTL for 24-hour window, no database persistence.

**Rejected because**: Memory loss on restart is poor UX. Conversational memory should survive system maintenance.

---

## Consequences

### Positive

- **Natural continuity**: Users experience Piper remembering recent context appropriately
- **User control**: History is searchable and deletable by user
- **Privacy support**: Private sessions excluded from memory
- **Greeting intelligence**: Context-aware greetings feel colleague-like
- **Explicit references**: Transparent when Piper uses memory

### Negative

- **Storage growth**: Conversation summaries accumulate (mitigated by pruning Layer 1)
- **Summary quality**: Auto-generated summaries may miss nuance
- **Sentiment detection**: Determining "negative" sessions is imprecise
- **Search performance**: Full-text search on conversations requires indexing

### Neutral

- **Complexity**: Three-layer model is conceptually clear but implementation touches multiple services
- **Testing**: Requires time-based test fixtures

---

## Integration Points

### 1. Session Start (Greeting Generation)
```python
# In greeting/home route
greeting_context = await memory_service.get_greeting_context(user_id)
greeting = await piper_voice.generate_greeting(greeting_context)
```

### 2. Session End (Memory Recording)
```python
# When conversation ends or times out
summary = await summarization_service.summarize_conversation(conversation_id)
await memory_service.record_conversation_end(
    user_id=user_id,
    conversation_id=conversation_id,
    summary=summary.topic,
    entities=summary.entities,
    outcome=summary.outcome,
    sentiment=summary.user_sentiment
)
```

### 3. Request Processing (Context Enrichment)
```python
# In intent processing
memory_context = await memory_service.get_context_for_request(ctx.user_id, ctx.conversation_id)
# Use memory_context.active_entities for reference resolution
```

### 4. UI (History Display)
```python
# API endpoint for conversation history
@router.get("/conversations/history")
async def get_history(page: int = 1, current_user: JWTClaims = Depends(get_current_user)):
    return await history_service.get_history(current_user.user_id, page=page)
```

---

## Relationship to Other ADRs

- **ADR-053 (Trust Computation)**: Trust affects greeting approach and proactivity in greetings
- **ADR-051 (Unified User Session Context)**: Memory services receive `RequestContext`
- **Composting/Learning ADRs (future)**: Layer 3 feeds from Layers 1 and 2 but is architecturally separate

---

## Forward-State Note — Anthropic Dreams API substratability (added 2026-05-27)

*Added by CIO during methodology-34 refresh window (per Architect Dreams API spec-read findings 2026-05-27). Does not change ADR-054's Layer 1/2 decisions; records a forward decision point for Layer 3.*

**When Layer 3 (Composted Learning) automated consolidation lands**, Anthropic's Dreams API (formal beta as of May 6, 2026) becomes a substrate option for the Type 1 memory-consolidation mechanism. The decision at that time is **sovereignty-vs-engineering-cost**, not pre-committed in either direction:

- **What Dreams API offers for Layer 3 Type 1**: async job model (`pending → running → completed`); input memory store never modified; separate output store; the four Pattern-070 invariants confirmed externally (transaction-boundary isolation, cancellation hygiene, lifespan wiring, failure-isolation envelope).
- **Sovereignty cost**: adopting Dreams API requires migrating substantive memory + session state into Anthropic-managed stores. Our current Layer 3 substrate (composted-learning per the Learning System architecture) is cohort-controlled filesystem + git surfaces. Migration relinquishes that sovereignty for a commodity-mechanism gain.
- **The split that matters** (per methodology-34 migrate-vs-stays taxonomy): Type 1 (memory consolidation) is substratable when timing forces it; Type 2 (anxiety-dreams / threat-simulation per methodology-27) stays PM-side definitively — sovereignty AND novelty.

**This note pre-commits nothing.** It makes the decision-point visible so that when Layer 3 automated consolidation is designed, the Dreams-API-vs-DIY evaluation is explicit rather than rediscovered. Reference: `mailboxes/cio/read/memo-arch-to-cio-cc-pa-lead-host-cxo-ceo-exec-anthropic-dreams-api-spec-read-findings-2026-05-27.md` + methodology-34 "Worked examples — the migrate-vs-stays taxonomy" section.

---

## Open Questions

1. **Conversation summarization**: How do we generate `topic_summary` automatically? LLM-based summarization at session end? Or rule-based extraction?

2. **Sentiment detection**: How do we detect negative sessions? Explicit signals (user said "this isn't working")? Implicit (abandoned mid-task)? LLM classification?

3. **Entity extraction**: What counts as a "mentioned entity" worth remembering? Integration with existing anaphoric reference system?

4. **Privacy mode UX**: How does user invoke private mode? Chat command? Toggle in UI? Both?

5. **Multi-device**: PDR-002 asks about multi-device continuity. Current design: memory is per-user, so devices share memory. Is additional device-awareness needed?

---

## Implementation Plan

**Phase 1: Core Memory Infrastructure**
- [ ] Create `ConversationalMemoryEntryDB` table and migration
- [ ] Implement `ConversationalMemoryService` with record/retrieve
- [ ] Implement 24-hour window pruning
- [ ] Unit tests for memory operations

**Phase 2: Greeting Context**
- [ ] Implement `GreetingContextService` with condition detection
- [ ] Create `GreetingContext` model with all PDR-002 conditions
- [ ] Integration tests for greeting scenarios

**Phase 3: User History Enhancements**
- [ ] Add `title`, `is_private`, `topics` fields to conversations
- [ ] Implement full-text search
- [ ] Implement history pagination API
- [ ] UI for conversation history (sidebar enhancement)

**Phase 4: Integration**
- [ ] Session end hook for memory recording
- [ ] Greeting generation integration
- [ ] Privacy mode implementation
- [ ] E2E tests for cross-session continuity

---

## References

- PDR-002: Conversational Glue - Three-layer model definition
- PDR-001: First Contact is First Recognition - Greeting patterns
- CXO UX Summary Report (Jan 3, 2026) - Context persistence decisions
- Issue #563: Conversation History & Persistence (foundation work)
- Issue #583: Chat persistence regression (recent fix)

---

*ADR-054 | PROPOSED | January 13, 2026*
