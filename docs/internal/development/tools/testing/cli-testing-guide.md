# CLI Testing Guide

**Status**: Active
**Last Updated**: August 28, 2025
**Scope**: Command Line Interface testing patterns and Notion CLI validation

## Overview

This document provides comprehensive testing guidance for Piper Morgan's CLI interfaces, with specific focus on the Notion integration CLI that was recently enhanced with full CRUD operations.

## CLI Testing Principles

### 1. Functional Testing Requirements

**Context**: Code inspection vs execution verification for integration success
**Solution**: Require actual command execution for integration proof, not just import testing
**Benefit**: Prevents false integration success claims, identifies initialization errors

**Implementation**:

```bash
# REQUIRED: Actual command execution
python cli/commands/notion.py status

# NOT SUFFICIENT: Import testing only
python -c "import cli.commands.notion; print('Import successful')"
```

### 2. End-to-End CRUD Validation

**Context**: Integration features requiring verification of complete data lifecycle
**Solution**: Implement comprehensive testing sequence covering Create, Read, Update, Delete operations

**Implementation**:

```bash
# Full CRUD cycle test for Notion CLI
python cli/commands/notion.py status          # Verify connection
python cli/commands/notion.py pages           # List existing pages
python cli/commands/notion.py search --query "test"  # Search content
python cli/commands/notion.py create "Test Page"     # Create new page
python cli/commands/notion.py search --query "Test Page"  # Verify creation
```

## Notion CLI Testing

### Test Coverage Matrix

| Command  | Test Type   | Status | Notes                                     |
| -------- | ----------- | ------ | ----------------------------------------- |
| `status` | Connection  | ✅     | Validates API key and workspace access    |
| `test`   | Integration | ✅     | Tests live API connection                 |
| `search` | Read        | ✅     | Validates search functionality            |
| `pages`  | Read        | ✅     | Lists up to 20 pages with metadata        |
| `create` | Write       | ✅     | Creates pages with smart parent selection |

### Test Scenarios

#### 1. Connection Testing

**Objective**: Verify Notion integration configuration and connectivity

```bash
# Test integration status
python cli/commands/notion.py status

# Expected output:
# ✅ Connected to Notion workspace
# 📊 Workspace: [Workspace Name]
# 🔑 API Key: Configured
# 🌐 Base URL: https://api.notion.com/v1
```

**Failure Scenarios**:

- Missing `NOTION_API_KEY` environment variable
- Invalid API key format
- Network connectivity issues
- Workspace access permissions

#### 2. Read Operations Testing

**Objective**: Validate search and listing functionality

```bash
# Test page listing
python cli/commands/notion.py pages

# Test search functionality
python cli/commands/notion.py search --query "project"
```

**Success Criteria**:

- Pages display with titles, IDs, and URLs
- Search returns relevant results
- Error handling for empty results
- Graceful degradation for API failures

#### 3. Write Operations Testing

**Objective**: Validate page creation with proper error handling

```bash
# Test page creation with automatic parent selection
python cli/commands/notion.py create "Test Page $(date '+%I:%M %p')"

# Test page creation with specific parent
python cli/commands/notion.py create "Child Page" --parent-id "parent-id-here"
```

**Success Criteria**:

- Page created successfully
- Proper parent page selection
- Clear success feedback with page details
- Error handling for invalid parent IDs

### Error Handling Validation

#### Graceful Degradation

**Test Cases**:

1. **Missing API Key**: Should provide clear setup instructions
2. **Invalid API Key**: Should fail gracefully with helpful error message
3. **Network Issues**: Should timeout appropriately with retry guidance
4. **Permission Errors**: Should explain access requirements

**Example Error Handling**:

```bash
$ python cli/commands/notion.py status
❌ Notion API key not configured
💡 Please set NOTION_API_KEY environment variable
📖 See docs/features/notion-integration.md for setup instructions
```

#### User Experience Validation

**Success Indicators**:

- Clear, actionable error messages
- Consistent formatting and color coding
- Helpful troubleshooting guidance
- Professional presentation

## CLI Testing Patterns

### 1. Command Structure Validation

**Test Command Registration**:

```bash
# Verify all commands are registered
python cli/commands/notion.py --help

# Expected output should include:
# status, test, search, pages, create
```

**Test Argument Parsing**:

```bash
# Test required arguments
python cli/commands/notion.py create
# Should show usage error

# Test optional arguments
python cli/commands/notion.py create "Title" --parent-id "valid-id"
# Should work correctly
```

### 2. Integration Testing

**Test Adapter Connection**:

- Verify CLI commands connect to underlying service adapters
- Test error propagation from adapters to CLI
- Validate response formatting and user feedback

**Test Configuration Integration**:

- Environment variable loading
- Configuration validation
- Default value handling

### 3. Performance Testing

**Response Time Validation**:

- Status command: < 2 seconds
- Search command: < 5 seconds
- Page creation: < 10 seconds
- Page listing: < 3 seconds

**Resource Usage**:

- Memory consumption during operations
- Network request efficiency
- Error handling performance

## Testing Automation

### Manual Testing Checklist

**Pre-Test Setup**:

- [ ] Notion API key configured
- [ ] Workspace access granted
- [ ] Test pages available for search
- [ ] Network connectivity verified

**Test Execution**:

- [ ] Status command validation
- [ ] Connection testing
- [ ] Read operations (search, pages)
- [ ] Write operations (create)
- [ ] Error scenario testing
- [ ] Performance validation

**Post-Test Validation**:

- [ ] Test pages created successfully
- [ ] Search results accurate
- [ ] Error handling appropriate
- [ ] User experience satisfactory

### Automated Testing Opportunities

**Unit Tests**:

- Command argument parsing
- Response formatting
- Error message generation

**Integration Tests**:

- Adapter connectivity
- Configuration loading
- End-to-end workflows

**Performance Tests**:

- Response time benchmarks
- Resource usage monitoring
- Load testing scenarios

## Troubleshooting

### Common Test Failures

1. **Import Errors**:

   ```bash
   ModuleNotFoundError: No module named 'notion_client'
   ```

   **Solution**: Install required dependencies with `pip install notion-client`

2. **Authentication Failures**:

   ```bash
   APIResponseError: 401 Unauthorized
   ```

   **Solution**: Verify `NOTION_API_KEY` environment variable

3. **Permission Errors**:

   ```bash
   APIResponseError: 403 Forbidden
   ```

   **Solution**: Grant workspace access to your Notion integration

4. **Network Timeouts**:
   ```bash
   TimeoutError: Request timed out
   ```
   **Solution**: Check network connectivity and Notion API status

### Debug Mode

**Enable Verbose Output**:

```bash
# Add debug logging to CLI commands
export PYTHONPATH=.
python -m cli.commands.notion status --verbose
```

**Check Adapter State**:

```python
# Interactive debugging
python -c "
from services.integrations.mcp.notion_adapter import NotionMCPAdapter
adapter = NotionMCPAdapter()
print(f'Adapter initialized: {adapter}')
print(f'Client configured: {hasattr(adapter, \"client\")}')
"
```

## Future Enhancements

### Planned Testing Improvements

1. **Automated Test Suite**: Comprehensive CLI testing automation
2. **Performance Benchmarks**: Automated performance validation
3. **Error Scenario Coverage**: Expanded error handling tests
4. **Integration Test Coverage**: End-to-end workflow validation

### Testing Infrastructure

1. **Mock Notion API**: Local testing without external dependencies
2. **Test Data Management**: Consistent test data across test runs
3. **CI/CD Integration**: Automated testing in deployment pipeline
4. **Test Reporting**: Comprehensive test result analysis

## References

- [Notion Integration Documentation](../../../../public/user-guides/features/notion-integration.md)
- [ADR-026: Notion Client Migration](../../../architecture/current/adrs/adr-026-notion-client-migration.md)
- [CLI Integration Pattern](../../../architecture/current/patterns/pattern-027-cli-integration.md)
- [End-to-End CRUD Validation Pattern](../../../architecture/current/patterns/pattern-010-cross-validation-protocol.md)
