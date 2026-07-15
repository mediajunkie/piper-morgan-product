"""
Piper Morgan 1.0 - Domain Models
The heart of the system - these models drive everything else.
Pure business logic with no persistence concerns.
"""

from __future__ import annotations

# 2025-06-14: Fixed Task type field and status enum to match database model and shared_types
# 2025-06-15: Added Project and ProjectIntegration models for PM-009
# 2025-06-17: Cleaned separation - removed SQLAlchemy code, fixed duplicate imports
# 2026-01-21: Added MUX lifecycle integration (#433)
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID, uuid4

# Import Item primitive for Todo to extend
from services.domain.primitives import Item

# MUX Lifecycle Integration (#433)
# Optional lifecycle support for domain models that evolve through stages
from services.mux.lifecycle import LifecycleState, LifecycleTransition

# MUX Ownership Integration (#435)
# Tracks Piper's relationship to objects: Native (Mind), Federated (Senses), Synthetic (Understanding)
from services.mux.ownership import OwnershipCategory, OwnershipMetadata

# Import shared types for consistency
from services.shared_types import (
    ConversationLifecycleState,
    EdgeType,
    HardnessLevel,
    IntegrationType,
    IntentCategory,
    ListType,
    NodeType,
    OrderingStrategy,
    PlaceConfidence,
    PlaceType,
    PortfolioOnboardingState,
    StandupConversationState,
    TaskStatus,
    TaskType,
    TodoPriority,
    TodoStatus,
    TrustStage,
    WorkflowStatus,
    WorkflowType,
)

# =============================================================================
# REQUEST CONTEXT - ADR-051: Unified User Session Context
# =============================================================================

# Issue #734: Default workspace for single-tenant deployments
# This UUID is used when no explicit workspace_id is provided.
# For multi-tenant deployments, each tenant will have their own workspace_id.
DEFAULT_WORKSPACE_ID = UUID("00000000-0000-0000-0000-000000000000")


@dataclass(frozen=True)
class RequestContext:
    """
    Cross-handler coordination object for the **intent processing path** (ADR-051,
    amended 2026-05-16 per #1015 scope-clarification ratification).

    SCOPE: This is the canonical identity-and-context object for the intent path
    specifically (`web/api/routes/intent.py` → `services/intent/intent_service.py`
    → `services/trust/trust_integration.py` + downstream conversation persistence,
    telemetry, soft-invocation, multi-handler dispatch). It is NOT a cross-cutting
    infrastructure primitive for all routes.

    For all other route/service surfaces (CRUD endpoints, admin, demos, etc.),
    the canonical identity flow is:
        - At routes: `current_user: JWTClaims = Depends(get_current_user)`
        - At services: `user_id: str` (or `UUID`) parameters

    These two patterns are NOT in conflict: dependency-injection is the boundary
    mechanism for identity extraction; RequestContext is the cross-handler
    coordination object for the intent path's multi-service flow.

    Why intent_service earns its keep: it coordinates classification, multi-intent
    orchestration, handler dispatch, conversation persistence, telemetry,
    soft-invocation, and trust gating across many sub-services. Carrying a
    unified context object (with user_id, conversation_id, request_id,
    user_email, formality_baseline) has real ergonomic value on that surface.
    Other route handlers don't have that surface — they make single repository
    or service calls.

    PATTERN-072 CONNECTION: Adopting RequestContext beyond the intent path is a
    Pattern-072 (Registries that Grow into Architectural Shapes) recognition-
    trigger decision. RequestContext currently has one real behavior-deciding
    consumer (intent_service). The trigger fires when a second non-trivial
    coordination surface emerges — a request flow that touches ≥3 service
    boundaries with state that depends on identity-and-context (not just
    identity). See ADR-051 amendment section "Future-state criterion" for
    qualifying-surface definition.

    Immutable (frozen) to prevent modification during request lifecycle.

    Attributes:
        user_id: Authenticated user's database PK (UUID)
        conversation_id: Database PK for conversation record (UUID)
        request_id: Unique per-request for tracing (UUID)
        user_email: User's email for logging/display (denormalized)
        timestamp: Request timestamp
        workspace_id: For future multi-tenant support (DEFAULT_WORKSPACE_ID single-tenant)
        formality_baseline: User's warmth baseline loaded at request boundary

    Example (intent path only):
        # In intent.py - create at boundary when authenticated
        ctx = RequestContext.from_jwt_and_request(
            claims=current_user,
            conversation_id=session_id,
        )

        # In intent_service - receive and use
        async def process_intent(self, ..., ctx: Optional[RequestContext] = None):
            effective_user_id = str(ctx.user_id) if ctx else user_id
    """

    # Core identity (required)
    user_id: UUID  # Authenticated user's database PK
    conversation_id: UUID  # Database PK for conversation record
    request_id: UUID  # Unique per-request for tracing

    # Denormalized for convenience (saves lookup cost on logs)
    user_email: str  # User's email for logging/display
    timestamp: datetime  # Request timestamp

    # Future-proofing
    workspace_id: Optional[UUID] = None  # For future multi-tenant support

    # Unified formality (#838): user's warmth baseline (0.0=professional, 1.0=warm)
    # Loaded from PersonalityProfile at request boundary. None = not yet loaded.
    formality_baseline: Optional[float] = None

    @classmethod
    def from_jwt_and_request(
        cls,
        claims: "JWTClaims",  # Forward reference to avoid circular import
        conversation_id: str,
        request_id: Optional[UUID] = None,
    ) -> "RequestContext":
        """
        Factory method to create context from JWT claims and request data.

        Args:
            claims: JWT claims from authenticated request
            conversation_id: Conversation ID from request (as string)
            request_id: Optional request ID (generated if not provided)

        Returns:
            RequestContext: Immutable context for request processing

        Raises:
            ValueError: If claims.sub or conversation_id is missing
        """
        # Validation - fail fast on malformed input
        if not claims.sub or not str(claims.sub).strip():
            raise ValueError("JWT claims missing 'sub' field")
        if not conversation_id or not str(conversation_id).strip():
            raise ValueError("conversation_id is required")

        # Issue #734: Use DEFAULT_WORKSPACE_ID for single-tenant deployments
        workspace = UUID(claims.workspace_id) if claims.workspace_id else DEFAULT_WORKSPACE_ID

        return cls(
            user_id=UUID(claims.sub),  # str → UUID at boundary
            conversation_id=UUID(conversation_id),  # str → UUID at boundary
            request_id=request_id or uuid4(),
            user_email=claims.user_email,
            timestamp=datetime.now(timezone.utc),
            workspace_id=workspace,
        )

    def __str__(self) -> str:
        """String representation for logging/debugging."""
        return f"RequestContext(user={self.user_id}, conv={self.conversation_id}, req={self.request_id})"


# =============================================================================
# SEC-RBAC Phase 2: Role-Based Permissions
# =============================================================================


class ShareRole(str, Enum):
    """Role for shared resource access (SEC-RBAC Phase 2)"""

    VIEWER = "viewer"  # Read-only access
    EDITOR = "editor"  # Can modify content
    ADMIN = "admin"  # Can share with others and change roles


@dataclass
class SharePermission:
    """Permission entry for a shared resource (SEC-RBAC Phase 2)"""

    user_id: str
    role: ShareRole

    def to_dict(self) -> Dict[str, str]:
        """Convert to dictionary for JSONB serialization"""
        return {"user_id": self.user_id, "role": self.role.value}

    @staticmethod
    def from_dict(data: Dict[str, str]) -> SharePermission:
        """Create from dictionary (JSONB deserialization)"""
        return SharePermission(user_id=data["user_id"], role=ShareRole(data["role"]))


# Core Entities
@dataclass
class Product:
    """A product being managed"""

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


@dataclass
class Feature:
    """A feature or capability"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    hypothesis: str = ""
    acceptance_criteria: List[str] = field(default_factory=list)
    status: str = "draft"
    product_id: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # MUX Lifecycle Integration (#433) - optional, backward compatible
    lifecycle_state: Optional[LifecycleState] = None
    lifecycle_history: List[LifecycleTransition] = field(default_factory=list)

    # Relationships
    dependencies: List["Feature"] = field(default_factory=list)
    risks: List["Risk"] = field(default_factory=list)
    work_items: List["WorkItem"] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.

        Follows the same pattern as WorkItem.to_dict() for consistency.
        Includes lifecycle_state when present (#705 MUX-LIFECYCLE-UI-B).
        """
        result = {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "hypothesis": self.hypothesis,
            "acceptance_criteria": self.acceptance_criteria,
            "status": self.status,
            "product_id": self.product_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
        # Include lifecycle state if present (#705 MUX-LIFECYCLE-UI-B)
        if self.lifecycle_state is not None:
            result["lifecycle_state"] = self.lifecycle_state.value
        return result


@dataclass
class Stakeholder:
    """Someone with interest in the product"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    email: Optional[str] = None
    role: str = ""
    interests: List[str] = field(default_factory=list)
    influence_level: int = 1  # 1-5 scale
    satisfaction: Optional[float] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class WorkItem:
    """Universal work item - can be from any system"""

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

    # MUX Lifecycle Integration (#433) - optional, backward compatible
    lifecycle_state: Optional[LifecycleState] = None
    lifecycle_history: List[LifecycleTransition] = field(default_factory=list)

    # Relationships
    feature: Optional["Feature"] = None
    product: Optional["Product"] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        result = {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "type": self.type,
            "status": self.status,
            "priority": self.priority,
            "labels": self.labels,
            "assignee": self.assignee,
            "project_id": self.project_id,
            "source_system": self.source_system,
            "external_id": self.external_id,
            "external_url": self.external_url,
            "metadata": self.metadata,
            "created_at": self.created_at.isoformat(),
        }
        # Include lifecycle state if present (#685 MUX-LIFECYCLE-OBJECTS)
        if self.lifecycle_state is not None:
            result["lifecycle_state"] = self.lifecycle_state.value
        return result


# PM-009: Project Management Domain Models
@dataclass
class ProjectIntegration:
    """Integration configuration for a project"""

    type: IntegrationType  # Required field - no default
    id: str = field(default_factory=lambda: str(uuid4()))
    project_id: str = ""
    name: str = ""  # User-friendly name like "Main Repository", "Bug Tracker"
    config: Dict[str, Any] = field(default_factory=dict)
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)

    # Relationships
    project: Optional["Project"] = None

    def validate_config(self) -> bool:
        """Validate configuration based on integration type"""
        if self.type == IntegrationType.GITHUB:
            return "repository" in self.config
        elif self.type == IntegrationType.JIRA:
            return all(k in self.config for k in ["url", "project_key"])
        elif self.type == IntegrationType.LINEAR:
            return all(k in self.config for k in ["api_key", "team_id"])
        elif self.type == IntegrationType.SLACK:
            return all(k in self.config for k in ["webhook_url", "channel"])
        return True


@dataclass
class Repository:
    """A code repository — first-class, provider-agnostic domain entity.

    Repositories are independent objects that can be linked to zero or more
    projects via many-to-many relationship (ProjectRepositoryLink).
    Issue #866: Repository as first-class domain entity.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""  # UUID FK to users — who registered this repo
    provider: str = "github"  # "github", "gitlab", "bitbucket"
    full_name: str = ""  # e.g. "octocat/hello-world"
    display_name: str = ""  # User-friendly name, defaults to repo part of full_name
    url: str = ""  # e.g. "https://github.com/octocat/hello-world"
    is_active: bool = True
    # GitHub API metadata (Issue #867) — populated on validation success
    description: Optional[str] = None
    language: Optional[str] = None
    visibility: Optional[str] = None  # "public" | "private" | "internal"
    default_branch: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    def __post_init__(self):
        """Auto-derive display_name from full_name if not set."""
        if not self.display_name and self.full_name:
            self.display_name = (
                self.full_name.split("/")[-1] if "/" in self.full_name else self.full_name
            )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "owner_id": self.owner_id,
            "provider": self.provider,
            "full_name": self.full_name,
            "display_name": self.display_name,
            "url": self.url,
            "is_active": self.is_active,
            "description": self.description,
            "language": self.language,
            "visibility": self.visibility,
            "default_branch": self.default_branch,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }


@dataclass
class ProjectRepositoryLink:
    """Link between a Project and a Repository (many-to-many).

    Issue #866: Repository as first-class domain entity.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    project_id: str = ""
    repository_id: str = ""
    is_primary: bool = False  # Whether this is the "main" repo for the project
    linked_at: datetime = field(default_factory=datetime.now)
    linked_by: str = ""  # User who created the link

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "project_id": self.project_id,
            "repository_id": self.repository_id,
            "is_primary": self.is_primary,
            "linked_at": self.linked_at.isoformat(),
            "linked_by": self.linked_by,
        }


@dataclass
class Project:
    """A PM project with multiple tool integrations"""

    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""
    name: str = ""
    description: str = ""
    integrations: List[ProjectIntegration] = field(default_factory=list)
    repositories: List["Repository"] = field(default_factory=list)
    shared_with: List[SharePermission] = field(default_factory=list)
    is_default: bool = False
    is_archived: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # MUX Ownership (#435) - Projects are NATIVE (user-created within Piper)
    mux_ownership: Optional[OwnershipMetadata] = None

    # MUX Lifecycle Integration (#709) - Projects naturally evolve through lifecycle stages
    lifecycle_state: Optional[LifecycleState] = None

    def get_integration(self, integration_type: IntegrationType) -> Optional[ProjectIntegration]:
        """Get first active integration of specified type"""
        for integration in self.integrations:
            if integration.type == integration_type and integration.is_active:
                return integration
        return None

    def get_github_repository(self) -> Optional[str]:
        """Get GitHub repository for this project.

        Checks Repository entities first (#866 M2M model), falls back to
        ProjectIntegration config for backward compatibility.
        """
        # New path: check linked Repository entities
        for repo in self.repositories:
            if repo.provider == "github" and repo.is_active:
                return repo.full_name

        # Legacy fallback: check ProjectIntegration config
        github_integration = self.get_integration(IntegrationType.GITHUB)
        return github_integration.config.get("repository") if github_integration else None

    def validate_integrations(self) -> List[str]:
        """Validate all integrations, return list of errors"""
        errors = []
        for integration in self.integrations:
            if not integration.validate_config():
                errors.append(f"{integration.type.value}: Invalid configuration")
        return errors

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.

        Includes lifecycle_state when present (#709 MUX-LIFECYCLE-UI-PROJECTS).
        """
        result = {
            "id": self.id,
            "owner_id": self.owner_id,
            "name": self.name,
            "description": self.description,
            "integrations": [
                {
                    "id": integ.id,
                    "type": integ.type.value,
                    "name": integ.name,
                    "config": integ.config,
                    "is_active": integ.is_active,
                    "created_at": integ.created_at.isoformat(),
                }
                for integ in self.integrations
            ],
            "repositories": [repo.to_dict() for repo in self.repositories],
            "shared_with": [perm.to_dict() for perm in self.shared_with],
            "is_default": self.is_default,
            "is_archived": self.is_archived,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "mux_ownership": self.mux_ownership.to_dict() if self.mux_ownership else None,
        }

        # Include lifecycle state if present (#709 MUX-LIFECYCLE-UI-PROJECTS)
        if self.lifecycle_state is not None:
            result["lifecycle_state"] = self.lifecycle_state.value

        return result


@dataclass
class ProjectContext:
    """Simplified project context for content generation"""

    name: str = ""
    description: str = ""
    technologies: List[str] = field(default_factory=list)


@dataclass
class Intent:
    """User intent parsed from natural language"""

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


@dataclass
class Task:
    """Individual task within a workflow"""

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

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type.value if self.type else None,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "created_at": self.created_at.isoformat(),
        }


@dataclass
class WorkflowResult:
    """Result of workflow execution"""

    success: bool = False
    data: Dict[str, Any] = field(default_factory=dict)
    error: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Workflow:
    """Workflow definition and state"""

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

    def get_next_task(self) -> Optional[Task]:
        """Get the next pending task in the workflow"""
        for task in self.tasks:
            if task.status == TaskStatus.PENDING:
                return task
        return None

    def mark_task_completed(self, task_id: str, result: Dict[str, Any]):
        """Mark a task as completed with result"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.COMPLETED
                task.result = result
                break

    def mark_task_failed(self, task_id: str, error: str):
        """Mark a task as failed with error"""
        for task in self.tasks:
            if task.id == task_id:
                task.status = TaskStatus.FAILED
                task.error = error
                break

    def is_complete(self) -> bool:
        """Check if all tasks are completed"""
        return all(task.status in [TaskStatus.COMPLETED, TaskStatus.FAILED] for task in self.tasks)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "type": self.type.value,
            "status": self.status.value,
            "tasks": [task.to_dict() for task in self.tasks],
            "context": self.context,
            "result": self.result.__dict__ if self.result else None,
            "error": self.error,
            "intent_id": self.intent_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Workflow":
        """Create Workflow from dictionary"""
        workflow = cls(
            id=data.get("id", str(uuid4())),
            type=WorkflowType(data["type"]),
            status=WorkflowStatus(data.get("status", "pending")),
            context=data.get("context", {}),
            error=data.get("error"),
            intent_id=data.get("intent_id"),
            created_at=datetime.fromisoformat(data.get("created_at", datetime.now().isoformat())),
            updated_at=datetime.fromisoformat(data.get("updated_at", datetime.now().isoformat())),
        )

        # Convert tasks
        for task_data in data.get("tasks", []):
            task = Task(
                id=task_data.get("id", str(uuid4())),
                name=task_data.get("name", ""),
                type=TaskType(task_data["type"]) if task_data.get("type") else None,
                status=TaskStatus(task_data.get("status", "pending")),
                result=task_data.get("result"),
                error=task_data.get("error"),
                created_at=datetime.fromisoformat(
                    task_data.get("created_at", datetime.now().isoformat())
                ),
            )
            workflow.tasks.append(task)

        # Convert result
        if data.get("result"):
            workflow.result = WorkflowResult(**data["result"])

        return workflow


# Events
@dataclass
class Event:
    """Base event class"""

    id: str = field(default_factory=lambda: str(uuid4()))
    type: str = ""
    data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class FeatureCreated(Event):
    """Feature was created"""

    type: str = "feature.created"
    feature_id: str = ""
    created_by: str = ""
    source: str = ""


@dataclass
class InsightGenerated(Event):
    """AI generated an insight"""

    type: str = "insight.generated"
    insight: str = ""
    confidence: float = 0.0
    sources: List[str] = field(default_factory=list)


@dataclass
class UploadedFile:
    """Domain model for uploaded files"""

    id: str = field(default_factory=lambda: str(uuid4()))
    owner_id: str = ""
    filename: str = ""
    file_type: str = ""  # MIME type
    file_size: int = 0
    storage_path: str = ""  # Where file is stored
    upload_time: datetime = field(default_factory=datetime.now)
    last_referenced: Optional[datetime] = None
    reference_count: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    file_metadata: Dict[str, Any] = field(default_factory=dict)


class AnalysisType(Enum):
    DATA = "data"
    DOCUMENT = "document"
    TEXT = "text"
    UNKNOWN = "unknown"


@dataclass
class ValidationResult:
    """Result of file security validation"""

    is_valid: bool
    message: str
    details: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FileTypeInfo:
    """File type detection results"""

    mime_type: str
    extension: str
    analyzer_type: str  # Will convert to AnalysisType enum later
    confidence: float = 0.0


@dataclass
class Document:
    """Core document entity for document memory system"""

    id: str = field(default_factory=lambda: str(uuid4()))
    title: str = ""
    content: str = ""
    document_type: str = "general"  # general, decision, meeting_notes, analysis

    # Document classification
    tags: List[str] = field(default_factory=list)
    topics: List[str] = field(default_factory=list)
    decisions: List[str] = field(default_factory=list)

    # File information
    file_path: Optional[str] = None
    file_size: Optional[int] = None
    mime_type: Optional[str] = None

    # Processing metadata
    summary: str = ""
    key_findings: List[str] = field(default_factory=list)
    analysis_metadata: Dict[str, Any] = field(default_factory=dict)

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to serializable dictionary"""
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,
            "document_type": self.document_type,
            "tags": self.tags,
            "topics": self.topics,
            "decisions": self.decisions,
            "file_path": self.file_path,
            "file_size": self.file_size,
            "mime_type": self.mime_type,
            "summary": self.summary,
            "key_findings": self.key_findings,
            "analysis_metadata": self.analysis_metadata,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Document":
        """Create from dictionary with type conversion"""
        # Convert ISO strings back to datetime objects
        data["created_at"] = datetime.fromisoformat(data["created_at"])
        data["updated_at"] = datetime.fromisoformat(data["updated_at"])
        data["last_accessed"] = datetime.fromisoformat(data["last_accessed"])
        return cls(**data)


class ArtifactSourceType(str, Enum):
    """What an Artifact is a projection of (#952). The discriminator that lets
    Artifact be the *unifying lens* over the existing MUX entities without
    flattening them — each origin type keeps its identity; its type-specific
    fields ride verbatim in ``Artifact.payload`` (lossless round-trip)."""

    DOCUMENT = "document"  # analyzed document (services.domain.models.Document)
    UPLOADED_FILE = "uploaded_file"  # on-disk file (UploadedFile)
    INSIGHT = "insight"  # composted learning (SurfaceableInsight)
    GENERATED = "generated"  # content generated in-conversation (e.g. saved chat output)


@dataclass
class Artifact:
    """Unifying lens over the MUX content entities (#952, Arch-ratified 2026-06-08).

    Artifact is NOT a fourth silo and NOT a flattening: a ``source_type``
    discriminator + a ``payload`` dict that preserves each origin type's
    type-specific fields verbatim make it the lossless *projection* of
    Document / UploadedFile / SurfaceableInsight (+ natively-generated content).
    Reuses the existing LifecycleState + OwnershipMetadata primitives.

    Round-trip invariant (tested): ``X == to_X(from_X(X))`` for each origin type.
    Full structural unification (re-backing the source repos onto Artifact) is
    deferred post-MVP, done incrementally via these converters — see
    docs/internal/architecture/current/artifact-model-design-952.md.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    content: str = ""  # inline content (generated) / projection of source content
    source_type: ArtifactSourceType = ArtifactSourceType.GENERATED
    lifecycle_state: Optional[LifecycleState] = None  # reuse the 8-state enum
    lifecycle_history: List[LifecycleTransition] = field(default_factory=list)
    owner_id: str = ""  # SEC ownership (matches #470 owner_id pattern)
    source_conversation_id: Optional[str] = None  # provenance
    mux_ownership: Optional[OwnershipMetadata] = None  # MUX epistemology (orthogonal)
    payload: Dict[str, Any] = field(default_factory=dict)  # type-specific fields, verbatim
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # ---- lossless round-trip converters (#952) ----
    # Additive: NO change to the source types/repos. payload carries every
    # source field not on Artifact's flat fields, so to_X reconstructs X exactly.

    @classmethod
    def from_document(cls, doc: "Document") -> "Artifact":
        return cls(
            id=doc.id,
            content=doc.content,
            source_type=ArtifactSourceType.DOCUMENT,
            created_at=doc.created_at,
            updated_at=doc.updated_at,
            payload={
                "title": doc.title,
                "document_type": doc.document_type,
                "tags": doc.tags,
                "topics": doc.topics,
                "decisions": doc.decisions,
                "file_path": doc.file_path,
                "file_size": doc.file_size,
                "mime_type": doc.mime_type,
                "summary": doc.summary,
                "key_findings": doc.key_findings,
                "analysis_metadata": doc.analysis_metadata,
                "last_accessed": doc.last_accessed,
            },
        )

    def to_document(self) -> "Document":
        p = self.payload
        return Document(
            id=self.id,
            title=p["title"],
            content=self.content,
            document_type=p["document_type"],
            tags=p["tags"],
            topics=p["topics"],
            decisions=p["decisions"],
            file_path=p["file_path"],
            file_size=p["file_size"],
            mime_type=p["mime_type"],
            summary=p["summary"],
            key_findings=p["key_findings"],
            analysis_metadata=p["analysis_metadata"],
            created_at=self.created_at,
            updated_at=self.updated_at,
            last_accessed=p["last_accessed"],
        )

    @classmethod
    def from_uploaded_file(cls, f: "UploadedFile") -> "Artifact":
        return cls(
            id=f.id,
            content="",  # file bytes live on disk (storage_path), not inline
            source_type=ArtifactSourceType.UPLOADED_FILE,
            owner_id=f.owner_id,
            created_at=f.upload_time,
            updated_at=f.upload_time,
            payload={
                "filename": f.filename,
                "file_type": f.file_type,
                "file_size": f.file_size,
                "storage_path": f.storage_path,
                "last_referenced": f.last_referenced,
                "reference_count": f.reference_count,
                "metadata": f.metadata,
                "file_metadata": f.file_metadata,
            },
        )

    def to_uploaded_file(self) -> "UploadedFile":
        p = self.payload
        return UploadedFile(
            id=self.id,
            owner_id=self.owner_id,
            filename=p["filename"],
            file_type=p["file_type"],
            file_size=p["file_size"],
            storage_path=p["storage_path"],
            upload_time=self.created_at,
            last_referenced=p["last_referenced"],
            reference_count=p["reference_count"],
            metadata=p["metadata"],
            file_metadata=p["file_metadata"],
        )

    @classmethod
    def from_insight(cls, ins: Any) -> "Artifact":
        """ins: SurfaceableInsight (duck-typed to avoid a circular import)."""
        learning = getattr(ins, "learning", None)
        return cls(
            id=ins.id,
            content=getattr(learning, "expression", "") if learning else "",
            source_type=ArtifactSourceType.INSIGHT,
            owner_id=ins.user_id,
            created_at=ins.created_at,
            updated_at=ins.created_at,
            payload={
                "object_id": ins.object_id,
                "learning": learning,
                "surfaced_count": ins.surfaced_count,
                "last_surfaced": ins.last_surfaced,
                "user_response": ins.user_response,
                "min_trust_stage": ins.min_trust_stage,
                "connected_insights": ins.connected_insights,
                "context_tags": ins.context_tags,
                "is_deleted": ins.is_deleted,
                "user_correction": ins.user_correction,
            },
        )

    def to_insight(self) -> Any:
        # Lazy import: composting_pipeline ↔ domain.models would otherwise cycle.
        from services.mux.composting_pipeline import SurfaceableInsight

        p = self.payload
        return SurfaceableInsight(
            id=self.id,
            object_id=p["object_id"],
            user_id=self.owner_id,
            created_at=self.created_at,
            learning=p["learning"],
            surfaced_count=p["surfaced_count"],
            last_surfaced=p["last_surfaced"],
            user_response=p["user_response"],
            min_trust_stage=p["min_trust_stage"],
            connected_insights=p["connected_insights"],
            context_tags=p["context_tags"],
            is_deleted=p["is_deleted"],
            user_correction=p["user_correction"],
        )


@dataclass(frozen=True)
class SessionActivity:
    """ADR-078 D1 (#1394) read-model — one external artifact a session created
    (an issue, a doc). Holds an external POINTER (``target_ref`` = 'owner/repo#107'),
    not content. Owner-scoping is enforced at ``SessionActivityRepository`` (the
    reader keys on ``owner_id`` by construction — D1a); this frozen record is what
    the B4 recall reader and B3 antecedent resolver consume."""

    id: str
    conversation_id: str
    owner_id: str
    action_type: str
    target_ref: str
    turn_id: Optional[str] = None
    target_title: Optional[str] = None
    created_at: Optional[datetime] = None


@dataclass
class DocumentSample:
    """Smart content sampling result"""

    content: str
    is_complete: bool
    sampling_method: str
    total_length: Optional[int] = None


@dataclass
class ContentSample:
    """Sample of file content for analysis"""

    text: str
    is_truncated: bool
    original_length: int
    sample_ranges: Optional[List[Tuple[int, int]]] = None


@dataclass
class AnalysisResult:
    """Results from file analysis"""

    file_id: str
    analysis_type: AnalysisType
    summary: str
    key_findings: List[str]
    metadata: Dict[str, Any]
    recommendations: List[str]
    generated_at: datetime
    filename: str = ""
    analysis_metadata: Dict[str, Any] = field(default_factory=dict)


# Document Summary Domain Models for JSON Mode
@dataclass
class SummarySection:
    """A section within a document summary"""

    heading: str
    points: List[str] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Generate clean markdown for this section"""
        if not self.points:
            return f"### {self.heading}\n\nNo items found.\n"

        markdown = f"### {self.heading}\n\n"
        for point in self.points:
            markdown += f"- {point}\n"
        markdown += "\n"
        return markdown


@dataclass
class DocumentSummary:
    """Structured document summary with clean markdown generation"""

    title: str
    document_type: str
    key_findings: List[str] = field(default_factory=list)
    sections: List[SummarySection] = field(default_factory=list)

    def to_markdown(self) -> str:
        """Generate clean, consistent markdown for the entire summary"""
        markdown = f"# {self.title}\n\n"
        markdown += f"**Document Type:** {self.document_type}\n\n"

        # Key findings section
        if self.key_findings:
            markdown += "## Key Findings\n\n"
            for finding in self.key_findings:
                markdown += f"- {finding}\n"
            markdown += "\n"

        # Additional sections
        for section in self.sections:
            markdown += section.to_markdown()

        return markdown

    def add_section(self, heading: str, points: List[str]) -> None:
        """Add a new section to the summary"""
        self.sections.append(SummarySection(heading=heading, points=points))

    def get_section(self, heading: str) -> Optional[SummarySection]:
        """Get a section by heading"""
        for section in self.sections:
            if section.heading == heading:
                return section
        return None


@dataclass
class ActionHumanization:
    """Cached human-readable version of technical action strings"""

    id: str = field(default_factory=lambda: str(uuid4()))
    action: str = ""  # e.g., "investigate_crash"
    category: Optional[str] = None  # e.g., "ANALYSIS"
    human_readable: str = ""  # e.g., "investigate a crash"
    created_at: datetime = field(default_factory=datetime.now)
    usage_count: int = 0
    last_used: Optional[datetime] = None


# Spatial Domain Models
# These models implement the spatial metaphor system using integer positions
# to maintain clean separation from external system identifiers


@dataclass
class SpatialEvent:
    """Spatial event within the spatial metaphor system"""

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

    def get_spatial_coordinates(self) -> Dict[str, int]:
        """Get spatial coordinates as integer positions"""
        coords = {
            "territory_position": self.territory_position,
            "room_position": self.room_position,
        }
        if self.path_position is not None:
            coords["path_position"] = self.path_position
        if self.object_position is not None:
            coords["object_position"] = self.object_position
        return coords


@dataclass
class SpatialObject:
    """Object placed within spatial environment"""

    id: str = field(default_factory=lambda: str(uuid4()))
    object_type: str = "text_message"  # text_message, file_document, code_block, etc.

    # Integer spatial positioning (pure domain)
    territory_position: int = 0
    room_position: int = 0
    path_position: Optional[int] = None
    object_position: Optional[int] = None

    # Object properties
    content: str = ""
    creator_id: str = ""
    size_category: str = "standard"  # minimal, standard, substantial, extensive

    # Spatial relationships
    attention_attractors: List[str] = field(default_factory=list)
    emotional_markers: List[str] = field(default_factory=list)
    connected_objects: List[str] = field(default_factory=list)

    # Context
    placement_time: Optional[datetime] = None
    last_interaction: Optional[datetime] = None
    interaction_count: int = 0

    def get_spatial_context(self) -> Dict[str, Any]:
        """Get spatial context for object interaction"""
        return {
            "object_type": self.object_type,
            "size_category": self.size_category,
            "attention_level": len(self.attention_attractors),
            "emotional_resonance": len(self.emotional_markers),
            "connections": len(self.connected_objects),
            "interaction_history": self.interaction_count,
            "spatial_coordinates": self.get_spatial_coordinates(),
        }

    def get_spatial_coordinates(self) -> Dict[str, int]:
        """Get spatial coordinates as integer positions"""
        coords = {
            "territory_position": self.territory_position,
            "room_position": self.room_position,
        }
        if self.path_position is not None:
            coords["path_position"] = self.path_position
        if self.object_position is not None:
            coords["object_position"] = self.object_position
        return coords


@dataclass
class SpatialContext:
    """Spatial context information for positioning"""

    # Integer spatial positioning (pure domain)
    territory_position: int = 0
    room_position: int = 0
    path_position: Optional[int] = None
    object_position: Optional[int] = None

    # Spatial characteristics
    attention_level: str = "medium"  # low, medium, high, urgent
    emotional_valence: str = "neutral"  # positive, negative, neutral
    navigation_intent: str = "monitor"  # respond, investigate, monitor, explore

    # External system mapping (via adapter)
    external_system: str = ""
    external_id: str = ""
    external_context: Dict[str, Any] = field(default_factory=dict)

    def get_spatial_coordinates(self) -> Dict[str, int]:
        """Get spatial coordinates as integer positions"""
        coords = {
            "territory_position": self.territory_position,
            "room_position": self.room_position,
        }
        if self.path_position is not None:
            coords["path_position"] = self.path_position
        if self.object_position is not None:
            coords["object_position"] = self.object_position
        return coords


@dataclass
class Place:
    """
    A window into an external source - where Piper observes FEDERATED data.

    Issue #684: MUX-NAV-PLACES
    ADR-045: Object Model (FEDERATED category - "Piper's Senses")
    ownership-metaphors.md: FEDERATED objects come from places with atmosphere

    Place represents Piper's view into external services like GitHub, Calendar, etc.
    Each Place has:
    - A type with distinct atmosphere (collaborative, temporal, reference)
    - Confidence level based on data freshness and completeness
    - Summary for inline display + details for expansion
    - Hardness for trust-gated visibility

    Experience language: "Over in {name}, I see..." (not "API returned...")

    Example:
        github_place = Place(
            id="gh-octocat-hello-world",
            place_type=PlaceType.ISSUE_TRACKING,
            name="octocat/hello-world repository",
            confidence=PlaceConfidence.HIGH,
            summary="I see 3 PRs waiting for review",
            source_url="https://github.com/octocat/hello-world",
            hardness=HardnessLevel.HARD,
        )
    """

    id: str
    place_type: PlaceType
    name: str  # Human-readable: "piper-morgan repository", "your calendar"
    confidence: PlaceConfidence
    summary: str  # Piper's perspective: "I see 3 PRs waiting"
    source_url: str  # Where to link for "visit source"
    hardness: HardnessLevel  # For trust-gated visibility

    # Optional detailed data
    details: Optional[Dict[str, Any]] = None
    last_fetched: Optional[datetime] = None

    # Ownership metadata (always FEDERATED for Places)
    ownership: OwnershipMetadata = field(
        default_factory=lambda: OwnershipMetadata(
            category=OwnershipCategory.FEDERATED,
            source="external",
            confidence=0.9,
        )
    )

    def is_stale(self, max_age_minutes: int = 5) -> bool:
        """Check if cached data is stale."""
        if not self.last_fetched:
            return True
        age = datetime.now(timezone.utc) - self.last_fetched
        return age.total_seconds() > (max_age_minutes * 60)

    def get_staleness_indicator(self) -> str:
        """Get human-readable staleness for UI."""
        if not self.last_fetched:
            return "unknown"
        age = datetime.now(timezone.utc) - self.last_fetched
        minutes = int(age.total_seconds() / 60)
        if minutes < 1:
            return "just now"
        if minutes < 5:
            return f"{minutes} min ago"
        if minutes < 60:
            return f"{minutes} minutes ago"
        hours = minutes // 60
        if hours < 24:
            return f"{hours} hour{'s' if hours > 1 else ''} ago"
        return "over a day ago"

    def narrate(self) -> str:
        """Generate consciousness-preserving narrative."""
        staleness = self.get_staleness_indicator()
        if staleness == "just now":
            return f"Over in {self.name}, {self.summary}"
        return f"Over in {self.name} ({staleness}), {self.summary}"

    @property
    def atmosphere(self) -> str:
        """Get atmospheric description for this place type."""
        atmospheres = {
            PlaceType.ISSUE_TRACKING: "collaborative, status-oriented",
            PlaceType.COMMUNICATION: "informal, conversational",
            PlaceType.TEMPORAL: "time-bounded, scheduled",
            PlaceType.DOCUMENTATION: "reference, authoritative",
        }
        return atmospheres.get(self.place_type, "unknown")


# PM-087 Ethics Domain Models
@dataclass
class EthicalDecision:
    """Domain model for ethics decisions"""

    decision_id: str = field(default_factory=lambda: str(uuid4()))
    boundary_type: str = ""
    violation_detected: bool = False
    explanation: str = ""
    audit_data: Dict[str, Any] = field(default_factory=dict)
    timestamp: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "decision_id": self.decision_id,
            "boundary_type": self.boundary_type,
            "violation_detected": self.violation_detected,
            "explanation": self.explanation,
            "audit_data": self.audit_data,
            "timestamp": self.timestamp.isoformat(),
            "session_id": self.session_id,
        }


@dataclass
class BoundaryViolation:
    """Domain model for boundary violations"""

    violation_id: str = field(default_factory=lambda: str(uuid4()))
    violation_type: str = ""
    context: str = ""
    session_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    severity: str = "medium"  # low, medium, high, critical
    audit_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class KnowledgeNode:
    """Domain model for knowledge graph nodes"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    node_type: NodeType = NodeType.CONCEPT
    description: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "node_type": self.node_type.value if self.node_type else None,
            "description": self.description,
            "metadata": self.metadata,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "session_id": self.session_id,
        }


@dataclass
class KnowledgeEdge:
    """Domain model for knowledge graph edges (Issue #278: CORE-KNOW-ENHANCE)"""

    id: str = field(default_factory=lambda: str(uuid4()))
    source_node_id: str = ""
    target_node_id: str = ""
    edge_type: EdgeType = EdgeType.REFERENCES
    weight: float = 1.0
    # Issue #278: Confidence weighting for relationship-based reasoning
    confidence: float = 1.0  # 0.0 to 1.0, strength of relationship
    usage_count: int = 0  # Reinforced with use
    metadata: Dict[str, Any] = field(default_factory=dict)
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_accessed: Optional[datetime] = None  # For confidence decay
    session_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "source_node_id": self.source_node_id,
            "target_node_id": self.target_node_id,
            "edge_type": self.edge_type.value if self.edge_type else None,
            "weight": self.weight,
            "confidence": self.confidence,
            "usage_count": self.usage_count,
            "metadata": self.metadata,
            "properties": self.properties,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "last_accessed": self.last_accessed.isoformat() if self.last_accessed else None,
            "session_id": self.session_id,
        }


# PM-081: Universal List Architecture
# Chief Architect's universal composition over specialization principle


@dataclass
class List:
    """Universal List model for ANY item type (todo, feature, bug, attendee)"""

    id: str = field(default_factory=lambda: str(uuid4()))
    name: str = ""
    description: str = ""
    item_type: str = "todo"  # todo, feature, bug, attendee, etc.
    list_type: str = "personal"  # personal, shared, project
    ordering_strategy: str = "manual"  # manual, due_date, priority, created
    color: Optional[str] = None  # Hex color for UI theming
    emoji: Optional[str] = None  # Emoji for visual identification
    is_archived: bool = False
    is_default: bool = False  # Default list for new items of this type

    # Metadata for PM-040 Knowledge Graph integration
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)

    # Project associations (many-to-many - L1 Sprint #477)
    project_ids: List[str] = field(default_factory=list)

    # Ownership and sharing (SEC-RBAC Phase 1.3 & 1.4 & 2)
    owner_id: Optional[str] = None
    shared_with: List[SharePermission] = field(default_factory=list)  # Array of {user_id, role}

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    # Performance optimization - cached counts (SEC-RBAC Phase 1)
    item_count: int = 0  # Total items in list (cached for performance)
    completed_count: int = 0  # Completed items in list (cached for performance)

    def get_user_role(self, user_id: str) -> Optional[ShareRole]:
        """Get user's role for this list (returns owner for owner, or role from shared_with)"""
        if self.owner_id == user_id:
            return None  # Owner has all permissions (represented as None/owner)

        for perm in self.shared_with:
            if perm.user_id == user_id:
                return perm.role

        return None

    def user_can_read(self, user_id: str) -> bool:
        """Check if user can read this list (any role can read)"""
        return self.owner_id == user_id or self.get_user_role(user_id) is not None

    def user_can_write(self, user_id: str) -> bool:
        """Check if user can modify this list (editor or admin can write)"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role in (ShareRole.EDITOR, ShareRole.ADMIN)

    def user_can_share(self, user_id: str) -> bool:
        """Check if user can share this list (only admin or owner)"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role == ShareRole.ADMIN

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "item_type": self.item_type,
            "list_type": self.list_type,
            "ordering_strategy": self.ordering_strategy,
            "color": self.color,
            "emoji": self.emoji,
            "is_archived": self.is_archived,
            "is_default": self.is_default,
            "metadata": self.metadata,
            "tags": self.tags,
            "project_ids": self.project_ids,
            "owner_id": self.owner_id,
            "shared_with": [perm.to_dict() for perm in self.shared_with],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "item_count": self.item_count,
            "completed_count": self.completed_count,
        }


@dataclass
class ListItem:
    """Universal ListItem relationship - polymorphic with item_type discriminator"""

    id: str = field(default_factory=lambda: str(uuid4()))
    list_id: str = ""
    item_id: str = ""
    item_type: str = "todo"  # todo, feature, bug, attendee, etc.
    position: int = 0  # Order within the list

    # Membership metadata
    added_at: datetime = field(default_factory=datetime.now)
    added_by: str = ""  # User who added item to this list

    # List-specific overrides (optional)
    list_priority: Optional[str] = None  # Override item's default priority
    list_due_date: Optional[datetime] = None  # Override item's default due date
    list_notes: str = ""  # List-specific notes

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "list_id": self.list_id,
            "item_id": self.item_id,
            "item_type": self.item_type,
            "position": self.position,
            "added_at": self.added_at.isoformat() if self.added_at else None,
            "added_by": self.added_by,
            "list_priority": self.list_priority,
            "list_due_date": self.list_due_date.isoformat() if self.list_due_date else None,
            "list_notes": self.list_notes,
        }


# PM-081: Refactored Todo to extend Item primitive (Phase 2)
@dataclass
class Todo(Item):
    """A todo is an Item that can be completed and has priority.

    Extends Item with todo-specific properties.
    Inherits from Item: id, text, position, list_id, created_at, updated_at

    Design Decision: Todo IS-A Item. This enables todos to use all
    generic Item operations (reordering, text updates) while adding
    todo-specific behavior (completion, priority).

    Examples:
        >>> todo = Todo(text="Review PR", priority="high")
        >>> assert isinstance(todo, Item)  # Todo IS-A Item
        >>> assert todo.text == "Review PR"
        >>> todo.complete()  # Todo-specific method
        >>> assert todo.completed is True
    """

    # Inherited from Item (do NOT redefine):
    # - id: str
    # - text: str (was 'title')
    # - position: int
    # - list_id: Optional[str]
    # - created_at: datetime
    # - updated_at: datetime

    # Todo-specific fields (matching TodoDB):
    # Core fields
    description: str = ""
    priority: str = "medium"  # low, medium, high, urgent
    status: str = "pending"  # pending, in_progress, completed, cancelled
    completed: bool = False

    # Hierarchical structure
    parent_id: Optional[str] = None

    # Scheduling
    due_date: Optional[datetime] = None
    reminder_date: Optional[datetime] = None
    scheduled_date: Optional[datetime] = None

    # Context and categorization
    tags: List[str] = field(default_factory=list)
    project_id: Optional[str] = None
    context: Optional[str] = None  # @home, @work, etc.

    # Progress tracking
    estimated_minutes: Optional[int] = None
    actual_minutes: Optional[int] = None
    completion_notes: str = ""

    # PM-040 Knowledge Graph integration
    metadata: Dict[str, Any] = field(default_factory=dict)
    knowledge_node_id: Optional[str] = None
    related_todos: List[str] = field(default_factory=list)

    # PM-034 Intent Classification integration
    creation_intent: Optional[str] = None
    intent_confidence: Optional[float] = None

    # External integrations
    external_refs: Dict[str, Any] = field(default_factory=dict)

    # Timestamps
    completed_at: Optional[datetime] = None

    # Ownership and sharing (SEC-RBAC Phase 1.3 & 1.4 & 2)
    owner_id: Optional[str] = None
    shared_with: List[SharePermission] = field(default_factory=list)  # Array of {user_id, role}
    assigned_to: Optional[str] = None

    # MUX Ownership (#435) - Piper's relationship to this object
    # Todos are NATIVE - created within Piper's domain
    mux_ownership: Optional[OwnershipMetadata] = None

    # MUX Lifecycle Integration (#708) - optional, for todos that warrant lifecycle treatment
    # Follows "Lifecycle Optionality" principle: simple status + optional lifecycle_state
    lifecycle_state: Optional[LifecycleState] = None

    def get_user_role(self, user_id: str) -> Optional[ShareRole]:
        """Get user's role for this todo (returns owner for owner, or role from shared_with)"""
        if self.owner_id == user_id:
            return None  # Owner has all permissions (represented as None/owner)

        for perm in self.shared_with:
            if perm.user_id == user_id:
                return perm.role

        return None

    def user_can_read(self, user_id: str) -> bool:
        """Check if user can read this todo (any role can read)"""
        return self.owner_id == user_id or self.get_user_role(user_id) is not None

    def user_can_write(self, user_id: str) -> bool:
        """Check if user can modify this todo (editor or admin can write)"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role in (ShareRole.EDITOR, ShareRole.ADMIN)

    def user_can_share(self, user_id: str) -> bool:
        """Check if user can share this todo (only admin or owner)"""
        if self.owner_id == user_id:
            return True
        role = self.get_user_role(user_id)
        return role == ShareRole.ADMIN

    @property
    def title(self) -> str:
        """Backward compatibility: title maps to text.

        DEPRECATED: Use .text instead.
        This property exists for backward compatibility during migration.
        """
        return self.text

    @title.setter
    def title(self, value: str):
        """Backward compatibility: setting title sets text."""
        self.text = value

    def complete(self):
        """Mark todo as complete."""
        self.completed = True
        self.completed_at = datetime.now()
        self.status = "completed"
        self.updated_at = datetime.now()

    def reopen(self):
        """Reopen completed todo."""
        self.completed = False
        self.completed_at = None
        self.status = "pending"
        self.updated_at = datetime.now()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization.

        Includes lifecycle_state when present (#708 MUX-LIFECYCLE-UI-TODOS).
        """
        result = {
            # Inherited from Item
            "id": self.id,
            "text": self.text,
            "title": self.title,  # Backward compatibility
            "position": self.position,
            "list_id": self.list_id,
            # Core Todo fields
            "description": self.description,
            "priority": self.priority,
            "status": self.status,
            "completed": self.completed,
            # Hierarchical structure
            "parent_id": self.parent_id,
            # Scheduling
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "reminder_date": self.reminder_date.isoformat() if self.reminder_date else None,
            "scheduled_date": self.scheduled_date.isoformat() if self.scheduled_date else None,
            # Context and categorization
            "tags": self.tags,
            "project_id": self.project_id,
            "context": self.context,
            # Progress tracking
            "estimated_minutes": self.estimated_minutes,
            "actual_minutes": self.actual_minutes,
            "completion_notes": self.completion_notes,
            # Knowledge Graph integration
            "metadata": self.metadata,
            "knowledge_node_id": self.knowledge_node_id,
            "related_todos": self.related_todos,
            # Intent Classification integration
            "creation_intent": self.creation_intent,
            "intent_confidence": self.intent_confidence,
            # External integrations
            "external_refs": self.external_refs,
            # Timestamps
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            # Ownership and sharing
            "owner_id": self.owner_id,
            "shared_with": [perm.to_dict() for perm in self.shared_with],
            "assigned_to": self.assigned_to,
            # MUX Ownership (#435)
            "mux_ownership": self.mux_ownership.to_dict() if self.mux_ownership else None,
        }
        # Include lifecycle state if present (#708 MUX-LIFECYCLE-UI-TODOS)
        if self.lifecycle_state is not None:
            result["lifecycle_state"] = self.lifecycle_state.value
        return result


# PM-081: Backward compatibility - TodoList as alias for List(item_type='todo')
@dataclass
class TodoList:
    """Backward compatibility alias for List(item_type='todo')"""

    def __init__(self, **kwargs):
        # Convert TodoList to universal List with item_type='todo'
        list_data = {**kwargs, "item_type": "todo"}
        self._list = List(**list_data)

    def __getattr__(self, name):
        """Delegate to underlying List object"""
        return getattr(self._list, name)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return self._list.to_dict()


# PM-081: Backward compatibility - ListMembership as alias for ListItem(item_type='todo')
@dataclass
class ListMembership:
    """Backward compatibility alias for ListItem(item_type='todo')"""

    def __init__(self, **kwargs):
        # Convert ListMembership to universal ListItem with item_type='todo'
        item_data = {**kwargs, "item_type": "todo"}
        self._list_item = ListItem(**item_data)

    def __getattr__(self, name):
        """Delegate to underlying ListItem object"""
        return getattr(self._list_item, name)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return self._list_item.to_dict()


# PM-034 Phase 1: Conversation Foundation Domain Models
@dataclass
class Conversation:
    """Domain model for conversational interactions"""

    id: str = field(default_factory=lambda: str(uuid4()))
    user_id: UUID = ""
    session_id: str = ""
    title: str = ""  # Optional conversation title/summary
    context: Dict[str, Any] = field(default_factory=dict)  # Conversation context
    is_active: bool = True  # DEPRECATED — use lifecycle_state (#715)

    # Lifecycle (#715, spec #858)
    lifecycle_state: ConversationLifecycleState = ConversationLifecycleState.ACTIVE
    archived_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    last_activity_at: Optional[datetime] = None

    # MUX Ownership (#435) - Conversations are NATIVE (Piper creates/manages them)
    mux_ownership: Optional[OwnershipMetadata] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "session_id": self.session_id,
            "title": self.title,
            "context": self.context,
            "is_active": self.is_active,
            "lifecycle_state": self.lifecycle_state.value if self.lifecycle_state else "active",
            "archived_at": self.archived_at.isoformat() if self.archived_at else None,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "last_activity_at": (
                self.last_activity_at.isoformat() if self.last_activity_at else None
            ),
            "mux_ownership": self.mux_ownership.to_dict() if self.mux_ownership else None,
        }


@dataclass
class ConversationTurn:
    """Domain model for individual turns in a conversation"""

    id: str = field(default_factory=lambda: str(uuid4()))
    conversation_id: str = ""
    turn_number: int = 0  # Sequential turn number within conversation

    # Turn content
    user_message: str = ""
    assistant_response: str = ""
    intent: Optional[str] = None  # Classified intent for this turn

    # Context and entities
    entities: List[str] = field(default_factory=list)  # Extracted entities
    references: Dict[str, str] = field(default_factory=dict)  # Anaphoric references
    context_used: Dict[str, Any] = field(default_factory=dict)  # Context used in response

    # Metadata
    metadata: Dict[str, Any] = field(default_factory=dict)
    processing_time: Optional[float] = None  # Response processing time in ms

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "conversation_id": self.conversation_id,
            "turn_number": self.turn_number,
            "user_message": self.user_message,
            "assistant_response": self.assistant_response,
            "intent": self.intent,
            "entities": self.entities,
            "references": self.references,
            "context_used": self.context_used,
            "metadata": self.metadata,
            "processing_time": self.processing_time,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class StandupItem:
    """A single standup line item.

    Carries structured per-item data so consumers (notably the standup.html
    template via #704) can read `lifecycle_state` when present. Pre-#1034
    these were pre-formatted strings (`f"✅ {commit.message}"`); structured
    items preserve the same display while exposing the underlying source +
    lifecycle metadata.

    Per PM #1034 audit dispositions (May 3):
    - Q1 Option 1: replaces string lists; canonical/slack/JSON formatters
      migrate to read `item.display`.
    - Q3 Option B: emoji stays as data field on the dict (single source of
      truth in the pipeline; presentation layers render `item.icon` +
      `item.display`).

    Per #900 Phase 2 (May 5, 2026): moved from
    `services/features/morning_standup.py` to `services/domain/models.py`
    so 3-part collection in `services/standup/` can use it without
    pulling features-layer imports. Re-exported from the original
    location for back-compat.
    """

    display: str
    source: str = ""  # "commit" | "work" | "active_repo" | "yesterday_context" | "system"
    lifecycle_state: Optional[str] = None
    icon: str = ""
    # Optional short context line (e.g. "hasn't moved in 5 days", a calendar time).
    # Mirrors RadarEntity.meta; populated for derived items (#1269). Defaults empty so
    # existing constructors / standup.html (which reads display/icon/lifecycle_state)
    # are unaffected. New field is LAST → positional construction stays valid.
    meta: str = ""

    def __str__(self) -> str:
        """Legacy rendering: `f"{icon} {display}"` matches pre-#1034 format."""
        if self.icon:
            return f"{self.icon} {self.display}"
        return self.display

    def to_dict(self) -> Dict[str, Any]:
        """API-friendly serialization."""
        return {
            "display": self.display,
            "source": self.source,
            "lifecycle_state": self.lifecycle_state,
            "icon": self.icon,
            "meta": self.meta,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StandupItem":
        """Reconstruct from a serialized dict (round-trip with to_dict)."""
        return cls(
            display=data.get("display", ""),
            source=data.get("source", ""),
            lifecycle_state=data.get("lifecycle_state"),
            icon=data.get("icon", ""),
            meta=data.get("meta", ""),
        )


@dataclass
class StandupPartialCapture:
    """Three-part standup capture: yesterday / today / blockers.

    Issue #900 Phase 2 (May 5, 2026). Holds the structured 3-part
    collection state for an in-flight standup. Persisted alongside the
    `StandupConversation` so escape/timeout → resume preserves what's
    already been captured.

    The shape is intentionally flat lists of `StandupItem` rather than
    free-form text — Phase 5's LLM generation reads this structure
    directly (#1034-aware), and the per-item structure preserves source
    + lifecycle metadata when items come from connected integrations
    (e.g., GitHub commits captured into `today` automatically).
    """

    yesterday: List[StandupItem] = field(default_factory=list)
    today: List[StandupItem] = field(default_factory=list)
    blockers: List[StandupItem] = field(default_factory=list)

    def is_empty(self) -> bool:
        """True if no part has any items captured."""
        return not (self.yesterday or self.today or self.blockers)

    def is_complete(self) -> bool:
        """True if at least one part has items captured.

        Used by the completion-detection logic (Phase 3) to decide
        whether the user's "I'm done" signals should advance to
        GENERATING. Distinct from "all 3 parts non-empty" because users
        legitimately have nothing to report in some categories.
        """
        return not self.is_empty()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "yesterday": [it.to_dict() for it in self.yesterday],
            "today": [it.to_dict() for it in self.today],
            "blockers": [it.to_dict() for it in self.blockers],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "StandupPartialCapture":
        return cls(
            yesterday=[StandupItem.from_dict(d) for d in data.get("yesterday", [])],
            today=[StandupItem.from_dict(d) for d in data.get("today", [])],
            blockers=[StandupItem.from_dict(d) for d in data.get("blockers", [])],
        )


@dataclass
class StandupSummary:
    """Derived standup read-model (#1269) — Piper's *derived view* over the observed
    entity catalog (Conversations / Documents / WorkItems via the Radar EntitySources),
    assembled by ``services.standup.assembler.StandupAssembler``.

    Deliberately distinct from ``StandupPartialCapture`` (above), which is the
    *interactive-capture write-state* — what the user typed, persisted alongside a
    ``StandupConversation`` for escape/resume. This is the *read-side*: what Piper
    derived from observed data. Same three-slot shape, different provenance and
    lifecycle (cf. CQRS read-model vs. write-model) — so it is its own type, not an
    overload of the capture state. Carries the narrative rendering (``to_prose()``,
    #1269 P3).

    Reuses ``StandupItem`` so derived items render through the same ``standup.html``
    path (#704); each item's ``source`` is tagged ``radar:{type}`` so the surface can
    tell derived-from-observed items apart from captured / commit items.
    """

    yesterday: List["StandupItem"] = field(default_factory=list)
    today: List["StandupItem"] = field(default_factory=list)
    # "Watch" not "Blockers" (CXO #1269): these are Piper-INFERRED potential blockers
    # (confirmed-blocked + staleness signals), lower-confidence than the user-DECLARED
    # blockers in StandupPartialCapture. Calling them "blockers" would overstate Piper's
    # confidence. Within the slot: confirmed-blocked first, then stale ("hasn't moved…").
    watch: List["StandupItem"] = field(default_factory=list)

    def is_empty(self) -> bool:
        """True if no slot has any derived item. Honest empty — the surface renders
        this gracefully ("nothing yet"), never a fabricated "all clear"."""
        return not (self.yesterday or self.today or self.watch)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "yesterday": [it.to_dict() for it in self.yesterday],
            "today": [it.to_dict() for it in self.today],
            "watch": [it.to_dict() for it in self.watch],
        }

    # --- prose rendering (#1269 P3, CXO experience design) ---

    # verb by the derived item's coarse lifecycle label (yesterday slot).
    _YESTERDAY_VERBS = {"closed": "closed", "new": "updated", "active": "discussed"}

    # #1269 PM UAT: cap how many items are read out loud per slot (the lists arrive
    # attention-sorted from the assembler, so the first N are the highest-signal);
    # the remainder is summarized as "N more" rather than enumerated inline.
    _PROSE_ITEM_CAP = 4

    @staticmethod
    def _oxford(parts: List[str]) -> str:
        """Oxford-comma join: [] → ""; [a] → "a"; [a,b] → "a and b"; [a,b,c] → "a, b, and c"."""
        parts = [p for p in parts if p]
        if not parts:
            return ""
        if len(parts) == 1:
            return parts[0]
        if len(parts) == 2:
            return f"{parts[0]} and {parts[1]}"
        return ", ".join(parts[:-1]) + f", and {parts[-1]}"

    @classmethod
    def _quoted(cls, names: List[str]) -> str:
        return cls._oxford([f'"{n}"' for n in names])

    @classmethod
    def _quoted_capped(cls, names: List[str], cap: int = _PROSE_ITEM_CAP) -> str:
        """Quote + oxford-join, capping the enumeration at ``cap`` items and
        summarizing the rest as "N more" (#1269 PM UAT: don't read ~18 items out
        loud). Callers pass attention-ordered lists, so the kept items are the
        highest-signal ones."""
        names = [n for n in names if n]
        if len(names) <= cap:
            return cls._quoted(names)
        shown = [f'"{n}"' for n in names[:cap]]
        return cls._oxford(shown + [f"{len(names) - cap} more"])

    def _yesterday_prose(self) -> str:
        if not self.yesterday:
            return ""
        groups: List[Any] = []  # [(verb, [displays])], order-preserving
        for it in self.yesterday:
            verb = self._YESTERDAY_VERBS.get((it.lifecycle_state or "").lower(), "worked on")
            if groups and groups[-1][0] == verb:
                groups[-1][1].append(it.display)
            else:
                groups.append((verb, [it.display]))
        phrases = [f"{verb} {self._quoted_capped(names)}" for verb, names in groups]
        return "You " + self._oxford(phrases) + "."

    def _today_prose(self) -> str:
        if not self.today:
            return ""
        # Work items render as "You're working on …"; calendar events render as a
        # separate "You have X at <time>." sentence (CXO #1269: calendar makes today real).
        work = [it.display for it in self.today if it.source != "calendar"]
        events = [it for it in self.today if it.source == "calendar"]
        sentences: List[str] = []
        if work:
            sentences.append("You're working on " + self._quoted_capped(work) + ".")
        if events:
            evs = [
                f'"{it.display}" at {it.meta}' if it.meta else f'"{it.display}"' for it in events
            ]
            sentences.append("You have " + self._oxford(evs) + ".")
        return " ".join(sentences)

    def _watch_prose(self) -> str:
        if not self.watch:
            return ""
        shown = self.watch[: self._PROSE_ITEM_CAP]
        parts: List[str] = []
        for it in shown:
            if (it.lifecycle_state or "").lower() == "blocked":
                parts.append(f'"{it.display}" is blocked.')
            else:
                detail = it.meta or "hasn't moved recently"
                parts.append(f'"{it.display}" {detail}.')
        rest = len(self.watch) - len(shown)
        if rest:
            parts.append(f"Plus {rest} more flagged to watch.")
        return " ".join(parts)

    def to_prose(self) -> str:
        """Render an honest spoken-standup narrative (CXO #1269: "say it out loud", the
        actual things not counts; empty = empty, no filler / fallback copy).

        Deterministic baseline — the floor, no LLM dependency; a richer LLM-polished
        rendering can layer on at the surface / chat skill (#1269 P4/P5).
        """
        if self.is_empty():
            return (
                "Nothing to show yet — as you work in connected tools (GitHub, docs, "
                "chats), your standup fills in here."
            )
        sections = [
            (
                "**Yesterday** — what got done",
                self._yesterday_prose(),
                "No completions yesterday — looks like you were in planning mode.",
            ),
            (
                "**Today** — what's active",
                self._today_prose(),
                "Nothing in progress right now.",
            ),
            (
                "**Watch** — what might be stuck",
                self._watch_prose(),
                "Nothing flagged as stuck.",
            ),
        ]
        # Each heading + body is its own markdown block, separated by a blank
        # line (#1269 PM UAT: a single "\n" is a markdown SOFT break — it renders
        # as a space, fusing heading into body as a run-on. "\n\n" forces real
        # paragraph blocks so marked.js renders distinct sections).
        return "\n\n".join(
            f"{heading}\n\n{body or empty_msg}" for heading, body, empty_msg in sections
        )


@dataclass
class StandupConversation:
    """
    Domain model for interactive standup conversations.

    Issue #552: STANDUP-CONV-STATE - Conversation State Management
    Epic #242: CONV-MCP-STANDUP-INTERACTIVE

    Wraps conversation context with standup-specific state machine and preferences.
    Follows composition pattern (Option C from gameplan).

    Issue #900 Phase 2 (May 5, 2026): Added `partial_capture`
    (`StandupPartialCapture`) for the structured 3-part collection flow
    (yesterday/today/blockers). Persists across escape/resume per Phase 4.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str = ""
    user_id: str = ""

    # State machine
    state: StandupConversationState = StandupConversationState.INITIATED
    previous_state: Optional[StandupConversationState] = None

    # User preferences for this standup
    # Examples: {"focus": "github", "exclude": ["docs"], "format": "brief"}
    preferences: Dict[str, Any] = field(default_factory=dict)

    # Generated content (evolves through refinement)
    current_standup: Optional[str] = None
    standup_versions: List[str] = field(default_factory=list)  # Version history

    # Conversation turns (standup-specific)
    turns: List[ConversationTurn] = field(default_factory=list)

    # Context from integrations
    # Examples: {"github_activity": [...], "calendar_events": [...]}
    context: Dict[str, Any] = field(default_factory=dict)

    # Issue #900 Phase 2: 3-part structured collection
    partial_capture: StandupPartialCapture = field(default_factory=StandupPartialCapture)

    # Timestamps
    # #1079: tz-aware UTC defaults so in-memory timestamps match the DB-issued
    # (TIMESTAMP WITH TIME ZONE) values and never produce naive-vs-aware
    # subtraction crashes downstream (e.g. transition-duration / timeout math).
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "state": self.state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "preferences": self.preferences,
            "current_standup": self.current_standup,
            "standup_versions": self.standup_versions,
            "turns": [t.to_dict() for t in self.turns],
            "context": self.context,
            "partial_capture": self.partial_capture.to_dict(),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


@dataclass
class PortfolioOnboardingSession:
    """
    Domain model for portfolio onboarding conversations.

    Issue #490: FTUX-PORTFOLIO - Project Portfolio Onboarding
    Epic: FTUX (First Time User Experience)

    Tracks multi-turn conversation for capturing user's project portfolio.
    Simpler than StandupConversation - focused on project capture.
    """

    id: str = field(default_factory=lambda: str(uuid4()))
    session_id: str = ""
    user_id: str = ""

    # State machine
    state: PortfolioOnboardingState = PortfolioOnboardingState.INITIATED
    previous_state: Optional[PortfolioOnboardingState] = None

    # Captured project info
    # List of dicts: [{"name": "HealthTrack", "description": "Fitness app", "repo": "owner/repo"}]
    captured_projects: List[Dict[str, Any]] = field(default_factory=list)

    # Repo-linking iteration index (Issue #863)
    repo_project_index: int = 0

    # Conversation turns
    turns: List[ConversationTurn] = field(default_factory=list)

    # Timestamps
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "id": self.id,
            "session_id": self.session_id,
            "user_id": self.user_id,
            "state": self.state.value,
            "previous_state": self.previous_state.value if self.previous_state else None,
            "captured_projects": self.captured_projects,
            "repo_project_index": self.repo_project_index,
            "turns": [t.to_dict() for t in self.turns],
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


# =============================================================================
# TRUST COMPUTATION - ADR-053: Trust Computation Architecture
# =============================================================================


@dataclass
class TrustEvent:
    """
    Individual interaction that affects trust computation.

    Issue #647: TRUST-LEVELS-1 - Core Infrastructure
    ADR-053: Trust Computation Architecture

    Records a single interaction outcome for trust tracking and discussability.
    When users ask "why did you do that?", these events provide context.
    """

    event_id: UUID
    timestamp: datetime
    outcome: str  # "successful", "neutral", "negative"
    context: str  # Brief description for discussability
    stage_at_time: TrustStage

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization."""
        return {
            "event_id": str(self.event_id),
            "timestamp": self.timestamp.isoformat(),
            "outcome": self.outcome,
            "context": self.context,
            "stage_at_time": self.stage_at_time.value,
        }


@dataclass
class UserTrustProfile:
    """
    Persisted trust state for a user.

    Issue #647: TRUST-LEVELS-1 - Core Infrastructure
    ADR-053: Trust Computation Architecture
    PDR-002: Conversational Glue

    Tracks user's progression through trust stages, enabling Piper to
    calibrate proactivity appropriately. Trust is invisible to users
    but its effects are noticeable through behavior changes.

    Key behaviors by stage:
    - NEW (1): Respond to queries only; no unsolicited help
    - BUILDING (2): Offer related capabilities after task completion
    - ESTABLISHED (3): Proactive suggestions based on observed context
    - TRUSTED (4): Anticipate needs; "I'll do X unless you stop me"
    """

    user_id: UUID
    current_stage: TrustStage = TrustStage.NEW

    # Counters for stage progression
    # CALIBRATION: Thresholds (10 for 1→2, 50 for 2→3) are starting points
    successful_count: int = 0
    neutral_count: int = 0
    negative_count: int = 0
    consecutive_negative: int = 0

    # History for discussability (bounded, not infinite)
    recent_events: List[TrustEvent] = field(default_factory=list)
    max_recent_events: int = 50

    # Stage progression tracking
    # List of (timestamp, new_stage, reason) tuples
    stage_history: List[Tuple[datetime, TrustStage, str]] = field(default_factory=list)
    highest_stage_achieved: TrustStage = TrustStage.NEW

    # Timestamps
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_interaction_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_stage_change_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for serialization."""
        return {
            "user_id": str(self.user_id),
            "current_stage": self.current_stage.value,
            "successful_count": self.successful_count,
            "neutral_count": self.neutral_count,
            "negative_count": self.negative_count,
            "consecutive_negative": self.consecutive_negative,
            "recent_events": [
                {
                    "event_id": str(e.event_id),
                    "timestamp": e.timestamp.isoformat(),
                    "outcome": e.outcome,
                    "context": e.context,
                    "stage_at_time": e.stage_at_time.value,
                }
                for e in self.recent_events
            ],
            "max_recent_events": self.max_recent_events,
            "stage_history": [
                {
                    "timestamp": ts.isoformat(),
                    "stage": stage.value,
                    "reason": reason,
                }
                for ts, stage, reason in self.stage_history
            ],
            "highest_stage_achieved": self.highest_stage_achieved.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "last_interaction_at": (
                self.last_interaction_at.isoformat() if self.last_interaction_at else None
            ),
            "last_stage_change_at": (
                self.last_stage_change_at.isoformat() if self.last_stage_change_at else None
            ),
        }
