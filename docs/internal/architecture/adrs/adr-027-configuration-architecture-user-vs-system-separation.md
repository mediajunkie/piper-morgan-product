# ADR-027: Configuration Architecture - User vs System Separation

**Status**: Accepted
**Date**: 2025-08-30
**Author**: Claude Code Agent
**Context**: Configuration refactoring mission - Phase 2 design

## Context

Multi-user adoption of Piper Morgan is blocked by hardcoded Notion workspace values scattered throughout the codebase. Phase 1 audit identified 5 hardcoded Notion IDs across 5 files, with 4 HIGH-risk values that completely prevent other developers from using ADR publishing, integration tests, and debugging tools.

**Strategic Context**:

- Current system: Environment variables + hardcoded values
- User pain: Cannot run tests or publish ADRs without modifying code
- Requirement: Enable seamless multi-user adoption with user-specific configurations

## Strategic Decisions Resolved

This ADR documents 5 critical strategic decisions made for the configuration architecture:

### Decision 1: Configuration File Strategy

**Extend PIPER.user.md vs separate configuration files**

**Chosen**: Extend existing PIPER.user.md with YAML section
**Rationale**:

- Maintains consistency with existing user configuration approach
- Single file for all user customizations (context + technical config)
- YAML section allows structured data within markdown document
- Gitignored by default - maintains privacy

**Alternative Rejected**: Separate notion_config.yaml file

- Would fragment user configuration across multiple files
- Requires additional gitignore management
- Less discoverable than unified approach

### Decision 2: Required vs Optional Field Categorization

**Categorization of configuration fields by criticality**

**Chosen**: Required (ADR database, default parent) vs Optional (development, validation)\*\*
**Rationale**:

- Based on Phase 1 audit findings and usage patterns
- Required fields block core functionality (ADR publishing, content publishing)
- Optional fields enhance but don't block basic usage
- Fail-fast validation ensures users configure critical functionality

**Implementation**:

- Required: `notion.adrs.database_id`, `notion.publishing.default_parent`
- Optional: `notion.development.*`, `notion.validation.*`, `notion.behavior.*`

### Decision 3: Error Handling Approach

**Fail-fast vs graceful degradation**

**Chosen**: Fail-fast error handling with actionable guidance
**Rationale**:

- Prevents "verification theater" - users know immediately if configuration is wrong
- Each error includes specific resolution steps
- Clear field path identification for targeted fixes
- Prevents partial functionality that leads to confusion

**Implementation**: ConfigurationError class with resolution steps array

### Decision 4: Migration Strategy

**Manual vs automated migration from hardcoded values**

**Chosen**: Manual migration with comprehensive documentation
**Rationale**:

- 5 hardcoded values across 5 files - manageable manually
- Allows users to understand their workspace structure
- Automated migration would require API discovery that may fail
- Manual approach enables customization during migration

**Implementation**: Migration guide with explicit value mappings from audit findings

### Decision 5: Validation Tiers

**Validation complexity levels**

**Chosen**: Tiered validation (basic → enhanced → full)
**Rationale**:

- MVP: Basic validation (format + environment) for immediate feedback
- Enhanced: API connectivity testing for production readiness
- Full: Permission verification for comprehensive validation
- Users can choose validation level based on their needs and environment

**Implementation**:

- Basic: Format validation + environment variable check
- Enhanced: Basic + API connectivity test
- Full: Enhanced + permission checking on configured resources

## Configuration Schema Design

### YAML Structure (Extension to PIPER.user.md)

```yaml
notion:
  # REQUIRED: Core functionality
  publishing:
    default_parent: "" # Maps: debug_parent.py:19
  adrs:
    database_id: "" # Maps: fields.py:12 + adr.py:12

  # OPTIONAL: Development & testing
  development:
    test_parent: "" # Maps: test_publish_command.py:18
    debug_parent: "" # Maps: debug_parent.py:19 (duplicate usage)
    mock_mode: false

  # OPTIONAL: Validation & behavior
  validation:
    level: "basic" # basic|enhanced|full
    connectivity_check: true
  behavior:
    confirm_overwrites: true
```

### Class Architecture

- **NotionUserConfig**: Main configuration loader with fail-fast validation
- **ConfigurationError**: Structured errors with resolution steps
- **ValidationResult**: Comprehensive validation results with multiple levels
- **ValidationLevel**: Enum for tiered validation approach

## Consequences

### Positive

- **Multi-user enablement**: Any developer can configure their workspace
- **Fail-fast feedback**: Users know immediately if configuration is wrong
- **Comprehensive coverage**: All 5 audit findings mapped to configuration fields
- **Scalable validation**: Tiered approach supports different use cases
- **Actionable errors**: Every error includes specific resolution steps
- **Consistent approach**: Extends existing PIPER.user.md pattern

### Negative

- **Manual migration**: Users must manually extract and configure hardcoded values
- **YAML complexity**: Adds structured data requirement to markdown file
- **Validation overhead**: Enhanced/full validation requires API calls
- **Configuration discovery**: Users must identify their workspace IDs manually

### Implementation Requirements

1. **Phase 3**: Implement configuration loader class with comprehensive test suite
2. **Phase 4**: Refactor 5 hardcoded references to use configuration system
3. **Phase 5**: Create migration documentation and user setup guides
4. **Phase 6**: Testing and validation of complete configuration system

### Monitoring & Success Criteria

- **User adoption**: Other developers can run tests and publish ADRs
- **Error clarity**: Configuration errors provide actionable resolution steps
- **Validation effectiveness**: Tiered validation catches configuration issues appropriately
- **Migration completeness**: All 5 hardcoded values successfully configured through schema

## Audit Mapping Verification

**Complete mapping of Phase 1 audit findings to configuration schema**:

| File:Line                                     | Hardcoded Value                    | Configuration Path                 | Migration Status        |
| --------------------------------------------- | ---------------------------------- | ---------------------------------- | ----------------------- |
| `fields.py:12`                                | `25e11704d8bf80deaac2f806390fe7da` | `notion.adrs.database_id`          | ✅ Required field       |
| `adr.py:12`                                   | `25e11704d8bf80deaac2f806390fe7da` | `notion.adrs.database_id`          | ✅ Same database        |
| `tests/publishing/test_publish_command.py:18` | `25d11704d8bf81dfb37acbdc143e6a80` | `notion.development.test_parent`   | ✅ Optional field       |
| `tests/integration/test_publish_gaps.py:21`   | `25d11704d8bf8135a3c9c732704c88a4` | `notion.development.test_parent`   | ✅ Environment fallback |
| `tests/debug_parent.py:19`                    | `25d11704d8bf80c8a71ddbe7aba51f55` | `notion.publishing.default_parent` | ✅ Required field       |

**Coverage**: 100% of hardcoded values mapped to configuration schema
**Risk mitigation**: 4 HIGH-risk and 1 MEDIUM-risk values all configurable
**User impact**: Complete multi-user enablement achieved through configuration

---

## Update October 2025

See **ADR-034: Plugin Architecture Implementation** for the plugin configuration system that extends the PIPER.user.md approach documented in this ADR. The plugin system adds a new YAML section to PIPER.user.md:

```yaml
## 🔌 Plugin Configuration
plugins:
  enabled:
    - github
    - slack
    - notion
    - calendar
```

This maintains the user-centric configuration philosophy established in this ADR while enabling dynamic plugin management.

---

**Decision Date**: August 30, 2025
**Next Actions**: Implement Phase 3 - Configuration loader with comprehensive test suite
**Review Schedule**: Post-implementation review after Phase 5 completion
