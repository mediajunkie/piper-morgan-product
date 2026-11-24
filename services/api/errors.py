from typing import Any, Dict

from fastapi import HTTPException


class APIError(Exception):
    """Base class for all application-specific API errors."""

    def __init__(self, status_code: int, error_code: str, details: Dict[str, Any] = None):
        self.status_code = status_code
        self.error_code = error_code
        self.details = details or {}
        super().__init__(f"API Error [{error_code}]")


class UserFacingHTTPException(HTTPException):
    """An HTTP error whose detail is vetted product copy: the app's error handler keeps
    it for a 5xx instead of masking it (#2154).

    Use it only where the detail is a fixed line the CXO has worded. A detail built from
    an exception's text, a path or a name stays a plain ``HTTPException``, which the
    handler masks (issue 2428 pins this for the setup routes).

    Lives here, beside ``APIError``, so a ``services/`` gate can raise it without a
    ``services`` -> ``web`` import (Arch, issue 2429); ``web.api.exceptions`` re-exports
    it. The guard in ``tests/unit/web/test_setup_lines_reach_the_page_2428.py`` reads
    every ``UserFacingHTTPException(...)`` call under ``web/`` and ``services/`` and
    refuses an import that renames it."""

    user_facing = True


# --- The three "couldn't be checked" lines (CXO, mail 01M8785ZVZ; issue 2429) ---
# One constant per line. "Nothing was changed." is a claim about behaviour: every site
# that says it refuses before any write, pinned in
# tests/unit/web/test_couldnt_be_checked_lines_2429.py.

SESSION_COULD_NOT_BE_CHECKED_MESSAGE = (
    "Your session couldn't be checked just now. Nothing was changed. "
    "Try again in a moment; if it keeps failing, tell us."
)
ADMIN_PERMISSIONS_COULD_NOT_BE_CHECKED_MESSAGE = (
    "Admin permissions couldn't be checked just now. Nothing was changed. "
    "Try again in a moment; if it keeps failing, tell us."
)
PERMISSIONS_COULD_NOT_BE_CHECKED_MESSAGE = (
    "Permissions couldn't be checked just now. "
    "Try again in a moment; if it keeps failing, tell us."
)


# --- Intent Errors ---


class IntentClassificationFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(500, "INTENT_CLASSIFICATION_FAILED", details)


class LowConfidenceIntentError(APIError):
    def __init__(self, suggestions: str = "clarify your request", details: Dict[str, Any] = None):
        details = details or {}
        details["suggestions"] = suggestions
        super().__init__(422, "LOW_CONFIDENCE_INTENT", details)


# --- Workflow Errors ---


class WorkflowTimeoutError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(504, "WORKFLOW_TIMEOUT", details)


class TaskFailedError(APIError):
    def __init__(
        self,
        task_description: str = "a task",
        recovery_suggestion: str = "please try again",
        details: Dict[str, Any] = None,
    ):
        details = details or {}
        details["task_description"] = task_description
        details["recovery_suggestion"] = recovery_suggestion
        super().__init__(500, "TASK_FAILED", details)


# --- Integration Errors ---


class GitHubRateLimitError(APIError):
    def __init__(self, retry_after: int = 1, details: Dict[str, Any] = None):
        details = details or {}
        details["retry_after"] = retry_after
        super().__init__(429, "GITHUB_RATE_LIMIT", details)


class GitHubAuthFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(502, "GITHUB_AUTH_FAILED", details)


class SlackAuthFailedError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(502, "SLACK_AUTH_FAILED", details)


class SlackInitializationError(APIError):
    """Raised when Slack service initialization fails"""

    def __init__(self, details: str):
        super().__init__(503, "SLACK_INIT_FAILED", {"message": details})


# --- Knowledge Base Errors ---


class NoRelevantKnowledgeError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(404, "NO_RELEVANT_KNOWLEDGE", details)


class DocumentProcessingError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(500, "DOCUMENT_PROCESSING_FAILED", details)


# --- Enhanced User Experience Errors ---


class ConfigurationError(APIError):
    def __init__(self, config_item: str = "system settings", details: Dict[str, Any] = None):
        details = details or {}
        details["config_item"] = config_item
        super().__init__(500, "CONFIGURATION_ERROR", details)


class ValidationError(APIError):
    def __init__(self, field: str = "input", details: Dict[str, Any] = None):
        details = details or {}
        details["field"] = field
        super().__init__(422, "VALIDATION_ERROR", details)


class AuthenticationRequiredError(APIError):
    def __init__(self, details: Dict[str, Any] = None):
        super().__init__(401, "AUTHENTICATION_REQUIRED", details)


class PermissionDeniedError(APIError):
    def __init__(self, resource: str = "this resource", details: Dict[str, Any] = None):
        details = details or {}
        details["resource"] = resource
        super().__init__(403, "PERMISSION_DENIED", details)


class ServiceUnavailableError(APIError):
    def __init__(self, service: str = "the service", details: Dict[str, Any] = None):
        details = details or {}
        details["service"] = service
        super().__init__(503, "SERVICE_UNAVAILABLE", details)


class RateLimitError(APIError):
    def __init__(self, retry_after: int = 60, details: Dict[str, Any] = None):
        details = details or {}
        details["retry_after"] = retry_after
        super().__init__(429, "RATE_LIMIT_EXCEEDED", details)


# --- Enhanced User-Friendly Error Messages ---

ERROR_MESSAGES = {
    # Intent errors with contextual help
    # ask-census: question answered by its own directive on the same line; nothing waits for a reply; CXO 2026-10-14
    "INTENT_CLASSIFICATION_FAILED": "I couldn't understand that request. Try using natural language like 'Show me that issue' or 'Update my tasks'. Need help? Check our conversation guide at /docs/public/user-guides/legacy-user-guides/getting-started-conversational-ai.md",
    # ask-census: question answered by its own directive on the same line; nothing waits for a reply; CXO 2026-10-14
    "LOW_CONFIDENCE_INTENT": "I'm not sure what you're asking for. Did you mean to '{suggestions}'? For more examples, see our reference guide at /docs/public/user-guides/legacy-user-guides/understanding-anaphoric-references.md",
    # Workflow errors with recovery guidance
    "WORKFLOW_TIMEOUT": "This task is taking longer than expected. I'll continue working on it in the background and notify you when complete. You can check status or try a simpler request in the meantime.",
    "TASK_FAILED": "I encountered an issue while {task_description}. {recovery_suggestion}. If this persists, try breaking your request into smaller steps.",
    "CONTEXT_VALIDATION_FAILED": "{user_message}. For help with context and references, see /docs/public/user-guides/legacy-user-guides/conversation-memory-guide.md",
    # Integration errors with troubleshooting
    "GITHUB_RATE_LIMIT": "GitHub is temporarily limiting our requests. Please wait {retry_after} minutes before trying again. This helps ensure stable service for all users.",
    # ask-census: question answered by its own directive on the same line; nothing waits for a reply; CXO 2026-10-14
    "GITHUB_AUTH_FAILED": "I couldn't connect to GitHub. Please verify your access token in settings or check if it has the required permissions. Need help? See our GitHub integration guide.",
    "SLACK_AUTH_FAILED": "I couldn't connect to Slack. Please check your bot token and app permissions. Ensure the Slack app is properly installed in your workspace.",
    # Knowledge base errors with guidance
    "NO_RELEVANT_KNOWLEDGE": "I don't have enough context about that topic. Try providing more details or uploading relevant documents. You can also reference specific files or projects for better context.",
    "DOCUMENT_PROCESSING_FAILED": "I couldn't process that document. Please check the file format (supported: PDF, TXT, MD, DOCX) and try again. Large files may take a moment to process.",
    # New user-friendly error categories
    "CONFIGURATION_ERROR": "There's an issue with the system configuration. Please check your settings or contact your administrator for assistance.",
    "VALIDATION_ERROR": "Please check the information you provided. {field} is required and must be in the correct format.",
    "AUTHENTICATION_REQUIRED": "You need to sign in to access this feature. Please check your authentication status and try again.",
    "PERMISSION_DENIED": "You don't have permission to access this resource right now. Please check with your administrator if you need help with permissions.",
    "SERVICE_UNAVAILABLE": "This service is temporarily unavailable. Please try again in a few minutes. If the problem persists, check our status page.",
    "RATE_LIMIT_EXCEEDED": "You've made too many requests recently. Please wait a moment before trying again. This helps maintain stable performance for everyone.",
}
