"""#2189 row 1: the #846 pending offer rides the hydrated conversation slice.

Arch's direction (#2189, 2026-10-28): the pending offer is session-scoped user
state, so it persists on the carrier that already survives a restart: the
Layer-4 slice ``ConversationContext.to_persistable_state`` /
``apply_persisted_state`` (#953), beside ``last_offer`` and the #1784
remainder tombstone. No new store, no Redis, no migration.

This module holds the pieces of that carrier that are not the context itself:

- the JSON codec for an offer record. Offer records are mostly strings and
  dicts, but the #1190 confirm carrier binds the ORIGINAL classified
  ``Intent`` (``pending_action["intent"]``), and a few carry datetimes, UUIDs
  or enums. Those are tagged on the way out and rebuilt on the way in. A
  record holding anything else is NOT persisted (logged
  ``pending_offer_not_persistable``): it keeps today's in-process lifetime
  rather than taking the whole slice write down with it.
- the effect read at the pop seam (Arch's condition, 22:44Z/23:10Z): a
  write-effect offer is persisted cleared BEFORE its action runs.
- the process-level consumed-offer ids, the in-process half of the
  idempotency backstop (the slice's ``last_consumed_offer_id`` is the
  durable half).
- CXO's lapsed-offer line (22:48Z), verbatim.
"""

from __future__ import annotations

from collections import OrderedDict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, Optional
from uuid import UUID

import structlog

from services.shared_types import EffectClass, IntentCategory, Outwardness

logger = structlog.get_logger(__name__)

# CXO, #2189 22:48Z ("Expiry word"): a hydrated offer past
# REMAINDER_MAX_AGE_MINUTES is dropped silently UNLESS the next message is
# accept-shaped; then this line, rather than letting the "yes" run as a fresh
# message. Copy is CXO's; do not edit it here.
LAPSED_OFFER_REPLY = "That was a while ago, so I let it go. Ask me again and I'll pick it up."

_INTENT_TAG = "__piper_intent__"
_DATETIME_TAG = "__piper_datetime__"
_UUID_TAG = "__piper_uuid__"
_TUPLE_TAG = "__piper_tuple__"
_ENUM_TAG = "__piper_enum__"
_RESERVED_TAGS = frozenset({_INTENT_TAG, _DATETIME_TAG, _UUID_TAG, _TUPLE_TAG, _ENUM_TAG})

# Arch (#2189, 2026-10-29 07:31, comment 6499472026): the decoder must never
# turn persisted data into a call. Router args are unconstrained model JSON on
# ``intent.context["inversion_args"]`` and the confirm carriers bind that
# Intent into the record, so a tag that reached the slice could name code. The
# enum tag therefore resolves ONLY through this in-code allowlist (tag name →
# class), with no import and no attribute walk; an unknown name drops the
# offer. Add a class here only when a record genuinely carries it.
_ENUM_ALLOWLIST: Dict[str, type] = {
    "IntentCategory": IntentCategory,
    "EffectClass": EffectClass,
    "Outwardness": Outwardness,
}
_ENUM_TAG_BY_CLASS: Dict[type, str] = {cls: name for name, cls in _ENUM_ALLOWLIST.items()}


class OfferNotPersistable(Exception):
    """Raised inside the codec when a record holds a value it cannot tag."""


def _encode(value: Any) -> Any:
    from services.domain.models import Intent

    if isinstance(value, Enum):  # before the primitives: str/int enums are both
        return _encode_enum(value)
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, Intent):
        if getattr(value, "workflow", None) is not None:
            raise OfferNotPersistable("intent carries a workflow relationship")
        return {
            _INTENT_TAG: {
                "category": _encode(value.category),
                "action": value.action,
                "id": value.id,
                "context": _encode(dict(value.context or {})),
                "confidence": value.confidence,
                "original_message": value.original_message,
                "workflow_id": value.workflow_id,
                "created_at": value.created_at.isoformat() if value.created_at else None,
            }
        }
    if isinstance(value, datetime):
        return {_DATETIME_TAG: value.isoformat()}
    if isinstance(value, UUID):
        return {_UUID_TAG: str(value)}
    if isinstance(value, tuple):
        return {_TUPLE_TAG: [_encode(v) for v in value]}
    if isinstance(value, list):
        return [_encode(v) for v in value]
    if isinstance(value, dict):
        out: Dict[str, Any] = {}
        for k, v in value.items():
            if not isinstance(k, str):
                raise OfferNotPersistable(f"non-string key of type {type(k).__name__}")
            if k in _RESERVED_TAGS:
                # Arch 07:31: data that already carries a tag key (model JSON on
                # the Intent's context, say) is refused outright, so it can never
                # be mistaken for the codec's own tagging on the way back in.
                raise OfferNotPersistable(f"reserved tag key {k!r} in data")
            out[k] = _encode(v)
        return out
    raise OfferNotPersistable(f"value of type {type(value).__name__}")


def _encode_enum(value: Enum) -> Dict[str, Any]:
    name = _ENUM_TAG_BY_CLASS.get(type(value))
    if name is None:
        raise OfferNotPersistable(f"enum {type(value).__name__} not in the codec allowlist")
    return {_ENUM_TAG: name, "value": _encode(value.value)}


def _decode(value: Any) -> Any:
    if isinstance(value, list):
        return [_decode(v) for v in value]
    if not isinstance(value, dict):
        return value
    if len(value) == 1:
        if _DATETIME_TAG in value:
            return datetime.fromisoformat(value[_DATETIME_TAG])
        if _UUID_TAG in value:
            return UUID(value[_UUID_TAG])
        if _TUPLE_TAG in value:
            return tuple(_decode(v) for v in value[_TUPLE_TAG])
        if _INTENT_TAG in value:
            return _decode_intent(value[_INTENT_TAG])
    if _ENUM_TAG in value and set(value) == {_ENUM_TAG, "value"}:
        cls = _ENUM_ALLOWLIST.get(str(value[_ENUM_TAG]))
        if cls is None:
            raise ValueError("enum tag not in the codec allowlist")
        return cls(_decode(value["value"]))
    if _RESERVED_TAGS & set(value):
        # A tag key beside other keys, or a tag the branches above did not
        # claim: not the codec's own output. Drop the offer rather than guess.
        raise ValueError("malformed tag")
    return {k: _decode(v) for k, v in value.items()}


def _decode_intent(data: Dict[str, Any]) -> Any:
    from services.domain.models import Intent

    created = data.get("created_at")
    kwargs: Dict[str, Any] = {
        "category": _decode(data["category"]),
        "action": data["action"],
        "context": _decode(data.get("context") or {}),
        "confidence": data.get("confidence", 0.0),
        "original_message": data.get("original_message") or "",
        "workflow_id": data.get("workflow_id"),
    }
    if data.get("id"):
        kwargs["id"] = data["id"]
    if created:
        kwargs["created_at"] = datetime.fromisoformat(created)
    return Intent(**kwargs)


def encode_offer_record(record: Any) -> Optional[Dict[str, Any]]:
    """The offer record as a JSON-safe dict, or None when it cannot be
    persisted (logged; the offer keeps its in-process lifetime). Never raises."""
    if not isinstance(record, dict):
        return None
    try:
        encoded = _encode(record)
    except OfferNotPersistable as e:
        logger.warning(
            "pending_offer_not_persistable",
            workflow_type=str(record.get("workflow_type")),
            reason=str(e),
        )
        return None
    except Exception as e:  # silent-ok: logged; a codec fault must never take the slice write down
        logger.warning(
            "pending_offer_not_persistable",
            workflow_type=str(record.get("workflow_type")),
            reason=type(e).__name__,
        )
        return None
    return encoded if isinstance(encoded, dict) else None


def decode_offer_record(data: Any) -> Optional[Dict[str, Any]]:
    """Inverse of :func:`encode_offer_record`. Malformed input → None (fail-safe:
    an offer we cannot rebuild exactly is not re-armed)."""
    if not isinstance(data, dict):
        return None
    try:
        decoded = _decode(data)
    except (
        Exception
    ) as e:  # silent-ok: logged; a malformed persisted offer is dropped, never half-armed
        logger.warning("pending_offer_hydrate_malformed", reason=type(e).__name__)
        return None
    return decoded if isinstance(decoded, dict) else None


def offer_is_write_effect(record: Any) -> bool:
    """True when popping this offer may lead to a write (Arch's condition).

    The bound entry is the record's ``workflow_type`` in the workflow
    registry; WRITE or DESTRUCTIVE is write-effect. Fail-safe toward
    write-effect: an unknown or missing entry counts as a write, and so does a
    READ entry whose record carries a ``pending_action`` payload, because the
    kind-specific turn handlers at the pop seam own those turns and some of
    them write even though the generic landing they register is READ (the
    #1648 reminder-time answer saves the reminder at the seam; its
    ``clarify_reminder_time`` entry is READ). Over-persisting costs one small
    write; under-persisting is the double write the condition exists to stop.
    """
    if not isinstance(record, dict):
        return True
    from services.intent_service.workflow_dispatcher import WORKFLOW_REGISTRY
    from services.shared_types import EffectClass

    entry = WORKFLOW_REGISTRY.get(str(record.get("workflow_type")))
    effect = getattr(entry, "effect", None)
    if effect is None:
        return True
    if effect >= EffectClass.WRITE:
        return True
    return bool(record.get("pending_action"))


# The in-process half of the idempotency backstop: offer ids popped in this
# process. A context (re)hydrated in this process from a slice whose early
# persist failed still drops the spent offer. Bounded; oldest ids fall off.
_CONSUMED_LIMIT = 1024
_consumed_offer_ids: "OrderedDict[str, None]" = OrderedDict()


def note_consumed(offer_id: Optional[str]) -> None:
    if not offer_id:
        return
    _consumed_offer_ids[offer_id] = None
    _consumed_offer_ids.move_to_end(offer_id)
    while len(_consumed_offer_ids) > _CONSUMED_LIMIT:
        _consumed_offer_ids.popitem(last=False)


def was_consumed(offer_id: Optional[str]) -> bool:
    return bool(offer_id) and offer_id in _consumed_offer_ids
