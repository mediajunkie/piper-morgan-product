"""
PM-087 BoundaryEnforcer Integration Tests
Comprehensive testing of BoundaryEnforcer service and middleware integration
"""

import asyncio
import json
from datetime import datetime
from typing import Any, Dict
from unittest.mock import AsyncMock, Mock, patch

import pytest
from fastapi import Request

from services.domain.models import BoundaryViolation, EthicalDecision
from services.ethics.boundary_enforcer import BoundaryDecision, BoundaryEnforcer, BoundaryType
from services.infrastructure.monitoring.ethics_metrics import ethics_metrics


class TestBoundaryEnforcer:
    """Test BoundaryEnforcer service functionality"""

    @pytest.fixture
    def boundary_enforcer(self):
        """Provide BoundaryEnforcer instance for tests"""
        return BoundaryEnforcer()

    @pytest.fixture
    def mock_request(self):
        """Provide mock FastAPI request for tests"""
        request = Mock(spec=Request)
        request.headers = {"X-Session-ID": "test_session_123"}
        request.url.path = "/api/test"
        request.method = "POST"
        return request

    @pytest.mark.asyncio
    async def test_enforce_boundaries_no_violation(self, boundary_enforcer, mock_request):
        """Test boundary enforcement with no violation"""
        # Mock request body
        mock_request.body = AsyncMock(return_value=b"Normal content")

        # Perform boundary enforcement
        decision = await boundary_enforcer.enforce_boundaries(mock_request)

        # Validate decision
        assert isinstance(decision, BoundaryDecision)
        assert decision.violation_detected is False
        assert decision.boundary_type == "none"
        assert "content_length" in decision.audit_data
        assert "response_time_ms" in decision.audit_data

    @pytest.mark.asyncio
    async def test_enforce_boundaries_harassment_violation(self, boundary_enforcer, mock_request):
        """Test boundary enforcement with harassment violation"""
        # Mock request body with harassment content
        mock_request.body = AsyncMock(return_value=b"This is harassment content")

        # Perform boundary enforcement
        decision = await boundary_enforcer.enforce_boundaries(mock_request)

        # Validate decision
        assert isinstance(decision, BoundaryDecision)
        assert decision.violation_detected is True
        assert decision.boundary_type == BoundaryType.HARASSMENT
        assert "harassment" in decision.explanation.lower()

    @pytest.mark.asyncio
    async def test_enforce_boundaries_professional_violation(self, boundary_enforcer, mock_request):
        """Test boundary enforcement with professional boundary violation"""
        # Mock request body with personal content
        mock_request.body = AsyncMock(return_value=b"Personal relationship content")

        # Perform boundary enforcement
        decision = await boundary_enforcer.enforce_boundaries(mock_request)

        # Validate decision
        assert isinstance(decision, BoundaryDecision)
        assert decision.violation_detected is True
        assert decision.boundary_type == BoundaryType.PROFESSIONAL
        assert "professional" in decision.explanation.lower()

    @pytest.mark.asyncio
    async def test_enforce_boundaries_inappropriate_content(self, boundary_enforcer, mock_request):
        """Test boundary enforcement with inappropriate content"""
        # Mock request body with inappropriate content
        mock_request.body = AsyncMock(return_value=b"Explicit sexual content")

        # Perform boundary enforcement
        decision = await boundary_enforcer.enforce_boundaries(mock_request)

        # Validate decision
        assert isinstance(decision, BoundaryDecision)
        assert decision.violation_detected is True
        assert decision.boundary_type == BoundaryType.INAPPROPRIATE_CONTENT
        assert "inappropriate" in decision.explanation.lower()

    @pytest.mark.asyncio
    async def test_validate_professional_boundaries(self, boundary_enforcer):
        """Test professional boundary validation"""
        # Test professional boundary violation
        result = await boundary_enforcer.validate_professional_boundaries(
            "Personal relationship content"
        )
        assert result is True

        # Test normal content
        result = await boundary_enforcer.validate_professional_boundaries("Normal work content")
        assert result is False

    @pytest.mark.asyncio
    async def test_check_harassment_patterns(self, boundary_enforcer):
        """Test harassment pattern detection"""
        # Test harassment content
        result = await boundary_enforcer.check_harassment_patterns("This is harassment")
        assert result is True

        # Test normal content
        result = await boundary_enforcer.check_harassment_patterns("Normal conversation")
        assert result is False

    @pytest.mark.asyncio
    async def test_check_inappropriate_content(self, boundary_enforcer):
        """Test inappropriate content detection"""
        # Test inappropriate content
        result = await boundary_enforcer.check_inappropriate_content("Explicit sexual content")
        assert result is True

        # Test normal content
        result = await boundary_enforcer.check_inappropriate_content("Normal content")
        assert result is False

    @pytest.mark.asyncio
    async def test_audit_decision(self, boundary_enforcer):
        """Test decision auditing"""
        # Create test decision
        decision = EthicalDecision(
            decision_id="test_decision_123",
            boundary_type="test_boundary",
            violation_detected=True,
            explanation="Test violation",
            audit_data={"test": "data"},
            session_id="test_session",
        )

        # Audit decision
        await boundary_enforcer.audit_decision(decision)

        # Verify audit was recorded (metrics should be updated)
        assert ethics_metrics.audit_trail_entries_total > 0

    @pytest.mark.asyncio
    async def test_extract_content_from_request(self, boundary_enforcer, mock_request):
        """Test content extraction from request"""
        # Mock request body
        mock_request.body = AsyncMock(return_value=b"Test content")

        # Extract content
        content = await boundary_enforcer._extract_content_from_request(mock_request)

        # Validate content
        assert content == "Test content"

    @pytest.mark.asyncio
    async def test_get_session_id_from_request(self, boundary_enforcer, mock_request):
        """Test session ID extraction from request"""
        # Test with session ID in headers
        session_id = boundary_enforcer._get_session_id_from_request(mock_request)
        assert session_id == "test_session_123"

        # Test without session ID
        mock_request.headers = {}
        session_id = boundary_enforcer._get_session_id_from_request(mock_request)
        assert session_id is None

    @pytest.mark.asyncio
    async def test_map_boundary_type_to_violation_type(self, boundary_enforcer):
        """Test boundary type to violation type mapping"""
        # Test harassment mapping
        violation_type = boundary_enforcer._map_boundary_type_to_violation_type(
            BoundaryType.HARASSMENT
        )
        assert violation_type.value == "harassment_attempt"

        # Test professional mapping
        violation_type = boundary_enforcer._map_boundary_type_to_violation_type(
            BoundaryType.PROFESSIONAL
        )
        assert violation_type.value == "professional_boundary_violation"

        # Test unknown mapping (should default to professional)
        violation_type = boundary_enforcer._map_boundary_type_to_violation_type("unknown")
        assert violation_type.value == "professional_boundary_violation"


class TestEthicalDecisionDomainModel:
    """Test EthicalDecision domain model"""

    def test_ethical_decision_creation(self):
        """Test EthicalDecision model creation"""
        decision = EthicalDecision(
            decision_id="test_123",
            boundary_type="professional",
            violation_detected=True,
            explanation="Test violation",
            audit_data={"test": "data"},
            session_id="test_session",
        )

        # Validate fields
        assert decision.decision_id == "test_123"
        assert decision.boundary_type == "professional"
        assert decision.violation_detected is True
        assert decision.explanation == "Test violation"
        assert decision.audit_data == {"test": "data"}
        assert decision.session_id == "test_session"
        assert isinstance(decision.timestamp, datetime)

    def test_ethical_decision_to_dict(self):
        """Test EthicalDecision serialization"""
        decision = EthicalDecision(
            decision_id="test_123",
            boundary_type="professional",
            violation_detected=True,
            explanation="Test violation",
            audit_data={"test": "data"},
            session_id="test_session",
        )

        # Convert to dictionary
        decision_dict = decision.to_dict()

        # Validate serialization
        assert decision_dict["decision_id"] == "test_123"
        assert decision_dict["boundary_type"] == "professional"
        assert decision_dict["violation_detected"] is True
        assert decision_dict["explanation"] == "Test violation"
        assert decision_dict["audit_data"] == {"test": "data"}
        assert decision_dict["session_id"] == "test_session"
        assert "timestamp" in decision_dict


class TestBoundaryViolationDomainModel:
    """Test BoundaryViolation domain model"""

    def test_boundary_violation_creation(self):
        """Test BoundaryViolation model creation"""
        violation = BoundaryViolation(
            violation_id="violation_123",
            violation_type="harassment",
            context="Test harassment content",
            session_id="test_session",
            severity="high",
        )

        # Validate fields
        assert violation.violation_id == "violation_123"
        assert violation.violation_type == "harassment"
        assert violation.context == "Test harassment content"
        assert violation.session_id == "test_session"
        assert violation.severity == "high"
        assert isinstance(violation.timestamp, datetime)
        assert violation.audit_data == {}

    def test_boundary_violation_to_dict(self):
        """Test BoundaryViolation serialization"""
        violation = BoundaryViolation(
            violation_id="violation_123",
            violation_type="harassment",
            context="Test harassment content",
            session_id="test_session",
            severity="high",
        )

        # Convert to dictionary
        violation_dict = violation.to_dict()

        # Validate serialization
        assert violation_dict["violation_id"] == "violation_123"
        assert violation_dict["violation_type"] == "harassment"
        assert violation_dict["context"] == "Test harassment content"
        assert violation_dict["session_id"] == "test_session"
        assert violation_dict["severity"] == "high"
        assert "timestamp" in violation_dict
        assert violation_dict["audit_data"] == {}


class TestBoundaryEnforcerIntegration:
    """Integration tests for BoundaryEnforcer with real components"""

    @pytest.mark.asyncio
    async def test_boundary_enforcer_with_metrics_integration(self):
        """Test BoundaryEnforcer integration with ethics metrics"""
        # Reset metrics for clean test
        ethics_metrics._instance = None
        ethics_metrics._init_metrics()

        # Create boundary enforcer
        enforcer = BoundaryEnforcer()

        # Create mock request with violation
        request = Mock(spec=Request)
        request.body = AsyncMock(return_value=b"This is harassment content")
        request.headers = {"X-Session-ID": "test_session"}
        request.url.path = "/api/test"

        # Perform boundary enforcement
        decision = await enforcer.enforce_boundaries(request)

        # Validate decision
        assert decision.violation_detected is True
        assert decision.boundary_type == BoundaryType.HARASSMENT

        # Validate metrics were recorded
        assert ethics_metrics.ethics_decisions_total > 0
        assert ethics_metrics.boundary_violations_total > 0
        assert len(ethics_metrics.boundary_violations_recent) > 0

    @pytest.mark.asyncio
    async def test_boundary_enforcer_performance(self):
        """Test BoundaryEnforcer performance characteristics"""
        enforcer = BoundaryEnforcer()

        # Create mock request
        request = Mock(spec=Request)
        request.body = AsyncMock(return_value=b"Normal content")
        request.headers = {"X-Session-ID": "test_session"}

        # Measure performance
        start_time = datetime.now()
        decision = await enforcer.enforce_boundaries(request)
        end_time = datetime.now()

        # Calculate response time
        response_time_ms = (end_time - start_time).total_seconds() * 1000

        # Validate performance (should be under 100ms)
        assert response_time_ms < 100

        # Validate decision
        assert decision.violation_detected is False
        assert "response_time_ms" in decision.audit_data
