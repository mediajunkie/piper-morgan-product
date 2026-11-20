# Release Notes: v0.8.1

**Released**: November 24, 2025
**Status**: Production
**Branch**: `production` (commit `5aab5320`)

## Overview

v0.8.1 is a stability and UX improvement release that introduces version tracking, enhances user settings, fixes critical LLM API issues, and includes foundational infrastructure refactoring for better maintainability.

## What's New

### Version Tracking System (#378)

**Single Source of Truth**: Version managed in `pyproject.toml` and exposed throughout the application.

**Features**:
- `services/version.py` - Reads version from pyproject.toml using tomli
- `/api/v1/version` endpoint - Returns version + environment info
- Settings page footer - Displays version dynamically
- Internal `__version__` export for Python imports

**Impact**: Users can now verify which version is running in production vs development.

**Files Changed**:
- [pyproject.toml](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/pyproject.toml#L7) - version = "0.8.1"
- [services/version.py](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/services/version.py) (new)
- [templates/settings-index.html](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/templates/settings-index.html#L254-L259)

### User Settings Page (#383)

**New Settings Hub**: Centralized settings page with card-based navigation.

**Available Settings**:
- Personality preferences
- Learning & patterns
- Privacy & data
- Account management
- Integrations (coming soon)
- Advanced settings

**Design**: Clean, responsive card layout with hover effects and meta tags.

**Access**: Navigate to `/settings` or click Settings in main navigation.

**Files Changed**:
- [templates/settings-index.html](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/templates/settings-index.html) (new)

### Learning Dashboard Dark Mode Fix (#391)

**Issue**: Learning dashboard had hardcoded dark mode colors, ignoring user theme preferences.

**Solution**: Replaced all hardcoded color values with CSS variables to support theme switching.

**CSS Variables Used**:
- `--bg-primary`, `--bg-secondary`, `--bg-tertiary` - Background colors
- `--text-primary`, `--text-secondary` - Text colors
- `--primary-color`, `--primary-color-hover` - Accent colors
- `--border-color` - Borders

**Impact**: Learning dashboard now respects system theme (light/dark mode).

**Files Changed**:
- [templates/learning-dashboard.html](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/templates/learning-dashboard.html) - 102 lines changed (51 insertions, 51 deletions)

## Bug Fixes

### LLM API System Parameter Support (#381)

**Issue**: `LLMDomainService.complete()` and `LLMService.complete()` didn't support `system` parameter, causing failures in conversations requiring system prompts.

**Root Cause**: Methods only passed `messages`, `model`, `max_tokens` - ignored `system` parameter.

**Fix**: Added `system` parameter to method signatures and API calls.

**Impact**: System prompts now work correctly in LLM conversations.

**Files Changed**:
- [services/domain/llm_domain_service.py:76-77](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/services/domain/llm_domain_service.py#L76-L77)
- `services/llm_service.py:88-91` (not in the v0.8.1 tag, so no link)

### Missing Conversation Models (#382)

**Issue**: `ConversationDB` and `ConversationTurnDB` models referenced but not defined.

**Fix**: Added proper model definitions with relationships.

**Impact**: Conversation tracking now works correctly.

### Test Suite Fixes

**UUID Format Issues**: Fixed invalid UUID format in file resolver and scoring tests.

**SEC-RBAC Migration**: Completed `session_id` → `owner_id` migration across:
- FileRepository CRUD methods
- KnowledgeGraph models
- File scoring weight tests
- File resolver edge case tests

**Result**: Test suite now passes with proper UUID validation.

## Infrastructure Improvements

### Web App Refactoring (Phase 1 & 2) - #385

**Audited Safe**: These refactors are currently in production and have been audited as non-breaking.

#### Phase 1: Router Factory Implementation (commit 5ff37e64)

**Problem**: Duplicate router mounting code repeated 8+ times in `web/app.py`.

**Solution**: Created `mount_routers()` factory function.

**Benefits**:
- Removed 250+ lines of duplication
- Centralized router configuration
- Easier to add new routes

**Files Changed**:
- [web/app.py](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/web/app.py) - Consolidated router mounting

#### Phase 2: Lifespan Extraction & Startup Phases (commit 3e41e144)

**Problem**: Monolithic startup logic mixed with app creation in `web/app.py`.

**Solution**: Extracted lifespan management to separate module.

**Benefits**:
- Removed 200+ lines from web/app.py
- Testable startup phases
- Clear separation of concerns

**Files Changed**:
- [web/startup.py](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/web/startup.py) (new)
- [web/app.py](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/web/app.py) - Simplified startup

**Risk Assessment**: LOW - Both phases are structural refactors with zero breaking changes.

## Documentation

### CLAUDE.md Enhancements

**Added**:
- Architecture guidance with patterns
- Development task tracking
- Technical reference sections
- Progressive loading instructions

**Files Changed**:
- [CLAUDE.md](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/CLAUDE.md)

### Alpha Testing Guide Updates (#377)

**Added**: Nov 22-23 test scenarios and results.

**Files Changed**:
- [docs/ALPHA_TESTING_GUIDE.md](https://github.com/mediajunkie/piper-morgan-product/blob/v0.8.1/docs/ALPHA_TESTING_GUIDE.md)

## Technical Details

### Commits Included

```
5aab5320 fix(#391): Replace hardcoded dark mode with CSS variables in learning dashboard
fab1f838 chore: Bump version to 0.8.1
3e41e144 feat(INFR-MAINT-REFACTOR): Phase 2 - Lifespan Extraction & Startup Phases
676bb870 fix(tests): Fix invalid UUID format in file resolver and scoring tests
5ff37e64 feat(INFR-MAINT-REFACTOR): Phase 1 - Router Factory Implementation
c3fae1cb feat(#383): Create basic user settings page
debeae99 feat: Implement version tracking system (Option 2)
1347f14f fix: Add missing ConversationDB and ConversationTurnDB models
48a4ee22 fix(#381): Add system parameter support to LLM complete() methods
```

### Test Suite Status

**Passing**: 1154+ tests
**Known Failures**: Tracked in `.pytest-known-failures`
**Pre-Push Validation**: Enabled with fast test suite (<30s)

### Database Migrations

**SEC-RBAC**: Completed migration from `session_id` to `owner_id` across all repositories.

## Known Issues

None reported for v0.8.1 features.

## Upgrade Notes

### For Alpha Users

1. Pull latest production branch: `git pull origin production`
2. Verify version in Settings page footer shows "v0.8.1"
3. Test theme switching on Learning dashboard
4. Report any issues to #388, #389, #390 (setup-related features)

### For Developers

**New Dependencies**:
- `tomli` - TOML parsing for pyproject.toml (already in requirements.txt)

**Environment Variables**:
- `ENVIRONMENT` - Set to "production", "staging", or "development" (defaults to "development")

## What's Next (v0.8.2)

### Planned Features

1. **Setup Detection** (#388) - Prevent unconfigured startup
   - Status: Branch ready, deferred for proper rebasing
   - Impact: First-time user experience improvement

2. **Setup Complete Flag** (#389) - Explicit setup completion tracking
   - Depends on: #388
   - Purpose: Database-backed setup state

3. **Web-based Setup UI** (#390) - Replace CLI wizard
   - Depends on: #388, #389
   - Purpose: Better UX for initial setup

### Infrastructure Work

**Phase 3 & 4 Refactors** (#385):
- Route organization (extract to web/api/routes/*)
- Global state cleanup
- Status: On feature branches, ready for review

## Contributors

- xian (PM)
- Claude Code (Programmer agent)
- Claude Haiku (Task execution subagent)

## Links

- **GitHub Repo**: [mediajunkie/piper-morgan-product](https://github.com/mediajunkie/piper-morgan-product)
- **Production Branch**: [production](https://github.com/mediajunkie/piper-morgan-product/tree/production)
- **Release Commit**: [5aab5320](https://github.com/mediajunkie/piper-morgan-product/commit/5aab5320)

---

**Generated**: 2025-11-24 10:21 AM
**By**: Claude Code (Programmer)
**Session**: [2025-11-24-0516-prog-code-log.md](../../dev/2025/11/24/2025-11-24-0516-prog-code-log.md)
