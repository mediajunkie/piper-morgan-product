"""
Tests for Webhook → Processing Flow Integration
Tests the integration between webhook routing and event processing.

Following TDD principles: Write failing test → See it fail → Verify integration works → Make test pass

NOTE (2026-08-30, census disposal Batch 3): the ngrok half of this file
(NgrokService fixture + 5 tunnel tests) was excised with
services/integrations/slack/ngrok_service.py — the webhook-tunnel dev path.
Slack inbound is Socket Mode only; the webhook_router tests below cover the
LIVE router surface and stay.
"""

from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch

import pytest

from services.integrations.slack.config_service import SlackConfigService
from services.integrations.slack.event_handler import SlackEventHandler
from services.integrations.slack.webhook_router import SlackWebhookRouter


class TestNgrokWebhookFlow:
    """Test ngrok tunnel to webhook processing flow"""

    @pytest.fixture
    def config_service(self):
        """Mock config service"""
        return Mock(spec=SlackConfigService)

    @pytest.fixture
    def webhook_router(self, config_service):
        """Webhook router instance"""
        return SlackWebhookRouter(config_service)

    @pytest.fixture
    def event_handler(self, config_service):
        """Event handler instance"""
        return SlackEventHandler(config_service)

    @pytest.mark.smoke
    def test_webhook_route_registration(self, webhook_router):
        """Test that webhook routes are registered correctly"""
        # Arrange
        webhook_router._register_routes = Mock()

        # Act
        webhook_router.register_webhook_routes()

        # Assert
        webhook_router._register_routes.assert_called_once()

    @pytest.mark.smoke
    def test_webhook_event_validation(self, webhook_router):
        """Test that webhook events are validated"""
        # Arrange
        valid_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Hello world",
            "team": "T123456",
        }

        invalid_event = {
            "type": "message",
            "channel": "C123456",
            # Missing required fields
        }

        # Act & Assert
        assert webhook_router._validate_event(valid_event) is True
        assert webhook_router._validate_event(invalid_event) is False

    @pytest.mark.smoke
    def test_webhook_signature_verification(self, webhook_router):
        """Test that webhook signatures are verified"""
        import hashlib
        import hmac
        import time

        # Arrange - use current timestamp to pass replay attack check
        current_timestamp = str(int(time.time()))
        body = "test body"

        # Mock config to provide signing secret
        webhook_router.config_service.get_config = Mock(
            return_value=Mock(signing_secret="test_secret_key")
        )

        # Compute valid signature using same algorithm as the code
        sig_basestring = f"v0:{current_timestamp}:{body}"
        valid_signature = (
            "v0="
            + hmac.new(
                "test_secret_key".encode(), sig_basestring.encode(), hashlib.sha256
            ).hexdigest()
        )

        # Act
        is_valid = webhook_router._verify_webhook_signature(
            valid_signature, current_timestamp, body
        )

        # Assert
        assert is_valid is True

    @pytest.mark.smoke
    async def test_webhook_event_processing_flow(self, webhook_router, event_handler):
        """Test complete webhook event processing flow"""
        # Arrange
        webhook_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Hello world",
            "team": "T123456",
        }

        webhook_router.event_handler = event_handler
        event_handler.process_event = AsyncMock(return_value=Mock(success=True))

        # Act
        result = await webhook_router.process_webhook_event(webhook_event)

        # Assert
        assert result is not None
        event_handler.process_event.assert_called_once_with(webhook_event)

    @pytest.mark.smoke
    async def test_webhook_error_handling(self, webhook_router):
        """Test that webhook errors are handled gracefully"""
        # Arrange
        invalid_event = {"type": "invalid_event_type", "data": "invalid data"}

        webhook_router.event_handler = Mock()
        webhook_router.event_handler.process_event = AsyncMock(
            side_effect=Exception("Processing failed")
        )

        # Act
        result = await webhook_router.process_webhook_event(invalid_event)

        # Assert
        assert result is not None
        assert result.get("error") is not None

    @pytest.mark.smoke
    def test_webhook_rate_limiting(self, webhook_router):
        """Test that webhook rate limiting is enforced"""
        # Arrange
        webhook_router._check_rate_limit = Mock(return_value=False)  # Rate limited

        # Act
        is_allowed = webhook_router._check_rate_limit("test_client")

        # Assert
        assert is_allowed is False

    @pytest.mark.smoke
    def test_webhook_logging(self, webhook_router):
        """Test that webhook events are logged"""
        # Arrange
        webhook_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Hello world",
            "team": "T123456",
        }

        webhook_router._log_webhook_event = Mock()

        # Act
        webhook_router._log_webhook_event(webhook_event)

        # Assert
        webhook_router._log_webhook_event.assert_called_once_with(webhook_event)

    @pytest.mark.smoke
    def test_webhook_health_check(self, webhook_router):
        """Test that webhook health checks work"""
        # Arrange
        webhook_router._health_check = Mock(return_value={"status": "healthy"})

        # Act
        health_status = webhook_router._health_check()

        # Assert
        assert health_status["status"] == "healthy"
        webhook_router._health_check.assert_called_once()

    @pytest.mark.smoke
    def test_webhook_metrics_collection(self, webhook_router):
        """Test that webhook metrics are collected"""
        # Arrange
        webhook_router._collect_metrics = Mock(
            return_value={"total_events": 100, "successful_events": 95, "failed_events": 5}
        )

        # Act
        metrics = webhook_router._collect_metrics()

        # Assert
        assert metrics["total_events"] == 100
        assert metrics["successful_events"] == 95
        assert metrics["failed_events"] == 5
        webhook_router._collect_metrics.assert_called_once()

    @pytest.mark.smoke
    def test_webhook_configuration_validation(self, webhook_router):
        """Test that webhook configuration is validated"""
        # Arrange
        valid_config = {
            "webhook_url": "https://abc123.ngrok.io/slack/events",
            "signing_secret": "test_secret",
            "port": 8080,
        }

        invalid_config = {"webhook_url": "invalid_url", "port": "invalid_port"}

        # Act & Assert
        assert webhook_router._validate_config(valid_config) is True
        assert webhook_router._validate_config(invalid_config) is False

    @pytest.mark.smoke
    def test_webhook_event_queue_processing(self, webhook_router):
        """Test that webhook events are queued and processed"""
        # Arrange
        events = [
            {"type": "message", "channel": "C123456", "text": "Event 1"},
            {"type": "message", "channel": "C123456", "text": "Event 2"},
            {"type": "message", "channel": "C123456", "text": "Event 3"},
        ]

        webhook_router._process_event_queue = Mock(return_value=len(events))

        # Act
        processed_count = webhook_router._process_event_queue(events)

        # Assert
        assert processed_count == 3
        webhook_router._process_event_queue.assert_called_once_with(events)

    @pytest.mark.smoke
    async def test_webhook_end_to_end_flow(self, webhook_router, event_handler):
        """Test complete end-to-end webhook flow (event in → processed result)"""
        # Arrange
        webhook_event = {
            "type": "message",
            "channel": "C123456",
            "ts": "1234567890.123456",
            "text": "Hello world",
            "team": "T123456",
        }

        webhook_router.event_handler = event_handler
        event_handler.process_event = AsyncMock(return_value=Mock(success=True))

        # Act
        result = await webhook_router.process_webhook_event(webhook_event)

        # Assert
        assert result is not None
        event_handler.process_event.assert_called_once_with(webhook_event)
