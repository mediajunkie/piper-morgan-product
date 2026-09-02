# Canonical Query Test Matrix v2

> ⚠️ **HISTORICAL — SUPERSEDED 2026-04-11**
> This v2 matrix describes a pre-M1 architecture and uses pure routing matching. After M1's floor inversion (#911) and the Apr 8 IDENTITY full migration to floor, most read-only categories route to the conversational floor. Routing-only verdicts no longer reflect quality.
>
> **Use [canonical-query-test-matrix-v3.md](../canonical-query-test-matrix-v3.md)** for current methodology with dual scoring (routing + Colleague Test quality rubric).
>
> This file is retained for historical reference only.

---

**Generated**: December 25, 2025 (Updated January 12, 2026)
**Based On**: Canonical Queries v2 (63 queries)
**Current Implementation**: 21/63 (33%)
**Last Tested**: January 12, 2026

**Recent Updates (v0.8.4)**:
- No new canonical query implementations in Sprint B1
- Focus was on Integration Settings (Epic #543) and Portfolio Onboarding (#490)
- Coverage remains at 33%

**v0.8.3.2 Updates**:
- Query #49 `/standup` → ✅ PASS (Slack slash command, Issue #520)
- Query #50 `/piper help` → ✅ PASS (Slack slash command, Issue #520)
- Interactive Standup (Epic #242) adds conversational standup creation to chat interface (complementary to Query #49)

## Summary Statistics

| Category | Total | PASS | PARTIAL | NOT IMPL | Coverage |
|----------|-------|------|---------|----------|----------|
| Identity | 5 | 5 | 0 | 0 | ✅ 100% |
| Temporal | 5 | 5 | 0 | 0 | ✅ 100% |
| Spatial | 4 | 4 | 0 | 0 | ✅ 100% |
| Capability | 5 | 5 | 0 | 0 | ✅ 100% |
| Predictive | 5 | 0 | 1 | 4 | ⚠️ 20% |
| Conversational | 5 | 0 | 0 | 5 | ❌ 0% |
| Scheduling | 5 | 0 | 0 | 5 | ❌ 0% |
| Documents | 5 | 0 | 0 | 5 | ❌ 0% |
| GitHub Ops | 8 | 0 | 0 | 8 | ❌ 0% |
| Slack | 5 | 2 | 0 | 3 | ⚠️ 40% |
| Productivity | 3 | 0 | 0 | 3 | ❌ 0% |
| Todos | 4 | 0 | 0 | 4 | ❌ 0% |
| Calendar Ext | 2 | 0 | 0 | 2 | ❌ 0% |
| Knowledge | 1 | 0 | 0 | 1 | ❌ 0% |
| **TOTAL** | **63** | **21** | **1** | **41** | **33%** |

## Detailed Test Matrix

### ✅ Identity Queries (100% Complete)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 1 | What's your name and role? | ✅ PASS | test_canonical_handlers.py | All formatters working |
| 2 | What can you help me with? | ✅ PASS | test_canonical_handlers.py | Dynamic capabilities |
| 3 | Are you working properly? | ✅ PASS | test_canonical_handlers.py | Health check functional |
| 4 | How do I get help? | ✅ PASS | test_canonical_handlers.py | Help system complete |
| 5 | What makes you different? | ✅ PASS | test_canonical_handlers.py | Differentiation clear |

### ✅ Temporal Queries (100% Complete)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 6 | What day is it? | ✅ PASS | test_canonical_handlers.py | Time awareness working |
| 7 | What did we accomplish yesterday? | ✅ PASS | test_canonical_handlers.py | Retrospective functional |
| 8 | What's on the agenda for today? | ✅ PASS | test_agenda_query.py | Calendar + todos |
| 9 | When was the last time we worked on this? | ✅ PASS | test_canonical_handlers.py | Activity tracking |
| 10 | How long have we been working on this? | ✅ PASS | test_canonical_handlers.py | Duration calculation |
| ~~15~~ | ~~Where are we in lifecycle?~~ | 🚫 REMOVED | - | Too abstract |

### ✅ Spatial Queries (100% Complete)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 11 | What projects are we working on? | ✅ PASS | test_canonical_handlers.py | Project list works |
| 12 | Show me the project landscape | ✅ PASS | test_canonical_handlers.py | Landscape view |
| 13 | Which project should I focus on? | ✅ PASS | test_canonical_handlers.py | Priority scoring |
| 14 | What's the status of project X? | ✅ PASS | test_canonical_handlers.py | Project-specific |

### ✅ Capability Queries (100% Complete)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 16 | Create a GitHub issue | ✅ PASS | test_canonical_handlers.py | Issue creation |
| 17 | Analyze this document | ✅ PASS | test_document_handlers.py | Notion analysis |
| 18 | List all my projects | ✅ PASS | test_canonical_handlers.py | Routes to #11 |
| 19 | Generate a status report | ✅ PASS | test_canonical_handlers.py | Report generation |
| 20 | Search for X in documents | ✅ PASS | test_document_handlers.py | Notion search |

### ⚠️ Predictive Queries (20% - Beta Target)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 21 | What should I focus on today? | ⚠️ PARTIAL | test_canonical_handlers.py | Time-based only |
| 22 | What patterns do you see? | ❌ NOT IMPL | - | Beta: LearnedPattern reporting |
| 23 | What risks should I be aware of? | ❌ NOT IMPL | - | Beta: Stale project detection |
| 24 | What opportunities should I pursue? | ❌ NOT IMPL | - | Beta: Feature suggestions |
| 25 | What's the next milestone? | ❌ NOT IMPL | - | Beta: Milestone extraction |

### ❌ Conversational Queries (0% - New)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 26 | What else can you help with? | ❌ NOT IMPL | - | Contextual discovery |
| 27 | Tell me more about X | ❌ NOT IMPL | - | Feature deep-dive |
| 28 | How do I use X? | ❌ NOT IMPL | - | Feature guidance |
| 29 | What changed since X? | ❌ NOT IMPL | - | Diff view |
| 30 | What needs my attention? | ❌ NOT IMPL | - | Notification aggregation |

### ❌ Scheduling & Reminders (0% - New)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 31 | Schedule a meeting about X | ❌ NOT IMPL | - | Calendar creation |
| 32 | Remind me to X | ❌ NOT IMPL | - | Reminder system |
| 33 | Find time for X with Y | ❌ NOT IMPL | - | Calendar deconfliction |
| 34 | How much time in meetings? | ❌ NOT IMPL | - | Time audit |
| 35 | Review my recurring meetings | ❌ NOT IMPL | - | Meeting audit |

### ❌ Document Management (0% - New)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 36 | Create doc from conversation | ❌ NOT IMPL | - | Conversation → Doc |
| 37 | Compare these documents | ❌ NOT IMPL | - | Document diff |
| 38 | Synthesize these sources | ❌ NOT IMPL | - | Multi-doc synthesis |
| 39 | Find docs about X | ❌ NOT IMPL | - | Notion search (partial via #20) |
| 40 | Update the X document | ❌ NOT IMPL | - | Notion update |

### ❌ GitHub Operations (0% - New)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 41 | What did we ship this week? | ❌ NOT IMPL | - | Release tracking |
| 42 | Show me stale PRs | ❌ NOT IMPL | - | PR hygiene |
| 43 | What's blocking the milestone? | ❌ NOT IMPL | - | Blocker identification |
| 44 | Create issues from this meeting | ❌ NOT IMPL | - | Meeting → Issues |
| 45 | Close completed issues | ❌ NOT IMPL | - | Issue hygiene |
| 58 | Update issue #X | ❌ NOT IMPL | - | Issue mutation |
| 59 | Comment on issue #X | ❌ NOT IMPL | - | Issue discussion |
| 60 | Review issue #X | ❌ NOT IMPL | - | Issue inspection |

### ⚠️ Slack Communication (40% - Issue #520)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 46 | Any mentions I missed? | ❌ NOT IMPL | - | Mention tracking |
| 47 | Summarize #channel | ❌ NOT IMPL | - | Channel digests |
| 48 | Post update to team | ❌ NOT IMPL | - | Broadcast messages |
| 49 | /standup | ✅ PASS | test_slash_commands.py | Issue #520; generates standup via Slack |
| 50 | /piper help | ✅ PASS | test_slash_commands.py | Issue #520; dynamic capabilities list |

### ❌ Productivity Tracking (0% - New)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 51 | What's my productivity? | ❌ NOT IMPL | - | Personal metrics |
| 52 | Are we on track? | ❌ NOT IMPL | - | Goal tracking |
| 53 | What did the team accomplish? | ❌ NOT IMPL | - | Team metrics |

### ❌ Todo Management (0% - Critical Gap)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 54 | Add a todo | ❌ NOT IMPL | - | **FUNDAMENTAL CRUD** |
| 55 | Complete todo | ❌ NOT IMPL | - | **FUNDAMENTAL CRUD** |
| 56 | Show my todos | ❌ NOT IMPL | - | **FUNDAMENTAL CRUD** |
| 57 | What's my next todo? | ❌ NOT IMPL | - | Priority query |

### ❌ Calendar Extended (0% - New)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 61 | What's my week look like? | ❌ NOT IMPL | - | Week planning |
| 62 | Check calendar conflicts | ❌ NOT IMPL | - | Conflict detection |

### ❌ Knowledge Operations (0% - New)

| # | Query | Status | Test File | Notes |
|---|-------|--------|-----------|-------|
| 63 | Upload a file | ❌ NOT IMPL | - | Knowledge ingestion |

---

## Testing Protocol

### For E2E Alpha Testing

1. **Test PASS queries first** (19 queries)
   - Verify all formatters (EMBEDDED/STANDARD/GRANULAR)
   - Test with real data
   - Confirm graceful degradation

2. **Test PARTIAL queries** (1 query)
   - Verify current functionality
   - Document what's missing
   - Test fallback behavior

3. **Test NOT IMPL queries** (43 queries)
   - Verify graceful "not implemented" response
   - Document user experience
   - Note which feel most critical

### Priority for Implementation

**Critical Gaps** (implement first):
1. Todo CRUD (#54-57) - Fundamental functionality missing
2. GitHub mutations (#58-60) - Users expect these
3. Conversational glue (#26-30) - Discovery issues

**Beta Targets** (next wave):
1. Complete Predictive (#21-25) - Infrastructure exists
2. Scheduling basics (#31-32) - Calendar integration
3. ~~Core Slack (#49-50) - Slash commands~~ ✅ Complete (Issue #520)

**v1.0 Targets** (production ready):
1. Document management (#36-40)
2. GitHub advanced (#41-45)
3. Productivity tracking (#51-53)

---

## Test Coverage Commands

```bash
# Run all canonical tests
pytest tests/unit/services/intent_service/test_canonical_handlers.py -v

# Run specific category tests
pytest tests/unit/services/intent_service/test_canonical_handlers.py::TestIdentityQueries -v
pytest tests/unit/services/intent_service/test_canonical_handlers.py::TestTemporalQueries -v
pytest tests/unit/services/intent_service/test_canonical_handlers.py::TestSpatialQueries -v

# Run agenda-specific tests
pytest tests/unit/services/intent_service/test_agenda_query.py -v

# Run document handler tests
pytest tests/unit/services/intent_service/test_document_handlers.py -v

# Count total tests
pytest tests/unit/services/intent_service/ --co -q | grep "<Function\|<Method" | wc -l
# Current: 227 tests (intent service)
# Standup tests: 260 tests (services/standup)
```

---

## Notes for Lead Developer

### When Testing NOT IMPL Queries
These should return graceful fallback messages, not errors:
- HTTP 200 (not 422)
- User-friendly message
- Suggestion for alternatives

### When Testing PARTIAL Queries
Document specifically what works vs what doesn't:
- Query #21 returns time-based guidance
- Missing: calendar integration, urgency signals

### When Adding New Implementations
1. Update this matrix
2. Add tests to test files
3. Verify all 3 formatters
4. Update ALPHA_KNOWN_ISSUES.md
5. Close GitHub issue with evidence

---

*Use this matrix for systematic E2E testing of all canonical queries. Update after each implementation sprint.*
