# CORE-KNOW: Connect Knowledge Graph to Conversation (#99)

## Description
Connect the Knowledge Graph to conversation flow, enabling queries for project context, recent patterns, and enhanced response generation with deep contextual understanding.

## Problem Statement
Existing Knowledge Graph (PM-040 complete ✅) is not integrated into conversation flow, missing opportunities for:
- Rich project context from graph relationships
- Pattern recognition from historical interactions
- Contextual connections between projects, goals, and stakeholders
- Proactive insights based on graph knowledge

## Solution: Knowledge Graph Conversation Integration
Wire Knowledge Graph queries into conversation context resolution:
- Query graph for relevant project relationships
- Retrieve recent interaction patterns
- Include graph insights in response generation
- Enable contextual recommendations based on graph analysis

## Acceptance Criteria
- [ ] Integration layer between conversation service and Knowledge Graph
- [ ] Query graph for project context based on conversation topics
- [ ] Retrieve recent patterns and relationships relevant to current query
- [ ] Include graph insights in response generation context
- [ ] Test with canonical queries - enhanced contextual responses
- [ ] Performance target: Graph queries add <100ms to response time
- [ ] Graceful degradation if Knowledge Graph unavailable

## Technical Implementation
```python
# services/conversation/knowledge_graph_integration.py
class ConversationKnowledgeGraphIntegration:
    def __init__(self, knowledge_graph_service: KnowledgeGraphService):
        self.kg_service = knowledge_graph_service

    async def get_conversation_context(self, query: str,
                                     user_context: Dict) -> Dict[str, Any]:
        """Get relevant Knowledge Graph context for conversation"""

    async def query_project_relationships(self, project_names: List[str]) -> List[Dict]:
        """Query graph for project relationships and dependencies"""

    async def get_recent_patterns(self, timeframe_days: int = 30) -> List[Dict]:
        """Retrieve recent interaction patterns from graph"""

    async def enhance_response_context(self, base_context: Dict,
                                     graph_context: Dict) -> Dict:
        """Enhance response context with graph insights"""
```

## Knowledge Graph Queries for Conversations
### Project Context Queries
- Find projects related to current query topics
- Retrieve project dependencies and relationships
- Get stakeholders associated with mentioned projects
- Identify recent project activities and updates

### Pattern Recognition Queries
- Recent conversation patterns and topics
- Frequently discussed project combinations
- Seasonal patterns in project focus and priorities
- Correlation between questions and project phases

### Contextual Enhancement Queries
- Related concepts and entities for current topic
- Historical decisions and outcomes for similar situations
- Best practices and lessons learned from graph knowledge
- Cross-project insights and recommendations

## Integration Points
### With PIPER.md System (UX-001.2)
```python
async def enhance_piper_context_with_graph(piper_context: Dict,
                                         graph_context: Dict) -> Dict:
    """Combine PIPER.md static context with dynamic graph insights"""
    enhanced_context = piper_context.copy()
    enhanced_context['graph_insights'] = graph_context
    enhanced_context['related_projects'] = graph_context.get('projects', [])
    enhanced_context['recent_patterns'] = graph_context.get('patterns', [])
    return enhanced_context
```

### With Conversation Manager
```python
# Enhanced conversation context with graph integration
class EnhancedConversationContext:
    def __init__(self, base_context: Dict, graph_context: Dict):
        self.base_context = base_context
        self.graph_context = graph_context
        self.enhanced_context = self._merge_contexts()

    def _merge_contexts(self) -> Dict:
        """Merge base conversation context with graph insights"""
```

## Response Enhancement Examples
### Before Graph Integration
```
User: "What's the status of the website project?"
Response: "I need more information about which website project you're referring to."
```

### After Graph Integration
```
User: "What's the status of the website project?"
Response: "The pmorgan.tech Website MVP (SITE-001) is in progress with 3 of 5 phases complete.
Based on recent activity, you've been focused on the technical foundation and design system.
The current blocker appears to be integrations with ConvertKit and Medium RSS feeds."
```

## Performance Requirements
- **Graph Query Time**: <100ms for conversation-relevant queries
- **Context Enhancement**: <50ms to merge graph context with conversation
- **Caching**: Cache frequently accessed graph patterns
- **Fallback**: Graceful degradation if Knowledge Graph slow/unavailable

## Testing Strategy
1. **Integration Tests**: Verify Knowledge Graph connection and queries
2. **Performance Tests**: Graph queries within time limits
3. **Context Tests**: Enhanced context improves response quality
4. **Canonical Query Tests**: Improved responses with graph context

## Success Criteria
- Knowledge Graph successfully integrated into conversation flow
- Canonical queries demonstrate enhanced contextual understanding
- Response quality improved with graph insights and relationships
- Performance targets met (<100ms additional latency)
- Foundation ready for proactive intelligence (Phase 3)

## Dependencies
- Knowledge Graph Service (PM-040 complete ✅)
- Conversation context system
- PIPER.md integration (UX-001.2)
- Performance monitoring and optimization

## Related Work
- Builds on UX-001.2 (PIPER.md system) and UX-001.3 (Document Ingestion)
- Enables UX-001.7 (Calendar Scanning) and UX-001.8 (Priority Calculation)
- Supports UX-001.11 (Strategic Recommendations)
- Foundation for enhanced conversational intelligence

**Implementation Priority**: Complete after Phase 1 foundation tasks
