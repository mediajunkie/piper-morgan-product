# Pattern-011: Context Resolution Pattern

## Status

**Proven**

## Context

Applications often need to resolve implicit context (like current project, user session, or workspace) from multiple potential sources with conflicting information. Without clear precedence rules, context resolution becomes unpredictable and error-prone. The Context Resolution Pattern addresses:

- What challenges does this solve? Provides systematic hierarchy for resolving context from multiple sources
- When should this pattern be considered? When applications have implicit context that can come from different sources
- What are the typical scenarios where this applies? Project resolution, user context, session management, workspace determination

## Pattern Description

The Context Resolution Pattern resolves implicit context from multiple sources using clear precedence rules, ensuring predictable and consistent context determination across the application.

Core concept:
- Hierarchical resolution with explicit precedence rules
- Session memory for context continuity
- Fallback mechanisms for graceful degradation
- Confirmation requirements for inferred context

## Implementation

### Structure

```python
class ProjectContext:
    """Resolves project from various sources"""

    def __init__(self, repository: ProjectRepository, llm: LLMClient):
        self.repo = repository
        self.llm = llm
        self._session_memory: Dict[str, str] = {}

    async def resolve_project(
        self,
        intent: Intent,
        session_id: str,
        confirmed: bool = False
    ) -> Tuple[Project, bool]:
        """
        Resolution hierarchy:
        1. Explicit project_id (always wins)
        2. Session history (if confirmed)
        3. LLM inference from message
        4. Default project fallback
        """

        # 1. Explicit always wins
        if project_id := intent.context.get("project_id"):
            project = await self.repo.get_by_id(project_id)
            if not project:
                raise ProjectNotFoundError(project_id)
            return project, False

        # 2. Session history
        if session_id in self._session_memory and confirmed:
            project = await self.repo.get_by_id(self._session_memory[session_id])
            return project, False

        # 3. Inference
        inferred = await self._infer_from_message(intent)
        if inferred:
            self._session_memory[session_id] = inferred.id
            needs_confirm = session_id in self._session_memory and \
                           self._session_memory[session_id] != inferred.id
            return inferred, needs_confirm

        # 4. Default fallback
        default = await self.repo.get_default_project()
        if default:
            return default, True

        raise NoProjectAvailableError("No project context available")

    async def _infer_from_message(self, intent: Intent) -> Optional[Project]:
        """Use LLM to infer project from message content"""
        projects = await self.repo.list_active_projects()
        if not projects:
            return None

        project_context = "\n".join([f"- {p.name}: {p.description}" for p in projects])

        prompt = f"""
        Given this message: "{intent.message}"
        And these available projects:
        {project_context}

        Which project is this message most likely referring to? Return just the project name or 'none'.
        """

        response = await self.llm.complete(prompt)
        for project in projects:
            if project.name.lower() in response.lower():
                return project

        return None
```

### Generic Context Resolver

```python
class ContextResolver[T]:
    """Generic context resolution pattern"""

    def __init__(self, sources: List[ContextSource[T]]):
        self.sources = sorted(sources, key=lambda s: s.priority, reverse=True)

    async def resolve(self, context_data: Dict[str, Any]) -> T:
        """Resolve context using source priority hierarchy"""
        for source in self.sources:
            try:
                result = await source.resolve(context_data)
                if result:
                    return result
            except ContextResolutionError:
                continue  # Try next source

        raise ContextNotResolvableError("No source could resolve context")

class ExplicitContextSource(ContextSource[Project]):
    """Highest priority - explicit specification"""
    priority = 100

    async def resolve(self, context_data: Dict[str, Any]) -> Optional[Project]:
        project_id = context_data.get("project_id")
        if project_id:
            return await self.repository.get_by_id(project_id)
        return None

class SessionContextSource(ContextSource[Project]):
    """Medium priority - session memory"""
    priority = 50

    async def resolve(self, context_data: Dict[str, Any]) -> Optional[Project]:
        session_id = context_data.get("session_id")
        if session_id and context_data.get("confirmed"):
            return await self.get_session_project(session_id)
        return None
```

## Usage Guidelines

### Resolution Hierarchy Design
- **Explicit > Implicit**: Explicit specification always takes precedence
- **Confirmed > Inferred**: Confirmed context beats inference
- **Recent > Historical**: More recent context preferred over older
- **Fallback Required**: Always provide graceful fallback mechanisms

### Session Management
- Store context decisions in session memory
- Require confirmation for context changes
- Clear session context when explicitly changed
- Handle session expiration gracefully

### Error Handling
- Distinguish between "not found" and "not resolvable"
- Provide clear error messages about resolution failure
- Log resolution decisions for debugging
- Fail fast when no resolution possible

## Benefits

- Predictable context resolution across application
- Clear precedence rules eliminate ambiguity
- Session continuity for better user experience
- Graceful fallback prevents application failures
- Debuggable resolution process

## Trade-offs

- Additional complexity for simple use cases
- Potential performance overhead with multiple sources
- Need to maintain resolution hierarchy consistency
- Session state management overhead

## Anti-patterns to Avoid

- ❌ Implicit resolution without clear rules
- ❌ Context resolution scattered across codebase
- ❌ No fallback mechanisms
- ❌ Session context without confirmation

## Related Patterns

- [Pattern-002: Service Pattern](pattern-002-service.md) - Services often need context resolution
- [Pattern-013: Session Management Pattern](pattern-013-session-management.md) - Session management for context continuity
- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Factories may use context for object creation

## References

- **Implementation**: Context resolution in service layers
- **Usage Example**: Project context resolution, session management
- **Related Concepts**: Dependency injection, service location

## Migration Notes

*Consolidated from:*
- `pattern-catalog.md#11-context-resolution-pattern` - Complete implementation with resolution hierarchy
- Codebase analysis - Generic context resolution patterns and session management
