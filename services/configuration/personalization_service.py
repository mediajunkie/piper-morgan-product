"""Personalization resolution service (ADR-075 Component B, #1366).

Resolves the system-prompt personalization content for a given principal —
the load-bearing closure of the #1366 leak: on a shared instance, a request
with no scoped personalization record for its principal degrades to a NEUTRAL
default, never to PM's personal `PIPER.user.md` (ADR-075 D4).

Deliberately a NEW, separate service rather than a change to
`piper_config_loader`'s existing sync methods (m-40 layer-then-migrate): the
loader's `get_system_prompt()` signature is unchanged and still works exactly
as before for any caller that doesn't thread a `user_id` (the D3 single-tenant/
local-dev default keeps working with zero regression). Callers that DO have a
resolved principal and are already in an async context (conversational_floor,
the classifiers) opt into this service instead.

Resolution order (D3 + D4):
  1. `user_id` is None (no principal resolved — ambient/legacy/local-dev call)
     → serve the file directly, unchanged behavior.
  2. `user_id` resolves to the configured PM (`resolve_pm_owner_id`) → serve
     the file directly (D3: "the file IS that owner's config" for the
     single-owner case — PM's own requests never regress to a generic prompt).
  3. `user_id` is a real, distinct principal → the owner_id-scoped
     `PersonalizationContext` row for that principal, if one exists;
     otherwise lazy-seed one with the neutral default and use that (OQ-3 /
     HOST's "real seeded record, not implicit empty fall-through").
  4. Anything else degrades gracefully to the file (never a crash, never
     silently empty — matches ADR-070 D5 / ADR-071 D3's never-silently-empty
     invariant one layer up).
"""

from __future__ import annotations

from typing import Optional
from uuid import UUID

import structlog

from services.configuration.personalization_repository import PersonalizationContextRepository

logger = structlog.get_logger()

# ADR-075 OQ-3 (CXO UX direction, 2026-07-06): the seeded neutral-default
# persona — a genuinely capable professional PM assistant, NOT PM's own
# portfolio/priorities/repos, NOT a generic chatbot, NOT blank. Keyed with the
# SAME section names `PiperConfigLoader._format_system_prompt()` already
# parses from PIPER.user.md, so both sources render through one formatter.
NEUTRAL_DEFAULT_CONTEXT: dict = {
    "User Context": (
        "You're speaking with a product manager. Communicate in a direct, "
        "concise, colleague register — like a sharp product-minded peer, "
        "not a formal assistant. No portfolio or standing priorities are "
        "on file for this account yet; work from what's in the conversation "
        "itself rather than assuming context you don't have."
    ),
    "Standing Priorities": (
        "Product development and team coordination — help with whatever "
        "the immediate need is, without assuming a specific existing "
        "portfolio or project history."
    ),
}

# ADR-075 OQ-3 (CXO UX direction): first-response injection copy. Appended
# ONCE, after the answer (capability first, metadata second), never before,
# never per-response. Capability-affirming register, not a degraded/error
# state; actionable (points at Settings -> Profile); non-catastrophizing.
FIRST_RESPONSE_PERSONALIZATION_NOTICE = (
    "(Running with a default configuration for now — I'm fully useful "
    "as-is, but once you add your context in Settings → Profile, "
    "I'll be tuned to your role and priorities.)"
)


async def _resolve_pm_owner_id_safe(session) -> Optional[UUID]:
    """`resolve_pm_owner_id`, tolerant of the lookup failing (D4: must degrade,
    never crash the personalization path over an unrelated PM-identity issue).
    """
    try:
        from services.repositories.document_repository import resolve_pm_owner_id

        return await resolve_pm_owner_id(session)
    except Exception as e:
        logger.warning("personalization_pm_owner_resolution_failed", error=str(e))
        return None


def _as_uuid_or_none(value) -> Optional[UUID]:
    if isinstance(value, UUID):
        return value
    try:
        return UUID(str(value))
    except (ValueError, TypeError, AttributeError):
        return None


class PersonalizationService:
    """ADR-075 D4 principal-resolution + neutral-degradation for the
    system-prompt personalization path."""

    async def resolve_system_prompt(self, user_id: Optional[str], session) -> str:
        """The system prompt for this principal — PM's file, the principal's
        own personalization record, or the seeded neutral default. Never
        raises; every failure path degrades to the existing file-based
        behavior (D3's no-regression guarantee doubles as the fail-closed
        default here, since the file behavior is what every caller already
        depended on before Component B existed).
        """
        from services.configuration.piper_config_loader import piper_config_loader

        principal = _as_uuid_or_none(user_id)
        if principal is None:
            # No resolved principal (ambient/legacy/local-dev call) — D3.
            return piper_config_loader.get_system_prompt()

        pm_owner_id = await _resolve_pm_owner_id_safe(session)
        if pm_owner_id is not None and pm_owner_id == principal:
            # PM's own request — D3 no-regression, serve the file directly.
            return piper_config_loader.get_system_prompt()

        try:
            repo = PersonalizationContextRepository(session)
            row = await repo.get_or_seed_default(principal, NEUTRAL_DEFAULT_CONTEXT)
            if row is None:
                # Shouldn't happen (principal is already a valid UUID at this
                # point), but degrade gracefully rather than crash if it does.
                return piper_config_loader.get_system_prompt()
            return piper_config_loader._format_system_prompt(dict(row.context))
        except Exception as e:
            logger.warning(
                "personalization_context_resolution_failed",
                user_id=str(principal),
                error=str(e),
            )
            return piper_config_loader.get_system_prompt()

    async def is_seeded_default(self, user_id: Optional[str], session) -> bool:
        """True if this principal is currently running on the lazy-seeded
        neutral default (never customized) — drives the first-response
        injection decision. False for PM, for a None principal, and for any
        principal with a real (non-default) personalization record.
        """
        principal = _as_uuid_or_none(user_id)
        if principal is None:
            return False

        pm_owner_id = await _resolve_pm_owner_id_safe(session)
        if pm_owner_id is not None and pm_owner_id == principal:
            return False

        try:
            repo = PersonalizationContextRepository(session)
            row = await repo.get(principal)
            return bool(row and row.is_seeded_default)
        except Exception as e:
            logger.warning(
                "personalization_seeded_check_failed", user_id=str(principal), error=str(e)
            )
            return False

    async def resolve_system_prompt_standalone(self, user_id: Optional[str]) -> str:
        """`resolve_system_prompt`, opening its own DB session — a convenience
        for callers (the classifiers) that aren't already inside one. Prefer
        `resolve_system_prompt(user_id, session)` directly when the caller
        already has a session in scope (avoids a second connection)."""
        from services.database.session_factory import AsyncSessionFactory

        async with AsyncSessionFactory.session_scope() as session:
            return await self.resolve_system_prompt(user_id, session)

    async def maybe_consume_first_response_notice(self, user_id: Optional[str]) -> Optional[str]:
        """ADR-075 OQ-3 (CXO UX direction): if this principal is on the seeded
        neutral default and hasn't seen the personalization notice yet, mark
        it seen and return the notice text to append after the answer.
        Returns None for PM, a None principal, a customized profile, or a
        principal who's already seen it — the "never reappears, never
        per-response" invariant. Opens its own session (this is a boundary
        call, mirroring `resolve_system_prompt_standalone`).

        Check-and-mark happen in the same session/transaction — not a hard
        real-time race guarantee, but sufficient for a one-time onboarding
        notice (not a security boundary; worst case on a genuine race is the
        notice showing twice for one user, not a leak).
        """
        principal = _as_uuid_or_none(user_id)
        if principal is None:
            return None

        from services.database.session_factory import AsyncSessionFactory

        try:
            async with AsyncSessionFactory.session_scope() as session:
                pm_owner_id = await _resolve_pm_owner_id_safe(session)
                if pm_owner_id is not None and pm_owner_id == principal:
                    return None

                repo = PersonalizationContextRepository(session)
                # Self-sufficient: don't assume an earlier call in this same
                # request already seeded the row (e.g. a cache-hit
                # classification skips resolve_system_prompt entirely — see
                # classifier.py's cache_eligible path). Seed here if needed
                # rather than silently no-op on `row is None`.
                row = await repo.get_or_seed_default(principal, NEUTRAL_DEFAULT_CONTEXT)
                if row is None or not row.is_seeded_default or row.has_seen_personalization_notice:
                    return None

                await repo.mark_notice_seen(principal)
                return FIRST_RESPONSE_PERSONALIZATION_NOTICE
        except Exception as e:
            logger.warning(
                "personalization_first_response_notice_failed",
                user_id=str(principal),
                error=str(e),
            )
            return None


personalization_service = PersonalizationService()
