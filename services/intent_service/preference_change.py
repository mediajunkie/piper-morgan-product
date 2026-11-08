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

from typing import Any, Dict, List, Optional, Tuple

import structlog

from services.intent_service import verified_inference as vi
from services.intent_service.reminder_clear import VALUE_COMPLETE, VALUE_DELETE

logger = structlog.get_logger(__name__)

CHANGE_FORGET = "forget"
CHANGE_DONE = "done"
CHANGE_DELETE = "delete"

#: Arch 07:33: the alias the classifier names → the change. Closed; code-held.
CHANGE_BY_ACTION: Dict[str, str] = {
    "forget_clear_preference": CHANGE_FORGET,
    # Arch 11-08 08:16: "ask me each time when I clear" (the classifier names this
    # alias, screen 6/6) is forget: line 3 says the next clear asks, and the next
    # clear's read-back discloses what it stores (CXO 08:09: forget's lines fit).
    "set_clear_preference_ask": CHANGE_FORGET,
    "set_clear_preference_done": CHANGE_DONE,
    "set_clear_preference_delete": CHANGE_DELETE,
}
# Arch 11-08 13:20 (forget) and 13:21 (set): per-verb aliases. The classifier names the
# verb by choosing the alias; code still acts only on that verb's STORED key (rule 2
# refined: never another verb's key, never a new key). "clear" aliases above name no
# verb and act over the whole stored family (one binds, several get the pick).
VERB_BY_ACTION: Dict[str, str] = {}
for _alias_verb, _label in (
    ("handle", "handle"),
    ("take_care_of", "take care of"),
    ("reset", "reset"),
):
    CHANGE_BY_ACTION[f"forget_{_alias_verb}_preference"] = CHANGE_FORGET
    CHANGE_BY_ACTION[f"set_{_alias_verb}_preference_done"] = CHANGE_DONE
    CHANGE_BY_ACTION[f"set_{_alias_verb}_preference_delete"] = CHANGE_DELETE
    for _a in (
        f"forget_{_alias_verb}_preference",
        f"set_{_alias_verb}_preference_done",
        f"set_{_alias_verb}_preference_delete",
    ):
        VERB_BY_ACTION[_a] = _label
#: The per-verb forget aliases (consent-narrowing, like forget; Arch 13:20).
PER_VERB_FORGET_ACTIONS = frozenset(
    a for a, c in CHANGE_BY_ACTION.items() if c == CHANGE_FORGET and a in VERB_BY_ACTION
)
CHANGE_ACTIONS = ("change_remembered_preference", *CHANGE_BY_ACTION)

CLEAR_KEY_PREFIX = "reminder_clear_verb:"

# Arch 11-08 09:28: ONE store, ONE vocabulary. The values are the clear path's own
# (reminder_clear.VALUE_COMPLETE / VALUE_DELETE, what its first-time answer stores);
# this module holds no value strings. ``change`` is the request's name for the edit.
STORED_VALUE = {CHANGE_DONE: VALUE_COMPLETE, CHANGE_DELETE: VALUE_DELETE}
#: CXO 18:03 (3): ``{X}`` is ``mark it done`` or ``delete it``, keyed on the stored value.
MEANING_WORDS = {VALUE_COMPLETE: "mark it done", VALUE_DELETE: "delete it"}

# CXO 11-07 18:03, verbatim for "clear"; the verb label takes its place for a sibling.
FORGOTTEN_LINE = (
    'Okay. I\'ve forgotten that "{verb}" means {x}. '
    "Next time you say {verb}, I'll ask which you want."
)
NOTHING_STORED_TEMPLATE = (
    "I wasn't remembering a {verb} preference, so there's nothing to forget. "
    "When you say {verb}, I ask which you want."
)
NOTHING_STORED_LINE = NOTHING_STORED_TEMPLATE.format(verb="clear")
# CXO 11-08 14:4x: a SET request with nothing stored for that verb (forget keeps line 4).
NOTHING_TO_CHANGE_TEMPLATE = (
    "I'm not remembering a {verb} preference yet, so there's nothing to change. "
    'Say "{verb}" on a todo and I\'ll ask which you want, then remember it.'
)
SET_LINE = (
    'Okay. From now on "{verb}" means {x}. '
    'Say "forget my {verb} preference" any time to be asked again.'
)
FAILED_LINE = (
    "I couldn't change that just now, so I'm still remembering that \"{verb}\" means {x}. "
    "Try again in a moment."
)
# CXO 11-08 08:09.
UNREADABLE_LINE = (
    "I couldn't check what I'm remembering just now, so I haven't changed anything. "
    "Try again in a moment."
)
ALREADY_LINE = '"{verb}" already means {x}, so I haven\'t changed anything.'
SET_DECLINE_LINE = "Okay. I won't change it."
SET_ASK_QUESTION = 'Change "{verb}" from {old} to {new}? (yes/no)'
# The several-keys forget pick (CXO 08:09), armed over exactly the rows shown.
FORGET_PICK_LEAD = "I'm remembering more than one of these:"
# Lead's interim (Arch 13:32 ruled the one-row pick; words owed to CXO): a clear forget
# with only another verb's key stored shows that row before anything is forgotten.
FORGET_PICK_LEAD_ONE = "Here's what I'm remembering:"
FORGET_PICK_QUESTION = (
    "Which one should I forget? Say the number, or 'never mind' to leave them alone."
)
FORGET_PICK_DECLINE_LINE = "Okay. I haven't forgotten anything."
FORGET_PICK_KIND = "preference_forget_pick"
# Lead's interim for SET with several keys stored (CXO worded only forget's pick).
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


def verb_for(intent: Any) -> Optional[str]:
    """The verb a per-verb alias names (None for the clear-family aliases)."""
    return VERB_BY_ACTION.get(getattr(intent, "action", None) or "")


CLEAR_KEY = f"{CLEAR_KEY_PREFIX}clear"


def _scope_for(
    keys: Dict[str, Dict[str, Any]], intent: Any
) -> Tuple[Dict[str, Dict[str, Any]], Optional[str]]:
    """The keys this request may act on, and the verb its replies name.

    Arch 11-08 13:32: a per-verb alias acts only on its verb's key; a CLEAR SET alias acts
    only on the "clear" key (the classifier sends "make take care of mean …" there, and
    a family-wide bind wrote the wrong verb); a clear forget keeps the whole family (the
    pick decides which)."""
    verb = verb_for(intent)
    if verb is None and change_for(intent) in (CHANGE_DONE, CHANGE_DELETE):
        verb = "clear"
    return _scope(keys, verb), verb


def _scope(keys: Dict[str, Dict[str, Any]], verb: Optional[str]) -> Dict[str, Dict[str, Any]]:
    """A per-verb alias acts only on that verb's stored key; otherwise the whole family."""
    if verb is None:
        return keys
    key = f"{CLEAR_KEY_PREFIX}{verb}"
    return {key: keys[key]} if key in keys else {}


def _nothing_line(verb: Optional[str], change: Optional[str] = None) -> str:
    template = (
        NOTHING_TO_CHANGE_TEMPLATE
        if change in (CHANGE_DONE, CHANGE_DELETE)
        else NOTHING_STORED_TEMPLATE
    )
    return template.format(verb=verb or "clear")


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


async def forget_one(user_id: str, key: str, old_x: str) -> Dict[str, Any]:
    """Forget one stored key, saying "forgotten" only after the read-back (Arch 20:26)."""
    verb = key[len(CLEAR_KEY_PREFIX) :]
    result = await vi.forget_verified_inference(user_id, key, read_back=True)
    if result.outcome is vi.ForgetOutcome.FORGOTTEN:
        x = _meaning(result.record) or old_x
        return {"message": FORGOTTEN_LINE.format(verb=verb, x=x), "outcome": "forgotten"}
    if result.outcome is vi.ForgetOutcome.NOTHING_STORED:
        return {"message": _nothing_line(verb), "outcome": "nothing_stored"}
    x = _meaning(result.record) or old_x
    return {"message": FAILED_LINE.format(verb=verb, x=x), "outcome": "failed"}


def _rows(keys: Dict[str, Dict[str, Any]]) -> List[Tuple[str, str]]:
    """``(key, '"verb" means X')`` for each stored key, in a stable order."""
    return [
        (k, f'"{k[len(CLEAR_KEY_PREFIX):]}" means {_meaning(v) or "something I can’t read"}')
        for k, v in sorted(keys.items())
    ]


def forget_pick_question(rows: List[Tuple[str, str]]) -> str:
    lines = "\n".join(f"{i}. {text}" for i, (_k, text) in enumerate(rows, start=1))
    lead = FORGET_PICK_LEAD if len(rows) > 1 else FORGET_PICK_LEAD_ONE
    return f"{lead}\n\n{lines}\n\n{FORGET_PICK_QUESTION}"


def _arm_forget_pick(
    intent: Any,
    rows: List[Tuple[str, str]],
    user_id: str,
    session_id: Optional[str],
    offer_service: Any,
) -> Optional[str]:
    """Arm the several-keys pick over exactly the rows shown; the question, or None
    when nothing could be armed (no session or store)."""
    if not session_id or offer_service is None:
        return None
    from services.intent_service.destructive_confirm import CONFIRM_PENDING_ACTION_WORKFLOW

    question = forget_pick_question(rows)
    offer = {
        "workflow_type": CONFIRM_PENDING_ACTION_WORKFLOW,
        "question": question,
        "pending_action": {
            "kind": FORGET_PICK_KIND,
            "action": getattr(intent, "action", None),
            "intent": intent,
            "summary": "forget a remembered preference",
            "user_id": user_id,
            "rows": [list(r) for r in rows],
        },
        "decline_message": FORGET_PICK_DECLINE_LINE,
    }
    try:
        offer_service.set_pending_offer(session_id, offer, user_id=user_id)
    except Exception as e:  # silent-ok: LOGGED; an unarmed pick is never asked (#1730)
        logger.error("preference_forget_pick_arm_failed", error=str(e))
        return None
    return question


async def change_remembered_preference(
    intent: Any,
    user_id: Optional[str],
    session_id: Optional[str] = None,
    offer_service: Any = None,
) -> Dict[str, Any]:
    """Returns ``{"message", "outcome"}`` (``"armed": True`` when a pick was armed).
    Writes only the person's own stored key."""
    change = change_for(intent)
    if not user_id:
        return {"message": UNREADABLE_LINE, "outcome": "no_principal"}
    try:
        keys, scoped_verb = _scope_for(await _stored_clear_keys(user_id), intent)
    except Exception as e:  # silent-ok: LOGGED; said as unreadable, nothing changed (#2151)
        logger.warning("preference_change_read_failed", error=str(e))
        return {"message": UNREADABLE_LINE, "outcome": "unreadable"}
    if not keys:
        # Arch 07:18 (iii): set-directly never creates a preference; a per-verb ask
        # whose verb isn't stored says so for that verb (Arch 13:20).
        return {"message": _nothing_line(scoped_verb, change), "outcome": "nothing_stored"}
    # Arch 13:32 (2): a clear forget binds one stored key only if it is "clear";
    # one other verb's key gets the pick with that one row.
    _one_other = (
        change == CHANGE_FORGET and scoped_verb is None and len(keys) == 1 and CLEAR_KEY not in keys
    )
    if len(keys) > 1 or _one_other:
        rows = _rows(keys)
        if change == CHANGE_FORGET:
            question = _arm_forget_pick(intent, rows, user_id, session_id, offer_service)
            if question is not None:
                return {"message": question, "outcome": "pick_armed", "armed": True}
        if len(rows) == 1:
            # Nothing could be armed (no session): say what is stored, change nothing.
            _k, _rec = next(iter(keys.items()))
            return {
                "message": CURRENT_LINE.format(
                    verb=_k[len(CLEAR_KEY_PREFIX) :],
                    x=_meaning(_rec) or "something I can’t read",
                ),
                "outcome": "unchanged",
            }
        listed = ", ".join(text for _k, text in rows)
        return {"message": SEVERAL_LINE.format(listed=listed), "outcome": "several"}

    key, record = next(iter(keys.items()))
    verb = key[len(CLEAR_KEY_PREFIX) :]
    old_x = _meaning(record) or "something I can’t read"
    if change is None:
        # An unnamed change binds nothing: say what is stored, change nothing.
        logger.info("preference_change_no_change_named")
        return {"message": CURRENT_LINE.format(verb=verb, x=old_x), "outcome": "unchanged"}

    if change == CHANGE_FORGET:
        return await forget_one(user_id, key, old_x)

    target = STORED_VALUE[change]
    if str(record.get("value")) == target:
        return {"message": ALREADY_LINE.format(verb=verb, x=old_x), "outcome": "already"}
    # Set directly (Arch 07:18 (i)): store, read back, and render from the STORED value.
    stored_ok = await vi.store_verified_inference(
        user_id, key, target, source=vi.SOURCE_USER_DECLARED
    )
    after = await vi.get_verified_inference(user_id, key) if stored_ok else None
    if after is not None and str(after.get("value")) == target:
        return {
            "message": SET_LINE.format(verb=verb, x=MEANING_WORDS[target]),
            "outcome": "set",
        }
    return {"message": FAILED_LINE.format(verb=verb, x=old_x), "outcome": "failed"}


async def change_preference_write_ask(request: Any) -> Any:
    """#2304 write_ask for the set aliases (CXO 08:09; Arch 08:16: built from the stored
    key and the target value, never the words). Forget never reaches the check
    (consent-narrowing), so its request passes through."""
    from services.intent_service.write_confirm_words import ConfirmWords, WriteAsk

    change = change_for(request.intent)
    if change not in (CHANGE_DONE, CHANGE_DELETE):
        # Forget never reaches the check (consent-narrowing); an unnamed change on the
        # canonical names nothing, so CXO's #2304 statement (resolve_write_ask's default).
        return WriteAsk()
    user_id = request.principal or request.user_id
    if not user_id:
        return WriteAsk(reply=UNREADABLE_LINE)
    try:
        keys, scoped_verb = _scope_for(await _stored_clear_keys(str(user_id)), request.intent)
    except Exception as e:  # silent-ok: LOGGED; said as unreadable, nothing armed (#2151)
        logger.warning("preference_write_ask_read_failed", error=str(e))
        return WriteAsk(reply=UNREADABLE_LINE)
    if not keys:
        return WriteAsk(reply=_nothing_line(scoped_verb, change))
    if len(keys) > 1:
        listed = ", ".join(text for _k, text in _rows(keys))
        return WriteAsk(reply=SEVERAL_LINE.format(listed=listed))
    key, record = next(iter(keys.items()))
    verb = key[len(CLEAR_KEY_PREFIX) :]
    old_x = _meaning(record) or "something I can’t read"
    target = STORED_VALUE[change]
    if str(record.get("value")) == target:
        return WriteAsk(reply=ALREADY_LINE.format(verb=verb, x=old_x))
    return WriteAsk(
        words=ConfirmWords(
            question=SET_ASK_QUESTION.format(verb=verb, old=old_x, new=MEANING_WORDS[target]),
            summary="change it",
            decline=SET_DECLINE_LINE,
        )
    )


async def handle_forget_pick_turn(
    pending_offer: Dict[str, Any],
    message: str,
    *,
    session_id: Optional[str],
    user_id: Optional[str],
) -> Optional[Dict[str, Any]]:
    """The several-keys pick's answer: a number on the list forgets that row's key.
    None hands the turn to the generic seam (a decline says CXO's decline line;
    a bare "yes" re-dispatches the original, which re-asks; anything else pops)."""
    payload = pending_offer.get("pending_action") or {}
    if payload.get("kind") != FORGET_PICK_KIND:
        return None
    if not user_id or (payload.get("user_id") and payload.get("user_id") != str(user_id)):
        return None
    answer = (message or "").strip().rstrip(".!?").strip()
    rows = payload.get("rows") or []
    if not answer.isdigit() or not (1 <= int(answer) <= len(rows)):
        return None
    key, text = rows[int(answer) - 1]
    old_x = text.split(" means ", 1)[1] if " means " in text else "something I can’t read"
    out = await forget_one(str(user_id), key, old_x)
    return {
        "message": out["message"],
        "intent_data": {
            "category": "query",
            "action": payload.get("action") or "forget_clear_preference",
            "preference_change": out["outcome"],
        },
    }
