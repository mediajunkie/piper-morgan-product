# After Git Pull - Environment Checklist

**Purpose**: What to check after pulling new code from production or main branches

**Time**: 2-3 minutes

---

## TL;DR Quick Check

```bash
# After git pull, run these 4 commands:
ls -la .env                    # 1. Verify .env still exists
python main.py status          # 2. Check system health
pip install -r requirements.txt  # 3. Update dependencies (if needed)
python main.py                 # 4. Test server starts
```

If all green checkmarks → you're good!

---

## Why This Guide Exists

**Your .env file NEVER disappears** - it's protected by `.gitignore`. But pulling new code might:
- Introduce new required environment variables
- Change dependency versions
- Add database migrations
- Require configuration updates

This guide helps you verify everything still works after pulling updates.

---

## Step-by-Step Post-Pull Checklist

### 1. Verify Environment File Intact

```bash
# Your .env should exist (git doesn't touch gitignored files)
ls -la .env
```

**Expected**: File exists with your JWT_SECRET_KEY

**If missing - COMMON ISSUE FOR FIRST-TIME SETUP**:
```bash
# If you never created .env during initial setup, create it now:
cp .env.example .env

# Generate JWT secret key:
openssl rand -hex 32

# Edit .env in your IDE/text editor and add the generated key:
# JWT_SECRET_KEY=<paste-generated-key-here>

# Note: API keys are stored in secure system keyring by the wizard
# You don't need to add API keys to .env (wizard handles that)
```

**Why this happens**: The setup wizard stores API keys in the system keyring (not .env). But JWT_SECRET_KEY must be in .env for authentication to work. If you skipped Step 2 during initial setup, you'll need to create .env now.

---

### 2. Check for New Environment Variables

```bash
# Compare .env.example with your .env to see if new vars were added
diff .env .env.example
```

**New variables in .env.example?**
- Add them to your `.env` with appropriate values
- Check git commit messages for guidance on new variables
- Run `python main.py status` to verify

**Common new variables** (check release notes):
- API keys for new integrations
- Feature flags
- Service configuration options

---

### 3. Update Python Dependencies

```bash
# If requirements.txt changed, update dependencies
pip install -r requirements.txt --upgrade
```

**When to run**: After pulling major version updates or if `python main.py` fails with import errors

---

### 4. Run System Health Check

```bash
python main.py status
```

**Expected output**: All green checkmarks (✅)

**If warnings/errors**:
- JWT_SECRET_KEY not set → Add to .env
- API keys missing → Run `python main.py setup`
- Database connection failed → Check Docker is running
- Migration needed → Run database migrations (see below)

---

### 5. Check for Database Migrations

```bash
# If new migrations were added, you'll see migration files in:
ls -la alembic/versions/

# Apply any new migrations:
alembic upgrade head
```

**When to run**: After pulling commits that mention "migration" or "database schema"

---

### 6. Test Server Startup

```bash
python main.py
```

**Expected**:
- No JWT_SECRET_KEY warnings
- Server starts on http://localhost:8001
- Browser opens automatically (unless --no-browser)
- No authentication errors

**If authentication errors**:
- Check `.env` has JWT_SECRET_KEY set
- Restart server completely (kill old process first)
- Clear browser cookies for localhost:8001

---

## Common Post-Pull Issues

### "JWT_SECRET_KEY not set" Warning

**Cause**: main.py now loads .env automatically, but .env is missing JWT_SECRET_KEY

**Fix**:
```bash
# Generate key
openssl rand -hex 32

# Add to .env
echo "JWT_SECRET_KEY=<your-generated-key>" >> .env

# Restart server
python main.py
```

---

### Authentication Required Error in Browser

**Cause**: Auth middleware now active, but you're not logged in

**Fix**:
- Visit http://localhost:8001/login (if login UI exists)
- Or temporarily disable auth for testing (see the auth middleware configuration, or [file an issue](https://github.com/mediajunkie/piper-morgan-product/issues/new) if it's not clear how)

---

### Import Errors / Module Not Found

**Cause**: New dependencies added to requirements.txt

**Fix**:
```bash
pip install -r requirements.txt
python main.py
```

---

### Database Migration Errors

**Cause**: Schema changed, migrations not applied

**Fix**:
```bash
# Check current migration status
alembic current

# Apply pending migrations
alembic upgrade head

# If conflicts, check the migration's docstring or file a GitHub issue before proceeding
```

---

## Version-Specific Migration Notes

### v0.8.1 → v0.8.1.1 (Nov 30, 2025)

**Changes**:
- ✅ AuthMiddleware registration fix (P0)
- ✅ main.py now loads .env automatically
- ✅ JWT_SECRET_KEY required in .env

**Action Required**:
1. Add JWT_SECRET_KEY to .env (see Step 1 above)
2. Restart server

---

### v0.8.0 → v0.8.1 (Nov 27, 2025)

**Changes**:
- Cookie-based authentication
- Login/logout UI
- Token blacklist

**Action Required**:
1. Clear browser cookies for localhost:8001
2. Re-login with your credentials

---

## Emergency Rollback

If new code breaks your environment and you need to go back:

```bash
# Option 1: Rollback to previous commit
git log --oneline -5  # Find commit hash before pull
git reset --hard <commit-hash>

# Option 2: Rollback to specific tag
git tag  # List available tags
git checkout production-pre-main-merge-2025-11-30

# Your .env will be intact in both cases
```

---

## Quick Reference

**Environment survived git pull?**: ✅ YES (gitignored)
**Dependencies need updating?**: Check requirements.txt diff
**Database migrations needed?**: Check alembic/versions/
**New env vars required?**: Diff .env vs .env.example

**Health check command**: `python main.py status`
**Full restart**: Kill server, `python main.py`

---

**Last Updated**: Nov 30, 2025
**Related Docs**: [ALPHA_QUICKSTART.md](../ALPHA_QUICKSTART.md), [ALPHA_TESTING_GUIDE.md](../ALPHA_TESTING_GUIDE.md)
