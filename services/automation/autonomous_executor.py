"""
Autonomous execution engine for intelligent automation.

SAFETY FIRST: Brings together all safety controls to enable safe autonomous execution.

Issue: #225 (CORE-LEARN-E)
"""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Awaitable, Callable, Dict, List, Optional
from uuid import UUID

from services.automation.action_classifier import ActionClassifier, ActionSafetyLevel
from services.automation.audit_trail import get_audit_trail
from services.automation.emergency_stop import get_emergency_stop


@dataclass
class ExecutionResult:
    """Result of an autonomous execution attempt."""

    action_type: str
    executed: bool
    result: Optional[Any]
    reason: str
    confidence: float
    safety_level: str
    requires_approval: bool
    timestamp: datetime
    rollback_available: bool


class AutonomousExecutor:
    """
    Autonomous execution engine with safety-first approach.

    CRITICAL SAFETY RULES:
    1. NEVER auto-execute destructive actions (delete, publish, deploy, etc.)
    2. ALWAYS require confirmation for publishes
    3. Only auto-execute SAFE actions with confidence >= 0.9
    4. Check emergency stop before every execution
    5. Audit trail for ALL automation

    Integrates:
    - ActionClassifier (safety classification)
    - EmergencyStop (halt capability)
    - AuditTrail (comprehensive logging)

    1613: the former PredictiveAssistant integration (pattern-based predictions
    read from the cross-user pooled learning store) was severed per PM ruling
    2026-08-31 — the pooled store contradicted published privacy claims.
    """

    def __init__(self):
        self.classifier = ActionClassifier()
        self.emergency_stop = get_emergency_stop()
        self.audit_trail = get_audit_trail()

        # Rollback stack for undo capability
        self._rollback_stack: List[Dict] = []

    async def execute_with_safety(
        self,
        action_type: str,
        action_handler: Callable[..., Awaitable[Any]],
        confidence: float,
        user_id: UUID,
        context: Optional[Dict] = None,
        auto_approve: bool = False,
    ) -> ExecutionResult:
        """
        Execute action with comprehensive safety checks.

        Args:
            action_type: Type of action (e.g., "create_github_issue")
            action_handler: Async function that performs the action
            confidence: Confidence score (0-1)
            user_id: User ID for audit trail
            context: Additional context for safety checks
            auto_approve: Override for testing (USE WITH EXTREME CAUTION)

        Returns:
            ExecutionResult with execution status and details

        SAFETY GUARANTEES:
        - NEVER executes destructive actions autonomously
        - Checks emergency stop before execution
        - Logs ALL execution attempts
        - Validates confidence thresholds
        """
        timestamp = datetime.now(timezone.utc)

        # SAFETY CHECK 1: Emergency stop
        if self.emergency_stop.is_stopped():
            result = ExecutionResult(
                action_type=action_type,
                executed=False,
                result=None,
                reason="Emergency stop active - automation halted",
                confidence=confidence,
                safety_level="BLOCKED",
                requires_approval=True,
                timestamp=timestamp,
                rollback_available=False,
            )

            # Log to audit trail
            self.audit_trail.log_event(
                event_type="execution_blocked",
                action_type=action_type,
                confidence=confidence,
                safety_level="EMERGENCY_STOP",
                auto_executed=False,
                user_id=user_id,
                result="blocked_by_emergency_stop",
                details=context or {},
            )

            return result

        # SAFETY CHECK 2: Action classification
        classification = self.classifier.classify_action(action_type, context)

        # SAFETY CHECK 3: Confidence and safety level validation
        can_auto_execute = self.classifier.is_safe_for_auto_execution(
            action_type, confidence, context
        )

        # SAFETY CHECK 4: NEVER auto-execute destructive actions
        if classification.safety_level == ActionSafetyLevel.DESTRUCTIVE:
            result = ExecutionResult(
                action_type=action_type,
                executed=False,
                result=None,
                reason=f"DESTRUCTIVE action - NEVER auto-executed: {classification.reason}",
                confidence=confidence,
                safety_level=classification.safety_level.value,
                requires_approval=True,
                timestamp=timestamp,
                rollback_available=False,
            )

            # Log to audit trail
            self.audit_trail.log_event(
                event_type="execution_blocked",
                action_type=action_type,
                confidence=confidence,
                safety_level=classification.safety_level.value,
                auto_executed=False,
                user_id=user_id,
                result="destructive_action_blocked",
                details={"classification": classification.reason, **(context or {})},
            )

            return result

        # Decision: Can we auto-execute?
        if can_auto_execute or auto_approve:
            # EXECUTE THE ACTION
            try:
                # Register operation with emergency stop
                operation_id = f"{action_type}_{timestamp.isoformat()}"
                self.emergency_stop.register_operation(operation_id)

                # Execute action
                action_result = await action_handler()

                # Unregister operation
                self.emergency_stop.unregister_operation(operation_id)

                # Store for rollback
                self._rollback_stack.append(
                    {
                        "action_type": action_type,
                        "timestamp": timestamp,
                        "result": action_result,
                        "context": context,
                    }
                )

                result = ExecutionResult(
                    action_type=action_type,
                    executed=True,
                    result=action_result,
                    reason=f"Auto-executed (confidence={confidence:.2f}, safety={classification.safety_level.value})",
                    confidence=confidence,
                    safety_level=classification.safety_level.value,
                    requires_approval=False,
                    timestamp=timestamp,
                    rollback_available=True,
                )

                # Log to audit trail
                self.audit_trail.log_event(
                    event_type="execution",
                    action_type=action_type,
                    confidence=confidence,
                    safety_level=classification.safety_level.value,
                    auto_executed=True,
                    user_id=user_id,
                    result="success",
                    details={
                        "classification": classification.reason,
                        "result": str(action_result)[:200],  # Truncate for logging
                        **(context or {}),
                    },
                )

                return result

            except Exception as e:
                # Execution failed
                self.emergency_stop.unregister_operation(operation_id)

                result = ExecutionResult(
                    action_type=action_type,
                    executed=False,
                    result=None,
                    reason=f"Execution failed: {str(e)}",
                    confidence=confidence,
                    safety_level=classification.safety_level.value,
                    requires_approval=False,
                    timestamp=timestamp,
                    rollback_available=False,
                )

                # Log to audit trail
                self.audit_trail.log_event(
                    event_type="execution_failed",
                    action_type=action_type,
                    confidence=confidence,
                    safety_level=classification.safety_level.value,
                    auto_executed=True,
                    user_id=user_id,
                    result="error",
                    details={"error": str(e), **(context or {})},
                )

                return result

        else:
            # Cannot auto-execute - requires approval
            result = ExecutionResult(
                action_type=action_type,
                executed=False,
                result=None,
                reason=f"Requires approval: {classification.reason} (confidence={confidence:.2f})",
                confidence=confidence,
                safety_level=classification.safety_level.value,
                requires_approval=True,
                timestamp=timestamp,
                rollback_available=False,
            )

            # Log to audit trail
            self.audit_trail.log_event(
                event_type="approval_required",
                action_type=action_type,
                confidence=confidence,
                safety_level=classification.safety_level.value,
                auto_executed=False,
                user_id=user_id,
                result="awaiting_approval",
                details={"classification": classification.reason, **(context or {})},
            )

            return result

    def get_rollback_info(self) -> List[Dict]:
        """
        Get rollback information for recent actions.

        Returns:
            List of rollback-able actions
        """
        return self._rollback_stack.copy()

    def clear_rollback_stack(self):
        """Clear rollback stack (for testing)."""
        self._rollback_stack.clear()


# Global autonomous executor instance
_autonomous_executor: Optional[AutonomousExecutor] = None


def get_autonomous_executor() -> AutonomousExecutor:
    """Get global autonomous executor instance."""
    global _autonomous_executor
    if _autonomous_executor is None:
        _autonomous_executor = AutonomousExecutor()
    return _autonomous_executor
