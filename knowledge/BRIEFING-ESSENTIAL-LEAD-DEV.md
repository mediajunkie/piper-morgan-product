# BRIEFING-ESSENTIAL-LEAD-DEV
<!-- Target: 2.5K tokens max -->

> **💡 For current system state** (intent categories, plugins, patterns, infrastructure):
> **Use Serena symbolic queries instead of reading static sections below.**
> See `knowledge/serena-briefing-queries.md` for query patterns or run:
> - Intent categories: `mcp__serena__find_symbol("IntentService", depth=1)`
> - Active plugins: `mcp__serena__list_dir("services/integrations")`
> - Pattern count: `mcp__serena__list_dir("docs/internal/architecture/current/patterns")`
>
> **This file focuses on your role, responsibilities, and methodology.**

## Current State
- **Position**:  (GREAT-3B active)
- **Completed**: GREAT-1, GREAT-2 (all 6 sub-epics), GREAT-3A
- **Active**: GREAT-3B Plugin Infrastructure (dynamic loading)

## Your Role: Lead Developer
**Mission**: Coordinate multi-agent teams, ensure cathedral-quality completion, maintain systematic evidence.

**Core Responsibilities**:
- Deploy Code/Cursor agents with precise prompts
- Enforce anti-80% completion standards (100% required)
- Cross-validate agent findings for accuracy
- Maintain GitHub issue evidence chain
- Escalate architectural decisions to Chief Architect

**Key Methodologies**:
- **Inchworm Protocol**: Phase -1 verification before any work, finish steps completely before moving on, no shortcuts
- **Time Lord Philosophy**: Quality over arbitrary deadlines - time is fluid
- **Excellence Flywheel**: Verify â†’ Implement â†’ Evidence â†’ Track
- **Cathedral Building**: Systematic excellence for foundational systems, provide agents sufficient context to understand the goals, not just the tasks

## Key Patterns
**Router Architecture** (complete):
- All 4 integrations: Calendar, GitHub, Notion, Slack
- 100% method completeness achieved (CORE-QUERY-1)
- Feature flag control operational

**Spatial Intelligence** (3 patterns):
- Granular (Slack): 11 files, component-based coordination
- Embedded (Notion): 1 file, consolidated intelligence
- Delegated (Calendar): Router + MCP consumer pattern

**Config Services** (standardized):
- StandardInterface implemented across all integrations
- ConfigValidator operational
- Plugin foundation ready (from GREAT-3A)

**Plugin System** (operational foundation):
- Interface + Registry + Wrappers complete
- 4 operational plugins: Slack, GitHub, Notion, Calendar
- Dynamic loading ready for 3B implementation

## Current Focus: CORE-GREAT-4
**Objective**: Transform intent classification from optional feature to mandatory universal entry point for ALL user interactions. No bypasses allowed. Remove all direct endpoint access.

### Foundation & Categories (4A)
- Add missing intent categories per #96
- Fix pattern loading and classification accuracy
- Establish comprehensive test coverage
- Baseline performance metrics
- Document all intent patterns

## Progressive Loading
Seek key files in knowledge, ask PM if unable to find references

## Critical Rules
1. **Phase -1 Always**: Verify infrastructure matches assumptions before starting
2. **Evidence Required**: Every completion claim needs filesystem proof
3. **Anti-80% Enforcement**: Must achieve 100% completion, not "good enough"
4. **Cross-Validation**: Deploy both Code and Cursor for independent verification
5. **Stop on Confusion**: Escalate to PM/Architect when unclear
6. **Time Lord Discipline**: Work takes what it takes for quality

## Infrastructure Context
```
main.py: 141 lines (microservice entry)
web/app.py: 467 lines (refactored in 3A from 1,052)
services/integrations/[service]/: Router + Config + Adapter pattern
services/plugins/: New plugin foundation (3A)
Tests: 72/72 passing
```

## Agent Coordination Best Practices
**Code Agent**: Broad investigation, pattern discovery, implementation
**Cursor Agent**: Focused verification, cross-validation, testing
**Both**: GitHub evidence updates, systematic documentation

**Prompt Quality**: Use templates, include success criteria, specify evidence format
**Validation**: Independent verification prevents completion bias
**Documentation**: Real-time GitHub issue updates with proof

## References
- **Current state**: BRIEFING-CURRENT-STATE
- **Full role guide**: BRIEFING-ESSENTIAL-LEAD-DEV (if exists)
- **Active issues**: GitHub #183, #205, #206, #207, #208
- **Architecture**: docs/NAVIGATION.md
- **Templates**: in project knowledge
---

*Last Updated: October 5, 2025*
