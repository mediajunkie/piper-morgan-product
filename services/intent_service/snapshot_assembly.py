"""SessionSnapshot ASSEMBLY — populate the #1595 Phase 2.0 contract from the real stores.

Sibling to ``session_snapshot.py`` deliberately: that file is the
Lead-authored CONTRACT (dataclass, serialization, caps — the golden-pin
review surface) and stays byte-identical through this phase; this file is
the implementation bound to it. The one-direction dependency is legible in
the imports: assembly reads the contract, never the reverse, and neither
file touches the Inversion's constrained router module (the shadow observer
stays the only module that may — TestInversionShadowNoExecutionBoundary's
token scan enforces it, which is also why this sentence names no modules).

Every read here honors the contract's five items; the load-bearing ones:

- **Item 1 (read-only)**: the offer store is PEEKED via
  ``WorkflowOfferService.peek_pending_offer`` (never the pop); the process
  probe is ``ProcessRegistry.first_active_type`` — see its docstring for
  the ONE accepted convergent side effect (lazy timeout housekeeping the
  next claim check would apply identically; adapters.py tail-timeout
  blocks). Nothing else writes anything.
- **Item 2 (cheap)**: the peek is a dict lookup; the probe is the same
  read process_intent's claim check already runs; the three DB reads
  (ledger head, working mode, clear verb) are the same owner-scoped
  queries the classifier Stage-0 / #1510 / #1605 paths already run
  per-turn. No LLM calls. Measured typical: see the #1595 review notes.
- **Item 3 (fail-open, field by field)**: each read group is wrapped;
  a raise yields None/default for exactly its fields plus a
  ``field_errors`` entry, in dataclass declaration order. One honest
  asymmetry, documented rather than hidden: ``get_verified_inference``
  swallows storage errors INTERNALLY by its own documented fail-safe
  (returns None), so a store-level failure there reads as
  "nothing stored" without a ``field_errors`` entry — the wrapper here
  still catches anything that raises through it.

``pending_offer_question`` is the offer's rendered ask
(``offer["question"]`` / ``pending_action["question"]``). Since issue 1665
every #846 arm site stores the ALREADY-RENDERED copy it just said to the
user (and the re-arm seams update it as the open question changes state),
so this field is populated in the normal case; None remains honest for a
record that predates its arm site's question or a third-party offer, and
``serialize_for_prompt`` renders the explicit "(question text unavailable)"
marker for it.

``pending_offer_is_confirm`` derives from the offer KIND via
``destructive_confirm.offer_is_confirm`` — the #1650 confirm-kind table in
ONE place (issue 1664: repo clarification rides the confirm carrier's
workflow_type with a non-yes/no open question, so carrier-derived
confirm-ness mislabeled it "(yes/no confirm)").
"""

from __future__ import annotations

import asyncio
import dataclasses
from typing import Any, Optional, Set

import structlog

from services.intent_service.session_snapshot import SessionSnapshot

logger = structlog.get_logger(__name__)

_FIELD_ORDER = tuple(f.name for f in dataclasses.fields(SessionSnapshot))


def _ordered(errors: Set[str]) -> tuple:
    """field_errors in dataclass declaration order (contract: deterministic)."""
    return tuple(name for name in _FIELD_ORDER if name in errors)


async def assemble_session_snapshot(
    session_id: Optional[str],
    user_id: Optional[str],
    intent_service: Any,
) -> SessionSnapshot:
    """Populate a :class:`SessionSnapshot` from the live stores. Never raises.

    ``intent_service`` supplies the session-scoped in-memory stores the pop
    seam already uses (``workflow_offer_service``); the process registry is
    the singleton; the DB-backed reads are the existing owner-scoped paths
    (see module docstring). Owner-scoping: the ledger and preference reads
    require ``user_id`` (D1a — no principal, no read, field stays None
    WITHOUT a field_errors entry: unscopeable is not an error).
    """
    errors: Set[str] = set()

    # --- armed state + draft state: ONE peek feeds five fields (#846) ---
    pending_offer_kind: Optional[str] = None
    pending_offer_question: Optional[str] = None
    pending_offer_is_confirm = False
    draft_in_compose = False
    draft_title: Optional[str] = None
    try:
        offer = None
        if session_id:
            # #1595 observer peek — read-only by construction (never the pop).
            offer = intent_service.workflow_offer_service.peek_pending_offer(
                session_id, user_id=user_id
            )
        if offer:
            from services.intent_service.destructive_confirm import (
                offer_is_confirm,
            )
            from services.intent_service.drafted_issue import DRAFTED_ISSUE_KIND

            pending_action = offer.get("pending_action") or {}
            pending_offer_kind = pending_action.get("kind") or None
            # The rendered ask the arm site stored (#1665; see module docstring).
            question = offer.get("question") or pending_action.get("question")
            pending_offer_question = question if isinstance(question, str) else None
            # #1664: confirm-ness derives from the offer KIND (the #1650
            # confirm-kind table, one home in destructive_confirm) — never
            # from the carrier workflow_type, which the open repo question
            # also rides.
            pending_offer_is_confirm = offer_is_confirm(offer)
            if pending_offer_kind == DRAFTED_ISSUE_KIND:
                # The draft rides pending_action["draft"] (#1571 carrier;
                # title None while untitled — the #1630 subjectless arm).
                draft = pending_action.get("draft") or {}
                draft_in_compose = True
                title = draft.get("title")
                draft_title = title if isinstance(title, str) and title else None
    except Exception as e:  # silent-ok: contract item 3 — the field group fails open (None/defaults + field_errors); a snapshot read must never break the turn
        logger.warning("snapshot_offer_peek_failed", error=str(e))
        errors.update(
            {
                "pending_offer_kind",
                "pending_offer_question",
                "pending_offer_is_confirm",
                "draft_in_compose",
                "draft_title",
            }
        )

    # --- the four awaited reads are independent → gathered concurrently
    #     (contract item 2: assembly latency ≈ the slowest single read, not
    #     the sum — measured 7.1ms median sequential vs ~3ms gathered on
    #     real Postgres 5433). Concurrency, not caching: each read is still
    #     its store's existing per-turn path, run once, uncached. Error
    #     attribution stays per-field: each probe wraps itself and reports
    #     its own field names into ``errors``.

    async def _probe_process() -> Optional[str]:
        # Read-only probe; accepted convergent side effect documented on
        # first_active_type (adapters.py lazy timeouts).
        try:
            from services.process.registry import get_process_registry

            return await get_process_registry().first_active_type(user_id, session_id)
        except Exception as e:  # silent-ok: contract item 3 — fails open to None + field_errors
            logger.warning("snapshot_process_probe_failed", error=str(e))
            errors.add("active_process_type")
            return None

    async def _read_ledger_head():
        # The #1394 ledger head, owner-scoped (D1a: no principal → no read,
        # handled by the caller's gate below).
        if not user_id or not session_id:
            # The call site gates on both already; mirrored here because a
            # closure can't carry that narrowing (D1a: unscoped read forbidden).
            return None
        try:
            from services.intent_service.session_activity_read import (
                issue_head,
                list_session_activities,
            )

            return issue_head(await list_session_activities(user_id, session_id))
        except Exception as e:  # silent-ok: contract item 3 — fails open to None + field_errors
            logger.warning("snapshot_ledger_read_failed", error=str(e))
            errors.update({"recent_issue_number", "recent_issue_repo"})
            return None

    async def _read_mode() -> Optional[str]:
        # #1510 declared mode (read_declared_working_mode raises on storage
        # error BY DESIGN so this wrapper can name the field).
        try:
            from services.intent_service.collaboration_gate import (
                read_declared_working_mode,
            )

            return await read_declared_working_mode(user_id)
        except Exception as e:  # silent-ok: contract item 3 — fails open to None + field_errors
            logger.warning("snapshot_working_mode_read_failed", error=str(e))
            errors.add("declared_working_mode")
            return None

    async def _read_clear_verb() -> Optional[str]:
        # #1605 per-verb default (belt over get_verified_inference's own
        # internal fail-safe — see module docstring asymmetry note).
        try:
            from services.intent_service.reminder_clear import inference_key
            from services.intent_service.verified_inference import (
                get_verified_inference,
            )

            record = await get_verified_inference(user_id, inference_key("clear"))
            value = (record or {}).get("value")
            return value if isinstance(value, str) and value else None
        except Exception as e:  # silent-ok: contract item 3 — fails open to None + field_errors
            logger.warning("snapshot_clear_verb_read_failed", error=str(e))
            errors.add("stored_clear_verb")
            return None

    async def _none() -> None:
        return None

    active_process_type, head, declared_working_mode, stored_clear_verb = (
        await asyncio.gather(
            _probe_process(),
            _read_ledger_head() if (user_id and session_id) else _none(),
            _read_mode() if user_id else _none(),
            _read_clear_verb() if user_id else _none(),
        )
    )

    recent_issue_number: Optional[int] = None
    recent_issue_repo: Optional[str] = None
    if head is not None:
        recent_issue_repo, recent_issue_number = head

    return SessionSnapshot(
        pending_offer_kind=pending_offer_kind,
        pending_offer_question=pending_offer_question,
        pending_offer_is_confirm=pending_offer_is_confirm,
        active_process_type=active_process_type,
        draft_in_compose=draft_in_compose,
        draft_title=draft_title,
        recent_issue_number=recent_issue_number,
        recent_issue_repo=recent_issue_repo,
        declared_working_mode=declared_working_mode,
        stored_clear_verb=stored_clear_verb,
        field_errors=_ordered(errors),
    )
