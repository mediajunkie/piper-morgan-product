"""Unwired WRITE actions — honest-degrade registry (#1331).

The bug (#1331, verified in UAT): a user asks Piper to perform a WRITE in chat
("add a milestone to my default repo"). The LLM classifier recognizes the action
(`create_milestone` — a free-form action; the canonical Verb enum has no CREATE
verb, so create-requests emit a free-form action name) but NO handler or
WorkflowEntry exists for it. The action therefore falls through to the
conversational floor (the LLM), which — being a helpful assistant — CONFABULATES a
success message ("Milestone created ✓") while NO GitHub write ever happens. That
is a trust-property violation: Piper claims an action that did not occur.

This module is the single source of truth for the set of recognized-but-unwired
WRITE actions that must HONEST-DEGRADE instead. Each is registered as an
action-triggered WorkflowEntry (see `workflow_entries.py`) routing to
`IntentService._handle_unwired_write`, so the ADR-059 / #1124 action-dispatch rail
intercepts the action BEFORE it can reach the floor.

SCOPE DISCIPLINE — this is the honest-degrade FLOOR, not real writes. The handler
performs NO GitHub write; it declines honestly and points to the GitHub
alternative. Real connector-backed writes are #1322 Q3 (a separate later effort).
When a real write handler ships for one of these actions, REMOVE that action from
`UNWIRED_WRITE_ACTIONS` (and register its real handler) in the same change.

Membership rule: an action belongs here iff (a) the classifier can emit it and
(b) it has NO real handler / WorkflowEntry today. Actions that DO have real
handlers must NOT be listed here (they already behave honestly — they error on a
dead PAT rather than confabulate):
  - create_issue / create_ticket → `_handle_create_issue`
  - update_issue / update_ticket → `_handle_update_issue`
  - generate_report            → ANALYSIS cohort `_handle_generate_report`
  - close_issue / reopen_issue / comment_issue → #1124 WorkflowEntries
  - complete_todo / create_todo / create_reminder / delete_todo → todo_handlers
"""

from typing import Dict

# Per-action decline copy. Tone (per #1331): honest, brief, not over-apologetic,
# point to the alternative. NEVER fabricate success. The {object} the user wanted
# is named so the decline reads naturally; "yet" + the GitHub pointer make clear
# this is a not-yet-built capability, not a failure.
#
# The verbs/objects below are the create-write family the classifier recognizes
# (llm_classifier.py:537 lists create_milestone explicitly; the create_* siblings
# are the same class of GitHub-object creation, all handler-less — confirmed: no
# `_handle_create_*` method exists and none are in ActionMapper). `update_status`
# is the one non-create entry: it is recognized (llm_classifier.py:537) and has no
# handler, so it would confabulate too; covered defensively with a generic decline.
UNWIRED_WRITE_DECLINES: Dict[str, str] = {
    "create_milestone": (
        "I can't create milestones from chat yet — that capability is on the way. "
        "For now you can add it directly in GitHub (Issues → Milestones → New milestone)."
    ),
    "create_release": (
        "I can't cut releases from chat yet — that's still on the way. "
        "For now you can create the release directly in GitHub (Releases → Draft a new release)."
    ),
    "create_label": (
        "I can't create labels from chat yet — that capability is on the way. "
        "For now you can add it directly in GitHub (Issues → Labels → New label)."
    ),
    "create_branch": (
        "I can't create branches from chat yet — that's still on the way. "
        "For now you can create the branch directly in GitHub or with `git`."
    ),
    "create_pull_request": (
        "I can't open pull requests from chat yet — that capability is on the way. "
        "For now you can open the PR directly in GitHub (Pull requests → New pull request)."
    ),
    "update_status": (
        "I can't update status from chat yet — that capability is on the way. "
        "For now you can make the change directly in GitHub."
    ),
}

# The canonical set the rail registers honest-degrade entries for.
UNWIRED_WRITE_ACTIONS = frozenset(UNWIRED_WRITE_DECLINES.keys())

# Generic decline for any unwired write that lacks bespoke copy (defensive — the
# handler should always find per-action copy above, but never confabulate even if
# the set grows without copy being added).
GENERIC_UNWIRED_WRITE_DECLINE = (
    "I can't do that from chat yet — that capability is still on the way. "
    "For now you can make the change directly in the relevant tool (e.g. GitHub)."
)


def get_unwired_write_decline(action: str) -> str:
    """Return the honest-decline message for an unwired write action.

    Falls back to the generic decline if the action has no bespoke copy — so the
    handler NEVER confabulates success even for an action added to the set without
    its own message.
    """
    return UNWIRED_WRITE_DECLINES.get(action, GENERIC_UNWIRED_WRITE_DECLINE)
