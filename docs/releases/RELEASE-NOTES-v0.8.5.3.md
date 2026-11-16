# Release Notes v0.8.5.3

**Release Date**: February 11, 2026
**Branch**: `production`
**Previous Version**: v0.8.5.2

---

## Summary

Windows compatibility and setup experience improvements based on comprehensive alpha testing feedback from Ted Nadeau. This release makes Piper Morgan installable and runnable on Windows systems and significantly improves the first-time setup experience with realistic expectations and better error handling.

---

## What's New

### Windows Compatibility Fixes

- **#795 - uvloop Windows fix**: Added PEP 508 environment marker to exclude uvloop on Windows (`sys_platform != 'win32'`). uvloop is Unix-only but was blocking Windows installation.

- **#796 - Missing database migrations**: Created missing migrations for `products`, `features`, and `work_items` tables. Made timestamp conversion migration resilient to missing tables.

- **#797 - CRLF line endings**: Added `.gitattributes` rules to force LF line endings for shell scripts, preventing Docker container startup failures on Windows.

### Setup Experience Improvements

- **#798 - Schema validation**: Fixed false positives in schema validator for ARRAY types.

- **#799 - Account creation errors**: Improved error message extraction to show actual error details instead of generic "Failed to create account". Added back navigation buttons to setup wizard.

- **#806 - Installation validator**: New `scripts/validate_install.py` script to verify all components are working after setup. Checks Python version, venv, .env, Docker, database connection, migrations, and API health.

- **#808 - Actionable error messages**: Enhanced error handling in setup routes with specific fix suggestions:
  - Missing tables → "Run 'python -m alembic upgrade head'"
  - Connection errors → "Ensure Docker is running: 'docker compose up -d'"

### Documentation Updates

- **#800 - docker-compose syntax**: Updated all user-facing documentation to use modern `docker compose` syntax.

- **#801 - Realistic time estimates**: Added Time & Storage Requirements table to ALPHA_QUICKSTART.md. First-time setup: 20-50 minutes (not "30 seconds"). Storage: ~6GB.

- **#802 - Setup path clarity**: Added "Choose Your Path" section distinguishing alpha testing from development setup.

- **#803 - venv activation**: Added callout boxes and troubleshooting for virtual environment activation requirements.

- **#804 - Windows localhost**: Documented that Windows users should use `127.0.0.1:8001` instead of `localhost:8001` due to IPv6 resolution.

- **#805 - pip upgrade**: Added `pip install --upgrade pip` step before requirements installation.

- **#807 - PostgreSQL access**: Added database browsing section with connection details, GUI tool instructions (pgAdmin, DBeaver), and CLI access commands.

---

## Database Migrations

**New migrations added** (run `alembic upgrade head`):

1. `f5b173cbab46_create_products_table_issue_796.py`
2. `4bd02594d62d_create_features_table_issue_796.py`
3. `4ba89dbf5347_create_work_items_table_issue_796.py`

**Modified migration**:
- `d73b3722eb03_convert_timestamps_to_timestamptz.py` - Now checks if tables/columns exist before altering

---

## Files Changed

### Code Changes
- `requirements.txt` - uvloop platform marker
- `web/api/routes/setup.py` - Enhanced error handling
- `web/static/js/setup.js` - Better error extraction, docker compose syntax
- `web/static/css/auth.css` - Secondary button style
- `templates/setup.html` - Back navigation buttons
- `tools/schema_validator.py` - ARRAY type recognition
- `.gitattributes` - Shell script LF enforcement

### New Files
- `scripts/validate_install.py` - Installation validation script
- `alembic/versions/f5b173cbab46_create_products_table_issue_796.py`
- `alembic/versions/4bd02594d62d_create_features_table_issue_796.py`
- `alembic/versions/4ba89dbf5347_create_work_items_table_issue_796.py`

### Documentation
- `docs/ALPHA_QUICKSTART.md` - Time estimates, paths, venv, validation script
- `docs/ALPHA_TESTING_GUIDE.md` - PostgreSQL browsing section
- `README.md`, `SETUP.md`, `CONTRIBUTING.md` - docker compose, pip upgrade
- Multiple docs updated for docker compose syntax

---

## Upgrade Instructions

```bash
# Pull latest changes
git pull origin production

# Update dependencies (Windows users: uvloop will now be skipped)
pip install -r requirements.txt

# Run new migrations
python -m alembic upgrade head

# Optional: Validate installation
python scripts/validate_install.py

# Start server
python main.py
```

---

## Issues Resolved

| Priority | Issue | Title |
|----------|-------|-------|
| BLOCKER | #795 | uvloop fails to install on Windows |
| BLOCKER | #796 | Migration fails - 'features' table does not exist |
| HIGH | #797 | Windows CRLF line endings break Docker |
| HIGH | #798 | Schema validation reports false positives |
| HIGH | #799 | Account creation fails with generic error |
| MEDIUM | #800 | docker-compose → docker compose syntax |
| MEDIUM | #801 | Realistic time estimates in docs |
| MEDIUM | #802 | Run vs develop setup paths |
| MEDIUM | #803 | venv activation documentation |
| MEDIUM | #804 | localhost vs 127.0.0.1 on Windows |
| LOW | #805 | pip upgrade step in docs |
| LOW | #806 | Installation validation script |
| LOW | #807 | PostgreSQL database browsing docs |
| LOW | #808 | Error messages with fix suggestions |

**Total**: 14 issues resolved

---

## Testing Notes

- Tested on fresh database with all migrations
- Windows compatibility verified via Ted Nadeau's testing feedback
- Installation validator passes all checks on macOS
- Pre-existing test failure in `test_context_tracker.py` unrelated to this release

---

## Contributors

- Ted Nadeau - Alpha testing (Windows setup feedback)
- Claude (Lead Developer) - Implementation

---

## See Also

- [Alpha Quickstart](../BETA_QUICKSTART.md) - Updated setup guide
- [Alpha Testing Guide](../BETA_TESTING_GUIDE.md) - PostgreSQL access docs
- [Known Issues](../BETA_KNOWN_ISSUES.md) - Current limitations

---

_Released: February 11, 2026_
