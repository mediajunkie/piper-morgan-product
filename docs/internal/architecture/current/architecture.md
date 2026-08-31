# Architecture Overview

> 🛑 **HISTORICAL — SUPERSEDED BY `docs/internal/architecture/SYSTEM.md` (2026-08-31, Architectural
> Review 2026 workstream B2).** This document accreted three generations of contradictory claims
> (the clean-room audit found it documenting a deleted QueryRouter as "✅ Complete" under its own
> deletion banner, with a revision log that could not be trusted). It is retained as history —
> do not plan from it. **Current system truth: SYSTEM.md. Current law: ESSENCE.md.**

> ⚠️ **STALE ARCHITECTURE WARNING (Apr 11, 2026)**
> This document describes the September 2025 architecture and predates the M1 floor inversion (#911), the Apr 8 IDENTITY full migration to floor, and several other M1-era architectural decisions. The diagrams below show "Intent Classifier → Workflow Factory" as the application core; the current reality is "Classifier → Action Gate → (Floor with Context | Canonical Handler | Workflow Dispatcher)" per [ADR-059](../adrs/adr-059-workflow-dispatcher-offer-consolidation.md) and [ADR-060](../adrs/adr-060-floor-first-routing.md).
>
> **Full rewrite pending in M2a doc cleanup.** Use this document for high-level DDD context only; refer to the ADRs above for current routing reality.

---

## System Architecture Status

**Last Updated**: 2026-04-11 (post-M1)
**Status**: M1 complete. Floor-first routing live in production.

### Changelog

- **2026-04-11**: Rewrote application-layer section to reflect M1 floor-first
  routing (#911, ADR-060), Apr 8 IDENTITY migration (commit 33e6758a), and
  provider-agnostic LLM (#940). Sections below the application layer
  (domain services, data, infra, MUX, Slack spatial) are retained from the
  Sep 12, 2025 baseline and still broadly accurate. Slack "641x improvement"
  numbers and fixed port text unchanged.
- **2025-09-12**: Original DDD-compliance milestone doc.

---

## Application Layer (Post-M1)

The application layer is now a **routing graph** rather than a simple
"classifier -> workflow factory" pair. The graph terminates at one of three
destinations: the conversational floor, a canonical handler, or the workflow
dispatcher.

```
User Message
  |
  v
Pre-classifier (fast pattern match)
  |                                  miss
  +-----> LLM Classifier (task_type="intent_classification")
  |                                  |
  v                                  v
Intent (category, action, confidence, context)
  |
  v
Action Gate
  |--- _requires_canonical_handler(intent) ----> Canonical Handler
  |      (PORTFOLIO, EXECUTION, TEMPORAL, STATUS,
  |       PRIORITY, CONVERSATION+greeting,
  |       GUIDANCE+setup-topic)
  |
  |--- _should_route_to_floor(intent) ---------> Conversational Floor
  |      (GUIDANCE, IDENTITY, DISCOVERY,              with assembled context
  |       TRUST, MEMORY, CONVERSATION,                (ContextAssembler)
  |       UNKNOWN)                                    + 6-turn history
  |                                                   + domain_context block
  |
  +--- otherwise ------------------------------> Workflow Dispatcher
         (ANALYSIS, SYNTHESIS, STRATEGY,              (ADR-059)
          PLANNING, REVIEW, LEARNING, QUERY)
```

**Source of truth**:
- `services/intent/intent_service.py` lines 9863-9962
  (`_requires_canonical_handler`, `_should_route_to_floor`,
  `_handle_floor_with_context`)
- `services/intent_service/canonical_handlers.py` line 129
  (`CanonicalHandler.can_handle`)
- `services/intent_service/conversational_floor.py`
  (floor impl, system prompt, fabrication guardrails)

### What Changed from the Sep 2025 Architecture

1. **Floor-first by default** (#911, ADR-060). The previous "workflow factory
   is the application core" framing no longer holds. Most conversational
   query categories (IDENTITY, DISCOVERY, TRUST, MEMORY, UNKNOWN, and most
   GUIDANCE) run through the floor — an LLM call with category-specific
   context — rather than through canned canonical templates or full workflow
   orchestration.
2. **IDENTITY full migration** (Apr 8, commit 33e6758a). All IDENTITY queries
   now route to the floor. The previous "core IDENTITY canonical, adjacent
   IDENTITY floor" split was removed when UAT Round 2 showed the canned
   template scored 1/3 on the Colleague Test.
3. **Canonical handlers retained for mutations + fast paths.** EXECUTION,
   PORTFOLIO, TEMPORAL (sub-ms time queries), STATUS, PRIORITY, and
   greeting/setup handlers still run canonical. These are operations the LLM
   cannot perform by itself, or deterministic fast paths where the LLM would
   add only latency.
4. **Conversation continuity** (#922, commit 25437f95). `ConversationTurn` in
   `services/intent_service/conversation_context.py` gained a `response`
   field so the floor sees both the user's message and Piper's prior reply
   when assembling history.
5. **Floor fabrication guardrails** (#960, commit 4789de64). The floor system
   prompt in `conversational_floor.py` now explicitly prohibits inventing
   user data (todos, projects, calendar entries) when the context block is
   empty. See [intent-categories-reference.md](intent-categories-reference.md).
6. **Provider-agnostic LLM** (#940). The hardcoded task-type-to-provider map
   is gone. Models resolve at runtime via `model_tier`. See
   [llm-configuration.md](llm-configuration.md).

### Destination Details

**Conversational Floor**
(`services/intent_service/conversational_floor.py`)
- Builds a FloorContext: user message, 6-turn history (user + assistant),
  trust stage, formality baseline, intent metadata, and a `domain_context`
  dict assembled per-category
- Calls `LLMClient.complete(task_type="conversation", ...)`
- On error, selects between three fallbacks via `_classify_llm_error`:
  auth/config, no-provider, or transient
- Categories routed here: see
  [intent-categories-reference.md](intent-categories-reference.md)

**Canonical Handlers** (`services/intent_service/canonical_handlers.py`)
- Deterministic, side-effect-bearing, or DB-mutating operations
- Current set: TEMPORAL, STATUS, PRIORITY, GUIDANCE (setup only),
  PORTFOLIO, CONVERSATION (greeting only)
- IDENTITY/DISCOVERY/TRUST/MEMORY were removed from this set in Issue #963
  post-M1 cleanup

**Workflow Dispatcher** (ADR-059, `services/workflows/`)
- Legacy orchestration path for action-oriented categories the floor is
  not appropriate for: ANALYSIS, SYNTHESIS, STRATEGY, PLANNING, REVIEW,
  LEARNING, QUERY
- Uses ValidationRegistry and pre-execution validation as before

---

## Legacy System Diagram (Sep 12, 2025 — retained for historical context)

The diagram below is the pre-M1 application-layer view. The domain-services,
data, and infrastructure layers it shows are still accurate; the application
layer is superseded by the routing graph above.

````

┌─────────────────────────────────────────────────────────────────────────────┐
│                           USER INTERFACE LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ FastAPI Web Server     │  ✅ Web UI (DDD, TDD, resizable chat window) │  📋 Admin Interface    │
│  (Built & Running)         │  (Built & Working)    │  (Not Yet Designed)   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          APPLICATION LAYER (SUPERSEDED — see above)        │
├─────────────────────────────────────────────────────────────────────────────┤
│  ⚠️ Intent Classifier       │  ⚠️ Workflow Factory    │  📋 Learning Engine   │
│  (Now one of 3 terminals)  │  (Now Workflow         │  (Not Yet Designed)   │
│                             │   Dispatcher, ADR-059) │                       │
│  ⚠️ Query Service           │  ⚠️ Orchestration       │  📋 Analytics Engine  │
│  (Part of floor context)    │  Engine                 │  (Not Yet Designed)   │
│                             │  (Pre-exec Validation)  │                      │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                          DOMAIN SERVICES LAYER                             │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ GitHubDomainService     │  ✅ SlackDomainService      │  ✅ NotionDomainService │
│  (Router Architecture)      │  (Mediation Complete)      │  (Mediation Complete)  │
│  • Router-based operations  │  • Webhook handling         │  • Workspace mgmt      │
│  • Spatial intelligence     │  • Spatial events           │  • Database ops        │
│  • Feature flag control     │  • Health monitoring        │  • Page operations     │
│                             │                             │                        │
│  ✅ StandupOrchestrationService  │  ✅ PortConfigurationService │  📋 Future Domain Services │
│  (Workflow Coordination)    │  (Centralized Config)      │  (As Needed)          │
│  • Domain workflow mgmt     │  • Environment-aware       │                       │
│  • Integration orchestration│  • URL generation           │                       │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                            SERVICE LAYER                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Domain Models           │  ✅ Workflow Service    │  📋 Feedback Service  │
│  (Built)                    │  (Built & Working)      │  (Not Yet Designed)   │
│                             │                         │                       │
│  ✅ Event System            │  ✅ GitHub Integration  │  ✅ Slack Integration  │
│  (Built)                    │  (Fully Integrated)     │  (Spatial Metaphors)  │
│                             │  (Issue Creation Working)│  (OAuth + Workflows)  │
│  ✅ Knowledge Base          │  ✅ Document Processor  │  📋 Report Generator  │
│  (Built & Working)          │  (Built & Working)      │  (Not Yet Designed)   │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                         RESPONSE ENHANCEMENT LAYER                         │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ ResponsePersonalityEnhancer│  ✅ PersonalityProfile    │  ✅ TransformationService │
│  (Production Ready)           │  (Database + YAML)       │  (Warmth + Confidence)    │
│  • <70ms performance          │  • User preferences       │  • Action guidance        │
│  • Circuit breaker           │  • LRU caching            │  • Context adaptation     │
│  • Graceful degradation      │  • Config overrides       │  • Performance optimized  │
└─────────────────────────────────────────────────────────────────────────────┘
                                       │
                                       ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                            UI MESSAGE LAYER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ActionHumanizer                                                            │
│  • Cache-first lookup                                                       │
│  • Rule-based conversion                                                    │
│  • Usage tracking                                                           │
│  (TemplateRenderer + template dicts removed 2026-08-29 per #1638 — never    │
│   wired to a production code path; recoverable from git history)            │
└─────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        │
                                        ▼
                              User-Facing Messages

┌─────────────────────────────────────────────────────────────────────────────┐
│                           DATA LAYER                                       │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ PostgreSQL              │  ✅ ChromaDB            │  ✅ Redis              │
│  (Domain-First Schema)      │  (Deployed & Working)   │  (Deployed & Working)  │
│                             │                         │                       │
│  ✅ Domain Persistence      │  ✅ Vector Storage      │  ✅ Event Queue        │
│  (Working)                  │  (Working)              │  (Working)             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                        INFRASTRUCTURE LAYER                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Docker Compose          │  ✅ Traefik Gateway     │  ✅ Temporal           │
│  (Deployed & Running)       │  (Deployed & Running)   │  (Deployed & Running)  │
│                             │                         │                       │
│  ✅ Service Discovery       │  ✅ Load Balancing      │  ✅ Workflow Engine    │
│  (Working)                  │  (Working)              │  (Working)             │
└─────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────┐
│                       EXTERNAL INTEGRATIONS                                │
├─────────────────────────────────────────────────────────────────────────────┤
│  ✅ Claude API              │  ✅ GitHub API          │  📋 Slack/Teams       │
│  (Connected & Working)      │  (Fully Integrated)    │  (Not Yet Designed)   │
│                             │  (Issue Creation Working)│                     │
│  ✅ OpenAI API              │  📋 Jira API            │  📋 Analytics APIs    │
│  (Connected & Working)      │  (Not Yet Designed)     │  (Planned Q3 2025)    │
│                             │                         │  - Datadog            │
│                             │                         │  - New Relic          │
│                             │                         │  - Google Analytics   │
└─────────────────────────────────────────────────────────────────────────────┘

## Infrastructure Constants

### Development Environment
- **Port**: 8001 (all local development, NOT 8080)
- **Web Pattern**: Single app.py (~750 lines as of Sept 2025)
- **Database**: PostgreSQL with AsyncSessionFactory pattern
- **Config**: PIPER.user.md in config/ directory
- **Python**: 3.11+ required

### API Patterns
- **REST Response Structure**:
  ```json
  {
    "status": "success",
    "data": {
      "field_name": "value",
      "nested_fields": {...}
    }
  }
````

- **Error Format**:
  ```json
  {
    "status": "error",
    "error": "message",
    "details": {}
  }
  ```
- **Auth**: OAuth2 with token.json for Google services
- **Headers**: Content-Type: application/json

### File Structure Reality

```
piper-morgan/
├── cli/
│   └── commands/        # Standalone CLI scripts
├── web/
│   └── app.py          # Single file (NO routes/ directory)
├── services/           # Domain-driven design
│   ├── features/       # Feature services
│   ├── infrastructure/ # Infrastructure services
│   └── shared_types.py # Shared type definitions
├── config/
│   └── PIPER.user.md   # User configuration
└── docs/
    ├── architecture/   # Technical documentation
    └── planning/       # Roadmaps, backlogs
```

### Refactoring Triggers

- **app.py > 1000 lines** → Consider routes/ pattern migration
- **Service > 500 lines** → Consider domain splitting
- **Test file > 1000 lines** → Consider test grouping
- **Performance < 200ms** → Consider optimization

## Database Layer

### Current Pattern: AsyncSessionFactory

The database layer uses PostgreSQL with SQLAlchemy 2.0+ async patterns.

```python
# Current pattern in ALL services
from services.infrastructure.database import AsyncSessionFactory

async def get_data():
    async with AsyncSessionFactory() as session:
        result = await session.execute(query)
        return result.scalars().all()
```

### Migration History

- **July 2025**: DatabasePool pattern (DEPRECATED)
- **August 2025**: Migrated to AsyncSessionFactory
- **Current**: All services use AsyncSessionFactory

### Connection Management

- Connection pooling via SQLAlchemy engine
- Async context managers for session lifecycle
- Automatic rollback on exceptions
- Connection limits: 20 concurrent

### Common Patterns

```python
# Query pattern
async with AsyncSessionFactory() as session:
    stmt = select(Model).where(Model.field == value)
    result = await session.execute(stmt)

# Insert pattern
async with AsyncSessionFactory() as session:
    session.add(new_object)
    await session.commit()
```

## Web Layer

### Current Pattern: Single app.py

The web layer uses a single FastAPI file (MVP pattern) with embedded HTML.

**File**: `web/app.py` (~750 lines as of Sept 2025)

### Architecture Decisions

- **Single File**: Intentional simplicity for rapid iteration
- **Embedded HTML**: JavaScript in Python strings (no templates yet)
- **No routes/ directory**: Will refactor at 1000 lines
- **FastAPI**: Modern async framework with future flexibility

### Endpoint Patterns

```python
# API endpoint returning JSON
@app.get("/api/standup")
async def morning_standup_api():
    return {
        "status": "success",
        "data": {
            "yesterday_accomplishments": [...],
            "today_priorities": [...],
            "blockers": []
        }
    }

# UI endpoint returning HTML
@app.get("/standup")
async def standup_ui():
    return HTMLResponse(content="""
        <!DOCTYPE html>
        <html>
        <!-- Embedded HTML with JavaScript -->
        </html>
    """)
```

### Common Issues

- **Field name mismatches**: API returns `yesterday_accomplishments`, not `accomplishments`
- **Nested data structure**: Access via `data.data.field_name` in JavaScript
- **Port confusion**: Always use 8001, not 8080

## MUX Object Model Layer (NEW - January 2026)

### Overview

The MUX (Modeled User Experience) Object Model provides consciousness and ownership tracking for Piper Morgan. This enables Piper to have identity, awareness, emotional states, and epistemological tracking of knowledge sources.

**Location**: `services/mux/`
**Tests**: 165+ tests covering consciousness (104) and ownership (61)
**Patterns**: 055-058 (documented in pattern catalog)

### Architecture Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    MUX Object Model Layer                        │
├─────────────────────────────────────────────────────────────────┤
│  Consciousness Module    │  Ownership Module       │  Grammar    │
│  (services/mux/         │  (services/mux/         │  Foundation │
│   consciousness.py)     │   ownership.py)         │             │
│  • PiperEntity          │  • OwnershipCategory    │  "Entities  │
│  • AwarenessLevel       │  • OwnershipMetadata    │  experience │
│  • EmotionalState       │  • OwnershipResolver    │  Moments    │
│  • ConsciousnessAttrs   │  • OwnershipTransform   │  at Places" │
│  • EntityContext        │  • HasOwnership Proto   │             │
│  • ConsciousnessExpr    │                         │             │
└─────────────────────────────────────────────────────────────────┘
```

### Key Concepts

#### Grammar: "Entities experience Moments at Places"

The MUX grammar provides semantic grounding for the object model:
- **Entities**: Actors with consciousness (Piper, Users, Stakeholders, Teams)
- **Moments**: Temporal events and experiences
- **Places**: Contexts where experiences occur (Slack channels, GitHub repos, etc.)

#### Consciousness Attributes

Piper and other entities can have:
- **Awareness Levels**: SLEEPING → DROWSY → ALERT → FOCUSED → OVERWHELMED
- **Emotional States**: CURIOUS, CONCERNED, SATISFIED, PUZZLED
- **Agency**: wants, fears, capabilities
- **Five Orientation Queries**: who_am_i(), when_am_i(), where_am_i(), what_can_i_do(), what_should_happen()

#### Ownership Categories (Mind/Senses/Understanding)

All knowledge has an epistemological relationship:
- **NATIVE (Mind)**: What Piper creates - sessions, memories, trust states
- **FEDERATED (Senses)**: What Piper observes - GitHub, Slack, Calendar
- **SYNTHETIC (Understanding)**: What Piper infers - patterns, risks, insights

### Integration with Existing Systems

#### Intent Classification
The grammar-driven classification (Pattern-057) uses MUX concepts:
- IntentCategory mapped to grammatical verb types
- Multi-intent detection (Pattern-055) for compound messages

#### Response Generation
ConsciousnessExpression generates first-person language:
- "I notice {observation}" (CURIOUS)
- "I'm concerned about {issue}" (CONCERNED)

#### Domain Models
OwnershipMetadata can be embedded in any domain model:
```python
@dataclass
class Session:
    id: str
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata.native("piper-core")
    )
```

### References

- **ADR-055**: Object Model Specification
- **Patterns**: 055 (Multi-Intent), 056 (Consciousness), 057 (Grammar), 058 (Ownership)
- **Issues**: #433, #434, #435, #595 (X1 Sprint), #532 (Gate)

---

## MCP Integration Layer

### Overview

Model Context Protocol (MCP) integration enables tool federation and spatial intelligence.

### Architecture Pattern

```python
# MCP Consumer pattern
from services.infrastructure.mcp_consumer import MCPConsumerCore

async def fetch_github_issues():
    consumer = MCPConsumerCore()
    return await consumer.fetch_resources("github-issues")
```

### Integrated Services

- **GitHub**: Via MCP spatial adapter
- **Google Calendar**: Via MCP calendar adapter
- **Document Memory**: Via ChromaDB + MCP
- **Notion**: Via MCP notion adapter

### Spatial Intelligence

8-dimensional analysis across:

1. Temporal (when)
2. Spatial (where)
3. Conceptual (what)
4. Social (who)
5. Causal (why)
6. Procedural (how)
7. Emotional (feeling)
8. Intentional (purpose)

### Performance Metrics

- MCP consumer: <1ms response time
- Spatial analysis: <10ms for 8 dimensions
- Tool federation: 642x improvement over direct APIs

## Testing Strategy

### Multi-Agent Verification Pattern

#### Dual Agent Deployment

```python
# Always deploy both Code and Cursor for critical fixes
# Phase 0: Investigation (both agents)
# Phase 1: Implementation (agent-specific)
# Phase 2: Cross-validation (verify each other)
```

#### Evidence Requirements

- **No "done" without proof**: Terminal output, diffs, test results
- **Layer-specific validation**: API testing ≠ UI testing
- **Visual proof for UI**: Screenshots or DOM inspection required
- **GitHub checklist discipline**: All checkboxes must be verified

#### Common Validation Failures

1. **Theater validation**: Claiming success without testing
2. **Wrong layer testing**: Testing API, claiming UI works
3. **Assumption cascade**: Each step assumes previous succeeded
4. **Uncommitted changes**: Testing working directory, not deployed code

### Performance Benchmarks

- Morning standup: <6 seconds generation
- Web response: <200ms API calls
- Test execution: <5 seconds for smoke tests
- Full test suite: <2 minutes

## Legend

- **✅ Built & Working**: Implemented and operational
- **🔄 In Progress**: Designed and partially implemented
- **📋 Not Started/Designed**: Planned for future phases

## Slack Integration with Spatial Metaphors (PM-074)

### Overview

The Slack integration implements a revolutionary spatial metaphor approach, enabling Piper Morgan to understand and navigate Slack environments as physical spaces. This creates an embodied AI experience where Piper develops spatial awareness and memory.

### Spatial Metaphor Architecture

#### Core Spatial Types

- **Territories** (Workspaces): Navigable buildings/territories with corporate or startup characteristics
- **Rooms** (Channels): Specific-purpose spaces (collaboration, development, support, planning, social)
- **Conversational Paths** (Threads): Temporal corridors connecting related discussions
- **Spatial Objects** (Messages): Content placed within rooms with metadata and context
- **Attention Attractors** (@mentions): Events that pull Piper's spatial attention
- **Emotional Markers** (Reactions): Valence indicators affecting room atmosphere

#### Integration Components

```
┌─────────────────────────────────────────────────────────────────┐
│                    Slack Spatial Integration                    │
├─────────────────────────────────────────────────────────────────┤
│  OAuth Handler       │  Spatial Mapper      │  Webhook Router   │
│  • Territory Init    │  • Metaphor Engine   │  • Event Process  │
│  • State Management  │  • Spatial Objects   │  • Signature Verify│
│                      │  • Coordinate System │                   │
├─────────────────────────────────────────────────────────────────┤
│  Workspace Navigator │  Attention Model     │  Spatial Memory   │
│  • Multi-Territory   │  • Priority Algorithms│  • Pattern Learning│
│  • State Tracking    │  • Decay Models      │  • JSON Persistence│
│  • Risk Assessment   │  • Focus Management  │  • Cross-Session   │
└─────────────────────────────────────────────────────────────────┘
```

### Technical Implementation

#### OAuth 2.0 Flow with Spatial Initialization

- Automatic spatial territory creation upon successful OAuth
- Workspace metadata extraction and spatial property assignment
- State management with 15-minute expiration for security

#### Advanced Attention Model

- **Multi-factor scoring**: Proximity, urgency, relationships, emotional context
- **Decay algorithms**: Linear, exponential, stepped, and contextual decay models
- **Pattern learning**: Automatic behavior adaptation based on interaction history
- **Focus management**: Intelligent attention switching with efficiency tracking

#### Spatial Memory Persistence

- **Cross-session memory**: JSON-based storage system preserving spatial awareness
- **Pattern accumulation**: Learning from navigation and interaction patterns
- **Relationship mapping**: Tracking connections between territories, rooms, and users
- **Analytics insights**: Rich analytics from accumulated spatial intelligence

### Integration with Piper Morgan Workflows

#### Slack → Spatial → Workflow Pipeline

```
Slack Event → Spatial Mapping → Attention Processing → Navigation Decision → Workflow Creation
     ↓              ↓                    ↓                     ↓               ↓
WebHook Event → Room/Territory → Attention Event → Priority Score → Piper Workflow
```

#### Supported Workflow Types

- **Help Requests**: `@piper help with feature` → CREATE_FEATURE workflow
- **Bug Reports**: Critical incidents → CREATE_TICKET workflow with emergency priority
- **Feature Proposals**: Product planning → CREATE_FEATURE workflow with research context

### Quality Standards

- **52 TDD Integration Tests**: Comprehensive test coverage following strict TDD methodology
- **Error Handling**: Graceful fallbacks with spatial learning from failures
- **Performance**: <100ms spatial processing for real-time responsiveness
- **Security**: Slack signature verification and secure token management
- **Scalability**: Multi-workspace support with intelligent resource management

## Query vs Command Pattern

### Command Flow (State Changes) - With Context Validation

```

User Intent → Intent Classifier → EXECUTION/SYNTHESIS → Workflow Factory (ValidationRegistry) → Context Validation → Orchestration Engine → External Systems
                                                              ↓                              ↓
                                                    Pre-execution Validation           State Changes
                                                    (User-friendly errors)

```

### Query Flow (Data Retrieval) - Updated September 2025

```

User Intent → Intent Classifier → QUERY → OrchestrationEngine.handle_query_intent()
    ↓
QueryRouter.get_query_router() → Session-Aware Services → Repository → Direct Data Access
    ↓
Formatted Results → Web Response

```

**Current Implementation Details**:

- **Entry Point**: `web/app.py` routes QUERY intents to `orchestration_engine.handle_query_intent(intent)`
- **QueryRouter Integration**: On-demand initialization with session-aware wrappers
- **Service Layer**: SessionAwareProjectQueryService, ConversationQueryService, SessionAwareFileQueryService
- **Performance**: Sub-500ms response times with concurrent request handling
- **Reliability**: LLM resilient parsing ensures consistent intent classification

### Decision Criteria

- **Use Workflows for**: Multi-step processes, state changes, external system updates, complex orchestration
- **Use Queries for**: Data retrieval, listings, searches, read-only operations, simple aggregations

### Benefits

- **Performance**: Queries bypass workflow overhead
- **Clarity**: Clear separation of concerns
- **Scalability**: Can optimize read and write paths independently
- **Simplicity**: No workflow complexity for simple data fetches

## Context Validation Framework (PM-057)

### Overview

The Context Validation Framework provides pre-execution validation for all workflow types, preventing runtime failures and delivering user-friendly error messages with actionable guidance.

### Architecture Components

#### ValidationRegistry Pattern

- **Location**: `services/orchestration/workflow_factory.py`
- **Purpose**: Defines context requirements for each workflow type
- **Structure**: Critical, Important, and Optional field classifications
- **Performance**: 30-75ms thresholds per workflow type

#### WorkflowContextValidator

- **Location**: `services/orchestration/validation.py`
- **Purpose**: Validates workflow context against defined rules
- **Features**: User-friendly error messages, GitHub URL validation, field existence checking
- **Integration**: Seamless integration with OrchestrationEngine error handling

### Validation Flow

```
Workflow Creation Request
         ↓
ValidationRegistry (Context Requirements)
         ↓
WorkflowContextValidator (Rule Validation)
         ↓
[Valid Context] → Workflow Execution
         ↓
[Invalid Context] → User-Friendly Error Message
```

### Workflow Type Coverage

- **CREATE_TICKET**: Requires `original_message`, validates `project_id` and `repository`
- **LIST_PROJECTS**: Requires `original_message` only
- **ANALYZE_FILE**: Requires `original_message`, validates `file_id` and `resolved_file_id`
- **GENERATE_REPORT**: Requires `original_message`, validates `data_source`
- **REVIEW_ITEM**: Requires `original_message`, validates `github_url`
- **PLAN_STRATEGY**: Requires `original_message`, validates `scope` and `objectives`

### Quality Standards

- **100% Test Coverage**: 17 comprehensive tests covering all scenarios
- **Performance Excellence**: All validation operations complete within defined thresholds
- **User Experience**: Error messages provide specific, actionable guidance
- **Production Ready**: Immediate deployment capability with zero breaking changes

## CQRS-lite Query Pattern Implementation

### Overview

The CQRS-lite pattern separates read operations (queries) from write operations (commands) in the Piper Morgan system. This provides clear architectural boundaries, better performance for simple data fetches, and prevents forcing query-like operations into complex workflow patterns.

### Implementation

### Intent Classification

Queries are identified through intent classification:

```python

python
# Intent classifier recognizes QUERY category for read-only operations
if intent.category == IntentCategory.QUERY:
# Route to QueryRouter
    result = await query_router.route_query(intent)
else:
# Route to WorkflowFactory for commands
    workflow = await workflow_factory.create_from_intent(intent)

```

### Query Router (PM-034 Implementation Complete)

The `QueryRouter` handles QUERY category intents by dispatching them to appropriate query services based on intent analysis. **Status: ✅ Operational and integrated**.

#### Integration with OrchestrationEngine

The QueryRouter is integrated into the OrchestrationEngine using an on-demand initialization pattern with session-aware wrappers:

```python
class OrchestrationEngine:
    def __init__(self, llm_client: Optional[LLMClient] = None):
        # QueryRouter initialized on-demand using async session pattern
        self.query_router = None

    async def get_query_router(self) -> QueryRouter:
        """Get QueryRouter, initializing on-demand with session-aware wrappers"""
        if self.query_router is None:
            # Initialize QueryRouter with session-aware services
            self.query_router = QueryRouter(
                project_query_service=SessionAwareProjectQueryService(),
                conversation_query_service=ConversationQueryService(),
                file_query_service=SessionAwareFileQueryService(),
            )
        return self.query_router

    async def handle_query_intent(self, intent: Intent) -> Dict[str, Any]:
        """Handle QUERY intents using QueryRouter integration (GREAT-1B bridge method)"""
        query_router = await self.get_query_router()

        if intent.action in ["search_projects", "list_projects", "find_projects"]:
            projects = await query_router.project_queries.list_active_projects()
            return {"message": f"Found {len(projects)} active projects", "data": projects}
        # ... other query routing logic
```

#### Current Implementation Architecture

> ⚠️ **STALE SECTION (noted 2026-08-02)**: `QueryRouter` and `LLMIntentClassifier`
> below were **deleted** (#1436 Family-3 on 2026-07-19 and #1432 on 2026-08-02).
> This excerpt is retained as historical description only; a fuller architecture.md
> sweep is tracked as discovered work.

The QueryRouter uses a comprehensive initialization pattern with multiple service integrations:

```python
class QueryRouter:
    """Routes QUERY intents to appropriate query services with LLM enhancement"""

    def __init__(
        self,
        project_query_service: ProjectQueryService,
        conversation_query_service: ConversationQueryService,
        file_query_service: FileQueryService,
        # PM-034 Phase 2B: LLM Intent Classification Integration
        llm_classifier: Optional[LLMIntentClassifier] = None,
        knowledge_graph_service: Optional[KnowledgeGraphService] = None,
        semantic_indexing_service: Optional[SemanticIndexingService] = None,
        # Performance and reliability features
        performance_targets: Optional[Dict[str, float]] = None,
        degradation_config: Optional[Dict] = None,
        # MCP Consumer integration for external tool federation
        mcp_consumer: Optional["MCPConsumerCore"] = None,
        enable_mcp_federation: bool = True,
    ):
        # Service initialization with comprehensive configuration
```

#### Request Processing Flow

The complete flow from user input to QueryRouter execution:

1. **Web Layer** (`web/app.py`): Receives user input and creates workflow
2. **Intent Classification**: User input classified using LLM with resilient JSON parsing
3. **Category Routing**: QUERY intents routed to `orchestration_engine.handle_query_intent(intent)`
4. **QueryRouter Initialization**: On-demand initialization with session-aware wrappers
5. **Query Dispatch**: QueryRouter selects appropriate service based on query action
6. **Response Assembly**: Results formatted and returned through orchestration pipeline

```python
# Actual flow in web/app.py
if intent.category.value == "QUERY":
    print(f"🔧 Routing generic QUERY intent to QueryRouter: {intent.action}")
    result = await orchestration_engine.handle_query_intent(intent)
    return {
        "message": f"Query processed successfully: {intent.action}",
        "result": result,
        "workflow_id": workflow.id,
    }
```

#### Error Handling and Resilience

The QueryRouter implementation includes comprehensive error handling:

- **Session Management**: Session-aware wrappers handle their own session management per-operation
- **LLM Integration**: Resilient JSON parsing with progressive fallback strategies (6-strategy system)
- **API Reliability**: `response_format={"type": "json_object"}` parameter ensures consistent JSON responses
- **Performance Optimization**: Sub-500ms target with concurrent request handling
- **Regression Prevention**: Comprehensive test suite in `tests/regression/test_queryrouter_lock.py` prevents accidental disabling

#### Implementation History

**September 2025 - PM-034 QueryRouter Resurrection**:

- **Issue Identified**: QueryRouter was 75% complete but disabled due to initialization failures
- **Root Cause**: Missing LLM response formatting parameters causing JSON parsing errors under load
- **Resolution Applied**:
  - Added `response_format={"type": "json_object"}` parameter to LLM calls
  - Implemented resilient JSON parsing with 6-strategy progressive fallback
  - Restored QueryRouter initialization in OrchestrationEngine using async session pattern
  - Created bridge method `handle_query_intent()` for seamless integration
- **Verification**: Comprehensive regression test suite added to prevent future disabling
- **Performance**: Achieved sub-500ms response times with concurrent request handling

**Key Technical Improvements**:

- **LLM Integration**: Robust parameter passing prevents malformed JSON responses
- **Error Handling**: Graceful degradation under load with fallback parsing strategies
- **Locking Mechanisms**: Test suite prevents accidental commenting out or disabling
- **Session Awareness**: Proper async session management for database operations

#### Current Status (September 2025 - Metrics Verified October 2025)

**Implementation Status**: ✅ Complete and operational

- **Location**: `services/queries/query_router.py` (935 lines total)
- **Class Structure**: Lines 39-934 (896 lines of QueryRouter class)
- **Methods**: 18 methods total (including `__init__`, `route_query`, `classify_and_route`, `federated_search`)
- **Instance Variables**: 16 variables
- **Integration**: Fully connected to OrchestrationEngine via `handle_query_intent()` bridge method
- **LLM Integration**: Resilient JSON parsing with progressive fallback (100% reliability achieved)
- **Performance**: Optimized with response_format parameter for reliable JSON responses
- **Testing**: 9 comprehensive regression tests (296 lines) in `tests/regression/test_queryrouter_lock.py` prevent accidental disabling
- **Dependencies**: AsyncSessionFactory for database operations, session-aware wrappers for service management

**Verified Metrics (October 13, 2025)**:
- QueryRouter implementation verified via Serena MCP symbolic analysis
- All quantifiable claims validated against actual codebase
- Lock test suite confirmed: 9 tests covering initialization, session management, and integration points
- Documentation accuracy: 98%+ (evidence package: `dev/2025/10/13/proof-1-great-1-evidence.md`)

### Query Services

Query services provide read-only access to domain data:

```python

python
class ProjectQueryService:
    async def list_active_projects(self) -> List[Project]:
        return await self.repo.list_active_projects()

    async def get_project_by_id(self, project_id: str) -> Optional[Project]:
        return await self.repo.get_by_id(project_id)

```

### Supported Query Actions

- `list_projects` - List all active projects
- `get_project` - Get specific project by ID
- `get_default_project` - Get the default project
- `find_project` - Find project by name
- `count_projects` - Count active projects

## Web UI: DDD-Compliant Response Rendering (2025)

The web UI is now implemented as a DDD-compliant, test-driven interface. All bot message rendering and response handling is unified in a shared domain module (`bot-message-renderer.js`), ensuring:

- Consistent user experience across all response types
- Separation of domain logic from UI/infrastructure
- Full test coverage via TDD (unit and integration tests)
- Easy extensibility for new message types and workflows

**Key Features:**

- Unified renderer for all bot messages (success, error, thinking)
- Modular, reusable domain logic
- Real-time feedback and error handling
- Markdown rendering with `marked.js` (battle-tested library)

**Architecture Impact:**

- UI layer now fully reflects DDD principles
- All message formatting and business rules live in the domain module, not the presentation layer
- TDD process ensures maintainability and reliability

#### Message Humanization Flow

1. **Intent Processing**: User input classified into category and action
2. **Workflow Execution**: Technical operations performed
3. **Template Selection**: Appropriate template chosen based on intent
4. **Action Humanization**: Technical strings converted via cache/rules
5. **Message Rendering**: Template populated with humanized content
6. **User Response**: Natural language message delivered

**Example Flow**:

```
User Input: "Users are complaining about crashes when uploading photos"
     ↓
Intent: ANALYSIS / investigate_crash
     ↓
Workflow: GENERATE_REPORT (crash analysis)
     ↓
Template: "I'll {human_action} you reported. Let me analyze this for you."
     ↓
Humanization: "investigate_crash" → "investigate the crash"
     ↓
Response: "I'll investigate the crash you reported. Let me analyze this for you."
```

#### Design Principles

- **Cache-First**: Always check cache before generating humanizations
- **Consistency**: Same action always produces same humanization
- **Performance**: Sub-millisecond response for cached entries
- **Extensibility**: Rule-based now, ML-enhanced future

## Current Architecture Strengths

### 1. Solid Infrastructure Foundation

All core infrastructure services are deployed and operational:

- **PostgreSQL**: Primary data store with domain-first schema (SQLAlchemy model-driven)
- **Redis**: Event queue and caching
- **ChromaDB**: Vector storage for knowledge base (85+ documents indexed)
- **Temporal**: Workflow orchestration engine
- **Traefik**: API gateway and load balancing

### 2. Working Intelligence Layer

Core AI capabilities are operational:

- **Intent Classification**: Natural language understanding with context (95%+ accuracy on PM tasks)
- **Knowledge Integration**: Document search and context injection
- **LLM Integration**: Claude and OpenAI APIs connected and working
- **Multi-turn Conversations**: Clarifying questions system operational

### 3. Domain-Driven Design

Clean separation of concerns with PM concepts driving architecture:

- **Domain Models**: Product, Feature, Stakeholder, WorkItem, Intent, Project
- **Event System**: Asynchronous communication patterns
- **Plugin Architecture**: External systems as modular components
- **Repository Pattern**: Clean data access layer
- **Domain-First Database**: Schema generated from domain models

## Recent Architectural Decisions (June 2025)

### 1. Stateless WorkflowFactory

Adopted per-call pattern for context injection rather than stateful factories. Benefits:

- Explicit dependencies
- Better testability
- Concurrency safety
- Follows functional programming principles

### 2. CQRS-lite Pattern

Introduced Query Service pattern to separate reads from writes:

- Commands go through workflows
- Queries go directly to services
- Prevents forcing simple reads into complex workflow patterns

### 3. Project Context Resolution

Implemented sophisticated project resolution with:

- Explicit project IDs take precedence
- Session-based project memory
- LLM-powered inference from context
- Graceful ambiguity handling

### 4. Domain-First Database Schema

Moved from hardcoded SQL to SQLAlchemy model-driven schema:

- Database schema generated from domain models
- Eliminates manual schema drift
- Ensures consistency between domain and persistence layers

### 5. Internal Task Handler Pattern (June 2025)

Discovered and documented during GitHub integration:

- OrchestrationEngine uses internal method handlers instead of separate task handler classes
- Pattern: `self.task_handlers = {TaskType.X: self._method_x}`
- Benefits: Simpler architecture, fewer files, direct access to engine state
- Example: `TaskType.GITHUB_CREATE_ISSUE: self._create_github_issue`

### 6. Repository Context Enrichment Pattern (June 2025)

Implemented automatic repository lookup for GitHub workflows:

- Context enrichment happens in `create_workflow_from_intent`
- Non-blocking pattern: failures logged but don't break workflow creation
- Hierarchy: Project → Integration → Repository → Workflow Context
- Enables seamless "create a ticket" without specifying repository

### 7. Docker Best Practices (June 2025)

**Named Volumes (Recommended)**:

```yaml
volumes:
  piper_postgres_data:
    name: piper_postgres_data_v1 # Explicit versioned name
```

**Benefits**:

- Survives directory renames
- Managed by Docker
- Explicit versioning
- No path dependencies

**Avoid Bind Mounts for Databases**:

- Fragile with directory changes
- Path-dependent
- Can be lost during refactoring

**Lesson Learned**: PM-011 - Directory rename caused data loss with bind mounts

## Critical Gaps (Current Priority)

### 1. Basic Error Handling

**Status**: Not implemented
**Impact**: Users get technical errors instead of helpful messages
**Solution**: Implement comprehensive error handling with user-friendly messages

### 2. Web Chat Interface

**Status**: Not started
**Impact**: API-only interaction blocks user testing
**Solution**: Build simple Streamlit or FastAPI chat interface

### 3. Query/Command Separation

**Status**: Partially implemented (PM-009 query work in progress)
**Impact**: Some queries forced into workflow pattern
**Solution**: Complete Query Service implementation for LIST_PROJECTS and similar operations

## Architectural Decisions

### 1. Event-Driven Communication

All services communicate through events for:

- **Scalability**: Asynchronous processing
- **Learning**: Event history for pattern analysis
- **Reliability**: Retry and replay capabilities

### 2. Multi-LLM Strategy

Different models for different tasks:

- **Claude Opus**: Complex reasoning and analysis
- **Claude Sonnet**: Quick intent classification
- **OpenAI**: Embeddings and specialized tasks
- **Future**: Task-specific model selection

### 3. Plugin-Based Integrations

External systems as plugins for:

- **Modularity**: Independent development and testing
- **Flexibility**: Easy addition of new integrations
- **Maintenance**: Isolated failure and updates

## Evolution Path

### Phase 1 (Current - Q2 2025): Foundation + Basic Execution

**Status**: 100% Complete

- ✅ Infrastructure deployment and configuration
- ✅ Core domain models and persistence
- ✅ Intent classification with high accuracy
- ✅ Basic workflow execution (working end-to-end)
- ✅ GitHub integration functional (issue creation and analysis automated)
- ✅ SUMMARIZE task handler domain model consistency fixed
- ✅ Workflow context handling robustness improved
- ✅ Database persistence with domain-first schema
- 🔄 PM-009 multi-project support (context resolution done, queries in progress)
- 🔄 Query/Command pattern introduction
- 📋 Basic error handling and user feedback
- 📋 Web chat interface

### Phase 2 (Next - Q3 2025): Intelligence Enhancement

**Goals**: Complete CQRS, activate learning, enhance workflows

- Complete Query/Command separation
- Implement feedback-based learning
- Multi-repository workflow support
- Enhanced knowledge search with relationship awareness
- Basic analytics and reporting
- Production monitoring and hardening
- Analytics platform integration (Datadog, New Relic, GA)
- Meeting transcript processing and visualization
- Advanced knowledge graph with relationship mapping
- Visual content analysis foundation

### Phase 3 (Future - Q4 2025+): Advanced Capabilities

**Vision**: Autonomous assistance and strategic insights

- Predictive analytics from PM patterns
- Cross-system orchestration (Jira, Slack, Analytics)
- Autonomous workflow optimization
- Strategic recommendations
- Multi-team support and knowledge sharing

## Technical Debt & Risks

### Immediate Risks

1. **Import Dependencies**: Some circular dependency risks in orchestration layer
2. **Error Handling**: No user-friendly error messages

### Medium-Term Considerations

1. **Performance**: Vector search needs optimization for larger knowledge bases
2. **Security**: API key rotation and audit logging needed
3. **Monitoring**: Observability gaps for debugging production issues

### Long-Term Architecture Evolution

1. **Microservices**: May need service decomposition as complexity grows
2. **Multi-Tenancy**: Current design assumes single organization
3. **Federated Learning**: Cross-organization knowledge sharing capabilities

## Success Metrics

### Current Performance

- **Intent Classification**: 95%+ accuracy on common PM tasks
- **Workflow Completion**: Working end-to-end with placeholder handlers
- **Knowledge Relevance**: 70%+ (needs tuning)
- **Response Time**: 2-4 seconds average

### Target Metrics (Q3 2025)

- **Query Response Time**: <1 second
- **Workflow Success Rate**: 95%+ with real handlers
- **Knowledge Relevance**: 90%+
- **User Satisfaction**: 4.5/5 rating
- **Error Handling**: 90%+ errors with user-friendly messages
- **Meeting Processing**: 90%+ action item extraction accuracy
- **Analytics Integration**: Daily automated insights generation
- **Knowledge Discovery**: 50%+ improvement in cross-project insight finding
- **Autonomous Operations**: 30%+ routine tasks self-managed

## Recent Architectural Refinements (July 2025)

### Type Safety and Context Handling Evolution

**Date**: July 13, 2025
**Impact**: High - Runtime reliability improvements, test contract changes

#### Database Interface Type Safety

**Problem Solved**: File analysis workflow failures due to type mismatches between workflow context (integers) and database queries (strings).

**Root Cause**: Workflow context handling evolved to pass file IDs as integers from session management, but PostgreSQL repository interfaces expected string parameters.

**Solution Pattern**:

```python
# Type conversion at service boundaries
file_id = str(file_id)  # Convert to expected type before repository call
```

**Architectural Lesson**: **Always validate and convert types at service boundaries** to maintain contract integrity between layers.

#### Context Propagation Enhancement

**Enhancement**: Added intent metadata to workflow context for template system integration.

**Pattern**:

```python
# Enhanced context propagation
context["intent_category"] = intent.category.value
context["intent_action"] = intent.action
```

**Impact**: Enables context-aware messaging without breaking domain model isolation.

#### Pre-Classifier Pattern Refinement

**Problem**: Rule-based pre-classification became too aggressive, matching compound messages that require LLM analysis.

**Evolution**:

- **Before**: Simple string matching for exact patterns
- **After**: Regex patterns with word boundaries for precision
- **Issue**: Lost compound message filtering (e.g., "hi there how are you" should not be pre-classified)

**Required Fix**: Add complexity detection to distinguish simple vs. compound messages.

**Architectural Principle**: **Pre-classification should handle only unambiguous patterns**. Complex or compound messages must flow through full LLM analysis.

### Template System Integration

**Date**: July 13, 2025
**Status**: REMOVED 2026-08-29 (#1638). The integration point described below was `main.py`'s
chat handler, which was gutted 2025-10-01; the template module was never re-wired into the
successor path (`web/app.py` / `IntentService`) and was disposed with zero production callers
per Arch's 2026-08-28 ruling. Kept as a historical record of the original design.

#### Design Success

- **Separation of Concerns**: Template logic isolated in dedicated module
- **Context Propagation**: Leverages existing workflow context patterns
- **Backward Compatibility**: Existing workflows continue functioning with fallback templates
- **Performance**: Negligible overhead from O(1) template lookups

#### Key Pattern

```python
# Intent-based template selection
template = get_message_template(
    intent_category=workflow.context.get("intent_category"),
    intent_action=workflow.context.get("intent_action"),
    workflow_type=workflow.type
)
```

### Test Contract Evolution

**Issue**: Architectural improvements broke test assumptions about context handling and pre-classification behavior.

**Root Cause**: Tests written against earlier patterns didn't evolve with architectural refinements.

**Lessons Learned**:

1. **Interface Evolution**: When improving internal patterns, verify test compatibility
2. **Contract Documentation**: Test expectations should be documented alongside implementation changes
3. **Regression Testing**: Architectural changes require comprehensive test validation

### File Analysis Pipeline Reliability

**Achievement**: Complete end-to-end file analysis pipeline now functional after resolving type safety issues.

**Components Validated**:

- File upload and storage
- Type detection and analyzer selection
- Content analysis and summarization
- Template-based response formatting
- UI integration and display

**Performance**: File analysis workflow success rate: 100% (post-fix)

---

## 2025-07-15: AsyncSessionFactory Migration & Test Suite Modernization

- **AsyncSessionFactory Migration:**

  - All orchestration and repository components now use a standardized async session management pattern (`AsyncSessionFactory`).
  - This improves testability, reliability, and future scalability of all workflow and database operations.

- **Business Logic Test Suite Modernization:**

  - All business logic tests have been updated to match improved system behavior (greetings, farewells, thanks, file references, clarifications).
  - Edge cases are now correctly classified; only one known limitation (verb usage of 'file') is tracked as xfail/TODO.
  - Pass rate is 85.5%; all remaining failures are infrastructure-related.

- **Current Infrastructure TODOs:**
  - Remaining test failures are due to asyncpg/SQLAlchemy event loop and session management issues.
  - Next focus: refactor test fixtures and connection pool handling for full async compatibility.

See session logs and migration guide for full details.

---

## 2025-07-18: MCP Connection Pool Architecture & Performance Optimization

### Connection Pool Pattern Implementation

**Date**: July 18, 2025
**Impact**: 642x performance improvement, production-ready infrastructure
**Status**: Complete with feature flag deployment

#### Problem Solved

The initial MCP integration suffered from a critical **connection-per-request** pattern causing:

- **103ms connection overhead** per request
- **Resource leaks** from unclosed connections
- **Memory growth** under sustained usage
- **Scalability barriers** for concurrent requests

#### Solution Architecture

**Singleton Connection Pool with Circuit Breaker Protection**:

```python
class MCPConnectionPool:
    """Thread-safe singleton with circuit breaker and health monitoring"""

    @asynccontextmanager
    async def connection(self, server_config: Dict[str, Any]):
        """Context manager for automatic connection lifecycle"""
        connection = await self.get_connection(server_config)
        try:
            yield connection
        finally:
            await self.return_connection(connection)
```

#### Key Architecture Patterns

##### 1. Thread-Safe Singleton Pattern

```python
_instance = None
_instance_lock = threading.Lock()

@classmethod
def get_instance(cls):
    if cls._instance is None:
        with cls._instance_lock:
            if cls._instance is None:  # Double-checked locking
                cls._instance = cls()
    return cls._instance
```

##### 2. Lazy Async Resource Initialization

```python
async def _ensure_async_resources(self):
    """Initialize async resources only when needed"""
    if self._connection_semaphore is None:
        self._connection_semaphore = asyncio.Semaphore(self.max_connections)
    if self._pool_lock is None:
        self._pool_lock = asyncio.Lock()
```

**Critical Discovery**: **Never hold async locks during I/O operations**. Initial implementation deadlocked due to nested lock acquisition during connection creation.

##### 3. Circuit Breaker Integration

```python
async def _check_circuit_breaker(self):
    """Prevent cascade failures with configurable thresholds"""
    if self._circuit_state == "open":
        if time.time() - self._last_failure_time > self.circuit_breaker_timeout:
            self._circuit_state = "half-open"
        else:
            raise MCPCircuitBreakerOpenError("Circuit breaker is open")
```

**Configuration**:

- **Failure Threshold**: 5 failures before opening
- **Recovery Timeout**: 60 seconds for half-open state
- **Health Monitoring**: Automatic dead connection removal

#### Feature Flag Integration

**Safe Deployment Pattern**:

```python
# Feature flag with graceful fallback
USE_MCP_POOL = os.getenv("USE_MCP_POOL", "false").lower() == "true"

# Dual-mode operation in MCPResourceManager
if self.use_pool:
    async with self.connection_pool.connection(self.client_config) as client:
        content_results = await client.search_content(query)
else:
    content_results = await self.client.search_content(query)
```

**Benefits**:

- **Zero-risk deployment**: Default disabled
- **Immediate rollback**: Configuration-based fallback
- **Production validation**: Both modes tested in production

#### Performance Results

| Metric             | Before (POC)       | After (Pool)         | Improvement       |
| ------------------ | ------------------ | -------------------- | ----------------- |
| Connection Time    | 103ms              | **0.16ms**           | **642x faster**   |
| Memory Usage       | Growing            | Stable               | Leak eliminated   |
| Concurrent Scaling | Linear degradation | Constant performance | Unlimited scaling |

**Real-World Impact**:

- 100 searches/day/user = 49.4 seconds saved per user
- 20 concurrent users = 16.5 minutes daily productivity gain
- Monthly savings: 5.5 hours of user productivity

#### Test-Driven Development Success

**TDD Metrics**:

- **17 comprehensive tests** written before implementation
- **100% test coverage** including edge cases and concurrency
- **Zero post-implementation bugs** through disciplined TDD
- **90-minute implementation** time after 30-minute test design

**Test Categories**:

- Singleton pattern enforcement and thread safety
- Connection lifecycle and reuse validation
- Circuit breaker failure and recovery scenarios
- Graceful shutdown and resource cleanup
- Health monitoring and dead connection removal

### Circuit Breaker Implementation Pattern

#### Design Principles

**Centralized Fault Tolerance**: Pool-level circuit breaker provides system-wide protection against cascade failures.

```python
class MCPConnectionPool:
    def __init__(self):
        # Circuit breaker configuration
        self.circuit_breaker_threshold = 5    # Failures before opening
        self.circuit_breaker_timeout = 60     # Recovery timeout (seconds)
        self._circuit_state = "closed"        # closed, open, half-open
        self._failure_count = 0
        self._last_failure_time = 0

    async def _record_failure(self):
        """Record failure and potentially open circuit breaker"""
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._failure_count >= self.circuit_breaker_threshold:
            self._circuit_state = "open"
            logger.error(f"Circuit breaker opened after {self._failure_count} failures")

    async def _record_success(self):
        """Record success and potentially close circuit breaker"""
        if self._circuit_state == "half-open":
            self._circuit_state = "closed"
            self._failure_count = 0
            logger.info("Circuit breaker closed after successful connection")
```

#### State Transition Logic

- **Closed → Open**: After threshold failures (5 consecutive)
- **Open → Half-Open**: After recovery timeout (60 seconds)
- **Half-Open → Closed**: After successful operation
- **Half-Open → Open**: After failure during test

#### Integration Benefits

- **Prevents Resource Exhaustion**: Stops connection attempts during outages
- **Automatic Recovery**: Self-healing after service restoration
- **Operational Visibility**: Clear state monitoring and logging
- **Graceful Degradation**: Fails fast rather than hanging

### Async Patterns and Lock Management

#### Critical Async Pattern Discovery

**❌ Anti-Pattern: Holding Locks During I/O**

```python
# WRONG - Causes deadlocks
async def _create_new_connection(self, server_config):
    async with self._pool_lock:  # Lock acquired
        connection = PiperMCPClient(server_config)
        await connection.connect()  # I/O operation while holding lock

        async with self._pool_lock:  # DEADLOCK - nested acquisition
            self._all_connections.append(connection)
```

**✅ Correct Pattern: Minimize Lock Scope**

```python
# CORRECT - Lock only for shared state modification
async def _create_new_connection(self, server_config):
    # I/O outside lock scope
    connection = PiperMCPClient(server_config)
    await connection.connect()

    # Lock only for state modification
    async with self._pool_lock:
        self._all_connections.append(connection)
```

#### Async Resource Management Patterns

##### 1. Lazy Async Initialization

**Problem**: Async resources (locks, semaphores) cannot be created in `__init__` due to event loop requirements.

**Solution**: Lazy initialization pattern:

```python
async def _ensure_async_resources(self):
    """Initialize async resources when first needed"""
    if self._connection_semaphore is None:
        self._connection_semaphore = asyncio.Semaphore(self.max_connections)
    if self._pool_lock is None:
        self._pool_lock = asyncio.Lock()
```

##### 2. Context Manager Pattern for Resource Lifecycle

**Automatic Resource Management**:

```python
@asynccontextmanager
async def connection(self, server_config: Dict[str, Any]):
    """Automatic connection acquisition and return"""
    connection = await self.get_connection(server_config)
    try:
        yield connection
    finally:
        await self.return_connection(connection)
```

**Usage Benefits**:

- **Guaranteed Cleanup**: Connection always returned to pool
- **Exception Safety**: Cleanup occurs even on failures
- **Clear Resource Scope**: Explicit connection lifetime boundaries

##### 3. Semaphore-Based Resource Limiting

**Connection Limiting Pattern**:

```python
async def get_connection(self, server_config):
    # Acquire semaphore with timeout
    await asyncio.wait_for(
        self._connection_semaphore.acquire(),
        timeout=self.connection_timeout
    )

    try:
        return await self._get_or_create_connection(server_config)
    except Exception:
        # Always release semaphore on failure
        self._connection_semaphore.release()
        raise
```

#### Best Practices Established

1. **Lock Scope Minimization**: Hold locks only for shared state modifications
2. **I/O Outside Locks**: Never perform I/O operations while holding async locks
3. **Lazy Async Initialization**: Initialize async resources when first needed
4. **Exception-Safe Cleanup**: Use try/finally or context managers for resource cleanup
5. **Semaphore Pattern**: Use semaphores for resource limiting with timeout protection

### Architecture Integration

#### MCPResourceManager Enhancement

**Dual-Mode Integration**: Enhanced existing `MCPResourceManager` to support both direct connections and pooled connections through feature flag.

**Key Integration Points**:

```python
# Initialize method - detects pool availability
async def initialize(self, enabled: bool = False):
    if self.use_pool:
        # Test pool connectivity
        async with self.connection_pool.connection(self.client_config) as test_client:
            if await test_client.is_connected():
                self.initialized = True
    else:
        # Direct connection (legacy mode)
        self.client = PiperMCPClient(self.client_config)
        # ... existing logic
```

**Enhanced Statistics**: Combined pool and connection metrics for comprehensive monitoring:

```python
async def get_connection_stats(self):
    base_stats = {
        "using_pool": self.use_pool,
        "enabled": self.enabled,
        "initialized": self.initialized,
        "available": await self.is_available()
    }

    if self.use_pool and self.connection_pool:
        pool_stats = self.connection_pool.get_stats()
        base_stats.update(pool_stats)
    elif self.client:
        client_stats = self.client.get_connection_stats()
        base_stats.update(client_stats)

    return base_stats
```

#### Zero-Breaking-Change Integration

**Backward Compatibility**: All existing `MCPResourceManager` APIs maintained without modification.

**Deployment Strategy**:

- **Default Disabled**: `USE_MCP_POOL=false` by default
- **Opt-In Activation**: Set `USE_MCP_POOL=true` to enable pool
- **Graceful Fallback**: Pool unavailable → automatic direct connection mode
- **Enhanced Monitoring**: Pool statistics integrated into existing stats API

### Performance Optimization Lessons

#### Connection Reuse Impact

**Measurement Methodology**:

- Baseline: POC with direct connections
- Test Environment: MacBook Pro M1, Python 3.9.6, simulated MCP server
- Metrics: Connection time, search latency, concurrent access scaling

**Key Findings**:

1. **Connection Establishment**: 642x improvement (103ms → 0.16ms)
2. **Search Operations**: 12x improvement (120ms → 10ms total)
3. **Memory Efficiency**: O(n) → O(1) resource usage
4. **Concurrent Scaling**: Linear degradation → constant performance

#### Real-World Performance Impact

**Production Load Simulation**:

- 100 file searches per user per day
- 8-hour work days
- 20 concurrent users

**Productivity Gains**:

- **Per Operation**: 102.84ms saved (98.4% reduction)
- **Per User Daily**: 49.4 seconds saved
- **Team Daily**: 16.5 minutes total saved
- **Monthly Impact**: 5.5 hours of reclaimed productivity

### Case Study Reference

**Complete Technical Documentation**: [MCP Connection Pool - 642x Performance Improvement](../../development/case-studies/mcp-connection-pool-642x.md)

**Comprehensive Analysis Including**:

- Detailed problem statement and root cause analysis
- TDD implementation methodology with test coverage
- Architecture patterns applicable to future infrastructure
- Performance benchmarks and real-world impact calculations
- Lessons learned and best practices for async infrastructure
- Production deployment strategy with feature flags

**Key Architectural Contributions**:

- **Singleton Connection Pool Pattern**: Template for resource pooling
- **Circuit Breaker Integration**: Fault tolerance for external services
- **Async Resource Management**: Patterns for lock-free I/O operations
- **Feature Flag Deployment**: Zero-risk infrastructure improvements
- **TDD Infrastructure**: Test-first approach for production reliability

---

## Python Version Requirements

### Current Standard

- **Python Version**: 3.11+ (required)
- **Rationale**: AsyncIO.timeout functionality, performance improvements, enhanced error messages

### Key Python 3.11 Features Used

- `asyncio.timeout()`: Critical for async operation timeouts
- Enhanced asyncio patterns: Improved async/await error handling
- Performance optimizations: Faster startup and async operations

### Environment Consistency

- **Development**: Python 3.11+ required
- **Docker**: python:3.11-slim-bullseye base images
- **CI/CD**: GitHub Actions use Python 3.11
- **Production**: Python 3.11+ required

### Migration Completed

- **PM-055**: Python version consistency achieved (July 2025)
- **AsyncIO.timeout bug**: Resolved through Python 3.11 upgrade
- **Environment standardization**: All contexts use Python 3.11

## GitHub Integration Router (COMPLETED - CORE-GREAT-2B)

### Overview
All GitHub operations now flow through GitHubIntegrationRouter, enabling feature flag control between spatial intelligence and legacy operations.

### Implementation Status - September 27, 2025
- **Router Completion**: 14/14 GitHubAgent methods implemented with 100% delegation pattern compliance
- **Service Conversion**: 6/6 services converted from direct imports to router usage
- **Feature Flag Control**: Spatial/legacy mode switching functional and tested
- **Architectural Lock**: Multi-layer enforcement prevents regression

### Services Using Router
1. `services/orchestration/engine.py` - OrchestrationEngine
2. `services/domain/github_domain_service.py` - GitHubDomainService
3. `services/domain/pm_number_manager.py` - PMNumberManager
4. `services/domain/standup_orchestration_service.py` - StandupOrchestrationService
5. `services/integrations/github/issue_analyzer.py` - GitHubIssueAnalyzer
6. `services/queries/query_router.py` - QueryRouter

### Enforcement Mechanisms
1. **Anti-Pattern Tests**: `tests/test_architecture_enforcement.py` (7 comprehensive tests)
2. **Pre-commit Hooks**: `.pre-commit-config.yaml` (automated violation blocking)
3. **CI/CD Integration**: `.github/workflows/architecture-enforcement.yml`
4. **Documentation**: Complete architectural guide at `docs/architecture/github-integration-router.md`

### Feature Flag Configuration
- `USE_SPATIAL_GITHUB=true`: Enables spatial intelligence (8-dimensional analysis)
- `USE_SPATIAL_GITHUB=false`: Uses legacy GitHub operations
- Both modes tested and functional across all converted services

### Migration Benefits Achieved
- **Spatial Intelligence**: 8-dimensional GitHub analysis when enabled
- **Feature Flag Control**: Centralized spatial/legacy integration management
- **Deprecation Management**: Proper warnings and migration path
- **Consistent Error Handling**: Standardized RuntimeError patterns
- **Future-Proof Architecture**: Ready for CORE-QUERY-1 integration router expansion

### Quality Metrics
- **Pattern Compliance**: 100% (no compromises accepted)
- **Test Coverage**: 100% (all enforcement mechanisms verified)
- **Service Compatibility**: 100% (no breaking changes)
- **Documentation**: Complete (architectural guide and migration instructions)

---

_Last Updated: January 21, 2026_

## Revision Log

- **January 21, 2026**: Added MUX Object Model Layer section documenting consciousness and ownership modules from X1 Sprint (#433, #434, #435, #595, #532)
- **September 27, 2025**: Added GitHub Integration Router completion (CORE-GREAT-2B), comprehensive architectural protection with multi-layer enforcement, spatial intelligence feature flag control
- **July 18, 2025**: Added MCP Connection Pool architecture patterns, circuit breaker implementation, async resource management best practices, and case study reference documenting 642x performance improvement
- **July 13, 2025**: Added architectural refinements from July 2025: type safety patterns, context handling evolution, pre-classifier pattern changes, template system integration, and test contract lessons learned
- **June 28, 2025**: GitHub integration complete, added Internal Task Handler and Repository Context Enrichment patterns, updated Service Layer and External Integrations, removed placeholder handler risk, updated Evolution Path
