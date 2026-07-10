"""#1278 — externally-supplied DATABASE_URLs must work for BOTH engines.

The Fly deploy failed twice on this seam (2026-07-10):
1. Fly's ``postgres attach`` sets ``DATABASE_URL=postgres://…`` — SQLAlchemy
   2.x removed the ``postgres`` scheme alias, so the migrate release-command
   died with ``NoSuchModuleError: sqlalchemy.dialects:postgres``.
2. The async resolver (`_get_database_url`) didn't honor DATABASE_URL AT ALL —
   the app would have built a localhost URL from POSTGRES_* defaults and
   crash-looped even after the migrate was fixed.
Also: asyncpg rejects ``?sslmode=`` (a libpq-ism Fly appends) as a connect
kwarg — translated/dropped for the async driver.
"""

from unittest.mock import patch

from services.database.session_factory import (
    _get_database_url,
    _normalize_pg_url,
    get_sync_migration_url,
)

FLY_URL = "postgres://piper_morgan:pw@piper-morgan-db.flycast:5432/piper_morgan?sslmode=disable"


class TestNormalize:
    def test_fly_attach_url_sync(self):
        assert _normalize_pg_url(FLY_URL, driver="sync") == (
            "postgresql://piper_morgan:pw@piper-morgan-db.flycast:5432/piper_morgan?sslmode=disable"
        )

    def test_fly_attach_url_async_drops_sslmode_disable(self):
        assert _normalize_pg_url(FLY_URL, driver="async") == (
            "postgresql+asyncpg://piper_morgan:pw@piper-morgan-db.flycast:5432/piper_morgan"
        )

    def test_sslmode_require_becomes_ssl_true_for_asyncpg(self):
        url = "postgres://u:p@h:5432/db?sslmode=require"
        assert _normalize_pg_url(url, driver="async") == (
            "postgresql+asyncpg://u:p@h:5432/db?ssl=true"
        )

    def test_already_canonical_urls_pass_through(self):
        assert (
            _normalize_pg_url("postgresql://u:p@h/db", driver="sync")
            == "postgresql://u:p@h/db"
        )
        assert (
            _normalize_pg_url("postgresql+asyncpg://u:p@h/db", driver="async")
            == "postgresql+asyncpg://u:p@h/db"
        )

    def test_async_to_sync(self):
        assert (
            _normalize_pg_url("postgresql+asyncpg://u:p@h/db", driver="sync")
            == "postgresql://u:p@h/db"
        )


class TestResolvers:
    def test_app_engine_honors_database_url(self):
        """THE Fly gap: the async resolver must read DATABASE_URL."""
        with patch.dict("os.environ", {"DATABASE_URL": FLY_URL}):
            assert _get_database_url() == (
                "postgresql+asyncpg://piper_morgan:pw@piper-morgan-db.flycast:5432/piper_morgan"
            )

    def test_migrate_honors_database_url_with_legacy_scheme(self):
        with patch.dict("os.environ", {"DATABASE_URL": FLY_URL}, clear=False):
            import os

            os.environ.pop("ALEMBIC_DATABASE_URL", None)
            assert get_sync_migration_url().startswith("postgresql://piper_morgan:")

    def test_no_database_url_keeps_local_defaults(self):
        import os

        env = {k: v for k, v in os.environ.items() if k not in (
            "DATABASE_URL", "ALEMBIC_DATABASE_URL", "POSTGRES_USER",
            "POSTGRES_PASSWORD", "POSTGRES_HOST", "POSTGRES_PORT", "POSTGRES_DB",
        )}
        with patch.dict("os.environ", env, clear=True):
            assert _get_database_url() == (
                "postgresql+asyncpg://piper:dev_changeme_in_production@localhost:5433/piper_morgan"
            )
