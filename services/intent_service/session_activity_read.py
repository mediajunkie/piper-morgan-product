"""Shared owner-scoped session-activity ledger read (#1394 / #1595).

ONE home for the ledger query that both the B3 referent resolver
(``classifier._resolve_issue_referent``) and the #1595 snapshot assembly
(``snapshot_assembly.assemble_session_snapshot``) need — extracted so the
query exists exactly once instead of as copied branches (the #1555 lesson:
a duplicated read drifts, and the drifted copy is the one that bites).

Error semantics are deliberately the CALLER's business: ``list_session_activities``
raises on storage error. The two consumers degrade differently —
B3 falls through to normal classification (pass-through, logged), the
snapshot assembly maps the raise to None fields + a ``field_errors`` entry
(contract item 3). Swallowing here would force one degradation on both.

D1a (ADR-078) holds by signature: both arguments are required — there is no
unscoped form of this read.
"""

from __future__ import annotations

from typing import Any, List, Optional, Tuple


async def list_session_activities(user_id: str, session_id: str) -> List[Any]:
    """The owner-scoped #1394 ledger read (newest first, per repository order).

    Raises on storage error — callers own their degradation (see module
    docstring). Never call with a missing owner/session: D1a forbids an
    unscoped read, so callers gate on both before calling.
    """
    from services.database.repositories import SessionActivityRepository
    from services.database.session_factory import AsyncSessionFactory

    async with AsyncSessionFactory.session_scope() as session:
        return await SessionActivityRepository(session).list_for_session(
            owner_id=str(user_id), conversation_id=str(session_id)
        )


def issue_head(activities: List[Any]) -> Optional[Tuple[str, int]]:
    """Parse the ledger head: newest ``issue_created`` row → ``(repository, number)``.

    ``target_ref`` is ``"owner/repo#107"``; a missing row, a ref without
    ``#``, or a malformed number all return None (nothing to fabricate —
    B3's N1 guard, reused verbatim by the snapshot assembly).
    """
    latest = next((a for a in activities if a.action_type == "issue_created"), None)
    if latest is None:
        return None
    ref = latest.target_ref or ""
    if "#" not in ref:
        return None
    repository, _, num = ref.rpartition("#")
    if not repository or not num.isdigit():
        return None
    return repository, int(num)
