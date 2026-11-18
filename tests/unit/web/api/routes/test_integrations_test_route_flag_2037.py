"""#2037 (Arch, ADR-070 B4/B5): the served GitHub Test route carries the resolver's serving
``leg`` and the stale OAuth ``stale_reason`` as structured fields beside ``message``, so the
page keys its warning on the flag, never on copy. Other integrations (and failures) carry
neither field (None).

The resolver and the one-read probe are stubbed as in
``test_integrations_oauth_test_probe_2012.py``; the route runs in-process via TestClient.
"""

from __future__ import annotations

import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from services.mcp.consumer.connector import DegradationReason, DegradationResponse
from services.mcp.consumer.github_adapter import GitHubCredential, GitHubReposResult
from web.api.routes import integrations
from web.app import app

_ADAPTER = "services.mcp.consumer.github_adapter.GitHubMCPSpatialAdapter"

OAUTH = "GitHub is working, using your GitHub connection."
PAT = "GitHub is working, using your personal token."
STALE = (
    "GitHub is working, using your personal token. "
    "GitHub no longer accepts your connection, so I'm not using it right now."
)


def _credential(leg: str, stale=None) -> GitHubCredential:
    return GitHubCredential(
        owner_id="u1",
        mcp_server_ref="github",
        token="ghp_x" if leg == "pat" else None,
        leg=leg,
        stale_oauth_reason=stale,
    )


def _patched(credential, probe_result):
    return (
        patch(f"{_ADAPTER}.resolve_credential", new=AsyncMock(return_value=credential)),
        patch(f"{_ADAPTER}.search_user_repositories", new=AsyncMock(return_value=probe_result)),
    )


@pytest.fixture
def client():
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2037@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    return c


@pytest.mark.parametrize(
    "credential,message,leg,stale_reason",
    [
        (_credential("oauth"), OAUTH, "oauth", None),
        (_credential("pat"), PAT, "pat", None),
        (_credential("pat", stale=DegradationReason.STALE_TOKEN), STALE, "pat", "stale_token"),
    ],
    ids=["oauth-only", "pat-only", "stale-plus-pat"],
)
def test_github_test_route_returns_leg_and_stale_reason(
    client, credential, message, leg, stale_reason
):
    resolve, probe = _patched(credential, GitHubReposResult(repositories=[{"full_name": "o/r"}]))
    with resolve, probe:
        r = client.post("/api/v1/integrations/test/github")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["success"] is True
    assert body["message"] == message
    assert body["leg"] == leg
    assert body["stale_reason"] == stale_reason


def test_github_failure_carries_no_leg_or_stale_reason(client):
    degraded = DegradationResponse(
        reason=DegradationReason.UNREACHABLE, user_message="down", action_hint=None
    )
    resolve, probe = _patched(_credential("oauth"), GitHubReposResult(degradation=degraded))
    with resolve, probe:
        r = client.post("/api/v1/integrations/test/github")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["success"] is False
    assert body["leg"] is None and body["stale_reason"] is None


def test_other_integrations_carry_no_leg_or_stale_reason(client):
    async def _ok(_name, user_id=None):
        return {"success": True}

    with patch.object(integrations, "_test_integration", new=_ok):
        r = client.post("/api/v1/integrations/test/notion")
    assert r.status_code == 200, r.text
    body = r.json()
    assert body["message"] == "Notion connection successful"
    assert body["leg"] is None and body["stale_reason"] is None
