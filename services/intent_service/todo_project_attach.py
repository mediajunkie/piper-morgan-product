"""#2297: a todo created with a named project is attached to that project.

Arch's ruling (decisions.log 2026-11-06 11:13, (A)) and CXO's words (11-06 11:14):

- WHICH project is meaning, and it is the router's: the ``project`` arg the router
  declares on ``create_todo`` (``context["inversion_args"]["project"]``). Code reads
  no project name out of the person's words (ADR-080); no pattern is written here.
- Code LOOKS that name UP among the person's own ACTIVE projects (Arch 11-20,
  mail 01M7XBJ38R). String comparison only, in two steps:
  1. the whole stored name equals it, ignoring case;
  2. only if step 1 matched nothing: one literal trailing word ``project`` is
     removed (the router copies it from "my Launch project") and step 1 runs again.
  Nothing else is stripped, and no step picks between candidates.
  - one: the todo is written with that project's id, and the reply names the
    STORED project, so a wrong match shows on the first reply;
  - several: nothing is written; an ARMED numbered pick (the #1987 shape, as
    #2271's archive pick), the project ids and the todo titles bound at ask time.
    A number answer writes the bound titles into the bound project at the pop
    seam (``handle_todo_project_pick_turn``);
  - none, with projects on the account: nothing is written; CXO's question that
    lists what exists (11-20, mail 01M7XAV6XH), ARMED with every active project
    and the titles bound. An answer that is one of those names, by the same
    lookup, writes at the pop seam;
  - none, and no projects at all: nothing is written; CXO's "Want it added
    without a project?", ARMED; a yes writes the bound titles with no project
    (``run_create_todo_without_project_workflow``);
  - the project read failed: nothing is written; CXO's couldn't-check line, which
    says neither "can't find" nor "no projects", since neither is known.
- A todo is never attached to a fuzzy guess, and a project is never created here.

No ``project`` arg: this module returns ``None`` and create_todo is unchanged.
"""

from __future__ import annotations

import string
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import structlog

# One rendering of a project's stored creation date for both picks (Arch 11-14).
from services.intent_service.project_archive_pick import created_label

logger = structlog.get_logger(__name__)

ROUTER_PROJECT_ARG = "project"

TODO_PROJECT_PICK_KIND = "todo_project_pick_question"
# The registered offer-only landing (action_triggered=False): a bare "yes" names
# no project, so it re-asks and re-arms.
TODO_PROJECT_PICK_WORKFLOW = "clarify_todo_project_pick"
# The yes/no asked when the account has no projects at all. Offer-acceptance only.
TODO_NO_PROJECT_KIND = "todo_no_project_confirm_question"
TODO_NO_PROJECT_WORKFLOW = "create_todo_without_project"
# How a which-project record is answered: by its number (several share the name)
# or by a listed name (none matched).
ANSWER_NUMBER = "number"
ANSWER_NAME = "name"
PICK_PENDING_FLAG = "todo_project_pick_pending"
# The result key the armed record rides from the resolver to the rail adapter.
OFFER_RECORD_KEY = "todo_project_offer"

# CXO 11-06 (verbatim).
ATTACHED_LINE = "I've added '{text}' to {project}."
# CXO 11-20 (mail 01M7XAV6XH, verbatim), by what is known when nothing matches.
# Each *_QUESTION is rendered only by its build_*_offer, which stores it as the
# record's ``question`` and arms the record (the #1766 rule).
NOT_FOUND_QUESTION = (
    "I can't find a project called \"{name}\", so I haven't added the todo yet. "
    "Your projects: {listed}. Which one did you mean?"
)
# More than MAX_LISTED projects: the first five, then this tail in place of the
# question. The record is armed the same way, with EVERY project bound.
NOT_FOUND_MANY_LINE = (
    "I can't find a project called \"{name}\", so I haven't added the todo yet. "
    "Your projects: {listed} …and {more} more. Tell me the name and I'll check."
)
MAX_LISTED = 5
NO_PROJECTS_QUESTION = (
    "I can't find a project called \"{name}\", and I don't see any projects on your "
    "account, so I haven't added the todo yet. Want it added without a project?"
)
# The read failed before any write. Must not say "can't find" or "no projects".
RESOLVE_FAILED_LINE = (
    "I couldn't check your projects just now, so I haven't added the todo. "
    "Try again in a moment."
)
# NOT YET RULED by CXO (in the build report): no store to hold the question, so
# no question is asked. Each is CXO's own line up to its first full stop.
NOT_FOUND_UNARMED_LINE = (
    "I can't find a project called \"{name}\", so I haven't added the todo yet."
)
NO_PROJECTS_UNARMED_LINE = (
    "I can't find a project called \"{name}\", and I don't see any projects on your "
    "account, so I haven't added the todo yet."
)
# Named *_QUESTION: rendered only by build_pick_offer / the re-ask landing, which
# store it as the record's ``question`` and arm the record (the #1766 rule).
# CXO 11-14 (pick-question mail, verbatim) on Arch's ruling 2 (11-14): the question
# shows the bound title(s) exactly as stored, so the number names both the project
# and a write the person has seen, and is the consent.
SEVERAL_QUESTION = (
    "I found more than one project with that name: {listed}. "
    "Which one should I add {titles} to? Say the number."
)
# CXO 11-14 (PASS): several titles into one project; the decline of the pick (the
# house decline sentence kept); a non-default priority the code stored is said,
# the default says nothing, and it is never inferred.
ATTACHED_PRIORITY_LINE = "I've added '{text}' to {project}, at {priority} priority."
ATTACHED_SEVERAL_LINE = "I've added {count} todos to {project}: {names}."
PICK_DECLINE_LINE = "Okay, I haven't added anything. Nothing has been changed."
PRINCIPAL_MISMATCH_LINE = "Let's hold off on that — nothing has been changed."
# CXO 11-14 (settled): no rename path exists today (Arch, from source) and the
# names differ at most in case, so the line stops here.
NOT_ARMED_LINE = "I found more than one project with that name, so I haven't added anything."
PROJECT_GONE_LINE = "I couldn't find that project anymore, so I haven't added anything."

# A pick answer is a short reply ("2", "the second one"); a longer message is a
# new request and routes normally.
_MAX_ANSWER_WORDS = 3


@dataclass(frozen=True)
class ProjectRef:
    """A resolved project: its id and its stored name (never the typed one).
    ``created`` is the stored creation date as ``3 Nov`` (the row's own
    ``created_at``, UTC as stored; never inferred), or "" when the row has none."""

    id: str
    name: str
    created: str = ""

    @property
    def label(self) -> str:
        """CXO 11-14: same-named projects in a pick show one stored difference,
        ``Launch (created 3 Nov)``."""
        return f"{self.name} (created {self.created})" if self.created else self.name


@dataclass(frozen=True)
class Resolution:
    """What the router's ``project`` arg resolved to among the person's own
    active projects. ``name`` is the arg as the router gave it."""

    name: str
    matches: List[ProjectRef] = field(default_factory=list)
    # Every active project the person has, in the order read: what a not-found
    # question lists and binds.
    projects: List[ProjectRef] = field(default_factory=list)

    @property
    def one(self) -> Optional[ProjectRef]:
        return self.matches[0] if len(self.matches) == 1 else None


def _key(name: Any) -> str:
    return " ".join(str(name or "").split()).casefold()


def _words(text: str) -> set:
    found = {w.strip(string.punctuation).lower() for w in (text or "").split()}
    found.discard("")
    return found


def router_project_name(intent: Any) -> Optional[str]:
    """The router's ``project`` arg, whitespace-collapsed, or ``None``.

    Arch 11-14 ruling 1 (the #1976 word-set guard, the ONE reader every caller
    uses): the arg counts as the person's only when every word of it occurs in
    their message. An arg with a word they did not say is NO arg: create_todo
    then runs exactly as it does without one, so a model-written name can neither
    stop a write the person asked for nor be shown to them. A non-string or empty
    value is no arg either. A word set, no pattern."""
    context = getattr(intent, "context", None) or {}
    args = context.get("inversion_args")
    raw = args.get(ROUTER_PROJECT_ARG) if isinstance(args, dict) else None
    if not isinstance(raw, str) or not raw.strip():
        return None
    name = " ".join(raw.split())
    message = getattr(intent, "original_message", None) or context.get("original_message") or ""
    wanted = _words(name)
    if not wanted or not wanted <= _words(message):
        logger.info("todo_project_arg_not_the_persons_words")
        return None
    return name


def exact_matches(projects: List[Any], name: str) -> List[ProjectRef]:
    """The projects whose whole stored name equals ``name``, case-insensitively, in
    the order given."""
    key = _key(name)
    if not key:
        return []
    return [
        ProjectRef(id=str(p.id), name=str(p.name), created=created_label(p))
        for p in projects or []
        if _key(getattr(p, "name", None)) == key
    ]


TRAILING_WORD = "project"


def without_trailing_project(name: str) -> Optional[str]:
    """``name`` with ONE literal trailing word ``project`` removed (a whole word at
    the end, ignoring case), or ``None`` when there is no such word or nothing
    would be left. The only suffix this module removes (Arch 11-20)."""
    words = str(name or "").split()
    if len(words) < 2 or words[-1].casefold() != TRAILING_WORD:
        return None
    return " ".join(words[:-1])


def lookup(projects: List[Any], name: str) -> List[ProjectRef]:
    """Arch 11-20: the name as given, exactly and ignoring case; only if that
    matches nothing, the same after one trailing ``project`` is removed. Returns
    every match of the step that matched. One is used; several are asked about;
    none is asked about. It never picks between candidates."""
    found = exact_matches(projects, name)
    if found:
        return found
    shorter = without_trailing_project(name)
    return exact_matches(projects, shorter) if shorter else []


def _refs(projects: List[Any]) -> List[ProjectRef]:
    return [
        ProjectRef(id=str(p.id), name=str(p.name), created=created_label(p)) for p in projects or []
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
            return ProjectRef(
                id=str(project.id), name=str(project.name), created=created_label(project)
            )
    return None


async def resolve(intent: Any, user_id: Any) -> Optional[Resolution]:
    """``None`` when the router named no project (create_todo is unchanged);
    otherwise the lookup's matches among the person's own active projects, with
    all of those projects. A failed read RAISES; the caller says the
    couldn't-check line."""
    name = router_project_name(intent)
    if name is None:
        return None
    projects = await _active_projects(str(user_id))
    matches = lookup(projects, name)
    logger.info("todo_project_resolved", matches=len(matches), projects=len(projects))
    return Resolution(name=name, matches=matches, projects=_refs(projects))


def _quoted(titles: List[str]) -> str:
    """``'a'``, ``'a' and 'b'``, ``'a', 'b' and 'c'``: each title as stored, in
    straight single quotes (CXO 11-14)."""
    names = [f"'{t}'" for t in titles]
    if len(names) <= 1:
        return "".join(names)
    return ", ".join(names[:-1]) + " and " + names[-1]


def render_attached(titles: List[str], project_name: str, priority: Optional[str] = None) -> str:
    if len(titles) == 1:
        if priority and priority != "medium":
            return ATTACHED_PRIORITY_LINE.format(
                text=titles[0], project=project_name, priority=priority
            )
        return ATTACHED_LINE.format(text=titles[0], project=project_name)
    return ATTACHED_SEVERAL_LINE.format(
        count=len(titles), project=project_name, names=_quoted(titles)
    )


def render_several(labels: List[str], titles: Optional[List[str]] = None) -> str:
    """The pick question. ``labels`` are the numbered lines as shown (name, with
    the stored created date when there is one). ``titles`` are the bound titles,
    shown exactly as stored (Arch 11-14 ruling 2)."""
    listed = " ".join(f"{i}. {n}" for i, n in enumerate(labels, 1))
    return SEVERAL_QUESTION.format(listed=listed, titles=_quoted(list(titles or [])))


def render_not_found(name: str, labels: List[str]) -> str:
    """CXO 11-20: the question that names what exists. Up to five are listed with
    the question; past five, the first five and the "…and N more" tail."""
    if len(labels) > MAX_LISTED:
        return NOT_FOUND_MANY_LINE.format(
            name=name, listed=", ".join(labels[:MAX_LISTED]), more=len(labels) - MAX_LISTED
        )
    return NOT_FOUND_QUESTION.format(name=name, listed=", ".join(labels))


def _pick_record(
    question: str,
    answer: str,
    principal: Optional[str],
    projects: List[ProjectRef],
    titles: List[str],
    priority: str,
    original_message: str,
) -> Dict[str, Any]:
    names = [m.name for m in projects]
    return {
        "workflow_type": TODO_PROJECT_PICK_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": TODO_PROJECT_PICK_KIND,
            "action": TODO_PROJECT_PICK_WORKFLOW,
            "answer": answer,
            "user_id": principal,
            "pick_ids": [m.id for m in projects],
            "pick_names": names,
            # The lines exactly as shown, so the re-ask is the same text.
            "pick_labels": [m.label for m in projects],
            "pick_created": [m.created for m in projects],
            # The question as asked; a bare "yes" re-asks exactly this.
            "question": question,
            "titles": list(titles),
            "priority": priority,
            "original_message": original_message,
            "summary": "pick which project to add the todo to",
        },
        "decline_message": PICK_DECLINE_LINE,
    }


def build_pick_offer(
    principal: Optional[str],
    matches: List[ProjectRef],
    titles: List[str],
    priority: str,
    original_message: str,
) -> Dict[str, Any]:
    """The #846 record for SEVERAL matches: the matched projects (ids and names in
    the order the question numbers them) and the todo titles, all bound at ask
    time. Answered by number."""
    question = render_several([m.label for m in matches], titles)
    return _pick_record(
        question, ANSWER_NUMBER, principal, matches, titles, priority, original_message
    )


def build_not_found_offer(
    principal: Optional[str],
    name: str,
    projects: List[ProjectRef],
    titles: List[str],
    priority: str,
    original_message: str,
) -> Dict[str, Any]:
    """The #846 record for NO match on an account that has projects: EVERY active
    project (not only the five listed) and the todo titles, bound at ask time.
    Answered by a listed name, looked up as the first name was."""
    question = render_not_found(name, [m.name for m in projects])
    return _pick_record(
        question, ANSWER_NAME, principal, projects, titles, priority, original_message
    )


def build_no_projects_offer(
    principal: Optional[str], name: str, titles: List[str], priority: str, original_message: str
) -> Dict[str, Any]:
    """The #846 record for an account with NO projects: the titles bound at ask
    time. A yes writes them with no project; a no writes nothing."""
    question = NO_PROJECTS_QUESTION.format(name=name)
    return {
        "workflow_type": TODO_NO_PROJECT_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": TODO_NO_PROJECT_KIND,
            "action": TODO_NO_PROJECT_WORKFLOW,
            "user_id": principal,
            "titles": list(titles),
            "priority": priority,
            "original_message": original_message,
            "summary": "add the todo without a project",
        },
        "decline_message": PICK_DECLINE_LINE,
    }


_ANSWER_EDGE = " \t\n.!?\"'“”‘’"


def _named_positions(names: List[str], text: str) -> List[int]:
    """The positions in ``names`` the answer names, by the lookup's two steps. The
    answer is tried as typed, then without sentence punctuation or quotes at its
    edges. Never a partial or fuzzy match."""
    stubs = [ProjectRef(id=str(i), name=n) for i, n in enumerate(names)]
    for candidate in (text, text.strip(_ANSWER_EDGE)):
        found = lookup(stubs, candidate)
        if found:
            return [int(m.id) for m in found]
    return []


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
    if not ids or not titles:
        return None
    if payload.get("answer") == ANSWER_NAME:
        # The not-found question: the answer is one of the names bound at ask time.
        names = [str(n) for n in payload.get("pick_names") or []]
        positions = _named_positions(names, text) if len(names) == len(ids) else []
        if not positions:
            return None
        if len(positions) > 1:
            # Two bound projects carry that name: the numbered pick, same titles.
            created = [str(c) for c in payload.get("pick_created") or []]
            matches = [
                ProjectRef(id=ids[i], name=names[i], created=created[i] if i < len(created) else "")
                for i in positions
            ]
            record = build_pick_offer(
                str(user_id),
                matches,
                titles,
                str(payload.get("priority") or "medium"),
                str(payload.get("original_message") or ""),
            )
            if not arm_pick(intent_service, record, session_id, user_id):
                return {"message": NOT_ARMED_LINE, "intent_data": intent_data}
            return {
                "message": record["question"],
                "intent_data": {**intent_data, PICK_PENDING_FLAG: True},
                "requires_clarification": True,
            }
        idx = positions[0]
    else:
        if len(text.split()) > _MAX_ANSWER_WORDS:
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
        return {"message": PROJECT_GONE_LINE, "intent_data": intent_data}
    logger.info("todo_project_pick_bound", session_id=session_id, position=idx + 1)
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
    question = str(payload.get("question") or "") or render_several(
        [str(n) for n in payload.get("pick_labels") or payload.get("pick_names") or []],
        [str(t) for t in payload.get("titles") or []],
    )
    record = {
        "workflow_type": TODO_PROJECT_PICK_WORKFLOW,
        "question": question,
        "pending_action": dict(payload),
        "decline_message": PICK_DECLINE_LINE,
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


async def run_create_todo_without_project_workflow(
    session_id: str,
    user_id: Optional[str] = None,
    context: Optional[Dict[str, Any]] = None,
) -> Any:
    """Generic-accept landing (registered ``create_todo_without_project``,
    action_triggered=False): the "yes" to "Want it added without a project?" writes
    exactly the titles bound at ask time, with no project, under the turn's own
    principal. effect: WRITE."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    titles = [str(t) for t in payload.get("titles") or [] if str(t).strip()]
    if payload.get("kind") != TODO_NO_PROJECT_KIND or intent_service is None or not titles:
        logger.error(
            "todo_no_project_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
            titles=len(titles),
        )
        return None
    from services.intent_service.reminder_clear import _principal_mismatch

    intent_data = {"category": "execution", "action": "create_todo"}
    if not user_id or _principal_mismatch(payload, user_id):
        logger.warning(
            "todo_no_project_principal_mismatch",
            offer_user=payload.get("user_id"),
            turn_user=user_id,
        )
        return {
            "message": PRINCIPAL_MISMATCH_LINE,
            "intent_data": {**intent_data, "principal_mismatch": True},
            "requires_clarification": False,
        }
    from services.intent.intent_service import _coerce_todo_principal

    todo_user = _coerce_todo_principal(user_id)
    if not todo_user:
        return {
            "message": PRINCIPAL_MISMATCH_LINE,
            "intent_data": intent_data,
            "requires_clarification": False,
        }
    reply = await intent_service.todo_handlers.create_titles_without_project(
        titles, session_id, todo_user, str(payload.get("priority") or "medium")
    )
    return {"message": reply, "intent_data": intent_data, "requires_clarification": False}
