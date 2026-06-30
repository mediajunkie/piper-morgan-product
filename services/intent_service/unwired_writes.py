"""Unwired WRITE actions — honest-decline COPY (#1331 → #1333).

The bug (#1331, verified in UAT): a user asks Piper to perform a WRITE in chat
("add a milestone to my default repo"). The LLM classifier recognizes the action
(`create_milestone` — a free-form action; the canonical Verb enum has no CREATE
verb, so create-requests emit a free-form action name) but NO handler exists for it.
The action falls through to the conversational floor (the LLM), which — being a
helpful assistant — CONFABULATES a success message ("Milestone created ✓") while NO
GitHub write ever happens. That is a trust-property violation: Piper claims an
action that did not occur.

The fix (#1333, Arch-ruled 2026-06-30): the honest-decline is DERIVED at dispatch,
not enumerated here. Any unwired EXECUTION action reaches
`IntentService._handle_execution_intent`'s else-branch, which deterministically
honest-declines and NEVER routes to the floor. So this module is NO LONGER a
registration list — it provides only the curated decline COPY (the *wording*, not
the *trigger*). A novel unwired action declines automatically via the generic copy;
add an entry below only to give a specific action nicer wording. (History: #1331's
first fix WAS a hand-maintained `UNWIRED_WRITE_ACTIONS` list fanned onto the
action-dispatch rail via `_handle_unwired_write`; #1333 retired the list + handler +
registration as the drift surface Arch flagged.)

SCOPE DISCIPLINE — honest-decline FLOOR only, NO real writes. The decline names the
capability, says it's not available *yet*, and points to the GitHub alternative.
Real connector-backed writes are #1322 Q3 (a separate later effort). When a real
handler ships for one of these actions (wired into `_handle_execution_intent` /
ActionMapper), it stops reaching the else-branch and behaves honestly on its own —
remove its curated copy here in that same change.

Copy rule: an action belongs in the curated map iff (a) the classifier can emit it and
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

# #1333 (Arch-ruled 2026-06-30): the former `UNWIRED_WRITE_ACTIONS` frozenset (which the
# rail fanned per-action honest-degrade entries over) is RETIRED. The decline-set is no
# longer enumerated here — it's DERIVED at dispatch: any unwired EXECUTION action reaches
# `IntentService._handle_execution_intent`'s else-branch, which deterministically declines
# (never routes to the floor). This module now provides only the curated decline COPY
# (override map below) — the *copy*, not the *trigger*. A novel unwired action declines
# automatically (via the generic copy) without being listed; add an entry here only to
# give a specific action nicer wording.

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
