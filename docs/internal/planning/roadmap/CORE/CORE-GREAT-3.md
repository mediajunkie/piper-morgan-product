# GREAT-3: Plugin Architecture - Updated Description

## Overview
Transform current integration architecture into plugin-based system, addressing monolith refactoring and configuration repair as prerequisites.

## Context (Updated Oct 2)
- Router infrastructure complete for all 4 integrations
- Three spatial patterns operational (Granular, Embedded, Delegated MCP)
- main.py (1,107 lines) and web/app.py (1,001 lines) need refactoring
- Configuration refactoring artifacts need repair

## Scope
- Refactor monolithic files (main.py, web/app.py)
- Repair configuration issues identified by ConfigValidator
- Define plugin interface building on router patterns
- Create plugin infrastructure (loader, discovery, config)
- Migrate all 4 integrations to plugins
- Preserve existing spatial intelligence patterns
- Validate and document plugin architecture

## Decomposition
- **GREAT-3A**: Foundation & Refactoring (prerequisites + investigation)
- **GREAT-3B**: Plugin Infrastructure (interface, loader, config)
- **GREAT-3C**: Integration Migration (all 4 services to plugins)
- **GREAT-3D**: Validation & Documentation (tests, guide, ADRs)

## Acceptance Criteria
- [ ] Monolithic files refactored into modules
- [ ] Configuration issues resolved
- [ ] Plugin interface defined and implemented
- [ ] All 4 integrations work as plugins
- [ ] Spatial patterns preserved
- [ ] Plugins can be enabled/disabled
- [ ] Contract tests passing
- [ ] ADR-034 implementation complete

## Lock Strategy
- No direct integration imports in core
- Plugin interface contract tests
- Configuration validation passing
- All existing features still work

## Dependencies
- GREAT-2 complete ✅

## Estimated Duration
2-3 digas (quality over speed)

## Success Validation
```bash
# Monoliths refactored
wc -l main.py  # Should be <500 lines
wc -l web/app.py  # Should be <500 lines

# Configuration valid
python validate_config.py --all-services  # All pass

# Plugins working
ls -la plugins/  # Shows all 4 integrations
DISABLED_PLUGINS=github python main.py  # Starts without GitHub

# Tests passing
pytest tests/plugins/ -v
```
