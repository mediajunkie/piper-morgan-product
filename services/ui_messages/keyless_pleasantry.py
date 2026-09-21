"""#1818(b) — the refusal-that-acknowledges: keyless copy for the /intent gate.

PM's ruling (decisions.log 2026-09-20 13:3x): option (b) — a keyless user's first
message gets a KIND-MATCHED acknowledgment plus the key requirement, with no
exemption machinery (a greeting does not pass the gate; the gate answers it like
a person would). CXO's copy set (issue comment 5752301343, memo 2026-09-20),
verbatim; Arch's supersession ruling (memo 2026-09-20) fixes the seams:

  - FIRST keyless message, any kind → kind-matched prefix + THE shared sentence.
  - LATER keyless pleasantry (a second "hi"/"thanks") → the short form — a
    restated policy, not a re-explained one (re-explaining reads as not
    listening; CXO).
  - LATER keyless SUBSTANTIVE message → NOT this module's business: that is the
    gate's own refusal string (today `_create_user_key_required_response`;
    #1823's branch-one string when it lands). One policy, one string per layer.

🔴 The shared half is ONE constant in source, deliberately — four near-identical
sentences drift (CXO's 09-19 finding: five vendor-specific key strings against
one neutral). Compose at render time; never paste this sentence into another
string.

⚠️ `thanks` is deliberately NOT "you're welcome": nothing has been done, so
"you're welcome" would claim a service never rendered — the honest-empty family
inside a pleasantry (CXO).

Session memory is in-process and best-effort (same durability class as the #846
pending-offer store): if it's lost, a repeat visitor gets the full copy again —
mildly repetitive, never wrong.
"""

from __future__ import annotations

import re
from typing import Dict, Optional

# THE shared sentence — CXO's copy, verbatim. ONE constant (see module docstring).
KEYLESS_SHARED_KEY_SENTENCE = (
    "Piper runs on an LLM key of your own, not on anyone else's account. "
    "Add an OpenAI or Anthropic key in Settings and I'll be ready when you are."
)

# Kind-matched acknowledgments — CXO's copy, verbatim.
KEYLESS_KIND_PREFIXES: Dict[str, str] = {
    "greeting": "Hello — good to meet you.",
    "farewell": "Goodbye for now.",
    "thanks": "That's kind — though I haven't actually done anything yet.",
    "neutral": "I'd like to help with that.",
}

# CXO's short form for a REPEATED keyless pleasantry (Arch's split, CXO-confirmed
# 2026-09-20: pleasantries only — a repeated substantive request is the gate's
# string, not this).
KEYLESS_REPEAT_SHORT_FORM = (
    "I'll need that key before I can take this on — OpenAI or Anthropic, in Settings."
)

# In-process, best-effort session memory: sessions that have already received the
# full first-contact copy. Bounded so an alpha instance can't grow it unbounded.
_SERVED_SESSIONS: Dict[str, bool] = {}
_SERVED_SESSIONS_MAX = 2048


def classify_pleasantry_kind(message: str) -> Optional[str]:
    """Deterministic, zero-LLM kind classification for the keyless gate.

    Returns "greeting" / "farewell" / "thanks" when the message is ONLY a
    pleasantry (reusing the pre-classifier's pattern lists and its #1416
    residue discipline: anything with substantive residue is NOT a pleasantry
    and returns None). Mixed pleasantries resolve farewell > thanks > greeting
    (a goodbye that also says hi is a goodbye).
    """
    from services.intent_service.pre_classifier import PreClassifier

    clean = message.strip().lower().rstrip("!?.,;: ")
    if not clean:
        return None
    if not PreClassifier._is_pleasantry_only(clean):
        return None
    for kind, patterns in (
        ("farewell", PreClassifier.FAREWELL_PATTERNS),
        ("thanks", PreClassifier.THANKS_PATTERNS),
        ("greeting", PreClassifier.GREETING_PATTERNS),
    ):
        if any(re.search(p, clean, flags=re.IGNORECASE) for p in patterns):
            return kind
    return None


def keyless_first_contact_message(kind: Optional[str]) -> str:
    """The full (b) copy: kind-matched acknowledgment + THE shared sentence."""
    prefix = KEYLESS_KIND_PREFIXES.get(kind or "neutral", KEYLESS_KIND_PREFIXES["neutral"])
    return f"{prefix} {KEYLESS_SHARED_KEY_SENTENCE}"


def keyless_gate_message(session_id: Optional[str], message: str) -> Optional[str]:
    """The (b) response for a keyless-refused turn, or None when this module
    has no claim and the gate's own refusal string should answer.

    - first refused turn this session (any kind) → the full kind-matched copy;
    - later refused turn that is a bare PLEASANTRY → the short form;
    - later refused turn that is substantive → None (the gate's string — one
      policy, one string per layer; #1823's when it lands).
    """
    kind = classify_pleasantry_kind(message)
    if session_id and _SERVED_SESSIONS.get(session_id):
        return KEYLESS_REPEAT_SHORT_FORM if kind else None
    if session_id:
        if len(_SERVED_SESSIONS) >= _SERVED_SESSIONS_MAX:
            _SERVED_SESSIONS.clear()  # best-effort memory; a reset only repeats copy
        _SERVED_SESSIONS[session_id] = True
    return keyless_first_contact_message(kind)


def _reset_served_sessions_for_tests() -> None:
    _SERVED_SESSIONS.clear()
