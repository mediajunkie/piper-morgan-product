# ADR-050: Conversation-as-Graph Model

**Status**: Accepted
**Date**: January 21, 2026 (Accepted)
**Original Date**: January 13, 2026
**Author**: Chief Architect
**Input**: Ted Nadeau, "MultiChat – Multi-Party, Multi-Agent Conversational Modeling Platform" PRD v1.0
**Related**: PDR-101 (Multi-Entity Conversation Support), ADR-046 (Moment.type Agent Architecture), ADR-054 (Cross-Session Memory)

## Context

Piper Morgan currently models conversations as linear sequences of `ConversationTurn` records—each turn storing a user message and assistant response in chronological order. This mirrors traditional chatbot design but fails to capture the structural complexity of real collaborative work.

Ted Nadeau's MultiChat PRD (January 2026) proposes treating conversation as a **graph model** rather than a linear log. His working proof-of-concept demonstrates:

- **Nodes**: Typed conversation elements (messages, tasks, whispers)
- **Links**: Explicit relationships between elements (reply, reference, blocking, annotates, resolves)
- **Multiple Views**: Same underlying data projected as timeline, threads, tasks, agreements

This architectural pattern addresses fundamental limitations:

1. **Lost Relationships**: When users say "getting back to what you mentioned earlier..." we have no explicit link—only implicit context
2. **Flat Structure**: Thread replies, decision points, and extracted tasks all live in the same linear sequence
3. **Single View**: Users can only navigate chronologically, not by topic, task, or decision
4. **1:1 Only**: Current model assumes one user per conversation—no multi-party support

Ted's insight: "Real conversations have complex non-linear relationships... the same underlying model supports multiple views (tasks, questions, agreements, domain-specific projections)."

## Decision

Adopt Ted's graph-based conversation model as the foundation for Piper's multi-entity conversation capability, implemented incrementally per PDR-101 phases.

### Core Data Model

Extend current domain models with graph primitives:

```python
# services/domain/models.py additions

class ConversationNodeType(str, Enum):
    MESSAGE = "message"
    TASK = "task"
    WHISPER = "whisper"
    DECISION = "decision"
    QUESTION = "question"

class ConversationLinkType(str, Enum):
    """
    Base link types. Per Ted's clarification (Jan 13, 2026):
    - Link types are EXTENSIBLE, not a fixed set
    - RELATES_TO is the default/generic type
    - Elements can have MULTIPLE links to the same target
    - Link types themselves have meta-relationships
    - Conversation sponsors can define domain-specific types
    """
    RELATES_TO = "relates_to"   # Default/generic relationship
    REPLY = "reply"             # Direct response
    REFERENCE = "reference"     # Non-sequential citation
    BLOCKING = "blocking"       # Dependency relationship
    VARIANT_OF = "variant_of"   # Alternative version
    ANNOTATES = "annotates"     # Commentary on content
    RESOLVES = "resolves"       # Closes/answers something
    # Extensible: conversation sponsors may define additional types

@dataclass
class ConversationNode:
    """Graph node representing a typed conversation element."""
    id: str
    type: ConversationNodeType
    content: str
    author_id: str
    timestamp: datetime
    parent_id: Optional[str] = None  # For simple threading
    data: Optional[Dict[str, Any]] = None  # Type-specific payload

@dataclass
class ConversationLink:
    """
    Explicit relationship between conversation elements.

    Design notes (per Ted, Jan 13, 2026):
    - One source can have multiple links to same target (different types)
    - Single link can carry multiple type annotations (multi-type)
    - Links relate to "reaction-deck" and "gesture-palette" concepts
    """
    id: str
    source_id: str
    target_id: str
    type: ConversationLinkType
    additional_types: Optional[List[str]] = None  # For multi-type links
    created_at: datetime = None
    created_by: str = None

@dataclass
class ConversationGraph:
    """Graph-structured conversation with typed elements and relationships."""
    id: str
    nodes: List[ConversationNode]
    links: List[ConversationLink]
    participants: List[str]  # User IDs
    owner_id: str
    created_at: datetime
    updated_at: datetime
```

### Migration Path

**Phase 0** (Current): No changes—methodology continues as prototype

**Phase 1** (Participant Mode):
- Add `parent_id` to `ConversationTurn` for threading
- Introduce `ConversationLink` table for explicit relationships
- Enhance Slack integration to track thread structure

**Phase 2** (Host Mode Foundation):
- Implement full `ConversationNode` model
- Add multiple view projections (timeline, thread, tasks)
- Support multi-participant conversations

**Phase 3** (Personal Agents):
- Add `WhisperNode` for private AI suggestions
- Per-participant context and preferences

### Facilitator Architecture

Per Ted's clarification (Jan 13, 2026), facilitators use an **AI layering model**:

```
                    ┌─────────────────────┐
                    │  Orchestrator       │
                    │  Facilitator        │
                    └─────────┬───────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
        ▼                     ▼                     ▼
┌───────────────┐   ┌───────────────┐   ┌───────────────┐
│ GitHub Agent  │   │ Calendar Agent│   │ Wiki Agent    │
│ (tasks/epics) │   │ (scheduling)  │   │ (artifacts)   │
└───────────────┘   └───────────────┘   └───────────────┘
```

**Key tuning parameters**:
- **Verbosity**: How often does the orchestrator speak? (Scale: every message ↔ only on gaps/problems)
- **Stance**: Reacting vs. leading
- **Alignment**: "Colleague" pattern from Piper design principles

**Human analogs** for facilitator patterns:
- Marriage counselor, meeting note-taker, wedding planner, mediator
- PM bridging business sponsors and technical implementers

### Whisper Agent Visibility

Per Ted's clarification: Whisper agents have **full conversation visibility by default** (same view as user). Complexity arises at "prior insertion points" (e.g., user reviewing earlier content—"no spoilers" mode). Input tokens are cheap; "see all" is default unless problematic.

### View Projections

The graph model enables multiple view projections over the same data:

| View | Query Pattern | Use Case |
|------|---------------|----------|
| Timeline | Nodes ordered by timestamp | Default chat experience |
| Thread | Nodes grouped by parent_id | Discussion navigation |
| Tasks | Nodes where type = 'task' | Kanban/action tracking |
| Decisions | Nodes where type = 'decision' | Agreement tracking |
| Questions | Nodes where type = 'question' | Q&A extraction |

### Relationship to Existing Architecture

**ADR-046 (Moment.type)**: Moment.types map to ConversationNodeTypes. The decomposition pipeline produces typed nodes that populate the graph.

**ADR-045 (Object Model)**: "Entities experience Moments in Places" — a ConversationGraph is a Place where multiple Entities collaborate through typed Moments (Nodes).

**ADR-054 (Cross-Session Memory)**: The graph model defines conversation *structure*; cross-session memory (ADR-054) handles *persistence* across sessions. A `ConversationGraph` may span multiple sessions; memory retrieval queries the graph.

**ConversationSession/Turn**: Existing models become a simplified view over the graph—ConversationTurn is a shorthand for a message Node and its assistant response Node linked by 'reply'.

## Consequences

### Benefits

1. **Rich Relationship Tracking**: Explicit links capture conversation structure
2. **Multiple Views**: Users navigate by time, topic, task, or decision
3. **Multi-Party Ready**: Graph naturally supports multiple participants
4. **Artifact Extraction**: Tasks, decisions, questions emerge from typed nodes
5. **Facilitator AI**: System can analyze graph structure, identify gaps, suggest actions

### Risks

1. **Migration Complexity**: Existing conversations need graph representation
2. **Query Performance**: Graph traversal more complex than linear scan
3. **UI Complexity**: Multiple views require more sophisticated frontend

### Mitigations

1. **Incremental Adoption**: Linear view remains default; graph features opt-in
2. **Materialized Views**: Pre-compute common projections (timeline, tasks)
3. **Reference Implementation**: Ted's POC provides proven UI patterns

## Implementation Notes

Ted's MultiChat POC (`external/ted-multichat/poc/`) provides:
- TypeScript interfaces for the data model
- React components for all view types
- Use case scenarios with validation scripts

Extract patterns into Piper's Python/FastAPI stack rather than merging Next.js code.

## References

- Ted Nadeau, "MultiChat PRD v1.0" (`external/ted-multichat/multichat_prd_v1.md`)
- Ted Nadeau, "MultiChat UI/UX Spec v1.0" (`external/ted-multichat/multichat_uiux_v1.md`)
- PDR-101: Multi-Entity Conversation Support
- ADR-046: Moment.type Agent Architecture
- ADR-045: Object Model

---

*ADR-050 | Proposed | January 13, 2026*
