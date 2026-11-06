"""#1987 (half 2) — the which-todo ask lists the candidates and ARMS the pick.

CXO's addition on #1987 (Web's alpha run, 651756d520, 2026-10-12): after two
reminders were just set, `delete a reminder` was answered "Which todo should
I remove? Try: 'delete todo [number]'" — the generic prompt. The user has
to leave the chat and find numbers. CXO's bar: when the candidates are known
and few, list them (numbered, with titles) in the question itself.

Arch's condition (the #2000 unarmed-ask census row on
``TodoIntentHandlers.handle_delete_todo``): the numbered pick must ARM via
the #846 pending-offer store, not ride ``last_numbered_list`` alone — the
answer turn ("2", "the first one", "water the plants") binds against the
list the question named (#1665: the rendered candidates ride the record),
never a fresh classification.

The shape is the #1906 pick-target carrier's, with one difference: a
reminder-clear pick re-enters the clear flow's own act path, whereas this
pick re-enters the #1666 title-bound DESTRUCTIVE confirm — delete ALWAYS
confirms (Arch's ruling carried from #1666), so the bound pick arms CXO's
D1 'Delete the reminder "X"? (yes/no)' (issue 2046: the one form on every
leg; "to-do" only when the user said it) with the row bound BY ID into the intent
(``destructive_confirm._armed_todo_delete``), and the confirmed yes deletes
exactly that row through the unchanged #1666 path. Two short questions, each
armed, rather than one unarmed prompt that sends the user to another page.

Binding is the SHARED #1906 binder (``reminder_clear._resolve_pick_target``:
ordinal / unambiguous status word / name match) — not reimplemented, and no
new extraction regex (the #1595 ratchet is untouched; the only text reads
here are word-set checks).

Candidates: the user's active rows, scoped to reminders (rows carrying a
``reminder_date``) when the ask says "reminder(s)", due-soonest first; at
most ``MAX_LISTED`` are shown and bound (the question names exactly what the
pick can choose from; a longer list says how many more there are and how to
see them). No candidates → an honest "nothing to delete" line, nothing armed
(not a question, so not an unarmed ask).
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional
from uuid import UUID

import structlog

from services.domain.models import Intent
from services.shared_types import IntentCategory

logger = structlog.get_logger(__name__)

# The #846 record kind (handled kind-specifically at the pop seam, before
# generic accept/decline — the same sanctioned seam the #1605/#1906 turns use).
DELETE_PICK_KIND = "delete_todo_pick_question"
# The registered offer-only workflow (action_triggered=False): the generic
# seam's ACCEPT path lands a bare "yes" here, which re-asks and re-arms.
CLARIFY_DELETE_PICK_WORKFLOW = "clarify_delete_todo_pick"
# The intent_data flag the ARM turn stamps so ``_apply_soft_offer`` never
# clobbers the one-slot store with a soft workflow offer (the #1648 belt).
PICK_PENDING_FLAG = "delete_todo_pick_pending"
# "Few" — CXO's word. Above this the question still lists this many (bound)
# and says how many more there are.
MAX_LISTED = 5

_REMINDER_WORDS = frozenset({"reminder", "reminders"})
# The pre-classifier's pleasantry-only claims (its own GREETING / THANKS
# pattern sets; nothing re-declared here) that an armed pick survives, and
# the one-line acknowledgement each gets before the open question (with its
# numbered list) is repeated. CXO's copy (2026-10-13 09:50 ruling, which
# superseded the 09:40 "nothing has been deleted yet" prefix): the plain
# ack — "You're welcome." matches the canned thanks constant, so there is
# one string, not two — and the numbered question directly under it already
# says nothing is done. FAREWELL RELEASES (CXO, both rulings): the user is
# leaving, not answering — the pick drops via the pop and the canned
# "Goodbye for now." serves unchanged.
_PLEASANTRY_ACTIONS = frozenset({"greeting", "thanks"})
_PLEASANTRY_ACK = {
    "thanks": "You're welcome.",
    "greeting": "Hi!",
}


# Issue 2019: answers that point at EVERY shown candidate. A word-set check
# (the _mentions_reminder idiom), not a message-parsing regex.
_ALL_CANDIDATE_WORDS = frozenset({"both", "all", "every", "everything"})


def _multi_pick_indices(text: str, texts: List[str], due_iso: List[Optional[str]]) -> List[int]:
    """The shown positions an answer names when it names MORE than one
    ("1 and 2", "the first and the last", "both"), in shown order; [] when it
    names one or none (the single-bind path below is unchanged).

    Reuses the shared binder's own ordinal reader one word at a time (no new
    pattern). A quantifier ("both", "all of them") counts only when the
    whole-answer binder does not bind a single candidate, so a title that
    happens to contain "all" still binds by name."""
    from services.intent_service.reminder_clear import _ordinal_index, _resolve_pick_target

    n = len(texts)
    words = [w.strip(".,!?;:'\"()").lower() for w in (text or "").split()]
    picked: List[int] = []
    for word in words:
        idx = _ordinal_index(word, n) if word else None
        if idx is not None and idx not in picked:
            picked.append(idx)
    if len(picked) > 1:
        return sorted(picked)
    if n > 1 and set(words) & _ALL_CANDIDATE_WORDS:
        status, _ = _resolve_pick_target(text, texts, due_iso)
        if status != "bound":
            return list(range(n))
    return []


def _mentions_reminder(message: str) -> bool:
    words = {w.strip(".,!?;:'\"").lower() for w in (message or "").split()}
    return bool(words & _REMINDER_WORDS)


# #2294 (Arch 11-06 08:06): a legacy ``delete_item`` emission reaches the delete path
# only when Piper just showed a numbered list; with none, this ask, and nothing is
# deleted. CXO's words (11-06 08:18); a statement, not a question, since nothing is
# armed to bind an answer (the #1730 unarmed-ask ratchet).
DELETE_ITEM_NO_LIST_ASK = (
    "I'm not sure which one you mean, because I haven't shown you a list to count "
    "from. Nothing was deleted. Tell me the name of the todo or reminder you want "
    "to delete."
)


def _last_list_kind(session_id: Optional[str], user_id: Any) -> Optional[str]:
    """The kind of the last numbered list this session showed, or None."""
    shown = last_numbered_list(session_id, user_id)
    return shown.kind if shown is not None else None


def last_numbered_list(session_id: Optional[str], user_id: Any) -> Any:
    """``ConversationContext.last_numbered_list`` for the session; None on any miss."""
    if not session_id:
        return None
    try:
        from services.intent_service.conversation_context import get_or_create_context

        return get_or_create_context(session_id, user_id=user_id).last_numbered_list
    except Exception as e:  # silent-ok: logged; read as "no list shown" (the honest ask)
        logger.warning("delete_pick_list_recall_failed", error=str(e), session_id=session_id)
        return None


def _shown_lines(shown: Any, todos: List[Any]) -> List[List[Any]]:
    """The open copies of each line of the last numbered todo LIST shown (#2219
    Gap A records ``groups`` only for "show my todos"), in shown order; a line
    with no open copy left is dropped. ``[]`` when no such list was shown."""
    groups = getattr(shown, "groups", None) or []
    if not groups:
        return []
    by_id = {str(t.id): t for t in todos or []}
    lines = [[by_id[str(i)] for i in group if str(i) in by_id] for group in groups]
    return [line for line in lines if line]


def _line_display(line: List[Any]) -> str:
    """A pick line as the list showed it (CXO 11-06): the count and the chip."""
    first = line[0]
    text = first.text + (f" (×{len(line)})" if len(line) > 1 else "")
    if getattr(first, "priority", None) == "urgent":
        text += " (urgent)"
    elif getattr(first, "priority", None) == "high":
        text += " (high)"
    return text


def _candidates(todos: List[Any], noun: str) -> List[Any]:
    """Reminders (rows with a reminder_date), due-soonest first, when the
    ask said "reminder"; otherwise every active row in list order."""
    if noun != "reminder":
        return list(todos)
    from services.utils.datetime_utils import ensure_utc

    rows = [t for t in todos if getattr(t, "reminder_date", None) is not None]
    return sorted(rows, key=lambda t: ensure_utc(t.reminder_date))


def render_pick_question(noun: str, texts: List[str], more: int = 0, reasked: bool = False) -> str:
    """The armed ask: the candidates numbered with their titles, then how to
    answer — and the #1920 exit ("never mind") so the user learns they can
    bail before failing once."""
    head = (
        f"Still not sure which {noun} you mean — you have:"
        if reasked
        else f"Which {noun} should I delete?"
    )
    lines = [head] + [f"{i}. {t}" for i, t in enumerate(texts, 1)]
    tail = "Say the number or the name, or 'never mind' to leave them alone."
    if more:
        tail = f"(+{more} more — say 'show my todos' for the full list.) " + tail
    # #2002: the chat page renders replies as Markdown (marked). A line that
    # follows a list item with no blank line is a lazy continuation of that
    # item, so the tail used to render INSIDE the last <li>. The blank line
    # makes it its own paragraph after the list.
    return "\n".join(lines) + "\n\n" + tail


def _pick_offer(
    principal: Optional[str],
    noun: str,
    ids: List[str],
    texts: List[str],
    due_iso: List[Optional[str]],
    original_message: str,
    question: str,
    reasked: bool = False,
    copies: Optional[List[int]] = None,
    display: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """The #846 record: the rendered candidates bound at ARM time (ids +
    texts in the order shown, #1665) plus each one's due timestamp so "the
    overdue one" binds offline on the answer turn (the #1906 idiom)."""
    return {
        "workflow_type": CLARIFY_DELETE_PICK_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": DELETE_PICK_KIND,
            "action": CLARIFY_DELETE_PICK_WORKFLOW,
            "user_id": principal,
            "noun": noun,
            "pick_ids": list(ids),
            "pick_texts": list(texts),
            "pick_due": list(due_iso),
            "original_message": original_message,
            "pick_reasked": reasked,
            "summary": f"pick which {noun} to delete",
            # #2219 interim (c): the shown list's copy counts and its lines as shown.
            "pick_copies": list(copies) if copies else None,
            "pick_display": list(display) if display else None,
        },
        "decline_message": (f"Okay — I haven't touched your {noun}s. Nothing has been deleted."),
    }


async def arm_delete_pick(
    message: str,
    session_id: Optional[str],
    principal: Optional[str],
    todo_user_id: Any,
    todo_service: Any,
    offer_service: Any,
) -> Optional[str]:
    """The ARM half, called by ``handle_delete_todo`` when the message names
    no number (and the #1666 gate's legs found no name and no referent).

    Returns the turn's message — the armed numbered question, or the honest
    "nothing to delete" line — or ``None`` when the ask cannot be armed here
    (no session, no store, or the list read failed), in which case the
    caller keeps its non-interrogative fallback instruction.
    """
    if not session_id or offer_service is None or todo_service is None:
        return None
    # #2294 (Arch 11-06 08:06, CXO 08:06): the #2219 noun rule, so after a reminders
    # list the pick asks "Which reminder…?" and its candidates are the reminders.
    from services.intent_service.reminder_copy import conversation_noun

    noun = conversation_noun(message, _last_list_kind(session_id, principal or todo_user_id))
    try:
        todos = await todo_service.list_todos(user_id=todo_user_id, include_completed=False)
    except Exception as e:  # silent-ok: warning-logged; the caller falls back to its instruction copy, nothing armed, nothing deleted
        logger.warning("delete_todo_pick_list_failed", error=str(e), user_id=str(todo_user_id))
        return None
    from services.intent_service.reminder_clear import _due_iso

    # #2219 interim (c) (Arch 11-06 09:58; CXO's words 10:1x): a delete with no
    # router target, right after the numbered todo list, picks over THAT list's
    # lines, in its order and grouping, so "2" means the line the person saw. Code
    # reads recorded state here, never the message's words.
    lines = _shown_lines(last_numbered_list(session_id, principal or todo_user_id), todos)
    if lines:
        ids = [str(line[0].id) for line in lines]
        texts = [line[0].text for line in lines]
        due = [_due_iso(line[0], noun) for line in lines]
        copies = [len(line) for line in lines]
        display = [_line_display(line) for line in lines]
        question = render_pick_question(noun, display)
        offer_service.set_pending_offer(
            session_id,
            _pick_offer(
                principal, noun, ids, texts, due, message, question, copies=copies, display=display
            ),
            user_id=principal,
        )
        logger.info(
            "delete_todo_pick_armed_on_shown_lines", session_id=session_id, lines=len(lines)
        )
        return question
    candidates = _candidates(todos or [], noun)
    if not candidates:
        return f"You don't have any {noun}s right now — nothing to delete."
    shown = candidates[:MAX_LISTED]
    more = len(candidates) - len(shown)

    ids = [str(t.id) for t in shown]
    texts = [t.text for t in shown]
    due = [_due_iso(t, noun) for t in shown]
    question = render_pick_question(noun, texts, more)
    offer_service.set_pending_offer(
        session_id,
        _pick_offer(principal, noun, ids, texts, due, message, question),
        user_id=principal,
    )
    logger.info(
        "delete_todo_pick_armed",
        session_id=session_id,
        noun=noun,
        listed=len(shown),
        more=more,
    )
    return question


async def handle_delete_todo_pick_turn(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """The ANSWER half, at the pop seam (before generic accept/decline).

    A bound pick arms the #1666 title-bound confirm with the row bound by
    id; the confirmed yes deletes exactly that row. Returns ``None`` to fall
    through to the generic seam for a state question (LOW_CEREMONY: the
    seam re-arms silently and normal processing answers), a decline (the
    honest ``decline_message``), a bare accept (the registered landing
    re-asks), or a released command (routes normally). A pure pleasantry
    (thanks / greeting) SURVIVES: the record is re-armed here and the reply
    acknowledges, then repeats the question with its list (Arch's condition
    3; CXO's copy). A farewell releases (CXO's ruling).
    """
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != DELETE_PICK_KIND:
        return None
    text = (message or "").strip()
    if not text:
        return None

    from services.intent_service.reminder_clear import (
        _principal_mismatch,
        _quoted_name,
        _resolve_pick_target,
    )

    if _principal_mismatch(payload, user_id):
        logger.warning(
            "delete_todo_pick_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": "Let's hold off on that — nothing has been changed.",
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_DELETE_PICK_WORKFLOW,
                "principal_mismatch": True,
            },
        }

    from services.intent_service.acceptance import (
        AcceptanceVerdict,
        declared_axes_for_workflow,
        evaluate_acceptance,
    )

    axes = declared_axes_for_workflow(CLARIFY_DELETE_PICK_WORKFLOW)
    verdict = evaluate_acceptance(
        text,
        effect=axes[0] if axes else None,
        outwardness=axes[1] if axes else None,
        armed_question=pending_offer.get("question"),  # #1665: threaded from the record
    )
    if verdict is AcceptanceVerdict.STATE_QUESTION:
        logger.info("delete_todo_pick_state_question_falls_through", session_id=session_id)
        return None
    if verdict is AcceptanceVerdict.DECLINE:
        logger.info("delete_todo_pick_declined", session_id=session_id)
        return None
    if verdict is AcceptanceVerdict.ACCEPT:
        logger.info("delete_todo_pick_bare_accept", session_id=session_id)
        return None  # names nothing — the registered landing re-asks + re-arms

    ids = payload.get("pick_ids") or []
    texts = payload.get("pick_texts") or []
    shown_texts = payload.get("pick_display") or texts
    due_iso = payload.get("pick_due") or []
    noun = payload.get("noun") or "todo"
    original_message = payload.get("original_message") or ""

    # Arch's condition 3 on #1987 (2026-10-12 ruling; 2026-10-13 ask): the
    # pick must SURVIVE a pleasantry. "thanks" reads PASS at the acceptance
    # seam, binds nothing, and surface-1 pre_classify CLAIMS it — so without
    # this branch the release discriminator below dropped the armed pick and
    # the user's next "2" bound nothing (the turn-9 drop CXO raised, on an
    # armed slot). A pure pleasantry (greeting / thanks / farewell, the
    # pre-classifier's own pleasantry-only claim — no new pattern) re-arms
    # the SAME record and answers with a short acknowledgement plus the
    # open question and its list (CXO's copy, 2026-10-13). Farewell is NOT
    # in the set: CXO ruled it releases (the user is leaving, not
    # answering) — it falls through to the discriminator like any claimed
    # turn and the canned "Goodbye for now." serves.
    # Beside STATE_QUESTION in spirit; handled here rather than at the
    # generic seam because the pop already cleared the slot.
    from services.intent_service.pre_classifier import PreClassifier

    claimed = PreClassifier.pre_classify(text)
    if claimed is not None and claimed.action in _PLEASANTRY_ACTIONS:
        question = pending_offer.get("question") or render_pick_question(noun, shown_texts, 0)
        intent_service.workflow_offer_service.set_pending_offer(
            session_id,
            {
                "workflow_type": CLARIFY_DELETE_PICK_WORKFLOW,
                "question": question,
                "pending_action": dict(payload),
                "decline_message": (
                    f"Okay — I haven't touched your {noun}s. Nothing has been deleted."
                ),
            },
            user_id=user_id,
        )
        logger.info(
            "delete_todo_pick_survives_pleasantry",
            session_id=session_id,
            pleasantry=claimed.action,
        )
        return {
            "message": f"{_PLEASANTRY_ACK[claimed.action]}\n{question}",
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_DELETE_PICK_WORKFLOW,
                PICK_PENDING_FLAG: True,
                "pick_survived_pleasantry": claimed.action,
            },
            "requires_clarification": True,
        }

    # Issue 2019 (xian 2026-10-14, interim until soft delete): an answer that
    # names several candidates arms NO delete and deletes nothing; CXO's
    # capped reply names them in the order shown. The pick is not re-armed
    # ("Tell me which one" is an instruction, not an offer).
    multi = [i for i in _multi_pick_indices(text, texts, due_iso) if i < len(ids)]
    if len(multi) > 1:
        from services.intent_service.delete_cap import (
            DELETE_CAPPED_FLAG,
            capped_delete_reply,
            remember_capped_list,
        )

        multi_texts = [texts[i] for i in multi]
        remember_capped_list(session_id, user_id, [ids[i] for i in multi], multi_texts, f"{noun}s")
        logger.info("delete_todo_pick_capped", session_id=session_id, count=len(multi))
        return {
            "message": capped_delete_reply(multi_texts, noun),
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_DELETE_PICK_WORKFLOW,
                DELETE_CAPPED_FLAG: True,
            },
        }

    status, idx = _resolve_pick_target(text, texts, due_iso)
    if status == "bound" and idx is not None and 0 <= idx < len(ids):
        copies = payload.get("pick_copies") or []
        return await _arm_bound_delete(
            ids[idx],
            texts[idx],
            noun,
            original_message,
            session_id,
            user_id,
            payload,
            intent_service,
            copies=copies[idx] if idx < len(copies) else 1,
        )

    # #2003 (served on alpha b713b91cb5, 2026-10-13): a QUOTED name that
    # matches no candidate is a named miss, not a bare unresolved turn —
    # say so, re-show the same list, stay armed with the record unchanged,
    # guess nothing. (The binder no longer fuzzy-matches a quoted name at
    # all, and an unquoted sibling title — "…alpha one" against "…alpha
    # two" — is 'none' too; that one takes the ordinary re-ask below.)
    quoted = _quoted_name(text)
    if status == "none" and quoted:
        question = render_pick_question(noun, shown_texts, 0)
        intent_service.workflow_offer_service.set_pending_offer(
            session_id,
            _pick_offer(
                payload.get("user_id"),
                noun,
                ids,
                texts,
                due_iso,
                original_message,
                question,
                reasked=bool(payload.get("pick_reasked")),
                copies=payload.get("pick_copies"),
                display=payload.get("pick_display"),
            ),
            user_id=user_id,
        )
        logger.info("delete_todo_pick_named_miss", session_id=session_id)
        return {
            "message": f'I don\'t see a {noun} called "{quoted}".\n\n{question}',
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_DELETE_PICK_WORKFLOW,
                PICK_PENDING_FLAG: True,
                "pick_named_miss": True,
            },
            "requires_clarification": True,
        }

    # Unresolved. A command-shaped turn releases (the #1906 discriminator:
    # surface-1 pre_classify first, then the router-read oracle for a
    # cross-family write) — an unrelated command is never swallowed as a
    # failed pick.
    from services.intent_service.pre_classifier import PreClassifier

    claimed = PreClassifier.pre_classify(text)
    if claimed is not None:
        logger.info(
            "delete_todo_pick_command_released",
            session_id=session_id,
            claimed_action=claimed.action,
        )
        return None

    from services.intent_service.inversion_live import (
        read_op_claims_turn,
        registry_category_for,
    )

    read_op = await read_op_claims_turn(
        text,
        session_id=session_id,
        user_id=user_id,
        intent_service=intent_service,
        carrier_category=registry_category_for("delete_todo"),
    )
    if read_op is not None:
        logger.info(
            "delete_todo_pick_command_released", session_id=session_id, claimed_action=read_op
        )
        return None

    if payload.get("pick_reasked"):
        logger.info("delete_todo_pick_release_after_reask", session_id=session_id)
        return None  # second unresolved turn in a row — release, no loop

    question = render_pick_question(noun, shown_texts, 0, reasked=True)
    intent_service.workflow_offer_service.set_pending_offer(
        session_id,
        _pick_offer(
            payload.get("user_id"),
            noun,
            ids,
            texts,
            due_iso,
            original_message,
            question,
            reasked=True,
            copies=payload.get("pick_copies"),
            display=payload.get("pick_display"),
        ),
        user_id=user_id,
    )
    logger.info("delete_todo_pick_reasked", session_id=session_id)
    return {
        "message": question,
        "intent_data": {
            "category": "execution",
            "action": CLARIFY_DELETE_PICK_WORKFLOW,
            PICK_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }


async def _arm_bound_delete(
    todo_id: str,
    text: str,
    noun: str,
    original_message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    payload: Dict[str, Any],
    intent_service: Any,
    copies: int = 1,
) -> Dict[str, Any]:
    """A bound pick → the #1666 title-bound confirm, row bound BY ID. The
    row is re-read first: a pick that names a row gone since the ask gets
    the #1987 didn't-find line, nothing armed."""
    from services.intent_service.destructive_confirm import _armed_todo_delete
    from services.intent_service.todo_handlers import _delete_confirm_question

    principal = str(user_id) if user_id else payload.get("user_id")
    try:
        todo_user_id = UUID(str(principal))
    except (ValueError, TypeError):
        return {
            "message": "I need you to be logged in to delete todos. Nothing has been changed.",
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_DELETE_PICK_WORKFLOW,
                "error_type": "AuthenticationRequired",
            },
        }
    todo_service = intent_service.todo_handlers.todo_service
    try:
        todos = await todo_service.list_todos(user_id=todo_user_id, include_completed=False)
    except Exception as e:  # silent-ok: error-logged with exc_info; honest no-op copy, nothing armed, nothing deleted
        logger.error("delete_todo_pick_list_failed", error=str(e), exc_info=True)
        return {
            "message": (
                "I couldn't look up your todos just now, so I haven't deleted anything. "
                "Try again in a moment."
            ),
            "intent_data": {"category": "execution", "action": CLARIFY_DELETE_PICK_WORKFLOW},
        }
    row = next((t for t in todos or [] if str(t.id) == str(todo_id)), None)
    if row is None:
        return {
            "message": (
                f'I can\'t find "{text}" anymore — it may already have been removed. '
                "Say 'show my todos' to see the list — nothing has been deleted."
            ),
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_DELETE_PICK_WORKFLOW,
                "pick_target_gone": True,
            },
        }
    position = next(i + 1 for i, t in enumerate(todos) if str(t.id) == str(row.id))
    intent = Intent(
        category=IntentCategory.EXECUTION,
        action="delete_todo",
        original_message=original_message,
        confidence=1.0,
        context={"original_message": original_message},
    )
    # Issue 2046: one confirm form on every leg. ``noun`` here scopes the
    # CANDIDATES ("todo" = every active row); the COPY noun is the user's
    # own word — "reminder" unless they said "to-do".
    from services.intent_service.reminder_copy import copy_noun, delete_summary_phrase

    copy = "reminder" if noun == "reminder" else copy_noun(original_message)
    if copies > 1:
        # #2219 (CXO 11-06 08:30): one copy of a grouped line says the count; the
        # #2019 cap holds, so the confirm deletes exactly this one row.
        from services.intent_service.todo_handlers import grouped_delete_confirm_question

        question = grouped_delete_confirm_question(row.text, copies, copy)
    else:
        question = _delete_confirm_question([row.text], [], copy)
    summary = delete_summary_phrase(row.text, copy)
    gate = _armed_todo_delete(intent, row, position, question=question, summary=summary, noun=copy)
    if copies > 1:
        from services.intent_service.destructive_confirm import RESOLVED_TODO_CONTEXT_KEY

        intent.context[RESOLVED_TODO_CONTEXT_KEY]["copies"] = copies
    confirmation = gate.offer
    assert confirmation is not None  # _armed_todo_delete always arms (the offer leg)
    intent_service.workflow_offer_service.set_pending_offer(
        session_id, confirmation.offer, user_id=user_id
    )
    logger.info("delete_todo_pick_bound", session_id=session_id, todo_id=str(row.id))
    return {
        "message": question,
        "intent_data": {
            "category": "execution",
            "action": "delete_todo",
            "delete_todo_pick_bound": True,
            "destructive_confirmation_pending": True,
        },
        "requires_clarification": True,
    }


async def run_clarify_delete_todo_pick_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing for the pick (registered
    ``clarify_delete_todo_pick``, action_triggered=False): a bare "yes"
    names no candidate — re-ask and re-arm. effect: READ (nothing written;
    the bind happens on an ANSWERED turn at the pop seam)."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != DELETE_PICK_KIND or intent_service is None:
        logger.error(
            "delete_todo_pick_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    noun = payload.get("noun") or "todo"
    texts = payload.get("pick_display") or payload.get("pick_texts") or []
    question = "Just so I get it right:\n" + render_pick_question(noun, texts, 0)
    intent_service.workflow_offer_service.set_pending_offer(
        session_id,
        {
            "workflow_type": CLARIFY_DELETE_PICK_WORKFLOW,
            "question": question,
            "pending_action": dict(payload),
            "decline_message": (
                f"Okay — I haven't touched your {noun}s. Nothing has been deleted."
            ),
        },
        user_id=user_id,
    )
    return {
        "message": question,
        "intent_data": {
            "category": "execution",
            "action": CLARIFY_DELETE_PICK_WORKFLOW,
            PICK_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }
