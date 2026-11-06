"""#2065: Settings link reads "Privacy & data"; /settings/privacy lists only what exists.

Layer: served HTML through the app's TestClient (template render), authenticated.
"""

from __future__ import annotations

import html
import uuid
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

REPO = Path(__file__).resolve().parents[3]

DELETION = (
    "There's no way to delete your account inside Piper yet. We plan to add one. "
    "Until then, email support@pipermorgan.ai and we'll delete your account and "
    "everything in it within 14 days."
)


@pytest.fixture(scope="module")
def client():
    if getattr(app.state, "templates", None) is None:
        from fastapi.templating import Jinja2Templates

        app.state.templates = Jinja2Templates(directory=str(REPO / "templates"))
    c = TestClient(app, follow_redirects=False)
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2065@example.com", scopes=["user"]
    )
    c.cookies.set("auth_token", token)
    return c


def _get(client, path):
    r = client.get(path)
    assert r.status_code == 200, r.status_code
    return html.unescape(r.text)


def test_settings_link_label(client):
    body = _get(client, "/settings")
    assert "Privacy & data" in body
    assert "Export/delete data" not in body
    assert 'href="/settings/privacy"' in body


def test_privacy_page_copy(client):
    body = _get(client, "/settings/privacy")
    assert DELETION in body
    assert "Conversations and todos can't be exported yet" in body
    assert 'href="/privacy"' in body
    assert 'href="/files"' in body and 'href="/learning"' in body
    for gone in (
        "Coming Soon",
        "Request complete data deletion",
        "Export your data in standard formats",
        "Export/delete data",
    ):
        assert gone not in body
