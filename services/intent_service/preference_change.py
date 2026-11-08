"""#955: the person changes or forgets a remembered "clear" preference.

Rulings: Arch 11-07 18:04 (one deletion path; which preference comes from the person's
stored keys, never the words), Arch 20:26 (say "forgotten" only after a read-back),
Arch 11-08 07:18 and 07:33 (one entry, ``change_remembered_preference``; the
classifier names one of three aliases and a closed table here maps the alias to the
change; set-directly writes only a key already stored and its reply says what was
stored). CXO 11-07 18:03 and 18:15: the words, no confirm.

The keys are the clear family's (``reminder_clear_verb:{verb}``, one per verb label:
"clear", "handle", "take care of", "reset"). A stored value is ``done`` or ``delete``.
"""

from __future__ import annotations

from typing import Any, Dict, Optional

import structlog

from services.intent_service import verified_inference as vi

logger = structlog.get_logger(__name__)

CHANGE_FORGET = "forget"
CHANGE_DONE = "done"
CHANGE_DELETE = "delete"

#: Arch 07:33: the alias the classifier names → the change. Closed; code-held.
CHANGE_BY_ACTION: Dict[str, str] = {
    "forget_clear_preference": CHANGE_FORGET,
    "set_clear_preference_done": CHANGE_DONE,
    "set_clear_preference_delete": CHANGE_DELETE,
}
CHANGE_ACTIONS = ("change_remembered_preference", *CHANGE_BY_ACTION)

CLEAR_KEY_PREFIX = "reminder_clear_verb:"

#: CXO 18:03 (3): ``{X}`` is ``mark it done`` or ``delete it``.
MEANING_WORDS = {CHANGE_DONE: "mark it done", CHANGE_DELETE: "delete it"}

# CXO 11-07 18:03, verbatim for "clear"; the verb label takes its place for a sibling.
FORGOTTEN_LINE = (
    'Okay. I\'ve forgotten that "{verb}" means {x}. '
    "Next time you say {verb}, I'll ask which you want."
)
NOTHING_STORED_LINE = (
    "I wasn't remembering a clear preference, so there's nothing to forget. "
    "When you say clear, I ask which you want."
)
SET_LINE = (
    'Okay. From now on "{verb}" means {x}. '
    'Say "forget my {verb} preference" any time to be asked again.'
)
FAILED_LINE = (
    "I couldn't change that just now, so I'm still remembering that \"{verb}\" means {x}. "
    "Try again in a moment."
)
# Interim lines (Arch 07:33 accepted the behaviour; words owed to CXO).
UNREADABLE_LINE = (
    "I couldn't check your clear preference just now, so I haven't changed anything. "
    "Try again in a moment."
)
CURRENT_LINE = 'Right now "{verb}" means {x}. I haven\'t changed it.'
SEVERAL_LINE = (
    "You have more than one of these remembered: {listed}. I haven't changed any of them."
)


def change_for(intent: Any) -> Optional[str]:
    """The alias's change from the closed table; a live router's ``change`` arg only
    when the op is named by its entry name. Anything else is None (binds nothing)."""
    action = getattr(intent, "action", None) or ""
    if action in CHANGE_BY_ACTION:
        return CHANGE_BY_ACTION[action]
    args = (getattr(intent, "context", None) or {}).get("inversion_args") or {}
    value = args.get("change") if isinstance(args, dict) else None
    return value if value in (CHANGE_FORGET, CHANGE_DONE, CHANGE_DELETE) else None


def _meaning(record: Optional[Dict[str, Any]]) -> Optional[str]:
    value = (record or {}).get("value")
    return MEANING_WORDS.get(str(value)) if value is not None else None


async def _stored_clear_keys(user_id: str) -> Dict[str, Dict[str, Any]]:
    """The person's stored clear-family records. Raises when the store can't be read
    (the #2151 rule: an unreadable store is never reported as empty)."""
    from services.intent_service.collaboration_gate import _load_preferences

    store = (await _load_preferences(str(user_id))).get(vi.VERIFIED_INFERENCES_PREF_KEY) or {}
    return {
        str(k): v
        for k, v in store.items()
        if str(k).startswith(CLEAR_KEY_PREFIX) and isinstance(v, dict)
    }


async def change_remembered_preference(intent: Any, user_id: Optional[str]) -> Dict[str, Any]:
    """Returns ``{"message", "outcome"}``. Writes only the person's own stored key."""
    change = change_for(intent)
    if not user_id:
        return {"message": UNREADABLE_LINE, "outcome": "no_principal"}
    try:
        keys = await _stored_clear_keys(user_id)
    except Exception as e:  # silent-ok: LOGGED; said as unreadable, nothing changed (#2151)
        logger.warning("preference_change_read_failed", error=str(e))
        return {"message": UNREADABLE_LINE, "outcome": "unreadable"}
    if not keys:
        # Arch 07:18 (iii): set-directly never creates a preference.
        return {"message": NOTHING_STORED_LINE, "outcome": "nothing_stored"}
    if len(keys) > 1:
        listed = ", ".join(
            f'"{k[len(CLEAR_KEY_PREFIX):]}" means {_meaning(v) or "something I can’t read"}'
            for k, v in sorted(keys.items())
        )
        return {"message": SEVERAL_LINE.format(listed=listed), "outcome": "several"}

    key, record = next(iter(keys.items()))
    verb = key[len(CLEAR_KEY_PREFIX) :]
    old_x = _meaning(record) or "something I can’t read"
    if change is None:
        # An unnamed change binds nothing: say what is stored, change nothing.
        logger.info("preference_change_no_change_named")
        return {"message": CURRENT_LINE.format(verb=verb, x=old_x), "outcome": "unchanged"}

    if change == CHANGE_FORGET:
        result = await vi.forget_verified_inference(user_id, key, read_back=True)
        if result.outcome is vi.ForgetOutcome.FORGOTTEN:
            x = _meaning(result.record) or old_x
            return {"message": FORGOTTEN_LINE.format(verb=verb, x=x), "outcome": "forgotten"}
        if result.outcome is vi.ForgetOutcome.NOTHING_STORED:
            return {"message": NOTHING_STORED_LINE, "outcome": "nothing_stored"}
        x = _meaning(result.record) or old_x
        return {"message": FAILED_LINE.format(verb=verb, x=x), "outcome": "failed"}

    # Set directly (Arch 07:18 (i)): store, read back, and render from the STORED value.
    stored_ok = await vi.store_verified_inference(
        user_id, key, change, source=vi.SOURCE_USER_DECLARED
    )
    after = await vi.get_verified_inference(user_id, key) if stored_ok else None
    if after is not None and str(after.get("value")) == change:
        return {
            "message": SET_LINE.format(verb=verb, x=MEANING_WORDS[change]),
            "outcome": "set",
        }
    return {"message": FAILED_LINE.format(verb=verb, x=old_x), "outcome": "failed"}
