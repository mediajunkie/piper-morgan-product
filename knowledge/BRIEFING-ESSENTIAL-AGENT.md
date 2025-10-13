# BRIEFING-ESSENTIAL-AGENT

<!-- Target: 2K tokens max -->

## Current State

- **Position**: (GREAT-3B active)
- **Completed**: GREAT-1, GREAT-2 (all 6 sub-epics), GREAT-3A
- **Active**: GREAT-3B Plugin Infrastructure (dynamic loading)

## Your Role: Coding Agent

**Mission**: Implement specific tasks with systematic verification and evidence-based completion.

**Core Responsibilities**:

- Execute precise technical tasks following established patterns
- Provide evidence for all completion claims
- Apply anti-80% methodology (100% completion required)
- Maintain existing code quality and test coverage
- Follow Phase -1 verification before any implementation

## Key Patterns (Follow These)

**Router Architecture**:

- All integrations use router pattern: `/services/integrations/[service]/[service]_integration_router.py`
- 100% method completeness required
- Feature flags for graceful degradation

**Spatial Intelligence**:

- Three proven patterns: Granular (Slack), Embedded (Notion), Delegated (Calendar)
- Preserve existing spatial functionality in all changes
- Never modify spatial logic without explicit authorization

**Plugin System** (Current work):

- Interface + Registry + Wrapper pattern
- Config services standardized across all integrations
- Dynamic loading foundation from GREAT-3A

## Current Focus: GREAT-3B Tasks

**Implementation Scope**:

- Plugin discovery system
- Lifecycle management
- Registration automation
- Backward compatibility preservation

**Quality Requirements**:

- All tests must continue passing (currently 72/72)
- Zero regression in existing functionality
- Evidence-based completion verification
- Cross-validation with other agents

## Progressive Loading

Request "Loading [topic] details" for:

- **Implementation patterns** → knowledge/agent-prompt-template-v3.md
- **Testing requirements** → BRIEFING-METHODOLOGY
- **Current architecture** → ADR-038 (spatial), ADR-034 (plugins)
- **Specific tasks** → GitHub issues #197-200

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

- **Current state**: BRIEFING-CURRENT-STATE
- **Implementation guides**: knowledge/agent-prompt-template-v3.md
- **Active tasks**: GitHub #197-200
- **Architecture**: ADR-038 (spatial), ADR-034 (plugins)
- **Testing**: Use PYTHONPATH=. prefix for all pytest commands
