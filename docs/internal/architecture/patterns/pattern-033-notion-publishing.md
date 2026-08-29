# Pattern-033: Notion Publishing

## Status

**Proven** - Implemented and validated with real API integration testing

## Context

Publishing markdown content to Notion workspaces is a core functionality for Piper Morgan's knowledge management capabilities. This pattern addresses:

- **Content Migration**: Moving local markdown documentation to Notion for collaboration
- **Knowledge Management**: Publishing ADRs, guides, and documentation programmatically
- **Multi-Platform Publishing**: Extensible architecture supporting future platforms beyond Notion
- **TDD Validation**: Preventing "verification theater" through real API testing

## Pattern Description

The Notion Publishing pattern implements a three-layer architecture:

1. **CLI Command Layer**: User-facing interface (`cli/commands/publish.py`)
2. **Publisher Service Layer**: Platform-agnostic orchestration (`services/publishing/publisher.py`)
3. **Converter Layer**: Format-specific transformations (`services/publishing/converters/`)

Core capabilities:
- Markdown to Notion blocks conversion
- Page and database publishing modes
- ADR metadata extraction and structured publishing
- Graceful degradation with user-friendly warnings
- Real API validation in tests

## Implementation

### Structure

```
cli/commands/
  publish.py              # CLI interface with argparse
services/publishing/
  publisher.py            # Main orchestration service
  converters/
    markdown_to_notion.py # Markdown → Notion blocks conversion
services/integrations/
  notion/
    notion_integration_router.py  # Notion API integration
tests/publishing/
  test_publish_command.py # TDD suite with real API calls
```

### Code Example

**CLI Usage**:
```bash
# Publish to Notion page
python cli/commands/publish.py publish README.md --to notion --location parent-id

# Publish to Notion database (for ADRs)
python cli/commands/publish.py publish docs/adrs/adr-026.md --to notion --database db-id
```

**Service Layer**:
```python
from services.publishing.publisher import Publisher

publisher = Publisher()

# Publish markdown file
result = await publisher.publish(
    file_path="docs/guide.md",
    platform="notion",
    location=parent_page_id,
    format="markdown"
)

if result["success"]:
    print(f"Published: {result['url']}")
    if result.get("warnings"):
        print(f"Warnings: {result['warnings']}")
else:
    print(f"Failed: {result['error']}")
```

**Markdown Conversion**:
```python
from services.publishing.converters.markdown_to_notion import (
    convert_markdown_to_notion_blocks
)

markdown_content = """
# My Document

This is a paragraph with **bold** text.

- List item 1
- List item 2
"""

result = convert_markdown_to_notion_blocks(markdown_content)
# Returns: {
#   "success": True,
#   "blocks": [...notion block objects...],
#   "warnings": ["Unsupported element: ..." if any]
# }
```

### Configuration

Environment variables:
```bash
NOTION_API_KEY=secret_...  # Notion integration token
```

User configuration (config/PIPER.user.md):
```markdown
## Notion Configuration

- **parent_id.test**: [test-parent-page-id]
- **parent_id.docs**: [docs-parent-page-id]
- **database_id.adrs**: [adr-database-id]
```

## Usage Guidelines

### When to Use

- **Markdown to Notion migration**: Convert local markdown files to Notion pages
- **Programmatic content publishing**: Automate documentation updates
- **ADR management**: Publish architectural decision records to structured databases
- **Batch operations**: Process multiple files systematically
- **CI/CD integration**: Publish documentation as part of deployment pipeline

### When NOT to Use

- **Complex formatting requirements**: Notion blocks are limited compared to markdown
- **Bi-directional sync**: This is one-way publish only (markdown → Notion)
- **Real-time collaboration**: Use Notion's native interface for editing
- **Binary content**: Images and attachments require separate handling

### Best Practices

**Environment Loading**:
```python
# CRITICAL: Load environment variables FIRST in CLI commands
from dotenv import load_dotenv
load_dotenv()

# Then import services that depend on environment
from services.publishing.publisher import Publisher
```

**Error Handling**:
```python
try:
    result = await publisher.publish(...)
    if result["success"]:
        # Success path with warnings
        if result.get("warnings"):
            for warning in result["warnings"]:
                print(f"⚠️  {warning}")
    else:
        # Failure path with actionable error
        print(f"❌ {result['error']}")
except ValueError as e:
    # User errors (invalid parent, bad configuration)
    print(f"Configuration error: {e}")
except Exception as e:
    # Unexpected errors
    print(f"Unexpected error: {e}")
```

**Test-Driven Development**:
```python
# Tests MUST use real API calls, not mocks for core functionality
@pytest.mark.integration
@pytest.mark.asyncio
async def test_publish_creates_actual_notion_page(test_parent_id, test_prefix):
    """CRITICAL: Verify publishing ACTUALLY creates page in Notion"""
    publisher = Publisher()
    result = await publisher.publish(
        file_path=test_file,
        platform="notion",
        location=test_parent_id
    )

    # Verify in Notion (real API call)
    notion = NotionMCPAdapter()
    await notion.connect()
    page = await notion.get_page(result["page_id"])
    assert page is not None, "Created page not found in Notion"
```

**Supported Markdown Elements** (MVP scope):
- ✅ Headers (H1, H2, H3)
- ✅ Paragraphs
- ✅ Bullet lists (ordered and unordered)
- ✅ Basic inline formatting (bold, italic, code)
- ⚠️ Tables → Converted to plain text with warning
- ⚠️ Images → Skipped with warning (future enhancement)
- ⚠️ Advanced formatting → Best-effort with warnings

## Examples in Codebase

### Primary Usage

- `cli/commands/publish.py:29-157` - CLI interface and command routing
- `services/publishing/publisher.py:14-293` - Main publisher service with dual-mode support
- `services/publishing/converters/markdown_to_notion.py` - Markdown conversion logic

### Test Examples

- `tests/publishing/test_publish_command.py:32-68` - Integration test with real Notion API
- `tests/publishing/test_publish_command.py:70-84` - Header conversion validation
- `tests/publishing/test_publish_command.py:86-98` - Paragraph conversion validation
- `tests/publishing/test_publish_command.py:100-112` - List conversion validation
- `tests/publishing/test_publish_command.py:114-125` - Warning generation for unsupported elements

## Related Patterns

### Complements

- [Pattern-022: MCP + Spatial Intelligence Integration](pattern-022-mcp-spatial-intelligence-integration.md) - Uses Notion integration router
- [Pattern-030: Plugin Interface](pattern-030-plugin-interface.md) - Notion as plugin for extensibility
- [Pattern-018: Configuration Access](pattern-018-configuration-access.md) - User config for workspace IDs

### Dependencies

- [Pattern-007: Async Error Handling](pattern-007-async-error-handling.md) - Publisher uses async/await pattern
- [Pattern-014: Error Handling API Contract](pattern-014-error-handling-api-contract.md) - Structured error responses

## Migration Notes

### From Issue #135 (CORE-NOTN-PUBLISH)

Implemented features:
- ✅ TDD test suite with real API validation (tests/publishing/test_publish_command.py)
- ✅ Markdown converter for MVP scope (headers, paragraphs, lists)
- ✅ Publisher service with error handling
- ✅ CLI command interface with dual-mode support (page/database)
- ✅ Integration testing with actual Notion API
- ✅ Documentation created (this pattern + ADR-026)

### From Handoff Document (2025-08-29)

Key learning preserved:
- **Anti-Pattern Avoided**: Tests now use real API calls, not mocks for core functionality
- **Environment Loading**: Fixed CLI environment loading issue (load_dotenv() before imports)
- **URL Return**: Publisher returns clickable Notion URLs for user verification
- **Error Messages**: Actionable error messages with configuration guidance

## References

### Documentation

- **ADR-026**: Notion Client Migration to Official Library
- **ADR-027**: Configuration Architecture (User vs System Separation)
- **Handoff Document**: `docs/internal/development/handoffs/prompts/2025-08-29-handoff-publish-complete.md`
- **GitHub Issue**: #135 (CORE-NOTN-PUBLISH)

### Usage Analysis

- **Current usage**: 3 files (CLI + Publisher + Converter)
- **Test coverage**: 8 tests (1 integration + 7 unit)
- **Last updated**: October 8, 2025
- **Maintenance status**: Active - production ready

### External References

- [Notion API Documentation](https://developers.notion.com/)
- [Notion Python Client](https://github.com/ramnes/notion-sdk-py)

---

_Pattern created: October 8, 2025_
_Status: Proven - Implemented and validated with real API testing_
_Maintenance: Active - Core knowledge management functionality_
