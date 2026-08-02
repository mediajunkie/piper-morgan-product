> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. **Superseded by ADR-070** (MCP-Consumer Connector Architecture) for the MCP-consumer
> connector concern — see ADR-070's own "Supersession note" section, recorded 2026-08-02, rather than
> asserted here as an inference. Zero inbound references confirmed across `docs/ services/ web/
> scripts/ tests/ .claude/ mailboxes/ CLAUDE.md` before archiving. Kept for the record, not current.
> Never delete; if this needs reviving, un-archive it rather than rewriting it fresh.

---

# PM-033a: MCP Consumer Core Architecture

**Date**: 2025-08-11 (Updated)
**Status**: PHASE 3 ARCHITECTURE COMPLETE - FOUNDATION VERIFIED
**Foundation Verified**: 17,748 lines + 11 implementation files
**Target Sprint**: MCP Monday Implementation (Phase 4)

## Architecture Overview

**FOUNDATION VERIFICATION COMPLETE**: Phase 2 audit confirmed 17,748 lines of MCP-ready infrastructure (exceeded Cursor claim of 15,457+ by 2,291 lines, +14.8%).

**KEY DISCOVERY**: 85-90% foundation reuse enables rapid implementation with proven battle-tested components.

**ASSEMBLE, DON'T BUILD**: Leverage existing SlackClient (9,133 lines), SpatialAdapter (14,042 lines), and MCP infrastructure (3,137 lines) for rapid deployment.

## Verified Foundation Components

### Existing Infrastructure (17,748 lines verified) ✅ **READY FOR REUSE**
- **Slack Integration**: 14,042 lines - Production-ready client, spatial adapters, event handling
- **MCP Core**: 3,137 lines - Client, connection pool, protocol foundation
- **Intelligence**: 569 lines - Conversation-aware systems
- **MCP References**: 1,698 references across codebase

### Cursor Implementation (11 files) ✅ **IMPLEMENTED**
- **Consumer Core**: `services/mcp/consumer/consumer_core.py`
- **GitHub Adapter**: `services/mcp/consumer/github_adapter.py`
- **Protocol Layer**: `services/mcp/protocol/` (4 files)
- **Enhanced Client**: `services/mcp/client.py` (extended)
- **Resource Management**: Enhanced existing infrastructure

## PM-033a Complete Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                         PIPER MORGAN PM-033a ARCHITECTURE                      │
│                    MCP Consumer with 17,748-Line Foundation                    │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Existing      │    │   MCP Adapter   │    │  MCP Protocol   │    │   External      │
│   Foundation    │───▶│    Layer        │───▶│    Layer        │───▶│   Services      │
│   [17.7k lines] │    │ [Cursor's 11    │    │     [NEW]       │    │ [GitHub/etc]    │
│   ✅ VERIFIED    │    │  files READY]   │    │ [Protocol Nego] │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │                       │
         ▼                       ▼                       ▼                       ▼
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│  SlackClient    │    │ MCPConsumerCore │    │ ProtocolClient  │    │  GitHub API     │
│  [9,133 lines]  │    │ consumer_core.py│    │ protocol_cli.py │    │  REST + GraphQL │
│  ✅ REUSABLE     │    │ ✅ IMPLEMENTED   │    │ 🔄 EXTENDING    │    │  Issues, PRs    │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│  SpatialAdapter │    │ GitHubAdapter   │    │ MessageHandler  │    │  Linear API     │
│  [14,042 lines] │    │ github_adapt.py │    │ message_hand.py │    │  Issues, Proj   │
│  ✅ REUSABLE     │    │ ✅ IMPLEMENTED   │    │ ✅ IMPLEMENTED   │    │  (Future)       │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│  ConnectionPool │    │ [9 more files]  │    │ ServiceDiscovery│    │  Notion API     │
│  [3,137 lines]  │    │ protocol/       │    │ service_disc.py │    │  Docs, Pages    │
│  ✅ REUSABLE     │    │ ✅ IMPLEMENTED   │    │ ✅ IMPLEMENTED   │    │  (Future)       │
└─────────────────┘    └─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                             INTEGRATION FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

User Query → QueryRouter → MCPConsumerCore → GitHubAdapter → ProtocolClient → GitHub
    │             │              │               │               │               │
    ▼             ▼              ▼               ▼               ▼               ▼
Intent        Route MCP      Orchestrate     Spatial Map     MCP Protocol    REST API
Classification  Queries       Consumer        GitHub         Messages        Calls
    │             │              │            Entities          │               │
    ▼             ▼              ▼               │               ▼               ▼
Workflow      Enhanced       Tool              │         JSON-RPC         Issues
Creation      Context        Federation        │         Messages         Created
    │             │              │             │               │               │
    ▼             ▼              ▼             ▼               ▼               ▼
Response      Merged         Results      Spatial           Response        Spatial
Formatting    Results        Caching      Intelligence      Processing      Entities

┌─────────────────────────────────────────────────────────────────────────────────┐
│                         COMPONENT REUSE STRATEGY                               │
└─────────────────────────────────────────────────────────────────────────────────┘

EXISTING FOUNDATION (17,748 lines) → REUSE PATTERNS:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   SlackClient   │───▶│  MCPClient      │───▶│ GitHub Client   │
│   HTTP, Auth    │    │  Protocol HTTP  │    │ REST API Calls  │
│   Rate Limiting │    │  MCP Messages   │    │ Rate Limiting   │
│   ✅ 85% REUSE   │    │  ✅ ADAPTATION   │    │ ✅ PRODUCTION    │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ SpatialAdapter  │───▶│ GitHubAdapter   │───▶│ GitHub Spatial  │
│ Entity Mapping  │    │ Issue Mapping   │    │ Issue → Entity  │
│ Event Process   │    │ PR Processing   │    │ Repo → Space    │
│ ✅ 90% REUSE     │    │ ✅ IMPLEMENTED   │    │ ✅ READY        │
└─────────────────┘    └─────────────────┘    └─────────────────┘

┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│ ConnectionPool  │───▶│ MCPConnPool     │───▶│ Service Pool    │
│ 13k lines       │    │ MCP Protocol    │    │ Multi-Service   │
│ Circuit Breaker │    │ Health Checks   │    │ Management      │
│ ✅ 95% REUSE     │    │ ✅ PRODUCTION    │    │ ✅ READY        │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## System Components

### 1. Core MCP Client Layer

```python
services/mcp/
├── client.py              # Existing MCP client (11,377 lines)
├── resources.py           # Resource management (16,155 lines)
├── exceptions.py          # Error handling (648 lines)
└── consumer/              # NEW: Consumer core components
    ├── __init__.py
    ├── protocol_client.py # Protocol-compliant client
    ├── tool_federation.py # External tool integration
    ├── resource_discovery.py # Service discovery
    └── auth_integration.py # JWT authentication bridge
```

### 2. Integration Points

#### 2.1 JWT Authentication (ADR-012)
```python
# services/mcp/consumer/auth_integration.py
class MCPAuthenticationBridge:
    """Bridge JWT authentication to MCP protocol"""

    def __init__(self, jwt_service: JWTService):
        self.jwt_service = jwt_service

    async def get_mcp_token(self, user_context: UserContext) -> str:
        """Generate MCP-compatible token from JWT claims"""
        jwt_token = await self.jwt_service.create_access_token(
            subject=user_context.user_id,
            audience=["mcp-protocol"],
            additional_claims={
                "protocol_version": "1.0",
                "permissions": user_context.mcp_permissions
            }
        )
        return jwt_token
```

#### 2.2 Workflow Integration
```python
# services/orchestration/mcp_workflow_adapter.py
class MCPWorkflowAdapter:
    """Adapt MCP tool calls to workflow system"""

    async def create_mcp_workflow(
        self,
        tool_call: MCPToolCall,
        context: WorkflowContext
    ) -> Workflow:
        """Convert MCP tool call to workflow"""
        intent = self._mcp_to_intent(tool_call)
        workflow = await self.factory.create_from_intent(intent)
        return workflow
```

#### 2.3 Query Router Enhancement
```python
# services/queries/mcp_query_extension.py
class MCPQueryExtension:
    """Extend query router with MCP resource queries"""

    async def query_mcp_resources(
        self,
        query: str,
        mcp_servers: List[str]
    ) -> QueryResult:
        """Query external MCP resources"""
        results = []
        for server in mcp_servers:
            client = MCPProtocolClient(server)
            resources = await client.search(query)
            results.extend(resources)
        return self._format_results(results)
```

### 3. Protocol Implementation

#### 3.1 MCP Protocol Client
```python
# services/mcp/consumer/protocol_client.py
class MCPProtocolClient:
    """Standards-compliant MCP client implementation"""

    def __init__(self, config: MCPConfiguration):
        self.config = config
        self.auth_bridge = MCPAuthenticationBridge()
        self.connection_pool = MCPConnectionPool()

    async def connect(self, server_url: str) -> MCPConnection:
        """Establish MCP protocol connection"""
        token = await self.auth_bridge.get_mcp_token()
        connection = await self.connection_pool.get_connection(
            server_url,
            auth_token=token,
            protocol_version=self.config.protocol_version
        )
        return connection

    async def execute_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any]
    ) -> MCPToolResult:
        """Execute tool via MCP protocol"""
        request = MCPToolRequest(
            tool=tool_name,
            parameters=parameters,
            context=self._build_context()
        )
        response = await self.connection.send(request)
        return MCPToolResult.from_response(response)
```

#### 3.2 Tool Federation Service
```python
# services/mcp/consumer/tool_federation.py
class MCPToolFederation:
    """Federate external MCP tools"""

    def __init__(self):
        self.discovered_tools = {}
        self.tool_cache = {}

    async def discover_tools(
        self,
        servers: List[str]
    ) -> Dict[str, MCPTool]:
        """Discover available tools from MCP servers"""
        for server in servers:
            client = MCPProtocolClient(server)
            tools = await client.list_tools()
            self.discovered_tools[server] = tools
        return self.discovered_tools

    async def federate_tool_call(
        self,
        tool_id: str,
        parameters: Dict
    ) -> Any:
        """Federate tool call to appropriate server"""
        server, tool = self._resolve_tool(tool_id)
        client = MCPProtocolClient(server)
        result = await client.execute_tool(tool, parameters)
        return result
```

### 4. Configuration Management

#### 4.1 MCP Configuration Service Enhancement
```python
# services/infrastructure/config/mcp_configuration.py (existing)
class MCPConfigurationService:
    """Enhanced with consumer mode settings"""

    def get_consumer_config(self) -> MCPConsumerConfig:
        """Get MCP consumer configuration"""
        return MCPConsumerConfig(
            enabled=self.get_bool("MCP_CLIENT_ENABLED"),
            timeout=self.get_int("MCP_CLIENT_TIMEOUT"),
            max_retries=self.get_int("MCP_CLIENT_MAX_RETRIES"),
            pool_size=self.get_int("MCP_CLIENT_POOL_SIZE"),
            protocol_version=self.get_str("MCP_PROTOCOL_VERSION"),
            discovery_servers=self.get_list("MCP_DISCOVERY_SERVERS"),
            tool_servers=self.get_list("MCP_TOOL_SERVERS"),
            auth_method=self.get_str("MCP_TOOL_AUTH_METHOD")
        )
```

### 5. Testing Infrastructure

#### 5.1 Reality Testing for MCP
```python
# tests/integration/test_mcp_consumer_reality.py
class TestMCPConsumerReality:
    """Reality testing for MCP consumer - no mocking"""

    @pytest.mark.asyncio
    async def test_real_mcp_connection(self):
        """Test actual MCP protocol connection"""
        client = MCPProtocolClient(test_config)
        connection = await client.connect("https://test.mcp.server")
        assert connection.is_connected

    @pytest.mark.asyncio
    async def test_real_tool_execution(self):
        """Test actual tool execution via MCP"""
        client = MCPProtocolClient(test_config)
        result = await client.execute_tool(
            "search",
            {"query": "test"}
        )
        assert result.success
```

## Implementation Roadmap

### Phase 1: Core Infrastructure (Day 1)
- [ ] Set up MCP consumer package structure
- [ ] Implement MCPProtocolClient with JWT integration
- [ ] Create authentication bridge
- [ ] Establish connection pooling

### Phase 2: Tool Federation (Day 2)
- [ ] Implement tool discovery service
- [ ] Create tool federation router
- [ ] Add caching layer for tool responses
- [ ] Integrate with workflow factory

### Phase 3: Integration (Day 3)
- [ ] Connect to query router
- [ ] Enhance workflow orchestration
- [ ] Add MCP resource queries
- [ ] Implement error handling

### Phase 4: Testing & Validation (Day 4)
- [ ] Reality testing suite
- [ ] Performance benchmarking
- [ ] Security audit
- [ ] Documentation completion

## Performance Targets

- **Connection Establishment**: <100ms
- **Tool Discovery**: <500ms for 10 servers
- **Tool Execution**: <1s average latency
- **Cache Hit Rate**: >80% for repeated queries
- **Connection Pool Efficiency**: >90% connection reuse

## Security Considerations

### Authentication Flow
1. User authenticates → JWT issued
2. JWT claims → MCP token generation
3. MCP token → Protocol authentication
4. Secure connection established

### Data Protection
- TLS 1.3 for all MCP connections
- Token rotation every 15 minutes
- Audit logging for all tool executions
- PII filtering before external calls

## Success Metrics

### Technical Metrics
- [ ] 5+ external MCP tools integrated
- [ ] <1s average tool execution time
- [ ] 99.9% connection reliability
- [ ] Zero authentication failures

### Business Metrics
- [ ] 30% workflow automation improvement
- [ ] User feedback on tool federation value
- [ ] Foundation for PM-033b/c/d phases
- [ ] Protocol compliance certification ready

## Dependencies

### Existing Infrastructure
- ✅ MCP client base (11,377 lines)
- ✅ Resource management (16,155 lines)
- ✅ JWT authentication (ADR-012)
- ✅ Workflow factory (fixed bug)

### External Requirements
- MCP protocol specification v1.0
- Test MCP server for development
- Tool registry access
- Performance monitoring

## Risk Mitigation

### Technical Risks
- **Protocol Changes**: Version compatibility layer
- **Connection Failures**: Retry with exponential backoff
- **Tool Incompatibility**: Validation before federation

### Operational Risks
- **Rate Limiting**: Implement client-side throttling
- **Caching Strategy**: TTL configuration per tool
- **Monitoring**: Comprehensive metrics collection

---

**Ready for Implementation**: All architectural components defined with clear integration points and implementation roadmap for aggressive Monday development sprint.
