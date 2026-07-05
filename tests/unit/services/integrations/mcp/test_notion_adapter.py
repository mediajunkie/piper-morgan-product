"""Tests for NotionMCPAdapter.get_current_user() method"""

from unittest.mock import MagicMock, patch

import pytest
from notion_client.errors import APIResponseError, RequestTimeoutError

from services.integrations.mcp.notion_adapter import NotionMCPAdapter


class TestNotionAdapterGetCurrentUser:
    """Test suite for get_current_user() method."""

    def setup_method(self):
        """Set up test fixtures."""
        # Create adapter with mocked config
        with patch("services.mcp.consumer.notion_adapter.NotionConfig"):
            self.adapter = NotionMCPAdapter()
            # Mock the Notion client
            self.adapter._notion_client = MagicMock()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_success_person(self):
        """Test successful retrieval of person user information."""
        # Mock the Notion client response for person user
        mock_response = {
            "id": "user-123",
            "name": "Test User",
            "type": "person",
            "person": {"email": "test@example.com"},
        }
        self.adapter._notion_client.users.me.return_value = mock_response

        # Call the method
        result = await self.adapter.get_current_user()

        # Assertions
        assert result is not None
        assert result["id"] == "user-123"
        assert result["name"] == "Test User"
        assert result["type"] == "person"
        assert result["email"] == "test@example.com"
        assert "workspace" not in result  # person type doesn't have workspace
        self.adapter._notion_client.users.me.assert_called_once()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_success_bot(self):
        """Test retrieval of bot user with workspace info."""
        # Mock bot user response
        mock_response = {
            "id": "bot-456",
            "name": "Test Bot",
            "type": "bot",
            "bot": {"workspace": {"id": "ws-789", "name": "Test Workspace"}},
        }
        self.adapter._notion_client.users.me.return_value = mock_response

        result = await self.adapter.get_current_user()

        assert result is not None
        assert result["id"] == "bot-456"
        assert result["name"] == "Test Bot"
        assert result["type"] == "bot"
        assert "workspace" in result
        assert result["workspace"]["id"] == "ws-789"
        assert result["workspace"]["name"] == "Test Workspace"

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_api_error(self):
        """Test handling of Notion API errors."""
        # Mock API error
        mock_response = MagicMock()
        mock_response.status_code = 401
        self.adapter._notion_client.users.me.side_effect = APIResponseError(
            response=mock_response, message="Unauthorized", code="unauthorized"
        )

        # Should raise APIResponseError
        with pytest.raises(APIResponseError):
            await self.adapter.get_current_user()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_timeout(self):
        """Test handling of request timeout."""
        # Mock timeout
        self.adapter._notion_client.users.me.side_effect = RequestTimeoutError("Timeout")

        # Should raise RequestTimeoutError
        with pytest.raises(RequestTimeoutError):
            await self.adapter.get_current_user()

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_no_client(self):
        """Test behavior when Notion client is not initialized."""
        # Set client to None
        self.adapter._notion_client = None

        # Should return None gracefully
        result = await self.adapter.get_current_user()

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_empty_response(self):
        """Test handling of empty user info response."""
        # Mock empty response
        self.adapter._notion_client.users.me.return_value = None

        result = await self.adapter.get_current_user()

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_missing_email(self):
        """Test user without email field (edge case)."""
        # Mock user without person.email
        mock_response = {
            "id": "user-789",
            "name": "No Email User",
            "type": "person",
            # No person.email attribute
        }
        self.adapter._notion_client.users.me.return_value = mock_response

        result = await self.adapter.get_current_user()

        assert result is not None
        assert result["id"] == "user-789"
        assert result["name"] == "No Email User"
        # Should handle missing email gracefully - email key may not exist
        assert result.get("email") is None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_missing_workspace(self):
        """Test bot user without workspace info (edge case)."""
        # Mock bot user without workspace
        mock_response = {
            "id": "bot-999",
            "name": "Bot No Workspace",
            "type": "bot",
            # No bot.workspace attribute
        }
        self.adapter._notion_client.users.me.return_value = mock_response

        result = await self.adapter.get_current_user()

        assert result is not None
        assert result["id"] == "bot-999"
        assert result["type"] == "bot"
        # Should handle missing workspace gracefully
        if "workspace" in result:
            assert result["workspace"]["id"] is None
            assert result["workspace"]["name"] is None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_unexpected_exception(self):
        """Test handling of unexpected exceptions."""
        # Mock unexpected exception
        self.adapter._notion_client.users.me.side_effect = ValueError("Unexpected error")

        # Should return None for unexpected errors (not raise)
        result = await self.adapter.get_current_user()

        assert result is None

    @pytest.mark.asyncio
    @pytest.mark.smoke
    async def test_get_current_user_with_real_api_key(self):
        """
        Test get_current_user() with real Notion API key.

        This test requires NOTION_API_KEY environment variable to be set.
        Skips if not available (for CI/CD environments).
        """
        import os

        api_key = os.getenv("NOTION_API_KEY")
        if not api_key:
            pytest.skip("NOTION_API_KEY not set - skipping real API test")

        # Create adapter with real API key
        with patch("services.mcp.consumer.notion_adapter.NotionConfig") as MockConfig:
            mock_config = MagicMock()
            mock_config.get_api_key.return_value = api_key
            mock_config.validate_config.return_value = True
            MockConfig.return_value = mock_config

            adapter = NotionMCPAdapter()

            # Call with real API
            result = await adapter.get_current_user()

            # Verify we got real user data
            assert result is not None
            assert "id" in result
            assert "name" in result
            assert "type" in result
            assert result["type"] in ["person", "bot"]

            # If person, should have email
            if result["type"] == "person":
                # Email might be present
                if "email" in result:
                    assert isinstance(result["email"], str)

            # If bot, should have workspace
            if result["type"] == "bot":
                assert "workspace" in result
                assert "id" in result["workspace"]
                assert "name" in result["workspace"]

            print(
                f"\n✅ Real API test successful! User: {result.get('name')} ({result.get('type')})"
            )
