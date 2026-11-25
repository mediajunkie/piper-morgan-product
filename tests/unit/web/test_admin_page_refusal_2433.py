"""Issue 2433: a non-admin who opens an admin-only PAGE gets a page, not raw JSON.

CXO's words (mail 01M87ZZX8Q): ``This page needs an admin account.`` with a link
``Back to Settings``. Arch's shape (mails 01M87ZCEAF, 01M880KDHY): the admin gate's 403
answers ``refusal_page(...)`` when ``wants_a_page(request)`` holds and JSON otherwise;
the link is ``WayOut.SETTINGS``, a member of a closed set.

LAYER: the real ``ui`` router and the app's real ``HTTPException`` handler, on a small
app with a signed-in non-admin. The page's template is never reached (the gate is a
dependency and refuses first). Not a browser render.
DENOMINATOR: every route on ``web.api.routes.ui.router`` that depends on
``require_admin``, read from the router.
"""

import uuid
from html.parser import HTMLParser

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from services.api.refusal_pages import ADMIN_PAGE_NEEDS_ADMIN_LINE, WayOut, refusal_page
from services.auth import auth_middleware
from services.auth.auth_middleware import (
    ADMIN_ACCOUNT_NEEDED_FOR_CONFIG_LINE,
    get_current_user,
    require_admin,
)


def _depends_on_require_admin(dependant) -> bool:
    return any(
        d.call is require_admin or _depends_on_require_admin(d) for d in dependant.dependencies
    )


def _admin_only_page_paths():
    from web.api.routes import ui

    return sorted(
        route.path
        for route in ui.router.routes
        if getattr(route, "dependant", None) is not None
        and "GET" in route.methods
        and _depends_on_require_admin(route.dependant)
    )


class _VisibleText(HTMLParser):
    def __init__(self):
        super().__init__()
        self.words, self.links, self._skip = [], [], 0

    def handle_starttag(self, tag, attrs):
        if tag in ("style", "script", "title"):
            self._skip += 1
        if tag == "a":
            self.links.append(dict(attrs).get("href"))

    def handle_endtag(self, tag):
        if tag in ("style", "script", "title"):
            self._skip -= 1

    def handle_data(self, data):
        if not self._skip and data.strip():
            self.words.append(data.strip())


def _read(body):
    parser = _VisibleText()
    parser.feed(body)
    return parser.words, parser.links


@pytest.fixture()
def client(monkeypatch):
    from web.api.routes import ui
    from web.app import app as real_app

    app = FastAPI()
    for exc_class, handler in real_app.exception_handlers.items():
        app.add_exception_handler(exc_class, handler)
    app.include_router(ui.router)

    class _Claims:
        user_id = uuid.uuid4()

    app.dependency_overrides[get_current_user] = lambda: _Claims()

    async def not_an_admin(user_id):
        return False

    monkeypatch.setattr(auth_middleware, "_user_is_admin", not_an_admin)
    return TestClient(app)


BROWSER = {"Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"}


class TestANonAdminOpeningAnAdminOnlyPage:
    def test_the_router_has_the_two_admin_only_pages(self):
        assert _admin_only_page_paths() == ["/settings/account-flags", "/settings/invites"]

    @pytest.mark.parametrize("path", _admin_only_page_paths())
    def test_a_browser_gets_a_page_with_cxos_line_and_the_way_back(self, client, path):
        reply = client.get(path, headers=BROWSER)
        assert reply.status_code == 403
        assert reply.headers["content-type"].startswith("text/html")
        words, links = _read(reply.text)
        # The whole of what a person reads.
        assert words == ["This page needs an admin account.", "Back to Settings"]
        assert links == ["/settings"]
        assert "Nothing was changed" not in reply.text
        assert "Try again" not in reply.text
        assert "Retry-After" not in reply.headers
        assert not reply.text.lstrip().startswith("{")

    @pytest.mark.parametrize("path", _admin_only_page_paths())
    @pytest.mark.parametrize("accept", ["application/json", "*/*", None])
    def test_a_script_asking_the_same_route_still_gets_the_403_json(self, client, path, accept):
        headers = {"Accept": accept} if accept else {}
        reply = client.get(path, headers=headers)
        assert reply.status_code == 403
        assert reply.json() == {
            "message": ADMIN_ACCOUNT_NEEDED_FOR_CONFIG_LINE,
            "detail": ADMIN_ACCOUNT_NEEDED_FOR_CONFIG_LINE,
        }

    def test_an_api_route_refusing_a_non_admin_browser_keeps_json(self, client):
        # ``wants_a_page`` is False under /api/ whatever the Accept header says.
        from fastapi import Depends

        @client.app.get("/api/v1/admin-only-thing")
        async def thing(admin=Depends(require_admin)):
            return {}

        reply = client.get("/api/v1/admin-only-thing", headers=BROWSER)
        assert reply.status_code == 403
        assert reply.json()["message"] == ADMIN_ACCOUNT_NEEDED_FOR_CONFIG_LINE

    def test_another_marked_403_on_a_page_route_is_not_given_the_admin_page(self, client):
        from fastapi import HTTPException

        from services.api.errors import UserFacingHTTPException
        from services.auth.auth_middleware import OPERATIONS_READERS_ONLY_LINE

        @client.app.get("/some-page")
        async def some_page():
            raise UserFacingHTTPException(status_code=403, detail=OPERATIONS_READERS_ONLY_LINE)

        @client.app.get("/plain-page")
        async def plain_page():
            raise HTTPException(status_code=403, detail=ADMIN_ACCOUNT_NEEDED_FOR_CONFIG_LINE)

        assert client.get("/some-page", headers=BROWSER).json()["message"] == (
            OPERATIONS_READERS_ONLY_LINE
        )
        # An unmarked 403 that happens to carry the same text is not the gate's refusal.
        assert "admin account" not in client.get("/plain-page", headers=BROWSER).text


class TestTheRefusalPagesWayOut:
    def test_the_default_is_the_reload_link_as_before(self):
        page = refusal_page("A line.", 503, 5)
        words, links = _read(page.body.decode())
        assert words == ["A line.", "Try again"]
        assert links == [""]
        assert page.headers["Retry-After"] == "5"

    def test_settings_is_the_way_back(self):
        page = refusal_page(ADMIN_PAGE_NEEDS_ADMIN_LINE, 403, None, way_out=WayOut.SETTINGS)
        words, links = _read(page.body.decode())
        assert words == [ADMIN_PAGE_NEEDS_ADMIN_LINE, "Back to Settings"]
        assert links == ["/settings"]
        assert "retry-after" not in {k.lower() for k in page.headers.keys()}

    @pytest.mark.parametrize("way_out", ["/settings", ("Go", "https://x.example"), None])
    def test_anything_but_a_member_is_refused(self, way_out):
        with pytest.raises(TypeError):
            refusal_page("A line.", 403, None, way_out=way_out)

    def test_no_slot_is_left_in_the_page(self):
        for way in WayOut:
            assert "__PIPER_" not in refusal_page("A line.", 503, 5, way_out=way).body.decode()
