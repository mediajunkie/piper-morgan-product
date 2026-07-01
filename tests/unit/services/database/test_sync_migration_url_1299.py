"""#1299(a) — alembic migration URL resolves from the ENVIRONMENT, not a hardcoded ini.

The hardcoded `sqlalchemy.url = ...@localhost:5433` meant the in-container migrate
connected to localhost:5433 (wrong — postgres is at postgres:5432 there) and failed
silently on every deploy → the hollow 0.8.8. `get_sync_migration_url` (used by
alembic/env.py) fixes it: env-driven, sync driver, local-dev default preserved.
"""

from unittest.mock import patch

from services.database.session_factory import get_sync_migration_url


def test_local_dev_default_preserved():
    """No env → localhost:5433 (local dev unaffected), SYNC driver (no +asyncpg)."""
    with patch.dict("os.environ", {}, clear=True):
        url = get_sync_migration_url()
    assert url == "postgresql://piper:dev_changeme_in_production@localhost:5433/piper_morgan"
    assert "+asyncpg" not in url


def test_container_env_resolves_correctly_1299():
    """The container case (POSTGRES_HOST=postgres, port 5432) — the bug this fixes."""
    with patch.dict(
        "os.environ",
        {"POSTGRES_HOST": "postgres", "POSTGRES_PORT": "5432", "POSTGRES_PASSWORD": "prod"},
        clear=True,
    ):
        url = get_sync_migration_url()
    assert url == "postgresql://piper:prod@postgres:5432/piper_morgan"


def test_explicit_database_url_override_normalized_to_sync():
    """An explicit (possibly async) DATABASE_URL is honored + normalized to the sync driver."""
    with patch.dict(
        "os.environ",
        {"DATABASE_URL": "postgresql+asyncpg://u:p@db.example:5432/piper"},
        clear=True,
    ):
        url = get_sync_migration_url()
    assert url == "postgresql://u:p@db.example:5432/piper"
    assert "+asyncpg" not in url


def test_alembic_database_url_takes_precedence():
    with patch.dict(
        "os.environ",
        {
            "ALEMBIC_DATABASE_URL": "postgresql://a:b@alembic-host:5432/x",
            "DATABASE_URL": "postgresql://c:d@other:5432/y",
            "POSTGRES_HOST": "ignored",
        },
        clear=True,
    ):
        url = get_sync_migration_url()
    assert url == "postgresql://a:b@alembic-host:5432/x"
