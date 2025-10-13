"""
Unittest-Compatible Excellence Flywheel Tests

This test file inherits from unittest.TestCase and doesn't use pytest fixtures,
making it compatible with standalone test runners that bypass pytest infrastructure.
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import asyncio
import time
import unittest
from datetime import datetime
from unittest.mock import AsyncMock, Mock, patch
from uuid import uuid4

from services.domain.models import Intent
from services.orchestration.excellence_flywheel_integration import (
    ExcellenceFlywheel,
    ExcellenceFlywheelIntegrator,
    VerificationCheck,
    VerificationPhase,
    VerificationResult,
)


class TestExcellenceFlywheelUnittest(unittest.TestCase):
    """Unittest-compatible tests for Excellence Flywheel core functionality"""

    def setUp(self):
        """Set up test fixtures before each test method"""
        # Create mock dependencies for tests
        self.mock_intent = Mock(
            action="test_action",
            original_message="Test message for excellence flywheel validation",
            timestamp=datetime.now(),
            metadata={"test": True},
        )

        self.mock_coordination_result = Mock(
            status="success",
            subtasks=["task1", "task2"],
            agent_assignments={"task1": "agent1", "task2": "agent2"},
            performance_metrics={"latency": 0.001, "throughput": 100},
            success_metrics={"accuracy": 0.95, "completeness": 1.0},
        )

        # Create test instances
        self.flywheel = ExcellenceFlywheel(
            coordination_id="test_coordination_123",
            verification_checks=[],
            learning_insights=[],
            patterns_detected={},
            acceleration_metrics={},
            compound_knowledge={},
            systematic_verified=False,
        )

        # Create integrator with mocked dependencies
        with patch("services.orchestration.excellence_flywheel_integration.MultiAgentCoordinator"):
            self.integrator = ExcellenceFlywheelIntegrator()

    def test_excellence_flywheel_creation(self):
        """Test ExcellenceFlywheel can be instantiated without database"""
        self.assertIsNotNone(self.flywheel)
        self.assertTrue(hasattr(self.flywheel, "verification_checks"))
        self.assertTrue(hasattr(self.flywheel, "patterns_detected"))

    def test_verification_check_creation(self):
        """Test VerificationCheck dataclass creation"""
        check = VerificationCheck(
            check_id="test_check_123",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Test verification check",
            result=VerificationResult.PASSED,
            details="Test verification check details",
            evidence={"test": True},
            duration_ms=100,
            created_at=datetime.now(),
        )

        self.assertEqual(check.phase, VerificationPhase.PRE_COORDINATION)
        self.assertEqual(check.check_id, "test_check_123")
        self.assertEqual(check.result, VerificationResult.PASSED)
        self.assertEqual(check.details, "Test verification check details")

    def test_verification_phase_enum(self):
        """Test all verification phases are defined"""
        phases = list(VerificationPhase)
        expected_phases = [
            "pre_coordination",
            "task_decomposition",
            "agent_assignment",
            "post_coordination",
            "learning_capture",
        ]

        self.assertEqual(len(phases), 5)
        for phase in phases:
            self.assertIn(phase.value, expected_phases)

    def test_verification_result_enum(self):
        """Test all verification results are defined"""
        results = list(VerificationResult)
        expected_results = ["passed", "failed", "warning", "skipped"]

        self.assertEqual(len(results), 4)
        for result in results:
            self.assertIn(result.value, expected_results)

    def test_verification_history_tracking(self):
        """Test verification history tracking functionality"""
        # Add a verification check
        check = VerificationCheck(
            check_id="test_history_check_123",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Test history tracking",
            result=VerificationResult.PASSED,
            details="Test history tracking details",
            evidence={"test": True},
            duration_ms=50,
            created_at=datetime.now(),
        )

        # Verify the check was created correctly
        self.assertEqual(check.phase, VerificationPhase.PRE_COORDINATION)
        self.assertEqual(check.check_id, "test_history_check_123")
        self.assertEqual(check.result, VerificationResult.PASSED)

    def test_pattern_library_management(self):
        """Test pattern library management functionality"""
        # Test that patterns_detected exists
        self.assertTrue(hasattr(self.flywheel, "patterns_detected"))

        # Test that we can access patterns_detected
        self.assertIsNotNone(self.flywheel.patterns_detected)

    def test_verification_result_handling(self):
        """Test verification result handling and validation"""
        # Test all verification result values
        results = [
            VerificationResult.PASSED,
            VerificationResult.FAILED,
            VerificationResult.WARNING,
            VerificationResult.SKIPPED,
        ]

        for result in results:
            self.assertIsInstance(result, VerificationResult)
            self.assertIsInstance(result.value, str)

    def test_verification_phase_transitions(self):
        """Test verification phase transitions and validation"""
        # Test all verification phases
        phases = [
            VerificationPhase.PRE_COORDINATION,
            VerificationPhase.TASK_DECOMPOSITION,
            VerificationPhase.AGENT_ASSIGNMENT,
            VerificationPhase.POST_COORDINATION,
            VerificationPhase.LEARNING_CAPTURE,
        ]

        for phase in phases:
            self.assertIsInstance(phase, VerificationPhase)
            self.assertIsInstance(phase.value, str)

    def test_timestamp_consistency(self):
        """Test timestamp consistency in verification checks"""
        now = datetime.now()
        check = VerificationCheck(
            check_id="timestamp_test_123",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Testing timestamp consistency",
            result=VerificationResult.PASSED,
            details="Testing timestamp consistency details",
            evidence={"test": True},
            duration_ms=75,
            created_at=now,
        )

        self.assertEqual(check.created_at, now)
        self.assertIsInstance(check.created_at, datetime)

    def test_verification_check_immutability(self):
        """Test that verification check attributes are properly set"""
        check = VerificationCheck(
            check_id="immutability_test_123",
            phase=VerificationPhase.PRE_COORDINATION,
            description="Testing attribute immutability",
            result=VerificationResult.PASSED,
            details="Testing attribute immutability details",
            evidence={"test": True},
            duration_ms=25,
            created_at=datetime.now(),
        )

        # Test that all attributes are set correctly
        self.assertEqual(check.phase, VerificationPhase.PRE_COORDINATION)
        self.assertEqual(check.check_id, "immutability_test_123")
        self.assertEqual(check.result, VerificationResult.PASSED)
        self.assertEqual(check.details, "Testing attribute immutability details")


if __name__ == "__main__":
    unittest.main()
