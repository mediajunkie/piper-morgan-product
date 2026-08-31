"""
Integration tests for intelligent automation system.

Tests end-to-end automation with all safety controls.

Issue: #225 (CORE-LEARN-E)
"""

import asyncio
from typing import Any, Dict

import pytest

from services.automation.action_classifier import ActionClassifier, ActionSafetyLevel
from services.automation.audit_trail import AuditTrail, get_audit_trail
from services.automation.autonomous_executor import AutonomousExecutor, get_autonomous_executor
from services.automation.emergency_stop import EmergencyStop, get_emergency_stop
from services.automation.user_approval_system import (
    ApprovalStatus,
    UserApprovalSystem,
    get_user_approval_system,
)


class TestIntelligentAutomationIntegration:
    """Integration tests for the complete automation system."""

    @pytest.fixture(autouse=True)
    def setup_and_teardown(self):
        """Setup and teardown for each test."""
        # Get global instances
        emergency_stop = get_emergency_stop()
        audit_trail = get_audit_trail()
        executor = get_autonomous_executor()
        approval_system = get_user_approval_system()

        # Reset state before test
        emergency_stop.reset()
        audit_trail.clear()
        executor.clear_rollback_stack()
        approval_system.clear_history()

        yield

        # Cleanup after test
        emergency_stop.reset()

    @pytest.mark.asyncio
    async def test_end_to_end_safe_automation(self):
        """Test complete automation flow for safe action."""
        executor = get_autonomous_executor()
        audit_trail = get_audit_trail()

        # Define a safe action
        async def fetch_data():
            return {"data": [1, 2, 3], "count": 3}

        # Execute with high confidence
        result = await executor.execute_with_safety(
            action_type="fetch_github_issues",
            action_handler=fetch_data,
            confidence=0.95,
            user_id="test_user",
            context={"repo": "piper-morgan"},
        )

        # Verify execution
        assert result.executed is True
        assert result.safety_level == "safe"
        assert result.confidence == 0.95
        assert result.rollback_available is True
        assert result.result == {"data": [1, 2, 3], "count": 3}

        # Verify audit trail
        events = audit_trail.get_events(event_type="execution")
        assert len(events) > 0
        assert events[0].auto_executed is True
        assert events[0].action_type == "fetch_github_issues"

    @pytest.mark.asyncio
    async def test_destructive_action_never_executes(self):
        """Test that destructive actions NEVER auto-execute."""
        executor = get_autonomous_executor()
        audit_trail = get_audit_trail()

        # Define a destructive action
        async def delete_repo():
            return {"deleted": True}

        # Try to execute with extremely high confidence
        result = await executor.execute_with_safety(
            action_type="delete_github_repo",
            action_handler=delete_repo,
            confidence=0.99,  # Even 99% confidence!
            user_id="test_user",
            context={"repo": "important-repo"},
        )

        # Verify NEVER executed
        assert result.executed is False
        assert result.safety_level == "destructive"
        assert "DESTRUCTIVE" in result.reason
        assert "NEVER" in result.reason

        # Verify audit trail logged the block
        events = audit_trail.get_events(event_type="execution_blocked")
        assert len(events) > 0
        assert events[0].auto_executed is False

    @pytest.mark.asyncio
    async def test_low_confidence_requires_approval(self):
        """Test that low confidence actions require approval."""
        executor = get_autonomous_executor()

        async def safe_action():
            return {"status": "ok"}

        # Execute with low confidence
        result = await executor.execute_with_safety(
            action_type="create_github_issue",
            action_handler=safe_action,
            confidence=0.7,  # Below 0.9 threshold
            user_id="test_user",
            context={},
        )

        # Verify requires approval
        assert result.executed is False
        assert result.requires_approval is True
        assert "Requires approval" in result.reason

    @pytest.mark.asyncio
    async def test_emergency_stop_blocks_all_automation(self):
        """Test that emergency stop blocks ALL automation."""
        executor = get_autonomous_executor()
        emergency_stop = get_emergency_stop()

        # Trigger emergency stop
        emergency_stop.trigger_emergency_stop("Test emergency")

        async def safe_action():
            return {"data": "test"}

        # Try to execute even safe action
        result = await executor.execute_with_safety(
            action_type="fetch_data",
            action_handler=safe_action,
            confidence=0.95,
            user_id="test_user",
            context={},
        )

        # Verify blocked
        assert result.executed is False
        assert "Emergency stop" in result.reason

        # Reset for other tests
        emergency_stop.reset()

    @pytest.mark.asyncio
    async def test_approval_workflow(self):
        """Test complete approval workflow."""
        executor = get_autonomous_executor()
        approval_system = get_user_approval_system()

        # Create approval request
        request = await approval_system.request_approval(
            user_id="test_user",
            action_type="publish_package",
            confidence=0.85,
            safety_level="DESTRUCTIVE",
            context={"package": "piper-cli"},
        )

        # Verify request created
        assert request.status == ApprovalStatus.PENDING

        # Get pending requests
        pending = approval_system.get_pending_requests("test_user")
        assert len(pending) == 1
        assert pending[0].action_type == "publish_package"

        # Approve request
        approved = approval_system.approve_request(request.request_id, reason="Verified safe")
        assert approved.status == ApprovalStatus.APPROVED

        # Verify moved to history
        pending_after = approval_system.get_pending_requests("test_user")
        assert len(pending_after) == 0

        history = approval_system.get_approval_history("test_user")
        assert len(history) == 1
        assert history[0].status == ApprovalStatus.APPROVED

    @pytest.mark.asyncio
    async def test_action_classification(self):
        """Test action safety classification."""
        classifier = ActionClassifier()

        # Test safe action
        safe_class = classifier.classify_action("fetch_github_issues")
        assert safe_class.safety_level == ActionSafetyLevel.SAFE
        assert not safe_class.requires_confirmation

        # Test destructive action
        destructive_class = classifier.classify_action("delete_github_repo")
        assert destructive_class.safety_level == ActionSafetyLevel.DESTRUCTIVE
        assert destructive_class.requires_confirmation

        # Test confirmation action
        confirm_class = classifier.classify_action("create_github_issue")
        assert confirm_class.safety_level == ActionSafetyLevel.REQUIRES_CONFIRMATION
        assert confirm_class.requires_confirmation

    @pytest.mark.asyncio
    async def test_auto_execution_safety_threshold(self):
        """Test that auto-execution requires both SAFE classification AND high confidence."""
        classifier = ActionClassifier()

        # SAFE + high confidence = auto-execute
        assert classifier.is_safe_for_auto_execution("fetch_data", 0.95) is True

        # SAFE + low confidence = manual
        assert classifier.is_safe_for_auto_execution("fetch_data", 0.7) is False

        # DESTRUCTIVE + high confidence = NEVER
        assert classifier.is_safe_for_auto_execution("delete_data", 0.99) is False

        # REQUIRES_CONFIRMATION + high confidence = manual
        assert classifier.is_safe_for_auto_execution("create_issue", 0.95) is False

    @pytest.mark.asyncio
    async def test_rollback_capability(self):
        """Test that executed actions can be rolled back."""
        executor = get_autonomous_executor()

        async def action_with_rollback():
            return {"created_id": "12345", "status": "created"}

        # Execute action
        result = await executor.execute_with_safety(
            action_type="fetch_report",
            action_handler=action_with_rollback,
            confidence=0.95,
            user_id="test_user",
            context={},
        )

        assert result.executed is True
        assert result.rollback_available is True

        # Verify rollback info
        rollback_info = executor.get_rollback_info()
        assert len(rollback_info) == 1
        assert rollback_info[0]["action_type"] == "fetch_report"

    @pytest.mark.asyncio
    async def test_audit_trail_completeness(self):
        """Test that audit trail logs all automation events."""
        executor = get_autonomous_executor()
        audit_trail = get_audit_trail()

        async def test_action():
            return {"success": True}

        # Execute multiple actions
        await executor.execute_with_safety("fetch_data", test_action, 0.95, "user1", {})
        await executor.execute_with_safety("delete_data", test_action, 0.95, "user1", {})  # Blocked
        await executor.execute_with_safety(
            "create_issue", test_action, 0.7, "user1", {}
        )  # Low confidence

        # Get all events
        all_events = audit_trail.get_events(limit=100)
        assert len(all_events) >= 3

        # Verify event types
        event_types = [e.event_type for e in all_events]
        assert "execution" in event_types  # fetch_data executed
        assert "execution_blocked" in event_types  # delete_data blocked
        assert "approval_required" in event_types  # create_issue needs approval

        # Get statistics
        stats = audit_trail.get_automation_statistics()
        assert stats["total_events"] >= 3

    @pytest.mark.asyncio
    async def test_concurrent_safety(self):
        """Test that safety controls work under concurrent execution."""
        executor = get_autonomous_executor()

        async def concurrent_action(action_id: int):
            await asyncio.sleep(0.01)  # Simulate async work
            return {"action_id": action_id}

        # Execute multiple actions concurrently
        tasks = [
            executor.execute_with_safety(
                f"fetch_data_{i}",
                lambda i=i: concurrent_action(i),
                0.95,
                "test_user",
                {},
            )
            for i in range(5)
        ]

        results = await asyncio.gather(*tasks)

        # All should execute (all SAFE with high confidence)
        executed_count = sum(1 for r in results if r.executed)
        assert executed_count == 5

    @pytest.mark.asyncio
    async def test_user_approval_preferences(self):
        """Test user-specific approval preferences."""
        approval_system = get_user_approval_system()

        # Set preferences
        await approval_system.set_automation_preferences(
            user_id="test_user",
            enabled=True,
            min_confidence=0.8,
            auto_approve_actions={"fetch_github_issues"},
        )

        # Note: Actual auto-approval will depend on UserPreferenceManager
        # persistence, which requires database in production.
        # This test verifies the API works correctly.
        stats = approval_system.get_approval_statistics("test_user")
        assert stats["pending_count"] == 0  # No pending requests yet

    @pytest.mark.asyncio
    async def test_emergency_stop_recovery(self):
        """Test that system can recover from emergency stop."""
        executor = get_autonomous_executor()
        emergency_stop = get_emergency_stop()

        async def test_action():
            return {"status": "ok"}

        # Normal execution works
        result1 = await executor.execute_with_safety("fetch_data", test_action, 0.95, "user1", {})
        assert result1.executed is True

        # Trigger emergency stop
        emergency_stop.trigger_emergency_stop("Test stop")

        # Execution blocked
        result2 = await executor.execute_with_safety("fetch_data", test_action, 0.95, "user1", {})
        assert result2.executed is False

        # Reset emergency stop
        emergency_stop.reset()

        # Execution works again
        result3 = await executor.execute_with_safety("fetch_data", test_action, 0.95, "user1", {})
        assert result3.executed is True

    @pytest.mark.asyncio
    async def test_approval_statistics(self):
        """Test approval statistics calculation."""
        approval_system = get_user_approval_system()

        # Create and approve some requests
        req1 = await approval_system.request_approval("user1", "action1", 0.8, "SAFE", {})
        approval_system.approve_request(req1.request_id)

        req2 = await approval_system.request_approval("user1", "action2", 0.8, "SAFE", {})
        approval_system.reject_request(req2.request_id)

        req3 = await approval_system.request_approval("user1", "action3", 0.8, "SAFE", {})
        approval_system.approve_request(req3.request_id)

        # Get statistics
        stats = approval_system.get_approval_statistics("user1")
        assert stats["total_requests"] == 3
        assert stats["approved_count"] == 2
        assert stats["rejected_count"] == 1
        assert stats["approval_rate"] == pytest.approx(2 / 3)


if __name__ == "__main__":
    # Run tests manually
    pytest.main([__file__, "-v"])
