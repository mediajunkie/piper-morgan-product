"""#1680 Dashboard Criterion E: the census of consequential-action sites.

This registry is the census of record (Arch, decisions.log 2026-11-02 11:00, condition
4; HOST's condition 2). Each entry is one production function that itself calls an
external send/write client (a Slack post or a GitHub write). Coverage is a site count,
never an action count: ``coverage_headline()`` reads "N of M sites instrumented", and
the dashboard leaves its distinct "partial" state only when every censused site is
instrumented (HOST's rollout trigger).

The registry carries three of the four flags because they are facts about the site's
code, not about any one call: ``proactive`` (Piper initiated it, not the user's own
request), ``external_message`` (it leaves Piper) and ``hard_to_reverse``. The fourth,
``credits_spent``, is NOT a registry default: each instrumented site passes it from its
own code path, by this rule (Arch, landing A validation, owed item 3):

    A site passes ``credits_spent=True`` exactly when its own function body (including
    what that body calls, but not the site's callers) made an LLM call for this action
    before the write; otherwise it passes False.

A spend in a caller (the chat turn's ``process_intent`` before a Slack reply) belongs to
that turn, not to the send. Each entry's ``credits_note`` records the value, what in the
body decides it, and the date it was checked against the code. Code sets every flag,
never the model's words (ADR-080).

Held by ``tests/test_architecture_enforcement.py::TestConsequentialSiteCensusRatchet``:
a production call to one of the scanned client methods outside a registered site fails
the build, an ``instrumented=True`` entry without a ``log_consequential_action(`` call
fails it, and the count of uninstrumented sites can only go down.

``TRANSPORT_MODULES`` are forwarders (routers, clients, adapters): they implement the
client methods and forward to the integration, so a call there is the transport, not a
consequential site. The site is whoever called the transport.
"""

from dataclasses import dataclass
from typing import Dict, FrozenSet, Tuple

SLACK = "slack"
GITHUB = "github"


@dataclass(frozen=True)
class ConsequentialSite:
    """One censused site: the function that performs the external send/write.

    ``key`` is stored as ``audit_logs.action`` on the site's rows. ``function`` is the
    dotted enclosing function (``Class.method``) the census test resolves calls to.
    ``client_method`` names the client call(s) the site makes.
    """

    key: str
    module: str
    function: str
    client_method: str
    family: str
    proactive: bool
    hard_to_reverse: bool
    instrumented: bool
    external_message: bool = True
    credits_note: str = ""


_SITES: Tuple[ConsequentialSite, ...] = (
    # ── Slack sends ────────────────────────────────────────────────────────────
    ConsequentialSite(
        key="slack.domain.post_message",
        module="services/domain/slack_domain_service.py",
        function="SlackDomainService.post_message",
        client_method="send_message",
        family=SLACK,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: validates user_id, builds kwargs and calls "
            "SlackIntegrationRouter.send_message; no LLM call in the body. Checked "
            "2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="slack.response.consolidated",
        module="services/integrations/slack/response_handler.py",
        function="SlackResponseHandler._send_consolidated_response",
        client_method="send_message",
        family=SLACK,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: formats buffered workflow results and posts them; the LLM ran upstream "
            "in handle_spatial_event, not in this function. Checked 2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="slack.response.individual",
        module="services/integrations/slack/response_handler.py",
        function="SlackResponseHandler._send_slack_response",
        client_method="send_message",
        family=SLACK,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: formats the workflow result (plus Notion refs) and posts it; the LLM "
            "ran upstream in handle_spatial_event, not in this function. Checked "
            "2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="slack.standup.post",
        module="services/integrations/mcp/skills/standup_workflow_skill.py",
        function="StandupWorkflowSkill._post_to_slack",
        client_method="post_message",
        family=SLACK,
        proactive=True,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: preference lookup, user_timezone_name and _format_for_slack (string "
            "formatting) before SlackDomainService.post_message; no LLM call. Checked "
            "2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="slack.socket.placeholder",
        module="services/integrations/slack/socket_mode_runner.py",
        function="SlackSocketModeRunner._handle_event",
        client_method="chat_postMessage",
        family=SLACK,
        proactive=True,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: the placeholder posts BEFORE _handle_event calls process_intent, so no "
            "LLM call precedes this write; the later process_intent spend belongs to the "
            "chat turn, not to the send. Checked 2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="slack.socket.reply",
        module="services/integrations/slack/socket_mode_runner.py",
        function="SlackSocketModeRunner._post_or_update",
        client_method="chat_update, chat_postMessage",
        family=SLACK,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: the body makes no LLM call (chat_update, then chat_postMessage as "
            "fallback); its caller _handle_event ran process_intent, and that spend belongs "
            "to the chat turn and is not attributed to the send. Checked 2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="slack.socket.slash_reply",
        module="services/integrations/slack/socket_mode_runner.py",
        function="SlackSocketModeRunner._handle_slash_command",
        client_method="send_dict",
        family=SLACK,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: _process_slash_command routes to deterministic handlers in "
            "webhook_router.py and canonical_handlers.py (git grep -i llm in both: 0 hits); "
            "no LLM call before send_dict. Checked 2026-11-02."
        ),
    ),
    # ── GitHub writes ──────────────────────────────────────────────────────────
    ConsequentialSite(
        key="github.chat.create_issue",
        module="services/intent/intent_service.py",
        function="IntentService._handle_create_issue",
        client_method="create_issue",
        family=GITHUB,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: deterministic slot-fill (_slotfill_issue_request), classify_framing "
            "(regex) and the collaborate-first gate (evaluate_consent, no LLM) only. "
            "Checked 2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="github.chat.close_issue",
        module="services/intent/intent_service.py",
        function="IntentService._handle_close_issue_query",
        client_method="update_issue",
        family=GITHUB,
        proactive=False,
        hard_to_reverse=False,
        instrumented=True,
        credits_note=(
            "False: regex issue number, deterministic fuzzy title match, no LLM. Checked "
            "2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="github.chat.reopen_issue",
        module="services/intent/intent_service.py",
        function="IntentService._handle_reopen_issue_query",
        client_method="update_issue",
        family=GITHUB,
        proactive=False,
        hard_to_reverse=False,
        instrumented=True,
        credits_note=(
            "False: regex issue number, deterministic fuzzy title match, no LLM. Checked "
            "2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="github.chat.comment_issue",
        module="services/intent/intent_service.py",
        function="IntentService._handle_comment_issue_query",
        client_method="add_comment",
        family=GITHUB,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "True: extract_slots(COMMENT_ISSUE_TEMPLATE, llm_service=self.llm_client) runs "
            "on every path that reaches add_comment. Checked 2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="github.chat.update_issue",
        module="services/intent/intent_service.py",
        function="IntentService._handle_update_issue",
        client_method="update_issue",
        family=GITHUB,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: deterministic slot-fill and regex issue number, no LLM. Checked " "2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="github.command.create_issue",
        module="services/actions/commands/github_issue_command.py",
        function="GithubIssueCommand.execute",
        client_method="create_issue",
        family=GITHUB,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: reads params/context and calls GitHubDomainService.create_issue; no LLM "
            "call (the learned pattern was approved upstream). Checked 2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="github.domain.create_issue",
        module="services/domain/github_domain_service.py",
        function="GitHubDomainService.create_issue",
        client_method="create_issue",
        family=GITHUB,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: splits the owner/name slug and calls the router; one site, two "
            "create_issue branches; no LLM call. Checked 2026-11-02."
        ),
    ),
    ConsequentialSite(
        key="github.domain.update_issue",
        module="services/domain/github_domain_service.py",
        function="GitHubDomainService.update_issue",
        client_method="update_issue",
        family=GITHUB,
        proactive=False,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=("False: forwards the fields to the router; no LLM call. Checked 2026-11-02."),
    ),
    ConsequentialSite(
        key="github.standup.create_issue",
        module="services/integrations/mcp/skills/standup_workflow_skill.py",
        function="StandupWorkflowSkill._process_github_items",
        client_method="create_issue",
        family=GITHUB,
        proactive=True,
        hard_to_reverse=True,
        instrumented=True,
        credits_note=(
            "False: _extract_action_items and _format_github_issue_body are string work "
            "over the assembled standup; no LLM call. Checked 2026-11-02."
        ),
    ),
)

CONSEQUENTIAL_SITES: Dict[str, ConsequentialSite] = {s.key: s for s in _SITES}

# Forwarders that implement the client methods; a call inside them is transport, not a
# consequential site (the site is the caller). Paths are repo-relative.
TRANSPORT_MODULES: FrozenSet[str] = frozenset(
    {
        "services/integrations/github/github_integration_router.py",
        "services/integrations/github/github_operations_protocol.py",
        "services/mcp/consumer/github_adapter.py",
        "services/integrations/slack/slack_integration_router.py",
        "services/integrations/slack/slack_client.py",
    }
)


def coverage() -> Tuple[int, int]:
    """(instrumented sites, censused sites)."""
    instrumented = sum(1 for s in CONSEQUENTIAL_SITES.values() if s.instrumented)
    return instrumented, len(CONSEQUENTIAL_SITES)


def coverage_headline() -> str:
    """HOST's headline: sites, never a bare percentage or an action count."""
    instrumented, total = coverage()
    return f"{instrumented} of {total} sites instrumented"
