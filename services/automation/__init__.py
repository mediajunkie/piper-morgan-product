"""
Intelligent Automation Services for Piper Morgan

CORE-LEARN-E: Intelligent Automation with Safety First

Issue: #225

1613: the former predictive-assistance layer (PredictiveAssistant — read
pattern predictions from the cross-user pooled learning store) was removed
per PM ruling 2026-08-31; the pooled store contradicted published privacy
claims.
"""

from services.automation.action_classifier import (
    ActionClassification,
    ActionClassifier,
    ActionSafetyLevel,
)
from services.automation.audit_trail import AuditTrail, AutomationEvent, get_audit_trail
from services.automation.autonomous_executor import (
    AutonomousExecutor,
    ExecutionResult,
    get_autonomous_executor,
)
from services.automation.emergency_stop import EmergencyStop, get_emergency_stop
from services.automation.user_approval_system import (
    ApprovalRequest,
    ApprovalStatus,
    UserApprovalSystem,
    get_user_approval_system,
)

__all__ = [
    # Safety Controls (Phase 1)
    "ActionClassifier",
    "ActionClassification",
    "ActionSafetyLevel",
    "EmergencyStop",
    "get_emergency_stop",
    "AuditTrail",
    "AutomationEvent",
    "get_audit_trail",
    # Autonomous Execution (Phase 3)
    "AutonomousExecutor",
    "ExecutionResult",
    "get_autonomous_executor",
    "UserApprovalSystem",
    "ApprovalRequest",
    "ApprovalStatus",
    "get_user_approval_system",
]
