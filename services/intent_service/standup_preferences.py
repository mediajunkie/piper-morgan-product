"""#1591 (Production/PUB half) — standup-mode preference capture + interview
invitation, as a CONSUMER of the #1510 verified-inference rail.

This module is wiring only. The mechanism — confidence gate, read-back offer,
session decline memory, verified-inference store — lives in
``services/intent_service/verified_inference.py`` and is used as-is (the
#1591 connective ruling: "the invitation IS the read-back … the mechanisms
converge. No redesign needed"). Nothing here forks or extends the rail.

The governing spec (issue #1591 + its comments):

- **CXO's three invitation properties**: (1) report first and complete;
  (2) invitation after, and cheap to decline; (3) declining changes nothing
  else — "the report is unconditional or it is a bargaining chip."
- **PPM's empty-case rule** (a different rule taking over, not an exception):
  when the read produced NOTHING, "demonstrate, then ask" has nothing to
  demonstrate — fail honestly and offer, invitation FIRST. The discriminator
  is whether the read produced anything (``StandupSummary.is_empty()``).
- **One preference persistence** (PPM+CXO): the standup grows NO local
  preference store. The mode preference lives in the rail's
  verified-inference store (users.preferences JSONB) under
  ``STANDUP_MODE_KEY``; reads go through ``get_verified_inference`` ("stored
  — not re-inferred each time"), writes only through the rail's read-back
  acceptance (source=user_verified) or its meta-endorsed apply
  (source=meta_auto).
- **#1532**: every read/write carries user_id; **#1603**: str at the
  String-column boundary (the rail normalizes; we pass str-able ids only).

What IS here:

- The **mode-choice tally**: transient, in-process evidence of which standup
  mode a user keeps choosing (the inference INPUT). Deliberately NOT a
  preference store — it persists nothing, shadows nothing, and is exactly
  the ``_SESSION_DECLINES`` lifetime class the rail already sanctions for
  transient conversational state. Losing it costs one re-observation, never
  a stored preference.
- The **inference**: majority mode chosen >= 2 times → a signal whose
  confidence feeds the rail's shared gate (``verified_inference.decide`` over
  preference_detection's thresholds — one scoring system, #1510).
- The **invitation offer**: the plain "try the guided interview" offer for
  turns with no inferable signal. It binds via the SAME #846 pending-offer
  carrier the rail uses (#1529 ordering — offer beats resume-check — holds by
  construction), and reuses the rail's session decline memory for its
  anti-nag ("no re-ask this session"), keyed under its own name.
"""

from __future__ import annotations

import logging
import re
from typing import Any, Dict, Optional, Tuple

from services.intent_service import verified_inference as vi

logger = logging.getLogger(__name__)

# The rail-store key for the user's standup-mode preference ("what kind of
# standup do you want going forward" — the #1591 capture question).
STANDUP_MODE_KEY = "standup_mode"

# The two modes (#1511: "two standups wear one name"). ⛔ Per PM's explicit
# veto on #1591: no per-user standup templating — two modes is the ceiling.
MODE_REPORT = "report"  # derived on-demand report (#1269, StandupAssembler)
MODE_INTERVIEW = "interview"  # interactive interview (#585, StandupConversationHandler)

# Human phrasing of the inference for the rail's read-back question — the
# consumer knows how to say its own inference (build_read_back_offer contract).
MODE_DESCRIPTIONS = {
    MODE_REPORT: "that you'd like the quick derived report as your usual standup",
    MODE_INTERVIEW: "that you'd like the guided interview as your usual standup",
}

# Offer-acceptance-only workflow that starts the EXISTING #585 interview
# (registered in workflow_entries with action_triggered=False, mirroring
# verify_inference — the classifier/rail can never emit it).
STANDUP_INTERVIEW_WORKFLOW = "standup_interview"

# pending_action ``kind`` marker for the invitation offer (the #1190 carrier
# is action-agnostic; ``kind`` is how seams recognize an offer family without
# a parallel store — same pattern as VERIFY_INFERENCE_KIND).
INVITE_KIND = "standup_interview_invitation"

# Key under which an invitation decline is recorded in the RAIL's
# session-scoped decline memory (vi.mark_declined / vi.was_declined) — reusing
# the sanctioned anti-nag mechanism rather than inventing a second one.
INVITE_DECLINE_KEY = "standup_interview_invitation"

# ---------------------------------------------------------------------------
# #1591 declaration path (PM live 2026-08-13) — a DIRECT declaration turn
# ---------------------------------------------------------------------------
# PM: "use the standup interview format by default from now on" → the floor
# improvised an unstored promise that broke two turns later. The wiring below
# infers preference from BEHAVIOR; a declaration is the highest-confidence
# signal there is and had no path to the store. Scope (sanctioned): ONLY
# standup-token phrasings — they ride the already-claiming standup surface as
# an in-handler branch (#1431 pattern; no new pre-classifier patterns, no
# claim widening under the moratorium). The tokenless "use the interview from
# now on" is a #1595 corpus row, deliberately NOT claimed here.
#
# A declaration composes with the rail as STORE + CONFIRMATION COPY, never a
# read-back (reading the user's own words back as a question would be
# verification theater) — stored source=user_declared, confidence 1.0.

_INTERVIEW_TOKEN_RE = re.compile(r"\binterview\b|\binteractive\b", re.IGNORECASE)
_REPORT_TOKEN_RE = re.compile(r"\breport\b|\bquick\b", re.IGNORECASE)
# "back to X" names a standing state to return to — the switch-back marker
# the confirmation copy below teaches ("back to my standup report").
_SWITCH_BACK_RE = re.compile(r"\bback\s+to\b", re.IGNORECASE)


def detect_standup_mode_declaration(message: Optional[str]) -> Optional[str]:
    """Detect a standing standup-mode declaration; None for anything else.

    Requires ALL of: the standup token (scope — see block comment), exactly
    one mode direction (interview xor report tokens; both present is
    ambiguous → no declaration), and durativity — the shared working-mode
    durative vocabulary (``collaboration_gate.has_durative_marker``, composed
    not copied) or the switch-back marker. One-off asks ("my standup
    interview") carry no durative marker and are untouched.
    """
    text = (message or "").strip()
    if not text or "standup" not in text.lower():
        return None
    from services.intent_service.collaboration_gate import has_durative_marker

    if not (has_durative_marker(text) or _SWITCH_BACK_RE.search(text)):
        return None
    wants_interview = bool(_INTERVIEW_TOKEN_RE.search(text))
    wants_report = bool(_REPORT_TOKEN_RE.search(text))
    if wants_interview == wants_report:  # neither, or both (ambiguous)
        return None
    return MODE_INTERVIEW if wants_interview else MODE_REPORT


def declaration_confirmation(mode: str, persisted: bool) -> str:
    """Confirmation copy for a stored declaration — states the new standing
    default and teaches the ROUTABLE switch-back phrase (#1571: never teach a
    phrase that doesn't route; both taught phrases carry the 'my standup' cue
    _is_standup_query claims, so they resolve deterministically).
    ``persisted=False`` must be visible (collaboration_gate's honesty rule —
    claiming a durable change that didn't save is a confabulated capability).
    """
    if mode == MODE_INTERVIEW:
        msg = (
            "Interview by default from now on — got it. Say 'back to my "
            "standup report' any time to switch back."
        )
    else:
        msg = (
            "Quick report by default from now on — got it. Say 'my standup "
            "interview' any time for the guided version."
        )
    if not persisted:
        msg += (
            "\n\n(Heads up: I couldn't save that preference just now, so it "
            "may not stick across sessions.)"
        )
    return msg


# The honest reply when a declaration arrives with no signed-in user: there
# is no store to write (#1532 — the preference is the USER's), and claiming
# otherwise would be the exact fabricated promise this path exists to replace.
DECLARATION_NO_USER_MESSAGE = (
    "I can't save a standing standup preference without a signed-in user. "
    "Say 'my standup interview' for the guided version any time, or 'my "
    "standup report' for the quick one."
)


# ---------------------------------------------------------------------------
# Mode-choice tally (transient inference EVIDENCE — not a preference store)
# ---------------------------------------------------------------------------
# Same in-memory, capped, process-lifetime class as the rail's
# _SESSION_DECLINES: nothing here persists or shadows users.preferences
# (the PPM+CXO one-store rule governs preferences; an observation count is
# not one). Keyed by user_id — the signal is the USER's behavior (#1532),
# not the session's. Eviction is oldest-user-first (dict insertion order).

_MODE_CHOICES: Dict[str, Dict[str, int]] = {}
_MODE_CHOICES_MAX_USERS = 2048

# Signal shape: a mode chosen once is not a pattern — the first choice gets
# the plain invitation, never a fabricated "you seem to prefer…" read-back.
_MIN_CHOICES_FOR_SIGNAL = 2
# Confidence ramp: 2 choices → 0.55, 3 → 0.70, 4 → 0.85, 5+ → 0.95 (cap).
# Feeds the SHARED gate (preference_detection thresholds via vi.decide):
# below 0.9 reads back; sustained repetition (5+) crosses the auto-apply bar.
_SIGNAL_BASE = 0.4
_SIGNAL_STEP = 0.15
_SIGNAL_CAP = 0.95


def record_mode_choice(user_id: Optional[str], mode: str) -> None:
    """Record that this user chose a standup mode (an OBSERVED choice — the
    interview token, the explicit report token, or a served non-empty report;
    an empty render demonstrates nothing and is never recorded)."""
    if not user_id or mode not in (MODE_REPORT, MODE_INTERVIEW):
        return
    uid = str(user_id)
    if uid not in _MODE_CHOICES and len(_MODE_CHOICES) >= _MODE_CHOICES_MAX_USERS:
        _MODE_CHOICES.pop(next(iter(_MODE_CHOICES)))
    tally = _MODE_CHOICES.setdefault(uid, {})
    tally[mode] = tally.get(mode, 0) + 1


def infer_mode_signal(user_id: Optional[str]) -> Optional[Tuple[str, float]]:
    """The #1591 inference: (mode, confidence) when the user has REPEATEDLY
    chosen one mode (strict majority, >= 2 choices), else None.

    The confidence is an input to the rail's shared gate — this function
    never decides read-back vs apply itself (one scoring system, #1510).
    A tie or a single choice is no signal: the honest state is "no inferable
    preference yet", which the caller answers with the plain invitation.
    """
    if not user_id:
        return None
    tally = _MODE_CHOICES.get(str(user_id))
    if not tally:
        return None
    report = tally.get(MODE_REPORT, 0)
    interview = tally.get(MODE_INTERVIEW, 0)
    if report == interview:
        return None
    mode, count = (
        (MODE_REPORT, report) if report > interview else (MODE_INTERVIEW, interview)
    )
    if count < _MIN_CHOICES_FOR_SIGNAL:
        return None
    confidence = min(_SIGNAL_BASE + _SIGNAL_STEP * (count - 1), _SIGNAL_CAP)
    return mode, confidence


# ---------------------------------------------------------------------------
# The interview invitation (CXO's three properties; PPM's empty-case lead)
# ---------------------------------------------------------------------------

# #1511's taught phrase, kept verbatim: it is deterministically claimed by
# _is_standup_query's "my standup" cue + the handler's interview token, so the
# invitation teaches a phrase that routes without the LLM classifier.
_TEACHING_LINE = "Want the guided version instead? Say 'my standup interview'."

# Appended after a COMPLETE report (CXO property 1 is the caller's job; this
# copy carries properties 2 and 3: one cheap yes, ignoring costs nothing).
INVITE_AFTER_REPORT = (
    f"{_TEACHING_LINE} Or just say yes and I'll walk you through it now — "
    "if not, the quick report stays exactly as it is."
)

# PPM's empty case: fail honestly, then the invitation IS the first move.
INVITE_EMPTY_LEAD = (
    "I don't have anything to build your standup from yet — no observed "
    "activity in your connected tools. Want to do a quick guided standup "
    "interview instead? You tell me what happened and what's ahead, and I'll "
    "put it together. (yes/no)"
)

# Property 3 made explicit at decline time: nothing changed, nothing stored,
# and the door stays visibly open (PPM: trivially revisable + visible).
INVITE_DECLINE_MESSAGE = (
    "No problem — your quick report stays exactly as it is, and I won't ask "
    "again this session. Say 'my standup interview' any time to try the "
    "guided version."
)


def build_interview_invitation(
    user_id: Optional[str], session_id: Optional[str]
) -> Optional[Dict[str, Any]]:
    """Build the invitation's pending-offer record (the #846/#1190 carrier —
    the SAME store the rail's read-back binds through, so the #1529 ordering
    holds and there is exactly one pending ask per turn), or None when it
    cannot or should not be armed:

    - no session → nothing to bind the next turn's "yes" to;
    - no user → the interview is the USER's flow (#1532) — an anonymous
      acceptance would key conversation state to nobody;
    - already declined this session → not re-asked (CXO property 2; the rail's
      session decline memory, consulted here exactly as build_read_back_offer
      consults it for read-backs).
    """
    if not session_id or not user_id:
        return None
    if vi.was_declined(session_id, INVITE_DECLINE_KEY):
        return None
    return {
        "workflow_type": STANDUP_INTERVIEW_WORKFLOW,
        "pending_action": {
            "kind": INVITE_KIND,
            # "action" keeps the #1190 carrier's field contract (the
            # off-intent abandonment log reads it) — not a rail key.
            "action": STANDUP_INTERVIEW_WORKFLOW,
            "user_id": str(user_id),
        },
        "decline_message": INVITE_DECLINE_MESSAGE,
    }
