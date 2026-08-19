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
Real connector-backed writes are #1440 (RECONNECT R2; was #1322 Q3 — closed) (a separate later effort). When a real
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
  - complete_todo / create_todo / create_reminder → todo_handlers (elif chain)
  - delete_todo → todo_handlers via its #1666 rail WorkflowEntry (DESTRUCTIVE,
    #1190-gated; the elif was removed with the migration)
"""

import re
from typing import Dict, Optional

# Per-action decline copy. Tone (per #1331): honest, brief, not over-apologetic,
# point to the alternative. NEVER fabricate success. The {object} the user wanted
# is named so the decline reads naturally; "yet" + the GitHub pointer make clear
# this is a not-yet-built capability, not a failure.
#
# The verbs/objects below are the create-write family the classifier recognizes
# (the deleted PM-034 llm_classifier (git history, #1432) listed create_milestone explicitly; the create_* siblings
# are the same class of GitHub-object creation, all handler-less — confirmed: no
# `_handle_create_*` method exists and none are in ActionMapper). `update_status`
# is the one non-create entry: it was recognized there and has no
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
# #1426 (census D3): the old second sentence — "make the change directly in the
# relevant tool (e.g. GitHub)" — MISDIRECTED for every non-GitHub-object request
# (connect-integrations, api-keys, lists…), where the relevant surface is
# Piper's own Settings/pages. Name both, presume neither.
GENERIC_UNWIRED_WRITE_DECLINE = (
    "I can't do that from chat yet — that capability is still on the way. "
    "Depending on what you're after, it may already be available in Piper's own "
    "pages (Settings, Files, Lists) or in the underlying tool (e.g. GitHub)."
)


# ---------------------------------------------------------------------------
# #1571 — nearest-wired-capability hint for the files-family decline shape.
#
# Incident (PM live, 2026-08-10): the LLM floor taught PM to "just say 'file it
# in [owner/repo]' and I'll create it". That phrase misclassified into a
# files-family action; the generic decline above replied "I can't do that from
# chat yet" — a FALSE denial as experienced, because create_issue IS wired and
# PM had used it minutes earlier. The decline was honest about the
# misclassified action but useless about the obvious intent.
#
# The hint: when declining a files-family WRITE whose ask looks issue-like,
# append ONE sentence offering the working create-issue form. Trust properties
# preserved (#1231/#1333): honest-gap (the decline stands), actionable (the
# hint IS the next action), once-per-response (one sentence on the one decline
# this response carries), and deterministic template — NEVER an LLM call.
#
# Derive-don't-hand-write (the MAX_INFERENCE_SITES=0 spirit): the action
# phrase is derived from workflow_dispatcher.wired_chat_actions() — the same
# registry the #1517 capability manifest reads. If the create-issue capability
# ever unwires or renames, _wired_issue_create_phrase() returns None and the
# hint vanishes rather than teaching a dead form (the false-affirmation dual
# of the #1426 false-denial class).
# ---------------------------------------------------------------------------

# Token sets, not substrings: "profile" must not read as files-family, and
# "issued" must not read as issue-like.
_FILES_FAMILY_TOKENS = frozenset({"file", "files"})
_ISSUE_LIKE_TOKENS = frozenset({"issue", "issues", "bug", "bugs", "ticket", "tickets"})

# owner/repo pair — the incident shape ("file it in mediajunkie/piper-morgan-product").
# Same guards as intent_service._slotfill_issue_request's bare-pair pattern:
# not preceded by ./ or a word char (excludes URLs matching as pair + domains),
# owner must contain a letter (excludes fractions/dates like "1/2").
_REPO_PAIR_RE = re.compile(
    r"(?<![./\w])(?=[A-Za-z0-9-]*[A-Za-z])[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?"
    r"/[A-Za-z0-9._-]+\b"
)


def _wired_issue_create_phrase() -> Optional[str]:
    """Derive the plain-language create-issue phrase from the wired registry.

    Looks for a wired action whose tokens are exactly a create-verb plus
    issue-noun (today: ``create_issue``) and renders it mechanically
    ("create an issue"). Returns None when no such action is wired — the
    caller then offers no hint (never teach a dead form).
    """
    from services.intent_service.workflow_dispatcher import wired_chat_actions

    for action in wired_chat_actions():
        tokens = action.lower().split("_")
        if tokens[0] == "create" and set(tokens[1:]) <= _ISSUE_LIKE_TOKENS and tokens[1:]:
            noun = " ".join(tokens[1:])
            article = "an" if noun[0] in "aeiou" else "a"
            return f"{tokens[0]} {article} {noun}"
    return None


def _issue_like_files_family_hint(action: str, original_message: Optional[str]) -> str:
    """Return the one-sentence create-issue hint, or "" when out of scope.

    Scope: files-family action (a "file"/"files" token in the action name)
    AND an issue-like ask — issue/bug/ticket wording in the action or message,
    or the incident shape (a file-verb action aimed at an owner/repo pair).
    """
    action_tokens = set((action or "").lower().split("_"))
    if not action_tokens & _FILES_FAMILY_TOKENS:
        return ""

    msg = original_message or ""
    issue_like = bool(
        action_tokens & _ISSUE_LIKE_TOKENS
        or re.search(r"\b(?:issue|bug|ticket)s?\b", msg, re.IGNORECASE)
        or _REPO_PAIR_RE.search(msg)
    )
    if not issue_like:
        return ""

    phrase = _wired_issue_create_phrase()
    if phrase is None:
        return ""
    return (
        f" If you're trying to get an issue filed, that part works today — "
        f"say \"{phrase} in owner/repo titled '…'\" and I'll take it from there."
    )


def get_unwired_write_decline(action: str, original_message: Optional[str] = None) -> str:
    """Return the honest-decline message for an unwired write action.

    Falls back to the generic decline if the action has no bespoke copy — so the
    handler NEVER confabulates success even for an action added to the set without
    its own message.

    #1571: for a files-family decline whose ask looks issue-like, appends a
    one-sentence nearest-wired-capability hint (the working create-issue form,
    derived from the wired registry). Deterministic template; no LLM call.
    ``original_message`` is optional — the pre-#1571 single-arg call shape
    behaves exactly as before.
    """
    decline = UNWIRED_WRITE_DECLINES.get(action, GENERIC_UNWIRED_WRITE_DECLINE)
    return decline + _issue_like_files_family_hint(action, original_message)
