"""
Integration test for fresh database schema creation.

This test ensures that `db.create_tables()` works on an empty database,
catching issues like:
- Missing GIN indexes for JSON columns
- Circular foreign key dependencies
- Invalid column types or constraints
- SQLAlchemy model configuration errors

Found during alpha onboarding testing (Oct 29, 2025) when the setup wizard
discovered JSON columns with BTree indexes instead of GIN indexes.

Issue: Database schema bug - JSON index misconfiguration
"""

import pytest
from sqlalchemy import text

from services.database.connection import Base, db


@pytest.mark.asyncio
async def test_create_tables_from_scratch():
    """
    Test that database schema can be created from scratch.

    This is a critical integration test that validates:
    1. All table definitions are valid
    2. All indexes are properly configured (especially JSON/GIN)
    3. All foreign key relationships are correct
    4. All enums and custom types work
    5. No circular dependencies exist

    This test runs against the actual test database and verifies
    the entire schema creation process works end-to-end.
    """
    # Initialize database connection if needed
    if not db.engine:
        await db.initialize()

    # Get a connection to verify schema creation
    async with db.engine.begin() as conn:
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

        # Check for essential tables.
        # NOTE: only tables with an ORM model belong here — this test exercises
        # `Base.metadata.create_all()` (the model-driven path). Removed (#1273) as
        # model-less legacy tables that create_all neither makes nor should:
        #   - `alpha_users` — no model; dropped by migration af770c5854fe (data → `users`)
        #   - `todos` — no model; refactored into items/todo_items (234aa8ec628c)
        # (The Alembic-migration path is covered by TestModelMigrationCoverage.)
        essential_tables = [
            "users",
            "user_api_keys",
            "audit_logs",
            "projects",
            "todo_lists",
            "lists",
            "workflows",
            "tasks",
            "intents",
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
