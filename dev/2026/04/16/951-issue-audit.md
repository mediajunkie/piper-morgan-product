# Audit: #951 against .github/ISSUE_TEMPLATE/feature.md

**Date**: 2026-04-16
**Auditor**: Lead Dev (code-opus)
**Phase**: Issue → Gameplan (first audit gate for #951)

## Gap Analysis — What's Actually Missing

Before auditing against the template, I audited the *technical scope* — what's already implemented vs what the acceptance criteria still need. The current `context_assembler.py` is substantially more built out than the #951 body suggests.

| Acceptance Criterion (from #951) | Current State | Gap |
|---------------------------------|---------------|-----|
| Context assembler handles all floor-routed categories | ✅ Done | Assembler has gatherers for IDENTITY, DISCOVERY, TRUST, MEMORY, CONVERSATION, TEMPORAL, STATUS, PRIORITY, UNKNOWN |
| STATUS intents get project state, sprint position, recent activity | ⚠️ Partial | Has: projects list, pending_todos, github_connected flag. Missing: **sprint position**, **recent activity** |
| PRIORITY intents get priority profile, deadlines, blocked items | ⚠️ Partial | Has: priorities list, pending_todos. Missing: **deadlines** (todo `due_date` not surfaced!), **blocked items** |
| TEMPORAL intents get current time, calendar events, deadline proximity | ⚠️ Partial | Has: current_date, pending/completed todos, projects. Missing: **calendar events** (biggest gap — formatter already expects them), **deadline proximity** |
| Project portfolio data assembled (replaces #100) | ✅ Done | Basic portfolio in `_gather_status_priority_context` |
| Temporal context injected (replaces #101) | ✅ Partial | Todos + projects assembled; calendar missing |
| Context format consistent and parseable | ✅ Done | Dict-based, consistent with `_format_domain_context` in conversational_floor.py |
| Performance: no unreasonable blocking | ⚠️ | No caching; calendar adds external API latency |

**Biggest real gap**: **calendar is never queried by the assembler**, but `conversational_floor.py:_format_domain_context` (lines 316-330) *already expects* calendar data (`next_meeting`, `next_free_block`, `time_available_minutes`). This is a latent wire-up task — the formatter was written assuming the assembler would fill this, and never got connected.

**Second-biggest gap**: todos have `due_date` field support (`services/domain/models.py:1411`, `todo_management_service.py:74`) but the assembler doesn't surface it. "Deadline proximity" can be computed trivially from `due_date - now`.

**Deferred gaps** (larger scope, not blocking #950 verification):
- Sprint/milestone data from GitHub API
- Recent activity feed (commits, comments, reviews)
- Blocked items from GitHub (depends on label conventions)

## Matrix: Issue vs Feature Template

| Template Requirement | Status in #951 | Notes |
|---------------------|----------------|-------|
| Priority / Labels / Milestone / Epic header | ❌ | Not present |
| Problem Statement > Current State | ⚠️ | One-sentence context paragraph |
| Problem Statement > Impact | ❌ | Missing |
| Problem Statement > Strategic Context | ⚠️ | Partial (ADR-060 referenced) |
| Goal > Primary Objective | ⚠️ | Implicit in Summary |
| Goal > Example User Experience | ❌ | Missing — important for context-assembly work |
| Goal > Not In Scope | ❌ | Missing |
| What Already Exists | ❌ | Missing — this is the biggest oversight; assembler has 200+ lines of code the issue doesn't acknowledge |
| Requirements > Phases | ❌ | Missing |
| Acceptance Criteria > Functionality | ✅ | Present (8 items) |
| Acceptance Criteria > Testing | ❌ | Missing |
| Acceptance Criteria > Quality | ❌ | Missing |
| Acceptance Criteria > Documentation | ❌ | Missing |
| Completion Matrix | ❌ | Intentional — filled after |
| Testing Strategy | ❌ | Missing |
| Success Metrics | ❌ | Missing |
| STOP Conditions | ❌ | Missing |
| Effort Estimate | ❌ | Missing |
| Dependencies | ⚠️ | "Supersedes #100, #101" noted; no blocking deps |
| Related Documentation | ⚠️ | ADR-060 noted, but no links to current architecture docs |

## Fix Plan

Update #951 body to:

1. **Acknowledge what's actually already implemented** — prevent future agents from duplicating the 200+ lines of gatherers
2. **Narrow acceptance criteria to actual gaps** — calendar, deadlines, plus defer sprint/activity/blocked to follow-ups
3. **Add the standard template sections** — Problem Statement, Goal with before/after example, Not In Scope, What Already Exists, Testing Strategy, STOP Conditions, Effort Estimate, Dependencies

## Items to defer as follow-up issues (file before closing #951)

- Sprint/milestone data assembly (requires GitHub API calls, config decisions)
- Recent activity feed (requires time-windowed queries across integrations)
- Blocked items identification (requires label convention decision)
- Redis caching for context assembly (performance criterion)

These should become separate issues referenced from the closed #951, not hand-waved as done.

## Decision

Proceed with updating #951 body (narrower scope acknowledging current state), then write gameplan. New body draft in `951-issue-body-updated.md`.
