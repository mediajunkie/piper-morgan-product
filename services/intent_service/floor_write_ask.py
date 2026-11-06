"""#2219 row 3: a write the classifier filed under a floor category asks, never writes.

Served on alpha 0d4938cf23: after "show my todos", "complete the second one" was
classified CONVERSATION/complete_todo. The #911 Action Gate is category-keyed, so
the turn went to the floor, which can't write and said "If you'd like me to mark
"high task" as complete, just tell me directly." Nothing was written.

Arch 11-06 10:48 (decisions.log): the gate's own predicate,
``IntentService._requires_canonical_handler``, now sends an action whose rail
entry declares a non-READ effect to its handler whatever the category. One
binding condition: a write under a floor category is a contradictory emission
(the classifier said "conversation" and named a write), so its meaning is
uncertain. Such a turn is MARKED (``FLOOR_WRITE_MARK_KEY`` in the intent's
context, set on the main path only when the category alone would have sent it
to the floor, and never on a router emission). On a marked turn no op writes:

- the rail's one consent decision is CONFIRM for every non-READ op, so each
  arms its #1190 yes/no (the delete, unlink and close/reopen builders as today;
  any other write the generic carrier), and "yes" re-dispatches the original
  intent unmarked (``run_confirm_pending_action_workflow`` drops the mark);
- complete (WRITE, so it reaches the confirm branch only when marked) names the
  one row it would complete, in CXO's words ('Mark "high task" as done?
  (yes/no)'); when it can't name one, it picks over the numbered list just
  shown (``delete_todo_pick.arm_complete_pick``), or says it can't tell;
- the #1605 clear-family flow, the one passthrough that could write on its
  first turn (a stored "complete" default, or the trust-inferences auto-apply),
  asks instead (``reminder_clear``, its existing always-ask questions).

The target is read with the complete handler's own extractors and matcher; no
new pattern. A positional-only target ("the second one") names nothing, as in
the delete gate (``destructive_confirm._is_positional_only``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

import structlog

from services.domain.models import Intent

logger = structlog.get_logger(__name__)

# The context flag. Set by the main path (IntentService), read by the rail and
# the clear-family flow, dropped by the confirmed "yes".
FLOOR_WRITE_MARK_KEY = "floor_category_write"

# CXO 11-06: no list was shown, so there's nothing to pick from. A statement,
# since nothing is armed to bind an answer (the #1730 unarmed-ask ratchet).
COMPLETE_NO_TARGET_STATEMENT = "I'm not sure which one you mean. Say its name."


def mark_floor_category_write(intent: Intent) -> None:
    """Mark the turn (copy-on-write: never mutate a context dict others share)."""
    intent.context = dict(intent.context or {})
    intent.context[FLOOR_WRITE_MARK_KEY] = True


def is_floor_category_write(intent: Any) -> bool:
    return bool((getattr(intent, "context", None) or {}).get(FLOOR_WRITE_MARK_KEY))


def unmark_floor_category_write(intent: Any) -> None:
    """The confirmed "yes" is the person's own answer: the intent runs unmarked."""
    context = getattr(intent, "context", None)
    if context and FLOOR_WRITE_MARK_KEY in context:
        intent.context = dict(intent.context or {})
        intent.context.pop(FLOOR_WRITE_MARK_KEY, None)


def complete_confirm_question(text: str) -> str:
    """CXO's words (11-06), verbatim."""
    return f'Mark "{text}" as done? (yes/no)'


@dataclass(frozen=True)
class FloorWriteCompleteAsk:
    """What a marked complete turn does: exactly one of

    - ``offer``: arm this yes/no (the one row it would complete, bound by id);
    - ``reply``: say this (an armed pick when ``armed``, else a statement);
    - neither: pass through to the complete workflow (a clear-family shape,
      whose flow asks on a marked turn, or no principal, which it declines).
    """

    offer: Any = None
    reply: Optional[str] = None
    armed: bool = False
    intent_data: Optional[Dict[str, Any]] = None


async def build_floor_write_complete_ask(
    intent: Intent,
    message: str,
    todo_handlers: Any,
    todo_user_id: Any,
    principal: Optional[str],
    session_id: Optional[str],
    offer_service: Any,
) -> FloorWriteCompleteAsk:
    """The marked complete turn's ask. Writes nothing."""
    from services.intent_service.consent_gate import CONSENT_CHECK_KIND
    from services.intent_service.delete_todo_pick import PICK_PENDING_FLAG, arm_complete_pick
    from services.intent_service.destructive_confirm import (
        CONFIRM_PENDING_ACTION_WORKFLOW,
        ConfirmationOffer,
        _is_positional_only,
    )
    from services.intent_service.reminder_clear import is_clear_family_passthrough
    from services.intent_service.todo_handlers import (
        BATCH_COMPLETE_IDS_KEY,
        BATCH_COMPLETE_LEFT_KEY,
        BATCH_COMPLETE_TEXTS_KEY,
        _split_completion_clause,
        resolve_named_todo_target,
    )

    original = intent.original_message or (intent.context or {}).get("original_message") or ""
    original = original or message or ""
    if todo_user_id is None:
        return FloorWriteCompleteAsk()  # the workflow's auth decline; it writes nothing
    if session_id and is_clear_family_passthrough(original):
        # #1605's own question owns the shape; on a marked turn it only asks. With
        # no session that flow steps aside, so the shape is resolved here instead.
        return FloorWriteCompleteAsk()

    try:
        todos = await todo_handlers.todo_service.list_todos(
            user_id=todo_user_id, include_completed=False
        )
    except (
        Exception
    ) as e:  # silent-ok: error-logged; an honest no-op turn, nothing armed, nothing written
        logger.error("floor_write_complete_lookup_failed", error=str(e))
        return FloorWriteCompleteAsk(
            reply=(
                "I couldn't look up your todos just now, so I haven't changed anything. "
                "Try again in a moment."
            )
        )
    if not todos:
        return FloorWriteCompleteAsk(
            reply=(
                "You don't have any active todos to complete. "
                "Add one with 'add todo: [task]' first."
            )
        )

    primary, _ = _split_completion_clause(original)
    row = None
    number = todo_handlers._extract_todo_id(primary)
    if number is not None:
        try:
            idx = int(number) - 1
        except ValueError:
            idx = -1
        if 0 <= idx < len(todos):
            row = todos[idx]
    else:
        named = todo_handlers._extract_completion_text(primary)
        if named and not _is_positional_only(named):
            matches = resolve_named_todo_target(named, todos)
            if len(matches) == 1:
                row = matches[0]

    if row is not None:
        # The yes completes exactly this row, by id (the #1943 confirmed re-entry
        # in handle_complete_todo_targets), never a fresh match on the words.
        intent.context = dict(intent.context or {})
        intent.context.pop(FLOOR_WRITE_MARK_KEY, None)
        intent.context[BATCH_COMPLETE_IDS_KEY] = [str(row.id)]
        intent.context[BATCH_COMPLETE_TEXTS_KEY] = [row.text]
        intent.context[BATCH_COMPLETE_LEFT_KEY] = []
        question = complete_confirm_question(row.text)
        summary = f'mark "{row.text}" done'
        logger.info("floor_write_complete_confirm_armed", todo_id=str(row.id))
        return FloorWriteCompleteAsk(
            offer=ConfirmationOffer(
                question=question,
                offer={
                    "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
                    "question": question,
                    "pending_action": {
                        "kind": CONSENT_CHECK_KIND,
                        "action": intent.action,
                        "intent": intent,
                        "summary": summary,
                    },
                    "decline_message": f"Okay — I won't {summary}. Nothing has been changed.",
                },
            )
        )

    question = arm_complete_pick(
        original, session_id, principal, todo_user_id, todos, offer_service
    )
    if question is not None:
        return FloorWriteCompleteAsk(
            reply=question, armed=True, intent_data={PICK_PENDING_FLAG: True}
        )
    return FloorWriteCompleteAsk(reply=COMPLETE_NO_TARGET_STATEMENT)
