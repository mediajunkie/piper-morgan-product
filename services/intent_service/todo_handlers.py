"""
Todo Intent Handlers - Natural language interface for todo operations

Issue #285: CORE-ALPHA-TODO-INCOMPLETE
Wires chat commands to TodoManagementService, reusing request models from
services/api/todo_management.py (PM-081). NOTE (#1427): that module's REST
surface is UNMOUNTED (it was mocked end-to-end); chat — this file — and the
Lists API are the live todos surfaces. The live /api/v1/todos REST routes are
web/api/routes/todos.py (a different module).

Enhanced with consciousness injection (#407 MUX-VISION-STANDUP-EXTRACT)
for more alive, present-feeling responses.

Issue #904: CANONICAL-TODO-COMPLETE — Added fuzzy text matching for
completion ("complete the PR review" matches "Review the PR for auth").

Example commands:
- "add todo: Review PR #285"
- "show my todos"
- "show all my todos" (includes completed)
- "mark todo 1 as complete"
- "complete the PR review todo"
- "delete todo about meeting"
"""

import re
from typing import List, Optional, Tuple
from uuid import UUID

import structlog
from sqlalchemy.exc import SQLAlchemyError

from services.api.todo_management import TodoCreateRequest, TodoUpdateRequest
from services.consciousness.todo_consciousness import (
    format_next_todo_conscious,
    format_todo_completed_conscious,
    format_todo_created_conscious,
    format_todo_deleted_conscious,
    format_todo_list_conscious,
)
from services.domain.models import Intent, Todo
from services.intent_service.temporal_utils import DURATION_NUMBER_SRC
from services.todo.todo_management_service import TodoManagementService

logger = structlog.get_logger()

# Words that don't contribute to meaningful matching
_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "in",
        "on",
        "at",
        "to",
        "for",
        "of",
        "with",
        "and",
        "or",
        "but",
        "is",
        "it",
        "my",
        "your",
        "this",
        "that",
        "i",
        "me",
        "we",
        "do",
        "did",
        "has",
        "have",
        "had",
        "be",
        "been",
        "todo",
        "task",
        "item",
        "thing",
    }
)

# Minimum fuzzy match score to consider a match
_FUZZY_MATCH_THRESHOLD = 0.3


# --- #1648: the reminder time-clarify carrier -------------------------------
#
# Instance 2 of the #1648 fabrication incident: handle_create_reminder's
# honest time-clarify ask ("When should I remind you?") returned a bare
# question with NOTHING armed — so the answer turn ("at 3pm") had nothing to
# bind to, traversed the whole routing chain as an orphan, and landed on the
# floor, which roleplayed the save ("Reminder set for 3pm today", no 📅
# line, no row). The fix is the #1190/#846 deferred-action carrier shape the
# drafted-issue flow uses: the clarify ask ARMS a pending offer (kind
# ``reminder_time_question``) binding the task text; the next turn's time
# answer is consumed at the offer seam — before any classification surface —
# and the REAL save runs (the 📅 confirmation is composed from the actual
# row write, never improvised). A turn that answers with no parseable time
# RE-ASKS honestly and RE-ARMS; a full reminder restatement or an unrelated
# command abandons via the pop and routes normally, per the carrier's rules.

REMINDER_TIME_QUESTION_KIND = "reminder_time_question"

# Generic-accept landing (a bare "yes" doesn't answer "when?") — registered
# action_triggered=False in workflow_entries, the #1605 clarify precedent.
CLARIFY_REMINDER_TIME_WORKFLOW = "clarify_reminder_time"

# A full reminder restatement ("remind me to X at 3pm") carries its own task
# AND time — it must route normally (the pre-classifier claims it
# deterministically) so the full handler re-extracts both, rather than this
# seam saving the OLD task text under the new time. Mirrors
# PreClassifier.REMINDER_PATTERNS.
_REMINDER_RESTATEMENT_RE = re.compile(
    r"\b(?:remind\s+me\s+(?:to|about)\b|set\s+(?:a\s+)?reminder\b|"
    r"create\s+(?:a\s+)?reminder\b|don'?t\s+let\s+me\s+forget\b|"
    r"need\s+to\s+remember\s+to\b)",
    re.IGNORECASE,
)

_TIME_SIGNAL_RE = None  # compiled lazily — needs TodoIntentHandlers._TIME_EXPR


def _has_time_signal(message: str) -> bool:
    """Does the turn carry any time expression parse_reminder_time could
    bind? Uses the class's _TIME_EXPR (kept mirrored with the parser) plus
    the bare day words the parser handles honestly ("today" → ask-shaped
    when unbindable, never a silent default). Without this gate, an
    arbitrary answer would fall into the parser's tomorrow-morning DEFAULT
    and save a time the user never said (#1490's silent-default class)."""
    global _TIME_SIGNAL_RE
    if _TIME_SIGNAL_RE is None:
        _TIME_SIGNAL_RE = re.compile(
            rf"(?:{TodoIntentHandlers._TIME_EXPR})|\btoday\b|\btonight\b",
            re.IGNORECASE,
        )
    return bool(_TIME_SIGNAL_RE.search(message))


def _reminder_saved_message(text: str, reminder_dt, time_label: str) -> str:
    """The one true save confirmation (📅 line included) — composed only
    beside an actual row write. Factored from handle_create_reminder so the
    #1648 time-answer seam and the primary path share one copy source."""
    time_display = time_label
    if reminder_dt:
        # PM live 2026-08-15: this rendered a UTC instant with no label
        # ("Saturday at 11:42 PM" for a 4:42 PM PT save) — the #1542/#1589
        # unlabeled-clock-face shape. Until #1572 supplies the user's real
        # tz, every clock face we print is UTC and must SAY so (the
        # reminders list already does).
        time_display = reminder_dt.strftime("%A, %B %-d at %-I:%M %p UTC")

    # #1562: labels from the bare-clock branch start with "at" ("at 5pm") —
    # strip a LEADING "at" so the copy never reads "(scheduled for at 5pm)".
    # Same doublet family as #1490's "tomorrow at at 3pm".
    schedule_label = re.sub(r"^at\s+", "", time_label)

    # Issue #1096 slice 2 (Pattern-073 discipline): verification-bounded
    # phrasing — surfaced "in conversation", the mechanism we actually have.
    # #1569: reminders ARE todos in storage (unified model, PM-ratified) —
    # the closing sentence TEACHES that relationship.
    return (
        f"Reminder saved: **{text}** "
        f"(scheduled for {schedule_label}).\n\n"
        f"📅 {time_display}\n\n"
        f"It lives with your todos (you'll see it on the Todos page) "
        f"and I'll surface it in conversation once it's due."
    )


def build_reminder_time_offer(task_text: str, user_id, question=None) -> dict:
    """The #846 pending-offer record arming the time question (the generic
    deferred-action carrier shape documented in destructive_confirm.py).

    ``question`` (#1665): the ALREADY-RENDERED "when?" ask the caller returns
    this turn — stored verbatim, never re-rendered, so the SessionSnapshot's
    pending_offer_question matches what the user saw. An open question, NOT
    a yes/no (pinned outside the #1664 confirm-kind set)."""
    return {
        "workflow_type": CLARIFY_REMINDER_TIME_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": REMINDER_TIME_QUESTION_KIND,
            "action": "create_reminder",
            "task_text": task_text,
            "user_id": str(user_id) if user_id else None,
            "summary": f'set a reminder for "{task_text}"',
        },
        "decline_message": (
            "Okay — I haven't set that reminder. Nothing was saved."
        ),
    }


class TodoIntentHandlers:
    """
    Chat integration for todo operations.
    Wires natural language commands to TodoManagementService for persistence.
    """

    def __init__(self):
        """Initialize with TodoManagementService."""
        self.todo_service = TodoManagementService()

    async def get_due_reminders(self, user_id: UUID) -> Optional[List[str]]:
        """
        Issue #903: Get reminders that are due now or overdue.

        Returns a list of reminder text strings for surfacing at greeting time.
        Queries todos where reminder_date <= now and status != completed.

        Issue #1491: both sides of the due-ness comparison are normalized to
        aware-UTC (the #1429 standup guard shape). reminder_date comes back
        tz-aware from Postgres timestamptz but tz-naive from backends that
        drop tzinfo (e.g. SQLite in tests); the old naive `datetime.now()`
        against an aware row raised TypeError, which the swallow below turned
        into the None sentinel — so saved reminders never surfaced (live on
        v30, 2026-08-07). Naive rows are assumed UTC per ensure_utc().
        """
        from datetime import datetime, timezone

        from services.utils.datetime_utils import ensure_utc

        todo_count: Optional[int] = None
        reminders_considered = 0
        try:
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)
            todo_count = len(todos)
            now = datetime.now(timezone.utc)
            due = []
            for todo in todos:
                reminder_date = getattr(todo, "reminder_date", None)
                if reminder_date is None or todo.completed:
                    continue
                reminders_considered += 1
                # #1491/#1429 guard: coerce the row aware-UTC before comparing.
                if ensure_utc(reminder_date) <= now:
                    due.append(todo.text)
            return due
        except Exception as e:  # silent-ok: logged at error w/ exc_info; None sentinel -> assembler flags source_failed instead of "no reminders due" (#1425)
            # #1491/#1423: error-level, never warning-swallow — this failure
            # hid the v30 TypeError for days because warnings don't surface.
            logger.error(
                "Failed to fetch due reminders (source failed)",
                error=str(e),
                todo_count=todo_count,
                reminders_considered=reminders_considered,
                exc_info=True,
            )
            return None

    async def handle_create_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """
        Handle: "add todo: Review PR #285"
        Extract text, create todo with database persistence, format response.
        """
        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")

        text = self._extract_todo_text(original_message)
        if not text:
            return "I didn't catch what you'd like me to add. Could you try: 'add todo: [description]'?"

        # Parse optional priority
        priority = self._extract_priority(original_message)

        try:
            # Create todo via service (database persistence)
            todo = await self.todo_service.create_todo(
                user_id=user_id, text=text, priority=priority
            )

            logger.info(
                "Todo created successfully",
                todo_id=str(todo.id),
                text=text,
                priority=priority,
                user_id=user_id,
            )

            # Format response with consciousness
            return format_todo_created_conscious(todo)

        except ValueError as e:
            logger.warning("Todo creation validation failed", error=str(e), user_id=user_id)
            return f"I had trouble with that: {str(e)}"

        # #1423: narrowed from `except Exception` — expected failures here are DB-layer
        # (unreachable/timeout/constraint), which SQLAlchemyError covers. Anything else
        # (a formatting bug, an attribute error) is a CODE bug and now propagates to the
        # route's degradation boundary instead of masquerading as "a temporary issue".
        except (SQLAlchemyError, OSError) as e:
            logger.error("Todo creation failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble saving that todo — it may be a temporary issue. You can try again, or rephrase with 'add todo: [your task]'."

    def _arm_time_question(
        self, intent_service, session_id: str, user_id, task_text: str,
        question: Optional[str] = None,
    ) -> None:
        """#1648: arm the reminder time-clarify carrier beside the honest
        ask, so the answer turn binds at the offer seam instead of orphaning
        into the routing chain (where the floor roleplayed the save live).
        Best-effort: a store failure is logged and the ask still goes out —
        the copy never claims anything was armed. ``question`` (#1665): the
        rendered ask the caller is about to return, stored on the record."""
        if intent_service is None or not session_id:
            return
        try:
            intent_service.workflow_offer_service.set_pending_offer(
                session_id,
                build_reminder_time_offer(task_text, user_id, question=question),
                user_id=str(user_id) if user_id else None,
            )
        except Exception as e:  # silent-ok: #1648 — arming is additive; the honest ask must go out regardless; logged ERROR
            logger.error(
                "reminder_time_question_arm_failed",
                error=str(e),
                session_id=session_id,
            )

    async def handle_create_reminder(
        self,
        intent: Intent,
        session_id: str,
        user_id: UUID,
        intent_service=None,
    ) -> str:
        """
        Issue #903: Handle "remind me to X" — creates a time-annotated todo.

        Extracts the reminder text and time from the message, creates a todo
        with reminder_date set, and confirms with the parsed time.

        #1648: ``intent_service`` (optional, back-compat default None) lets
        the time-clarify asks arm the ``reminder_time_question`` carrier so
        the answer turn binds at the offer seam. Callers without it still
        get the honest ask — just without the binding.
        """
        from services.intent_service.temporal_utils import (
            PAST_TODAY_PREFIX,
            parse_reminder_time,
        )

        original_message = intent.original_message or intent.context.get("original_message", "")

        # Extract reminder text (strip "remind me to/about", "set a reminder to", etc.)
        text = self._extract_reminder_text(original_message)
        if not text:
            return (
                "I didn't catch what you'd like to be reminded about. "
                "Try: 'remind me to review PRs tomorrow' or "
                "'remind me to check in with the team in 2 hours'."
            )

        # Parse time from message
        reminder_dt, time_label = parse_reminder_time(original_message)

        # Issue #1490 invariant: parse_reminder_time returns None ONLY when
        # the message carried an explicit clock time it couldn't bind (e.g.
        # "at 25:99"). Never save with a silently-guessed default — echo the
        # unparsed time honestly and ask.
        # (RESTORED 2026-08-08: reverted by the arch-seat merge-drop incident,
        # d99b3d068/d5ae5484f — second casualty after the audit doc.)
        if reminder_dt is None:
            # #1648: BOTH honest asks arm the time-question carrier — the
            # answer turn ("at 3pm") must bind at the offer seam, never
            # orphan into the routing chain. #1665: the ask is rendered
            # ONCE, stored on the armed record, and returned — never two
            # renders that could drift.
            # #1562: explicit "today" + a clock time that has already passed
            # on the server clock — honest ask, never a silent roll to
            # tomorrow. (The server's clock is not the user's until
            # #1535/#747 lands, so this can fire while the time is still in
            # the user's future; the ask keeps the user in control either way.)
            if time_label.startswith(PAST_TODAY_PREFIX):
                passed_time = time_label[len(PAST_TODAY_PREFIX) :]
                ask = (
                    f"Did you mean tomorrow? "
                    f"Say 'remind me at {passed_time} tomorrow' — or give me "
                    f"another time — and I'll set it."
                )
                self._arm_time_question(
                    intent_service, session_id, user_id, text, question=ask
                )
                return (
                    f"I caught the task — **{text}** — but {passed_time} today "
                    f"has already passed on my clock. {ask}"
                )
            ask = (
                "When should I remind you? "
                "(For example: 'at 3pm tomorrow' or 'in 2 hours'.)"
            )
            self._arm_time_question(
                intent_service, session_id, user_id, text, question=ask
            )
            return (
                f"I caught the task — **{text}** — but couldn't work out "
                f'the time from "{time_label}". {ask}'
            )

        try:
            todo = await self.todo_service.create_todo(
                user_id=user_id,
                text=text,
                priority="medium",
                reminder_date=reminder_dt,
                due_date=reminder_dt,
            )

            logger.info(
                "Reminder created",
                todo_id=str(todo.id),
                text=text,
                reminder_date=str(reminder_dt),
                time_label=time_label,
                user_id=user_id,
            )

            # Format confirmation with time (#1648: factored to module level
            # so the time-answer seam shares the ONE real save confirmation —
            # per-line rationale comments live on _reminder_saved_message).
            return _reminder_saved_message(text, reminder_dt, time_label)

        except Exception as e:
            logger.error(
                "Reminder creation failed",
                error=str(e),
                user_id=user_id,
                exc_info=True,
            )
            return (
                "I had trouble saving that reminder. "
                "You can try again, or use 'add todo: [your task]' as a fallback."
            )

    # Issue #1490: time expressions a reminder message may carry, shared by the
    # time-first patterns (skip them to find the task) and the trailing strip
    # (remove them from the saved todo text). Mirrors what parse_reminder_time
    # in temporal_utils can actually parse.
    _TIME_EXPR = (
        r"(?:tomorrow(?:\s+(?:morning|afternoon|evening))?|tonight|"
        r"this\s+(?:morning|afternoon|evening)|"
        r"next\s+week|"
        r"(?:next|on)\s+(?:monday|tuesday|wednesday|thursday|friday|saturday|sunday)|"
        # Issue #1542: duration numbers are digit OR word form ("in two
        # hours", "in an hour"). DURATION_NUMBER_SRC is imported from
        # temporal_utils (non-capturing) so this stays mirrored with what
        # find_explicit_duration can actually bind.
        rf"in\s+{DURATION_NUMBER_SRC}\s+(?:minutes?|mins?|hours?|hrs?|days?)|"
        # Issue #1490 (inverted-order reopen): "at" forms now cover
        # noon/midnight and an optional TRAILING "today" ("at 9:41 today"),
        # plus bare "3pm"/"9:41am" and bare noon/midnight — mirroring what
        # find_explicit_clock_time can bind. (RESTORED 2026-08-08, merge-drop.)
        r"(?:today\s+)?at\s+(?:\d{1,2}(?::\d{2})?\s*(?:am|pm)?|noon|midnight)(?:\s+today)?|"
        r"\d{1,2}(?::\d{2})?\s*(?:am|pm)|"
        r"noon|midnight)"
    )

    def _extract_reminder_text(self, message: str) -> Optional[str]:
        """
        Issue #903: Extract the actionable text from a reminder request.

        Strips command phrases like "remind me to", "set a reminder to", etc.

        Issue #1490: also handles [time-first, task-after-'to'] ordering
        ("remind me tomorrow at 3pm to review the PR"), trailing punctuation,
        and compound trailing time expressions ("tomorrow at 3pm").
        """
        import re

        time_expr = self._TIME_EXPR

        # Order matters — try most specific patterns first.
        # Time-first variants (Issue #1490) precede the generic forms: the
        # generic forms can't match them ('to|about' must directly follow the
        # command phrase), and the time-first forms can't match task-first
        # messages (a time expression must directly follow the command phrase),
        # so neither shadows the other.
        patterns = [
            rf"(?:please\s+)?remind\s+me\s+(?:{time_expr}\s+)+(?:to|about)\s+(.+)",
            rf"(?:please\s+)?set\s+(?:a\s+)?reminder\s+(?:for\s+)?(?:{time_expr}\s+)+(?:to|about)\s+(.+)",
            rf"(?:please\s+)?create\s+(?:a\s+)?reminder\s+(?:for\s+)?(?:{time_expr}\s+)+(?:to|about)\s+(.+)",
            r"(?:please\s+)?remind\s+me\s+(?:to|about)\s+(.+)",
            r"(?:please\s+)?set\s+(?:a\s+)?reminder\s+(?:to|for|about)\s+(.+)",
            r"(?:please\s+)?create\s+(?:a\s+)?reminder\s+(?:to|for|about)\s+(.+)",
            r"don'?t\s+let\s+me\s+forget\s+(?:to\s+)?(.+)",
            r"(?:i\s+)?need\s+to\s+remember\s+to\s+(.+)",
        ]

        message_lower = message.lower().strip()
        for pattern in patterns:
            match = re.search(pattern, message_lower)
            if match:
                text = match.group(1).strip()
                # Strip trailing punctuation and time expressions so the todo
                # text is clean. Loop until stable: "review PRs tomorrow at
                # 3pm." sheds ".", then "at 3pm", then "tomorrow" (#1490).
                while text:
                    stripped = text.rstrip(".,!?;: ").strip()
                    stripped = re.sub(
                        rf"\s+{time_expr}\s*$",
                        "",
                        stripped,
                        flags=re.IGNORECASE,
                    ).strip()
                    if stripped == text:
                        break
                    text = stripped
                if text:
                    return text

        return None

    async def handle_list_reminders(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """
        Issue #1521: Handle "what reminders do I have?" — list the STORED
        reminders instead of misrouting to the temporal/calendar answer.

        Reads this user's active todos (owner-scoped via user_id, the #1493
        discipline) and reports the ones carrying a reminder_date, split into
        due-now/overdue vs upcoming. Both sides of the due-ness comparison are
        normalized aware-UTC per the #1491/#1429 guard shape (naive rows from
        tz-dropping backends are assumed UTC via ensure_utc, never TypeError).
        """
        from datetime import datetime, timezone

        from services.utils.datetime_utils import ensure_utc

        try:
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            reminders = [
                todo
                for todo in todos
                if getattr(todo, "reminder_date", None) is not None and not todo.completed
            ]

            logger.info(
                "Reminder list retrieved",
                user_id=user_id,
                todo_count=len(todos),
                reminder_count=len(reminders),
            )

            if not reminders:
                # Pattern-073 discipline: describe what was actually queried
                # (saved reminders), not a categorical "nothing scheduled".
                return (
                    "I checked your saved reminders and there are none right now. "
                    "You can set one with 'remind me to [task] tomorrow at 9am'."
                )

            now = datetime.now(timezone.utc)
            due: List[tuple] = []
            upcoming: List[tuple] = []
            for todo in reminders:
                when = ensure_utc(todo.reminder_date)
                (due if when <= now else upcoming).append((when, todo))
            due.sort(key=lambda pair: pair[0])
            upcoming.sort(key=lambda pair: pair[0])

            def _line(when, todo) -> str:
                return f"- **{todo.text}** — {when.strftime('%A, %B %-d at %-I:%M %p')} UTC"

            count = len(reminders)
            parts = [f"You have {count} reminder{'s' if count != 1 else ''} saved:"]
            if due:
                parts.append("\n⏰ Due now:")
                parts.extend(_line(when, todo) for when, todo in due)
            if upcoming:
                parts.append("\n📅 Upcoming:")
                parts.extend(_line(when, todo) for when, todo in upcoming)
            return "\n".join(parts)

        except Exception as e:  # silent-ok: logged at error w/ exc_info; user gets honest trouble-loading copy, never a false "no reminders" (#1425)
            logger.error(
                "Reminder list retrieval failed", error=str(e), user_id=user_id, exc_info=True
            )
            # #1425 discipline: a source failure must read as trouble-loading,
            # never as "no reminders".
            return (
                "I had trouble loading your reminders right now. "
                "You can try 'what reminders do I have?' again in a moment."
            )

    async def handle_list_todos(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "show my todos" or "list todos" - shows active todos from database.

        Issue #904: Now supports "show all my todos" to include completed items.
        """
        try:
            original_message = intent.original_message or intent.context.get("original_message", "")
            include_completed = self._wants_completed_todos(original_message)

            # Get todos from database
            todos = await self.todo_service.list_todos(
                user_id=user_id, include_completed=include_completed
            )

            logger.info(
                "Todo list retrieved",
                user_id=user_id,
                count=len(todos),
                include_completed=include_completed,
            )

            # Format with consciousness
            return format_todo_list_conscious(todos, include_completed=include_completed)

        # #1423: narrowed from `except Exception` — expected failures are DB-layer
        # (unreachable/timeout), covered by SQLAlchemyError. Code bugs (e.g. in the
        # conscious formatter) now propagate to the route's degradation boundary
        # instead of vanishing into "try again in a moment".
        except (SQLAlchemyError, OSError) as e:
            logger.error("Todo list retrieval failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble loading your todos right now. You can try 'show my todos' again in a moment, or add a new one with 'add todo: [task]'."

    async def handle_next_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "what's my next todo?" or "next task" - shows highest priority todo."""
        try:
            # Get active todos from database (already sorted by priority)
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            logger.info("Next todo retrieved", user_id=user_id, has_todos=len(todos) > 0)

            if not todos:
                # Issue #1096 slice 3 (Pattern-073 discipline): describe what
                # was actually queried ("active todos") rather than the
                # categorical "nothing pending" (which would imply "nothing
                # pending in your life").
                return (
                    "I checked your active todos and there are none. "
                    "If something comes to mind, just say 'add todo: [task]'."
                )

            # Get the first todo (highest priority due to sorting in repository)
            next_todo = todos[0]

            # Format with consciousness
            return format_next_todo_conscious(next_todo, len(todos))

        except Exception as e:
            logger.error("Next todo retrieval failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble finding your next todo right now. You can try 'show my todos' to see your full list, or ask again in a moment."

    async def handle_complete_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "mark todo 1 as complete" or "complete the PR review todo"

        Issue #904: Supports both number-based and fuzzy text-based matching.
        Number path: "mark todo 3 as complete" → completes todo #3 by position.
        Text path: "complete the PR review" → fuzzy matches against todo texts.
        """
        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")

        try:
            # Get user's todo list
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            if not todos:
                return (
                    "You don't have any active todos to complete. "
                    "Add one with 'add todo: [task]' first."
                )

            # Path 1: Try number-based matching first
            todo_number = self._extract_todo_id(original_message)
            if todo_number is not None:
                try:
                    idx = int(todo_number) - 1
                    if idx < 0 or idx >= len(todos):
                        return (
                            f"I couldn't find todo #{todo_number}. "
                            f"You have {len(todos)} active todos."
                        )
                    todo = todos[idx]
                except ValueError:
                    return (
                        f"'{todo_number}' doesn't look like a number. "
                        "Try: 'mark todo 1 as complete'"
                    )
            else:
                # Path 2: Fuzzy text matching (Issue #904)
                completion_text = self._extract_completion_text(original_message)
                if not completion_text:
                    return (
                        "Which todo would you like to complete? "
                        "Try 'complete todo 1' or 'complete the [description]'."
                    )

                todo = self._find_best_matching_todo(completion_text, todos)
                if todo is None:
                    return (
                        f"I couldn't find a todo matching '{completion_text}'. "
                        "Try 'show my todos' to see your list, then "
                        "'complete todo [number]'."
                    )

            # Mark as complete
            # #1436: domain Todo.id is a str(uuid4); the service is typed UUID.
            # Same value either way — this makes the contract explicit.
            completed_todo = await self.todo_service.complete_todo(
                todo_id=UUID(todo.id), user_id=user_id
            )

            if completed_todo:
                logger.info("Todo completed", todo_id=str(todo.id), user_id=user_id)
                return format_todo_completed_conscious(completed_todo)
            else:
                return "I couldn't complete that todo. It might have been deleted."

        except Exception as e:
            logger.error("Todo completion failed", error=str(e), user_id=user_id, exc_info=True)
            return (
                "I had trouble marking that as complete. You can try again with "
                "'complete todo [number]', or say 'show my todos' to check the list first."
            )

    async def handle_delete_todo(self, intent: Intent, session_id: str, user_id: UUID) -> str:
        """Handle: "delete todo 3" or "remove todo about meeting"""
        # Note: original_message may be in intent.original_message OR intent.context["original_message"]
        # depending on how the Intent was created (Issue #744)
        original_message = intent.original_message or intent.context.get("original_message", "")
        todo_number = self._extract_todo_id(original_message)
        if not todo_number:
            return "Which todo should I remove? Try: 'delete todo [number]'"

        try:
            # Get user's todo list to find the todo by position
            todos = await self.todo_service.list_todos(user_id=user_id, include_completed=False)

            # Convert todo number to index
            try:
                idx = int(todo_number) - 1
                if idx < 0 or idx >= len(todos):
                    return (
                        f"I couldn't find todo #{todo_number}. You have {len(todos)} active todos."
                    )
            except ValueError:
                return f"'{todo_number}' doesn't look like a number. Try: 'delete todo 1'"

            # Get the todo at that position
            todo = todos[idx]
            todo_text = todo.text

            # Delete the todo
            # #1436: same str(uuid4) → UUID contract fix as complete_todo above.
            deleted = await self.todo_service.delete_todo(todo_id=UUID(todo.id), user_id=user_id)

            if deleted:
                logger.info("Todo deleted", todo_id=str(todo.id), user_id=user_id)
                return format_todo_deleted_conscious(todo_text)
            else:
                return "I couldn't delete that todo. It might have already been removed."

        except Exception as e:
            logger.error("Todo deletion failed", error=str(e), user_id=user_id, exc_info=True)
            return "I had trouble removing that todo. You can try again with 'delete todo [number]', or say 'show my todos' to verify the list."

    def _extract_todo_text(self, message: str) -> str:
        """Extract todo text from 'add todo: TEXT' pattern.

        Issue #940 UAT Finding 5: Accept natural phrasing with articles
        ('Add a todo:', 'create a new todo:') not just rigid 'add todo:'.
        """
        # Try "add [a] [new] todo: TEXT" pattern
        match = re.search(r"add\s+(?:a\s+)?(?:new\s+)?todo:?\s+(.+)", message, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Try "create [a] [new] todo: TEXT" pattern
        match = re.search(r"create\s+(?:a\s+)?(?:new\s+)?todo:?\s+(.+)", message, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        # Try "todo: TEXT" pattern
        match = re.search(r"^todo:?\s+(.+)", message, re.IGNORECASE)
        if match:
            return match.group(1).strip()

        return ""

    def _extract_priority(self, message: str) -> str:
        """Extract priority from message (low, medium, high, urgent)."""
        message_lower = message.lower()

        if "urgent" in message_lower:
            return "urgent"
        elif "high priority" in message_lower or "high" in message_lower:
            return "high"
        elif "low priority" in message_lower or "low" in message_lower:
            return "low"
        else:
            return "medium"

    def _extract_todo_id(self, message: str) -> Optional[str]:
        """Extract todo ID from message (by number)."""
        # Try "todo N" or "todo #N" pattern
        match = re.search(r"todo\s+#?(\d+)", message, re.IGNORECASE)
        if match:
            return match.group(1)

        # Try just a number after "mark" or "complete" or "delete"
        match = re.search(r"(?:mark|complete|delete|remove)\s+(\d+)", message, re.IGNORECASE)
        if match:
            return match.group(1)

        return None

    # ------------------------------------------------------------------
    # Issue #904: Fuzzy text matching for todo completion
    # ------------------------------------------------------------------

    def _extract_completion_text(self, message: str) -> Optional[str]:
        """Extract the descriptive text from a completion request.

        Extracts the part of the message that describes which todo to complete.
        Returns None if the message uses a number (handled by _extract_todo_id).

        Examples:
            "complete the PR review todo" → "PR review"
            "finish the deployment task" → "deployment"
            "mark todo 3 as complete" → None (number-based)
        """
        # If a number is present, defer to number-based path
        if self._extract_todo_id(message) is not None:
            return None

        # Try various completion patterns and extract the descriptive part
        patterns = [
            # "complete todo X" (strip "todo" prefix from descriptive text)
            r"(?:complete|finish)\s+todo\s+(.+?)(?:\s*$)",
            # "complete the X todo/task"
            r"(?:complete|finish|done with)\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
            # "mark the X as done/complete"
            r"mark\s+(?:the\s+)?(.+?)\s+(?:as\s+)?(?:done|complete|finished)",
            # "mark done: X" or "mark done the X"
            r"mark\s+done:?\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
            # "I'm done with X"
            r"(?:i'?m\s+)?done\s+with\s+(?:the\s+)?(.+?)(?:\s+todo|\s+task|\s*$)",
        ]

        for pattern in patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                text = match.group(1).strip()
                # Clean up trailing noise
                text = re.sub(r"\s+(todo|task|item|thing)$", "", text, flags=re.IGNORECASE)
                if text:
                    return text

        return None

    def _find_best_matching_todo(self, search_text: str, todos: List[Todo]) -> Optional[Todo]:
        """Find the todo that best matches the search text using fuzzy word overlap.

        Returns the best matching todo if score >= threshold, else None.
        """
        if not todos or not search_text:
            return None

        scored: List[Tuple[float, Todo]] = []
        for todo in todos:
            score = self._fuzzy_match_score(search_text, todo.text)
            if score >= _FUZZY_MATCH_THRESHOLD:
                scored.append((score, todo))

        if not scored:
            return None

        # Sort by score descending, return best match
        scored.sort(key=lambda x: x[0], reverse=True)
        return scored[0][1]

    @staticmethod
    def _fuzzy_match_score(query: str, candidate: str) -> float:
        """Score how well query words match candidate words (0.0 to 1.0).

        Uses word overlap with stopword filtering. Score is the fraction
        of meaningful query words found in the candidate.
        """
        query_words = {w for w in re.findall(r"\w+", query.lower()) if w not in _STOPWORDS}
        candidate_words = {w for w in re.findall(r"\w+", candidate.lower()) if w not in _STOPWORDS}

        if not query_words:
            return 0.0

        overlap = query_words & candidate_words
        return len(overlap) / len(query_words)

    @staticmethod
    def _wants_completed_todos(message: str) -> bool:
        """Check if the user wants to see completed todos too.

        Issue #904: "show all my todos" or "show completed todos" includes done items.
        """
        message_lower = message.lower()
        return any(
            phrase in message_lower
            for phrase in [
                "all my todos",
                "all todos",
                "completed todos",
                "done todos",
                "finished todos",
                "including completed",
                "include completed",
                "show everything",
            ]
        )


# --- #1648: the reminder time-question turn handler -------------------------


# #1665: the re-ask turns' open question — one constant, embedded in the
# re-ask reply AND stored on the re-armed record (same string, no drift).
_TIME_REASK_TAIL = (
    "Tell me when (for example: 'at 3pm tomorrow' or 'in 2 hours'), "
    "or say 'no' to drop it."
)


def _rearm_time_question(
    intent_service, session_id, user_id, pending_offer
) -> bool:
    """Re-arm the SAME offer (the pop already consumed it; a re-ask turn must
    re-store it or the next answer has nothing to bind to). Returns False on
    a store failure so the copy never claims a binding that isn't there.
    #1665: the re-armed record's open question becomes the re-ask tail every
    re-ask turn renders (set BEFORE the store — what's stored is what's said)."""
    try:
        pending_offer["question"] = _TIME_REASK_TAIL
        intent_service.workflow_offer_service.set_pending_offer(
            session_id, pending_offer, user_id=user_id
        )
        return True
    except Exception as e:  # silent-ok: #1648 — a store failure must not crash the turn; logged ERROR, and callers keep the user-facing copy honest
        logger.error("reminder_time_question_rearm_failed", error=str(e))
        return False


def _time_reask(
    task_text: str,
    detail: str,
    rearmed: bool,
) -> dict:
    """The honest re-ask shape: nothing saved, here's why, here's what works."""
    if rearmed:
        tail = _TIME_REASK_TAIL
    else:
        tail = (
            "I couldn't keep the reminder bound either — ask me again "
            "('remind me to … at …') and I'll set it fresh."
        )
    return {
        "message": (
            f"Nothing has been saved yet for **{task_text}** — {detail} {tail}"
        ),
        "intent_data": {
            "category": "execution",
            "action": "create_reminder",
            "reminder_time_question_pending": rearmed,
            "reminder_time_reasked": True,
        },
        "requires_clarification": True,
    }


async def handle_reminder_time_turn(
    pending_offer: dict,
    message: str,
    *,
    session_id: str,
    user_id,
    intent_service,
) -> Optional[dict]:
    """#1648 — kind-specific turn handling for a pending reminder time
    question, run at the offer seam BEFORE any classification surface (the
    #1605/#1571 sanctioned handler-internal seam; the pop already happened).

    Returns a ``{"message", "intent_data", ...}`` dict when this turn is
    consumed here; ``None`` falls through to the generic offer flow
    (declines and bare exits drop honestly via ``decline_message``; full
    reminder restatements and unrelated commands abandon via the pop and
    route normally — the pre-classifier claims restatements
    deterministically, so the full handler re-extracts task AND time).

    The save path is the REAL one: a row write via TodoManagementService,
    confirmed with the same 📅 copy the primary path composes — never an
    improvised confirmation (the floor roleplayed exactly that, live).
    """
    from services.intent_service.destructive_confirm import detect_bare_exit
    from services.intent_service.drafted_issue import is_command_shaped
    from services.intent_service.soft_invocation import detect_offer_response
    from services.intent_service.temporal_utils import (
        PAST_TODAY_PREFIX,
        parse_reminder_time,
    )

    payload = pending_offer.get("pending_action") or {}
    task_text = (payload.get("task_text") or "").strip()
    text = (message or "").strip()
    if not task_text or not text:
        if not task_text:
            logger.error(
                "reminder_time_question_missing_task", session_id=session_id
            )
        return None

    # Principal binding (the #1605 discipline): the offer belongs to the user
    # who asked — a different principal's turn must not save under it.
    offer_user = payload.get("user_id")
    if offer_user and user_id and str(user_id) != str(offer_user):
        logger.warning(
            "reminder_time_question_principal_mismatch",
            offer_user=offer_user,
            turn_user=str(user_id),
        )
        return {
            "message": "Let's hold off on that — nothing has been saved.",
            "intent_data": {
                "category": "execution",
                "action": "create_reminder",
                "principal_mismatch": True,
            },
        }

    if detect_bare_exit(text):
        return None  # generic flow → honest decline via decline_message
    resp = detect_offer_response(text)
    if resp == "decline":
        return None  # same honest decline path

    if _REMINDER_RESTATEMENT_RE.search(text):
        # A full restatement carries its own task and time — abandon via the
        # pop and let it route normally (deterministic pre-classifier claim).
        logger.info(
            "reminder_time_question_restatement_released", session_id=session_id
        )
        return None

    if _has_time_signal(text):
        reminder_dt, time_label = parse_reminder_time(text)
        if reminder_dt is None:
            rearmed = _rearm_time_question(
                intent_service, session_id, user_id, pending_offer
            )
            if time_label.startswith(PAST_TODAY_PREFIX):
                passed_time = time_label[len(PAST_TODAY_PREFIX) :]
                detail = (
                    f"{passed_time} today has already passed on my clock. "
                    f"Did you mean tomorrow?"
                )
            else:
                detail = f'I couldn\'t work out the time from "{time_label}".'
            logger.info(
                "reminder_time_question_unbindable_reasked",
                session_id=session_id,
                rearmed=rearmed,
            )
            return _time_reask(task_text, detail, rearmed)

        # The REAL save — the same write the primary path performs.
        principal = user_id or offer_user
        try:
            user_uuid = UUID(str(principal))
        except (ValueError, TypeError):
            return {
                "message": (
                    "I need you to be logged in to set reminders. "
                    "Nothing has been saved."
                ),
                "intent_data": {
                    "category": "execution",
                    "action": "create_reminder",
                    "error_type": "AuthenticationRequired",
                },
            }
        try:
            todo = await intent_service.todo_handlers.todo_service.create_todo(
                user_id=user_uuid,
                text=task_text,
                priority="medium",
                reminder_date=reminder_dt,
                due_date=reminder_dt,
            )
        except Exception as e:  # silent-ok: #1648 — a failed write must surface as an HONEST failure (never a crash, never a success claim); logged ERROR + traceback
            logger.error(
                "reminder_time_question_save_failed",
                error=str(e),
                session_id=session_id,
                exc_info=True,
            )
            rearmed = _rearm_time_question(
                intent_service, session_id, user_id, pending_offer
            )
            return _time_reask(
                task_text,
                "I had trouble saving it just now.",
                rearmed,
            )

        logger.info(
            "reminder_time_question_saved",
            todo_id=str(todo.id),
            reminder_date=str(reminder_dt),
            time_label=time_label,
            session_id=session_id,
        )
        return {
            "message": _reminder_saved_message(task_text, reminder_dt, time_label),
            "intent_data": {
                "category": "execution",
                "action": "create_reminder",
                "confidence": 1.0,
                "reminder_saved": True,
            },
        }

    # No time signal in the turn.
    if resp != "accept" and is_command_shaped(text):
        # An unrelated command abandons via the pop and routes normally —
        # the carrier's documented off-intent rule.
        return None

    # A bare "yes" doesn't answer "when?", and anything else unrecognized
    # gets the honest re-ask — never a silent abandon into the routing chain
    # mid-flow (#1648 direction 2).
    rearmed = _rearm_time_question(intent_service, session_id, user_id, pending_offer)
    logger.info(
        "reminder_time_question_reasked",
        session_id=session_id,
        rearmed=rearmed,
    )
    return _time_reask(
        task_text,
        "I still need a time for it.",
        rearmed,
    )


async def run_clarify_reminder_time_workflow(
    session_id: str,
    user_id=None,
    context=None,
):
    """Generic-accept landing for the time question (defense in depth — the
    kind-specific seam claims accepts itself, but a registered landing means
    a stray generic accept can never fall into _handle_unknown_intent and
    reach the floor): re-ask and re-arm. effect: READ (nothing written; the
    real write happens on an ANSWERED turn at the offer seam)."""
    ctx = context or {}
    payload = ctx.get("pending_action") or {}
    intent_service = ctx.get("intent_service")
    if payload.get("kind") != REMINDER_TIME_QUESTION_KIND or intent_service is None:
        logger.error(
            "clarify_reminder_time_missing_or_foreign_payload",
            kind=payload.get("kind"),
            has_intent_service=intent_service is not None,
        )
        return None
    task_text = (payload.get("task_text") or "").strip() or "that"
    offer = {
        "workflow_type": CLARIFY_REMINDER_TIME_WORKFLOW,
        "pending_action": dict(payload),
        "decline_message": (
            "Okay — I haven't set that reminder. Nothing was saved."
        ),
    }
    rearmed = _rearm_time_question(intent_service, session_id, user_id, offer)
    return _time_reask(task_text, "I still need a time for it.", rearmed)
