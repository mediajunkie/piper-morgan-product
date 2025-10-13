"""
Test suite for publish command with REAL API validation.
This implements TDD approach with actual Notion API verification to prevent verification theater.
"""

import os
import tempfile
import time
from pathlib import Path

import pytest

from config.notion_user_config import ConfigurationError, NotionUserConfig


@pytest.fixture
def test_parent_id():
    """Fixture to load test parent ID from configuration"""
    try:
        config = NotionUserConfig.load_from_user_config(Path("config/PIPER.user.md"))
        return config.get_parent_id("test")
    except (ConfigurationError, FileNotFoundError):
        # Fallback to old hardcoded value for backward compatibility during transition
        return "25d11704d8bf81dfb37acbdc143e6a80"


@pytest.fixture
def test_prefix():
    """Fixture to generate unique test prefix"""
    return f"TEST_{int(time.time())}_"


class TestPublishCommand:
    """Test suite for publish command with real functionality validation"""

    @pytest.mark.integration
    @pytest.mark.asyncio
    async def test_publish_creates_actual_notion_page(self, test_parent_id, test_prefix):
        """CRITICAL: Verify publishing ACTUALLY creates page in Notion"""
        from services.integrations.mcp.notion_adapter import NotionMCPAdapter
        from services.publishing.publisher import Publisher

        # 1. Create test markdown file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(
                f"# {test_prefix}Test Page\n\nThis is test content.\n\n## Subheading\n\nMore content."
            )
            test_file = f.name

        try:
            # 2. Publish using our service
            publisher = Publisher()
            result = await publisher.publish(
                file_path=test_file, platform="notion", location=test_parent_id
            )

            # 3. VERIFY page EXISTS in Notion (real API call)
            assert result["success"] is True, f"Publish failed: {result.get('error')}"
            assert "page_id" in result
            assert "url" in result

            # 4. Verify page content in Notion
            notion = NotionMCPAdapter()
            await notion.connect()
            page = await notion.get_page(result["page_id"])
            assert page is not None, "Created page not found in Notion"

            # 5. Verify we can get the blocks
            blocks = await notion.get_page_blocks(result["page_id"])
            assert len(blocks) > 0, "No content blocks found in created page"

        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    def test_markdown_converter_headers(self):
        """Test headers convert to correct Notion blocks"""
        from services.publishing.converters.markdown_to_notion import (
            convert_markdown_to_notion_blocks,
        )

        markdown = "# Header 1\n## Header 2\n### Header 3\n"
        result = convert_markdown_to_notion_blocks(markdown)

        assert result["success"] is True
        blocks = result["blocks"]
        assert len(blocks) == 3
        assert blocks[0]["type"] == "heading_1"
        assert blocks[1]["type"] == "heading_2"
        assert blocks[2]["type"] == "heading_3"

    def test_markdown_converter_paragraphs(self):
        """Test paragraphs and empty lines"""
        from services.publishing.converters.markdown_to_notion import (
            convert_markdown_to_notion_blocks,
        )

        markdown = "First paragraph.\n\nSecond paragraph."
        result = convert_markdown_to_notion_blocks(markdown)

        assert result["success"] is True
        blocks = result["blocks"]
        assert len(blocks) == 2  # Empty line should be skipped
        assert all(block["type"] == "paragraph" for block in blocks)

    def test_markdown_converter_lists(self):
        """Test bullet list conversion"""
        from services.publishing.converters.markdown_to_notion import (
            convert_markdown_to_notion_blocks,
        )

        markdown = "* First item\n* Second item\n- Third item"
        result = convert_markdown_to_notion_blocks(markdown)

        assert result["success"] is True
        blocks = result["blocks"]
        assert len(blocks) == 3
        assert all(block["type"] == "bulleted_list_item" for block in blocks)

    def test_unsupported_element_warnings(self):
        """Test unsupported elements convert with warnings"""
        from services.publishing.converters.markdown_to_notion import (
            convert_markdown_to_notion_blocks,
        )

        markdown = "# Title\n| Col 1 | Col 2 |\n|-------|-------|\n| Data  | More  |"
        result = convert_markdown_to_notion_blocks(markdown)

        assert result["success"] is True
        assert len(result["warnings"]) > 0
        assert any("Table converted to plain text" in warning for warning in result["warnings"])

    @pytest.mark.asyncio
    async def test_file_not_found_handling(self, test_parent_id):
        """Test graceful failure for missing files"""
        from services.publishing.publisher import Publisher

        publisher = Publisher()

        with pytest.raises(FileNotFoundError):
            await publisher.publish(
                file_path="nonexistent_file.md", platform="notion", location=test_parent_id
            )

    @pytest.mark.asyncio
    async def test_unsupported_platform_error(self):
        """Test error handling for unsupported platforms"""
        from services.publishing.publisher import Publisher

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Test\n\nContent")
            test_file = f.name

        try:
            publisher = Publisher()

            with pytest.raises(ValueError, match="Platform .* not supported"):
                await publisher.publish(
                    file_path=test_file, platform="unsupported_platform", location="some_id"
                )
        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    def test_title_extraction(self):
        """Test title extraction from markdown"""
        from services.publishing.publisher import Publisher

        publisher = Publisher()

        # Test with H1 header
        content = "# My Title\n\nContent"
        assert publisher._extract_title(content) == "My Title"

        # Test without header
        content = "Just content without header"
        assert publisher._extract_title(content) == "Untitled"

        # Test with H2 first (should still be untitled)
        content = "## Subheading\n\nContent"
        assert publisher._extract_title(content) == "Untitled"
