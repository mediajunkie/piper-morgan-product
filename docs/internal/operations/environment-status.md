# Environment Status

⚠️ **STALE — flagged 2026-08-11, found during weekly-docs-audit #1583/#1585.** ~9 months old.
Migration/DB-size state isn't something Docs can verify independently; flagged to Lead Dev/
infra owner rather than guessed at.

**Last Updated**: November 12, 2025

## Current Status

| Environment | Migration    | App Version | Database Size | Status |
|-------------|--------------|-------------|---------------|--------|
| Development | d8aeb665e878 | 0.8.0       | 10 MB         | ✓      |
| Test        | -            | -           | -             | -      |
| Staging     | -            | -           | -             | -      |
| Production  | -            | -           | -             | -      |

## Update Instructions

Update this file after every migration using:

```bash
# Get current migration
alembic current

# Get database size
docker exec piper-postgres psql -U piper -d piper_morgan -c "SELECT pg_size_pretty(pg_database_size('piper_morgan'));"

# Get app version
grep "version" pyproject.toml | head -1
```

## Migration History

### November 12, 2025
- **Migration**: d8aeb665e878 (UUID migration from Issue #262)
- **Environment**: Development
- **Status**: Active
- **Notes**: Users table migrated to UUID primary keys, alpha_users merged

## Notes

- Development environment only (no staging/production yet)
- Database running on Docker container `piper-postgres`
- Port: 5433
- Alpha testing starting with external testers

---

_Update this file after every migration deployment_
