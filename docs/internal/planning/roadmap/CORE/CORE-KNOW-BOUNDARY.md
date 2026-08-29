# CORE-KNOW-BOUNDARY: Implement Knowledge Graph Boundary Enforcement (#230)

## Context
Knowledge graph operations need boundary checking to prevent infinite traversal, resource exhaustion, and ensure predictable performance. Currently marked as TODO in knowledge services.

## Current State
```python
# services/knowledge/knowledge_service.py
# TODO: Implement boundary checking for graph traversal
# TODO: Add depth limits for recursive operations
```

## Scope

### 1. Traversal Boundaries
```python
class TraversalBoundaries:
    max_depth: int = 5           # Maximum traversal depth
    max_nodes: int = 1000         # Maximum nodes to visit
    max_time_ms: int = 5000       # Maximum execution time
    max_memory_mb: int = 100      # Maximum memory usage
```

### 2. Boundary Enforcement
```python
class BoundaryEnforcer:
    async def check_depth(self, current_depth: int) -> bool:
        """Check if depth limit exceeded"""

    async def check_node_count(self, visited: int) -> bool:
        """Check if node limit exceeded"""

    async def check_timeout(self, start_time: float) -> bool:
        """Check if time limit exceeded"""

    async def check_memory(self) -> bool:
        """Check if memory limit exceeded"""

    async def enforce_boundaries(self, operation: GraphOperation):
        """Enforce all boundaries during operation"""
```

### 3. Graceful Degradation
- Return partial results when limits hit
- Include boundary metadata in response
- Log boundary violations for monitoring
- Suggest query refinement when limits hit

### 4. Configurable Limits
```yaml
# config/knowledge.yaml
boundaries:
  default:
    max_depth: 5
    max_nodes: 1000
    max_time_ms: 5000

  search:
    max_depth: 3
    max_nodes: 500
    max_time_ms: 2000

  analysis:
    max_depth: 10
    max_nodes: 5000
    max_time_ms: 10000
```

### 5. Operation Types
- **Search**: Find specific nodes/relationships
- **Traversal**: Follow paths through graph
- **Analysis**: Complex graph algorithms
- **Export**: Bulk data extraction

## Acceptance Criteria
- [ ] Boundary limits enforced for all operations
- [ ] Partial results returned when limits hit
- [ ] Performance stays within boundaries
- [ ] Configuration per operation type
- [ ] Monitoring/logging of violations
- [ ] User feedback when limits hit
- [ ] Tests for each boundary type
- [ ] No resource exhaustion possible

## Implementation Details

### Depth Tracking
```python
async def traverse_with_depth(node: Node, depth: int = 0):
    if depth >= self.boundaries.max_depth:
        return PartialResult(
            data=collected_data,
            truncated=True,
            reason="max_depth_reached"
        )
```

### Node Count Tracking
```python
class NodeCounter:
    def __init__(self, max_nodes: int):
        self.visited = set()
        self.max_nodes = max_nodes

    def visit(self, node_id: str) -> bool:
        if len(self.visited) >= self.max_nodes:
            return False
        self.visited.add(node_id)
        return True
```

### Timeout Management
```python
async def with_timeout(operation: Callable, timeout_ms: int):
    return await asyncio.wait_for(
        operation(),
        timeout=timeout_ms / 1000
    )
```

## Performance Requirements
- Boundary checks: <1ms overhead
- Memory tracking: <5% overhead
- Partial result assembly: <10ms
- Configuration loading: Cached

## User Experience
When limits hit, return:
```json
{
  "results": [...],  // Partial results
  "metadata": {
    "complete": false,
    "truncated_reason": "max_depth_reached",
    "nodes_visited": 1000,
    "depth_reached": 5,
    "suggestion": "Refine query to be more specific"
  }
}
```

## Testing Strategy
1. Test each boundary independently
2. Test combined boundaries
3. Test graceful degradation
4. Test performance overhead
5. Test configuration loading

## Time Estimate
1 day

## Priority
Medium - Needed before production but not blocking Alpha

## Dependencies
- CORE-KNOW #99 (basic connection must work first)
- Knowledge graph must be operational

## Notes
- Consider adaptive boundaries based on system load
- Future: User-specific quotas for resource usage
- Monitor which boundaries are hit most frequently
