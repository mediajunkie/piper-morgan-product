"""#2304: every write's yes/no names the thing it would change, in CXO's words.

CXO 11-06 11:28 (the body of #2304): the question says what "yes" does, with the
thing named, in the shape of the ordinary confirms. If the arguments cannot name
it, no write question is asked and nothing is armed; the reply is
``NOT_SURE_STATEMENT``. An op name is never shown to a person.

Arch 11-06 11:38: the per-op words live ON THE RAIL ENTRY
(``WorkflowEntry.write_ask``), and both askers read them: the #1509 consent check
(``consent_gate.build_consent_check_offer``) and the #1190 generic confirm
(``destructive_confirm.build_confirmation_offer``). ``resolve_write_ask`` is the one
reader; an entry with no ``write_ask``, or one whose args name nothing, gets the
statement. The DESTRUCTIVE entries with their own resolve-before-arming builders
(delete_todo, unlink_repo, close/reopen) keep them; the rail never asks those
entries here.

Each builder fills its line ONLY from what that op's own handler would act on:
the intent's context slots, the router's args read through the handler's own
arg reader, or the handler's own named resolver function. No new pattern is
written for a question. An op whose handler finds its target with an LLM call or
with a pattern written inline in the handler (update_document, comment_issue,
link_repo, set_default_repo, set_timezone) has nothing the question can read
before "yes", so it gets the statement; its row is listed in #2304's report.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Dict, Optional

import structlog

logger = structlog.get_logger(__name__)

# CXO 11-06 (verbatim). A statement: nothing is armed (the #1730 ratchet).
NOT_SURE_STATEMENT = (
    "I'm not sure what you want changed, so I haven't done anything. Tell me what to change."
)

# CXO 11-06 11:28 (verbatim): add_project with no name. Armed through the #2080
# add-project name carrier (consent_owed), so the answer is bound as the name and
# the named turn arms the one "Add a project called …?" confirm. No write is armed.
ADD_PROJECT_NAME_QUESTION = (
    'What should I call the project? Say its name, for example "add project Mobile Redesign".'
)


@dataclass(frozen=True)
class ConfirmWords:
    """A filled question and its decline summary (``Okay — I won't {summary}. …``)."""

    question: str
    summary: str


@dataclass(frozen=True)
class WriteAskRequest:
    """What a builder may read. ``message`` is the text the rail's gates read (the
    sibling's own segment on the multi-intent path)."""

    intent: Any
    message: str
    intent_service: Any = None
    principal: Optional[str] = None
    session_id: Optional[str] = None
    user_id: Optional[str] = None


@dataclass(frozen=True)
class WriteAsk:
    """Exactly one of: ``words`` (arm this question through the caller's carrier);
    ``reply`` (say this; ``armed`` when the builder armed a carrier itself);
    ``passthrough`` (dispatch the op, which asks or declines on its own)."""

    words: Optional[ConfirmWords] = None
    reply: Optional[str] = None
    armed: bool = False
    intent_data: Optional[Dict[str, Any]] = None
    passthrough: bool = False


WriteAskBuilder = Callable[[WriteAskRequest], Awaitable[WriteAsk]]


async def resolve_write_ask(entry: Any, request: WriteAskRequest) -> WriteAsk:
    """The entry's ask, or the "not sure" statement when nothing is named."""
    builder = getattr(entry, "write_ask", None)
    ask = await builder(request) if builder is not None else WriteAsk()
    if ask.words is None and ask.reply is None and not ask.passthrough:
        logger.info("write_ask_names_nothing", action=getattr(request.intent, "action", None))
        return WriteAsk(reply=NOT_SURE_STATEMENT)
    return ask


def _original(intent: Any) -> str:
    return (
        (getattr(intent, "context", None) or {}).get("original_message")
        or getattr(intent, "original_message", None)
        or ""
    )


def _context(intent: Any) -> Dict[str, Any]:
    return getattr(intent, "context", None) or {}


def _text(value: Any) -> Optional[str]:
    if isinstance(value, str) and value.strip():
        return " ".join(value.split())
    return None


# ---------------------------------------------------------------------------
# Binding (Arch 11-06 13:23): what the question shows is what "yes" writes
# ---------------------------------------------------------------------------

# The armed record carries the original Intent (#1190); the values a builder named
# ride its context under this key, tagged with the op, and that op's handler writes
# them on the confirmed turn instead of extracting again (#1665: what was asked is
# what is stored, and what is stored is what is written).
WRITE_ASK_BOUND_KEY = "write_ask_bound"


def bind_write_values(intent: Any, op: str, **values: Any) -> None:
    """Bind the named values into the intent the offer will carry (copy-on-write)."""
    intent.context = dict(intent.context or {})
    intent.context[WRITE_ASK_BOUND_KEY] = {"op": op, **values}


def bound_write_values(intent: Any, op: str) -> Dict[str, Any]:
    """The values bound for ``op`` at ask time, or {} (never another op's)."""
    bound = (getattr(intent, "context", None) or {}).get(WRITE_ASK_BOUND_KEY)
    if isinstance(bound, dict) and bound.get("op") == op:
        return bound
    return {}


# ---------------------------------------------------------------------------
# The per-op builders (registered on the entries in workflow_entries.py)
# ---------------------------------------------------------------------------


async def create_todo_write_ask(request: WriteAskRequest) -> WriteAsk:
    """``Add "x" to your todos?`` from handle_create_todo's own resolver chain: the
    router's items / text (its honesty-guarded readers), else its extractor.
    Several router items have no CXO row, and no project arg exists yet (#2297),
    so neither is worded here."""
    from services.intent_service.todo_handlers import TodoIntentHandlers

    intent = request.intent
    message = _original(intent)
    items = TodoIntentHandlers._router_todo_items(intent, message)
    if len(items) >= 2:
        return WriteAsk()
    text = (items[0] if items else "") or TodoIntentHandlers._router_todo_text(intent, message)
    handlers = getattr(request.intent_service, "todo_handlers", None)
    if not text and handlers is not None:
        text = TodoIntentHandlers._strip_leading_to(handlers._extract_todo_text(message))
    named = _text(text)
    if not named:
        return WriteAsk()
    bind_write_values(intent, "create_todo", text=named)
    return WriteAsk(
        words=ConfirmWords(
            question=f'Add "{named}" to your todos? (yes/no)',
            summary=f'add "{named}" to your todos',
        )
    )


async def create_reminder_write_ask(request: WriteAskRequest) -> WriteAsk:
    """``Set a reminder "x" for {when}?`` from handle_create_reminder's own text
    extractor and time parser, on the person's clock as the handler reads it.
    No time said (the handler family's ``_has_time_signal``), or a time the parser
    can't bind: nothing named."""
    from services.intent_service.temporal_utils import parse_reminder_time
    from services.intent_service.todo_handlers import _has_time_signal

    handlers = getattr(request.intent_service, "todo_handlers", None)
    message = _original(request.intent)
    if handlers is None or not message or not _has_time_signal(message):
        return WriteAsk()
    text = _text(handlers._extract_reminder_text(message))
    if not text:
        return WriteAsk()
    user_tz = None
    if request.principal:
        try:
            from services.intent.intent_service import _coerce_todo_principal
            from services.utils.user_timezone import get_user_timezone

            todo_user = _coerce_todo_principal(request.principal)
            if todo_user is not None:
                user_tz = await get_user_timezone(todo_user)
        except Exception as e:  # silent-ok: logged; the label falls back to the server clock
            logger.warning("write_ask_reminder_timezone_failed", error=str(e))
    when_dt, when = parse_reminder_time(message, user_timezone=user_tz)
    if when_dt is None or not when:
        return WriteAsk()
    bind_write_values(
        request.intent, "create_reminder", text=text, when=when, when_at=when_dt.isoformat()
    )
    return WriteAsk(
        words=ConfirmWords(
            question=f'Set a reminder "{text}" for {when}? (yes/no)',
            summary=f'set a reminder "{text}" for {when}',
        )
    )


def _project_write_ask(operation: str, question: str, summary: str) -> WriteAskBuilder:
    """archive / restore: the existing wording (ADOPTED_WRITE_CONFIRM_QUESTIONS),
    named by ``display_name_for`` (#2070: the handler's own resolver)."""

    async def _ask(request: WriteAskRequest) -> WriteAsk:
        from services.intent_service.adopted_category_reads_only import display_name_for

        name = display_name_for(
            operation, _original(request.intent), _context(request.intent).get("inversion_args")
        )
        if not name:
            return WriteAsk()
        bind_write_values(request.intent, f"{operation}_project", name=name)
        return WriteAsk(
            words=ConfirmWords(
                question=question.format(name=name), summary=summary.format(name=name)
            )
        )

    _ask.__name__ = f"{operation}_project_write_ask"
    return _ask


archive_project_write_ask = _project_write_ask(
    "archive", 'Archive the project "{name}"? (yes/no)', 'archive the project "{name}"'
)
restore_project_write_ask = _project_write_ask(
    "restore", 'Restore the project "{name}"? (yes/no)', 'restore the project "{name}"'
)


async def add_project_write_ask(request: WriteAskRequest) -> WriteAsk:
    """``Add a project called "X"?`` named by the add handler's own resolver
    (``resolve_add_project_slots`` via ``display_name_for``, #2069). No name: CXO's
    name question, armed on the #2080 name carrier with ``consent_owed`` (#2082),
    so a "yes" can never run an add with no name."""
    from services.intent_service.adopted_category_reads_only import display_name_for

    intent = request.intent
    message = _original(intent) or request.message
    name = display_name_for("add", message, _context(intent).get("inversion_args"))
    if name:
        bind_write_values(intent, "add_project", name=name)
        return WriteAsk(
            words=ConfirmWords(
                question=f'Add a project called "{name}"? (yes/no)',
                summary=f'add a project called "{name}"',
            )
        )
    offers = getattr(request.intent_service, "workflow_offer_service", None)
    if offers is None or not request.session_id:
        return WriteAsk()  # nowhere to bind the answer: the statement, nothing armed
    from services.intent_service.add_project_clarify import build_add_project_name_offer

    offers.set_pending_offer(
        request.session_id,
        build_add_project_name_offer(
            message, request.user_id, question=ADD_PROJECT_NAME_QUESTION, consent_owed=True
        ),
        user_id=request.user_id,
    )
    logger.info("add_project_name_asked_before_consent", session_id=request.session_id)
    return WriteAsk(
        reply=ADD_PROJECT_NAME_QUESTION,
        armed=True,
        intent_data={
            "action": "add_project_needs_name",
            "add_project_name_question_pending": True,
            "consent_owed": True,
        },
    )


async def create_issue_write_ask(request: WriteAskRequest) -> WriteAsk:
    """``Create an issue titled "x" in owner/repo?`` from the handler's own slots:
    the intent's ``title`` / ``repository``, else ``_slotfill_issue_request``. A repo
    the handler would only find by lookup (the default) is not named here."""
    from services.intent.intent_service import IntentService

    intent = request.intent
    ctx = _context(intent)
    slots = IntentService._slotfill_issue_request(_original(intent))
    title = _text(ctx.get("title")) or _text(slots.get("title"))
    repository = _text(ctx.get("repository")) or _text(slots.get("repository"))
    if not title or not repository:
        return WriteAsk()
    from services.intent_service.repo_clarification import strip_repo_phrase_for

    # The handler's own last step on the title (#1543): a trailing phrase naming
    # the target repo is routing, not subject. Shown and bound after it.
    title = _text(strip_repo_phrase_for(title, repository))
    if not title:
        return WriteAsk()
    bind_write_values(intent, "create_issue", title=title, repository=repository)
    return WriteAsk(
        words=ConfirmWords(
            question=f'Create an issue titled "{title}" in {repository}? (yes/no)',
            summary=f'create an issue titled "{title}" in {repository}',
        )
    )


# update_issue's fields: the handler's own reads (context, then slot-fill), and how
# each is said.
_UPDATE_ISSUE_FIELDS = (
    ("title", "the title"),
    ("body", "the description"),
    ("state", "the state"),
    ("labels", "the labels"),
    ("assignees", "the assignees"),
)


async def update_issue_write_ask(request: WriteAskRequest) -> WriteAsk:
    """``Change {the field} of issue #N in owner/repo?`` from _handle_update_issue's
    own reads: the intent's slots, ``_slotfill_issue_request``, and the #1190 issue
    number parse the handlers share. No field said: nothing named. The number, the
    repo and every field's value are bound; the handler writes exactly those."""
    from services.intent.intent_service import IntentService
    from services.intent_service.destructive_confirm import _issue_number_from

    intent = request.intent
    ctx = _context(intent)
    slots = IntentService._slotfill_issue_request(_original(intent))
    number = ctx.get("issue_number") or _issue_number_from(intent)
    repository = (
        _text(ctx.get("repository")) or _text(ctx.get("repo")) or _text(slots.get("repository"))
    )
    values = {
        "title": ctx.get("title") or slots.get("title"),
        "body": ctx.get("body") or ctx.get("description") or slots.get("body"),
        "state": ctx.get("state"),
        "labels": ctx.get("labels"),
        "assignees": ctx.get("assignees"),
    }
    fields = [said for key, said in _UPDATE_ISSUE_FIELDS if values[key]]
    if not number or not repository or not fields:
        return WriteAsk()
    bind_write_values(intent, "update_issue", issue_number=number, repository=repository, **values)
    changed = " and ".join(fields)
    return WriteAsk(
        words=ConfirmWords(
            question=f"Change {changed} of issue #{number} in {repository}? (yes/no)",
            summary=f"change {changed} of issue #{number} in {repository}",
        )
    )
