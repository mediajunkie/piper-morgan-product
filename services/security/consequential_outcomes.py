"""#1680 Dashboard Criterion E: the status a consequential site reports, from the call.

One home for the outcome mappers every instrumented site uses, so a site in any module
maps its client's result (or exception) the same way. Each returns
``(status, details)`` with ``status`` in ``audit_logger.CONSEQUENTIAL_STATUSES``.

The rule (#2151, Arch 2026-11-02): "failed" only when the result proves nothing went
out; a call that returned or raised without a verifiable result is "unconfirmed",
never "success" and never a clean "failed".

Landing A defined the GitHub and SlackClient mappers in ``intent_service.py`` and
``response_handler.py``; landing B moved them here (those modules import them under
their old private names) and added the Slack SDK mappers the socket-mode runner needs.
"""

from typing import Any, Dict, Tuple

Outcome = Tuple[str, Dict[str, Any]]

# Slack Web API error codes (``response["error"]``) that mean Slack refused the call,
# so no message was posted or changed. Matched on the API's structured error field of
# a typed ``SlackApiError``, never on exception text. Anything else is "unconfirmed".
SLACK_REFUSAL_ERRORS = frozenset(
    {
        "account_inactive",
        "cant_update_message",
        "channel_not_found",
        "edit_window_closed",
        "invalid_auth",
        "invalid_blocks",
        "is_archived",
        "message_not_found",
        "missing_scope",
        "msg_too_long",
        "no_text",
        "not_authed",
        "not_in_channel",
        "ratelimited",
        "restricted_action",
        "token_revoked",
    }
)


def github_write_outcome(exc: BaseException) -> Outcome:
    """The consequential-row status for a GitHub write that raised.

    "failed" only when the exception proves nothing was written (a refusal, a
    not-found, an undesignated target, no resolvable repo). Anything else raised
    without a verifiable result, so it is "unconfirmed", never "success" and never
    a clean "failed" (#1220/#1322: a fired write may or may not have landed).
    """
    from services.integrations.github.github_integration_router import (
        GitHubIssueNotFound,
        GitHubWriteRefused,
        GitHubWriteRejected,
        GitHubWriteTargetUndesignated,
    )

    name = type(exc).__name__
    if isinstance(
        exc,
        (
            GitHubWriteRefused,
            GitHubWriteRejected,
            GitHubWriteTargetUndesignated,
            GitHubIssueNotFound,
        ),
    ):
        return "failed", {"error_type": name}
    if isinstance(exc, RuntimeError) and "no repo could be resolved" in str(exc):
        return "failed", {"error_type": name, "reason": "no_repo_resolved"}
    if "may or may not have landed" in str(exc):
        return "unconfirmed", {
            "error_type": name,
            "write_unconfirmed": "may_or_may_not_have_landed",
        }
    return "unconfirmed", {
        "error_type": name,
        "write_unconfirmed": "raised_without_verifiable_result",
    }


def github_write_result_outcome(result: Any) -> Outcome:
    """The status for a GitHub write that returned: a non-empty result is "success",
    an empty one is "unconfirmed" (the write returned nothing to verify)."""
    if result:
        return "success", {}
    return "unconfirmed", {"write_unconfirmed": "empty_result"}


def slack_send_outcome(response: Any) -> Outcome:
    """The status for a SlackClient / SlackIntegrationRouter send that returned.

    SlackResponse carries ``success`` (a raw Slack dict carries ``ok``): True is
    "success", False is Slack saying it refused ("failed"); anything else returned
    without a verifiable result is "unconfirmed", never "success"."""
    ok = response.get("ok") if isinstance(response, dict) else getattr(response, "success", None)
    if ok is True:
        return "success", {}
    if ok is False:
        error = (
            response.get("error")
            if isinstance(response, dict)
            else getattr(response, "error", None)
        )
        return "failed", {"error": str(getattr(error, "message", error) or "unknown")}
    return "unconfirmed", {"write_unconfirmed": f"unverifiable_result:{type(response).__name__}"}


def slack_send_error_outcome(exc: BaseException) -> Outcome:
    """The status for a SlackClient / router send that raised. Only "no integration"
    proves nothing went out; any other exception is "unconfirmed"."""
    name = type(exc).__name__
    if isinstance(exc, RuntimeError) and "No Slack integration available" in str(exc):
        return "failed", {"error_type": name, "reason": "no_slack_integration"}
    return "unconfirmed", {
        "error_type": name,
        "write_unconfirmed": "raised_without_verifiable_result",
    }


def _sdk_field(response: Any, key: str) -> Any:
    """``response[key]`` for a slack_sdk SlackResponse or a dict; None when absent.
    A test double (MagicMock) has no real field, so it reads as absent."""
    if isinstance(response, dict):
        return response.get(key)
    data = getattr(response, "data", None)
    if isinstance(data, dict):
        return data.get(key)
    return None


def slack_sdk_outcome(response: Any) -> Outcome:
    """The status for a slack_sdk Web API call that returned (``chat_postMessage``,
    ``chat_update``) or a webhook ``send_dict``.

    Web API: ``ok`` True is "success"; ``ok`` False is "failed" with Slack's ``error``.
    Webhook (``WebhookResponse``, no ``ok`` field): HTTP 200 is "success" (Slack
    answers "ok"), a 4xx is "failed" with the body. Any other result is "unconfirmed".
    """
    ok = _sdk_field(response, "ok")
    if ok is True:
        return "success", {}
    if ok is False:
        return "failed", {"error": str(_sdk_field(response, "error") or "unknown")}
    status_code = getattr(response, "status_code", None)
    if isinstance(status_code, int) and not isinstance(status_code, bool):
        if status_code == 200:
            return "success", {"status_code": 200}
        if 400 <= status_code < 500:
            body = getattr(response, "body", None)
            return "failed", {"status_code": status_code, "error": str(body or "unknown")}
        return "unconfirmed", {"status_code": status_code, "write_unconfirmed": "http_status"}
    return "unconfirmed", {"write_unconfirmed": f"unverifiable_result:{type(response).__name__}"}


def slack_sdk_error_outcome(exc: BaseException) -> Outcome:
    """The status for a slack_sdk call that raised.

    A ``SlackApiError`` whose structured ``error`` code is a known refusal
    (``SLACK_REFUSAL_ERRORS``) is "failed"; any other exception (another API error,
    a timeout, a dropped connection) is "unconfirmed"."""
    from slack_sdk.errors import SlackApiError

    name = type(exc).__name__
    if isinstance(exc, SlackApiError):
        code = _sdk_field(getattr(exc, "response", None), "error")
        if isinstance(code, str) and code in SLACK_REFUSAL_ERRORS:
            return "failed", {"error_type": name, "error": code}
        return "unconfirmed", {
            "error_type": name,
            "error": str(code or "unknown"),
            "write_unconfirmed": "slack_api_error_not_a_known_refusal",
        }
    return "unconfirmed", {
        "error_type": name,
        "write_unconfirmed": "raised_without_verifiable_result",
    }


def domain_send_result_outcome(result: Any) -> Outcome:
    """The status for a call to a domain-service send that returns the
    ``{"success": bool, "error": str}`` envelope (``SlackDomainService.post_message``).

    ``success`` True is "success". ``success`` False is "unconfirmed", not "failed":
    the envelope folds a Slack refusal and a transport exception into the same False,
    so it cannot prove nothing went out (the domain service's own row, written at the
    send, carries the precise status)."""
    if isinstance(result, dict) and result.get("success") is True:
        return "success", {}
    error = result.get("error") if isinstance(result, dict) else None
    return "unconfirmed", {
        "write_unconfirmed": "domain_envelope_not_success",
        "error": str(error or "unknown"),
    }


def notion_write_outcome(exc: BaseException) -> Outcome:
    """#2262: the status for a Notion write that raised. The router forwards to the
    integration, which may have written before it raised, so it is "unconfirmed", never
    "success" and never a clean "failed" (the #1220 rule GitHub's writes follow)."""
    return "unconfirmed", {"write_error": type(exc).__name__}


def notion_write_result_outcome(result: Any) -> Outcome:
    """#2262: a Notion write that returned. A non-empty result is "success"; an empty
    one is "unconfirmed" (the integration returned nothing to verify)."""
    if result:
        return "success", {}
    return "unconfirmed", {"write_unconfirmed": "empty_result"}
