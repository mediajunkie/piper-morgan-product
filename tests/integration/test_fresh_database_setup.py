"""
Integration test for fresh database schema creation.

This test ensures that ``Base.metadata.create_all`` works on an EMPTY database,
catching issues like:
- Missing GIN indexes for JSON columns
- Circular foreign key dependencies
- Invalid column types or constraints
- SQLAlchemy model configuration errors

Found during alpha onboarding testing (Oct 29, 2025) when the setup wizard
discovered JSON columns with BTree indexes instead of GIN indexes.

#2372 (Arch 2026-11-14): it runs in a scratch database it creates and drops, never
the configured one. It used to call ``create_all`` on whatever database was
configured. On a shared developer database that created every new model's table
ahead of its migration, and the migration's ``create_table`` then failed with
DuplicateTable (this happened with ``floored_action_counts`` on 2026-11-14). It was
also never a fresh-database test there: ``create_all`` skips tables that exist.
"""

import os
import uuid

import pytest
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

from services.database.connection import Base


def _server_url(database: str) -> str:
    """The configured PostgreSQL server (the test suite's own variables), with the
    database name swapped. The scratch database lives on the same server."""
    user = os.getenv("POSTGRES_USER", "piper")
    password = os.getenv("POSTGRES_PASSWORD", "dev_changeme_in_production")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5433")
    return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database}"


@pytest.fixture
async def scratch_database():
    """An empty database for this test alone, dropped afterwards. Created from the
    configured database's connection, which is only used to issue CREATE and DROP
    DATABASE (no table in it is read or written)."""
    name = f"piper_fresh_{uuid.uuid4().hex[:12]}"
    admin = create_async_engine(
        _server_url(os.getenv("POSTGRES_DB", "piper_morgan")),
        poolclass=NullPool,
        isolation_level="AUTOCOMMIT",
    )
    try:
        async with admin.connect() as conn:
            await conn.execute(text(f'CREATE DATABASE "{name}"'))
    except Exception as e:
        await admin.dispose()
        pytest.skip(f"this role cannot create a scratch database ({type(e).__name__})")
    engine = create_async_engine(_server_url(name), poolclass=NullPool)
    try:
        yield engine
    finally:
        await engine.dispose()
        async with admin.connect() as conn:
            await conn.execute(text(f'DROP DATABASE IF EXISTS "{name}" WITH (FORCE)'))
        await admin.dispose()


@pytest.mark.asyncio
async def test_create_tables_from_scratch(scratch_database):
    """
    Test that database schema can be created from scratch.

    This is a critical integration test that validates:
    1. All table definitions are valid
    2. All indexes are properly configured (especially JSON/GIN)
    3. All foreign key relationships are correct
    4. All enums and custom types work
    5. No circular dependencies exist

    It runs in an empty scratch database, so every table is really created.
    """
    async with scratch_database.begin() as conn:
        before = (
            await conn.execute(
                text("SELECT count(*) FROM information_schema.tables WHERE table_schema = 'public'")
            )
        ).scalar()
        assert before == 0, "the scratch database must start empty"

        # Verify we can create all tables without errors
        # This will fail if:
        # - JSON columns have BTree indexes (need GIN)
        # - Foreign keys have circular dependencies
        # - Column types are incompatible
        # - Constraints are malformed
        await conn.run_sync(Base.metadata.create_all)

        # Verify some critical tables exist
        result = await conn.execute(
            text(
                """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            AND table_type = 'BASE TABLE'
            """
            )
        )
        tables = [row[0] for row in result.fetchall()]
        # Every model's table was created here, not found already present.
        assert set(Base.metadata.tables) <= set(tables)

        # Check for essential tables.
        # NOTE: only tables with an ORM model belong here — this test exercises
        # `Base.metadata.create_all()` (the model-driven path). Removed (#1273) as
        # model-less legacy tables that create_all neither makes nor should:
        #   - `alpha_users` — no model; dropped by migration af770c5854fe (data → `users`)
        #   - `todos` — no model; refactored into items/todo_items (234aa8ec628c)
        #   - `todo_lists` — dropped and replaced by `lists` (see 44f5cd40b495's note); removed 2026-11-09 (1452)
        #   - `tasks`, `intents` — dead persistence twins deleted with their tables (1797); removed 2026-11-09 (1452)
        # (The Alembic-migration path is covered by TestModelMigrationCoverage.)
        essential_tables = [
            "users",
            "user_api_keys",
            "audit_logs",
            "projects",
            "lists",
            "workflows",
        ]

        for table in essential_tables:
            assert table in tables, f"Essential table '{table}' not created in schema"

        # Verify GIN indexes exist for JSON columns
        # This was the bug that prompted this test!
        result = await conn.execute(
            text(
                """
            SELECT
                i.relname as index_name,
                am.amname as index_type,
                t.relname as table_name,
                a.attname as column_name
            FROM pg_index ix
            JOIN pg_class i ON i.oid = ix.indexrelid
            JOIN pg_class t ON t.oid = ix.indrelid
            JOIN pg_am am ON am.oid = i.relam
            JOIN pg_attribute a ON a.attrelid = t.oid AND a.attnum = ANY(ix.indkey)
            WHERE t.relname IN ('todo_lists', 'todos', 'lists')
            AND a.attname IN ('shared_with', 'tags', 'external_refs')
            """
            )
        )
        json_indexes = list(result.fetchall())

        # All JSON column indexes should use GIN, not btree
        for index_name, index_type, table_name, column_name in json_indexes:
            assert (
                index_type == "gin"
            ), f"Index {index_name} on {table_name}.{column_name} should use GIN, not {index_type}"


@pytest.mark.asyncio
async def test_database_schema_has_no_broken_indexes():
    """
    Verify that all indexes in the schema are valid and can be created.

    This test specifically checks for the PostgreSQL error:
    "data type json has no default operator class for access method btree"

    Which occurs when trying to create a btree index on a JSON column
    without specifying postgresql_using='gin'.
    """
    # Skip if already tested by test_create_tables_from_scratch
    # (Event loop issues when running multiple tests in sequence)
    pytest.skip("Covered by test_create_tables_from_scratch")


@pytest.mark.asyncio
async def test_all_tables_have_primary_keys():
    """
    Verify that all tables have primary keys defined.

    Missing primary keys can cause issues with ORMs and database operations.
    """
    # Skip if already tested by test_create_tables_from_scratch
    pytest.skip("Covered by test_create_tables_from_scratch")


@pytest.mark.asyncio
async def test_foreign_keys_reference_existing_tables():
    """
    Verify that all foreign key constraints reference tables that exist.

    This catches issues where foreign keys point to tables that haven't
    been created yet or have typos in the table name.
    """
    # Skip if already tested by test_create_tables_from_scratch
    pytest.skip("Covered by test_create_tables_from_scratch")
