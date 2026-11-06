"""#2286 (CXO's final words): the GitHub connect card says what GitHub's approval page
will show, before the redirect. A tester on 11-04 read the app owner's name on GitHub's
button as their own account being used.

LAYER (m-43): the REAL ASGI app through a TestClient, real AuthMiddleware and JWT, the
real ``/settings/integrations/github`` route and ``templates/`` on disk (the #1918 render
test's idiom). DENOMINATOR: the rendered card, signed in. Not covered: the client JS
that hides the connect group once connected (it saves and restores the group's HTML
whole, #2287, so the note travels with it).
"""

from __future__ import annotations

import uuid

import pytest
from fastapi.testclient import TestClient

from services.auth.container import AuthContainer
from web.app import app

PAGE_PATH = "/settings/integrations/github"

_WORDS = (
    "GitHub will ask you to approve Piper Morgan. Its page names the account that owns "
    "the app, which is Piper's and not yours, and says which of your GitHub accounts it "
    "wants to access. Check that account is the one you mean. Piper only gets access to "
    "the account you approve there."
)


@pytest.fixture(scope="module")
def client():
    if getattr(app.state, "templates", None) is None:
        from pathlib import Path

        from fastapi.templating import Jinja2Templates

        repo_root = Path(__file__).resolve().parents[3]
        app.state.templates = Jinja2Templates(directory=str(repo_root / "templates"))
    return TestClient(app, follow_redirects=False)


def _body(client) -> str:
    token = AuthContainer.get_jwt_service().generate_access_token(
        user_id=uuid.uuid4(), user_email="u2286@example.com", scopes=["user"]
    )
    client.cookies.set("auth_token", token)
    try:
        r = client.get(PAGE_PATH)
    finally:
        client.cookies.delete("auth_token")
    assert r.status_code == 200, f"{PAGE_PATH} returned {r.status_code}: {r.text[:300]}"
    return r.text


def test_the_card_says_what_githubs_page_will_show(client):
    assert _WORDS in " ".join(_body(client).split())


def test_the_note_sits_inside_the_connect_group_before_the_button(client):
    body = _body(client)
    group = body.index('id="oauth-connect-group"')
    note = body.index('id="oauth-approval-note"')
    button = body.index('id="oauth-connect-btn"')
    assert group < note < button
