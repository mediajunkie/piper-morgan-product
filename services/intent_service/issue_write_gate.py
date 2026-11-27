"""2459 (Arch's ruling, part 2): the one gate in front of every GitHub issue write
that takes an issue number (update, close, reopen, comment).

The rule:

1. A number the person typed in THIS message is accepted as today. "Typed" is read
   from the person's own message text with the handlers' existing pattern
   (``#?(\\d+)``, the parse ``_issue_number_from`` and the handlers use): a number
   counts as typed when that pattern would find it anywhere in the message (read as
   digit runs, the same matches), so nothing accepted today is refused. No new
   pattern.
2. Otherwise the number is accepted only if it is the session's created head
   (``issue_head``: owner- and session-scoped, as ``_issue_referent_from_ledger``
   reads it) AND the created head is the session's referent under
   ``choose_issue_referent`` (no newer read showed a different issue or several),
   with the same repository when one is carried.
3. Anything else is refused: the caller says its existing ask for a number, and
   nothing is armed, recorded or sent. That covers a number taken from the RECENT
   ISSUE line for a shown issue, a router arg, and a model's guess.

The gate never trusts the router: it compares the candidate with the message text
and the ledger in code. A failed ledger read is "no created head" (refusal unless
typed), never a pass.

An accepted verdict is stamped on the intent (``GATE_CONTEXT_KEY``), so the same
intent re-dispatched by a confirmed "yes" or a repository answer is not gated a
second time against a ledger read that might fail on that turn.

``issue_number_arg`` is the one normaliser for the issue key (``issue_number`` or
``issue``; the router emits both): the gate and the handlers read through it.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Mapping, Optional, Set, Tuple

import structlog

from services.intent_service.shown_issue import (
    LEDGER_UNREADABLE,
    SHOWN_ISSUE_WHICH_ASK,
    CreatedIssueRef,
    choose_issue_referent,
    last_shown_issue,
)

logger = structlog.get_logger(__name__)

# Each handler's EXISTING ask for an issue number, moved here byte for byte so the
# gate's refusal and the handler's own no-number path say the same sentence. No new
# copy (2459: a refused write gets the existing ask).
UPDATE_ISSUE_NUMBER_ASK = (
    "I couldn't find an issue number in your request. Please specify an issue number "
    "(e.g., 'update issue #123')."
)
COMMENT_ISSUE_NUMBER_ASK = (
    "I couldn't find an issue number in your request. Please specify an issue number "
    "(e.g., 'comment on issue #123 saying...')."
)
# #2120: no search ran, so no "couldn't find" claim (close and its reopen twin).
CLOSE_ISSUE_NUMBER_ASK = (
    "I can close a particular issue if you give me its number, like "
    '"close #123". I don\'t search for finished issues or close them in '
    "bulk yet."
)
REOPEN_ISSUE_NUMBER_ASK = (
    "I can reopen a particular issue if you give me its number, like "
    '"reopen #123". I don\'t search for closed issues or reopen them in '
    "bulk yet."
)

#: Where an accepted verdict rides the intent's context.
GATE_CONTEXT_KEY = "issue_write_gate"

_ISSUE_KEYS = ("issue_number", "issue")

CreatedHeadReader = Callable[[Optional[str], Optional[str]], Awaitable[Optional[CreatedIssueRef]]]


def _as_issue_number(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, str):
        text = value.strip().lstrip("#")
        if text.isdigit():
            n = int(text)
            return n if n > 0 else None
    return None


def issue_number_arg(mapping: Optional[Mapping[str, Any]]) -> Optional[int]:
    """The issue number a context or args dict carries, under ``issue_number`` or
    ``issue``, as one positive int. A non-integer value counts as absent."""
    if not isinstance(mapping, Mapping):
        return None
    for key in _ISSUE_KEYS:
        number = _as_issue_number(mapping.get(key))
        if number is not None:
            return number
    return None


def message_of(intent: Any) -> str:
    """The person's own message for this intent (the text the handlers parse)."""
    ctx = getattr(intent, "context", None) or {}
    return ctx.get("original_message") or getattr(intent, "original_message", None) or ""


def typed_issue_numbers(message: str) -> Set[int]:
    """Every number the handlers' pattern finds in the person's message."""
    # Every maximal run of digits: exactly what the handlers' ``#?(\d+)`` matches
    # (the ``#`` is optional, so it never changes which digits match). Read here by
    # character class, not a second copy of the pattern (the binder ratchet).
    runs = "".join(ch if ch.isdigit() else " " for ch in (message or "")).split()
    return {int(r) for r in runs if int(r) > 0}


@dataclass(frozen=True)
class IssueWriteVerdict:
    """``shown`` (refusals only): the single SHOWN issue that is the session's
    referent, ``(repository, number)`` from the slot's data, when the refusal is
    because that shown issue is the only candidate referent. The caller then says
    ``SHOWN_ISSUE_WHICH_ASK`` (``refusal_line``) instead of its plain ask."""

    accepted: bool
    number: Optional[int] = None
    repository: Optional[str] = None
    reason: str = ""
    shown: Optional[Tuple[str, int]] = None


def _same_repo(a: Optional[str], b: Optional[str]) -> bool:
    return bool(a) and bool(b) and str(a).casefold() == str(b).casefold()


def _stamp(intent: Any, verdict: IssueWriteVerdict) -> None:
    """Mark the intent's own context dict in place (never replaced: the #1459
    original_message ratchet). No context dict: nothing marked, so a re-dispatch is
    only gated again."""
    ctx = getattr(intent, "context", None)
    if not isinstance(ctx, dict):
        return
    try:
        ctx[GATE_CONTEXT_KEY] = {
            "number": verdict.number,
            "repository": verdict.repository,
            "reason": verdict.reason,
        }
    except Exception as e:  # silent-ok: logged; an unstamped intent is only gated again
        logger.warning("issue_write_gate_stamp_failed", error=str(e))


def _non_integer_issue_key(intent: Any) -> bool:
    """An issue key is present (context or router args) but is not an integer."""
    ctx = getattr(intent, "context", None) or {}
    for mapping in (ctx, ctx.get("inversion_args")):
        if not isinstance(mapping, Mapping):
            continue
        for key in _ISSUE_KEYS:
            value = mapping.get(key)
            if value not in (None, "") and _as_issue_number(value) is None:
                return True
    return False


async def _read_head(
    created_head: Optional[CreatedHeadReader], user_id: Optional[str], session_id: Optional[str]
) -> Optional[CreatedIssueRef]:
    """The owner-scoped created head; a reader that raises counts as unreadable."""
    if created_head is None or not user_id or not session_id:
        return None
    try:
        return await created_head(user_id, session_id)
    except Exception as e:  # silent-ok: logged; unreadable means the ask, never a pass
        logger.warning("issue_write_gate_ledger_failed", error=str(e))
        return LEDGER_UNREADABLE


def _shown_referent(
    head: Optional[CreatedIssueRef], user_id: Optional[str], session_id: Optional[str]
) -> Optional[Tuple[str, int]]:
    """The single shown issue when it is the session's referent (shown only, or a
    show newer than the create), from the slot's data; else None."""
    shown = last_shown_issue(session_id, user_id)
    if shown is None or not getattr(shown, "single", False):
        return None
    chosen = choose_issue_referent(head, shown)
    if chosen is None or (chosen[0], chosen[1]) != (shown.repository, shown.number):
        return None
    return chosen


def _refuse(
    action: Any,
    reason: str,
    number: Optional[int],
    repository: Optional[str],
    shown: Optional[Tuple[str, int]] = None,
) -> IssueWriteVerdict:
    logger.info("issue_write_gate_refused", action=action, reason=reason, named=bool(shown))
    return IssueWriteVerdict(False, number, repository, reason, shown)


def refusal_line(verdict: IssueWriteVerdict, plain_ask: str) -> str:
    """What a refused write says: the named ask when the only candidate referent is
    a single shown issue, else the handler's existing ask, byte for byte."""
    if verdict.shown is not None:
        repository, number = verdict.shown
        return SHOWN_ISSUE_WHICH_ASK.format(number=number, repository=repository)
    return plain_ask


async def gate_issue_write(
    intent: Any,
    candidate: Any,
    *,
    repository: Optional[str],
    user_id: Optional[str],
    session_id: Optional[str],
    created_head: Optional[CreatedHeadReader],
    stamp: bool = True,
) -> IssueWriteVerdict:
    """Decide whether ``candidate`` (the number the write would act on, or None when
    the write found none) may be written. ``repository`` is the repository the write
    would use when the turn carries one (context or slot-fill), else None.
    ``created_head`` reads the owner-scoped ledger head
    (``IntentService._issue_referent_from_ledger``).

    ``stamp=False`` (the ask-time callers) leaves the intent untouched: an ask binds
    only what its question shows (the #2304/#2379 pins).

    A refusal carries ``shown`` when the session's referent is a single shown issue
    (see ``refusal_line``), except for a repository mismatch or a non-integer issue
    key, which keep the plain ask."""
    action = getattr(intent, "action", None)
    number = _as_issue_number(candidate)
    if number is None:
        if _non_integer_issue_key(intent):
            return _refuse(action, "non_integer", None, repository)
        # The ledger is read only when a single shown issue could be the referent
        # (the named ask); otherwise the plain ask needs no read.
        shown = last_shown_issue(session_id, user_id)
        if shown is None or not getattr(shown, "single", False):
            return _refuse(action, "no_number", None, repository)
        head = await _read_head(created_head, user_id, session_id)
        return _refuse(
            action, "no_number", None, repository, _shown_referent(head, user_id, session_id)
        )

    ctx = getattr(intent, "context", None) or {}
    args_number = issue_number_arg(ctx.get("inversion_args"))
    if args_number is not None and args_number != number:
        # The router's number is not what this write acts on; logged, never used.
        logger.info(
            "issue_write_gate_args_differ", action=action, args_number=args_number, number=number
        )

    stamped = ctx.get(GATE_CONTEXT_KEY)
    if isinstance(stamped, dict) and stamped.get("number") == number:
        return IssueWriteVerdict(
            True, number, stamped.get("repository") or repository, "gated_earlier"
        )

    if number in typed_issue_numbers(message_of(intent)):
        verdict = IssueWriteVerdict(True, number, repository, "typed")
        if stamp:
            _stamp(intent, verdict)
        return verdict

    head = await _read_head(created_head, user_id, session_id)
    usable = head if head is not None and not head.unreadable else None
    if usable is not None and usable.number == number:
        chosen = choose_issue_referent(usable, last_shown_issue(session_id, user_id))
        if chosen is not None and chosen[1] == number and _same_repo(chosen[0], usable.repository):
            if repository and not _same_repo(repository, usable.repository):
                return _refuse(action, "repository_differs", number, repository)
            verdict = IssueWriteVerdict(True, number, usable.repository, "created_head")
            if stamp:
                _stamp(intent, verdict)
            return verdict
        return _refuse(
            action,
            "created_head_not_newest",
            number,
            repository,
            _shown_referent(head, user_id, session_id),
        )
    return _refuse(
        action,
        "not_typed_or_created",
        number,
        repository,
        _shown_referent(head, user_id, session_id),
    )
