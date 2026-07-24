"""
Integration tests for publish command specification gaps.
These tests MUST use real Notion API - no mocks for core functionality.
"""

import os
import tempfile
import time
from pathlib import Path

import pytest

# #1452: these exercise the LIVE Notion publisher (CI evidence: 'NoneType'
# object has no attribute 'pages' — no configured client keyless) — keyed
# integration lane.
pytestmark = pytest.mark.llm
import requests
from dotenv import load_dotenv

from config.notion_user_config import ConfigurationError, NotionUserConfig
from services.publishing.publisher import Publisher

# Load real environment - CRITICAL for integration tests
load_dotenv()

# Test configuration - Load from configuration with env variable fallback
try:
    config = NotionUserConfig.load_from_user_config(Path("config/PIPER.user.md"))
    TEST_PARENT_ID = os.getenv("TEST_PARENT_ID", config.get_parent_id("test"))
except (ConfigurationError, FileNotFoundError):
    # Fallback to environment variable or hardcoded value for backward compatibility
    TEST_PARENT_ID = os.getenv("TEST_PARENT_ID", "25d11704d8bf8135a3c9c732704c88a4")

INVALID_PARENT_ID = "invalid_parent_xyz_123"


class TestURLReturnGap:
    """Gap 1: Verify URL is returned and displayed to user"""

    @pytest.mark.integration
    async def test_publisher_returns_real_notion_url(self):
        """INTEGRATION: Publisher must return actual Notion URL from API"""
        # Create temporary markdown file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write(f"# URL Test {int(time.time())}\n\nThis tests URL return functionality.\n")
            test_file = f.name

        try:
            publisher = Publisher()
            result = await publisher.publish(
                file_path=test_file, platform="notion", location=TEST_PARENT_ID
            )

            # Verify result structure
            assert result["success"] is True, f"Publish failed: {result.get('error')}"
            assert "url" in result, "Result missing 'url' key"
            assert result["url"], "URL is empty"

            # Verify URL format
            url = result["url"]
            assert url.startswith("https://www.notion.so/"), f"Invalid URL format: {url}"

            # CRITICAL: Verify URL is real and accessible
            response = requests.head(url, timeout=10)
            assert response.status_code == 200, f"URL not accessible: {response.status_code}"

            print(f"✅ Real URL validated: {url}")

        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    @pytest.mark.integration
    async def test_cli_displays_url_in_output(self):
        """INTEGRATION: CLI must display URL in terminal output"""
        # This will be implemented when CLI is fixed
        # For now, verify Publisher provides URL for CLI to display

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# CLI URL Test\n\nTesting CLI URL display.")
            test_file = f.name

        try:
            publisher = Publisher()
            result = await publisher.publish(
                file_path=test_file, platform="notion", location=TEST_PARENT_ID
            )

            # CLI will use this URL - must be present and valid
            assert "url" in result
            assert result["url"].startswith("https://www.notion.so/")

        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)


class TestParentErrorHandlingGap:
    """Gap 2: Verify explicit error handling for invalid parent locations"""

    @pytest.mark.integration
    async def test_invalid_parent_raises_explicit_error(self):
        """INTEGRATION: Invalid parent must raise explicit error with options"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# Error Test\n\nTesting error handling.")
            test_file = f.name

        try:
            publisher = Publisher()

            with pytest.raises(ValueError) as exc_info:
                await publisher.publish(
                    file_path=test_file, platform="notion", location=INVALID_PARENT_ID
                )

            # Verify error message is helpful
            error_msg = str(exc_info.value)
            assert "Cannot create page" in error_msg
            assert "Options:" in error_msg
            assert "available parents" in error_msg or "different parent" in error_msg

            print(f"✅ Explicit error validated: {error_msg}")

        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)

    @pytest.mark.integration
    async def test_no_silent_fallback_behavior(self):
        """INTEGRATION: Must not silently create page in default location"""

        with tempfile.NamedTemporaryFile(mode="w", suffix=".md", delete=False) as f:
            f.write("# No Fallback Test\n\nShould fail, not fallback.")
            test_file = f.name

        try:
            publisher = Publisher()

            # This MUST raise an error, not silently succeed
            with pytest.raises(ValueError):
                await publisher.publish(
                    file_path=test_file,
                    platform="notion",
                    location="definitely_invalid_parent_id_12345",
                )

            print("✅ No silent fallback - error raised as expected")

        finally:
            if os.path.exists(test_file):
                os.unlink(test_file)
