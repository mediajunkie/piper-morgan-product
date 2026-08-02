> **ARCHIVED 2026-08-02** — moved from `docs/internal/architecture/current/` per the docs/ tree
> audit (`docs/internal/operations/docs-tree-audit-2026-08-01.md`, Finding 2) and Arch's per-file
> ruling. **Superseded by ADR-070** (MCP-Consumer Connector Architecture) for the MCP-consumer
> connector concern — see ADR-070's own "Supersession note" section, recorded 2026-08-02, rather than
> asserted here as an inference. Zero inbound references confirmed across `docs/ services/ web/
> scripts/ tests/ .claude/ mailboxes/ CLAUDE.md` before archiving. Kept for the record, not current.
> Never delete; if this needs reviving, un-archive it rather than rewriting it fresh.

---

# MCP Integration Points Architecture

**Date**: July 17, 2025
**Purpose**: Architectural analysis of MCP integration with existing Piper Morgan patterns
**Scope**: File Search POC integration points

## Current Architecture Overview

### File Handling Architecture
Piper Morgan follows a layered architecture for file operations:

```
API Layer (main.py)
    ↓
Query Router (file_queries.py)
    ↓
File Repository (file_repository.py) + File Resolver (file_resolver.py)
    ↓
Database Layer (AsyncSession + SQLAlchemy)
    ↓
Domain Models (UploadedFile)
```

### Key Components Analysis

#### 1. FileRepository (services/repositories/file_repository.py)
- **Pattern**: Repository Pattern with AsyncSession
- **Capabilities**:
  - Filename-based search (`search_files_by_name`)
  - Session-scoped and cross-session queries
  - Metadata operations (upload, reference counting)
- **Integration Point**: Name-based search is primary target for MCP enhancement

#### 2. FileResolver (services/file_context/file_resolver.py)
- **Pattern**: Intelligent scoring algorithm
- **Capabilities**:
  - Multi-factor scoring (recency, type, name, usage)
  - Ambiguity detection and resolution
  - Context-aware file selection
- **Integration Point**: Scoring algorithm can incorporate MCP content analysis

#### 3. FileQueryService (services/queries/file_queries.py)
- **Pattern**: Query service for read-only operations
- **Current State**: Basic file metadata retrieval
- **Integration Point**: Primary location for MCP-enhanced queries

#### 4. ProjectContext (services/project_context/project_context.py)
- **Pattern**: Context resolution with session memory
- **Capabilities**: Project resolution hierarchy, session tracking
- **Integration Point**: MCP resources can be project-scoped

## MCP Integration Architecture

### Enhanced File Search Flow
```
Current Flow:
User Query → FileQueryService → FileRepository → SQLAlchemy → File Metadata

Enhanced Flow:
User Query → FileQueryService → MCP Resource Manager → FileRepository + MCP Server → Enhanced Results
```

### Integration Points Mapping

#### 1. Primary Integration: FileQueryService Enhancement
**Location**: `services/queries/file_queries.py`
**Current Method**: `read_file_contents()`, `summarize_file()`
**Enhancement**: Add MCP-powered content search

```python
# Current (metadata only)
async def read_file_contents(self, file_id: str) -> Dict[str, Any]:
    file_data = await self.file_repository.get_file_by_id(file_id)
    return {"success": True, "file": file_data}

# Enhanced (with MCP content)
async def read_file_contents(self, file_id: str, include_content: bool = False) -> Dict[str, Any]:
    file_data = await self.file_repository.get_file_by_id(file_id)

    if include_content and self.mcp_manager:
        content = await self.mcp_manager.get_file_content(file_data.filepath)
        file_data["content"] = content

    return {"success": True, "file": file_data}
```

#### 2. Secondary Integration: FileRepository Search Enhancement
**Location**: `services/repositories/file_repository.py`
**Current Method**: `search_files_by_name()`
**Enhancement**: Add content-aware search method

```python
# New method alongside existing ones
async def search_files_with_content(
    self, session_id: str, query: str, mcp_results: List[MCPFileResult] = None
) -> List[UploadedFile]:
    """Enhanced search combining metadata and content results"""

    # Get standard name-based results
    name_results = await self.search_files_by_name(session_id, query)

    # Merge with MCP content results if available
    if mcp_results:
        combined_results = self._merge_search_results(name_results, mcp_results)
        return combined_results

    return name_results
```

#### 3. Context Integration: FileResolver Enhancement
**Location**: `services/file_context/file_resolver.py`
**Current Method**: `_calculate_score()`
**Enhancement**: Add content relevance scoring

```python
# Enhanced scoring with MCP content analysis
def _calculate_score(self, file: UploadedFile, intent: Intent) -> float:
    total_score = 0.0

    # Existing factors (adjusted weights)
    total_score += self._calculate_recency_score(file.upload_time) * 0.25
    total_score += self._calculate_type_score(file.file_type, intent.action) * 0.25
    total_score += self._calculate_name_score(file.filename, intent) * 0.15
    total_score += self._calculate_usage_score(file) * 0.15

    # New factor: Content relevance (via MCP)
    content_score = await self._calculate_content_score(file, intent)
    total_score += content_score * 0.20

    return min(total_score, 1.0)
```

#### 4. Project Integration: MCP Resource Scoping
**Location**: `services/project_context/project_context.py`
**Integration**: Project-aware MCP resource access

```python
# Project-scoped MCP resources
async def get_project_files(self, project_id: str) -> List[MCPResource]:
    """Get MCP resources scoped to project"""
    if self.mcp_manager:
        return await self.mcp_manager.list_resources(project_filter=project_id)
    return []
```

## Architectural Patterns Preservation

### 1. AsyncSessionFactory Pattern
**Status**: ✅ Preserved
**Implementation**: MCP client uses separate connection management
```python
# MCP client is stateful, but doesn't interfere with AsyncSession
class MCPFileSearch:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository  # AsyncSession-based
        self.mcp_client = MCPClient()           # Separate connection
```

### 2. Domain-Driven Design Boundaries
**Status**: ✅ Preserved
**Implementation**: MCP integration respects domain boundaries
```python
# Domain layer (unchanged)
@dataclass
class UploadedFile:
    id: str
    filename: str
    # ... existing fields

# Infrastructure layer (new)
@dataclass
class MCPFileContent:
    file_id: str
    content: str
    metadata: Dict[str, Any]

# Application layer (enhanced)
class FileQueryService:
    def __init__(self, file_repository: FileRepository, mcp_manager: MCPManager = None):
        self.file_repository = file_repository  # Domain access
        self.mcp_manager = mcp_manager          # Infrastructure access
```

### 3. Error Handling Patterns
**Status**: ✅ Preserved and Extended
**Implementation**: MCP errors follow existing patterns
```python
# Existing error handling for FileRepository
try:
    files = await self.file_repository.search_files_by_name(session_id, query)
except SQLAlchemyError as e:
    logger.error(f"Database error in file search: {e}")
    return []

# New error handling for MCP
try:
    mcp_content = await self.mcp_manager.search_content(query)
except MCPConnectionError as e:
    logger.warning(f"MCP search unavailable: {e}")
    mcp_content = []  # Graceful fallback
```

### 4. Background Task Safety
**Status**: ✅ Preserved
**Implementation**: MCP operations use safe wrapper pattern
```python
# Apply safe_execute_workflow pattern to MCP operations
async def safe_mcp_operation(operation, *args, **kwargs):
    """Safely execute MCP operations with error handling."""
    try:
        return await operation(*args, **kwargs)
    except MCPConnectionError as e:
        logger.warning(f"MCP operation failed: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected MCP error: {e}")
        return None
```

## POC-Specific Architecture

### Directory Structure
```
services/
├── file_context/              (existing)
│   ├── file_resolver.py      (enhanced with MCP content scoring)
│   └── exceptions.py         (add MCP-specific exceptions)
├── mcp/                      (new)
│   ├── __init__.py
│   ├── client.py            (MCP client wrapper)
│   ├── handlers.py          (File-specific MCP handlers)
│   ├── resources.py         (Resource management)
│   └── exceptions.py        (MCP-specific exceptions)
├── queries/                  (existing)
│   └── file_queries.py      (enhanced with MCP capabilities)
├── repositories/             (existing)
│   └── file_repository.py   (minimal changes, new methods)
└── api/                      (existing)
    └── main.py              (integration point for MCP-enhanced endpoints)
```

### Integration Layer Pattern
```python
# services/mcp/integration.py
class MCPFileIntegration:
    """Integration layer between Piper Morgan and MCP"""

    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository
        self.mcp_client = MCPClient()
        self.enabled = settings.ENABLE_MCP_FILE_SEARCH

    async def enhanced_search(self, query: str, session_id: str) -> List[EnhancedFileResult]:
        """Combine traditional and MCP search results"""

        # Always get traditional results
        traditional_results = await self.file_repository.search_files_by_name(session_id, query)

        # Enhance with MCP if available
        if self.enabled and await self.mcp_client.is_connected():
            mcp_results = await self.mcp_client.search_content(query)
            return self._merge_results(traditional_results, mcp_results)

        return self._convert_to_enhanced(traditional_results)
```

## Performance Considerations

### 1. Caching Strategy
**Current**: No caching for file operations
**Enhanced**: MCP results cached with TTL
```python
class MCPResultCache:
    def __init__(self, ttl_seconds: int = 300):
        self.cache = {}
        self.ttl = ttl_seconds

    async def get_or_fetch(self, key: str, fetch_func):
        if key in self.cache and not self._is_expired(key):
            return self.cache[key]

        result = await fetch_func()
        self.cache[key] = {"data": result, "timestamp": time.time()}
        return result
```

### 2. Fallback Performance
**Strategy**: Parallel execution with timeout
```python
async def search_with_fallback(self, query: str, session_id: str):
    """Search with MCP enhancement and fallback"""

    # Run traditional search and MCP search in parallel
    traditional_task = asyncio.create_task(
        self.file_repository.search_files_by_name(session_id, query)
    )

    mcp_task = asyncio.create_task(
        self.mcp_client.search_content(query)
    )

    # Wait for traditional search (always available)
    traditional_results = await traditional_task

    # Wait for MCP with timeout
    try:
        mcp_results = await asyncio.wait_for(mcp_task, timeout=2.0)
        return self._merge_results(traditional_results, mcp_results)
    except asyncio.TimeoutError:
        logger.warning("MCP search timeout, using traditional results")
        return traditional_results
```

## Testing Strategy

### 1. Test Infrastructure Compatibility
**Pattern**: Existing async test fixtures work with MCP
```python
# Existing pattern (preserved)
async def test_file_search(async_session):
    file_repo = FileRepository(async_session)
    result = await file_repo.search_files_by_name("session123", "test")
    assert len(result) == 1

# New pattern (compatible)
async def test_mcp_enhanced_search(async_session, mock_mcp_client):
    file_repo = FileRepository(async_session)
    mcp_integration = MCPFileIntegration(file_repo)
    mcp_integration.mcp_client = mock_mcp_client

    result = await mcp_integration.enhanced_search("test", "session123")
    assert len(result) >= 1  # May include MCP results
```

### 2. Isolation Testing
**Strategy**: MCP tests are isolated from core functionality
```python
# Core functionality tests (unchanged)
class TestFileRepository:
    async def test_search_files_by_name(self, async_session):
        # Test traditional search without MCP
        pass

# MCP integration tests (new, isolated)
class TestMCPFileIntegration:
    async def test_enhanced_search_with_mcp(self, async_session, mock_mcp):
        # Test MCP-enhanced search
        pass

    async def test_fallback_when_mcp_unavailable(self, async_session):
        # Test graceful degradation
        pass
```

## Risk Mitigation Architecture

### 1. Feature Flag Pattern
```python
# Environment-based feature flag
class Settings:
    ENABLE_MCP_FILE_SEARCH: bool = env.bool("ENABLE_MCP_FILE_SEARCH", default=False)
    MCP_SERVER_URL: str = env.str("MCP_SERVER_URL", default="stdio://./scripts/mcp_file_server.py")
    MCP_TIMEOUT_SECONDS: int = env.int("MCP_TIMEOUT_SECONDS", default=5)
```

### 2. Circuit Breaker Pattern
```python
class MCPCircuitBreaker:
    def __init__(self, failure_threshold: int = 5, recovery_timeout: int = 60):
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.last_failure_time = 0
        self.state = "closed"  # closed, open, half-open

    async def call(self, func, *args, **kwargs):
        if self.state == "open":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "half-open"
            else:
                raise MCPCircuitBreakerOpenError()

        try:
            result = await func(*args, **kwargs)
            self.failure_count = 0
            self.state = "closed"
            return result
        except Exception as e:
            self.failure_count += 1
            self.last_failure_time = time.time()
            if self.failure_count >= self.failure_threshold:
                self.state = "open"
            raise
```

### 3. Monitoring Integration
```python
# Performance monitoring hooks
class MCPMonitor:
    def __init__(self):
        self.metrics = {
            "connection_success_rate": 0.0,
            "average_response_time": 0.0,
            "error_rate": 0.0
        }

    async def track_operation(self, operation_name: str, func, *args, **kwargs):
        start_time = time.time()
        try:
            result = await func(*args, **kwargs)
            self._record_success(operation_name, time.time() - start_time)
            return result
        except Exception as e:
            self._record_error(operation_name, str(e))
            raise
```

## Summary

This architecture preserves all existing patterns while enabling MCP integration through:

1. **Minimal Core Changes**: Existing FileRepository and FileResolver remain largely unchanged
2. **Clear Boundaries**: MCP integration is isolated in new service layer
3. **Graceful Enhancement**: MCP augments rather than replaces existing functionality
4. **Robust Fallback**: System works normally even when MCP is unavailable
5. **Performance Safety**: Timeouts, caching, and monitoring prevent degradation
6. **Test Compatibility**: Existing test infrastructure works with MCP integration

The POC can be implemented with minimal risk to existing functionality while providing a clear path to evaluate MCP's value proposition.

---
*This integration architecture enables the file search POC while maintaining system stability and architectural integrity.*
