"""#1190 — multi-turn confirmation gate for DESTRUCTIVE rail actions.

PM ruling (decisions.log 2026-08-10 ~10:55): close_issue / reopen_issue are
DESTRUCTIVE (blast-radius protection — a close removes the issue from every
open-state board and query at once; the 2026-07 auto-close incident closed a
live Beta Blocker from a commit message). A classified intent whose rail
entry derives ``needs_confirm`` (== EffectClass.DESTRUCTIVE) must NOT
execute on the turn it was classified: the gate registers a pending action
and asks one clear yes/no question instead.

WHERE THE GATE SITS (routing-fix moratorium, Lead 2026-08-08): at the ACTION
layer, post-classification — the #1124 rail dispatch seam in
``IntentService.process_intent`` (the ``intent.action in
get_action_workflows()`` branch). No pre-classifier or prompt changes. The
#1510 collaborate-gate (compose-vs-execute working mode, upstream of
creates) is ORTHOGONAL: an execute-mode user still confirms destructive
actions — different failures need different protections (PPM).

HOW THE CONFIRMATION RIDES THE EXISTING SEAM (#846 / #1529 — verified by
reading, not invented in parallel):

- The confirmation IS a pending offer in ``WorkflowOfferService``'s
  session-scoped store (#846 — deliberately session-keyed, one-turn-shaped).
  No parallel store exists or is permitted.
- ``process_intent`` pops the pending offer BEFORE classification and before
  the process-resume check, so the #1529 offer-binding ordering (pending
  offer beats resume-check) holds for confirmations by construction.
- "yes" → the acceptance path dispatches ``workflow_type`` — here the
  CONFIRM_PENDING_ACTION_WORKFLOW entry — whose entry point re-dispatches
  the ORIGINAL rail action with the ORIGINAL classified Intent (resolved
  params intact). The "yes" itself is NEVER re-classified.
- "no" / refusal → the decline path returns the stored honest-cancel copy;
  nothing fires. Bare #888/#1529 exit commands ("cancel", "stop", "forget
  it") count as refusal via :func:`detect_bare_exit` — the #1529 exit tier
  applied to a one-turn offer.
- Any other message (off-intent) → the pop already cancelled the pending
  action (nothing can fire it later), and normal processing answers the new
  message — the #1529 off_intent tier ("let normal processing answer").

PENDING-ACTION RECORD SHAPE (the generic deferred-action carrier, Part 3):

    {
        "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
        "question": str,   # #1665: the ALREADY-RENDERED ask the user saw this
                           # turn — stored verbatim at arm time (never
                           # re-rendered later) so the SessionSnapshot's
                           # pending_offer_question can never drift from what
                           # was actually said. Optional on the shape; every
                           # arm site populates it.
        "pending_action": {
            "kind": str,       # offer family (#1664: confirm-ness derives from
                               # this — see offer_is_confirm below); this
                               # module's records carry DESTRUCTIVE_CONFIRM_KIND
            "action": str,     # rail key to dispatch on "yes" (e.g. "close_issue")
            "intent": Intent,  # ORIGINAL classified Intent — resolved params
                               # (issue number, repo context, principal) intact
            "summary": str,    # human phrase ("close issue #123 'title'"),
                               # reused in the question and the cancel copy
        },
        "decline_message": str,  # honest-cancel copy for the "no" path
    }

The carrier is deliberately action-agnostic: ``pending_action`` can hold ANY
deferred rail action + its params — acceptance always re-dispatches
``action`` with ``intent`` through the workflow registry. #1571's
drafted-issue binding SHIPPED as the second consumer (2026-08-15):
``services/intent_service/drafted_issue.py`` builds its own record (kind
``drafted_issue``) and delegates acceptance to the same
``run_confirm_pending_action_workflow`` mirror.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, Optional

import structlog

from services.domain.models import Intent

logger = structlog.get_logger(__name__)

# Registered in workflow_entries.register_default_workflows with
# action_triggered=False: the classifier can never emit it; only the
# offer-acceptance seam dispatches it.
CONFIRM_PENDING_ACTION_WORKFLOW = "confirm_pending_action"

# #1664: the destructive-confirmation records this module builds now carry a
# kind of their own (they were the one kindless #846 producer), so confirm-ness
# can be derived from the offer KIND instead of the carrier workflow_type —
# repo clarification rides the same carrier with a non-yes/no open question,
# and deriving from the carrier mislabeled it "(yes/no confirm)".
DESTRUCTIVE_CONFIRM_KIND = "destructive_action_confirmation"

# ---------------------------------------------------------------------------
# #1664 — is_confirm derives from the offer KIND, in ONE place.
#
# The #1650 confirm-kind table (soft_invocation's CONFIRM-tier comment +
# intent_service's offer-seam enumeration): the offer kinds whose OPEN
# QUESTION is a yes/no — an accept FIRES a held action, so they ride the
# strict detect_confirm_response detector. Exactly this set:
#
#   - destructive close/reopen confirms ..... DESTRUCTIVE_CONFIRM_KIND (here)
#   - reminder-clear delete confirms ........ reminder_clear.CLEAR_DELETE_CONFIRMATION_KIND
#   - consent checks ........................ consent_gate.CONSENT_CHECK_KIND
#   - unmapped-status-value close confirm ... intent_service._offer_status_close_clarification
#         (a destructive close confirm by another name — its copy is literally
#         "...? (yes/no)" and "yes" dispatches close_issue)
#   - drafted-issue FILE confirm ............ drafted_issue.DRAFTED_ISSUE_KIND,
#         but ONLY in the ready-to-file state (title AND body present) — the
#         mid-compose states' open question is "what's it about?"/"what should
#         the body say?", which is NOT a yes/no
#   - closed-default repo bind .............. repo_clarification.REPO_QUESTION_KIND,
#         but ONLY with a default on offer (payload["default_repo"]) — a crisp
#         "yes" then binds the default and FIRES the held operation; the OPEN
#         repo question ("Which repository...?") is NOT a yes/no (issue 1664's
#         literal defect)
#
# The kind strings are literals here (their home modules import THIS module,
# so importing theirs back would be circular); the #1664 tests pin each
# literal against its source constant so drift fails loudly.
_CONFIRM_KINDS = frozenset(
    {
        DESTRUCTIVE_CONFIRM_KIND,
        "reminder_clear_delete_confirmation",  # reminder_clear.CLEAR_DELETE_CONFIRMATION_KIND
        "consent_check",  # consent_gate.CONSENT_CHECK_KIND
        "unmapped_field_value_clarification",  # intent_service._offer_status_close_clarification
    }
)

_DRAFTED_ISSUE_KIND = "drafted_issue"  # drafted_issue.DRAFTED_ISSUE_KIND
_REPO_QUESTION_KIND = "issue_repo_question"  # repo_clarification.REPO_QUESTION_KIND


def offer_is_confirm(offer: Optional[Dict[str, Any]]) -> bool:
    """#1664 — is the pending offer's open question a yes/no confirm?

    Derived from the offer KIND per the #1650 confirm-kind table (enumerated
    above), never from the carrier workflow_type: repo clarification rides
    CONFIRM_PENDING_ACTION_WORKFLOW with an open "Which repository...?" ask,
    so carrier-derived confirm-ness lied to the router about what kind of
    answer is expected. The two state-dependent rows (drafted-issue file
    confirm, closed-default repo bind) read the payload fields that define
    the state; everything else is a set membership.

    One deliberate fallback: a carrier record with NO kind at all reads as a
    confirm — the only kindless #846 producer was ever this module's own
    destructive-confirmation builder (which now stamps its kind), so a stale
    in-flight record still renders honestly instead of losing its confirm
    marker.
    """
    if not offer:
        return False
    pending = offer.get("pending_action") or {}
    kind = pending.get("kind")
    if kind in _CONFIRM_KINDS:
        return True
    if kind == _DRAFTED_ISSUE_KIND:
        # File confirm only when the draft is fully shaped: with title AND
        # body present the open ask is 'say "file it as is"' — a yes/no.
        # Mid-compose (either slot empty) the open ask is the compose
        # question, and a crisp "yes" is re-asked, not fired blind.
        draft = pending.get("draft") or {}
        return bool((draft.get("title") or "").strip() and (draft.get("body") or "").strip())
    if kind == _REPO_QUESTION_KIND:
        # Closed-default bind only: with a default on offer, a crisp "yes"
        # binds it and fires the held operation (#1650). The open form's
        # "yes" merely re-asks — not a confirm.
        return bool(pending.get("default_repo"))
    return kind is None and offer.get("workflow_type") == CONFIRM_PENDING_ACTION_WORKFLOW


# Context marker the confirm entry point sets before re-dispatching, so the
# close/reopen handlers' own in-message confirmation (#902's "yes, close
# #123" regex) recognizes the rail confirmation and executes in ONE turn
# instead of asking a second time.
CONFIRMED_CONTEXT_KEY = "destructive_confirmed"

# Rail-key families whose handlers were READ (verify-first, 2026-08-10) to
# take every mutating call ONLY after a successful issue-number parse: with
# no number in the message, both handlers run fuzzy-match / clarification
# paths that never write. For those messages the gate passes through — there
# is no blast radius to confirm, and the handler's clarification copy is the
# better turn. ⚠️ Invariant: if either handler ever writes on its no-number
# path, this pass-through must be removed in the same commit.
_CLOSE_FAMILY = frozenset({"close_issue", "close_issue_query"})
_REOPEN_FAMILY = frozenset({"reopen_issue", "reopen_issue_query"})

# #1666: the delete-todo rail family — the canonical action plus the
# ActionMapper raw-emission aliases (remove_todo / cancel_todo → delete_todo)
# that the classifier can emit and workflow_entries registers on the same
# WorkflowEntry. This family's confirm is built by the ASYNC builder below
# (build_todo_delete_confirmation), never by build_confirmation_offer: the
# target is POSITIONAL ("todo 3" is a list index, not an id), so the only
# honest "confirm WHAT, not just WHICH" ask requires the same owner-scoped
# list read the handler itself performs — done once here, one turn earlier,
# with the resolved row BOUND into the intent so the confirmed yes deletes
# exactly what was named in the ask.
_DELETE_TODO_FAMILY = frozenset({"delete_todo", "remove_todo", "cancel_todo"})

# Context key for the gate-time resolution (see build_todo_delete_confirmation):
# {"todo_id": str, "text": str, "number": str}. handle_delete_todo honors it
# ONLY together with CONFIRMED_CONTEXT_KEY — an unconfirmed intent never
# carries a usable binding.
RESOLVED_TODO_CONTEXT_KEY = "delete_todo_resolved"


def is_delete_todo_action(action: Optional[str]) -> bool:
    """True when ``action`` is a delete-todo rail key (#1666 family)."""
    return action in _DELETE_TODO_FAMILY


# Bare full-message exits that cancel a pending confirmation honestly —
# the #888 registry set ∪ the #1529 additions, applied at the offer seam.
# (detect_offer_response's DECLINE_PATTERNS already catch "no"/"nope"/
# "not now"/"never mind"; this covers the exit-verb shapes it misses.)


def _bare_exit_commands() -> frozenset:
    from services.process.escape import BARE_EXIT_COMMANDS
    from services.process.registry import ESCAPE_COMMANDS

    return ESCAPE_COMMANDS | BARE_EXIT_COMMANDS | frozenset({"abort", "don't", "dont"})


def detect_bare_exit(message: str) -> bool:
    """True when the whole message is a bare exit command ("cancel", "stop",
    "forget it") — the #1529 exit tier for a pending confirmation. Exact
    match on the stripped, lowercased full message (Arch guidance on #888)."""
    if not message:
        return False
    return message.strip().lower().rstrip(".!?") in _bare_exit_commands()


@dataclass(frozen=True)
class ConfirmationOffer:
    """What the gate hands back: the question to ask this turn, and the
    pending-offer record (shape documented in the module docstring) to store
    in the #846 session-scoped store."""

    question: str
    offer: Dict[str, Any]


def _issue_number_from(intent: Intent) -> Optional[int]:
    """The same parse the handlers use (their first mutating step is gated on
    it): first ``#N`` / bare number in the original message."""
    message = ""
    if intent.context:
        message = intent.context.get("original_message", "") or ""
    if not message:
        message = intent.original_message or ""
    match = re.search(r"#?(\d+)", message)
    return int(match.group(1)) if match else None


def _issue_title_from(intent: Intent) -> Optional[str]:
    """Cheap-read-only title lookup (#1190 spec: fetch the title only if a
    read is ALREADY available on the path — never issue a new call here).
    Present when an upstream turn (e.g. the #902 fuzzy-match flow) stashed it."""
    if not intent.context:
        return None
    return intent.context.get("issue_title") or intent.context.get("matched_issue_title")


def build_confirmation_offer(intent: Intent) -> Optional[ConfirmationOffer]:
    """Build the confirmation question + pending-action record for a
    DESTRUCTIVE rail intent, or ``None`` to pass through to the handler.

    ``None`` is returned ONLY for the two verified read-only-clarification
    shapes (close/reopen with no parseable issue number — see the
    ``_CLOSE_FAMILY`` invariant note). Unknown destructive actions ALWAYS
    defer (safe default: an unconfirmed destructive write must never fire).
    """
    action = intent.action
    issue_number = _issue_number_from(intent)

    if action in _CLOSE_FAMILY or action in _REOPEN_FAMILY:
        if issue_number is None:
            # Verified read-only clarification path — nothing destructive can
            # fire without a number; let the handler ask "which issue?".
            return None
        verb = "close" if action in _CLOSE_FAMILY else "reopen"
        title = _issue_title_from(intent)
        summary = f"{verb} issue #{issue_number}"
        if title:
            summary += f" '{title}'"
        question = f"{summary[0].upper()}{summary[1:]}? (yes/no)"
    else:
        # Generic carrier: a future destructive rail action lands here with a
        # generic (but honest) question. Refine per-action summaries as
        # consumers arrive.
        # #1571 SHIPPED (2026-08-15): the drafted-issue binding is the
        # carrier's second consumer — it builds its own record in
        # services/intent_service/drafted_issue.py (kind "drafted_issue",
        # armed at the #1510 collaborate turn, accepted via the same
        # run_confirm_pending_action_workflow mirror), not through this
        # builder, which stays destructive-classification-only.
        summary = action.replace("_", " ")
        question = f"Are you sure you want me to {summary}? (yes/no)"

    return ConfirmationOffer(
        question=question,
        offer={
            "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
            # #1665: the rendered ask rides the record — same string the
            # caller returns as the turn's message (built once, above).
            "question": question,
            "pending_action": {
                "kind": DESTRUCTIVE_CONFIRM_KIND,
                "action": action,
                "intent": intent,
                "summary": summary,
            },
            "decline_message": (f"Okay — I won't {summary}. Nothing has been changed."),
        },
    )


# ---------------------------------------------------------------------------
# #1666 — the delete-todo confirm builder (async: positional target needs the
# owner-scoped list read to say WHAT would be deleted).
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class TodoDeleteGate:
    """Outcome of :func:`build_todo_delete_confirmation` — exactly one leg set.

    - ``offer``: arm this confirmation (the resolvable destructive shape).
    - ``passthrough``: dispatch to the rail entry point unconfirmed — used
      ONLY for the verified read-only / non-owning shapes (see builder body).
    - ``error_message``: the todo lookup itself failed — return this honest
      no-op turn directly. Never pass a possibly-deleting turn through
      unverified, and never arm a number-only confirm (#1666 AC: the user
      confirms WHAT, not just WHICH).
    - ``clarification``: a named target resolved to zero or several todos
      (#1527 named-target leg) — return this honest ask/didn't-find turn
      directly. Nothing armed, nothing deleted; it names todos/reminders,
      never projects (the 1527 misroute's exact wound).
    """

    offer: Optional[ConfirmationOffer] = None
    passthrough: bool = False
    error_message: Optional[str] = None
    clarification: Optional[str] = None


# --- #1527 named-target delete: deriving the target WITHOUT new patterns ----
#
# PM live 2026-08-29 (v64): "delete my hydrate reminder" — the phrase Piper
# itself taught — ROUTES correctly post-1527 but then died on this gate's
# no-number passthrough: handle_delete_todo's only no-number answer was
# "Which todo? Try: 'delete todo [number]'". The named target must resolve
# the way complete_todo's already does.
#
# The extraction-pattern ratchet (TestExtractionPatternRatchet, PM-ratified
# the same day) forbids growing the regex micro-parsers, so the target is
# NOT parsed out of the message — it is derived by set subtraction: drop the
# delete-command vocabulary and stopwords, keep the rest, and match THAT
# against the DB list with the shared todo_handlers matcher. String
# filtering against known word sets, zero new interpretation patterns.
_DELETE_COMMAND_NOISE = frozenset(
    {
        # the delete-family verbs this gate's rail actions cover
        "delete",
        "remove",
        "cancel",
        "erase",
        "drop",
        "trash",
        "scrap",
        # "get rid of" (phrasal, #1527's third verb)
        "get",
        "rid",
        # domain nouns — the user names the KIND, the todo text never does
        # ("todo"/"task" are already _STOPWORDS; plurals and "reminder" not)
        "reminder",
        "reminders",
        "todos",
        "tasks",
        # connective/lead-in noise around a named target
        "about",
        "called",
        "titled",
        "named",
        "please",
    }
)


def _named_delete_target(message: str) -> str:
    """The message minus delete-command vocabulary and stopwords, in order.

    "delete my hydrate reminder" → "hydrate"; "delete the reminder to
    hydrate" → "hydrate"; "delete my reminders" → "" (nothing named — the
    caller passes through to the handler's which-todo ask).
    """
    from services.intent_service.todo_handlers import _STOPWORDS

    kept = [
        word
        for word in re.findall(r"\w+", message)
        if word.lower() not in _STOPWORDS and word.lower() not in _DELETE_COMMAND_NOISE
    ]
    return " ".join(kept)


def _armed_todo_delete(
    intent: Intent, todo: Any, position: int, question: str, summary: str
) -> TodoDeleteGate:
    """Bind the resolved row into the intent (list-shift protection: the
    confirmed yes deletes exactly this row by id, never a positional
    re-resolve) and arm the #1190 confirm. Copy-on-write on the context."""
    intent.context = dict(intent.context or {})
    intent.context[RESOLVED_TODO_CONTEXT_KEY] = {
        "todo_id": todo.id,
        "text": todo.text,
        "number": str(position),
    }
    return TodoDeleteGate(
        offer=ConfirmationOffer(
            question=question,
            offer={
                "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
                # #1665: the rendered ask rides the record — the same string
                # the caller returns as the turn's message (built once).
                "question": question,
                "pending_action": {
                    "kind": DESTRUCTIVE_CONFIRM_KIND,
                    "action": intent.action,
                    "intent": intent,
                    "summary": summary,
                },
                "decline_message": (f"Okay — I won't {summary}. Nothing has been changed."),
            },
        )
    )


async def build_todo_delete_confirmation(
    intent: Intent,
    todo_handlers: Any,
    todo_user_id: Any,
) -> TodoDeleteGate:
    """Build the #1190 confirmation for a delete-todo rail intent (#1666).

    Passthrough legs — each verified read-only or non-deleting at the rail
    entry point (mirror of the _CLOSE_FAMILY invariant; if any of these paths
    ever deletes, its passthrough must be removed in the same commit):

    - **clear-family shape** (#1605 boundary, pinned both ways): an ambiguous
      clear/handle/reset utterance the classifier guessed as delete_todo
      belongs to ``reminder_clear.maybe_handle_clear_family``'s three-variant
      flow, which the rail entry point runs FIRST — this gate never steals
      those shapes, and reminder_clear's own delete confirms stay #1190-gated
      inside that flow. Conversely, explicit imperatives ("delete todo 3")
      are ``None`` to ``detect_clear_family_ask`` by its _EXPLICIT_VERB_RE,
      so this gate owns them — the boundary holds in both directions.
    - **no principal**: the entry point returns the auth-required decline.
    - **no parseable todo number AND no named target**: handle_delete_todo
      returns the "Which todo should I remove?" clarification (its only
      no-number path).
    - **number out of range / non-numeric**: handle_delete_todo returns the
      "couldn't find todo #N" / "doesn't look like a number" copy.

    Named-target leg (#1527's remaining scope, PM live 2026-08-29): a
    no-number delete that DOES name a target ("delete my hydrate reminder")
    resolves it against the owner's list with complete_todo's shared matcher
    (exact → fuzzy, same threshold). One match → the title-bound confirm
    arms ('Delete todo: "hydrate"? (yes/no)', DESTRUCTIVE kind, resolved row
    bound). Several → the clarification leg asks which, listing candidates
    by real list position. Zero → the clarification leg answers honestly in
    todo/reminder vocabulary — never a project lookup.
    """
    # Lazy import: reminder_clear imports THIS module (kind constants), so a
    # module-level import back would be circular.
    from services.intent_service.reminder_clear import detect_clear_family_ask

    message = ""
    if intent.context:
        message = intent.context.get("original_message", "") or ""
    if not message:
        message = intent.original_message or ""

    if detect_clear_family_ask(message) is not None:
        return TodoDeleteGate(passthrough=True)

    if todo_user_id is None:
        return TodoDeleteGate(passthrough=True)

    todo_number = todo_handlers._extract_todo_id(message)
    named_target = None
    if todo_number is None:
        named_target = _named_delete_target(message)
        if not named_target:
            # Nothing numbered AND nothing named — the handler's
            # "Which todo should I remove?" ask is the honest turn.
            return TodoDeleteGate(passthrough=True)

    try:
        todos = await todo_handlers.todo_service.list_todos(
            user_id=todo_user_id, include_completed=False
        )
    except Exception as e:  # silent-ok: error-logged; returns an honest no-op turn, never an ungated delete or a number-only confirm
        logger.error(
            "todo_delete_confirm_lookup_failed",
            error=str(e),
            action=intent.action,
        )
        return TodoDeleteGate(
            error_message=(
                "I couldn't look up your todos just now, so I haven't "
                "deleted anything. Try again in a moment."
            )
        )

    if todo_number is not None:
        try:
            idx = int(todo_number) - 1
        except ValueError:
            return TodoDeleteGate(passthrough=True)
        if idx < 0 or idx >= len(todos):
            return TodoDeleteGate(passthrough=True)

        todo = todos[idx]
        # Bind WHAT, not just WHICH (#1666 AC): stash the row resolved AT
        # ASK TIME so the confirmed yes deletes exactly the todo named in
        # the ask, even if the list shifts between the ask and the yes.
        return _armed_todo_delete(
            intent,
            todo,
            idx + 1,
            question=f'Delete todo {todo_number}: "{todo.text}"? (yes/no)',
            summary=f'delete todo {todo_number}: "{todo.text}"',
        )

    # --- named-target leg (#1527 remaining scope) ---------------------------
    # Lazy import (same circularity note as reminder_clear above).
    from services.intent_service.todo_handlers import resolve_named_todo_target

    matches = resolve_named_todo_target(named_target, todos)

    if not matches:
        return TodoDeleteGate(
            clarification=(
                f'I couldn\'t find a todo or reminder matching "{named_target}". '
                "Say 'show my todos' to see the list — nothing has been deleted."
            )
        )

    if len(matches) > 1:
        position_by_id = {t.id: i + 1 for i, t in enumerate(todos)}
        candidates = ", ".join(f'{position_by_id[t.id]}. "{t.text}"' for t in matches)
        return TodoDeleteGate(
            clarification=(
                f'I found {len(matches)} todos matching "{named_target}": '
                f"{candidates}. Which one should I delete? "
                "Try 'delete todo [number]'."
            )
        )

    todo = matches[0]
    position = next(i + 1 for i, t in enumerate(todos) if t.id == todo.id)
    # Same WHAT-binding as the positional leg: the confirmed yes deletes the
    # row named in the ask by id, immune to list shift.
    return _armed_todo_delete(
        intent,
        todo,
        position,
        question=f'Delete todo: "{todo.text}"? (yes/no)',
        summary=f'delete the todo "{todo.text}"',
    )
