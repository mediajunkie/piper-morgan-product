# Pattern-018: Configuration Access Pattern

## Status

**Proven**

## Context

Modern applications require configuration management that respects architectural boundaries while providing practical access to configuration data across different layers. Without consistent configuration access patterns, applications suffer from tight coupling, difficult testing, and violations of clean architecture principles. The Configuration Access Pattern addresses:

- Maintaining clean architecture boundaries while accessing configuration
- Providing layer-appropriate configuration access mechanisms
- Supporting both application-level and infrastructure-level configuration needs
- Enabling comprehensive testing without environment dependency
- Ensuring consistent configuration patterns across the application
- Supporting feature flags and runtime configuration changes

## Pattern Description

The Configuration Access Pattern provides layer-appropriate configuration access that maintains architectural boundaries through dependency injection of configuration services, utility classes for infrastructure toggles, and comprehensive testing patterns. The pattern establishes clear rules for different architectural layers while supporting practical infrastructure needs.

## Implementation

### Structure

```python
# Configuration access framework
class ConfigurationAccessManager:
    def __init__(self):
        self.config_service = ConfigService()
        self.feature_flags = FeatureFlags()

    def get_application_config(self, key: str, default: Any = None) -> Any:
        """Get application-level configuration through service"""
        pass

    def get_infrastructure_config(self, feature: str) -> bool:
        """Get infrastructure-level configuration through feature flags"""
        pass

    def create_layer_config(self, layer_type: str) -> LayerConfig:
        """Create layer-appropriate configuration interface"""
        pass
```

### Example (Application/Domain Layer Configuration)

```python
from services.config.config_service import ConfigService
from typing import Optional
import structlog

logger = structlog.get_logger()

class WorkflowService:
    """Application service with proper configuration access"""

    def __init__(self, config_service: ConfigService):
        """Inject ConfigService for application configuration"""
        self.config = config_service
        self.logger = logger.bind(service="workflow_service")

    async def process_workflow(self, workflow_type: WorkflowType) -> WorkflowResult:
        """Process workflow with configuration-driven behavior"""

        # Application configuration through service
        if self.config.feature_enabled("advanced_workflows"):
            self.logger.info(
                "Processing advanced workflow",
                workflow_type=workflow_type,
                feature="advanced_workflows"
            )
            return await self._process_advanced_workflow(workflow_type)

        self.logger.info(
            "Processing basic workflow",
            workflow_type=workflow_type
        )
        return await self._process_basic_workflow(workflow_type)

    def get_timeout_config(self) -> int:
        """Get workflow timeout from configuration"""
        timeout = self.config.get_timeout("workflow_execution", default=300)
        self.logger.debug("Retrieved workflow timeout", timeout=timeout)
        return timeout

    def get_retry_config(self) -> Dict[str, int]:
        """Get retry configuration for workflow operations"""
        return {
            "max_attempts": self.config.get_int("workflow_max_retries", 3),
            "base_delay": self.config.get_int("workflow_retry_delay", 1),
            "max_delay": self.config.get_int("workflow_max_retry_delay", 60)
        }

    def is_feature_enabled(self, feature_name: str) -> bool:
        """Check if application feature is enabled"""
        enabled = self.config.feature_enabled(feature_name)
        self.logger.debug(
            "Feature flag checked",
            feature=feature_name,
            enabled=enabled
        )
        return enabled

class OrchestrationService:
    """Domain service with configuration-driven orchestration"""

    def __init__(self, config_service: ConfigService):
        self.config = config_service
        self.logger = logger.bind(service="orchestration_service")

    async def orchestrate_workflow(self, workflow_data: Dict[str, Any]) -> OrchestrationResult:
        """Orchestrate workflow with configuration-based routing"""

        # Get orchestration configuration
        parallel_enabled = self.config.feature_enabled("parallel_orchestration")
        max_concurrent = self.config.get_int("max_concurrent_workflows", 5)

        if parallel_enabled and len(workflow_data.get('steps', [])) > 1:
            return await self._orchestrate_parallel(
                workflow_data,
                max_concurrent=max_concurrent
            )

        return await self._orchestrate_sequential(workflow_data)
```

### Example (Infrastructure Layer Configuration)

```python
from services.infrastructure.config.feature_flags import FeatureFlags
from services.config.config_service import ConfigService

class FileRepository(BaseRepository):
    """Infrastructure repository with dual configuration access"""

    def __init__(self, session: AsyncSession, config_service: ConfigService):
        super().__init__(session)
        self.config = config_service
        self.logger = logger.bind(repository="file_repository")

    async def search_files_with_content(self, session_id: str, query: str) -> List[FileResult]:
        """Search files with configuration-driven enhancement"""

        # Infrastructure feature detection through utility
        if FeatureFlags.is_mcp_content_search_enabled():
            self.logger.info(
                "Using enhanced MCP search",
                session_id=session_id,
                feature="mcp_content_search"
            )
            return await self._enhanced_mcp_search(session_id, query)

        self.logger.info(
            "Using standard search",
            session_id=session_id
        )
        return await self._standard_search(session_id, query)

    def _get_cache_config(self) -> Dict[str, int]:
        """Get caching configuration through service"""
        return {
            "ttl": self.config.get_int("file_cache_ttl", 300),
            "max_size": self.config.get_int("file_cache_max_size", 1000),
            "cleanup_interval": self.config.get_int("cache_cleanup_interval", 60)
        }

    def _get_search_config(self) -> Dict[str, Any]:
        """Get search configuration with infrastructure toggles"""
        return {
            "max_results": self.config.get_int("search_max_results", 100),
            "timeout": self.config.get_int("search_timeout", 30),
            "use_fuzzy_matching": self.config.feature_enabled("fuzzy_search"),
            "use_mcp_enhancement": FeatureFlags.is_mcp_content_search_enabled()
        }

class MCPResourceManager:
    """Infrastructure manager with proper configuration patterns"""

    def __init__(self, config_service: ConfigService):
        self.config = config_service
        self.logger = logger.bind(manager="mcp_resource")

    async def get_connection_pool(self) -> ConnectionPool:
        """Get connection pool with configuration-driven behavior"""

        # Infrastructure toggle for connection pooling
        if FeatureFlags.is_mcp_connection_pooling_enabled():
            pool_size = self.config.get_int("mcp_pool_size", 10)
            self.logger.info(
                "Creating MCP connection pool",
                pool_size=pool_size
            )
            return await self._create_connection_pool(pool_size)

        self.logger.info("Using direct MCP connections")
        return await self._create_direct_connections()
```

### Example (Test Configuration Patterns)

```python
import pytest
from unittest.mock import Mock, patch
from services.config.config_service import ConfigService

@pytest.fixture
def mock_config_with_features_enabled():
    """Mock ConfigService with features enabled"""
    mock_config = Mock(spec=ConfigService)
    mock_config.feature_enabled.return_value = True
    mock_config.get_int.return_value = 300
    mock_config.get_timeout.return_value = 60
    return mock_config

@pytest.fixture
def mock_config_with_features_disabled():
    """Mock ConfigService with features disabled"""
    mock_config = Mock(spec=ConfigService)
    mock_config.feature_enabled.return_value = False
    mock_config.get_int.return_value = 100
    mock_config.get_timeout.return_value = 30
    return mock_config

def test_advanced_workflow_behavior(mock_config_with_features_enabled):
    """Test workflow service with advanced features enabled"""
    service = WorkflowService(mock_config_with_features_enabled)

    # Test focuses on behavior, not environment state
    result = await service.process_workflow(WorkflowType.ANALYSIS)

    assert result.uses_advanced_features == True
    mock_config_with_features_enabled.feature_enabled.assert_called_with("advanced_workflows")

def test_basic_workflow_behavior(mock_config_with_features_disabled):
    """Test workflow service with features disabled"""
    service = WorkflowService(mock_config_with_features_disabled)

    result = await service.process_workflow(WorkflowType.ANALYSIS)

    assert result.uses_advanced_features == False
    mock_config_with_features_disabled.feature_enabled.assert_called_with("advanced_workflows")

@pytest.fixture
def config_service_with_custom_values():
    """Create ConfigService with specific test values"""
    mock_config = Mock(spec=ConfigService)
    mock_config.get_int.side_effect = lambda key, default: {
        "workflow_max_retries": 5,
        "workflow_retry_delay": 2,
        "max_concurrent_workflows": 10
    }.get(key, default)
    mock_config.feature_enabled.side_effect = lambda feature: {
        "parallel_orchestration": True,
        "fuzzy_search": False
    }.get(feature, False)
    return mock_config

def test_orchestration_with_custom_config(config_service_with_custom_values):
    """Test orchestration with specific configuration values"""
    service = OrchestrationService(config_service_with_custom_values)

    # Test configuration-driven behavior
    workflow_data = {"steps": ["step1", "step2", "step3"]}
    result = await service.orchestrate_workflow(workflow_data)

    assert result.execution_mode == "parallel"
    assert result.max_concurrent == 10
```

## Usage Guidelines

### Layer-Specific Configuration Rules

- **Application/Domain Layer**: Use ConfigService exclusively through dependency injection
- **Infrastructure Layer**: ConfigService for application behavior, FeatureFlags utility for infrastructure toggles
- **Testing Layer**: Mock ConfigService, avoid environment variable patching
- **Integration Layer**: Utility classes for environment-specific configuration access

### Configuration Categories

- **ConfigService**: Application behavior, user-facing features, business logic parameters, timeouts, and retry settings
- **FeatureFlags**: Infrastructure toggles, runtime detection, emergency overrides, and system-level features
- **Environment Direct**: Container orchestration, security credentials (accessed through dedicated utilities)
- **Test Configuration**: Mock services with predictable behavior for comprehensive testing

### Best Practices for Configuration Access

- **Dependency Injection**: Always inject configuration services rather than accessing globally
- **Layer Boundaries**: Respect architectural boundaries when accessing configuration
- **Default Values**: Always provide sensible defaults for configuration parameters
- **Logging**: Log configuration access for debugging and observability
- **Testing**: Use mock configuration services for predictable test behavior

### Anti-Patterns to Avoid

- **Direct Environment Access**: Accessing environment variables directly in domain/application layers
- **Mixed Configuration Patterns**: Using different configuration access methods within the same class
- **Environment Patching in Tests**: Modifying environment variables in test fixtures
- **Global Configuration Access**: Using global configuration objects instead of dependency injection
- **Hardcoded Configuration**: Embedding configuration values directly in business logic
- **Inconsistent Configuration Keys**: Using different naming conventions for similar configuration items

## Related Patterns

- [Pattern-002: Service Pattern](pattern-002-service.md) - Service-level configuration management
- [Pattern-008: DDD Service Layer](pattern-008-ddd-service-layer.md) - Domain service configuration access
- [Pattern-003: Factory Pattern](pattern-003-factory.md) - Configuration-driven object creation
- [Pattern-005: Transaction Management](pattern-005-transaction-management.md) - Configuration for transaction behavior

## Migration Notes (for consolidation from legacy systems)

- **From `pattern-catalog.md`**: Section 18 "Configuration Access Pattern" - comprehensive layer-specific rules and implementation examples
- **From `PATTERN-INDEX.md`**: No direct equivalent - this is an infrastructure pattern
- **From ADR-010**: Configuration Access Patterns architectural decision
- **From codebase**: Implementation examples in `services/infrastructure/config/feature_flags.py`
- **Consolidation Strategy**: Expanded pattern-catalog.md content with comprehensive testing patterns and layer-specific guidelines

## Quality Assurance Checklist

- [x] Pattern description is clear and concise
- [x] Context explains problem and applicability
- [x] Implementation examples are provided and correct
- [x] Usage guidelines are comprehensive
- [x] Related patterns are linked
- [x] All information from source catalog is preserved
- [x] Follows ADR-style numbering and naming conventions

## Agent Coordination Notes

- **Agent A (Code)**: Responsible for configuration service implementation and feature flag utilities
- **Agent B (Cursor)**: Responsible for layer-appropriate access pattern documentation and testing guidelines
- **Integration Points**: Configuration services, feature flag utilities, and dependency injection frameworks

## References

- Original catalog: `docs/architecture/pattern-catalog.md#18-configuration-access-pattern`
- ADR-010: Configuration Access Patterns
- Feature flags implementation: `services/infrastructure/config/feature_flags.py`
- Configuration service: `services/config/config_service.py`
- Migration issues: GitHub Issues #39 (MCPResourceManager), #40 (FileRepository)

_Last updated: September 15, 2025_
