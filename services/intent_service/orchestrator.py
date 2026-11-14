"""
Intent orchestration for multi-substantive intent handling.

Issue #764: GLUE-MULTIINTENT — Multi-Intent Handling Enhancements

Provides:
- ExecutionPlan for planning multi-intent execution
- IntentOrchestrator for executing multiple intents and aggregating responses
- Graceful fallback on partial failure
"""

import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional

import structlog

from services.domain.models import Intent
from services.intent_service.pre_classifier import MultiIntentResult

logger = structlog.get_logger()

# Maximum intents to process in a single message
MAX_INTENTS = 4


class ExecutionStrategy(str, Enum):
    """How to execute multiple intents."""

    PARALLEL = "parallel"  # All intents can run independently (default)
    SEQUENTIAL = "sequential"  # Intents have dependencies


@dataclass
class ExecutionPlan:
    """Plan for executing multiple intents from a single message."""

    intents: List[Intent]
    strategy: ExecutionStrategy = ExecutionStrategy.PARALLEL
    original_message: str = ""
    has_greeting: bool = False
    capped: bool = False  # True if intents were capped at MAX_INTENTS

    @property
    def intent_count(self) -> int:
        return len(self.intents)


@dataclass
class IntentExecutionResult:
    """Result of executing a single intent within an orchestrated plan."""

    intent: Intent
    response: str = ""
    intent_data: Dict[str, Any] = field(default_factory=dict)
    success: bool = True
    error: Optional[str] = None
    duration_ms: float = 0.0
    # #2030 (Arch's ruling, issuecomment-6203827433): the handler's #852
    # ``offer_hint``, carried — never armed here. The orchestrator does no
    # session-store writes; IntentService arms the ONE picked hint.
    offer_hint: Optional[Dict[str, Any]] = None
    # #2041 (Arch's ruling, 2026-10-15): the handler's #2035 ``write_offer``
    # (the #846 pending-offer record a yes/no offer whose "yes" leads to a
    # WRITE hands back), carried the same way — never armed here.
    write_offer: Optional[Dict[str, Any]] = None


@dataclass
class OrchestratedResponse:
    """Aggregated response from executing multiple intents."""

    results: List[IntentExecutionResult] = field(default_factory=list)
    aggregated_message: str = ""
    has_partial_failure: bool = False
    total_duration_ms: float = 0.0
    greeting_prefix: bool = False
    # #2030: the one hint this turn arms (first successful sub-result, in
    # plan order, whose offer_text was removed verbatim from its response).
    # Its offer_text is the composed reply's LAST sentence. IntentService
    # hands it to ``_track_offer_hint`` before ``_apply_soft_offer``.
    armed_offer_hint: Optional[Dict[str, Any]] = None
    # #2041: the one write offer this turn arms (first successful sub-result,
    # in plan order, whose record's ``question`` was removed verbatim). A
    # write offer OUTRANKS a hint: when this is set, ``armed_offer_hint`` is
    # None and the question asked last is this record's ``question``.
    # IntentService hands it to ``_arm_write_offer`` before
    # ``_track_offer_hint`` and ``_apply_soft_offer``.
    armed_write_offer: Optional[Dict[str, Any]] = None

    @property
    def successful_results(self) -> List[IntentExecutionResult]:
        return [r for r in self.results if r.success]

    @property
    def failed_results(self) -> List[IntentExecutionResult]:
        return [r for r in self.results if not r.success]

    @property
    def primary_intent_data(self) -> Dict[str, Any]:
        """Get intent_data from first successful result."""
        for result in self.results:
            if result.success:
                return result.intent_data
        return {}


class IntentOrchestrator:
    """
    Orchestrates execution of multiple intents from a single message.

    Receives a MultiIntentResult with 2+ substantive intents, creates an
    execution plan, runs each through existing handlers, and aggregates
    the responses into a single coherent message.

    Per Chief Architect guidance: handlers stay single-intent; this layer
    orchestrates and aggregates.
    """

    def __init__(self, canonical_handlers):
        """
        Args:
            canonical_handlers: CanonicalHandlers instance for dispatching intents
        """
        self._handlers = canonical_handlers

    def create_plan(self, multi_result: MultiIntentResult) -> ExecutionPlan:
        """
        Create an execution plan from a multi-intent result.

        Caps at MAX_INTENTS and determines execution strategy.
        All execution is parallel by default (no dependency detection yet).
        """
        intents = list(multi_result.intents)
        capped = len(intents) > MAX_INTENTS

        if capped:
            logger.warning(
                "multi_intent_capped",
                original_count=len(intents),
                max_intents=MAX_INTENTS,
            )
            intents = intents[:MAX_INTENTS]

        plan = ExecutionPlan(
            intents=intents,
            strategy=ExecutionStrategy.PARALLEL,
            original_message=multi_result.original_message,
            has_greeting=multi_result.has_greeting,
            capped=capped,
        )

        logger.info(
            "execution_plan_created",
            intent_count=plan.intent_count,
            strategy=plan.strategy.value,
            has_greeting=plan.has_greeting,
            capped=capped,
        )

        return plan

    async def execute_plan(
        self,
        plan: ExecutionPlan,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> OrchestratedResponse:
        """
        Execute all intents in the plan and aggregate responses.

        Currently executes sequentially (async for each) since handlers
        may share state. Can be upgraded to asyncio.gather for true parallel.
        """
        start_time = time.monotonic()
        results: List[IntentExecutionResult] = []

        for intent in plan.intents:
            result = await self._execute_single(intent, session_id, user_id)
            results.append(result)

        total_ms = (time.monotonic() - start_time) * 1000
        has_failure = any(not r.success for r in results)

        response = OrchestratedResponse(
            results=results,
            has_partial_failure=has_failure,
            total_duration_ms=total_ms,
            greeting_prefix=plan.has_greeting,
        )

        # #2030: pick the one armed hint and take every hinted question out
        # of its sibling's text, BEFORE aggregation. #2041 (Arch's ruling):
        # the same for write offers, and a write offer OUTRANKS a hint, so
        # one question is armed and asked per composed turn.
        response.armed_write_offer = self._pick_armed_write_offer(response.results)
        armed_hint = self._pick_armed_offer(response.results)
        if response.armed_write_offer is not None and armed_hint is not None:
            logger.info(
                "multi_intent_offer_dropped",
                continuation_hint=armed_hint.get("continuation_hint"),
                reason="outranked_by_write_offer",
            )
            armed_hint = None
        response.armed_offer_hint = armed_hint

        # Aggregate the messages
        response.aggregated_message = self._aggregate_messages(response)

        logger.info(
            "orchestrated_execution_complete",
            total_intents=len(results),
            successful=len(response.successful_results),
            failed=len(response.failed_results),
            duration_ms=round(total_ms, 1),
        )

        return response

    async def _execute_single(
        self,
        intent: Intent,
        session_id: str,
        user_id: Optional[str] = None,
    ) -> IntentExecutionResult:
        """Execute a single intent through canonical handlers.

        Gates on ``CanonicalHandlers.claims_category`` (category-only),
        deliberately NOT the rail-aware ``can_handle`` (Arch's split-
        predicate ruling, 2026-10-04,
        mailboxes/lead/inbox/rule-arch-to-lead-cc-cxo-exec-take-a-split-
        predicate-adapter-parity-lands-with-it-b-uses-0926-sequencing-
        2026-10-04.md). This method dispatches straight to
        ``CanonicalHandlers.handle()`` below — there is no rail adapter in
        this path — so a rail-aware decline would make every rail-keyed
        sibling (e.g. a PORTFOLIO write) undispatchable here and dropped to
        the floor mid-multi-intent (the #1763 guard ``IntentService.
        _is_orchestratable_sibling`` exists to prevent, using the SAME
        predicate so the two can never disagree).

        KNOWN COST (today's gap, not new): because this calls
        ``CanonicalHandlers.handle()`` directly, a PORTFOLIO write named as a
        multi-intent sibling skips the #1509 consent gate the rail enforces
        on the single-intent path. Tracked follow-up: give the orchestrator
        its own rail-aware dispatch (the ruling's item (b)).
        """
        start_time = time.monotonic()

        try:
            if not self._handlers.claims_category(intent):
                return IntentExecutionResult(
                    intent=intent,
                    success=False,
                    error=f"No handler for category: {intent.category.value}",
                    duration_ms=(time.monotonic() - start_time) * 1000,
                )

            result = await self._handlers.handle(intent, session_id, user_id)
            duration_ms = (time.monotonic() - start_time) * 1000

            return IntentExecutionResult(
                intent=intent,
                response=result.get("message", ""),
                intent_data=result.get("intent", {}),
                success=True,
                duration_ms=duration_ms,
                # #2030: carry the hint (the single path arms it at
                # _process_intent_internal; this path's holder arms it
                # through OrchestratedResponse.armed_offer_hint).
                offer_hint=result.get("offer_hint") or None,
                # #2041: carry the write offer the same way (the single path
                # arms it at _process_intent_internal's _arm_write_offer;
                # this path's holder arms it through
                # OrchestratedResponse.armed_write_offer).
                write_offer=result.get("write_offer") or None,
            )

        except Exception as e:
            duration_ms = (time.monotonic() - start_time) * 1000
            logger.warning(
                "intent_execution_failed",
                category=intent.category.value,
                action=intent.action,
                error=str(e),
                duration_ms=round(duration_ms, 1),
            )
            return IntentExecutionResult(
                intent=intent,
                success=False,
                error=str(e),
                duration_ms=duration_ms,
            )

    def _pick_armed_offer(self, results: List[IntentExecutionResult]) -> Optional[Dict[str, Any]]:
        """#2030 (Arch's ruling, issuecomment-6203827433): carry, pick one,
        ask it last.

        For EVERY sub-result with an ``offer_hint``, its ``offer_text`` is
        removed from its response by exact match (#2010 adequacy makes the
        rendered question verbatim ``offer_text``; #2024 hardening (a) makes
        it a question). The first SUCCESSFUL sub-result in plan order whose
        removal matched is the armed one; ``_aggregate_messages`` appends its
        ``offer_text`` once, last. A sibling whose ``offer_text`` is not
        found verbatim (drift) arms nothing and gets nothing appended; its
        text is left exactly as the handler rendered it (nothing else is
        stripped) and the drift is logged. Rewrites the hinted results'
        ``response`` in place; returns the armed hint or None. No store writes.
        """
        return _strip_and_pick(results, "offer_hint", "offer_text")

    def _pick_armed_write_offer(
        self, results: List[IntentExecutionResult]
    ) -> Optional[Dict[str, Any]]:
        """#2041 (Arch's ruling, 2026-10-15): ``_pick_armed_offer`` for the
        #2035 ``write_offer`` records. The question is the record's
        ``question`` (#1665: stored as rendered), stripped from EVERY
        sub-result that carries one by exact match; the first SUCCESSFUL
        sub-result in plan order whose removal matched is the armed one. A
        drifted question arms nothing and gets nothing appended. Precedence
        over a hint is applied by ``execute_plan``. No store writes."""
        return _strip_and_pick(results, "write_offer", "question")

    def _aggregate_messages(self, response: OrchestratedResponse) -> str:
        """
        Aggregate multiple intent responses into a single coherent message.

        Uses natural transitions between responses. Handles partial failures
        by noting what couldn't be processed. #2030: the armed offer's
        ``offer_text`` (``response.armed_offer_hint``, set by
        ``_pick_armed_offer``) is appended once as the LAST paragraph.
        #2041: when a write offer won (``response.armed_write_offer``), its
        record's ``question`` is the one appended instead.
        """
        body = self._aggregate_bodies(response)
        question = _armed_question(response)
        if question and response.successful_results:
            # Its own paragraph, like the failure note (#1431): a space-join
            # after a bullet list would read as part of the last item.
            body = f"{body}\n\n{question}" if body else question
        return body

    def _aggregate_bodies(self, response: OrchestratedResponse) -> str:
        """The statement parts of the composed reply (pre-#2030 aggregation)."""
        successful = response.successful_results
        failed = response.failed_results

        if not successful:
            return "I'm having trouble processing that right now. You could try rephrasing your request, or ask about something specific like your calendar or tasks."

        # Build the aggregated message
        parts: List[str] = []

        # Add greeting prefix if detected
        if response.greeting_prefix:
            parts.append("Hi there!")

        # Single successful result — no aggregation needed
        if len(successful) == 1 and not failed:
            if parts:
                parts.append(successful[0].response)
                return " ".join(parts)
            return successful[0].response

        # Multiple successful results — use transitions
        # #1984 (CXO's copy, 2026-10-11): two templates, alternating. The old
        # third, "On the {topic} front", read "On the your calendar front" for
        # every "your …" label at index 2 (3-part plans) — dropped.
        transitions = [
            "As for {topic}",
            "Regarding {topic}",
        ]

        for i, result in enumerate(successful):
            if i == 0:
                parts.append(result.response)
            else:
                topic = _intent_topic_label(result.intent)
                # #1984: no label → the topic-free join. Never an action id
                # humanized into prose ("Regarding list archived projects, …"
                # is what the old fallback served).
                if topic is None:
                    transition = TOPIC_FREE_TRANSITION
                else:
                    transition = transitions[i % len(transitions)].format(topic=topic)
                parts.append(f"{transition}, {_lowercase_first(result.response)}")

        body = " ".join(parts)

        # Note any failures — as their OWN paragraph, never space-joined onto
        # the last content line. #1431 bonus defect (PM screenshots 2026-08-09):
        # when the preceding response ended in a bullet list, the space-join
        # rendered the failure note as part of the last item's name
        # ("- One Job I wasn't able to check on project status ...").
        if failed:
            # #1984: an unlabeled failed intent is named by UNLABELED_FAILURE_TOPIC,
            # never by its action id; duplicates collapse so two unlabeled
            # failures read once.
            failure_topics: List[str] = []
            any_unlabeled = False
            for r in failed:
                label = _intent_topic_label(r.intent)
                if label is None:
                    any_unlabeled = True
                elif label not in failure_topics:
                    failure_topics.append(label)
            if any_unlabeled:
                # CXO's copy: a plan can include writes, so the unlabeled part is
                # something Piper could not "do", never something it "checked on".
                failure_topics.append(UNLABELED_FAILURE_TOPIC)
            if len(failure_topics) == 1 and any_unlabeled:
                # #1198: no false retry promise — nothing retries in the background.
                failure_note = (
                    f"I wasn't able to do {UNLABELED_FAILURE_TOPIC} right now — "
                    "ask me again and I'll retry."
                )
            elif len(failure_topics) == 1:
                # #1198: no false retry promise — nothing retries in the background.
                failure_note = f"I wasn't able to check on {failure_topics[0]} right now — ask me again and I'll retry."
            else:
                topics = " and ".join([", ".join(failure_topics[:-1]), failure_topics[-1]])
                # #1198: no false retry promise — nothing retries in the background.
                failure_note = (
                    f"I wasn't able to check on {topics} right now — ask me again and I'll retry."
                )
            body = f"{body}\n\n{failure_note}" if body else failure_note

        return body


def _armed_question(response: OrchestratedResponse) -> str:
    """#2041: the one question the composed reply asks last: the armed write
    offer's ``question`` (it outranks a hint), else the armed hint's
    ``offer_text``, else none."""
    if response.armed_write_offer:
        return response.armed_write_offer.get("question") or ""
    if response.armed_offer_hint:
        return response.armed_offer_hint.get("offer_text") or ""
    return ""


def _strip_and_pick(
    results: List[IntentExecutionResult], attr: str, question_key: str
) -> Optional[Dict[str, Any]]:
    """#2030 / #2041: for every sub-result carrying an offer record under
    ``attr`` (``offer_hint`` or ``write_offer``), remove the record's
    question (``record[question_key]``) from its response by exact match;
    return the record of the first SUCCESSFUL sub-result in plan order whose
    removal matched, or None. A drifted question (not verbatim in the
    response) leaves that response as rendered, arms nothing, and is logged."""
    armed: Optional[Dict[str, Any]] = None
    for r in results:
        record = getattr(r, attr)
        if not record:
            continue
        question = record.get(question_key) or ""
        label = record.get("continuation_hint") or record.get("workflow_type")
        stripped = _remove_offer_text(r.response, question) if question else None
        if stripped is None:
            logger.warning(
                "multi_intent_offer_text_drift",
                action=r.intent.action,
                kind=attr,
                offer=label,
                offer_text=question,
                note="offer question not found verbatim in the response; not armed",
            )
            continue
        r.response = stripped
        if armed is None and r.success:
            armed = record
            logger.info("multi_intent_offer_armed", action=r.intent.action, kind=attr, offer=label)
        else:
            logger.info(
                "multi_intent_offer_dropped",
                action=r.intent.action,
                kind=attr,
                offer=label,
                reason="already_armed" if armed is not None else "sub_result_failed",
            )
    return armed


def _remove_offer_text(response: str, offer_text: str) -> Optional[str]:
    """#2030: ``response`` with its first verbatim ``offer_text`` removed, or
    None when it does not occur verbatim (drift: the caller arms nothing).

    Only the question and the whitespace at the cut are touched: spaces and
    tabs either side of it go, and the two sides rejoin with one space
    (mid-line), the line break(s) already there (capped at one blank line),
    or nothing (at either end). No other text is stripped.
    """
    if not offer_text or offer_text not in response:
        return None
    before, after = response.split(offer_text, 1)
    before = before.rstrip(" \t")
    after = after.lstrip(" \t")
    if not before.strip():
        return after.lstrip("\n")
    if not after.strip():
        return before.rstrip("\n")
    if before.endswith("\n") or after.startswith("\n"):
        breaks = (len(before) - len(before.rstrip("\n"))) + (len(after) - len(after.lstrip("\n")))
        return before.rstrip("\n") + "\n" * min(breaks, 2) + after.lstrip("\n")
    return f"{before} {after}"


# #1984 (Arch's placement, 2026-10-11): the words that stand in when an intent
# has no label. CXO owns them; change the constant, not the call sites.
TOPIC_FREE_TRANSITION = "Also"  # → "Also, <next reply>"
UNLABELED_FAILURE_TOPIC = "part of that"  # → "I wasn't able to check on part of that …"


def _intent_topic_label(intent: Intent) -> Optional[str]:
    """A human-readable topic label for an intent, or None when none is defined.

    #1984: the old fallback humanized the action id (``list_archived_projects``
    → "list archived projects") and served it in prose ("Regarding list
    archived projects, you don't have any archived projects."). The plan path
    can emit any catalog action, so a missing row must never reach the user as
    an identifier: callers substitute TOPIC_FREE_TRANSITION /
    UNLABELED_FAILURE_TOPIC, pinned catalog-wide by
    tests/unit/services/intent_service/test_topic_label_catalog_1984.py.
    """
    labels = {
        "meeting_time": "your calendar",
        "week_calendar": "your calendar",
        "recurring_meetings": "your calendar",
        "get_project_status": "project status",
        "get_top_priority": "priorities",
        "get_contextual_guidance": "guidance",
        "get_identity": "that",
        "get_capabilities": "that",
        "list_todos_query": "your todos",
        "list_project_todos": "your todos",
        "github_query": "GitHub",
        "productivity_query": "productivity",
        "get_current_time": "the time",
        "explain_trust": "trust",
        "get_memory": "memory",
        "manage_portfolio": "your portfolio",
        "list_archived_projects": "your archived projects",  # #1984 (Arch's read; CXO's words)
        "list_projects": "your projects",
        "list_milestones": "your milestones",  # #1984 CXO
        "session_activity_query": "this session",  # #1984 CXO
    }
    return labels.get(intent.action)


# #1984 (CXO's rule, 2026-10-11): lowercase stays the default — "As for your
# calendar, You don't have…" is worse than "google Calendar" — with five closed,
# mechanical exceptions. A proper noun outside the list is a one-word addition
# to the list, never a rule change.
_LOWERCASE_FIRST_BRANDS = frozenset(
    {"Google", "GitHub", "Slack", "Notion", "Piper", "Gmail", "Claude", "Anthropic"}
)
_LOWERCASE_FIRST_CALENDAR_WORDS = frozenset(
    {
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December",
    }
)
_LOWERCASE_FIRST_I_FORMS = frozenset({"I", "I'm", "I'll", "I've", "I'd"})


def _lowercase_first(text: str) -> str:
    """Lowercase the first character of a string (for natural transitions),
    except when the first word is (1) a form of "I", (2) has a capital after
    its first letter (GitHub, iPhone), (3) is followed by another capitalized
    word (Google Calendar, New York), (4) is a day-of-week or month name, or
    (5) is on the short brand list. #1984, CXO's rule."""
    if not text:
        return text
    words = text.split(None, 2)
    first = words[0] if words else ""
    bare = first.rstrip(".,;:!?'\"")
    if bare in _LOWERCASE_FIRST_I_FORMS or first.startswith("I'"):
        return text
    if any(ch.isupper() for ch in bare[1:]):
        return text
    if len(words) > 1 and words[1][:1].isupper():
        return text
    if bare in _LOWERCASE_FIRST_CALENDAR_WORDS or bare in _LOWERCASE_FIRST_BRANDS:
        return text
    return text[0].lower() + text[1:]
