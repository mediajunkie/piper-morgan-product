# Documentation Index

## Document Hierarchy

| Level | Purpose | Token Size | When to Load |
|-------|---------|------------|--------------|
| Essential | Role-specific start | 2-2.5K | Always first |
| Current State | Live status | 3K | As needed |
| Full Briefing | Complete context | 10-15K | For deep work |
| Templates | Work artifacts | Variable | Task-specific |

## Essential Briefings

### Role-Specific Entry Points
- **[Lead Developer](../../briefing/BRIEFING-ESSENTIAL-LEAD-DEV.md)** - Agent coordination, quality enforcement, systematic evidence
- **[Chief Architect](../../briefing/BRIEFING-ESSENTIAL-ARCHITECT.md)** - Pattern governance, architectural decisions, design evolution
- **[Chief of Staff](../../briefing/BRIEFING-ESSENTIAL-CHIEF-STAFF.md)** - Strategic coordination, progress tracking, team communication
- **[Communications](../../briefing/BRIEFING-ESSENTIAL-COMMS.md)** - Achievement narratives, methodology storytelling, weekly updates
- **[Coding Agent](../../briefing/BRIEFING-ESSENTIAL-AGENT.md)** - Implementation tasks, pattern compliance, evidence verification

### Current State References
- **[Current State](../../briefing/BRIEFING-CURRENT-STATE.md)** - Live project status and inchworm position

## Progressive Loading System

Each essential briefing includes references to load additional context only when needed:

### Methodology Details
- Request "Loading methodology details" → **BRIEFING-METHODOLOGY**
- Templates → **knowledge/gameplan-template**, **agent-prompt-template**

### Architecture Context
- Request "Loading architecture details" → **ADR-038** (spatial patterns), **ADR-034** (plugins)
- Patterns → **docs/internal/architecture/current/patterns/**

### Current Work
- Request "Loading current work" → **GitHub issues #197-200**
- Session logs → **docs/omnibus-logs/** (weekly synthesis)

## Token Usage Optimization

**Before Essential Briefings**: 21% token usage (39K tokens)
**After Essential Briefings**: ~5% token usage (2-2.5K tokens)
**Reduction**: 60% improvement in briefing efficiency

## Navigation

- **[Full Navigation](NAVIGATION.md)** - Complete internal documentation hub
- **[README](README.md)** - Public project information and user documentation
