# Publish Command

## Overview

The `publish` command publishes markdown files to various platforms. Currently supports Notion with plans for additional platforms.

## Usage

```bash
python cli/commands/publish.py publish <file> --to <platform> [options]
```

## Platforms

### Notion

Publish markdown content to Notion pages or databases.

#### Publish to Notion Page

```bash
python cli/commands/publish.py publish README.md --to notion --location <parent-page-id>
```

**Parameters:**
- `<file>`: Path to markdown file to publish
- `--to notion`: Target platform (default: notion)
- `--location <parent-page-id>`: Parent page ID where new page will be created
- `--format markdown`: Content format (default: markdown)

**Example:**
```bash
python cli/commands/publish.py publish docs/guide.md --to notion --location a1b2c3d4e5f6
```

**Output:**
```
📤 Publishing docs/guide.md to notion...
✅ Published successfully!
📄 Page ID: 123abc...
🔗 URL: https://www.notion.so/workspace/Guide-123abc...
⚠️ Conversion notes:
  - Table converted to plain text (advanced formatting not yet supported)
```

#### Publish to Notion Database (ADRs)

```bash
python cli/commands/publish.py publish docs/adrs/adr-026.md --to notion --database <database-id>
```

**Parameters:**
- `<file>`: Path to ADR markdown file
- `--to notion`: Target platform (default: notion)
- `--database <database-id>`: Database ID for ADR publishing
- `--format markdown`: Content format (default: markdown)

**ADR Metadata Extraction:**

The command automatically extracts and populates database properties:
- **Name**: Extracted from `# ADR-XXX: Title` format
- **ADR Number**: Extracted from header (e.g., "026")
- **Status**: Extracted from `**Status:**` or `Status:` field
- **Author**: Extracted from `**Author:**` or `**Decision Maker:**` field
- **Date**: Extracted from `**Date:**` field (optional)

**Example:**
```bash
python cli/commands/publish.py publish docs/adrs/adr-026-notion-client.md --to notion --database xyz123
```

**Output:**
```
📤 Publishing docs/adrs/adr-026-notion-client.md to Notion database...
✅ Published successfully!
📄 Page ID: 456def...
🔗 URL: https://www.notion.so/workspace/Database-456def...
📊 ADR Metadata:
  - Title: Notion Client Migration to Official Library
  - Number: 026
  - Status: Accepted
  - Author: Lead Developer
  - Date: 2025-08-28
```

## Configuration

### Environment Variables

Required:
```bash
NOTION_API_KEY=secret_...
```

### User Configuration

Configure default parent pages and databases in `config/PIPER.user.md`:

```markdown
## Notion Configuration

### Parent IDs (for page publishing)
- **parent_id.test**: a1b2c3d4e5f6  # Test parent page
- **parent_id.docs**: g7h8i9j0k1l2  # Documentation parent page
- **parent_id.guides**: m3n4o5p6q7r8  # Guides parent page

### Database IDs (for structured publishing)
- **database_id.adrs**: xyz123abc456  # ADR database
- **database_id.projects**: def789ghi012  # Projects database
```

## Supported Markdown

### Fully Supported

- **Headers**: H1 (`#`), H2 (`##`), H3 (`###`)
- **Paragraphs**: Regular text blocks
- **Lists**: Bullet lists (`*`, `-`) and ordered lists (`1.`)
- **Inline Formatting**: **bold**, *italic*, `code`

### Partially Supported (with warnings)

- **Tables**: Converted to plain text
  ```
  ⚠️ Table converted to plain text (advanced formatting not yet supported)
  ```

- **Images**: Skipped with warning
  ```
  ⚠️ Image skipped (image embedding not yet supported)
  ```

- **Advanced Markdown**: Best-effort conversion with warnings

## Error Handling

### File Not Found

```bash
$ python cli/commands/publish.py publish missing.md --to notion --location abc123
❌ File not found: missing.md
```

### Invalid Parent ID

```bash
$ python cli/commands/publish.py publish README.md --to notion --location invalid
❌ Cannot create page under parent 'invalid'. Invalid parent page.

Options:
1. Use 'piper notion pages' to list available parent pages
2. Verify the parent ID in your Notion workspace
3. Ensure the integration has access to the parent page
```

### Missing Configuration

```bash
$ python cli/commands/publish.py publish README.md --to notion --location abc123
❌ NOTION_API_KEY not found in environment

Please set NOTION_API_KEY:
1. Create .env file with: NOTION_API_KEY=secret_your_key
2. Or export NOTION_API_KEY=secret_your_key
```

### Platform Not Supported

```bash
$ python cli/commands/publish.py publish README.md --to medium --location abc123
❌ Platform 'medium' not supported. Currently only 'notion' is supported.
```

## Exit Codes

- `0`: Success
- `1`: Error (file not found, invalid configuration, API error)

## Options Reference

### Required Arguments

- `<file>`: Path to markdown file to publish

### Optional Arguments

- `--to <platform>`: Target platform (default: `notion`)
  - Supported: `notion`

- `--location <parent-id>`: Parent page ID for page publishing
  - Mutually exclusive with `--database`
  - Required if `--database` not provided

- `--database <database-id>`: Database ID for database publishing
  - Mutually exclusive with `--location`
  - Required if `--location` not provided
  - Automatically extracts ADR metadata

- `--format <format>`: Content format (default: `markdown`)
  - Currently only `markdown` supported

## Examples

### Publish Documentation

```bash
# Publish README to docs parent page
python cli/commands/publish.py publish README.md --to notion --location g7h8i9j0k1l2

# Publish guide to guides parent page
python cli/commands/publish.py publish docs/user-guide.md --to notion --location m3n4o5p6q7r8
```

### Publish ADRs

```bash
# Publish ADR to database
python cli/commands/publish.py publish docs/adrs/adr-027-config-arch.md --to notion --database xyz123

# Batch publish all ADRs (using shell loop)
for adr in docs/adrs/adr-*.md; do
    python cli/commands/publish.py publish "$adr" --to notion --database xyz123
    sleep 1  # Rate limiting
done
```

### Publish from CI/CD

```bash
# GitHub Actions example
- name: Publish Documentation
  env:
    NOTION_API_KEY: ${{ secrets.NOTION_API_KEY }}
  run: |
    python cli/commands/publish.py publish README.md --to notion --location ${{ vars.DOCS_PARENT_ID }}
```

## Testing

Run integration tests:

```bash
# Run all publish tests
PYTHONPATH=. python -m pytest tests/publishing/ -v

# Run integration test with real API
PYTHONPATH=. python -m pytest tests/publishing/test_publish_command.py::TestPublishCommand::test_publish_creates_actual_notion_page -v

# Run unit tests only
PYTHONPATH=. python -m pytest tests/publishing/ -m "not integration" -v
```

## Troubleshooting

### Permission Errors

**Problem**: `Cannot create page under parent 'abc123'`

**Solutions**:
1. Verify the Notion integration has access to the parent page
2. In Notion, go to the parent page → `...` menu → Connections → Add your integration
3. Ensure the parent ID is correct (copy from Notion page URL)

### Rate Limiting

**Problem**: Multiple publishes fail with rate limit errors

**Solution**: Add delays between publishes:
```bash
for file in docs/*.md; do
    python cli/commands/publish.py publish "$file" --to notion --location abc123
    sleep 1  # Wait 1 second between requests
done
```

### Conversion Warnings

**Problem**: Tables or images not appearing correctly

**Explanation**: Not all Markdown features are supported yet. Check warnings in output:
```
⚠️ Conversion notes:
  - Table converted to plain text (advanced formatting not yet supported)
  - Image skipped (image embedding not yet supported)
```

**Future**: Advanced formatting support planned for future releases.

## Related Documentation

- [Pattern-033: Notion Publishing](../internal/architecture/current/patterns/pattern-033-notion-publishing.md) - Architecture pattern
- [ADR-026: Notion Client Migration](../internal/architecture/current/adrs/adr-026-notion-client-migration.md) - Implementation decision
- [ADR-027: Configuration Architecture](../internal/architecture/current/adrs/adr-027-configuration-architecture-user-vs-system-separation.md) - User configuration

## See Also

- `piper notion pages` - List available Notion pages
- `piper notion databases` - List available Notion databases
- Notion API: https://developers.notion.com/

---

_Last updated: October 8, 2025_
_Command status: Stable - Production ready_
