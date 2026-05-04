"""
Database Models
SQLAlchemy models for persistent storage
"""

import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    ForeignKeyConstraint,
    Index,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import relationship

import services.domain.models as domain
from services.mux.lifecycle import LifecycleState
from services.shared_types import (
    EdgeType,
    IntegrationType,
    IntentCategory,
    ListType,
    NodeType,
    OrderingStrategy,
    PatternType,
    TaskStatus,
    TaskType,
    TodoPriority,
    TodoStatus,
    TrustStage,
    WorkflowStatus,
    WorkflowType,
)

from .connection import Base


class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps to models"""

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )


class User(Base):
    """
    User account model.

    Unified user table for all users (production and alpha).
    Alpha users migrated from alpha_users table with is_alpha=true.

    Issue #228 CORE-USERS-API
    Issue #262 CORE-USER-ID-MIGRATION (UUID conversion complete)
    """

    __tablename__ = "users"

    # Primary key - UUID (migrated from VARCHAR in Issue #262)
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # Authentication fields
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(500), nullable=True)  # For future password auth
    role = Column(String(50), default="user", nullable=False)

    # Status flags
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_alpha = Column(Boolean, default=False, nullable=False)  # Issue #262 - alpha user flag
    is_admin = Column(Boolean, default=False, nullable=False)  # Issue #357 - SEC-RBAC admin bypass

    # Setup tracking (Issue #389)
    setup_complete = Column(Boolean, default=False, nullable=False)
    setup_completed_at = Column(DateTime(timezone=True), nullable=True)  # When setup was completed

    # Orientation tracking (Issue #549)
    orientation_seen = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    last_login_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships (Issue #262/#291 - FK constraints restored with UUID)
    personality_profiles = relationship(
        "PersonalityProfileModel", back_populates="user", lazy="select"
    )
    api_keys = relationship(
        "UserAPIKey", back_populates="user", cascade="all, delete-orphan", lazy="select"
    )
    blacklisted_tokens = relationship(
        "TokenBlacklist", back_populates="user", cascade="all, delete-orphan", lazy="select"
    )  # Issue #291 - FK restored
    feedback = relationship("FeedbackDB", back_populates="user", lazy="select")
    learned_patterns = relationship(
        "LearnedPattern", back_populates="user", cascade="all, delete-orphan", lazy="select"
    )  # Issue #300 - Learning system
    learning_settings = relationship(
        "LearningSettings",
        back_populates="user",
        cascade="all, delete-orphan",
        lazy="select",
        uselist=False,  # One-to-one relationship
    )  # Issue #300 - Learning settings
    # NOTE: AuditLog relationship still disabled (audit_logs.user_id has no FK constraint)
    # audit_logs = relationship("AuditLog", back_populates="user", lazy="select")

    # Indexes
    __table_args__ = (
        Index("idx_users_username", "username", unique=True),
        Index("idx_users_email", "email", unique=True),
        Index("idx_users_active", "is_active"),
    )

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, active={self.is_active})>"


# NOTE: AlphaUser model removed in Issue #262
# Alpha users merged into User table with is_alpha=true flag
# Table dropped, data migrated to users table


class UserAPIKey(Base):
    """
    User-specific API keys stored securely in OS keychain.

    This model stores metadata about keys; actual keys are in OS keychain
    with references using format: "piper_{user_id}_{provider}"

    Issue #228 CORE-USERS-API Phase 1B
    Issue #262 - UUID migration complete
    """

    __tablename__ = "user_api_keys"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(
        postgresql.UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )  # Issue #262 - FK restored with UUID
    provider = Column(String(50), nullable=False)  # openai, anthropic, github, etc
    key_reference = Column(String(500), nullable=False)  # keychain identifier

    # Key metadata
    is_active = Column(Boolean, default=True, nullable=False)
    is_validated = Column(Boolean, default=False)
    last_validated_at = Column(DateTime(timezone=True), nullable=True)

    # Audit fields
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    created_by = Column(String(255), nullable=True)

    # Rotation support
    previous_key_reference = Column(String(500), nullable=True)
    rotated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships (Issue #262 - restored with UUID)
    user = relationship("User", back_populates="api_keys")

    # Constraints
    __table_args__ = (
        UniqueConstraint("user_id", "provider", name="uq_user_provider"),
        Index("idx_user_api_keys_user_id", "user_id"),
        Index("idx_user_api_keys_provider", "provider"),
        Index("idx_user_api_keys_active", "is_active"),
    )

    def __repr__(self):
        return f"<UserAPIKey(user_id={self.user_id}, provider={self.provider}, active={self.is_active})>"


class AuditLog(Base, TimestampMixin):
    """
    Comprehensive audit trail for security and compliance.

    Tracks all security-relevant events including:
    - Authentication (login, logout, token operations)
    - API key management (store, retrieve, delete, rotate)
    - Data modifications
    - Security events

    Issue #249 CORE-AUDIT-LOGGING
    Issue #262 - UUID migration complete (NO FK constraint - intentional)
    """

    __tablename__ = "audit_logs"

    # Identity (follow User model pattern - String primary key)
    id = Column(String(255), primary_key=True, default=lambda: str(uuid.uuid4()))
    # NOTE: FK intentionally NOT added - audit logs should persist even if user deleted
    # user_id stores UUID as string for reference only
    user_id = Column(postgresql.UUID(as_uuid=True), nullable=True, index=True)
    session_id = Column(String(255), nullable=True, index=True)

    # Event classification
    event_type = Column(String(50), nullable=False, index=True)  # auth, api_key, data, system
    action = Column(String(100), nullable=False, index=True)  # login, logout, store_key, etc
    resource_type = Column(String(50), nullable=True, index=True)  # user, api_key, token, etc
    resource_id = Column(String(255), nullable=True, index=True)  # Specific resource identifier

    # Event details
    status = Column(String(20), nullable=False, index=True)  # success, failed, error
    severity = Column(String(20), nullable=False, index=True)  # info, warning, error, critical
    message = Column(Text, nullable=False)  # Human-readable description
    details = Column(JSON, nullable=True)  # Additional structured data

    # Request context
    ip_address = Column(String(45), nullable=True, index=True)  # IPv4/IPv6 support
    user_agent = Column(String(500), nullable=True)  # Browser/client info
    request_id = Column(String(255), nullable=True, index=True)  # Request correlation
    request_path = Column(String(500), nullable=True)  # API endpoint called

    # Change tracking
    old_value = Column(JSON, nullable=True)  # Previous state
    new_value = Column(JSON, nullable=True)  # New state

    # Relationships
    # NOTE: Relationship to User disabled during alpha phase (Issue #259)
    # FK constraint removed to support alpha_users (UUID) - relationship requires explicit primaryjoin
    # user = relationship("User", back_populates="audit_logs")

    # Strategic indexes for query performance
    __table_args__ = (
        Index("idx_audit_user_date", "user_id", "created_at"),
        Index("idx_audit_event_type", "event_type"),
        Index("idx_audit_action", "action"),
        Index("idx_audit_resource", "resource_type", "resource_id"),
        Index("idx_audit_severity", "severity"),
        Index("idx_audit_status", "status"),
        Index("idx_audit_ip", "ip_address"),
        Index("idx_audit_session", "session_id"),
        Index("idx_audit_request", "request_id"),
    )

    def __repr__(self):
        return (
            f"<AuditLog(id={self.id}, event_type={self.event_type}, "
            f"action={self.action}, user_id={self.user_id}, status={self.status})>"
        )


class EthicsAuditLogDB(Base, TimestampMixin):
    """
    Durable storage for ethics-decision audit entries.

    Maps directly from `services.ethics.audit_transparency.AuditLogEntry`.
    Replaces the in-memory list (max 10K, lost on restart) with PostgreSQL
    persistence so transparency endpoints can honor their durability claim
    across deploys/crashes.

    Issue #1018 (Phase 2 implementation per ratified Phase 1 design).
    Sibling to `AuditLog` above — that table is for security/auth events
    (Issue #249); this one is for ethics-decision events. Separate
    schemas, separate access patterns, separate retention.
    """

    __tablename__ = "ethics_audit_log"

    # Identity — string PK matches existing audit_logs precedent + the
    # pre-#1018 in-memory entry_id format (uuid for new entries; legacy
    # `audit_{unix_ts}` format also fits).
    entry_id = Column(String(64), primary_key=True)

    # Event classification — current shipped values: "ethics_decision",
    # "boundary_violation". Indexed for system-summary queries.
    event_type = Column(String(50), nullable=False, index=True)

    # Event time (decision timestamp; may differ from created_at insertion time)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)

    # Per-session and per-user references. No FK to users — audit must
    # survive user deletion, matches AuditLog precedent above.
    session_id = Column(String(255), nullable=True, index=True)
    user_id = Column(postgresql.UUID(as_uuid=True), nullable=True, index=True)

    # Redacted detail payload. JSONB for query/index support.
    details = Column(postgresql.JSONB, nullable=False, default=dict)

    # Whether redaction was applied (matches in-memory AuditLogEntry.redacted).
    redacted = Column(Boolean, nullable=False, default=True)

    # Strategic indexes matching audit_transparency.py query patterns:
    #   - get_user_audit_log(session_id) → idx_ethics_audit_session
    #   - get_system_audit_summary(days, group by event_type) → idx_ethics_audit_event_time
    #   - retention sweep delete_older_than(timestamp) → idx_ethics_audit_timestamp
    __table_args__ = (
        Index("idx_ethics_audit_user_time", "user_id", "timestamp"),
        Index("idx_ethics_audit_event_time", "event_type", "timestamp"),
    )

    def __repr__(self):
        return (
            f"<EthicsAuditLogDB(entry_id={self.entry_id}, "
            f"event_type={self.event_type}, session_id={self.session_id})>"
        )

    @classmethod
    def from_domain(cls, entry: "AuditLogEntry") -> "EthicsAuditLogDB":  # noqa: F821
        """Construct DB row from the domain `AuditLogEntry` dataclass.

        Imported lazily inside the method to keep services/database from
        depending on services/ethics. Reverse direction (`to_domain`) is
        below.
        """
        return cls(
            entry_id=entry.entry_id,
            event_type=entry.event_type,
            timestamp=entry.timestamp,
            session_id=entry.session_id,
            user_id=entry.user_id,
            details=entry.details or {},
            redacted=entry.redacted,
        )

    def to_domain(self):
        """Convert DB row back to the domain `AuditLogEntry` dataclass."""
        from services.ethics.audit_transparency import AuditLogEntry

        return AuditLogEntry(
            entry_id=self.entry_id,
            event_type=self.event_type,
            timestamp=self.timestamp,
            session_id=self.session_id,
            user_id=self.user_id,
            details=self.details or {},
            redacted=self.redacted,
        )


class InsightDB(Base, TimestampMixin):
    """
    Durable storage for SurfaceableInsight (composted learnings ready for surfacing).

    Maps from `services.mux.composting_pipeline.SurfaceableInsight`.
    Replaces the in-memory `InsightJournal._insights` Dict (lost on restart)
    with PostgreSQL persistence so insights composted during quiet-hours
    survive server restarts.

    Issue #1035 (Phase 2 of MUX-COMPOSTING-ACTIVATION).
    Sibling pattern to `EthicsAuditLogDB` above (#1018) — same
    repository + AsyncSessionFactory.session_scope() pattern; user-scoped
    queries; soft-delete-via-flag postponed to #1031 (per audit walkthrough).
    """

    __tablename__ = "insights"

    # Identity — string PK matches SurfaceableInsight.id format (uuid4)
    id = Column(String(64), primary_key=True)

    # The COMPOSTED object that produced this insight (audit trail)
    object_id = Column(String(255), nullable=False, index=True)

    # User scoping — partition by user_id from day one (PM directive May 3:
    # "anything else is a false economy"). String to match existing user_id
    # propagation patterns; not a FK because insights survive user deletion.
    user_id = Column(String(255), nullable=False, index=True)

    # The typed learning, serialized as JSONB. Bridges via from_dict/to_dict
    # on the SurfaceableInsight + ExtractedLearning dataclasses.
    # JSONB().with_variant(JSON, "sqlite") lets unit tests run against
    # in-memory SQLite (which doesn't have JSONB) while production keeps
    # JSONB and its indexing/operator benefits on PostgreSQL.
    learning = Column(postgresql.JSONB().with_variant(JSON(), "sqlite"), nullable=True)

    # Surfacing control fields
    surfaced_count = Column(Integer, nullable=False, default=0)
    last_surfaced = Column(DateTime(timezone=True), nullable=True)
    user_response = Column(String(50), nullable=True)  # "engaged"|"dismissed"|"corrected"

    # Trust-based visibility threshold (Stage 1-4)
    min_trust_stage = Column(Integer, nullable=False, default=1)

    # Relationship metadata — JSONB on PostgreSQL, JSON on SQLite for tests.
    # Application-level default (default=list) handles new rows; server-side
    # default in migration handles any pre-existing rows on schema-introduce.
    connected_insights = Column(
        postgresql.JSONB().with_variant(JSON(), "sqlite"), nullable=False, default=list
    )
    context_tags = Column(
        postgresql.JSONB().with_variant(JSON(), "sqlite"), nullable=False, default=list
    )

    # #1031: soft-delete flag + free-text correction (PM Q1 + Q2 May 3)
    is_deleted = Column(Boolean, nullable=False, default=False)
    user_correction = Column(Text, nullable=True)

    # Strategic indexes matching InsightJournal query patterns:
    #   - get_for_context(user_id, ...) → idx_insights_user_created
    #   - get_unsurfaced(user_id, ...) → idx_insights_user_surfaced_count
    #   - get_for_object(object_id) → idx_insights_object
    __table_args__ = (
        Index("idx_insights_user_created", "user_id", "created_at"),
        Index("idx_insights_user_surfaced", "user_id", "surfaced_count"),
    )

    def __repr__(self):
        return (
            f"<InsightDB(id={self.id}, user_id={self.user_id}, "
            f"object_id={self.object_id}, surfaced_count={self.surfaced_count})>"
        )

    @classmethod
    def from_domain(cls, insight) -> "InsightDB":
        """Construct DB row from `SurfaceableInsight` dataclass.

        Imported lazily to keep services/database independent of services/mux.
        """
        learning_data = None
        if insight.learning is not None:
            learning_data = insight.learning.to_dict()

        return cls(
            id=insight.id,
            object_id=insight.object_id,
            user_id=insight.user_id,
            learning=learning_data,
            surfaced_count=insight.surfaced_count,
            last_surfaced=insight.last_surfaced,
            user_response=insight.user_response,
            min_trust_stage=insight.min_trust_stage,
            connected_insights=list(insight.connected_insights or []),
            context_tags=list(insight.context_tags or []),
            created_at=insight.created_at,
            is_deleted=getattr(insight, "is_deleted", False),
            user_correction=getattr(insight, "user_correction", None),
        )

    def to_domain(self):
        """Convert DB row back to `SurfaceableInsight` dataclass."""
        from services.mux.composting_models import ExtractedLearning
        from services.mux.composting_pipeline import SurfaceableInsight

        learning = None
        if self.learning:
            learning = ExtractedLearning.from_dict(self.learning)

        return SurfaceableInsight(
            id=self.id,
            object_id=self.object_id,
            user_id=self.user_id,
            created_at=self.created_at,
            learning=learning,
            surfaced_count=self.surfaced_count or 0,
            last_surfaced=self.last_surfaced,
            user_response=self.user_response,
            min_trust_stage=self.min_trust_stage or 1,
            connected_insights=list(self.connected_insights or []),
            context_tags=list(self.context_tags or []),
            is_deleted=bool(self.is_deleted),
            user_correction=self.user_correction,
        )


class Product(Base):
    """Product being managed"""

    __tablename__ = "products"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    vision = Column(Text)
    strategy = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    features = relationship("Feature", back_populates="product")
    work_items = relationship("WorkItem", back_populates="product")


class Feature(Base):
    """Feature or capability"""

    __tablename__ = "features"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    name = Column(String, nullable=False)
    description = Column(Text)
    hypothesis = Column(Text)
    acceptance_criteria = Column(JSON)  # List of criteria
    status = Column(String, default="draft")
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    product = relationship("Product", back_populates="features")
    work_items = relationship("WorkItem", back_populates="feature")


class WorkItem(Base):
    """Universal work item - can sync to any external system"""

    __tablename__ = "work_items"

    id = Column(String, primary_key=True)
    product_id = Column(String, ForeignKey("products.id"))
    feature_id = Column(String, ForeignKey("features.id"))
    title = Column(String, nullable=False)
    description = Column(Text)
    type = Column(String)  # bug, feature, task, improvement
    status = Column(String, default="open")
    priority = Column(String, default="medium")
    labels = Column(JSON)  # List of labels
    assignee = Column(String)  # Assigned person
    project_id = Column(String)  # Project association (separate from FK)
    source_system = Column(String)  # Source system name
    external_id = Column(String)  # External system ID
    external_url = Column(String)  # External system URL
    item_metadata = Column(JSON)  # Additional metadata (renamed to avoid SQLAlchemy conflict)

    # External system references
    external_refs = Column(JSON)  # {"github": "issue-123", "jira": "PROJ-456"}

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    # MUX Lifecycle (#710) - optional lifecycle state for MUX UI indicators
    lifecycle_state = Column(String(50), nullable=True)

    # Relationships
    product = relationship("Product", back_populates="work_items")
    feature = relationship("Feature", back_populates="work_items")

    def to_domain(self) -> domain.WorkItem:
        """Convert database model to domain model"""
        # Convert lifecycle_state string to enum if present (#710)
        lifecycle_state = None
        if self.lifecycle_state:
            try:
                lifecycle_state = LifecycleState(self.lifecycle_state)
            except ValueError:
                pass  # Invalid value, leave as None

        return domain.WorkItem(
            id=self.id,
            title=self.title,
            description=self.description,
            type=self.type or "task",
            status=self.status or "open",
            priority=self.priority or "medium",
            labels=self.labels or [],
            assignee=self.assignee,
            project_id=self.project_id,
            source_system=self.source_system or "",
            external_id=self.external_id or "",
            external_url=self.external_url,
            metadata=self.item_metadata or {},  # Map item_metadata to metadata
            created_at=self.created_at,
            lifecycle_state=lifecycle_state,
        )

    @classmethod
    def from_domain(cls, work_item: domain.WorkItem) -> "WorkItem":
        """Create database model from domain model"""
        return cls(
            id=work_item.id,
            title=work_item.title,
            description=work_item.description,
            type=work_item.type,
            status=work_item.status,
            priority=work_item.priority,
            labels=work_item.labels,
            assignee=work_item.assignee,
            project_id=work_item.project_id,
            source_system=work_item.source_system,
            external_id=work_item.external_id,
            external_url=work_item.external_url,
            item_metadata=work_item.metadata,  # Map metadata to item_metadata
        )


class Intent(Base):
    """Captured user intent"""

    __tablename__ = "intents"

    id = Column(String, primary_key=True)
    category = Column(Enum(IntentCategory))
    action = Column(String)
    confidence = Column(Float)
    context = Column(JSON)
    original_message = Column(Text)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationship to workflow if one was created
    workflow_id = Column(String, ForeignKey("workflows.id"))
    workflow = relationship("Workflow", back_populates="intent")


class Workflow(Base):
    """Workflow execution record"""

    __tablename__ = "workflows"

    id = Column(String, primary_key=True)
    type = Column(Enum(WorkflowType))
    status = Column(Enum(WorkflowStatus))
    input_data = Column(JSON)
    output_data = Column(JSON)
    context = Column(JSON)
    result = Column(JSON)  # Workflow execution result
    error = Column(Text)
    intent_id = Column(String(255), nullable=True)  # Matches domain Optional[str]

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    intent = relationship("Intent", back_populates="workflow", uselist=False)
    tasks = relationship("Task", back_populates="workflow")

    def to_domain(self) -> domain.Workflow:
        """Convert database model to domain model"""
        return domain.Workflow(
            id=self.id,
            type=self.type,
            status=self.status,
            context=self.context or {},
            result=self.output_data,
            error=self.error,
            intent_id=self.intent.id if self.intent else None,
            created_at=self.created_at,
            updated_at=self.completed_at
            or self.created_at,  # Use completed_at as updated_at, fallback to created_at
        )

    @classmethod
    def from_domain(cls, workflow: domain.Workflow) -> "Workflow":
        """Create database model from domain model"""
        return cls(
            id=workflow.id,
            type=workflow.type,
            status=workflow.status,
            input_data=workflow.input_data if hasattr(workflow, "input_data") else None,
            output_data=workflow.result,
            context=workflow.context,
            error=workflow.error,
            created_at=workflow.created_at,
            completed_at=workflow.completed_at,
        )


class Task(Base, TimestampMixin):
    """Individual task in a workflow"""

    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    workflow_id = Column(String, ForeignKey("workflows.id"))
    name = Column(String, nullable=False)  # Task name
    type = Column(Enum(TaskType))
    status = Column(Enum(TaskStatus))
    input_data = Column(JSON)
    output_data = Column(JSON)
    result = Column(JSON)  # Task execution result
    error = Column(Text)

    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Relationships
    workflow = relationship("Workflow", back_populates="tasks")


class Stakeholder(Base):
    """People involved with products"""

    __tablename__ = "stakeholders"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String)
    role = Column(String)
    interests = Column(JSON)  # List of interest areas
    influence_level = Column(Integer, default=1)
    satisfaction = Column(Float)  # Stakeholder satisfaction level
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))


class ProjectDB(Base):
    """A PM project with multiple tool integrations"""

    __tablename__ = "projects"
    __table_args__ = (
        # Composite unique constraint: project names unique per owner (multi-tenancy)
        # Issue #736: Changed from name-only to (owner_id, name)
        UniqueConstraint("owner_id", "name", name="uq_projects_owner_name"),
    )

    id = Column(String, primary_key=True)
    # owner_id is UUID in database - must match schema (Issue #479)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    name = Column(String, nullable=False)  # Unique per owner via __table_args__
    description = Column(Text)
    shared_with = Column(JSON, default=lambda: [])
    is_default = Column(Boolean, default=False)
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    # MUX Lifecycle (#718) - optional lifecycle state for MUX UI indicators
    lifecycle_state = Column(String(50), nullable=True)

    # Relationships
    integrations = relationship(
        "ProjectIntegrationDB", back_populates="project", cascade="all, delete-orphan"
    )
    repository_links = relationship(
        "ProjectRepositoryLinkDB", back_populates="project", cascade="all, delete-orphan"
    )

    def to_domain(self) -> domain.Project:
        # Convert shared_with JSON to SharePermission objects
        shared_with = []
        if self.shared_with:
            for perm_dict in self.shared_with:
                shared_with.append(
                    domain.SharePermission(
                        user_id=perm_dict["user_id"], role=domain.ShareRole(perm_dict["role"])
                    )
                )

        # Convert lifecycle_state string to enum if present (#718)
        lifecycle_state = None
        if self.lifecycle_state:
            try:
                lifecycle_state = LifecycleState(self.lifecycle_state)
            except ValueError:
                pass  # Invalid value, leave as None

        project = domain.Project(
            id=self.id,
            owner_id=self.owner_id or "",
            name=self.name,
            description=self.description,
            shared_with=shared_with,
            is_default=self.is_default,
            is_archived=self.is_archived,
            created_at=self.created_at,
            updated_at=self.updated_at,
            lifecycle_state=lifecycle_state,
        )
        # Map integrations relationship
        project.integrations = [integration.to_domain() for integration in self.integrations]
        # Map repositories through link table (#866)
        project.repositories = [
            link.repository.to_domain() for link in self.repository_links if link.repository
        ]
        return project

    @classmethod
    def from_domain(cls, project: domain.Project) -> "ProjectDB":
        # Convert SharePermission objects to JSONB-serializable format
        shared_with_json = [perm.to_dict() for perm in project.shared_with]

        return cls(
            id=project.id,
            owner_id=project.owner_id,
            name=project.name,
            description=project.description,
            shared_with=shared_with_json,
            is_default=project.is_default,
            is_archived=project.is_archived,
            created_at=project.created_at,
            updated_at=project.updated_at,
            # Note: integrations handled separately in repository
        )


class ProjectIntegrationDB(Base):
    """Integration configuration for a project"""

    __tablename__ = "project_integrations"

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    type = Column(Enum(IntegrationType), nullable=False)
    name = Column(String, nullable=False)
    config = Column(JSON, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    # Relationships
    project = relationship("ProjectDB", back_populates="integrations")

    def to_domain(self) -> domain.ProjectIntegration:
        return domain.ProjectIntegration(
            id=self.id,
            type=self.type,
            name=self.name,
            config=self.config,
            is_active=self.is_active,
            created_at=self.created_at,
        )

    @classmethod
    def from_domain(
        cls, integration: domain.ProjectIntegration, project_id: str
    ) -> "ProjectIntegrationDB":
        return cls(
            id=integration.id,
            project_id=project_id,
            type=integration.type,
            name=integration.name,
            config=integration.config,
            is_active=integration.is_active,
            created_at=integration.created_at,
        )


class RepositoryDB(Base):
    """A code repository — first-class, provider-agnostic entity.

    Issue #866: Repository as first-class domain entity.
    """

    __tablename__ = "repositories"
    __table_args__ = (
        UniqueConstraint(
            "owner_id", "provider", "full_name", name="uq_repositories_owner_provider_fullname"
        ),
        Index("idx_repositories_owner_id", "owner_id"),
        Index("idx_repositories_full_name", "full_name"),
    )

    id = Column(String, primary_key=True)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    provider = Column(String(50), nullable=False, default="github")
    full_name = Column(String, nullable=False)  # "owner/repo"
    display_name = Column(String, nullable=False)
    url = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    # Issue #867: GitHub API metadata
    description = Column(String, nullable=True)
    language = Column(String(100), nullable=True)
    visibility = Column(String(20), nullable=True)  # "public", "private", "internal"
    default_branch = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    project_links = relationship(
        "ProjectRepositoryLinkDB", back_populates="repository", cascade="all, delete-orphan"
    )

    def to_domain(self) -> domain.Repository:
        return domain.Repository(
            id=self.id,
            owner_id=self.owner_id or "",
            provider=self.provider,
            full_name=self.full_name,
            display_name=self.display_name,
            url=self.url or "",
            is_active=self.is_active,
            description=self.description,
            language=self.language,
            visibility=self.visibility,
            default_branch=self.default_branch,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, repo: domain.Repository) -> "RepositoryDB":
        return cls(
            id=repo.id,
            owner_id=repo.owner_id,
            provider=repo.provider,
            full_name=repo.full_name,
            display_name=repo.display_name,
            url=repo.url,
            is_active=repo.is_active,
            description=repo.description,
            language=repo.language,
            visibility=repo.visibility,
            default_branch=repo.default_branch,
            created_at=repo.created_at,
            updated_at=repo.updated_at,
        )


class ProjectRepositoryLinkDB(Base):
    """Join table: Project <-> Repository many-to-many.

    Issue #866: Repository as first-class domain entity.
    """

    __tablename__ = "project_repository_links"
    __table_args__ = (
        UniqueConstraint("project_id", "repository_id", name="uq_project_repo_link"),
        Index("idx_project_repo_links_project_id", "project_id"),
        Index("idx_project_repo_links_repository_id", "repository_id"),
    )

    id = Column(String, primary_key=True)
    project_id = Column(String, ForeignKey("projects.id"), nullable=False)
    repository_id = Column(String, ForeignKey("repositories.id"), nullable=False)
    is_primary = Column(Boolean, default=False)
    linked_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    linked_by = Column(String, nullable=False)  # User who created the link

    # Relationships
    project = relationship("ProjectDB", back_populates="repository_links")
    repository = relationship("RepositoryDB", back_populates="project_links")

    def to_domain(self) -> domain.ProjectRepositoryLink:
        return domain.ProjectRepositoryLink(
            id=self.id,
            project_id=self.project_id,
            repository_id=self.repository_id,
            is_primary=self.is_primary,
            linked_at=self.linked_at,
            linked_by=self.linked_by,
        )

    @classmethod
    def from_domain(cls, link: domain.ProjectRepositoryLink) -> "ProjectRepositoryLinkDB":
        return cls(
            id=link.id,
            project_id=link.project_id,
            repository_id=link.repository_id,
            is_primary=link.is_primary,
            linked_at=link.linked_at,
            linked_by=link.linked_by,
        )


class UploadedFileDB(Base):
    """Database model for uploaded files"""

    __tablename__ = "uploaded_files"

    id = Column(String, primary_key=True)
    owner_id = Column(postgresql.UUID(as_uuid=False), nullable=False)  # UUID type in database
    filename = Column(String(500), nullable=False)
    file_type = Column(String(255))
    file_size = Column(Integer)
    storage_path = Column(String(1000))
    upload_time = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    last_referenced = Column(DateTime(timezone=True), nullable=True)
    reference_count = Column(Integer, default=0)
    file_metadata = Column(JSON, default=dict)

    __table_args__ = (
        Index("idx_files_owner", "owner_id", "upload_time"),
        Index("idx_files_filename", "filename"),
    )

    def to_domain(self) -> domain.UploadedFile:
        return domain.UploadedFile(
            id=self.id,
            owner_id=str(self.owner_id) if self.owner_id else None,
            filename=self.filename,
            file_type=self.file_type,
            file_size=self.file_size,
            storage_path=self.storage_path,
            upload_time=self.upload_time,
            last_referenced=self.last_referenced,
            reference_count=self.reference_count,
            metadata={},  # Not stored separately in database
            file_metadata=self.file_metadata or {},
        )

    @classmethod
    def from_domain(cls, file: domain.UploadedFile) -> "UploadedFileDB":
        return cls(
            id=file.id,
            owner_id=file.owner_id,  # Will be converted to UUID by SQLAlchemy
            filename=file.filename,
            file_type=file.file_type,
            file_size=file.file_size,
            storage_path=file.storage_path,
            upload_time=file.upload_time,
            last_referenced=file.last_referenced,
            reference_count=file.reference_count,
            file_metadata=file.file_metadata,
        )


class ConversationDB(Base):
    """Database model for conversations"""

    __tablename__ = "conversations"

    id = Column(String, primary_key=True)
    user_id = Column(String, nullable=False)
    session_id = Column(String, nullable=False)
    title = Column(String, nullable=False, default="")
    context = Column(postgresql.JSONB, nullable=False, default={})
    is_active = Column(Boolean, nullable=False, default=True)  # DEPRECATED — use lifecycle_state
    # Issue #715: Conversation lifecycle states (spec #858)
    lifecycle_state = Column(String(20), nullable=False, default="active")
    archived_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    last_activity_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        Index("idx_conversations_user_session", "user_id", "session_id"),
        Index("idx_conversations_last_activity", "last_activity_at"),
        Index("idx_conversations_lifecycle_state", "lifecycle_state"),
    )

    def to_domain(self) -> domain.Conversation:
        from services.shared_types import ConversationLifecycleState

        return domain.Conversation(
            id=self.id,
            user_id=self.user_id,
            session_id=self.session_id,
            title=self.title,
            context=self.context or {},
            is_active=self.is_active,
            lifecycle_state=ConversationLifecycleState(self.lifecycle_state or "active"),
            archived_at=self.archived_at,
            deleted_at=self.deleted_at,
            created_at=self.created_at,
            updated_at=self.updated_at,
            last_activity_at=self.last_activity_at,
        )

    @classmethod
    def from_domain(cls, conversation: domain.Conversation) -> "ConversationDB":
        return cls(
            id=conversation.id,
            user_id=conversation.user_id,
            session_id=conversation.session_id,
            title=conversation.title,
            context=conversation.context,
            is_active=conversation.is_active,
            lifecycle_state=(
                conversation.lifecycle_state.value if conversation.lifecycle_state else "active"
            ),
            archived_at=conversation.archived_at,
            deleted_at=conversation.deleted_at,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            last_activity_at=conversation.last_activity_at,
        )


class ConversationTurnDB(Base):
    """Database model for conversation turns"""

    __tablename__ = "conversation_turns"

    id = Column(String, primary_key=True)
    conversation_id = Column(String, nullable=False)
    turn_number = Column(Integer, nullable=False, default=0)
    user_message = Column(Text, nullable=False, default="")
    assistant_response = Column(Text, nullable=False, default="")
    intent = Column(String, nullable=True)
    entities = Column(postgresql.JSONB, nullable=False, default=[])
    references = Column(postgresql.JSONB, nullable=False, default={})
    context_used = Column(postgresql.JSONB, nullable=False, default={})
    turn_metadata = Column("metadata", postgresql.JSONB, nullable=False, default={})
    processing_time = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    completed_at = Column(DateTime(timezone=True), nullable=True)

    __table_args__ = (
        ForeignKeyConstraint(["conversation_id"], ["conversations.id"], ondelete="CASCADE"),
        Index("idx_conversation_turns_conversation", "conversation_id", "turn_number"),
        Index("idx_conversation_turns_created", "created_at"),
    )

    def to_domain(self) -> domain.ConversationTurn:
        return domain.ConversationTurn(
            id=self.id,
            conversation_id=self.conversation_id,
            turn_number=self.turn_number,
            user_message=self.user_message,
            assistant_response=self.assistant_response,
            intent=self.intent,
            entities=self.entities or [],
            references=self.references or {},
            context_used=self.context_used or {},
            metadata=self.turn_metadata or {},
            processing_time=self.processing_time,
            created_at=self.created_at,
            completed_at=self.completed_at,
        )

    @classmethod
    def from_domain(cls, turn: domain.ConversationTurn) -> "ConversationTurnDB":
        return cls(
            id=turn.id,
            conversation_id=turn.conversation_id,
            turn_number=turn.turn_number,
            user_message=turn.user_message,
            assistant_response=turn.assistant_response,
            intent=turn.intent,
            entities=turn.entities,
            references=turn.references,
            context_used=turn.context_used,
            turn_metadata=turn.metadata,
            processing_time=turn.processing_time,
            created_at=turn.created_at,
            completed_at=turn.completed_at,
        )


class KnowledgeNodeDB(Base):
    """Database model for knowledge graph nodes"""

    __tablename__ = "knowledge_nodes"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    node_type = Column(String, nullable=False)  # String per ADR-041, convert to enum in to_domain()
    description = Column(Text)
    node_metadata = Column(JSON, default=dict)
    properties = Column(JSON, default=dict)
    session_id = Column(String)  # Legacy - kept for backward compatibility
    # owner_id is UUID in database - must match schema (Issue #479)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    embedding_vector = Column(
        postgresql.ARRAY(Float)
    )  # Will be upgraded to pgvector VECTOR type later
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    outgoing_edges = relationship(
        "KnowledgeEdgeDB",
        foreign_keys="KnowledgeEdgeDB.source_node_id",
        back_populates="source_node",
    )
    incoming_edges = relationship(
        "KnowledgeEdgeDB",
        foreign_keys="KnowledgeEdgeDB.target_node_id",
        back_populates="target_node",
    )

    __table_args__ = (
        Index("idx_nodes_session", "session_id"),
        Index("idx_nodes_type", "node_type"),
        Index("idx_nodes_name", "name"),
    )

    def to_domain(self) -> domain.KnowledgeNode:
        return domain.KnowledgeNode(
            id=self.id,
            name=self.name,
            node_type=NodeType(self.node_type),  # String → Enum (ADR-041)
            description=self.description,
            metadata=self.node_metadata or {},
            properties=self.properties or {},
            created_at=self.created_at,
            updated_at=self.updated_at,
            session_id=self.session_id,
        )

    @classmethod
    def from_domain(cls, node: domain.KnowledgeNode) -> "KnowledgeNodeDB":
        return cls(
            id=node.id,
            name=node.name,
            node_type=(
                node.node_type.value if isinstance(node.node_type, NodeType) else node.node_type
            ),  # Enum → String (ADR-041)
            description=node.description,
            node_metadata=node.metadata,
            properties=node.properties,
            created_at=node.created_at,
            updated_at=node.updated_at,
            session_id=node.session_id,
        )


class KnowledgeEdgeDB(Base):
    """Database model for knowledge graph edges"""

    __tablename__ = "knowledge_edges"

    id = Column(String, primary_key=True)
    source_node_id = Column(String, ForeignKey("knowledge_nodes.id"), nullable=False)
    target_node_id = Column(String, ForeignKey("knowledge_nodes.id"), nullable=False)
    edge_type = Column(String, nullable=False)  # String per ADR-041, convert to enum in to_domain()
    weight = Column(Float, default=1.0)
    node_metadata = Column(JSON, default=dict)
    properties = Column(JSON, default=dict)
    session_id = Column(String)  # Legacy - kept for backward compatibility
    # owner_id is UUID in database - must match schema (Issue #479)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relationships
    source_node = relationship(
        "KnowledgeNodeDB", foreign_keys=[source_node_id], back_populates="outgoing_edges"
    )
    target_node = relationship(
        "KnowledgeNodeDB", foreign_keys=[target_node_id], back_populates="incoming_edges"
    )

    __table_args__ = (
        Index("idx_edges_source", "source_node_id"),
        Index("idx_edges_target", "target_node_id"),
        Index("idx_edges_type", "edge_type"),
        Index("idx_edges_session", "session_id"),
        Index("idx_edges_source_target", "source_node_id", "target_node_id"),
    )

    def to_domain(self) -> domain.KnowledgeEdge:
        return domain.KnowledgeEdge(
            id=self.id,
            source_node_id=self.source_node_id,
            target_node_id=self.target_node_id,
            edge_type=EdgeType(self.edge_type),  # String → Enum (ADR-041)
            weight=self.weight,
            metadata=self.node_metadata or {},
            properties=self.properties,
            created_at=self.created_at,
            updated_at=self.updated_at,
            session_id=self.session_id,
        )

    @classmethod
    def from_domain(cls, edge: domain.KnowledgeEdge) -> "KnowledgeEdgeDB":
        return cls(
            id=edge.id,
            source_node_id=edge.source_node_id,
            target_node_id=edge.target_node_id,
            edge_type=(
                edge.edge_type.value if isinstance(edge.edge_type, EdgeType) else edge.edge_type
            ),  # Enum → String (ADR-041)
            weight=edge.weight,
            node_metadata=edge.metadata,
            properties=edge.properties,
            created_at=edge.created_at,
            updated_at=edge.updated_at,
            session_id=edge.session_id,
        )


# PM-081: Todo Management System Database Models
class TodoListDB(Base):
    """Database model for TodoList with strategic indexing"""

    __tablename__ = "todo_lists"

    # Primary key
    id = Column(String, primary_key=True)

    # Core fields
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    list_type = Column(Enum(ListType), nullable=False, default=ListType.PERSONAL)
    ordering_strategy = Column(
        Enum(OrderingStrategy), nullable=False, default=OrderingStrategy.MANUAL
    )

    # UI customization
    color = Column(String(7))  # Hex color codes
    emoji = Column(String(4))  # Unicode emoji

    # Status flags
    is_archived = Column(Boolean, default=False, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    # Metadata and tags
    list_metadata = Column("metadata", JSON, default=dict)
    tags = Column(postgresql.JSONB, default=list)  # Array of tag strings

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Ownership and sharing - owner_id is UUID in database (Issue #484)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    shared_with = Column(postgresql.JSONB, default=list)  # Array of user IDs

    # Performance optimization - cached counts
    todo_count = Column(Integer, default=0, nullable=False)
    completed_count = Column(Integer, default=0, nullable=False)

    # Relationships
    memberships = relationship(
        "ListMembershipDB", back_populates="todo_list", cascade="all, delete-orphan"
    )

    # Strategic indexes for performance
    __table_args__ = (
        Index("idx_todo_lists_owner_type", "owner_id", "list_type"),
        Index("idx_todo_lists_owner_archived", "owner_id", "is_archived"),
        Index(
            "idx_todo_lists_shared", "shared_with", postgresql_using="gin"
        ),  # GIN index for JSON array
        Index("idx_todo_lists_default", "owner_id", "is_default"),
        Index("idx_todo_lists_tags", "tags", postgresql_using="gin"),  # GIN index for tag search
    )

    def to_domain(self) -> domain.TodoList:
        """Convert to domain model"""
        return domain.TodoList(
            id=self.id,
            name=self.name,
            description=self.description,
            list_type=self.list_type,
            ordering_strategy=self.ordering_strategy,
            color=self.color,
            emoji=self.emoji,
            is_archived=self.is_archived,
            is_default=self.is_default,
            metadata=self.list_metadata or {},
            tags=self.tags or [],
            created_at=self.created_at,
            updated_at=self.updated_at,
            owner_id=self.owner_id,
            shared_with=self.shared_with or [],
            todo_count=self.todo_count,
            completed_count=self.completed_count,
        )

    @classmethod
    def from_domain(cls, todo_list: domain.TodoList) -> "TodoListDB":
        """Create from domain model"""
        return cls(
            id=todo_list.id,
            name=todo_list.name,
            description=todo_list.description,
            list_type=todo_list.list_type,
            ordering_strategy=todo_list.ordering_strategy,
            color=todo_list.color,
            emoji=todo_list.emoji,
            is_archived=todo_list.is_archived,
            is_default=todo_list.is_default,
            metadata=todo_list.metadata,
            tags=todo_list.tags,
            created_at=todo_list.created_at,
            updated_at=todo_list.updated_at,
            owner_id=todo_list.owner_id,
            shared_with=todo_list.shared_with,
            todo_count=todo_list.todo_count,
            completed_count=todo_list.completed_count,
        )


class ListMembershipDB(Base):
    """Database model for many-to-many Todo-to-List relationships"""

    __tablename__ = "list_memberships"

    # Primary key
    id = Column(String, primary_key=True)

    # Foreign keys
    list_id = Column(String, ForeignKey("todo_lists.id"), nullable=False)
    todo_id = Column(String, ForeignKey("todo_items.id"), nullable=False)

    # Position tracking
    position = Column(Integer, default=0, nullable=False)

    # Membership metadata
    added_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    added_by = Column(String, nullable=False)

    # List-specific overrides
    list_priority = Column(Enum(TodoPriority))
    list_due_date = Column(DateTime(timezone=True))
    list_notes = Column(Text, default="")

    # SEC-RBAC ownership - owner_id is UUID in database (Issue #479)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)

    # Relationships
    todo_list = relationship("TodoListDB", back_populates="memberships")
    # Disabled: TodoDB.memberships relationship disabled after foundation refactor
    # todo = relationship("TodoDB", back_populates="memberships")

    # Strategic indexes for many-to-many queries
    __table_args__ = (
        # Ensure unique membership per list-todo pair
        Index("idx_unique_list_todo", "list_id", "todo_id", unique=True),
        # Position-based ordering within lists
        Index("idx_membership_list_position", "list_id", "position"),
        # Todo-centric queries
        Index("idx_membership_todo", "todo_id"),
        # List-centric queries
        Index("idx_membership_list", "list_id"),
        # User-added tracking
        Index("idx_membership_added_by", "added_by"),
        Index("idx_membership_added_at", "added_at"),
        # List-specific overrides
        Index("idx_membership_list_priority", "list_id", "list_priority"),
        Index("idx_membership_list_due", "list_id", "list_due_date"),
    )

    def to_domain(self) -> domain.ListMembership:
        """Convert to domain model"""
        return domain.ListMembership(
            id=self.id,
            list_id=self.list_id,
            todo_id=self.todo_id,
            position=self.position,
            added_at=self.added_at,
            added_by=self.added_by,
            list_priority=self.list_priority,
            list_due_date=self.list_due_date,
            list_notes=self.list_notes,
        )

    @classmethod
    def from_domain(cls, membership: domain.ListMembership) -> "ListMembershipDB":
        """Create from domain model"""
        return cls(
            id=membership.id,
            list_id=membership.list_id,
            todo_id=membership.todo_id,
            position=membership.position,
            added_at=membership.added_at,
            added_by=membership.added_by,
            list_priority=membership.list_priority,
            list_due_date=membership.list_due_date,
            list_notes=membership.list_notes,
        )


# PM-081: Universal List Architecture Database Models
# Chief Architect's universal composition over specialization principle


class ListDB(Base):
    """Universal List database model for ANY item type"""

    __tablename__ = "lists"

    # Primary key
    id = Column(String, primary_key=True)

    # Core fields
    name = Column(String, nullable=False)
    description = Column(Text, default="")
    item_type = Column(String, nullable=False, default="todo")  # todo, feature, bug, attendee, etc.
    list_type = Column(String, nullable=False, default="personal")  # personal, shared, project
    ordering_strategy = Column(
        String, nullable=False, default="manual"
    )  # manual, due_date, priority, created

    # UI customization
    color = Column(String(7))  # Hex color codes
    emoji = Column(String(4))  # Unicode emoji

    # Status flags
    is_archived = Column(Boolean, default=False, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    # Metadata and tags
    list_metadata = Column("metadata", JSON, default=dict)
    tags = Column(postgresql.JSONB, default=list)  # Array of tag strings

    # Project associations (many-to-many - L1 Sprint #477)
    project_ids = Column(postgresql.JSONB, default=list)  # Array of project IDs

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Ownership and sharing - owner_id is UUID in database (Issue #484)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    shared_with = Column(postgresql.JSONB, default=list)  # Array of user IDs

    # Performance optimization - cached counts
    item_count = Column(Integer, default=0, nullable=False)
    completed_count = Column(Integer, default=0, nullable=False)

    # Relationships
    items = relationship("ListItemDB", back_populates="list", cascade="all, delete-orphan")

    # Strategic indexes for performance
    __table_args__ = (
        Index("idx_lists_owner_type", "owner_id", "item_type"),
        Index("idx_lists_owner_list_type", "owner_id", "list_type"),
        Index("idx_lists_owner_archived", "owner_id", "is_archived"),
        Index(
            "idx_lists_shared", "shared_with", postgresql_using="gin"
        ),  # GIN index for JSON array
        Index("idx_lists_default", "owner_id", "item_type", "is_default"),
        Index("idx_lists_tags", "tags", postgresql_using="gin"),  # GIN index for tag search
        Index(
            "idx_lists_projects", "project_ids", postgresql_using="gin"
        ),  # GIN index for project lookup
    )

    def to_domain(self) -> domain.List:
        """Convert to domain model"""
        return domain.List(
            id=self.id,
            name=self.name,
            description=self.description,
            item_type=self.item_type,
            list_type=self.list_type,
            ordering_strategy=self.ordering_strategy,
            color=self.color,
            emoji=self.emoji,
            is_archived=self.is_archived,
            is_default=self.is_default,
            metadata=self.list_metadata or {},
            tags=self.tags or [],
            project_ids=self.project_ids or [],
            created_at=self.created_at,
            updated_at=self.updated_at,
            owner_id=self.owner_id,
            shared_with=self.shared_with or [],
            item_count=self.item_count,
            completed_count=self.completed_count,
        )

    @classmethod
    def from_domain(cls, list_obj: domain.List) -> "ListDB":
        """Create from domain model"""
        return cls(
            id=list_obj.id,
            name=list_obj.name,
            description=list_obj.description,
            item_type=list_obj.item_type,
            list_type=list_obj.list_type,
            ordering_strategy=list_obj.ordering_strategy,
            color=list_obj.color,
            emoji=list_obj.emoji,
            is_archived=list_obj.is_archived,
            is_default=list_obj.is_default,
            metadata=list_obj.metadata,
            tags=list_obj.tags,
            project_ids=list_obj.project_ids,
            created_at=list_obj.created_at,
            updated_at=list_obj.updated_at,
            owner_id=list_obj.owner_id,
            shared_with=list_obj.shared_with,
            item_count=getattr(list_obj, "item_count", 0),
            completed_count=getattr(list_obj, "completed_count", 0),
        )


class ListItemDB(Base):
    """Universal ListItem database model - polymorphic relationship"""

    __tablename__ = "list_items"

    # Primary key
    id = Column(String, primary_key=True)

    # Foreign keys
    list_id = Column(String, ForeignKey("lists.id"), nullable=False)
    item_id = Column(String, nullable=False)  # Polymorphic reference
    item_type = Column(String, nullable=False)  # todo, feature, bug, attendee, etc.

    # Position tracking
    position = Column(Integer, default=0, nullable=False)

    # Membership metadata
    added_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    added_by = Column(String, nullable=False)

    # List-specific overrides
    list_priority = Column(String)  # Override item's default priority
    list_due_date = Column(DateTime(timezone=True))  # Override item's default due date
    list_notes = Column(Text, default="")

    # SEC-RBAC ownership - owner_id is UUID in database (Issue #479)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=True)

    # Relationships
    list = relationship("ListDB", back_populates="items")

    # Strategic indexes for many-to-many queries
    __table_args__ = (
        Index("idx_list_items_list_id", "list_id"),
        Index("idx_list_items_item_id_type", "item_id", "item_type"),
        Index("idx_list_items_position", "list_id", "position"),
        Index("idx_list_items_added_by", "added_by"),
    )

    def to_domain(self) -> domain.ListItem:
        """Convert to domain model"""
        return domain.ListItem(
            id=self.id,
            list_id=self.list_id,
            item_id=self.item_id,
            item_type=self.item_type,
            position=self.position,
            added_at=self.added_at,
            added_by=self.added_by,
            list_priority=self.list_priority,
            list_due_date=self.list_due_date,
            list_notes=self.list_notes,
        )

    @classmethod
    def from_domain(cls, item: domain.ListItem) -> "ListItemDB":
        """Create from domain model"""
        return cls(
            id=item.id,
            list_id=item.list_id,
            item_id=item.item_id,
            item_type=item.item_type,
            position=item.position,
            added_at=item.added_at,
            added_by=item.added_by,
            list_priority=item.list_priority,
            list_due_date=item.list_due_date,
            list_notes=item.list_notes,
        )


class FeedbackDB(Base, TimestampMixin):
    """Database model for user feedback tracking - PM-005

    Issue #262 - UUID migration complete
    """

    __tablename__ = "feedback"

    # Primary key
    id = Column(String, primary_key=True)

    # Core feedback data
    session_id = Column(String, nullable=False, index=True)
    feedback_type = Column(String, nullable=False)  # "bug", "feature", "ux", "general"
    rating = Column(Integer)  # 1-5 rating (optional)
    comment = Column(Text, nullable=False)
    context = Column(JSON, default=dict)  # Additional context data

    # User and session context
    user_id = Column(
        postgresql.UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True
    )
    conversation_context = Column(JSON, default=dict)  # Conversation context if available

    # Feedback metadata
    source = Column(String, default="api")  # "api", "ui", "conversation"
    status = Column(String, default="new")  # "new", "reviewed", "addressed", "closed"
    priority = Column(String, default="medium")  # "low", "medium", "high", "critical"

    # Analysis and processing
    sentiment_score = Column(Float)  # -1.0 to 1.0
    categories = Column(JSON, default=list)  # Auto-detected categories
    tags = Column(JSON, default=list)  # User or system tags

    # Relationships
    user = relationship("User", back_populates="feedback")
    # related_issues = Column(JSON, default=list)  # Links to related GitHub issues

    # Strategic indexes for query performance
    __table_args__ = (
        Index("idx_feedback_session_id", "session_id"),
        Index("idx_feedback_type", "feedback_type"),
        Index("idx_feedback_rating", "rating"),
        Index("idx_feedback_status", "status"),
        Index("idx_feedback_created_at", "created_at"),
        Index("idx_feedback_user_id", "user_id"),
        Index("idx_feedback_source", "source"),
    )

    def to_domain(self) -> "Feedback":
        """Convert to domain model"""
        from services.feedback.models import Feedback

        return Feedback(
            id=self.id,
            session_id=self.session_id,
            feedback_type=self.feedback_type,
            rating=self.rating,
            comment=self.comment,
            context=self.context,
            user_id=self.user_id,
            conversation_context=self.conversation_context,
            source=self.source,
            status=self.status,
            priority=self.priority,
            sentiment_score=self.sentiment_score,
            categories=self.categories,
            tags=self.tags,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, feedback: "Feedback") -> "FeedbackDB":
        """Create from domain model"""
        return cls(
            id=feedback.id,
            session_id=feedback.session_id,
            feedback_type=feedback.feedback_type,
            rating=feedback.rating,
            comment=feedback.comment,
            context=feedback.context,
            user_id=feedback.user_id,
            conversation_context=feedback.conversation_context,
            source=feedback.source,
            status=feedback.status,
            priority=feedback.priority,
            sentiment_score=feedback.sentiment_score,
            categories=feedback.categories,
            tags=feedback.tags,
            created_at=feedback.created_at,
            updated_at=feedback.updated_at,
        )


class PersonalityProfileModel(Base, TimestampMixin):
    """Database model for personality profiles

    Issue #262 - UUID migration complete
    """

    __tablename__ = "personality_profiles"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True)
    user_id = Column(
        postgresql.UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, unique=True
    )
    warmth_level = Column(Float, nullable=False, default=0.6)
    confidence_style = Column(String(50), nullable=False, default="contextual")
    action_orientation = Column(String(50), nullable=False, default="medium")
    technical_depth = Column(String(50), nullable=False, default="balanced")
    is_active = Column(Boolean, nullable=False, default=True)

    # Relationships
    user = relationship("User", back_populates="personality_profiles")

    # Indexes are defined in the migration
    __table_args__ = (
        Index("idx_personality_profiles_user_id", "user_id", unique=True),
        Index("idx_personality_profiles_active", "is_active"),
        Index("idx_personality_profiles_user_active", "user_id", "is_active"),
        Index("idx_personality_profiles_warmth", "warmth_level"),
        Index("idx_personality_profiles_confidence", "confidence_style"),
        Index("idx_personality_profiles_action", "action_orientation"),
        Index("idx_personality_profiles_technical", "technical_depth"),
    )

    def to_domain(self) -> "domain.PersonalityProfile":
        """Convert to domain model"""
        # Import here to avoid circular imports
        from services.personality.personality_profile import (
            ActionLevel,
            ConfidenceDisplayStyle,
            PersonalityProfile,
            TechnicalPreference,
        )

        return PersonalityProfile(
            warmth_level=self.warmth_level,
            confidence_style=ConfidenceDisplayStyle(self.confidence_style),
            action_orientation=ActionLevel(self.action_orientation),
            technical_depth=TechnicalPreference(self.technical_depth),
        )

    @classmethod
    def from_domain(
        cls, profile: "domain.PersonalityProfile", user_id: uuid.UUID
    ) -> "PersonalityProfileModel":
        """Create from domain model"""
        import uuid

        return cls(
            id=uuid.uuid4(),
            user_id=user_id,
            warmth_level=profile.warmth_level,
            confidence_style=profile.confidence_style.value,
            action_orientation=profile.action_orientation.value,
            technical_depth=profile.technical_depth.value,
            is_active=True,
        )


class TokenBlacklist(Base):
    """
    Blacklisted JWT tokens (database fallback for Redis)

    Stores revoked tokens for security invalidation when Redis unavailable.
    Redis is primary storage with TTL; this is fallback only.

    Issue #291 - FK constraint restored with CASCADE delete
    """

    __tablename__ = "token_blacklist"

    # Primary key
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Token identification
    token_id = Column(String(255), unique=True, nullable=False, index=True)
    # Issue #291 - FK constraint restored (was temporarily removed for alpha)
    user_id = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
    )

    # Blacklist metadata
    reason = Column(String(50), nullable=False)  # logout, security, admin
    expires_at = Column(DateTime(timezone=True), nullable=False, index=True)
    created_at = Column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    # Relationships (Issue #291 - restored)
    user = relationship("User", back_populates="blacklisted_tokens")

    # Strategic indexes for performance
    __table_args__ = (
        Index("idx_token_blacklist_token_id", "token_id", unique=True),
        Index("idx_token_blacklist_expires", "expires_at"),
        Index("idx_token_blacklist_user_id", "user_id"),
        Index("idx_token_blacklist_user_expires", "user_id", "expires_at"),
    )


# ============================================================================
# PRIMITIVE DOMAIN MODELS (Phase 1: Foundation)
# ============================================================================


class ItemDB(Base):
    """
    Database representation of universal Item primitive.

    This is the base table for all item types using SQLAlchemy's
    polymorphic inheritance (joined table inheritance pattern).

    Future item types (Todo, ShoppingItem, etc.) will have their own tables
    that join to this one via foreign key on id.

    Phase 1: Create base items table
    Phase 2: Create todo_items table (joins to items)
    Future: Other item types can follow same pattern
    """

    __tablename__ = "items"

    # Core fields
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    text = Column(String, nullable=False)  # Universal property - all items have text
    position = Column(Integer, default=0, nullable=False)  # Order within list
    list_id = Column(String, nullable=True)  # Which list contains this item
    item_type = Column(String(50), nullable=False, default="item")  # Discriminator

    # Timestamps
    created_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Polymorphic configuration for future inheritance
    __mapper_args__ = {
        "polymorphic_identity": "item",
        "polymorphic_on": item_type,
    }

    # Indexes for performance
    __table_args__ = (
        Index("idx_items_list_id", "list_id"),
        Index("idx_items_item_type", "item_type"),
        Index("idx_items_list_position", "list_id", "position"),
        Index("idx_items_created", "created_at"),
    )

    def to_domain(self) -> "domain.Item":
        """Convert database model to domain model."""
        # Import here to avoid circular imports
        from services.domain.primitives import Item

        return Item(
            id=self.id,
            text=self.text,
            position=self.position,
            list_id=self.list_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @classmethod
    def from_domain(cls, item: "domain.Item") -> "ItemDB":
        """Convert domain model to database model."""
        return cls(
            id=item.id,
            text=item.text,
            position=item.position,
            list_id=item.list_id,
            item_type="item",  # Base type
            created_at=item.created_at,
            updated_at=item.updated_at,
        )


class TodoDB(ItemDB):
    """Database model for Todo using polymorphic inheritance.

    Extends ItemDB using SQLAlchemy's joined table inheritance:
    - Base data in 'items' table (id, text, position, list_id, created_at, updated_at)
    - Todo-specific data in 'todo_items' table
    - Joined via foreign key on id

    Design: TodoDB IS-A ItemDB, matching domain's Todo IS-A Item
    """

    __tablename__ = "todo_items"

    # Primary key is also foreign key to items.id
    id = Column(String, ForeignKey("items.id"), primary_key=True)

    # Todo-specific fields only (NOT duplicating ItemDB fields)
    # Note: text (was title), position, created_at, updated_at are inherited from ItemDB

    # Core Todo fields
    description = Column(Text, default="")
    status = Column(String(11), nullable=False, default="pending")  # Changed from Enum to String
    priority = Column(String(6), nullable=False, default="medium")  # Changed from Enum to String
    completed = Column(Boolean, default=False, nullable=False)

    # Hierarchical structure
    parent_id = Column(String, ForeignKey("todo_items.id"))

    # Scheduling
    due_date = Column(DateTime(timezone=True))
    reminder_date = Column(DateTime(timezone=True))
    scheduled_date = Column(DateTime(timezone=True))

    # Context and categorization
    tags = Column(postgresql.JSONB, default=list)
    project_id = Column(String, ForeignKey("projects.id"))
    context = Column(String)  # @home, @work, etc.

    # Progress tracking
    estimated_minutes = Column(Integer)
    actual_minutes = Column(Integer)
    completion_notes = Column(Text, default="")

    # PM-040 Knowledge Graph integration
    list_metadata = Column("list_metadata", JSON, default=dict)
    knowledge_node_id = Column(String)  # Link to Knowledge Graph
    related_todos = Column(JSON, default=list)  # Array of todo IDs

    # PM-034 Intent Classification integration
    creation_intent = Column(String)
    intent_confidence = Column(Float)

    # External integrations
    external_refs = Column(postgresql.JSONB, default=dict)  # {"github_issue": "123"}

    # Timestamps (inherited: created_at, updated_at from ItemDB)
    completed_at = Column(DateTime(timezone=True))

    # Ownership - owner_id is UUID in database (Issue #484)
    owner_id = Column(postgresql.UUID(as_uuid=False), ForeignKey("users.id"), nullable=False)
    assigned_to = Column(String)

    # Polymorphic configuration - TodoDB is a specialized ItemDB
    __mapper_args__ = {
        "polymorphic_identity": "todo",
    }

    # Relationships
    parent = relationship(
        "TodoDB", remote_side=[id], foreign_keys="[TodoDB.parent_id]", back_populates="children"
    )
    children = relationship(
        "TodoDB",
        foreign_keys="[TodoDB.parent_id]",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    # Disabled: list_memberships table was dropped in foundation/item-list-primitives refactor
    # TODO: Re-enable after UniversalList migration is complete
    # memberships = relationship(
    #     "ListMembershipDB", back_populates="todo", cascade="all, delete-orphan"
    # )

    # Comprehensive indexes for query performance
    # NOTE: Indexes on inherited fields (position, created_at, updated_at)
    # belong in items table, not todo_items table
    __table_args__ = (
        # Core query patterns
        Index("idx_todos_owner_status", "owner_id", "status"),
        Index("idx_todos_owner_priority", "owner_id", "priority"),
        Index("idx_todos_assigned_status", "assigned_to", "status"),
        # Date-based queries
        Index("idx_todos_due_date", "due_date"),
        Index("idx_todos_owner_due", "owner_id", "due_date"),
        Index("idx_todos_scheduled", "scheduled_date"),
        Index("idx_todos_reminder", "reminder_date"),
        # Hierarchical queries
        Index("idx_todos_parent", "parent_id"),
        # Context and categorization
        Index("idx_todos_context", "context"),
        Index("idx_todos_project", "project_id"),
        Index("idx_todos_tags", "tags", postgresql_using="gin"),  # GIN index for tag search
        # PM-040/PM-034 integration
        Index("idx_todos_knowledge_node", "knowledge_node_id"),
        Index("idx_todos_creation_intent", "creation_intent"),
        # External references
        Index(
            "idx_todos_external_refs", "external_refs", postgresql_using="gin"
        ),  # GIN index for JSON search
    )

    def to_domain(self) -> domain.Todo:
        """Convert to domain model.

        Maps database fields to domain model, including inherited ItemDB fields.
        """
        return domain.Todo(
            # Inherited from ItemDB
            id=self.id,
            text=self.text,  # ItemDB uses 'text', domain Todo has 'text' and 'title' property
            position=self.position,
            list_id=self.list_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
            # Todo-specific fields
            description=self.description,
            status=self.status,
            priority=self.priority,
            completed=self.completed,
            parent_id=self.parent_id,
            due_date=self.due_date,
            reminder_date=self.reminder_date,
            scheduled_date=self.scheduled_date,
            tags=self.tags or [],
            project_id=self.project_id,
            context=self.context,
            estimated_minutes=self.estimated_minutes,
            actual_minutes=self.actual_minutes,
            completion_notes=self.completion_notes,
            metadata=self.list_metadata or {},
            knowledge_node_id=self.knowledge_node_id,
            related_todos=self.related_todos or [],
            creation_intent=self.creation_intent,
            intent_confidence=self.intent_confidence,
            external_refs=self.external_refs or {},
            completed_at=self.completed_at,
            owner_id=self.owner_id,
            assigned_to=self.assigned_to,
        )

    @classmethod
    def from_domain(cls, todo: domain.Todo) -> "TodoDB":
        """Create from domain model.

        Maps domain model fields to database, including inherited ItemDB fields.
        Note: ItemDB fields (id, text, position, list_id) are set automatically
        by SQLAlchemy's polymorphic inheritance.
        """
        return cls(
            # Inherited from ItemDB (polymorphic inheritance handles these)
            id=todo.id,
            text=todo.text,  # Use text, not title
            position=todo.position,
            list_id=todo.list_id,
            item_type="todo",  # Polymorphic discriminator
            created_at=todo.created_at,
            updated_at=todo.updated_at,
            # Todo-specific fields
            description=todo.description,
            status=todo.status,
            priority=todo.priority,
            completed=todo.completed,
            parent_id=todo.parent_id,
            due_date=todo.due_date,
            reminder_date=todo.reminder_date,
            scheduled_date=todo.scheduled_date,
            tags=todo.tags,
            project_id=todo.project_id,
            context=todo.context,
            estimated_minutes=todo.estimated_minutes,
            actual_minutes=todo.actual_minutes,
            completion_notes=todo.completion_notes,
            metadata=todo.metadata,
            knowledge_node_id=todo.knowledge_node_id,
            related_todos=todo.related_todos,
            creation_intent=todo.creation_intent,
            intent_confidence=todo.intent_confidence,
            external_refs=todo.external_refs,
            completed_at=todo.completed_at,
            owner_id=todo.owner_id,
            assigned_to=todo.assigned_to,
        )


class LearnedPattern(Base, TimestampMixin):
    """
    Learned patterns for auto-learning system.

    Stores user-specific patterns discovered through real-time learning.
    Confidence increases with successful applications, decreases with failures.

    Issue #300: CORE-ALPHA-LEARNING-BASIC - Basic Auto-Learning
    Foundation Stone #1 of the learning cathedral.
    """

    __tablename__ = "learned_patterns"

    # Primary key
    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # User association
    user_id = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Pattern identification
    pattern_type = Column(Enum(PatternType), nullable=False)
    pattern_data = Column(JSON, nullable=False)  # Flexible pattern storage

    # Confidence tracking
    confidence = Column(Float, default=0.5, nullable=False)  # 0.0 to 1.0
    usage_count = Column(Integer, default=0, nullable=False)
    success_count = Column(Integer, default=0, nullable=False)
    failure_count = Column(Integer, default=0, nullable=False)

    # Status
    enabled = Column(Boolean, default=True, nullable=False)

    # Timestamps (from TimestampMixin: created_at, updated_at)
    last_used_at = Column(DateTime(timezone=True), nullable=True)

    # Relationships
    user = relationship("User", back_populates="learned_patterns")

    # Indexes for performance
    __table_args__ = (
        Index("ix_learned_patterns_user_confidence", "user_id", "confidence"),
        Index("ix_learned_patterns_user_enabled", "user_id", "enabled"),
    )

    def update_confidence(self):
        """
        Calculate confidence from success/failure rates with volume factor.

        Formula: confidence = (success_rate * 0.8 + previous_confidence * 0.2) * volume_factor
        Volume factor: min(usage_count / 10, 1.0) - caps at 10 uses
        """
        total = self.success_count + self.failure_count
        if total == 0:
            return  # No outcomes yet

        # Success rate (0.0 - 1.0)
        success_rate = self.success_count / total

        # Volume factor (more uses = more confidence, caps at 10)
        volume_factor = min(self.usage_count / 10, 1.0)

        # Weighted: 80% current success, 20% previous confidence
        new_confidence = success_rate * 0.8 + self.confidence * 0.2

        # Apply volume factor
        self.confidence = new_confidence * volume_factor

        # Disable if too low
        if self.confidence < 0.3:
            self.enabled = False

        self.updated_at = datetime.now(timezone.utc)


class LearningSettings(Base, TimestampMixin):
    """
    User learning preferences and configuration.

    Controls auto-learning behavior, suggestion thresholds, and automation settings.
    One settings record per user (enforced by unique constraint).
    """

    __tablename__ = "learning_settings"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # One settings per user
        index=True,
    )

    # Learning behavior controls
    learning_enabled = Column(
        Boolean, default=True, nullable=False, comment="Master switch for learning system"
    )
    suggestion_threshold = Column(
        Float,
        default=0.7,
        nullable=False,
        comment="Minimum confidence to show suggestions",
    )
    automation_threshold = Column(
        Float,
        default=0.9,
        nullable=False,
        comment="Minimum confidence for automatic execution",
    )

    # Optional: Future settings placeholders
    auto_apply_enabled = Column(
        Boolean,
        default=False,
        nullable=False,
        comment="Allow automatic pattern application",
    )
    notification_enabled = Column(
        Boolean,
        default=True,
        nullable=False,
        comment="Show learning notifications",
    )

    # Relationship
    user = relationship("User", back_populates="learning_settings")


# Note: ListDB already exists at line 1126 with full implementation
# It includes all fields from domain.List plus owner_id, shared_with, etc.


class UserTrustProfileDB(Base, TimestampMixin):
    """
    Persisted trust state for a user.

    Issue #647: TRUST-LEVELS-1 - Core Infrastructure
    ADR-053: Trust Computation Architecture

    Tracks user's progression through trust stages, enabling Piper to
    calibrate proactivity appropriately. One profile per user.
    """

    __tablename__ = "user_trust_profiles"

    id = Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(
        postgresql.UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,  # One trust profile per user
        index=True,
    )

    # Current trust stage (1=NEW, 2=BUILDING, 3=ESTABLISHED, 4=TRUSTED)
    current_stage = Column(Integer, default=1, nullable=False)
    highest_stage_achieved = Column(Integer, default=1, nullable=False)

    # Counters for stage progression
    # CALIBRATION: Thresholds (10 for 1→2, 50 for 2→3) are starting points
    successful_count = Column(Integer, default=0, nullable=False)
    neutral_count = Column(Integer, default=0, nullable=False)
    negative_count = Column(Integer, default=0, nullable=False)
    consecutive_negative = Column(Integer, default=0, nullable=False)

    # JSON fields for complex data (bounded history for discussability)
    recent_events = Column(JSON, default=list, nullable=False)
    stage_history = Column(JSON, default=list, nullable=False)

    # Timestamps (beyond TimestampMixin)
    last_interaction_at = Column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False
    )
    last_stage_change_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship
    user = relationship("User", backref="trust_profile")

    @classmethod
    def from_domain(cls, profile: domain.UserTrustProfile) -> "UserTrustProfileDB":
        """Create DB model from domain model."""
        return cls(
            user_id=profile.user_id,
            current_stage=profile.current_stage.value,
            highest_stage_achieved=profile.highest_stage_achieved.value,
            successful_count=profile.successful_count,
            neutral_count=profile.neutral_count,
            negative_count=profile.negative_count,
            consecutive_negative=profile.consecutive_negative,
            recent_events=[
                {
                    "event_id": str(e.event_id),
                    "timestamp": e.timestamp.isoformat(),
                    "outcome": e.outcome,
                    "context": e.context,
                    "stage_at_time": e.stage_at_time.value,
                }
                for e in profile.recent_events
            ],
            stage_history=[
                {
                    "timestamp": ts.isoformat(),
                    "stage": stage.value,
                    "reason": reason,
                }
                for ts, stage, reason in profile.stage_history
            ],
            last_interaction_at=profile.last_interaction_at,
            last_stage_change_at=profile.last_stage_change_at,
            created_at=profile.created_at,
        )

    def to_domain(self) -> domain.UserTrustProfile:
        """Convert DB model to domain model."""
        from datetime import datetime as dt
        from uuid import UUID

        # Parse recent_events from JSON
        recent_events = []
        for e in self.recent_events or []:
            recent_events.append(
                domain.TrustEvent(
                    event_id=UUID(e["event_id"]),
                    timestamp=dt.fromisoformat(e["timestamp"]),
                    outcome=e["outcome"],
                    context=e["context"],
                    stage_at_time=TrustStage(e["stage_at_time"]),
                )
            )

        # Parse stage_history from JSON
        stage_history = []
        for h in self.stage_history or []:
            stage_history.append(
                (
                    dt.fromisoformat(h["timestamp"]),
                    TrustStage(h["stage"]),
                    h["reason"],
                )
            )

        return domain.UserTrustProfile(
            user_id=self.user_id,
            current_stage=TrustStage(self.current_stage),
            highest_stage_achieved=TrustStage(self.highest_stage_achieved),
            successful_count=self.successful_count,
            neutral_count=self.neutral_count,
            negative_count=self.negative_count,
            consecutive_negative=self.consecutive_negative,
            recent_events=recent_events,
            stage_history=stage_history,
            created_at=self.created_at,
            last_interaction_at=self.last_interaction_at,
            last_stage_change_at=self.last_stage_change_at,
        )


class ConversationalMemoryEntryDB(Base):
    """
    Database model for conversational memory entries (ADR-054 Layer 1).

    Part of #657 MEM-ADR054-P1.
    Stores memorable items from conversations for 24-hour continuity window.
    """

    __tablename__ = "conversational_memory_entries"

    id = Column(String, primary_key=True)  # UUID as string
    user_id = Column(String, nullable=False, index=True)
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)

    timestamp = Column(DateTime(timezone=True), nullable=False)
    topic_summary = Column(String(500), nullable=False)
    entities_mentioned = Column(postgresql.JSONB, default=list)
    outcome = Column(String(500), nullable=True)
    user_sentiment = Column(String(20), nullable=True)  # positive/neutral/negative

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (Index("idx_cme_user_timestamp", "user_id", "timestamp"),)
