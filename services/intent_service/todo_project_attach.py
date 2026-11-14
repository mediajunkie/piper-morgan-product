"""#2297: a todo created with a named project is attached to that project.

Arch's ruling (decisions.log 2026-11-06 11:13, (A)) and CXO's words (11-06 11:14):

- WHICH project is meaning, and it is the router's: the ``project`` arg the router
  declares on ``create_todo`` (``context["inversion_args"]["project"]``). Code reads
  no project name out of the person's words (ADR-080); no pattern is written here.
- Code RESOLVES that name against the person's own ACTIVE projects: the whole
  stored name equals it, case-insensitively. String comparison only.
  - one: the todo is written with that project's id, and the reply says so;
  - none: nothing is written; CXO's not-found line;
  - several: nothing is written; an ARMED numbered pick (the #1987 shape, as
    #2271's archive pick), the project ids and the todo titles bound at ask time.
    A number answer writes the bound titles into the bound project at the pop
    seam (``handle_todo_project_pick_turn``).
- A todo is never attached to a fuzzy guess, and a project is never created here.

No ``project`` arg: this module returns ``None`` and create_todo is unchanged.

#2301 (Arch 11-06 13:34: "a project-scoped todo read reached through its own
catalog line"): the ``list_project_todos`` op resolves its ``project`` arg the same
way and shows that one project's open todos. One: the list (CXO's header). None,
or no arg: a statement; nothing is guessed. Several: the same armed numbered pick
with ``purpose`` "read", whose number shows the bound project's todos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import structlog

logger = structlog.get_logger(__name__)

ROUTER_PROJECT_ARG = "project"

TODO_PROJECT_PICK_KIND = "todo_project_pick_question"
# The registered offer-only landing (action_triggered=False): a bare "yes" names
# no project, so it re-asks and re-arms.
TODO_PROJECT_PICK_WORKFLOW = "clarify_todo_project_pick"
PICK_PENDING_FLAG = "todo_project_pick_pending"
# The result key the armed record rides from the resolver to the rail adapter.
OFFER_RECORD_KEY = "todo_project_offer"

# CXO 11-06 (verbatim).
ATTACHED_LINE = "I've added '{text}' to {project}."
NOT_FOUND_LINE = (
    "I couldn't find a project called \"{name}\", so I haven't added anything. "
    'Check the name, or say "show my projects".'
)
# Named *_QUESTION: rendered only by build_pick_offer / the re-ask landing, which
# store it as the record's ``question`` and arm the record (the #1766 rule).
SEVERAL_QUESTION = (
    "I found more than one project with that name: {listed}. "
    "Which one should I add it to? Say the number."
)
# NOT YET RULED by CXO (asked in the 2297 build report): several titles into one
# project, and the decline of the pick. Shaped on the ruled single line and on the
# adopted-write decline copy.
ATTACHED_SEVERAL_LINE = "I've added {count} todos to {project}: {names}."
PICK_DECLINE_LINE = "Okay, I haven't added anything. Nothing has been changed."
# #2301. CXO 11-06 11:14 (verbatim): the empty project. The header for a project
# with todos is format_todo_list_grouped(owner=...).
PROJECT_EMPTY_LINE = "{project} has no todos yet."
# NOT YET RULED by CXO (asked in the 2301 build report): the read's not-found,
# no-name, several-match and decline lines, shaped on the ruled create lines.
READ_NOT_FOUND_LINE = (
    'I couldn\'t find a project called "{name}". Check the name, or say "show my projects".'
)
READ_NO_NAME_LINE = 'I\'m not sure which project you mean. Say its name, or say "show my projects".'
READ_SEVERAL_QUESTION = (
    "I found more than one project with that name: {listed}. "
    "Which one do you mean? Say the number."
)
READ_PICK_DECLINE_LINE = "Okay. Nothing has been changed."
PURPOSE_ADD = "add"
PURPOSE_READ = "read"
PRINCIPAL_MISMATCH_LINE = "Let's hold off on that — nothing has been changed."
NOT_ARMED_LINE = (
    "I found more than one project with that name, so I haven't added anything. "
    "Rename one of them, then ask again."
)
# NOT YET RULED by CXO: the project read failed before the write (nothing written).
RESOLVE_FAILED_LINE = (
    "I couldn't check your projects just now, so I haven't added anything. "
    "Try again in a moment; if it keeps failing, tell us."
)
READ_PROJECT_GONE_LINE = "I couldn't find that project anymore."
LIST_PROJECT_TODOS_OP = "list_project_todos"
PROJECT_GONE_LINE = "I couldn't find that project anymore, so I haven't added anything."

# A pick answer is a short reply ("2", "the second one"); a longer message is a
# new request and routes normally.
_MAX_ANSWER_WORDS = 3


@dataclass(frozen=True)
class ProjectRef:
    """A resolved project: its id and its stored name (never the typed one)."""

    id: str
    name: str


@dataclass(frozen=True)
class Resolution:
    """What the router's ``project`` arg resolved to among the person's own
    active projects. ``name`` is the arg as the router gave it."""

    name: str
    matches: List[ProjectRef] = field(default_factory=list)

    @property
    def one(self) -> Optional[ProjectRef]:
        return self.matches[0] if len(self.matches) == 1 else None


def _key(name: Any) -> str:
    return " ".join(str(name or "").split()).casefold()


def router_project_name(intent: Any) -> Optional[str]:
    """The router's ``project`` arg, whitespace-collapsed, or ``None``. A non-string
    or empty value is no arg at all."""
    args = (getattr(intent, "context", None) or {}).get("inversion_args")
    raw = args.get(ROUTER_PROJECT_ARG) if isinstance(args, dict) else None
    if not isinstance(raw, str) or not raw.strip():
        return None
    return " ".join(raw.split())


def exact_matches(projects: List[Any], name: str) -> List[ProjectRef]:
    """The projects whose whole stored name equals ``name``, case-insensitively, in
    the order given."""
    key = _key(name)
    if not key:
        return []
    return [
        ProjectRef(id=str(p.id), name=str(p.name))
        for p in projects or []
        if _key(getattr(p, "name", None)) == key
    ]


async def _active_projects(user_id: str) -> List[Any]:
    from services.database.repositories import ProjectRepository
    from services.database.session_factory import AsyncSessionFactory
    from services.onboarding.portfolio_service import PortfolioService

    async with AsyncSessionFactory.session_scope() as session:
        service = PortfolioService(ProjectRepository(session))
        return list(await service.list_active_projects(user_id=user_id))


async def _owned_active_project(project_id: str, user_id: str) -> Optional[ProjectRef]:
    """The project by id IF this person owns it and it is still active."""
    for project in await _active_projects(user_id):
        if str(project.id) == str(project_id):
            return ProjectRef(id=str(project.id), name=str(project.name))
    return None


async def resolve(intent: Any, user_id: Any) -> Optional[Resolution]:
    """``None`` when the router named no project (create_todo is unchanged);
    otherwise the exact matches among the person's own active projects."""
    name = router_project_name(intent)
    if name is None:
        return None
    matches = exact_matches(await _active_projects(str(user_id)), name)
    logger.info("todo_project_resolved", matches=len(matches))
    return Resolution(name=name, matches=matches)


def render_attached(titles: List[str], project_name: str) -> str:
    if len(titles) == 1:
        return ATTACHED_LINE.format(text=titles[0], project=project_name)
    names = [f"'{t}'" for t in titles]
    joined = ", ".join(names[:-1]) + " and " + names[-1]
    return ATTACHED_SEVERAL_LINE.format(count=len(titles), project=project_name, names=joined)


def render_several(names: List[str], purpose: str = PURPOSE_ADD) -> str:
    listed = " ".join(f"{i}. {n}" for i, n in enumerate(names, 1))
    template = READ_SEVERAL_QUESTION if purpose == PURPOSE_READ else SEVERAL_QUESTION
    return template.format(listed=listed)


def _decline_line(purpose: str) -> str:
    return READ_PICK_DECLINE_LINE if purpose == PURPOSE_READ else PICK_DECLINE_LINE


def build_pick_offer(
    principal: Optional[str],
    matches: List[ProjectRef],
    titles: List[str],
    priority: str,
    original_message: str,
    purpose: str = PURPOSE_ADD,
) -> Dict[str, Any]:
    """The #846 record: the matched projects (ids and names in the order the
    question numbers them) and the todo titles, all bound at ask time.
    ``purpose`` "read" (#2301) carries no titles: the number shows the project."""
    names = [m.name for m in matches]
    return {
        "workflow_type": TODO_PROJECT_PICK_WORKFLOW,
        "question": render_several(names, purpose),
        "pending_action": {
            "kind": TODO_PROJECT_PICK_KIND,
            "action": TODO_PROJECT_PICK_WORKFLOW,
            "user_id": principal,
            "pick_ids": [m.id for m in matches],
            "pick_names": names,
            "titles": list(titles),
            "priority": priority,
            "purpose": purpose,
            "original_message": original_message,
            "summary": (
                "pick which project to show"
                if purpose == PURPOSE_READ
                else "pick which project to add the todo to"
            ),
        },
        "decline_message": _decline_line(purpose),
    }


def arm_pick(
    intent_service: Any, record: Dict[str, Any], session_id: Optional[str], user_id: Optional[str]
) -> bool:
    """Arm the pick in the #846 one-slot store BEFORE the question is shown.
    False when there is no session or store: the caller must not show a question
    nothing will answer."""
    offer_service = getattr(intent_service, "workflow_offer_service", None)
    if not session_id or offer_service is None:
        logger.warning("todo_project_pick_not_armed", session_id=session_id)
        return False
    offer_service.set_pending_offer(session_id, record, user_id=user_id)
    logger.info("todo_project_pick_armed", session_id=session_id)
    return True


async def handle_todo_project_pick_turn(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> Optional[Dict[str, Any]]:
    """The ANSWER half, at the pop seam. A short answer naming one listed position
    writes the bound titles into the project bound BY ID at ask time, after
    re-checking the turn's own principal still owns it. Anything else returns
    ``None``: the generic seam handles a decline, a bare "yes" (the registered
    landing re-asks) or a new request (routes normally; the record is popped)."""
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != TODO_PROJECT_PICK_KIND:
        return None
    text = (message or "").strip()
    if not text:
        return None
    from services.intent_service.reminder_clear import _ordinal_index, _principal_mismatch

    intent_data = {"category": "execution", "action": TODO_PROJECT_PICK_WORKFLOW}
    if not user_id or _principal_mismatch(payload, user_id):
        logger.warning(
            "todo_project_pick_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": PRINCIPAL_MISMATCH_LINE,
            "intent_data": {**intent_data, "principal_mismatch": True},
        }
    ids = [str(i) for i in payload.get("pick_ids") or []]
    titles = [str(t) for t in payload.get("titles") or [] if str(t).strip()]
    reading = payload.get("purpose") == PURPOSE_READ
    if not ids or (not titles and not reading) or len(text.split()) > _MAX_ANSWER_WORDS:
        return None
    idx = _ordinal_index(text, len(ids))
    if idx is None:
        return None
    from services.intent.intent_service import _coerce_todo_principal

    todo_user = _coerce_todo_principal(user_id)
    if not todo_user:
        return {"message": PRINCIPAL_MISMATCH_LINE, "intent_data": intent_data}
    project = await _owned_active_project(ids[idx], str(todo_user))
    if project is None:
        return {
            "message": READ_PROJECT_GONE_LINE if reading else PROJECT_GONE_LINE,
            "intent_data": intent_data,
        }
    logger.info("todo_project_pick_bound", session_id=session_id, position=idx + 1, reading=reading)
    if reading:
        reply = await intent_service.todo_handlers.handle_list_project_todos(
            session_id, todo_user, project
        )
        return {"message": reply, "intent_data": {**intent_data, "action": LIST_PROJECT_TODOS_OP}}
    reply = await intent_service.todo_handlers.create_titles_in_project(
        titles, session_id, todo_user, str(payload.get("priority") or "medium"), project
    )
    return {"message": reply, "intent_data": {**intent_data, "action": "create_todo"}}


async def run_clarify_todo_project_pick_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing (registered ``clarify_todo_project_pick``,
    action_triggered=False): a bare "yes" names no project, so ask again with the
    same bound list and re-arm it. effect: READ (nothing is written)."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != TODO_PROJECT_PICK_KIND or intent_service is None:
        logger.error(
            "todo_project_pick_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    purpose = str(payload.get("purpose") or PURPOSE_ADD)
    question = render_several([str(n) for n in payload.get("pick_names") or []], purpose)
    record = {
        "workflow_type": TODO_PROJECT_PICK_WORKFLOW,
        "question": question,
        "pending_action": dict(payload),
        "decline_message": _decline_line(purpose),
    }
    intent_service.workflow_offer_service.set_pending_offer(session_id, record, user_id=user_id)
    return {
        "message": question,
        "intent_data": {
            "category": "execution",
            "action": TODO_PROJECT_PICK_WORKFLOW,
            PICK_PENDING_FLAG: True,
        },
        "requires_clarification": True,
    }
