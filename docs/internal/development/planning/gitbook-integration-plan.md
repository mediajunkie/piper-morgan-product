# GitBook MCP + Spatial Intelligence Integration Plan

> ⚠️ **Dated note (2026-08-29)**: this plan is HISTORICAL. The GitBook spatial modules it
> describes (`services/intelligence/spatial/gitbook_spatial.py`, its `integrations/spatial`
> counterpart, and the GitBook MCP adapters) were disposed of in the PM-ruled 2026-08-15/16
> spatial cold-island disposal — never-wired committed-theory code, zero importers. Prior art:
> commit-hash references in the 2026-08-29 spatial-disposal entry of
> `docs/internal/architecture/decisions/decisions.log`; design semantics in
> `docs/internal/architecture/design-records/spatial-cold-island-per-connector-place-modeling.md`.

## 🎯 **OBJECTIVE**

Complete PM-033b final criterion by implementing GitBook integration following our proven MCP+Spatial Intelligence pattern.

## 🔍 **RESEARCH FINDINGS**

### **GitBook API Overview**

- **Base URLs**:
  - REST API: `https://api.gitbook.com/v1/`
  - GraphQL API: `https://api.gitbook.com/graphql`
- **Authentication**: Personal Access Tokens (Bearer) + OAuth 2.0
- **Rate Limits**: 1000 requests per hour per token
- **API Version**: v1 (REST), GraphQL (latest)

### **GitBook Data Structures**

```
GitBook Hierarchy:
├── Spaces (organizations/workspaces)
│   ├── Collections (content groupings)
│   │   ├── Pages (individual content)
│   │   │   └── Sub-pages (nested content)
│   │   └── Users (permissions, roles)
│   └── Users (space members)
```

### **GitBook vs Notion Differences**

| Aspect        | GitBook                   | Notion                            |
| ------------- | ------------------------- | --------------------------------- |
| **Structure** | Space → Collection → Page | Workspace → Database/Page → Block |
| **Focus**     | Documentation-centric     | Database-driven                   |
| **Hierarchy** | Fixed 3-level             | Flexible nesting                  |
| **Content**   | Markdown-based            | Rich text + properties            |
| **API**       | REST + GraphQL            | REST only                         |

## 🏗️ **IMPLEMENTATION ARCHITECTURE**

### **1. MCP Adapter Layer (`services/integrations/mcp/gitbook_adapter.py`)**

```python
class GitBookMCPAdapter(BaseSpatialAdapter):
    """GitBook MCP spatial adapter implementation"""

    def __init__(self):
        super().__init__("gitbook_mcp")
        self._gitbook_token: Optional[str] = None
        self._api_base = "https://api.gitbook.com/v1"
        self._session: Optional[aiohttp.ClientSession] = None

    async def configure_gitbook_api(self, token: str, api_base: Optional[str] = None):
        """Configure GitBook API access"""

    async def get_spaces(self) -> List[Dict[str, Any]]:
        """Get accessible GitBook spaces"""

    async def get_space_content(self, space_id: str) -> Dict[str, Any]:
        """Get space content tree (collections + pages)"""

    async def get_page(self, space_id: str, page_id: str) -> Optional[Dict[str, Any]]:
        """Get specific page content"""

    async def search_pages(self, space_id: str, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        """Search pages within a space"""

    async def get_collections(self, space_id: str) -> List[Dict[str, Any]]:
        """Get collections in a space"""

    async def get_users(self, space_id: str) -> List[Dict[str, Any]]:
        """Get space users and permissions"""
```

### **2. Spatial Intelligence Layer (`services/intelligence/spatial/gitbook_spatial.py`)**

```python
class GitBookSpatialIntelligence:
    """GitBook integration using MCP + Spatial Intelligence pattern"""

    def __init__(self):
        self.mcp_adapter = GitBookMCPAdapter()

        # 8-dimensional analysis functions
        self.dimensions = {
            "HIERARCHY": self.analyze_space_hierarchy,      # Space → Collection → Page
            "TEMPORAL": self.analyze_content_timeline,      # Last updated, created
            "PRIORITY": self.analyze_visibility_status,     # Public, private, restricted
            "COLLABORATIVE": self.analyze_user_activity,    # Authors, editors, permissions
            "FLOW": self.analyze_content_workflow,          # Content states, publishing
            "QUANTITATIVE": self.analyze_content_metrics,   # Page counts, sizes, engagement
            "CAUSAL": self.analyze_content_relations,      # Parent-child, references
            "CONTEXTUAL": self.analyze_space_context,       # Space context, collections
        }

    async def analyze_space_hierarchy(self, space_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze GitBook space hierarchy (HIERARCHY dimension)"""
        # Map: Space → Collections → Pages → Sub-pages
        # Territory: GitBook organization
        # Room: Space
        # Path: Collection hierarchy
        # Object: Individual pages

    async def analyze_content_timeline(self, page_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content temporal patterns (TEMPORAL dimension)"""
        # Last updated, created, publishing dates
        # Content freshness, update frequency

    async def analyze_visibility_status(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content visibility and access (PRIORITY dimension)"""
        # Public, private, restricted access
        # Publishing status, approval workflows

    async def analyze_user_activity(self, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze user collaboration patterns (COLLABORATIVE dimension)"""
        # Authors, editors, permissions
        # Last activity, contribution patterns

    async def analyze_content_workflow(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content workflow states (FLOW dimension)"""
        # Draft, published, archived
        # Review status, approval workflows

    async def analyze_content_metrics(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze quantitative content metrics (QUANTITATIVE dimension)"""
        # Page counts, content sizes
        # View counts, engagement metrics

    async def analyze_content_relations(self, content_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze content relationships (CAUSAL dimension)"""
        # Parent-child page relationships
        # Cross-references, dependencies

    async def analyze_space_context(self, space_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze space and collection context (CONTEXTUAL dimension)"""
        # Space purpose, collection themes
        # Content organization patterns
```

### **3. QueryRouter Integration (`services/queries/query_router_spatial_migration.py`)**

```python
# Extend existing QueryRouterSpatialEnhancement
class QueryRouterSpatialEnhancement:
    def __init__(self, query_router):
        # ... existing code ...
        self.gitbook_spatial = None

        if self.query_router.enable_mcp_federation:
            self._upgrade_to_spatial()

    def _upgrade_to_spatial(self):
        # ... existing code ...
        self.gitbook_spatial = GitBookSpatialIntelligence()
        self.query_router.gitbook_adapter = self.gitbook_spatial.mcp_adapter

    async def federated_search_with_spatial(
        self, query: str, include_gitbook: bool = True
    ) -> Dict[str, Any]:
        """Enhanced federated search with GitBook + GitHub + Linear"""
        # ... existing code ...
        if include_gitbook and self.gitbook_spatial:
            gitbook_results = await self._search_gitbook_with_spatial(query)
            results["gitbook_results"] = gitbook_results
            if gitbook_results:
                results["sources"].append("gitbook_mcp")
```

## 🔧 **IMPLEMENTATION STEPS**

### **Phase 1: Core MCP Adapter (Day 1)**

1. **Create GitBook MCP Adapter**

   - Implement authentication (Personal Access Token)
   - Basic API calls (spaces, collections, pages)
   - Error handling and rate limiting
   - Spatial position mapping

2. **Implement Core Methods**
   - `get_spaces()` - List accessible spaces
   - `get_space_content()` - Get content tree
   - `get_page()` - Get specific page
   - `search_pages()` - Search within space

### **Phase 2: Spatial Intelligence (Day 2)**

1. **Implement 8-Dimensional Analysis**

   - HIERARCHY: Space → Collection → Page mapping
   - TEMPORAL: Content timeline analysis
   - PRIORITY: Visibility and access analysis
   - COLLABORATIVE: User activity patterns
   - FLOW: Content workflow states
   - QUANTITATIVE: Content metrics
   - CAUSAL: Content relationships
   - CONTEXTUAL: Space and collection context

2. **Spatial Context Creation**
   - Map GitBook entities to spatial positions
   - Create comprehensive spatial context
   - Integrate with existing spatial metaphor system

### **Phase 3: QueryRouter Integration (Day 3)**

1. **Extend Spatial Migration**

   - Add GitBook to QueryRouterSpatialEnhancement
   - Implement federated search with GitBook
   - Maintain backward compatibility

2. **Testing and Validation**
   - Unit tests for each dimension
   - Integration tests with QueryRouter
   - Performance validation (<150ms targets)

## 📊 **8-DIMENSIONAL FRAMEWORK MAPPING**

### **HIERARCHY Dimension**

- **Territory**: GitBook organization
- **Room**: Individual space
- **Path**: Collection hierarchy
- **Object**: Individual pages

### **TEMPORAL Dimension**

- **Content Age**: Creation and update timestamps
- **Activity Level**: Update frequency patterns
- **Publishing Timeline**: Draft → Published → Archived

### **PRIORITY Dimension**

- **Visibility**: Public, private, restricted
- **Access Level**: Read, write, admin permissions
- **Content Status**: Draft, published, archived

### **COLLABORATIVE Dimension**

- **Authors**: Content creators
- **Editors**: Content modifiers
- **Permissions**: User access levels
- **Activity**: Last contribution timestamps

### **FLOW Dimension**

- **Content States**: Draft, review, published, archived
- **Workflow**: Approval processes, publishing pipelines
- **Transitions**: State change patterns

### **QUANTITATIVE Dimension**

- **Page Counts**: Total pages per space/collection
- **Content Sizes**: Page lengths, media counts
- **Engagement**: View counts, edit frequencies

### **CAUSAL Dimension**

- **Parent-Child**: Page hierarchy relationships
- **References**: Cross-page links and citations
- **Dependencies**: Content prerequisites

### **CONTEXTUAL Dimension**

- **Space Purpose**: Documentation focus areas
- **Collection Themes**: Content grouping patterns
- **Organizational Context**: Business unit alignment

## 🚀 **SUCCESS CRITERIA**

### **Functional Requirements**

- ✅ GitBook API integration operational
- ✅ All 8 dimensions implemented and functional
- ✅ QueryRouter federation working (GitHub + Linear + GitBook)
- ✅ Performance targets met (<150ms federated queries)

### **Technical Requirements**

- ✅ MCP protocol compliance
- ✅ Spatial intelligence integration
- ✅ Error handling and circuit breaker protection
- ✅ Rate limiting compliance (1000 req/hour)
- ✅ Comprehensive test coverage

### **PM-033b Completion**

- ✅ Multi-tool federation operational
- ✅ Spatial intelligence across all tools
- ✅ Architectural signature established
- ✅ Production readiness validated

## 🔒 **CONFIGURATION REQUIREMENTS**

### **Environment Variables**

```bash
GITBOOK_API_TOKEN=your_personal_access_token
GITBOOK_API_BASE=https://api.gitbook.com/v1
GITBOOK_ORGANIZATION_ID=your_org_id  # Optional
```

### **API Permissions**

- **Read Access**: Spaces, collections, pages
- **User Info**: Basic user details and permissions
- **Search**: Content search capabilities

## 📚 **RESOURCES & REFERENCES**

### **GitBook API Documentation**

- [GitBook API Reference](https://docs.gitbook.com/api/)
- [Authentication Guide](https://docs.gitbook.com/api/authentication)
- [Rate Limiting](https://docs.gitbook.com/api/rate-limiting)

### **Implementation Patterns**

- **Notion Integration**: `services/intelligence/spatial/notion_spatial.py`
- **Linear Integration**: `services/intelligence/spatial/linear_spatial.py`
- **MCP Pattern**: `services/integrations/mcp/notion_adapter.py`

### **Testing Framework**

- **Test File**: `tests/integration/test_gitbook_spatial_federation.py`
- **Pattern**: Follow existing Linear/Notion test structure
- **Coverage**: All 8 dimensions + integration scenarios

---

**Status**: 📋 **PLAN COMPLETE** - Ready for implementation
**Timeline**: 3 days for full integration
**Dependencies**: GitBook API access token
**Next Step**: Begin Phase 1 implementation
