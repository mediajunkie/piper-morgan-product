# Environment Status

**Last Updated**: 2026-08-11 (Lead Dev) — refreshed after Docs flagged the November 2025 snapshot
~9 months stale. Every value below was **read from the live environment**, not carried forward.

## Current Status

| Environment | Migration | App Version | Database Size | Status |
|-------------|-----------|-------------|---------------|--------|
| Development | `l1466slack` (head) | 0.8.11.0 | 18 MB | ✓ up (postgres/redis/chromadb healthy) |
| Test | — | — | — | not a standing environment; suites run against dev Postgres :5433 |
| Staging | — | — | — | none provisioned |
| Production (Fly.io) | **not verified** — see below | release **v48**, machine `2869e7ec495248` (sjc), 1/1 checks passing | not verified | ✓ started |

⚠️ **Two production cells read "not verified" deliberately.** `fly ssh console -C "alembic current"`
was blocked from this seat, and a production migration/DB-size figure is exactly the kind of number
that gets copied forward for nine months once someone guesses it. An unverified cell is worth more
than a plausible one — fill these in only from an actual read (m-44: "clear" is not a measurement).

**Naming note**: production runs on **Fly.io** (`piper-morgan.fly.dev`, #1278), which did not exist
when this file was last written. The old "Development environment only (no staging/production yet)"
line is retired.

## Update Instructions

Run these and paste the actual output — do not carry a prior value forward.

```bash
# Dev containers must be up first (they do NOT survive an Amber reboot — see below)
docker compose up -d postgres redis chromadb
docker ps --format '{{.Names}}\t{{.Status}}'

# Current migration (env-strip: a Claude Code shell exports an EMPTY ANTHROPIC_API_KEY)
env -u ANTHROPIC_API_KEY -u ANTHROPIC_BASE_URL -u ANTHROPIC_AUTH_TOKEN -u ANTHROPIC_CUSTOM_HEADERS \
  POSTGRES_PORT=5433 venv/bin/alembic current

# Database size
docker exec piper-postgres psql -U piper -d piper_morgan \
  -c "SELECT pg_size_pretty(pg_database_size('piper_morgan'));"

# App version
grep -m1 '^version' pyproject.toml

# Production (from the shared checkout)
cd /Users/xian/Development/piper-morgan-product && fly status && fly releases
```

⚠️ **Verify a deploy with `fly status` / `fly releases`, never a bare `curl /health`** — `/health`
returns 200 from the *old* machine while a new one is still rolling. This nearly produced a false
all-clear on 2026-08-10.

## Operational notes

- 🔴 **Docker containers do NOT restart after an Amber reboot.** Found 2026-08-11: `piper-postgres`,
  `piper-redis`, and `piper-chromadb` were all `Exited (255)` six hours after the macOS 26.6 reboot,
  with nothing having restarted them. Nothing alerts on this — the first symptom is a connection
  error in whatever you were doing. **After any host reboot, run `docker compose up -d postgres
  redis chromadb` before assuming the dev environment works.** (`piper-ghmcp` came back on its own;
  the data services did not.)
- Dev Postgres is on **port 5433**, not 5432. Redis 6379, ChromaDB 8000, app server 8001.
- Database runs in the Docker container `piper-postgres`; volume `piper_postgres_data`.

## Migration History

### 2026-08-11 — status refresh (no migration)
Dev head is `l1466slack`; 79 revision files in `alembic/versions/`. Recorded as the first verified
snapshot since the file went stale.

### November 12, 2025
- **Migration**: d8aeb665e878 (UUID migration from Issue #262)
- **Environment**: Development
- **Notes**: Users table migrated to UUID primary keys, alpha_users merged.

---

_Update this file after every migration deployment — with read values, not remembered ones._
