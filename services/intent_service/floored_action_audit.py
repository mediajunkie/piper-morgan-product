"""#2327: note a floored action name that is outside every vocabulary.

#2270 was a handler gap: the legacy classifier invented ``analyze_repository``, a
name in no vocabulary; it was floored, the floor's reply looked like working
behaviour, and the gap was found days later from a live mismatch. Four fallthrough
sites floor an action; this is the check they share.

Arch's ruling (2026-11-14), HOST's content bar:

- The check uses ``routing_vocabulary.importable_vocabulary()`` only (computed once).
  A pre-classifier name may be over-reported; the tally script filters those.
- What is recorded: the site, the action name ONLY when it is a short identifier
  (``routing_vocabulary.fits_recorded_shape``), else withheld (never truncated), and the message's
  sha256. No message text, no user id, nothing else.
- It feeds two things: one evidence line (``piper.evidence``, so it survives the
  hosts' WARNING root logger) and a counter row keyed by (name, site, UTC day) that
  an admin can read without a served-log read.
- It never fails the person's turn: any error here is logged and swallowed.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Dict, Optional

import structlog

from services.infrastructure.logging.evidence import evidence
from services.intent_service.routing_vocabulary import fits_recorded_shape, importable_vocabulary
from services.utils.utterance_log import utterance_sha256

logger = structlog.get_logger(__name__)

EVIDENCE_EVENT = "floored_action_outside_vocabulary"
# The counter's value for a name that is off the shape. It cannot match the shape
# (parentheses), so it can never collide with a real name.
WITHHELD = "(withheld)"

SITE_CANONICAL_GENERIC = "canonical_generic_detected_routing_to_floor"
SITE_QUERY_ACTION = "query_action_routing_to_floor"
SITE_ANALYSIS_ACTION = "analysis_action_routing_to_floor"
SITE_ACTION_GATE = "action_gate_routing_to_floor"
SITES = frozenset(
    {SITE_CANONICAL_GENERIC, SITE_QUERY_ACTION, SITE_ANALYSIS_ACTION, SITE_ACTION_GATE}
)


def outside_vocabulary(action: Any) -> bool:
    """True when ``action`` is a non-empty string no importable vocabulary knows.
    No action at all (None, empty) is not an invented name."""
    return (
        isinstance(action, str) and bool(action.strip()) and action not in importable_vocabulary()
    )


def recorded_name(action: str) -> Optional[str]:
    """The name as it may be recorded, or ``None`` when it must be withheld."""
    return action if fits_recorded_shape(action) else None


async def _increment(name: str, site: str) -> None:
    """One idempotent upsert: the row for (name, site, today in UTC) gains one. Its
    own short session, so nothing here touches the turn's own transaction."""
    from sqlalchemy.dialects.postgresql import insert

    from services.database.models import FlooredActionCountDB
    from services.database.session_factory import AsyncSessionFactory

    day = datetime.now(timezone.utc).date()
    statement = insert(FlooredActionCountDB).values(name=name, site=site, day=day, count=1)
    statement = statement.on_conflict_do_update(
        index_elements=["name", "site", "day"],
        set_={"count": FlooredActionCountDB.count + 1},
    )
    async with AsyncSessionFactory.session_scope() as session:
        await session.execute(statement)
        await session.commit()


async def note_floored_action(site: str, action: Any, message: Optional[str]) -> None:
    """Called at each floor fallthrough site, after its own log line. Records only a
    name outside the importable vocabulary. Never raises."""
    try:
        if site not in SITES:
            logger.warning("floored_action_audit_unknown_site", site=site)
            return
        if not outside_vocabulary(action):
            return
        name = recorded_name(action)
        fields: Dict[str, Any] = {
            "site": site,
            "message_sha256": utterance_sha256(message or ""),
        }
        if name is None:
            fields["action_withheld"] = True
        else:
            fields["action"] = name
        # A literal name: the evidence pin reads call sites for listed literals.
        evidence("floored_action_outside_vocabulary", **fields)
    except Exception as e:  # silent-ok: logged; an audit note must never fail the person's turn
        logger.warning("floored_action_audit_failed", error=str(e))
        return
    try:
        await _increment(name if name is not None else WITHHELD, site)
    except (
        Exception
    ) as e:  # silent-ok: logged; the evidence line above already recorded the sighting
        logger.warning("floored_action_count_failed", error=str(e), site=site)
