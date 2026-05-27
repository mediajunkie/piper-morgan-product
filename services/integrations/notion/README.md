# Notion Integration

Tool-based MCP integration for Notion API following the Calendar pattern established in ADR-037.

## Status

**Activated 2026-05-13 (#304)** — search-only scope. Auth + connection + search end-to-end smoke green against live workspace.

**Write capability activated 2026-05-25 (#1080 NOTION-WRITE)** — `update_document` action handler now appends a paragraph block to the named page via `NotionMCPAdapter.append_blocks()` (wraps `blocks.children.append` with token counting; fail-graceful). Live smoke green against PM's workspace. Handler bug at `services/intent/intent_service.py:_handle_update_document_notion` fixed in the same commit (was calling `update_page(properties={})` no-op + reporting success; Pattern-073 Instance 12). See "Write capability" section below for the user-facing flow.

**Phase 2 Complete** ✅ (October 18, 2025)
- Configuration loading: ✅ Complete
- Test coverage: ✅ 19 comprehensive tests
- Pattern consistency: ✅ Matches Calendar exactly
- Documentation: ✅ Complete

## Activation: how to provision a token

The integration uses **macOS Keychain** as the primary credential store (worktree-friendly; survives the worktree-isolation gap that `.env` files have). Env-var fallback is supported for backward compatibility.

### One-time PM steps

1. Go to https://www.notion.so/my-integrations → "New integration"
2. Name it (e.g. "Piper Alpha")
3. Capabilities: **Read content**, **Read user information**, **Update content**, **Insert content**. (Read-only is sufficient for `search_documents`; the two write capabilities are required for `update_document` per #1080. PMs who don't need chat-driven writes can stay read-only.)
4. Save → copy the **Internal Integration Token** (starts with `ntn_*` or `secret_*`)
5. Store via macOS keychain:
   ```
   security add-generic-password -s piper-morgan -a notion_api_key -w 'YOUR_TOKEN' -U
   ```
6. Open each Notion page/database you want Piper to search → ⋯ menu → **Connections** → add your integration. (Sub-pages inherit.)

### Verify

```bash
./venv/bin/python -c "from config.notion_config import NotionConfig; print(NotionConfig.validate_config())"
```
Should print `True`. If `False`, the keychain entry is missing or malformed.

### Fallback paths (in resolution order)

1. `NOTION_API_KEY` env var (legacy + dev convention)
2. `KeychainService().get_api_key("notion")` (keychain entry: service `piper-morgan`, account `notion_api_key`)

### Write capability — `update_document` (#1080, activated 2026-05-25)

The activation ships both **search** and **append-paragraph write**:

| Action | Surface | Required Notion capability |
|---|---|---|
| `search_documents` / `find_documents` / `search_notion` | Find a page by name; return matches with URLs | Read content, Read user information |
| `update_document` / `edit_document` / `update_document_query` | Append a paragraph block to the bottom of a named page | Update content, Insert content (+ the read caps above) |

**User-facing flow** (chat-driven):

1. User: *"Update the [page-name] doc with: [content paragraph]"*
2. Handler does a fuzzy `search_notion()` for the page by name
3. On a single match → builds a Notion paragraph block from the content + calls `NotionIntegrationRouter.append_blocks(page_id, [block])`
4. On success → *"✓ Appended to [page-name] / Added paragraph: ..."* with link
5. On failure (append returns None) → honest fallback message naming the actual failure mode + link

**Ambiguity handling**: 0 matches → clarification request; multiple matches → list with "Which one?"; 1 match → proceed.

**Important**: `update_document` only **appends** a new paragraph block at the bottom — it doesn't edit existing content or replace anything. Notion's data model treats a page as `properties + child content blocks`; "update" semantics in the chat are append-shape until/unless a richer edit-surface is filed as a follow-up issue.

### Sibling activations

Slack-Notion cross-reference verification is filed as **#1081 NOTION-SLACK-XREF** — also demand-gated; live smoke pending PM bandwidth.

Test cleanup landed 2026-05-24: **#1082 NOTION-TEST-REWRITE** rewrote 9 stale aiohttp-architecture tests against the notion-client library (17 active tests passing post-rewrite).

## Architecture

**Pattern**: Tool-based MCP (ADR-037)
**Configuration**: PIPER.user.md with 3-layer priority (ADR-010)
**Router**: NotionIntegrationRouter with spatial delegation

### Components

```
NotionIntegrationRouter
├── NotionMCPAdapter (Primary)
│   └── Tool-based MCP with 22 complete operations
├── NotionConfigService
│   └── 3-layer priority configuration loading
└── Feature Flag: USE_SPATIAL_NOTION (defaults true)
```

**Files**:
- **Config Service**: `services/integrations/notion/config_service.py`
- **MCP Adapter**: `services/integrations/mcp/notion_adapter.py` (29KB, 22 methods)
- **Router**: `services/integrations/notion/notion_integration_router.py`

## Configuration

### Quick Start

**Option 1: Environment Variable** (recommended for sensitive data):
```bash
export NOTION_API_KEY="secret_your_integration_token"
export NOTION_WORKSPACE_ID="workspace_id"  # Optional
```

**Option 2: PIPER.user.md** (user-specific config):
```yaml
notion:
  authentication:
    api_key: "secret_your_integration_token"
    workspace_id: "optional_workspace_id"

  # Optional API configuration
  api_base_url: "https://api.notion.com/v1"
  timeout_seconds: 30
  max_retries: 3
  requests_per_minute: 30
```

**Option 3: Defaults** (no authentication):
- Integration initializes with empty credentials
- Operations requiring authentication will fail gracefully

### Configuration Priority

```
1. Environment Variables (HIGHEST)
   ↓ overrides
2. PIPER.user.md (MIDDLE)
   ↓ overrides
3. Hardcoded Defaults (LOWEST)
```

### Environment Variables

**Authentication**:
- `NOTION_API_KEY` - Notion integration token (required for API operations)
- `NOTION_WORKSPACE_ID` - Workspace ID (optional)

**API Configuration**:
- `NOTION_API_BASE_URL` - API base URL (default: `https://api.notion.com/v1`)
- `NOTION_TIMEOUT_SECONDS` - Request timeout (default: 30)
- `NOTION_MAX_RETRIES` - Retry attempts (default: 3)
- `NOTION_REQUESTS_PER_MINUTE` - Rate limit (default: 30)
- `NOTION_ENVIRONMENT` - Environment (development/staging/production)

### PIPER.user.md Format

See `config/PIPER.user.md` for the complete configuration template with all available options.

## Usage

### Basic Usage

```python
from services.integrations.notion.notion_integration_router import NotionIntegrationRouter

# Initialize with automatic configuration loading
router = NotionIntegrationRouter()

# Use Notion operations
await router.connect()  # Connect to Notion API
database = await router.get_database("database_id")
pages = await router.query_database("database_id", filter={...})
```

### Available Operations

**Connection** (3 methods):
- `connect(integration_token: Optional[str])` - Connect to Notion API
- `test_connection()` - Test API connectivity
- `is_configured()` - Check if configured

**Database Operations** (4 methods):
- `fetch_databases(page_size: int)` - Fetch all databases
- `list_databases(page_size: int)` - List databases (alias)
- `get_database(database_id: str)` - Get specific database
- `query_database(database_id, filter, sorts, page_size)` - Query database

**Page Operations** (4 methods):
- `get_page(page_id: str)` - Get page content
- `get_page_blocks(page_id: str, page_size: int)` - Get page blocks
- `create_page(parent_id, properties, content)` - Create new page
- `update_page(page_id, properties)` - Update page properties

**Database Item Operations** (1 method):
- `create_database_item(database_id, properties)` - Create item in database

**Search & Users** (3 methods):
- `search_notion(query, filter_type, page_size)` - Search workspace
- `get_user(user_id)` - Get user info
- `list_users()` - List workspace users

**Workspace** (1 method):
- `get_workspace_info()` - Get workspace information

**Spatial Intelligence** (4 methods):
- `map_to_position(external_id, context)` - Map Notion ID to spatial position
- `map_from_position(position)` - Reverse mapping
- `store_mapping(external_id, position)` - Store ID mapping
- `get_context(external_id)` - Get spatial context

**Total**: 22 complete operations

## Testing

### Run Configuration Tests

```bash
# All Notion config loading tests
pytest tests/integration/test_notion_config_loading.py -v

# Specific test categories
pytest tests/integration/test_notion_config_loading.py::TestNotionConfigLoading -v
pytest tests/integration/test_notion_config_loading.py::TestNotionConfigServiceBasics -v
```

### Test Coverage

**19 comprehensive tests** covering:
- **PIPER.user.md loading** (5 tests): File parsing, missing files, malformed YAML
- **Priority system** (3 tests): Env override, user config, defaults
- **Authentication** (2 tests): Auth section parsing, missing auth section
- **API configuration** (4 tests): API settings, environment, rate limits
- **Service basics** (3 tests): Initialization, caching, validation
- **Edge cases** (2 tests): Empty files, partial configuration

**All tests passing** ✅ (19/19)

### Example Test

```python
def test_env_vars_override_user_config(tmp_path):
    """Test that environment variables override PIPER.user.md."""
    # Setup PIPER.user.md with user config
    piper_config = tmp_path / "PIPER.user.md"
    piper_config.write_text("""
## 📝 Notion Integration

```yaml
notion:
  authentication:
    api_key: "user_config_key"
  timeout_seconds: 30
```
    """)

    # Set environment variables (should override)
    os.environ["NOTION_API_KEY"] = "env_override_key"

    service = NotionConfigService()
    config = service.get_config()

    # Verify priority: env > user > defaults
    assert config.api_key == "env_override_key"  # From env
    assert config.timeout_seconds == 30  # From user config
```

## Implementation Details

### Pattern Consistency

Notion configuration follows **Calendar pattern exactly**:
- ✅ Same 3-layer priority system
- ✅ Same YAML parsing approach
- ✅ Same error handling (graceful fallback)
- ✅ Same testing patterns
- ✅ Same configuration structure

### Configuration Service

```python
class NotionConfigService:
    def _load_from_user_config(self) -> Dict[str, Any]:
        """Load Notion config from PIPER.user.md"""
        # Parse YAML from markdown file
        # Extract notion: section
        # Return configuration dict

    def _load_config(self) -> NotionConfig:
        """Load with 3-layer priority: env > user > defaults"""
        user_config = self._load_from_user_config()
        auth = user_config.get("authentication", {})

        return NotionConfig(
            api_key=os.getenv("NOTION_API_KEY", auth.get("api_key", "")),
            workspace_id=os.getenv("NOTION_WORKSPACE_ID", auth.get("workspace_id", "")),
            # ... other fields with same pattern
        )
```

### MCP Adapter

```python
class NotionMCPAdapter(BaseSpatialAdapter):
    """Tool-based MCP adapter for Notion API"""

    def __init__(self, config_service: Optional[NotionConfigService] = None):
        super().__init__("notion_mcp")
        self.config_service = config_service or NotionConfigService()
        # Service injection pattern
```

### Router

```python
class NotionIntegrationRouter:
    """Router with spatial delegation"""

    def __init__(self, config_service: Optional[NotionConfigService] = None):
        # Use spatial if enabled (defaults true)
        self.use_spatial = FeatureFlags.should_use_spatial_notion()

        if self.use_spatial:
            self.spatial_notion = NotionMCPAdapter(config_service)
```

## Related ADRs

- **ADR-010**: Configuration Patterns (PIPER.user.md loading)
- **ADR-037**: Tool-based MCP Standardization
- **ADR-038**: Spatial Intelligence Integration Patterns

## Migration History

### Phase -1: Discovery (October 16, 2025)
- Found existing tool-based NotionMCPAdapter (22 methods)
- Discovered router already wired to MCP adapter
- Identified: Already 95% complete (not server-based!)

### Phase 2 Step 0: Investigation (October 18, 2025, 7:05-7:15 AM)
- Documented current state (already tool-based)
- Inventoried 22 complete operations
- Assessed migration complexity: LOW (completion, not conversion)
- **Time**: 17 minutes

### Phase 2 Step 1: Configuration Loading (October 18, 2025, 7:35-7:55 AM)
- Added `_load_from_user_config()` to NotionConfigService
- Implemented 3-layer priority (env > user > defaults)
- Added authentication section to PIPER.user.md
- Verified configuration loading works
- **Time**: 20 minutes

### Phase 2 Step 2: Test Suite (October 18, 2025, 7:59-8:20 AM)
- Created 19 comprehensive tests
- All tests passing (19/19 ✅)
- Exceeded Calendar's 8-test baseline
- **Time**: 21 minutes

### Phase 2 Step 3: Documentation (October 18, 2025, 8:08 AM)
- Updated ADR-010 with Notion configuration
- Created this README
- **Time**: In progress

### Total Phase 2 Time
- **Estimated**: 3-4 hours
- **Actual**: ~1 hour (investigation + implementation + testing)
- **Under budget**: 67% time savings (completion vs conversion)

## Comparison: Phase 1 vs Phase 2

| Aspect | Calendar (Phase 1) | Notion (Phase 2) |
|--------|-------------------|------------------|
| **Architecture** | Tool-based MCP | Tool-based MCP ✅ |
| **Task Type** | Completion | Completion ✅ |
| **Config Loading** | Added | Added ✅ |
| **Test Count** | 8 tests | 19 tests (138% more) |
| **Time Estimate** | 2 hours | 2 hours |
| **Actual Time** | 2 hours | 1 hour (50% faster) |
| **Pattern** | Reference | Follows Calendar |

**Key Insight**: Notion Phase 2 was identical to Calendar Phase 1 (both completion tasks, not conversions). Following the established pattern enabled faster execution with better test coverage.

## Troubleshooting

### Configuration Not Loading

**Problem**: Notion operations fail with authentication errors

**Solution**:
1. Verify `NOTION_API_KEY` environment variable is set
2. Or check `config/PIPER.user.md` has `notion.authentication.api_key`
3. Run test: `python -c "from services.integrations.notion.config_service import NotionConfigService; print(NotionConfigService().get_config().api_key)"`

### PIPER.user.md Not Found

**Problem**: Warning about missing PIPER.user.md

**Solution**: This is normal graceful fallback behavior. Config will use environment variables or defaults. No action needed unless you want user-specific config.

### Test Failures

**Problem**: Configuration tests failing

**Solution**:
```bash
# Run with verbose output
pytest tests/integration/test_notion_config_loading.py -vvs

# Check for environment variable pollution
env | grep NOTION
```

## Future Work

- [ ] Performance benchmarking (MCP vs direct API)
- [ ] Connection pooling optimization
- [ ] Circuit breaker tuning
- [ ] Additional operations as needed

## Contributing

When adding new Notion operations:
1. Add method to `NotionMCPAdapter`
2. Wire to `NotionIntegrationRouter`
3. Add tests to cover new operation
4. Update this README's operation list

## References

- **Calendar Implementation**: `services/integrations/calendar/` (reference pattern)
- **GitHub Implementation**: `services/integrations/github/` (delegation pattern)
- **Notion Investigation Report**: `dev/2025/10/18/notion-investigation-report.md`
- **Test Suite**: `tests/integration/test_notion_config_loading.py`

---

**Status**: ✅ Ready for production use
**Last Updated**: October 18, 2025
**Pattern**: CORE-MCP-MIGRATION #198 Phase 2
