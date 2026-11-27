"""2459: the session's last-shown issue, and the referent rule for a bare "it".

Arch's rule (issue 2459, "Arch, the lever for 2459"):

1. When a code read hands the person exactly ONE issue, it records that issue as the
   session's last-shown issue: owner- and session-scoped, ``(repository, number)``,
   taken from the read's data, never parsed from reply text. The reads in scope are
   the status gather's GitHub open-issue set (``ContextAssembler.gather_context`` on a
   STATUS/PRIORITY turn) and the issue listing (``_handle_list_issues_query``). A read
   that shows zero issues or several, or one whose repository the data does not carry,
   records the not-single marker, so an earlier single is never reused after it.
   The slot lives on the conversation context (the todo pattern,
   ``_remember_numbered_list``), NOT in the session activity ledger.
2. ``_handle_review_issue_query`` with no number in the words takes the NEWER of the
   created head (the ledger, issue 2114) and this slot (``choose_issue_referent``).
   Neither holds an issue, or the newest is a read that was not a single issue, or the
   two cannot be ordered: the existing ask for a number stands. An ambiguous "it" is
   never guessed.

Every write and read here is best-effort: a failure is logged and never changes or
blocks a reply (a lost slot only costs the ask).
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, NamedTuple, Optional, Sequence, Tuple

import structlog

logger = structlog.get_logger(__name__)

#: CXO's words (issue 2459, "Words I owe"): code resolved the referent ("it") but the
#: read of that issue failed. No cause, no repository claim.
REFERENT_READ_FAILED_LINE = "I couldn't pull up that issue just now."


class CreatedIssueRef(NamedTuple):
    """The ledger's created head (issue 2114) with the time its row was written."""

    repository: str
    number: int
    created_at: Optional[datetime] = None


def _valid_repository(value: Any) -> Optional[str]:
    """``owner/name`` exactly as the read's data carried it, else None (no guessing)."""
    if not isinstance(value, str):
        return None
    owner, sep, name = value.strip().partition("/")
    if not sep or not owner or not name or "/" in name:
        return None
    return value.strip()


def _valid_number(value: Any) -> Optional[int]:
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value if value > 0 else None
    if isinstance(value, str) and value.isdigit():
        n = int(value)
        return n if n > 0 else None
    return None


def record_shown_issues(
    session_id: Optional[str],
    user_id: Any,
    shown: Sequence[Tuple[Any, Any]],
    total: Optional[int] = None,
) -> None:
    """Record what an issue read just showed: ``shown`` is ``(repository, number)``
    per issue shown, from the read's data; ``total`` is how many the read found when
    that can exceed what was shown. Exactly one shown, of exactly one found, with a
    valid repository and number → that issue. Anything else → the not-single marker.
    No principal or no session → nothing (owner-scoped by construction)."""
    if not session_id or not user_id:
        return
    try:
        from services.intent_service.conversation_context import (
            ShownIssue,
            get_or_create_context,
        )

        repository: Optional[str] = None
        number: Optional[int] = None
        if len(shown) == 1 and (total is None or total == 1):
            repository = _valid_repository(shown[0][0])
            number = _valid_number(shown[0][1])
            if repository is None or number is None:
                repository, number = None, None
        ctx = get_or_create_context(str(session_id), user_id=str(user_id))
        ctx.last_shown_issue = ShownIssue(repository=repository, number=number)
    except Exception as e:  # silent-ok: logged; a lost slot only costs the ask for a number
        logger.warning("shown_issue_record_failed", error=str(e), session_id=session_id)


def last_shown_issue(session_id: Optional[str], user_id: Any):
    """The session's last-shown issue slot (a ``ShownIssue``), or None. Best-effort."""
    if not session_id or not user_id:
        return None
    try:
        from services.intent_service.conversation_context import get_or_create_context

        return get_or_create_context(str(session_id), user_id=str(user_id)).last_shown_issue
    except Exception as e:  # silent-ok: logged; treated as "nothing shown"
        logger.warning("shown_issue_recall_failed", error=str(e), session_id=session_id)
        return None


def _as_utc(value: Any) -> Optional[datetime]:
    if not isinstance(value, datetime):
        return None
    return value if value.tzinfo is not None else value.replace(tzinfo=timezone.utc)


def choose_issue_referent(
    created: Optional[CreatedIssueRef], shown: Any
) -> Optional[Tuple[str, int]]:
    """Arch's rule 2: the newer of the created head and the shown slot.

    - Only one of them present: that one (a not-single slot yields None).
    - Both: the newer wins; if the newer is a not-single read, None. If they cannot
      be ordered (a missing timestamp, or the same instant), None: never a guess.
    """
    shown_at = _as_utc(getattr(shown, "shown_at", None)) if shown is not None else None
    shown_ref: Optional[Tuple[str, int]] = None
    if shown is not None and getattr(shown, "single", False):
        shown_ref = (str(shown.repository), int(shown.number))
    if created is None:
        return shown_ref
    created_ref = (created.repository, created.number)
    if shown is None:
        return created_ref
    created_at = _as_utc(created.created_at)
    if created_at is None or shown_at is None or created_at == shown_at:
        return None
    return created_ref if created_at > shown_at else shown_ref
