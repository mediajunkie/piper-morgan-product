"""
Action classification for intelligent automation safety.

Classifies actions as SAFE or DESTRUCTIVE to prevent auto-execution of
dangerous operations.

Issue: #225 (CORE-LEARN-E)
"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, Optional


class ActionSafetyLevel(Enum):
    """Safety classification for actions."""

    SAFE = "safe"  # Auto-executable with high confidence
    REQUIRES_CONFIRMATION = "confirmation"  # Needs user approval
    DESTRUCTIVE = "destructive"  # NEVER auto-execute


@dataclass
class ActionClassification:
    """Classification result for an action."""

    action_type: str
    safety_level: ActionSafetyLevel
    reason: str
    requires_confirmation: bool


class ActionClassifier:
    """
    Classifies actions by safety level for automation decisions.

    CRITICAL SAFETY RULES:
    1. NEVER auto-execute destructive actions (delete, publish, deploy)
    2. ALWAYS require confirmation for publishes
    3. Only auto-execute truly safe operations
    """

    def __init__(self):
        # Destructive actions - NEVER auto-execute
        self._destructive_actions = {
            "delete",
            "remove",
            "destroy",
            "drop",
            "truncate",
            "publish",
            "deploy",
            "release",
            "merge",
            "push",
            "execute",
            "run",
            "start",
            "stop",
            "restart",
            "modify",
            "update",
            "change",
            "alter",
            "edit",
        }

        # Safe actions - Can auto-execute with high confidence
        self._safe_actions = {
            "read",
            "get",
            "fetch",
            "list",
            "search",
            "query",
            "view",
            "show",
            "display",
            "preview",
            "check",
            "validate",
            "verify",
            "test",
            "analyze",
        }

        # Confirmation actions - Need user approval.
        # #1210: "close"/"reopen" added — these mutating GitHub verbs were in no
        # list, so close_issue_query / reopen_issue_query fell through to the safe
        # "query" substring and were auto-executable. Matched as exact tokens
        # (see classify_action) so they're not fooled by the "_query" suffix.
        self._confirmation_actions = {
            "create",
            "add",
            "insert",
            "post",
            "send",
            "assign",
            "label",
            "tag",
            "comment",
            "reply",
            "close",
            "reopen",
        }

    def classify_action(
        self, action_type: str, context: Optional[Dict] = None
    ) -> ActionClassification:
        """
        Classify action by safety level.

        Args:
            action_type: Type of action (e.g., "create_github_issue")
            context: Additional context for classification

        Returns:
            ActionClassification with safety level and requirements
        """
        action_lower = action_type.lower()
        # #1210: action names are {verb}_{object}[_query]. The "_query" suffix is a
        # ROUTING convention, not a safety signal — but it contains the SAFE
        # keyword "query", so a plain substring scan green-lit mutating actions
        # (close_issue_query / reopen_issue_query / comment_issue_query) for
        # autonomous execution. Fix: match CONFIRMATION (mutating) verbs as exact
        # underscore-delimited TOKENS and check them BEFORE the safe scan, so the
        # leading verb decides and "query" can't pre-empt a mutating verb. Safe
        # stays a substring fallback so verb-less reads (attention_query,
        # shipped_query) still classify SAFE via the "query" token. Destructive
        # stays a broad substring scan — never-auto-execute should err broad.
        tokens = set(action_lower.split("_"))

        # 1) Destructive (broad substring) — NEVER auto-execute.
        for keyword in self._destructive_actions:
            if keyword in action_lower:
                return ActionClassification(
                    action_type=action_type,
                    safety_level=ActionSafetyLevel.DESTRUCTIVE,
                    reason=f"Contains destructive keyword: {keyword}",
                    requires_confirmation=True,  # Actually, NEVER auto-execute
                )

        # 2) Confirmation (exact token) — mutating verbs the "_query" suffix masks.
        #    Checked BEFORE safe so e.g. comment_issue_query → confirmation, not
        #    SAFE-via-"query". Token (not substring) so list_labels_query's
        #    "labels" token never matches the "label" verb.
        for keyword in self._confirmation_actions:
            if keyword in tokens:
                return ActionClassification(
                    action_type=action_type,
                    safety_level=ActionSafetyLevel.REQUIRES_CONFIRMATION,
                    reason=f"Contains confirmation verb: {keyword}",
                    requires_confirmation=True,
                )

        # 3) Safe (exact token) — read/list/get/query/... reads. Token (not
        #    substring) so a safe keyword embedded in a non-read word doesn't
        #    falsely green-light it (e.g. "widget" contains "get", "blacklist"
        #    contains "list"). All allow-listed reads carry a real safe token
        #    (list/get/query), so this keeps them SAFE while closing the
        #    false-positive that substring matching opened.
        for keyword in self._safe_actions:
            if keyword in tokens:
                return ActionClassification(
                    action_type=action_type,
                    safety_level=ActionSafetyLevel.SAFE,
                    reason=f"Contains safe keyword: {keyword}",
                    requires_confirmation=False,
                )

        # Default to requiring confirmation if unsure
        return ActionClassification(
            action_type=action_type,
            safety_level=ActionSafetyLevel.REQUIRES_CONFIRMATION,
            reason="Unknown action type - defaulting to safe",
            requires_confirmation=True,
        )

    def is_safe_for_auto_execution(
        self, action_type: str, confidence: float, context: Optional[Dict] = None
    ) -> bool:
        """
        Determine if action is safe for autonomous execution.

        Args:
            action_type: Type of action
            confidence: Confidence score (0-1)
            context: Additional context

        Returns:
            True if safe for auto-execution, False otherwise

        CRITICAL: Returns False for ANY destructive action regardless of confidence!
        """
        classification = self.classify_action(action_type, context)

        # NEVER auto-execute destructive actions
        if classification.safety_level == ActionSafetyLevel.DESTRUCTIVE:
            return False

        # Only auto-execute if confidence is high enough AND action is safe
        if classification.safety_level == ActionSafetyLevel.SAFE and confidence >= 0.9:
            return True

        # Everything else requires confirmation
        return False
