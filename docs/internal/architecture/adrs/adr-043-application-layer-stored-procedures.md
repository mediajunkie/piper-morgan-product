# ADR-043: Application-Layer Stored Procedures Pattern

**Date**: November 22, 2025
**Status**: Accepted
**Deciders**: Chief Architect, Lead Developer
**Classification**: Architectural (Core Pattern)
**Issue**: #332 (DOCUMENTATION-STORED-PROCS)

---

## Context

The question "Are there stored procedures in use?" requires clarification because Piper Morgan implements a "stored procedures" pattern, but at the application layer rather than the database layer.

### Background

Traditionally, stored procedures live in the database (SQL, PL/pgSQL) to encapsulate multi-step business logic. This approach has trade-offs:

**Database-layer Stored Procedures:**
- ✅ Reduced network round-trips
- ✅ Logic co-located with data
- ❌ Tight coupling to PostgreSQL
- ❌ Hard to version control
- ❌ Require migrations for changes
- ❌ Limited debugging capabilities

### Piper Morgan's Implementation

Piper Morgan implements the stored procedure concept in the **application layer** using async Python, routing through the OrchestrationEngine. This decouples multi-step workflows from the database, while maintaining the core benefit: composable, reusable, versioned business logic.

### Discovery Context

During #356 (PERF-INDEX) and #532 (PERF-CONVERSATION-ANALYTICS) work, complex multi-step procedures were needed to:
1. Analyze incoming intents
2. Extract requirements
3. Identify dependencies
4. Generate documentation
5. Execute external actions

These procedures are composed, executed, and tested entirely in Python—making them version-controlled, testable, and database-agnostic.

---

## Decision

Piper Morgan uses **application-layer stored procedures** through orchestrated Python workflows rather than database-layer SQL procedures.

### Core Pattern

```
Intent → WorkflowFactory → Workflow (sequence of tasks) → OrchestrationEngine → Result
```

### Three Key Components

#### 1. **OrchestrationEngine** (services/orchestration/engine.py)

Executes workflows as composable, multi-step procedures:

```python
class OrchestrationEngine:
    async def execute_workflow(self, workflow: Workflow) -> WorkflowResult:
        """Execute a complete workflow with task dependencies and error recovery"""
        for task in workflow.tasks:
            task_result = await self._execute_task(task, workflow)

            # Critical task failure stops execution
            if task_result.failed and task.critical:
                return WorkflowResult(status=FAILED, error=...)

        return WorkflowResult(status=COMPLETED, ...)
```

**Key Methods:**
- `execute_workflow()` - Multi-step orchestrated execution
- `create_workflow_from_intent()` - Intent → Workflow translation
- `_execute_task()` - Individual task execution
- `handle_query_intent()` - Query-specific orchestration

**Pattern:**
- Tasks execute in dependency order
- Critical tasks abort workflow if they fail
- Non-critical tasks allow workflow continuation
- Each task receives workflow context for dependency resolution

---

#### 2. **WorkflowFactory** (services/orchestration/workflow_factory.py)

Defines and instantiates workflows from intents:

```python
class WorkflowFactory:
    def __init__(self):
        self.workflow_registry = {
            "create_github_issue": WorkflowType.CREATE_TICKET,
            "analyze_data": WorkflowType.ANALYZE_FILE,
            "generate_report": WorkflowType.GENERATE_REPORT,
            # ... mappings for each intent type
        }

        self.validation_registry = {
            WorkflowType.CREATE_TICKET: {
                "context_requirements": {
                    "critical": ["original_message"],
                    "important": ["project_id"],
                    "optional": ["labels", "priority"],
                },
                "performance_threshold_ms": 50,
                "pre_execution_checks": ["project_resolution"],
            },
            # ... validation rules per workflow
        }

    async def create_from_intent(self, intent: Intent) -> Workflow:
        """Create a workflow from an intent"""
        # Validate context before execution
        self._validate_workflow_context(intent)

        # Return appropriate workflow type
        workflow_type = self.workflow_registry[intent.type]
        return Workflow(type=workflow_type, tasks=[...])
```

**Key Capabilities:**
- Registry maps intents to workflows
- Validation registry defines context requirements
- Pre-execution checks prevent invalid workflow starts
- Performance thresholds track execution time

**Pattern:**
- Fail early: validation before execution
- Context-aware: each workflow knows its requirements
- Discoverable: registry shows all available workflows

---

#### 3. **IntentService** (services/intent/intent_service.py)

Routes intents to appropriate handlers, each implementing multi-step procedures:

```python
class IntentService:
    async def process_intent(self, intent: Intent) -> IntentProcessingResult:
        """Route intent to appropriate handler"""

        # Intent → Handler dispatch
        if intent.category == IntentCategory.QUERY:
            return await self._handle_query_intent(intent)
        elif intent.category == IntentCategory.EXECUTION:
            return await self._handle_execution_intent(intent)
        elif intent.category == IntentCategory.ANALYSIS:
            return await self._handle_analysis_intent(intent)
        # ... 25+ intent types with dedicated handlers

    async def _handle_execution_intent(self, intent: Intent) -> IntentProcessingResult:
        """Multi-step procedure: validate → prepare → execute"""

        # Step 1: Validate
        validation = await self._validate_execution(intent)
        if not validation.valid:
            return IntentProcessingResult(status=FAILED, error=...)

        # Step 2: Prepare
        workflow = await self.factory.create_from_intent(intent)

        # Step 3: Execute through OrchestrationEngine
        result = await self.orchestration_engine.execute_workflow(workflow)

        return IntentProcessingResult(status=SUCCEEDED, data=result)
```

**Key Methods:**
- 65+ handler methods for different intent types
- Each handler implements a multi-step procedure
- Handlers use OrchestrationEngine for complex workflows
- Pattern: validate → prepare → execute → return

**Handler Categories:**
- Query handlers: `_handle_query_intent()`, `_handle_standup_query()`
- Execution handlers: `_handle_execution_intent()`, `_handle_create_issue()`
- Analysis handlers: `_handle_analysis_intent()`, `_handle_analyze_data()`
- Strategy handlers: `_handle_strategic_planning()`, `_handle_prioritization()`
- Learning handlers: `_handle_learn_pattern()`, `_handle_learning_intent()`

---

## Comparison: Application vs Database Layer

| Aspect | Application Layer (Piper) | Database Layer (SQL) |
|--------|-------------------------|----------------------|
| **Technology** | Python async/await | SQL/PL/pgSQL |
| **Location** | services/orchestration/ | Database procedures |
| **Composability** | High (Python functions) | Medium (SQL procedures) |
| **Version Control** | Git commits | Database migrations |
| **Testing** | Unit tests in Python | Database/integration tests |
| **Debugging** | Python debugger tools | Database query logs |
| **Database Agnostic** | Yes (any DB backend) | No (DB-specific) |
| **Network Traffic** | More round-trips | Fewer round-trips |
| **Deployment** | Code deploy | Code + migration deploy |
| **Error Handling** | Python exceptions | SQL error codes |
| **Integration** | Tight with app logic | Separate layer |
| **Performance** | Depends on impl | Optimized by DB |

---

## Implementation Details

### Workflow Composition

A workflow is a sequence of typed tasks with dependencies:

```python
@dataclass
class Task:
    id: str
    type: TaskType  # ANALYZE_REQUEST, EXTRACT_REQUIREMENTS, etc.
    params: Dict[str, Any]
    critical: bool = False  # Stop workflow if fails

@dataclass
class Workflow:
    id: str
    type: WorkflowType
    status: WorkflowStatus
    tasks: List[Task]

# Example workflow for intent processing:
workflow = Workflow(
    type=WorkflowType.CREATE_TICKET,
    tasks=[
        Task(type=ANALYZE_REQUEST, params={"intent": intent}),
        Task(type=EXTRACT_REQUIREMENTS, params={"analyzed": ...}, critical=True),
        Task(type=IDENTIFY_DEPENDENCIES, params={"requirements": ...}),
        Task(type=EXECUTE_GITHUB_ACTION, params={"dependencies": ...}),
    ]
)
```

### Execution Model

```
1. Intent received
   ↓
2. WorkflowFactory.create_from_intent() → Workflow
   ├─ Validate context requirements
   ├─ Check pre-execution conditions
   └─ Build task sequence
   ↓
3. OrchestrationEngine.execute_workflow()
   ├─ For each task in workflow.tasks:
   │  ├─ _execute_task()
   │  ├─ Track task status
   │  └─ If critical and failed → abort
   ├─ Track timing and metrics
   └─ Return WorkflowResult
   ↓
4. Return result to caller
```

### Error Handling Strategy

```python
# Critical task failure = workflow failure
if task.critical and task_result.failed:
    return WorkflowResult(
        status=FAILED,
        error=f"Critical task {task.id} failed"
    )

# Non-critical task failure = continue with next task
# (allows partial success in complex procedures)
```

---

## Consequences

### Positive ✅

1. **Database Agnostic**: Workflows run on any SQL database, no vendor lock-in
2. **Version Controlled**: All procedures tracked in git with code
3. **Testable in Isolation**: Unit test workflows without database
4. **Debuggable**: Use Python debuggers, not database query tools
5. **Composable**: Workflows build on other workflows easily
6. **Scalable**: Add new procedures without database changes
7. **Deployable**: Code changes deploy; no migrations required for new procedures
8. **Auditable**: Full procedure history in git commits
9. **Integrated**: Tight integration with application logic, caching, monitoring
10. **Async-Ready**: Non-blocking execution, parallelizable

### Negative ❌

1. **Network Overhead**: More round-trips to database than SQL procedures
2. **Development Complexity**: Developers learn application-layer patterns
3. **Testing Burden**: Must test all multi-step sequences
4. **Orchestration Overhead**: Small overhead vs direct execution (mitigated by ADR-019)
5. **Distributed Debugging**: Workflow state spread across application code
6. **Performance Analysis**: Harder to optimize without database query tools

### Trade-offs

**When to prefer application-layer procedures:**
- Multi-step processes that benefit from version control
- Workflows that might change frequently
- Procedures that involve external services (GitHub, Notion, MCP)
- Complex error handling and retry logic
- Testing and debugging are important
- Future portability to non-SQL databases

**When database procedures might be better:**
- Extremely latency-sensitive operations (rare for Piper)
- Complex set operations (bulk updates, aggregations)
- Minimal-footprint microservices
- PL/pgSQL expertise available

**Piper's Choice:** Application layer, because:
- Workflows change frequently (intent processing)
- Integration with external services is common
- Version control and testing are priorities
- Database portability is valuable
- Python ecosystem integration is important

---

## Related Decisions

**Supports:**
- ADR-019: Full Orchestration Commitment (everything goes through orchestration)
- ADR-032: Intent Classification as Universal Entry (intents route to handlers)
- ADR-029: Domain Service Mediation Architecture (services coordinate through intent handlers)

**Supports Implementation Of:**
- PM-002: Orchestration Foundation
- PM-033: Enhanced Autonomy (needs orchestration)
- #356: PERF-INDEX (requires multi-step index creation)
- #532: PERF-CONVERSATION-ANALYTICS (requires analytics workflow)

**Differs From:**
- Traditional SQL stored procedures approach
- Direct execution without orchestration
- Monolithic single-step operations

---

## References & Examples

### Code Locations

- **OrchestrationEngine**: `services/orchestration/engine.py:63-490`
- **WorkflowFactory**: `services/orchestration/workflow_factory.py:22-539`
- **IntentService**: `services/intent/intent_service.py:65-5184`
- **Workflow Models**: `services/domain/models.py` (Intent, Task, Workflow classes)
- **Status Enums**: `services/shared_types.py` (TaskStatus, WorkflowStatus, TaskType)

### Example: Query Intent Workflow

```python
# Input: User asks "Show me my projects"
intent = Intent(
    type="query",
    content="Show me my projects",
    category=IntentCategory.QUERY
)

# IntentService dispatch
result = await intent_service.process_intent(intent)
  → calls _handle_query_intent()

# Handler creates workflow
workflow = await workflow_factory.create_from_intent(intent)
  → type: WorkflowType.LIST_PROJECTS
  → tasks: [validate, fetch, format, return]

# Orchestration engine executes
result = await orchestration_engine.execute_workflow(workflow)
  → executes each task in order
  → returns list of projects
```

### Example: Issue Creation Workflow

```python
# Input: "Create a GitHub issue about performance"
intent = Intent(
    type="execution",
    content="Create GitHub issue about performance",
    category=IntentCategory.EXECUTION
)

# Multi-step workflow created by factory
workflow = Workflow(
    type=WorkflowType.CREATE_TICKET,
    tasks=[
        Task(ANALYZE_REQUEST, critical=True),      # Understand intent
        Task(EXTRACT_REQUIREMENTS, critical=True), # What's needed
        Task(IDENTIFY_DEPENDENCIES, critical=False), # Dependencies
        Task(EXECUTE_GITHUB_ACTION, critical=False), # Create issue
    ]
)

# Orchestration executes all steps
result = await engine.execute_workflow(workflow)
  → Returns GitHub issue creation result
  → If ANALYZE_REQUEST fails → abort (critical)
  → If IDENTIFY_DEPENDENCIES fails → continue (non-critical)
```

---

## Testing Strategy

### Unit Tests

Test individual handlers and workflow composition:

```python
async def test_create_from_intent():
    factory = WorkflowFactory()
    intent = Intent(type="create_github_issue", ...)

    workflow = await factory.create_from_intent(intent)

    assert workflow.type == WorkflowType.CREATE_TICKET
    assert len(workflow.tasks) > 0
    assert workflow.tasks[0].type == TaskType.ANALYZE_REQUEST
```

### Integration Tests

Test full workflow execution:

```python
async def test_execute_github_creation_workflow():
    engine = OrchestrationEngine()
    workflow = Workflow(
        type=WorkflowType.CREATE_TICKET,
        tasks=[...],
    )

    result = await engine.execute_workflow(workflow)

    assert result.status == WorkflowStatus.COMPLETED
    assert result.github_issue_created
```

### Load Tests

Verify workflow execution performance:

```python
# Each workflow type has performance_threshold_ms
CREATE_TICKET: 50ms
LIST_PROJECTS: 30ms
ANALYZE_FILE: 75ms
```

---

## Future Considerations

### Scaling

- Workflows can be parallelized (future enhancement)
- Async execution enables connection pooling
- Caching at workflow level (planned)

### Enhancement Opportunities

1. **Workflow Templates**: Pre-defined compositions for common patterns
2. **Conditional Execution**: Skip tasks based on results
3. **Parallel Tasks**: Execute independent tasks concurrently
4. **Retry Logic**: Automatic retry for transient failures
5. **Monitoring**: Per-workflow timing and error rates
6. **Workflow Versioning**: Multiple versions of same workflow type

### Potential Risks

- Performance regression if workflows get too complex
- Debugging difficulty if task interdependencies become complex
- Database connection pool exhaustion with many concurrent workflows

---

## Decision Rationale

**Question: "Are there stored procedures in use?"**

**Answer: Yes—at the application layer.**

Piper Morgan implements a stored procedures pattern through orchestrated Python workflows rather than database-layer SQL procedures. This decision enables:

1. **Flexibility** through version control
2. **Composability** through Python functions
3. **Testability** through unit testing
4. **Portability** through database agnosticism
5. **Integration** with intent-driven architecture
6. **Scalability** through async/await patterns

This is a deliberate architectural choice, not an accident or limitation.

---

## Approval & Sign-off

**Decision Made**: November 22, 2025
**Status**: Accepted
**Implementation**: Active (OrchestrationEngine, WorkflowFactory, IntentService)
**Documentation**: Issue #332 (DOCUMENTATION-STORED-PROCS)

---

🤖 Generated with [Claude Code](https://claude.com/claude-code)
