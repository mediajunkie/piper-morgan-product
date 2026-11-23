"""Issue 2415 (and 2416): a status turn where code has nothing for the floor to say is
answered by code alone, with no floor call.

Arch 2026-11-23 (mails 01M84SB40Q, 01M84SMP0J), mechanism B; CXO 2026-11-23 (mail
01M84S7E7T), the words; PPM 2026-11-23 (mail 01M84SKC86), acceptance. ADR-080: the
router decided the turn's meaning; code decides only WHETHER the floor runs, and only
from state. Nothing here reads the person's words or the floor's.

Measured on main before this: on a status turn that names one of the person's projects
(issue 2301's block path), an account with no working GitHub got a floor reply that
offered to fetch the status it had just been asked for (the output seam then rewrote
the offer, 23 of 24 replies), or, told about the block, narrated it ("I'm pulling up
the status now"). Five wording screens never held. So on that turn, when the floor
would have nothing true to add, it is not called.

The rules:

1. Only on the 2301 block path: ``status_todos_for_project`` returned a non-empty
   block, so exactly one project matched. No project arg, no match, several matches,
   and a resolved 2197 milestone keep today's reply byte for byte (they never reach
   this call). A named milestone that is absent or tied (``_milestone_prefix``
   non-empty) also keeps today's reply: B does not fire (Lead's reading, put to Arch).
2. The switch is a KEY SET, not "no GitHub". After ``without_todo_keys`` the gathered
   context must hold no content key: only GitHub status flags and the person's own
   records and clock (``KEY_CLASSIFICATION.status_or_own_record``). Any key in
   ``KEY_CLASSIFICATION.content`` with a value that counts, or any key the
   classification does not know, means the floor runs exactly as today.
3. B also needs a GitHub state it has words for, read from the status flags in this
   order: could not check (``integrations_source_failed``), needs reconnecting
   (``github_needs_reconnecting``), never connected (``github_connected`` present and
   false). GitHub connected and healthy, or no GitHub flags at all (the status gather
   did not run): the floor runs as today. The connected case is held under a named
   blocker (no seat has an App-connected account to screen it on); nothing is built
   for it.
4. The reply is one GitHub line, a blank line, then the block exactly as built. There
   is no bridge sentence. ``{project}`` is the STORED project name the block's header
   shows.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, FrozenSet, Optional

import structlog

from services.intent_service.capability_answer import (
    GITHUB_NOT_CONNECTED_SENTENCE,
    needs_reconnecting_sentence,
)

logger = structlog.get_logger(__name__)

KIND_COULD_NOT_CHECK = "could_not_check"
KIND_NEEDS_RECONNECTING = "needs_reconnecting"
KIND_NEVER_CONNECTED = "never_connected"

#: CXO's words (01M84S7E7T). The second sentence of the reconnect line is
#: ``needs_reconnecting_sentence(["GitHub"])``, so the Settings pointer has one source.
GITHUB_LINES: Dict[str, str] = {
    KIND_NEEDS_RECONNECTING: (
        "I can't give you GitHub status for {project} right now: "
        + needs_reconnecting_sentence(["GitHub"])
    ),
    KIND_NEVER_CONNECTED: (
        "I can't give you GitHub status for {project} yet: " + GITHUB_NOT_CONNECTED_SENTENCE
    ),
    KIND_COULD_NOT_CHECK: "I couldn't check GitHub for {project} just now.",
}


@dataclass(frozen=True)
class KeyClassification:
    """Every key the STATUS gather can put in the floor's context, in exactly one of
    two sets. ``empty_is_no_content`` is a subset of ``content``: keys the gatherer
    emits even when there is nothing, so a falsy value there is no content."""

    content: FrozenSet[str]
    status_or_own_record: FrozenSet[str]
    empty_is_no_content: FrozenSet[str]


#: The one classification (Arch 01M84SB40Q, rule 2). Read from ``context_assembler``
#: 2026-11-23: ``gather_context``, ``_gather_status_priority_context`` and every gatherer
#: it calls, the reminder rider, the first-contact and FTUX riders, plus
#: ``guided_flow_escape`` (added by ``intent_service``). When in doubt, content: the
#: floor then runs, which is today's behaviour. The guard test
#: (``test_status_all_code_2415.py``) fails when a gatherer emits a key not listed here.
KEY_CLASSIFICATION = KeyClassification(
    content=frozenset(
        {
            # Calendar: a next meeting or free block the floor could rightly mention;
            # a failed calendar read the floor would truthfully say it couldn't check.
            "calendar",
            "calendar_source_failed",
            # Due reminders (the rider; only on reminder-rendering ops today).
            "due_reminders",
            "reminder_count",
            "due_reminder_ages",
            "source_failed",
            # GitHub content: blocked items, milestones, recent activity, issues.
            "blocked_items",
            "blocked_count",
            "blocked_count_capped",
            "active_milestones",
            "active_milestone_count",
            "recent_activity",
            "recent_activity_count",
            "recent_activity_count_capped",
            "recent_activity_counts_by_source",
            "recent_activity_window_days",
            "high_priority_issues",
            "open_issue_count",
            "open_issue_count_capped",
            # Non-GitHub reads inside recent activity that failed: the floor has a
            # true "couldn't check" to say that the GitHub line does not cover.
            "calendar_activity_source_failed",
            "slack_activity_source_failed",
            # A failed projects or preferences read: the floor says so.
            "projects_source_failed",
            "priorities_source_failed",
            # The person's todos. Taken out by ``without_todo_keys`` before this runs;
            # listed so the guard sees them classified.
            "pending_todos",
            "pending_todo_count",
            "pending_todos_in_reminders",
            "pending_todos_source_failed",
            "completed_todos",
            "completed_todos_source_failed",
            # Session riders: reads this session performed, the FTUX answer, the
            # first-contact demo (or its failed read), a guided flow that just closed.
            "recorded_reads",
            "ftux_interview_answer",
            "first_contact_demo",
            "first_contact_source_failed",
            "guided_flow_escape",
        }
    ),
    status_or_own_record=frozenset(
        {
            # Clock.
            "current_time",
            "current_date",
            # GitHub's status flags: the B reply's GitHub line says what they say.
            "github_connected",
            "github_needs_reconnecting",
            "integrations_source_failed",
            # GitHub setup: no repository resolves. A GitHub state, said by the line.
            "github_repo_unconfigured",
            # A GitHub content read that failed: "can't give you / couldn't check
            # GitHub" already says it, and B never fires with GitHub healthy.
            "blocked_items_source_failed",
            "milestones_source_failed",
            "open_issues_source_failed",
            "github_activity_source_failed",
            # The person's own records.
            "projects",
            "project_count",
            "priorities",
            "organization",
        }
    ),
    # ``_compute_high_priority_issues`` emits ``{"high_priority_issues": [],
    # "open_issue_count": 0, ...}`` exactly when there is nothing (no open issues and no
    # repository), and ``_get_high_priority_issues_cached`` always carries
    # ``open_issue_count_capped`` (default False). Every other content key is emitted
    # only when it has something, so for those an empty value still counts.
    # Arch-ruled (01M84VT64G, 2026-11-23): exactly these three keys. Widening this set is
    # a ruling, not a code edit.
    empty_is_no_content=frozenset(
        {"high_priority_issues", "open_issue_count", "open_issue_count_capped"}
    ),
)


def _content_keys(domain_context: Dict[str, Any]) -> list:
    """The keys that keep the floor running: content with a value that counts, and
    any key the classification does not know (fail towards today's behaviour)."""
    found = []
    for key, value in domain_context.items():
        if key in KEY_CLASSIFICATION.status_or_own_record:
            continue
        if key in KEY_CLASSIFICATION.empty_is_no_content and not value:
            continue
        found.append(key)
    return found


def github_kind(domain_context: Dict[str, Any]) -> Optional[str]:
    """The GitHub state B has words for, or None (connected and healthy, or never
    read). Checked in Arch's order."""
    if domain_context.get("integrations_source_failed"):
        return KIND_COULD_NOT_CHECK
    if domain_context.get("github_needs_reconnecting"):
        return KIND_NEEDS_RECONNECTING
    if "github_connected" in domain_context and not domain_context["github_connected"]:
        return KIND_NEVER_CONNECTED
    return None


def status_all_code_result(
    intent: Any,
    category: str,
    block: str,
    project: Optional[str],
    domain_context: Dict[str, Any],
    milestone_prefix: str,
) -> Optional[Any]:
    """The all-code ``IntentProcessingResult`` for this status turn, or None (the floor
    runs as today). ``domain_context`` is the floor's context AFTER ``without_todo_keys``."""
    if not block or not project or milestone_prefix:
        return None
    if _content_keys(domain_context):
        return None
    kind = github_kind(domain_context)
    if kind is None:
        return None
    from services.intent.intent_service import IntentProcessingResult

    logger.info(
        "status_all_code_reply",
        kind=kind,
        context_keys=sorted(domain_context.keys()),
    )
    return IntentProcessingResult(
        success=True,
        message=f"{GITHUB_LINES[kind].format(project=project)}\n\n{block}",
        intent_data={
            "category": category,
            "action": intent.action,
            "confidence": intent.confidence,
            "original_message": intent.original_message,
            "floor_hit": False,
            "status_all_code": kind,
            "context_keys": list(domain_context.keys()),
        },
        workflow_id=None,
        requires_clarification=False,
    )
