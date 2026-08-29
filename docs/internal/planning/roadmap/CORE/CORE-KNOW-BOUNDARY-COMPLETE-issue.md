# CORE-KNOW-BOUNDARY-COMPLETE: Complete BoundaryEnforcer Integration

**Labels**: `technical-debt`, `security`, `ethics`, `alpha`
**Milestone**: Alpha
**Estimate**: 2-3 hours
**Priority**: High (Security/Ethics critical)

---

## Context

Sprint A3 activated the ethics layer and boundary enforcement, but 5 TODOs remain in the knowledge graph service where BoundaryEnforcer integration is incomplete. This means knowledge graph queries may bypass ethics checks.

## Current State

```python
# services/knowledge/knowledge_graph_service.py

# Lines with TODOs:
# Line 423: TODO: Apply boundary filtering to results
# Line 456: TODO: Check boundaries before returning
# Line 489: TODO: Enforce user context boundaries
# Line 512: TODO: Apply ethical boundaries to graph traversal
# Line 567: TODO: Boundary validation for sensitive nodes
```

The BoundaryEnforcer exists and works, but isn't wired into all knowledge operations.

## Scope

### 1. Complete Integration Points

```python
class KnowledgeGraphService:
    def __init__(self, boundary_enforcer: BoundaryEnforcer):
        self.boundary_enforcer = boundary_enforcer  # Already exists

    async def query_graph(self, query: str, user_context: UserContext):
        # Line 423 - Apply boundary filtering
        results = await self._execute_query(query)
        filtered_results = await self.boundary_enforcer.filter_results(
            results,
            user_context
        )
        return filtered_results

    async def get_node(self, node_id: str, user_context: UserContext):
        # Line 456 - Check boundaries before returning
        node = await self._fetch_node(node_id)
        if not await self.boundary_enforcer.can_access(node, user_context):
            raise BoundaryViolationError(f"Access denied to node {node_id}")
        return node

    async def traverse_graph(self, start_node: str, depth: int, user_context: UserContext):
        # Line 512 - Apply ethical boundaries to traversal
        traversal_filter = await self.boundary_enforcer.get_traversal_filter(
            user_context
        )
        return await self._traverse_with_filter(start_node, depth, traversal_filter)
```

### 2. Add Boundary Tests

```python
# tests/knowledge/test_boundary_integration.py

async def test_knowledge_graph_respects_boundaries():
    """Verify all knowledge operations enforce boundaries"""

    # Create restricted context
    restricted_user = UserContext(
        user_id="test_user",
        access_level="limited"
    )

    # Attempt to access restricted knowledge
    with pytest.raises(BoundaryViolationError):
        await kg_service.get_node("restricted_node", restricted_user)

    # Verify filtered results
    results = await kg_service.query_graph("all nodes", restricted_user)
    assert "restricted_content" not in results
```

### 3. Add Boundary Metrics

```python
class BoundaryMetrics:
    """Track boundary enforcement in knowledge operations"""

    async def log_boundary_check(self, operation: str, allowed: bool):
        # Track what's being filtered
        # Identify patterns in violations
        # Monitor performance impact
```

## Acceptance Criteria

- [ ] All 5 TODOs in knowledge_graph_service.py resolved
- [ ] BoundaryEnforcer integrated at all query points
- [ ] Tests verify boundary enforcement works
- [ ] No performance degradation (benchmark before/after)
- [ ] Metrics show boundaries being applied
- [ ] Documentation updated

## Why This Matters for Alpha

Without complete boundary enforcement:
- Users might access knowledge they shouldn't
- Ethical guidelines could be bypassed
- Privacy boundaries might leak
- Multi-user isolation could fail

This is a security/ethics critical fix before real users.

## Implementation Notes

1. BoundaryEnforcer already exists from Sprint A3
2. Just need to wire it into the 5 locations
3. Add comprehensive tests
4. Verify no performance impact

## Testing Checklist

- [ ] Unit tests for each integration point
- [ ] Integration tests for full query paths
- [ ] Performance benchmarks (should be <10ms overhead)
- [ ] Multi-user isolation tests
- [ ] Ethical boundary tests

---

**Created**: October 22, 2025
**Author**: Chief Architect
