# ADR-010: Configuration Access Patterns

## Status
**ACCEPTED** - July 21, 2025

## Context

PM-015 Group 2 analysis revealed configuration pattern inconsistency across services that blocks 100% test success rate:

- **MCPResourceManager**: Hybrid ConfigService + environment fallback violates clean architecture principles
- **FileRepository**: Direct `os.getenv()` calls in repository layer violate domain boundaries
- **Test Evidence**: `test_mcp_resource_manager_uses_configuration_service` and `test_file_repository_uses_configuration_service` failing

While achieving 91% test success rate demonstrates architectural robustness, the mixed patterns pose long-term maintainability risks, testing inconsistencies, and developer confusion about configuration access approaches.

**Business Impact**: Configuration inconsistency affects:
- Testing reliability and isolation
- Developer onboarding and patterns adoption
- Maintenance burden across service boundaries
- Architectural pattern enforcement

**Technical Debt**: Two GitHub issues created for systematic resolution:
- Issue #39: MCPResourceManager configuration architecture standardization
- Issue #40: FileRepository environment access cleanup

## Decision

We will implement **Hybrid Configuration Access with Clean Abstractions** using layer-appropriate patterns that balance pragmatism with architectural consistency.

### Layer-Specific Rules

1. **Application/Domain Layers**: Use ConfigService exclusively
   - WorkflowService, IntentService, OrchestrationEngine
   - Business logic requiring configuration decisions
   - All user-facing feature behavior

2. **Infrastructure Layer**: ConfigService preferred, direct environment access allowed for:
   - Feature flags and toggles (`ENABLE_MCP_FILE_SEARCH`)
   - Runtime detection (e.g., MCP availability)
   - Emergency overrides and circuit breakers
   - Container orchestration variables

3. **Testing**: Mock ConfigService, not environment variables
   - Consistent test behavior across environments
   - Elimination of environment-dependent test failures
   - Cleaner test setup and isolation

### Strategic Rationale

- **Pragmatic Balance**: Avoids dependency injection ceremony while maintaining clean boundaries
- **Existing Investment**: Leverages working ConfigService infrastructure without wholesale rewrites
- **Layer Boundaries**: Different layers have different configuration responsibilities and constraints
- **Testing Reality**: Accommodates varied testing needs across architectural layers
- **Gradual Migration**: Enables incremental improvement without breaking existing functionality

## Approved Patterns with Code Examples

### PRIMARY PATTERN - Application/Domain Services

```python
# ✅ APPROVED: Service layer with ConfigService injection
class WorkflowService:
    def __init__(self, config_service: ConfigService):
        self.config = config_service

    async def process_workflow(self, workflow_type: WorkflowType):
        # Application configuration through service
        if self.config.feature_enabled("advanced_workflows"):
            return await self._process_advanced_workflow(workflow_type)
        return await self._process_basic_workflow(workflow_type)

    def get_timeout_config(self) -> int:
        return self.config.get_timeout("workflow_execution", default=300)
```

### INFRASTRUCTURE PATTERN - Repository Layer

```python
# ✅ APPROVED: Repository with ConfigService + infrastructure utilities
from services.infrastructure.config.feature_flags import FeatureFlags

class FileRepository(BaseRepository):
    def __init__(self, session: AsyncSession, config_service: ConfigService):
        super().__init__(session)
        self.config = config_service

    async def search_files_with_content(self, session_id: str, query: str, limit: int = 10):
        # Get database results first (always available)
        filename_matches = await self.search_files_by_name(session_id, query)

        # Infrastructure layer feature detection
        if FeatureFlags.is_mcp_content_search_enabled():
            try:
                return await self._enhanced_mcp_search(session_id, query, filename_matches, limit)
            except Exception as e:
                logger.warning(f"MCP search failed, falling back: {e}")

        return filename_matches[:limit]

    def _get_repository_config(self) -> dict:
        # Repository-specific configuration through ConfigService
        return {
            "cache_ttl": self.config.get_int("file_cache_ttl", 300),
            "max_results": self.config.get_int("max_file_results", 1000)
        }
```

### FEATURE FLAGS UTILITY (New Infrastructure Component)

```python
# ✅ APPROVED: Infrastructure utility for feature flags
# File: services/infrastructure/config/feature_flags.py

import os
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class FeatureFlags:
    """
    Static utility for feature flag access in infrastructure layer.

    Use this for infrastructure-level toggles, runtime detection,
    and emergency overrides. Application logic should use ConfigService.
    """

    @staticmethod
    def is_mcp_content_search_enabled() -> bool:
        """Check if MCP content search is enabled"""
        return FeatureFlags._get_boolean_flag("ENABLE_MCP_FILE_SEARCH", False)

    @staticmethod
    def is_mcp_connection_pooling_enabled() -> bool:
        """Check if MCP connection pooling is enabled"""
        return FeatureFlags._get_boolean_flag("USE_MCP_POOL", False)

    @staticmethod
    def is_debug_mode_enabled() -> bool:
        """Check if debug mode is enabled (infrastructure logging)"""
        return FeatureFlags._get_boolean_flag("DEBUG", False)

    @staticmethod
    def get_max_connection_pool_size() -> int:
        """Get infrastructure connection pool configuration"""
        return FeatureFlags._get_int_flag("MAX_CONNECTION_POOL_SIZE", 5)

    @staticmethod
    def _get_boolean_flag(flag_name: str, default: bool = False) -> bool:
        """Internal: Get boolean environment variable"""
        value = os.getenv(flag_name, str(default)).lower()
        return value in ("true", "1", "yes", "on")

    @staticmethod
    def _get_int_flag(flag_name: str, default: int) -> int:
        """Internal: Get integer environment variable"""
        try:
            return int(os.getenv(flag_name, str(default)))
        except (ValueError, TypeError):
            logger.warning(f"Invalid integer value for {flag_name}, using default {default}")
            return default
```

### ENHANCED CONFIGSERVICE PATTERN

```python
# ✅ APPROVED: Enhanced ConfigService usage
class MCPResourceManager:
    def __init__(self, client_config: Optional[Dict[str, Any]] = None,
                 config_service: Optional[ConfigService] = None):
        self.client_config = client_config or self._get_default_client_config()
        self.config_service = config_service or get_config_service()

        # Application configuration through service
        self.cache_ttl = self.config_service.get_int("mcp_cache_ttl", 300)
        self.timeout = self.config_service.get_float("mcp_timeout", 5.0)

        # Infrastructure feature detection
        self.use_connection_pool = (
            FeatureFlags.is_mcp_connection_pooling_enabled() and
            self._is_pool_infrastructure_available()
        )

    def _get_default_client_config(self) -> Dict[str, Any]:
        # Configuration service for application config
        return {
            "url": self.config_service.get_string("mcp_server_url", "stdio://./scripts/mcp_file_server.py"),
            "timeout": self.config_service.get_float("mcp_timeout", 5.0)
        }

    def _is_pool_infrastructure_available(self) -> bool:
        # Infrastructure runtime detection
        try:
            from services.infrastructure.mcp.connection_pool import MCPConnectionPool
            return True
        except ImportError:
            return False
```

## Counter-Examples (What NOT to Do)

### ❌ AVOID: Direct environment access in domain/application layers

```python
# ❌ BAD: Domain service accessing environment directly
class WorkflowService:
    async def process_workflow(self, workflow_type: WorkflowType):
        # This violates layer boundaries - domain logic shouldn't know about environment
        if os.getenv("ENABLE_ADVANCED_WORKFLOWS", "false").lower() == "true":
            return await self._process_advanced_workflow(workflow_type)
        return await self._process_basic_workflow(workflow_type)
```

### ❌ AVOID: Mixed patterns in same service

```python
# ❌ BAD: Inconsistent configuration access
class MCPResourceManager:
    def __init__(self):
        # Sometimes use ConfigService
        if CONFIG_SERVICE_AVAILABLE:
            config = get_config()
            self.timeout = config.mcp_timeout
        else:
            # Sometimes use environment - creates confusion and testing issues
            self.timeout = float(os.getenv("MCP_TIMEOUT", "5.0"))
            self.use_pool = os.getenv("USE_MCP_POOL", "false").lower() == "true"
```

### ❌ AVOID: Testing environment variables directly

```python
# ❌ BAD: Environment patching in tests creates brittle, environment-dependent tests
@pytest.fixture
def test_with_mcp_enabled():
    original = os.environ.get("ENABLE_MCP_FILE_SEARCH")
    os.environ["ENABLE_MCP_FILE_SEARCH"] = "true"
    yield
    if original is None:
        del os.environ["ENABLE_MCP_FILE_SEARCH"]
    else:
        os.environ["ENABLE_MCP_FILE_SEARCH"] = original

def test_mcp_search_enabled(test_with_mcp_enabled):
    # Test becomes environment-dependent and brittle
    result = repository.search_files_with_content("session", "query")
```

### ✅ CORRECT: Mock configuration service

```python
# ✅ GOOD: Test configuration behavior through service mocking
@pytest.fixture
def mock_config_with_mcp_enabled():
    mock_config = Mock(spec=ConfigService)
    mock_config.feature_enabled.return_value = True
    mock_config.get_int.return_value = 300
    return mock_config

def test_mcp_search_enabled(mock_config_with_mcp_enabled):
    # Clean, predictable test that focuses on behavior
    repository = FileRepository(session, mock_config_with_mcp_enabled)
    result = await repository.search_files_with_content("session", "query")
    assert len(result) > 0
```

## Migration Strategy

### Phase 1: Document and Establish Patterns (This Week - July 21-25) ✅ COMPLETE

- ✅ Create ADR-010 with approved patterns and examples - COMPLETE (July 21, 2025)
- ✅ FeatureFlags utility implementation - COMPLETE (July 22, 2025, PM-015 Group 3)
- ✅ Configuration pattern standardization - COMPLETE (July 22, 2025)
- ✅ Migration foundation established - Ready for Phase 2 implementation
- ✅ PM-015 Group 3 systematic completion - All architectural decisions documented

### Phase 2: Gradual Service Migration (Next 2 Weeks - July 28 - August 8)

**Priority 1: MCPResourceManager** (GitHub Issue #39)
- **Complexity**: Low-Medium (self-contained service)
- **Approach**:
  - Extract feature flag logic to FeatureFlags utility
  - Inject ConfigService for application configuration (timeouts, URLs)
  - Update tests to mock ConfigService instead of patching environment
  - Maintain backward compatibility during transition

**Priority 2: FileRepository** (GitHub Issue #40)
- **Complexity**: Medium-High (touches domain boundaries)
- **Approach**:
  - Extract infrastructure feature detection to FeatureFlags utility
  - Inject ConfigService for repository configuration (cache settings, limits)
  - Ensure domain purity through clean service injection
  - Update FileQueryService and other consumers as needed

### Phase 3: Enforcement and Automation (August 2025)

- Add linting rules against direct `os.getenv` in `services/domain/` and `services/orchestration/`
- Update code review checklist with configuration pattern verification
- Add configuration pattern examples to new developer documentation
- Create automated tests to verify configuration pattern adherence

## ConfigService vs Environment Variables Guidelines

### ConfigService Should Handle:

- **Application behavior configuration**: Feature toggles affecting business logic
- **User-facing features**: Settings that change user experience
- **Business logic parameters**: Timeouts, limits, thresholds for workflows
- **Integration endpoints**: API URLs, service discovery
- **Quality of service**: Performance tuning parameters

### Direct Environment Access Allowed For:

- **Infrastructure runtime detection**: Service availability, capability detection
- **Emergency overrides**: Circuit breakers, kill switches
- **Development/debugging flags**: Logging levels, debug modes
- **Container orchestration**: Port bindings, health check intervals
- **Security credentials**: When used through proper credential utilities

### Migration Checklist Template

For each service requiring configuration updates:

**Analysis Phase:**
- [ ] **Inventory current patterns**: Document all configuration access points
- [ ] **Categorize by layer**: Application logic vs infrastructure concerns
- [ ] **Identify test dependencies**: Which tests patch environment variables?
- [ ] **Map configuration types**: Feature flags vs application config vs credentials

**Implementation Phase:**
- [ ] **Create/update ConfigService injection**: Constructor parameter for application config
- [ ] **Extract feature flags**: Move infrastructure toggles to FeatureFlags utility
- [ ] **Update tests**: Replace environment patching with ConfigService mocking
- [ ] **Verify backward compatibility**: Ensure existing behavior preserved
- [ ] **Update documentation**: Service-specific configuration examples

**Validation Phase:**
- [ ] **Test isolation verified**: No environment variable dependencies in tests
- [ ] **Configuration consistency**: Service follows approved patterns
- [ ] **Performance impact**: No degradation from configuration changes
- [ ] **Developer experience**: Configuration easier to understand and modify

## Success Metrics and Validation

### Technical Metrics

- **Configuration Consistency Score**: 100% of services following approved patterns by August 2025
- **Test Reliability**: Zero environment-dependent test failures post-migration
- **Developer Velocity**: <15 minutes to implement configuration in new services
- **Production Stability**: Zero incidents related to configuration pattern issues

### Implementation Tracking

**GitHub Issues Progress:**
- **Issue #39 (MCPResourceManager)**: Ready for Phase 2 implementation (Week 2)
- **Issue #40 (FileRepository)**: Ready for Phase 2 implementation (Week 2)
- **Pattern Compliance**: ADR-010 foundation complete, ready for service migration
- **Foundation Sprint Impact**: All architectural decisions documented and approved

**Test Health Validation:**
- `test_mcp_resource_manager_uses_configuration_service`: Must pass after Issue #39
- `test_file_repository_uses_configuration_service`: Must pass after Issue #40
- PM-015 overall success rate: Target 100% (currently 91%)

### Quality Assurance

**Code Review Verification:**
- All configuration access follows layer-appropriate patterns
- No direct `os.getenv()` in application/domain layers without justification
- Tests mock ConfigService rather than patching environment
- New services include configuration pattern documentation

**Automated Enforcement:**
- Linting rules prevent regression to anti-patterns
- CI/CD pipeline validates configuration pattern compliance
- Test suite includes pattern adherence verification

### Long-term Benefits

**Developer Experience:**
- Consistent configuration patterns across all services
- Clear guidelines for feature flag vs application config decisions
- Improved test reliability and isolation
- Reduced onboarding time for configuration concepts

**Architectural Health:**
- Clean separation of concerns across layers
- Maintainable configuration management at scale
- Foundation for advanced configuration features (hot reload, environment-specific overrides)
- Technical debt elimination and prevention

## PIPER.user.md Configuration Loading Pattern

**Status:** ✅ IMPLEMENTED (October 17, 2025)
**Reference Implementation:** CalendarConfigService (CORE-MCP-MIGRATION #198)

### Pattern Description

Integration services support user-specific configuration via `config/PIPER.user.md`, a gitignored markdown file containing YAML configuration blocks. This enables per-user customization without committing credentials or personal preferences to the repository.

### Configuration Priority Order

All integrations following this pattern implement three-layer configuration:

1. **Environment variables** (highest priority) - Overrides everything
2. **PIPER.user.md** (middle priority) - User-specific defaults
3. **Hardcoded defaults** (lowest priority) - Fallback values

### Implementation Pattern

```python
# ✅ APPROVED: Integration config service with PIPER.user.md loading
# File: services/integrations/calendar/config_service.py

import os
import re
import yaml
from pathlib import Path
from typing import Any, Dict

class CalendarConfigService:
    """
    Calendar configuration service with PIPER.user.md support.

    Implements three-layer configuration priority:
    1. Environment variables (highest)
    2. PIPER.user.md calendar section (middle)
    3. Hardcoded defaults (lowest)
    """

    def _load_from_user_config(self) -> Dict[str, Any]:
        """
        Load calendar configuration from PIPER.user.md.

        Returns:
            Dict with calendar configuration, or empty dict if not found/invalid
        """
        try:
            user_config_path = Path("config/PIPER.user.md")
            if not user_config_path.exists():
                return {}

            # Read markdown file
            content = user_config_path.read_text()

            # Find Calendar Integration section by heading
            calendar_section_match = re.search(
                r"##\s+📅\s+Calendar Integration(.*?)(?=##\s+|$)",
                content,
                re.DOTALL
            )

            if not calendar_section_match:
                return {}

            section_content = calendar_section_match.group(1)

            # Extract YAML from markdown code blocks
            yaml_match = re.search(r"```yaml.*?```", section_content, re.DOTALL)
            if not yaml_match:
                return {}

            # Parse YAML content
            full_yaml_block = yaml_match.group(0)
            yaml_content = (
                full_yaml_block.replace("```yaml", "")
                              .replace("```", "")
                              .strip()
            )
            config_data = yaml.safe_load(yaml_content)

            if config_data and "calendar" in config_data:
                return config_data["calendar"]

            return {}

        except Exception as e:
            # Graceful fallback - don't crash on config errors
            print(f"Warning: Could not load calendar config from PIPER.user.md: {e}")
            return {}

    def _load_config(self) -> CalendarConfig:
        """
        Load configuration with priority: env vars > PIPER.user.md > defaults.

        Returns:
            CalendarConfig: Configuration with priority order applied
        """
        # Load from PIPER.user.md first (base layer)
        user_config = self._load_from_user_config()

        # Environment variables override user config
        return CalendarConfig(
            client_secrets_file=os.getenv(
                "GOOGLE_CLIENT_SECRETS_FILE",
                user_config.get("client_secrets_file", "credentials.json"),
            ),
            token_file=os.getenv(
                "GOOGLE_TOKEN_FILE",
                user_config.get("token_file", "token.json")
            ),
            calendar_id=os.getenv(
                "GOOGLE_CALENDAR_ID",
                user_config.get("calendar_id", "primary")
            ),
            timeout_seconds=int(
                os.getenv(
                    "GOOGLE_CALENDAR_TIMEOUT",
                    str(user_config.get("timeout_seconds", 30))
                )
            ),
            # ... additional config fields
        )
```

### PIPER.user.md Format

```markdown
## 📅 Calendar Integration

Configure Google Calendar integration with OAuth 2.0 credentials.

```yaml
calendar:
  # OAuth 2.0 Configuration
  client_secrets_file: "credentials.json"
  token_file: "token.json"

  # API Configuration
  calendar_id: "primary"
  scopes:
    - "https://www.googleapis.com/auth/calendar.readonly"

  # Timeouts & Circuit Breaker
  timeout_seconds: 30
  circuit_timeout: 300
  error_threshold: 5

  # Feature Flags
  enable_spatial_mapping: true
```

**Configuration Priority:**
1. Environment variables (highest - overrides everything)
2. PIPER.user.md (middle - overrides defaults)
3. Hardcoded defaults (lowest - fallback)
```

### Testing Pattern

```python
# ✅ APPROVED: Test PIPER.user.md loading with Path mocking
def test_loads_from_piper_user_md(tmp_path):
    """Test that config loads from PIPER.user.md when present."""
    piper_config = tmp_path / "PIPER.user.md"
    piper_config.write_text("""
## 📅 Calendar Integration

```yaml
calendar:
  client_secrets_file: "test_credentials.json"
  calendar_id: "test@calendar.com"
  timeout_seconds: 60
```
    """)

    with patch.object(Path, "exists", return_value=True):
        with patch.object(Path, "read_text", return_value=piper_config.read_text()):
            service = CalendarConfigService()
            config = service.get_config()

            # Verify values from PIPER.user.md
            assert config.client_secrets_file == "test_credentials.json"
            assert config.calendar_id == "test@calendar.com"
            assert config.timeout_seconds == 60

def test_env_vars_override_user_config(tmp_path):
    """Test that environment variables override PIPER.user.md."""
    piper_config = tmp_path / "PIPER.user.md"
    piper_config.write_text("""
```yaml
calendar:
  calendar_id: "user_config@calendar.com"
```
    """)

    os.environ["GOOGLE_CALENDAR_ID"] = "env_override@calendar.com"

    try:
        with patch.object(Path, "exists", return_value=True):
            with patch.object(Path, "read_text", return_value=piper_config.read_text()):
                service = CalendarConfigService()
                config = service.get_config()

                # Env var wins over user config
                assert config.calendar_id == "env_override@calendar.com"
    finally:
        os.environ.pop("GOOGLE_CALENDAR_ID", None)
```

### Implementation Requirements

1. **Graceful Fallback**: Config loading must never crash the application
   - Missing PIPER.user.md → Return empty dict
   - Malformed YAML → Return empty dict and log warning
   - Missing section → Return empty dict

2. **Priority Order Enforcement**: Environment variables ALWAYS override PIPER.user.md
   - Check `if ENV_VAR in os.environ` for explicit override detection
   - Use `os.getenv(ENV_VAR, user_config.get(key, default))` pattern

3. **Section Identification**: Use regex to find service-specific sections
   - Pattern: `r"##\s+📅\s+Calendar Integration(.*?)(?=##\s+|$)"`
   - Emoji markers provide visual organization in PIPER.user.md
   - DOTALL flag to capture multiline content

4. **YAML Extraction**: Parse YAML from markdown code blocks
   - Pattern: `r"```yaml.*?```"` with DOTALL flag
   - Remove markdown markers before yaml.safe_load()
   - Look for service key in parsed dict (e.g., "calendar")

### Slack Configuration Service

**Location**: `services/integrations/slack/config_service.py`

**Pattern**: Service injection with PIPER.user.md YAML parsing

**Architecture Note**: Slack uses direct spatial (ADR-039), NOT tool-based MCP

**Configuration Priority**:
1. Environment variables (highest priority)
   - `SLACK_BOT_TOKEN`
   - `SLACK_APP_TOKEN`
   - `SLACK_SIGNING_SECRET`
   - `SLACK_API_BASE_URL`
   - `SLACK_TIMEOUT_SECONDS`
   - `SLACK_MAX_RETRIES`
   - `SLACK_ENVIRONMENT`
   - `SLACK_DEFAULT_CHANNEL`
   - `SLACK_RATE_LIMIT_RPM`
   - `SLACK_BURST_LIMIT`
   - `SLACK_WEBHOOK_URL`
   - `SLACK_CLIENT_ID`
   - `SLACK_CLIENT_SECRET`
   - `SLACK_REDIRECT_URI`

2. PIPER.user.md configuration (middle priority)
   ```yaml
   slack:
     authentication:
       bot_token: "xoxb-..."
       app_token: "xapp-..."
       signing_secret: "..."

     api:
       base_url: "https://slack.com/api"
       timeout_seconds: 30
       max_retries: 3
       environment: "development"  # development|staging|production

     behavior:
       default_channel: "general"
       rate_limit_per_minute: 60
       burst_limit: 10
       webhook_url: "https://hooks.slack.com/..."

     features:
       enable_webhooks: true
       enable_socket_mode: false
       enable_spatial_mapping: true

     oauth:
       client_id: "..."
       client_secret: "..."
       redirect_uri: "..."
   ```

3. Hardcoded defaults (lowest priority)
   - Empty tokens
   - Default behavior settings
   - 60/min rate limit
   - 3 retries
   - 30s timeout

**Implementation**:
```python
class SlackConfigService:
    def _load_from_user_config(self) -> Dict[str, Any]:
        """Load Slack configuration from PIPER.user.md"""
        # Parse YAML from markdown
        # Supports two patterns: ## 💬 Slack Integration and slack:
        # Return slack: section configuration

    def _load_config(self) -> SlackConfig:
        """Load with 3-layer priority"""
        user_config = self._load_from_user_config()
        auth = user_config.get("authentication", {})
        api = user_config.get("api", {})
        behavior = user_config.get("behavior", {})
        features = user_config.get("features", {})
        oauth = user_config.get("oauth", {})

        return SlackConfig(
            bot_token=os.getenv("SLACK_BOT_TOKEN", auth.get("bot_token", "")),
            app_token=os.getenv("SLACK_APP_TOKEN", api.get("app_token", "")),
            # ... other fields with same 3-layer pattern
        )
```

**Test Coverage**: 36 comprehensive tests:
- 20 config loading tests in `tests/integration/test_slack_config_loading.py`
- 16 unit tests in `tests/services/integrations/slack/test_slack_config.py`

**Status**: ✅ Implemented (October 2025, Phase 3)

**Architectural Difference**: Unlike Calendar/Notion (tool-based MCP), Slack uses direct spatial architecture per ADR-039.

### Integrations Using This Pattern

- ✅ **Calendar** (services/integrations/calendar/config_service.py) - Reference implementation
  - **Status**: 100% complete (Phase 1, October 17, 2025)
  - **Test Coverage**: 8 comprehensive tests
  - **Pattern**: PIPER.user.md YAML parsing with 3-layer priority
- ✅ **GitHub** (services/configuration/piper_config_loader.py::load_github_config) - PiperConfigLoader
  - **MCP Integration** (October 17, 2025): GitHubIntegrationRouter now supports GitHubMCPSpatialAdapter with USE_MCP_GITHUB feature flag
  - **Status**: 95% complete (Phase 1, October 17, 2025)
  - **Test Coverage**: 16 comprehensive tests
- ✅ **Notion** (services/integrations/notion/config_service.py) - ConfigService with PIPER.user.md support
  - **Status**: 100% complete (Phase 2, October 18, 2025)
  - **Test Coverage**: 19 comprehensive tests
  - **Pattern**: Follows Calendar implementation exactly (tool-based MCP per ADR-037)
  - **Implementation**: `_load_from_user_config()` with authentication section parsing
- ✅ **Standup** (services/configuration/piper_config_loader.py::load_standup_config) - PiperConfigLoader
- ✅ **Slack** (services/integrations/slack/config_service.py) - ConfigService with PIPER.user.md support
  - **Status**: 100% complete (Phase 3, October 18, 2025)
  - **Test Coverage**: 36 comprehensive tests (20 config loading + 16 unit)
  - **Pattern**: Follows Calendar/Notion config pattern exactly
  - **Architecture**: Direct Spatial (ADR-039) - NOT tool-based MCP like Calendar/Notion
  - **Implementation**: `_load_from_user_config()` with 5 configuration sections (authentication, api, behavior, features, oauth)

### Benefits

**User Experience:**
- Per-user customization without repository commits
- Credentials and personal preferences stay local (gitignored)
- Visual organization with emoji section headers
- Self-documenting YAML format

**Testing:**
- Clean test isolation with Path mocking
- No environment variable pollution
- Comprehensive priority order validation

**Maintenance:**
- Consistent pattern across all integrations
- Reference implementation (Calendar) for new integrations
- Clear documentation in PIPER.user.md itself

## Configuration Pattern Summary

| Integration | Config Service | PIPER.user.md | Env Vars | Tests | Architecture | Status |
|-------------|----------------|---------------|----------|-------|--------------|--------|
| Calendar    | ✅ Yes         | ✅ Yes        | ✅ Yes   | 8     | Tool-based   | 100%   |
| GitHub      | ✅ Yes         | ✅ Yes        | ✅ Yes   | 16    | Delegated    | 100%   |
| Notion      | ✅ Yes         | ✅ Yes        | ✅ Yes   | 19    | Tool-based   | 100%   |
| Slack       | ✅ Yes         | ✅ Yes        | ✅ Yes   | 36    | Direct       | 100%   |

**Pattern Consistency**: All MCP integrations follow the same configuration approach:
- Service injection with dedicated ConfigService
- PIPER.user.md YAML parsing for user configuration
- Environment variable overrides for sensitive data
- Three-layer priority (env > user > defaults)
- Comprehensive test coverage for all scenarios

**Architectural Diversity**: While configuration patterns are consistent, integration architectures vary based on requirements:
- Calendar/Notion: Tool-based MCP (ADR-037)
- GitHub: Delegated MCP (ADR-038)
- Slack: Direct Spatial (ADR-039)

## Implementation History

### Phase 1: Calendar (October 17, 2025)
- Added PIPER.user.md configuration loading
- Established 3-layer priority pattern
- Created 8 comprehensive tests
- Architecture: Tool-based MCP
- **Status**: ✅ Complete

### Phase 1: GitHub (October 17, 2025)
- Verified existing PIPER.user.md support
- Wired MCP adapter following Delegated MCP Pattern (ADR-038)
- Added 16 comprehensive tests
- Architecture: Delegated MCP (primary + fallback)
- **Status**: ✅ Complete

### Phase 2: Notion (October 18, 2025)
- Added PIPER.user.md configuration loading
- Followed Calendar pattern exactly
- Created 19 comprehensive tests (most thorough config coverage)
- Architecture: Tool-based MCP
- **Status**: ✅ Complete

### Phase 3: Slack (October 18, 2025)
- Added PIPER.user.md configuration loading
- Followed Calendar/Notion pattern
- Created 20 config loading tests + 16 unit tests (36 total)
- Architecture: Direct Spatial (ADR-039) - NOT tool-based MCP
- Fixed pre-existing test isolation issue
- **Time**: 25 minutes (investigation + implementation + testing + docs)
- **Status**: ✅ Complete

**Pattern Evolution**: Configuration approach proven across 4 integrations with 3 different architectural patterns (tool-based, delegated, direct spatial).

## Related Documents

- **GitHub Issues**: #39 (MCPResourceManager), #40 (FileRepository)
- **Parent Issue**: PM-015 Test Infrastructure Isolation Fix (#29)
- **Implementation Tracking**: Foundation & Cleanup Sprint (July 21-25, 2025)
- **Architecture Patterns**: `docs/architecture/pattern-catalog.md`
- **Configuration Service**: `services/infrastructure/config/mcp_configuration.py`

---

**Decision Rationale**: This ADR provides the architectural foundation needed to eliminate configuration-related technical debt while supporting the pragmatic needs of different service layers. The hybrid approach balances architectural purity with development productivity, ensuring long-term maintainability without requiring disruptive wholesale rewrites.

**Next Steps**: Implement FeatureFlags utility, update pattern catalog, and begin Phase 2 service migrations per GitHub issues #39 and #40.
