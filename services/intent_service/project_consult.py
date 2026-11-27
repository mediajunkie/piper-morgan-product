"""Issue 2425: a second router call only when the first one CLARIFYs and the person has
stored projects, accepting only ``create_todo`` into one of those projects.

BUILT ON A BRANCH FOR REVIEW. Not landed and not approved: this is a second consult
class beside ADR-083 D5, so it needs xian's explicit word through Exec before main.

The Chief Architect's rule (issue 2425, comment "Arch: the lever for 2425"), binding:

1. **The main call is unchanged**, with no project names in it, so every turn it
   answers today is untouched by construction (D5's rule).
2. **Only when the main call returns CLARIFY** and the person has at least one stored
   project does code make one more ``route()`` call on the same message. Its session
   block adds one fact line: the person's own project names, owner-scoped, as stored,
   capped at 20, sorted for determinism.
3. **Code accepts the second answer only when** it names ``create_todo`` with a
   ``project`` arg that equals one of those stored names exactly, ignoring case, and a
   non-empty todo text. Anything else keeps the CLARIFY byte for byte, and the turn goes
   on as today. The write then runs the existing 2297 attach path, its lookup and its
   bound confirm unchanged. The consult adds no write path.
4. **The new fact line** is router prompt text on the consult only, so rule 7 applies
   to the consult population.
5. **Latency:** the consult uses D5's own ceiling, 1.5 s. On a timeout it keeps the
   CLARIFY.

How this module holds each item:

- (1) ``inversion_live`` builds the main call's block exactly as before; the fact line
  is added here, to a COPY of that block, for the second call only. The line is never
  part of ``SessionSnapshot`` or ``serialize_for_prompt``, so no other router call
  (live first call, shadow, pre-claim) can carry it.
- (2) ``consult_projects_on_clarify`` returns the first decision unread unless its
  outcome is ``clarify``; with no principal, a failed read, or zero projects it makes
  no call. The names come from 2297's own owner-scoped read
  (``todo_project_attach._active_projects``). ``project_fact_line`` sorts and caps.
- (3) ``accepted_project`` decides on the structured decision only (outcome, operation,
  args), never on reply text. The comparison is against the STORED names from the read,
  with 2297's own comparison (``todo_project_attach.exact_matches``), never against the
  sanitised prompt text. It also requires that the two downstream readers will see what
  was accepted: 2297's ``router_project_name`` (the word-set guard) must return the
  stored name, and the handler's ``_router_todo_text`` (keys ``text`` then ``task``)
  must return a non-empty title. On acceptance the decision is copied with the
  ``project`` arg set to the stored spelling; nothing is written here.
- (5) one deadline of ``D5_CONSULT_CEILING_S`` covers the project read and the second
  call together; a timeout or any error keeps the first decision object itself.

Composition with D5 (``list_consult.consult_on_clarify``): ``inversion_live`` runs D5
first, unchanged, and passes its result here. This consult fires only when that result
is still a CLARIFY, which means D5 either was not in scope or did not accept. So D5's
behaviour is byte for byte what it was, and each consult class makes at most one extra
call. A turn makes TWO extra calls only when a numbered list is in scope, D5's call did
not accept (kept, failed or timed out), and the person has stored projects.
"""

from __future__ import annotations

import asyncio
import dataclasses
import json
import time
import unicodedata
from typing import Any, Awaitable, Callable, List, Optional, Sequence

import structlog

from services.intent_service import todo_project_attach as _attach
from services.intent_service.list_consult import D5_CONSULT_CEILING_S

logger = structlog.get_logger(__name__)

# The one operation this consult may accept (Arch rule 3).
CONSULT_OPERATION = "create_todo"
# Arch rule 2: at most this many names, sorted, in the fact line.
MAX_PROJECT_NAMES = 20
# Each name as shown to the router: whitespace collapsed, control characters dropped,
# clipped to this many characters. Display only; acceptance compares STORED names.
PROJECT_NAME_CHARS = 60
# The fact line (new router prompt text, consult only). Plain and factual: a label and
# the names, each JSON-quoted so a comma, quote or backslash in a name cannot change
# where one name ends. No instruction about what to do with them.
PROJECT_FACT_LABEL = "STORED PROJECTS"
PROJECT_FACT_LINE = PROJECT_FACT_LABEL + ": {names}"

ProjectReader = Callable[[str], Awaitable[Optional[List[Any]]]]


def _display_name(name: Any) -> str:
    """One stored name made safe for one prompt line: control and format characters
    dropped, whitespace (newlines included) collapsed, clipped with an ellipsis."""
    text = "".join(
        ch if not unicodedata.category(ch).startswith("C") else " " for ch in str(name or "")
    )
    text = " ".join(text.split())
    if len(text) > PROJECT_NAME_CHARS:
        text = text[: PROJECT_NAME_CHARS - 1].rstrip() + "…"
    return text


def listed_projects(projects: Sequence[Any]) -> List[Any]:
    """The stored projects the fact line names: sorted by name (case-folded, then as
    stored, so the order is deterministic), first ``MAX_PROJECT_NAMES``."""
    named = [p for p in projects or [] if str(getattr(p, "name", "") or "").strip()]
    named.sort(key=lambda p: (str(p.name).casefold(), str(p.name), str(getattr(p, "id", ""))))
    return named[:MAX_PROJECT_NAMES]


def project_fact_line(projects: Sequence[Any]) -> str:
    """The consult's one fact line, or "" when no project has a name."""
    shown = [_display_name(p.name) for p in listed_projects(projects)]
    shown = [s for s in shown if s]
    if not shown:
        return ""
    return PROJECT_FACT_LINE.format(
        names=", ".join(json.dumps(s, ensure_ascii=False) for s in shown)
    )


def consult_block(main_block: str, fact_line: str) -> str:
    """The second call's session block: the main call's block plus the fact line."""
    return f"{main_block}\n{fact_line}" if main_block else fact_line


def accepted_project(decision: Any, projects: Sequence[Any], message: str) -> Optional[str]:
    """The STORED project name when the second answer may replace the CLARIFY, else
    ``None``. Structured fields only; never reply text."""
    if getattr(decision, "outcome", None) != "operation":
        return None
    if getattr(decision, "operation", None) != CONSULT_OPERATION:
        return None
    args = getattr(decision, "args", None)
    if not isinstance(args, dict):
        return None
    raw = args.get(_attach.ROUTER_PROJECT_ARG)
    if not isinstance(raw, str) or not raw.strip():
        return None
    # Equal to a stored name ignoring case (2297's own comparison), against EVERY
    # stored project: two stored names that differ only in case are ambiguous here.
    matches = _attach.exact_matches(list(projects or []), raw)
    if len(matches) != 1:
        return None
    listed_ids = {str(getattr(p, "id", "")) for p in listed_projects(projects)}
    if matches[0].id not in listed_ids:
        return None  # a stored name the fact line did not show
    stored = matches[0].name
    # The downstream readers must see what was accepted, or the write would run
    # without the project (2297's word-set guard) or without the title.
    probe_args = dict(args)
    probe_args[_attach.ROUTER_PROJECT_ARG] = stored
    # A real Intent, the type both readers are written for (the type gate refuses a
    # stand-in here, and a stand-in could drift from what the handler is handed).
    from services.domain.models import Intent
    from services.shared_types import IntentCategory

    probe = Intent(
        original_message=message,
        category=IntentCategory.EXECUTION,
        action=CONSULT_OPERATION,
        confidence=1.0,
        context={"inversion_args": probe_args, "original_message": message},
    )
    if _attach.router_project_name(probe) != " ".join(stored.split()):
        return None
    from services.intent_service.todo_handlers import TodoIntentHandlers

    if not TodoIntentHandlers._router_todo_text(probe, message):
        return None
    return stored


async def read_stored_projects(user_id: str) -> Optional[List[Any]]:
    """The person's own active projects, by 2297's read; ``None`` with no principal.
    A failed read RAISES (the caller keeps the CLARIFY)."""
    from services.intent.intent_service import _coerce_todo_principal

    todo_user = _coerce_todo_principal(user_id)
    if not todo_user:
        return None
    return list(await _attach._active_projects(str(todo_user)))


async def consult_projects_on_clarify(
    message: str,
    decision: Any,
    main_block: str,
    *,
    route: Any,
    router_snapshot: Any,
    llm_service: Any,
    grammar: Any,
    user_id: Optional[str],
    session_id: Optional[str] = None,
    read_projects: Optional[ProjectReader] = None,
) -> Any:
    """Issue 2425: the first decision, or the second call's answer when it is accepted
    (with the stored project spelling). Never writes."""
    if getattr(decision, "outcome", None) != "clarify" or not user_id:
        return decision
    reader = read_projects or read_stored_projects
    started = time.monotonic()

    def _elapsed_ms() -> int:
        return int((time.monotonic() - started) * 1000)

    try:
        projects = await asyncio.wait_for(reader(user_id), timeout=D5_CONSULT_CEILING_S)
    except (
        Exception
    ) as e:  # silent-ok: Arch (2425): a failed read means no consult; the CLARIFY stands, logged
        logger.warning(
            "inversion_live_project_consult",
            outcome="kept",
            reason=f"project_read_failed:{type(e).__name__}",
            elapsed_ms=_elapsed_ms(),
            session_id=session_id,
        )
        return decision
    if not projects:
        return decision  # no principal or no projects: no consult, no extra call
    line = project_fact_line(projects)
    if not line:
        return decision
    from services.intent_service.session_snapshot import MAX_SERIALIZED_CHARS

    block = consult_block(main_block or "", line)
    if len(block) > MAX_SERIALIZED_CHARS:
        logger.warning(
            "inversion_live_project_consult",
            outcome="kept",
            reason="block_over_cap",
            elapsed_ms=_elapsed_ms(),
            session_id=session_id,
        )
        return decision
    remaining = D5_CONSULT_CEILING_S - (time.monotonic() - started)
    try:
        if remaining <= 0:
            raise asyncio.TimeoutError()
        second = await asyncio.wait_for(
            route(
                message,
                router_snapshot(state_block=block),
                llm_service=llm_service,
                grammar=grammar,
                user_id=user_id,
            ),
            timeout=remaining,
        )
    except (
        Exception
    ) as e:  # silent-ok: Arch (2425) rule 5: a timeout or failure keeps the CLARIFY, logged
        logger.warning(
            "inversion_live_project_consult",
            outcome="kept",
            reason=type(e).__name__,
            project_count=len(projects),
            elapsed_ms=_elapsed_ms(),
            session_id=session_id,
        )
        return decision
    stored = accepted_project(second, projects, message)
    # Warning, as D5's line: alpha keeps warning-level events only. No message text
    # and no project names are logged.
    logger.warning(
        "inversion_live_project_consult",
        outcome="accepted" if stored is not None else "kept",
        operation=getattr(second, "operation", None),
        second_outcome=getattr(second, "outcome", None),
        project_count=len(projects),
        project_arg_present=isinstance(
            (getattr(second, "args", None) or {}).get(_attach.ROUTER_PROJECT_ARG), str
        ),
        llm_calls=getattr(second, "llm_calls", None),
        repair_attempted=getattr(second, "repair_attempted", None),
        repair_error=(getattr(second, "repair_error", None) or "")[:200] or None,
        served_provider=getattr(second, "served_provider", None),
        served_model=getattr(second, "served_model", None),
        output_tokens=(getattr(second, "usage", None) or {}).get("output_tokens"),
        llm_latency_ms=getattr(second, "llm_latency_ms", None),
        elapsed_ms=_elapsed_ms(),
        session_id=session_id,
    )
    if stored is None:
        return decision
    args = dict(second.args)
    args[_attach.ROUTER_PROJECT_ARG] = stored
    return dataclasses.replace(second, args=args)
