# Database Setup Guide

**Last Updated**: October 31, 2026 (rewritten against the current code, issue #1904)

## Overview

Piper Morgan uses PostgreSQL through SQLAlchemy async (asyncpg) and Alembic migrations. Hosted environments run on Fly.io with Postgres on Fly. Local development uses Docker Compose.

Deploy, backup and incident procedure for the hosted databases lives in internal runbooks, not here:

- [alpha-deployment-runbook.md](internal/operations/alpha-deployment-runbook.md)
- [deploy-environments-and-release-train.md](internal/operations/deploy-environments-and-release-train.md)
- [alpha-fly-cutover-runbook-2026-09-22.md](internal/operations/alpha-fly-cutover-runbook-2026-09-22.md) (the move from the old droplet, with dump and snapshot steps)
- [staging-fly-setup-2026-09-22.md](internal/operations/staging-fly-setup-2026-09-22.md)

## Local development

`docker-compose.yml` runs `postgres:15` with container name `piper-postgres`, host port 5433 mapped to 5432, and the named volume `piper_postgres_data_v1`.

```bash
docker compose up -d
python -m alembic upgrade head
```

Connection settings are read by `services/database/connection.py`. If `DATABASE_URL` is set it wins (this is how Fly supplies it). Otherwise these variables apply, with these defaults:

| Variable | Default |
|---|---|
| `POSTGRES_HOST` | `localhost` |
| `POSTGRES_PORT` | `5433` |
| `POSTGRES_DB` | `piper_morgan` |
| `POSTGRES_USER` | `piper` |
| `POSTGRES_PASSWORD` | a development placeholder, set your own anywhere that matters |
| `POSTGRES_SSL_MODE` | `prefer` |

`POSTGRES_SSL_ROOT_CERT`, `POSTGRES_SSL_CERT` and `POSTGRES_SSL_KEY` are added to the URL when set. Valid SSL modes are the standard PostgreSQL ones (`disable`, `prefer`, `require`, `verify-ca`, `verify-full`). The code passes the value to asyncpg as `ssl=<mode>`.

## Connection pool

From `services/database/connection.py` (`DatabaseConnection.initialize`):

- `pool_size=10`, `max_overflow=20`, `pool_timeout=30`
- `pool_pre_ping=True` and `pool_recycle=600`, because Fly's proxy closes idle database connections without telling the pool (issues 2085 and 2101 are cited in the code comment)

A global instance `db = DatabaseConnection()` is exported from that module.

## Migrations

Alembic config is `alembic.ini` and the revisions are in `alembic/versions/`.

```bash
python -m alembic upgrade head
python -m alembic current
python -m alembic revision --autogenerate -m "description"   # review the generated file before applying
```

On Fly, `fly.toml` sets `release_command = "python -m alembic upgrade head"`, so each deploy migrates a temporary machine against the app's database before the new version starts. CI also runs `alembic upgrade head` against a fresh Postgres in `.github/workflows/test.yml`.

The revision graph currently has one head, `s2014items` (`alembic/versions/s2014items_base_item_has_list.py`), found by reading the revision chain in `alembic/versions/` (89 files at the time of writing). Do not copy a head id from this page. Run `python -m alembic heads`.

## Health endpoints

`web/api/routes/health.py` mounts these under `/api/v1/health`:

- `GET /api/v1/health` basic status
- `GET /api/v1/health/database` database check (returns 503 if the connection fails)
- `GET /api/v1/health/detailed` database plus system resources

`fly.toml` also configures a check on path `/health`. The alpha runbook describes `/health` as the unauthenticated deploy-identity check (version and git sha).

## Hosted databases

- Production-side apps run on Fly. The Postgres app for alpha is `piper-morgan-db` according to the cutover runbook. Staging is the separate app `piper-morgan-staging`.
- `restart-alpha-postgres.yml` is a guarded workflow for restarting alpha's Postgres machine. Its header comments explain when it applies.
- For backups and restores, use the Fly volume snapshots and `pg_dump` over `fly proxy` described in the cutover runbook, and follow the current runbook rather than any command copied from this page.

## Local backup

```bash
docker exec piper-postgres pg_dump -U piper piper_morgan > backup.sql
docker exec -i piper-postgres psql -U piper piper_morgan < backup.sql
```

## Troubleshooting (local)

- **Connection refused on 5433.** Run `docker ps | grep postgres`, then `docker compose up -d postgres`, then `docker logs piper-postgres`.
- **SSL errors.** Try `POSTGRES_SSL_MODE=disable` locally to separate a certificate problem from a connection problem.
- **`QueuePool limit ... reached`.** Look for sessions that are never closed before raising pool sizes.
- **Alembic cannot connect inside the app container.** Read the 2026-06-22 correction in the alpha deployment runbook. `alembic.ini` carries a development URL and the container reaches Postgres at a different host and port.

## Not verified here

- The Postgres major version on Fly (the compose file pins 15, CI uses 16, and the Fly app version was not checked).
- The name `piper-morgan-db` is taken from the cutover runbook, not from a live `fly` command.
- Behavior of each SSL mode against Fly Postgres (only the code path that builds the URL was read).
- That `/health` returns what the alpha runbook says (the route's code was not located, only the `fly.toml` check path and the runbook).
- The performance tests file `tests/performance/test_database_performance.py` exists, but its current pass state and the old benchmark figures were not re-run, so the figures were removed.
- Retention and schedule of Fly volume snapshots (the cutover runbook mentions daily snapshots with 5-day retention as of September 2026).
