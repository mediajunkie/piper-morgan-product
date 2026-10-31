"""#2233: a due reminder reaches the user unasked only through this seam.

ADR-080: code decides whether and where; the model never sees ``due_reminders`` off the
reminder list (context_assembler) and never paraphrases the line. Eligibility is the
declared op set ``DUE_REMINDER_LINE_OPS`` (workflow_dispatcher), keyed on the router's
verdict, never on the message. Exclusions win: no principal, an unsuccessful or
clarifying result, or an error. Once per todo id per principal's session, held on the
principal-keyed conversation context (#2223 rule). A failed read renders nothing.
"""

from __future__ import annotations

from typing import Any, List, Optional

import structlog

logger = structlog.get_logger(__name__)

MAX_NAMED = 3


def _when(reminder_date: Any, tz_name: str) -> str:
    """CXO's rule: a clock time with "today" only if the date is today in the user's
    zone, otherwise the date ("Oct 29"). Zone math is datetime_utils' (#2204)."""
    from services.utils.datetime_utils import format_user_time, now_in_zone, to_user_tz

    local = to_user_tz(reminder_date, tz_name)
    if local.date() == now_in_zone(tz_name).date():
        return f"today at {format_user_time(reminder_date, tz_name)}"
    return f"{local.strftime('%b')} {local.day}"


def render_due_reminder_line(rows: List[Any], tz_name: str) -> str:
    """CXO's words (2026-10-30): one item, two or three, or the first three plus a count."""
    items = [(str(r.text), _when(r.reminder_date, tz_name)) for r in rows]
    if len(items) == 1:
        text, when = items[0]
        return f'Reminder: "{text}" came due {when}.'
    named = ", ".join(f'"{t}" ({w})' for t, w in items[:MAX_NAMED])
    more = len(items) - MAX_NAMED
    tail = f", and {more} more." if more > 0 else "."
    return f"Reminders that came due: {named}{tail}"


async def due_reminder_line(
    *, action: Optional[str], result: Any, user_id: Optional[str], session_id: Optional[str]
) -> Optional[str]:
    """The line to append after this turn's answer, or None."""
    from services.intent_service.conversation_context import get_or_create_context
    from services.intent_service.workflow_dispatcher import (
        DUE_REMINDER_LINE_OPS,
        DUE_REMINDER_SELF_RENDERING_OPS,
        normalize_action,
    )

    if not user_id or not session_id or not action:
        return None  # anonymous: no principal, no todos to read
    op = normalize_action(action)
    if op not in DUE_REMINDER_LINE_OPS:
        return None
    if (
        not getattr(result, "success", False)
        or getattr(result, "requires_clarification", False)
        or getattr(result, "error", None)
        or getattr(result, "error_type", None)
    ):
        return None  # a decline, an error, a could-not-check reply
    try:
        from uuid import UUID

        from services.intent_service.todo_handlers import TodoIntentHandlers
        from services.utils.datetime_utils import user_timezone_name

        rows = await TodoIntentHandlers().get_due_reminder_rows(UUID(str(user_id)))
        if rows is None:
            logger.warning("due_reminder_line_read_failed", session_id=session_id)
            return None
        surfaced = get_or_create_context(session_id, user_id=user_id).surfaced_reminder_ids
        fresh = [r for r in rows if str(r.id) not in surfaced]
        if not fresh:
            return None
        surfaced.update(str(r.id) for r in fresh)
        if op in DUE_REMINDER_SELF_RENDERING_OPS:
            return None  # the op's own answer shows them: surfaced, no second mention
        return render_due_reminder_line(fresh, await user_timezone_name(user_id))
    except (
        Exception
    ) as e:  # silent-ok: logged; the line is unrequested, so silence is honest (#2151)
        logger.warning("due_reminder_line_error", error=str(e), session_id=session_id)
        return None
