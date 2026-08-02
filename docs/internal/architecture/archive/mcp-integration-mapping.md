> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. **Superseded by ADR-070** (MCP-Consumer Connector Architecture) for the MCP-consumer
> connector concern — see ADR-070's own "Supersession note" section, recorded 2026-08-02, rather than
> asserted here as an inference. Zero inbound references confirmed across `docs/ services/ web/
> scripts/ tests/ .claude/ mailboxes/ CLAUDE.md` before archiving. Kept for the record, not current.
> Never delete; if this needs reviving, un-archive it rather than rewriting it fresh.

---

# MCP Integration Points - Complete System Mapping

**Date**: 2025-08-10
**Purpose**: Document all integration points for MCP protocol implementation
**Scope**: PM-033a Consumer Core through PM-033d Server Mode

## Integration Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     External MCP Ecosystem                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐   │
│  │MCP Tools │  │MCP Agents│  │MCP Hubs  │  │Registries│   │
│  └────▲─────┘  └────▲─────┘  └────▲─────┘  └────▲─────┘   │
└───────┼─────────────┼─────────────┼─────────────┼──────────┘
        │             │             │             │
    ┌───▼─────────────▼─────────────▼─────────────▼────┐
    │           MCP Protocol Layer (PM-033a)           │
    │  ┌─────────────────────────────────────────────┐ │
    │  │  JWT Auth  │  Connection Pool  │  Discovery │ │
    │  └─────────────────────────────────────────────┘ │
    └───────────────────┬───────────────────────────────┘
                        │
    ┌───────────────────▼───────────────────────────────┐
    │              Piper Morgan Core Systems            │
    │  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
    │  │Workflow  │  │Query     │  │Intent    │       │
    │  │Engine    │  │Router    │  │Service   │       │
    │  └──────────┘  └──────────┘  └──────────┘       │
    └────────────────────────────────────────────────────┘
```

## Primary Integration Points

### 1. Authentication Integration (JWT → MCP)

**Location**: `services/mcp/consumer/auth_integration.py`
**Integrates With**:
- JWT Service (ADR-012)
- MCP Protocol Authentication
- User Context Management

**Key Functions**:
```python
class MCPAuthenticationBridge:
    async def get_mcp_token(user_context) -> str
    async def validate_federation_token(token) -> bool
    async def refresh_mcp_credentials() -> TokenPair
```

**Data Flow**:
1. User authenticates via JWT
2. JWT claims extracted
3. MCP-specific claims added
4. Protocol token generated
5. Token used for MCP connections

### 2. Workflow Orchestration Integration

**Location**: `services/orchestration/mcp_workflow_adapter.py`
**Integrates With**:
- WorkflowFactory (fixed in PM-090)
- OrchestrationEngine
- MCP Tool Results

**Key Functions**:
```python
class MCPWorkflowAdapter:
    async def mcp_tool_to_workflow(tool_call) -> Workflow
    async def workflow_to_mcp_response(workflow) -> MCPResponse
    async def federate_workflow_execution(workflow) -> MCPResult
```

**Integration Pattern**:
- MCP tool calls → Intent classification
- Intent → Workflow creation
- Workflow execution → MCP response
- Result formatting for protocol compliance

### 3. Query Router Enhancement

**Location**: `services/queries/mcp_query_extension.py`
**Integrates With**:
- QueryRouter (with degradation handling)
- MCP Resource Discovery
- External MCP Services

**Key Functions**:
```python
class MCPQueryExtension:
    async def query_mcp_resources(query, servers) -> QueryResult
    async def federate_query(query) -> FederatedResults
    async def cache_mcp_responses(results) -> None
```

**Query Flow**:
1. User query received
2. Local resources searched
3. MCP federation triggered
4. Results aggregated
5. Response formatted

### 4. Slack → MCP Bridge (PM-033c)

**Location**: `services/integrations/mcp_bridge/`
**Integrates With**:
- Slack Spatial Intelligence (9,063 lines)
- MCP Server Mode
- Protocol Translation Layer

**Key Services to Bridge**:
```python
# High-Value Slack Services for MCP Exposure
spatial_services = {
    "spatial_intent_classifier": SpatialIntentClassifier,
    "attention_model": AttentionModel,
    "spatial_memory": SpatialMemory,
    "spatial_mapper": SpatialMapper,
    "workspace_navigator": WorkspaceNavigator
}
```

**Bridge Architecture**:
```python
class SlackMCPBridge:
    async def expose_spatial_intelligence() -> MCPService
    async def translate_slack_event(event) -> MCPEvent
    async def serve_attention_model() -> MCPTool
```

### 5. Configuration Management

**Location**: `services/infrastructure/config/mcp_configuration.py`
**Integrates With**:
- Environment Variables
- Feature Flags
- Dynamic Configuration

**Configuration Hierarchy**:
```yaml
MCP Configuration:
  Consumer Mode:
    - Client settings
    - Connection pooling
    - Tool federation
  Bridge Mode:
    - Service exposure
    - Translation rules
    - Performance tuning
  Server Mode:
    - API endpoints
    - Rate limiting
    - Authentication
```

### 6. Database Integration

**Location**: `services/repositories/mcp_repository.py`
**Integrates With**:
- PostgreSQL (AsyncSessionFactory)
- Redis Cache
- ChromaDB Vectors

**Data Models**:
```python
class MCPToolCache:
    tool_id: str
    server_url: str
    metadata: Dict
    cached_at: datetime

class MCPFederationLog:
    request_id: str
    tool_name: str
    parameters: Dict
    result: Any
    latency_ms: float
```

### 7. Monitoring & Observability

**Location**: `services/observability/mcp_metrics.py`
**Integrates With**:
- Health Monitor
- Performance Metrics
- Audit Logging

**Key Metrics**:
```python
mcp_metrics = {
    "connection_pool_size": Gauge,
    "tool_execution_latency": Histogram,
    "federation_success_rate": Counter,
    "cache_hit_ratio": Gauge,
    "protocol_errors": Counter
}
```

## Secondary Integration Points

### 8. Error Handling Integration

**Integrates With**: Global error handler, User guides
**Pattern**: MCP errors → User-friendly messages → Help links

### 9. Testing Infrastructure

**Integrates With**: Reality testing framework
**Pattern**: No mocking of MCP protocol paths

### 10. Security Layer

**Integrates With**: Rate limiting, Audit logging, PII filtering
**Pattern**: All MCP calls through security middleware

## Integration Priorities

### Phase 1 (PM-033a) - Must Have
1. ✅ JWT Authentication Bridge
2. ✅ Basic MCP Client
3. ✅ Configuration Management
4. ✅ Error Handling

### Phase 2 (PM-033b) - Should Have
5. Query Router Enhancement
6. Workflow Adapter
7. Tool Federation
8. Caching Layer

### Phase 3 (PM-033c) - Nice to Have
9. Slack Bridge
10. Monitoring Integration
11. Database Persistence
12. Performance Optimization

### Phase 4 (PM-033d) - Future
13. Server Mode Endpoints
14. Federation Management
15. Marketplace Integration
16. Enterprise Features

## Integration Testing Strategy

### Reality Testing Requirements
```python
# tests/integration/mcp/test_integration_reality.py
class TestMCPIntegrationReality:
    """Test real integration points without mocking"""

    async def test_jwt_to_mcp_flow():
        # Real JWT → Real MCP token

    async def test_workflow_federation():
        # Real workflow → Real MCP execution

    async def test_query_aggregation():
        # Real query → Real federated results
```

### Performance Benchmarks
- JWT → MCP token: <10ms
- Tool discovery: <500ms
- Tool execution: <1s
- Query federation: <2s
- Cache operations: <5ms

## Risk Mitigation

### Integration Risks
1. **Protocol Version Mismatch**: Compatibility layer
2. **Authentication Failures**: Fallback to local execution
3. **Network Latency**: Aggressive caching strategy
4. **Rate Limiting**: Client-side throttling

### Mitigation Strategies
- Circuit breakers on all external calls
- Graceful degradation to local services
- Comprehensive error recovery
- Performance monitoring alerts

## Success Criteria

### Technical Success
- [ ] All 10 primary integration points functional
- [ ] <1s average integration latency
- [ ] 99.9% authentication success rate
- [ ] Zero data loss during federation

### Business Success
- [ ] 5+ external tools integrated
- [ ] 30% workflow automation improvement
- [ ] User satisfaction with federation
- [ ] Foundation for server mode

---

**Integration Readiness**: Complete mapping of all integration points with clear implementation priorities and testing strategies for Monday's aggressive MCP development sprint.
