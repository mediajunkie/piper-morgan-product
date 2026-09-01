# How to Use the Multi-Agent Coordinator

> 🔴 **HISTORICAL — the whole subsystem this guide teaches is deleted (2026-09-01 banner, supersedes
> the 2026-05-15 one below).** `services/orchestration/` — including `multi_agent_coordinator.py`,
> which the prior banner claimed "survives" — was fully deleted 2026-07-18 (#1436, Tier-3 Family-2
> orchestration-island deletion, commit `addb61c99`; PM-033d thinking preserved as a design record).
> That claim is confirmed false as of this correction: `services/orchestration/` does not exist in
> the live tree. There is no live code this guide can be followed against. Confirmed via B3
> corpus-disposition (CIO, 2026-09-01): `docs/internal/architecture/reviews/2026-08-architectural-review/b3-methodology-disposition.md`.
> Guide content preserved below for historical reference only — do not write code against it.
>
> <details><summary>Prior (2026-05-15) staleness banner, superseded above</summary>
>
> Sections of this guide reference `services/orchestration/engine.py` and `OrchestrationEngine`,
> both deleted in #1094 (ENGINE-DELETION, γ-preserve). The
> `from services.orchestration.engine import OrchestrationEngine` import +
> `engine.create_workflow_from_intent(...)` + `engine.execute_workflow(...)` examples are no
> longer valid. EXECUTION-intent dispatch now flows through `intent_service.process_intent`
> direct dispatch via the `task_type` registry (Pattern-072, promoted to Proven via #1094). The
> `MultiAgentCoordinator` (`services/orchestration/multi_agent_coordinator.py`) survives. Use
> intent_service handler dispatch instead of engine workflow creation.
>
> </details>

**Purpose**: Practical guide for using the Multi-Agent Coordinator in development workflows
**Audience**: Developers implementing complex features (historical — subsystem deleted, see banner)
**Status**: 🔴 HISTORICAL — subsystem fully deleted 2026-07-18 (#1436); preserved for reference only

---

## Overview

The Multi-Agent Coordinator enables decomposing complex development tasks into parallelizable subtasks assigned to specialized agents (CODE for infrastructure/backend, CURSOR for testing/UI/documentation).

### When to Use Multi-Agent Coordination

Use multi-agent coordination when you have:
- **Complex features** requiring >120 minutes of work
- **Multiple domains** (backend, frontend, testing, docs)
- **Parallelizable work** that different agents can work on simultaneously
- **Clear separations** between concerns

### When NOT to Use

- Simple tasks <30 minutes
- Work that's inherently sequential
- Tasks that require constant context switching

---

## Basic Usage Pattern

### 1. Trigger Coordination

```python
from services.orchestration.multi_agent_coordinator import MultiAgentCoordinator, Intent

coordinator = MultiAgentCoordinator()

# Define the task you want to decompose
intent = Intent(
    id="unique_task_id",
    category="EXECUTION",
    action="build_user_preference_system",
    original_message="Build a complete user preference management system with API, tests, and documentation"
)

# Get coordination result
coordination_result = await coordinator.coordinate_task(intent, context={})
```

### 2. Review Decomposition

```python
# coordination_result contains:
# - coordination_result.subtasks: List of decomposed tasks
# - coordination_result.status: CoordinationStatus (COMPLETED, FAILED, etc.)

for subtask in coordination_result.subtasks:
    print(f"{subtask.title} ({subtask.estimated_duration_minutes}min)")
    print(f"  Assigned to: {subtask.assigned_agent}")
    print(f"  Description: {subtask.description}")
```

### 3. Execute Subtasks

```python
# Each subtask is now ready for execution
# CODE agent handles infrastructure/backend tasks
# CURSOR agent handles testing/UI/documentation tasks

for subtask in coordination_result.subtasks:
    agent_type = subtask.assigned_agent  # "CODE" or "CURSOR"

    if agent_type == "CODE":
        # Route to code agent
        await code_agent.execute(subtask)
    else:
        # Route to cursor/testing agent
        await cursor_agent.execute(subtask)
```

---

## Task Complexity Levels

The coordinator automatically assigns complexity based on task characteristics:

### SIMPLE (< 30 minutes)
- Single-domain work
- Clear requirements
- No external dependencies
- Minimal testing needed

**Example**: "Add a logging statement to main.py"

### MODERATE (30-120 minutes)
- Multi-step implementation
- Integration required
- Some testing needed
- Clear success criteria

**Example**: "Implement configuration validator with validation tests"

**Typical Decomposition**:
1. Architecture Design (16 min, CODE)
2. Core Implementation (26 min, CODE)
3. Integration & Polish (13 min, CURSOR)
4. Comprehensive Testing (9 min, CURSOR)

### COMPLEX (> 120 minutes)
- Multiple domains
- Significant testing
- Documentation required
- Integration with existing systems

**Example**: "Build multi-agent coordinator deployment system"

**Typical Decomposition**:
1. Architecture & Design (30 min, CODE)
2. Core Coordinator Implementation (40 min, CODE)
3. API Integration & Endpoints (35 min, CODE)
4. Comprehensive Testing (45 min, CURSOR)
5. Documentation & Examples (30 min, CURSOR)
6. Performance Validation (20 min, CODE)

---

## Agent Capabilities

### CODE Agent
**Best for**:
- Infrastructure and backend development
- Configuration and system design
- Core implementation
- API endpoint development
- Architecture decisions

**Characteristics**:
- Deep system understanding
- Can implement complex business logic
- Good at optimization
- Handles non-UI code

### CURSOR Agent
**Best for**:
- Testing and validation
- UI/frontend work (when applicable)
- Documentation creation
- Integration testing
- User-facing features

**Characteristics**:
- Excellent at test design
- Can validate integration points
- Creates clear documentation
- Validates user workflows

---

## Practical Examples

### Example 1: Simple Configuration Validator

**Task**: "Add a validator for checking service configurations"

**Decomposition**:
```
- Subtask 1: Design validation schema (10 min, CODE)
- Subtask 2: Implement validation logic (15 min, CODE)
```

**Process**:
1. CODE agent designs schema
2. CODE agent implements validator
3. Done (no separate testing phase for simple tasks)

### Example 2: Feature with Backend + Tests

**Task**: "Implement user preference API with comprehensive testing"

**Decomposition**:
```
- Subtask 1: Design API architecture (15 min, CODE)
- Subtask 2: Implement core API endpoints (30 min, CODE)
- Subtask 3: Integration testing (20 min, CURSOR)
- Subtask 4: Documentation (10 min, CURSOR)
```

**Process**:
1. CODE agent designs and implements API
2. While CODE is working, or after, CURSOR agent writes tests
3. CURSOR creates documentation
4. Both agents run tests and validate

### Example 3: Multi-Domain System

**Task**: "Build complete user preference management system"

**Decomposition**:
```
- Subtask 1: Architecture & domain modeling (25 min, CODE)
- Subtask 2: Core API implementation (35 min, CODE)
- Subtask 3: Database integration (25 min, CODE)
- Subtask 4: API testing & validation (30 min, CURSOR)
- Subtask 5: Integration testing (25 min, CURSOR)
- Subtask 6: Documentation & examples (20 min, CURSOR)
- Subtask 7: Performance validation (20 min, CODE)
```

**Process**:
1. CODE designs architecture (all agents benefit from this)
2. CODE builds core API (parallel)
3. CODE handles database integration (parallel)
4. CURSOR begins testing while CODE finishes implementation
5. CURSOR writes documentation (parallel with testing)
6. CODE validates performance (final step)

---

## Performance Expectations

The coordinator is designed for fast task decomposition:

- **Coordination latency**: <1000ms (P95)
- **Decomposition time**: <500ms for typical tasks
- **Overhead**: Minimal compared to task execution time

### Monitoring Performance

```python
# Get real-time metrics
metrics = await coordinator.get_performance_metrics()

print(f"Average coordination time: {metrics['average_latency_ms']}ms")
print(f"Success rate: {metrics['success_rate'] * 100}%")
print(f"Target met: {metrics['performance_target_met']}")
```

---

## Troubleshooting

### Decomposition Too Granular (Too Many Subtasks)

**Symptom**: Task decomposed into 8+ subtasks

**Cause**: Complex task interpretation

**Solution**:
1. Simplify task description
2. Break into smaller, focused tasks
3. Run coordination separately on each

### Decomposition Too Coarse (Too Few Subtasks)

**Symptom**: Task only has 1-2 subtasks

**Cause**: Simpler task than expected

**Solution**:
1. This is correct behavior
2. Don't force artificial decomposition
3. Simple tasks don't benefit from multi-agent

### Wrong Agent Assigned

**Symptom**: CODE task assigned to CURSOR or vice versa

**Cause**: Task characteristics not clearly specified

**Solution**:
1. Add more detail to task description
2. Specify required skills explicitly
3. Include context about complexity

---

## Integration with Workflow Engine

### Automatic Integration

The coordinator integrates with the existing workflow engine:

```python
from services.orchestration.engine import OrchestrationEngine

engine = OrchestrationEngine()

# Automatically detects complexity and uses multi-agent if needed
workflow = await engine.create_workflow_from_intent(intent, context)

# workflow.tasks contains the decomposed subtasks
# Each task has an assigned agent type
```

### Manual Integration

```python
# Get coordination result
result = await coordinator.coordinate_task(intent, context)

# Convert to workflow tasks
workflow = engine._create_workflow_from_coordination(intent, result)

# Execute workflow
await engine.execute_workflow(workflow)
```

---

## Best Practices

### 1. Clear Task Descriptions

**❌ Bad**: "Build the API"

**✅ Good**: "Build a REST API for user preferences with CRUD operations, validation, error handling, and comprehensive test coverage"

### 2. Realistic Complexity Assessment

- Don't overestimate simple tasks
- Don't underestimate complex ones
- Use actual time data from similar tasks

### 3. Coordinate at Task Boundaries

Decompose at natural boundaries:
- Architecture → Implementation → Testing → Documentation
- Backend → Frontend → Integration
- Core features → Secondary features

### 4. Don't Over-Decompose

Simple tasks don't benefit from decomposition:
- "Add logging" should stay as 1 task
- "Update README" should stay as 1 task
- Reserve multi-agent for truly complex work

### 5. Monitor and Learn

Track decomposition quality over time:
- Are estimated durations accurate?
- Are agent assignments appropriate?
- Are tasks completing on schedule?

---

## Performance Tips

### For Fast Decomposition

1. **Be specific**: Detailed descriptions decompose better
2. **Include context**: Mention related systems and constraints
3. **Clarify success**: Define what "done" looks like
4. **List dependencies**: Note what must happen first

### For Effective Execution

1. **Assign agents early**: Don't wait for full workflow
2. **Parallelize where possible**: CODE and CURSOR tasks can run in parallel
3. **Track progress**: Monitor subtask completion
4. **Validate integration points**: Test where subtasks meet

---

## Related Documentation

- **[MULTI_AGENT_INTEGRATION_GUIDE.md](MULTI_AGENT_INTEGRATION_GUIDE.md)** - Technical integration details
- **[MULTI_AGENT_QUICK_START.md](MULTI_AGENT_QUICK_START.md)** - 5-minute deployment guide
- **[methodology-02-AGENT-COORDINATION.md](methodology-02-AGENT-COORDINATION.md)** - Coordination methodology
- **Services Reference**: `services/orchestration/multi_agent_coordinator.py`

---

**Last Updated**: November 22, 2025
**Status**: ✅ Complete & Operational
**Tested**: With real development tasks
