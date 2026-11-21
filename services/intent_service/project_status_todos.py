"""#2301 (handler-only): a status ask that names one of the person's projects also
shows that project's open todos.

Arch 2026-11-20 (mails 01M7Y2ZP7C, 01M7Y3JVMS), after two catalog wordings for a
``list_project_todos`` line failed their rule-7 screens: no catalog text changes.
Main's router already sends ``get_project_status`` with a ``project`` arg for
"what's in my Mobile Redesign project?" and "what's left to do in Mobile
Redesign", so the read hangs off that op:

1. The project is the router's arg, through the one reader
   (``todo_project_attach.router_project_name``, the word-set guard), then
   ``lookup``. Nothing reads a project name out of the person's words. No arg:
   today's reply, nothing added.
2. Only EXACTLY ONE match adds anything. Several, none, no projects, or a failed
   project read: today's reply, nothing added and no question (a status read asks
   nothing new). A failed project read is logged under its own event.
3. The block is code's, never the floor's: the floor does not receive the list.
   It goes after the floor's reply, under CXO's header, in the main list's own
   render (grouping, chips, numbering, cap line), and its lines are recorded as
   the last numbered list, so "complete the first one" binds to what was shown.
   A failed todo read says CXO's line; a partial list is never shown.
4. It goes on every status ask that names a project ("how is X going?" too):
   code cannot tell the phrasings apart, and a word check would be the parsing
   ADR-080 forbids.
5. The #2197 milestone branch comes first; when it resolves, nothing is added.

CXO 2026-11-20 (mails 01M7Y2W1YE, 01M7Y3EYRS): the three lines below. The header
names the STORED project, so "Launch project" typed against a stored "Launch"
shows what was matched.
"""

from __future__ import annotations

from typing import Any, Optional

import structlog
from sqlalchemy.exc import SQLAlchemyError

from services.intent_service import todo_project_attach as _attach

logger = structlog.get_logger(__name__)

STATUS_OP = "get_project_status"

OPEN_TODOS_HEADER = "Open todos in {project}:"
# CXO may drop this once today's status reply has been quoted (01M7Y3EYRS).
NO_OPEN_TODOS_LINE = "No open todos in it."
TODOS_READ_FAILED_LINE = "I couldn't check its todos just now."
CAP_LINE = "Showing the first {count} todos in {project}."


async def status_todos_block(
    intent: Any, session_id: Optional[str], user_id: Optional[str], todo_handlers: Any
) -> str:
    """The text to put after the floor's status reply, or "" when nothing is
    added. Never raises for a failed read: the status reply must stand."""
    if getattr(intent, "action", None) != STATUS_OP:
        return ""
    from services.intent.intent_service import _coerce_todo_principal

    todo_user = _coerce_todo_principal(user_id)
    if not todo_user:
        return ""
    try:
        resolution = await _attach.resolve(intent, todo_user)
    except (SQLAlchemyError, OSError) as e:
        logger.error("project_status_todos_project_read_failed", error=str(e))
        return ""
    if resolution is None or resolution.one is None:
        logger.info(
            "project_status_todos_not_one_project",
            named=resolution is not None,
            matches=len(resolution.matches) if resolution is not None else 0,
        )
        return ""
    project = resolution.one
    try:
        return str(await todo_handlers.project_status_todos(session_id, todo_user, project))
    except (SQLAlchemyError, OSError) as e:
        logger.error("project_status_todos_todo_read_failed", error=str(e))
        return TODOS_READ_FAILED_LINE
