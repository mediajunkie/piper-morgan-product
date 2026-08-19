"""#1510 (inferred half) — the SHARED verified-inference preference mechanism.

PM ruling (relayed by Exec 2026-08-13, recorded on #1510): **"When the
trust-gradient score for a given inference is low, Piper reads the inference
back to the user for verification. Once verified, it's stored — not
re-inferred each time."** And the explicit second half: the user's
meta-feedback about the verification process itself ("stop asking me every
time," "don't make assumptions") **"is a distinct steering signal from
feedback about the underlying task preference, and needs its own handling —
not folded into the inference-confidence mechanism."**

This module is the shared rail for three consumers — #1591 (standup
preference persistence), #1509 (consent/legibility), and the working-mode
surface in ``collaboration_gate.py``. The consumers' own wiring is
deliberately NOT here; this is the mechanism they call.

Design constraints honored (each a ratified house rule):

- **One scoring system** (#1591 path, Exec's recommended shape): the
  confidence gate EXTENDS ``services/personality/preference_detection.py``'s
  existing ``confidence_score`` thresholds (``AUTO_APPLY_THRESHOLD`` /
  ``SUGGESTION_THRESHOLD``, hoisted there to named constants) — no parallel
  scoring mechanism. ``is_low_confidence()`` here is the resurrected trigger
  the ruling named (it did not previously exist under that name;
  ``UserStandupPreference.needs_confirmation`` was the nearest analog — the
  standup dataclass now delegates its own ``is_low_confidence()`` to this
  one).
- **One preference persistence** (PPM+CXO: no consumer grows a local
  preference store): reads/writes go through ``collaboration_gate``'s
  ``_load_preferences`` / ``_save_preference`` seam — the same
  ``users.preferences`` JSONB the declared working mode lives in.
- **The read-back offer binds via the existing pending-offer machinery**
  (#846 store, #1529 ordering: offer beats resume-check; #1190's
  ``pending_action`` carrier shape). No parallel store for pending
  confirmations. Acceptance stores the preference; decline discards WITHOUT
  storing and is not re-asked in the same session (session-scoped anti-nag
  memory below).
- **Meta-feedback is a distinct channel**: detected INSIDE the confirmation
  flow's own turn handling (sanctioned handler-internal logic — under the
  routing moratorium no pre-classifier patterns were added), stored under
  its own preference key, never folded into per-inference confidence.
- **The store is the USER's** (#1532 class — no principal dropping): every
  read/write carries ``user_id``, normalized to ``str`` at the boundary
  (#1603 lesson: String columns take str params).
"""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, Optional

from services.personality.preference_detection import (
    AUTO_APPLY_THRESHOLD,
    SUGGESTION_THRESHOLD,
)

logger = logging.getLogger(__name__)

# Registered in workflow_entries.register_default_workflows with
# action_triggered=False: the classifier/rail can never emit it; only the
# offer-acceptance seam dispatches it (same pattern as #1190's
# confirm_pending_action).
VERIFY_INFERENCE_WORKFLOW = "verify_inference"

# Marker inside the pending_action payload identifying a verification offer
# (the #1190 carrier is deliberately action-agnostic; ``kind`` is how the
# pending-offer seam recognizes ours without a parallel store).
VERIFY_INFERENCE_KIND = "verify_inference"

# users.preferences JSONB keys — the ONE preference persistence, shared with
# the declared working mode (collaboration_gate.WORKING_MODE_PREF_KEY).
VERIFIED_INFERENCES_PREF_KEY = "verified_inferences"
"""Dict of inference_key → verified record ({value, source, confidence_at_verification, verified_at})."""

VERIFICATION_META_PREF_KEY = "inference_verification_meta"
"""The DISTINCT meta-feedback signal's home: {"mode": VerificationMetaMode, "set_at": iso}.
Deliberately a separate key from VERIFIED_INFERENCES_PREF_KEY — PM's ruling:
process steering is not a task preference and must not be folded in."""

# Provenance values for a stored record's "source" field — legibility (#1509
# consumer) needs to distinguish an explicit yes from a meta-endorsed apply.
SOURCE_USER_VERIFIED = "user_verified"  # user answered the read-back with an accept
SOURCE_META_AUTO = "meta_auto"  # applied under a "stop asking me" meta-preference
# #1591 declaration path (PM live 2026-08-13): the user STATED the preference
# outright ("use the standup interview format by default from now on") — the
# highest-confidence signal there is. A declaration is not an inference: it
# warrants store + confirmation copy, never a read-back question (reading a
# user's own words back as a question would be verification theater).
SOURCE_USER_DECLARED = "user_declared"


class VerificationDecision(str, Enum):
    """What to do with a fresh inference, given its confidence + meta mode."""

    AUTO_APPLY = "auto_apply"  # confident enough (or meta-trusted): apply, no read-back
    READ_BACK = "read_back"  # low confidence: read the inference back for verification
    DISCARD = "discard"  # too weak to act on at all (below the suggestion floor)


class VerificationMetaMode(str, Enum):
    """The user's steering of the verification PROCESS itself (distinct signal).

    - DEFAULT: PM's ruled behavior — low-confidence inferences are read back.
    - TRUST_INFERENCES: "stop asking me every time" — lower the gate; apply
      inferences without read-back (down to the suggestion floor).
    - ALWAYS_ASK: "don't make assumptions" — raise the gate; read back even
      high-confidence inferences.
    """

    DEFAULT = "default"
    TRUST_INFERENCES = "trust_inferences"
    ALWAYS_ASK = "always_ask"


def is_low_confidence(confidence_score: float) -> bool:
    """The resurrected #1510 read-back trigger: below the shared auto-apply
    threshold = low confidence = read the inference back before relying on it.
    (One gate for the whole cohort — the threshold is preference_detection's.)
    """
    return confidence_score < AUTO_APPLY_THRESHOLD


def decide(
    confidence_score: float,
    meta_mode: VerificationMetaMode = VerificationMetaMode.DEFAULT,
) -> VerificationDecision:
    """The inference-confidence gate, meta-mode adjusted.

    DEFAULT (PM's ruling): auto-apply at/above ``AUTO_APPLY_THRESHOLD``
    (0.9, preference_detection's existing auto-apply bar); read back between
    ``SUGGESTION_THRESHOLD`` (0.4) and the auto-apply bar; below the
    suggestion floor the inference is too weak to surface at all (matching
    ``is_ready_for_suggestion``) — discard, don't nag.

    TRUST_INFERENCES ("stop asking me every time"): the ask-threshold drops —
    anything at/above the suggestion floor auto-applies; nothing is read back.

    ALWAYS_ASK ("don't make assumptions"): the ask-threshold rises — even
    high-confidence inferences are read back; nothing silently applies.

    The meta mode moves the ASK THRESHOLD only; the suggestion floor is a
    property of the inference being worth anything, not of the process
    preference, so DISCARD is mode-independent.
    """
    if confidence_score < SUGGESTION_THRESHOLD:
        return VerificationDecision.DISCARD
    if meta_mode is VerificationMetaMode.ALWAYS_ASK:
        return VerificationDecision.READ_BACK
    if meta_mode is VerificationMetaMode.TRUST_INFERENCES:
        return VerificationDecision.AUTO_APPLY
    if is_low_confidence(confidence_score):
        return VerificationDecision.READ_BACK
    return VerificationDecision.AUTO_APPLY


# ---------------------------------------------------------------------------
# Persistence — through collaboration_gate's seam (users.preferences JSONB).
# ONE preference store (PPM+CXO ruling); every call carries user_id (#1532).
# ---------------------------------------------------------------------------


async def get_verified_inference(user_id: Optional[str], key: str) -> Optional[Dict[str, Any]]:
    """The 'stored — not re-inferred each time' read. Consumers call this
    FIRST; a hit means skip inference entirely and use the verified value.

    Returns the stored record ({value, source, confidence_at_verification,
    verified_at}) or None. Fail-safe direction: a storage error reads as
    'nothing verified' (the consumer falls back to inferring + read-back),
    never as a fabricated verified value.
    """
    if not user_id or not key:
        return None
    from services.intent_service.collaboration_gate import _load_preferences

    try:
        store = (await _load_preferences(str(user_id))).get(VERIFIED_INFERENCES_PREF_KEY) or {}
    except Exception as e:  # silent-ok: fail-safe DIRECTION — a storage error degrades to "nothing verified yet" (re-infer + read back), never fabricates a verified preference
        logger.warning("verified_inference_read_failed user_id=%s key=%s error=%s", user_id, key, e)
        return None
    record = store.get(str(key))
    return record if isinstance(record, dict) else None


async def store_verified_inference(
    user_id: Optional[str],
    key: str,
    value: Any,
    source: str = SOURCE_USER_VERIFIED,
    confidence: Optional[float] = None,
) -> bool:
    """Store a verified inference in the user's preference store.

    False = not persisted (callers surface that honestly, mirroring
    collaboration_gate.set_working_mode). The record keeps provenance
    (source + confidence at verification time) so #1509's legibility
    consumer can show WHY Piper believes this.
    """
    if not user_id or not key:
        return False
    from services.intent_service.collaboration_gate import (
        _load_preferences,
        _save_preference,
    )

    try:
        store = dict(
            (await _load_preferences(str(user_id))).get(VERIFIED_INFERENCES_PREF_KEY) or {}
        )
        store[str(key)] = {
            "value": value,
            "source": str(source),
            "confidence_at_verification": confidence,
            "verified_at": datetime.now(timezone.utc).isoformat(),
        }
        return await _save_preference(str(user_id), VERIFIED_INFERENCES_PREF_KEY, store)
    except Exception as e:  # silent-ok: False = "not persisted", surfaced honestly to the caller rather than claiming a save that did not happen
        logger.warning(
            "verified_inference_write_failed user_id=%s key=%s error=%s", user_id, key, e
        )
        return False


async def get_meta_mode(user_id: Optional[str]) -> VerificationMetaMode:
    """The user's verification-process meta-preference; DEFAULT when unset,
    unknown, or on storage error (fail-safe: the ruled read-back behavior)."""
    if not user_id:
        return VerificationMetaMode.DEFAULT
    from services.intent_service.collaboration_gate import _load_preferences

    try:
        record = (await _load_preferences(str(user_id))).get(VERIFICATION_META_PREF_KEY) or {}
    except Exception as e:  # silent-ok: fail-safe DIRECTION — a storage error degrades to the PM-ruled DEFAULT (read low-confidence inferences back), never silently trusts or nags
        logger.warning("verification_meta_read_failed user_id=%s error=%s", user_id, e)
        return VerificationMetaMode.DEFAULT
    try:
        return VerificationMetaMode(record.get("mode"))
    except (ValueError, TypeError):
        return VerificationMetaMode.DEFAULT


async def set_meta_mode(user_id: Optional[str], mode: VerificationMetaMode) -> bool:
    """Persist the meta-preference under its OWN key (visible in the store —
    the ruling's distinct-signal requirement). False = not persisted."""
    if not user_id:
        return False
    from services.intent_service.collaboration_gate import _save_preference

    try:
        return await _save_preference(
            str(user_id),
            VERIFICATION_META_PREF_KEY,
            {"mode": mode.value, "set_at": datetime.now(timezone.utc).isoformat()},
        )
    except Exception as e:  # silent-ok: False = "not persisted", surfaced honestly to the caller rather than claiming a save that did not happen
        logger.warning("verification_meta_write_failed user_id=%s error=%s", user_id, e)
        return False


# ---------------------------------------------------------------------------
# Session-scoped decline memory (anti-nag; NOT a preference store)
# ---------------------------------------------------------------------------
# A declined read-back must not be re-asked in the same session. This is
# transient per-process conversational state — the same in-memory,
# session-keyed lifetime as WorkflowOfferService._pending_offers (#846), NOT
# a preference store (nothing here persists or shadows users.preferences;
# the PPM+CXO one-store rule governs preferences, and a "don't re-nag this
# session" memo is not one). Capped so long-lived processes don't grow it
# unboundedly; eviction is oldest-session-first (dict insertion order).

_SESSION_DECLINES: Dict[str, set] = {}
_SESSION_DECLINES_MAX_SESSIONS = 2048


def mark_declined(session_id: Optional[str], key: Optional[str]) -> None:
    """Record that this session declined the read-back for this inference."""
    if not session_id or not key:
        return
    sid = str(session_id)
    if sid not in _SESSION_DECLINES and len(_SESSION_DECLINES) >= _SESSION_DECLINES_MAX_SESSIONS:
        _SESSION_DECLINES.pop(next(iter(_SESSION_DECLINES)))
    _SESSION_DECLINES.setdefault(sid, set()).add(str(key))


def was_declined(session_id: Optional[str], key: Optional[str]) -> bool:
    """Has this session already declined the read-back for this inference?"""
    if not session_id or not key:
        return False
    return str(key) in _SESSION_DECLINES.get(str(session_id), set())


# ---------------------------------------------------------------------------
# The read-back offer (binds via the EXISTING pending-offer machinery)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class ReadBackOffer:
    """What a consumer stores + asks: the read-back question for this turn,
    and the pending-offer record (the #1190 ``pending_action`` carrier shape)
    for ``WorkflowOfferService.set_pending_offer`` — the #846 session store,
    popped before classification, so the #1529 ordering (offer beats
    resume-check) holds for verification turns by construction."""

    question: str
    offer: Dict[str, Any]


def build_read_back_offer(
    user_id: Optional[str],
    key: str,
    value: Any,
    description: str,
    confidence: Optional[float] = None,
    session_id: Optional[str] = None,
) -> Optional[ReadBackOffer]:
    """Build the read-back for a low-confidence inference, or None when this
    session already declined it (decline is not re-asked in-session).

    ``description`` is the human phrasing of the inference ("that you want
    brief standups", "that piper-morgan-product is your default repo") —
    the consumer knows how to say its own inference; the mechanism shapes
    the verification turn around it.
    """
    if not key:
        return None
    if was_declined(session_id, key):
        return None
    question = (
        f"Before I rely on it — I've inferred {description}. Did I get that right? (yes/no)"
    )
    return ReadBackOffer(
        question=question,
        offer={
            "workflow_type": VERIFY_INFERENCE_WORKFLOW,
            # #1665: the rendered ask rides the record — same string the
            # consumer surfaces as the turn's trailing question (built once,
            # above), so the SessionSnapshot never drifts from what was said.
            "question": question,
            "pending_action": {
                "kind": VERIFY_INFERENCE_KIND,
                # "action" keeps the #1190 carrier's field contract (the
                # off-intent abandonment log reads it); it is NOT a rail key
                # here — acceptance dispatches VERIFY_INFERENCE_WORKFLOW,
                # whose entry stores the preference itself.
                "action": VERIFY_INFERENCE_WORKFLOW,
                "user_id": str(user_id) if user_id else None,
                "inference_key": str(key),
                "inference_value": value,
                "confidence": confidence,
                "summary": description,
            },
            "decline_message": (
                f"Got it — I won't assume {description}. Nothing has been stored, "
                "and I won't ask again this session."
            ),
        },
    )


# ---------------------------------------------------------------------------
# Meta-feedback detection (the DISTINCT channel)
# ---------------------------------------------------------------------------
# Small, pattern-based vocabulary by design. Routing moratorium honored: these
# patterns are NOT pre-classifier additions — detection runs only inside the
# confirmation flow's own turn handling (a verification offer is pending),
# which is sanctioned handler-internal logic. Note the deliberate distance
# from collaboration_gate's mode-declaration regexes: those require a durative
# marker and steer the compose/execute working mode; these steer the
# verification process and fire only on a verification turn.

# "Trust your inferences" — lower the ask-threshold. Negated-ask phrasings
# ("stop asking", "don't ask", "quit asking") + "just go with it" shapes.
_META_TRUST_RE = re.compile(
    r"""
    \b(?:stop|quit)\s+asking\b
    | \bdon'?t\s+ask\b
    | \bno\s+need\s+to\s+(?:ask|check|verify|confirm)\b
    | \bjust\s+(?:do\s+it|go\s+with\s+(?:it|that)|use\s+(?:it|that|your\s+judgm?ent))\b
    | \bstop\s+checking\b
    """,
    re.IGNORECASE | re.VERBOSE,
)

# "Verify everything" — raise the ask-threshold. Anti-assumption phrasings.
_META_ALWAYS_ASK_RE = re.compile(
    r"""
    \bdon'?t\s+(?:make\s+)?assum(?:e|ptions?)\b
    | \bstop\s+(?:making\s+)?assum(?:ing|ptions?)\b
    | \bno\s+assumptions?\b
    | \balways\s+(?:ask|check|verify|confirm)\b
    | \b(?:ask|check\s+with)\s+me\s+(?:every\s+time|each\s+time|first|before)\b
    """,
    re.IGNORECASE | re.VERBOSE,
)


def detect_meta_feedback(message: Optional[str]) -> Optional[VerificationMetaMode]:
    """Detect verification-process steering in a message; None otherwise.

    TRUST patterns are checked first: they are all negations of asking, and
    the ALWAYS_ASK set contains ask-verbs that could otherwise shadow them.
    """
    text = (message or "").strip()
    if not text:
        return None
    if _META_TRUST_RE.search(text):
        return VerificationMetaMode.TRUST_INFERENCES
    if _META_ALWAYS_ASK_RE.search(text):
        return VerificationMetaMode.ALWAYS_ASK
    return None


def _meta_confirmation_message(
    mode: VerificationMetaMode,
    meta_persisted: bool,
    stored_current: bool,
    description: str,
) -> str:
    """Honest copy for a meta-feedback turn (persisted=False must be visible —
    claiming a durable change that didn't save would be a confabulated
    capability, same rule as collaboration_gate.mode_confirmation_message)."""
    if mode is VerificationMetaMode.TRUST_INFERENCES:
        msg = "Understood — I'll stop checking my inferences with you and just go with them."
        if stored_current:
            msg += f" I'll go with {description}."
        else:
            msg += f" I've dropped {description} for now."
        msg += ' (Say "don\'t make assumptions" any time and I\'ll go back to checking first.)'
    else:
        msg = (
            "Understood — I won't act on my own inferences without checking with you first, "
            f"and I've dropped {description}."
        )
        msg += ' (Say "stop asking me every time" if you\'d rather I use my judgment.)'
    if not meta_persisted:
        msg += (
            "\n\n(Heads up: I couldn't save that preference just now, so it may "
            "not stick across sessions.)"
        )
    return msg


async def handle_verification_turn_meta(
    pending_offer: Dict[str, Any],
    message: str,
    session_id: Optional[str],
    user_id: Optional[str],
) -> Optional[Dict[str, Any]]:
    """The meta-feedback half of a verification turn (PM's ruling: a distinct
    steering signal with its own handling, not folded into confidence).

    Called by the pending-offer seam ONLY when the popped offer is a
    verification read-back, BEFORE generic accept/decline detection (meta
    phrasings are more specific and may co-occur with a decline: "no, stop
    asking me every time" declines the inference AND steers the process).

    Returns the acceptance-seam dict shape ({"message", "intent_data"}) when
    the turn was meta-feedback, None to fall through to generic handling.

    Semantics:
    - TRUST_INFERENCES: persist the meta-preference; the CURRENT inference is
      applied+stored (source=meta_auto) unless the same message also declines
      it — "stop asking me every time" while being asked means "go with it";
      "no, stop asking me" means "not this one, and stop asking".
    - ALWAYS_ASK: persist the meta-preference; the current inference is
      DISCARDED (pushing back on assumptions is a decline of this assumption)
      and not re-asked this session.
    """
    meta = detect_meta_feedback(message)
    if meta is None:
        return None

    payload = pending_offer.get("pending_action") or {}
    key = payload.get("inference_key")
    value = payload.get("inference_value")
    confidence = payload.get("confidence")
    description = payload.get("summary") or "that inference"

    # #1532: the store is the USER's. The offer was built for the user it was
    # inferred about; if the turn's principal differs (auth changed between
    # turns), do not write another user's store — decline-shaped no-op.
    offer_user = payload.get("user_id")
    principal = str(user_id) if user_id else None
    if offer_user and principal and offer_user != principal:
        logger.warning(
            "verification_turn_principal_mismatch offer_user=%s turn_user=%s", offer_user, principal
        )
        mark_declined(session_id, key)
        return {
            "message": (
                f"Got it — I won't assume {description}, and nothing has been stored."
            ),
            "intent_data": {
                "category": "execution",
                "action": VERIFY_INFERENCE_WORKFLOW,
                "verified": False,
                "principal_mismatch": True,
            },
        }
    effective_user = principal or offer_user

    meta_persisted = await set_meta_mode(effective_user, meta)

    stored_current = False
    if meta is VerificationMetaMode.TRUST_INFERENCES:
        from services.intent_service.soft_invocation import detect_offer_response

        # #1631 opt-out (prose_override=False): meta feedback legitimately
        # arrives as long prose ("no, that's wrong — and stop asking me every
        # time, because…"), and a decline caught inside it is the
        # conservative direction here — it only prevents a store, nothing
        # fires. The default override would silently store the current
        # inference despite the "no".
        declines_current = (
            detect_offer_response(message, prose_override=False) == "decline"
        )
        if not declines_current and key is not None:
            stored_current = await store_verified_inference(
                effective_user,
                key,
                value,
                source=SOURCE_META_AUTO,
                confidence=confidence,
            )
        if declines_current:
            mark_declined(session_id, key)
    else:  # ALWAYS_ASK
        mark_declined(session_id, key)

    logger.info(
        "verification_meta_feedback user_id=%s mode=%s meta_persisted=%s stored_current=%s key=%s",
        effective_user,
        meta.value,
        meta_persisted,
        stored_current,
        key,
    )
    return {
        "message": _meta_confirmation_message(meta, meta_persisted, stored_current, description),
        "intent_data": {
            "category": "execution",
            "action": VERIFY_INFERENCE_WORKFLOW,
            "meta_mode": meta.value,
            "meta_persisted": meta_persisted,
            "verified": stored_current,
            "inference_key": key,
        },
    }
