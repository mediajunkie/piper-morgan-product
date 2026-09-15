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
                     and on a FAILED read: FAIL CLOSED by REFUSING the turn
                     (``ConsentUnreadableError``). Census F1 established the
                     fail-closed requirement; #1816 made it reachable (the old
                     branch could not fire in production) and #1815 Gap 2
                     replaced its "narrow to the server default" degradation
                     with a refusal, because PM abolished the server-key
                     concept (#1812). See ``resolve_authorized_providers``.

Keychain slots (server/global slots kept for the local single-user install and
as the authenticated fallback; per-user slots are username-scoped per #1185):

  default_llm_provider          / {user}_default_llm_provider_api_key
  authorized_llm_providers      / {user}_authorized_llm_providers_api_key
"""

from __future__ import annotations

from typing import List, Optional

import structlog

from services.infrastructure.keychain_service import SecretProvenance, SecretRead

logger = structlog.get_logger()

DEFAULT_SLOT = "default_llm_provider"
CONSENT_SLOT = "authorized_llm_providers"


def _keychain(keychain=None):
    if keychain is not None:
        return keychain
    from services.infrastructure.keychain_service import KeychainService

    return KeychainService()


def _read_slot(kc, username: Optional[str]) -> SecretRead:
    """One consent-slot read, with provenance, from whatever keychain we were given.

    ``keychain=`` is an injection point, so this must cope with stand-ins that
    implement only the ``get_api_key`` primitive. It deliberately validates the
    RESULT rather than probing for the attribute: a ``Mock(spec=KeychainService)``
    grows a ``read_secret`` that returns a ``Mock``, whose ``.store_failed`` is
    truthy — i.e. attribute-presence detection would make every such stand-in
    refuse every turn while looking like a real provenance read. Trust the shape
    you got back, not the name you found.

    For a stand-in on the primitive path, an exception propagates (the caller
    converts it to STORE_FAILED) and a ``None`` is a verified absence — which is
    the truth for a dict-backed double.
    """
    reader = getattr(kc, "read_secret", None)
    if reader is not None:
        read = reader(CONSENT_SLOT, username=username)
        if isinstance(read, SecretRead):
            return read

    value = kc.get_api_key(CONSENT_SLOT, username=username)
    if isinstance(value, str) and value:
        return SecretRead(SecretProvenance.PRESENT, value=value)
    return SecretRead(SecretProvenance.VERIFIED_ABSENT)


def _read_consent_slot(kc, user_id: Optional[str]) -> SecretRead:
    """Read the consent slot for the acting principal (#1816).

    Per-user slot first, then the server/global slot — but only ever falling
    through on a **verified absence**. A failed read of the per-user slot stops
    here: falling through to the global list on an error would be the same
    absence-means-permission mistake one slot down, and the global list is
    typically the permissive one.
    """
    if user_id:
        per_user = _read_slot(kc, str(user_id))
        if not per_user.is_verified_absent:
            return per_user
    # global-ok: server-level consent list — the per-user slot was checked first (#1415)
    return _read_slot(kc, None)


def resolve_authorized_providers(
    user_id: Optional[str],
    all_configured: List[str],
    keychain=None,
) -> List[str]:
    """Apply the #946 consent filter for the acting principal.

    Per-user list first, then the server/global list, else legacy behavior
    (no list anywhere -> everything configured is authorized).

    FAIL CLOSED (#1415 F1, repaired by #1816): if the consent read FAILS, this
    raises ``ConsentUnreadableError`` and the turn is refused. It never returns
    the full configured set, and it no longer narrows to the server default.

    ⚠️ Read the two rulings behind that sentence before changing it:

    **#1816 — why the read is provenance-carrying.** The F1 fail-closed branch
    was *unreachable in production*. ``KeychainService.get_api_key`` swallows
    ``Exception`` and returns ``None`` (correctly, for a credential — #1711), so
    a real keyring failure never reached the old ``except``; control fell to
    ``return list(all_configured)``, the fail-OPEN path F1 was written to
    eliminate. Measured 2026-09-15 with a real ``KeychainService`` and a raising
    backend: ``['anthropic', 'openai']``. **Absence was read as permission.**
    The cure is a read that reports WHY (``KeychainService.read_secret``), not a
    change to the credential primitive — see ``SecretProvenance``.

    **#1815 Gap 2 — why the closed state refuses instead of degrading.** F1's
    closed state was "the server-default provider only", which assumes a server
    that owns a key. PM ruled that concept abolished (#1812), so degrading to it
    would silently reassign a BYOC user's turn to a credential that should not
    exist — and on a BYOC-only instance it resolves to ``[]`` anyway, which
    manufactures the #1814 "no provider configured" wall from a second cause.
    Refusing with the #1807-family error is the honest closed state.

    Raises:
        ConsentUnreadableError: the consent list could not be read.
    """
    from services.llm.request_key import ConsentUnreadableError

    kc = _keychain(keychain)
    try:
        read = _read_consent_slot(kc, user_id)
    except Exception as e:  # silent-ok: NOT a swallow — the exception is converted to STORE_FAILED provenance, which the very next block logs and re-raises as ConsentUnreadableError. This handler exists so a keychain stand-in that signals failure by RAISING and one that signals it by returning STORE_FAILED land on the same fail-closed path (#1816).
        read = SecretRead(SecretProvenance.STORE_FAILED, error=str(e))

    if read.store_failed:
        logger.warning(
            "authorized_providers_read_failed_refusing",
            error=read.error,
            user_id=str(user_id) if user_id else None,
            configured=all_configured,
        )
        raise ConsentUnreadableError(
            "Could not read the authorized-provider list for this caller — "
            "refusing the turn rather than guessing at consent (#1816/#1815)."
        )

    if read.is_present and read.value:
        allowed = {p.strip().lower() for p in read.value.split(",") if p.strip()}
        return [p for p in all_configured if p.lower() in allowed]

    # VERIFIED ABSENT — no consent list anywhere. Legacy behavior: everything
    # configured is authorized. This is the "consent inferred from key presence"
    # inference, and per Arch's ruling (2026-09-15 §4) it is a DATED ASSUMPTION,
    # not a design:
    #
    #   Consent is inferred from key presence. Dated 2026-09-15. This is valid
    #   ONLY while no surface lets a user de-authorize a provider whose key they
    #   still hold — today the consent list has exactly one writer (/setup) and
    #   is derived mechanically from which keys the user supplied, so "has a key"
    #   and "authorized it" cannot disagree. THE FIRST SUCH DE-AUTHORIZE SURFACE
    #   INVALIDATES THIS LINE: from that moment a verified-absent list stops
    #   meaning "nothing was restricted" and starts meaning "we never asked", and
    #   this branch must be revisited rather than inherited. INVALIDATION TRIGGER
    #   TRACKED ON #1817; an inferred consent that carries no expiry silently
    #   becomes a claim about a user's wishes the user never made.
    return list(all_configured)


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
