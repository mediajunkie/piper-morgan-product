"""#1273: create intents / workflows / tasks / stakeholders — missing create-migrations

Revision ID: a1273coretables
Revises: a1267projintegrations
Create Date: 2026-06-17

Same class as #1267: these 4 ORM models existed but were only ever created via
`Base.metadata.create_all()` (test-only path) — they have NO `create_table` migration,
so a fresh `alembic upgrade head` does not create them. They're present on existing
DBs only because those DBs were create_all'd + stamped; a clean from-base build would
lack them (and workflows/tasks/intents are core orchestration tables). Surfaced by the
#1267 `TestModelMigrationCoverage` guard; filed as #1273.

Schema = the exact compiled model DDL (SQLAlchemy CreateTable for the current models),
hardcoded here so it is immutable (future model changes apply via their own alter
migrations on top — NOT regenerated from the model). Enum labels are the member NAMES
(the default `Enum(PyEnum)` mapping), matching the create_all-produced PG types.

Idempotent (repairs already-deployed at-head DBs AND fresh ones): each enum via an
`IF NOT EXISTS` DO-block (the 8e4f idiom), each table created only if absent, with
`postgresql.ENUM(create_type=False)` columns so create_table doesn't re-emit CREATE TYPE.

FK order: workflows first (no FKs); intents + tasks FK workflows.id; stakeholders
independent.
"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a1273coretables"
down_revision: Union[str, Sequence[str], None] = "a1267projintegrations"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Enum labels = member NAMES (default Enum(PyEnum) mapping; matches create_all PG types).
_WORKFLOWTYPE = (
    "CREATE_FEATURE",
    "ANALYZE_METRICS",
    "CREATE_TICKET",
    "CREATE_TASK",
    "REVIEW_ITEM",
    "GENERATE_REPORT",
    "PLAN_STRATEGY",
    "LEARN_PATTERN",
    "ANALYZE_FEEDBACK",
    "CONFIRM_PROJECT",
    "SELECT_PROJECT",
    "ANALYZE_FILE",
    "LIST_PROJECTS",
    "MULTI_AGENT",
)
_WORKFLOWSTATUS = ("PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED")
_INTENTCATEGORY = (
    "EXECUTION",
    "ANALYSIS",
    "SYNTHESIS",
    "STRATEGY",
    "PLANNING",
    "REVIEW",
    "LEARNING",
    "QUERY",
    "CONVERSATION",
    "IDENTITY",
    "DISCOVERY",
    "TEMPORAL",
    "STATUS",
    "PRIORITY",
    "GUIDANCE",
    "TRUST",
    "MEMORY",
    "PORTFOLIO",
    "PROVENANCE",
    "UNKNOWN",
)
_TASKTYPE = (
    "ANALYZE_REQUEST",
    "EXTRACT_REQUIREMENTS",
    "IDENTIFY_DEPENDENCIES",
    "CREATE_WORK_ITEM",
    "UPDATE_WORK_ITEM",
    "NOTIFY_STAKEHOLDERS",
    "GENERATE_DOCUMENT",
    "CREATE_SUMMARY",
    "GITHUB_CREATE_ISSUE",
    "GENERATE_GITHUB_ISSUE_CONTENT",
    "ANALYZE_GITHUB_ISSUE",
    "ANALYZE_FILE",
    "SUMMARIZE",
    "LIST_PROJECTS",
    "EXTRACT_WORK_ITEM",
    "JIRA_CREATE_TICKET",
    "SLACK_SEND_MESSAGE",
    "PROCESS_USER_FEEDBACK",
    "ANALYZE_DOCUMENT",
    "QUESTION_ANSWER_DOCUMENT",
    "COMPARE_DOCUMENTS",
    "SUMMARIZE_DOCUMENT",
    "SEARCH_DOCUMENTS",
)
_TASKSTATUS = ("PENDING", "RUNNING", "COMPLETED", "FAILED", "SKIPPED")

_ENUMS = {
    "workflowtype": _WORKFLOWTYPE,
    "workflowstatus": _WORKFLOWSTATUS,
    "intentcategory": _INTENTCATEGORY,
    "tasktype": _TASKTYPE,
    "taskstatus": _TASKSTATUS,
}


def _ensure_enum(name: str, labels: tuple) -> None:
    values = ", ".join(f"'{label}'" for label in labels)
    op.execute(
        f"""
        DO $$ BEGIN
            IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{name}') THEN
                CREATE TYPE {name} AS ENUM ({values});
            END IF;
        END $$;
        """
    )


def upgrade() -> None:
    bind = op.get_bind()
    existing = set(sa.inspect(bind).get_table_names())

    # Enum types first (idempotent — no-op if present).
    for name, labels in _ENUMS.items():
        _ensure_enum(name, labels)

    if "workflows" not in existing:
        op.create_table(
            "workflows",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column(
                "type",
                postgresql.ENUM(*_WORKFLOWTYPE, name="workflowtype", create_type=False),
                nullable=True,
            ),
            sa.Column(
                "status",
                postgresql.ENUM(*_WORKFLOWSTATUS, name="workflowstatus", create_type=False),
                nullable=True,
            ),
            sa.Column("input_data", sa.JSON(), nullable=True),
            sa.Column("output_data", sa.JSON(), nullable=True),
            sa.Column("context", sa.JSON(), nullable=True),
            sa.Column("result", sa.JSON(), nullable=True),
            sa.Column("error", sa.Text(), nullable=True),
            sa.Column("intent_id", sa.String(length=255), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )

    if "intents" not in existing:
        op.create_table(
            "intents",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column(
                "category",
                postgresql.ENUM(*_INTENTCATEGORY, name="intentcategory", create_type=False),
                nullable=True,
            ),
            sa.Column("action", sa.String(), nullable=True),
            sa.Column("confidence", sa.Float(), nullable=True),
            sa.Column("context", sa.JSON(), nullable=True),
            sa.Column("original_message", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("workflow_id", sa.String(), nullable=True),
            sa.ForeignKeyConstraint(["workflow_id"], ["workflows.id"]),
            sa.PrimaryKeyConstraint("id"),
        )

    if "tasks" not in existing:
        op.create_table(
            "tasks",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("workflow_id", sa.String(), nullable=True),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column(
                "type",
                postgresql.ENUM(*_TASKTYPE, name="tasktype", create_type=False),
                nullable=True,
            ),
            sa.Column(
                "status",
                postgresql.ENUM(*_TASKSTATUS, name="taskstatus", create_type=False),
                nullable=True,
            ),
            sa.Column("input_data", sa.JSON(), nullable=True),
            sa.Column("output_data", sa.JSON(), nullable=True),
            sa.Column("result", sa.JSON(), nullable=True),
            sa.Column("error", sa.Text(), nullable=True),
            sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
            sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
            sa.ForeignKeyConstraint(["workflow_id"], ["workflows.id"]),
            sa.PrimaryKeyConstraint("id"),
        )

    if "stakeholders" not in existing:
        op.create_table(
            "stakeholders",
            sa.Column("id", sa.String(), nullable=False),
            sa.Column("name", sa.String(), nullable=False),
            sa.Column("email", sa.String(), nullable=True),
            sa.Column("role", sa.String(), nullable=True),
            sa.Column("interests", sa.JSON(), nullable=True),
            sa.Column("influence_level", sa.Integer(), nullable=True),
            sa.Column("satisfaction", sa.Float(), nullable=True),
            sa.Column("created_at", sa.DateTime(timezone=True), nullable=True),
            sa.PrimaryKeyConstraint("id"),
        )


def downgrade() -> None:
    bind = op.get_bind()
    existing = set(sa.inspect(bind).get_table_names())
    # FK-safe drop order: dependents (intents, tasks → workflows) before workflows.
    for table in ("intents", "tasks", "workflows", "stakeholders"):
        if table in existing:
            op.drop_table(table)
    for name in _ENUMS:
        op.execute(f"DROP TYPE IF EXISTS {name}")
