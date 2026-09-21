"""#1818(b) — the keyless gate acknowledges the person before naming the policy.

PM RULED (b), 2026-09-20 (decisions.log 13:3x): a keyless user's first message —
the first thing a new alpha tester types is usually "hi" — gets a KIND-MATCHED
acknowledgment plus the key requirement. No exemption machinery: the greeting
does not pass the gate; the gate answers it like a person would (zero LLM, zero
spend — the spend-free ratchet is this lane's canary and its membership must not
change).

Copy is CXO's, verbatim (issue comment 5752301343). Seam split is Arch's
(2026-09-20, CXO-confirmed): repeated bare pleasantry → the short form; repeated
SUBSTANTIVE request → the gate's own refusal string, unchanged (#1823's when it
lands). One policy, one string per layer.

LAYER (m-43): the module tests are pure-unit (deterministic classifier + copy
composition); the route tests drive the REAL `/api/v1/intent` route through a
real ASGI TestClient with a real JWT, so the copy observed is what an alpha
tester's browser receives. DENOMINATOR: all four kinds, first + repeat turns,
keyless + keyed control; the anonymous (#1320) path is deliberately unchanged
and pinned so.
"""

import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from services.ui_messages.keyless_pleasantry import (
    KEYLESS_KIND_PREFIXES,
    KEYLESS_REPEAT_SHORT_FORM,
    KEYLESS_SHARED_KEY_SENTENCE,
    _reset_served_sessions_for_tests,
    classify_pleasantry_kind,
    keyless_first_contact_message,
    keyless_gate_message,
)
from web.api.routes.intent import router as intent_router

SECRET = "test-secret-1818-not-a-real-key"


@pytest.fixture(autouse=True)
def _fresh_session_memory():
    _reset_served_sessions_for_tests()
    yield
    _reset_served_sessions_for_tests()


class TestKindClassification:
    """Deterministic, zero-LLM — reuses the pre-classifier's own patterns."""

    @pytest.mark.parametrize(
        "message,kind",
        [
            ("hi", "greeting"),
            ("Hello!", "greeting"),
            ("good morning", "greeting"),
            ("bye", "farewell"),
            ("goodbye!", "farewell"),
            ("thanks", "thanks"),
            ("thank you so much", "thanks"),
            ("thanks, bye!", "farewell"),  # mixed resolves farewell-first
        ],
    )
    def test_pure_pleasantries_classify(self, message, kind):
        assert classify_pleasantry_kind(message) == kind

    @pytest.mark.parametrize(
        "message",
        [
            "create an issue",
            "hi, can you create an issue for me?",  # substantive residue (#1416)
            "what can you do",
            "",
        ],
    )
    def test_substantive_or_empty_is_not_a_pleasantry(self, message):
        assert classify_pleasantry_kind(message) is None


class TestCopyComposition:
    def test_every_kind_composes_prefix_plus_the_one_shared_sentence(self):
        """🔴 CXO's structural requirement: the shared half is ONE constant —
        every rendered form must contain the identical sentence, so a future
        edit lands everywhere at once instead of drifting four ways."""
        for kind, prefix in KEYLESS_KIND_PREFIXES.items():
            rendered = keyless_first_contact_message(kind)
            assert rendered == f"{prefix} {KEYLESS_SHARED_KEY_SENTENCE}"

    def test_unknown_kind_falls_back_to_neutral(self):
        assert keyless_first_contact_message(None).startswith(KEYLESS_KIND_PREFIXES["neutral"])

    def test_thanks_never_claims_you_are_welcome(self):
        """CXO: nothing has been done, so 'you're welcome' would claim a service
        never rendered — the honest-empty family inside a pleasantry."""
        assert "welcome" not in keyless_first_contact_message("thanks").lower()

    def test_shared_sentence_is_one_constant_in_source(self):
        src = open("services/ui_messages/keyless_pleasantry.py").read()
        assert src.count("Piper runs on an LLM key of your own") == 1, (
            "the shared sentence was pasted more than once — CXO's drift defect, "
            "self-inflicted (four near-identical sentences drift)"
        )


class TestSessionSeam:
    """First turn full copy; repeat pleasantry short form; repeat substantive
    falls through to the gate's own string (returns None)."""

    def test_first_turn_any_kind_gets_full_copy(self):
        msg = keyless_gate_message("sess-1", "hi")
        assert msg == keyless_first_contact_message("greeting")

    def test_first_substantive_turn_gets_neutral_full_copy(self):
        msg = keyless_gate_message("sess-2", "create an issue for the login bug")
        assert msg == keyless_first_contact_message("neutral")

    def test_repeat_pleasantry_gets_the_short_form(self):
        keyless_gate_message("sess-3", "hi")
        assert keyless_gate_message("sess-3", "hello again") == KEYLESS_REPEAT_SHORT_FORM

    def test_repeat_substantive_falls_through_to_the_gate_string(self):
        """Arch's split, CXO-confirmed: a real request hitting the gate on turn
        2+ is the gate's refusal (#1823's string when it lands) — never the
        courtesy short form. One policy, one string per layer."""
        keyless_gate_message("sess-4", "hi")
        assert keyless_gate_message("sess-4", "create an issue") is None

    def test_sessions_do_not_share_memory(self):
        keyless_gate_message("sess-5", "hi")
        assert keyless_gate_message("sess-6", "hi") == keyless_first_contact_message("greeting")


# ---------------------------------------------------------------------------
# Route layer — the real /api/v1/intent gate serves the copy
# ---------------------------------------------------------------------------


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


class _CountingIntentService:
    def __init__(self) -> None:
        self.calls = 0

    async def process_intent(self, **kwargs):
        self.calls += 1
        return _intent_result()


@contextlib.asynccontextmanager
async def _fake_session_scope():
    yield object()


@contextlib.contextmanager
def _stored_key(value):
    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            lambda *a, **k: _fake_session_scope(),
        ),
        patch(
            "services.security.user_api_key_service.UserAPIKeyService.retrieve_user_key",
            AsyncMock(return_value=value),
        ),
    ):
        yield


def _client():
    app = FastAPI()
    app.include_router(intent_router)
    jwt_service = JWTService(secret_key=SECRET)
    service = _CountingIntentService()
    app.state.jwt_service = jwt_service
    app.state.intent_service = service
    return TestClient(app, raise_server_exceptions=False), jwt_service, service


def _token(jwt_service: JWTService) -> str:
    user_id = uuid.uuid4()
    return jwt_service.generate_access_token(
        user_id=user_id,
        user_email=f"{user_id}@example.com",
        scopes=["user"],
    )


def _post(client, headers, message, session_id="default_session"):
    response = client.post(
        "/api/v1/intent",
        json={"message": message, "session_id": session_id},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response.json()


class TestRouteServesTheRuledCopy:
    @pytest.mark.smoke
    def test_keyless_hi_gets_the_greeting_acknowledgment(self):
        """THE (b) pin: the first thing a new tester types gets acknowledged as
        a greeting AND told the policy — refused before any LLM (zero spend)."""
        client, jwt_service, service = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            body = _post(client, {"Authorization": f"Bearer {token}"}, "hi")

        assert body["message"].startswith(KEYLESS_KIND_PREFIXES["greeting"])
        assert KEYLESS_SHARED_KEY_SENTENCE in body["message"]
        assert body["error_type"] == "user_key_required"
        assert service.calls == 0, "refused before IntentService/the LLM — zero spend"

    def test_keyless_thanks_gets_the_honest_thanks_acknowledgment(self):
        client, jwt_service, _ = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            body = _post(client, {"Authorization": f"Bearer {token}"}, "thanks!")

        assert body["message"].startswith(KEYLESS_KIND_PREFIXES["thanks"])
        assert "welcome" not in body["message"].lower()

    def test_second_keyless_pleasantry_gets_the_short_form(self):
        client, jwt_service, _ = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            _post(client, {"Authorization": f"Bearer {token}"}, "hi", session_id="s-rep")
            body = _post(client, {"Authorization": f"Bearer {token}"}, "hello", session_id="s-rep")

        assert body["message"] == KEYLESS_REPEAT_SHORT_FORM

    def test_second_keyless_substantive_gets_the_gate_string(self):
        client, jwt_service, _ = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            _post(client, {"Authorization": f"Bearer {token}"}, "hi", session_id="s-sub")
            body = _post(
                client,
                {"Authorization": f"Bearer {token}"},
                "create an issue for the login bug",
                session_id="s-sub",
            )

        # The gate's own voice, not the courtesy forms (— #1823's string later).
        assert KEYLESS_SHARED_KEY_SENTENCE not in body["message"]
        assert body["message"] != KEYLESS_REPEAT_SHORT_FORM
        assert "LLM key of your own" in body["message"]

    def test_keyed_greeting_is_untouched_control(self):
        """A keyed user's 'hi' flows to the normal pipeline — this lane changes
        only the refusal's voice, never routing for entitled users."""
        client, jwt_service, service = _client()
        token = _token(jwt_service)

        with _stored_key("sk-user-own-key"):
            body = _post(client, {"Authorization": f"Bearer {token}"}, "hi")

        assert service.calls == 1
        assert body["message"] == "ok"

    def test_anonymous_path_unchanged_no_regress_1320(self):
        """The anonymous refusal keeps its own copy — (b) ruled the
        authenticated-keyless surface only."""
        client, _, service = _client()

        with _stored_key(None):
            body = _post(client, {}, "hi")

        assert body["error_type"] == "anonymous_key_required"
        assert KEYLESS_SHARED_KEY_SENTENCE not in body["message"]
        assert service.calls == 0
