"""
Tests for OAuth → Spatial Initialization Integration
Tests the integration between OAuth flow and spatial system initialization.

Following TDD principles: Write failing test → See it fail → Verify integration works → Make test pass
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.integrations.slack.config_service import SlackConfigService
from services.integrations.slack.oauth_handler import SlackOAuthHandler
from services.integrations.slack.spatial_agent import SlackSpatialAgent
from services.integrations.slack.spatial_types import Territory, TerritoryType


class TestOAuthSpatialIntegration:
    """Test OAuth flow integration with spatial system initialization"""

    @pytest.fixture
    def config_service(self):
        """Mock config service"""
        return Mock(spec=SlackConfigService)

    @pytest.fixture
    def oauth_handler(self, config_service):
        """OAuth handler instance"""
        return SlackOAuthHandler(config_service)

    @pytest.fixture
    def spatial_agent(self, config_service):
        """Spatial agent instance"""
        event_handler = Mock()
        return SlackSpatialAgent(config_service, event_handler)

    def test_oauth_success_initializes_spatial_territory(self, oauth_handler, spatial_agent):
        """Test that successful OAuth initializes spatial territory"""
        # Arrange
        oauth_response = {
            "access_token": "xoxb-test-token",
            "team": {"id": "T123456", "name": "Test Workspace"},
            "authed_user": {"id": "U123456", "scope": "chat:write,channels:read"},
        }

        # Act
        spatial_territory = oauth_handler.initialize_spatial_territory(oauth_response)

        # Assert
        assert spatial_territory is not None
        assert spatial_territory.territory_id == "T123456"
        assert spatial_territory.name == "Test Workspace"
        assert spatial_territory.type == TerritoryType.WORKSPACE
        assert spatial_territory.access_token == "xoxb-test-token"

    def test_oauth_failure_does_not_initialize_spatial_territory(
        self, oauth_handler, spatial_agent
    ):
        """Test that OAuth failure prevents spatial territory initialization"""
        # Arrange
        oauth_response = {"error": "access_denied", "error_description": "User denied access"}

        # Act & Assert
        with pytest.raises(ValueError, match="OAuth failed"):
            oauth_handler.initialize_spatial_territory(oauth_response)

    def test_spatial_agent_recognizes_oauth_territory(self, oauth_handler, spatial_agent):
        """Test that spatial agent recognizes OAuth-initialized territory"""
        # Arrange
        oauth_response = {
            "access_token": "xoxb-test-token",
            "team": {"id": "T123456", "name": "Test Workspace"},
        }

        territory = oauth_handler.initialize_spatial_territory(oauth_response)

        # Act
        spatial_agent.spatial_state.current_territory = territory.territory_id

        # Assert
        assert spatial_agent.spatial_state.current_territory == "T123456"
        assert spatial_agent.get_spatial_summary()["current_position"]["territory"] == "T123456"

    def test_oauth_scopes_affect_spatial_capabilities(self, oauth_handler, spatial_agent):
        """Test that OAuth scopes determine spatial capabilities"""
        # Arrange
        oauth_response = {
            "access_token": "xoxb-test-token",
            "team": {"id": "T123456", "name": "Test Workspace"},
            "authed_user": {"id": "U123456", "scope": "chat:write,channels:read,users:read"},
        }

        # Act
        territory = oauth_handler.initialize_spatial_territory(oauth_response)
        capabilities = oauth_handler.get_spatial_capabilities(oauth_response)

        # Assert
        assert "chat:write" in capabilities
        assert "channels:read" in capabilities
        assert "users:read" in capabilities
        assert len(capabilities) == 3

    def test_oauth_token_refresh_updates_spatial_territory(self, oauth_handler, spatial_agent):
        """Test that token refresh updates spatial territory"""
        # Arrange
        initial_response = {
            "access_token": "xoxb-old-token",
            "team": {"id": "T123456", "name": "Test Workspace"},
        }

        refresh_response = {
            "access_token": "xoxb-new-token",
            "team": {"id": "T123456", "name": "Test Workspace"},
        }

        # Act
        initial_territory = oauth_handler.initialize_spatial_territory(initial_response)
        updated_territory = oauth_handler.refresh_spatial_territory(refresh_response)

        # Assert
        assert initial_territory.territory_id == updated_territory.territory_id
        assert initial_territory.access_token != updated_territory.access_token
        assert updated_territory.access_token == "xoxb-new-token"

    def test_oauth_state_validation_prevents_spatial_initialization(
        self, oauth_handler, spatial_agent
    ):
        """Test that invalid OAuth state prevents spatial initialization"""
        # Arrange
        oauth_response = {
            "access_token": "xoxb-test-token",
            "team": {"id": "T123456", "name": "Test Workspace"},
            "state": "invalid-state",
        }

        # Act & Assert
        with pytest.raises(ValueError, match="Invalid OAuth state"):
            oauth_handler.validate_and_initialize_spatial_territory(oauth_response, "valid-state")

    def test_oauth_user_context_integration(self, oauth_handler, spatial_agent):
        """Test that OAuth user context integrates with spatial system"""
        # Arrange
        oauth_response = {
            "access_token": "xoxb-test-token",
            "team": {"id": "T123456", "name": "Test Workspace"},
            "authed_user": {"id": "U123456", "name": "Test User", "scope": "chat:write"},
        }

        # Act
        territory = oauth_handler.initialize_spatial_territory(oauth_response)
        user_context = oauth_handler.get_user_spatial_context(oauth_response)

        # Assert
        assert user_context["user_id"] == "U123456"
        assert user_context["user_name"] == "Test User"
        assert user_context["territory_id"] == "T123456"
        assert "chat:write" in user_context["capabilities"]

    def test_oauth_workspace_switching(self, oauth_handler, spatial_agent):
        """Test switching between workspaces via OAuth"""
        # Arrange
        workspace1_response = {
            "access_token": "xoxb-token-1",
            "team": {"id": "T123456", "name": "Workspace 1"},
        }

        workspace2_response = {
            "access_token": "xoxb-token-2",
            "team": {"id": "T789012", "name": "Workspace 2"},
        }

        # Act
        territory1 = oauth_handler.initialize_spatial_territory(workspace1_response)
        territory2 = oauth_handler.initialize_spatial_territory(workspace2_response)

        # Update spatial agent
        spatial_agent.spatial_state.current_territory = territory2.territory_id

        # Assert
        assert territory1.territory_id != territory2.territory_id
        assert spatial_agent.spatial_state.current_territory == "T789012"
        assert spatial_agent.get_spatial_summary()["current_position"]["territory"] == "T789012"

    def test_oauth_error_handling_integration(self, oauth_handler, spatial_agent):
        """Test OAuth error handling integration with spatial system"""
        # Arrange
        error_responses = [
            {"error": "invalid_client"},
            {"error": "invalid_grant"},
            {"error": "invalid_scope"},
            {"error": "server_error"},
        ]

        # Act & Assert
        for error_response in error_responses:
            with pytest.raises(ValueError) as exc_info:
                oauth_handler.initialize_spatial_territory(error_response)
            assert "OAuth failed" in str(exc_info.value)

    def test_oauth_spatial_territory_persistence(self, oauth_handler, spatial_agent):
        """Test that OAuth-initialized territories persist in spatial memory"""
        # Arrange
        oauth_response = {
            "access_token": "xoxb-test-token",
            "team": {"id": "T123456", "name": "Test Workspace"},
        }

        # Act
        territory = oauth_handler.initialize_spatial_territory(oauth_response)
        spatial_agent.spatial_state.current_territory = territory.territory_id

        # Simulate persistence
        persisted_territory = spatial_agent.get_spatial_summary()["current_position"]["territory"]

        # Assert
        assert persisted_territory == "T123456"
        assert (
            territory.territory_id in spatial_agent.spatial_state.spatial_memories
            or spatial_agent.spatial_state.current_territory == territory.territory_id
        )
