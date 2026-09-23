"""a1599admin's zero-row guard keys on the DATABASE's state, not on an env var.

Pard's finding (2026-09-23): the guard was `if os.environ.get("FLY_APP_NAME")`,
which meant "production" while there was one Fly app and meant "any Fly app"
the moment staging existed — staging's first deploy failed at this revision on
an empty database. The rule now: `users` empty → fresh environment, warn and
no-op; `users` populated but no PM row → the silent-no-op failure #1599
exists to catch → raise.

LAYER (m-43): the migration's own `upgrade()` executed through a real alembic
`Operations` context against the dev Postgres, with a TEMP `users` table that
shadows `public.users` on the session's search_path — so the SQL is the SQL
that runs on a release machine, the transaction is rolled back, and nothing in
the real `users` table is touched. DENOMINATOR (m-44): the three states the
guard distinguishes (empty / PM present / populated-without-PM); FLY_APP_NAME
is set in one of them to prove it no longer participates.
"""

from __future__ import annotations

import importlib.util
import os
from pathlib import Path

import pytest
import sqlalchemy as sa

from alembic.migration import MigrationContext
from alembic.operations import Operations

pytestmark = pytest.mark.integration

_MIGRATION = (
    Path(__file__).resolve().parents[2]
    / "alembic"
    / "versions"
    / "a1599admin_grant_is_admin_to_pm_beta_username_1599.py"
)


def _sync_db_url() -> str:
    user = os.getenv("POSTGRES_USER", "piper")
    pw = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    db = os.getenv("POSTGRES_DB", "piper_morgan")
    return f"postgresql://{user}:{pw}@{host}:{port}/{db}"


@pytest.fixture(scope="module")
def migration():
    spec = importlib.util.spec_from_file_location("a1599admin", _MIGRATION)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def engine():
    eng = sa.create_engine(_sync_db_url())
    try:
        with eng.connect():
            pass
    except Exception as e:  # silent-ok: infra absence is a skip, not a verdict
        pytest.skip(f"dev Postgres not reachable: {e}")
    return eng


def _run_upgrade(engine, migration, *seed_rows: tuple[str, bool]):
    """Execute upgrade() against a shadowing TEMP users table; roll back after."""
    with engine.connect() as conn:
        conn.execute(
            sa.text("CREATE TEMP TABLE users (username text, is_admin boolean DEFAULT false)")
        )
        for username, is_admin in seed_rows:
            conn.execute(
                sa.text("INSERT INTO users VALUES (:u, :a)"), {"u": username, "a": is_admin}
            )
        try:
            with Operations.context(MigrationContext.configure(conn)):
                migration.upgrade()
            return conn.execute(sa.text("SELECT username, is_admin FROM users")).fetchall()
        finally:
            conn.rollback()


def test_empty_users_is_a_fresh_environment_and_no_ops(engine, migration, monkeypatch, capsys):
    """Staging's case: empty database → warned no-op, even on a Fly release machine."""
    monkeypatch.setenv("FLY_APP_NAME", "piper-morgan-staging")
    rows = _run_upgrade(engine, migration)
    assert rows == []
    assert "fresh database" in capsys.readouterr().out


def test_pm_row_present_is_granted(engine, migration):
    rows = _run_upgrade(engine, migration, ("dinp", False), ("someone", False))
    assert dict(rows) == {"dinp": True, "someone": False}


def test_populated_without_pm_row_raises(engine, migration, monkeypatch):
    """The #1599 failure itself: a real population where the grant matched nothing."""
    monkeypatch.delenv("FLY_APP_NAME", raising=False)
    with pytest.raises(RuntimeError, match="populated database \\(2 users"):
        _run_upgrade(engine, migration, ("alice", False), ("bob", False))
