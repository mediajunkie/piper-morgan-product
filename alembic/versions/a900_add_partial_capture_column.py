"""add_partial_capture_to_standup_conversations_issue_900

Issue #900 Phase 2: 3-part structural collection.

Adds `partial_capture` JSONB column to `standup_conversations` for the
new structured collection flow (yesterday/today/blockers). Persists
across escape/timeout → resume so partial captures aren't lost (Phase 4
behavior).

Shape: {"yesterday": [StandupItem.to_dict(), ...], "today": [...],
"blockers": [...]}.

Revision ID: a900partialcapture
Revises: a1052standupconv
Create Date: 2026-05-05 11:55:00.000000

"""

from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a900partialcapture"
down_revision: Union[str, Sequence[str], None] = "a1052standupconv"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add partial_capture column to standup_conversations."""
    op.add_column(
        "standup_conversations",
        sa.Column(
            "partial_capture",
            postgresql.JSONB(),
            nullable=False,
            server_default=sa.text("""'{"yesterday": [], "today": [], "blockers": []}'::jsonb"""),
        ),
    )


def downgrade() -> None:
    """Remove partial_capture column."""
    op.drop_column("standup_conversations", "partial_capture")
