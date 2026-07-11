"""#1312 schema reconciliation — the five reviewed DDL ops closing model↔DB drift.

The #1312 drift audit (2026-07-08 inventory → Arch three-rulings memo → PM product
confirm 2026-07-09) resolved ~41 autogenerate ops. Almost all were closed
MODEL-side (park-with-model / FK-name declarations / the todo_lists orphan
excise, PM-confirmed) with zero DDL. These five are the remainder — the only
ops where the DATABASE is the side that changes, each deliberate:

1+2. DROP the two GIN indexes on conversation_turns.entities/.references.
     Those columns are EncryptedJSON (#358): the GIN trees index ciphertext
     tokens — unsearchable by design, pure write amplification on every turn.

3+4. CREATE idx_conversations_user_session + idx_files_owner. Both declared in
     the models for their real query paths; never materialized in the DB.

5.   DROP user_api_keys_user_id_fkey1 — an exact-duplicate FK (same column,
     same target) alongside user_api_keys_user_id_fkey. Two enforcers of the
     same constraint; the named survivor is declared in the model (CASCADE).

After this revision, `alembic revision --autogenerate` against a head-migrated
DB produces an EMPTY diff — enforced from here on by the autogen-empty guard
(tests/security/test_schema_reconciled_1312.py).

Revision ID: h1312recon
Revises: g1382creds
Create Date: 2026-07-09
"""

from alembic import op

revision = "h1312recon"
down_revision = "g1382creds"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1+2: GIN over ciphertext — drop (idempotent: droplet/local may drift)
    op.execute("DROP INDEX IF EXISTS idx_conversation_turns_entities")
    op.execute("DROP INDEX IF EXISTS idx_conversation_turns_references")

    # 3+4: model-declared indexes that never reached the DB
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_conversations_user_session "
        "ON conversations (user_id, session_id)"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_files_owner "
        "ON uploaded_files (owner_id, upload_time)"
    )

    # 5: the duplicate FK (keep the named CASCADE one the model declares)
    op.execute(
        "ALTER TABLE user_api_keys DROP CONSTRAINT IF EXISTS user_api_keys_user_id_fkey1"
    )


def downgrade() -> None:
    op.execute(
        "ALTER TABLE user_api_keys ADD CONSTRAINT user_api_keys_user_id_fkey1 "
        "FOREIGN KEY (user_id) REFERENCES users (id)"
    )
    op.execute("DROP INDEX IF EXISTS idx_files_owner")
    op.execute("DROP INDEX IF EXISTS idx_conversations_user_session")
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_conversation_turns_references "
        "ON conversation_turns USING gin (\"references\")"
    )
    op.execute(
        "CREATE INDEX IF NOT EXISTS idx_conversation_turns_entities "
        "ON conversation_turns USING gin (entities)"
    )
