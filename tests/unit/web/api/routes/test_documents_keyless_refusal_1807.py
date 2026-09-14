"""#1807 — the /documents LLM routes refuse a keyless caller instead of billing the operator.

#1185 Phase 2 taught these five routes to resolve the caller's key. They then inherited
the #1807 hole wholesale: no stored key ⇒ `None` ⇒ the server's client. Worse than
/intent, in one respect — every one of these routes wraps its body in a broad
`except Exception` that relabels anything raised as a 500 `"<operation> failed"`. A
refusal arriving as a 500 tells the user the server broke, when in fact the server
worked correctly and the remediation is theirs. So the fix here is two things: refuse,
and let the refusal through.

LAYER (m-43). Real ASGI requests through a real `TestClient`, real HS256 token, real
`get_current_user` dependency, real route bodies, real `except` chains. The document
handler is stubbed — and the stub's job is to ask the REAL `anthropic_client_for_request`
which client this request would use, so "the server key was not consumed" is measured at
the selector rather than inferred from a status code.

DENOMINATOR. `analyze` is exercised end-to-end for all four properties. The other four
LLM routes (`question`, `summarize`, `compare`, `reference`) are covered for the refusal
property by parametrized request, since all five now route through the single
`_resolve_key_or_refuse` helper. `search_documents` is not covered: it does not resolve a
key and makes no LLM call.
"""

import contextlib
import uuid
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from services.auth.jwt_service import JWTService
from services.llm.request_key import anthropic_client_for_request
from web.api.routes.documents import router as documents_router

SECRET = "test-secret-1807-documents-not-real"
SERVER_CLIENT = SimpleNamespace(name="THE-SERVERS-OWN-ANTHROPIC-CLIENT")
FILE_ID = "8f14e45f-ceea-467a-9575-8b1e0e0a0a0a"


@contextlib.asynccontextmanager
async def _fake_session():
    yield object()


@contextlib.contextmanager
def _stored_key(value):
    with (
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope",
            lambda *a, **k: _fake_session(),
        ),
        patch(
            "services.database.session_factory.AsyncSessionFactory.session_scope_fresh",
            lambda *a, **k: _fake_session(),
        ),
        patch(
            "services.security.user_api_key_service.UserAPIKeyService.retrieve_user_key",
            AsyncMock(return_value=value),
        ),
    ):
        yield


class _Observer:
    def __init__(self):
        self.calls = 0
        self.client_for_request = None

    async def __call__(self, *args, **kwargs):
        self.calls += 1
        self.client_for_request = anthropic_client_for_request(SERVER_CLIENT)
        return {"summary": "ok", "key_findings": []}


def _client(handler_name: str, observer: _Observer):
    app = FastAPI()
    app.include_router(documents_router)
    jwt_service = JWTService(secret_key=SECRET)
    user_id = uuid.uuid4()
    token = jwt_service.generate_access_token(
        user_id=user_id,
        user_email=f"{user_id}@example.com",
        scopes=["user"],
    )
    return (
        TestClient(app, raise_server_exceptions=False),
        token,
        patch.object(AuthContainer, "_jwt_service", jwt_service),
        patch(f"web.api.routes.documents.{handler_name}", observer),
    )


class TestKeylessCallerIsRefusedNotBilled:
    @pytest.mark.smoke
    def test_no_stored_key_does_not_consume_the_server_key(self):
        """The #1807 property on the REST surface. Pre-fix this returned 200 with the
        analysis, paid for by the operator."""
        observer = _Observer()
        client, token, auth, handler = _client("handle_analyze_document", observer)

        with auth, handler, _stored_key(None):
            response = client.post(
                f"/api/v1/documents/{FILE_ID}/analyze",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert observer.calls == 0, "the handler ran — the request reached the LLM layer"
        assert observer.client_for_request is not SERVER_CLIENT
        assert response.status_code == 403, response.text

    @pytest.mark.smoke
    def test_the_refusal_is_honest_and_not_a_500(self):
        """It must not arrive as `500 Analysis failed` — the broad handler used to
        relabel every raise that way, blaming the server for the caller's missing key."""
        observer = _Observer()
        client, token, auth, handler = _client("handle_analyze_document", observer)

        with auth, handler, _stored_key(None):
            response = client.post(
                f"/api/v1/documents/{FILE_ID}/analyze",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code != 500, response.text
        detail = response.json()["detail"].lower()
        assert "analysis failed" not in detail
        assert "api key" in detail
        assert "add" in detail
        assert "nothing was charged" in detail

    def test_control_a_user_with_a_stored_key_still_works(self):
        observer = _Observer()
        client, token, auth, handler = _client("handle_analyze_document", observer)

        with auth, handler, _stored_key("sk-their-own-key"):
            response = client.post(
                f"/api/v1/documents/{FILE_ID}/analyze",
                headers={"Authorization": f"Bearer {token}"},
            )

        assert response.status_code == 200, response.text
        assert observer.calls == 1
        assert observer.client_for_request is not SERVER_CLIENT
        assert observer.client_for_request.api_key == "sk-their-own-key"

    @pytest.mark.parametrize(
        "handler_name,path,method_kwargs",
        [
            ("handle_question_document", f"/api/v1/documents/{FILE_ID}/question?question=why", {}),
            ("handle_summarize_document", f"/api/v1/documents/{FILE_ID}/summarize", {}),
            (
                "handle_compare_documents",
                "/api/v1/documents/compare",
                {"params": [("file_ids", FILE_ID), ("file_ids", FILE_ID)]},
            ),
            (
                "handle_reference_in_conversation",
                "/api/v1/documents/reference",
                {"json": {"message": "about that doc", "file_id": FILE_ID}},
            ),
        ],
    )
    def test_every_llm_document_route_refuses(self, handler_name, path, method_kwargs):
        """All five share `_resolve_key_or_refuse`, so none of them can drift back to
        the silent fallback independently."""
        observer = _Observer()
        client, token, auth, handler = _client(handler_name, observer)

        with auth, handler, _stored_key(None):
            response = client.post(
                path, headers={"Authorization": f"Bearer {token}"}, **method_kwargs
            )

        assert observer.calls == 0, f"{handler_name} ran despite the caller having no key"
        assert response.status_code == 403, response.text
