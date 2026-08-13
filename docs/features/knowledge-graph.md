# Knowledge Graph - Piper Morgan's Memory System

## Overview

The Knowledge Graph is Piper Morgan's memory system, enabling context-aware conversations by storing and retrieving information about projects, people, documents, technologies, and their relationships.

**Status**: ✅ ACTIVATED (Issue #99, #230 complete)
**Activated**: October 18, 2025
**Sprint**: A3 "Some Assembly Required"

## What It Does

The Knowledge Graph enhances conversation context by:
- **Project Memory**: Remembers project details, status, phases, blockers
- **Pattern Recognition**: Identifies recent interaction patterns
- **Entity Tracking**: Links people, documents, technologies
- **Relationship Mapping**: Connects related concepts across sessions
- **Session Isolation**: Each session's data is private

## Architecture

### Components

1. **Database Layer** (`services/knowledge/knowledge_graph_repository.py`)
   - PostgreSQL storage
   - Tables: `knowledge_nodes`, `knowledge_edges`
   - Node types: CONCEPT, PERSON, DOCUMENT, TECHNOLOGY, ORGANIZATION
   - Edge types: RELATED_TO, DEPENDS_ON, SUPPORTS, REFERENCES

2. **Service Layer** (`services/knowledge/knowledge_graph_service.py`)
   - Node CRUD operations
   - Edge management
   - Graph traversal with boundaries
   - Search with session filtering

3. **Integration Layer** (`services/knowledge/conversation_integration.py`)
   - Context enhancement for conversations
   - Keyword extraction
   - Project/pattern/entity queries
   - Graceful degradation

4. **Boundary Enforcement** (`services/knowledge/boundaries.py`)
   - Depth limits (prevent infinite loops)
   - Node count limits (prevent memory exhaustion)
   - Timeout enforcement (prevent hung queries)
   - Operation-specific configurations

### Integration Points

**IntentService** (`services/intent/intent_service.py` lines 154-181):
- Checks `ENABLE_KNOWLEDGE_GRAPH` flag
- Calls `ConversationKnowledgeGraphIntegration.enhance_conversation_context()`
- Merges graph insights with base context
- Graceful degradation on failures

### Data Flow

```
User Message
    ↓
IntentService.process_intent()
    ↓
ConversationKnowledgeGraphIntegration.enhance_conversation_context()
    ↓
KnowledgeGraphService.search_nodes() [with boundaries]
    ↓
KnowledgeGraphRepository (PostgreSQL)
    ↓
Enhanced Context → Response Generation
```

## Configuration

### Environment Variables

```bash
# Feature Flag (default: true after Phase 3)
ENABLE_KNOWLEDGE_GRAPH=true

# Performance Tuning
KNOWLEDGE_GRAPH_TIMEOUT_MS=100      # Query timeout
KNOWLEDGE_GRAPH_CACHE_TTL=300       # Cache TTL (5 minutes)
```

**Location**: `.env` file (lines 48-51)

### Boundary Limits

Three operation types with different limits:

**SEARCH** (conversation context):
- Max Depth: 3
- Max Nodes: 500
- Timeout: 100ms
- Use: Real-time conversation enhancement

**TRAVERSAL** (user exploration):
- Max Depth: 5
- Max Nodes: 1000
- Timeout: 500ms
- Use: Interactive graph exploration

**ANALYSIS** (admin analytics):
- Max Depth: 10
- Max Nodes: 5000
- Timeout: 2000ms
- Use: Background analysis & reports

**Configuration**: `services/knowledge/boundaries.py` lines 47-65

## Usage Examples

### Canonical Query Enhancement

**Before Knowledge Graph**:
```
User: "What's the status of the website project?"
Response: "I need more information about which website project..."
```

**After Knowledge Graph**:
```
User: "What's the status of the website project?"
Context Enhanced With:
  - Project: pmorgan.tech Website Initial Launch (SITE-001)
  - Status: in_progress, 3 of 5 phases complete
  - Focus: technical foundation, design system
  - Blockers: ConvertKit integration, Medium RSS feeds
Response: [Contextual answer with specific details]
```

### Session Pattern Recognition

Knowledge Graph tracks interaction history:
- Recent discussions
- Technology stack mentions
- Document references
- Decision patterns

## Performance

### Measured Performance

**Context Enhancement**:
- Average: 2.3ms (97.7% under 100ms target)
- Cold cache: 37ms
- Warm cache: 3-5ms
- Cache improvement: 85-90%

**Resource Protection**:
- Depth limits prevent infinite loops
- Node limits prevent memory exhaustion
- Timeouts prevent hung queries
- All operations complete predictably

### Database Queries

- Single node: 0.4-0.6ms
- Search nodes: 3-5ms (cached)
- Traverse relationships: 10-50ms (depending on depth)

## Testing

**Test Coverage**: 15/15 tests passing (100%)

**Phase 2 Tests** (6/6):
- Integration tests
- Feature flag control
- Graceful degradation
- Performance validation

**Phase 3 Tests** (3/3):
- Canonical query enhancement
- Without KG comparison
- Session pattern recognition

**Phase 4 Tests** (6/6):
- Depth limit enforcement
- Node count enforcement
- Timeout enforcement
- Result size limits
- Operation boundaries
- Statistics tracking

## Deployment

### Database Setup

```bash
# Tables created in Phase 1
# Verify with:
docker exec -it piper-postgres psql -U piper -d piper_morgan -c "\dt knowledge*"
```

**Tables**:
- `knowledge_nodes` - Entities (projects, people, documents, etc.)
- `knowledge_edges` - Relationships between entities

**Indexes**:
- `idx_nodes_type` - Node type queries
- `idx_nodes_session` - Session filtering
- `idx_edges_source` - Source node lookups
- `idx_edges_target` - Target node lookups

### Activation

```bash
# Already activated in Phase 3
# Verify with:
echo $ENABLE_KNOWLEDGE_GRAPH  # Should be: true
```

### Rollback

If issues arise:
```bash
# Instant disable (< 1 minute)
export ENABLE_KNOWLEDGE_GRAPH=false

# Or update .env
echo "ENABLE_KNOWLEDGE_GRAPH=false" >> .env

# Restart service
# System continues normally without KG enhancement
```

## Troubleshooting

### Issue: No context enhancement

**Symptoms**: Responses don't include project/pattern details

**Check**:
1. `ENABLE_KNOWLEDGE_GRAPH=true` in .env?
2. Service restarted after config change?
3. Check logs for KG enhancement messages

**Solution**: Ensure flag set and service restarted

### Issue: Slow queries

**Symptoms**: Response lag, timeout warnings in logs

**Check**:
1. Database indexes created? (Phase 1)
2. Hitting boundary limits? (check logs)
3. Cache working? (warm queries should be faster)

**Solution**: Review boundary logs, tune limits if needed

### Issue: Feature flag not working

**Symptoms**: KG active when disabled or vice versa

**Check**:
1. IntentService reading env var correctly?
2. Test through IntentService layer (not direct integration)

**Solution**: Test with `test-knowledge-graph-integration.py`

### Issue: Partial results

**Symptoms**: Logs show "max nodes reached"

**Explanation**: Boundary limits hit (expected behavior)

**Action**:
- If too restrictive: Increase `max_nodes_visited` in boundaries.py
- If acceptable: No action needed (graceful degradation working)

## Monitoring

### What to Monitor

- **KG enhancement errors** (should be rare)
- **Query performance** (should stay <5ms warm cache)
- **Cache hit rate** (should be >80%)
- **Boundary violations** (logged when limits hit)

### Log Messages to Watch

**Normal Operation**:
- "Knowledge Graph enhancement enabled" (info)
- "Knowledge Graph enhancement successful" (info)
- "Traversal complete: {...}" (info with stats)

**Investigate**:
- "Knowledge Graph enhancement failed" (error - check cause)
- "Search failed with boundaries" (error - check query)

**Expected Occasionally**:
- "Max depth reached" (warning - boundary hit)
- "Max nodes reached" (warning - boundary hit)
- "Time limit exceeded" (warning - boundary hit)

## Future Enhancements

**Phase 3 Foundation** (complete):
- Basic context enhancement
- Session-based queries
- Keyword matching

**Future Possibilities**:
- Advanced NER (Named Entity Recognition)
- Semantic search with embeddings
- Temporal pattern analysis
- Cross-session insights (with privacy controls)
- Proactive recommendations
- Graph visualization

## Related Documentation

- **Issue #99**: CORE-KNOW (Knowledge Graph connection)
- **Issue #230**: CORE-KNOW-BOUNDARY (Boundary enforcement)
- **Sprint A3**: "Some Assembly Required"
- **Phase Reports**: `dev/2025/10/18/phase-*-report.md`
- **Configuration Guide**: `docs/operations/knowledge-graph-config.md`

## Status

**Current**: ✅ PRODUCTION READY

**Timeline**:
- Activated: October 18, 2025 (Phase 3)
- Protected: October 18, 2025 (Phase 4)
- Documented: October 18, 2025 (Phase 5)

**Confidence**: HIGH
- All tests passing (100%)
- Performance excellent (2.3ms)
- Safety measures active
- Rollback available (<1 minute)

**Risk Level**: LOW
- Feature flag control
- Graceful degradation
- Boundary protection
- Comprehensive testing

---

*Last Updated: October 18, 2025*
*Sprint: A3 "Some Assembly Required"*
*Status: Production Ready*
