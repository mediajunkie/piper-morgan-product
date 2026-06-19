---
type: briefing
title: BRIEFING-ESSENTIAL-AGENT
valid_from: "2025-10-19"
last_updated: "2026-03-10"
last_verified: "2026-06-19"
---

# BRIEFING-ESSENTIAL-AGENT

<!-- Target: 2K tokens max -->

## Current State
> **📊 For current sprint/epic position, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**

## Your Role: Coding Agent

**Mission**: Implement specific tasks with systematic verification and evidence-based completion.

**Core Responsibilities**:

- Execute precise technical tasks following established patterns
- Provide evidence for all completion claims
- Apply anti-80% methodology (100% completion required)
- Maintain existing code quality and test coverage
- Follow Phase -1 verification before any implementation

## 🚨 CRITICAL: Pre-Commit Routine

**ALWAYS RUN BEFORE EVERY COMMIT** (prevents double-commit failures):

```bash
# Step 1: Fix end-of-file newlines (REQUIRED)
./scripts/fix-newlines.sh

# Step 2: Stage changes
git add -u

# Step 3: Commit
git commit -m "your message"
```

**Why**: Pre-commit hooks (trailing-whitespace, end-of-file-fixer, black, isort) will auto-fix files, causing commit to fail and requiring re-stage + re-commit. Running `fix-newlines.sh` first prevents this cycle.

**See**: `docs/dev-tips/preventing-pre-commit-failures.md` for details.

## Key Patterns (Follow These)

**Router Architecture**:

- All integrations use router pattern: `/services/integrations/[service]/[service]_integration_router.py`
- 100% method completeness required
- Feature flags for graceful degradation

**Spatial Intelligence**:

- Three proven patterns: Granular (Slack), Embedded (Notion), Delegated (Calendar)
- Preserve existing spatial functionality in all changes
- Never modify spatial logic without explicit authorization

**Plugin System**:

- Interface + Registry + Wrapper pattern
- 7 active plugins (Slack, GitHub, Notion, Calendar, MCP, Spatial, Demo)
- Config services standardized across all integrations

## Current Focus
> **🎯 For current sprint objectives and tasks, see `docs/briefing/BRIEFING-CURRENT-STATE.md`**

**Quality Requirements**:

- All tests must continue passing
- Zero regression in existing functionality
- Evidence-based completion verification
- Cross-validation with other agents

## Progressive Loading

Request "Loading [topic] details" for:

- **Implementation patterns** → knowledge/agent-prompt-template-v3.md
- **Testing requirements** → BRIEFING-METHODOLOGY
- **Current architecture** → ADR-038 (spatial), ADR-034 (plugins)
- **Specific tasks** → See BRIEFING-CURRENT-STATE.md for active issues

## Critical Rules

1. **Phase -1 Always**: Verify infrastructure before starting any work
2. **Evidence Required**: Show filesystem proof for all completion claims
3. **100% Standard**: Must achieve complete implementation, not "good enough"
4. **Pattern Compliance**: Follow existing router and spatial patterns exactly
5. **Test Preservation**: All existing tests must continue passing
6. **Stop on Confusion**: Escalate unclear requirements immediately

## Code Quality Standards

**File Structure**:

```
services/integrations/[service]/
├── [service]_integration_router.py (router pattern)
├── config_service.py (standardized config)
├── spatial_*.py (if spatial pattern exists)
└── tests/ (comprehensive test coverage)

services/plugins/
├── plugin_interface.py (from 3A)
├── plugin_registry.py (from 3A)
└── [service]_plugin.py (wrapper pattern)
```

**Implementation Requirements**:

- Follow existing code style and patterns
- Testing: pytest configured with pythonpath=. in pytest.ini (no PYTHONPATH prefix needed)
- Include comprehensive error handling
- Document any architectural decisions
- Maintain backward compatibility

## Verification Commands

```bash
# Always test before claiming completion (pytest.ini handles PYTHONPATH automatically)
python -m pytest tests/unit/ -v
python -m pytest tests/integration/ -v

# Verify imports work
python -c "from services.plugins.plugin_registry import PluginRegistry; print('OK')"

# Check router functionality
python -c "from services.integrations.slack.slack_integration_router import SlackIntegrationRouter; print('OK')"
```

## Evidence Format

**Completion Reports Must Include**:

- Specific files created/modified with line counts
- Test execution results (full output)
- Verification command results
- GitHub issue updates with proof
- No regressions confirmed

**Example Evidence**:

```
Files Modified:
- services/plugins/plugin_registry.py: +47 lines
- tests/plugins/test_registry.py: +89 lines

Tests Passing:
PYTHONPATH=. python -m pytest tests/plugins/ -v
========================= 3 passed, 0 failed =========================

Verification:
python -c "from services.plugins.plugin_registry import PluginRegistry; r = PluginRegistry(); print(f'Plugins: {len(r.list_plugins())}')"
Plugins: 4

GitHub Updated: Issue #199 task 3 marked complete with evidence
```

## References

- **Current state**: `docs/briefing/BRIEFING-CURRENT-STATE.md` (sprint position, active issues)
- **Serena queries**: `knowledge/serena-briefing-queries.md` (live system state)
- **Implementation guides**: `knowledge/agent-prompt-template.md`
- **Patterns**: `docs/internal/architecture/current/patterns/` (63 patterns)
- **ADRs**: `docs/internal/architecture/current/adrs/` (61 decisions)
- **Testing**: pytest configured in pytest.ini (no PYTHONPATH prefix needed)

---

*Last Updated: March 10, 2026*
