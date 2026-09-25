# Gameplan: UX-105 Phase 0 - DDD Design & Architecture

**Later disposition (2026-09-24, #1775/#1883)**: this plan's `StandupToChatBridge`/
`standup_bridge.py` was built, but never instantiated or called in production — deleted
2026-09-24 as unreachable dead code. Kept below as the historical planning record, not as a
description of live code.

## Context
- **Issue**: UX-105 Response Personality Enhancement
- **Phase**: 0 - Design & Architecture
- **Prerequisites**: Extended Phase -1 investigation complete
- **Foundation**: DDD Model created, documentation requirements defined

## Critical Process Requirement
**GitHub Issue Updates**: Update UX-105 at EACH checkpoint with design decisions

## Phase 0: Design & Architecture Completion

### Part A: Technical Architecture Decisions

#### 1. Configuration Strategy
- [ ] Determine where personality preferences live:
  - Option A: Extend PIPER.user.md structure
  - Option B: New personality_config.py module
  - Option C: Database table with defaults
- [ ] Define default PersonalityProfile values
- [ ] Design user preference override mechanism

#### 2. Performance Implementation
- [ ] Design caching strategy for PersonalityProfiles
- [ ] Define performance monitoring points
- [ ] Create degradation strategy if >100ms
- [ ] Plan concurrent request handling

#### 3. Integration Architecture
Based on DDD model, define precise integration:
- [ ] Template interception point (before/after ActionHumanizer?)
- [ ] Standup bridge implementation approach
- [ ] Error response enhancement strategy
- [ ] Confidence threshold handling (< 0.3, 0.3-0.7, > 0.8)

**Checkpoint A**: Technical decisions documented
- [ ] Update UX-105 with architecture choices
- [ ] Get PM approval before Part B

### Part B: Implementation Blueprint

#### 1. Module Structure
```python
services/personality/
├── __init__.py
├── response_enhancer.py      # Main aggregate
├── personality_profile.py    # Domain models
├── transformations.py         # Enhancement logic
├── standup_bridge.py         # Standup integration
└── cache.py                  # Profile caching
```

#### 2. Database Schema (if needed)
- [ ] Design PersonalityProfile table (if persisted)
- [ ] Migration script approach
- [ ] Default data strategy

#### 3. Testing Framework
- [ ] Unit test structure for transformations
- [ ] Integration test approach
- [ ] A/B testing framework design (if Phase 1)
- [ ] Performance benchmark setup

#### 4. Documentation Updates
From DDD model requirements:
- [ ] List all docs to create (4 new)
- [ ] List all docs to update (7+ existing)
- [ ] Assign to Code/Cursor agents

**Checkpoint B**: Implementation blueprint complete
- [ ] Update UX-105 with full technical design
- [ ] Get PM go-ahead for Phase 1

### Part C: Workflow & Orchestration

#### 1. Response Flow Design
```
Current: Intent → Templates → ActionHumanizer → Output
Target:  Intent → Templates → PersonalityEnhancer → ActionHumanizer → Output
                                     ↑
                            UserPreferences + Context
```

#### 2. Standup Bridge Design
- [ ] How standup formatting gets personality
- [ ] Unified experience strategy
- [ ] Migration path for existing standup

#### 3. Error Handling
- [ ] Enhancement failure strategy
- [ ] Logging and monitoring approach
- [ ] Graceful degradation design

**Checkpoint C**: Workflow documented
- [ ] Update UX-105 with complete flow
- [ ] PM validation of approach

## Phase 0 Deliverables

### Required Outputs
1. **Technical Architecture Document**
   - Configuration approach
   - Performance strategy
   - Integration points

2. **Implementation Blueprint**
   - Module structure
   - Database changes (if any)
   - Testing approach

3. **Documentation Plan**
   - Critical updates list
   - Assignment strategy

4. **Risk Assessment**
   - Performance risks
   - Integration risks
   - Migration risks

### Success Criteria
- [ ] All architectural decisions documented
- [ ] Implementation path clear and validated
- [ ] Documentation requirements assigned
- [ ] No blocking questions remain
- [ ] PM approves moving to Phase 1

## Design Principles (from DDD Model)

### Core Principles
1. **Extend, don't replace** - Leverage ActionHumanizer and TemplateRenderer
2. **Cross-cutting concern** - Works across ALL interfaces
3. **Bridge the gap** - Unify standup with core response flow
4. **Performance budget** - <100ms overhead is non-negotiable
5. **Graceful degradation** - Failures don't break responses

### Anti-patterns to Avoid
- ❌ Building parallel response pipeline
- ❌ Standup-specific personality implementation
- ❌ Over-casualization losing professionalism
- ❌ Hidden complexity in transformations
- ❌ Inconsistent personality across interfaces

## Notes from Investigation

### Key Findings to Leverage
- Intent confidence already exists (0.0-1.0)
- Templates ready for enhancement (15+ defined)
- ActionHumanizer proven and operational
- 4,240+ tests provide safety net
- Standup correctly identified as variant

### Critical Decisions Made
- ResponsePersonalityEnhancer as aggregate root
- Transformation order: Warmth → Confidence → Actions
- StandupToChatBridge for unification
- Anti-corruption layer for template safety

## Next: Phase 1 Implementation
Once Phase 0 complete with PM approval:
- Build core PersonalityEnhancer
- Implement transformations
- Integrate with pipeline
- Bridge standup formatting
