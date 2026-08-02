"""
ActionMapper - Maps EXECUTION category action name variations to handler methods.

Issue #284: CORE-ALPHA-ACTION-MAPPING
Issue #294: CORE-ALPHA-ACTIONMAPPER-CLEANUP

SCOPE: This mapper handles EXECUTION category actions ONLY.

Why EXECUTION needs mapping:
- Classifier generates variations like 'create_github_issue' or 'make_github_issue'
- Handler method is named 'create_issue'
- ActionMapper bridges this naming gap by normalizing variations

Why other categories DON'T need mapping:
- QUERY category: Routes to query handler regardless of action name
- ANALYSIS category: Routes to analysis handler regardless of action name
- SYNTHESIS category: Routes to synthesis handler regardless of action name
- They route by CATEGORY first, not by action name variations

This is by design - EXECUTION actions are more varied and specific (create_issue,
add_todo, update_issue), while other categories have uniform handling within
their category (all queries go to query handler, all analysis goes to analysis handler).

Architecture Note:
IntentService.process_intent() routes by category FIRST. Only EXECUTION category
calls ActionMapper.map_action(). Other categories route directly to their handlers.

See: services/intent/intent_service.py - process_intent() method
"""

import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)


class ActionMapper:
    """
    Maps EXECUTION category action name variations to handler method names.

    SCOPE: EXECUTION actions ONLY.

    The intent classifier outputs varied action names for EXECUTION category
    (e.g., "create_github_issue", "make_github_issue", "new_github_issue")
    while handler methods use normalized names (e.g., "create_issue").

    This mapper provides the normalization layer for EXECUTION actions.

    Other categories (QUERY, ANALYSIS, SYNTHESIS) route by category and
    do NOT use this mapper.

    Design Principles:
    1. Explicit mappings for EXECUTION action variations
    2. Graceful fallback to original action if unmapped
    3. Logging for discovery of new EXECUTION patterns
    4. No silent failures - always returns a string
    """

    # EXECUTION action mappings: classifier output -> handler method name
    # NOTE: Only EXECUTION category actions belong here
    ACTION_MAPPING: Dict[str, str] = {
        # ===== GITHUB ACTIONS (EXECUTION category) =====
        # GitHub Issue Creation
        "create_github_issue": "create_issue",
        "create_item": "create_issue",
        "create_ticket": "create_issue",
        "create_issue": "create_issue",
        "make_github_issue": "create_issue",
        "new_github_issue": "create_issue",
        # GitHub Issue Updates
        "update_github_issue": "update_issue",
        "update_ticket": "update_issue",
        "update_issue": "update_issue",
        "modify_issue": "update_issue",
        # ===== TODO ACTIONS (EXECUTION category) =====
        # Todo Creation
        "create_todo": "create_todo",
        "add_todo": "create_todo",
        "new_todo": "create_todo",
        # Todo Listing
        "list_todos": "list_todos",
        "show_todos": "list_todos",
        "get_todos": "list_todos",
        "my_todos": "list_todos",
        "list_completed_todos": "list_todos",  # Issue #904: handler detects completed flag from message
        "list_todos_query": "list_todos",
        "next_todo_query": "next_todo",
        # Todo Reminders (Issue #903)
        "create_reminder": "create_reminder",
        "set_reminder": "create_reminder",
        "add_reminder": "create_reminder",  # #1426: census-observed LLM emission (was mapper-missed)
        # Todo Completion
        "complete_todo": "complete_todo",
        "finish_todo": "complete_todo",
        "mark_complete": "complete_todo",
        "mark_done": "complete_todo",
        # Todo Deletion
        "delete_todo": "delete_todo",
        "remove_todo": "delete_todo",
        "cancel_todo": "delete_todo",
        # ===== SPECIAL ACTIONS =====
        # Clarification/Unknown (fallback handling)
        "clarification_needed": "unknown_intent",
        "unknown": "unknown_intent",
    }

    @classmethod
    def map_action(cls, classifier_action: str) -> str:
        """
        Map EXECUTION category action name to handler method name.

        SCOPE: Use for EXECUTION category actions ONLY.

        Args:
            classifier_action: EXECUTION action from classifier (e.g., "create_github_issue")

        Returns:
            Normalized action name for handler (e.g., "create_issue")

        Note:
            - Always returns a string - never None
            - Falls back to original action if no explicit mapping exists
            - Only EXECUTION actions should call this method
            - Other categories (QUERY, ANALYSIS, SYNTHESIS) route by category

        Raises:
            None - Graceful fallback behavior
        """
        if not classifier_action:
            logger.warning("ActionMapper received empty action string")
            return "unknown_intent"

        # Check for explicit mapping
        mapped_action = cls.ACTION_MAPPING.get(classifier_action)

        if mapped_action:
            if mapped_action != classifier_action:
                logger.debug(f"EXECUTION action mapped: '{classifier_action}' -> '{mapped_action}'")
            return mapped_action

        # No explicit mapping found - log for future EXECUTION action additions
        logger.warning(
            f"Unmapped EXECUTION action: '{classifier_action}' - using original. "
            f"Consider adding to ACTION_MAPPING if this is a common EXECUTION action. "
            f"Note: Only EXECUTION actions use this mapper."
        )

        # Fallback: use original action
        return classifier_action

    @classmethod
    def get_unmapped_count(cls, all_actions: list[str]) -> int:
        """
        Return count of unmapped actions for metrics.

        Args:
            all_actions: List of classifier action strings to check

        Returns:
            Number of actions not in ACTION_MAPPING
        """
        return sum(1 for action in all_actions if action not in cls.ACTION_MAPPING)

    @classmethod
    def get_mapping_coverage(cls, all_actions: list[str]) -> float:
        """
        Calculate mapping coverage percentage.

        Args:
            all_actions: List of classifier action strings to check

        Returns:
            Percentage of actions that have explicit mappings (0.0 to 100.0)
        """
        if not all_actions:
            return 100.0

        mapped_count = sum(1 for action in all_actions if action in cls.ACTION_MAPPING)
        return (mapped_count / len(all_actions)) * 100.0

    @classmethod
    def list_all_mappings(cls) -> Dict[str, str]:
        """
        Return copy of all action mappings for inspection/debugging.

        Returns:
            Dictionary of classifier_action -> handler_action mappings
        """
        return cls.ACTION_MAPPING.copy()

    @classmethod
    def add_mapping(cls, classifier_action: str, handler_action: str) -> None:
        """
        Dynamically add a new action mapping.

        Args:
            classifier_action: Action string from classifier
            handler_action: Normalized action for handler

        Note:
            Used for runtime learning/adaptation. Changes not persisted.
        """
        if classifier_action in cls.ACTION_MAPPING:
            logger.info(
                f"Overwriting existing mapping: '{classifier_action}' "
                f"(was: '{cls.ACTION_MAPPING[classifier_action]}', now: '{handler_action}')"
            )
        else:
            logger.info(f"Adding new mapping: '{classifier_action}' -> '{handler_action}'")

        cls.ACTION_MAPPING[classifier_action] = handler_action
