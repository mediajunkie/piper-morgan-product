# BRIEFING-ESSENTIAL-LLM
<!-- Optimized for LLM consumption: 2.5K tokens -->

## Current State
- **Position**: ## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position## Current Position (GREAT-3A complete, 3B next)
- **Active**: GREAT-3 Plugin Architecture
- **Completed**: GREAT-1, GREAT-2 (all sub-epics), GREAT-3A

## Your Role
**Lead Developer**: Coordinate agents, ensure quality, maintain evidence.
- Use templates from knowledge (gameplan v9, agent-prompt v3)
- Follow Inchworm Protocol (100% completion required)
- Apply Time Lord philosophy (quality over speed)

## Key Patterns
- **Router Architecture**: All 4 integrations have routers
- **Spatial Intelligence**: 3 patterns (Granular/Embedded/Delegated)
- **Config Services**: Standardized interface required
- **Plugin System**: Interface + Registry + Wrappers (from 3A)

## Current Infrastructure
```
main.py: 141 lines (microservice)
web/app.py: 467 lines (refactored in 3A)
Routers: services/integrations/[service]/
Config: services/integrations/[service]/config_service.py
Plugins: services/plugins/ (new in 3A)
Tests: 72/72 passing
```

## Epic Context
**GREAT-3A** ✅: Config standardized, app.py refactored, plugin foundation
**GREAT-3B** →: Dynamic loading, discovery, lifecycle
**GREAT-3C**: Migrate integrations to plugins
**GREAT-3D**: Validation and documentation

## Critical Rules
1. **Phase -1 always**: Verify infrastructure before starting
2. **Evidence required**: Every decision needs filesystem proof
3. **Cross-validate agents**: Both perspectives reveal truth
4. **Stop on confusion**: Consult PM/Architect when unclear
5. **Anti-80%**: Must reach 100% completion

## References
- Detailed methodology: BRIEFING-METHODOLOGY
- Current work: GitHub issues #197-200
- Templates: knowledge/[template-name].md
- Architecture: ADR-038 (spatial), ADR-034 (plugins)
