"""#1510 FTUX-TRUST — compose vs. execute: the collaborate-first gate.

PM's spec (2026-08-07, verbatim): "It clearly does not involve writing out
anywhere by default. Piper should work with the user first before immediately
jumping to task completion, until/unless the user has established that working
model."

What lives here (the UNGATED half, per PPM's 2026-08-09 unblock memo):

1. **The declaration surface** — a per-user declared working mode:
   - ``WorkingMode.COLLABORATE`` (the default; nobody has to declare it):
     Piper drafts/proposes and checks in before external writes when the
     request isn't an explicit imperative.
   - ``WorkingMode.EXECUTE`` (explicitly declared, e.g. "just do things
     directly from now on"; revertible, e.g. "ask me first from now on"):
     ambiguous requests escalate to direct execution.
   Persisted per-user in the ``users.preferences`` JSONB column — the
   existing DB-backed preference store (#1422; same store the onboarding
   formality writer and ``PersonalityProfile.load_with_preferences`` use).
   Deliberately NOT ``UserPreferenceManager``: that store is in-memory and
   per-instance — a "persisted" mode there would silently reset on restart.

2. **Framing classification** — deterministic compose / execute / ambiguous
   read of the request phrasing. Explicit framing wins both ways: a compose
   ask ("help me write…") collaborates even in execute mode (executing a
   request for drafting HELP is the Jake failure again), and an explicit
   imperative ("create an issue…") executes even in collaborate mode. Only
   AMBIGUOUS framing consults the declared mode — that is the "tied to the
   declared mode, not hardcoded per-verb" requirement.

3. **The gate decision** (``gate_holds``) + the collaboration/confirmation
   copy the wired handler surfaces.

Layer context (diagnosed 2026-08-09): the Understanding layer cannot express
compose-vs-execute — the classifier prompt has no compose-side action name
for issue writes, so "help me write a ticket about X" emits create_ticket —
and the Acting layer executed any classified write action unconditionally.
The classifier half is routing-moratorium material (corpus/inversion); this
module is the action-layer half, which is where a declared-mode gate belongs
regardless: deterministic, mode-tied, and testable.

Deliberately NOT built (blocked pending PM, per PPM memo): anything
inferential — counters, per-kind thresholds, trust decay, graduation
matrices. Do not add them here without PM's ruling on the #1510 fork.
"""

from __future__ import annotations

import logging
import re
from enum import Enum
from typing import Optional

logger = logging.getLogger(__name__)

WORKING_MODE_PREF_KEY = "working_mode"
"""users.preferences JSONB key holding the declared working mode ('collaborate'/'execute')."""


class WorkingMode(str, Enum):
    """The user's declared compose-vs-execute working model (#1510)."""

    COLLABORATE = "collaborate"
    EXECUTE = "execute"


# Framing verdicts (strings, not an enum — they travel into log lines and tests)
FRAMING_COMPOSE = "compose"
FRAMING_EXECUTE = "execute"
FRAMING_AMBIGUOUS = "ambiguous"


# TODO(#1510): replace with WorkflowEntry.effect once the enum lands
# (READ < WRITE < DESTRUCTIVE is being added to WorkflowEntry in a parallel
# change; this local mapping is the agreed integration point until then).
# Deliberately covers ONLY the create-issue family — the wired gate site for
# the #1510 ungated half. Extending to close/reopen/comment awaits both the
# effect enum and coordination with #1190 (destructive-mutation confirmation),
# whose confirmation-turn design owns those verbs.
GATED_WRITE_ACTIONS = frozenset(
    {
        "create_issue",
        "create_github_issue",
        "create_item",
        "create_ticket",
        "make_github_issue",
        "new_github_issue",
    }
)


# ---------------------------------------------------------------------------
# Framing classification (deterministic)
# ---------------------------------------------------------------------------

# Compose markers: the user is asking to WORK ON the artifact together.
# "draft" is compose by definition — a draft is the thing you make before
# filing, so even imperative "draft a ticket…" is a compose ask.
_COMPOSE_RE = re.compile(
    r"""
    \bhelp\s+me\b
    | \blet'?s\b
    | \bcan\s+we\b | \bcould\s+we\b | \bshould\s+we\b
    | \btogether\b
    | \bwork\s+with\s+me\b
    | \bdraft\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Execute markers: an explicit imperative aimed at the write itself, allowing
# politeness/address prefixes ("please…", "hey piper, …", "can you…").
_EXECUTE_RE = re.compile(
    r"^\s*"
    r"(?:(?:please|hey|hi|ok(?:ay)?|piper)[,!\s]+)*"
    r"(?:go\s+ahead\s+and\s+)?"
    r"(?:(?:can|could|would|will)\s+you\s+(?:please\s+)?)?"
    r"(?:create|file|open|make|add|submit|log)\b",
    re.IGNORECASE,
)


def classify_framing(message: Optional[str]) -> str:
    """Deterministic compose/execute/ambiguous read of a request's phrasing.

    Compose markers are checked first so "help me create a ticket…" reads as
    compose, not execute. Anything with neither marker is AMBIGUOUS — and
    ambiguity is exactly what the declared mode (default: collaborate) decides.
    """
    text = (message or "").strip()
    if not text:
        return FRAMING_AMBIGUOUS
    if _COMPOSE_RE.search(text):
        return FRAMING_COMPOSE
    if _EXECUTE_RE.search(text):
        return FRAMING_EXECUTE
    return FRAMING_AMBIGUOUS


# ---------------------------------------------------------------------------
# Mode declarations (the declaration surface, detection half)
# ---------------------------------------------------------------------------

# A declaration is a STANDING instruction, so it needs a durative marker
# ("from now on", "going forward", …) — a bare "just do it" is a one-off nudge
# about the current task, not a working-model change. "go back to…" carries
# its own durativity (it names a standing state to return to).
_DURATIVE_RE = re.compile(
    r"\b(?:from\s+now\s+on|going\s+forward|in\s+(?:the\s+)?future|always|"
    r"go\s+back\s+to)\b",
    re.IGNORECASE,
)

# Collaborate-mode declarations / reverts. Checked FIRST: negated execute
# phrasings ("stop doing things directly…") contain execute-ish substrings.
_COLLAB_DECL_RE = re.compile(
    r"""
    \bcheck(?:ing)?\s+with\s+me\b
    | \bask(?:ing)?\s+(?:me\s+)?(?:first|before)\b
    | \bdrafts?\s+first\b
    | \bwork(?:ing)?\s+with\s+me\b
    | \bcollaborat(?:e|ing|ion)\b
    | \bstop\s+(?:just\s+)?doing\s+things\s+directly\b
    | \bdon'?t\s+just\s+do\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

# Execute-mode declarations (PM's example: "just do things directly from now on").
_EXEC_DECL_RE = re.compile(
    r"""
    \bjust\s+do\s+(?:things|it|them)\b
    | \bdo\s+things\s+directly\b
    | \bdon'?t\s+ask\b
    | \bno\s+need\s+to\s+(?:ask|check|confirm)\b
    | \bskip\s+the\s+(?:draft|check|confirmation)s?\b
    | \bexecute\s+mode\b
    """,
    re.IGNORECASE | re.VERBOSE,
)


def detect_mode_declaration(message: Optional[str]) -> Optional[WorkingMode]:
    """Detect an explicit working-mode declaration; None for anything else.

    Conservative on purpose: requires a durative marker so task requests and
    one-off nudges never flip a standing mode. Collaborate/revert phrasings
    win over execute phrasings (negations contain execute substrings).
    """
    text = (message or "").strip()
    if not text or not _DURATIVE_RE.search(text):
        return None
    if _COLLAB_DECL_RE.search(text):
        return WorkingMode.COLLABORATE
    if _EXEC_DECL_RE.search(text):
        return WorkingMode.EXECUTE
    return None


# ---------------------------------------------------------------------------
# Persistence — users.preferences JSONB (the existing per-user pref store)
# ---------------------------------------------------------------------------


async def _load_preferences(user_id: str) -> dict:
    """Read users.preferences for one user. Seam kept tiny for testability."""
    from sqlalchemy import select

    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope() as session:
        row = await session.execute(select(User.preferences).where(User.id == str(user_id)))
        prefs = row.scalar_one_or_none()
        return prefs or {}


async def _save_preference(user_id: str, key: str, value) -> bool:
    """Write one key into users.preferences. False if the user row is absent."""
    from sqlalchemy import select

    from services.database.models import User
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope() as session:
        result = await session.execute(select(User).where(User.id == str(user_id)))
        user = result.scalar_one_or_none()
        if user is None:
            return False
        # New dict on purpose: reassignment is what marks the JSONB column
        # dirty; mutating the existing dict in place can silently not persist.
        prefs = dict(user.preferences or {})
        prefs[key] = value
        user.preferences = prefs
        await session.commit()
        return True


async def get_working_mode(user_id: Optional[str]) -> WorkingMode:
    """The user's declared working mode; COLLABORATE when unset/unknown/error.

    Fail-safe direction is load-bearing: a storage error must degrade to
    collaborate-first (draft and ask), never escalate to direct execution.
    """
    if not user_id:
        return WorkingMode.COLLABORATE
    try:
        raw = (await _load_preferences(str(user_id))).get(WORKING_MODE_PREF_KEY)
    except Exception as e:
        logger.warning("working_mode_read_failed user_id=%s error=%s", user_id, e)
        return WorkingMode.COLLABORATE
    try:
        return WorkingMode(raw)
    except (ValueError, TypeError):
        return WorkingMode.COLLABORATE


async def set_working_mode(user_id: Optional[str], mode: WorkingMode) -> bool:
    """Persist a declared working mode. False = not persisted (be honest about it)."""
    if not user_id:
        return False
    try:
        return await _save_preference(str(user_id), WORKING_MODE_PREF_KEY, mode.value)
    except Exception as e:
        logger.warning("working_mode_write_failed user_id=%s error=%s", user_id, e)
        return False


# ---------------------------------------------------------------------------
# The gate decision
# ---------------------------------------------------------------------------


async def gate_holds(action: Optional[str], message: Optional[str], user_id: Optional[str]) -> bool:
    """True → collaborate (draft + ask) instead of executing this action.

    Semantics (#1510, collaborate-first):
    - Non-gated actions never hold (this gate covers external writes only).
    - COMPOSE framing always holds — an explicit ask for drafting help is
      collaboration by definition, whatever the declared mode.
    - EXECUTE framing never holds — explicit imperatives keep working; the
      default confiscates ambiguity, not imperatives.
    - AMBIGUOUS framing is decided by the declared mode: collaborate-first
      unless the user has established EXECUTE ("just do things directly from
      now on"). Mode-tied, not per-verb.
    """
    if action not in GATED_WRITE_ACTIONS:
        return False
    framing = classify_framing(message)
    if framing == FRAMING_COMPOSE:
        return True
    if framing == FRAMING_EXECUTE:
        return False
    return (await get_working_mode(user_id)) is not WorkingMode.EXECUTE


# ---------------------------------------------------------------------------
# Copy builders (deterministic, no LLM — testable and honest)
# ---------------------------------------------------------------------------


def build_collaboration_response(
    subject: Optional[str] = None, repository: Optional[str] = None
) -> str:
    """The collaborate-first reply for a gated issue-write: draft + ask.

    Proposes a starting draft grounded in what was extractable from the
    request and asks the user to shape it — it never announces a write.
    """
    if subject:
        where = f" in **{repository}**" if repository else ""
        return (
            "Happy to shape this with you before anything gets filed. "
            f"Here's a draft to start from{where}:\n\n"
            f"**Title**: {subject}\n\n"
            "What should the body say — the problem, steps to reproduce, "
            "impact? Tell me what to add or change, and when it looks right, "
            'say something like "create this issue in owner/repo about '
            f'{subject}" and I\'ll file it. '
            "(If you'd rather I just file things directly, say "
            '"just do things directly from now on" and I will.)'
        )
    return (
        "Happy to work on this ticket with you before anything gets filed. "
        "What's it about? A sentence on the problem is plenty — we can shape "
        "the title and details together from there. "
        "(If you'd rather I just file things directly, say "
        '"just do things directly from now on" and I will.)'
    )


def mode_confirmation_message(mode: WorkingMode, persisted: bool) -> str:
    """Confirmation copy for a working-mode declaration.

    ``persisted=False`` must be visible to the user — claiming a durable mode
    change that didn't save would be a confabulated capability.
    """
    if mode is WorkingMode.EXECUTE:
        msg = (
            "Got it — I'll act on your requests directly from now on. "
            'Say "ask me first from now on" any time and I\'ll go back to '
            "drafting things with you before acting."
        )
    else:
        msg = (
            "Got it — I'll draft and check with you before taking action "
            'from now on. Say "just do things directly from now on" if you '
            "want me to act without checking."
        )
    if not persisted:
        msg += (
            "\n\n(Heads up: I couldn't save that preference just now, so it "
            "may not stick across sessions.)"
        )
    return msg
