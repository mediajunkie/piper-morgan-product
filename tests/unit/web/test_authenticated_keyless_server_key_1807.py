"""#1807 — an authenticated user with no key of their own must NOT spend the operator's key.

THE DEFECT. `resolve_request_api_key` resolved `header > stored > server-fallback`. The
third rung returned `None` for ANY caller with a truthy `user_id`, and `None` means "use
the server's configured client" (`services/llm/clients.py:488` →
`anthropic_client_for_request`). #1320 closed the ANONYMOUS half of the #1162 paired fix;
the authenticated-but-keyless half was left open because, at the time, the only
authenticated identity was PM. Every alpha tester who logs in and skips the key step is by
construction a known authenticated identity — and silently billed PM's balance.

Authentication is not billing authorization. Being a known identity establishes WHO you
are; it does not establish that you may spend the operator's money.

LAYER (m-43). These are not resolver unit tests. They drive the REAL `/api/v1/intent`
route through a real ASGI `TestClient`, with a real `JWTService` minting and verifying a
real HS256 token, through the real `get_current_user_optional` dependency. The observable
is the REAL `anthropic_client_for_request` — the exact function `LLMClient._anthropic_complete`
calls to choose a client — invoked from inside the stubbed IntentService, i.e. at the point
in the request where an LLM call would actually happen. `SERVER_CLIENT` appearing there IS
the server key being consumed. A resolver-only assertion would not have proven that the
route binds what the resolver returns, and the route is where #1320's sibling bug (#1520)
actually lived.

DENOMINATOR. Four callers are covered at the route: (1) authenticated + no stored key
[the defect], (2) authenticated + stored key [the control — must still work], (3) fully
anonymous [#1320 no-regress], (4) authenticated + BYOC header [#1162 no-regress]. The
designated-operator path is covered at the resolver + config layer in
`tests/unit/services/llm/test_operator_server_key_1807.py`; the `/documents` family's
refusal surface is covered in `tests/unit/web/api/routes/test_documents_keyless_refusal_1807.py`.
NOT covered here: the Slack/MCP entry points, which do not route through `/intent`.
"""

import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.jwt_service import JWTService
from services.llm.request_key import anthropic_client_for_request
from web.api.routes.intent import router as intent_router

SECRET = "test-secret-1807-not-a-real-key"

# The sentinel that stands in for the operator's own configured Anthropic client. If a
# test ever observes this object bound to a request, that request consumed PM's key.
SERVER_CLIENT = SimpleNamespace(name="THE-SERVERS-OWN-ANTHROPIC-CLIENT")


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


class _ObservingIntentService:
    """Stands where IntentService stands, and does the one thing that matters: asks
    `anthropic_client_for_request` which client this request would use. That is the
    real production selector, not a re-implementation of it."""

    def __init__(self) -> None:
        self.calls = 0
        self.client_for_request = None

    async def process_intent(self, **kwargs):
        self.calls += 1
        self.client_for_request = anthropic_client_for_request(SERVER_CLIENT)
        return _intent_result()


@contextlib.asynccontextmanager
async def _fake_session_scope():
    yield object()


@contextlib.contextmanager
def _stored_key(value):
    """Point the route's DB-backed stored-key fetcher at `value` without a database.

    Patches the two names the route's inline `_fetch_stored_anthropic_key` imports at
    call time; everything else on the path (resolution, binding, refusal) runs for real.
    """
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


def _client() -> tuple[TestClient, JWTService, _ObservingIntentService]:
    app = FastAPI()
    app.include_router(intent_router)
    jwt_service = JWTService(secret_key=SECRET)
    observer = _ObservingIntentService()
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


def _post(client: TestClient, headers: dict) -> dict:
    # session_id "default_session" deliberately skips the conversation auto-create
    # block, which is unrelated to key resolution and would need a real database.
    response = client.post(
        "/api/v1/intent",
        json={"message": "what did I ship this week?", "session_id": "default_session"},
        headers=headers,
    )
    assert response.status_code == 200, response.text
    return response.json()


class TestAuthenticatedKeylessCallerCannotSpendTheOperatorsKey:
    """The #1807 property: a login is not a licence to spend someone else's money."""

    @pytest.mark.smoke
    def test_authenticated_user_with_no_key_does_not_consume_the_server_key(self):
        """THE red-first pin. Pre-fix, `client_for_request is SERVER_CLIENT` — the
        request reached the LLM selector and got PM's own client. Post-fix the request
        is refused before IntentService is touched at all."""
        client, jwt_service, observer = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            body = _post(client, {"Authorization": f"Bearer {token}"})

        assert observer.client_for_request is not SERVER_CLIENT, (
            "an authenticated user with no key of their own consumed the SERVER's "
            "Anthropic client — this is the #1807 billing exposure"
        )
        assert observer.calls == 0, "refusal must happen before IntentService/the LLM"
        assert body["error_type"] == "user_key_required"

    @pytest.mark.smoke
    def test_refusal_is_honest_and_actionable_not_a_crash_or_a_silent_no_op(self):
        """#1425/#1792 family: name the real remediation. Not "service unavailable"
        (retrying changes nothing), not "sign in" (they already are), not a 500."""
        client, jwt_service, _ = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            body = _post(client, {"Authorization": f"Bearer {token}"})

        msg = body["message"].lower()
        assert "llm key" in msg or "api key" in msg, body["message"]
        assert "add" in msg or "connect" in msg, "must say what to do, not merely fail"
        # Wrong-blame copy from the two sibling refusals must not leak onto this path.
        assert "sign in" not in msg, "they ARE signed in — that is the whole point"
        assert "expired" not in msg
        assert "try again" not in msg, "retrying without a key changes nothing"
        assert body["requires_clarification"] is True
        assert body["clarification_type"] == "user_key_required"
        assert body["suggestions"], "an actionable refusal carries a next step"

    @pytest.mark.smoke
    def test_control_authenticated_user_with_a_stored_key_still_works(self):
        """The fix must not break the paying user. Their stored key is bound, and the
        client chosen is keyed to it — not the server's."""
        client, jwt_service, observer = _client()
        token = _token(jwt_service)

        with _stored_key("sk-user-b-stored-key"):
            body = _post(client, {"Authorization": f"Bearer {token}"})

        assert observer.calls == 1
        assert observer.client_for_request is not SERVER_CLIENT
        assert observer.client_for_request.api_key == "sk-user-b-stored-key"
        assert body["message"] == "ok"
        assert body.get("error_type") is None

    def test_control_byoc_header_still_works_1162(self):
        """#1162 no-regress: an explicit per-call header key wins and never touches
        the DB — BYOC works with or without a stored key."""
        client, jwt_service, observer = _client()
        token = _token(jwt_service)

        with _stored_key(None):
            body = _post(
                client,
                {"Authorization": f"Bearer {token}", "X-User-Api-Key": "sk-byoc-header"},
            )

        assert observer.calls == 1
        assert observer.client_for_request.api_key == "sk-byoc-header"
        assert body["message"] == "ok"

    def test_no_regress_1320_anonymous_caller_still_refused(self):
        """#1320 must not regress: no login and no header key → the sign-in-or-bring-a-key
        copy, refused before the LLM, and still not the server's client."""
        client, _, observer = _client()

        with _stored_key(None):
            body = _post(client, {})

        assert body["error_type"] == "anonymous_key_required"
        assert observer.calls == 0
        assert observer.client_for_request is not SERVER_CLIENT
        assert "sign in" in body["message"].lower()
