"""
Universal escape detection for guided processes (#1529, FLOW-ESCAPE).

Issue #1529: a guided flow (the standup interview) hijacked a live PM session —
five explicit commands, including "i am not doing the standup right now", were
transcribed INTO the standup as answers, and "end standup" fell through to a
classifier and misrouted. The #888 escape hatch only recognized six exact-match
words; the #899 off-topic layer declared any message containing the word
"standup" ON-topic — so refusals that NAMED the flow were the most reliably
swallowed messages of all.

This module is the deterministic escape check that runs at the guided-process
seam (ProcessRegistry.check_active_processes) BEFORE a flow is allowed to
consume a turn, and before any classifier sees the message. It is flow-generic:
any registered process gets the same three checks.

Three signal kinds, most-specific first:

1. **exit** — the whole message is an exit command aimed at the flow:
   "end standup", "stop the standup", "cancel this", "quit", plus bare forms
   ("never mind", "not now", "forget it"). The flow is CLOSED (not suspended —
   a suspended flow re-offers itself, which is the nag loop #1529 documents)
   and the turn is claimed with honest exit copy.
2. **refusal** — the message contains a refusal clause naming the flow:
   "i am not doing the standup right now", "i don't want to do the standup",
   "no standup". The flow is closed. If the message carries residual content
   beyond the refusal ("… restore CoVa"), the turn falls through to normal
   intent processing with an honest exit prefix, so the user's actual request
   gets answered.
3. **off_intent** — the message is a clear cross-domain ACTION the flow cannot
   use ("restore CoVa", "remind me to …", "create an issue …"). Option A UX
   (#899, PM-ratified): pause the flow and let normal processing answer.
   The verb list is deliberately MINIMAL — only shapes no guided flow could
   ever consume as an answer. This is a stopgap the understanding-layer
   inversion rebuild replaces; do not grow it into a router.

Scope note (routing-fix moratorium, Lead 2026-08-08): this is context-carrying
seam work — the check only ever runs while a guided flow holds (or is about to
claim) the turn. It adds NO pre-classifier patterns and dies with the rebuild.

**#1617 — the completion tail (PM live 2026-08-13 3:29–3:30 PM)**: after the
standup interview's final summary, the flow's tail states ('share this or
save your preferences?' / 'anything else?') kept claiming turns — "change the
status of issue #108 to Done" was consumed TWICE as a tail response (the
REFINING acceptance substring matched the word "Done"). The instructive
asymmetry in the same transcript: the working-mode declaration ("do things
directly from now on") DID escape — because its deterministic detector
(collaboration_gate.detect_mode_declaration) runs at the very top of
process_intent, ABOVE the guided-process claim. The generalization here is
that same property granted through THIS seam rather than a new pre-claim
special case: in a completion tail, a turn that one of the codebase's
deterministic full-confidence cross-domain detectors claims (currently the
#1411 Stage-0 explicit-issue-update detector, DELEGATED — never a copied
pattern) is off_intent, and the registry RELEASES the delivered flow
(terminal, no resume nag) instead of suspending it. Tail-only on purpose:
mid-gathering, "I need to change the status of issue #108 to Done" is a
legitimate standup answer; after the summary has been delivered it can only
be a command.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Dict, List, Optional, Pattern

import structlog

from services.process.registry import ProcessType

logger = structlog.get_logger(__name__)


# --- Flow vocabulary -------------------------------------------------------

# How a user refers to each flow in natural language. SLOT_FILLING has no
# user-facing name; it is reachable through the generic words only.
_FLOW_WORDS: Dict[ProcessType, Optional[str]] = {
    ProcessType.STANDUP: r"(?:daily\s+)?stand[\s\-]?up",
    ProcessType.ONBOARDING: r"on[\s\-]?boarding",
    ProcessType.SLOT_FILLING: None,
    ProcessType.PLANNING: r"planning(?:\s+session)?",
    ProcessType.FEEDBACK: r"feedback(?:\s+session)?",
    ProcessType.CLARIFICATION: None,
}

# Generic references that mean "whatever flow is currently running".
_GENERIC_FLOW_WORDS = (
    r"this|it|that|the\s+process|this\s+process|the\s+flow|this\s+flow|"
    r"this\s+conversation|the\s+interview|this\s+interview"
)

_EXIT_VERBS = r"end|stop|cancel|quit|exit|abort"

# Bare full-message exits that extend the #888 ESCAPE_COMMANDS frozenset.
# (#888's set — cancel/exit/stop/skip/quit/never mind — is checked by the
# registry before this module runs; these are the additions #1529 evidenced.)
BARE_EXIT_COMMANDS: frozenset = frozenset(
    {
        "nevermind",
        "not now",
        "forget it",
        "stop it",
    }
)


def _flow_words_for(process_type: ProcessType, include_generic: bool = True) -> str:
    """Alternation of ways the user might name this flow."""
    specific = _FLOW_WORDS.get(process_type)
    parts: List[str] = []
    if specific:
        parts.append(specific)
    if include_generic:
        parts.append(_GENERIC_FLOW_WORDS)
    return "|".join(parts)


def _exit_re(process_type: ProcessType) -> Pattern[str]:
    """Full-message exit command aimed at this flow: 'end standup', 'stop this'."""
    words = _flow_words_for(process_type)
    return re.compile(
        rf"^(?:please\s+)?(?:let'?s\s+)?(?:{_EXIT_VERBS})\s+"
        rf"(?:the\s+|this\s+|my\s+)?(?:{words})"
        rf"(?:\s+(?:now|please|for\s+now|for\s+today))?\s*[.!?]*$",
        re.IGNORECASE,
    )


def _refusal_res(process_type: ProcessType) -> List[Pattern[str]]:
    """Refusal clauses aimed at this flow.

    Two precision tiers, because generic pronouns are dangerous mid-flow
    (a standup answer like "I'm not going to do that refactor today" must
    NOT read as a refusal of the standup):

    - **Flow-specific words** ("standup") → clause-level, matched anywhere,
      so residual content ("… restore CoVa") survives to be answered.
    - **Generic pronouns** ("this", "it") → full-message only; when the whole
      message is "i'm not doing this right now" there is nothing else it can
      be about.
    """
    trailing = r"(?:\s+(?:right\s+now|now|today|at\s+the\s+moment|yet))?"
    article = r"(?:the\s+|this\s+|my\s+|a\s+)?"
    refuse_verb = r"(?:doing|going\s+to\s+do|gonna\s+do|up\s+for)"
    dont_want = r"(?:don'?t|do\s+not|won'?t|will\s+not)\s+want\s+(?:to\s+(?:do\s+)?)?"

    patterns: List[Pattern[str]] = []
    specific = _FLOW_WORDS.get(process_type)

    if specific:
        patterns.extend(
            [
                # "i am not doing the standup right now" — clause-level
                re.compile(
                    rf"\bi\s*(?:'m|am|’m)?\s*not\s+{refuse_verb}\s+{article}(?:{specific}){trailing}",
                    re.IGNORECASE,
                ),
                # "i don't want to do the standup" — clause-level
                re.compile(
                    rf"\bi\s+{dont_want}{article}(?:{specific}){trailing}",
                    re.IGNORECASE,
                ),
                # "let's not do the standup" — clause-level
                re.compile(
                    rf"\blet'?s\s+not\s+(?:do\s+)?{article}(?:{specific}){trailing}",
                    re.IGNORECASE,
                ),
                # "no standup" — full message
                re.compile(
                    rf"^no\s+(?:{specific})(?:\s+(?:right\s+now|now|today|please))?\s*[.!]*$",
                    re.IGNORECASE,
                ),
                # Exit command as a leading clause of a longer message:
                # "stop the standup and restore CoVa"
                re.compile(
                    rf"\b(?:{_EXIT_VERBS})\s+{article}(?:{specific})\b",
                    re.IGNORECASE,
                ),
            ]
        )

    # Generic-pronoun refusals — FULL MESSAGE only (see docstring)
    patterns.extend(
        [
            re.compile(
                rf"^i\s*(?:'m|am|’m)?\s*not\s+{refuse_verb}\s+{article}(?:{_GENERIC_FLOW_WORDS}){trailing}\s*[.!]*$",
                re.IGNORECASE,
            ),
            re.compile(
                rf"^i\s+{dont_want}{article}(?:{_GENERIC_FLOW_WORDS}){trailing}\s*[.!]*$",
                re.IGNORECASE,
            ),
            re.compile(
                rf"^let'?s\s+not\s+(?:do\s+)?{article}(?:{_GENERIC_FLOW_WORDS}){trailing}\s*[.!]*$",
                re.IGNORECASE,
            ),
        ]
    )
    return patterns


# Cross-domain ACTION shapes no guided flow could consume as an answer.
# Deliberately minimal (see module docstring) — the evidenced #1529 case is
# "restore CoVa" typed mid-standup.
_OFF_INTENT_RES: List[Pattern[str]] = [
    re.compile(r"^(?:please\s+)?(?:restore|unarchive)\s+\S+", re.IGNORECASE),
    re.compile(r"^(?:please\s+)?remind\s+me\b", re.IGNORECASE),
    re.compile(
        r"^(?:please\s+)?(?:create|open|file)\s+(?:an?\s+|a\s+new\s+)?(?:issue|ticket|bug)\b",
        re.IGNORECASE,
    ),
]


# --- Result model ----------------------------------------------------------


@dataclass
class EscapeSignal:
    """A detected escape from a guided flow.

    kind: "exit" | "refusal" | "off_intent"
    matched: the text span (or pattern name) that fired, for logging
    residual: for refusals — the message content beyond the refusal clause,
        or None when the refusal was the whole message.
    """

    kind: str
    matched: str
    residual: Optional[str] = None


# --- Detection -------------------------------------------------------------


def detect_flow_exit(message: str, process_type: ProcessType) -> bool:
    """True when the whole message is an exit command aimed at this flow.

    Also used OUTSIDE the active seam: `_check_pending_resume_offer` (#889)
    consults it so "end standup" against a SUSPENDED standup abandons the
    flow deterministically instead of falling to a classifier (#1529 part 3 —
    the 'end standup' → todo-complete misroute).
    """
    if not message:
        return False
    stripped = message.strip()
    if stripped.lower().rstrip(".!?") in BARE_EXIT_COMMANDS:
        return True
    return bool(_exit_re(process_type).match(stripped))


def _residual_after(message: str, start: int, end: int) -> Optional[str]:
    """Message content outside the matched clause, cleaned of connectives."""
    residual = (message[:start] + " " + message[end:]).strip()
    residual = re.sub(r"^(?:[.,;:!?\s]|and\b|then\b|but\b|so\b)+", "", residual, flags=re.IGNORECASE)
    residual = residual.strip(" .,;:!?")
    return residual if len(residual) >= 3 else None


def _detect_tail_cross_domain_action(message: str) -> Optional[str]:
    """#1617: deterministic cross-domain detection for COMPLETION-TAIL turns,
    DELEGATED to the existing detectors (never a parallel pattern copy — the
    #1555 rule). Currently: the #1411 Stage-0 explicit-issue-update detector
    ("change the status of issue #108 to Done"). Returns a match label for
    logging, or None. Guarded: a detector import/failure must never trap the
    user in the flow (same posture as the registry's escape wrapper)."""
    try:
        from services.intent_service.classifier import _detect_explicit_issue_update

        issue_number = _detect_explicit_issue_update(message)
    except Exception as e:  # pragma: no cover - defensive import guard
        logger.warning("tail_cross_domain_detection_failed", error=str(e))
        return None
    if issue_number is not None:
        return f"explicit_issue_update:#{issue_number}"
    return None


def check_escape(
    message: str,
    process_type: ProcessType,
    in_completion_tail: bool = False,
) -> Optional[EscapeSignal]:
    """Run the three escape checks, most-specific first.

    Returns None when the message should proceed to the flow's handler.

    ``in_completion_tail`` (#1617): the flow has already delivered its result
    and is in a post-summary tail state — the off_intent tier additionally
    consults the deterministic cross-domain detectors (see
    :func:`_detect_tail_cross_domain_action`), because in a tail state an
    off-tail-shaped turn can only be a command the user wants answered.
    """
    if not message or not message.strip():
        return None
    stripped = message.strip()

    # 1. Full-message exit
    if detect_flow_exit(stripped, process_type):
        return EscapeSignal(kind="exit", matched=stripped.lower())

    # 2. Refusal clause (possibly with residual content to answer)
    for pattern in _refusal_res(process_type):
        m = pattern.search(stripped)
        if m:
            return EscapeSignal(
                kind="refusal",
                matched=m.group(0),
                residual=_residual_after(stripped, m.start(), m.end()),
            )

    # 3. Cross-domain action the flow can't use
    for pattern in _OFF_INTENT_RES:
        m = pattern.search(stripped)
        if m:
            return EscapeSignal(kind="off_intent", matched=m.group(0))

    # 3b. #1617 tail-only: deterministic detectors' turf is off_intent here.
    if in_completion_tail:
        matched = _detect_tail_cross_domain_action(stripped)
        if matched is not None:
            return EscapeSignal(kind="off_intent", matched=matched)

    return None


# --- Honest exit copy ------------------------------------------------------

_EXIT_COPY: Dict[ProcessType, str] = {
    ProcessType.STANDUP: (
        "Okay — I've ended the standup. Say '/standup' whenever you want to start a fresh one."
    ),
    ProcessType.ONBOARDING: "Okay — I've ended onboarding. You can restart it anytime.",
    ProcessType.SLOT_FILLING: "Okay — I've dropped what we were filling in.",
}

_REFUSAL_PREFIX: Dict[ProcessType, str] = {
    ProcessType.STANDUP: "Okay — no standup. I've ended it.",
    ProcessType.ONBOARDING: "Okay — no onboarding. I've ended it.",
    ProcessType.SLOT_FILLING: "Okay — I've dropped what we were filling in.",
}


def format_exit_message(process_type: ProcessType) -> str:
    """Honest copy for a claimed exit turn."""
    return _EXIT_COPY.get(process_type, "Okay — I've ended that.")


def format_refusal_prefix(process_type: ProcessType) -> str:
    """Honest prefix prepended when a refusal carries residual content that
    normal intent processing goes on to answer."""
    return _REFUSAL_PREFIX.get(process_type, "Okay — I've ended that.")


_RELEASE_PREFIX: Dict[ProcessType, str] = {
    ProcessType.STANDUP: "(Your standup's all set — on to your request.)",
    ProcessType.ONBOARDING: "(Onboarding's wrapped — on to your request.)",
}


def format_release_prefix(process_type: ProcessType) -> str:
    """#1617: honest prefix when a COMPLETED flow releases at an off-tail
    turn — the flow's work stands, and normal processing answers the turn."""
    return _RELEASE_PREFIX.get(process_type, "(That's wrapped up — on to your request.)")
