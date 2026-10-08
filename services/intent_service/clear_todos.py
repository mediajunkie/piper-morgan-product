"""Clear-family build plan piece 2 (2026-10-07) — ``clear_todos``, a RESOLVER
rail entry (Arch's ruling 2026-10-06, binding): mutates nothing, resolves
WHICH operation an ambiguous "clear/handle/take care of/reset" ask over the
reminder/todo domain means (mark done, or delete), and re-enters the
action-dispatch rail as a concrete ``complete_todo`` or ``delete_todo``
Intent carrying the SAME router args — so that op's own gates (consent,
the #1190 enumerating confirm) run unchanged. ``clear_todos`` never calls
``todo_handlers`` directly; every execution leg goes through
``workflow_dispatcher.dispatch_workflow`` (the ``run_confirm_pending_action_
workflow`` rail-re-entry precedent), per Arch's ruling.

ADR-080 D1: the router decides meaning (which items — ``inversion_args.
targets``/``exclude``, already extracted by the Inversion router under
complete_todo's mini-grammar). This module never regexes the user's message
for meaning; it only RESOLVES the router's tokens against real data (D2) and
renders the CXO-ruled disambiguation copy. The verb word said in copy is
always literally "clear" and the noun is always "reminder" (CXO's family
rule, 2026-10-06 ruling point 1 — "Use the user's noun? NO for the new
strings"), regardless of which clear-family synonym ("handle", "take care
of", "reset") the router mapped to this action — parsing the message for
WHICH synonym was said would itself be new interpretation code (D1), which
this build does not add.

Copy sources, all read in full on 2026-10-07 before this file was written:
- CXO ruling: mailboxes/lead/read/rule-cxo-to-lead-cc-arch-ppm-clear-family-
  strings-sets-confirm-first-numbered-list-ratified-two-small-fixes-2026-10-06.md
- Arch ruling: mailboxes/lead/read/rule-arch-to-lead-cc-cxo-ppm-exec-strings-
  ok-scope-is-d4-clear-todos-as-resolver-entry-catalog-change-full-rescore-
  2026-10-06.md
- Build plan: dev/2026/10/07/clear-family-resolver-build-plan-2026-10-07.md

⚠️ One deliberate deviation from the CXO memo's literal example text, and
why: the memo's variant-1-with-set example renders "Before I touch THEM —
…", but the ACTUAL ratified #1605 function (``reminder_clear.
variant_one_question``, test-pinned verbatim) emits "Before I touch THESE
— …". The memo's "Everything after 'Before I touch them' is the ratified
#1605 sentence, unchanged" instruction is honored by calling that function
directly rather than hand-transcribing the memo's paraphrase — the source
function, not a quoted example of it, is the copy-seam authority here (the
module's own "a drifted word is a bug" discipline). This build's output
therefore says "these", matching the test-pinned source.

⚠️ Second deviation, and why: the verb-answer-turn re-entry (the "no stored
verb" branch's answer) is NOT routed through ``_handle_verb_answer_turn``
(reminder_clear.py) — that function is RATIFIED #1605 behavior, shared by
the OLD regex-triggered carrier, and redirecting it through the new
router-args rail for every caller risks changing #1605's tested behavior
for messages that never touch this new resolver. Instead: this module arms
the EXISTING ``_verb_question_offer`` carrier (same kind, same offer shape
— ids/texts ARE already parameters of that function, so no carrier change
was needed to bind them) with one added marker key
(``clear_todos_resolver``), and ``reminder_clear._handle_verb_answer_turn``
gets a 3-line, purely-additive early-return guard at its very top: when the
marker is present, delegate to THIS module's own answer handler instead of
running any of the ratified code below that guard. Every existing caller
(the old regex-triggered ``maybe_handle_clear_family`` offers) never sets
the marker, so #1605's ratified code path is byte-for-byte unreached and
unchanged for them. See the guard in reminder_clear.py for the one-line
citation back to this module AND its NAMED RETIREMENT condition (Arch's
2026-10-07 ruling point 1): this guard is an interim transition shape,
deleted — along with the ratified code it guards — once ``clear_todos``
flips live and ``detect_clear_family_ask`` retires.

Re-entry Intents (every branch below, and the verb-answer handler) carry
the SAME ``original_message`` the resolver was called with — NOT blanked.
Arch's 2026-10-07 ruling, point 2, corrected an earlier version of this
build that blanked the message to stop ``reminder_clear.
maybe_handle_clear_family`` reclaiming the re-entered turn via its own
regex seam: blanking destroyed information every downstream consumer might
read (decline copy, logging, consent framing) and fought #1942's
one-Intent-shape guarantee. Instead, every re-entered Intent's context
carries ``reminder_clear.CLEAR_FAMILY_RESOLVED_KEY: True`` — a CODE-WRITTEN
marker, never sourced from ``inversion_args`` or any user input — and
``maybe_handle_clear_family`` stands down unconditionally when it sees that
key (reminder_clear.py, checked first thing in that function).

CXO ruling 4 ("if the answer turn carries its own targets/exclude … refine
the set") IS implemented, via Arch's 2026-10-07 generalization of the
#1886(b) armed-turn consult (point 3): ``handle_clear_todos_verb_answer``
calls ``armed_turn_consult.classify_armed_reply`` with
``answering_operations={"complete_todo", "delete_todo"}``. When the router
names one of those two operations at/above the live-consult threshold,
THAT operation is the answer, and its own ``args`` (the SAME
``inversion_args`` shape the router always produces) refine the bound shown
set — resolved by ``_refine_bound_set`` against the IDS/TEXTS the offer
actually bound (never re-reading the router's token list as a set on its
own; D2). Any OTHER operation at/above threshold releases (a genuinely new
ask). The router's ``none`` outcome, CLARIFY, sub-threshold, a consult
error, or no key all fall back to the ORIGINAL #1605 crisp-claim regex
parse on the UNREFINED bound set — never a guess, and the concrete op's own
rail re-entry always re-renders the (possibly refined) set in its confirm
or disclosure before anything executes.
"""

from __future__ import annotations

import re
from typing import Any, Dict, FrozenSet, List, Optional, Tuple

import structlog

logger = structlog.get_logger(__name__)

# The marker on a ``reminder_clear._verb_question_offer`` pending_action
# payload that tells reminder_clear._handle_verb_answer_turn to delegate the
# answer turn to THIS module instead of running #1605's ratified inline
# completion. Never set by the old regex-triggered carrier.
CLEAR_TODOS_RESOLVER_MARKER = "clear_todos_resolver"

# Context marker threaded onto the re-entered complete_todo/delete_todo
# Intent so that op's own confirmed-reentry can tell "this mutation was
# reached via the clear-family resolver" — todo_handlers.
# handle_complete_todo_targets reads this to append the variant-2 disclosure
# to its post-"yes" summary (CXO ruling point 2's "then" clause).
VIA_CLEAR_VERB_CONTEXT_KEY = "via_clear_verb"

# Arch's 2026-10-07 ruling, point 3: the verb carrier's own answering set
# for the generalized #1886(b) armed-turn consult — the two verb choices
# this resolver could have re-entered as. See armed_turn_consult.py's
# module docstring ("PER-CARRIER ANSWERING OPERATIONS") for the full
# contract.
_ANSWERING_OPERATIONS: FrozenSet[str] = frozenset({"complete_todo", "delete_todo"})

_CLEAR_VERB_LITERAL = "clear"
_CLEAR_NOUN_LITERAL = "reminder"


def _rail_reentry_context(icx: Dict[str, Any]) -> Dict[str, Any]:
    """Context for a rail-re-entry Intent (complete_todo / delete_todo).

    Arch's 2026-10-07 ruling, point 2 (superseding this function's earlier
    behavior, which blanked ``original_message``): ``inversion_args`` AND
    ``original_message`` both carry forward UNCHANGED — the message is
    never blanked. The earlier mechanism (dropping the message so
    ``reminder_clear.maybe_handle_clear_family``'s own regex seam,
    ``detect_clear_family_ask``, couldn't re-claim the re-entered turn)
    destroyed information every downstream consumer might read (decline
    copy, logging, consent framing) and fought #1942's one-Intent-shape
    guarantee (``Intent.__post_init__`` mirrors the message into both
    ``original_message`` and ``context["original_message"]`` — blanking one
    without the other would have created a third, unmirrored shape).
    ``maybe_handle_clear_family`` now stands down on a CODE-WRITTEN marker
    instead (``reminder_clear.CLEAR_FAMILY_RESOLVED_KEY`` — set by every
    caller of this helper, never by this function itself, so the marker is
    always visibly added at the call site, not hidden inside a generic
    context-builder)."""
    return dict(icx)


# ---------------------------------------------------------------------------
# Live-eligibility guard (Arch's ruling: "a resolver must never become a
# back door to an op that isn't live"). Mirrors the per-element check
# inversion_live.consult_inversion_live runs (resolve_live_match +
# _effect_guard_passes against get_action_workflows()), scoped to one op
# name, outside of a full consult.
# ---------------------------------------------------------------------------


def _op_is_live_eligible(op: str) -> bool:
    """Is ``op`` (a rail-registered action name) currently live-dispatchable
    under the SAME mechanism ``consult_inversion_live`` uses to decide live
    eligibility for the Inversion router? Reused, not reimplemented:
    ``inversion_live.resolve_live_match`` + ``inversion_live.
    _effect_guard_passes`` against ``workflow_dispatcher.
    get_action_workflows()``. A resolver may only re-enter an op for which
    this returns True."""
    from services.intent_service.inversion_live import (
        _effect_guard_passes,
        live_categories,
        registry_category_for,
        resolve_live_match,
    )
    from services.intent_service.workflow_dispatcher import get_action_workflows

    entry = get_action_workflows().get(op)
    if entry is None:
        return False
    category = registry_category_for(op)
    cats = live_categories()
    live_match = resolve_live_match(
        operation=op,
        canonical=op,
        flip_group=entry.flip_group,
        category=category,
        cats=cats,
    )
    if live_match is None:
        return False
    return _effect_guard_passes(entry, op, op)


# ---------------------------------------------------------------------------
# Copy composition — the CXO-ruled clear-family strings, reusing #1605's
# ratified functions/constants where the ruling says to, composing new
# clear-specific sentences only where CXO ruled NEW copy (the set-sentence
# wrapper, the unresolved tail, and the enumerated variant-3 confirm).
# ---------------------------------------------------------------------------


def _title_phrase_and_leaving(picked_texts: List[str], left_texts: List[str]):
    from services.intent_service.todo_handlers import _leaving_line, _title_phrase

    return _title_phrase(picked_texts), _leaving_line(left_texts)


def _clear_set_lead(picked_texts: List[str], left_texts: List[str]) -> str:
    """CXO ruling point 1: the set-naming lead sentence for the no-stored-
    default ask. One item: 'You want to clear the reminder "x".'; 2+:
    'You want to clear N reminders: …'. A Leaving clause only with a
    carve-out (CXO: "No set extracted: the ratified string alone" — i.e. no
    Leaving sentence without one)."""
    from services.intent_service.todo_handlers import _leaving_line, _title_phrase

    n = len(picked_texts)
    if n == 1:
        lead = f'You want to clear the reminder "{picked_texts[0]}".'
    else:
        lead = f"You want to clear {n} reminders: {_title_phrase(picked_texts)}."
    leaving = _leaving_line(left_texts)
    if leaving:
        lead += f" {leaving}"
    return lead


def _clear_variant_one_with_set(picked_texts: List[str], left_texts: List[str]) -> str:
    """CXO ruling point 1, in full: the set-naming lead, then the UNCHANGED
    ratified #1605 sentence (``reminder_clear.variant_one_question``,
    called directly — not hand-transcribed, per this module's docstring)."""
    from services.intent_service.reminder_clear import variant_one_question

    lead = _clear_set_lead(picked_texts, left_texts)
    return f"{lead} {variant_one_question(_CLEAR_VERB_LITERAL, _CLEAR_NOUN_LITERAL)}"


def _clear_variant_three_question(picked_texts: List[str], left_texts: List[str]) -> str:
    """CXO ruling point 3: 'You've set 'clear' to mean delete — delete N
    reminders: … Leaving … as is. (yes/no)'. Built from the SAME
    ``_confirm_question`` body ``delete_todo``'s own enumerating confirm
    uses (todo_handlers._delete_confirm_question), lower-cased, because
    this resolver — unlike the old #1605 module — supports carve-outs and
    needs the Leaving line; ``reminder_clear.variant_three_question`` has no
    such line and is the WRONG function to compose this from."""
    from services.intent_service.todo_handlers import _confirm_question

    body = _confirm_question(
        "delete",
        picked_texts,
        left_texts,
        one_item_template='delete the reminder "{title}"?',
    )
    return f"You've set 'clear' to mean delete — {body}"


def _clear_disclosure_clause() -> str:
    """CXO ruling point 2's disclosure clause, appended to a stored=done
    single-item auto-apply's reply: 'That's what 'clear' has meant for
    you. Say so if you meant delete this time.' Reuses CORRECTION_WINDOW_ASK
    (the ratified constant) for the tail; the lead clause is new glue copy
    at this seam (not a #1605 original — spelled out verbatim in the build
    task, not guessed)."""
    from services.intent_service.reminder_clear import CORRECTION_WINDOW_ASK

    return f"That's what '{_CLEAR_VERB_LITERAL}' has meant for you. {CORRECTION_WINDOW_ASK}"


# ---------------------------------------------------------------------------
# Candidate-pool + unresolved-reply rendering — mirrors (not shares, to
# avoid touching the ratified #1943/piece-1 handlers) the SAME resolution
# todo_handlers.handle_complete_todo_targets / handle_delete_todo_targets
# run, so the SET clear_todos decides branches on is the SET those ops will
# independently re-derive from the SAME args against the SAME pools.
# ---------------------------------------------------------------------------


async def _candidate_pools(todo_handlers, todo_user_id, session_id, principal):
    due = await todo_handlers._due_reminder_todos(todo_user_id)
    if due:
        name_pool, pool_kind = due, "due reminders"
    else:
        name_pool = await todo_handlers.todo_service.list_todos(
            user_id=todo_user_id, include_completed=False
        )
        pool_kind = "active to-dos"
    numbered = todo_handlers._recall_numbered_list(session_id, principal or todo_user_id)
    ordinal_pool: List[Any] = []
    ordinal_kind = pool_kind
    if numbered is not None:
        by_id = {t.id: t for t in name_pool}
        ordinal_pool = [by_id[i] for i in numbered.ids if i in by_id]
        ordinal_kind = numbered.kind
    return name_pool, pool_kind, ordinal_pool, ordinal_kind


def _render_unresolved_reply(
    name_pool,
    pool_kind: str,
    ordinal_pool,
    ordinal_kind: str,
    picked: List[Any],
    unresolved: List[str],
):
    """CXO ruling point 5: complete_todo's unresolved reply (CXO string 4),
    with the verb clause struck — 'Tell me which one.' in place of 'Tell me
    which one, and I'll mark it done.' Returns (message, listing_kind,
    shown_ids, shown_texts) so the caller can remember the numbered list."""
    from services.intent_service.todo_handlers import _is_positional

    listing_pool = (
        ordinal_pool if any(_is_positional(t) for t in unresolved) and ordinal_pool else name_pool
    )
    listing_kind = ordinal_kind if listing_pool is ordinal_pool and ordinal_pool else pool_kind
    first = unresolved[0]
    if _is_positional(first):
        n = re.sub(r"^#", "", first.strip())
        head = f"There's no number {n} in your {listing_kind}. You have {len(listing_pool)}:"
    else:
        name = first[5:].strip() if first.lower().startswith("name:") else first
        head = f'I couldn\'t find "{name}" in your {listing_kind}. You have:'
    lines = [head] + [f"{i + 1}. {t.text}" for i, t in enumerate(listing_pool[:10])]
    if len(listing_pool) > 10:
        lines.append(f"…and {len(listing_pool) - 10} more.")
    if picked:
        lines.append("Nothing has been changed. Say it again with the right name or number.")
    else:
        # CXO: strike the verb clause — nothing changes, nothing is armed,
        # and asking the verb question on a turn that holds no pending
        # state has nowhere for the answer to bind.
        lines.append("Tell me which one.")
    shown = listing_pool[:10]
    return (
        "\n".join(lines),
        listing_kind,
        [t.id for t in shown],
        [t.text for t in shown],
    )


# ---------------------------------------------------------------------------
# The resolver entry point. Called by workflow_entries.run_clear_todos_
# workflow (the registered entry_point); this function holds the logic,
# matching the todo_handlers delegation pattern run_delete_todo_workflow /
# run_complete_todo_workflow already use.
# ---------------------------------------------------------------------------


async def run_clear_todos(
    intent, session_id: Optional[str], user_id: Optional[str], intent_service
):
    from services.domain.models import Intent
    from services.intent.intent_service import (
        IntentProcessingResult,
        _coerce_todo_principal,
    )
    from services.intent_service.reminder_clear import (
        CLARIFY_CLEAR_VERB_WORKFLOW,
        CLEAR_FAMILY_RESOLVED_KEY,
        CLEAR_VERB_QUESTION_KIND,
        VALUE_COMPLETE,
        VALUE_DELETE,
        _verb_question_offer,
        inference_key,
    )
    from services.intent_service.todo_handlers import (
        TodoIntentHandlers,
        _router_target_tokens,
        resolve_router_targets,
    )
    from services.intent_service.verified_inference import get_verified_inference
    from services.intent_service.workflow_dispatcher import dispatch_workflow
    from services.shared_types import IntentCategory

    category = intent.category.value if intent.category else "execution"
    todo_user_id = _coerce_todo_principal(user_id)
    if not todo_user_id:
        return IntentProcessingResult(
            success=False,
            message="I need you to be logged in to clear todos. Please log in and try again.",
            intent_data={"category": category, "action": intent.action},
            error="User not authenticated",
            error_type="AuthenticationRequired",
        )

    principal = str(user_id) if user_id else str(todo_user_id)
    icx = dict(intent.context or {})
    args = icx.get("inversion_args") or {}
    targets = _router_target_tokens(args.get("targets")) if isinstance(args, dict) else []
    exclude = _router_target_tokens(args.get("exclude")) if isinstance(args, dict) else []
    original_message = intent.original_message or icx.get("original_message") or ""

    todo_handlers = intent_service.todo_handlers
    name_pool, pool_kind, ordinal_pool, ordinal_kind = await _candidate_pools(
        todo_handlers, todo_user_id, session_id, principal
    )
    if not name_pool:
        return IntentProcessingResult(
            success=True,
            message=f"You have no {pool_kind} to clear.",
            intent_data={"category": category, "action": intent.action},
        )

    picked, unresolved = resolve_router_targets(targets, name_pool, ordinal_candidates=ordinal_pool)
    excluded, unresolved_ex = (
        resolve_router_targets(exclude, name_pool, ordinal_candidates=ordinal_pool)
        if exclude
        else ([], [])
    )
    unresolved += unresolved_ex

    if unresolved:
        msg, listing_kind, shown_ids, shown_texts = _render_unresolved_reply(
            name_pool, pool_kind, ordinal_pool, ordinal_kind, picked, unresolved
        )
        TodoIntentHandlers._remember_numbered_list(
            session_id, principal or todo_user_id, listing_kind, shown_ids, shown_texts
        )
        return IntentProcessingResult(
            success=True,
            message=msg,
            intent_data={"category": category, "action": intent.action, "router_targets": True},
            requires_clarification=False,
        )

    ex_ids = {t.id for t in excluded}
    picked = [t for t in picked if t.id not in ex_ids]
    if not picked:
        return IntentProcessingResult(
            success=True,
            message="Nothing matched after the exceptions. Nothing has been changed.",
            intent_data={"category": category, "action": intent.action},
        )
    left = [t.text for t in name_pool if t.id not in {p.id for p in picked}]
    picked_texts = [t.text for t in picked]

    if session_id is None:
        # No session to bind an offer or re-entry to — mirrors the
        # no-stored-default branch's own established message below. Every
        # branch past this point re-enters the rail (dispatch_workflow
        # requires a concrete session_id) or arms a verb-question offer, so
        # this guard also narrows session_id: Optional[str] -> str for the
        # rest of the function (mypy gate, #1436).
        return IntentProcessingResult(
            success=True,
            message=(
                "I can ask you about several at once, but I need a session to do "
                "that. Try one at a time: 'complete todo 1' or 'delete todo 1'."
            ),
            intent_data={"category": category, "action": intent.action},
        )

    offer_service = getattr(intent_service, "workflow_offer_service", None)

    stored = await get_verified_inference(principal, inference_key(_CLEAR_VERB_LITERAL))
    stored_value = (stored or {}).get("value")

    # ── stored = done (WRITE): re-enter as complete_todo with the SAME args.
    if stored_value == VALUE_COMPLETE:
        if not _op_is_live_eligible("complete_todo"):
            return None  # legacy #1605 path handles the turn
        new_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="complete_todo",
            original_message=original_message,
            confidence=intent.confidence,
            context={
                **_rail_reentry_context(icx),
                VIA_CLEAR_VERB_CONTEXT_KEY: _CLEAR_VERB_LITERAL,
                CLEAR_FAMILY_RESOLVED_KEY: True,
            },
        )
        result = await dispatch_workflow(
            "complete_todo",
            session_id=session_id,
            user_id=user_id,
            context={"intent": new_intent, "intent_service": intent_service, "workflow_id": None},
        )
        if result is None:
            logger.error("clear_todos_complete_dispatch_failed", session_id=session_id)
            return IntentProcessingResult(
                success=False,
                message="I ran into trouble clearing those just now. Nothing has been changed.",
                intent_data={"category": category, "action": intent.action},
                error="complete_todo dispatch failed",
                error_type="DispatchError",
            )
        if result.requires_clarification:
            # CXO ruling point 2: the enumerating confirm arms UNCHANGED —
            # no extra clause. The disclosure lands on the "yes" summary,
            # via VIA_CLEAR_VERB_CONTEXT_KEY threaded through the bound
            # Intent (handle_complete_todo_targets's confirmed-reentry
            # branch reads it).
            return result
        return IntentProcessingResult(
            success=result.success,
            message=f"{result.message}\n\n{_clear_disclosure_clause()}",
            intent_data={**result.intent_data, "reminder_clear_disclosure": True},
        )

    # ── stored = delete (DESTRUCTIVE): re-enter as delete_todo with the
    #    SAME args; override the confirm copy with CXO's variant-3 text
    #    (the concrete op always arms, but with ITS default copy — this
    #    branch is the one case CXO ruled DIFFERENT copy for).
    if stored_value == VALUE_DELETE:
        if not _op_is_live_eligible("delete_todo"):
            return None  # legacy #1605 path handles the turn
        new_intent = Intent(
            category=IntentCategory.EXECUTION,
            action="delete_todo",
            original_message=original_message,
            confidence=intent.confidence,
            context={
                **_rail_reentry_context(icx),
                VIA_CLEAR_VERB_CONTEXT_KEY: _CLEAR_VERB_LITERAL,
                CLEAR_FAMILY_RESOLVED_KEY: True,
            },
        )
        result = await dispatch_workflow(
            "delete_todo",
            session_id=session_id,
            user_id=user_id,
            context={"intent": new_intent, "intent_service": intent_service, "workflow_id": None},
        )
        if result is None:
            logger.error("clear_todos_delete_dispatch_failed", session_id=session_id)
            return IntentProcessingResult(
                success=False,
                message="I ran into trouble clearing those just now. Nothing has been changed.",
                intent_data={"category": category, "action": intent.action},
                error="delete_todo dispatch failed",
                error_type="DispatchError",
            )
        question = _clear_variant_three_question(picked_texts, left)
        if result.requires_clarification and offer_service is not None and session_id:
            armed = offer_service.peek_pending_offer(session_id, user_id=principal)
            if armed is not None:
                armed = dict(armed)
                armed["question"] = question
                offer_service.set_pending_offer(session_id, armed, user_id=principal)
            return IntentProcessingResult(
                success=True,
                message=question,
                intent_data={**result.intent_data, "verb_default_applied": VALUE_DELETE},
                requires_clarification=True,
            )
        # Defensive: delete_todo always confirms (DESTRUCTIVE); an
        # unarmed result here is unexpected. Pass it through honestly
        # rather than claiming a confirm that did not arm.
        return result

    # ── no stored default: ask (CXO variant-1-with-set), binding the
    #    RESOLVED ids onto the EXISTING #1605 verb-question carrier.
    if not (_op_is_live_eligible("complete_todo") and _op_is_live_eligible("delete_todo")):
        return None  # legacy #1605 path handles the turn
    if offer_service is None or not session_id:
        return IntentProcessingResult(
            success=True,
            message=(
                "I can ask you about several at once, but I need a session to do "
                "that. Try one at a time: 'complete todo 1' or 'delete todo 1'."
            ),
            intent_data={"category": category, "action": intent.action},
        )
    question = _clear_variant_one_with_set(picked_texts, left)
    offer = _verb_question_offer(
        principal,
        _CLEAR_VERB_LITERAL,
        _CLEAR_NOUN_LITERAL,
        [t.id for t in picked],
        picked_texts,
        original_message,
        question=question,
    )
    offer["pending_action"][CLEAR_TODOS_RESOLVER_MARKER] = True
    offer_service.set_pending_offer(session_id, offer, user_id=principal)
    logger.info(
        "clear_todos_verb_question_offered",
        count=len(picked),
        session_id=session_id,
    )
    return IntentProcessingResult(
        success=True,
        message=question,
        intent_data={
            "category": category,
            "action": intent.action,
            "verb_disambiguation_pending": True,
        },
        requires_clarification=True,
    )


# ---------------------------------------------------------------------------
# Answer-turn handling for the verb question armed above (the
# CLEAR_TODOS_RESOLVER_MARKER branch reminder_clear._handle_verb_answer_turn
# delegates to). Reuses #1605's crisp-claim regexes and acceptance-tier
# machinery (same axes, same STATE_QUESTION passthrough contract) as the
# SHARED-FALLBACK path only; the primary discriminator is the generalized
# #1886(b) armed-turn consult (Arch's 2026-10-07 ruling, point 3) — see
# ``_refine_bound_set`` and the call site below.
# ---------------------------------------------------------------------------


def _refine_bound_set(
    ids: List[str], texts: List[str], args: Dict[str, Any]
) -> Tuple[List[str], List[str]]:
    """CXO ruling 4, as implemented via Arch's generalized #1886(b) armed-
    turn consult (point 3): when the verb-ANSWER turn itself names a
    refinement ("delete them, but not the PR one" → ``delete_todo`` with
    ``exclude: ["name:the pr"]``), narrow the bound (shown) set by the
    router's OWN ``targets``/``exclude`` for THAT turn — resolved by CODE
    against the ids/texts the offer actually bound at arm time, never by
    trusting the router's token list as a set on its own (D2).

    No targets AND no exclude token → the full bound set, unchanged
    ("them", bare, means everything shown). An unresolved target, or an
    exclusion that empties the set, is a malformed refinement — this falls
    back to the FULL bound set rather than silently narrowing to something
    never actually verified; the concrete op's own rail re-entry still
    renders whatever set this returns, in its own confirm/disclosure,
    before anything executes — this function only ever narrows what gets
    shown and acted on, never widens past what was already bound."""
    from services.domain.models import Todo
    from services.intent_service.todo_handlers import (
        _router_target_tokens,
        resolve_router_targets,
    )

    pool: List[Any] = []
    for tid, text in zip(ids, texts):
        row = Todo(text=text, priority="medium")
        row.id = tid
        pool.append(row)

    targets = _router_target_tokens(args.get("targets")) if isinstance(args, dict) else []
    exclude = _router_target_tokens(args.get("exclude")) if isinstance(args, dict) else []
    if not targets and not exclude:
        return ids, texts

    if targets:
        picked, unresolved = resolve_router_targets(targets, pool, ordinal_candidates=pool)
        if unresolved or not picked:
            return ids, texts
    else:
        picked = list(pool)

    if exclude:
        excluded, _unresolved_ex = resolve_router_targets(exclude, pool, ordinal_candidates=pool)
        ex_ids = {t.id for t in excluded}
        picked = [t for t in picked if t.id not in ex_ids]

    if not picked:
        return ids, texts
    return [t.id for t in picked], [t.text for t in picked]


async def handle_clear_todos_verb_answer(
    payload: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service,
    armed_question: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    from services.domain.models import Intent
    from services.intent_service import reminder_clear as _rc
    from services.intent_service.acceptance import (
        AcceptanceVerdict,
        declared_axes_for_workflow,
        evaluate_acceptance,
    )
    from services.intent_service.armed_turn_consult import (
        ArmedReplyOutcome,
        classify_armed_reply,
    )
    from services.intent_service.soft_invocation import is_prose_reply
    from services.intent_service.verified_inference import (
        SOURCE_USER_VERIFIED,
        store_verified_inference,
    )
    from services.intent_service.workflow_dispatcher import dispatch_workflow
    from services.shared_types import IntentCategory

    if _rc._principal_mismatch(payload, user_id):
        logger.warning(
            "clear_todos_verb_answer_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": "Let's hold off on that — nothing has been changed or stored.",
            "intent_data": {
                "category": "execution",
                "action": _rc.CLARIFY_CLEAR_VERB_WORKFLOW,
                "principal_mismatch": True,
            },
        }

    if session_id is None:
        # An armed offer is always session-bound, so this is not reachable
        # in practice — but the type is Optional[str] and dispatch_workflow
        # below requires str; narrow explicitly (mypy gate, #1436) rather
        # than assert, and decline honestly in the theoretical case.
        return {
            "message": "Let's hold off on that — nothing has been changed or stored.",
            "intent_data": {
                "category": "execution",
                "action": _rc.CLARIFY_CLEAR_VERB_WORKFLOW,
                "no_session": True,
            },
        }

    principal = str(user_id) if user_id else payload.get("user_id")
    ids = payload.get("clear_target_ids") or []
    texts = payload.get("clear_target_texts") or []
    original_message = payload.get("original_message") or ""
    key = _rc.inference_key(_CLEAR_VERB_LITERAL)

    _axes = declared_axes_for_workflow(_rc.CLARIFY_CLEAR_VERB_WORKFLOW)
    verdict = evaluate_acceptance(
        message,
        effect=_axes[0] if _axes else None,
        outwardness=_axes[1] if _axes else None,
        armed_question=armed_question,
    )
    if verdict is AcceptanceVerdict.STATE_QUESTION:
        logger.info("clear_todos_verb_state_question_falls_through", session_id=session_id)
        return None

    # Arch's 2026-10-07 ruling, point 3 (CXO ruling 4, generalized via the
    # #1886(b) armed-turn consult): the router decides whether this turn
    # ANSWERS the open verb question (naming complete_todo/delete_todo, with
    # its own args refining the shown set) or is an unrelated new ask (any
    # OTHER operation at/above threshold releases this turn entirely).
    consult = await classify_armed_reply(
        message,
        principal,
        session_id=session_id,
        intent_service=intent_service,
        answering_operations=_ANSWERING_OPERATIONS,
    )
    if consult.outcome is ArmedReplyOutcome.RELEASE:
        logger.info(
            "clear_todos_verb_answer_released",
            session_id=session_id,
            claimed_action=consult.operation,
            confidence=consult.confidence,
        )
        return None

    refined_ids, refined_texts = ids, texts
    if consult.outcome is ArmedReplyOutcome.BIND and consult.operation in _ANSWERING_OPERATIONS:
        # The router itself named the verb (and, implicitly, may have named
        # a refinement of the shown set) — this IS the answer.
        target_op = consult.operation
        value = _rc.VALUE_DELETE if target_op == "delete_todo" else _rc.VALUE_COMPLETE
        refined_ids, refined_texts = _refine_bound_set(ids, texts, consult.args)
    else:
        # Shared fallback (Arch's ruling): the router's bare "none" (not
        # informative for a yes/no verb question — unlike the #1886 name
        # carrier, this carrier's answering set deliberately excludes
        # "none"), CLARIFY, sub-threshold, a consult error, or no key all
        # fall back to the ORIGINAL #1605 crisp-claim regex parse on the
        # UNREFINED bound set — never a guess.
        text = (message or "").strip()
        prose = is_prose_reply(text)
        wants_delete = (
            not prose
            and bool(_rc._CORRECTION_CLAIM_RE.match(text))
            and not _rc._NEGATED_DELETE_RE.search(text)
        )
        wants_complete = not prose and bool(_rc._COMPLETE_ANSWER_RE.search(message))
        if wants_delete == wants_complete:
            # Neither claimed, or both (contradictory) — re-ask + re-arm,
            # keeping the marker so this module keeps claiming the answer turn.
            return _reask_clear_todos_verb_question(payload, intent_service, session_id, user_id)
        value = _rc.VALUE_DELETE if wants_delete else _rc.VALUE_COMPLETE
        target_op = "delete_todo" if wants_delete else "complete_todo"

    if not _op_is_live_eligible(target_op):
        return {
            "message": (
                "I can't do that yet — that capability isn't live right now. "
                "Nothing has been changed."
            ),
            "intent_data": {
                "category": "execution",
                "action": _rc.CLARIFY_CLEAR_VERB_WORKFLOW,
                "op_not_live": True,
            },
        }

    persisted = await store_verified_inference(
        principal, key, value, source=SOURCE_USER_VERIFIED, confidence=_rc.VERB_CONFIDENCE
    )

    # Name tokens reproduce the (possibly REFINED) bound set deterministically
    # against the concrete op's own (same-pool) resolution — never ids
    # directly; resolve_router_targets only understands the mini-grammar
    # (ordinal / range / last / all / name:<text>). The concrete op's own
    # rail re-entry re-renders this set in its confirm/disclosure before
    # anything executes (CXO ruling 4: never act on an answer turn without
    # the render).
    tokens = [f"name:{t}" for t in dict.fromkeys(refined_texts)]
    # original_message carries forward UNCHANGED (Arch's 2026-10-07 ruling,
    # point 2 — see _rail_reentry_context's docstring for why blanking was
    # the wrong mechanism). maybe_handle_clear_family stands down on the
    # CLEAR_FAMILY_RESOLVED_KEY marker below instead.
    new_intent = Intent(
        category=IntentCategory.EXECUTION,
        action=target_op,
        original_message=original_message,
        confidence=1.0,
        context={
            "inversion_args": {"targets": tokens},
            VIA_CLEAR_VERB_CONTEXT_KEY: _CLEAR_VERB_LITERAL,
            _rc.CLEAR_FAMILY_RESOLVED_KEY: True,
        },
    )
    result = await dispatch_workflow(
        target_op,
        session_id=session_id,
        user_id=user_id,
        context={"intent": new_intent, "intent_service": intent_service, "workflow_id": None},
    )
    if result is None:
        logger.error("clear_todos_verb_answer_dispatch_failed", target_op=target_op)
        return {
            "message": "I couldn't find those reminders just now. Nothing has been changed.",
            "intent_data": {
                "category": "execution",
                "action": _rc.CLARIFY_CLEAR_VERB_WORKFLOW,
                "dispatch_failed": True,
            },
        }

    logger.info(
        "clear_todos_verb_answered",
        value=value,
        persisted=persisted,
        session_id=session_id,
    )
    out: Dict[str, Any] = {
        "message": result.message,
        "intent_data": {
            **result.intent_data,
            "verb_default_stored": value,
            "verb_default_persisted": persisted,
        },
    }
    if result.requires_clarification:
        out["requires_clarification"] = True
    return out


def _reask_clear_todos_verb_question(
    payload: Dict[str, Any],
    intent_service,
    session_id: Optional[str],
    user_id: Optional[str],
) -> Dict[str, Any]:
    """Generic re-ask + re-arm for an unrecognized answer turn — mirrors
    reminder_clear's own re-arm idiom (store the question verbatim,
    #1665), keeping the CLEAR_TODOS_RESOLVER_MARKER so this module keeps
    claiming the answer turn on the next try."""
    from services.intent_service import reminder_clear as _rc

    question = "Just so I get it right — for these reminders: mark them done, or delete them?"
    payload = dict(payload)
    payload[CLEAR_TODOS_RESOLVER_MARKER] = True
    intent_service.workflow_offer_service.set_pending_offer(
        session_id,
        {
            "workflow_type": _rc.CLARIFY_CLEAR_VERB_WORKFLOW,
            "question": question,
            "pending_action": payload,
            "decline_message": (
                f"Okay — I haven't touched your {_rc._plural(_CLEAR_NOUN_LITERAL, 2)}. "
                f"Nothing has been changed."
            ),
        },
        user_id=user_id,
    )
    return {
        "message": question,
        "intent_data": {
            "category": "execution",
            "action": _rc.CLARIFY_CLEAR_VERB_WORKFLOW,
            "verb_disambiguation_pending": True,
        },
        "requires_clarification": True,
    }
