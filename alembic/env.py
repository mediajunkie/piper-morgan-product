from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Import your SQLAlchemy Base
from services.database.connection import Base

# #1312: autogenerate compares target_metadata to the DB, so every module that
# registers tables on the shared Base MUST be imported here — otherwise its
# tables read as false-positive "removed table" drift (action_humanizations
# did, before persistence.models was imported). If you add a module here, add
# it to tests/security/test_schema_reconciled_1312.py too — the autogen-empty
# guard mirrors this import set. (The old multi-Base exception is gone:
# services/personality/models.py was a stale duplicate, deleted 2026-07-09
# per the Arch ruling; one Base per DB is now lint-enforced.)
import services.database.models  # noqa: E402,F401
import services.persistence.models  # noqa: E402,F401

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


# #1299(a): env-driven migration URL lives with the DB layer (testable; shared).
from services.database.session_factory import get_sync_migration_url as _resolve_db_url


def _compare_type(context, inspected_column, metadata_column, inspected_type, metadata_type):
    """#1312: make ``compare_against_backend`` authoritative for autogenerate.

    Alembic's default type comparison inspects the dialect impl of a
    TypeDecorator (EncryptedJSON loads as JSONB on Postgres), so the decorator's
    own ``compare_against_backend`` (which declares the whole JSON family
    equivalent — ciphertext is valid JSON under json OR jsonb) never gets
    consulted, and every encrypted-JSON column re-drifts in every run.
    Returning False = "types are the same"; None falls back to the default.
    """
    hook = getattr(metadata_type, "compare_against_backend", None)
    if callable(hook):
        same = hook(context.dialect, inspected_type)
        if same is not None:
            return not same
    return None


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = _resolve_db_url()  # #1299(a): env-driven, not the hardcoded ini value
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=_compare_type,  # #1312
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    # #1299(a): override the ini's hardcoded sqlalchemy.url with the env-resolved URL.
    # Set it on the section dict (not via config.set_main_option) to bypass ConfigParser
    # %-interpolation — DB passwords can contain '%'.
    section = config.get_section(config.config_ini_section, {})
    section["sqlalchemy.url"] = _resolve_db_url()
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            # PostgreSQL supports transactional DDL, but we disable it here to allow
            # individual migrations to fail without rolling back all previous migrations.
            # This is important for development and testing environments where we want
            # partial progress even if some migrations fail.
            transaction_per_migration=True,
            compare_type=_compare_type,  # #1312
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
