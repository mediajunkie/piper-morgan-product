"""#1823 branch one — ONE stored key of ANY spendable provider passes the LLM gate.

PPM RULED (2026-09-19, final): gate on any spendable provider; branch two (task-type
copy) out of scope — `resolve_model` is provider-agnostic by construction. Arch's
frame: the gate checked one provider while the spend was already multi-provider
(#1819) — the binding outgrew the thing the gate checks. The seam-era caveat is
dissolved (#1812 steps 5–6), so the gate is exactly the resolver + the Slack arm
(#1822's shape, now shared).

Before this fix: an OpenAI-only user was refused at /intent with add-your-Anthropic-key
copy, for a turn their own key could serve. CXO: the policy is OWNERSHIP, not a vendor —
the refusal copy is provider-neutral now, matching FLOOR_FALLBACK_NO_PROVIDER's
convention (the product stops answering "what key do I need?" two different ways).

LAYER (m-43): resolver unit tests + the real /api/v1/intent route through a real ASGI
client with a real JWT and a PROVIDER-AWARE stored-key world (the #1822 test double —
`_stored_key`'s single-value mock can't distinguish rows and would mask exactly this
fix). DENOMINATOR: openai-only, anthropic-only, both, neither, anonymous; /intent and
the /documents analyze representative.
"""

import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from services.llm.request_key import (
    AnonymousLLMKeyRequiredError,
    UserLLMKeyRequiredError,
    get_request_api_key,
)
from web.api.routes.intent import router as intent_router
from web.utils.llm_key import resolve_user_llm_binding

SECRET = "test-secret-1823-not-a-real-key"

OPENAI_KEY = "sk-oai-the-users-own-1823"
ANTHROPIC_KEY = "sk-ant-the-users-own-1823"


@contextlib.asynccontextmanager
async def _fake_session():
    yield object()


@contextlib.contextmanager
def _stored_keys(anthropic=None, openai=None):
    """A PROVIDER-AWARE stored-key world (the #1822 double): the anthropic and
    openai rows are distinct, the way a one-key user actually looks."""
    rows = {"anthropic": anthropic, "openai": openai}

    async def _retrieve(session, user_id, provider):
        return rows.get(provider)

    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            lambda *a, **k: _fake_session(),
        ),
        patch(
            "services.security.user_api_key_service.UserAPIKeyService.retrieve_user_key",
            AsyncMock(side_effect=_retrieve),
        ),
    ):
        yield


# ---------------------------------------------------------------------------
# Resolver unit layer
# ---------------------------------------------------------------------------


class TestResolveUserLlmBinding:
    @pytest.mark.asyncio
    async def test_openai_only_user_gets_an_openai_binding(self):
        """THE #1823 pin: the user the old gate refused."""
        with _stored_keys(anthropic=None, openai=OPENAI_KEY):
            binding = await resolve_user_llm_binding(None, "u-openai-only")
        assert binding == {"openai": OPENAI_KEY}

    @pytest.mark.asyncio
    async def test_anthropic_only_user_unchanged(self):
        with _stored_keys(anthropic=ANTHROPIC_KEY, openai=None):
            binding = await resolve_user_llm_binding(None, "u-ant-only")
        assert binding == {"anthropic": ANTHROPIC_KEY}

    @pytest.mark.asyncio
    async def test_both_keys_bind_both_providers(self):
        """#1819's widening survives: selection can route either leg, each on
        the user's own key."""
        with _stored_keys(anthropic=ANTHROPIC_KEY, openai=OPENAI_KEY):
            binding = await resolve_user_llm_binding(None, "u-both")
        assert binding == {"anthropic": ANTHROPIC_KEY, "openai": OPENAI_KEY}

    @pytest.mark.asyncio
    async def test_no_keys_still_refuses(self):
        """Widening the gate never widens a refusal into a grant."""
        with _stored_keys():
            with pytest.raises(UserLLMKeyRequiredError):
                await resolve_user_llm_binding(None, "u-keyless")

    @pytest.mark.asyncio
    async def test_anonymous_refusal_propagates_untouched(self):
        """#1320 no-regress: the OpenAI arm runs only for AUTHENTICATED callers."""
        with _stored_keys(openai=OPENAI_KEY):
            with pytest.raises(AnonymousLLMKeyRequiredError):
                await resolve_user_llm_binding(None, None)

    @pytest.mark.asyncio
    async def test_header_key_still_wins_no_db(self):
        """#1162 no-regress: BYOC header short-circuits; the openai row still
        rides along per #1819's expansion."""
        with _stored_keys(openai=OPENAI_KEY):
            binding = await resolve_user_llm_binding("sk-byoc-hdr", "u1")
        assert binding["anthropic"] == "sk-byoc-hdr"
        assert binding["openai"] == OPENAI_KEY


# ---------------------------------------------------------------------------
# Route layer — the real /api/v1/intent gate
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


class _BindingObserver:
    """Captures what the request could actually spend, per provider."""

    def __init__(self) -> None:
        self.calls = 0
        self.anthropic_key = None
        self.openai_key = None

    async def process_intent(self, **kwargs):
        self.calls += 1
        self.anthropic_key = get_request_api_key("anthropic")
        self.openai_key = get_request_api_key("openai")
        return _intent_result()


def _client():
    app = FastAPI()
    app.include_router(intent_router)
    jwt_service = JWTService(secret_key=SECRET)
    observer = _BindingObserver()
    app.state.jwt_service = jwt_service
    app.state.intent_service = observer
    return TestClient(app, raise_server_exceptions=False), jwt_service, observer


def _token(jwt_service: JWTService) -> str:
    user_id = uuid.uuid4()
    return jwt_service.generate_access_token(
        user_id=user_id,
        user_email=f"{user_id}@example.com",
        scopes=["user"],
    )


def _post(client, headers, message="create an issue for the login bug", session_id=None):
    response = client.post(
        "/api/v1/intent",
        json={"message": message, "session_id": session_id or f"s-{uuid.uuid4().hex[:8]}"},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response.json()


class TestIntentGateAnyProvider:
    @pytest.mark.smoke
    def test_openai_only_user_is_served_on_their_own_key(self):
        """THE route pin: the exact user #1823 was filed about — one stored
        OpenAI key, no Anthropic — now passes the gate and their turn can only
        spend THEIR key on THEIR provider."""
        client, jwt_service, observer = _client()
        token = _token(jwt_service)

        with _stored_keys(anthropic=None, openai=OPENAI_KEY):
            body = _post(client, {"Authorization": f"Bearer {token}"})

        assert body["message"] == "ok"
        assert observer.calls == 1
        assert observer.openai_key == OPENAI_KEY
        assert observer.anthropic_key is None  # nothing invented for the other leg

    def test_anthropic_only_user_unchanged_control(self):
        client, jwt_service, observer = _client()
        token = _token(jwt_service)

        with _stored_keys(anthropic=ANTHROPIC_KEY, openai=None):
            body = _post(client, {"Authorization": f"Bearer {token}"})

        assert body["message"] == "ok"
        assert observer.anthropic_key == ANTHROPIC_KEY

    def test_keyless_user_still_refused_with_provider_neutral_copy(self):
        """The refusal survives, and its copy names the POLICY (ownership) with
        both providers — never 'add your Anthropic key' to someone whose OpenAI
        key would have served (CXO's fourth-time-bitten copy defect)."""
        client, jwt_service, observer = _client()
        token = _token(jwt_service)
        sid = "s-keyless-1823"

        with _stored_keys():
            # First contact gets the #1818(b) kind copy; the SECOND substantive
            # turn is the gate's own string — assert on that one.
            _post(client, {"Authorization": f"Bearer {token}"}, session_id=sid)
            body = _post(client, {"Authorization": f"Bearer {token}"}, session_id=sid)

        assert body["error_type"] == "user_key_required"
        assert observer.calls == 0
        msg = body["message"]
        assert "OpenAI or Anthropic" in msg
        assert "Anthropic API key" not in msg  # the vendor-specific form is retired
        assert "doesn't bill anyone else's account" in msg

    def test_anonymous_caller_unchanged_no_regress_1320(self):
        client, _, observer = _client()

        with _stored_keys(openai=OPENAI_KEY):
            body = _post(client, {})

        assert body["error_type"] == "anonymous_key_required"
        assert observer.calls == 0


class TestDocumentsGateAnyProvider:
    @pytest.mark.asyncio
    async def test_analyze_serves_an_openai_only_user(self):
        """The /documents family shares the widened gate (Arch's corrected
        census: 2 of 3 call sites were affected; this is the representative)."""
        from web.api.routes import documents

        seen = {}

        async def _spy(**kwargs):
            seen["openai"] = get_request_api_key("openai")
            seen["anthropic"] = get_request_api_key("anthropic")
            return {"summary": "s", "key_findings": []}

        user = SimpleNamespace(sub="u-oai", user_id="uuid-oai")
        with _stored_keys(anthropic=None, openai=OPENAI_KEY):
            with patch.object(documents, "handle_analyze_document", _spy):
                result = await documents.analyze_document(file_id="f", current_user=user)

        assert result["summary"] == "s"
        assert seen["openai"] == OPENAI_KEY
        assert seen["anthropic"] is None
