# Pattern-015: Internal Task Handler Pattern

## Status

**Proven**

## Context

Complex orchestration systems need to handle various task types without creating excessive indirection or separate handler classes. Traditional approaches create separate handler classes for each task type, leading to scattered logic, difficult debugging, and complex state management. The Internal Task Handler Pattern addresses:

- What challenges does this solve? Reduces complexity by handling orchestration tasks as internal engine methods rather than external handlers
- When should this pattern be considered? When building orchestration engines that need direct access to engine state and simplified architecture
- What are the typical scenarios where this applies? Workflow engines, task orchestration, command processing, multi-step operations

## Pattern Description

The Internal Task Handler Pattern handles orchestration tasks using internal engine methods rather than separate handler classes, ensuring direct access to engine state, reducing indirection, and simplifying the codebase.

Core concept:

- Task handlers as internal methods of the orchestration engine
- Single mapping dictionary for all task type handlers
- Direct access to engine state and dependencies
- Simplified architecture with fewer abstractions

## Implementation

### Orchestration Engine with Internal Handlers

```python
from typing import Dict, Callable, Any
from enum import Enum

class TaskType(Enum):
    FILE_ANALYSIS = "file_analysis"
    GITHUB_CREATE_ISSUE = "github_create_issue"
    WORKFLOW_EXECUTE = "workflow_execute"
    VALIDATION_CHECK = "validation_check"

class Task:
    def __init__(self, task_type: TaskType, data: Dict[str, Any]):
        self.type = task_type
        self.data = data

class OrchestrationEngine:
    """Main orchestration engine with internal task handlers"""

    def __init__(self, github_agent, file_service, validation_service):
        self.github_agent = github_agent
        self.file_service = file_service
        self.validation_service = validation_service

        # Internal handler mapping
        self.task_handlers: Dict[TaskType, Callable] = {
            TaskType.FILE_ANALYSIS: self._analyze_file,
            TaskType.GITHUB_CREATE_ISSUE: self._create_github_issue,
            TaskType.WORKFLOW_EXECUTE: self._execute_workflow,
            TaskType.VALIDATION_CHECK: self._validate_context,
        }

    async def handle_task(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Route task to appropriate internal handler"""
        handler = self.task_handlers.get(task.type)
        if not handler:
            raise NotImplementedError(f"No handler for task type: {task.type}")

        try:
            result = await handler(task, context)
            return {"status": "success", "result": result}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    async def _analyze_file(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle file analysis tasks"""
        file_path = task.data.get("file_path")
        analysis_type = task.data.get("analysis_type", "basic")

        if not file_path:
            raise ValueError("file_path required for file analysis")

        # Direct access to engine dependencies
        analysis_result = await self.file_service.analyze(
            file_path=file_path,
            analysis_type=analysis_type,
            project_context=context.get("project")
        )

        return {
            "file_path": file_path,
            "analysis": analysis_result,
            "timestamp": context.get("timestamp")
        }

    async def _create_github_issue(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle GitHub issue creation tasks"""
        repo = context.get("repository")
        title = task.data.get("title")
        body = task.data.get("body")
        labels = task.data.get("labels", [])

        if not all([repo, title, body]):
            raise ValueError("repository, title, and body required for issue creation")

        # Direct access to GitHub agent
        issue_result = await self.github_agent.create_issue(
            repository=repo,
            title=title,
            body=body,
            labels=labels
        )

        return {
            "issue_url": issue_result.get("html_url"),
            "issue_number": issue_result.get("number"),
            "repository": repo
        }

    async def _execute_workflow(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle workflow execution tasks"""
        workflow_id = task.data.get("workflow_id")
        parameters = task.data.get("parameters", {})

        if not workflow_id:
            raise ValueError("workflow_id required for workflow execution")

        # Direct access to engine state for workflow coordination
        execution_context = {
            **context,
            "engine_state": self._get_current_state(),
            "parameters": parameters
        }

        workflow_result = await self._execute_workflow_steps(
            workflow_id, execution_context
        )

        return {
            "workflow_id": workflow_id,
            "execution_result": workflow_result,
            "final_state": self._get_current_state()
        }

    async def _validate_context(self, task: Task, context: Dict[str, Any]) -> Dict[str, Any]:
        """Handle context validation tasks"""
        validation_rules = task.data.get("rules", [])

        validation_results = []
        for rule in validation_rules:
            result = await self.validation_service.validate_rule(rule, context)
            validation_results.append({
                "rule": rule,
                "valid": result.is_valid,
                "details": result.details
            })

        return {
            "validation_results": validation_results,
            "all_valid": all(r["valid"] for r in validation_results)
        }

    def _get_current_state(self) -> Dict[str, Any]:
        """Get current engine state for context"""
        return {
            "active_tasks": len(self.task_handlers),
            "github_connected": self.github_agent.is_connected,
            "timestamp": datetime.utcnow().isoformat()
        }

    async def _execute_workflow_steps(self, workflow_id: str, context: Dict[str, Any]):
        """Internal workflow execution logic"""
        # Implementation for executing workflow steps
        pass
```

### Task Registration and Management

```python
class TaskRegistry:
    """Registry for managing task types and their handlers"""

    def __init__(self, engine: OrchestrationEngine):
        self.engine = engine

    def register_handler(self, task_type: TaskType, handler_method_name: str):
        """Register a new handler method on the engine"""
        if not hasattr(self.engine, handler_method_name):
            raise ValueError(f"Handler method {handler_method_name} not found on engine")

        handler_method = getattr(self.engine, handler_method_name)
        self.engine.task_handlers[task_type] = handler_method

    def get_supported_tasks(self) -> List[TaskType]:
        """Get list of supported task types"""
        return list(self.engine.task_handlers.keys())

    def validate_task(self, task: Task) -> bool:
        """Validate if task type is supported"""
        return task.type in self.engine.task_handlers

# Usage example
engine = OrchestrationEngine(github_agent, file_service, validation_service)
registry = TaskRegistry(engine)

# Task execution
task = Task(
    task_type=TaskType.GITHUB_CREATE_ISSUE,
    data={
        "title": "New Feature Request",
        "body": "Detailed description...",
        "labels": ["enhancement"]
    }
)

context = {
    "repository": "owner/repo",
    "project": project_instance,
    "timestamp": datetime.utcnow().isoformat()
}

result = await engine.handle_task(task, context)
```

## Usage Guidelines

### Handler Method Design

- Keep handlers as private methods (prefix with `_`)
- Use descriptive method names that clearly indicate purpose
- Accept task and context parameters consistently
- Return structured dictionaries with clear result format
- Handle validation and error cases within each handler

### State Management

- Leverage direct access to engine dependencies
- Use engine state for coordination between handlers
- Keep handler logic close to orchestration context
- Avoid external state dependencies where possible

### Error Handling

- Validate required parameters at handler start
- Use specific exceptions for different failure modes
- Return consistent error format from main handler
- Log errors appropriately for debugging

## Benefits

- Simpler architecture with fewer files to maintain
- Direct access to orchestration state and dependencies
- Easier to trace, debug, and extend task handling logic
- Reduces indirection and cognitive overhead
- Better encapsulation of orchestration logic

## Trade-offs

- Larger engine class with more responsibilities
- Potential for methods to become complex
- Less flexibility for external handler implementations
- Need to maintain internal handler registry

## Anti-patterns to Avoid

- ❌ Creating separate handler class for each task type
- ❌ Scattering handler logic across multiple modules
- ❌ Indirect state access via external handler classes
- ❌ Registering handlers dynamically in multiple places
- ❌ Breaking handler consistency with different signatures

## Related Patterns

- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Factory for creating task instances
- [Pattern-002: Service Pattern](pattern-002-service.md) - Services used by internal handlers
- [Pattern-004: CQRS-lite Pattern](pattern-004-cqrs-lite.md) - Command handling integration

## References

- **Implementation**: Orchestration engine with internal task routing
- **Usage Example**: GitHub integration, file analysis, workflow execution
- **Related Concepts**: Command pattern, orchestration architecture

## Migration Notes

_Consolidated from:_

- `pattern-catalog.md#15-internal-task-handler-pattern` - Complete orchestration engine implementation with internal handlers
- Codebase analysis - Orchestration patterns and task management systems
