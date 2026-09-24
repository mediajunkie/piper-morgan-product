"""
Enhanced user-friendly error message service.

Converts technical errors into helpful, conversational messages with recovery suggestions.
Issue #255 CORE-UX-ERROR-MESSAGING
Enhanced with consciousness: #631 CONSCIOUSNESS-TRANSFORM: Error Messages
"""

import logging
import re
from enum import Enum
from typing import Dict, Optional, Tuple

from services.consciousness.error_consciousness import (
    enhance_error_pattern,
    format_conversational_error_conscious,
)

logger = logging.getLogger(__name__)


class ErrorSeverity(str, Enum):
    """Error severity levels for appropriate user messaging"""

    INFO = "info"  # Informational, no action needed
    WARNING = "warning"  # User should be aware, minor issue
    ERROR = "error"  # Something went wrong, user action needed
    CRITICAL = "critical"  # Serious issue, immediate attention required


# #1870: named module-level constant, not just an inline dict key, so
# `services/intent_service/conversational_floor.py::_classify_llm_error` (the
# OTHER LLM-error classifier — #1824's four/five-bucket runtime classifier) can
# delegate its quota detection to the SAME regex instead of maintaining an
# independent copy. Before #1870 the floor had NO quota bucket at all — a
# quota/billing-exhausted key fell to its generic "transient... try again in a
# moment" copy, which is actively wrong advice for a permanent billing problem
# (retrying a dead-credit key never recovers). Single source of truth here;
# the floor imports this constant rather than re-deriving the pattern.
QUOTA_PATTERN = (
    r"insufficient_quota|exceeded your current quota|billing.*hard limit|current quota"
    r"|credit.balance.*too low|credit_balance_exhausted"
)

# #1872: Gemini's real invalid-key wording, live-verified by the #1870 lane
# (HTTP 400 body carries `"status": "INVALID_ARGUMENT"`, `"reason":
# "API_KEY_INVALID"`, human message "API key not valid. Please pass a valid
# API key.") — a gap NEITHER classifier recognized before this issue: the
# translator's own invalid-key pattern below didn't carry it, and neither did
# the floor's `_classify_llm_error` rejected_credential term list.
GEMINI_INVALID_KEY_PATTERN = r"api_key_invalid|api key not valid"

# #1872: named so BOTH classifiers add from the one place instead of two
# independently-drifting copies — this is the translator's original invalid-
# key regex (below), now also OR'd into `classify_llm_error_text`'s
# rejected_credential check. That closes a real gap the issue's own example
# surfaced: a primary-provider reason as short as "invalid x-api-key" (no
# surrounding "401"/"authentication_error" wrapper) carried none of the
# floor's plain substring terms, but DOES match this pattern's
# `invalid.*x-api-key` clause — the translator already caught it, the floor
# didn't.
INVALID_KEY_PATTERN = (
    r"invalid_api_key|incorrect api key|invalid.*x-api-key|authentication_error"
    rf"|invalid api key provided|{GEMINI_INVALID_KEY_PATTERN}"
)


def classify_llm_error_text(text: str) -> str:
    """Classify raw LLM-failure text into one of the shared runtime buckets.

    #1872: extracted verbatim (branch order preserved exactly — the #1870
    agreement pin depends on it) from
    `services.intent_service.conversational_floor._classify_llm_error`'s
    string-matching branches, so that classifier can DELEGATE its bucket
    decision here instead of maintaining an independently-drifting copy. This
    module is the shared home per the issue's design: the floor keeps only
    what's floor-specific (the two TYPE-based checks — ConsentUnreadableError,
    AllProvidersFailed — and the bucket-to-copy selection); this function only
    ever sees TEXT, so it has no opinion on a typed exception's honest
    `no_providers` fact.

    Returns one of: "quota_exhausted", "no_provider", "not_configured",
    "insufficient_permission", "rejected_credential", "config_endpoint",
    "transient" (catch-all). NOT the translator's own `category` vocabulary
    (llm_key/llm/auth/...) — that stays `UserFriendlyErrorService`'s own
    pattern-table decision below; the two vocabularies are related but not
    merged (per the issue: don't pick winners on copy for the known
    disagreements pinned in test_llm_error_classifier_agreement_1870.py).
    """
    error_str = text.lower()

    # Same regex as the quota bucket below — one source (#1870); checked
    # first so a quota message can't fall through to 'transient'.
    if re.search(QUOTA_PATTERN, error_str, re.IGNORECASE):
        return "quota_exhausted"

    # No provider configured at all
    if "not configured" in error_str or "no llm provider" in error_str:
        return "no_provider"

    # #1824: the old "auth" bucket returned one label for five causes — two of
    # its own branches said "config issue" in a comment while returning
    # "auth". Split per the ruled criterion (a bucket earns its own name when
    # the honest user-facing sentence differs):

    # A client that was never constructed — no credential was rejected at all.
    if "not initialized" in error_str:
        return "not_configured"

    # A VALID key without permission (scope/entitlement — fix is at the provider).
    if "403" in error_str or "forbidden" in error_str:
        return "insufficient_permission"

    # A rejected credential — the only cause the old bucket's docstring
    # described. The bare-word terms below (401/unauthorized/authentication)
    # are the floor's OWN broader net — deliberately NOT narrowed to the
    # translator's pattern, per the pinned disagreement finding (b) in
    # test_llm_error_classifier_agreement_1870.py (a bare status code/word is
    # correctly rejected_credential here; the translator's narrower patterns
    # miss it and that's an accepted, unresolved disagreement, not a defect
    # this issue fixes). INVALID_KEY_PATTERN — including #1872's Gemini
    # addition — is OR'd in on top so the SHARED gap (finding (d)) and the
    # short-reason gap (a typed exception's `primary_reason` with no "401"
    # wrapper, e.g. "invalid x-api-key") both close for both classifiers.
    if any(
        term in error_str
        for term in [
            "401",
            "unauthorized",
            "invalid api key",
            "invalid_api_key",
            "authentication",
        ]
    ) or re.search(INVALID_KEY_PATTERN, error_str, re.IGNORECASE):
        return "rejected_credential"

    # Operator-side config: model ID stale, or a wrong endpoint. The user's key
    # and account are fine; nothing on their side will help.
    if "model" in error_str and ("not found" in error_str or "does not exist" in error_str):
        return "config_endpoint"
    if "404" in error_str:
        return "config_endpoint"

    # Everything else is transient (timeout, 500, network, etc.)
    return "transient"


class UserFriendlyErrorService:
    """Service to convert technical errors into helpful user messages"""

    def __init__(self):
        # Common technical error patterns and their user-friendly translations
        # NOTE: Order matters! More specific patterns should come first
        self.error_patterns = {
            # LLM API-key failures (#1381-adjacent, PM 2026-07-14) — these MUST
            # come before the generic 429/rate-limit pattern below. An exhausted
            # or invalid key is a PERMANENT config problem the user fixes in
            # Settings, NOT a transient "slow down and retry" (retrying a dead
            # key never recovers). "temporarily unavailable, try again" here is a
            # lie that leaves the user with no path forward.
            # #1718: extended (same bucket, same copy) to catch Anthropic's
            # real no-credits phrasing at key-validation time ("credit
            # balance is too low", "credit_balance_exhausted") — OpenAI's
            # insufficient_quota envelope already matched; Anthropic's did not.
            QUOTA_PATTERN: {
                "message": "I can't reach a language model — the API key on your account is out of quota (or its billing needs attention).",
                "recovery": "Top up the key's billing, or replace it with a funded one under Settings → LLM API Keys.",
                "severity": ErrorSeverity.ERROR,
                "category": "llm_key",
            },
            INVALID_KEY_PATTERN: {
                "message": "The language-model API key on your account isn't valid.",
                "recovery": "Check or replace it under Settings → LLM API Keys.",
                "severity": ErrorSeverity.ERROR,
                "category": "llm_key",
            },
            # #1824 insufficient-permission (CXO's bucket 2 copy): a VALID key the
            # provider won't allow for this model/endpoint. Deliberately does NOT
            # point at our Settings — the fix is at the provider, and sending them
            # to our Settings would recommend a known-failing action (#1108).
            r"permission_error|permission denied.*model|does not have access to model": {
                "message": "Your key works, but the provider won't allow this model or endpoint for it.",
                "recovery": "That's a permissions setting on your account with them — it isn't something I can change from here.",
                "severity": ErrorSeverity.ERROR,
                "category": "llm_key",
            },
            # #1807/#1812 — the caller has NO key at all. Distinct from the two
            # entries above (which describe a key that EXISTS and is broken) and
            # from #1320's anonymous refusal (they ARE signed in). Copy is CXO's,
            # deliberately weaker than the entry-point copy in intent.py/documents.py
            # because the generic layer knows less: surface-neutral ("That needs",
            # not "I can't run this"), no "Nothing was charged" (a generic handler
            # cannot cash that claim), and a recovery that promises the action only,
            # never an outcome. Pattern matches what request_key.py actually raises.
            r"has no llm key of their own|user llm key required|no llm key configured|no api key configured": {
                "message": "That needs an LLM key of your own — Piper doesn't bill anyone else's account.",
                "recovery": "Add an OpenAI or Anthropic key under Settings → LLM API Keys.",
                "severity": ErrorSeverity.ERROR,
                "category": "llm_key",
            },
            r"all configured llm providers failed": {
                "message": "I couldn't reach a language model just now.",
                "recovery": "If you've added your own API key, check it under Settings → LLM API Keys; otherwise this is usually a brief outage — try again in a moment.",
                "severity": ErrorSeverity.ERROR,
                "category": "llm",
            },
            # Database errors
            r"relation '(\w+)' does not exist": {
                "message": "I'm having trouble accessing the database. Let me try reconnecting...",
                "recovery": "This usually resolves itself in a moment. If it persists, please contact support.",
                "severity": ErrorSeverity.ERROR,
                "category": "database",
            },
            r"connection.*refused|connection.*timeout": {
                "message": "I can't connect to the database right now. Let me try again...",
                "recovery": "I'll keep trying to reconnect. This usually resolves quickly.",
                "severity": ErrorSeverity.WARNING,
                "category": "database",
            },
            # API/Network errors
            r"HTTP.*404|Not Found": {
                "message": "I couldn't find what you're looking for.",
                "recovery": "Please check if the item still exists or try searching for it differently.",
                "severity": ErrorSeverity.INFO,
                "category": "api",
            },
            r"HTTP.*401|Unauthorized": {
                "message": "I need permission to access that resource.",
                "recovery": "Please check your login status or contact your administrator for access.",
                "severity": ErrorSeverity.WARNING,
                "category": "auth",
            },
            r"HTTP.*403|Forbidden": {
                "message": "You don't have permission to access that resource.",
                "recovery": "If you think you should have access, please contact your administrator.",
                "severity": ErrorSeverity.WARNING,
                "category": "auth",
            },
            # GitHub-specific errors (must come before general HTTP errors)
            r"GitHub.*rate limit": {
                "message": "GitHub is asking me to slow down my requests.",
                "recovery": "I'll wait and try again. This helps GitHub stay responsive for everyone.",
                "severity": ErrorSeverity.INFO,
                "category": "github",
            },
            r"GitHub.*authentication": {
                "message": "I can't authenticate with GitHub right now.",
                "recovery": "Please check your GitHub token in settings or try reconnecting your account.",
                "severity": ErrorSeverity.WARNING,
                "category": "github",
            },
            # General rate limit (after GitHub-specific)
            r"HTTP.*429|Rate limit": {
                "message": "I'm being asked to slow down by the service.",
                "recovery": "Let me wait a moment and try again. This helps keep things running smoothly for everyone.",
                "severity": ErrorSeverity.INFO,
                "category": "rate_limit",
            },
            r"HTTP.*500|Internal Server Error": {
                "message": "The service I'm trying to reach is having issues.",
                "recovery": "I'll try again in a moment. If this continues, the service team has been notified.",
                "severity": ErrorSeverity.ERROR,
                "category": "api",
            },
            # File/IO errors
            r"No such file or directory": {
                "message": "I can't find that file.",
                "recovery": "Please check the file path or make sure the file hasn't been moved or deleted.",
                "severity": ErrorSeverity.INFO,
                "category": "file",
            },
            r"Permission denied": {
                "message": "I don't have permission to access that file.",
                "recovery": "Please check the file permissions or try a different file.",
                "severity": ErrorSeverity.WARNING,
                "category": "file",
            },
            # Slack API errors
            r"Slack.*token": {
                "message": "I'm having trouble connecting to Slack.",
                "recovery": "Please check your Slack integration settings or try reconnecting.",
                "severity": ErrorSeverity.WARNING,
                "category": "slack",
            },
            # Validation errors
            # Summarize content-length validation (#1188) — the technical message
            # is already user-actionable; preserve it instead of the generic fallback.
            r"too short to summarize": {
                "message": "That content is too short to summarize — I need at least 50 characters to work with.",
                "recovery": "Try pasting a longer passage, or point me at a document or GitHub issue instead.",
                "severity": ErrorSeverity.INFO,
                "category": "validation",
            },
            r"required field|missing.*required": {
                "message": "Some required information is missing.",
                "recovery": "Please provide all the necessary details and try again.",
                "severity": ErrorSeverity.INFO,
                "category": "validation",
            },
            r"invalid.*format|malformed": {
                "message": "The information provided isn't in the right format.",
                "recovery": "Please check the format and try again. Need help? Check our examples.",
                "severity": ErrorSeverity.INFO,
                "category": "validation",
            },
            # Timeout errors
            r"timeout|timed out": {
                "message": "That operation is taking longer than expected.",
                "recovery": "I'll keep working on it. You can try a simpler request or check back in a moment.",
                "severity": ErrorSeverity.WARNING,
                "category": "timeout",
            },
            # Memory/Resource errors
            r"out of memory|memory.*exceeded": {
                "message": "That request is too large for me to handle right now.",
                "recovery": "Try breaking it into smaller pieces or simplifying your request.",
                "severity": ErrorSeverity.WARNING,
                "category": "resource",
            },
        }

        # Contextual recovery suggestions based on user action
        self.contextual_suggestions = {
            "create": "Try creating with less data or check if a similar item already exists.",
            "update": "Make sure the item still exists and you have permission to modify it.",
            "delete": "Verify the item exists and you have permission to delete it.",
            "search": "Try different search terms or check your filters.",
            "list": "Try refreshing or check if you have permission to view this data.",
            "analyze": "Try with a smaller dataset or simpler analysis.",
            "generate": "Try with less complex requirements or break it into steps.",
        }

    def make_user_friendly(
        self, error: Exception, context: Optional[str] = None, user_action: Optional[str] = None
    ) -> Dict[str, str]:
        """
        Convert a technical error into a user-friendly message.

        Args:
            error: The technical error/exception
            context: Optional context about what was being done
            user_action: Optional user action that triggered the error

        Returns:
            Dict with 'message', 'recovery', 'severity', and 'category'
        """
        error_str = str(error)

        # Try to match against known patterns
        for pattern, response in self.error_patterns.items():
            if re.search(pattern, error_str, re.IGNORECASE):
                result = response.copy()

                # Add contextual information if available
                if context:
                    result["message"] = f"While {context.lower()}: {result['message']}"

                # Add action-specific recovery suggestion
                if user_action and user_action in self.contextual_suggestions:
                    result["recovery"] = (
                        f"{result['recovery']} {self.contextual_suggestions[user_action]}"
                    )

                logger.info(
                    f"Converted error to user-friendly message: {pattern} -> {result['message']}"
                )
                return result

        # Fallback for unknown errors
        fallback_message = "Something unexpected happened."
        if context:
            fallback_message = f"I encountered an issue while {context.lower()}."

        fallback_recovery = "Please try again in a moment."
        if user_action and user_action in self.contextual_suggestions:
            fallback_recovery = f"{fallback_recovery} {self.contextual_suggestions[user_action]}"

        logger.warning(f"No pattern matched for error: {error_str}")

        return {
            "message": fallback_message,
            "recovery": fallback_recovery,
            "severity": ErrorSeverity.ERROR,
            "category": "unknown",
        }

    def format_error_response(
        self,
        error: Exception,
        context: Optional[str] = None,
        user_action: Optional[str] = None,
        include_technical_details: bool = False,
    ) -> Dict[str, str]:
        """
        Format a complete error response for the user.

        Args:
            error: The technical error
            context: What was being done when error occurred
            user_action: User action that triggered the error
            include_technical_details: Whether to include technical error info (for debugging)

        Returns:
            Formatted error response dict
        """
        friendly_error = self.make_user_friendly(error, context, user_action)

        response = {
            "user_message": friendly_error["message"],
            "recovery_suggestion": friendly_error["recovery"],
            "severity": friendly_error["severity"],
            "category": friendly_error["category"],
        }

        # Add technical details if requested (for development/debugging)
        if include_technical_details:
            response["technical_error"] = str(error)
            response["error_type"] = type(error).__name__

        return response

    def get_conversational_error(self, error: Exception, context: Optional[str] = None) -> str:
        """
        Get a conversational error message suitable for chat interfaces.

        Uses consciousness patterns for identity voice, epistemic humility,
        and dialogue invitation.

        Args:
            error: The technical error
            context: Optional context

        Returns:
            Conversational error message string with consciousness
        """
        # Get base error without context (consciousness wrapper handles context)
        friendly_error = self.make_user_friendly(error, context=None)

        # Use consciousness-enhanced formatting
        # Issue #631: Error messages now use consciousness patterns
        message = friendly_error["message"]
        recovery = friendly_error["recovery"]
        severity = friendly_error["severity"]

        # Get severity value for consciousness function
        severity_value = severity.value if isinstance(severity, ErrorSeverity) else severity

        return format_conversational_error_conscious(
            message=message,
            recovery=recovery,
            severity=severity_value,
            context=context,
        )


# Global instance for easy access
user_friendly_errors = UserFriendlyErrorService()


def make_error_user_friendly(
    error: Exception, context: Optional[str] = None, user_action: Optional[str] = None
) -> Dict[str, str]:
    """
    Convenience function to convert errors to user-friendly messages.

    Args:
        error: The technical error
        context: Optional context about what was being done
        user_action: Optional user action that triggered the error

    Returns:
        User-friendly error information
    """
    return user_friendly_errors.make_user_friendly(error, context, user_action)


def get_conversational_error_message(error: Exception, context: Optional[str] = None) -> str:
    """
    Convenience function to get conversational error messages.

    Args:
        error: The technical error
        context: Optional context

    Returns:
        Conversational error message
    """
    return user_friendly_errors.get_conversational_error(error, context)
