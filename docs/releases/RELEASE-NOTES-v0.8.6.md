# Release Notes v0.8.6

**Release Date**: March 4, 2026
**Branch**: `main`
**Previous Version**: v0.8.5.3
**Sprint**: M0 — Conversational Glue

---

## Summary

This release delivers the M0 Conversational Glue sprint, transforming Piper from "chatbot with features" into a conversational colleague. Users can now converse naturally with Piper — workflows emerge from conversation; commands are shortcuts, not requirements. The release also includes repository management, conversation lifecycle tracking, security hardening, and 8 bug fixes from post-gate CXO testing.

**Reference**: PDR-002 v3.1 (Conversational Glue)

---

## What's New

### Conversational Glue (M0 Sprint)

Five core features that make Piper conversational:

- **#766 - Narrative System**: Piper adapts tone to relationship stage (first meeting → warm introduction, returning user → concise colleague). Eliminates the repeated "Is that your main project?" question during onboarding.

- **#763 - Conversational Lens Tracking**: Piper remembers what you're talking about. Follow-up queries like "what about next week?" resolve correctly based on conversational context (>90% follow-up resolution). 152 new tests.

- **#765 - Natural Slot Filling**: When Piper needs information to complete a task, it asks naturally instead of interrogating. Lens-aware prompt phrasing adapts to conversational context. 124 new tests.

- **#764 - Multi-Intent Orchestration**: Handle compound queries like "check my calendar and create an issue for the API bug" coherently, with natural topic transitions ("As for your calendar..."). 47 new tests.

- **#767 - Soft Workflow Invocation**: Piper offers workflows conversationally ("Sounds like you might want to set up a meeting...") instead of requiring explicit commands. Graceful decline handling. 79 new tests.

### Repository Management

- **#866 - Repository Entity**: Repository as a first-class domain entity with many-to-many Project links.
- **#861 - Settings UI**: Project integration and repository management page.
- **#860 - Setup Wizard**: Project-repo linking step in onboarding.
- **#863 - Portfolio Onboarding**: Repo-linking step during portfolio setup.
- **#862 - Conversational Repo Management**: Natural language handler for repo operations.
- **#867 - GitHub Validation**: API validation for repository link operations.

### Conversation Lifecycle

- **#715/#858 - Conversation State Machine**: Conversations now track lifecycle state (active, stale, archived) with proper database columns and repository support.

### Supporting Infrastructure

- **#852 - Contextual Offer Continuation**: Bare-affirmative responses ("yes", "sure") correctly continue soft-offer workflows.
- **#838 - Unified Formality Framework**: Consistent formality calibration across all interaction channels.
- **#853 - SessionStart Hook**: Automated session start checks for agent session logs, mailbox, and briefing freshness.
- **#849 - User-Scoped Keychain Isolation**: Security fix ensuring integration credentials are properly scoped per user.

---

## Bug Fixes (Post-Gate Testing)

CXO testing on March 1-3 surfaced and resolved these issues:

| Issue | Bug | Fix |
|-------|-----|-----|
| #871 | Legacy POC header visible in templates | Removed header, compacted greeting area |
| #875 | Business errors returned as HTTP 422 instead of 200 | Restored 200 OK for business-logic errors |
| #878 | Workflow polling on synchronous handlers (60s timeout) | Added `async_work_started` flag to prevent spurious polling |
| #879 | `create_issue` missing assignees parameter | Added assignees passthrough to GitHub router |
| #876 | 26 raw exception messages leaked to users | Routed all handler errors through `UserFriendlyErrorService` |
| #880 | Calendar/Slack settings 401 Unauthorized | Added `credentials: 'include'` to 16 fetch() calls |
| #870 | Flaky `test_verbosity_gradient` test | Seeded random for deterministic template selection |

---

## Additional Changes

### Documentation

- Consolidated briefings to `docs/briefing/` (removed `knowledge/` duplicates)
- Removed `piper-education/` tree (content migrated to `docs/internal/development/`)
- Added Pattern-061: Human-AI Collaboration Referee
- Added Period 4 retrospective documents
- Added alpha tester and collaborator profiles
- Updated staggered audit calendar to weekly docs cadence
- Added daily omnibus logs (Feb 6 – Mar 2)

### Housekeeping

- Removed dead `ROUTERS` list and unused methods from `RouterInitializer` (#719)
- Fixed setup request routing to interactive onboarding (#814)
- Removed shadowing `__init__.py` files from test directories (#868)
- Updated CLAUDE.md with subagent commit-verification guideline

---

## Database Migrations

**New migrations** (run `alembic upgrade head`):

1. `a715_add_conversation_lifecycle_columns.py` — Adds lifecycle state tracking to conversations
2. `a866_create_repositories_and_links_tables.py` — Creates repositories and project-repository link tables
3. `a867_add_repository_metadata_columns.py` — Adds metadata columns to repositories

---

## Files Changed

**244 files changed** — 34,982 additions, 8,290 deletions

### New Services
- `services/intent_service/lens_inference.py` — Conversational lens tracking
- `services/intent_service/orchestrator.py` — Multi-intent orchestration
- `services/intent_service/soft_invocation.py` — Soft workflow invocation
- `services/slot_filling/` — Complete slot filling framework (6 files)
- `services/personality/formality.py` — Unified formality framework
- `services/infrastructure/github_repo_validator.py` — GitHub API validation
- `web/api/routes/repositories.py` — Repository CRUD endpoints

### Modified Services
- `services/intent/intent_service.py` — Major: glue integration, error handling overhaul
- `services/intent_service/canonical_handlers.py` — Lens-aware handler updates
- `services/intent_service/conversation_context.py` — Enhanced context tracking
- `services/intent_service/pre_classifier.py` — Multi-intent detection
- `services/onboarding/portfolio_handler.py` — Narrative bridge, repo linking
- `services/database/repositories.py` — Repository and conversation lifecycle support
- `services/domain/models.py` — Repository entity, conversation lifecycle fields

### New Test Files (402+ new tests)
- 12 new test files for lens tracking, multi-intent, soft invocation
- 8 new test files for slot filling
- Test files for repository management, conversation lifecycle, security
- Integration and E2E test additions

---

## Upgrade Instructions

```bash
# Pull latest changes
git pull origin main

# Update dependencies
pip install -r requirements.txt

# Run new migrations
python -m alembic upgrade head

# Start server
python main.py
```

---

## Issues Resolved

### M0 Conversational Glue Sprint

| Issue | Title | Tests |
|-------|-------|-------|
| #766 | Narrative System (onboarding tone) | — |
| #763 | Conversational Lens Tracking | 152 |
| #765 | Natural Slot Filling | 124 |
| #764 | Multi-Intent Orchestration | 47 |
| #767 | Soft Workflow Invocation | 79 |
| #779 | Sprint Completion Gate (3 gates passed) | — |
| #762 | M0 GLUE Epic (all children closed) | — |

### Repository Management

| Issue | Title |
|-------|-------|
| #866 | Repository as first-class entity |
| #861 | Project integration settings page |
| #860 | Setup wizard repo linking |
| #863 | Portfolio onboarding repo linking |
| #862 | Conversational repo management handler |
| #867 | GitHub API validation for repo links |

### Bug Fixes & Infrastructure

| Issue | Title |
|-------|-------|
| #871 | Legacy POC header in templates |
| #875 | Business errors returned as HTTP 422 |
| #878 | Workflow polling on sync handlers |
| #879 | create_issue missing assignees |
| #876 | 26 raw exception message leaks |
| #880 | Calendar/Slack settings 401 |
| #870 | Flaky test_verbosity_gradient |
| #858 | Conversation lifecycle state machine |
| #852 | Contextual offer continuation |
| #838 | Unified formality framework |
| #853 | SessionStart hook |
| #849 | User-scoped keychain isolation |
| #814 | Setup request routing |
| #868 | Shadowing __init__.py removal |
| #719 | Dead router code removal |

**Total**: 27 issues resolved

---

## Testing Notes

- **6,146 tests passing**, 7 skipped (pre-existing)
- 402+ new tests added in M0 sprint
- Sprint completion gate verified: persistence audit, anti-flattening, multi-tenancy
- Post-gate CXO testing completed March 1-3 with all bugs resolved

---

## Contributors

- Claude (Lead Developer) — Implementation
- xian (PM/CXO) — Design, testing, sprint management

---

## See Also

- [PDR-002 v3.1](../../docs/internal/planning/conversational-glue/) — Conversational Glue design
- [Sprint Completion Gate (#779)](https://github.com/mediajunkie/piper-morgan-product/issues/779) — Gate verification evidence
- [Alpha Quickstart](../BETA_QUICKSTART.md) — Setup guide

---

_Released: March 4, 2026_
