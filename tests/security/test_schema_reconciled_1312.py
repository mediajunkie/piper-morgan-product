"""#1312 — the autogen-empty guard: model and database must never drift again.

The #1312 audit found ~41 accumulated autogenerate ops: orphan models whose
tables were never created (todo_lists), DB-side DDL whose models were never
merged (the MUX 601 family, SEC-RBAC owner_id columns), name-mismatched FKs,
and dead indexes. Reconciliation closed all of it (model-side declarations +
the h1312recon migration). This guard makes the end state — EMPTY autogenerate
diff — a CI invariant instead of a one-time achievement.

Runs against the REAL local/CI Postgres at migrated head (house pattern for
tests/security/). If the DB is unreachable, it SKIPS (unit lanes without
Postgres); the Postgres CI suite is where it has teeth. If it fails for you:
either your DB isn't at `alembic upgrade head`, or you changed a model without
a migration (or vice versa) — resolve per the #1312 discipline: model = DB
truth, additive park-with-model first, deliberate DDL only when reviewed.
"""

import pytest
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool


def _db_engine_or_skip():
    from services.database.session_factory import get_sync_migration_url

    engine = create_engine(get_sync_migration_url(), poolclass=NullPool)
    try:
        with engine.connect():
            pass
    except sqlalchemy.exc.OperationalError:
        pytest.skip("Postgres unreachable — autogen guard runs in the Postgres suite")
    return engine


class TestSchemaReconciled:
    def test_autogenerate_diff_is_empty(self):
        """alembic autogenerate against the migrated DB proposes NOTHING."""
        from alembic.autogenerate import compare_metadata
        from alembic.migration import MigrationContext
        from alembic.runtime.environment import EnvironmentContext
        from alembic.script import ScriptDirectory
        from alembic.config import Config

        # the app's full metadata — MUST mirror alembic/env.py's import set
        # exactly (every module registering tables on the shared Base):
        import services.database.models  # noqa: F401
        import services.persistence.models  # noqa: F401
        from services.database.connection import Base

        engine = _db_engine_or_skip()

        # refuse to compare against a stale DB — that's a different failure
        cfg = Config("alembic.ini")
        script = ScriptDirectory.from_config(cfg)
        head = script.get_current_head()
        with engine.connect() as conn:
            current = MigrationContext.configure(conn).get_current_revision()
            if current != head:
                pytest.skip(
                    f"DB at {current}, head is {head} — run `alembic upgrade head` first"
                )

            mc = MigrationContext.configure(
                conn,
                opts={"compare_type": False, "compare_server_default": False},
            )
            diffs = compare_metadata(mc, Base.metadata)

        assert diffs == [], (
            "Model↔DB drift reintroduced (#1312 was fully reconciled 2026-07-09). "
            "Every entry below is a model change without a migration or DDL without "
            f"a model:\n" + "\n".join(f"  - {d}" for d in diffs)
        )
