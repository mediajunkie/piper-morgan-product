"""Create orchestration tables: workflows, intents, tasks, stakeholders (Issue #942)

These models existed in services/database/models.py but had no migration.
The test_workflow_repository_migration test was failing because the workflows
table did not exist.

Revision ID: b942_orchestration_tables
Revises: a715_conv_lifecycle
Create Date: 2026-04-07
"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "b942_orchestration_tables"
down_revision: Union[str, Sequence[str], None] = "a715_conv_lifecycle"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    from sqlalchemy import text

    conn = op.get_bind()

    # Create enum types that don't already exist
    for enum_name, values in [
        (
            "workflowtype",
            ["CREATE_TASK", "ANALYZE_FILE", "GENERATE_REPORT", "EXTRACT_WORK_ITEM", "SUMMARIZE"],
        ),
        ("workflowstatus", ["PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED"]),
        (
            "intentcategory",
            [
                "EXECUTION",
                "QUERY",
                "CONVERSATION",
                "DISCOVERY",
                "GUIDANCE",
                "TRUST",
                "IDENTITY",
                "MEMORY",
                "UNKNOWN",
            ],
        ),
        ("taskstatus", ["PENDING", "RUNNING", "COMPLETED", "FAILED", "CANCELLED"]),
    ]:
        exists = conn.execute(
            text(f"SELECT 1 FROM pg_type WHERE typname = '{enum_name}'")
        ).fetchone()
        if not exists:
            values_str = ", ".join(f"'{v}'" for v in values)
            conn.execute(text(f"CREATE TYPE {enum_name} AS ENUM ({values_str})"))

    # Use raw DDL to avoid SQLAlchemy Enum create_type hooks fighting with pre-existing types
    conn.execute(
        text("""
        CREATE TABLE workflows (
            id VARCHAR NOT NULL PRIMARY KEY,
            type workflowtype,
            status workflowstatus,
            input_data JSON,
            output_data JSON,
            context JSON,
            result JSON,
            error TEXT,
            intent_id VARCHAR(255),
            created_at TIMESTAMP WITH TIME ZONE,
            started_at TIMESTAMP WITH TIME ZONE,
            completed_at TIMESTAMP WITH TIME ZONE,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """)
    )

    conn.execute(
        text("""
        CREATE TABLE intents (
            id VARCHAR NOT NULL PRIMARY KEY,
            category intentcategory,
            action VARCHAR,
            confidence FLOAT,
            context JSON,
            original_message TEXT,
            created_at TIMESTAMP WITH TIME ZONE,
            workflow_id VARCHAR REFERENCES workflows(id)
        )
    """)
    )

    conn.execute(
        text("""
        CREATE TABLE tasks (
            id VARCHAR NOT NULL PRIMARY KEY,
            workflow_id VARCHAR REFERENCES workflows(id),
            name VARCHAR NOT NULL,
            type tasktype,
            status taskstatus,
            input_data JSON,
            output_data JSON,
            result JSON,
            error TEXT,
            started_at TIMESTAMP WITH TIME ZONE,
            completed_at TIMESTAMP WITH TIME ZONE,
            created_at TIMESTAMP WITH TIME ZONE,
            updated_at TIMESTAMP WITH TIME ZONE
        )
    """)
    )

    conn.execute(
        text("""
        CREATE TABLE stakeholders (
            id VARCHAR NOT NULL PRIMARY KEY,
            name VARCHAR NOT NULL,
            email VARCHAR,
            role VARCHAR,
            interests JSON,
            influence_level INTEGER,
            satisfaction FLOAT,
            created_at TIMESTAMP WITH TIME ZONE
        )
    """)
    )


def downgrade() -> None:
    op.drop_table("stakeholders")
    op.drop_table("tasks")
    op.drop_table("intents")
    op.drop_table("workflows")
