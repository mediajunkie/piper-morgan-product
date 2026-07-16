"""#1422: re-add the preferences column the #262 merge dropped.

alpha_users.preferences (JSONB, af770c5854fe) held questionnaire answers that
PersonalityProfile.load_with_preferences, UserContextService, and the onboarding
formality writer all still read/write via ``user.preferences`` — but the #262
alpha_users->users merge (d8aeb665e878b step 3) carried 11 columns and
preferences was not one of them, so every call has raised AttributeError into a
silent-default fallback since. The old data was dropped with the table
(unrecoverable); preferences are re-collected from users going forward.

Additive and reversible.

Revision ID: k1422prefs
Revises: j1394ledger
Create Date: 2026-07-16
"""

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

revision = "k1422prefs"
down_revision = "j1394ledger"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "preferences",
            postgresql.JSONB(),
            server_default=sa.text("'{}'::jsonb"),
            nullable=True,
        ),
    )


def downgrade() -> None:
    op.drop_column("users", "preferences")
