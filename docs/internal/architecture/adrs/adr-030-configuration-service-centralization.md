# ADR-030: Configuration Service Centralization

## Status

Accepted (September 12, 2025)

## Context

During Step 4 of comprehensive DDD refactoring, configuration management was scattered and problematic:

### Configuration Issues Identified

- **Hardcoded Values**: Port numbers and URLs hardcoded in multiple locations

  - `web/app.py`: Hardcoded backend URLs and port references
  - `start-piper.sh`: Hardcoded port overrides in deployment script
  - Multiple service files with embedded configuration values

- **Deployment Complexity**: Environment-specific configuration required manual script modifications
- **Maintenance Overhead**: Configuration changes required updates in multiple files
- **Testing Difficulties**: Hard to test with different port configurations
- **Production Risk**: Hardcoded values created deployment reliability issues

### Specific Violations Found

```bash
# Before: Hardcoded values in multiple locations
web/app.py: "http://localhost:8001"
start-piper.sh: "export WEB_PORT=8081"
```

## Decision

Implement centralized configuration management through dedicated domain service:

### PortConfigurationService Implementation

**Location**: `services/configuration/port_configuration_service.py`

**Key Features**:

- Environment-aware configuration loading (development/staging/production)
- Dynamic URL generation based on environment
- Centralized port management for all services
- Integration with existing PiperConfigLoader

### Configuration Architecture

```python
class PortConfigurationService:
    def __init__(self):
        self.environment = os.getenv('ENVIRONMENT', 'development')
        self._load_configuration()

    def get_service_urls(self) -> Dict[str, str]:
        return {
            'backend': f'http://127.0.0.1:{self._backend_port}',
            'web': f'http://127.0.0.1:{self._web_port}',
            'api_base': f'http://127.0.0.1:{self._backend_port}'
        }
```

### Integration Points

- **Web Layer**: Uses PortConfigurationService for backend URL generation
- **Deployment Scripts**: Uses environment variables instead of hardcoded overrides
- **Development**: Automatic configuration loading from user config
- **Production**: Environment-based configuration selection

## Consequences

### Positive

- **Deployment Simplicity**: Environment variables control all configuration
- **Maintainability**: Single source of truth for port/URL configuration
- **Testability**: Easy to test with different configurations
- **Environment Flexibility**: Supports development/staging/production seamlessly
- **Reduced Errors**: No more hardcoded value inconsistencies

### Negative

- **Additional Abstraction**: One more service to understand
- **Initialization Dependency**: Services must properly initialize configuration service

### Migration Results

- **Zero Hardcoded Values**: All hardcoded ports/URLs eliminated from active code
- **Deployment Ready**: `start-piper.sh` modernized with environment variables
- **Backward Compatibility**: Existing functionality preserved

## Implementation Evidence

### Validation Results (September 12, 2025)

- ✅ PortConfigurationService created and functional
- ✅ Dynamic URL generation working: backend http://127.0.0.1:8001, web http://127.0.0.1:8081
- ✅ Environment-based configuration operational (development mode)
- ✅ Hardcoded values eliminated (only found in backup directories)
- ✅ End-to-end workflow functional (0s response time)

### Configuration Service Usage

```python
# Application layer usage
config = PortConfigurationService()
service_urls = config.get_service_urls()
backend_port = config.get_port_for_service("backend")
```

### Environment Configuration

```bash
# Development (default)
ENVIRONMENT=development

# Production deployment
ENVIRONMENT=production
```

## Future Considerations

- **Additional Configuration**: Service can be extended for other configuration needs
- **Configuration Validation**: Could add configuration validation and health checks
- **Secret Management**: Foundation for secure configuration management
- **Monitoring Integration**: Configuration service provides natural monitoring points

## References

- Issue #168: STANDUP-REGRESS DDD Refactoring (Step 4)
- Implementation: September 12, 2025
- Validation: Perfect configuration centralization validation
- Related: ADR-029 Domain Service Mediation Architecture
