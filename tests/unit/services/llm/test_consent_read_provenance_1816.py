"""#1816 + #1815 Gap 2 — a consent boundary that failed OPEN, and a closed state that refuses.

THE DEFECT (#1816). ``services/llm/provider_selection.py::resolve_authorized_providers``
documented a security guarantee — *"a keychain hiccup must not route a user's messages to
providers they explicitly de-authorized"* — that the code could not deliver. One layer
down, ``KeychainService.get_api_key`` swallows ``Exception`` and returns ``None``. So a
REAL keyring failure never reached the #1415 F1 ``except``; ``raw`` was merely falsy and
control fell to ``return list(all_configured)`` — the fail-OPEN path F1 was written to
eliminate. **Absence was read as permission.** Only an injected raising double reached the
closed branch, which is precisely why green tests survived alongside the hole.

Root shape (Arch, 2026-09-15 §2): the honest-empty family at the security layer.
``None`` was doing two incompatible jobs. For a CREDENTIAL, absent and unreadable both
truthfully mean *try the next source* (#1711, sound, unchanged). For a CONSENT list they
mean opposite things. The cure is a provenance-carrying read, not a change to the
credential primitive — and ``TestTheCredentialPrimitiveIsUntouched`` pins that ruling so a
later "cleanup" cannot quietly widen #1711's blast radius.

THE RULING ON THE CLOSED STATE (#1815 Gap 2, Arch §3). F1's degradation — "narrow to the
server-default provider" — assumed a server that owns a key. PM ruled that concept
abolished (#1812), and on a BYOC-only instance it resolves to ``[]``, manufacturing the
#1814 "no provider configured" wall from a second cause. The closed state now REFUSES with
``ConsentUnreadableError``. Fail-closed means closed, not quietly reassigned to the
operator's key.

LAYER (m-43). Four seams, each measured where it can actually fail:
  1. the REAL ``KeychainService`` with a genuinely failing backend — keyring raising,
     keyring hung (#1711), and the #1382 DB store raising. **Not an injected keychain
     double**: a double measures the other branch and reports clean, which is exactly what
     let this survive. This is the layer the defect lived on.
  2. ``LLMConfigService.get_configured_providers`` — that it PROPAGATES rather than
     substituting a list.
  3. ``LLMClient._complete_raw`` — that the refusal is not swallowed by the blanket
     selection handler and served from the operator's own initialized client. Measured
     before the fix: it was.
  4. ``IntentService._process_intent_internal`` and the ``/api/v1/intent`` route — that the
     refusal reaches the user as its own honest copy, not as "service unavailable, try
     again" and not as "add a key you already have".

DENOMINATOR. One consent slot (``authorized_llm_providers``) on one resolver, plus the
four seams above. NOT covered: the ``default_llm_provider`` slot's three ``except``
branches in the same module (they read SELECTION, not consent — a failure there narrows
which authorized provider serves and cannot widen access), other consumers of
``get_api_key`` for the same absence-means-permission shape (unaudited; plausible), a live
billable vendor call, and the Slack/MCP entry points, which do not route through /intent.
"""

import asyncio
import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from services.infrastructure import keychain_service as ks_module
from services.infrastructure.keychain_service import (
    KeychainService,
    KeychainTimeoutError,
    SecretProvenance,
)
from services.intent_service.conversational_floor import (
    FLOOR_FALLBACK_AUTH,
    FLOOR_FALLBACK_CONSENT_UNREADABLE,
    FLOOR_FALLBACK_NO_PROVIDER,
    FLOOR_FALLBACK_TRANSIENT,
    _classify_llm_error,
)
from services.llm.provider_selection import CONSENT_SLOT, resolve_authorized_providers
from services.llm.request_key import ConsentUnreadableError, LLMKeyRequiredError
from web.api.routes.intent import router as intent_router

ALL_CONFIGURED = ["anthropic", "openai"]

SECRET = "test-secret-1816-not-a-real-key"


class _ExplodingStore:
    """A #1382 encrypted-DB credential store whose reads fail."""

    def get(self, key):
        raise RuntimeError("db credential store unavailable")

    def store(self, key, value):
        raise RuntimeError("db credential store unavailable")


def _real_keychain_on_os_backend() -> KeychainService:
    """A REAL KeychainService pinned to the OS-keyring path.

    The two fields are set explicitly rather than trusted, so the test measures the
    same branch on a Mac (live keyring), on CI (#1382 DB store) and on a keyring-less
    box — otherwise the machine, not the code, decides which path is under test.
    """
    kc = KeychainService()
    kc._db_store = None
    kc._no_secure_store = None
    return kc


@contextlib.contextmanager
def _keyring_raising():
    """Patch the module's keyring so the underlying store genuinely fails."""

    def _boom(*args, **kwargs):
        raise RuntimeError("keyring backend exploded (real store failure)")

    fake = SimpleNamespace(get_password=_boom, set_password=_boom, get_keyring=lambda: None)
    with patch.object(ks_module, "keyring", fake):
        yield


@contextlib.contextmanager
def _keyring_returning(value):
    def _get(service, key):
        return value

    fake = SimpleNamespace(
        get_password=_get, set_password=lambda *a: None, get_keyring=lambda: None
    )
    with patch.object(ks_module, "keyring", fake):
        yield


# ---------------------------------------------------------------------------
# Seam 1 — the real keychain, really failing. THE red-first pin.
# ---------------------------------------------------------------------------


class TestRealKeychainFailureDoesNotWidenConsent:
    @pytest.mark.smoke
    def test_real_keyring_failure_refuses_instead_of_returning_all_configured(self):
        """THE #1816 pin, driven through the layer that broke.

        Pre-fix this returned ``['anthropic', 'openai']`` — the full configured set —
        because the credential swallow turned a store failure into an empty consent
        list. Measured 2026-09-15 with this exact setup.
        """
        kc = _real_keychain_on_os_backend()

        with _keyring_raising():
            # The primitive itself still swallows — that is #1711's contract and it is
            # correct for a credential. The consent path must not depend on it.
            assert kc.get_api_key(CONSENT_SLOT, username="user-a") is None

            with pytest.raises(ConsentUnreadableError):
                resolve_authorized_providers("user-a", ALL_CONFIGURED, kc)

    @pytest.mark.smoke
    def test_keychain_timeout_is_unreadable_not_absent_1711(self):
        """#1711's ACL hang: the store answered NOTHING. It did not say "empty"."""
        kc = _real_keychain_on_os_backend()
        ks_module._keychain_hung = True  # the post-hang short-circuit raises
        try:
            with pytest.raises(KeychainTimeoutError):
                kc._keyring_call("get_password", lambda *a: None, "s", "k")
            assert kc.read_secret(CONSENT_SLOT).store_failed
            with pytest.raises(ConsentUnreadableError):
                resolve_authorized_providers("user-a", ALL_CONFIGURED, kc)
        finally:
            ks_module._reset_keychain_hang_for_tests()

    def test_db_credential_store_failure_is_also_unreadable_1382(self):
        """The hosted path (#1382) has its own store, and it fails its own way."""
        kc = _real_keychain_on_os_backend()
        kc._db_store = _ExplodingStore()

        assert kc.get_api_key(CONSENT_SLOT) is None  # primitive contract unchanged
        with pytest.raises(ConsentUnreadableError):
            resolve_authorized_providers("user-a", ALL_CONFIGURED, kc)

    def test_per_user_slot_failure_does_not_fall_through_to_the_global_list(self):
        """The fall-through is only ever licensed by a VERIFIED absence.

        If a failed per-user read fell through to the server/global list, the same
        absence-means-permission mistake would just move one slot down — and the global
        list is typically the permissive one.
        """
        kc = _real_keychain_on_os_backend()
        calls = []

        def _get(service, key):
            calls.append(key)
            if key.startswith("user-a_"):
                raise RuntimeError("per-user slot unreadable")
            return "anthropic,openai"  # a permissive global list sitting right there

        fake = SimpleNamespace(
            get_password=_get, set_password=lambda *a: None, get_keyring=lambda: None
        )
        with patch.object(ks_module, "keyring", fake):
            with pytest.raises(ConsentUnreadableError):
                resolve_authorized_providers("user-a", ALL_CONFIGURED, kc)

        assert len(calls) == 1, f"the global slot must not be consulted after a failure: {calls}"


class TestGenuineAbsenceStaysOpen:
    """Fail-closed on UNREADABLE must not become fail-closed on ABSENT — that would
    brick every install that never stored a consent list."""

    def test_verified_absent_consent_list_returns_all_configured(self):
        kc = _real_keychain_on_os_backend()
        with _keyring_returning(None):
            assert resolve_authorized_providers("user-a", ALL_CONFIGURED, kc) == ALL_CONFIGURED

    def test_present_list_still_filters(self):
        kc = _real_keychain_on_os_backend()
        with _keyring_returning("anthropic"):
            assert resolve_authorized_providers("user-a", ALL_CONFIGURED, kc) == ["anthropic"]

    def test_no_secure_store_is_verified_absent_not_a_failure_1382(self):
        """Deliberate call, documented on ``read_secret``: with NO store there is
        definitively no stored consent list — nothing failed to answer. Treating it as a
        failure would fail closed on every keyring-less install, i.e. brick the instance,
        which is the outcome F1's own note said the closed state must avoid."""
        kc = _real_keychain_on_os_backend()
        kc._no_secure_store = "no secure credential store (#1382)"

        assert kc.read_secret(CONSENT_SLOT).provenance is SecretProvenance.VERIFIED_ABSENT
        assert resolve_authorized_providers("user-a", ALL_CONFIGURED, kc) == ALL_CONFIGURED


class TestSecretReadProvenance:
    """The tri-state itself — the cure for the honest-empty collapse."""

    def test_present(self):
        kc = _real_keychain_on_os_backend()
        with _keyring_returning("anthropic"):
            read = kc.read_secret(CONSENT_SLOT)
        assert read.provenance is SecretProvenance.PRESENT
        assert read.is_present and read.value == "anthropic"
        assert not read.store_failed

    def test_verified_absent(self):
        kc = _real_keychain_on_os_backend()
        with _keyring_returning(None):
            read = kc.read_secret(CONSENT_SLOT)
        assert read.is_verified_absent
        assert read.value is None and not read.store_failed

    def test_store_failed_carries_the_reason(self):
        kc = _real_keychain_on_os_backend()
        with _keyring_raising():
            read = kc.read_secret(CONSENT_SLOT)
        assert read.store_failed
        assert "exploded" in (read.error or "")

    def test_the_three_states_are_distinguishable(self):
        """The whole point: pre-fix all three were the same falsy value."""
        kc = _real_keychain_on_os_backend()
        with _keyring_returning("anthropic"):
            present = kc.read_secret(CONSENT_SLOT)
        with _keyring_returning(None):
            absent = kc.read_secret(CONSENT_SLOT)
        with _keyring_raising():
            failed = kc.read_secret(CONSENT_SLOT)

        assert len({present.provenance, absent.provenance, failed.provenance}) == 3
        # ...whereas the primitive still collapses two of them, correctly:
        with _keyring_returning(None):
            assert kc.get_api_key(CONSENT_SLOT) is None
        with _keyring_raising():
            assert kc.get_api_key(CONSENT_SLOT) is None


class TestTheCredentialPrimitiveIsUntouched:
    """Arch's ruling 1, pinned: the fix belongs at the CONSENT reader, never at the
    credential primitive. ``get_api_key`` returning ``None`` on failure is CORRECT for a
    credential (#1711) — absent and unreadable both mean *try the next source*. Changing
    it to fix a consent bug would break a sound contract to patch its caller, and every
    other credential reader would inherit the blast radius.
    """

    def test_get_api_key_still_returns_none_on_store_failure(self):
        kc = _real_keychain_on_os_backend()
        with _keyring_raising():
            assert kc.get_api_key("anthropic") is None

    def test_get_api_key_still_returns_none_on_timeout_1711(self):
        kc = _real_keychain_on_os_backend()
        ks_module._keychain_hung = True
        try:
            assert kc.get_api_key("anthropic") is None
        finally:
            ks_module._reset_keychain_hang_for_tests()

    def test_get_api_key_never_raises_for_a_credential(self):
        kc = _real_keychain_on_os_backend()
        kc._db_store = _ExplodingStore()
        assert kc.get_api_key("anthropic") is None


# ---------------------------------------------------------------------------
# Seam 2 — the config service propagates rather than substituting
# ---------------------------------------------------------------------------


class TestConfigServicePropagatesTheRefusal:
    def test_get_configured_providers_propagates(self):
        from services.config.llm_config_service import LLMConfigService

        cfg = LLMConfigService()
        cfg._keychain_service = _real_keychain_on_os_backend()
        with patch.object(LLMConfigService, "get_api_key", return_value="sk-test"):
            with _keyring_raising():
                with pytest.raises(ConsentUnreadableError):
                    cfg.get_configured_providers("user-a")

    def test_get_available_providers_propagates(self):
        from services.config.llm_config_service import LLMConfigService

        cfg = LLMConfigService()
        cfg._keychain_service = _real_keychain_on_os_backend()
        with patch.object(LLMConfigService, "get_api_key", return_value="sk-test"):
            with _keyring_raising():
                with pytest.raises(ConsentUnreadableError):
                    cfg.get_available_providers("user-a")


# ---------------------------------------------------------------------------
# Seam 3 — closed means CLOSED, not reassigned to the operator's key
# ---------------------------------------------------------------------------


class _RefusingConfigService:
    def get_default_provider(self, user_id=None):
        raise ConsentUnreadableError("consent read failed")

    def get_configured_providers(self, user_id=None):
        raise ConsentUnreadableError("consent read failed")


def _client_with_operator_clients(config_service):
    from services.llm.clients import LLMClient

    client = LLMClient.__new__(LLMClient)  # skip __init__ (builds real SDKs)
    client._config_service = config_service
    client._output_filter = None
    # The operator's OWN long-lived clients, sitting right there and initialized.
    client.anthropic_client = SimpleNamespace(name="THE-OPERATORS-OWN-ANTHROPIC-CLIENT")
    client.openai_client = SimpleNamespace(name="THE-OPERATORS-OWN-OPENAI-CLIENT")
    client.gemini_client = None
    return client


@pytest.mark.smoke
def test_consent_refusal_is_not_served_from_the_operators_own_client_1815_gap2():
    """#1815 Gap 2, red-first.

    Pre-fix, ``_complete_raw``'s blanket ``except (ValueError, Exception)`` swallowed the
    consent-read failure and selected ``primary_provider`` from *whichever client is
    initialized* — the server's own. Measured 2026-09-15: the turn was served, by the
    operator's Anthropic client, after the consent read had failed. That is fail-closed
    quietly reassigned to a key PM has abolished (#1812).
    """
    client = _client_with_operator_clients(_RefusingConfigService())
    attempted = []

    async def _fake_call(provider, *a, **k):
        attempted.append(provider.value)
        return "served"

    with patch.object(type(client), "_call_provider", new=AsyncMock(side_effect=_fake_call)):
        with pytest.raises(ConsentUnreadableError):
            asyncio.run(client._complete_raw("conversation", "hi", user_id="user-a"))

    assert attempted == [], f"a refused turn called a provider anyway: {attempted}"


def test_consent_unreadable_is_a_member_of_the_1807_refusal_family():
    assert issubclass(ConsentUnreadableError, LLMKeyRequiredError)


# ---------------------------------------------------------------------------
# Seam 4 — the honest error reaches the user, with its OWN copy
# ---------------------------------------------------------------------------


class TestTheUserVisibleRefusal:
    def test_floor_classifies_the_refusal_by_type(self):
        assert _classify_llm_error(ConsentUnreadableError("boom")) == "consent_unreadable"

    def test_the_copy_is_not_any_of_its_three_siblings(self):
        """CXO, 2026-09-15: one error class does not imply one string. Three states now
        share this family and two of them would be lied to by the same sentence — the
        keyless copy would tell a consent-read-failure user to add a key they already
        have (the #1108 'recommends a known-failing action' shape)."""
        assert FLOOR_FALLBACK_CONSENT_UNREADABLE not in (
            FLOOR_FALLBACK_NO_PROVIDER,
            FLOOR_FALLBACK_AUTH,
            FLOOR_FALLBACK_TRANSIENT,
        )

    def test_the_copy_reports_a_failed_read_and_does_not_blame_the_user(self):
        """The three properties CXO made load-bearing, asserted rather than assumed."""
        copy = FLOOR_FALLBACK_CONSENT_UNREADABLE.lower()
        assert "couldn't read" in copy  # a FAILED READ, not an absence
        assert "ours to fix, not yours" in copy  # whose fault it is
        assert "try again" in copy  # admissible HERE, uniquely in this family
        # and the thing it must never say — they may already HAVE a key:
        assert "settings" not in copy
        assert "add your" not in copy


@pytest.mark.asyncio
async def test_intent_service_does_not_wrap_the_refusal_into_a_processing_error():
    """A refusal is a correct ANSWER, not a processing failure. Wrapping it in
    ``IntentProcessingError`` erases the type the route branches on, and the user gets
    the generic "service unavailable, try again" degradation — wrong blame."""
    from services.intent.intent_service import IntentService

    dummy_self = SimpleNamespace(logger=SimpleNamespace(info=lambda *a, **k: None))

    with patch(
        "services.intent_service.collaboration_gate.detect_mode_declaration",
        side_effect=ConsentUnreadableError("consent read failed"),
    ):
        with pytest.raises(ConsentUnreadableError):
            await IntentService._process_intent_internal(
                dummy_self, message="hi", session_id="default_session", user_id="user-a"
            )


def _intent_result(message: str = "ok") -> SimpleNamespace:
    return SimpleNamespace(
        message=message,
        intent_data={},
        workflow_id=None,
        requires_clarification=False,
        clarification_type=None,
        suggestions=[],
        preferences={},
        error=None,
        error_type=None,
        async_work_started=False,
    )


class _RefusingIntentService:
    """Stands where IntentService stands and raises what a consent-read failure raises
    once it has travelled up through the config service and the LLM client."""

    async def process_intent(self, **kwargs):
        raise ConsentUnreadableError("consent read failed")


@pytest.mark.smoke
def test_route_serves_the_honest_refusal_not_a_generic_degradation():
    """The user-visible end of the chain, through the REAL /api/v1/intent route."""
    app = FastAPI()
    app.include_router(intent_router)
    jwt_service = JWTService(secret_key=SECRET)
    app.state.jwt_service = jwt_service
    app.state.intent_service = _RefusingIntentService()
    client = TestClient(app, raise_server_exceptions=False)

    user_id = uuid.uuid4()
    token = jwt_service.generate_access_token(
        user_id=user_id, user_email=f"{user_id}@example.com", scopes=["user"]
    )

    with patch(
        "services.security.user_api_key_service.UserAPIKeyService.retrieve_user_key",
        AsyncMock(return_value="sk-ant-the-users-own-key"),
    ):
        response = client.post(
            "/api/v1/intent",
            json={"message": "What can you do?", "session_id": "default_session"},
            headers={"Authorization": f"Bearer {token}"},
        )

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["message"] == FLOOR_FALLBACK_CONSENT_UNREADABLE
    assert body["error_type"] == "consent_unreadable"
    # NOT the generic degradation, and NOT the keyless copy:
    assert body["message"] != FLOOR_FALLBACK_NO_PROVIDER
    assert "service unavailable" not in body["message"].lower()
