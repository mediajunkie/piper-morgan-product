# CORE-KNOW-ENHANCE: Optimize Knowledge Graph for Relationship-Based Reasoning

**Sprint**: A8
**Priority**: High
**Effort**: 2-3 hours
**Impact**: High (cost reduction, intelligence improvement)

---

## Problem

PM-040 Knowledge Graph is 95% complete but underutilized:
- Storing isolated facts instead of relationships
- Missing causal and temporal connections
- Not integrated with intent classification
- Using expensive models for simple retrieval

Current implementation treats the graph as a fact store:
```
(user, prefers, morning_standups)
(user, uses, notion)
```

Missing the reasoning potential of relationship chains.

---

## Solution - Phase 1 (Sprint A8)

Transform knowledge graph from fact storage to relationship-based reasoning engine with three focused improvements.

### 1. Enrich Edge Types (1 hour)

**Current**: 10 basic edge types (HAS, USES, OWNS, etc.)

**Add Causal Relationships**:
```python
class CausalEdgeTypes(Enum):
    BECAUSE = "because"          # user prefers X BECAUSE Y
    ENABLES = "enables"          # X ENABLES Y capability
    REQUIRES = "requires"        # X REQUIRES Y to function
    PREVENTS = "prevents"        # X PREVENTS Y from happening
    LEADS_TO = "leads_to"       # X LEADS_TO Y outcome
```

**Add Temporal Relationships**:
```python
class TemporalEdgeTypes(Enum):
    BEFORE = "before"
    DURING = "during"
    AFTER = "after"
    TRIGGERS = "triggers"
```

**Add Confidence Weights**:
```python
class WeightedEdge:
    def __init__(self, source, edge_type, target, confidence=1.0):
        self.confidence = confidence  # 0.0 to 1.0
        self.usage_count = 0          # Strengthen with use
        self.last_accessed = None     # For decay
```

### 2. Implement Graph-First Retrieval (1 hour)

**Pattern**: Query → Graph → Context → LLM (not Query → LLM)

```python
class GraphFirstRetrieval:
    async def get_context(self, user_query: str, user_id: str):
        """
        Use knowledge graph for initial context gathering
        before expensive LLM processing
        """
        # Step 1: Use Haiku for semantic search (90% cheaper)
        relevant_nodes = await self.graph.semantic_search(
            query=user_query,
            user_id=user_id,
            model='claude-3-haiku',  # Cheap model for retrieval
            max_nodes=10
        )

        # Step 2: Expand to related nodes (2-hop traversal)
        context_graph = await self.graph.expand(
            nodes=relevant_nodes,
            max_hops=2,
            edge_types=['BECAUSE', 'ENABLES', 'REQUIRES']
        )

        # Step 3: Extract reasoning chains
        reasoning_paths = self.extract_reasoning_chains(context_graph)

        # Step 4: Only NOW use expensive model with focused context
        return {
            'nodes': context_graph.nodes,
            'relationships': context_graph.edges,
            'reasoning': reasoning_paths,
            'tokens_saved': self.calculate_savings(context_graph)
        }
```

### 3. Connect to Intent Classification (30 min)

**The Missing 5%**: Wire knowledge graph into intent routing

```python
class KnowledgeAwareIntentClassifier:
    def __init__(self, knowledge_graph: KnowledgeGraphService):
        self.graph = knowledge_graph

    async def classify_with_context(self, user_input: str, user_id: str):
        """
        Enhance intent classification with knowledge graph context
        """
        # Get graph context FIRST
        graph_context = await self.graph.get_relevant_context(
            user_input,
            user_id
        )

        # Use context to improve classification
        if graph_context.has_pattern('morning_standup'):
            # User has standup preferences in graph
            intent_hints = ['standup', 'daily', 'status']

        # Classify with hints
        intent = await self.classify(
            user_input,
            context_hints=intent_hints
        )

        return intent, graph_context
```

---

## Implementation Details

### Storage Changes

**Before**:
```sql
-- Simple fact storage
INSERT INTO edges (source, type, target)
VALUES ('user_123', 'prefers', 'morning_standups');
```

**After**:
```sql
-- Relationship with reason and confidence
INSERT INTO edges (source, type, target, metadata)
VALUES (
    'user_123',
    'prefers',
    'morning_standups',
    jsonb_build_object(
        'because', 'highest_energy_time',
        'confidence', 0.9,
        'usage_count', 1,
        'discovered_at', now()
    )
);
```

### Query Examples

**Simple Fact Query** (current):
```
Q: "What does user prefer?"
A: "morning standups" (single fact)
```

**Reasoning Query** (enhanced):
```
Q: "Why should we schedule the architecture review?"
Graph traversal:
  user → prefers_mornings → BECAUSE → highest_energy
  architecture_review → REQUIRES → high_focus
  high_focus → ENABLED_BY → highest_energy
A: "Schedule for morning - your high energy time enables the focus needed for architecture work"
```

---

## Testing

```python
async def test_relationship_based_reasoning():
    """Test that graph provides reasoning chains not just facts"""

    # Create relationship chain
    graph.add_relationship(
        'user', 'prefers_mornings', 'BECAUSE', 'highest_energy'
    )
    graph.add_relationship(
        'highest_energy', 'ENABLES', 'complex_problem_solving'
    )

    # Query should return chain, not single fact
    result = await graph.query("When should I tackle hard problems?")

    assert 'morning' in result
    assert 'highest_energy' in result.reasoning
    assert len(result.reasoning_chain) >= 2
```

---

## Acceptance Criteria

- [ ] 15+ edge types including causal and temporal
- [ ] Confidence weights on all edges
- [ ] Graph-first retrieval pattern implemented
- [ ] Connected to intent classification
- [ ] Cost reduction demonstrated (>50% on retrieval)
- [ ] Reasoning chains extracted from traversal
- [ ] Tests for relationship-based queries

---

## Performance Targets

- Graph traversal: <50ms for 2-hop expansion
- Haiku retrieval: <200ms
- Total context gathering: <300ms
- Token reduction: >60% vs direct LLM query

---

## Risk Mitigation

- Keep existing fact-based queries working
- Add feature flag for graph-first retrieval
- Monitor latency closely
- Fallback to direct LLM if graph fails

---

## Success Metrics

- Cost per query reduced by 50%+
- Context relevance improved (measure via feedback)
- Response quality maintained or improved
- Alpha testers report better contextual understanding

---

**Created**: October 24, 2025
**Author**: Chief Architect
**Review**: Chief of Staff memo validated - small effort, big impact
