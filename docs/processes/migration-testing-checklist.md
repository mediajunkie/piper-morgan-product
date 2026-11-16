# Database Migration Testing Checklist

**Use this before**: Every migration deployment
**Time required**: 15-30 minutes per migration
**Purpose**: Catch schema/code mismatches before they hit users

---

## Pre-Migration Checklist

### Planning Phase
- [ ] Migration has clear purpose documented
- [ ] Migration is atomic (one logical change)
- [ ] Rollback strategy defined
- [ ] Data backup plan exists
- [ ] Estimated downtime documented (if any)

### Code Review
- [ ] Migration file has descriptive name
- [ ] Upgrade function (`upgrade()`) implemented
- [ ] Downgrade function (`downgrade()`) implemented
- [ ] SQL is database-agnostic (or PostgreSQL-specific if needed)
- [ ] No hardcoded values (use variables)
- [ ] No data loss operations without safeguards

### Impact Assessment
- [ ] Tables affected: [list]
- [ ] Columns added/removed/modified: [list]
- [ ] Indexes added/removed: [list]
- [ ] Foreign keys affected: [list]
- [ ] Data transformation needed: [yes/no]

---

## Testing Phase

### Test 1: Fresh Database Migration
**Purpose**: Verify migration works on clean install

```bash
# 1. Drop and recreate test database
# Only for a computer that runs a single copy of Piper. This stops the stack, and a volume flag deletes its database. Never run it on a shared stack.
docker-compose down -v
docker-compose up -d postgres
sleep 5

# 2. Run all migrations
alembic upgrade head

# 3. Verify success
alembic current
# Expected: Shows latest migration

# 4. Check schema
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d"
# Verify all tables present
```

**Checklist**:
- [ ] All migrations apply without errors
- [ ] Schema matches expected state
- [ ] All tables exist
- [ ] All indexes created
- [ ] Foreign keys correct

### Test 2: Incremental Migration
**Purpose**: Verify migration works on existing database

```bash
# 1. Start from previous migration
alembic downgrade -1

# 2. Apply new migration
alembic upgrade +1

# 3. Verify success
alembic current

# 4. Check schema changes
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d [affected_table]"
# Verify changes applied correctly
```

**Checklist**:
- [ ] Migration applies cleanly
- [ ] No constraint violations
- [ ] Data preserved
- [ ] Indexes updated
- [ ] Foreign keys intact

### Test 3: Rollback Test
**Purpose**: Verify downgrade works

```bash
# 1. Apply migration
alembic upgrade head

# 2. Downgrade migration
alembic downgrade -1

# 3. Verify rollback
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\d [affected_table]"
# Schema should be in previous state

# 4. Re-apply migration
alembic upgrade head
# Should work again
```

**Checklist**:
- [ ] Downgrade completes without errors
- [ ] Schema returns to previous state
- [ ] Data preserved during rollback
- [ ] Can re-apply migration after rollback

### Test 4: Code Compatibility Test
**Purpose**: Verify code works with new schema

```bash
# 1. Apply migration
alembic upgrade head

# 2. Run application
python main.py &
sleep 3

# 3. Test affected features
pytest tests/ -k [affected_feature] -v

# 4. Manual verification
# - Login/logout if auth migration
# - Create/read if model migration
# - Upload/download if file migration
# etc.

# 5. Stop application
kill %1
```

**Checklist**:
- [ ] Application starts without errors
- [ ] No import errors
- [ ] Models load correctly
- [ ] Tests pass
- [ ] Manual tests successful

### Test 5: Multi-Environment Sync
**Purpose**: Verify migration works in all environments

**Environments to test**:
- [ ] Development (local)
- [ ] Test (CI)
- [ ] Staging (if exists)
- [ ] Production (final deployment)

**For each environment**:
```bash
# 1. Check current migration
alembic current

# 2. Backup database
docker exec piper-postgres pg_dump -U piper -d piper_morgan > backup_pre_migration.sql

# 3. Apply migration
alembic upgrade head

# 4. Verify
python main.py status
pytest tests/ -v

# 5. Document completion
echo "Environment: [name], Migration: [hash], Date: $(date)" >> migration_log.txt
```

---

## Post-Migration Checklist

### Verification
- [ ] All environments migrated successfully
- [ ] No error logs in application
- [ ] Tests passing in all environments
- [ ] Manual verification complete
- [ ] Performance acceptable

### Documentation
- [ ] Migration logged in change log
- [ ] ADR created (if architectural change)
- [ ] README updated (if user-facing)
- [ ] Known issues documented

### Cleanup
- [ ] Old backup files retained (7 days)
- [ ] Migration notes added to issue
- [ ] PR created with migration details
- [ ] Team notified

---

## Emergency Rollback Procedure

**If migration causes issues in production**:

```bash
# 1. STOP - Don't panic
# 2. Check error logs
tail -f logs/piper.log

# 3. Attempt rollback
alembic downgrade -1

# 4. Restore from backup if rollback fails
docker exec -i piper-postgres psql -U piper -d piper_morgan < backup_pre_migration.sql

# 5. Restart application
python main.py

# 6. Verify system operational
python main.py status

# 7. Document incident
# - What happened
# - What was rolled back
# - What needs fixing
```

**When to rollback**:
- Critical functionality broken
- Data corruption detected
- Performance unacceptable
- Schema/code mismatch

**When NOT to rollback**:
- Minor cosmetic issues
- Non-critical feature affected
- Issue can be hot-fixed

---

## Sign-Off

**Before deploying migration to production**:

- [ ] All tests passing (✓)
- [ ] Code review complete (✓)
- [ ] Rollback tested (✓)
- [ ] Backup confirmed (✓)
- [ ] Team notified (✓)

**Signed off by**: [Your name]
**Date**: [Date]
**Migration**: [Migration hash]

---

_Created: November 12, 2025_
_Issue: #289_
_Version: 1.0_
