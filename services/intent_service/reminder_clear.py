"""#1605 — reminder/todo "clear"-family verb disambiguation (three-variant copy).

PM ruling (decisions.log 2026-08-13 ~14:1x, relayed by Lead): when a verb has
no confident mapping onto the baked-in operations, Piper ASKS — never a
term-of-art decree ("'clear' shall mean delete"). CXO+PPM joint design
(FINAL copy memo 2026-08-13 22:17, PPM sign-off 22:22): three variants —

1. **First encounter** (no stored default): ask which the user means, store
   the answer via the #1510 rail (store-on-verify, distinct provenance key).
2. **Stored default = complete (WRITE)**: auto-apply + disclosure-after; no
   block; correctable on the immediately-following turn ("I meant delete").
3. **Stored default = delete (DESTRUCTIVE)**: the stored preference changes
   the MAPPING, never the consent tier — the batch delete routes through the
   REAL #1190 confirm gate (DESTRUCTIVE -> CONFIRM in every consent-matrix
   cell, consent_gate.decide_consent; PPM verified the cells personally).

WHERE IT FIRES (routing moratorium honored — no pre-classifier or prompt
changes): detection is handler-internal, inside the EXECUTION surfaces that
already claim these turns — `_handle_execution_intent`'s complete_todo /
delete_todo branches (the classifier's guess for a clear-family utterance)
and its #1333 unmapped else-branch (the classifier emitted e.g.
"clear_reminders", which no surface maps — previously a false capability
denial, the exact #1605 transcript bug). The mechanism consumed is
`consent_gate.decide_verb_interpretation` (effect-weighted per #1557: a
WRITE candidate under a "stop asking me" meta-preference may auto-apply;
a DESTRUCTIVE candidate asks regardless — process steering never lowers a
destructive ask).

SCOPE (deliberate): set-complement asks ("clear these except X") are
#1563's dangling-offer lane, NOT this build — an exception clause falls
back to a variant-1-style clarification of the whole ask rather than
guessing the set (joint-design ruling; PM's original transcript phrasing
is the pinned case).

⚠️ COPY SEAM: the three variant strings below are RATIFIED verbatim (CXO
FINAL copy, PPM signed off) — a drifted word is a bug; tests pin them
exactly. The surrounding glue copy (empty-state, batch summaries, the
correction/meta re-asks) is Lead-drafted mechanism copy at this seam; CXO
owns the voice — adjust wording here (one place), not at call sites.

Vocabulary (#1569): the copy's noun tracks the user's own noun in the
triggering turn ("reminder" vs "todo" — the per-item rule's utterance-level
form); the ratified strings are the reminder-noun forms.

CORRECTION WINDOW (the "cheapest honest version", documented per the joint
design): after a variant-2 auto-apply, "I meant delete" works on the
IMMEDIATELY-FOLLOWING turn — it rides the #846 pending-offer store (one-turn
carrier, popped before classification), so the window is one turn, not the
whole session. The correction confirms via the #1190 gate before deleting
(the items are batch-completed by then; deleting removes them entirely) and
does NOT flip the stored default — the ratified copy says "this time".
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple
from uuid import UUID

import structlog

from services.shared_types import EffectClass

logger = structlog.get_logger(__name__)

# ── Carrier kinds (the #1190 pending_action carrier is action-agnostic;
#    ``kind`` is how the offer seam recognizes ours without a parallel store)
CLEAR_VERB_QUESTION_KIND = "reminder_clear_verb_question"
CLEAR_CORRECTION_KIND = "reminder_clear_correction"
CLEAR_DELETE_CONFIRMATION_KIND = "reminder_clear_delete_confirmation"

# ── Registered workflow types (all action_triggered=False — offer-seam only)
CLARIFY_CLEAR_VERB_WORKFLOW = "clarify_reminder_clear_verb"
CLEAR_CORRECTION_WORKFLOW = "reminder_clear_correction"
CLEAR_DELETE_WORKFLOW = "clear_reminders_delete"

# Effect-weighted gate input: a clear-family verb is a plausible-but-
# unverified mapping — between the suggestion floor (0.4) and the auto-apply
# bar (0.9). Same fixed value as the #1411 unmapped-status-value precedent.
VERB_CONFIDENCE = 0.7

VALUE_COMPLETE = "complete"
VALUE_DELETE = "delete"


def inference_key(verb: str) -> str:
    """Distinct provenance key in the #1510 verified-inference store, per
    verb — PM rejected decrees partly because every synonym would demand its
    own mapping forever; asked-once-remembered is per-verb by construction
    ("handle" gets its own first encounter; a stored "clear" never speaks
    for it). #1603: keys and values are str at the JSONB boundary."""
    return f"reminder_clear_verb:{verb}"


# ---------------------------------------------------------------------------
# RATIFIED COPY (CXO FINAL 2026-08-13 22:17; PPM sign-off 22:22) — verbatim
# for verb='clear', noun='reminder'; parametrized so sibling verbs and the
# noun form "todo" reuse the same shape (#1569 vocabulary rule).
# ---------------------------------------------------------------------------


def variant_one_question(verb: str = "clear", noun: str = "reminder") -> str:
    """Variant 1 — first encounter, no stored default."""
    return (
        f"Before I touch these — when you say '{verb}' on a {noun}, "
        f"do you want me to mark it done, or delete it? "
        f"I'll remember for next time."
    )


def variant_two_disclosure(verb: str = "clear") -> str:
    """Variant 2 — stored default = complete (WRITE): auto-apply,
    disclosure-after, no block."""
    return (
        f"Marking these done — that's what '{verb}' has meant for you. "
        f"Say so if you meant delete this time."
    )


def variant_two_always_ask_question() -> str:
    """RATIFIED COPY (CXO 2026-08-14 07:19, PPM confirmed 07:22) — V2's form
    under ALWAYS_ASK: a stored mapping is a prior EXPLICIT answer, not an
    assumption, so it is never flushed — but under "don't make assumptions"
    the assert-then-disclose form becomes a QUESTION that leads with the
    stored value as the suggested answer. Verbatim; a drifted word is a bug."""
    return "Want me to mark these done, like usual, or something different this time?"


def variant_three_question(count: int, verb: str = "clear", noun: str = "reminder") -> str:
    """Variant 3 — stored default = delete (DESTRUCTIVE): the question that
    rides the #1190 confirm gate. Ratified form is the N>1 shape; N==1 takes
    the grammatical singular (seam note: same sentence, singular referent)."""
    target = f"these {count} {noun}s" if count != 1 else f"this {noun}"
    return f"You've set '{verb}' to mean delete — delete {target}? (yes/no)"


# ---------------------------------------------------------------------------
# Detection (handler-internal — the routing moratorium's sanctioned seam)
# ---------------------------------------------------------------------------

# The clear family: the named verbs (clear / handle / take care of / reset).
# Unmapped classifier SIBLINGS ("clear_reminders", "reset_todos", ...) reach
# the else-branch call site and are detected by the SAME message scan.
_CLEAR_FAMILY_VERBS: Tuple[Tuple[str, str], ...] = (
    ("clear", r"\bclear\b"),
    ("handle", r"\bhandle\b"),
    ("take care of", r"\btake\s+care\s+of\b"),
    ("reset", r"\breset\b"),
)

# Domain nouns — the reminder/todo family only (the unified model's two
# vocabularies, #1569). No noun, no claim.
_REMINDER_NOUN_RE = re.compile(r"\breminders?\b", re.IGNORECASE)
_TODO_NOUN_RE = re.compile(r"\bto-?dos?\b", re.IGNORECASE)

# An explicit disambiguating verb in the same message means the ask is NOT
# ambiguous — the user already said which operation they mean.
_EXPLICIT_VERB_RE = re.compile(
    r"""
    \bdelete\b | \bremove\b | \berase\b
    | \bcomplete(?:d)?\b | \bfinish(?:ed)?\b
    | \bmark(?:ing)?\b [^.!?]{0,40} \b(?:done|complete)\b
    | \bdone\s+with\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Exception clauses — set-complement scope, #1563's lane, never guessed here.
_EXCEPTION_RE = re.compile(
    r"\bexcept\b|\bbut\s+not\b|\bother\s+than\b|\bapart\s+from\b"
    r"|\baside\s+from\b|\bexcluding\b",
    re.IGNORECASE,
)


@dataclass(frozen=True)
class ClearAsk:
    """A detected clear-family utterance over the reminder/todo domain."""

    verb: str  # family label ("clear", "handle", "take care of", "reset")
    noun: str  # "reminder" | "todo" — the user's own vocabulary (#1569)
    has_exception: bool  # exception clause present (fall back, never guess)


def detect_clear_family_ask(message: Optional[str]) -> Optional[ClearAsk]:
    """Detect an ambiguous clear-family ask over the reminder/todo domain.

    Fires only when (a) a clear-family verb is present, (b) a reminder/todo
    noun is present, and (c) NO explicit complete/delete verb disambiguates
    the ask already. Explicit messages ("delete todo 3", "mark the PR review
    done") pass through untouched — the gate confiscates ambiguity, never
    imperatives (#1510's principle)."""
    text = (message or "").strip()
    if not text:
        return None
    if _EXPLICIT_VERB_RE.search(text):
        return None
    has_reminder = bool(_REMINDER_NOUN_RE.search(text))
    has_todo = bool(_TODO_NOUN_RE.search(text))
    if not (has_reminder or has_todo):
        return None
    for label, pattern in _CLEAR_FAMILY_VERBS:
        if re.search(pattern, text, re.IGNORECASE):
            return ClearAsk(
                verb=label,
                # The user's own noun wins; "reminder" wins a mixed mention
                # (the more specific origin — same tiebreak as the render
                # rule's item-in-both-blocks case, #1569).
                noun="reminder" if has_reminder else "todo",
                has_exception=bool(_EXCEPTION_RE.search(text)),
            )
    return None


# ---------------------------------------------------------------------------
# Target resolution + batch operations
# ---------------------------------------------------------------------------


_DIFFERENT_ANSWER_RE = re.compile(r"\b(different|something else|not (this|that)|delete)\b", re.I)
_USUAL_ANSWER_RE = re.compile(r"\b(yes|yeah|yep|sure|ok(ay)?|usual|as usual|like usual|done|please do)\b", re.I)


def _plural(noun: str, n: int) -> str:
    return noun if n == 1 else f"{noun}s"


async def _resolve_targets(todo_service, user_uuid: UUID, noun: str) -> List[Any]:
    """The whole ask's target set (scope narrowing is #1563's lane):
    noun 'reminder' -> active todos carrying a reminder_date (the
    `context:reminders` family's own membership rule); noun 'todo' -> all
    active todos. Owner-scoped via user_id (#1493/#1532)."""
    todos = await todo_service.list_todos(user_id=user_uuid, include_completed=False)
    if noun == "reminder":
        return [
            t
            for t in todos
            if getattr(t, "reminder_date", None) is not None and not t.completed
        ]
    return [t for t in todos if not t.completed]


async def _complete_ids(
    todo_service, ids: List[str], texts: List[str], user_uuid: UUID
) -> Tuple[List[str], int]:
    """Batch-complete by id. Returns (completed texts, failure count) —
    failures are counted honestly, never silently dropped."""
    done: List[str] = []
    failed = 0
    for tid, text in zip(ids, texts):
        try:
            result = await todo_service.complete_todo(todo_id=UUID(tid), user_id=user_uuid)
            if result:
                done.append(text)
            else:
                failed += 1
        except Exception as e:  # silent-ok: counted + logged; the summary copy states the honest denominator (m-44), never a fabricated all-done
            failed += 1
            logger.warning("reminder_clear_complete_failed", todo_id=tid, error=str(e))
    return done, failed


def _completion_summary(done: List[str], failed: int, noun: str) -> str:
    lines = [f"Marked {len(done)} {_plural(noun, len(done))} done:"]
    lines.extend(f"• {text}" for text in done)
    if failed:
        lines.append(
            f"({failed} couldn't be updated just now — say 'show my todos' to check.)"
        )
    return "\n".join(lines)


def _empty_targets_message(verb: str, noun: str) -> str:
    # Pattern-073 discipline: describe what was actually queried.
    scope = "saved reminders" if noun == "reminder" else "active todos"
    return (
        f"I checked your {scope} and there are none to {verb} right now. "
        f"Nothing has been changed."
    )


# ---------------------------------------------------------------------------
# Offer builders (all ride the EXISTING #846 store / #1190 carrier shape)
# ---------------------------------------------------------------------------


def _delete_confirmation_offer(
    principal: Optional[str],
    verb: str,
    noun: str,
    ids: List[str],
    texts: List[str],
    original_message: str,
    kind: str = CLEAR_DELETE_CONFIRMATION_KIND,
) -> Dict[str, Any]:
    """A #1190 pending_action offer whose "yes" dispatches the batch delete
    through CONFIRM_PENDING_ACTION_WORKFLOW -> CLEAR_DELETE_WORKFLOW. The
    target ids are resolved at OFFER time so the question's N is exactly
    what a "yes" deletes — no drift between the ask and the act."""
    from services.domain.models import Intent
    from services.intent_service.destructive_confirm import (
        CONFIRM_PENDING_ACTION_WORKFLOW,
    )
    from services.shared_types import IntentCategory

    n = len(ids)
    delete_intent = Intent(
        category=IntentCategory.EXECUTION,
        action=CLEAR_DELETE_WORKFLOW,
        original_message=original_message,
        confidence=1.0,
        context={
            "original_message": original_message,
            "user_id": principal,
            "clear_target_ids": list(ids),
            "clear_target_texts": list(texts),
            "clear_noun": noun,
            "clear_verb": verb,
        },
    )
    summary = f"delete {n} {_plural(noun, n)}"
    return {
        "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
        "pending_action": {
            "kind": kind,
            "action": CLEAR_DELETE_WORKFLOW,
            "intent": delete_intent,
            "summary": summary,
            "user_id": principal,
        },
        "decline_message": (
            f"Okay — I won't delete anything. Your {_plural(noun, 2)} are untouched."
        ),
    }


def _verb_question_offer(
    principal: Optional[str],
    verb: str,
    noun: str,
    ids: List[str],
    texts: List[str],
    original_message: str,
) -> Dict[str, Any]:
    """The variant-1 pending offer. Its answer is either/or ("mark it done" /
    "delete it"), handled kind-specifically at the offer seam BEFORE generic
    accept/decline (the verify_inference precedent). A bare affirmative falls
    to the generic accept path, which dispatches CLARIFY_CLEAR_VERB_WORKFLOW —
    an entry that re-asks and re-arms this same offer."""
    return {
        "workflow_type": CLARIFY_CLEAR_VERB_WORKFLOW,
        "pending_action": {
            "kind": CLEAR_VERB_QUESTION_KIND,
            "action": CLARIFY_CLEAR_VERB_WORKFLOW,
            "user_id": principal,
            "inference_key": inference_key(verb),
            "clear_verb": verb,
            "clear_noun": noun,
            "clear_target_ids": list(ids),
            "clear_target_texts": list(texts),
            "original_message": original_message,
            "summary": f"{verb} {len(ids)} {_plural(noun, len(ids))}",
        },
        "decline_message": (
            f"Okay — I haven't touched your {_plural(noun, 2)}. "
            f"Nothing has been changed."
        ),
    }


def _correction_offer(
    principal: Optional[str],
    verb: str,
    noun: str,
    completed_ids: List[str],
    completed_texts: List[str],
    original_message: str,
) -> Dict[str, Any]:
    """The one-turn correction window after a variant-2 auto-apply ("Say so
    if you meant delete this time"). A correction phrase next turn routes to
    a #1190-gated delete of the just-completed items; anything else abandons
    it via the pop (the #1529 off-intent tier)."""
    return {
        "workflow_type": CLEAR_CORRECTION_WORKFLOW,
        "pending_action": {
            "kind": CLEAR_CORRECTION_KIND,
            "action": CLEAR_CORRECTION_WORKFLOW,
            "user_id": principal,
            "clear_verb": verb,
            "clear_noun": noun,
            "clear_target_ids": list(completed_ids),
            "clear_target_texts": list(completed_texts),
            "original_message": original_message,
            "summary": f"correct '{verb}' to delete",
        },
        "decline_message": "Good — they stay marked done.",
    }


# ---------------------------------------------------------------------------
# The main flow — called from _handle_execution_intent's claiming branches
# ---------------------------------------------------------------------------


async def maybe_handle_clear_family(
    intent_service,
    intent,
    session_id: Optional[str],
    user_id: Optional[str],
    todo_user_id: UUID,
    candidate_effect: EffectClass,
):
    """Run the #1605 three-variant flow for a clear-family utterance, or
    return None -> the caller proceeds with its normal handling (explicit
    verbs, non-domain messages).

    ``candidate_effect`` is the CLASSIFIER'S candidate mapping's declared
    effect (WRITE at the complete_todo call site, DESTRUCTIVE at the
    delete_todo and unmapped call sites) — the quantity
    ``decide_verb_interpretation`` weights (#1557): a WRITE candidate under
    TRUST_INFERENCES may auto-apply; a DESTRUCTIVE candidate reads back even
    then (process steering never lowers a destructive ask).
    """
    from services.intent.intent_service import IntentProcessingResult
    from services.intent_service.consent_gate import decide_verb_interpretation
    from services.intent_service.verified_inference import (
        SOURCE_META_AUTO,
        VerificationDecision,
        get_meta_mode,
        get_verified_inference,
        store_verified_inference,
    )

    original_message = intent.original_message or (intent.context or {}).get(
        "original_message", ""
    )
    ask = detect_clear_family_ask(original_message)
    if ask is None:
        return None
    if not session_id:
        # No session to bind an answer to — never guess a destructive-capable
        # mapping without one. Fall through to the caller's normal handling.
        return None

    principal = str(user_id) if user_id else str(todo_user_id)
    base_intent_data = {
        "category": intent.category.value if intent.category else "execution",
        "action": intent.action,
        "confidence": intent.confidence,
        "clear_verb": ask.verb,
        "clear_noun": ask.noun,
    }

    # ── Exception clause: #1563's set-complement lane — clarify the whole
    #    ask (variant-1-style), never guess the set. No write; PM live-found
    #    (2026-08-15) that the original no-offer version asked the verb
    #    question and then had nowhere to land the bare answer it INVITED
    #    ("delete" fell to the floor's canned denial). The offer is armed
    #    with NO TARGETS: the answer stores the verb (the question promises
    #    "I'll remember"), and the reply re-asks for the explicit list —
    #    still never acting on a guessed set.
    if ask.has_exception:
        logger.info(
            "reminder_clear_exception_clause_fallback",
            verb=ask.verb,
            noun=ask.noun,
            session_id=session_id,
        )
        offer = _verb_question_offer(
            principal, ask.verb, ask.noun, [], [], original_message
        )
        offer["pending_action"]["exception_no_targets"] = True
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, offer, user_id=user_id
        )
        message = (
            f"{variant_one_question(ask.verb, ask.noun)}\n\n"
            f"Also — you carved out an exception, and I don't want to guess "
            f"which {_plural(ask.noun, 2)} you mean. Once you answer, tell me "
            f"exactly which ones to include and I'll act on just those."
        )
        return IntentProcessingResult(
            success=True,
            message=message,
            intent_data={
                **base_intent_data,
                "verb_disambiguation_pending": True,
                "exception_clause_fallback": True,
            },
            requires_clarification=True,
        )

    todo_service = intent_service.todo_handlers.todo_service
    try:
        targets = await _resolve_targets(todo_service, todo_user_id, ask.noun)
    except Exception as e:  # silent-ok: logged at error w/ exc_info; a source failure must read as trouble-loading (#1425), never fall through to a guessed mapping
        logger.error(
            "reminder_clear_target_resolution_failed",
            error=str(e),
            user_id=principal,
            exc_info=True,
        )
        scope = "reminders" if ask.noun == "reminder" else "todos"
        return IntentProcessingResult(
            success=True,
            message=(
                f"I had trouble loading your {scope} just now, so I haven't "
                f"touched anything. You can try again in a moment."
            ),
            intent_data=base_intent_data,
        )

    if not targets:
        return IntentProcessingResult(
            success=True,
            message=_empty_targets_message(ask.verb, ask.noun),
            intent_data=base_intent_data,
        )

    ids = [str(t.id) for t in targets]
    texts = [t.text for t in targets]

    stored = await get_verified_inference(principal, inference_key(ask.verb))
    stored_value = (stored or {}).get("value")

    # ── Variant 2: stored default = complete (WRITE) — auto-apply +
    #    disclosure-after; no block; one-turn correction window armed.
    #    EXCEPT under ALWAYS_ASK (CXO/PPM ruling 2026-08-14): the stored
    #    mapping is NOT flushed (a prior explicit answer is not an
    #    assumption), but the form flips from assert-then-disclose to a
    #    question that LEADS with the stored value. V3 needs no such flip —
    #    it already blocks in every mode.
    if stored_value == VALUE_COMPLETE:
        from services.intent_service.verified_inference import (
            VerificationMetaMode as _VMM,
        )

        if await get_meta_mode(principal) is _VMM.ALWAYS_ASK:
            offer = _verb_question_offer(
                principal, ask.verb, ask.noun, ids, texts, original_message
            )
            offer["pending_action"]["stored_default_leading"] = VALUE_COMPLETE
            intent_service.workflow_offer_service.set_pending_offer(
                session_id, offer, user_id=user_id
            )
            logger.info(
                "reminder_clear_always_ask_question",
                verb=ask.verb,
                targets=len(ids),
                session_id=session_id,
            )
            return IntentProcessingResult(
                success=True,
                message=variant_two_always_ask_question(),
                intent_data={
                    **base_intent_data,
                    "verb_default_leading": VALUE_COMPLETE,
                    "verb_disambiguation_pending": True,
                },
                requires_clarification=True,
            )
        done, failed = await _complete_ids(todo_service, ids, texts, todo_user_id)
        intent_service.workflow_offer_service.set_pending_offer(
            session_id,
            _correction_offer(principal, ask.verb, ask.noun, ids, texts, original_message),
            user_id=user_id,
        )
        logger.info(
            "reminder_clear_default_applied",
            value=VALUE_COMPLETE,
            verb=ask.verb,
            completed=len(done),
            failed=failed,
            session_id=session_id,
        )
        return IntentProcessingResult(
            success=True,
            message=(
                f"{variant_two_disclosure(ask.verb)}\n\n"
                f"{_completion_summary(done, failed, ask.noun)}"
            ),
            intent_data={
                **base_intent_data,
                "verb_default_applied": VALUE_COMPLETE,
                "reminder_clear_correction_pending": True,
            },
        )

    # ── Variant 3: stored default = delete (DESTRUCTIVE) — the stored
    #    preference changes the mapping, never the consent tier: the batch
    #    routes through the REAL #1190 confirm gate. Blocks in every meta
    #    mode (consent matrix: DESTRUCTIVE -> CONFIRM in every cell).
    if stored_value == VALUE_DELETE:
        intent_service.workflow_offer_service.set_pending_offer(
            session_id,
            _delete_confirmation_offer(
                principal, ask.verb, ask.noun, ids, texts, original_message
            ),
            user_id=user_id,
        )
        logger.info(
            "reminder_clear_delete_confirmation_offered",
            verb=ask.verb,
            count=len(ids),
            session_id=session_id,
        )
        return IntentProcessingResult(
            success=True,
            message=variant_three_question(len(ids), ask.verb, ask.noun),
            intent_data={
                **base_intent_data,
                "action": CLEAR_DELETE_WORKFLOW,
                "verb_default_applied": VALUE_DELETE,
                "destructive_confirmation_pending": True,
            },
            requires_clarification=True,
        )

    # ── No stored default: effect-weighted gate (one scoring system).
    meta_mode = await get_meta_mode(principal)
    decision = decide_verb_interpretation(VERB_CONFIDENCE, candidate_effect, meta_mode)

    if decision is VerificationDecision.AUTO_APPLY:
        # Only reachable with a WRITE candidate under TRUST_INFERENCES
        # ("stop asking me every time") — the rail's meta semantics: apply
        # the candidate without a read-back, store with meta_auto provenance
        # so the next 'clear' is a variant-2 turn. A DESTRUCTIVE candidate
        # never lands here (decide_verb_interpretation pins READ_BACK).
        done, failed = await _complete_ids(todo_service, ids, texts, todo_user_id)
        persisted = await store_verified_inference(
            principal,
            inference_key(ask.verb),
            VALUE_COMPLETE,
            source=SOURCE_META_AUTO,
            confidence=VERB_CONFIDENCE,
        )
        intent_service.workflow_offer_service.set_pending_offer(
            session_id,
            _correction_offer(principal, ask.verb, ask.noun, ids, texts, original_message),
            user_id=user_id,
        )
        logger.info(
            "reminder_clear_meta_auto_applied",
            verb=ask.verb,
            completed=len(done),
            failed=failed,
            persisted=persisted,
            session_id=session_id,
        )
        # Glue copy (seam): variant 2's middle clause claims a history this
        # first meta-endorsed apply doesn't have — dropped honestly.
        return IntentProcessingResult(
            success=True,
            message=(
                f"Marking these done. Say so if you meant delete this time.\n\n"
                f"{_completion_summary(done, failed, ask.noun)}"
            ),
            intent_data={
                **base_intent_data,
                "verb_default_applied": VALUE_COMPLETE,
                "verb_default_source": SOURCE_META_AUTO,
                "reminder_clear_correction_pending": True,
            },
        )

    if decision is not VerificationDecision.READ_BACK:
        # DISCARD is unreachable at VERB_CONFIDENCE (0.7 > suggestion floor);
        # defensive fall-through to the caller's normal handling.
        return None

    # ── Variant 1: first encounter — ask, bind the answer via the offer seam.
    intent_service.workflow_offer_service.set_pending_offer(
        session_id,
        _verb_question_offer(principal, ask.verb, ask.noun, ids, texts, original_message),
        user_id=user_id,
    )
    logger.info(
        "reminder_clear_verb_question_offered",
        verb=ask.verb,
        noun=ask.noun,
        count=len(ids),
        session_id=session_id,
    )
    return IntentProcessingResult(
        success=True,
        message=variant_one_question(ask.verb, ask.noun),
        intent_data={**base_intent_data, "verb_disambiguation_pending": True},
        requires_clarification=True,
    )


# ---------------------------------------------------------------------------
# Offer-seam turn handling (kind-specific, BEFORE generic accept/decline —
# the verified_inference.handle_verification_turn_meta precedent)
# ---------------------------------------------------------------------------

_DELETE_ANSWER_RE = re.compile(r"\bdelete\b|\bremove\b|\bget\s+rid\b", re.IGNORECASE)
_COMPLETE_ANSWER_RE = re.compile(
    r"\bdone\b|\bcomplete(?:d)?\b|\bfinish(?:ed)?\b|\bcheck(?:ed)?\s+(?:them|these|it)?\s*off\b",
    re.IGNORECASE,
)
_NEGATED_DELETE_RE = re.compile(
    r"\b(?:don'?t|do\s+not|never)\b[^.!?]{0,20}\bdelete\b", re.IGNORECASE
)


def _principal_mismatch(payload: Dict[str, Any], user_id: Optional[str]) -> bool:
    """#1532: the store and the todos are the USER's. If the turn's principal
    differs from the one the offer was built for (auth changed between
    turns), nothing may act or store."""
    offer_user = payload.get("user_id")
    principal = str(user_id) if user_id else None
    return bool(offer_user and principal and offer_user != principal)


async def handle_reminder_clear_turn(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service,
) -> Optional[Dict[str, Any]]:
    """Kind-specific handling for a popped reminder-clear offer. Returns the
    acceptance-seam dict shape ({"message", "intent_data"[, "requires_clarification"]})
    when this turn was claimed; None falls through to generic accept /
    decline / off-intent handling (bare "yes" -> the registered workflow's
    re-ask; "no"/bare exit -> the offer's honest decline copy; anything
    else -> abandoned via the pop)."""
    payload = pending_offer.get("pending_action") or {}
    kind = payload.get("kind")
    if kind == CLEAR_VERB_QUESTION_KIND:
        return await _handle_verb_answer_turn(
            payload, message, session_id, user_id, intent_service
        )
    if kind == CLEAR_CORRECTION_KIND:
        return await _handle_correction_turn(
            payload, message, session_id, user_id, intent_service
        )
    return None


async def _handle_verb_answer_turn(
    payload: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service,
) -> Optional[Dict[str, Any]]:
    from services.intent_service.verified_inference import (
        SOURCE_USER_VERIFIED,
        detect_meta_feedback,
        set_meta_mode,
        store_verified_inference,
    )
    from services.intent_service.verified_inference import (
        VerificationMetaMode,
    )

    verb = payload.get("clear_verb") or "clear"
    noun = payload.get("clear_noun") or "reminder"
    ids = payload.get("clear_target_ids") or []
    texts = payload.get("clear_target_texts") or []
    key = payload.get("inference_key") or inference_key(verb)
    original_message = payload.get("original_message") or ""

    if _principal_mismatch(payload, user_id):
        logger.warning(
            "reminder_clear_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": "Let's hold off on that — nothing has been changed or stored.",
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_CLEAR_VERB_WORKFLOW,
                "principal_mismatch": True,
            },
        }
    principal = str(user_id) if user_id else payload.get("user_id")

    # Meta-feedback is the DISTINCT channel (PM's #1510 ruling) — it steers
    # the process, but delete stays on the table for THIS ask, so the verb
    # question re-arms rather than resolving silently (the same principle
    # that keeps variant 3 blocking under TRUST_INFERENCES).
    meta = detect_meta_feedback(message)
    if meta is not None:
        meta_persisted = await set_meta_mode(principal, meta)
        _rearm_verb_question(intent_service, session_id, user_id, payload)
        if meta is VerificationMetaMode.TRUST_INFERENCES:
            lead = "Understood — I'll stop checking my inferences with you."
        else:
            lead = (
                "Understood — I won't act on my own inferences without "
                "checking with you first."
            )
        msg = (
            f"{lead} For this one I still need the call, since delete isn't "
            f"something I'll guess at: mark these done, or delete them?"
        )
        if not meta_persisted:
            msg += (
                "\n\n(Heads up: I couldn't save that preference just now, "
                "so it may not stick across sessions.)"
            )
        return {
            "message": msg,
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_CLEAR_VERB_WORKFLOW,
                "meta_mode": meta.value,
                "verb_disambiguation_pending": True,
            },
            "requires_clarification": True,
        }

    wants_delete = bool(_DELETE_ANSWER_RE.search(message)) and not _NEGATED_DELETE_RE.search(
        message
    )
    wants_complete = bool(_COMPLETE_ANSWER_RE.search(message))
    if wants_delete and wants_complete:
        return None  # contradictory — fall to generic handling (likely off-intent)

    # ── Exception-clause answers (PM live 2026-08-15): the verb STORES (the
    #    question promised "I'll remember"), but there are NO bound targets —
    #    the exception made the set unresolved, so nothing executes and no
    #    V3 confirm arms. The reply confirms the stored verb and re-asks for
    #    the explicit list. Never guess the set.
    if payload.get("exception_no_targets"):
        value = None
        if wants_delete:
            value = VALUE_DELETE
        elif wants_complete:
            value = VALUE_COMPLETE
        if value is None:
            return None  # not a verb answer — generic handling
        persisted = await store_verified_inference(
            principal, key, value, source=SOURCE_USER_VERIFIED, confidence=VERB_CONFIDENCE
        )
        logger.info(
            "reminder_clear_exception_verb_stored",
            value=value,
            persisted=persisted,
            session_id=session_id,
        )
        verb_meaning = "delete" if value == VALUE_DELETE else "mark done"
        msg = (
            f"Got it — '{verb}' means {verb_meaning}, and I'll remember that. "
            f"Now tell me exactly which {_plural(noun, 2)} to include "
            f"(your exception noted), and I'll act on just those."
        )
        if not persisted:
            msg += (
                "\n\n(Heads up: I couldn't save that preference just now, "
                "so I may ask again in a future session.)"
            )
        return {
            "message": msg,
            "intent_data": {
                "category": "execution",
                "action": CLARIFY_CLEAR_VERB_WORKFLOW,
                "verb_default_stored": value,
                "exception_list_pending": True,
            },
            "requires_clarification": True,
        }

    # ── ALWAYS_ASK leading-question answers (CXO/PPM 2026-08-14): the stored
    #    default is a prior explicit answer — NEVER flipped here. "like
    #    usual"/bare yes → complete without re-store ceremony; "different"/
    #    delete → the V3 confirm for THIS batch only, stored default intact.
    if payload.get("stored_default_leading") == VALUE_COMPLETE:
        if wants_delete or _DIFFERENT_ANSWER_RE.search(message):
            intent_service.workflow_offer_service.set_pending_offer(
                session_id,
                _delete_confirmation_offer(
                    principal, verb, noun, ids, texts, original_message
                ),
                user_id=user_id,
            )
            logger.info(
                "reminder_clear_always_ask_this_time_delete",
                session_id=session_id,
            )
            return {
                # ⚠️ COPY SEAM (glue): the parenthetical is Lead-drafted.
                "message": (
                    f"{variant_three_question(len(ids), verb, noun)}\n"
                    f"(Your usual '{verb}' stays mark-done — this is just "
                    f"for this batch.)"
                ),
                "intent_data": {
                    "category": "execution",
                    "action": CLEAR_DELETE_WORKFLOW,
                    "this_time_only": True,
                    "destructive_confirmation_pending": True,
                },
                "requires_clarification": True,
            }
        if wants_complete or _USUAL_ANSWER_RE.search(message):
            todo_service = intent_service.todo_handlers.todo_service
            try:
                user_uuid = UUID(str(principal))
            except (ValueError, TypeError):
                return {
                    "message": (
                        "I need you to be logged in to update todos. "
                        "Nothing has been changed."
                    ),
                    "intent_data": {
                        "category": "execution",
                        "action": CLARIFY_CLEAR_VERB_WORKFLOW,
                        "error_type": "AuthenticationRequired",
                    },
                }
            done, failed = await _complete_ids(todo_service, ids, texts, user_uuid)
            logger.info(
                "reminder_clear_always_ask_usual_applied",
                completed=len(done),
                failed=failed,
                session_id=session_id,
            )
            return {
                "message": _completion_summary(done, failed, noun),
                "intent_data": {
                    "category": "execution",
                    "action": "complete_todo",
                    "verb_default_applied": VALUE_COMPLETE,
                },
            }
        return None  # not an answer — generic handling

    if wants_delete:
        persisted = await store_verified_inference(
            principal, key, VALUE_DELETE, source=SOURCE_USER_VERIFIED, confidence=VERB_CONFIDENCE
        )
        intent_service.workflow_offer_service.set_pending_offer(
            session_id,
            _delete_confirmation_offer(principal, verb, noun, ids, texts, original_message),
            user_id=user_id,
        )
        logger.info(
            "reminder_clear_verb_answered",
            value=VALUE_DELETE,
            persisted=persisted,
            session_id=session_id,
        )
        msg = variant_three_question(len(ids), verb, noun)
        if not persisted:
            msg += (
                "\n\n(Heads up: I couldn't save that preference just now, "
                "so I may ask again in a future session.)"
            )
        return {
            "message": msg,
            "intent_data": {
                "category": "execution",
                "action": CLEAR_DELETE_WORKFLOW,
                "verb_default_stored": VALUE_DELETE,
                "verb_default_persisted": persisted,
                "destructive_confirmation_pending": True,
            },
            "requires_clarification": True,
        }

    if wants_complete:
        persisted = await store_verified_inference(
            principal, key, VALUE_COMPLETE, source=SOURCE_USER_VERIFIED, confidence=VERB_CONFIDENCE
        )
        todo_service = intent_service.todo_handlers.todo_service
        try:
            user_uuid = UUID(str(principal))
        except (ValueError, TypeError):
            return {
                "message": (
                    "I need you to be logged in to update todos. "
                    "Nothing has been changed."
                ),
                "intent_data": {
                    "category": "execution",
                    "action": CLARIFY_CLEAR_VERB_WORKFLOW,
                    "error_type": "AuthenticationRequired",
                },
            }
        done, failed = await _complete_ids(todo_service, ids, texts, user_uuid)
        logger.info(
            "reminder_clear_verb_answered",
            value=VALUE_COMPLETE,
            persisted=persisted,
            completed=len(done),
            failed=failed,
            session_id=session_id,
        )
        msg = (
            f"Got it — '{verb}' means mark done, and I'll remember that.\n\n"
            f"{_completion_summary(done, failed, noun)}"
        )
        if not persisted:
            msg += (
                "\n\n(Heads up: I couldn't save that preference just now, "
                "so I may ask again in a future session.)"
            )
        return {
            "message": msg,
            "intent_data": {
                "category": "execution",
                "action": "complete_todo",
                "verb_default_stored": VALUE_COMPLETE,
                "verb_default_persisted": persisted,
            },
        }

    return None  # not an answer — generic accept/decline/off-intent handling


async def _handle_correction_turn(
    payload: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service,
) -> Optional[Dict[str, Any]]:
    """"I meant delete" on the turn after a variant-2 auto-apply: route the
    just-completed batch to a #1190-gated delete. Does NOT flip the stored
    default (ratified copy: "this time"). Anything else falls through."""
    if not _DELETE_ANSWER_RE.search(message) or _NEGATED_DELETE_RE.search(message):
        return None
    if _principal_mismatch(payload, user_id):
        logger.warning(
            "reminder_clear_correction_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": "Let's hold off on that — nothing has been changed.",
            "intent_data": {
                "category": "execution",
                "action": CLEAR_CORRECTION_WORKFLOW,
                "principal_mismatch": True,
            },
        }

    principal = str(user_id) if user_id else payload.get("user_id")
    verb = payload.get("clear_verb") or "clear"
    noun = payload.get("clear_noun") or "reminder"
    ids = payload.get("clear_target_ids") or []
    texts = payload.get("clear_target_texts") or []
    n = len(ids)
    intent_service.workflow_offer_service.set_pending_offer(
        session_id,
        _delete_confirmation_offer(
            principal,
            verb,
            noun,
            ids,
            texts,
            payload.get("original_message") or "",
        ),
        user_id=user_id,
    )
    logger.info(
        "reminder_clear_correction_claimed", count=n, session_id=session_id
    )
    target = f"these {n} {_plural(noun, n)}" if n != 1 else f"this {noun}"
    return {
        "message": f"Got it — delete {target} instead? (yes/no)",
        "intent_data": {
            "category": "execution",
            "action": CLEAR_DELETE_WORKFLOW,
            "destructive_confirmation_pending": True,
            "correction_of": VALUE_COMPLETE,
        },
        "requires_clarification": True,
    }


def _rearm_verb_question(intent_service, session_id, user_id, payload) -> None:
    """Re-arm the variant-1 offer with its original payload (the pop already
    consumed it; a re-ask turn must re-store it or the next answer has
    nothing to bind to)."""
    intent_service.workflow_offer_service.set_pending_offer(
        session_id,
        {
            "workflow_type": CLARIFY_CLEAR_VERB_WORKFLOW,
            "pending_action": dict(payload),
            "decline_message": (
                f"Okay — I haven't touched your "
                f"{_plural(payload.get('clear_noun') or 'reminder', 2)}. "
                f"Nothing has been changed."
            ),
        },
        user_id=user_id,
    )


# ---------------------------------------------------------------------------
# Workflow entry points (registered action_triggered=False in
# workflow_entries.register_default_workflows — offer-seam reachable only)
# ---------------------------------------------------------------------------


async def run_clarify_reminder_clear_verb_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing for the variant-1 offer: a bare "yes" doesn't
    answer an either/or question — re-ask and re-arm the offer. effect: READ
    (nothing written; the real writes happen on an ANSWERED turn)."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != CLEAR_VERB_QUESTION_KIND or intent_service is None:
        logger.error(
            "clarify_reminder_clear_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    _rearm_verb_question(intent_service, session_id, user_id, payload)
    noun = payload.get("clear_noun") or "reminder"
    return {
        "message": (
            f"Just so I get it right — for these {_plural(noun, 2)}: "
            f"mark them done, or delete them?"
        ),
        "intent_data": {
            "category": "execution",
            "action": CLARIFY_CLEAR_VERB_WORKFLOW,
            "verb_disambiguation_pending": True,
        },
    }


async def run_reminder_clear_correction_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing for the correction window: a bare "yes" after
    "Say so if you meant delete this time" is ambiguous — point at the
    working phrase and re-arm the window one more turn. effect: READ."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != CLEAR_CORRECTION_KIND or intent_service is None:
        logger.error(
            "reminder_clear_correction_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    intent_service.workflow_offer_service.set_pending_offer(
        session_id,
        {
            "workflow_type": CLEAR_CORRECTION_WORKFLOW,
            "pending_action": dict(payload),
            "decline_message": "Good — they stay marked done.",
        },
        user_id=user_id,
    )
    return {
        "message": (
            "They're marked done. If you meant delete, say 'I meant delete' "
            "and I'll take care of it."
        ),
        "intent_data": {
            "category": "execution",
            "action": CLEAR_CORRECTION_WORKFLOW,
            "reminder_clear_correction_pending": True,
        },
    }


async def run_clear_reminders_delete_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """The CONFIRMED batch delete — dispatched ONLY through the #1190
    confirm path (run_confirm_pending_action_workflow re-dispatches the
    stored action on an explicit "yes"; action_triggered=False keeps the
    classifier/rail structurally away). effect: DESTRUCTIVE — deletes the
    todo rows resolved at offer time, by id, owner-scoped (#1532)."""
    ctx = context or {}
    intent = ctx.get("intent")
    intent_service = ctx.get("intent_service")
    if intent is None or intent_service is None:
        logger.error(
            "clear_reminders_delete_missing_context",
            has_intent=intent is not None,
            has_intent_service=intent_service is not None,
        )
        return None
    ictx = intent.context or {}
    ids = ictx.get("clear_target_ids") or []
    texts = ictx.get("clear_target_texts") or []
    noun = ictx.get("clear_noun") or "reminder"

    offer_user = ictx.get("user_id")
    principal = str(user_id) if user_id else offer_user
    if offer_user and principal and offer_user != principal:
        logger.warning(
            "clear_reminders_delete_principal_mismatch",
            offer_user=offer_user,
            turn_user=principal,
        )
        return {
            "message": "Let's hold off on that — nothing has been deleted.",
            "intent_data": {
                "category": "execution",
                "action": CLEAR_DELETE_WORKFLOW,
                "principal_mismatch": True,
            },
        }
    try:
        user_uuid = UUID(str(principal))
    except (ValueError, TypeError):
        return {
            "message": (
                "I need you to be logged in to delete todos. "
                "Nothing has been deleted."
            ),
            "intent_data": {
                "category": "execution",
                "action": CLEAR_DELETE_WORKFLOW,
                "error_type": "AuthenticationRequired",
            },
        }

    todo_service = intent_service.todo_handlers.todo_service
    deleted: List[str] = []
    failed = 0
    for tid, text in zip(ids, texts):
        try:
            ok = await todo_service.delete_todo(todo_id=UUID(tid), user_id=user_uuid)
            if ok:
                deleted.append(text)
            else:
                failed += 1
        except Exception as e:  # silent-ok: counted + logged; the summary states the honest denominator (m-44), never a fabricated all-deleted
            failed += 1
            logger.warning("reminder_clear_delete_failed", todo_id=tid, error=str(e))

    logger.info(
        "reminder_clear_batch_deleted",
        deleted=len(deleted),
        failed=failed,
        session_id=session_id,
    )
    n = len(deleted)
    lines = [f"Deleted {n} {_plural(noun, n)}:"]
    lines.extend(f"• {text}" for text in deleted)
    if failed:
        lines.append(
            f"({failed} couldn't be deleted just now — it may already be gone. "
            f"Say 'show my todos' to check.)"
        )
    return {
        "message": "\n".join(lines),
        "intent_data": {
            "category": "execution",
            "action": CLEAR_DELETE_WORKFLOW,
            "deleted_count": n,
            "failed_count": failed,
        },
    }
