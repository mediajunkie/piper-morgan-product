# Canonical Query Test Matrix

> ⚠️ **HISTORICAL — SUPERSEDED 2026-04-11**
> This v1 matrix describes a pre-M1 architecture in which canonical handlers were the primary routing destination. After the M1 floor inversion (#911) and the Apr 8 IDENTITY full migration to floor (commit 33e6758a), most read-only categories route to the conversational floor instead.
>
> **Use [canonical-query-test-matrix-v3.md](../canonical-query-test-matrix-v3.md)** for current methodology and routing expectations.
>
> This file is retained for historical reference only.

---

**Purpose**: Ground truth for alpha testing - what Piper can actually do
**Related**: ADR-039 (Canonical Query Architecture), Issue #492 (Canonical test matrix)
**Last Updated**: December 24, 2025

## Overview

This test matrix provides the definitive reference for testing Piper's canonical query capabilities. It maps the 25 canonical queries from `dev/active/canonical-queries-list.md` to actual handler behavior, providing honest assessments of what works, what's partial, and what's not yet implemented.

**Critical for Alpha**: Testers need to know what Piper can actually do vs. what returns placeholders. This document is the ground truth.

## Summary

| Category | Total | PASS | PARTIAL | FAIL | NOT IMPL |
|----------|-------|------|---------|------|----------|
| Identity | 5 | 5 | 0 | 0 | 0 |
| Temporal | 5 | 5 | 0 | 0 | 0 |
| Spatial | 5 | 4 | 0 | 0 | 1 |
| Capability | 5 | 5 | 0 | 0 | 0 |
| Predictive | 5 | 0 | 1 | 0 | 4 |
| **Total** | **25** | **19** | **1** | **0** | **5** |

**Legend:**
- **PASS**: Fully functional, returns real data
- **PARTIAL**: Works but returns limited/hardcoded data
- **FAIL**: Returns error or incorrect response
- **NOT IMPL**: Returns placeholder/"capability pending" message

---

## Detailed Matrix

### Identity Queries (1-5)

**Handler**: `canonical_handlers.py::_handle_identity_query()`
**Status**: ✅ COMPLETE (5/5 PASS)

| # | Query | Expected Behavior | Actual Behavior | Status | Notes |
|---|-------|------------------|-----------------|--------|-------|
| 1 | What's your name? | Name + role description | "I'm Piper Morgan, your AI Product Management assistant..." | ✅ PASS | Works correctly with spatial awareness |
| 2 | What can you help me with? | Dynamic capability list from active plugins | Queries PluginRegistry for active integrations, returns core capabilities + dynamic plugin list | ✅ PASS | Issue #493 - Complete with tests |
| 3 | Are you working properly? | System health check | Checks database + integrations, returns health status with spatial formatting | ✅ PASS | Issue #506 - Complete with tests |
| 4 | How do I get help? | Onboarding/help guidance | Returns help resources, getting started guides, example queries with spatial formatting | ✅ PASS | Issue #507 - Complete with tests |
| 5 | What makes you different? | Unique value proposition | Returns unique features, positioning vs other tools, dynamic capabilities with spatial formatting | ✅ PASS | Issue #508 - Complete with tests |

**Current Implementation**:
```python
# Issue #493: Dynamic capabilities from PluginRegistry (COMPLETE)
capabilities = self._get_dynamic_capabilities()
# Returns:
# {
#   "core": ["development coordination", "issue tracking", "strategic planning"],
#   "integrations": [{"name": "slack", "description": "...", "capabilities": [...]}],
#   "capabilities_list": ["development coordination", ..., "slack integration", ...]
# }
```

**What Needs to Happen**:
1. ~~Query #2: Query active integrations to build dynamic capability list~~ ✅ DONE (Issue #493)
2. ~~Query #3: Add health check handler (ping services, check config)~~ ✅ DONE (Issue #506)
3. ~~Query #4: Add help/onboarding handler (link to docs, show first steps)~~ ✅ DONE (Issue #507)
4. ~~Query #5: Add differentiation handler (unique features vs other tools)~~ ✅ DONE (Issue #508)

**Identity Category: 100% COMPLETE** 🎉

---

### Temporal Queries (6-10)

**Handler**: `canonical_handlers.py::_handle_temporal_query()`
**Status**: Datetime and agenda work; historical/activity queries not implemented

| # | Query | Expected Behavior | Actual Behavior | Status | Notes |
|---|-------|------------------|-----------------|--------|-------|
| 6 | What day is it? | Current date/time with calendar context | "Today is Saturday, December 21, 2025 at 02:30 PM PT." + calendar info | ✅ PASS | Works with Calendar integration |
| 7 | What did we accomplish yesterday? | Todo/commit summary from yesterday | Queries completed todos from yesterday with spatial formatting | ✅ PASS | Issue #501 - Historical retrospective |
| 8 | What's on the agenda for today? | Today's todos + calendar + priorities | Aggregates calendar + todos + priorities with spatial formatting | ✅ PASS | Issue #499 - Full agenda aggregation |
| 9 | When was the last time we worked on this? | Last modified timestamp for project/issue | Queries GitHub for recent activity, formats with spatial awareness | ✅ PASS | Issue #504 - Last activity temporal query |
| 10 | How long have we been working on this project? | Project duration calculation | Calculates duration from project created_at with spatial formatting | ✅ PASS | Issue #505 - Project duration temporal query |

**Current Implementation**:
```python
# Issue #501: Retrospective detection routes to _handle_retrospective_query()
if self._detect_retrospective_request(intent):
    return await self._handle_retrospective_query(intent, session_id)
    # Queries: completed todos from yesterday via TodoDB.completed_at
    # Formats: EMBEDDED (brief) / STANDARD (balanced) / GRANULAR (detailed)

# Issue #499: Agenda detection routes to _handle_agenda_query()
if self._detect_agenda_request(intent):
    return await self._handle_agenda_query(intent, session_id)
    # Aggregates: calendar_context + todos + priorities
    # Formats: EMBEDDED (brief) / STANDARD (balanced) / GRANULAR (detailed)

# Issue #504: Last activity detection routes to _handle_temporal_last_activity()
project_name = self._detect_last_activity_request(intent)
if project_name:
    return await self._handle_temporal_last_activity(intent, session_id, project_name)
    # Queries: GitHub recent activity (last 30 days)
    # Formats: EMBEDDED (brief) / STANDARD (balanced) / GRANULAR (detailed)

# Issue #505: Project duration detection routes to _handle_temporal_project_duration()
duration_project = self._detect_duration_request(intent)
if duration_project:
    return await self._handle_temporal_project_duration(intent, session_id, duration_project)
    # Queries: PIPER.user.md for project created_at
    # Calculates: Duration in months/weeks/days
    # Formats: EMBEDDED (brief) / STANDARD (balanced) / GRANULAR (detailed)

# Otherwise: handles datetime queries
current_date = datetime.now().strftime("%A, %B %d, %Y")
current_time = datetime.now().strftime(f"%I:%M %p {timezone_short}")
# Returns: "Today is {date} at {time}. {calendar_context}"
```

**What Needs to Happen**:
1. ~~Query #7: Add `_handle_retrospective_query()` - query todos/commits from yesterday~~ ✅ DONE (Issue #501)
2. ~~Query #8: Add `_handle_agenda_query()` - aggregate todos + calendar + priorities~~ ✅ DONE (Issue #499)
3. ~~Query #9: Add `_handle_temporal_last_activity()` - query last modified timestamp~~ ✅ DONE (Issue #504)
4. ~~Query #10: Add `_handle_temporal_project_duration()` - calculate project timeline~~ ✅ DONE (Issue #505)

---

### Spatial Queries (11-15)

**Handler**: `canonical_handlers.py::_handle_status_query()` (queries 11-14), `canonical_handlers.py::_handle_priority_query()` (query 13)
**Status**: ✅ 4/5 PASS (only #15 lifecycle detection NOT IMPL)

| # | Query | Expected Behavior | Actual Behavior | Status | Notes |
|---|-------|------------------|-----------------|--------|-------|
| 11 | What projects are we working on? | List of active projects from PIPER.md | Returns project list with GitHub metadata (open issues, recent activity) | ✅ PASS | Issue #509 - Complete with tests |
| 12 | Show me the project landscape | Project portfolio with status/health | Groups projects by health status (healthy/at-risk/stalled) with spatial formatting | ✅ PASS | Issue #510 - Complete with tests |
| 13 | Which project should I focus on? | Priority recommendation based on context | Calculates priority score (staleness + issues + urgency), returns ranked recommendations | ✅ PASS | Issue #511 - Complete with tests |
| 14 | What's the status of project X? | Specific project status/progress | Extracts project name, shows detailed status with GitHub issues | ✅ PASS | Issue #500 - Project-specific detection + formatting |
| 15 | Where are we in the project lifecycle? | Lifecycle phase detection | Not implemented | ❌ NOT IMPL | Needs workflow state tracking |

**Current Implementation** (Query #11-14):
```python
# Issue #500: Project-specific detection
specific_project = self._detect_project_specific_query(intent, projects)
if specific_project:
    return self._format_project_specific_status(project, metadata, user_context, spatial_pattern)
    # Shows: Open issues, issue previews, repository link, organization

# Returns projects from PIPER.md (user_context)
projects = user_context.projects  # List with GitHub metadata
```

**What Needs to Happen**:
1. ~~Query #11: Add project metadata (issues, activity)~~ ✅ DONE (Issue #509)
2. ~~Query #12: Add project health metrics (commits, issues, activity)~~ ✅ DONE (Issue #510)
3. ~~Query #13: Add priority recommendation engine (context-aware)~~ ✅ DONE (Issue #511)
4. ~~Query #14: Add project-specific status handler (extract project name from query)~~ ✅ DONE (Issue #500)
5. Query #15: Add lifecycle tracking (detect phase from workflow state) - **Deferred** (may remove from canonical list)

---

### Capability Queries (16-20)

**Handler**: `intent_service.py::_handle_execution_intent()` + various domain handlers
**Status**: ✅ COMPLETE (5/5 PASS)

| # | Query | Expected Behavior | Actual Behavior | Status | Notes |
|---|-------|------------------|-----------------|--------|-------|
| 16 | Create a GitHub issue about X | Create issue via GitHub integration | Uses default repo from PIPER.md, auto-generates title from message, applies default labels | ✅ PASS | Issue #494 - Full defaults from config |
| 17 | Analyze this document | Document analysis via MCP or Notion | Routes to `_handle_analyze_document_notion()` - fetches page content and provides analysis summary. Graceful fallback if Notion not configured. | ✅ PASS | Issue #515 - Complete with 13 tests |
| 18 | List all my projects | Return project list | Routes to Query #11 handler - returns project list with GitHub metadata | ✅ PASS | Detected by _detect_project_list_request() |
| 19 | Give me a status report | Create aggregated status report | Aggregates project health + open todos with spatial formatting | ✅ PASS | Issue #513 - Complete with tests |
| 20 | Search for X in our documents | Document search via Notion/MCP | Routes to `_handle_search_documents_notion()` - searches Notion and returns formatted results. Graceful fallback if Notion not configured. | ✅ PASS | Issue #516 - Complete with 13 tests |

**Current Implementation** (Query #16):
```python
# Issue #494: GitHub issue creation with full defaults from PIPER.md
if mapped_action in ["create_issue", "create_ticket"]:
    return await self._handle_create_issue(intent, workflow.id, session_id)
    # Defaults:
    # - repository: github_config.default_repository from PIPER.md
    # - title: First 50 chars of message if not specified
    # - labels: github_config.default_labels from PIPER.md
    # Returns: Issue URL with repository info
```

**Current Implementation** (Query #17 - Document Analysis via Notion):
```python
# Issue #515: Document analysis via Notion
# In intent_service.py::_handle_analysis_intent()
if intent.action in ["analyze_document", "analyze_file"]:
    return await self._handle_analyze_document_notion(intent, workflow.id, session_id)
    # Checks: NotionIntegrationRouter.is_configured()
    # Searches: For document if no document_id in context
    # Fetches: Page data and blocks via get_page() and get_page_blocks()
    # Returns: Analysis summary with extracted text content
    # Fallback: Graceful message if Notion not configured
```

**Current Implementation** (Query #20 - Document Search via Notion):
```python
# Issue #516: Document search via Notion
# In intent_service.py::_handle_query_intent()
if intent.action in ["search_documents", "find_documents", "search_notion"]:
    return await self._handle_search_documents_notion(intent, workflow.id, session_id)
    # Checks: NotionIntegrationRouter.is_configured()
    # Extracts: Search query from context
    # Calls: NotionIntegrationRouter.search_notion()
    # Returns: Formatted results with titles and URLs
    # Fallback: Graceful message if Notion not configured
```

**Current Implementation** (Query #19):
```python
# Issue #513: Status report detection routes to _handle_status_report()
if self._detect_status_report_request(intent):
    return await self._handle_status_report(intent, session_id, user_context, spatial_pattern)
    # Aggregates: project health summary + open todos count
    # Formats: EMBEDDED (brief) / STANDARD (balanced) / GRANULAR (detailed)
```

**What Needs to Happen**:
1. ~~Query #17: Add document analysis handler (integrate with MCP/Notion)~~ ✅ DONE (Issue #515)
2. ~~Query #19: Add simplified status report handler (no params required)~~ ✅ DONE (Issue #513)
3. ~~Query #20: Add document search handler (integrate with Notion/MCP)~~ ✅ DONE (Issue #516)

**Capability Category: 100% COMPLETE** 🎉

---

### Predictive Queries (21-25)

**Handler**: `canonical_handlers.py::_handle_guidance_query()` (query 21), `canonical_handlers.py::_handle_priority_query()` (query 21)
**Status**: Time-based guidance works, but no pattern/risk/opportunity detection

| # | Query | Expected Behavior | Actual Behavior | Status | Notes |
|---|-------|------------------|-----------------|--------|-------|
| 21 | What should I focus on today? | Contextual guidance based on priorities + time | Returns time-of-day advice + top priority from PIPER.md | ⚠️ PARTIAL | Works for basic guidance, but limited intelligence |
| 22 | What patterns do you see? | Pattern detection from historical data | Not implemented | ❌ NOT IMPL | Needs LEARNING intent handler |
| 23 | What risks should I be aware of? | Risk analysis from project data | Not implemented | ❌ NOT IMPL | Needs risk detection handler |
| 24 | What opportunities should I pursue? | Opportunity recommendation from context | Not implemented | ❌ NOT IMPL | Needs opportunity detection handler |
| 25 | What's the next milestone? | Milestone detection from roadmap/calendar | Not implemented | ❌ NOT IMPL | Needs milestone tracking handler |

**Current Implementation** (Query #21):
```python
# Time-based guidance only
def _get_immediate_focus(self, current_hour: int, user_context):
    if 6 <= current_hour < 9:
        return "Morning development work - perfect time for deep focus..."
    elif 9 <= current_hour < 14:
        return "Collaboration time - coordinate with your team..."
    # ... etc for different time blocks
```

**What Needs to Happen**:
1. Query #21: Enhance with calendar context, deadline awareness, workload analysis
2. Query #22: Add pattern detection handler (use LEARNING intent)
3. Query #23: Add risk analysis handler (blocked issues, overdue tasks, dependency conflicts)
4. Query #24: Add opportunity detection (underutilized features, optimization suggestions)
5. Query #25: Add milestone tracking (parse roadmap, detect next deadline)

---

## Testing Protocol

### For Alpha Testers

1. **Test Tier 1: PASS Queries** (Expected to work)
   - Query #1: "What's your name?"
   - Query #6: "What day is it?"
   - Query #7: "What did we accomplish yesterday?"
   - Query #8: "What's on the agenda for today?"
   - Query #14: "What's the status of [project name]?"

   **Expected**: Correct, complete responses

2. **Test Tier 2: PARTIAL Queries** (Works with limitations)
   - Query #21: "What should I focus on today?" (time-based only)

   **Expected**: Functional but limited responses

3. **Test Tier 3: NOT IMPL Queries** (Graceful fallback)
   - Query #15: Lifecycle phase detection
   - Queries #22-25: Pattern/risk/opportunity/milestone detection

   **Expected**: Friendly "not yet implemented" message

4. **Test Tier 4: Notion-Dependent Queries** (Works with Notion configured)
   - Query #17: Document analysis (via Notion)
   - Query #20: Document search (via Notion)

   **Expected**: Returns Notion results if configured, graceful fallback if not

### For Developers

**Smoke Test Coverage**:
```bash
# Test PASS queries
curl -X POST http://localhost:8001/api/v1/intent \
  -d '{"message": "What is your name?"}' \
  -H "Content-Type: application/json"

curl -X POST http://localhost:8001/api/v1/intent \
  -d '{"message": "What day is it?"}' \
  -H "Content-Type: application/json"

# Test PARTIAL queries
curl -X POST http://localhost:8001/api/v1/intent \
  -d '{"message": "What can you help me with?"}' \
  -H "Content-Type: application/json"

curl -X POST http://localhost:8001/api/v1/intent \
  -d '{"message": "Create a GitHub issue about testing"}' \
  -H "Content-Type: application/json"

# Test NOT IMPL queries
curl -X POST http://localhost:8001/api/v1/intent \
  -d '{"message": "What patterns do you see?"}' \
  -H "Content-Type: application/json"
```

**Expected Responses**:
- PASS: Real data with confidence=1.0
- PARTIAL: Limited data but no errors
- NOT IMPL: Graceful fallback message, success=true

---

## Implementation Roadmap

### Phase 1: Complete Partial Features
**Priority**: ✅ COMPLETE (Alpha blocker resolved)
**Effort**: N/A (all high-priority features implemented)

- [x] Query #2: Dynamic capability list from active integrations ✅ Issue #493
- [x] Query #11: Add project metadata (status, health, activity) ✅ Issue #509
- [x] Query #16: GitHub issue creation with full defaults ✅ Issue #494
- [ ] Query #21: Enhance guidance with calendar/deadline awareness (PARTIAL - time-based only)

### Phase 2: Add Missing Temporal Handlers
**Priority**: ✅ COMPLETE
**Effort**: N/A (all temporal queries implemented)

- [x] Query #7: Historical retrospective handler ✅ Issue #501
- [x] Query #8: Daily agenda aggregation handler ✅ Issue #499
- [x] Query #9: Last activity tracker ✅ Issue #504
- [x] Query #10: Project duration calculator ✅ Issue #505

### Phase 3: Add Missing Spatial Handlers
**Priority**: MEDIUM (Post-alpha)
**Effort**: 1-2 days (reduced - #14 complete)

- [ ] Query #12: Project portfolio health view
- [ ] Query #13: Intelligent priority recommendation
- [x] Query #14: Project-specific status handler ✅ Issue #500
- [ ] Query #15: Lifecycle phase detection

### Phase 4: Add Missing Capability Handlers
**Priority**: ✅ COMPLETE
**Effort**: N/A (all capability queries implemented)

- [x] Query #17: Document analysis (MCP/Notion integration) ✅ Issue #515
- [x] Query #19: Simplified status report generator ✅ Issue #513
- [x] Query #20: Document search (Notion/MCP integration) ✅ Issue #516

### Phase 5: Add Predictive Handlers
**Priority**: LOW (Future enhancement)
**Effort**: 5-7 days

- [ ] Query #22: Pattern detection (LEARNING intent)
- [ ] Query #23: Risk analysis
- [ ] Query #24: Opportunity detection
- [ ] Query #25: Milestone tracking

---

## Known Issues

### Issue #492: Missing Test Matrix
**Status**: ✅ RESOLVED (this document)
**Resolution**: Created comprehensive test matrix

### Issue #489: 422 Errors for Unhandled Capabilities
**Status**: ✅ RESOLVED
**Resolution**: Added graceful fallback for unhandled EXECUTION actions
**File**: `services/intent/intent_service.py:721-745`

### PIPER.md Dependency
**Status**: ⚠️ PARTIAL
**Impact**: Queries #11-13, #21 fail if PIPER.md missing
**Mitigation**: Returns helpful error message with setup guidance
**File**: `services/intent_service/canonical_handlers.py:331-347`

### Issue #493: Hardcoded Capabilities
**Status**: ✅ RESOLVED
**Impact**: Query #2 previously returned outdated hardcoded capability list
**Resolution**: Implemented `_get_dynamic_capabilities()` to query PluginRegistry for active integrations
**File**: `services/intent_service/canonical_handlers.py:60-109`
**Tests**: `tests/unit/services/intent_service/test_canonical_handlers.py` (9 tests passing)

### Issue #498: Setup Request Routing
**Status**: ✅ RESOLVED
**Issue**: "Help me set up my projects" routed to generic GUIDANCE response
**Resolution**: Added setup request detection in GUIDANCE handler
**File**: `services/intent_service/canonical_handlers.py:1305-1516`
**Behavior**: Now detects setup requests for projects, integrations, and general setup, returning structured guidance with settings links

### Issue #500: Project-Specific Status Query
**Status**: ✅ RESOLVED
**Issue**: "What's the status of project X?" returned generic all-projects list
**Resolution**: Added `_detect_project_specific_query()` + `_format_project_specific_status()`
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Extracts project name from query, shows detailed single-project status with GitHub issues

### Issue #501: Historical Retrospective Query
**Status**: ✅ RESOLVED
**Issue**: "What did we accomplish yesterday?" returned datetime only
**Resolution**: Added `_detect_retrospective_request()` + `_handle_retrospective_query()`
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Queries TodoDB.completed_at for todos completed yesterday, formats with spatial awareness

### Issue #504: Last Activity Temporal Query
**Status**: ✅ RESOLVED
**Issue**: "When was the last time we worked on X?" returned datetime only
**Resolution**: Added `_detect_last_activity_request()` + `_handle_temporal_last_activity()`
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Queries GitHub for recent activity (last 30 days), formats with spatial awareness (EMBEDDED/STANDARD/GRANULAR)
**Tests**: 14 tests in `tests/unit/services/intent_service/test_canonical_handlers.py`

### Issue #505: Project Duration Temporal Query
**Status**: ✅ RESOLVED
**Issue**: "How long have we been working on X?" returned datetime only
**Resolution**: Added `_detect_duration_request()` + `_handle_temporal_project_duration()` + `_calculate_duration()` + formatting methods
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Queries PIPER.user.md for project created_at, calculates duration in months/weeks/days, formats with spatial awareness (EMBEDDED/STANDARD/GRANULAR)
**Tests**: 18 tests in `tests/unit/services/intent_service/test_canonical_handlers.py` (6 detection, 4 calculation, 8 formatting)

### Issue #506: Health Check Identity Query
**Status**: ✅ RESOLVED
**Issue**: "Are you working properly?" returned generic identity response
**Resolution**: Added `_detect_health_check_request()` + `_handle_identity_health_check()` + `_get_system_health()` + formatting methods
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Checks database connection + plugin status, returns health report with spatial awareness (EMBEDDED/STANDARD/GRANULAR)
**Tests**: 13 tests in `tests/unit/services/intent_service/test_canonical_handlers.py` (7 detection, 6 formatting)

### Issue #509: Project List with Metadata
**Status**: ✅ RESOLVED
**Issue**: "What projects are we working on?" returned names only without metadata
**Resolution**: Added `_detect_project_list_request()` + `_handle_spatial_project_list()` + formatting methods
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Returns project list with GitHub metadata (open issues, recent activity) with spatial awareness
**Tests**: 8 tests in `tests/unit/services/intent_service/test_canonical_handlers.py`

### Issue #510: Project Landscape Health View
**Status**: ✅ RESOLVED
**Issue**: "Show me the project landscape" returned same as project list
**Resolution**: Added `_detect_landscape_request()` + `_calculate_project_health()` + `_handle_spatial_project_landscape()` + formatting methods
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Groups projects by health status (healthy/at-risk/stalled), calculates based on activity and issue count
**Tests**: 18 tests in `tests/unit/services/intent_service/test_canonical_handlers.py`

### Issue #511: Priority Recommendation
**Status**: ✅ RESOLVED
**Issue**: "Which project should I focus on?" returned generic priority list
**Resolution**: Added `_detect_priority_recommendation_request()` + `_calculate_priority_score()` + `_handle_spatial_priority_recommendation()` + formatting methods
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Calculates priority score (staleness + issues + urgency), returns ranked recommendations with reasoning
**Tests**: 17 tests in `tests/unit/services/intent_service/test_canonical_handlers.py`

### Issue #513: Status Report Generator
**Status**: ✅ RESOLVED
**Issue**: "Give me a status report" returned graceful fallback or required specific params
**Resolution**: Added `_detect_status_report_request()` + `_handle_status_report()` + formatting methods (embedded/standard/granular)
**File**: `services/intent_service/canonical_handlers.py`
**Behavior**: Aggregates project health summary (healthy/at-risk/stalled) + open todos count, formats with spatial awareness
**Tests**: 15 tests in `tests/unit/services/intent_service/test_canonical_handlers.py` (8 detection, 7 formatting)

### Issue #515: Document Analysis via Notion
**Status**: ✅ RESOLVED
**Issue**: "Analyze this document" returned graceful fallback instead of using Notion
**Resolution**: Added routing in `_handle_analysis_intent()` + `_handle_analyze_document_notion()` handler
**File**: `services/intent/intent_service.py`
**Behavior**: Checks Notion configuration, searches for document, fetches page content and blocks, returns analysis summary. Graceful fallback if Notion not configured.
**Tests**: 13 tests in `tests/unit/services/intent_service/test_document_handlers.py`

### Issue #516: Document Search via Notion
**Status**: ✅ RESOLVED
**Issue**: "Search for X in our documents" returned graceful fallback instead of using Notion
**Resolution**: Added routing in `_handle_query_intent()` + `_handle_search_documents_notion()` handler
**File**: `services/intent/intent_service.py`
**Behavior**: Checks Notion configuration, extracts search query, calls Notion search API, formats results with titles and URLs. Graceful fallback if Notion not configured.
**Tests**: 13 tests in `tests/unit/services/intent_service/test_document_handlers.py`

---

## Additional Capabilities (Beyond 25 Canonical Queries)

The following capabilities have been added beyond the original 25 canonical queries:

### Setup Guidance Queries
**Handler**: `canonical_handlers.py::_handle_guidance_query()` (via `_detect_setup_request()`)
**Status**: ✅ IMPLEMENTED (Issue #498)

| Query | Expected Behavior | Actual Behavior | Status |
|-------|------------------|-----------------|--------|
| Help me set up my projects | Project configuration guidance | Returns setup steps + link to /settings/projects | ✅ PASS |
| Configure my integrations | Integration setup guidance | Returns integration list + setup links | ✅ PASS |
| Get started with Piper | General onboarding | Returns getting started checklist | ✅ PASS |

---

## Verification

**Last Verified**: December 24, 2025 (Updated with Issues #515, #516 - Document analysis and search via Notion)
**Verification Method**: Code inspection + handler tracing + unit tests
**Files Reviewed**:
- `services/intent_service/canonical_handlers.py` (~4015 lines)
- `services/intent/intent_service.py` (updated with document handlers)
- `dev/active/canonical-queries-list.md` (25 queries)
- `tests/unit/services/intent_service/test_canonical_handlers.py` (227 tests total, all passing)
- `tests/unit/services/intent_service/test_document_handlers.py` (13 tests, all passing)

**Next Verification**: After each implementation phase (Phase 1-5 above)

---

## References

- **ADR-039**: Canonical Query Architecture
- **Issue #489**: 422 errors for unhandled capabilities (resolved)
- **Issue #492**: Create canonical query test matrix
- **Issue #493**: Dynamic capability list from PluginRegistry (resolved)
- **Issue #498**: Setup request routing (resolved)
- **Issue #499**: Agenda aggregation query (resolved)
- **Issue #500**: Project-specific status query (resolved)
- **Issue #501**: Historical retrospective query (resolved)
- **Issue #504**: Last activity temporal query (resolved)
- **Issue #505**: Project duration temporal query (resolved)
- **Issue #506**: Health check identity query (resolved)
- **Issue #507**: Help request identity query (resolved)
- **Issue #508**: Differentiation identity query (resolved)
- **Issue #509**: Project list with metadata (resolved)
- **Issue #510**: Project landscape health view (resolved)
- **Issue #511**: Priority recommendation (resolved)
- **Issue #513**: Status report generator (resolved)
- **Issue #515**: Document analysis via Notion (resolved)
- **Issue #516**: Document search via Notion (resolved)
- **Canonical Query List**: `dev/active/canonical-queries-list.md`
- **Handler Implementation**: `services/intent_service/canonical_handlers.py`
- **Intent Router**: `services/intent/intent_service.py`
