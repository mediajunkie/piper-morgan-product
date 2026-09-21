"""#1824 — the "auth" bucket splits into four; the honest sentence differs per cause.

Arch's finding: `_classify_llm_error` returned "auth" for FIVE distinct causes — two
of its own branches said "config issue" in a comment while returning "auth". The user-
facing copy could not be honest because the distinction was destroyed before the
sentence was written (CXO: a claim's honesty is a property of the layer that utters
it). Ruled split criterion: **a bucket earns its own name when the honest user-facing
sentence differs.** Copy is CXO's four-bucket draft (2026-09-15), verbatim.

Live justification (alpha v0.8.12.0, 2026-09-20): a stored-but-INVALID key produced a
real provider 401 and the user saw the generic "Something unexpected happened" — the
cause was destroyed a second time by the DOUBLE WRAP (`IntentClassificationFailedError`
→ `IntentProcessingError`) which dropped `details["original_error"]` so the route's
#1414 unwrap found nothing. That propagation fix is pinned here too.

LAYER (m-43): pure-unit on the classifier + the floor's dispatch dict + the route's
degradation extractor. DENOMINATOR: all five old "auth" causes, the three neighbors
(no_provider / consent / transient), and the live double-wrap chain shape.
"""

import pytest

from services.intent_service.conversational_floor import (
    FLOOR_FALLBACK_CONFIG_ENDPOINT,
    FLOOR_FALLBACK_INSUFFICIENT_PERMISSION,
    FLOOR_FALLBACK_NOT_CONFIGURED,
    FLOOR_FALLBACK_REJECTED_CREDENTIAL,
    _classify_llm_error,
)


class TestClassifierSplit:
    """One label per honest sentence — the five old 'auth' causes, discriminated."""

    @pytest.mark.parametrize(
        "message",
        [
            "Error code: 401 - authentication_error: API key is invalid",
            "Unauthorized",
            "invalid_api_key",
            "Invalid API key provided",
        ],
    )
    def test_rejected_credential(self, message):
        assert _classify_llm_error(Exception(message)) == "rejected_credential"

    @pytest.mark.parametrize(
        "message",
        ["Error code: 403", "Forbidden: your account does not allow this model"],
    )
    def test_insufficient_permission(self, message):
        assert _classify_llm_error(Exception(message)) == "insufficient_permission"

    def test_not_configured_is_its_own_bucket_not_auth(self):
        """A client never constructed — no credential was rejected at all.
        Latent (never observed firing); NOT the #1814 wall per the issue's own
        refutation."""
        assert _classify_llm_error(Exception("Anthropic client not initialized")) == (
            "not_configured"
        )

    @pytest.mark.parametrize(
        "message",
        [
            "The model claude-old-1 was not found",
            "model gpt-x does not exist",
            "Error code: 404 - not_found_error",
        ],
    )
    def test_config_endpoint(self, message):
        """The branches whose own comments said 'config issue' while returning
        'auth' — the classifier documented its own defect (CXO)."""
        assert _classify_llm_error(Exception(message)) == "config_endpoint"

    def test_neighbors_unchanged(self):
        from services.llm.request_key import ConsentUnreadableError

        assert _classify_llm_error(Exception("No LLM provider not configured")) == "no_provider"
        assert _classify_llm_error(ConsentUnreadableError("boom")) == "consent_unreadable"
        assert _classify_llm_error(Exception("Read timed out")) == "transient"

    def test_auth_is_no_longer_a_reachable_label(self):
        """The old label has no producing branch left — the split is total."""
        import inspect

        src = inspect.getsource(_classify_llm_error)
        assert 'return "auth"' not in src


class TestFloorDispatchServesTheHonestCopy:
    """Each bucket's copy is CXO's, and the dict actually carries all four."""

    def test_dispatch_covers_the_four_buckets(self):
        from services.intent_service import conversational_floor as cf
        import inspect

        # The dispatch dict is built inline in respond(); assert its members by
        # the constants' presence in source next to their labels.
        src = inspect.getsource(cf.ConversationalFloor.respond)
        for label, const in [
            ("rejected_credential", "FLOOR_FALLBACK_REJECTED_CREDENTIAL"),
            ("insufficient_permission", "FLOOR_FALLBACK_INSUFFICIENT_PERMISSION"),
            ("not_configured", "FLOOR_FALLBACK_NOT_CONFIGURED"),
            ("config_endpoint", "FLOOR_FALLBACK_CONFIG_ENDPOINT"),
        ]:
            assert label in src and const in src

    def test_insufficient_permission_never_points_at_our_settings(self):
        """CXO's deliberate omission: the fix is at the provider; sending them to
        our Settings would recommend a known-failing action (#1108)."""
        assert "Settings" not in FLOOR_FALLBACK_INSUFFICIENT_PERMISSION

    def test_config_endpoint_offers_no_recovery_action(self):
        """The first member of the family with NO recovery, correctly — the user
        can do nothing, and the slot's existence is not a reason to invent an
        affordance that can't be taken (CXO)."""
        for phrase in ("try again", "Settings", "check"):
            assert phrase.lower() not in FLOOR_FALLBACK_CONFIG_ENDPOINT.lower()

    def test_not_configured_asserts_nothing_about_their_key(self):
        """The label doesn't say whether they have a key, so the copy mustn't."""
        assert "key" not in FLOOR_FALLBACK_NOT_CONFIGURED.lower()
        assert "our side" in FLOOR_FALLBACK_NOT_CONFIGURED

    def test_rejected_credential_names_the_rejection_and_the_fix(self):
        assert "rejected" in FLOOR_FALLBACK_REJECTED_CREDENTIAL
        assert "Settings" in FLOOR_FALLBACK_REJECTED_CREDENTIAL


class TestDoubleWrapPropagation:
    """The live alpha chain: provider 401 → IntentClassificationFailedError →
    IntentProcessingError → route. The middle wrap now carries original_error, so
    the route's #1414 unwrap reaches the humanizer's honest invalid-key copy
    instead of 'Something unexpected happened'."""

    PROVIDER_401 = (
        "All configured LLM providers failed. Details: anthropic: Error code: 401 - "
        "authentication_error: API key is invalid"
    )

    def test_route_extractor_surfaces_the_honest_key_copy(self):
        from services.intent.intent_service import IntentProcessingError
        from web.api.routes.intent import _extract_degradation_message

        # The wrap as production now builds it: outer stringifies uselessly,
        # details carries the truth.
        err = IntentProcessingError("Intent processing failed: API Error [500]")
        err.details = {"original_error": self.PROVIDER_401}

        msg = _extract_degradation_message(err)

        assert "isn't valid" in msg
        assert "Settings" in msg
        assert "unexpected" not in msg.lower()

    def test_bare_double_wrap_would_have_fallen_to_generic(self):
        """The pre-fix shape, pinned so the defect stays understood: without
        details, the wrapped string matches nothing key-shaped."""
        from services.intent.intent_service import IntentProcessingError
        from web.api.routes.intent import _extract_degradation_message

        err = IntentProcessingError("Intent processing failed: API Error [500]")

        msg = _extract_degradation_message(err)
        assert "isn't valid" not in msg

    def test_the_wrap_function_itself_carries_the_cause(self):
        """The REAL wrap (extracted as _wrap_processing_error so it is
        unit-testable): an inner APIError with details.original_error comes out
        still carrying it; a plain exception carries its own string."""
        from services.api.errors import IntentClassificationFailedError
        from services.intent.intent_service import _wrap_processing_error

        inner = IntentClassificationFailedError(details={"original_error": self.PROVIDER_401})
        err = _wrap_processing_error(inner)
        assert err.details["original_error"] == self.PROVIDER_401

        plain = _wrap_processing_error(ValueError("chroma exploded"))
        assert plain.details["original_error"] == "chroma exploded"
