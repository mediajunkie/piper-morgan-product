"""
Consciousness Expression Framework

This module provides tools for transforming data-driven output into
conscious expression that feels like interaction with an embodied AI.

Created: January 21, 2026
Issue: #407 MUX-VISION-STANDUP-EXTRACT
ADR: ADR-056 Consciousness Expression Patterns

Usage:
    from services.consciousness import inject_consciousness, validate_mvc

    # Transform data into conscious narrative
    output = await inject_consciousness(standup_result)

    # Validate output meets MVC requirements
    result = validate_mvc(output)
    if not result.passes:
        output = ensure_mvc(output)
"""

from services.consciousness.auth_consciousness import (
    format_account_inactive_conscious,
    format_invalid_credentials_conscious,
    format_login_success_conscious,
    format_logout_success_conscious,
    format_password_changed_conscious,
    format_session_expired_conscious,
    format_settings_saved_conscious,
)
from services.consciousness.cli_consciousness import (
    format_cli_error_conscious,
    format_cli_progress_conscious,
    format_cli_success_conscious,
    format_ready_conscious,
    format_services_ready_conscious,
    format_shutdown_conscious,
    format_startup_conscious,
)
from services.consciousness.context import ConsciousnessContext, analyze_context

# #1754: format_chitchat/farewell/thanks_conscious deleted with
# ConversationHandler's live-unreachable non-greeting branches.
from services.consciousness.conversation_consciousness import format_greeting_conscious
from services.consciousness.error_consciousness import (
    enhance_error_pattern,
    format_conversational_error_conscious,
    format_error_conscious,
)
from services.consciousness.files_consciousness import (
    format_files_conscious,
    format_project_detail_conscious,
    format_projects_conscious,
)
from services.consciousness.injection import ensure_mvc, inject_consciousness
from services.consciousness.learning_consciousness import (
    format_learning_event_conscious,
    format_patterns_learned_conscious,
    format_preference_saved_conscious,
)
from services.consciousness.loading_consciousness import (
    format_progress_conscious,
    get_conscious_loading_message,
)
from services.consciousness.search_consciousness import (
    format_no_results_conscious,
    format_search_error_conscious,
    format_search_results_conscious,
)
from services.consciousness.standup_consciousness import (
    format_accomplishments_conscious,
    format_blockers_conscious,
    format_full_standup_conscious,
    format_priorities_conscious,
    format_standup_closing_conscious,
    format_standup_greeting_conscious,
)
from services.consciousness.todo_consciousness import (
    format_next_todo_conscious,
    format_todo_completed_conscious,
    format_todo_created_conscious,
    format_todo_deleted_conscious,
    format_todo_list_conscious,
)
from services.consciousness.ui_consciousness import (
    format_button_label_conscious,
    format_delete_confirmation_conscious,
    format_empty_state_conscious,
    format_empty_state_title_conscious,
    format_toast_delete_conscious,
    format_toast_error_conscious,
    format_toast_success_conscious,
    get_empty_state_cta,
    get_empty_state_data,
    get_empty_state_icon,
)
from services.consciousness.validation import MVCResult, validate_mvc

__all__ = [
    # Core framework
    "ConsciousnessContext",
    "analyze_context",
    "inject_consciousness",
    "ensure_mvc",
    "validate_mvc",
    "MVCResult",
    # Todo consciousness (Phase 3)
    "format_todo_list_conscious",
    "format_todo_created_conscious",
    "format_todo_completed_conscious",
    "format_todo_deleted_conscious",
    "format_next_todo_conscious",
    # Conversation consciousness (Phase 3; greeting-only since #1754)
    "format_greeting_conscious",
    # Loading consciousness (Wave 1)
    "get_conscious_loading_message",
    "format_progress_conscious",
    # Error consciousness (Wave 1)
    "format_error_conscious",
    "format_conversational_error_conscious",
    "enhance_error_pattern",
    # Standup consciousness (Wave 2)
    "format_standup_greeting_conscious",
    "format_accomplishments_conscious",
    "format_priorities_conscious",
    "format_blockers_conscious",
    "format_standup_closing_conscious",
    "format_full_standup_conscious",
    # CLI consciousness (Wave 2)
    "format_startup_conscious",
    "format_ready_conscious",
    "format_shutdown_conscious",
    "format_cli_success_conscious",
    "format_cli_error_conscious",
    "format_cli_progress_conscious",
    "format_services_ready_conscious",
    # Search consciousness (Issue #634)
    "format_search_results_conscious",
    "format_no_results_conscious",
    "format_search_error_conscious",
    # Files/Projects consciousness (Issue #635)
    "format_files_conscious",
    "format_projects_conscious",
    "format_project_detail_conscious",
    # Learning consciousness (Issue #636)
    "format_patterns_learned_conscious",
    "format_preference_saved_conscious",
    "format_learning_event_conscious",
    # Auth/Settings consciousness (Issue #637)
    "format_login_success_conscious",
    "format_logout_success_conscious",
    "format_session_expired_conscious",
    "format_invalid_credentials_conscious",
    "format_settings_saved_conscious",
    "format_account_inactive_conscious",
    "format_password_changed_conscious",
    # UI/Template consciousness (Issue #638)
    "format_empty_state_conscious",
    "format_empty_state_title_conscious",
    "format_delete_confirmation_conscious",
    "format_toast_success_conscious",
    "format_toast_error_conscious",
    "format_toast_delete_conscious",
    "format_button_label_conscious",
    "get_empty_state_icon",
    "get_empty_state_cta",
    "get_empty_state_data",
]
