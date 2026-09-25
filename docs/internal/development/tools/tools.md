# Development Tools

This document describes the development tools available in the Piper Morgan codebase.

## Schema Validation Tool (PM-056)

**Location**: `tools/schema_validator.py`

*(Corrected 2026-09-24, #1882 — this page previously named `tools/check_domain_db_consistency.py`,
a second, unwired `SchemaValidator` implementation with no CI or Makefile wiring. That file has been
deleted; `tools/schema_validator.py` is the only PM-056 validator now, and is the one CI has always
gated on.)*

### Purpose
Validates consistency between SQLAlchemy database models and domain dataclasses to prevent schema
drift and ensure Domain-Driven Design integrity.

### Features
- Automatic model discovery from `services.domain.models` and `services.database.models`, with
  direct-name mapping plus a small explicit pattern table (`Project`→`ProjectDB`,
  `ProjectIntegration`→`ProjectIntegrationDB`, `UploadedFile`→`UploadedFileDB`)
- Field presence validation (detects missing fields in either layer), with architectural
  awareness so it does not cry wolf on known-intentional differences:
  - `FIELD_MAPPINGS` — domain field renamed at the DB column (e.g. `WorkItem.metadata` →
    `item_metadata`, since `metadata` is SQLAlchemy-reserved)
  - `ARCHITECTURAL_EXCEPTIONS` — fields intentionally deferred/absent by ratified design
    (reported as `info`, not `error`)
  - `RELATIONSHIP_MAPPINGS` — domain fields persisted through a SQLAlchemy relationship/association
    table rather than a column on the model's own table
  - `PERSISTENCE_ONLY_COLUMNS` — DB columns that are persistence/authorization anchors with no
    domain-layer counterpart by design
- Type compatibility checking (maps Python types, including `Optional[T]` and generic containers,
  to compatible SQLAlchemy column types)
- Enum consistency validation (domain enum vs DB enum vs enum-stored-as-string, including a genuine
  enum-class mismatch check)
- Relationship consistency validation (DB relationship attributes vs domain fields)

### Usage

```bash
# Validate all mapped models
PYTHONPATH=. python tools/schema_validator.py

# Validate one model
PYTHONPATH=. python tools/schema_validator.py --model Project

# Verbose (prints discovered model mappings)
PYTHONPATH=. python tools/schema_validator.py --verbose

# CI mode: exit 1 if any ERROR-severity issue is found, 0 otherwise
# (--ci is required for a red build; without it the tool always exits 0)
PYTHONPATH=. python tools/schema_validator.py --ci
```

### Exit Codes
- `0` - No `error`-severity issues (with `--ci`); without `--ci` the tool always exits 0 regardless
  of findings, so CI/Makefile invocations always pass `--ci`
- `1` - `--ci` mode found one or more `error`-severity issues

### Issue severities
- `error` — genuine drift requiring a fix (missing field, type mismatch, missing enum)
- `warning` — a DB column with no domain counterpart and no recorded persistence-only reason
- `info` — a recorded architectural exception, relationship-backed field, persistence-only column,
  or enum-stored-as-string pattern; visible for auditability but not a failure

### Integration with CI/CD
Runs automatically via `.github/workflows/schema-validation.yml` (job `schema-validation`) on any
push/PR touching `services/domain/models.py`, `services/database/models.py`,
`tools/schema_validator.py`, or `scripts/check_conversion_methods.py`. A sibling job in the same
workflow, `known-issues-check`, independently greps for the historical object_id/object_position
regression and runs `scripts/check_conversion_methods.py`; the two jobs report independently (no
`needs:` dependency between them, by design — see the workflow file's 2026-09-13 comment).

Also wired into the `Makefile`:
```bash
make validate-schema   # PYTHONPATH=. python3 tools/schema_validator.py
make ci-validate        # PYTHONPATH=. python3 tools/schema_validator.py --ci
make validate-all       # validate-schema + check-conversions
```

### Maintenance
When adding new domain models or database tables:
1. Ensure corresponding models exist in both layers, or record the exception (`FIELD_MAPPINGS`,
   `ARCHITECTURAL_EXCEPTIONS`, `RELATIONSHIP_MAPPINGS`, or `PERSISTENCE_ONLY_COLUMNS` at the top of
   `tools/schema_validator.py`) if the difference is intentional
2. Run `PYTHONPATH=. python tools/schema_validator.py --verbose` to check consistency
3. Fix any reported `error`-severity issues before committing
4. Tests: `tests/test_schema_validator.py` (16 tests)

## Other Tools

### Pattern Sweep (`scripts/pattern_sweep.py`)
Standalone automated pattern discovery and learning acceleration tool.
- Usage: `./scripts/run_pattern_sweep.sh --verbose`
- Compound learning acceleration for development workflow optimization

### Database Initialization (`scripts/init_db.py`)
Initialize the PostgreSQL database with proper schema.

---

*Last updated: 2025-08-18* - TLDR deprecated, Pattern Sweep preserved as standalone tool
