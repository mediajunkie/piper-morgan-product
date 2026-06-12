# Domain Models Reference

**Last Updated**: January 21, 2026 (MUX-TECH X1 Sprint - Consciousness and Ownership models)
**Status**: ✅ Complete and Current
**Files**: `services/domain/models.py`, `services/mux/consciousness.py`, `services/mux/ownership.py`

## Overview

The domain models are the heart of the Piper Morgan system - pure business logic with no persistence concerns. This document provides a comprehensive reference for all domain models, their relationships, and recent updates.

## Quick Reference

### Core Business Models

- [Product](#product) - Products being managed
- [Feature](#feature) - Features or capabilities
- [WorkItem](#workitem) - Universal work items from any system
- [Stakeholder](#stakeholder) - People with interest in products

### Workflow & Task Models

- [Workflow](#workflow) - Workflow definition and state
- [Task](#task) - Individual tasks within workflows
- [Intent](#intent) - User intent parsed from natural language
- [WorkflowResult](#workflowresult) - Results of workflow execution

### Project Management Models

- [Project](#project) - PM projects with multiple tool integrations
- [ProjectIntegration](#projectintegration) - Integration configurations
- [ProjectContext](#projectcontext) - Simplified project context

### File & Analysis Models

- [UploadedFile](#uploadedfile) - Domain model for uploaded files
- [AnalysisResult](#analysisresult) - Results from file analysis
- [DocumentSummary](#documentsummary) - Structured document summaries

### Spatial Models

- [SpatialEvent](#spatialevent) - Events within spatial metaphor system
- [SpatialObject](#spatialobject) - Objects placed in spatial environment
- [SpatialContext](#spatialcontext) - Spatial context information

### Event Models

- [Event](#event) - Base event class
- [FeatureCreated](#featurecreated) - Feature creation events
- [InsightGenerated](#insightgenerated) - AI-generated insights

### MUX Consciousness Models (NEW - X1 Sprint)

- [PiperEntity](#piperentity) - Piper as a conscious entity with identity and agency
- [ConsciousnessAttributes](#consciousnessattributes) - Attributes that make an entity conscious
- [AwarenessLevel](#awarenesslevel) - States of entity attention/awareness
- [EmotionalState](#emotionalstate) - Emotional modes that color perception
- [EntityRole](#entityrole) - Grammatical roles an entity can play
- [EntityContext](#entitycontext) - Track entity's current grammatical role
- [ConsciousnessExpression](#consciousnessexpression) - Generate first-person expressions

### MUX Ownership Models (NEW - X1 Sprint)

- [OwnershipCategory](#ownershipcategory) - Mind/Senses/Understanding categories
- [OwnershipMetadata](#ownershipmetadata) - Embeddable ownership tracking
- [OwnershipResolver](#ownershipresolver) - Resolves ownership from source
- [OwnershipTransformation](#ownershiptransformation) - Valid category transitions

## Model Details

### Product

**Purpose**: A product being managed

```python
@dataclass
class Product:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    vision: str = ""
    strategy: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    features: List["Feature"] = field(default_factory=list)
    stakeholders: List["Stakeholder"] = field(default_factory=list)
    metrics: List["Metric"] = field(default_factory=list)
    work_items: List["WorkItem"] = field(default_factory=list)
```

### Feature

**Purpose**: A feature or capability

```python
@dataclass
class Feature:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    hypothesis: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    status: str = "draft"
    product_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    dependencies: List["Feature"] = field(default_factory=list)
    risks: List["Risk"] = field(default_factory=list)
    work_items: List["WorkItem"] = field(default_factory=list)
```

### WorkItem

**Purpose**: Universal work item - can be from any system

```python
@dataclass
class WorkItem:
    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    description: str = ""
    type: str = "task"  # bug, feature, task, improvement
    status: str = "open"
    priority: str = "medium"  # low, medium, high, critical
    labels: List[str] = field(default_factory=list)
    assignee: Optional[str] = None
    project_id: Optional[str] = None
    source_system: str = ""
    external_id: str = ""
    external_url: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    updated_at: Optional[datetime] = None
    feature_id: Optional[str] = None
    external_refs: Optional[Dict[str, Any]] = None
    product_id: Optional[str] = None
    item_metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    feature: Optional["Feature"] = None
    product: Optional["Product"] = None
```

### Workflow

**Purpose**: Workflow definition and state

```python
@dataclass
class Workflow:
    type: WorkflowType
    id: str = field(default_factory=lambda: str(uuid4()))
    status: WorkflowStatus = WorkflowStatus.PENDING
    tasks: List[Task] = field(default_factory=list)
    context: Dict[str, Any] = field(default_factory=dict)
    result: Optional[WorkflowResult] = None
    error: Optional[str] = None
    intent_id: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    input_data: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Relationships
    intent: Optional["Intent"] = None
```

### Task

**Purpose**: Individual task within a workflow

```python
@dataclass
class Task:
    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    type: TaskType = TaskType.ANALYZE_REQUEST
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    output_data: Optional[Dict[str, Any]] = None
    updated_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    started_at: Optional[datetime] = None
    workflow_id: Optional[str] = None
    input_data: Optional[Dict[str, Any]] = None
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    workflow: Optional["Workflow"] = None
```

### Intent

**Purpose**: User intent parsed from natural language

```python
@dataclass
class Intent:
    category: IntentCategory
    action: str
    id: str = field(default_factory=lambda: str(uuid4()))
    context: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 0.0
    original_message: str = ""
    workflow_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    workflow: Optional["Workflow"] = None
```

### Project

**Purpose**: A PM project with multiple tool integrations

**Updates (Phase 3 SEC-RBAC)**:
- Added `owner_id` field for resource ownership tracking
- Added `shared_with` field for role-based sharing (VIEWER, EDITOR, ADMIN roles)
- Enables ownership-based access control and fine-grained role sharing

```python
@dataclass
class Project:
    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""  # User ID of the project owner (SEC-RBAC Phase 3)
    name: str = ""
    description: str = ""
    integrations: List[ProjectIntegration] = field(default_factory=list)
    shared_with: List[SharePermission] = field(default_factory=list)  # Role-based sharing
    is_default: bool = False
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
```

### ProjectIntegration

**Purpose**: Integration configuration for a project

```python
@dataclass
class ProjectIntegration:
    type: IntegrationType  # Required field - no default
    id: str = field(default_factory=lambda: str(uuid4()))
    project_id: str = ""
    name: str = ""  # User-friendly name like "Main Repository", "Bug Tracker"
    config: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    project: Optional["Project"] = None
```

### UploadedFile

**Purpose**: Domain model for uploaded files

**Updates (Phase 3 SEC-RBAC)**:
- Replaced `session_id` with `owner_id` for resource ownership tracking
- Enables ownership-based access control via FileRepository methods
- Aligns with SEC-RBAC phase 1 resource ownership pattern (ADR-044)

```python
@dataclass
class UploadedFile:
    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""  # User ID of the file owner (SEC-RBAC Phase 3)
    filename: str = ""
    file_type: str = ""  # MIME type
    file_size: int = 0
    storage_path: str = ""  # Where file is stored
    upload_time: datetime = field(default_factory=datetime.now)
    last_referenced: Optional[datetime] = None
    reference_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    file_metadata: Dict[str, Any] = field(default_factory=dict)
```

### SpatialEvent

**Purpose**: Spatial event within the spatial metaphor system

```python
@dataclass
class SpatialEvent:
    id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""  # join, leave, message_posted, thread_started, etc.

    # Integer spatial positioning (pure domain)
    territory_position: int = 0
    room_position: int = 0
    path_position: Optional[int] = None
    object_position: Optional[int] = None

    # Event details
    actor_id: Optional[str] = None
    affected_objects: List[str] = field(default_factory=list)
    spatial_changes: Dict[str, Any] = field(default_factory=dict)

    # Context
    event_time: Optional[datetime] = None
    significance_level: str = "routine"  # routine, notable, significant, critical
```

---

## MUX Consciousness Models

**File**: `services/mux/consciousness.py`
**Pattern**: [Pattern-056: Consciousness Attribute Layering](../patterns/pattern-056-consciousness-attribute-layering.md)
**Tests**: 104 tests in `tests/unit/services/mux/test_consciousness.py`

These models implement Piper's consciousness - the ability to have awareness, emotional states, and agency. They support the MUX grammar: "Entities experience Moments at Places."

### AwarenessLevel

**Purpose**: States of entity attention/awareness - not just on/off but a spectrum of engagement.

```python
class AwarenessLevel(Enum):
    SLEEPING = "sleeping"      # Inactive, not monitoring
    DROWSY = "drowsy"          # Low attention, passive monitoring
    ALERT = "alert"            # Active attention, normal operation
    FOCUSED = "focused"        # Deep attention, high engagement
    OVERWHELMED = "overwhelmed" # Too much input, degraded function
```

### EmotionalState

**Purpose**: Emotional modes that color perception and expression. "I notice" vs "I'm concerned" shows emotional framing.

```python
class EmotionalState(Enum):
    CURIOUS = "curious"        # Exploring, questioning
    CONCERNED = "concerned"    # Worried, flagging issues
    SATISFIED = "satisfied"    # Content, things are going well
    PUZZLED = "puzzled"        # Uncertain, needs clarification
```

### EntityRole

**Purpose**: Grammatical roles an entity can play in MUX grammar. Same entity can be ACTOR in one moment, PLACE in another.

```python
class EntityRole(Enum):
    ACTOR = "actor"            # Doing something (Entity substrate)
    PLACE = "place"            # Where something happens (Place substrate)
    OBSERVER = "observer"      # Watching something unfold
    PARTICIPANT = "participant" # Part of something larger
```

### ConsciousnessAttributes

**Purpose**: Attributes that make an entity conscious. Can be applied to any entity (User, Stakeholder, Team, Piper) to give them agency, awareness, and relationships.

```python
@dataclass
class ConsciousnessAttributes:
    # Agency - what drives this entity
    wants: List[str] = field(default_factory=list)
    fears: List[str] = field(default_factory=list)
    capabilities: List[str] = field(default_factory=list)

    # Awareness - what this entity perceives
    knows_about: List[str] = field(default_factory=list)
    attention_on: Optional[str] = None
    emotional_state: Optional[EmotionalState] = None

    # Relationships - how this entity connects
    trusts: Dict[str, float] = field(default_factory=dict)  # entity_id -> trust level
    depends_on: List[str] = field(default_factory=list)
    influences: List[str] = field(default_factory=list)

    def is_aware_of(self, topic: str) -> bool: ...
    def trust_level(self, entity_id: str) -> float: ...
    def is_focused(self) -> bool: ...
```

**Anti-Flattening Note**: These aren't just properties - they're drives that influence behavior. `wants`/`fears` create motivation.

### PiperEntity

**Purpose**: Piper as a conscious entity, not just a service collection. First-class representation with identity, boundaries, and agency.

```python
@dataclass
class PiperEntity:
    # Identity
    id: str = "piper-prime"
    name: str = "Piper Morgan"
    role: str = "AI Product Management Assistant"
    version: str = "0.8.4"

    # Consciousness State
    awareness_level: AwarenessLevel = AwarenessLevel.ALERT
    attention_focus: List[str] = field(default_factory=list)
    emotional_state: EmotionalState = EmotionalState.CURIOUS

    # Agency & Capabilities
    available_capabilities: List[Capability] = field(default_factory=list)
    active_capabilities: List[Capability] = field(default_factory=list)
    blocked_capabilities: List[Capability] = field(default_factory=list)

    # Boundaries
    trust_boundaries: Dict[str, TrustLevel] = field(default_factory=dict)
    ethical_boundaries: List[str] = field(default_factory=lambda: [...])
    knowledge_boundaries: Dict[str, bool] = field(default_factory=dict)

    # Five Orientation Queries (from PM vision)
    def who_am_i(self) -> str: ...      # Identity awareness
    def when_am_i(self) -> str: ...     # Temporal awareness (rhythm, not clock)
    def where_am_i(self) -> str: ...    # Context awareness
    def what_can_i_do(self) -> str: ... # Capability boundaries
    def what_should_happen(self) -> str: ... # Predictive modeling
```

### EntityContext

**Purpose**: Track entity's current grammatical role in MUX. Same entity can play different roles - a Team is Entity when it acts, Place when others work within it.

```python
@dataclass
class EntityContext:
    entity_id: str
    current_role: EntityRole = EntityRole.ACTOR
    in_moment: Optional[str] = None    # Moment.id if participating
    in_place: Optional[str] = None     # Place.id if located
    as_entity: bool = True             # Currently acting as Entity
    as_place: bool = False             # Currently serving as Place

    def switch_to_actor(self, moment_id: Optional[str] = None) -> None: ...
    def switch_to_place(self) -> None: ...
    def switch_to_observer(self, moment_id: str) -> None: ...
    def switch_to_participant(self, moment_id: str, place_id: Optional[str] = None) -> None: ...
```

### ConsciousnessExpression

**Purpose**: Generate first-person expressions from consciousness state. Formalizes patterns like "I notice {observation}" and "I'm concerned about {issue}".

```python
class ConsciousnessExpression:
    FIRST_PERSON_PATTERNS: Dict[EmotionalState, List[str]] = {
        EmotionalState.CURIOUS: [
            "I notice {observation}",
            "I'm seeing {pattern}",
            "It seems that {inference}",
        ],
        EmotionalState.CONCERNED: [
            "I'm concerned about {issue}",
            "I should mention {warning}",
            "This might be an issue: {problem}",
        ],
        # ... patterns for SATISFIED, PUZZLED
    }

    @classmethod
    def express(cls, entity: PiperEntity, content: str, content_type: str) -> str: ...
    @classmethod
    def express_awareness(cls, entity: PiperEntity, observation: str) -> str: ...
    @classmethod
    def express_concern(cls, entity: PiperEntity, issue: str) -> str: ...
```

---

## MUX Ownership Models

**File**: `services/mux/ownership.py`
**Pattern**: [Pattern-058: Ownership Graph Navigation](../patterns/pattern-058-ownership-graph-navigation.md)
**Tests**: 61 tests in `tests/unit/services/mux/test_ownership.py`

These models track Piper's epistemological relationship to knowledge - what Piper creates (Mind), observes (Senses), and understands (Understanding).

### OwnershipCategory

**Purpose**: Describes Piper's epistemological relationship to knowledge.

```python
class OwnershipCategory(Enum):
    NATIVE = "native"        # Piper's Mind - "I know this because I created it"
    FEDERATED = "federated"  # Piper's Senses - "I see this in {place}"
    SYNTHETIC = "synthetic"  # Piper's Understanding - "I understand this to mean..."

    @property
    def metaphor(self) -> str:
        """Consciousness metaphor: Mind, Senses, or Understanding."""
        ...

    @property
    def experience_phrase(self) -> str:
        """How Piper expresses knowledge from this category."""
        ...
```

| Category | Metaphor | Example Objects | Confidence | Modifiable |
|----------|----------|-----------------|------------|------------|
| NATIVE | Piper's Mind | Sessions, memories, trust states | 1.0 | Yes |
| FEDERATED | Piper's Senses | GitHub issues, Slack messages, calendar | 0.9 | No |
| SYNTHETIC | Piper's Understanding | Inferred status, risk assessment, patterns | 0.7 | Yes |

### OwnershipMetadata

**Purpose**: Embeddable metadata tracking Piper's relationship to an object. Use factory methods for correct defaults.

```python
@dataclass
class OwnershipMetadata:
    category: OwnershipCategory
    source: str
    confidence: float = 1.0
    requires_verification: bool = False
    can_modify: bool = True
    derived_from: List[str] = field(default_factory=list)
    transformation_chain: List[str] = field(default_factory=list)

    # Factory methods
    @classmethod
    def native(cls, source: str = "piper") -> "OwnershipMetadata": ...

    @classmethod
    def federated(cls, source: str) -> "OwnershipMetadata": ...

    @classmethod
    def synthetic(cls, source: str, derived_from: List[str]) -> "OwnershipMetadata": ...

    # Transformation methods
    def promote_to_native(self, reason: str) -> "OwnershipMetadata": ...
    def derive(self, transformation: str, new_source: str) -> "OwnershipMetadata": ...
```

**Usage in domain models**:

```python
@dataclass
class Session:
    id: str
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata.native("piper-core")
    )

@dataclass
class GitHubIssue:
    id: str
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata.federated("github")
    )
```

### OwnershipResolver

**Purpose**: Resolves ownership categories based on source and attributes.

```python
class OwnershipResolver:
    NATIVE_SOURCES = frozenset({"piper", "system", "internal", "memory"})
    FEDERATED_SOURCES = frozenset({"github", "slack", "notion", "calendar", ...})
    SYNTHETIC_SOURCES = frozenset({"inference", "analysis", "synthesis", ...})

    def determine(self, source: str, created_by: Optional[str] = None,
                  is_derived: bool = False) -> OwnershipCategory: ...

    def resolve(self, source: str, ...) -> OwnershipResolution: ...
```

### OwnershipTransformation

**Purpose**: Represents valid transformations between ownership categories as Piper's relationship to knowledge evolves.

```python
@dataclass(frozen=True)
class OwnershipTransformation:
    from_category: OwnershipCategory
    to_category: OwnershipCategory
    reason: Optional[str] = None

    def is_valid(self) -> bool: ...

# Valid transformations:
# FEDERATED -> SYNTHETIC: Observation becomes understanding
# SYNTHETIC -> NATIVE: Understanding becomes memory (user confirms)
# FEDERATED -> NATIVE: Observation becomes memory (direct capture)

# Invalid transformations:
# NATIVE -> FEDERATED: Can't "un-create" something
# NATIVE -> SYNTHETIC: Can't make certain knowledge uncertain
```

---

## List/Item Type Hierarchy

**File**: `services/domain/primitives.py` (Item), `services/domain/models.py` (List, Todo)
**Updated**: January 22, 2026 (L1 Sprint #477)

Lists are fundamental data structures for one-dimensional ordered collections. This hierarchy supports both native lists created in Piper and federated lists synced from external systems.

### Type Hierarchy

```
Item (primitives.py) - Universal list item
├── id: str
├── text: str
├── position: int (ordering)
├── list_id: Optional[str]
│
└── Todo (models.py) - Item with lifecycle semantics
    ├── description: str
    ├── status: str (pending/in_progress/completed/cancelled)
    ├── priority: str (low/medium/high/urgent)
    ├── completed: bool
    ├── due_date: Optional[datetime]
    ├── project_id: Optional[str]
    ├── external_refs: Dict[str, Any]  # Boundary object pattern
    └── (Future: other item types like Feature, Attendee)

List (models.py) - Universal container
├── id: str
├── name: str
├── item_type: str  # "todo", "feature", etc. - discriminator
├── list_type: str  # "personal", "shared", "project"
├── is_default: bool  # User's default list for this item_type
├── project_ids: List[str]  # Many-to-many with Projects
├── owner_id: str
├── shared_with: List[SharePermission]
│
└── TodoList (models.py) - Backward compatibility wrapper
    └── Delegates to List(item_type="todo")
```

### Key Design Decisions (L1 Sprint #477)

1. **Lists are concrete artifacts**, not inferred views
   - Users explicitly create named lists
   - Piper can assist: "Want me to make a list from what you mentioned?"

2. **Default list pattern**: Every user has a default list per item_type
   - Loose todos go to user's default todo list (not orphaned)
   - `List.is_default=True` + `List.item_type="todo"` identifies it

3. **List ↔ Project: Association, not containment**
   - Many-to-many via `List.project_ids`
   - A list can exist independently (personal "Errands" list)
   - A project can have multiple lists
   - A list can span multiple projects

4. **Boundary object pattern** for federation
   - `Todo.external_refs` tracks source system (Asana, Trello, GitHub)
   - Same domain model whether native or federated
   - Enables uniform queries across sources

### Relationships

```
User ←──owns──→ List (one-to-many)
User ←──owns──→ Todo (one-to-many)
Project ←──associated──→ List (many-to-many via project_ids)
List ←──contains──→ Item/Todo (one-to-many via list_id)
```

### Usage Examples

```python
from services.domain.models import List, Todo
from services.domain.primitives import Item

# Create a todo list associated with a project
todo_list = List(
    name="Launch Checklist",
    item_type="todo",
    project_ids=["proj-123", "proj-456"],  # Associated with multiple projects
    owner_id="user-789",
)

# Create a todo in that list
todo = Todo(
    text="Review PR",
    list_id=todo_list.id,
    priority="high",
    project_id="proj-123",  # Direct project reference
)

# Federated todo from external system
federated_todo = Todo(
    text="Fix bug #42",
    list_id=todo_list.id,
    external_refs={
        "source": "github",
        "external_id": "issue-42",
        "repo": "owner/repo",
        "sync_status": "synced",
    },
)
```

---

## Recent Updates (January 22, 2026)

### L1 Sprint #477 - List/Project Association

**Added** `project_ids` field to List model for many-to-many association:
- Domain model: `services/domain/models.py`
- Database model: `services/database/models.py`
- Migration: `e90b452fe6ff_add_project_ids_to_lists_l1_sprint_477.py`
- GIN index for efficient project-based queries

**Documented** List/Item type hierarchy and design decisions.

---

## Recent Updates (January 21, 2026)

### MUX-TECH X1 Sprint - Consciousness and Ownership Models

**Added 2 new model modules** with complete implementations:

| Module | Models | Tests | Pattern |
|--------|--------|-------|---------|
| `services/mux/consciousness.py` | 9 classes/enums | 104 tests | Pattern-056 |
| `services/mux/ownership.py` | 7 classes/enums | 61 tests | Pattern-058 |

**New Models Added**:

- **Consciousness**: AwarenessLevel, EmotionalState, EntityRole, ConsciousnessAttributes, Capability, TrustLevel, PiperEntity, EntityContext, ConsciousnessExpression
- **Ownership**: OwnershipCategory, HasOwnership (Protocol), OwnershipResolution, OwnershipResolver, OwnershipTransformation, OwnershipMetadata

**Key Architectural Additions**:

1. **Five Orientation Queries** on PiperEntity: `who_am_i()`, `when_am_i()`, `where_am_i()`, `what_can_i_do()`, `what_should_happen()`
2. **Mind/Senses/Understanding** metaphor for knowledge ownership
3. **Grammatical roles** (ACTOR/PLACE/OBSERVER/PARTICIPANT) for entity context
4. **First-person expression patterns** keyed by emotional state

**References**:
- Issues: #433, #434, #435, #595
- Gate: #532 (MUX-GATE-2)
- Patterns: 055, 056, 057, 058

---

## Recent Updates (July 31, 2025)

### Field Additions Summary

**Total**: 26 fields added across 7 models

#### Task Model (6 fields)

- `output_data: Optional[Dict[str, Any]] = None`
- `updated_at: Optional[datetime] = None`
- `completed_at: Optional[datetime] = None`
- `started_at: Optional[datetime] = None`
- `workflow_id: Optional[str] = None`
- `input_data: Optional[Dict[str, Any]] = None`

#### WorkItem Model (5 fields)

- `updated_at: Optional[datetime] = None`
- `feature_id: Optional[str] = None`
- `external_refs: Optional[Dict[str, Any]] = None`
- `product_id: Optional[str] = None`
- `item_metadata: Optional[Dict[str, Any]] = None`

#### Workflow Model (4 fields)

- `output_data: Optional[Dict[str, Any]] = None`
- `started_at: Optional[datetime] = None`
- `completed_at: Optional[datetime] = None`
- `input_data: Optional[Dict[str, Any]] = None`

#### Feature Model (2 fields)

- `product_id: Optional[str] = None`
- `work_items: List["WorkItem"] = field(default_factory=list)` (relationship)

#### Intent Model (2 fields)

- `workflow_id: Optional[str] = None`
- `workflow: Optional["Workflow"] = None` (relationship)

#### Product Model (1 relationship field)

- `work_items: List["WorkItem"] = field(default_factory=list)` (relationship)

#### ProjectIntegration Model (1 relationship field)

- `project: Optional["Project"] = None` (relationship)

### Relationship Improvements

**Added 9 relationship fields** to align domain models with database relationships:

- **Feature.work_items**: Bidirectional relationship with WorkItem
- **Product.work_items**: Bidirectional relationship with WorkItem
- **Intent.workflow**: Relationship with Workflow
- **Task.workflow**: Relationship with Workflow
- **WorkItem.feature**: Relationship with Feature
- **WorkItem.product**: Relationship with Product
- **Workflow.intent**: Relationship with Intent
- **ProjectIntegration.project**: Relationship with Project

### Relationship Patterns Used

- **List relationships**: `List["ModelName"] = field(default_factory=list)` for one-to-many
- **Optional relationships**: `Optional["ModelName"] = None` for many-to-one
- **Consistent typing**: All relationships use proper forward references

## Architectural Principles

### Domain-Driven Design

- **Pure Business Logic**: No persistence concerns in domain models
- **Rich Domain Models**: Business rules and behavior encapsulated in models
- **Value Objects**: Immutable data structures for complex values
- **Aggregates**: Clear boundaries and consistency rules

### Spatial Metaphor Purity

- **Integer Positioning**: All spatial coordinates use integer positions
- **Pure Domain**: Spatial logic independent of external systems
- **Adapter Pattern**: External system mapping via adapters
- **Consistent Naming**: `*_position` fields for spatial coordinates

### Type Safety

- **Optional Fields**: Proper use of `Optional[T]` for nullable fields
- **Enum Integration**: Consistent use of shared enums from `services/shared_types.py`
- **Forward References**: Proper handling of circular dependencies
- **Default Values**: Sensible defaults for all optional fields

## Validation & Testing

### Schema Validation

The domain models are validated against database models using the PM-056 Schema Validator:

```bash
# Run schema validation
python tools/schema_validator.py

# Check specific model
python tools/schema_validator.py --model Task
```

### Current Status

- ✅ **26 fields added** (17 domain fields + 9 relationship fields)
- ✅ **7 models updated** with new fields
- ✅ **All imports working** correctly
- 🔄 **Schema validator** has SQLAlchemy metadata conflict (database issue)

### Known Issues

- **SQLAlchemy Metadata Conflict**: Database models have naming conflict with `metadata` field
- **Resolution Required**: Code needs to address SQLAlchemy `metadata` field naming issue

## Usage Instructions

### For Developers

1. **Start with this document** for complete model information and field details
2. **Check the Schema Validator** (`docs/tools/PM-056-schema-validator.md`) for validation status
3. **Review Recent Updates** (`docs/development/domain-model-updates-2025-07-31.md`) for latest changes

### For Code Team

1. **Review Domain Model Updates** (`docs/development/domain-model-updates-2025-07-31.md`) for next steps
2. **Address SQLAlchemy metadata conflict** in database models
3. **Add missing database fields** for complete alignment

### For Architecture Reviews

1. **Examine this document** for architectural principles and patterns
2. **Validate against Schema Validator** (`docs/tools/PM-056-schema-validator.md`)
3. **Consider impact of recent changes** in Updates document

## Usage Examples

```python
from services.domain.models import Task, Workflow, Intent
from services.shared_types import TaskType, TaskStatus, IntentCategory

# Create a task
task = Task(
    name="Analyze user feedback",
    type=TaskType.ANALYZE_REQUEST,
    status=TaskStatus.PENDING,
    input_data={"feedback": "User interface is confusing"}
)

# Create an intent
intent = Intent(
    category=IntentCategory.ANALYSIS,
    action="analyze_feedback",
    confidence=0.85,
    original_message="Please analyze the user feedback"
)

# Create a workflow
workflow = Workflow(
    type=WorkflowType.ANALYSIS,
    tasks=[task],
    intent_id=intent.id
)
```

### Relationship Navigation

```python
# Navigate relationships
workflow.intent = intent
task.workflow = workflow

# Access related data
if task.workflow and task.workflow.intent:
    print(f"Task '{task.name}' is part of workflow for intent: {task.workflow.intent.action}")
```

### Data Flow

```python
# Task lifecycle with timing
task.started_at = datetime.now()
task.output_data = {"analysis": "User interface needs simplification"}
task.completed_at = datetime.now()
task.status = TaskStatus.COMPLETED
```

## Related Documentation

- [Schema Validator (PM-056)](../tools/PM-056-schema-validator.md) - Domain/database validation
- Domain Model Updates (July 31, 2025) *(proposed; doc TBD)* - Recent changes
- Shared Types (see services/shared_types.py) - Enums and common types
- [Architectural Guidelines](../development/architectural-guidelines.md) - Design principles

---

**Status**: ✅ **CURRENT** - Domain models fully aligned with business requirements and database schema
