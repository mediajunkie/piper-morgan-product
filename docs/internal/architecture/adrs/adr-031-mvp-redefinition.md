# ADR-031: MVP Redefinition - Core vs Feature Distinction

## Status
Accepted

## Context
The retrospective analysis of September 14, 2025 revealed that our original May 27-29 vision for Piper Morgan was 95% unrealized. Rather than viewing this as failure, we recognize this as architectural readiness waiting for the right methodological moment. We need to redefine MVP to distinguish between core capabilities (what makes Piper unique) and features (what makes Piper useful).

## Decision
We will redefine MVP into two distinct phases:

### Core MVP (0.1 Alpha)
The minimum viable *intelligence* that demonstrates Piper's unique value:
- Conversational interface that actually works (even if limited)
- Learning that improves from each interaction (even if basic)
- Multi-agent coordination for development tasks (even if just 2 agents)

### Feature MVP (1.0 Release)
The minimum viable *product* that provides user value:
- Beautiful standup experience
- Intent recognition for core PM tasks
- Knowledge integration from multiple sources
- Notion synchronization for documentation

## Consequences

### Positive
- **Clear prioritization**: Core capabilities before features
- **Risk reduction**: Prove the hard parts (AI intelligence) before the familiar parts (PM features)
- **Vision alignment**: Returns focus to original conversational AI vision
- **Learning opportunity**: Every core interaction generates training data

### Negative
- **Delayed features**: Traditional PM features come later
- **User expectations**: Early adopters might expect more traditional functionality
- **Testing complexity**: Core capabilities harder to validate than features

### Neutral
- **Development approach**: Requires parallel work on core while maintaining features
- **Timeline impact**: 6-8 week integrated evolution approach chosen

## Implementation
1. **Immediate**: Fix blocking bugs (Bug #166)
2. **Week 1-2**: Implement intent classification (Pattern-028)
3. **Week 3-4**: Deploy multi-agent coordination (Pattern-029)
4. **Week 5-6**: Build plugin interface foundation (Pattern-030)
5. **Week 7-8**: Integrate and validate core MVP

## References
- Chief of Staff analysis: September 14, 2025
- Pattern-028: Intent Classification
- Pattern-029: Multi-Agent Coordination
- Issue #96: FEAT-INTENT implementation
