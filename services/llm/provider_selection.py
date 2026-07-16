"""#1415 — per-user LLM provider SELECTION, resolved statelessly per call.

The incident (2026-07-16, PM's beta account): provider selection —
``default_llm_provider`` + the ``authorized_llm_providers`` consent list (#946)
— was read from GLOBAL keychain slots, so one tester's setup pinned the whole
instance and a second user's per-user key (#1185) was un-selectable. Selection
now resolves per acting principal, mirroring PersonalizationService's
stateless resolve-per-call pattern (ADR-075) and #1185's per-user key
resolution: nothing is cached per-process, nothing global shadows a user's own
choice.

Resolution chains (every call, no instance state):

  default provider:  per-user choice -> server/global choice -> env default
                     -> first available
  consent filter:    per-user list  -> server/global list    -> legacy (all
                     configured)
                     and on ANY read error: FAIL CLOSED to the server-default
                     provider only (census F1: the old code failed OPEN to all
                     configured providers, silently disabling the #946 consent
                     boundary).

Keychain slots (server/global slots kept for the local single-user install and
as the authenticated fallback; per-user slots are username-scoped per #1185):

  default_llm_provider          / {user}_default_llm_provider_api_key
  authorized_llm_providers      / {user}_authorized_llm_providers_api_key
"""

from __future__ import annotations

from typing import List, Optional

import structlog

logger = structlog.get_logger()

DEFAULT_SLOT = "default_llm_provider"
CONSENT_SLOT = "authorized_llm_providers"


def _keychain(keychain=None):
    if keychain is not None:
        return keychain
    from services.infrastructure.keychain_service import KeychainService

    return KeychainService()


def resolve_authorized_providers(
    user_id: Optional[str],
    all_configured: List[str],
    server_default: Optional[str],
    keychain=None,
) -> List[str]:
    """Apply the #946 consent filter for the acting principal.

    Per-user list first, then the server/global list, else legacy behavior
    (no list anywhere -> everything configured is authorized).

    FAIL CLOSED (#1415 F1): if the consent read errors, return the
    server-default provider only (if configured) — never the full configured
    set. A keychain hiccup must not route a user's messages to providers they
    explicitly de-authorized; it also must not brick the instance, so the
    operator's default stays usable.
    """
    kc = _keychain(keychain)
    try:
        raw = None
        if user_id:
            raw = kc.get_api_key(CONSENT_SLOT, username=str(user_id))
        if not raw:
            # global-ok: server-level consent list — the per-user slot was checked first (#1415)
            raw = kc.get_api_key(CONSENT_SLOT)
        if raw:
            allowed = {p.strip().lower() for p in raw.split(",") if p.strip()}
            return [p for p in all_configured if p.lower() in allowed]
        return list(all_configured)
    except Exception as e:  # silent-ok: fail-CLOSED consent — degrades to server default only, logged; never widens to de-authorized providers (#1415 F1)
        logger.warning(
            "authorized_providers_read_failed_failing_closed",
            error=str(e),
            user_id=str(user_id) if user_id else None,
            fallback=server_default,
        )
        return [p for p in all_configured if server_default and p == server_default]


def resolve_default_provider(
    user_id: Optional[str],
    available: List[str],
    env_default: Optional[str] = None,
    keychain=None,
) -> Optional[str]:
    """Resolve the provider to use for the acting principal.

    Chain: the user's own stored choice -> the server/global stored choice ->
    the env default -> first available. Every step is validated against
    ``available`` (already consent-filtered by the caller), so a stored choice
    pointing at an unavailable/de-authorized provider falls through instead of
    hard-failing (PM 2026-07-16: selection must never lock a user out).

    Returns None when ``available`` is empty (caller decides how to degrade).
    """
    if not available:
        return None
    kc = _keychain(keychain)

    if user_id:
        try:
            choice = kc.get_api_key(DEFAULT_SLOT, username=str(user_id))
            if choice:
                if choice in available:
                    return choice
                logger.info(
                    "user_provider_choice_unavailable_falling_through",
                    user_id=str(user_id),
                    choice=choice,
                    available=available,
                )
        except Exception as e:  # silent-ok: selection falls through to the server default; failure never widens access, only affects which authorized provider serves (#1415)
            logger.warning("user_provider_choice_read_failed", error=str(e))

    try:
        # global-ok: server-level default — the per-user slot was checked first (#1415)
        choice = kc.get_api_key(DEFAULT_SLOT)
        if choice and choice in available:
            return choice
    except Exception as e:  # silent-ok: selection falls through to the env default; failure never widens access (#1415)
        logger.warning("server_provider_choice_read_failed", error=str(e))

    if env_default and env_default in available:
        return env_default
    return available[0]
