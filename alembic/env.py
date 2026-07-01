from logging.config import fileConfig

from sqlalchemy import engine_from_config, pool

from alembic import context

# Import your SQLAlchemy Base
from services.database.connection import Base

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
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
